#!/usr/bin/env python3
"""Publish the reviewed S4 reader and renew its exact-reader author deltas."""
import argparse
import json
from pathlib import Path

import build_s4_reader_v2_20261017 as build
import prepare_s4_20261017 as work
import review_s4_20261017 as review
import s4_extension_20261017 as extension
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
    assert report['pages']==917 and report['cited_records']==707
    assert measured['status']=='pass' and measured['substantive_page_credit']==12
    assert measured['allocation_minimum_met'] and not measured['planning_target_met']
    assert work.examples.calculate()==read(work.BASE/'exact-results.json')
    assert extension.calculate()==read(extension.BASE/'exact-results.json')
    assert read(OUT/'text-layout-review.json')['status']=='pass'
    return report


def record():
    verify()
    for identifier,name in [('TEXT.DRAFT.S4','draft-operation-receipt.json'),('TEXT.REVIEW.S4','review-operation-receipt.json')]:
        state=core.read(ROOT,core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256']==core.sha(BASE/name)
            continue
        transition('record',identifier,BASE/name)


def publish():
    report=verify();state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.CANONICAL_OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(k in state['execution_program']['results'] for k in ['TEXT.DRAFT.S4','TEXT.REVIEW.S4'])
    audit=read(OUT/'source-audit.json');reviewed=read(BASE/'release-source-review.json')
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=917,
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving917-page effects reader'),
        source_review=ref(BASE/'release-source-review.json','Author source, mathematics and exclusive-depth review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=audit['tex_files']+reviewed['evidence']+[
            ref(review.REVIEW,'Twelve substantive pages meet minimum ten; target fourteen unmet'),
            ref(Path(__file__),'Publication and review procedure')],
        visual_acceptance=False,mandatory_repairs_closed=[],
        changes=['Connect assignment-dependent estimands, fitted score paths and exact remainders.',
                 'Develop common-population joint comparisons, precision design and resource/robust allocation.',
                 'Prove restricted finite-policy bounds and sharp discrete-score restrictions; preserve the initial depth failure.'],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed S4 working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=917,status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_s4_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report=verify()
    findings={
        'Q2':'All703 canonical and706 first-candidate records and citation-context multisets survive;707 audited records and187 genuine scholarly PDFs support the successor. Thirteen original excerpts and inherited version/cutoff limits remain explicit.',
        'Q3':'Seven original and five extension exact-reference families reproduce with separate checks. Assignment derivatives, overlap remainder, common-population covariance, resource duals, quadratic/fuzzy approximation and sharp Lipschitz witnesses have scoped derivations. Extension equations21.14-21.23 and extracted pages agree. Finite-policy concentration assumes known randomized assignment, independent evaluation and bounded fixed candidates; no new measured coverage or package qualification is inferred.',
        'Q4':'Stipulated costs/resources yield exact allocation net13/5 versus3/2USD. Rectangular net gains give maximin guarantee2 with worst regret2, versus minimax regret1 with guarantee3/2. Known bounded randomized scores give sufficient selected-policy regret4.4936USD at10000 accounts and201921 accounts for a1USD sufficient bound. Unit Lipschitz score-gap restrictions give effect[2,6] and net[-1,3]USD. These are proofs/illustrations, not bank ROI or a recommended pilot size.'}
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
                  ref(review.REVIEW,'Exclusive S4 subject/depth review'),
                  ref(work.BASE/'exact-results.json','Seven exact authored families'),
                  ref(extension.BASE/'exact-results.json','Five scoped derivation/bound families'),
                  ref(Path(__file__),'Exact-reader delta findings')]
        write(folder/'reopen.json',dict(reason='Changed reader requires preserved successor author review.',
            prior_result=previous,reviewed_reader=report['pdf'],evidence=evidence,
            next_action='Record scoped S4 source, mathematics and financial delta.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state)
        node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+review.LIMITS))
        scope='Author exact-reader delta review; proposal evidence only'
        write(output,dict(operation=identifier,status='pass',criterion=node['criteria'][0],
            reviewer=work.REVIEWER,reviewed_reader=report['pdf'],review_attempt=attempt,
            acceptance_scope='proposal_only',scope=scope,findings=[finding],evidence=evidence,
            limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,
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
