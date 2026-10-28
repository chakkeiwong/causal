"""Refresh mutable controls after preserving publication; retain historical bytes."""
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
BASE = DAY / 'program-refresh-blip-helpers-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    run = controller.base
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    results = merged['execution_program']['results']
    reader = read(DAY / 'blip-helpers-reader-v1/working-release.json')
    sponsor = read(DAY / 'sponsor-blip-helpers-v2/working-release.json')
    for item in (reader, sponsor):
        verify_bindings(item)
    assert run.same_reader(state['reader'], reader['pdf'])
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    nodes = [n for n in graph['nodes'] if stages[n['id']] == 'proposal_now']
    unresolved = {n['id'] for n in nodes if results.get(n['id'], {}).get('outcome') != 'pass'}
    prior = DAY / 'program-refresh-nested-v1/remaining-operations.json'
    remaining = copy.deepcopy(read(prior))
    assert len(nodes) == 376 and len(unresolved) == 150
    assert unresolved == {r['id'] for r in remaining['operations']}
    assert Counter(results.get(k, {}).get('outcome', 'open') for k in unresolved) == dict(inconclusive=121, open=25, negative=4)
    for row in remaining['operations']:
        key = row['id']
        if key in ('TEXT.REVIEW.L1', 'TEXT.REVIEW.L6'):
            binding = results[key]
            row.update(action=read(ROOT / binding['path'])['revisit_trigger'], evidence=binding, action_basis=binding)
        if key == 'SW.CELL.discovery_iid.Python':
            row.update(later_source_delta=ref(DAY / 'python-continuation-recovery-v1/reconciliation.json', 'Correct stale exact-license omission and retain selected source reviews'),
                       corrected_continuation='Do not reacquire the exact causal-learn license or completed CDT/RL/attention helpers. Screen remaining aliases and original editions; declare one reproducible profile and complete terms before matched native qualification.')
        if key == 'SW.CELL.discovery_iid.Java':
            row.update(later_source_delta=ref(DAY / 'blip-helper-review-v1/review.json', 'Nine additional exact helpers and bounded witnesses'),
                       corrected_continuation='Retain Weka/Banjo/Tetrad, seven Aitiotita, twenty Spot/BLIP and nine helper originals. Repair selected DATA input progress/test assertion and declare common-row, numeric and representation contracts; inspect remaining readers/searchers/origins/rights/artifact equality.')
        if key == 'SW.CELL.discovery_iid.Cxx':
            row.update(later_source_delta=ref(DAY / 'cxx-tail-reconciliation-v1/reconciliation.json', 'Three exact candidate-group continuations'),
                       corrected_continuation='Use the three-group C++ reconciliation and exact pinned identities. Retain inspected XGES/LGES/secondary-source comparisons; obtain concrete source grants and unreviewed delegate/artifact identities without repeating unchanged failed routes.')
        if key == 'SW.CELL.panels_did.R':
            row.update(later_source_delta=ref(DAY / 'panel-lead-reconciliation-v1/lead-register.json', 'All ten metadata leads dispositioned against retained sources'),
                       corrected_continuation='Use the ten-lead panel register: four related leads have retained evidence with edition/source-type limits; six remain wholly uninspected. Acquire only genuinely missing originals and keep source identity separate from native or bank qualification.')
    protected = [ROOT / 'docs/program/master-program.md', ROOT / 'docs/program/master-current.md']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    BASE.mkdir()
    for rel, name in [('docs/program/master-live.md', 'prior-master-live.md'), ('docs/program/execution/current-program.md', 'prior-current-program.md'), ('docs/mission-control.md', 'prior-mission-control.md')]:
        (BASE / name).write_bytes((ROOT / rel).read_bytes())
    remaining.update(reader=state['reader'], ready=len(ready), predecessor=ref(prior, 'Preserved original unresolved statuses'),
        complete_continuation_inventory=ref(DAY / 'continuation-inventory-v1/continuation-register.json', '150 obligations and all 105 software/reuse rows'))
    write(BASE / 'remaining-operations.json', remaining)
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'followup-snapshot.json', view(load(ROOT, selected())))
    evidence = [ref(DAY / name, 'Verified exact current evidence') for name in
        ('blip-helpers-reader-v1/working-release.json', 'sponsor-blip-helpers-v2/working-release.json',
         'blip-helper-review-v1/review.json', 'continuation-inventory-v1/author-review.json',
         'python-continuation-recovery-v1/author-review.json', 'python-continuation-recovery-v1/reference-replay.json',
         'panel-lead-reconciliation-v1/author-review.json', 'cxx-tail-reconciliation-v1/author-review.json',
         'nested-delivery-v1/push-verification.json')]
    evidence += [ref(BASE / 'remaining-operations.json', 'All original gaps retained'), ref(Path(__file__), 'Exact refresh logic')]
    write(BASE / 'program-review.json', dict(status='pass_for_consistency_not_completion', recorded=351,
        proposal_operations=376, nonpassing=150, software_reuse_rows=105, evidence=evidence,
        protected_historical_hashes=hashes, visual_acceptance=False, final_acceptance=False))
    summary = f'''The current monograph has {reader['pages']:,} pages, 1,440 audited citation
records and 274 genuine scholarly PDFs. Its exact paired sponsor has
{sponsor['pages']} pages and 1,107 records. All 1,438 reader and 1,103 sponsor
predecessor records, reader citation contexts and compiled inputs remain.
Q2-Q4 exact-reader author checks pass. Q1/Q5, coverage/depth, fresh visual
inspection and final acceptance remain open.

351/376 original operations are recorded. All 150 nonpassing obligations remain:
121 inconclusive, 25 open and four negative. Software coverage is 3 passing,
98 inconclusive and 1 open; reuse is 109 passing, 4 inconclusive and 2 open.
The frontier census remains 82 inspected and 31 unread. Zero-ready is not completion.

The preceding publication was committed and pushed as
4d88f7ece9f0da195d1b532737f00fc7554a3a8c. Recovery repaired the continuation
inventory: 105 unresolved software/reuse rows, including an omitted commercial
cell. Four rows have bounded later deltas; 101 still need semantic reconciliation.
The exact causal-learn license omission was stale and is corrected by existing
pinned original evidence. Two historical authored-reference hashes remain
explicitly mismatched; a separate current replay preserves every earlier exact
output. Passing controller checks are not a claim of recursive historical closure.

Nine additional BLIP helper originals are now integrated. They establish precise
test, missingness/input-progress, count, representation and numerical boundaries.
The native Java engine was not executed. Earlier source reviews and the 48-case
local fixture remain preserved, with no broader capability or bank acceptance.
'''
    continuation = '''Use python3 tools/run_followup_program_v2_20261028.py status, next and check.
Consume each actual step exit once. Publication depends only on its reviewed source
addition; PANEL.LEADS and CXX.TAILS have no unrelated prerequisites. Continue the
remaining inventory using exact later-evidence deltas before acquiring originals.
The ten R-panel leads and three C++ omission groups now have performed bounded
reconciliations; register their receipts after publication without repeating them.
R-panel priorities are nonabsorbing, multiple-event, stacked, panel-approach and
trend-weighting identities plus remaining delegates. Java priorities are explicit
input/test repair, common-row scoring and remaining origin/reader/search/rights/
binary contracts. Do not repeat completed acquisitions or the 48-case fixture.

Current image allowance is exhausted; fresh visual acceptance stays local and
open. Public proposal research does not wait for bank validation. Unknown bank
assignment and unrestricted latent/dependent uncertainty require new information
or justified restrictions; no universal repair is promised. No unattended research
worker is running. Checkpoints retain exact commands rather than completion claims.'''
    old = (BASE / 'prior-current-program.md').read_text()
    gaps = old[old.index('## Remaining gaps and routes'):old.index('## Execution and recovery')]
    current = f'''# Current executable proposal program

Updated 28 October 2026. [Live master](../master-live.md),
[program review](2026-10-28/{BASE.name}/program-review.json),
[all unresolved obligations](2026-10-28/{BASE.name}/remaining-operations.json), and
[complete continuation inventory](2026-10-28/continuation-inventory-v1/continuation-guide.md).

This is a scholarly product proposal. Software/reuse, LLM/agent and CLI/MCP
coverage remain mandatory. Public and synthetic evidence justify later costly
experiments; they do not establish independent, bank or adoption acceptance.

## Current integrated documents

[Monograph](../../{Path(reader['pdf']['path']).name}) and
[paired sponsor](../../{Path(sponsor['pdf']['path']).name}).

{summary}
{gaps}## Execution and recovery

Both historical masters retain exact bytes. Prior failures, mismatches and repairs
remain recorded. Mutable controls use saved evidence snapshots.

## Exact continuation

{continuation}
'''
    (ROOT / 'docs/program/execution/current-program.md').write_text(current)
    (ROOT / 'docs/program/master-live.md').write_text(f'''# Current master program: causal banking proposal

Updated 28 October 2026. [Executable program](execution/current-program.md),
[all unresolved obligations](execution/2026-10-28/{BASE.name}/remaining-operations.json),
and [complete continuation inventory](execution/2026-10-28/continuation-inventory-v1/continuation-guide.md).

The standard is a connected banking argument from information clocks through
assumptions, identification, estimation, uncertainty, diagnostics, alternatives
and monetary consequences. Genuine local scholarly PDFs and exact primary source
identities, hashes and anchors support claims. Reproducible examples and rendered
inspection are required. FinMarketing is an exposition standard, not a length target.
Software, LLM/agent and CLI/MCP coverage remain mandatory.

[Current monograph](../{Path(reader['pdf']['path']).name}) and
[paired sponsor](../{Path(sponsor['pdf']['path']).name}).

{summary}
{continuation}
''')
    controller.render(ROOT, state)
    mission = ROOT / 'docs/mission-control.md'
    text = mission.read_text()
    start, end = text.index('Current entrypoint:'), text.index('Public design outcomes:')
    text = text[:start] + '[Current master program](program/master-live.md).\n\nCurrent work: python3 tools/run_followup_program_v2_20261028.py status, next, check.\n\n**351/376 recorded; 150 nonpassing.** Complete continuation inventory includes 105 unresolved software/reuse rows.\n\n' + text[end:]
    text += f'\n[Current paired sponsor]({Path(sponsor["pdf"]["path"]).name}) — {sponsor["pages"]} pages.\n'
    mission.write_text(text)
    html = subprocess.run(['pandoc', '--from=gfm', '--to=html'], input=text, text=True, capture_output=True, check=True, timeout=20).stdout
    (ROOT / 'docs/mission-control.html').write_text('<!doctype html><meta charset="utf-8"><title>Causal proposal execution</title>' + html)
    assert hashes == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    write(BASE / 'continuation-checkpoint.json', dict(reader=state['reader'], sponsor=sponsor['pdf'], evidence=evidence,
        next_action='Consume unchanged controller exits; close finite helper publication and execute independent panel/C++ continuations.',
        visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(recorded=351, nonpassing=150, reader_pages=reader['pages'], sponsor_pages=sponsor['pages'], protected_master_bytes_unchanged=True)))


if __name__ == '__main__':
    main()
