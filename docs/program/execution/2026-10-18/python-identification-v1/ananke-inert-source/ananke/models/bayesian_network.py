import copy
import itertools
from typing import Dict, List, Union

import numpy as np
import pgmpy
import sympy as sp
from pgmpy.factors.discrete import TabularCPD

from ..factors import SymCPD
from ..graphs import DAG


class BayesianNetwork(DAG):
    def __init__(self, graph: DAG, cpds: Dict[str, Union[TabularCPD, SymCPD]]):
        """
        A discrete variable Bayesian Network. This is implemented as an augmented
        ananke.graphs.DAG.


        :param graph: A DAG
        :param cpds: A dictionary of vertex names to CPDs. This implementation supports both
        pgmpy's TabularCPD (numpy-backed) as well as ananke's SymCPD (sympy-backed).

        """
        # TODO: raise error if ADMG not DAG

        self.cpds = cpds  # vertex: CPD

        super().__init__(vertices=graph.vertices, di_edges=graph.di_edges)

    def fix(self, variables: List[str]):
        """
        Performs an intervention by setting the conditional distribution of each intervened variable
        to be a point mass at the intervened value. This is a faithful operation (the graph is
        changed and the associated CPD structure reflects the lack of parents).

        """
        super().fix(list(variables))
        if isinstance(variables, dict):
            for vertex, value in variables.items():
                old_cpd = self.cpds[vertex]
                new_values = np.zeros((old_cpd.variable_card, 1))
                new_values[value, :] = 1
                if isinstance(old_cpd.values, np.ndarray):

                    new_cpd = old_cpd.__class__(
                        variable=vertex,
                        variable_card=old_cpd.variable_card,
                        values=np.array(new_values),
                    )
                else:
                    new_cpd = old_cpd.__class__(
                        variable=vertex,
                        variable_card=old_cpd.variable_card,
                        values=old_cpd.values.__class__(new_values),
                    )

                self.cpds[vertex] = new_cpd

        return self

    def copy(self):
        return copy.deepcopy(self)

    def get_cpds(self, vertex):
        return self.cpds[vertex]

    def to_pgmpy(self):
        """
        Converts into pgmpy.models.BayesianNetwork object.
        """
        from pgmpy.models import BayesianNetwork as PgmpyBayesianNetwork

        net = PgmpyBayesianNetwork()
        net.add_nodes_from(self.vertices)
        net.add_edges_from(self.di_edges)

        cpds = [
            x if isinstance(x, TabularCPD) else x.to_pgmpy()
            for x in self.cpds.values()
        ]

        net.add_cpds(*cpds)
        return net


def create_symbolic_cpds(ls_dag, use_uniform_unobs_var=True):
    if hasattr(ls_dag, "get_cards_dict"):
        cards = ls_dag.get_cards_dict()
    else:
        cards = {v.name: v.cardinality for v in ls_dag.vertices.values()}
    if hasattr(ls_dag, "context_variable"):
        context_variable = ls_dag.context_variable
        contexts = ls_dag.contexts
    else:
        context_variable = None
        contexts = None

    all_vars = list()
    cpds = dict()
    for vertex in ls_dag.vertices:
        vertex_vars = []
        param_counter = 1
        relevant_vars = sorted(
            list(ls_dag.parents(vertex))
        )  # some subset of all vars not including v
        fn_map = dict()

        for i, e in enumerate(
            itertools.product(*[range(cards[x]) for x in relevant_vars])
        ):
            for j in range(cards[vertex] - 1):
                # In this if statement, check if intervention occurred
                val_dict = dict(zip(relevant_vars + [vertex], e + (j,)))
                values = e + (j,)
                if use_uniform_unobs_var:
                    if vertex.startswith("U"):
                        fn_map[values] = sp.Rational(1, cards[vertex])
                        continue

                if (
                    context_variable in val_dict
                    and context_variable is not None
                ):
                    current_context = list(contexts)[val_dict[context_variable]]
                    if vertex in current_context:
                        current_ix = current_context.index(vertex)
                        prob = list(contexts.values())[
                            val_dict[context_variable]
                        ][current_ix][j]
                        fn_map[values] = sp.Rational(prob)
                        continue
                if e:

                    symbol = sp.Symbol(
                        f"q_{vertex}_{j}_{''.join([str(x) for x in e])}"
                    )
                else:
                    symbol = sp.Symbol(f"q_{vertex}_{j}")

                fn_map[values] = symbol
                all_vars.append(symbol)
                param_counter += 1

        def func(
            vars,
            relevant_vars=relevant_vars,
            fn_map=fn_map,
            func_var=vertex,
            cards=cards,
        ):
            fn_tuple = tuple([vars[x] for x in relevant_vars + [func_var]])

            if vars[func_var] == cards[func_var] - 1:

                all_fn_tuples = [
                    tuple(
                        [
                            vars[x] if x != func_var else i
                            for x in relevant_vars + [func_var]
                        ]
                    )
                    for i in range(cards[func_var] - 1)
                ]
                return 1 - sum([fn_map[tup] for tup in all_fn_tuples])

            else:
                return fn_map[fn_tuple]

        final_values = sp.Array(
            [
                [
                    func(dict(zip(relevant_vars, e)) | {vertex: i})
                    for e in itertools.product(
                        *[range(cards[x]) for x in relevant_vars]
                    )
                ]
                for i in range(cards[vertex])
            ]
        )
        if relevant_vars:
            cpd = SymCPD(
                variable=vertex,
                variable_card=cards[vertex],
                values=final_values,
                evidence=relevant_vars,
                evidence_card=[cards[v] for v in relevant_vars],
            )
        else:
            cpd = SymCPD(
                variable=vertex,
                variable_card=cards[vertex],
                values=final_values,
            )

        cpds[vertex] = cpd

    return cpds, all_vars


