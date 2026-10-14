"""Regression tests for the material proposal-versus-product boundary."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import proposal_program as p


@pytest.fixture
def candidate():
    return json.loads((ROOT / 'docs/program/public-data-v15/candidate-state.json').read_text())


def test_real_candidate_and_preserved_history_validate(candidate):
    assert p.validate_state(ROOT, candidate) == []


@pytest.mark.parametrize('failure', ['missing_operation', 'later_dependency', 'authentic_input', 'unknown_stage', 'false_proposal_acceptance', 'false_product_acceptance', 'missing_input_stage', 'false_study', 'unaudited_dataset'])
def test_invalid_scope_is_rejected(candidate, monkeypatch, failure):
    read = p.core.read
    scope = copy.deepcopy(p.scope_for(ROOT, candidate))
    graph = copy.deepcopy(p.ledger.graph_for(ROOT, candidate))
    register_path = candidate['proposal_program']['documents']['dataset_register']['path']
    register = copy.deepcopy(read(ROOT, register_path))
    key = 'SW.REVIEW.discovery_iid'
    if failure == 'missing_operation':
        scope['operation_stages'].pop(key)
    elif failure == 'later_dependency':
        scope['operation_stages']['SW.COMP.discovery_iid'] = 'later_conditional'
    elif failure == 'authentic_input':
        scope['operation_stages']['EXT.VALIDATE.bank_truth'] = 'proposal_now'
    elif failure == 'unknown_stage':
        scope['operation_stages'][key] = 'completed_by_renaming'
    elif failure == 'false_proposal_acceptance':
        scope['proposal_accepted'] = True
    elif failure == 'false_product_acceptance':
        scope['product_accepted'] = True
    elif failure == 'missing_input_stage':
        scope['input_stages'].pop('bank_truth')
    elif failure == 'false_study':
        register['new_fitted_causal_studies'] = 1
    elif failure == 'unaudited_dataset':
        register['families'][0]['source_keys'] = ['fabricated']
    monkeypatch.setattr(p, 'scope_for', lambda *_: scope)
    monkeypatch.setattr(p.ledger, 'graph_for', lambda *_: graph)
    monkeypatch.setattr(p.core, 'read', lambda root, path: register if path == register_path else read(root, path))
    assert p.validate_state(ROOT, candidate)


def test_private_inputs_do_not_hide_ready_proposal_work(candidate):
    assert candidate['input_receipts'] == {}
    view = p.overview(candidate, p.ledger.graph_for(ROOT, candidate))
    assert view['ready_proposal_operations'] > 0
    assert view['continue'] is True
    assert view['product_acceptance_is_current_goal'] is False
    assert len(view['public_evidence_next']) == 6


def test_source_tampering_rejected(candidate):
    candidate['proposal_program']['documents']['source_audit']['sha256'] = '0' * 64
    assert p.validate_state(ROOT, candidate)
