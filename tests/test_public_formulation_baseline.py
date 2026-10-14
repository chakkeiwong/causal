"""Check information leakage and unsupported-causality boundaries, not LLM skill."""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from public_formulation_baseline import formulate


@pytest.mark.parametrize('feature', ['duration', 'campaign', 'y', 'contact', 'euribor3m', 'invented_field'])
def test_unsafe_or_unverified_precontact_features_are_not_admitted(feature):
    result = formulate({'dataset': 'uci_bank', 'target': 'pre_contact_prediction', 'features': ['age', feature]})
    assert result['status'] == 'refuse_features'
    assert result['numerical_effect'] is None


def test_request_claim_cannot_manufacture_randomization():
    result = formulate({'dataset': 'uci_bank', 'target': 'contact_ate', 'randomized': True, 'assumptions_verified': True})
    assert result['status'] == 'refuse_causal_identification'
    assert not result['verified_causal_truth']


def test_eligibility_and_participation_cannot_be_conflated():
    eligibility = formulate({'dataset': '401k', 'target': 'eligibility_ate'})
    participation = formulate({'dataset': '401k', 'target': 'participation_late'})
    assert eligibility['target'] != participation['target']
    assert 'exclusion' in participation['assumptions']
    assert 'not_all_household_participation_ate' in participation['refusals']


def test_clock_safe_fields_do_not_turn_prediction_into_causality():
    result = formulate({'dataset': 'uci_bank', 'target': 'pre_contact_prediction', 'features': ['age', 'job']})
    assert result['status'] == 'conditional_prediction'
    assert 'candidate_features_available_at_decision_time' in result['assumptions']
    assert 'not_contact_treatment_effect' in result['refusals']


def test_ambiguous_question_is_not_silently_resolved():
    result = formulate({'dataset': '401k', 'question': 'How much will retirement saving help?'})
    assert result['status'] == 'clarify' and result['target'] is None
