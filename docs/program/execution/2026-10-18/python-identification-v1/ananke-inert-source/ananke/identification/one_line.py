"""
Class for one line ID algorithms.
"""

import copy
import functools
import itertools
import logging
import math
import os
from collections import ChainMap, namedtuple
from typing import Dict, List, NamedTuple, Union

import numpy as np
import pgmpy
import sympy as sp
from pgmpy.factors.discrete import DiscreteFactor, TabularCPD
from pgmpy.inference import VariableElimination

from ..factors import SymCPD, SymDiscreteFactor
from ..graphs import DAG, Vertex
from ..inference.variable_elimination import variable_elimination
from ..models import bayesian_network
from ..models.bayesian_network import BayesianNetwork, intervene

logger = logging.getLogger(__name__)


class NotIdentifiedError(Exception):
    """
    Custom error for when desired functional is not identified.
    """

    pass


class OneLineID:
    def __init__(self, graph, treatments, outcomes):
        """
        Applies the ID algorithm (Shpitser and Pearl, 2006) reformulated in a 'one-line' fashion (Richardson et al., 2017).

        :param graph: Graph on which the query will run.
        :param treatments: iterable of names of variables being intervened on.
        :param outcomes: iterable of names of variables whose outcomes we are interested in.
        """

        self.graph = graph
        self.treatments = [A for A in treatments]
        self.outcomes = [Y for Y in outcomes]
        self.swig = copy.deepcopy(graph)
        self.swig.fix(self.treatments)
        self.ystar = {
            v
            for v in self.swig.ancestors(self.outcomes)
            if not self.swig.vertices[v].fixed
        }
        self.Gystar = self.graph.subgraph(self.ystar)
        # dictionary mapping the fixing order for each p(D | do(V\D) )
        self.fixing_orders = {}

    def draw_swig(self, direction=None):
        """
        Draw the proper SWIG corresponding to the causal query.

        :return: dot language representation of the SWIG.
        """

        swig = copy.deepcopy(self.graph)

        # add fixed vertices for each intervention
        for A in self.treatments:

            fixed_vertex_name = A.lower()
            swig.add_vertex(fixed_vertex_name)
            swig.vertices[fixed_vertex_name].fixed = True

            # delete all outgoing edges from random vertex
            # and give it to the fixed vertex
            for edge in swig.di_edges:
                if edge[0] == A:
                    swig.delete_diedge(edge[0], edge[1])
                    swig.add_diedge(fixed_vertex_name, edge[1])

            # finally, add a fake edge between interventions and fixed vertices
            # just for nicer visualization
            swig.add_diedge(A, A.lower())

        return swig.draw(direction)

    def id(self):
        """
        Run one line ID for the query.

        :return: boolean that is True if p(Y(a)) is ID, else False.
        """

        self.fixing_orders = {}
        vertices = set(self.graph.vertices)

        # check if each p(D | do(V\D) ) corresponding to districts in Gystar is ID
        for district in self.Gystar.districts:

            fixable, order = self.graph.fixable(vertices - district)

            # if any piece is not ID, return not ID
            if not fixable:
                return False

            self.fixing_orders[tuple(district)] = order

        return True

    # TODO try to reduce functional
    def functional(self):
        """
        Creates and returns a string for identifying functional.

        :return: string representing the identifying functional.
        """

        if not self.id():
            raise NotIdentifiedError

        # create and return the functional
        functional = "" if set(self.ystar) == set(self.outcomes) else "\u03A3"

        for y in self.ystar:
            if y not in self.outcomes:
                functional += y
        if len(self.ystar) > 1:
            functional += " "

        print(self.fixing_orders)
        for district in sorted(list(self.fixing_orders)):
            functional += (
                "\u03A6"
                + "".join(reversed(self.fixing_orders[district]))
                + "(p(V);G) "
            )
        return functional

    # TODO export intermediate CADMGs for visualization
    def export_intermediates(self, folder="intermediates"):
        """
        Export intermediate CADMGs obtained during fixing.

        :param folder: string specifying path to folder where the files will be written.
        :return: None.
        """

        # make the folder if it doesn't exist
        if not os.path.exists(folder):
            os.mkdir(folder)

        # clear the directory
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        # do the fixings and render intermediate CADMGs
        for district in self.fixing_orders:

            G = copy.deepcopy(self.graph)

            fixed_vars = ""
            dis_name = "".join(district)

            for v in self.fixing_orders[district]:
                fixed_vars += v
                G.fix(v)
                G.draw().render(
                    os.path.join(
                        folder, "phi" + fixed_vars + "_dis" + dis_name + ".pdf"
                    )
                )


