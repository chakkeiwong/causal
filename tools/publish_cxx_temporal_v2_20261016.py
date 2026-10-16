#!/usr/bin/env python3
"""Review, record and publish the native temporal working successor."""
import argparse
from collections import Counter
import json
import re
from pathlib import Path
import build_cxx_temporal_reader_v2_20261016 as build
import review_cxx_temporal_20261016 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT,BASE,OUT,WORK=build.ROOT,build.BASE,build.OUT,build.WORK


def review():
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text());prior=json.loads(build.PRIOR.read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((WORK/'author-review.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==175
    layout=json.loads((OUT/'text-layout-review.json').read_text())
    assert layout['status']=='pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text()==build.expected_driver()
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==649 and len(new)==656 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    previous=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x,sort_keys=True) for x in row['citation_contexts'])-contexts[row['citation_key']]
    text=' '.join((OUT/'reader.txt').read_text().split())
    text=re.sub(r'-\s+', '-', text)
    for phrase in ['Native temporal and interventional engines','7.86365','93.2','70.8','22.4',
                   'root license contains LGPL2.1','LGPL3-or-later','physical interval',
                   'mixed diagnostic/result stream','reversed pair','DBN++','EISALab/DBN','pdbntk']:
        assert phrase in text,phrase
    assert work.exact()==json.loads((WORK/'exact-results.json').read_text())
    evidence=[ref(p,a) for p,a in [
        (OUT/'build-report.json','Preserving native temporal reader'),(OUT/'source-audit.json','656 source records'),
        (BASE/'traceability-review.json','175 genuine scholarly PDFs and retained contexts'),
        (OUT/'text-layout-review.json','All-page text bounds'),(OUT/'reader.txt','Inspected integrated comparison'),
        (WORK/'source-review.json','38 original files,two inherited licenses and genuine primary paper reread'),
        (WORK/'exact-results.json','Five exact authored reference families'),
        (WORK/'independent-verification-v2.json','Separate enumeration and covariance review'),
        (WORK/'proposed-contract.json','Five reuse choices and proposed CLI/MCP/public prototype'),
        (WORK/'omissions-register.json','Thirty leads,aliases,search truncation and omissions'),
        (WORK/'plan-review.json','Reviewed plan and source-specific corrections'),
        (WORK/'author-review.json','Criterion-specific review'),(BASE/'repair.json','Preserved spacing and phrase-check repair'),(work.OUTPUT,'Bounded cell coverage review'),
        (Path(__file__),'Exact-reader review and transitions')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,
        'reviewed_reader':report['pdf'],'scope':'Author primary-source,arithmetic and extracted-text review;coverage remains inconclusive',
        'preserved_records':649,'new_records':7,'preserved_compiled_sources':len(kept),'original_contexts_retained':True,
        'evidence':evidence,'findings':[
            'Native known-intervention search,supplied-model inference,temporal training and constrained genetic-network search remain distinct.',
            'Intercept/default,regime indexing,state-order,window dependence,constraint and output-channel findings are bound to actual source paths.',
            'License discrepancy and missing rights remain explicit;no integration permission or upstream runtime is claimed.',
            'Five exact references and separate arithmetic support proposed public/generated tests and stipulated economics.',
            'All inherited sources and contexts remain;bounded omissions do not block independent proposal work.'],
        'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'sections':report['cxx_temporal_sections']}))


def record():
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    author=json.loads((WORK/'author-review.json').read_text())
    state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,work.OP)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',
        scope='Bounded five-family native temporal/interventional source comparison;broader coverage remains open',
        reviewer=work.REVIEWER,limitations=work.LIMITS,capabilities=[],outputs=[ref(work.OUTPUT,'Reviewed cell coverage')],
        nonexecution_reason='',revisit_trigger='Inspect omitted native leads and later theory;resolve source-specific rights and frozen environments before enabling any adapter.',
        criteria=[{'index':i,'verdict':author['criteria_verdicts'][i],'finding':finding,
                   'evidence':[ref(WORK/'author-review.json','Criterion review'),ref(BASE/'release-source-review.json','Preserving integration')]}
                  for i,finding in enumerate(author['findings'])])
    write(BASE/'operation-receipt.json',receipt);transition('record',work.OP,BASE/'operation-receipt.json')


def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None and work.OP in state['execution_program']['results']
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    canonical_status=state['reader']['status'];assert canonical_status=='Working monograph; not I02 acceptance'
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving native temporal reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Compare five native temporal/interventional software families with source-specific reuse conditions.',
            'Develop exact regime,intercept,dependence,state-order and graph-constraint examples and a proposed public/generated test.'],
        'sponsor_binding':'Preserved sponsor baseline;Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed native temporal working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status=canonical_status);state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_cxx_temporal_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader']}))


def renew():
    report=json.loads((OUT/'build-report.json').read_text());verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={
        'Q2':'All649 inherited citation records and contexts remain. Seven additions bind38 pinned originals,two inherited license originals,a genuine GIES paper reread,authored arithmetic and the proposed contract.656 records and175 scholarly PDFs are traceable;omissions and file-specific rights remain explicit.',
        'Q3':'Five authored reference families reproduce equal Gaussian observational laws with different interventions,score defaults,repeated-subject variance,state-label conversion and constraint predicates. Separate enumeration and covariance calculations pass. No upstream compilation,runtime,prototype accuracy or bank truth is claimed.',
        'Q4':'Stipulated net6/-4USD and93.2/70.8USD differences motivate checking intervention and conversion meaning before costly bank studies. Generated cases,public-data roles,full workflow costs and license/environment prerequisites are explicit;actual performance,prices and bank ROI remain unclaimed.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE);assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),ref(BASE/'release-source-review.json','Inspected native temporal delta'),
            ref(work.OUTPUT,'Reviewed bounded comparison'),ref(WORK/'independent-verification-v2.json','Reproduced illustrative economics'),
            ref(Path(__file__),'Review findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires preserved successor author review.',
            'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record reviewed native temporal delta with preserved evidence and scope limits.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader proposal delta review'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':work.REVIEWER,
            'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only','scope':scope,
            'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open'}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['review','record','publish','renew']);args=p.parse_args()
    {'review':review,'record':record,'publish':publish,'renew':renew}[args.command]()
