"""Deliver the reviewed recovery packet with exact transitive evidence custody."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'fixture-java-delivery-v1'


def relative(path):
    return str(path.relative_to(ROOT))


def prepare():
    assert not BASE.exists(), 'Recover the existing delivery; never replace its plan.'
    checks = DAY / 'fixture-java-publication-v1'
    evidence = []
    for name in ('legacy-check', 'program-check'):
        path = checks / (name + '-exit.json')
        result = json.loads(path.read_text())
        verify_bindings(result)
        assert result['unwrapped'] and result['actual_exit_code'] == 0
        evidence.append(ref(path, 'Observed unwrapped full-check exit'))
    packet = DAY / 'followup-runtime-v7/publication-receipt.json'
    result = json.loads(packet.read_text())
    verify_bindings(result)
    assert result['outcome'] == 'pass' and not result['awards_acceptance']
    paths = {
        'docs/program/state.json', 'docs/mission-control.md', 'docs/mission-control.html',
        'docs/program/execution/current-program.md', 'docs/program/master-live.md',
        'docs/program/execution/followup-current.json', 'docs/literature/fetch-manifest.json',
        'tools/audit_recovery_staging_v4_20261028.py', relative(Path(__file__)),
        'tests/test_public_attention_contract_v2_20261028.py',
    }
    patterns = (
        'tools/*attention*20261028.py', 'tools/*fixture_java*20261028.py',
        'tools/*aitiotita*20261028.py', 'tools/repair_protocol_master_pointer_20261028.py',
        'docs/program/execution/2026-10-28/*attention-protocol*',
        'docs/program/execution/2026-10-28/*fixture-java*',
        'docs/program/execution/2026-10-28/public-attention-contract-v2',
        'docs/program/execution/2026-10-28/aitiotita-delegates-v1',
        'docs/program/execution/2026-10-28/followup-runtime-v6',
        'docs/program/execution/2026-10-28/followup-runtime-v7',
        'docs/causal_proposal_attention_protocol_reviewed*2026-10-28.*',
        'docs/sponsor_proposal_attention_protocol_reviewed*2026-10-28.pdf',
        'docs/causal_proposal_fixture_java_reviewed*2026-10-28.*',
        'docs/sponsor_proposal_fixture_java_reviewed*2026-10-28.pdf',
        'docs/literature/raw/exec28_aitiotita_delegate_*',
    )
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            files = path.rglob('*') if path.is_dir() else [path]
            paths.update(relative(p) for p in files if p.is_file() and '__pycache__' not in p.parts)
    for name in ('delivery-consumed.json', 'push-verification.json'):
        paths.add('docs/program/execution/2026-10-28/attention-discovery-delivery-v1/' + name)
    for path in paths:
        assert (ROOT / path).is_file(), path
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip(), 'Preserve preexisting staged work.'
    parent = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    BASE.mkdir()
    write(BASE / 'delivery-plan.json', dict(
        status='reviewed_for_scoped_delivery', parent=parent,
        scope='Recovered protocol publication, stronger local fixture, Java delegates and exact paired documents',
        paths=[dict(path=p, sha256=hashlib.sha256((ROOT / p).read_bytes()).hexdigest()) for p in sorted(paths)],
        evidence=evidence + [ref(packet, 'Completed finite publication packet')],
        transitive_custody='The fixed v4 audit stages exact local dependencies reachable from these JSON/JSONL records.',
        unrelated_historical_logs='Excluded unless reached by an explicit evidence binding.',
        visual_acceptance=False, final_acceptance=False,
    ))
    print(json.dumps(dict(prepared=relative(BASE / 'delivery-plan.json'), paths=len(paths), parent=parent)))


def step(name, command):
    log = BASE / (name + '.log')
    assert not log.exists(), 'Consume the existing step exit before recovery: ' + name
    with log.open('x') as stream:
        result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    event = dict(step=name, actual_exit_code=result.returncode, command=command, log=relative(log))
    with (BASE / 'delivery-sequence.jsonl').open('a') as stream:
        stream.write(json.dumps(event) + '\n')
    print(json.dumps(event), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def deliver():
    plan = json.loads((BASE / 'delivery-plan.json').read_text())
    verify_bindings(plan)
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == plan['parent']
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
    paths = [p['path'] for p in plan['paths']] + [relative(BASE / 'delivery-plan.json')]
    step('stage-publication', ['git', 'add', '-f', '--', *paths])
    step('staging-audit', [sys.executable, 'tools/audit_recovery_staging_v4_20261028.py', relative(BASE)])
    step('authored-whitespace-check', ['git', 'diff', '--cached', '--check', '--', 'tools', 'tests', 'docs/mission-control.md', 'docs/program/master-live.md', 'docs/program/execution/current-program.md'])
    staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().split('\0')
    write(BASE / 'staged-review.json', dict(
        status='pass', staged_count=sum(bool(p) for p in staged),
        evidence=[ref(BASE / 'delivery-plan.json', 'Reviewed explicit scope'), ref(BASE / 'evidence-staging-review.json', 'Performed transitive custody audit')],
        checks='Both unchanged full controllers passed; exact source bindings and authored whitespace checked.',
        visual_acceptance=False, final_acceptance=False,
    ))
    step('stage-delivery-records', ['git', 'add', '-f', '--', relative(BASE)])
    step('git-commit', ['git', '-c', 'user.name=Codex', '-c', 'user.email=codex@users.noreply.github.com', 'commit', '-m', 'Recover proposal publication and integrate fixture and Java evidence'])
    step('git-push', ['git', 'push'])
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    assert commit == remote
    write(BASE / 'push-verification.json', dict(status='pass', commit=commit, origin_main=remote, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(pushed=commit, final_acceptance=False)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'deliver'))
    globals()[parser.parse_args().command]()
