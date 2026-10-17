#!/usr/bin/env python3
"""Publish reviewed S9 without losing prior candidates or exact-reader gates."""
import argparse
import json
from pathlib import Path
import s9_successor_v4_20261017 as build
import review_s9_20261017 as review
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.PUB,build.OUT


def read(p):return json.loads(p.read_text())


def verify():
    report=read(OUT/'build-report.json')
    for p in [OUT/'build-report.json',BASE/'release-source-review.json',BASE/'draft-operation-receipt.json',
              BASE/'review-operation-receipt.json',review.REVIEW]:verify_bindings(read(p))
    measured=read(review.REVIEW)
    assert report['cited_records']==731 and measured['status']=='pass'
    assert measured['allocation_minimum_met'] and 6<=measured['substantive_page_credit']<=10
    assert read(OUT/'text-layout-review.json')['status']=='pass'
    build.verify_exact()
    return report


def record():
    verify()
    for identifier,name in [('TEXT.DRAFT.S9','draft-operation-receipt.json'),('TEXT.REVIEW.S9','review-operation-receipt.json')]:
        state=core.read(ROOT,core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256']==core.sha(BASE/name);continue
        transition('record',identifier,BASE/name)


def publish():
    report=verify();state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.CANONICAL_OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(k in state['execution_program']['results'] for k in ['TEXT.DRAFT.S9','TEXT.REVIEW.S9'])
    audit=read(OUT/'source-audit.json');reviewed=read(BASE/'release-source-review.json')
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving S9 reader'),
        source_review=ref(BASE/'release-source-review.json','Exact source/math/exclusive-depth review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page bounds'),
        source_artifacts=audit['tex_files']+reviewed['evidence']+[
            ref(review.REVIEW,'S9 exclusive depth7.0; minimum6 met; target8 unmet'),ref(Path(__file__),'Publication and exact-reader delta procedure')],
        visual_acceptance=False,mandatory_repairs_closed=[],
        changes=['Develop pinned R/Python/Java/C++ reuse routes with explicit bridge and port limitations.',
                 'Derive numerical composition, adaptive conditional laws, retry selection, persistent failures and correction variance.',
                 'Preserve all three failed-depth candidates and repair14 misleading source-review pointers in a successor.'],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed S9 working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_s9_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report=verify()
    findings={
        'Q2':'All726 canonical source records, compiled sources and citation contexts survive; all730 v3 records remain unchanged.731 audited records retain188 genuine scholarly PDFs. Fourteen descriptive provenance pointers are corrected in a preserving successor, with original records and line anchors unchanged. This remains bounded source review, not complete license/dependency or historical-cutoff closure.',
        'Q3':'Exact K1–4 finite attempt paths agree with independent closed forms. Adaptive conditional-kernel and numerical composition derivations state their domains. Retained-result missing-score bounds are[0,9/16]; inverse-correction variance is23/14 and a misspecified completion probability creates bias1/16. All19 equations, source preservation and all-page bounds pass.7.0 exclusive pages meet minimum6; target8 unmet. No upstream runtime or bank calibration is inferred.',
        'Q4':'Two retries with identical expected cost11/8 calls can have completion55/64 versus23/32 and returned-score means3/5 versus9/23. At a stipulated USD100 per score unit these become USD60 and aboutUSD39.13 despite an ideal zero mean. All-assigned fallback value and computation cost must be included; these are exact hypothetical reporting distortions, not observed intervention benefit or ROI.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=read(ROOT/previous['path'])
        if run.same_reader(old.get('reviewed_reader',{}),report['pdf']):
            assert old['outcome']=='pass';continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),ref(BASE/'release-source-review.json','Source/math author review'),
                  ref(review.REVIEW,'Exclusive S9 topic and depth review'),ref(BASE/'exact-results.json','Finite composition and retry laws'),
                  ref(BASE/'primary-source-review-successor.json','Corrected source pointers'),ref(Path(__file__),'Exact-reader delta findings')]
        write(folder/'reopen.json',dict(reason='Changed reader needs a preserving successor author review.',prior_result=previous,
            reviewed_reader=report['pdf'],evidence=evidence,next_action='Record scoped S9 source, mathematical and economic delta.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+review.LIMITS));scope='Author exact-reader delta review; proposal evidence only'
        write(output,dict(operation=identifier,status='pass',criterion=node['criteria'][0],reviewer=review.REVIEWER,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,
            findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=review.REVIEWER,limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Exact-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2–Q4 pass',Q1_Q5='open',proposal_accepted=False)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['record','publish','renew']);a=p.parse_args()
    {'record':record,'publish':publish,'renew':renew}[a.command]()
