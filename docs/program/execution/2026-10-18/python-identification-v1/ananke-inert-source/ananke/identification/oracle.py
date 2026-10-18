import copy
import functools
import logging
from collections import ChainMap

import numpy as np
from pgmpy.factors.discrete import DiscreteFactor, TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

from ananke.inference.variable_elimination import variable_elimination

from ..graphs import ADMG, DAG

logger = logging.getLogger(__name__)


def compute_effect_from_discrete_model(
    net, treatment_dict, outcome_dict, conditioning_dict=None
):
    """
    Compute the causal effect by directly performing an intervention in a Bayesian
    Network corresponding to the true structural equation model to obtain the
    counterfactual distribution, and then computing the marginal distribution of the outcome.
    Note that this function does not consider issues of identification as
    interventions are performed in the true model (regardless if those
    interventions were identified).

    :param net: A Bayesian Network representing the causal problem. Note that this object is used only as a representation of the observed data distribution.
    :param treatment_dict: Dictionary of treatment variables to treatment values.
    :param outcome_dict: Dictionary of outcome variables to outcome values.
    """

    int_net = copy.deepcopy(net)
    int_net.fix(treatment_dict)

    if conditioning_dict is None:
        truth = variable_elimination(
            int_net, list(outcome_dict.keys())
        ).get_value(**outcome_dict)
    else:
        num = variable_elimination(
            int_net, list(outcome_dict.keys()) + list(conditioning_dict.keys())
        )
        denom = variable_elimination(int_net, list(conditioning_dict.keys()))
        final = num.divide(denom, inplace=False)
        truth = final.get_value(**(outcome_dict | conditioning_dict))

    return truth
