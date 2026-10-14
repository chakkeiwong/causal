"""Behavioral regressions for the missing proposal execution lifecycle."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import run_program as run


@pytest.fixture
def workspace(tmp_path):
    old = {'id': 'OLD', 'lane': 'software', 'title': 'Existing task', 'action': 'Inspect source',
           'depends': [], 'requires_inputs': [], 'capabilities': [], 'study': False,
           'priority': 1, 'outputs': ['out/old.json'], 'criteria': ['Inspected bytes']}
    graph = {'lanes': ['software'], 'nodes': [old, dict(old, id='STUDY', study=True, outputs=['out/study.json']),
                                          dict(old, id='LATER', outputs=['out/later.json'])]}
    nodes = [dict(old, id=f'P{i}.DESIGN', lane='public_evidence', outputs=[f'out/p{i}.json']) for i in range(1, 7)]
    nodes += [dict(old, id=f'PROPOSAL.Q{i}', lane='proposal_acceptance', depends=[{'id': 'OLD', 'outcomes': ['pass']}],
                   outputs=[f'out/q{i}.json']) for i in range(1, 6)]
    scope = {'operation_stages': {'OLD': 'proposal_now', 'STUDY': 'proposal_now', 'LATER': 'later_conditional'},
             'proposal_acceptance': [{'id': 'Q' + str(i)} for i in range(1, 6)]}
    for name, obj in [('graph.json', graph), ('scope.json', scope), ('contracts.json', {'nodes': nodes})]:
        run.core.write(tmp_path / name, obj)
    def empty():
        return {'results': {}, 'registrations': {}, 'blocks': {}, 'progress': {}, 'turns': []}
    state = {'events': [], 'reader': {'path': 'book.pdf', 'sha256': '0' * 64}, 'input_receipts': {},
             'execution_program': dict(empty(), documents={'graph': {'path': 'graph.json'}}),
             'proposal_program': {'revision': 'test', 'documents': {'scope': {'path': 'scope.json'}}},
             'execution_runtime': dict(empty(), contracts={'path': 'contracts.json'}, active=None)}
    return tmp_path, state


def receipt(root, state, key):
    graph, _, _ = run.combined(root, state)
    node = run.ledger.operation(graph, key)
    for name in node['outputs']:
        run.core.write(root / name, {'actual': 'reviewed result'})
    refs = [run.bind(root, p, 'Inspected result') for p in node['outputs']]
    data = run.ledger.receipt_template(node)
    data.update(outcome='pass', execution='performed', scope='Test design only', reviewer={'name': 'test author', 'kind': 'author'}, outputs=refs,
                criteria=[{'index': i, 'verdict': 'pass', 'finding': 'Observed result', 'evidence': refs} for i in range(len(node['criteria']))])
    path = 'receipts/' + key + '.json'
    run.core.write(root / path, data)
    return path


def transition(root, state, command, key, path=None):
    event = run.apply(root, state, command, key, path, 'Scheduled eligible work')
    state['events'].append(event)


def test_public_task_completes_and_advances_to_existing_lane(workspace):
    root, state = workspace
    assert run.status(root, state)['next'] == 'P1.DESIGN'
    transition(root, state, 'start', 'P1.DESIGN')
    transition(root, state, 'record', 'P1.DESIGN', receipt(root, state, 'P1.DESIGN'))
    view = run.status(root, state)
    assert view['public_designs']['P1.DESIGN'] == 'pass'
    assert view['next'] == 'OLD' and view['continue']
    assert view['recorded_proposal_operations'] == 1


def test_interrupted_checkpoint_resumes_exact_action(workspace):
    root, state = workspace
    transition(root, state, 'start', 'P1.DESIGN')
    output = receipt(root, state, 'P1.DESIGN')
    run.core.write(root / 'checkpoint.json', {'finding': 'Four briefs drafted', 'next_action': 'Review exclusion restriction in brief 2',
                                             'evidence': [run.bind(root, output, 'Draft')]})
    transition(root, state, 'progress', 'P1.DESIGN', 'checkpoint.json')
    recovered = json.loads(json.dumps(state))
    view = run.status(root, recovered)
    assert view['next'] == 'P1.DESIGN'
    assert view['next_action'] == 'Review exclusion restriction in brief 2'
    assert not recovered['execution_runtime']['results']


def test_local_blocker_does_not_stop_independent_work_and_resume_needs_evidence(workspace):
    root, state = workspace
    proof = receipt(root, state, 'P1.DESIGN')
    note = {'reason': 'Source unavailable', 'revisit_trigger': 'Exact source becomes accessible',
            'evidence': [run.bind(root, proof, 'Observed failed source request')]}
    run.core.write(root / 'block.json', note)
    transition(root, state, 'block', 'P1.DESIGN', 'block.json')
    assert run.status(root, state)['next'] == 'OLD'
    with pytest.raises(ValueError, match='resolution'):
        transition(root, state, 'resume', 'P1.DESIGN', 'block.json')
    run.core.write(root / 'resume.json', {'resolution': 'Source now accessible', 'evidence': note['evidence']})
    transition(root, state, 'resume', 'P1.DESIGN', 'resume.json')
    assert 'P1.DESIGN' not in state['execution_runtime']['blocks']


@pytest.mark.parametrize('failure', ['changed_evidence', 'missing_evidence', 'missing_criterion', 'false_execution'])
def test_no_completion_without_valid_evidence(workspace, failure):
    root, state = workspace
    path = receipt(root, state, 'P1.DESIGN')
    data = run.core.read(root, path)
    if failure == 'changed_evidence':
        (root / data['outputs'][0]['path']).write_text('changed')
    elif failure == 'missing_evidence':
        data['criteria'][0]['evidence'] = []
    elif failure == 'missing_criterion':
        data['criteria'] = []
    else:
        data['execution'] = 'not_performed'
        # Historical validator allows pass/not_performed without capabilities;
        # the current controller must explicitly close that loophole.
    run.core.write(root / path, data)
    with pytest.raises(ValueError):
        transition(root, state, 'record', 'P1.DESIGN', path)
    assert not state['execution_runtime']['results']


def test_completed_tasks_cannot_be_silently_repeated(workspace):
    root, state = workspace
    path = receipt(root, state, 'P1.DESIGN')
    transition(root, state, 'record', 'P1.DESIGN', path)
    with pytest.raises(ValueError, match='already recorded'):
        transition(root, state, 'record', 'P1.DESIGN', path)
    assert run.status(root, state)['next'] != 'P1.DESIGN'


def test_later_work_cannot_be_selected_as_proposal_work(workspace):
    root, state = workspace
    with pytest.raises(ValueError, match='optional/later'):
        transition(root, state, 'start', 'LATER')
    assert 'LATER' not in [n['id'] for n in run.queue(root, state)[3]]


def test_final_study_cannot_run_without_prospective_registration(workspace):
    root, state = workspace
    assert [n['id'] for n in run.queue(root, state)[4]] == ['STUDY']
    with pytest.raises(ValueError, match='registration'):
        transition(root, state, 'record', 'STUDY', receipt(root, state, 'STUDY'))


def test_recording_existing_task_uses_preserved_ledger(workspace):
    root, state = workspace
    transition(root, state, 'record', 'OLD', receipt(root, state, 'OLD'))
    assert 'OLD' in state['execution_program']['results']
    assert 'OLD' not in state['execution_runtime']['results']
    assert run.status(root, state)['continue']


def test_second_task_cannot_discard_active_checkpoint(workspace):
    root, state = workspace
    transition(root, state, 'start', 'P1.DESIGN')
    with pytest.raises(ValueError, match='active task'):
        transition(root, state, 'start', 'OLD')


def test_empty_queue_does_not_invent_acceptance(workspace):
    root, state = workspace
    view = run.status(root, state)
    assert not view['proposal_accepted'] and not view['background_worker_running']


def test_yield_preserves_exact_resume_action(workspace):
    root, state = workspace
    transition(root, state, 'start', 'P1.DESIGN')
    proof = receipt(root, state, 'P1.DESIGN')
    run.core.write(root / 'yield.json', {'finding': 'Draft available', 'next_action': 'Review IV assumptions',
                                       'yield_reason': 'Inspect independent source while this draft is preserved',
                                       'evidence': [run.bind(root, proof, 'Draft')]})
    transition(root, state, 'yield', 'P1.DESIGN', 'yield.json')
    assert run.status(root, state)['next'] == 'OLD'
    transition(root, state, 'start', 'P1.DESIGN')
    assert run.status(root, state)['next_action'] == 'Review IV assumptions'


def test_proposal_acceptance_requires_exact_release_review(workspace):
    root, state = workspace
    transition(root, state, 'record', 'OLD', receipt(root, state, 'OLD'))
    path = receipt(root, state, 'PROPOSAL.Q1')
    with pytest.raises(ValueError, match='acceptance scope'):
        transition(root, state, 'record', 'PROPOSAL.Q1', path)
    assert not run.status(root, state)['proposal_accepted']


def test_stale_state_cannot_overwrite_concurrent_progress(workspace, monkeypatch):
    root, state = workspace
    run.core.write(root / run.core.STATE, state)
    old_hash = run.core.sha(root / run.core.STATE)
    changed = copy.deepcopy(state)
    changed['events'].append({'action': 'concurrent_work'})
    run.core.write(root / run.core.STATE, changed)
    monkeypatch.setattr(run.core, 'validate_state', lambda *_: [])
    monkeypatch.setattr(run.core, 'render', lambda *_: None)
    with pytest.raises(ValueError, match='State changed'):
        run.core.commit_state(root, old_hash, state, {'action': 'lost_update'})
    assert run.core.read(root, run.core.STATE) == changed
