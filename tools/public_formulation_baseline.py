#!/usr/bin/env python3
"""Deterministic reference for normalized P1 briefs, not a language model.

This development baseline routes explicitly supplied dataset/target/feature
fields. It neither parses arbitrary business language nor fits causal effects.
Dataset limitations cannot be overridden by an unverified request assertion.
"""
import json
import sys

PRECALL_CANDIDATES = {'age', 'job', 'marital', 'education', 'default', 'housing', 'loan',
                      'previous', 'pdays', 'poutcome'}
POST_OR_UNVERIFIED = {'duration', 'campaign', 'y', 'contact', 'month', 'day_of_week',
                      'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed'}


def formulate(request):
    dataset = request.get('dataset')
    target = request.get('target')
    features = request.get('features', [])
    result = {'status': 'clarify', 'target': None, 'numerical_effect': None,
              'assumptions': [], 'refusals': [], 'alternatives': [], 'verified_causal_truth': False}
    if not isinstance(features, list) or any(not isinstance(f, str) for f in features):
        result['refusals'] = ['features_must_be_named_fields']; return result
    if dataset == '401k' and target == 'eligibility_ate':
        result.update(status='conditional_estimand', target='E[net_tfa(eligible=1)-net_tfa(eligible=0)]',
                      assumptions=['consistency_and_no_interference', 'conditional_exchangeability', 'positivity',
                                   'controls_precede_eligibility', 'iid_working_covariance_not_survey_design'],
                      alternatives=['conditional_observational_contrast', 'confounding_sensitivity'],
                      refusals=['not_participation_ate', 'not_established_bank_transport'])
    elif dataset == '401k' and target == 'participation_late':
        result.update(status='conditional_iv_estimand', target='E[net_tfa(participate=1)-net_tfa(participate=0)|eligibility_complier]',
                      assumptions=['eligibility_relevance', 'conditional_instrument_exogeneity', 'exclusion',
                                   'monotonicity', 'consistency_and_no_interference', 'instrument_positivity',
                                   'controls_precede_eligibility', 'nonzero_first_stage'],
                      alternatives=['participation_ate_requires_distinct_backdoor_assumptions', 'weak_instrument_or_exclusion_sensitivity'],
                      refusals=['not_all_household_participation_ate', 'exclusion_not_verified_by_data'])
    elif dataset == 'uci_bank' and target == 'pre_contact_prediction':
        denied = sorted(set(features) & POST_OR_UNVERIFIED)
        unknown = sorted(set(features) - PRECALL_CANDIDATES - POST_OR_UNVERIFIED)
        if denied or unknown:
            result.update(status='refuse_features', target='P(subscription|verified_pre_contact_features)',
                          refusals=['post_contact_or_unverified_clock:' + f for f in denied] + ['unrecognized_field:' + f for f in unknown],
                          alternatives=['remove_unavailable_fields_and_verify_remaining_clocks'])
        else:
            result.update(status='conditional_prediction', target='P(subscription|verified_pre_contact_features)',
                          assumptions=['candidate_features_available_at_decision_time', 'archive_population_only',
                                       'missing_unknown_categories_retained', 'future_shift_not_established'],
                          refusals=['not_contact_treatment_effect', 'not_randomized_assignment', 'row_split_is_not_customer_split'])
    elif dataset == 'uci_bank' and target in ('contact_ate', 'duration_effect'):
        result.update(status='refuse_causal_identification', target=target,
                      refusals=['no_documented_assignment_and_counterfactual_comparison', 'prediction_does_not_identify_effect'],
                      alternatives=['descriptive_association', 'propose_randomized_contact_design_after_prototype_merit'])
    elif dataset == 'uci_bank' and target == 'post_call_description':
        result.update(status='descriptive_only', target='association_in_archived_contact_records',
                      refusals=['not_pre_call_policy', 'not_treatment_effect'])
    else:
        result['refusals'] = ['specify_population_action_comparator_outcome_and_decision_time']
    return result


if __name__ == '__main__':
    request = json.load(sys.stdin)
    print(json.dumps(formulate(request), indent=2))