def generate_random_cpds(graph, dir_conc=10, context_variable="S", seed=42):
    """
    Given a graph and a set of cardinalities for variables in a DAG, constructs random conditional probability distributions. Supports optional contexts and context variable to generate CPDs consistent with a context specific DAG for data fusion.

    :param graph: A graph whose variables have cardinalities, and optionally
    :type Graph: DAG, ADMG, LSADMG
    :param dir_conc: The Dirichlet concetration parameter
    :param context_variable: Name of the context variable
    """
    rng = np.random.default_rng(seed=seed)

    cpds = dict()
    cards = {v: graph.vertices[v].cardinality for v in graph.vertices}
    for k, v in cards.items():
        if v is None:
            raise ValueError(
                "Invalid cardinality provided for vertex {}".format(k)
            )
    if hasattr(graph, "contexts"):
        contexts = list(graph.contexts.keys())
        context_distributions = list(graph.contexts.values())
    else:
        contexts = None

    for vertex in sorted(graph.vertices):
        parents = sorted(list(graph.parents(vertex)))

        if context_variable not in parents or contexts is None:
            if not graph.parents(vertex):
                values = rng.dirichlet(
                    cards[vertex] * [dir_conc],
                    1,
                ).T
                cpd = TabularCPD(
                    variable=vertex, variable_card=cards[vertex], values=values
                )

            else:
                values = rng.dirichlet(
                    cards[vertex] * [dir_conc],
                    np.prod([cards[x] for x in parents]),
                ).T

                cpd = TabularCPD(
                    variable=vertex,
                    variable_card=cards[vertex],
                    values=values,
                    evidence=parents,
                    evidence_card=[cards[x] for x in parents],
                )

        else:
            no_s_parents = parents.copy()
            no_s_parents.remove(context_variable)
            no_s_parents = list(no_s_parents)
            reordered_parents = [context_variable] + no_s_parents
            s_specific_values = rng.dirichlet(
                cards[vertex] * [dir_conc],
                int(np.prod([cards[x] for x in no_s_parents])),
            ).T
            values = []
            for i, context in enumerate(contexts):
                if vertex in set(context):
                    ix = context.index(vertex)
                    distribution = context_distributions[i][ix]
                    intervened_values = np.tile(
                        distribution,
                        (np.prod([cards[x] for x in no_s_parents]), 1),
                    ).T
                    values.append(intervened_values)
                else:
                    values.append(s_specific_values)
            values = np.hstack(values)
            cpd = TabularCPD(
                variable=vertex,
                variable_card=cards[vertex],
                values=values,
                evidence=reordered_parents,
                evidence_card=[cards[x] for x in reordered_parents],
            )

        cpds[vertex] = cpd

    return cpds


def intervene(net, treatment_dict):
    """
    Performs an intervention on a pgmpy.models.BayesianNetwork, by setting the conditional distribution of
    each intervened variable to be a point mass at the intervened value. Does not alter the structure of the parents of the network (i.e. is a non-faithful operation).

    If you have an ananke.models.BayesianNetwork, consider using the .fix(treatment_dict) method
    instead, which has the further advantage of performing the operation faithfully (the underlying
    DAG is modified accordingly, and the parents of the intervened variables
    in that conditional probability distributions are removed).


    :param net: pgmpy.models.Bayesian Network
    :type net: pgmpy.models.BayesianNetwork
    :param treatment_dict: dictionary of variables to values:
    :type treatment_dict: dict
    """
    net_copy = net.copy()

    for vertex, value in treatment_dict.items():
        old_cpd = net_copy.get_cpds(vertex)
        old_values = old_cpd.get_values()
        new_values = np.zeros(old_values.shape)
        new_values[value, :] = 1
        new_cpd = TabularCPD(
            variable=vertex,
            variable_card=old_cpd.variable_card,
            values=new_values,
            evidence=old_cpd.variables[1:],
            evidence_card=old_cpd.cardinality[1:],
        )
        net_copy.add_cpds(new_cpd)

    return net_copy
