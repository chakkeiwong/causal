"""Preserve failed read-only staging and resume the exact reviewed scope."""
import argparse
import json
import subprocess
from pathlib import Path

import deliver_panel_delegate_publication_20261028 as original
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = original.ROOT
PRIOR = original.BASE
BASE = original.DAY / 'panel-delegate-delivery-v2'


def prepare():
    assert not BASE.exists()
    plan = json.loads((PRIOR / 'delivery-plan.json').read_text())
    verify_bindings(plan)
    events = [json.loads(x) for x in (PRIOR / 'delivery-sequence.jsonl').read_text().splitlines()]
    assert [(x['step'], x['actual_exit_code']) for x in events] == [('stage-publication', 128)]
    assert 'Read-only file system' in (PRIOR / 'stage-publication.log').read_text()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == plan['parent']
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
    BASE.mkdir()
    (BASE / 'preparation.log').write_bytes(Path('/tmp/causal-panel-delegate-delivery-prepare-20261028.log').read_bytes())
    write(BASE / 'preparation-exit.json', dict(actual_exit_code=0, execution='performed', observed='PTY session 1733 completed with exit 0', evidence=[ref(BASE / 'preparation.log', 'Exact preparation output')]))
    additions = [PRIOR / 'delivery-plan.json', PRIOR / 'delivery-sequence.jsonl', PRIOR / 'stage-publication.log', Path(__file__), BASE / 'preparation.log', BASE / 'preparation-exit.json']
    plan['paths'] += [ref(p, 'Preserved staging failure or narrowly scoped retry') for p in additions]
    plan.update(status='reviewed_exact_scope_retry_after_readonly_staging', recovery='No path was staged. Preserve exit 128 and retry exact scoped Git operations with required environment permission.', predecessor=ref(PRIOR / 'delivery-plan.json', 'Original 180-path reviewed scope'))
    write(BASE / 'delivery-plan.json', plan)
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)), paths=len(plan['paths']), parent=plan['parent'])))


def deliver():
    original.BASE = BASE
    original.deliver()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'deliver'))
    globals()[parser.parse_args().command]()
