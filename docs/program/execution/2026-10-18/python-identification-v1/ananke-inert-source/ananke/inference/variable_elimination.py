import functools
import logging

import numpy as np
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference.EliminationOrder import (
    MinFill,
    MinNeighbors,
    MinWeight,
    WeightedMinFill,
)
from pgmpy.models import BayesianNetwork

logger = logging.getLogger(__name__)


def variable_elimination(
    bayesian_network, variables, elimination_order_alg="minfill"
):
    """
    Implements the exact inference variable elimination algorithm to compute marginals of a Bayesian
    Network.

    :param bayesian_network: An ananke.BayesianNetwork representing the graph
    :param variables: A list of variables representing the desired marginal
    :param elimination_order_alg: Name of elimination order algorithm (supplied by
    pgmpy.inference.EliminationOrder)

    """
    elimination_order_algs = {
        "minfill": MinFill,
        "weightedminfill": WeightedMinFill,
        "minweight": MinWeight,
        "minneighbors": MinNeighbors,
    }
    elimination_order = elimination_order_algs.get(elimination_order_alg)
    if elimination_order is None:
        raise ValueError(
            f"Invalid choice of ordering: {elimination_order_alg}. Select one from {list(elimination_order_algs)}"
        )

    # Convert bayesian_network into pgmpy.BayesianNetwork, compute elimination ordering
    pgmpy_network = BayesianNetwork()
    pgmpy_network.add_nodes_from(list(bayesian_network.vertices))
    pgmpy_network.add_edges_from(bayesian_network.di_edges)
    random_cpds = list()

    random_cpds = [
        TabularCPD(
            vertex,
            cpd.variable_card,
            np.random.rand(*cpd.get_values().shape),
            cpd.variables[1:],
            cpd.cardinality[1:],
        )
        for vertex, cpd in bayesian_network.cpds.items()
    ]
    pgmpy_network.add_cpds(*random_cpds)

    ordering = elimination_order(pgmpy_network).get_elimination_order(
        set(bayesian_network.vertices) - set(variables)
    )
    # Create factors from each cpd in bayesian network
    factors = [v.to_factor() for v in bayesian_network.cpds.values()]

    for var in ordering:
        logger.debug(f"eliminating {var}")
        selected_factors = list()
        other_factors = list()
        for factor in factors:

            if var in factor.variables:
                selected_factors.append(factor)
            else:
                other_factors.append(factor)

        tau_factor = functools.reduce(
            lambda x, y: x.product(y, inplace=False), selected_factors
        ).marginalize([var], inplace=False)

        factors = other_factors + [tau_factor]
    final_factor = functools.reduce(
        lambda x, y: x.product(y, inplace=False), factors
    )

    return final_factor
