"""Deliver only changed bound evidence against the verified committed baseline."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import audit_recovery_staging_v7_20261028 as custody
import recover_fixture_java_delivery_20261028 as delivery
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = delivery.ROOT
DAY = delivery.DAY
BASE = DAY / 'blip-helper-delivery-v1'
PARENT = '4d88f7ece9f0da195d1b532737f00fc7554a3a8c'


def rel(p):
    return str(p.relative_to(ROOT))


def prepare():
    assert not BASE.exists()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == PARENT
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
    receipt = DAY / 'followup-runtime-v9/publication-receipt.json'
    v = json.loads(receipt.read_text())
    verify_bindings(v)
    assert v['outcome'] == 'pass' and not v['awards_acceptance']
    for name in ['legacy-check', 'program-check']:
        v = json.loads((DAY / 'blip-helper-publication-v2' / (name + '-exit.json')).read_text())
        verify_bindings(v)
        assert v['actual_exit_code'] == 0 and v['unwrapped']
    paths = {'docs/program/state.json', 'docs/program/execution/followup-current.json',
             'docs/program/execution/current-program.md', 'docs/program/master-live.md',
             'docs/mission-control.md', 'docs/mission-control.html', 'docs/literature/fetch-manifest.json', rel(Path(__file__))}
    patterns = [
        'tools/*blip*20261028.py', 'tools/index_recovery_continuations_20261028.py', 'tools/dispatch_recovery_helpers_20261028.py',
        'tools/reconcile_python_continuation_20261028.py', 'tools/reconcile_panel_leads_20261028.py',
        'tools/reconcile_cxx_continuation_20261028.py', 'tools/finish_recovery_independent_20261028.py',
        'docs/program/execution/2026-10-28/*blip*',
        'docs/program/execution/2026-10-28/continuation-control-recovery-v1',
        'docs/program/execution/2026-10-28/continuation-inventory-v1',
        'docs/program/execution/2026-10-28/python-continuation-recovery-v1',
        'docs/program/execution/2026-10-28/panel-lead-reconciliation-v1',
        'docs/program/execution/2026-10-28/cxx-tail-reconciliation-v1',
        'docs/program/execution/2026-10-28/followup-runtime-v9',
        'docs/program/execution/2026-10-28/nested-delivery-v1',
        'docs/literature/raw/exec28_blip_helper_*',
        'docs/causal_proposal_blip_helpers_reviewed_v1_2026-10-28.*',
        'docs/sponsor_proposal_blip_helpers_reviewed*2026-10-28.pdf',
    ]
    for pattern in patterns:
        for p in ROOT.glob(pattern):
            items = p.rglob('*') if p.is_dir() else [p]
            paths.update(rel(f) for f in items if f.is_file() and '__pycache__' not in f.parts)
    paths.update(rel(p) for p in (DAY / 'nested-delivery-v1').iterdir() if p.is_file())
    queue = [p for p in paths if p.endswith(('.json', '.jsonl'))]
    seen = set(queue)
    bound = set()
    while queue:
        p = queue.pop()
        f = ROOT / p
        try:
            values = [json.loads(x) for x in f.read_text().splitlines() if x.strip()] if f.suffix == '.jsonl' else [json.loads(f.read_text())]
        except (UnicodeError, ValueError):
            continue
        for value in values:
            for q in custody.bindings(value):
                assert (ROOT / q).is_file(), q
                bound.add(q)
                if q.endswith(('.json', '.jsonl')) and q not in seen:
                    seen.add(q)
                    queue.append(q)
        if len(seen) % 1000 == 0:
            print(json.dumps(dict(progress='binding_walk', documents=len(seen), pending=len(queue))), flush=True)
    dirty = set(subprocess.check_output(['git', 'diff', '--name-only', '-z', 'HEAD'], cwd=ROOT).decode().split(chr(0)))
    untracked = set(subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=ROOT).decode().split(chr(0)))
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split(chr(0)))
    additions = {p for p in bound if p in dirty or p in untracked or p not in tracked}
    paths |= additions
    # Unchanged tracked dependencies already exist in the previously audited commit.
    # Both unwrapped controllers just validated current source identities. Avoid
    # recomputing LFS identities for multi-gigabyte unchanged historical archives.
    BASE.mkdir()
    write(BASE / 'delivery-plan.json', dict(status='reviewed_incremental_custody', parent=PARENT,
        paths=[ref(ROOT / p, 'Exact scoped delivery bytes') for p in sorted(paths)],
        traversed_documents=len(seen), bound_paths=len(bound), changed_bound_paths=len(additions),
        evidence=[ref(receipt, 'Completed finite publication'), ref(DAY / 'fixture-java-delivery-v3/evidence-staging-review.json', 'Prior full 30000-path custody audit'), ref(DAY / 'blip-helper-publication-v2/legacy-check-exit.json', 'Current unchanged legacy check'), ref(DAY / 'blip-helper-publication-v2/program-check-exit.json', 'Current unchanged program check')],
        optimization='Traverse all bindings; stage every untracked or Git-different bound dependency. Preserve unchanged tracked dependencies already in audited parent. Do not blanket-stage unrelated historical logs.',
        visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(prepared=rel(BASE), paths=len(paths), bound_paths=len(bound), changed_bound_paths=len(additions))), flush=True)


def deliver():
    plan = json.loads((BASE / 'delivery-plan.json').read_text())
    verify_bindings(plan)
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == plan['parent']
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
    delivery.BASE = BASE
    delivery.step('stage-publication', ['git', 'add', '-f', '--', rel(BASE / 'delivery-plan.json'), *[p['path'] for p in plan['paths']]])
    delivery.step('authored-whitespace-check', ['git', 'diff', '--cached', '--check', '--', 'tools', 'docs/program/master-live.md', 'docs/program/execution/current-program.md', 'docs/mission-control.md'])
    staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().split(chr(0))) - {''}
    allowed = {p['path'] for p in plan['paths']} | {rel(BASE / 'delivery-plan.json')}
    assert staged <= allowed
    changed = set(subprocess.check_output(['git', 'diff', '--name-only', '-z'], cwd=ROOT).decode().split(chr(0))) - {''}
    assert not changed & allowed, sorted(changed & allowed)
    write(BASE / 'staged-review.json', dict(status='pass', staged_count=len(staged), exact_worktree_versions=True, evidence=[ref(BASE / 'delivery-plan.json', 'Complete reviewed scope')], visual_acceptance=False, final_acceptance=False))
    delivery.step('stage-delivery-records', ['git', 'add', '-f', '--', rel(BASE)])
    delivery.step('git-commit', ['git', '-c', 'user.name=Codex', '-c', 'user.email=codex@users.noreply.github.com', 'commit', '-m', 'Recover continuation inventory and review BLIP score and input helpers'])
    delivery.step('git-push', ['git', 'push'])
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    assert head == remote
    write(BASE / 'push-verification.json', dict(status='pass', commit=head, origin_main=remote, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(pushed=head)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'deliver'))
    globals()[parser.parse_args().command]()
