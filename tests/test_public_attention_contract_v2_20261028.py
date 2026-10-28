"""Adversarial scientific contract checks for proposal-owned graph fixtures."""
from dataclasses import fields, replace
from fractions import Fraction
import hashlib
import importlib.util
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('public_attention_v2', ROOT / 'tools/public_attention_contract_v2_20261028.py')
contract = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = contract
SPEC.loader.exec_module(contract)
EDGE = frozenset({('a', 'b')})
REVERSE = frozenset({('b', 'a')})


def cases():
    return [contract.CaseRef(key, 'graph-' + key, hashlib.sha256(key.encode()).hexdigest(), split)
            for key, split in [('t', 'training'), ('v', 'validation'),
                               ('e1', 'evaluation'), ('e2', 'evaluation')]]


def inputs():
    reg = contract.registry(cases(), {'a', 'b'})
    valid = contract.truth_view(reg, 'validation', {'v': EDGE})
    heldout = contract.truth_view(reg, 'evaluation', {'e1': EDGE, 'e2': REVERSE})
    candidates = {Fraction(1, 2): {'v': EDGE}, Fraction(3, 4): {'v': frozenset()}}
    return reg, valid, heldout, candidates


def test_case_identity_carries_no_truth_and_registry_is_order_invariant():
    assert {f.name for f in fields(contract.CaseRef)} == {'case_id', 'graph_instance_id', 'data_sha256', 'split'}
    assert contract.registry(cases(), {'a', 'b'}).sha256 == contract.registry(reversed(cases()), {'b', 'a'}).sha256


@pytest.mark.parametrize('field', ['case_id', 'graph_instance_id', 'data_sha256'])
@pytest.mark.parametrize('pair', [(0, 1), (0, 2), (1, 2), (2, 3)])
def test_duplicate_identity_rejected_in_every_split_pair(field, pair):
    rows = cases()
    left, right = pair
    rows[right] = replace(rows[right], **{field: getattr(rows[left], field)})
    with pytest.raises(ValueError):
        contract.registry(rows, {'a', 'b'})


@pytest.mark.parametrize('change', [{'case_id': ''}, {'graph_instance_id': ''},
                                   {'data_sha256': 'metadata-only'}, {'split': 'unknown'}])
def test_bad_registry_identity(change):
    rows = cases()
    rows[0] = replace(rows[0], **change)
    with pytest.raises(ValueError):
        contract.registry(rows, {'a', 'b'})


def test_all_three_splits_required():
    with pytest.raises(ValueError):
        contract.registry(cases()[1:], {'a', 'b'})


@pytest.mark.parametrize('edges', [frozenset({('a', 'a')}), frozenset({('a', 'c')}),
                                  frozenset({('a', 'b', 'c')}), {('a', 'b')}])
def test_graph_scoring_universe(edges):
    reg, _, _, _ = inputs()
    with pytest.raises(ValueError):
        contract.graph(edges, reg)


@pytest.mark.parametrize('labels', [{}, {'v': EDGE, 'e1': EDGE}, {'e1': EDGE}])
def test_validation_truth_exact_identity(labels):
    reg, _, _, _ = inputs()
    with pytest.raises(ValueError):
        contract.truth_view(reg, 'validation', labels)


def test_selector_rejects_heldout_truth_and_changed_registry():
    reg, valid, heldout, candidates = inputs()
    for wrong in (heldout, replace(valid, registry_sha256='0' * 64)):
        with pytest.raises(ValueError):
            contract.choose_threshold(reg, wrong, candidates)


@pytest.mark.parametrize('predictions', [{}, {'v': EDGE, 'e1': EDGE}, {'e1': EDGE}])
def test_selector_prediction_identity(predictions):
    reg, valid, _, _ = inputs()
    with pytest.raises(ValueError):
        contract.choose_threshold(reg, valid, {Fraction(1, 2): predictions})


@pytest.mark.parametrize('threshold', [float('nan'), float('inf'), -float('inf'), True, -1, 2, 0.5])
def test_threshold_domain(threshold):
    reg, valid, _, _ = inputs()
    with pytest.raises(ValueError):
        contract.choose_threshold(reg, valid, {threshold: {'v': EDGE}})


def test_empty_candidates_rejected():
    reg, valid, _, _ = inputs()
    with pytest.raises(ValueError):
        contract.choose_threshold(reg, valid, {})


def test_ties_and_heldout_changes_cannot_change_selection_inputs():
    reg, valid, heldout, _ = inputs()
    forward = {Fraction(3, 4): {'v': EDGE}, Fraction(1, 2): {'v': EDGE}}
    selected = contract.choose_threshold(reg, valid, forward)
    assert selected == contract.choose_threshold(reg, valid, dict(reversed(list(forward.items()))))
    assert selected.threshold == Fraction(1, 2)
    a = contract.evaluate(reg, selected, heldout, {'e1': EDGE, 'e2': EDGE})
    b = contract.evaluate(reg, selected, contract.truth_view(reg, 'evaluation', {'e1': REVERSE, 'e2': REVERSE}),
                          {'e1': EDGE, 'e2': EDGE})
    assert a['threshold'] == b['threshold'] == Fraction(1, 2)
    assert a['macro_f1']['value'] == Fraction(1, 2) and b['macro_f1']['value'] == 0


@pytest.mark.parametrize('minimum', [0, -1, True, 1.5])
def test_invalid_denominator_rule(minimum):
    with pytest.raises(ValueError):
        contract.valid_mean([Fraction(1)], minimum)


def test_nonfinite_and_missing_requests_stay_in_denominator():
    result = contract.valid_mean([Fraction(1, 2), None, float('nan'), float('inf'), -float('inf')])
    assert (result['requested'], result['valid'], result['missing'], result['nonfinite']) == (5, 1, 1, 3)
    assert result['value'] == Fraction(1, 2) and result['availability'] == Fraction(1, 5)
    assert contract.valid_mean([None, float('nan')])['value'] is None
    assert contract.valid_mean([])['status'] == 'unavailable'
    assert contract.valid_mean([1], 2)['status'] == 'unavailable'


@pytest.mark.parametrize('metric', [True, '1', object()])
def test_invalid_metric_not_silently_counted(metric):
    with pytest.raises(ValueError):
        contract.valid_mean([metric])


def test_exact_mean_and_explicit_empty_graph_convention():
    assert contract.valid_mean([Fraction(1, 3), Fraction(2, 3)])['value'] == Fraction(1, 2)
    assert contract.f1(frozenset(), frozenset()) == 1
    assert contract.f1(EDGE, frozenset()) == 0


def test_evaluation_failure_has_an_explicit_retained_request():
    reg, valid, heldout, candidates = inputs()
    selected = contract.choose_threshold(reg, valid, candidates)
    result = contract.evaluate(reg, selected, heldout, {'e1': EDGE, 'e2': None})
    assert result['macro_f1']['requested'] == 2 and result['macro_f1']['valid'] == 1
    assert result['macro_f1']['availability'] == Fraction(1, 2)
    assert result['requests']['e2']['status'] == 'unavailable'
    with pytest.raises(ValueError):
        contract.evaluate(reg, selected, heldout, {'e1': EDGE})
    with pytest.raises(ValueError):
        contract.evaluate(reg, replace(selected, registry_sha256='0' * 64), heldout, {'e1': EDGE, 'e2': None})