def get_required_intrinsic_sets(admg):
    required_intrinsic_sets, _ = admg.get_intrinsic_sets()
    return required_intrinsic_sets


def get_allowed_intrinsic_sets(experiments):
    allowed_intrinsic_sets = set()
    allowed_intrinsic_dict = dict()
    fixing_orders = dict()
    for index, experiment in enumerate(experiments):
        intrinsic_sets, order_dict = experiment.get_intrinsic_sets()
        allowed_intrinsic_sets.update(intrinsic_sets)
        fixing_orders[index] = order_dict
        for s in intrinsic_sets:
            allowed_intrinsic_dict[frozenset(s)] = index
    return allowed_intrinsic_sets, allowed_intrinsic_dict, fixing_orders


def check_experiments_ancestral(admg, experiments):
    """
    Check that each experiment G(S(b_i)) is ancestral in ADMG G(V(b_i))
    https://simpleflying.com/

    :param admg: An ADMG
    :param experiments: A list of ADMGs representing experiments
    :return:
    """
    for experiment in experiments:
        graph = copy.deepcopy(admg)
        fixed = experiment.fixed
        graph.fix(fixed)
        if not experiment.is_ancestral_subgraph(admg):
            return False

    return True


def check_experiments_conform_to_gid(admg, experiments):
    graph = copy.deepcopy(admg)
    for experiment in experiments:
        if set(graph.vertices) != set(experiment.vertices):
            return False
    return True


class OneLineAID:
    def __init__(self, graph, treatments, outcomes):
        """
        Applies the one-line AID algorithm.

        :param graph: Graph on which the query will be run
        :param treatments: Iterable of treatment variables
        :param outcomes: Iterable of outcome variables
        """
        self.graph = graph
        self.treatments = treatments
        self.outcomes = outcomes
        self.swig = copy.deepcopy(graph)
        self.swig.fix(self.treatments)
        self.ystar = {
            v
            for v in self.swig.ancestors(self.outcomes)
            if not self.swig.vertices[v].fixed
        }
        self.Gystar = self.graph.subgraph(self.ystar)

        self.checked_id = False

    def id(self, experiments):
        """
        Checks if identification query is identified given the set of experimental distributions.

        :param experiments: a list of ADMG objects in which intervened variables are fixed.
        """
        if not check_experiments_ancestral(
            admg=self.graph, experiments=experiments
        ):

            raise NotIdentifiedError

        return self._id(experiments)

    def _id(self, experiments):
        self.required_intrinsic_sets = get_required_intrinsic_sets(
            admg=self.Gystar
        )
        (
            self.allowed_intrinsic_sets,
            self.allowed_intrinsic_dict,
            self.fixing_orders,
        ) = get_allowed_intrinsic_sets(experiments=experiments)

        is_id = False
        if self.allowed_intrinsic_sets >= self.required_intrinsic_sets:
            is_id = True

        self.checked_id = True

        return is_id

    def functional(self, experiments):
        """
        Creates a string representing the identifying functional

        :param experiments: A list of sets denoting the interventions of the available experimental distributions
        :return:
        """
        # if not check_experiments_ancestral(admg=self.graph, experiments=experiments):
        #    raise NotIdentifiedError
        if not self.id(experiments=experiments):
            raise NotIdentifiedError

        # create and return the functional
        functional = "" if set(self.ystar) == set(self.outcomes) else "\u03A3"

        for y in self.ystar:
            if y not in self.outcomes:
                functional += y
        if len(self.ystar) > 1:
            functional += " "

        # guarantee a deterministic printing order
        fixing = []
        intrinsic_sets = []
        for intrinsic_set in self.required_intrinsic_sets:
            fixed = experiments[
                self.allowed_intrinsic_dict[intrinsic_set]
            ].fixed
            fixing.append(list(fixed))
            intrinsic_sets.append(intrinsic_set)

        sorted_intrinsic_sets = sorted(
            intrinsic_sets, key=dict(zip(intrinsic_sets, fixing)).get
        )
        sorted_fixing = sorted(fixing)

        for i, intrinsic_set in enumerate(sorted_intrinsic_sets):
            fixed = sorted_fixing[i]
            vars = sorted(
                set(
                    [
                        v
                        for v in experiments[
                            self.allowed_intrinsic_dict[intrinsic_set]
                        ].vertices
                    ]
                )
                - set(fixed)
            )
            correct_order = self.fixing_orders[
                self.allowed_intrinsic_dict[intrinsic_set]
            ][frozenset(intrinsic_set) - frozenset(fixed)]
            if len(correct_order):
                functional += "\u03A6" + ",".join(reversed(correct_order))
            functional += " p({0} | do({1}))".format(
                ",".join(vars), ",".join(fixed)
            )

        return functional


