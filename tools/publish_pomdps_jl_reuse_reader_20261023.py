#!/usr/bin/env python3
"""Publish exact-byte source-contract successor without changing past evidence."""
import argparse,json
from pathlib import Path
import build_pomdps_jl_reuse_reader_20261023 as build
import run_program_checkpoint_v3 as controller
from review_publish_observations_v2_20261022 import contexts
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write
run=controller.base;core=run.core;ROOT=build.ROOT;BASE=build.BASE;OUT=build.OUT
read=lambda p:json.loads(p.read_text())
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Author source, project-owned data/arithmetic and all-page text review only; visual and independent acceptance remain open.',
'No upstream package code executed; tests and caller contracts do not establish native behavior.',
'Q1/Q5, mandatory coverage/depth repairs, dependency rights and bank qualification remain open.']
def verify():
 for n in ['prepared-inputs.json','source-audit.json','plan-review.json','mathematical-review.json','copyedit-review.json','traceability-review.json','reader/source-audit.json','reader/build-report.json','reader/text-layout-review.json']:verify_bindings(read(BASE/n))
 report=read(OUT/'build-report.json');audit=read(OUT/'source-audit.json');index=read(BASE/'traceability-review.json');bounds=read(OUT/'text-layout-review.json')
 assert index['status']==bounds['status']=='pass' and not index['issues']
 assert report['cited_records']==1000 and index['scholarly_pdfs']==232
 assert not bounds['empty_pages'] and not bounds['out_of_bounds']
 assert all('Underfull' in w for w in report['warnings'])
 assert build.DRIVER.read_text()==build.expected_driver()
 assert build.DEVELOPMENT.read_bytes()==(build.SOURCE/'development.tex').read_bytes()
 assert build.exact.calculate()==read(BASE/'exact-results.json')
 old={s['integrated_citation_key']:s for s in read(build.PRIOR)['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
 assert len(old)==998 and all(new[k]==v for k,v in old.items())
 assert new.keys()-old.keys()=={'exec23_pomdpsjl_sources','exec23_pomdpsjl_reference'}
 compiled={x['path']:x for x in audit['tex_files']};kept=[x for x in read(build.PRIOR)['tex_files'] if x['path']!=str(build.OLD.relative_to(ROOT))]
 assert all(compiled[x['path']]['sha256']==x['sha256'] for x in kept)
 before=contexts(read(build.PREDECESSOR/'traceability-review.json'));after=contexts(index,{str(build.DEVELOPMENT.relative_to(ROOT))})
 assert all(v==after[k] for k,v in before.items())
 pages=[' '.join(x.split()).replace('- ','-').replace('−','-') for x in (OUT/'reader.txt').read_text().split(chr(12))]
 start=next(i for i,p in enumerate(pages) if 'A bank considering Julia for sequential servicing' in p)
 end=next(i for i,p in enumerate(pages) if i>=start and 'adoption remain open' in p)
 section=' '.join(pages[start:end+1])
 for token in ['POMDPs.jl','35/4','5/8','1/16','zero','reference','terminal']:
  assert token in section,token
 return report,dict(preserved_citation_records=998,added_citation_records=2,scholarly_pdfs=232,unchanged_compiled_inputs=len(kept),prior_citation_contexts_preserved=True,rendered_pages=[start+1,end+1],native_execution=False,visual_acceptance=False)
def review():
 report,checks=verify()
 write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,scope='POMDPs.jl joint generation and model-conversion source review',reviewed_reader=report['pdf'],checks=checks,
 evidence=[ref(BASE/n,'Reviewed preserving integration') for n in ['prepared-inputs.json','source-audit.json','plan-review.json','mathematical-review.json','copyedit-review.json','traceability-review.json','development.tex','reader/build-report.json','reader/text-layout-review.json']]+[ref(Path(__file__),'Exact source/context/output review')],
 findings=['All 998 predecessor records, claims, citation contexts and compiled content inputs preserved.','Two audited records add sixteen authenticated software blobs and independent joint-generation and conversion witnesses.','Source contracts, exact examples and native qualification remain separate.'],limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
 print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))
def publish():
 report,_=verify();review=read(BASE/'release-source-review.json');verify_bindings(review)
 state=core.read(ROOT,core.STATE);digest=core.sha(ROOT/core.STATE)
 assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],ref(build.OLD.with_suffix('.pdf'),'Predecessor'))
 manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],supersedes={k:state['reader'][k] for k in ['path','sha256']},build_report=ref(OUT/'build-report.json','Preserving build'),source_review=ref(BASE/'release-source-review.json','Author review'),text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),source_artifacts=read(OUT/'source-audit.json')['tex_files']+review['evidence'],changes=['POMDPs.jl joint-generation, belief and conversion contracts; prior contents preserved.'],visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair sponsor to exact reader bytes.')
 write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed source-contract successor');run.ledger.validate_working_release(ROOT,binding)
 state['execution_program']['working_releases'].append(binding);state['reader']={k:report['pdf'][k] for k in ['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance');state['deliveries'].append(dict(state['reader']))
 run.commit(ROOT,digest,state,dict(action='publish_pomdps_jl_reuse_reader',manifest=binding,final_acceptance=False))
 print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))
def renew():
 report,_=verify();binding=ref(BASE/'working-release.json','Exact current reader');run.ledger.validate_working_release(ROOT,binding)
 findings=dict(Q2='All 998 source records, contexts and claims preserved; sixteen software blobs and independent checks add two records.',Q3='Independent joint-generation, expected-reward, terminal-entry and observation-arity witnesses reproduce; no measured economics.',Q4='No native execution; source-specific joint-event, reward, observation, belief and dependency qualification remain prerequisites.')
 for q,finding in findings.items():
  op='PROPOSAL.'+q;state=core.read(ROOT,core.STATE);assert run.same_reader(state['reader'],report['pdf'])
  previous=state['execution_runtime']['results'][op];old=core.read(ROOT,previous['path']);assert old['reviewed_reader']['sha256']!=report['pdf']['sha256']
  folder=BASE/q;folder.mkdir();evidence=[previous,binding,ref(BASE/'release-source-review.json','Preservation review'),ref(BASE/'source-audit.json','Primary source audit'),ref(BASE/'mathematical-review.json','Data and arithmetic checks'),ref(Path(__file__),'Exact-reader delta review')]
  write(folder/'reopen.json',dict(reason='Preserving successor requires exact-byte delta review.',prior_result=previous,reviewed_reader=report['pdf'],evidence=evidence,next_action='Record bounded exact-reader author review.'))
  transition('reopen',op,folder/'reopen.json');state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op)
  attempt=len(state['execution_runtime']['review_history'][op]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0];limits=list(dict.fromkeys(old['limitations']+LIMITS));scope='Author source-contract delta; proposal only'
  write(output,dict(operation=op,status='pass',criterion=node['criteria'][0],reviewer=REVIEWER,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
  receipt=run.ledger.receipt_template(node);receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',outputs=[ref(output,'Exact reader review')],nonexecution_reason='',revisit_trigger='',criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
  write(folder/'operation-receipt.json',receipt);transition('record',op,folder/'operation-receipt.json')
 print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish','renew']);globals()[p.parse_args().command]()
