#!/usr/bin/env python3
"""Publish the recovered S7 working reader and bind its author delta reviews."""
import argparse
import json
from pathlib import Path

import build_s7_reader_v2_20261017 as build
import prepare_s7_20261017 as work
import review_s7_20261017 as review
import s7_depth_extension_20261017 as extension
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
    assert report['pages']==977 and report['cited_records']==721
    assert measured['status']=='pass' and measured['substantive_page_credit']==9.25
    assert measured['allocation_minimum_met'] and measured['planning_target_met']
    assert work.examples.calculate()==read(work.BASE/'exact-results.json')
    assert extension.calculate()==read(extension.BASE/'exact-results.json')
    assert read(OUT/'text-layout-review.json')['status']=='pass'
    return report


def record():
    verify()
    for identifier,name in [('TEXT.DRAFT.S7','draft-operation-receipt.json'),('TEXT.REVIEW.S7','review-operation-receipt.json')]:
        state=core.read(ROOT,core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256']==core.sha(BASE/name)
            continue
        transition('record',identifier,BASE/name)


def publish():
    report=verify();state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.CANONICAL_OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(key in state['execution_program']['results'] for key in ['TEXT.DRAFT.S7','TEXT.REVIEW.S7'])
    audit=read(OUT/'source-audit.json');reviewed=read(BASE/'release-source-review.json')
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=977,
        supersedes={key:state['reader'][key] for key in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving977-page observation/transport reader'),
        source_review=ref(BASE/'release-source-review.json','Author source, mathematics and exclusive-depth review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=audit['tex_files']+reviewed['evidence']+[
            ref(review.REVIEW,'9.25 exclusive pages meet minimum8 and target9'),
            ref(Path(__file__),'Publication and exact-reader delta review procedure')],
        visual_acceptance=False,mandatory_repairs_closed=[],
        changes=['Develop joint relationship/action meaning, feasible coordination, topology transport and sharp pooled-information target bounds.',
                 'Derive prospective truthful joint-audit design, target weighting and matched price-constrained alternatives.',
                 'Use an exact pooled constraint to optimize a declared variance envelope; retain noisy-pool variance, covariance and bias, plus the original depth failure.'],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed S7 working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={key:report['pdf'][key] for key in ['path','sha256']}
    state['reader'].update(pages=977,status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_s7_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report=verify()
    findings={
        'Q2':'All717 canonical source records and citation-context multisets survive; all720 initial-candidate records are unchanged. The721-record reader cites188 genuine scholarly PDFs. Ten authentic primary excerpts retain scientific, version and cutoff limitations. Removing one inserted input recovers the initial logical chapter; changed source paths and citation windows are recomputed explicitly.',
        'Q3':'Exact finite graph/action and eight-node topology enumeration, sharp pooled-moment witnesses,473-audit concentration design and target/price allocations reproduce. The new constraint-aware coefficient proof, global envelope attainment, twelve finite Bernoulli audit laws and noisy-pool covariance checks support equations24.1-24.33. All-page text bounds pass.9.25 exclusive pages meet minimum8 and target9. No actual minimax variance, sampled coverage or upstream runtime qualification is established.',
        'Q4':'Separate edge margins leave sharp hypothetical value[-8,8]; feasible coordinated pair actions can remove the overlap term under the matched baseline. Exact pooled information leaves transported value[-10/3,58/3]. The constraint-aware envelope at700 equal-price audits is1156/1575 versus28/25; at prices(1,4)/budget1820 it is4624/4095 versus52/35. All methods share already-available pooled information. Noisy-pool error retains coefficient32/3 and covariance8704/9. These are exact hypothetical design comparisons, not empirical bank benefit or ROI.'}
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
                  ref(review.REVIEW,'Exclusive S7 topic/depth review'),
                  ref(work.BASE/'exact-results.json','Exact graph/action, topology, transport and audit laws'),
                  ref(extension.BASE/'exact-results.json','Constraint-aware global envelope, budget and covariance references'),
                  ref(Path(__file__),'Exact-reader delta findings')]
        write(folder/'reopen.json',dict(reason='Changed reader requires preserved successor author review.',
            prior_result=previous,reviewed_reader=report['pdf'],evidence=evidence,
            next_action='Record scoped S7 source, mathematics and financial delta.'))
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
