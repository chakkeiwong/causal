"""Resume failed delivery with verified upstream/local path disambiguation."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
PRIOR = DAY / 'fixture-java-delivery-v1'
BASE = DAY / 'fixture-java-delivery-v2'


def rel(p):
    return str(p.relative_to(ROOT))


def prepare():
    assert not BASE.exists()
    prior = json.loads((PRIOR / 'delivery-plan.json').read_text())
    verify_bindings(prior)
    events = [json.loads(x) for x in (PRIOR / 'delivery-sequence.jsonl').read_text().splitlines()]
    assert [(x['step'], x['actual_exit_code']) for x in events] == [('stage-publication', 0), ('staging-audit', 1)]
    assert 'tests/testthat/test-gformula.R' in (PRIOR / 'staging-audit.log').read_text()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == prior['parent']
    staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().split(chr(0))) - {''}
    allowed = {p['path'] for p in prior['paths']} | {rel(PRIOR / 'delivery-plan.json')}
    assert staged <= allowed, sorted(staged - allowed)
    added = [ROOT / 'tools/audit_recovery_staging_v5_20261028.py', Path(__file__), ROOT / 'tools/reconcile_java_panel_tails_20261028.py']
    added += sorted((DAY / 'software-tail-java-panel-delta-v1').glob('*'))
    added += [PRIOR / 'delivery-sequence.jsonl', PRIOR / 'staging-audit.log', PRIOR / 'stage-publication.log']
    BASE.mkdir()
    write(BASE / 'repair-plan.json', dict(
        status='reviewed_delivery_recovery', parent=prior['parent'], preserved_staged_count=len(staged),
        evidence=[ref(PRIOR / 'delivery-plan.json', 'Original reviewed delivery scope'),
                  ref(PRIOR / 'staging-audit.log', 'Preserved false missing-local-path failure'),
                  ref(ROOT / 'docs/program/execution/2026-10-20/gformula-reuse-v1/authenticated-source-identities.json', 'Explicit upstream path, local_path, Git blob and SHA-256')],
        additions=[ref(p, 'Scoped recovery or bounded source-tail continuation') for p in added],
        repair='Recognize local_path and git_blob_sha1 in authenticated upstream records. Exclude upstream path only after both local SHA-256 and Git blob verification; keep authored tests in custody scope.',
        verification=['Original upstream fixture maps to its genuine saved bytes.', 'Authored test paths remain local dependencies.', 'A tampered upstream SHA-256 is refused.'],
        unchanged='No manuscript, acceptance outcome, citation identity or original evidence is altered by this repair.',
        final_acceptance=False,
    ))
    print(json.dumps(dict(prepared=rel(BASE), staged=len(staged), additions=len(added))))


def step(name, command):
    log = BASE / (name + '.log')
    assert not log.exists(), 'Consume existing step first: ' + name
    with log.open('x') as stream:
        result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    event = dict(step=name, actual_exit_code=result.returncode, command=command, log=rel(log))
    with (BASE / 'delivery-sequence.jsonl').open('a') as stream:
        stream.write(json.dumps(event) + chr(10))
    print(json.dumps({k: event[k] for k in ('step', 'actual_exit_code', 'log')}), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def deliver():
    plan = json.loads((BASE / 'repair-plan.json').read_text())
    verify_bindings(plan)
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == plan['parent']
    step('stage-repair', ['git', 'add', '-f', '--', rel(BASE / 'repair-plan.json'), *[x['path'] for x in plan['additions']]])
    step('staging-audit', [sys.executable, 'tools/audit_recovery_staging_v5_20261028.py', rel(BASE)])
    step('authored-whitespace-check', ['git', 'diff', '--cached', '--check', '--', 'tools', 'tests', 'docs/mission-control.md', 'docs/program/master-live.md', 'docs/program/execution/current-program.md'])
    paths = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().split(chr(0))
    write(BASE / 'staged-review.json', dict(status='pass', staged_count=sum(bool(p) for p in paths),
        evidence=[ref(BASE / 'repair-plan.json', 'Reviewed recovery'), ref(BASE / 'evidence-staging-review.json', 'Performed transitive custody')],
        visual_acceptance=False, final_acceptance=False))
    step('stage-delivery-records', ['git', 'add', '-f', '--', rel(BASE)])
    step('git-commit', ['git', '-c', 'user.name=Codex', '-c', 'user.email=codex@users.noreply.github.com', 'commit', '-m', 'Recover proposal publication and reconcile fixture and Java evidence'])
    step('git-push', ['git', 'push'])
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    assert commit == remote
    write(BASE / 'push-verification.json', dict(status='pass', commit=commit, origin_main=remote, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(pushed=commit)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'deliver'))
    globals()[parser.parse_args().command]()
