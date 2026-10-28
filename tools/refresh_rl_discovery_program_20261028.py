"""Refresh canonical-facing program and retain the complete unresolved register."""
import copy,json
from collections import Counter
from pathlib import Path
import run_program_checkpoint_v3 as controller
from run_followup_program_v2_20261028 import selected
from run_followup_program_20261028 import load,view
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'program-refresh-rl-discovery-v1';PRIOR=DAY/'program-refresh-boundary-profile-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();run=controller.base;state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph,merged,stages,ready,_=run.queue(ROOT,state);results=merged['execution_program']['results']
    reader=read(DAY/'rl-discovery-reader-v1/working-release.json');sponsor=read(DAY/'sponsor-rl-discovery-v1/working-release.json')
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
    evidence=[ref(BASE/'remaining-operations.json','Complete remaining register'),ref(selected()/'contracts.json','Current independent followup contracts'),ref(DAY/'rl-discovery-reader-v1/working-release.json','Exact reader'),ref(DAY/'sponsor-rl-discovery-v1/working-release.json','Paired sponsor'),ref(Path(__file__),'Reconciliation logic')]
    write(BASE/'program-review.json',dict(status='pass_for_consistency_not_completion',recorded=351,proposal_operations=376,ready=len(ready),nonpassing=150,outcome_counts=dict(Counter(results.get(r['id'],{}).get('outcome','open') for r in remaining['operations'])),evidence=evidence,followup=queue,visual_acceptance=False,final_acceptance=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    text=current.read_text().replace('program-refresh-boundary-profile-v1/','program-refresh-rl-discovery-v1/')
    text=text.replace('causal_proposal_boundary_profile_reviewed_v2_2026-10-28.pdf','causal_proposal_rl_discovery_reviewed_v1_2026-10-28.pdf').replace('sponsor_proposal_boundary_profile_reviewed_v2_2026-10-28.pdf','sponsor_proposal_rl_discovery_reviewed_2026-10-28.pdf')
    text=text.replace('1,742 pages',f"{reader['pages']:,} pages").replace('1,418 audited','1,423 audited').replace('163 pages and 1,073 citations',f"{sponsor['pages']} pages and 1,080 citations").replace('All 1,415 predecessor','All 1,418 predecessor')
    text=text.replace('Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.','Use python3 tools/run_followup_program_v2_20261028.py status, next and check for current followup work. Original acceptance and integrity remain governed by python3 tools/run_program_checkpoint_v3.py and tools/causal_program.py. Continue independent branches across phases.')
    a=text.index('## Recovered continuation and current delta')
    text=text[:a]+'''## Recovered continuation and current delta

The durable followup queue now governs concrete work rather than repeating the
original scheduler zero-ready result. Batches1-3 completed five,four and three
finite work packets. Current work separates publication,attention-family search
and the remaining CDT installer-source review. Independent routes do not wait
for another route's local access limit. No unattended research worker is implied.

The current reader preserves all1418previous citation records and adds five:
two genuine primary RL/CORL papers,eight selected gCastle source files,ten CDT
dependency/interpreter originals,and an independent exact reference. The paper
count is273. The source argument separates score search from identification and
qualifies a non-strict cycle-penalty condition:an optimal DAG and objective value
can survive while a cyclic minimizer ties. Strict domination or a justified
acyclic tie rule addresses that narrow conclusion,not global learning success.

The selected source review records CORL keyword-mask lookup,RL positive-penalty
attribute naming,order/pruning/transpose semantics and attention/evaluation
contracts. These are static findings; no third-party code was executed. CDT
manifests are unpinned and do not determine a historical resolved environment.
Six public/generated fixture classes specify identity,permutation,score,failure,
interruption and numerical checks before native enablement.

L1/L6 remain inconclusive for full coverage. Prior14task comparisons,31unread
LLM-causality originals and existing exclusive depth remain preserved. Newly
reviewed discovery papers do not silently remove unrelated census obligations.

## Exact continuation

Run python3 tools/run_followup_program_v2_20261028.py status and check. Consume
actual publication/check exits and verify commit/push before the next publication.
Continue the independent attention-family search and CDT installer-source review
from exact contracts; preserve already inspected papers and source delegates.
Register the next bounded successors from their findings. Zero ready original
nodes is not proposal completion. Fresh visual acceptance alone requires a
fresh safe image allowance.
'''
    text=text.replace('271 genuine scholarly PDFs','273 genuine scholarly PDFs');current.write_text(text);controller.render(ROOT,state)
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
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],next_action='Consume actual full-check exit,commit/push then execute attention and installer packets.',remaining=ref(BASE/'remaining-operations.json','All150unresolved obligations'),queue=ref(selected()/'contracts.json','Current work contracts'),visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(recorded=351,nonpassing=150,reader_pages=reader['pages'],sponsor_pages=sponsor['pages'],queue=queue['next'])))

if __name__=='__main__':main()
