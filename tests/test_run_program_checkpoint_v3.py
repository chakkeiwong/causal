"""A yielded task's dashboard must agree with its durable resumption receipt."""
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from test_run_program import workspace, receipt, transition
import run_program_checkpoint_v3 as current

run = current.base


def checkpoint(root, state, key, filename, action):
    proof = receipt(root, state, key)
    run.core.write(root / filename, dict(finding='New inspected evidence', next_action=action,
        yield_reason='Continue independent work', evidence=[run.bind(root, proof, 'Reviewed evidence')]))
    transition(root, state, 'start', key)
    transition(root, state, 'yield', key, filename)


def select_old_without_active_task(root, state):
    for i in range(1, 7):
        transition(root, state, 'record', f'P{i}.DESIGN', receipt(root, state, f'P{i}.DESIGN'))
    assert state['execution_runtime']['active'] is None


def test_latest_checkpoint_survives_roundtrip_and_drives_dashboard(workspace):
    root, state = workspace
    checkpoint(root, state, 'OLD', 'first.json', 'Inspect newly recovered original')
    checkpoint(root, state, 'OLD', 'second.json', 'Write comparison from inspected original')
    select_old_without_active_task(root, state)
    recovered = json.loads(json.dumps(state))
    view = run.status(root, recovered)
    assert view['next'] == 'OLD'
    assert view['next_action'] == 'Write comparison from inspected original'
    assert view['next_action_checkpoint']['path'] == 'second.json'
    transition(root, recovered, 'start', 'OLD')
    assert run.status(root, recovered)['next_action'] == view['next_action']
    assert not recovered['execution_program']['results']


def test_changed_checkpoint_is_rejected_instead_of_displayed(workspace):
    root, state = workspace
    checkpoint(root, state, 'OLD', 'resume.json', 'Inspect pinned source')
    select_old_without_active_task(root, state)
    (root / 'resume.json').write_text('{"next_action":"skip required work"}')
    with pytest.raises(ValueError):
        run.status(root, state)


def test_fresh_task_keeps_original_action_and_unfinished_status(workspace):
    root, state = workspace
    view = run.status(root, state)
    assert view['next'] == 'P1.DESIGN'
    assert view['next_action'] == 'Inspect source'
    assert view['recorded_proposal_operations'] == 0
    assert view['proposal_accepted'] is False
    assert view['controller'] == current.CONTROLLER
