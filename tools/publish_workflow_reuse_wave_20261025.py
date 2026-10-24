#!/usr/bin/env python3
"""Publish reviewed Dataiku/DataRobot deltas together against the actual agent predecessor."""
import argparse,json
from pathlib import Path
import publish_datarobot_reuse_reader_v2_20261025 as final
import publish_dataiku_reuse_reader_20261025 as intermediate
import run_program_checkpoint_v3 as controller
from review_publish_observations_v2_20261022 import contexts
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings,transition
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/workflow-reuse-wave-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-25/agents-reuse-reader-v1'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=list(dict.fromkeys(final.LIMITS+intermediate.LIMITS+['Two reference dispositions published as one wave; no native integrations or capability admission.']))

def verify():
    report,last=final.verify();_,middle=intermediate.verify()
    for p in [PRIOR/'release-source-review.json',intermediate.BASE/'release-source-review.json',final.BASE/'release-source-review.json']:verify_bindings(read(p))
    old=read(PRIOR/'reader/source-audit.json');new=read(final.OUT/'source-audit.json')
    old_records={x['integrated_citation_key']:x for x in old['sources']};new_records={x['integrated_citation_key']:x for x in new['sources']}
    assert len(old_records)==1206 and len(new_records)==1209
    assert all(new_records[k]==v for k,v in old_records.items())
    assert new_records.keys()-old_records.keys()=={'exec25_dataiku_choice','exec25_datarobot_choice','exec25_datarobot_notebook'}
    old_driver='docs/causal_proposal_agents_reuse_reviewed_2026-10-25.tex';kept=[x for x in old['tex_files'] if x['path']!=old_driver];compiled={x['path']:x for x in new['tex_files']}
    assert all(compiled[x['path']]['sha256']==x['sha256'] for x in kept)
    before=contexts(read(PRIOR/'traceability-review.json'));excluded={str(intermediate.build.DEVELOPMENT.relative_to(ROOT)),str(final.build.DEVELOPMENT.relative_to(ROOT))};after=contexts(read(final.BASE/'traceability-review.json'),excluded)
    assert all(v==after[k] for k,v in before.items())
    return report,dict(preserved_citation_records=1206,added_citation_records=3,scholarly_pdfs=258,unchanged_compiled_inputs=len(kept),prior_citation_contexts_preserved=True,rendered_pages=dict(dataiku=middle['rendered_pages'],datarobot=last['rendered_pages']),native_execution=False,visual_acceptance=False)

def review():
    report,checks=verify();evidence=[ref(BASE/'plan.md','Grouped preserving execution plan'),ref(PRIOR/'release-source-review.json','Actual predecessor'),ref(intermediate.BASE/'release-source-review.json','Preserved intermediate delta'),ref(final.BASE/'release-source-review.json','Final delta'),ref(ROOT/'docs/program/execution/2026-10-25/dataiku-reuse-v1/review.json','Dataiku source decision'),ref(ROOT/'docs/program/execution/2026-10-25/datarobot-reuse-v1/review.json','DataRobot source decision'),ref(ROOT/'docs/program/execution/2026-10-25/datarobot-reuse-v1/reader-review-repair.json','Preserved anchor failure and repair'),ref(Path(__file__),'Direct transitive preservation check')]
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,scope='Grouped Dataiku/DataRobot reference decisions without native admission',reviewed_reader=report['pdf'],checks=checks,evidence=evidence,findings=['Every actual predecessor record,context and compiled input survives directly.','Intermediate reviewed draft remains preserved; one final canonical publication and exact-byte review cycle.','Reference decisions remain separately auditable; source rights and native uncertainty remain open.'],limitations=LIMITS,visual_acceptance=False,final_acceptance=False));print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))

def publish():
    report,_=verify();review=read(BASE/'release-source-review.json');verify_bindings(review)
    state=core.read(ROOT,core.STATE);digest=core.sha(ROOT/core.STATE)
    prior_pdf=ref(ROOT/'docs/causal_proposal_agents_reuse_reviewed_2026-10-25.pdf','Actual predecessor')
    assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],prior_pdf)
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],supersedes={k:state['reader'][k] for k in ['path','sha256']},build_report=ref(final.OUT/'build-report.json','Preserving final build'),source_review=ref(BASE/'release-source-review.json','Direct grouped author review'),text_layout=ref(final.OUT/'text-layout-review.json','All-page text bounds'),source_artifacts=read(final.OUT/'source-audit.json')['tex_files']+review['evidence'],changes=['Dataiku workflow/scientific acceptance and DataRobot propensity/weighting reference decisions;all predecessor content preserved.'],visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair one sponsor to exact final reader.')
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Grouped preserving successor');run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding);state['reader']={k:report['pdf'][k] for k in ['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance');state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,digest,state,dict(action='publish_workflow_reuse_wave',manifest=binding,final_acceptance=False));print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))

def renew():
    report,_=verify();binding=ref(BASE/'working-release.json','Exact current reader');run.ledger.validate_working_release(ROOT,binding)
    findings=dict(Q2='All1206 actual predecessor records and contexts preserved;three new records;1209 records and258 scholarly PDFs.',Q3='Exact request/run/deadline,normalized-weight/ESS and cost witnesses reproduce;no vendor behavior or bank result claimed.',Q4='Separate Dataiku execution/scientific acceptance and DataRobot propensity/weighting contracts preserve target,identity,failure and complete costs;no native capability.')
    for q,finding in findings.items():
        op='PROPOSAL.'+q;state=core.read(ROOT,core.STATE);assert run.same_reader(state['reader'],report['pdf']);previous=state['execution_runtime']['results'][op];old=core.read(ROOT,previous['path']);assert old['reviewed_reader']['sha256']!=report['pdf']['sha256']
        folder=BASE/q;folder.mkdir();evidence=[previous,binding,ref(BASE/'release-source-review.json','Direct preservation review'),ref(intermediate.BASE/'source-audit.json','Dataiku authored audit'),ref(final.BASE/'source-audit.json','DataRobot source/decision audit'),ref(intermediate.BASE/'mathematical-review.json','Dataiku arithmetic'),ref(final.BASE/'mathematical-review.json','DataRobot arithmetic'),ref(Path(__file__),'Exact-reader grouped review')]
        write(folder/'reopen.json',dict(reason='One grouped successor requires exact-byte delta review.',prior_result=previous,reviewed_reader=report['pdf'],evidence=evidence,next_action='Record bounded exact-reader author review.'));transition('reopen',op,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);attempt=len(state['execution_runtime']['review_history'][op]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0];limits=list(dict.fromkeys(old['limitations']+LIMITS));scope='Author grouped workflow/propensity reference delta;proposal only'
        write(output,dict(operation=op,status='pass',criterion=node['criteria'][0],reviewer=REVIEWER,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node);receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',outputs=[ref(output,'Exact-reader author review')],nonexecution_reason='',revisit_trigger='',criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt);transition('record',op,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish','renew']);globals()[p.parse_args().command]()
