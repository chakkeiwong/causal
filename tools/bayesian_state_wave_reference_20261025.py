#!/usr/bin/env python3
"""Exact authored proposal witnesses; never execute downloaded implementations."""
from fractions import Fraction as F
import json


def calculate():
    prior = F(1, 2)
    filter_one = prior * F(3, 4) / F(1, 2)
    smooth_one = (prior * F(3, 4) ** 2) / (
        prior * F(3, 4) ** 2 + prior * F(1, 4) ** 2
    )
    value = lambda p: p * 100 - (1 - p) * 400
    energies = [F(0), F(10), F(0), F(10)]
    mean = sum(energies) / len(energies)
    variance = sum((e - mean) ** 2 for e in energies) / (len(energies) - 1)
    successive = sum((b - a) ** 2 for a, b in zip(energies, energies[1:]))
    ratio_increment = successive / len(energies) / variance
    ratio_dimension = 1 / variance
    a, b = F(8), F(7)
    post_mean = a / (a + b)
    post_var = a * b / ((a + b) ** 2 * (a + b + 1))
    mixture_var = 2 * a * b * (a + b + 2) / ((a + b) ** 2 * (a + b + 1))
    fixed_var = 2 * post_mean * (1 - post_mean)
    retained_indices = list(range(0, 11 - 2, 4))
    weights = [F(9, 10), F(1, 10)]
    ess = 1 / sum(w * w for w in weights)
    return dict(
        kind="authored_exact_laws_not_native_execution",
        observational_equivalence=dict(
            prior_odds="3/2", likelihood_ratio="1", posterior_odds="3/2",
            intervention_effects=[1, 0], posterior_effect_mean="3/5",
        ),
        filtering_smoothing=dict(
            persistent_binary_state=True, emission_accuracy="3/4",
            filter_t1=str(filter_one), smooth_t1_given_second_positive=str(smooth_one),
            current_action_value_usd=str(value(filter_one)),
            future_informed_value_usd=str(value(smooth_one)),
            current_information_action="decline", future_informed_action="act",
            hypothetical_10000_account_loss_usd=str(-10000 * value(filter_one)),
        ),
        beta_reference=dict(prior=[2, 3], successes=6, failures=4,
            posterior=[8, 7], mean=str(post_mean), variance=str(post_var),
            two_trial_predictive_variance=str(mixture_var),
            fixed_probability_variance=str(fixed_var),
            omitted_parameter_variance=str(mixture_var - fixed_var)),
        energy_diagnostics=dict(energies=[0, 10, 0, 10], sample_variance=str(variance),
            dimension_based_ratio=str(ratio_dimension), increment_based_ratio=str(ratio_increment),
            threshold="1/5", dimension_flags=ratio_dimension < F(1, 5),
            increment_flags=ratio_increment < F(1, 5)),
        sample_accounting=dict(total_transitions=11, dropped=2, thinning=4,
            retained_zero_based_indices=retained_indices, ceiling_count=len(retained_indices),
            floor_count=(11 - 2) // 4),
        importance=dict(weights=[str(x) for x in weights], ess=str(ess),
            uniform_two_particle_ess=2, duplicate_particles_distinct_ancestors=1),
        normalization=dict(unnormalized_evidence_estimates=[str(F(1, 2)), str(F(3, 2))],
            mean_estimate="1", mean_log="log(3/4)/2", log_mean="0"),
        omitted_mode=dict(true_equal_mixture_mean="0", retained_positive_mode_mean="10",
            native_failure_observed=False),
        native_execution=False,
    )


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2))
