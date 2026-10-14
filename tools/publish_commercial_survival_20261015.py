#!/usr/bin/env python3
"""Publish scoped commercial survival evidence and preserve exact-reader reviews."""
import argparse
import json
from pathlib import Path
import build_commercial_survival_v3_20261015 as build
import commercial_survival_examples_20261014 as exact
import review_commercial_survival_20261015 as review
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write
ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
WORK=review.WORK


def verify():
    report=json.loads((OUT/'build-report.json').read_text())
    for path in [OUT/'build-report.json',BASE/'release-source-review.json',BASE/'operation-receipt.json',review.OUTPUT]:
        verify_bindings(json.loads(path.read_text()))
    assert report['cited_records']==614
    assert exact.calculate()==json.loads((WORK/'exact-results.json').read_text())
    assert json.loads(review.OUTPUT.read_text())['status']=='inconclusive'
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    return report


def record():
    verify();state=core.read(ROOT,core.STATE)
    if review.OP in state['execution_program']['results']:
        assert state['execution_program']['results'][review.OP]['sha256']==core.sha(BASE/'operation-receipt.json')
    else:transition('record',review.OP,BASE/'operation-receipt.json')


def publish():
    report=verify();state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert review.OP in state['execution_program']['results']
    audit=json.loads((OUT/'source-audit.json').read_text())
    checked=json.loads((BASE/'release-source-review.json').read_text())
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Integrated commercial survival reader'),
        'source_review':ref(BASE/'release-source-review.json','Author source and exact construction review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page extraction and bounds'),
        'source_artifacts':audit['tex_files']+checked['evidence']+[ref(review.OUTPUT,'Bounded inconclusive coverage result'),
            ref(Path(__file__).resolve(),'Exact-reader publication and renewal procedure')],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Compare eight commercial survival/longitudinal families with an explicit ninth-source omission.',
                   'Develop competing-event, time-zero, sequential confounding, censoring and bootstrap examples.',
                   'Specify target-preserving adapters, documented local capability gaps and conditional licensed experiments.'],
        'sponsor_binding':'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed commercial survival working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_commercial_survival_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))


def renew():
    report=verify()
    findings={
      'Q2':'All603 inherited source records and citation uses remain. Eleven additions bind fourteen successful original vendor documents, inspected semantic limits and exact project scenarios. Eight commercial families have bounded primary text; MATLAB, some edition/cutoff identities and broader coverage remain unqualified. No unavailable-source waiver or runtime performance claim is granted.',
      'Q3':'Inherited demonstrations remain unchanged. Five exact authored constructions reproduce: competing-event recursion and independent paths, future-defined exposure counts, sixteen-state sequential g-formula/IPW, conditional observation correction and rare-path bootstrap omission. These are stipulated references, not vendor runs, estimated bank effects or empirical failure rates.',
      'Q4':'The new banking example has lower default incidence .15 versus .18 but lower stipulated net value minus12 versus minus3.6USD because event mix and resource value differ. The next investment is a public/generated target-and-conversion prototype before conditional licensed or bank experiments. All prices and laws are exposed scenarios; actual licenses, execution costs and bank value are unknown.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier]
        old=json.loads((ROOT/previous['path']).read_text())
        if run.same_reader(old.get('reviewed_reader',{}),report['pdf']):
            assert old['outcome']=='pass';continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),
                  ref(BASE/'release-source-review.json','Source/claim and exact-example review'),
                  ref(review.OUTPUT,'Coverage limitations and proposed acceptance cases'),
                  ref(WORK/'exact-results.json','Five exact construction groups'),
                  ref(WORK/'primary-review.json','Inspected vendor originals'),
                  ref(Path(__file__).resolve(),'Exact-reader author delta findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires preserved successor review.',
            'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record the bounded survival source, demonstration and investment delta.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+review.LIMITS))
        scope='Author exact-reader delta review; proposal evidence only'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],
            'reviewer':review.REVIEWER,'reviewed_reader':report['pdf'],'review_attempt':attempt,
            'acceptance_scope':'proposal_only','scope':scope,'findings':[finding],
            'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=review.REVIEWER,
            limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open','proposal_accepted':False}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['record','publish','renew']);a=p.parse_args()
    {'record':record,'publish':publish,'renew':renew}[a.command]()