class OneLineGID(OneLineAID):
    def __init__(self, graph, treatments, outcomes):
        """
        Applies the naive one-line GID algorithm.

        :param graph: Graph on which the query will be run.
        :param interventions: Iterable of treatment variables.
        :param outcomes: Iterable of outcome variables.
        """
        super().__init__(graph, treatments, outcomes)

    def id(self, experiments=list()):
        """
        Checks if identification query is identified given the set of experimental distributions.

        :param experiments: A list of ADMG objects denoting the interventions of the available experimental distributions.
        :return: boolean indicating if query is ID or not.
        """
        if not check_experiments_conform_to_gid(
            admg=self.graph, experiments=experiments
        ):

            raise NotIdentifiedError

        return self._id(experiments)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


def _assert_valid_ananke_witness(
    net_1, net_2, observed_variables, treatment_dict, outcome_variables
):
    marginal_1 = variable_elimination(net_1, observed_variables)
    marginal_2 = variable_elimination(net_2, observed_variables)

    for v in observed_variables:
        assert net_1.vertices[v].cardinality == net_2.vertices[v].cardinality

    for val in itertools.product(
        *[range(net_1.vertices[v].cardinality) for v in observed_variables]
    ):
        val_dict = dict(zip(observed_variables, val))
        if isinstance(marginal_1, SymDiscreteFactor):
            val1 = marginal_1.get_value(**val_dict)
            val2 = marginal_2.get_value(**val_dict)
            logger.debug(f"{val_dict}, {val1}, {val2}")

            assert (
                sp.simplify(val1 - val2) == 0
            ), f"Observed distributions disagree for {val_dict}: {val1} != {val2}"
        elif isinstance(marginal_1, DiscreteFactor):
            val_dict = dict(zip(observed_variables, val))
            val1 = marginal_1.get_value(**val_dict)
            val2 = marginal_2.get_value(**val_dict)
            logger.debug(f"{val_dict}, {val1}, {val2}")

            assert math.isclose(
                val1, val2
            ), f"Observed distributions disagree for {val_dict}: {val1} != {val2}"

    intervened_marginal_1 = variable_elimination(
        copy.deepcopy(net_1).fix(treatment_dict), outcome_variables
    )
    intervened_marginal_2 = variable_elimination(
        copy.deepcopy(net_2).fix(treatment_dict), outcome_variables
    )
    diff = list()
    for val in itertools.product(
        *[range(net_1.vertices[v].cardinality) for v in outcome_variables]
    ):
        val_dict = dict(zip(outcome_variables, val))
        diff.append(
            intervened_marginal_1.get_value(**val_dict)
            - intervened_marginal_2.get_value(**val_dict)
        )

    assert diff != [0] * len(
        diff
    ), "Counterfactual distributions agree between models"


