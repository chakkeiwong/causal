#!/usr/bin/env python3
"""Publish the preserving S6 reader and renew its exact-reader author reviews."""
import argparse
import json
from pathlib import Path

import build_s6_reader_v2_20261017 as build
import prepare_s6_20261017 as work
import review_s6_20261017 as review
import s6_depth_extension_20261017 as extension
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT


def read(path):
    return json.loads(path.read_text())


def verify():
    report=read(OUT/'build-report.json')
    for path in [OUT/'build-report.json',BASE/'release-source-review.json',
                 BASE/'draft-operation-receipt.json',BASE/'review-operation-receipt.json',review.REVIEW]:
        verify_bindings(read(path))
    measured=read(review.REVIEW)
    assert report['pages']==963 and report['cited_records']==717
    assert measured['status']=='pass' and measured['substantive_page_credit']==14.75
    assert measured['allocation_minimum_met'] and not measured['planning_target_met']
    assert work.examples.calculate()==read(work.BASE/'exact-results.json')
    assert extension.calculate()==read(extension.BASE/'exact-results.json')
    assert read(OUT/'text-layout-review.json')['status']=='pass'
    return report


def record():
    verify()
    for identifier,name in [('TEXT.DRAFT.S6','draft-operation-receipt.json'),('TEXT.REVIEW.S6','review-operation-receipt.json')]:
        state=core.read(ROOT,core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256']==core.sha(BASE/name)
            continue
        transition('record',identifier,BASE/name)


def publish():
    report=verify();state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.CANONICAL_OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(key in state['execution_program']['results'] for key in ['TEXT.DRAFT.S6','TEXT.REVIEW.S6'])
    audit=read(OUT/'source-audit.json');reviewed=read(BASE/'release-source-review.json')
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=963,
        supersedes={key:state['reader'][key] for key in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving963-page panel/time-series reader'),
        source_review=ref(BASE/'release-source-review.json','Author source, mathematics and exclusive-depth review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=audit['tex_files']+reviewed['evidence']+[
            ref(review.REVIEW,'14.75 exclusive pages meet minimum14; target17 unmet'),
            ref(Path(__file__),'Publication and exact-reader review procedure')],
        visual_acceptance=False,mandatory_repairs_closed=[],
        changes=['Develop heterogeneous event-time projection, sharp trend budgets and signed donor/calendar uncertainty.',
                 'Prove joint unit/time oracle risk and compare constrained versus exact weighting on one law.',
                 'Distinguish feedback interventions and full replacement value with paired action costs, robust convergence and monetary tails; retain the initial depth failure.'],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed S6 working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={key:report['pdf'][key] for key in ['path','sha256']}
    state['reader'].update(pages=963,status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_s6_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report=verify()
    findings={
        'Q2':'All712 canonical records and citation contexts survive; all716 initial-candidate records remain unchanged. The717-record reader cites188 genuine scholarly PDFs. Eleven primary excerpts preserve version/cutoff limits. Removing the inserted input recovers the exact first chapter; changed paths/windows are recomputed rather than falsely declared identical.',
        'Q3':'Exact projection/FWL, curvature vertices, donor contamination, factor noise, calendar covariance and feedback references reproduce. New polynomial certificates,512-sign enumeration and direct two-regime recursion support equations23.1-23.62. All-page text bounds pass.14.75 exclusive pages meet minimum14, target17 unmet. Fixed oracle weights, supplied structural class and convergence limits do not qualify fitted packages or empirical coverage.',
        'Q4':'On the stipulated joint-weight law at s1/8, global risk1 compares with1.5 nonnegative and4.5 both-axis exact. Supplied beta[1,2] and costs give rule.44 worst infinite value52.7002USD but-5.4812USD through index20; rule.47 can have convergent benefits and adverse divergent expenses. The H80 paired tail has uniform bound4.3531689459USD. These are authored exact sensitivity examples, not bank ROI or measured package results.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=read(ROOT/previous['path'])
        if run.same_reader(old.get('reviewed_reader',{}),report['pdf']):
            assert old['outcome']=='pass'
            continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),
                  ref(BASE/'release-source-review.json','Author source/math review'),
                  ref(review.REVIEW,'Exclusive S6 topic/depth review'),
                  ref(work.BASE/'exact-results.json','Exact initial authored laws'),
                  ref(work.BASE/'robust-results.json','Contamination and calendar references'),
                  ref(work.BASE/'value-checks/exact-results.json','Action costs and tails'),
                  ref(extension.BASE/'exact-results.json','Joint global weights and full-controller values'),
                  ref(Path(__file__),'Exact-reader delta findings')]
        write(folder/'reopen.json',dict(reason='Changed reader requires preserved successor author review.',
            prior_result=previous,reviewed_reader=report['pdf'],evidence=evidence,
            next_action='Record scoped S6 source, mathematics and financial delta.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state)
        node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+review.LIMITS))
        scope='Author exact-reader delta review; proposal evidence only'
        write(output,dict(operation=identifier,status='pass',criterion=node['criteria'][0],
            reviewer=review.REVIEWER,reviewed_reader=report['pdf'],review_attempt=attempt,
            acceptance_scope='proposal_only',scope=scope,findings=[finding],evidence=evidence,
            limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=review.REVIEWER,
            limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,
            acceptance_scope='proposal_only',outputs=[ref(output,'Current-reader '+q+' author review')],
            nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt)
        transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['record','publish','renew'])
    args=parser.parse_args();{'record':record,'publish':publish,'renew':renew}[args.command]()
