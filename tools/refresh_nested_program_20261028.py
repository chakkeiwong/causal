"""Refresh live dashboards from exact releases without rewriting frozen masters."""
import copy
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import load, view
from run_followup_program_v2_20261028 import selected

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'program-refresh-nested-v1'
PRIOR = DAY / 'program-refresh-fixture-java-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    run = controller.base
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    results = merged['execution_program']['results']
    reader = read(DAY / 'nested-reader-v2/working-release.json')
    sponsor = read(DAY / 'sponsor-nested-v1/working-release.json')
    for release in (reader, sponsor):
        verify_bindings(release)
    assert run.same_reader(state['reader'], reader['pdf'])
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    nodes = [n for n in graph['nodes'] if stages[n['id']] == 'proposal_now']
    remaining = copy.deepcopy(read(PRIOR / 'remaining-operations.json'))
    ids = {n['id'] for n in nodes if results.get(n['id'], {}).get('outcome') != 'pass'}
    assert len(nodes) == 376 and len(ids) == 150
    assert ids == {r['id'] for r in remaining['operations']}
    assert Counter(results.get(k, {}).get('outcome', 'open') for k in ids) == dict(inconclusive=121, open=25, negative=4)
    assert sum(n['id'] in results for n in nodes) == 351
    for row in remaining['operations']:
        if row['id'] in ('TEXT.REVIEW.L1', 'TEXT.REVIEW.L6'):
            binding = results[row['id']]
            row.update(action=read(ROOT / binding['path'])['revisit_trigger'], evidence=binding, action_basis=binding)
        if row['id'] == 'SW.CELL.discovery_iid.Java':
            row['later_source_delta'] = ref(DAY / 'reliableai-nested-v1/author-review.json', '20 selected nested originals; broad qualification unchanged')
            row['corrected_continuation'] = 'Retain later Weka/Banjo/Tetrad reviews, seven Aitiotita delegates and 20 BLIP/Spot originals. Address remaining origin/helper/artifact/rights and conversion tails; do not repeat completed acquisitions.'
    protected = [ROOT / 'docs/program/master-program.md', ROOT / 'docs/program/master-current.md']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    BASE.mkdir()
    current = ROOT / 'docs/program/execution/current-program.md'
    live = ROOT / 'docs/program/master-live.md'
    for src, name in [(current, 'prior-current-program.md'), (live, 'prior-master-live.md')]:
        (BASE / name).write_bytes(src.read_bytes())
    remaining.update(reader=state['reader'], ready=len(ready), predecessor=ref(PRIOR / 'remaining-operations.json', 'All prior unresolved IDs'))
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'remaining-operations.json', remaining)
    write(BASE / 'followup-snapshot.json', view(load(ROOT, selected())))
    evidence = [ref(DAY / p, 'Verified current evidence') for p in ('nested-reader-v2/working-release.json', 'sponsor-nested-v1/working-release.json', 'reliableai-nested-v1/author-review.json', 'software-tail-java-panel-delta-v1/author-review.json', 'fixture-java-delivery-v4/push-verification.json')]
    evidence += [ref(BASE / 'remaining-operations.json', 'All 150 nonpassing obligations'), ref(Path(__file__), 'Refresh logic')]
    write(BASE / 'program-review.json', dict(status='pass_for_consistency_not_completion', recorded=351, proposal_operations=376, nonpassing=150, ready=len(ready), evidence=evidence, protected_historical_hashes=hashes, visual_acceptance=False, final_acceptance=False))
    old = current.read_text()
    gaps = old[old.index('## Remaining gaps and routes'):old.index('## Execution and recovery')]
    continuation = '''Continue later-evidence reconciliation for the other 102 software/reuse trace
rows. R panel work targets nonabsorbing, multiple-event, stacked, panel-approach
and trend-weighting leads plus remaining delegates. Java successors target the
nested review's exact origin, helper, artifact, rights and conversion gaps.
Do not repeat completed acquisitions or the 48-case fixture. Unknown bank truth
and unrestricted latent/dependent inference need new information or research.
Public proposal work remains eligible independently of later bank trials.
Fresh visual acceptance requires a new image allowance. No unattended research
worker is running; checkpoints retain exact actions, not completion claims.'''
    summary = f'''The current monograph has {reader['pages']:,} pages, 1,438 audited citation
records and 274 genuine scholarly PDFs. The exact paired sponsor has
{sponsor['pages']} pages and 1,103 records. All 1,436 reader and 1,099 sponsor
predecessor citation records survive, with reader contexts and compiled inputs
preserved. Q2-Q4 exact-byte author checks pass; Q1/Q5, coverage/depth, fresh
visual review and final acceptance remain open.

351/376 original operations are recorded; 150 are nonpassing: 121 inconclusive,
25 open and four negative. Software remains 3 passing, 98 inconclusive and
1 open; reuse 109 passing, 4 inconclusive and 2 open. The inherited frontier
census remains 82 inspected and 31 unread. Zero original ready work is not completion.

The recovered publication was committed and pushed as
682c1f2a41b8a29f45219d710371c7179b6e24c3. Its custody audit failures and verified
repairs remain preserved. The 48-case local fixture and seven Aitiotita delegates
remain integrated. Twenty additional pinned BLIP/Spot originals now add precise
source findings, endpoint identity witnesses, prior sensitivity and conditional
reuse decisions. No acquired engine, Java binary or setup script was executed.
The two-row Java/R tail reconciliation preserves later Weka/Banjo/Tetrad work.
'''
    current.write_text(f'''# Current executable proposal program

Updated 28 October 2026. [Live master](../master-live.md),
[program review](2026-10-28/{BASE.name}/program-review.json), and
[all unresolved obligations](2026-10-28/{BASE.name}/remaining-operations.json).

The program develops a source-grounded banking research and product proposal.
Software/reuse, LLM/agent and CLI/MCP repairs are mandatory. Public evidence and
synthetic fixtures justify later costly experiments; source review, native
implementation, independent acceptance and bank adoption remain distinct.

Use python3 tools/run_followup_program_v2_20261028.py status, next and check.
Original controllers retain integrity and acceptance. Independent eligible
work continues across phase boundaries; local blockers stay local.

## Current integrated documents

[Monograph](../../{Path(reader['pdf']['path']).name}) and
[paired sponsor](../../{Path(sponsor['pdf']['path']).name}).

{summary}
{gaps}## Execution and recovery

Both historical master files retain exact bytes. Mutable dashboards use saved
snapshots for evidence. Failed builds and audit repairs remain recorded.

## Exact continuation

{continuation}
''')
    live.write_text(f'''# Current master program: causal banking proposal

Updated 28 October 2026. [Executable program](execution/current-program.md) and
[all 150 unresolved obligations](execution/2026-10-28/{BASE.name}/remaining-operations.json)
govern continuation. V11 and the earlier recovery pointer remain historical.

The standard is a connected scholarly argument from banking questions through
assumptions, identification, estimation, uncertainty, diagnostics, alternatives
and monetary consequences. Genuine local scholarly PDFs, exact primary software
identities, hashes and anchors, reproducible examples and rendered inspection
are required. FinMarketing is an exposition standard, not a length target.
Software coverage, LLM/agent frontiers and CLI/MCP integration remain mandatory.

[Current monograph](../{Path(reader['pdf']['path']).name}) and
[paired sponsor](../{Path(sponsor['pdf']['path']).name}).

{summary}
{continuation}
''')
    controller.render(ROOT, state)
    mission = ROOT / 'docs/mission-control.md'
    text = mission.read_text()
    start, end = text.index('Current entrypoint:'), text.index('Public design outcomes:')
    text = text[:start] + '[Current master program](program/master-live.md).\n\nCurrent work: python3 tools/run_followup_program_v2_20261028.py status, next, check.\n\n**351/376 recorded; 150 nonpassing.** Zero-ready is not completion.\n\n' + text[end:]
    text += f'\n[Current paired sponsor]({Path(sponsor["pdf"]["path"]).name}) — {sponsor["pages"]} pages.\n'
    mission.write_text(text)
    html = subprocess.run(['pandoc', '--from=gfm', '--to=html'], input=text, text=True, capture_output=True, check=True, timeout=20).stdout
    (ROOT / 'docs/mission-control.html').write_text('<!doctype html><meta charset="utf-8"><title>Causal proposal execution</title>' + html)
    assert hashes == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    write(BASE / 'continuation-checkpoint.json', dict(reader=state['reader'], sponsor=sponsor['pdf'], evidence=evidence, next_action='Consume both unchanged full-controller exits and record publication; continue explicit independent source-tail routes.', visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(recorded=351, nonpassing=150, reader_pages=reader['pages'], sponsor_pages=sponsor['pages'], protected_master_bytes_unchanged=True)))


if __name__ == '__main__':
    main()
