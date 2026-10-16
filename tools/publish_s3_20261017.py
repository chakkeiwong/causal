#!/usr/bin/env python3
"""Publish the reviewed identification successor and renew exact-reader reviews."""
import argparse
import json
from pathlib import Path

import build_s3_reader_v3_20261017 as build
import prepare_s3_20261017 as work
import review_s3_20261017 as review
import s3_sensitivity_20261017 as sensitivity
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
    assert report['pages']==899 and report['cited_records']==703
    assert measured['status']=='pass' and measured['substantive_page_credit']==10
    assert measured['allocation_minimum_met'] and not measured['planning_target_met']
    assert work.examples.calculate()==read(work.BASE/'exact-results.json')
    assert sensitivity.calculate()==read(sensitivity.BASE/'exact-results.json')
    assert read(OUT/'text-layout-review.json')['status']=='pass'
    return report


def record():
    verify()
    for identifier,name in [('TEXT.DRAFT.S3','draft-operation-receipt.json'),('TEXT.REVIEW.S3','review-operation-receipt.json')]:
        state=core.read(ROOT,core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256']==core.sha(BASE/name)
            continue
        transition('record',identifier,BASE/name)


def publish():
    report=verify();state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    # V2 was an unpublished candidate. Publication succeeds the canonical 883-page reader.
    assert state['reader']['path']==str(build.CANONICAL_OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(k in state['execution_program']['results'] for k in ['TEXT.DRAFT.S3','TEXT.REVIEW.S3'])
    audit=read(OUT/'source-audit.json');reviewed=read(BASE/'release-source-review.json')
    manifest=dict(
        kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving 899-page identification reader'),
        source_review=ref(BASE/'release-source-review.json','Author source, mathematics and exclusive-depth review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=audit['tex_files']+reviewed['evidence']+[
            ref(review.REVIEW,'Ten substantive pages meet minimum; target twelve unmet'),
            ref(Path(__file__),'Publication and review procedure')],
        visual_acceptance=False,mandatory_repairs_closed=[],
        changes=['Connect identification, individual counterfactuals, IV targets and effect-set decisions.',
                 'Develop exact full-table sharp bounds, bounded defiers and explicitly outer exclusion sensitivity.',
                 'Preserve initial depth failure and correct five equation references in an immutable successor.'],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed S3 working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=899,status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_s3_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report=verify()
    findings={
        'Q2':'All699 canonical records and702 original-candidate records/contexts survive. All703 V2 records are unchanged;187 genuine scholarly PDFs remain. Five equation displays alone are numbered in a preserving sensitivity copy, with exact new context windows verified.',
        'Q3':'Six exact authored law families, separate algebra and36 feasible sensitivity vertices reproduce. Full eight-cell witnesses establish sharp IV population and bounded-defier complier ranges. Explicit Y(z,d) exclusion envelopes are necessary outer ranges only. Five equation references are repaired. No upstream, empirical or universal qualification is inferred.',
        'Q4':'Stipulated USD100/12 values map consistency effects to[-42,58] and IV population effects to[-28,32] USD. Ten-percent defier budget gives sharp complier[1/25,9/25] and net[-8,24]. Direct-encouragement budgets give explicitly outer net[3,13] or[-2,18]. Feasible randomized encouragement has exact net6/5USD with2USD message cost; these are illustrations, not bank ROI.'}
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
                  ref(review.REVIEW,'Exclusive S3 subject/depth review'),
                  ref(work.BASE/'exact-results.json','Six exact authored families'),
                  ref(sensitivity.BASE/'exact-results.json','Full-law sensitivity witnesses'),
                  ref(Path(__file__),'Exact-reader delta findings')]
        write(folder/'reopen.json',dict(
            reason='Changed reader requires preserved successor author review.',prior_result=previous,
            reviewed_reader=report['pdf'],evidence=evidence,
            next_action='Record scoped S3 source, mathematics and decision delta.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state)
        node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+review.LIMITS))
        scope='Author exact-reader delta review; proposal evidence only'
        write(output,dict(operation=identifier,status='pass',criterion=node['criteria'][0],reviewer=work.REVIEWER,
                          reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
                          scope=scope,findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,limitations=limits,
                       reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
                       outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
                       criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt)
        transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['record','publish','renew'])
    args=parser.parse_args();{'record':record,'publish':publish,'renew':renew}[args.command]()
