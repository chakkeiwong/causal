"""Refresh canonical-facing program and retain the complete unresolved register."""
import copy,json
from collections import Counter
from pathlib import Path
import run_program_checkpoint_v3 as controller
from run_followup_program_v2_20261028 import selected
from run_followup_program_20261028 import load,view
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'program-refresh-boundary-profile-v1';PRIOR=DAY/'program-refresh-delegate-contract-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();run=controller.base;state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph,merged,stages,ready,_=run.queue(ROOT,state);results=merged['execution_program']['results']
    reader=read(DAY/'boundary-profile-reader-v2/working-release.json');sponsor=read(DAY/'sponsor-boundary-profile-v2/working-release.json')
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
    evidence=[ref(BASE/'remaining-operations.json','Complete remaining register'),ref(selected()/'contracts.json','Current independent followup contracts'),ref(DAY/'boundary-profile-reader-v2/working-release.json','Exact reader'),ref(DAY/'sponsor-boundary-profile-v2/working-release.json','Paired sponsor'),ref(Path(__file__),'Reconciliation logic')]
    write(BASE/'program-review.json',dict(status='pass_for_consistency_not_completion',recorded=351,proposal_operations=376,ready=len(ready),nonpassing=150,outcome_counts=dict(Counter(results.get(r['id'],{}).get('outcome','open') for r in remaining['operations'])),evidence=evidence,followup=queue,visual_acceptance=False,final_acceptance=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    text=current.read_text().replace('program-refresh-delegate-contract-v1/','program-refresh-boundary-profile-v1/')
    text=text.replace('causal_proposal_delegate_contract_reviewed_v1_2026-10-28.pdf','causal_proposal_boundary_profile_reviewed_v2_2026-10-28.pdf').replace('sponsor_proposal_delegate_contract_reviewed_2026-10-28.pdf','sponsor_proposal_boundary_profile_reviewed_v2_2026-10-28.pdf')
    text=text.replace('1,739 pages',f"{reader['pages']:,} pages").replace('1,415 audited','1,418 audited').replace('162 pages and 1,068 citations',f"{sponsor['pages']} pages and 1,073 citations").replace('All 1,403 predecessor','All 1,415 predecessor')
    text=text.replace('Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.','Use python3 tools/run_followup_program_v2_20261028.py status, next and check for current followup work. Original acceptance and integrity remain governed by python3 tools/run_program_checkpoint_v3.py and tools/causal_program.py. Continue independent branches across phases.')
    a=text.index('## Exact continuation');text=text[:a]+'''## Recovered continuation and current delta

The durable followup queue now exists. Batch1 completed five reconciliation packets;
batch2 completed four source/review packets. These work results do not change the376
original acceptance obligations. The current batch has independent publication,
Python RL/CORL source-tail and CDT dependency packets. A completed/inconclusive
packet does not stop another branch. No unattended research worker is implied.

The current reader integrates three new audited records: the selected CDT delegates
and separate pcalg comparator, eleven pinned Ollama server originals, and independent
variable-order/stream-admission witnesses. All prior records and content survive.
The first build failed on an overfull commit identifier; its immutable failure is
preserved and the successor changes only the permissible line break.

L1 retains14supported task comparisons,31unread originals and an eight-page exclusive
minimum. L6 retains its29-file delegate review and ten-page minimum, and now records
the server's routing,streaming,model-residency and rights boundaries. Both exact-reader
chapter successors remain inconclusive for full coverage. Local URL,HTTP200,done and
keep_alive do not independently establish local inference,scientific admission or
durable workflow recovery. Exact build/model/dependency profiles remain separate.

## Exact continuation

Run python3 tools/run_followup_program_v2_20261028.py status and check. Consume the
current publication exit and unchanged full checks; commit and verify push before a
later publication. Then execute independent Python RL/CORL and CDT dependency packets
from their exact contracts. Reconcile their outputs into subsequent bounded work,
without repeating reviewed ENCO,gCastle PC/NOTEARS or the completed server originals.
The unchanged original scheduler's zero-ready count is not proposal completion.
Fresh visual acceptance alone requires a fresh safe image allowance.
'''
    current.write_text(text);controller.render(ROOT,state)
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
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],next_action='Consume actual full-check exit,commit/push then execute independent followup packets.',remaining=ref(BASE/'remaining-operations.json','All150unresolved obligations'),queue=ref(selected()/'contracts.json','Current work contracts'),visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(recorded=351,nonpassing=150,reader_pages=reader['pages'],sponsor_pages=sponsor['pages'],queue=queue['next'])))

if __name__=='__main__':main()
