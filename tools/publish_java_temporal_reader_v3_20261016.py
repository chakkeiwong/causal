#!/usr/bin/env python3
"""Preserve and review the Java temporal proposal successor."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_java_temporal_reader_v3_20261016 as build
import review_java_temporal_20261015 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT


def review():
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(build.PRIOR.read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((work.BASE/'author-review.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==175
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==626 and len(new)==634 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    previous=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for r in previous['records']:
        inherited=Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts'])
        assert not inherited-contexts[r['citation_key']],r['citation_key']
    assert work.exact()==json.loads((work.BASE/'exact-results.json').read_text())
    text=' '.join((OUT/'reader.txt').read_text().split())
    phrases=['Java temporal discovery: clocks, regimes','a five-minute search budget',
        'missing-data path does not consistently honor','time-lag container','rounded mean size',
        '15 of the 17 shared paths','conditional proxy for net benefit','prospective design, not an executed Java experiment']
    for phrase in phrases:assert phrase.lower() in text.lower(),phrase
    primary=json.loads((work.BASE/'primary-review.json').read_text())
    assert len(primary['sources'])==31 and len(primary['packages'])==6
    evidence=[ref(p,a) for p,a in [(OUT/'build-report.json','Exact preserving Java successor'),
        (OUT/'source-audit.json','634 traceable source records'),(BASE/'traceability-review.json','175 genuine scholarly PDFs;all inherited citation contexts retained'),
        (OUT/'text-layout-review.json','All-page extraction and bounds'),(OUT/'reader.txt','Integrated Java temporal comparison'),
        (work.BASE/'primary-review.json','31 pinned source/document blobs'),(work.BASE/'exact-results.json','Nine exact reference families'),
        (work.BASE/'reuse-and-prototype-contract.json','Concrete conditional reuse decisions and proposed prototype'),
        (work.BASE/'candidate-register.json','19 candidates/aliases,searches and omissions'),
        (work.BASE/'author-review.json','Scoped technical review'),(work.BASE/'disk-recovery.json','Preserved ENOSPC and limited cache cleanup'),
        (Path(__file__),'Exact-reader checks')]]
    findings=[
        'Physical and positional clocks,series boundaries and lag-before-bootstrap are separated from dependent-sample uncertainty.',
        'Exact finite-law variance and weighting examples reproduce;target choice changes stipulated monetary decisions.',
        'Selected callers and callees support weighting-default,stationarity-flag,process-exit,resource-budget and graph-projection concerns without claiming upstream execution.',
        'Six repository decisions distinguish graph discovery,dynamic structure,forecasting,clustering and supplied-model EM;rights and wider coverage remain explicit.',
        '626 inherited citation records and all prior contexts remain;8 additions yield634 records and175 genuine scholarly PDFs.',
        'Known engineering/acquisition remedies are distinguished from unresolved dependent graph/effect uncertainty;no mandatory repair or final acceptance is awarded.'
    ]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,
        'reviewed_reader':report['pdf'],'scope':'Author source,math and exact-reader review;coverage outcome inconclusive',
        'evidence':evidence,'preserved_records':626,'new_records':8,'preserved_compiled_sources':len(kept),
        'original_contexts_retained':True,'findings':findings,'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'new_records':8,'sections':report['java_temporal_sections']}))


def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving Java temporal reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Develop six Java temporal repository routes with31 pinned original files.',
            'Add nine exact clock,dependence,score,target and intervention references.',
            'State conditional reuse decisions,typed failures and public/generated prototype design with coverage and research limits.'],
        'sponsor_binding':'Preserved sponsor baseline;Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed Java temporal working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_java_temporal_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))


def renew():
    report=json.loads((OUT/'build-report.json').read_text());verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={
      'Q2':'626 inherited records and all prior contexts retained;8 additions yield634 records and175 genuine scholarly PDFs.31 source/document blobs match complete pinned trees and acquisition hashes;version,rights and census limits remain explicit.',
      'Q3':'Inherited demonstrations retained.Nine exact authored references reproduce clocks,boundaries,resampling,dependent variance,weights,targets,selected source branches and observational/intervention distinctions.No upstream Java or fitted performance claim.',
      'Q4':'Stipulated customer-target net72/11USD versus equal-branch net-18USD and conditional-proxy2USD versus intervention net-8USD connect target/identification mistakes to decisions.A public/generated prototype precedes costly bank work;real prices and ROI remain unknown.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current working reader'),
            ref(BASE/'release-source-review.json','Source,math and text review'),ref(work.OUTPUT,'Bounded Java coverage review'),
            ref(work.BASE/'exact-results.json','Exact authored constructions'),ref(Path(__file__),'Exact-reader findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires a preserved successor review.','prior_result':previous,
            'reviewed_reader':report['pdf'],'evidence':evidence,'next_action':'Record scoped Java temporal source,mathematical and economic review.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader delta review;proposal evidence only'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':work.REVIEWER,
            'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only','scope':scope,
            'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open','proposal_accepted':False}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['review','publish','renew']);args=parser.parse_args()
    {'review':review,'publish':publish,'renew':renew}[args.command]()
