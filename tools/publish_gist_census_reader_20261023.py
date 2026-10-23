#!/usr/bin/env python3
"""Publish exact-byte source-contract successor without changing past evidence."""
import argparse,json
from pathlib import Path
import build_gist_census_reader_20261023 as build
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
 assert report['cited_records']==988 and index['scholarly_pdfs']==231
 assert not bounds['empty_pages'] and not bounds['out_of_bounds']
 assert all('Underfull' in w for w in report['warnings'])
 assert build.DRIVER.read_text()==build.expected_driver()
 assert build.DEVELOPMENT.read_bytes()==(build.SOURCE/'development.tex').read_bytes()
 assert build.exact.calculate()==read(BASE/'exact-results.json')
 old={s['integrated_citation_key']:s for s in read(build.PRIOR)['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
 assert len(old)==985 and all(new[k]==v for k,v in old.items())
 assert new.keys()-old.keys()=={'exec23_gist_paper','exec23_gist_sources','exec23_gist_reference'}
 compiled={x['path']:x for x in audit['tex_files']};kept=[x for x in read(build.PRIOR)['tex_files'] if x['path']!=str(build.OLD.relative_to(ROOT))]
 assert all(compiled[x['path']]['sha256']==x['sha256'] for x in kept)
 before=contexts(read(build.PREDECESSOR/'traceability-review.json'));after=contexts(index,{str(build.DEVELOPMENT.relative_to(ROOT))})
 assert all(v==after[k] for k,v in before.items())
 pages=[' '.join(x.split()).replace('- ','-').replace('−','-') for x in (OUT/'reader.txt').read_text().split(chr(12))]
 start=next(i for i,p in enumerate(pages) if 'A request to improve a distressed-loan portfolio' in p)
 end=next(i for i,p in enumerate(pages) if i>=start and 'broader frontier coverage remain open' in p)
 section=' '.join(pages[start:end+1])
 for token in ['GIST','815','673','53','560','3,520','388021','163979']:
  assert token in section,token
 return report,dict(preserved_citation_records=985,added_citation_records=3,scholarly_pdfs=231,unchanged_compiled_inputs=len(kept),prior_citation_contexts_preserved=True,rendered_pages=[start+1,end+1],native_execution=False,visual_acceptance=False)
def review():
 report,checks=verify()
 write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,scope='Goal clarification and benchmark provenance source review',reviewed_reader=report['pdf'],checks=checks,
 evidence=[ref(BASE/n,'Reviewed preserving integration') for n in ['prepared-inputs.json','source-audit.json','plan-review.json','mathematical-review.json','copyedit-review.json','traceability-review.json','development.tex','reader/build-report.json','reader/text-layout-review.json']]+[ref(Path(__file__),'Exact source/context/output review')],
 findings=['All985 predecessor records, claims, citation contexts and compiled content inputs preserved.','Three audited records add one authentic original, eleven authenticated artifacts and independent saved-data/AST checks.','Goal-state tool filtering, causal-effect identification and native replay remain separate.'],limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
 print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))
def publish():
 report,_=verify();review=read(BASE/'release-source-review.json');verify_bindings(review)
 state=core.read(ROOT,core.STATE);digest=core.sha(ROOT/core.STATE)
 assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],ref(build.OLD.with_suffix('.pdf'),'Predecessor'))
 manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],supersedes={k:state['reader'][k] for k in ['path','sha256']},build_report=ref(OUT/'build-report.json','Preserving build'),source_review=ref(BASE/'release-source-review.json','Author review'),text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),source_artifacts=read(OUT/'source-audit.json')['tex_files']+review['evidence'],changes=['Goal clarification, artifact provenance and public-evidence qualification route; prior contents preserved.'],visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair sponsor to exact reader bytes.')
 write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed source-contract successor');run.ledger.validate_working_release(ROOT,binding)
 state['execution_program']['working_releases'].append(binding);state['reader']={k:report['pdf'][k] for k in ['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance');state['deliveries'].append(dict(state['reader']))
 run.commit(ROOT,digest,state,dict(action='publish_gist_census_reader',manifest=binding,final_acceptance=False))
 print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))
def renew():
 report,_=verify();binding=ref(BASE/'working-release.json','Exact current reader');run.ledger.validate_working_release(ROOT,binding)
 findings=dict(Q2='All985 source records, contexts and claims preserved;One authentic original, eleven authenticated artifacts and independently authored checks add three audited records.',Q3='Independent final-row aggregation and stipulated cost arithmetic reproduce; no causal superiority or measured economics.',Q4='No new native execution; generating revision, labels, raw traces and schema reconciliation remain prerequisites. Reference review grants no adapter approval.')
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
