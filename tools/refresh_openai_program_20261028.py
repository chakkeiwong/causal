"""Reconcile every proposal obligation after the finite census and provider review."""
import copy
import json
from collections import Counter
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'program-refresh-openai-contract-v1'
PRIOR = DAY / 'program-refresh-followup-causal-v1'


def read(p):
    return json.loads(p.read_text())


def main():
    assert not BASE.exists()
    run = controller.base
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    view = controller.status(ROOT, state)
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    results = merged['execution_program']['results']
    assert view['recorded_proposal_operations'] == 351 and view['proposal_operations'] == 376
    assert results['LL.CENSUS']['outcome'] == 'inconclusive'
    assert results['TEXT.REVIEW.L6']['outcome'] == 'inconclusive'
    reader = read(DAY / 'openai-contract-reader-v1/working-release.json')
    sponsor = read(DAY / 'sponsor-openai-contract-v1/working-release.json')
    assert run.same_reader(state['reader'], reader['pdf']) and run.same_reader(state['reader'], sponsor['paired_monograph'])
    for value in [reader, sponsor, read(PRIOR / 'remaining-operations.json')]:
        verify_bindings(value)
    remaining = copy.deepcopy(read(PRIOR / 'remaining-operations.json'))
    actual = {n['id'] for n in graph['nodes'] if stages[n['id']] == 'proposal_now' and results.get(n['id'], {}).get('outcome') != 'pass'}
    assert actual == {x['id'] for x in remaining['operations']} and len(actual) == 150
    for row in remaining['operations']:
        if row['id'] in ['LL.CENSUS', 'TEXT.REVIEW.L6']:
            binding = results[row['id']]
            receipt = read(ROOT / binding['path'])
            row.update(status='inconclusive', action=receipt['revisit_trigger'], evidence=binding, action_basis=binding)
            for k in ['action_checkpoint', 'corrected_action_checkpoint', 'superseded_pre_result_checkpoint']:
                row.pop(k, None)
    groups = {}
    for label, prefix, total in [('software', 'SW.CELL.', 102), ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = [v for k, v in results.items() if k.startswith(prefix)]
        groups[label] = dict(Counter(v['outcome'] for v in selected), open=total-len(selected), total=total)
    remaining.update(reader=state['reader'], recorded=351, ready=len(ready), coverage=groups,
        census=ref(DAY / 'census-criterion-review-v1/census-register.json', 'Corrected selected-source flag; 82/31 unchanged'),
        predecessor=ref(PRIOR / 'remaining-operations.json', 'All 150 unresolved obligations preserved'))
    BASE.mkdir()
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'status-snapshot.json', view)
    write(BASE / 'remaining-operations.json', remaining)
    action = ('Continue the exact acquired provider/framework delegate reviews and the bounded hosted-service/model rights profiles in the L6 matrix. '
              'The finite LL.CENSUS review is recorded inconclusive; future source/edition and essentiality work needs a reviewed successor. '
              'Do not restart completed source reads, reader/sponsor builds or the finite census audit. Fresh visual review remains separate.')
    scheduler = dict(status='control_eligibility_gap' if not ready else 'ready_work_present',
        ready_count=len(ready), next=view['next'],
        observation='Recording the last ready finite census outcome can leave the existing scheduler without a ready node, although known independent followups remain. This is a successor-registration limitation, not a scientific or global source-access blocker.',
        route='Use the already reviewed chapter-successor path for new L6 evidence; prepare an explicit reviewed operation successor before changing any other recorded contract. Do not relabel recorded outcomes as ready or pass.',
        independent_work=action)
    write(BASE / 'scheduler-review.json', scheduler)
    review = dict(status='pass_for_consistency_not_completion', evidence=[ref(BASE / 'remaining-operations.json', 'All 376 proposal obligations reconciled'),
        ref(DAY / 'openai-contract-reader-v1/working-release.json', 'Exact reader'), ref(DAY / 'sponsor-openai-contract-v1/working-release.json', 'Exact paired sponsor'),
        ref(DAY / 'census-criterion-review-v1/operation-receipt.json', 'Performed finite audit'), ref(DAY / 'l6-criterion-review-v1/operation-receipt.json', 'L6 successor'),
        ref(BASE / 'scheduler-review.json', 'Explicit queue limitation'), ref(Path(__file__), 'Reconciliation implementation')],
        recorded=351, proposal_operations=376, ready=len(ready), nonpassing=150,
        outcome_counts=dict(Counter(results.get(x['id'], {}).get('outcome', 'open') for x in remaining['operations'])),
        visual_acceptance=False, final_acceptance=False, no_global_scientific_blocker=True)
    verify_bindings(review)
    write(BASE / 'program-review.json', review)
    current = ROOT / 'docs/program/execution/current-program.md'
    (BASE / 'prior-current-program.md').write_bytes(current.read_bytes())
    text = current.read_text().replace('program-refresh-followup-causal-v1/', 'program-refresh-openai-contract-v1/')
    start = text.index('## Current integrated documents')
    end = text.index('## Remaining gaps and routes')
    section = f'''## Current integrated documents

The [monograph](../../causal_proposal_openai_contract_reviewed_v1_2026-10-28.pdf) has {reader['pages']:,} pages,
1,403 audited citation records and 271 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../sponsor_proposal_openai_contract_reviewed_2026-10-28.pdf) has {sponsor['pages']} pages and 1,054 citations.
All 1,400 predecessor records, citation contexts and 413 compiled content inputs survive.
Source traceability, exact authored examples and all-page text/bounds checks pass; Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open.

**351 recorded outcomes of 376; {len(ready)} ready; 150 nonpassing obligations.**
Software remains three pass / 98 inconclusive / one open; reuse 109 pass / four inconclusive / two open.
The nonpassing total is 121 inconclusive, 25 open and four negative outcomes. These are dispositions, not qualified capabilities.

## Completed recovery and new findings

The prior 1,732-page reader and 161-page sponsor were committed and pushed as 9cfd20d38276b355b0cb45e59b99e01840964fa7.
The actual publication process exit was consumed before changing the source manifest or starting this publication.

The finite [census review](../../program/comprehensive-v14/work/LL.CENSUS/search-closure.json) now has a recorded inconclusive result.
Its bounded search-route criterion passes; essential-source and full task coverage remain inconclusive.
All 113 inherited candidates and 95 later rows retain task mappings and claim restrictions: 82 inspected / 31 unread,
79 later metadata identities, 16 duplicates and 66 acquisition/edition obligations. These denominators are not additive.
The stale candidate214 technical-review flag was corrected without asserting final-edition equivalence or native replication.

The new provider section integrates twelve exact Git-blob-verified official OpenAI files from two cutoff-pinned repositories.
It separates completion, schema validation, scientific identification, refusal, message phases and nested retries.
The stipulated six-attempt, USD1.50 and 33-second examples reproduce; they are not vendor prices or measured performance.
Official live-guide Markdown routes still return403; their failures remain preserved. The repository originals establish narrower contracts.

The [L6 contract matrix](2026-10-28/l6-criterion-review-v1/contract-matrix.json) records six named provider/client families,
six additional framework source profiles, scientific-envelope design, rights boundaries and preserved minimum depth.
L6 remains inconclusive because hosted-service/model profiles and material acquired delegates still need explicit review.
Native trials, later bank qualification and visual acceptance remain separate from literature disposition.

'''
    text = text[:start] + section + text[end:]
    text = text.replace('Census remains 82 inspected / 31 unread plus four crosscutting tasks.', 'Census has a recorded finite review; 82 inspected / 31 unread and four separate crosscutting tasks remain explicit.')
    start = text.index('## Exact continuation')
    text = text[:start] + '## Exact continuation' + chr(10)*2 + action + chr(10)*2 + (
        'The current scheduler has no ready original operation after the last finite audit is recorded. '
        'This does not mean the proposal is complete: use reviewed successors for the known independent followups. '
        'The chapter-successor mechanism is available; do not weaken prerequisites or silently reopen historical results.' + chr(10)*2 +
        'Serialize canonical mutations, consume actual process exits, and verify commit/push before the next publication. '
        'Preserve failures and immutable originals. Phase boundaries are not permission gates.' + chr(10))
    current.write_text(text)
    controller.render(ROOT, state)
    write(BASE / 'continuation-checkpoint.json', dict(reader=state['reader'], sponsor=sponsor['pdf'], next_action=action,
        remaining=ref(BASE / 'remaining-operations.json', 'All unresolved operations'), scheduler=ref(BASE / 'scheduler-review.json', 'Explicit eligibility limitation'),
        visual_acceptance=False, final_acceptance=False, background_worker_running=False))
    print(json.dumps(dict(recorded=351, ready=len(ready), nonpassing=150, reader_pages=reader['pages'], sponsor_pages=sponsor['pages'])))


if __name__ == '__main__':
    main()
