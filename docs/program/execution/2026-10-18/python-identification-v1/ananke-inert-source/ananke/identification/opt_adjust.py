"""
Optimal adjustment sets finding
"""

import logging
import unittest

import numpy as np

import ananke
from ananke.graphs import ADMG, DAG

logger = logging.getLogger("opt_adjust")


def get_opt_set(G, vertex1, vertex2):

    """
    function to get the optimal set from two vertices

    :param G: the graph
    :param vertex1: inference from vertex1, say treatment
    :param vertex2: inference to vertex2, say outcome

    """

    causal_nodes = [
        item
        for item in G.descendants([vertex1])
        if item in G.ancestors([vertex2])
    ]
    if len(causal_nodes) == 0:
        logger.info("No causal node!")
        return None
    causal_nodes.remove(vertex1)
    forb_set = [item for item in G.descendants(causal_nodes)]
    forb_set = forb_set + [
        vertex1
    ]  # The forbidden set characterizes those covariates that may never be included into a valid adjustment set

    opt_set = [item for item in G.parents(causal_nodes) if item not in forb_set]
    return set(opt_set)


def get_opt_set_from_set(G, node_set1, node_set2):

    """
    function to get the optimal set from two vertices sets

    :param G: the graph
    :param node_set1: set of inference from
    :param node_set2: set of inference to

    """

    causal_nodes = [
        item
        for item in G.descendants(node_set1)
        if item in G.ancestors(node_set2)
    ]
    causal_nodes.remove(node_set1)
    forb_set = [item for item in G.descendants(causal_nodes)]
    forb_set = forb_set + [node_set1]
    input_set = [item for item in G.vertices if item not in forb_set]
    for element in input_set:
        new_set = [item for item in input_set if item not in element]
        condition_set = new_set + [vertex1]
        flag_new_set = G.d_separated(
            element, node_set2, condition_set
        )  # check if d-separated
        if flag_new_set:
            input_set = new_set
    return set(input_set)


def get_min_set(G, input, vertex1, vertex2):

    """
    function for minimal set

    :param G: DAG
    :param input: optimal set found using get_opt_set function
    :param vertex1: inference from vertex1, say treatment
    :param vertex2: inference to vertex2, say outcome

    """

    if len(input) == 0:
        logger.info("Adjustment set is empty!")
        return

    input_set = [item for item in input]

    is_minimal_set = 0  # flag for the minimal set

    for element in G.children(
        [vertex1]
    ):  # prepare for d-separation test, construct a SWIG
        G.delete_diedge(vertex1, element)

    for element in input_set:
        new_set = [item for item in input_set if item not in element]
        is_d_separated = G.d_separated(
            vertex1, vertex2, new_set
        )  # check if d-separated
        if is_d_separated:
            is_minimal_set = 1
            final_set = get_min_set(G, new_set, vertex1, vertex2)

    if not is_minimal_set:
        # input set is minimal set
        return set(input_set)

    return set(final_set)


class OptAdjustment:
    def __init__(self, graph):
        self.graph = graph

    def generate_opt_adjustment_set(self, vertex1, vertex2):

        """
        Fits the binary nested model. Let N the number of observations, M the number of variables.

        :param self: DAG
        :param vertex1: inference from vertex1, say treatment
        :param vertex2: inference to vertex2, say outcome

        """

        model = self.graph

        if type(model) == ADMG:
            logger.info("Found ADMG graph, not applicable")
            return None

        is_d_separated = model.d_separated(vertex1, vertex2, [])

        if is_d_separated:
            logger.info(
                "Tested vertices are independent so no set is needed to condition on"
            )
            return []

        opt_set = get_opt_set(model, vertex1, vertex2)

        if opt_set == None:
            logger.info("No adjustment set!")
            return None

        result = get_min_set(model, opt_set, vertex1, vertex2)

        return result
