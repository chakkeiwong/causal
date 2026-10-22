#!/usr/bin/env python3
"""Preserve reviewed controllers and display the latest durable resume action."""
import run_program_reviews_v2 as previous

base = previous.base
_status = base.status
_render = base.render
CONTROLLER = 'python3 tools/run_program_checkpoint_v3.py'


def status(root, state):
    result = _status(root, state)
    result['controller'] = CONTROLLER
    key = result['next']
    if key and not result['active'] and key not in result['review_reopen_candidates']:
        _, merged, _ = base.combined(root, state)
        checkpoints = merged['execution_program']['progress'].get(key, [])
        if checkpoints:
            latest = checkpoints[-1]
            base.core.bound(root, latest)
            note = base.core.read(root, latest['path'])
            base.validate_note(root, note, 'progress')
            result['next_action'] = note['next_action']
            result['next_action_checkpoint'] = latest
    return result


def render(root, state):
    _render(root, state)
    for name in ['docs/mission-control.md', 'docs/mission-control.html']:
        path = root / name
        path.write_text(path.read_text().replace('tools/run_program_reviews_v2.py',
            'tools/run_program_checkpoint_v3.py'))


base.status = status
base.render = render


if __name__ == '__main__':
    previous.main()
