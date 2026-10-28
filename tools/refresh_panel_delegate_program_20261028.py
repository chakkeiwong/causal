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
BASE = DAY / 'program-refresh-panel-delegates-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    run = controller.base
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    results = merged['execution_program']['results']
    reader = read(DAY / 'panel-delegates-reader-v1/working-release.json')
    sponsor = read(DAY / 'sponsor-panel-delegates-v1/working-release.json')
    for item in (reader, sponsor):
        verify_bindings(item)
    assert run.same_reader(state['reader'], reader['pdf'])
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    nodes = [n for n in graph['nodes'] if stages[n['id']] == 'proposal_now']
    unresolved = {n['id'] for n in nodes if results.get(n['id'], {}).get('outcome') != 'pass'}
    prior = DAY / 'program-refresh-panel-designs-v1/remaining-operations.json'
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
            row.update(later_source_delta=ref(DAY / 'panel-delegates-v1/review.json', 'Ten additional pinned delegates and exact adapter witnesses'),
                       corrected_continuation='Retain exact Roth v2, Tsai v3, NBER stacked original and five pinned candidate identities. The selected fastdid target-first branch matches the Appendix anchor; later paper edition and M>=3 proof remain. Retain ten inspected delegates. Inspect final nuisance/bootstrap, tidier, alias, leaps and test paths; preserve supported cells, intervals and original row clocks. Obtain remaining genuine pampe, Synth and trend-weighting originals. Run candidate-specific support/weight/rights checks before native qualification.')
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
        ('panel-delegates-reader-v1/working-release.json', 'sponsor-panel-delegates-v1/working-release.json',
         'panel-delegates-v1/review.json', 'panel-delegates-v1/remaining-obligations.json', 'panel-originals-v1/omissions-register.json', 'continuation-inventory-v1/author-review.json',
         'python-continuation-recovery-v1/author-review.json', 'python-continuation-recovery-v1/reference-replay.json',
         'panel-lead-reconciliation-v1/author-review.json', 'cxx-tail-reconciliation-v1/author-review.json',
         'panel-design-delivery-v2/push-verification.json')]
    evidence += [ref(BASE / 'remaining-operations.json', 'All original gaps retained'), ref(Path(__file__), 'Exact refresh logic')]
    write(BASE / 'program-review.json', dict(status='pass_for_consistency_not_completion', recorded=351,
        proposal_operations=376, nonpassing=150, software_reuse_rows=105, evidence=evidence,
        protected_historical_hashes=hashes, visual_acceptance=False, final_acceptance=False))
    summary = f'''The current monograph has {reader['pages']:,} pages, 1,447 audited citation
records and 277 genuine scholarly PDFs. Its paired sponsor has {sponsor['pages']}
pages and 1,118 records. All 1,445 reader and 1,114 sponsor predecessor records,
reader citation contexts and compiled inputs remain. Q2-Q4 exact-reader author
checks pass; Q1/Q5, complete coverage/depth, visual and final acceptance remain open.

351/376 original operations are recorded. All 150 nonpassing obligations remain:
121 inconclusive, 25 open and four negative. Software is 3 passing, 98 inconclusive
and 1 open; reuse is 109 passing, 4 inconclusive and 2 open. The frontier census
remains 82 inspected and 31 unread. A finite source packet is not full completion.

The verified predecessor commit is 47c2a6bc23031c29e7763bbdbdf47c61a36de904.
Recovery retained all earlier evidence. The continuation inventory includes 105
software/reuse rows; four have bounded later deltas and 101 still need semantic
reconciliation. Two historical authored-reference hashes remain explicitly
mismatched, with a separately passing current replay. Controller checks do not
claim recursive historical closure.

The preceding panel publication reviewed three genuine originals and eleven pinned
identity/example files. Ten further delegates now establish selected event-order,
donor-intersection, influence transformation, validation and wrapper contracts.
The target-first code uses the Appendix base anchor; paper-edition and broader
multiple-event proof limits remain. Independent exact examples expose unbalanced
triangular counts, numeric-date inclusion, donor composition and lost pampe row
clocks. No acquired package ran, and no canonical coverage outcome is upgraded.
'''
    continuation = '''Use python3 tools/run_followup_program_v2_20261028.py status, next and check.
Consume actual exits once. Delegate and stack-fixture work are independent;
publication depends only on these reviewed inputs. Do not repeat the three
panel originals, eleven earlier identity/example files or ten delegate originals.

Next: inspect fastdid final estimate_did/nuisance and BMisc bootstrap dependencies,
option combinations, interior cohort support and M>=3 proof edition. Inspect
nonabsdid aliases, data resolution, event tidiers and upstream packages; retain
native interval provenance. Inspect exact leaps selector and original pampe
papers; preserve supplied row indices and distinguish fixed-subset sensitivity
from repeated model selection. Test declared balanced R/Stata stack profiles and
resolve concrete rights terms. These are proposal contracts, not a product build.

Pampe, Synth and trend-weighting genuine originals still need authentic permitted
source routes. Other software/reuse reconciliation, Java/C++ source/rights and
31 unread frontier-original routes remain independently eligible. Bank assignment,
unrestricted latent/dependent uncertainty and adoption need new information or
justified restrictions; no universal repair is promised.

The six-image allowance is exhausted, so fresh rendered visual acceptance remains
open locally. Public proposal work does not wait for bank validation. No unattended
research worker runs. Checkpoints retain actions, evidence and actual failures.
'''
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
    (ROOT / 'docs/program/execution/current-program.md').write_text(current.rstrip() + chr(10))
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
    live = ROOT / 'docs/program/master-live.md'
    live.write_text(live.read_text().rstrip() + chr(10))
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
        next_action='Consume unchanged controller exits; close finite delegate publication and continue remaining nuisance/bootstrap/tidier/original-source obligations.',
        visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(recorded=351, nonpassing=150, reader_pages=reader['pages'], sponsor_pages=sponsor['pages'], protected_master_bytes_unchanged=True)))


if __name__ == '__main__':
    main()
