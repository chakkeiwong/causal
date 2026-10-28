"""Commit the verified publication and its transitive local evidence, then push."""
import json
import subprocess
from execute_openai_publication_20261028 import ROOT, BASE, step


def main():
    assert json.loads((BASE / 'publication-checkpoint.json').read_text())['status'] == 'published_checked'
    paths = {'docs/program/state.json', 'docs/mission-control.md', 'docs/mission-control.html',
        'docs/program/execution/current-program.md', 'docs/literature/fetch-manifest.json',
        'docs/program/comprehensive-v14/work/LL.CENSUS/search-closure.json',
        'tools/review_census_criteria_20261028.py'}
    for pattern in ['tools/*openai*20261028.py',
        'docs/program/execution/2026-10-28/*openai*',
        'docs/program/execution/2026-10-28/census-criterion-review-v1',
        'docs/program/execution/2026-10-28/l6-criterion-review-v1',
        'docs/program/execution/2026-10-28/l6-official-markdown-v1',
        'docs/literature/raw/exec28_openai*', 'docs/literature/raw/exec28_l6_*',
        'docs/causal_proposal_openai_contract_reviewed_v1_2026-10-28.*',
        'docs/sponsor_proposal_openai_contract_reviewed_2026-10-28.pdf']:
        paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
    prior = BASE.parent / 'followup-causal-review-v1'
    for name in ['push-verification.json', 'delivery-consumed.json', 'git-commit.log', 'git-push.log']:
        paths.add(str((prior / name).relative_to(ROOT)))
    step('stage-publication', ['git', 'add', '-f', '--', *sorted(paths)])
    step('staging-audit', ['python3', 'tools/audit_recovery_staging_v3_20261028.py', str(BASE.relative_to(ROOT))])
    step('authored-whitespace-check', ['git', 'diff', '--cached', '--check', '--', 'tools', 'docs/mission-control.md', 'docs/program/execution/current-program.md'])
    subprocess.run(['git', 'add', '-f', '--', str(BASE.relative_to(ROOT))], cwd=ROOT, check=True)
    step('git-commit', ['git', '-c', 'user.name=Codex', '-c', 'user.email=codex@users.noreply.github.com', 'commit', '-m',
        'Complete finite census review and integrate pinned provider response contracts'])
    step('git-push', ['git', 'push'])
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    assert commit == remote
    p = BASE / 'push-verification.json'
    assert not p.exists()
    p.write_text(json.dumps(dict(status='pass', commit=commit, origin_main=remote), indent=2) + chr(10))
    print(json.dumps(dict(pushed=commit)), flush=True)


if __name__ == '__main__':
    main()
