#!/usr/bin/env python3
"""Review and publish a preserving discovery-delegate and server-boundary reader; renew exact-byte reviews."""
import argparse,json
from pathlib import Path
import build_boundary_profile_reader_20261028 as build
import run_program_checkpoint_v3 as controller
from review_publish_observations_v2_20261022 import contexts
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write
run=controller.base;core=run.core;ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
read=lambda p:json.loads(p.read_text());REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Author source, exact arithmetic and all-page extracted text/bounds review; no fresh visual or independent acceptance.',
 'No downloaded code or native product executed; conditional static findings are not observed benchmark failures.',
 'Q1/Q5, mandatory coverage/depth, task/split/scorer identity, artifact rights and full-cost qualification, rights, prices and native/bank qualification remain open.']

def verify():
    for n in ['prepared-inputs.json','source-audit.json','plan-review.json','mathematical-review.json','copyedit-review.json',
              'traceability-review.json','reader/source-audit.json','reader/build-report.json','reader/text-layout-review.json']:
        verify_bindings(read(BASE/n))
    report,audit,index,bounds=[read(BASE/n) for n in ['reader/build-report.json','reader/source-audit.json','traceability-review.json','reader/text-layout-review.json']]
    assert index['status']==bounds['status']=='pass' and not index['issues']
    assert report['cited_records']==1418 and index['scholarly_pdfs']==271
    assert not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text()==build.expected_driver() and build.DEVELOPMENT.read_text()==build.expected_development()
    assert build.exact.calculate()==read(BASE/'exact-results.json')
    old={s['integrated_citation_key']:s for s in read(build.PRIOR)['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==1415 and all(new[k]==v for k,v in old.items())
    assert new.keys()-old.keys()=={'exec28_bp_'+k for k in ['cdt','ollama','reference']}
    compiled={x['path']:x for x in audit['tex_files']};kept=[x for x in read(build.PRIOR)['tex_files'] if x['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(compiled[x['path']]['sha256']==x['sha256'] for x in kept)
    before=contexts(read(build.PREDECESSOR/'traceability-review.json'));after=contexts(index,{str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(v==after[k] for k,v in before.items())
    pages=[' '.join(p.split()).replace('- ','-') for p in (OUT/'reader.txt').read_text().split(chr(12))]
    opening='A banking proposal must preserve variable identity across discovery and execution boundaries.';closing='Variable identity and execution identity must survive every boundary before a causal result is admitted.'
    matches=[i for i,p in enumerate(pages) if opening in p];assert len(matches)==1, ('Expected one discovery-delegate and server-boundary opening anchor',matches)
    start=matches[0];offset=pages[start].index(opening)
    endings=[i for i in range(start,min(start+24,len(pages))) if closing in (pages[i][offset:] if i==start else pages[i])]
    assert len(endings)==1,('Expected one bounded discovery-delegate and server-boundary closing anchor',endings)
    end=endings[0]
    section=' '.join(pages[start:end+1]);section=section[section.index(opening):];section=section[:section.index(closing)+len(closing)]
    for token in ['HTTP','Gaussian','schema','reminder','unload']:assert token in section,token
    return report,dict(preserved_citation_records=1415,added_citation_records=3,scholarly_pdfs=271,unchanged_compiled_inputs=len(kept),prior_citation_contexts_preserved=True,rendered_pages=[start+1,end+1],native_execution=False,visual_acceptance=False)

def review():
    report,checks=verify()
    evidence=[ref(BASE/n,'Reviewed preserving integration') for n in ['prepared-inputs.json','source-audit.json','plan-review.json','mathematical-review.json','copyedit-review.json','traceability-review.json','development.tex','reader/build-report.json','reader/text-layout-review.json']]+[ref(Path(__file__),'Exact preservation and output checks')]
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,scope='Separate discovery-delegate and server-boundary choices, query semantics and public qualification',reviewed_reader=report['pdf'],checks=checks,evidence=evidence,findings=['Every predecessor source record, claim, context and compiled content input preserved.','Selected CDT and Ollama server paths are inspected; exact witnesses remain distinct from native behavior.','Scientific identity, numerical accuracy and workflow completion remain distinct; no native qualification.'],limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))

def publish():
    report,_=verify();review=read(BASE/'release-source-review.json');verify_bindings(review)
    state=core.read(ROOT,core.STATE);digest=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],ref(build.OLD.with_suffix('.pdf'),'Predecessor'))
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],supersedes={k:state['reader'][k] for k in ['path','sha256']},build_report=ref(OUT/'build-report.json','Preserving build'),source_review=ref(BASE/'release-source-review.json','Author review'),text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),source_artifacts=read(OUT/'source-audit.json')['tex_files']+review['evidence'],changes=['Selected CDT score,order and launcher paths and Ollama routing,streaming and residency contracts with exact authored witnesses; all previous content preserved.'],visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair sponsor to exact reader bytes.')
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed discovery-delegate and server-boundary successor');run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding);state['reader']={k:report['pdf'][k] for k in ['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance');state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,digest,state,dict(action='publish_boundary_profile_reader',manifest=binding,final_acceptance=False));print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))

def renew():
    report,_=verify();binding=ref(BASE/'working-release.json','Exact current reader');run.ledger.validate_working_release(ROOT,binding)
    verify_bindings(read(build.PREDECESSOR/'release-source-review.json'))
    findings=dict(Q2='All1415 prior records and contexts preserved; three additional selected-software and independent-project records;1418 records and271 scholarly PDFs.',Q3='Exact finite examples show a label-only permutation reversing the named edge and one admitted result among six stipulated HTTP200 traces; no native behavior or bank performance claimed.',Q4='Proposed request contracts distinguish completion,representation,scientific admission,refusal and transport uncertainty,with full attempts and costs; no native capability.')
    for q,finding in findings.items():
        op='PROPOSAL.'+q;state=core.read(ROOT,core.STATE);assert run.same_reader(state['reader'],report['pdf']);previous=state['execution_runtime']['results'][op];old=core.read(ROOT,previous['path']);assert old['reviewed_reader']['sha256']!=report['pdf']['sha256']
        folder=BASE/q;folder.mkdir();evidence=[previous,binding,ref(BASE/'release-source-review.json','Preservation review'),ref(BASE/'source-audit.json','Primary audit'),ref(BASE/'mathematical-review.json','Exact arithmetic'),ref(Path(__file__),'Exact-reader review')]
        write(folder/'reopen.json',dict(reason='Preserving successor requires exact-byte delta review.',prior_result=previous,reviewed_reader=report['pdf'],evidence=evidence,next_action='Record bounded exact-reader author review.'));transition('reopen',op,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);attempt=len(state['execution_runtime']['review_history'][op]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0];limits=list(dict.fromkeys(old['limitations']+LIMITS));scope='Author discovery-delegate and server-boundary delta; proposal only'
        write(output,dict(operation=op,status='pass',criterion=node['criteria'][0],reviewer=REVIEWER,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node);receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',outputs=[ref(output,'Exact-reader author review')],nonexecution_reason='',revisit_trigger='',criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt);transition('record',op,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish','renew']);globals()[p.parse_args().command]()
