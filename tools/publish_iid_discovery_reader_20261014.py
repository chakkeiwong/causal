#!/usr/bin/env python3
"""Review, publish and renew scoped iid-discovery proposal evidence."""
import argparse
import json
from pathlib import Path

import build_iid_discovery_reader_20261014 as build
import review_iid_discovery_20261014 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT


def review():
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(build.PRIOR.read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((work.BASE/'author-review.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass'and not index['issues']and index['scholarly_pdfs']==164
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not [w for w in report['warnings']if'Underfull'not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==577 and len(new)==582 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files']if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256']for r in kept)
    previous=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:r['citation_contexts']for r in index['records']}
    assert all(all(c in contexts[r['citation_key']]for c in r['citation_contexts'])for r in previous['records'])
    assert json.loads(json.dumps(work.exact()))==json.loads((work.BASE/'exact-results.json').read_text())
    text=' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['From language guidance to a defensible discovery','A token score does not',
                   'covariance determinant is three','USD 6 per decision','0.95',
                   'fine-tuning','missing stored row returns zero']:
        assert phrase.lower()in text.lower(),phrase
    evidence=[ref(p,a)for p,a in[
        (OUT/'build-report.json','Exact preserving successor'),
        (OUT/'source-audit.json','582 citations with original identities'),
        (BASE/'traceability-review.json','All inherited contexts retained;164 genuine scholarly PDFs'),
        (OUT/'text-layout-review.json','All-page bounds and extraction'),
        (OUT/'reader.txt','Inspected integrated discovery section'),
        (work.BASE/'primary-review.json','Fourteen pinned source blobs and primary papers'),
        (work.BASE/'exact-results.json','Independent exact Gaussian, token and decision examples'),
        (work.BASE/'prototype-contract.json','Proposed generated/public adapter and discovery comparison'),
        (work.BASE/'author-review.json','Scoped proposal decision'),
        (Path(__file__).resolve(),'Exact-reader review and publication procedure')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,
        'reviewed_reader':report['pdf'],'scope':'Author review of primary iid-discovery sources and exact examples; no native execution',
        'evidence':evidence,'preserved_records':577,'new_records':5,'preserved_compiled_sources':len(kept),
        'original_contexts_retained':True,'findings':[
            'Identical observed Gaussian laws retain consequential causal ambiguity with allowed latent mechanisms.',
            'Response tests and token scores remain distinct from sampling-law tests and effect confidence.',
            'Missing answers, hardcoded metadata, token parsing and backend constraint semantics yield concrete prototype remedies.',
            'The recovered materials original supports its documented workflow, not a trained checkpoint or calibrated effect claim.',
            'All inherited scientific bytes and citation contexts remain; new contexts have explicit primary anchors.'],
        'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'new_records':5}))


def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k]for k in['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving discovery reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page text bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Develop primary iid-discovery evidence and three pinned package families.',
            'Derive clock-compatible Gaussian ambiguity, token/threshold cases and decision value.',
            'Specify public/generated adapter and matched discovery remedies without enabling integration.'],
        'sponsor_binding':'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed discovery working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k]for k in['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_iid_discovery_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))


def renew():
    report=json.loads((OUT/'build-report.json').read_text())
    verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={
        'Q2':'All577 inherited records and citation contexts retained; five additions produce582 records and164 genuine scholarly PDFs. Fourteen source blobs match pinned trees. The recovered materials original has version metadata and inspected primary anchors. Missing originals and wider coverage remain explicit.',
        'Q3':'Inherited demonstrations remain unchanged. Gaussian covariance/effects, token/threshold cases, ancestry and conditional decision values reproduce exactly. No live LLM or upstream execution is claimed; the matched public/generated study remains proposed.',
        'Q4':'Stipulated action values40/minus60USD yield expected30USD and perfect-information upper bound6USD at assumed direct-world probability0.9. This is neither bank ROI nor an experiment budget. The proposed comparison includes all-request losses, refusals and complete workflow costs.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),
            ref(BASE/'release-source-review.json','Source, math and text review'),
            ref(work.OUTPUT,'Discovery synthesis and prototype obligations'),
            ref(work.BASE/'exact-results.json','Exact constructions'),ref(Path(__file__).resolve(),'Exact-reader findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires a preserved successor review.',
            'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record exact-reader discovery source, demonstration and economics review.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state)
        node=run.ledger.operation(graph,identifier);attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader delta review; proposal evidence only'
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
    p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish','renew']);a=p.parse_args()
    {'review':review,'publish':publish,'renew':renew}[a.command]()
