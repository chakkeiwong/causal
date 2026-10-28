"""Reconcile the preserved obligations and name precise next independent work."""
import copy,json
from collections import Counter
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings

ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'program-refresh-delegate-contract-v1';PRIOR=DAY/'program-refresh-openai-contract-v1'
def read(p):return json.loads(p.read_text())


def main():
    assert not BASE.exists();run=controller.base;state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    view=controller.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
    results=merged['execution_program']['results']
    reader=read(DAY/'delegate-contract-reader-v1/working-release.json');sponsor=read(DAY/'sponsor-delegate-contract-v1/working-release.json')
    for obj in [reader,sponsor]:verify_bindings(obj)
    assert run.same_reader(state['reader'],reader['pdf']) and run.same_reader(state['reader'],sponsor['paired_monograph'])
    remaining=copy.deepcopy(read(PRIOR/'remaining-operations.json'))
    ids={n['id'] for n in graph['nodes'] if stages[n['id']]=='proposal_now' and results.get(n['id'],{}).get('outcome')!='pass'}
    assert ids=={r['id'] for r in remaining['operations']} and len(ids)==150
    for r in remaining['operations']:
        if r['id']=='TEXT.REVIEW.L6':
            b=results[r['id']];receipt=read(ROOT/b['path']);r.update(action=receipt['revisit_trigger'],evidence=b,action_basis=b)
    remaining.update(reader=state['reader'],ready=len(ready),predecessor=ref(PRIOR/'remaining-operations.json','All unresolved operations retained'))
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view);write(BASE/'remaining-operations.json',remaining)
    action='Install a reviewed durable followup queue without rewriting historical outcomes; reconcile named L6 service/artifact profiles and L1 task-specific essentiality independently. Preserve the completed 29-file review.'
    write(BASE/'scheduler-review.json',dict(status='control_eligibility_gap',ready_count=len(ready),observation='Original scheduler excludes recorded operations even when explicit successor work remains.',route=action,evidence=[ref(PRIOR/'scheduler-review.json','Previously observed queue gap')]))
    write(BASE/'program-review.json',dict(status='pass_for_consistency_not_completion',recorded=351,proposal_operations=376,ready=len(ready),nonpassing=150,outcome_counts=dict(Counter(results.get(r['id'],{}).get('outcome','open') for r in remaining['operations'])),evidence=[ref(BASE/'remaining-operations.json','Complete remaining register'),ref(DAY/'l6-delegate-criterion-v1/operation-receipt.json','Finite review successor'),ref(DAY/'delegate-contract-reader-v1/working-release.json','Exact reader'),ref(DAY/'sponsor-delegate-contract-v1/working-release.json','Exact paired sponsor'),ref(Path(__file__),'Reconciliation')],visual_acceptance=False,final_acceptance=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    text=current.read_text().replace('program-refresh-openai-contract-v1/','program-refresh-delegate-contract-v1/')
    a=text.index('## Current integrated documents');b=text.index('## Remaining gaps and routes')
    section=f'''## Current integrated documents

The [monograph](../../causal_proposal_delegate_contract_reviewed_v1_2026-10-28.pdf) has {reader['pages']:,} pages,
1,415 audited citation records and 271 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../sponsor_proposal_delegate_contract_reviewed_2026-10-28.pdf) has {sponsor['pages']} pages and 1,068 citations.
All 1,403 predecessor records, citation contexts and compiled content inputs survive.
Source traceability, exact authored examples and all-page text/bounds checks pass; Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open.

**351 recorded outcomes of 376; {len(ready)} ready original operations; 150 nonpassing obligations.**
Software remains three pass / 98 inconclusive / one open; reuse 109 pass / four inconclusive / two open.
The nonpassing total is 121 inconclusive, 25 open and four negative. These are dispositions, not qualified capabilities.

## Completed recovery and new findings

The recovered 1,734-page reader and 161-page sponsor were committed and pushed as 19513afff0f47b8928c31bc7dc6a7c3848b28851.
Its actual delivery exit was consumed and HEAD/origin verified before the next publication.

The finite census review remains recorded inconclusive: 82 inspected / 31 unread inherited candidates,
95 later rows with 79 metadata identities, 16 duplicates and 66 acquisition/edition obligations.
These denominators are not additive. The candidate 214 selected-author-original correction remains preserved.

The new comparison resolves the finite 29-file worklist:23 technical files and 6 scope-only documents.
Exact source identity, cutoff pins, SHA-256, Git blobs and inspected anchors are recorded.
The argument distinguishes conditional tool validation, terminal events, retry scope, compaction costs,
schema-conversion warnings, native stop reasons, recovery identities and learned-program evaluation.
Exact authored witnesses give five versus nine attempts and stipulated USD 1.25 versus USD 2.25; they are not vendor measurements.

The [L6 matrix](2026-10-28/l6-delegate-criterion-v1/contract-matrix.json) no longer calls those 29 files inventory-only.
It preserves the ten-page exclusive minimum and the inconclusive full-coverage result.
Named service/model/artifact profiles and migration leads still need bounded dispositions.
Unlisted code branches are outside this source review; no downloaded code or live model was executed.

'''
    text=text[:a]+section+text[b:];a=text.index('## Exact continuation')
    text=text[:a]+'## Exact continuation'+chr(10)*2+action+chr(10)*2+'The unchanged original scheduler has no ready node. This is a successor-registration limitation, not proposal completion. Serialize canonical mutations, consume actual exits and verify delivery. Fresh visual review alone requires a fresh safe image allowance.'+chr(10)
    current.write_text(text);controller.render(ROOT,state)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],next_action=action,remaining=ref(BASE/'remaining-operations.json','All unresolved obligations'),visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print(json.dumps(dict(recorded=351,nonpassing=150,reader_pages=reader['pages'],sponsor_pages=sponsor['pages'])))


if __name__=='__main__':main()
