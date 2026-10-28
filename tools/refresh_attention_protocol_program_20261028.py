"""Reconcile the protocol publication without changing acceptance contracts."""
import copy
import json
from collections import Counter
from pathlib import Path

import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import load, view
from run_followup_program_v2_20261028 import selected

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'program-refresh-attention-protocol-v1'
PRIOR = DAY / 'program-refresh-attention-discovery-v1'


def read(path):
    return json.loads(path.read_text())


def main():
    assert not BASE.exists(), 'Preserve the completed refresh; use a successor.'
    run = controller.base
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    results = merged['execution_program']['results']
    reader_base = DAY / 'attention-protocol-reader-v2'
    sponsor_base = DAY / 'sponsor-attention-protocol-v2'
    reader = read(reader_base / 'working-release.json')
    sponsor = read(sponsor_base / 'working-release.json')
    for release in (reader, sponsor):
        verify_bindings(release)
    assert run.same_reader(state['reader'], reader['pdf'])
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    remaining = copy.deepcopy(read(PRIOR / 'remaining-operations.json'))
    nodes = [n for n in graph['nodes'] if stages[n['id']] == 'proposal_now']
    ids = {n['id'] for n in nodes if results.get(n['id'], {}).get('outcome') != 'pass'}
    assert len(nodes) == 376 and ids == {r['id'] for r in remaining['operations']}
    assert len(ids) == 150
    for row in remaining['operations']:
        if row['id'] in ('TEXT.REVIEW.L1', 'TEXT.REVIEW.L6'):
            binding = results[row['id']]
            receipt = read(ROOT / binding['path'])
            row.update(action=receipt['revisit_trigger'], evidence=binding, action_basis=binding)
    counts = Counter(results.get(n['id'], {}).get('outcome', 'open') for n in nodes)
    unresolved = Counter(results.get(key, {}).get('outcome', 'open') for key in ids)
    recorded = sum(n['id'] in results for n in nodes)
    assert recorded == 351 and unresolved == dict(inconclusive=121, open=25, negative=4)
    BASE.mkdir()
    remaining.update(reader=state['reader'], ready=len(ready),
                     predecessor=ref(PRIOR / 'remaining-operations.json', 'All unresolved IDs retained'))
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'remaining-operations.json', remaining)
    queue = view(load(ROOT, selected()))
    write(BASE / 'followup-snapshot.json', queue)
    fixture_base = DAY / 'public-attention-contract-v2'
    java_base = DAY / 'aitiotita-delegates-v1'
    for packet in (fixture_base, java_base):
        verify_bindings(read(packet / 'author-review.json'))
    assert read(fixture_base / 'author-review.json')['tests'] == dict(
        tests=48, failures=0, errors=0, skipped=0)
    evidence = [ref(BASE / 'remaining-operations.json', 'Complete nonpassing register'),
                ref(selected() / 'contracts.json', 'Current independent work contracts'),
                ref(reader_base / 'working-release.json', 'Exact reviewed reader'),
                ref(sponsor_base / 'working-release.json', 'Exact paired sponsor'),
                ref(fixture_base / 'author-review.json', 'Completed stronger local fixture'),
                ref(java_base / 'author-review.json', 'Seven inspected Java delegates'),
                ref(Path(__file__), 'Reconciliation logic')]
    write(BASE / 'program-review.json', dict(
        status='pass_for_consistency_not_completion', recorded=recorded,
        proposal_operations=len(nodes), nonpassing=len(ids), ready=len(ready),
        outcome_counts=dict(counts), unresolved_counts=dict(unresolved), evidence=evidence,
        followup=queue, visual_acceptance=False, final_acceptance=False))

    current = ROOT / 'docs/program/execution/current-program.md'
    (BASE / 'prior-current-program.md').write_bytes(current.read_bytes())
    old = current.read_text()
    # Retain the full gap analysis and execution diagnosis, and replace stale delivery instructions.
    a = old.index('## Remaining gaps and routes')
    b = old.index('## Recovered execution and remaining evidence')
    gaps = old[a:b]
    current.write_text(f'''# Current executable proposal program

Updated 28 October 2026. The [program review](2026-10-28/{BASE.name}/program-review.json)
and [complete nonpassing register](2026-10-28/{BASE.name}/remaining-operations.json)
reconcile all 376 original proposal obligations. Canonical state and reviewed receipts govern acceptance.
The [preserved predecessor](2026-10-28/{BASE.name}/prior-current-program.md) retains earlier findings.

The master program governs a research and product proposal for four banking journeys.
It includes software coverage and reuse, LLM and agent methods, CLI/MCP integration,
public-data prototype design, manuscript quality and the investment argument.
Public/generated evidence supports the case for later costly bank experiments.
Proposal completion is distinct from implementation, independent review, bank validation and adoption.

Use `python3 tools/run_followup_program_v2_20261028.py status`, `next` and `check`
for followup work. Original acceptance and full integrity remain governed by
`tools/causal_program.py` and `tools/run_program_checkpoint_v3.py`.
Continue independent eligible work across phases; a checkpoint is a recovery record.
There is no unattended worker. Do not edit sibling repositories or execute downloaded code.

## Current integrated documents

The [monograph](../../{Path(reader['pdf']['path']).name}) has {reader['pages']:,} pages,
1,433 audited citation records and 274 genuine scholarly PDFs.
The exact paired [sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has
{sponsor['pages']} pages and 1,094 audited citation records.
All 1,430 predecessor monograph records and all 1,089 sponsor records survive.
Source identities, citation contexts, exact authored calculations and all-page text/bounds checks pass.
Q2-Q4 are author reviews bound to these exact reader bytes. Q1/Q5, required coverage/depth,
fresh visual review and final acceptance remain open.

**{recorded} of 376 original operations recorded; {len(ready)} ready original operations;
{len(ids)} nonpassing obligations.** These comprise 121 inconclusive, 25 open and four negative outcomes.
Software remains three passing, 98 inconclusive and one open cell;
reuse remains 109 passing, four inconclusive and two open decisions.
The frontier census remains 82 inspected and 31 unread inherited originals;
later metadata and acquisition denominators remain separate.
The zero-ready original scheduler requires reviewed successors; it does not establish completion.

## Recovered protocol work

The interrupted reader passed its preserving review before publication. An undefined citation,
incorrect expected prefixes and stale sponsor counts were repaired in successors;
failed attempts remain in the evidence register.
Six pinned TCDF/TACD delegate files support the new protocol discussion.
For the declared convolution settings, non-target support is lags 0-7 and shifted-target support
is lags 1-8. All four inspected TACD profiles enter the shared training/validation branch.
Truth-assisted graph selection, threshold ties, diagonal scoring, device selection and
zero-valid denominators now have explicit proposal qualification conditions.
These are source-derived findings and selected authored fixtures, with no native performance claim.

The earlier public fixture demonstrates selected examples with truth-bearing case objects,
incomplete overlap checks and insufficient nonfinite validation. Its evidence is preserved.
The [reviewed successor](2026-10-28/public-attention-contract-v2/author-review.json)
uses truth-free immutable split identities, explicit local access boundaries, deterministic
selection and complete finite-denominator checks. All 48 adversarial test cases passed,
with no failures, errors or skips. A mistaken wrapper count expectation was preserved and
repaired by reconciling the actual JUnit cases with every declared test function.
These are trusted local API contracts, not process isolation or authentic-label verification.

The [Java delegate review](2026-10-28/aitiotita-delegates-v1/author-review.json)
binds seven Aitiotita originals to the pinned 2023 revision, inspected anchors and exact
logical witnesses. The generic Gaussian shortcut counterexample remains separate from
the bundled linguistic flow oracle. Half-vote orientation, the contradictory rule-3
endpoint condition, optional literal-p-value callback and non-enforcing low-level
preset mutations now have precise adoption/porting routes. No Java code was executed.
Both independent successor packets are reviewed source/evidence packages pending
preserving manuscript and sponsor integration; they award no original acceptance.

{gaps}
## Exact continuation

Consume and preserve both integrity-check exits and record the completed protocol packet.
Install a reviewed independent successor queue for the completed stronger fixture and
Java delegate packets, then integrate both into a preserving paired monograph and sponsor.
Deliver the scoped commit and push with exact evidence custody. Continue remaining
software/source work; do not repeat the completed 48-case run or the seven-file acquisition.
Do not repeat completed TCDF/TACD acquisition or unchanged rate-limited identity requests.
The CausalTransformer/CAMCNs original-access limits remain local omissions;
metadata and repositories do not substitute for scholarly technical originals.
Visual acceptance remains locally pending the fresh image allowance recorded under
`/home/ubuntu/AGENTS.md`; source work and public fixtures remain eligible.
''')

    master = ROOT / 'docs/program/master-program.md'
    (BASE / 'prior-master-program.md').write_bytes(master.read_bytes())
    heading = '# Integrated master program for causal banking\n'
    text = master.read_text()
    assert text.startswith(heading)
    notice = f'''
Current execution and integrated documents are governed by the
[current executable program](execution/current-program.md) and
[28 October reconciliation](execution/2026-10-28/{BASE.name}/program-review.json).
The current monograph has {reader['pages']:,} pages; 150 original proposal obligations remain nonpassing.
The V11 baseline and its dated counts below are historical evidence.

'''
    master.write_text(heading + notice + text[len(heading):])
    controller.render(ROOT, state)
    mission = ROOT / 'docs/mission-control.md'
    m = mission.read_text()
    a = m.index('Current entrypoint:')
    b = m.index('Public design outcomes:')
    m = m[:a] + f'''Current work entrypoint: `python3 tools/run_followup_program_v2_20261028.py status`, `next` and `check`.
Use the original controllers for unchanged proposal acceptance and full integrity checks.

**{recorded} / 376 original proposal operations recorded; {len(ids)} remain nonpassing.**
The zero-ready original scheduler requires reviewed successors; it does not establish completion.
The current followup queue schedules active-agent work and cannot award original acceptance.
Checkpoints and phase boundaries do not block independent eligible work.

''' + m[b:]
    mission.write_text(m)
    html = ROOT / 'docs/mission-control.html'
    if html.exists():
        h = html.read_text()
        notice = '<p>Current followup execution: tools/run_followup_program_v2_20261028.py. See current-program.md for exact continuation and all remaining obligations.</p>'
        html.write_text(h.replace('<body>', '<body>' + notice, 1) if '<body>' in h else h + notice)
    write(BASE / 'continuation-checkpoint.json', dict(
        reader=state['reader'], sponsor=sponsor['pdf'],
        next_action='Record actual check exits, finish protocol receipt, install reviewed fixture/Java successor queue, integrate both completed packets and deliver the scoped commit/push.',
        remaining=ref(BASE / 'remaining-operations.json', 'All 150 unresolved obligations'),
        queue=ref(selected() / 'contracts.json', 'Current work contracts'),
        visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(recorded=recorded, nonpassing=len(ids),
                          reader_pages=reader['pages'], sponsor_pages=sponsor['pages'])))


if __name__ == '__main__':
    main()
