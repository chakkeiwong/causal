"""Refresh canonical-facing program and retain the complete unresolved register."""
import copy,json
from collections import Counter
from pathlib import Path
import run_program_checkpoint_v3 as controller
from run_followup_program_v2_20261028 import selected
from run_followup_program_20261028 import load,view
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'program-refresh-attention-discovery-v1';PRIOR=DAY/'program-refresh-rl-discovery-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();run=controller.base;state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph,merged,stages,ready,_=run.queue(ROOT,state);results=merged['execution_program']['results']
    reader=read(DAY/'attention-discovery-reader-v1/working-release.json');sponsor=read(DAY/'sponsor-attention-discovery-v1/working-release.json')
    for obj in [reader,sponsor]:verify_bindings(obj)
    assert run.same_reader(state['reader'],reader['pdf']) and run.same_reader(state['reader'],sponsor['paired_monograph'])
    remaining=copy.deepcopy(read(PRIOR/'remaining-operations.json'))
    ids={n['id'] for n in graph['nodes'] if stages[n['id']]=='proposal_now' and results.get(n['id'],{}).get('outcome')!='pass'}
    assert ids=={r['id'] for r in remaining['operations']} and len(ids)==150
    for row in remaining['operations']:
        if row['id'] in ['TEXT.REVIEW.L1','TEXT.REVIEW.L6']:
            binding=results[row['id']];receipt=read(ROOT/binding['path']);row.update(action=receipt['revisit_trigger'],evidence=binding,action_basis=binding)
    remaining.update(reader=state['reader'],ready=len(ready),predecessor=ref(PRIOR/'remaining-operations.json','All150unresolved operations retained'))
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'remaining-operations.json',remaining)
    queue=view(load(ROOT,selected()));write(BASE/'followup-snapshot.json',queue)
    evidence=[ref(BASE/'remaining-operations.json','Complete remaining register'),ref(selected()/'contracts.json','Current independent followup contracts'),ref(DAY/'attention-discovery-reader-v1/working-release.json','Exact reader'),ref(DAY/'sponsor-attention-discovery-v1/working-release.json','Paired sponsor'),ref(Path(__file__),'Reconciliation logic')]
    write(BASE/'program-review.json',dict(status='pass_for_consistency_not_completion',recorded=351,proposal_operations=376,ready=len(ready),nonpassing=150,outcome_counts=dict(Counter(results.get(r['id'],{}).get('outcome','open') for r in remaining['operations'])),evidence=evidence,followup=queue,visual_acceptance=False,final_acceptance=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    text=current.read_text().replace('program-refresh-rl-discovery-v1/','program-refresh-attention-discovery-v1/')
    text=text.replace('causal_proposal_rl_discovery_reviewed_v1_2026-10-28.pdf','causal_proposal_attention_discovery_reviewed_v1_2026-10-28.pdf').replace('sponsor_proposal_rl_discovery_reviewed_2026-10-28.pdf','sponsor_proposal_attention_discovery_reviewed_2026-10-28.pdf')
    text=text.replace('1,745 pages',f"{reader['pages']:,} pages").replace('1,423 audited','1,430 audited').replace('164 pages and 1,080 citations',f"{sponsor['pages']} pages and 1,089 citations").replace('All 1,418 predecessor','All 1,423 predecessor')
    text=text.replace('Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.','Use python3 tools/run_followup_program_v2_20261028.py status, next and check for current followup work. Original acceptance and integrity remain governed by python3 tools/run_program_checkpoint_v3.py and tools/causal_program.py. Continue independent branches across phases.')
    a=text.index('## Recovered continuation and current delta')
    text=text[:a]+"""## Recovered continuation and current delta

The pending RL publication is committed and pushed as
900c119826780a089cc2f55890402f35804a5f3c. Its actual delivery exit and
HEAD/origin equality were verified before publishing this successor.
Batch4 completed all three independent packets. Batch5 has separate attention
publication, TCDF delegate, TACD protocol and unavailable-original routes.
A local source limit does not block another ready branch.

The current reader preserves all1423 prior citation records and adds seven:
one genuine Liu2026 preprint, four selected attention discovery source profiles,
the pinned CDT installer and an independent exact permutation reference.
There are274 genuine scholarly PDFs. Six finite queries returned28 distinct
repository metadata leads and20 scholarly metadata leads; these denominators
are separate and do not establish saturation. Two unavailable scholarly originals
remain in the bound omissions register, without substitute summaries.

The connected argument separates predictive graphs from interventions and
qualifies distribution preservation under permutation. An exact witness preserves
marginal counts while changing covariance1/4to-1/4, fixed-predictor MSE0to1 and
temporal agreement2/3to0; a stipulated common-cause intervention effect remains0.
Selected static source findings concern CAMCNs namespace definitions, TACD
truth-assisted selection and empty-denominator/split branches, CausalTransformer
figure-only reproduction and missing TeX inputs, and CDT mutable dependencies.
No acquired code was executed, and no native benchmark failures are claimed.

L1/L6 full coverage, the31 unread LLM originals, all150 original nonpassing
obligations and fresh visual/final acceptance remain open. New discovery sources
do not silently close unrelated census or software acceptance obligations.

## Exact continuation

Consume the actual publication/check exit and verify the scoped commit/push.
Continue the independent TCDF, TACD and original-source work in batch5. Record
precise source/evaluation protocols and integrate subsequent findings in a
preserving successor; do not rerun completed acquisitions or historical receipts.
The followup controller schedules active-agent work, not an unattended worker.
Fresh visual review remains locally limited by the exhausted image allowance.
"""
    text=text.replace('273 genuine scholarly PDFs','274 genuine scholarly PDFs');current.write_text(text);controller.render(ROOT,state)
    mission=ROOT/'docs/mission-control.md';m=mission.read_text();start=m.index('Current entrypoint:');end=m.index('Public design outcomes:')
    m=m[:start]+'''Current work entrypoint: python3 tools/run_followup_program_v2_20261028.py status, next and check.
Use the original controllers for unchanged proposal acceptance and full integrity checks.

**351 /376 original proposal operations recorded;150 remain nonpassing.**
The original scheduler has zero ready nodes because recorded inconclusive outcomes
need successors. The reviewed followup queue supplies concrete independent packets;
its current phase does not award proposal acceptance. See the linked current program.

'''+m[end:];mission.write_text(m)
    html=ROOT/'docs/mission-control.html'
    if html.exists():
        h=html.read_text();notice='<p><strong>Current followup work:</strong> python3 tools/run_followup_program_v2_20261028.py status. Original zero-ready count is not completion; see current-program.md for independent packet execution.</p>'
        h=h.replace('<body>','<body>'+notice,1) if '<body>' in h else h+notice
        html.write_text(h)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],next_action='Consume full-check exit,commit/push,continue TCDF/TACD/original-source packets without phase stopping.',remaining=ref(BASE/'remaining-operations.json','All150unresolved obligations'),queue=ref(selected()/'contracts.json','Current work contracts'),visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(recorded=351,nonpassing=150,reader_pages=reader['pages'],sponsor_pages=sponsor['pages'],queue=queue['next'])))

if __name__=='__main__':main()
