"""Refresh L1 on the current reader without waiving unread-original limits."""
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
from run_followup_program_20261028 import append,load
from run_followup_program_v2_20261028 import selected

ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
def read(p):return json.loads(p.read_text())


def main():
    base=selected();key='L1.SUCCESSOR';node=load(ROOT,base)['nodes'][key]
    source=DAY/'followup-runtime-v1/l1-essentiality.json'
    start=base/'l1-successor-start.json';write(start,dict(task=key,awards_acceptance=False,next_action=node['action'],evidence=[ref(source,'14task current claim review')]))
    append('start',key,str(start.relative_to(ROOT)),ROOT,base)
    run=controller.base;state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    current=DAY/'delegate-contract-reader-v1';release=read(current/'working-release.json');verify_bindings(release)
    assert run.same_reader(state['reader'],release['pdf'])
    oldaudit=read(ROOT/'docs/program/execution/2026-10-17/l1-review-v1/reader/source-audit.json');newaudit=read(current/'reader/source-audit.json')
    oldfiles={x['path']:x for x in oldaudit['tex_files']};newfiles={x['path']:x for x in newaudit['tex_files']}
    content=[x for x in oldaudit['tex_files'] if x['path']!='docs/causal_proposal_frontier_authors_reviewed_2026-10-17.tex']
    assert all(p['path'] in newfiles and newfiles[p['path']]['sha256']==p['sha256'] for p in content)
    oldsources={s['integrated_citation_key']:s for s in oldaudit['sources']};newsources={s['integrated_citation_key']:s for s in newaudit['sources']}
    assert all(newsources[k]==s for k,s in oldsources.items())
    oldreview=ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.L1/chapter-review.json';old=read(oldreview);assert old['substantive_page_credit']==8
    coverage=read(source);assert len(coverage['tasks'])==14 and len(coverage['unread_candidates'])==31
    graph,merged,_=run.combined(ROOT,state);op='TEXT.REVIEW.L1';contract=run.ledger.operation(graph,op);prior=merged['execution_program']['results'][op]
    assert prior['outcome']=='inconclusive'
    folder=DAY/'l1-current-criterion-v1';assert not folder.exists();folder.mkdir()
    evidence=[ref(source,'14supported comparisons and31unread identities'),ref(oldreview,'Prior eight exclusive page-equivalents'),ref(current/'reader/source-audit.json','All prior source records and compiled content preserved'),ref(current/'release-source-review.json','Current preserving source/text review'),ref(current/'working-release.json','Exact reader'),ref(Path(__file__),'Preservation and criterion logic')]
    attempt=len(state['execution_runtime'].get('chapter_review_successors',{}).get(op,[]))+1
    output=ROOT/run.review_output_paths(contract,state['reader'],attempt)[0]
    finding='Current14task comparison binds inspected evidence and distinct limits;31selected originals remain unread,including three separate journal editions with inspected related preprints. Complete frontier/essential-source coverage remains inconclusive.'
    revisit='Resolve task-specific essentiality and selected-original/edition gaps through distinct permitted originals; retain bounded integrated claims and do not repeat already inspected evidence.'
    report=dict(operation_id=op,status='inconclusive',reviewer=dict(name='Codex author/coordinator',kind='author'),reviewed_reader=release['pdf'],allocation=old['allocation'],substantive_page_credit=8,depth_basis='Prior exclusive eight-page minimum preserved byte-for-byte; no new/current page allocation claimed',preserved_compiled_inputs=len(content),preserved_source_records=len(oldsources),findings=[finding,'Current per-task support does not require native execution or authentic bank validation.'],evidence=evidence,remaining_coverage=['31selected unread originals','Task-specific essentiality and full cutoff coverage','No fresh visual/final acceptance'],revisit_trigger=revisit,visual_acceptance=False,final_acceptance=False)
    write(output,report)
    receipt=run.ledger.receipt_template(contract);receipt.update(execution='performed',outcome='inconclusive',scope='Preserving current-reader L1 coverage and existing depth review',reviewer=report['reviewer'],prior_result=prior,reviewed_reader=release['pdf'],review_attempt=attempt,outputs=[ref(output,'Exact-reader L1 successor')],limitations=['Author scope review;no independent or visual acceptance.','Eight-page minimum preserved;target9 and full MR02 not claimed.'],revisit_trigger=revisit,criteria=[dict(index=0,verdict='inconclusive',finding=finding,evidence=evidence),dict(index=1,verdict='pass',finding='All prior compiled content and source records preserved;existing eight exclusive page-equivalents remain without duplicate credit.',evidence=evidence[1:4])])
    write(folder/'operation-receipt.json',receipt)
    before=run.core.sha(ROOT/run.core.STATE);event=controller.previous.record_chapter(ROOT,state,op,str((folder/'operation-receipt.json').relative_to(ROOT)));run.commit(ROOT,before,state,event)
    out=base/'l1-successor.json';write(out,dict(status='recorded_inconclusive',operation=op,receipt=ref(folder/'operation-receipt.json','Canonical chapter successor'),reviewed_reader=release['pdf'],coverage='inconclusive',awards_acceptance=False))
    result=base/'l1-successor-receipt.json';write(result,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Performed preserving review')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='Prior source/content preserved and eight-page minimum retained.'),dict(index=1,verdict='pass',finding='Same original criteria reviewed on exact reader;full coverage remains inconclusive and no visual acceptance awarded.')],next_action='Continue independent local-server profile;later reconcile current program and source integration.'))
    append('record',key,str(result.relative_to(ROOT)),ROOT,base);print(json.dumps(dict(chapter='L1',outcome='inconclusive',inspected=82,unread=31,next=load(ROOT,base)['next'])))


if __name__=='__main__':main()
