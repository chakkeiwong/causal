"""Preserve chapter criteria and record exact-reader source deltas."""
import copy,json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28';run=controller.base
read=lambda p:json.loads(p.read_text())

def main():
    reader=DAY/'panel-estimators-reader-v1';release=read(reader/'working-release.json');verify_bindings(release)
    review=read(reader/'release-source-review.json');assert review['checks']['prior_citation_contexts_preserved']
    base=DAY/'panel-estimator-chapters-v1';assert not base.exists();base.mkdir()
    for chapter in ['L1','L6']:
        state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active'] is None
        assert run.same_reader(state['reader'],release['pdf'])
        graph,merged,_=run.combined(ROOT,state);op='TEXT.REVIEW.'+chapter;node=run.ledger.operation(graph,op)
        prior=merged['execution_program']['results'][op];old=read(ROOT/prior['path']);assert old['outcome']=='inconclusive'
        attempt=len(state['execution_runtime'].get('chapter_review_successors',{}).get(op,[]))+1
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        original=read(ROOT/old['outputs'][0]['path']);report=copy.deepcopy(original)
        extra=[ref(reader/'release-source-review.json','All 1447 prior records, contexts and content preserved'),ref(reader/'working-release.json','Exact current reader'),ref(DAY/'followup-runtime-v2/local-profile.json','Eleven inspected server originals with model/build limits'),ref(DAY/'followup-runtime-v2/cdt-delegates.json','Selected discovery delegates and separate comparator')]
        revisit=('Resolve the31unread original/edition identities through task-specific permitted-source routes; preserve14supported task comparisons and eight-page minimum.' if chapter=='L1' else 'Complete named model/build/runner/rights profiles and migration-lead originals; preserve inspected29framework files and11Ollama server files. No universal schema,cancellation or local-routing guarantee is inferred.')
        report.update(reviewed_reader=release['pdf'],review_attempt=attempt,revisit_trigger=revisit,visual_acceptance=False,final_acceptance=False)
        report['evidence']=original['evidence']+extra
        report['nested_source_delta']=dict(completed='Prior L1/L6 content and source identities preserved. The nine pinned estimator and conversion sources with exact support and naming witnesses add no LLM scholarly original and do not change frontier census counts.',remaining='Uninspected originals,full coverage and fresh visual acceptance remain open',substantive_page_credit=8 if chapter=='L1' else 10,new_page_credit=0)
        write(output,report)
        receipt=run.ledger.receipt_template(node);criteria=copy.deepcopy(old['criteria'])
        for c in criteria:c['evidence']=c.get('evidence',[])+extra
        if chapter=='L6':criteria[0]['finding']='The29framework-file review and11server-original profile are integrated; exact model/build/rights and full named-family coverage remain inconclusive.'
        receipt.update(execution='performed',outcome='inconclusive',scope='Exact-reader preserving '+chapter+' source delta',reviewer=dict(name='Codex author/coordinator',kind='author'),prior_result=prior,reviewed_reader=release['pdf'],review_attempt=attempt,outputs=[ref(output,'Exact-reader chapter successor')],limitations=old['limitations'],revisit_trigger=revisit,criteria=criteria)
        folder=base/chapter;folder.mkdir();write(folder/'operation-receipt.json',receipt)
        before=run.core.sha(ROOT/run.core.STATE);event=controller.previous.record_chapter(ROOT,state,op,str((folder/'operation-receipt.json').relative_to(ROOT)));run.commit(ROOT,before,state,event)
    print('L1/L6 exact-reader successors recorded; full coverage remains inconclusive.')

if __name__=='__main__':main()
