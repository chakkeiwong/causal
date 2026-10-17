#!/usr/bin/env python3
"""Publish the reviewed S8 working reader and preserve exact-reader reviews."""
import argparse
import json
from pathlib import Path
import build_s8_reader_v3_20261017 as build
import prepare_s8_20261017 as work
import review_s8_20261017 as review
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT


def read(p):return json.loads(p.read_text())


def verify():
    report=read(OUT/'build-report.json')
    for p in [OUT/'build-report.json',BASE/'release-source-review.json',
              BASE/'draft-operation-receipt.json',BASE/'review-operation-receipt.json',review.REVIEW]:
        verify_bindings(read(p))
    measured=read(review.REVIEW)
    assert report['cited_records']==726 and measured['status']=='pass'
    assert measured['allocation_minimum_met'] and measured['substantive_page_credit']>=10
    assert read(OUT/'text-layout-review.json')['status']=='pass'
    build.verify_exact()
    return report


def record():
    verify()
    for identifier,name in [('TEXT.DRAFT.S8','draft-operation-receipt.json'),('TEXT.REVIEW.S8','review-operation-receipt.json')]:
        state=core.read(ROOT,core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256']==core.sha(BASE/name)
            continue
        transition('record',identifier,BASE/name)


def publish():
    report=verify();state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.CANONICAL_OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(k in state['execution_program']['results'] for k in ['TEXT.DRAFT.S8','TEXT.REVIEW.S8'])
    audit=read(OUT/'source-audit.json');reviewed=read(BASE/'release-source-review.json')
    measured=read(review.REVIEW)
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving commercial reader'),
        source_review=ref(BASE/'release-source-review.json','Author source, math and exclusive-depth review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=audit['tex_files']+reviewed['evidence']+[
            ref(review.REVIEW,f"Exclusive S8 credit{measured['substantive_page_credit']}"),
            ref(Path(__file__),'Publication and exact-reader delta procedure')],
        visual_acceptance=False,mandatory_repairs_closed=[],
        changes=['Develop four banking purchasing units,17-area commercial comparison and explicit capability/edition/rights omissions.',
                 'Derive information-parent utility, matched route costs, quote ceiling and complete-choice compatibility signal.',
                 'Develop loaded-instance residency, online versus known-batch acquisition and shared cold-recovery dependencies; preserve two depth failures.'],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed S8 working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_s8_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report=verify();depth=read(review.REVIEW)['substantive_page_credit']
    findings={
        'Q2':'All721 canonical source records, compiled sources and citation-context multisets survive; all724 and725 candidate records are unchanged.726 records retain188 genuine scholarly PDFs. Eighteen inspected primary excerpts support scoped commercial claims; edition, rights, prices, historical cutoff bytes and vendor runtime omissions remain explicit. Changed S8 windows are recomputed.',
        'Q3':f'Exact cost,quote,regret,scheduling,information-parent and full-choice signal laws reproduce. Residency recurrence and exhaustive resident paths agree; all729 workload sequences match independent probability formulas. Shared/local cold-readiness enumeration confirms the conditional ceiling. Equations25.1-25.23 and all-page bounds pass;{depth} exclusive page equivalents meet minimum10. No vendor execution, general uptime or bank calibration is inferred.',
        'Q4':'The complete-choice compatibility signal has gross value7250, net2250 at5000 and negative7750 at15000; perfect information has value10000. Timely history changes stipulated feasible utility5 to0. Known-batch, expected online and hard-deadline choices select different capacities; shared validation can make a99-percent recovery target unattainable by adding replicas. Every price, probability and duration is hypothetical; actual procurement and ROI remain open.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=read(ROOT/previous['path'])
        if run.same_reader(old.get('reviewed_reader',{}),report['pdf']):
            assert old['outcome']=='pass';continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),
                  ref(BASE/'release-source-review.json','Source/math author review'),
                  ref(review.REVIEW,'Exclusive S8 topic/depth review'),
                  ref(work.BASE/'exact-results.json','Original exact acquisition laws'),
                  ref(build.previous.extension.BASE/'exact-results.json','Residency and workload laws'),
                  ref(build.extension.BASE/'exact-results.json','Cold-recovery readiness law'),
                  ref(Path(__file__),'Exact-reader delta findings')]
        write(folder/'reopen.json',dict(reason='Changed reader needs preserved successor author review.',
            prior_result=previous,reviewed_reader=report['pdf'],evidence=evidence,
            next_action='Record scoped S8 source, mathematics and economic delta.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state)
        node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+review.LIMITS))
        scope='Author exact-reader delta review; proposal evidence only'
        write(output,dict(operation=identifier,status='pass',criterion=node['criteria'][0],reviewer=review.REVIEWER,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,
            findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=review.REVIEWER,
            limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Exact-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['record','publish','renew'])
    args=parser.parse_args();{'record':record,'publish':publish,'renew':renew}[args.command]()
