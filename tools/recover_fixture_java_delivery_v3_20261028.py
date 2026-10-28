"""Resume custody delivery after distinguishing API envelopes from source bytes."""
import argparse
import json
import subprocess
from pathlib import Path

import recover_fixture_java_delivery_20261028 as delivery
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = delivery.ROOT
DAY = delivery.DAY
PRIOR = DAY / 'fixture-java-delivery-v2'
BASE = DAY / 'fixture-java-delivery-v3'


def prepare():
    assert not BASE.exists()
    plan = json.loads((PRIOR / 'repair-plan.json').read_text())
    verify_bindings(plan)
    events = [json.loads(x) for x in (PRIOR / 'delivery-sequence.jsonl').read_text().splitlines()]
    assert [(x['step'], x['actual_exit_code']) for x in events] == [('stage-repair', 0), ('staging-audit', 1)]
    assert 'Git blob mismatch' in (PRIOR / 'custody-diagnostic.log').read_text()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == plan['parent']
    staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().split(chr(0))) - {''}
    additions = [ROOT / 'tools/audit_recovery_staging_v6_20261028.py', ROOT / 'tools/audit_recovery_staging_v7_20261028.py', Path(__file__)]
    additions += [p for p in sorted(PRIOR.iterdir()) if p.is_file()]
    BASE.mkdir()
    write(BASE / 'repair-plan.json', dict(
        status='reviewed_delivery_recovery', parent=plan['parent'], preserved_staged_count=len(staged),
        evidence=[ref(PRIOR / 'repair-plan.json', 'Preserved prior repair'),
                  ref(PRIOR / 'staging-audit.log', 'Preserved second audit failure'),
                  ref(PRIOR / 'custody-diagnostic.log', 'Exact envelope versus source mismatch'),
                  ref(ROOT / 'docs/program/execution/2026-10-25/agents-reuse-v1/git-byte-validation.json', 'Existing envelope and decoded-license identities')],
        additions=[ref(p, 'Scoped recovery evidence') for p in additions],
        repair='Validate API-envelope and decoded-source SHA-256 separately; verify exact base64 equality and Git blob identity on decoded source. Deduplicate traversal without dropping any path.',
        verification=['All 17 gformula source records authenticate.',
                      'All 72 agents-reuse source bindings authenticate, including API envelope and decoded license.',
                      'Authored local test paths remain in custody scope.'],
        unchanged='No source bytes, manuscript, acceptance outcome or historical receipt changed.',
        final_acceptance=False))
    print(json.dumps(dict(prepared=delivery.rel(BASE), staged=len(staged), additions=len(additions))))


def deliver():
    delivery.BASE = BASE
    original = delivery.step

    def step(name, command):
        command = ['tools/audit_recovery_staging_v7_20261028.py' if x == 'tools/audit_recovery_staging_v5_20261028.py' else x for x in command]
        return original(name, command)

    delivery.step = step
    delivery.deliver()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'deliver'))
    globals()[parser.parse_args().command]()