def _assert_valid_pgmpy_witness(
    net_1, net_2, observed_variables, treatment_dict, outcome_variables
):
    inference_1 = VariableElimination(net_1)
    inference_2 = VariableElimination(net_2)
    marginal_1 = inference_1.query(observed_variables)
    marginal_2 = inference_2.query(observed_variables)

    for v in observed_variables:
        assert net_1.get_cardinality(v) == net_2.get_cardinality(v)

    for val in itertools.product(
        *[range(net_1.get_cardinality(v)) for v in observed_variables]
    ):
        val_dict = dict(zip(observed_variables, val))
        val1 = marginal_1.get_value(**val_dict)
        val2 = marginal_2.get_value(**val_dict)
        logger.debug(f"{val_dict}, {val1}, {val2}")

        assert math.isclose(
            val1, val2
        ), f"Observed distributions disagree for {val_dict}: {val1} != {val2}"

    intervened_net_1 = intervene(net_1, treatment_dict)
    intervened_net_2 = intervene(net_2, treatment_dict)
    intervened_inference_1 = VariableElimination(intervened_net_1)
    intervened_inference_2 = VariableElimination(intervened_net_2)
    intervened_marginal_1 = intervened_inference_1.query(outcome_variables)
    intervened_marginal_2 = intervened_inference_2.query(outcome_variables)

    m1 = list()
    m2 = list()
    for val in itertools.product(
        *[range(net_1.get_cardinality(v)) for v in outcome_variables]
    ):
        val_dict = dict(zip(outcome_variables, val))
        m1.append(intervened_marginal_1.get_value(**val_dict))
        m2.append(intervened_marginal_2.get_value(**val_dict))

    assert m1 != m2, "Counterfactual distributions agree between models"


def assert_valid_witness(
    net_1: Union[
        pgmpy.models.BayesianNetwork, bayesian_network.BayesianNetwork
    ],
    net_2: Union[
        pgmpy.models.BayesianNetwork, bayesian_network.BayesianNetwork
    ],
    observed_variables: list,
    treatment_dict: dict,
    outcome_variables=None,
):
    """
    Asserts that two BayesianNetwork objects represent a valid witness for identification, meaning
    that the two Bayesian networks agree on the marginal distribution over `observed_variables` but disagree in
    at least one part of the counterfactual distribution for `outcome_variables` under the
    intervention specified by `treatment_dict`.

    :param net_1: The first BayesianNetwork object
    :param net_2: The second BayesianNetwork object
    :param observed_variables: A list of variables for the observed margin
    :param treatment_dict: A dictionary of treatment variables and values
    :param outcome_variables: An optional list of outcome variables. If left unspecified, then it is
    all variables in `observed_variables` except those in `treatment_dict`.
    """

    if outcome_variables is None:
        outcome_variables = [
            v for v in observed_variables if v not in treatment_dict
        ]
    if isinstance(net_1, pgmpy.models.BayesianNetwork) and isinstance(
        net_2, pgmpy.models.BayesianNetwork
    ):
        _assert_valid_pgmpy_witness(
            net_1, net_2, observed_variables, treatment_dict, outcome_variables
        )
    elif isinstance(net_1, bayesian_network.BayesianNetwork) and isinstance(
        net_2, bayesian_network.BayesianNetwork
    ):
        _assert_valid_ananke_witness(
            net_1, net_2, observed_variables, treatment_dict, outcome_variables
        )
    else:
        raise ValueError("Mismatched or unrecognized Bayesian Network objects")
