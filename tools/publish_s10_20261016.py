#!/usr/bin/env python3
"""Record and publish the reviewed software qualification chapter."""
import argparse
import json
from pathlib import Path
import build_s10_reader_20261016 as build
import prepare_s10_20261016 as work
import review_s10_20261016 as review
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT

def verify():
    report=json.loads((OUT/'build-report.json').read_text())
    for p in [OUT/'build-report.json',BASE/'release-source-review.json',BASE/'draft-operation-receipt.json',BASE/'review-operation-receipt.json',review.REVIEW]:
        verify_bindings(json.loads(p.read_text()))
    assert report['pages']==816 and report['cited_records']==641
    measured=json.loads(review.REVIEW.read_text())
    assert measured['status']=='pass' and measured['substantive_page_credit']==4
    assert measured['allocation_minimum_met'] and not measured['planning_target_met']
    assert work.examples.calculate()==json.loads((work.BASE/'exact-results.json').read_text())
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    return report

def record():
    verify()
    for identifier,name in [('TEXT.DRAFT.S10','draft-operation-receipt.json'),('TEXT.REVIEW.S10','review-operation-receipt.json')]:
        state=core.read(ROOT,core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256']==core.sha(BASE/name)
            continue
        transition('record',identifier,BASE/name)

def publish():
    report=verify();state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(k in state['execution_program']['results'] for k in ['TEXT.DRAFT.S10','TEXT.REVIEW.S10'])
    audit=json.loads((OUT/'source-audit.json').read_text());reviewed=json.loads((BASE/'release-source-review.json').read_text())
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
      'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
      'build_report':ref(OUT/'build-report.json','Preserving816-page qualification reader'),
      'source_review':ref(BASE/'release-source-review.json','Author source,math and chapter-depth review'),
      'text_layout':ref(OUT/'text-layout-review.json','All-page text bounds'),
      'source_artifacts':audit['tex_files']+reviewed['evidence']+[ref(review.REVIEW,'Four nonduplicate substantive pages;target6 not claimed'),ref(Path(__file__),'Publication and review procedure')],
      'visual_acceptance':False,'mandatory_repairs_closed':[],
      'changes':['Develop route admission,matched scientific and operating comparisons and full-procedure port obligations.',
        'Derive exact paired-law,failure-bound,numerical-decision and maintenance-cost examples.',
        'Specify prototype acceptance and build/buy/bridge/port/reference alternatives with later owner inputs.'],
      'sponsor_binding':'Preserved sponsor baseline;Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed S10 working successor')
    run.ledger.validate_working_release(ROOT,binding);state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']));run.commit(ROOT,before,state,{'action':'publish_s10_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))

def renew():
    report=verify()
    findings={
      'Q2':'639 inherited source records and all citation uses preserved;two project additions yield641 records and175 genuine scholarly PDFs.Seven inherited citation records retain pinned primary-source and proposal scope.',
      'Q3':'Four exact authored families reproduce paired-law counts/covariance,fixed Bernoulli zero-failure inequalities,numerical decision enclosures and maintenance break-even.No package/bridge trial or general statistical guarantee inferred.',
      'Q4':'Stipulated loss threshold8.75USD,net4500/2000USD,numerical enclosure[-1.5,3.5] with reference-0.25USD,and maintenance break-even190000 versus100000 requests connect qualification to acquisition decisions.No market prices or bank ROI inferred.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        if run.same_reader(old.get('reviewed_reader',{}),report['pdf']):
            assert old['outcome']=='pass';continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),ref(BASE/'release-source-review.json','Author source/math review'),
          ref(review.REVIEW,'S10 topic/depth review'),ref(work.BASE/'exact-results.json','Four exact reference families'),ref(Path(__file__),'Exact-reader findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires preserved successor author review.','prior_result':previous,
          'reviewed_reader':report['pdf'],'evidence':evidence,'next_action':'Record scoped S10 source,math and acquisition delta.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+review.LIMITS));scope='Author exact-reader delta review;proposal evidence only'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':work.REVIEWER,
          'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only','scope':scope,
          'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node);receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,
          limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
          outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
          criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open','proposal_accepted':False}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['record','publish','renew']);args=p.parse_args()
    {'record':record,'publish':publish,'renew':renew}[args.command]()
