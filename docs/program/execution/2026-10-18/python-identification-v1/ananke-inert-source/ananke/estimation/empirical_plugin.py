import functools
import logging
from collections import ChainMap

from pgmpy.factors.discrete import DiscreteFactor, TabularCPD

from ananke.inference.variable_elimination import variable_elimination

from ..graphs import ADMG, DAG

logger = logging.getLogger(__name__)


def compute_district_factor(graph: ADMG, obs_dist, fixing_order):
    """
    Compute the interventional distribution associated with a district (or equivalently, its fixing order)

    :param graph: Graph representing the problem
    :type graph: ananke.ADMG
    :param obs_dist: Probability distribution corresponding to the graph
    :type obs_dist: pgmpy.discrete.DiscreteFactor
    :param fixing_order: A fixing sequence for the implied district D
    """
    new_graph = graph.copy()
    curr_factor = obs_dist

    logger.info(
        f"implied district is {set(graph.vertices) - set(fixing_order)}"
    )

    for var in fixing_order:
        non_descendants = list(
            set(new_graph.vertices) - set(new_graph.descendants(var))
        )
        logger.info(f"fixing by q({var}|{', '.join(non_descendants)})")
        div_joint = curr_factor.marginalize(
            set(new_graph.descendants(var)) - {var}, inplace=False
        )
        if non_descendants:
            div_cond = div_joint.marginalize([var], inplace=False)
            div_factor = div_joint.divide(div_cond, inplace=False)
        else:
            div_factor = div_joint
        new_graph = new_graph.fix(var)

        curr_factor = curr_factor.divide(div_factor, inplace=False)

    return curr_factor


def get_obs_dist_from_net(net, graph):
    return variable_elimination(net, graph.vertices)


def estimate_effect_from_discrete_dist(
    oid, obs_dist, treatment_dict, outcome_dict
):
    """
    Performs the ID algorithm to identify a causal effect given a discrete
    probability distribution representing the observed data distribution.


    :param oid: Ananke OneLineID object
    :type oid: OneLineID
    :param obs_dist: observed data distribution
    :param treatment_dict: dictionary of treatment variables and values
    :param outcome_dict: dictionary of outcome variables and values
    """
    if not oid.id():
        return None

    factors = list()
    for district in sorted(oid.Gystar.districts):
        fixing_order = oid.fixing_orders[tuple(district)]
        factors.append(
            compute_district_factor(oid.graph, obs_dist, fixing_order)
        )

    intervened_distribution = functools.reduce(
        (lambda first, last: first.product(last, inplace=False)), factors
    )

    # construct the variable tuples here using itertools.product (Y* - Y) with A = a
    summed_vars = oid.ystar - set(outcome_dict)

    # compute the causal effect

    causal_effect = intervened_distribution.marginalize(
        summed_vars, inplace=False
    ).get_value(**dict(ChainMap(treatment_dict, outcome_dict)))

    return causal_effect
