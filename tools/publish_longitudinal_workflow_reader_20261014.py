#!/usr/bin/env python3
"""Review, record and publish L5 author work with exact-reader continuity."""
import argparse
import json
from pathlib import Path
import re

import build_longitudinal_workflow_reader_20261014 as build
import develop_longitudinal_workflow_20261014 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT=core.ROOT
BASE=build.BASE
OUT=build.OUT
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
LIMITS=[
    'Author review only; no independent scientific or bank acceptance.',
    'Exact known-law identities and moments do not qualify fitted estimators or confidence coverage.',
    'No ltmle, OCI, other upstream engine, live model or bank experiment was executed by this work.',
    'Whole-manuscript coverage/depth and Q1 remain open; draft completion does not confer page credit.',
    'Inherited six-preview allowance is exhausted under /home/ubuntu/AGENTS.md; further rendered-image review requires a fresh session.',
    'Sponsor reconciliation and Q5 exact-release acceptance remain open.',
]


def review():
    work.verify()
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(work.PRIOR.read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    layout=json.loads((OUT/'text-layout-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text())]:
        verify_bindings(obj)
    assert index['status']=='pass' and not index['issues']
    assert layout['status']=='pass'
    assert not [s for s in report['warnings'] if 'Underfull' not in s]
    old={s['integrated_citation_key']:s for s in prior['sources']}
    current={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(current)==515 and all(current[k]==s for k,s in old.items())
    assert set(current)-set(old)=={'exec14_workflow_oracle'}
    prior_files={r['path']:r for r in prior['tex_files']}
    current_files={r['path']:r for r in audit['tex_files']}
    inherited=set(prior_files)-{str(build.OLD.relative_to(ROOT))}
    assert all(current_files[k]['sha256']==prior_files[k]['sha256'] for k in inherited)
    text=re.sub(r'\s+',' ',(OUT/'reader.txt').read_text())
    for phrase in ['Servicing decisions: intervention histories and net value',
                   'Retention, recursive augmentation and uncertainty',
                   'Branch adoption is a panel question with a different target',
                   'Observation construction can determine the answer',
                   'What assistance and software reuse can responsibly achieve',
                   '97.5','248.832','1228.8','17500']:
        assert phrase.lower() in text.lower(),phrase
    evidence=[ref(OUT/'build-report.json','Exact compiled successor'),
        ref(OUT/'source-audit.json','515 whole-reader source records'),
        ref(BASE/'traceability-review.json','All citation contexts and153 genuine scholarly PDFs'),
        ref(OUT/'text-layout-review.json','Every-page text/bounds review'),
        ref(BASE/'prepared-inputs.json','Preserving input identities'),
        ref(work.BASE/'primary-review.json','Five actual technical rereads'),
        ref(work.BASE/'exact-oracle.json','Eight-history independent exact enumeration'),
        ref(work.CHAPTER,'Preserving L5 chapter'),ref(work.ADDITION,'Reviewed connected development'),
        ref(Path(__file__),'Review and publication procedure')]
    findings=[
        'Sequential policy value, transition law, matching bias, mediator substitution and gross/net value are distinguished and reproduce94.8/68/90.',
        'Retention correction requires its conditional observation law; the augmented score is centered term by term and known-law moments are not advertised as fitted coverage.',
        'Sequential robustness is attributed to the inspected recursive construction, not a point-treatment loop.',
        'Cohort/time ATT, anticipation and comparison support are separate from dynamic policies. Valid effects5/15/4, contaminated−6, aggregation8/4.5 and the exact within coefficient are consistent.',
        'An identical observed panel with an untreated cohort shock changes the early effect, so pretrend agreement is not treated as proof.',
        'Sampling-frame inclusion, label inversion and shared branch/calendar covariance are distinguished from ownership truth and individual effect identification.',
        'Point-treatment OCI and source-inspected ltmle are discussed with their actual scope and interface restrictions; analyst baselines and unresolved outputs are developed.',
        '514 inherited citation records and all inherited chapter bytes remain unchanged; one new source binds the exact project mechanisms.']
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':REVIEWER,
        'scope':'Exact-reader L5 content, source, mathematical and banking delta; no automatic depth or visual acceptance',
        'reviewed_reader':report['pdf'],'findings':findings,'evidence':evidence,
        'unchanged_source_records':514,'new_source_records':['exec14_workflow_oracle'],
        'unchanged_inherited_compiled_sources':len(inherited),
        'limits':LIMITS,'visual_acceptance':False,'bank_ROI_established':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'cited_sources':515,
                      'exact_reference':'pass','page_credit_awarded':False}))


def record_draft():
    reviewed=json.loads((BASE/'release-source-review.json').read_text())
    verify_bindings(reviewed)
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']=='TEXT.DRAFT.L5'
    graph,_,_=run.combined(ROOT,state)
    node=run.ledger.operation(graph,'TEXT.DRAFT.L5')
    receipt=run.ledger.receipt_template(node)
    evidence=[ref(BASE/'release-source-review.json','Actual content/source/mathematics author review'),
              ref(work.BASE/'primary-review.json','Primary-text rereads'),
              ref(work.BASE/'exact-oracle.json','Reproducible finite mechanisms')]
    facts=['Connected argument develops longitudinal policies, retention, recursive scores, panel comparisons, observation truth, diagnostics and matched alternatives.',
           'Five primary texts and inherited OCI evidence support scoped claims; exact project mechanisms replay and are explicitly distinct from bank data and fitted qualification.']
    receipt.update(outcome='pass',execution='performed',scope=reviewed['scope'],reviewer=REVIEWER,
        limitations=LIMITS,outputs=[ref(work.CHAPTER,'Completed L5 workflow development')],
        nonexecution_reason='',revisit_trigger='',
        criteria=[{'index':i,'verdict':'pass','finding':fact,'evidence':evidence} for i,fact in enumerate(facts)])
    write(work.BASE/'operation-receipt.json',receipt)
    transition('record','TEXT.DRAFT.L5',work.BASE/'operation-receipt.json')


def publish():
    state=core.read(ROOT,core.STATE)
    before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert 'TEXT.DRAFT.L5' in state['execution_program']['results']
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    review=json.loads((BASE/'release-source-review.json').read_text())
    verify_bindings(review)
    manifest={'kind':'working_monograph','final_acceptance':False,
        'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Compiled preserving L5 successor'),
        'source_review':ref(BASE/'release-source-review.json','Actual content/source/mathematics delta review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page text and physical bounds'),
        'source_artifacts':audit['tex_files']+review['evidence'],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Developed sequential servicing, retention and known-law uncertainty.',
                   'Developed staggered panel targets, alternatives and counterfactual ambiguity.',
                   'Developed population inclusion, noisy labels, dependence and assistant/reuse limits.'],
        'sponsor_binding':'Preserved sponsor baseline;Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed longitudinal/panel/observation working reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_longitudinal_workflow_reader',
                                'manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'final_acceptance':False}))


def renew():
    report=json.loads((OUT/'build-report.json').read_text())
    findings={
        'Q2':'All514 predecessor source records and inherited chapter bytes are retained; one new record binds exact project laws. Five current primary-text rereads and whole-reader traceability support the scoped development. Census completeness and whole-repair depth receive no waiver.',
        'Q3':'Earlier demonstration evidence and negative verdicts remain unchanged. Eight-history enumeration verifies policy and retention values; exact cohort residualization, framed means, label inversion and known-law score moments reproduce. No fitted interval study, upstream estimator, live agent or bank experiment is inferred.',
        'Q4':'Preserved investment scenarios remain unchanged. The new servicing example includes gross recovery and contact costs, distinguishes fixed-policy values and explains why the narrow public/generated-data prototype can test target errors before expensive bank trials. Full bank costs, prices, learned-policy value and measured ROI remain unestablished.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q
        state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier]
        old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q
        folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact successor working reader'),
                  ref(BASE/'release-source-review.json','Reviewed mathematical/source/business delta')]
        write(folder/'reopen.json',{'reason':'Reader changed; preserve and renew the preceding exact-reader author review.',
            'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record the actual author review of the L5 preserving successor.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE)
        graph,_,_=run.combined(ROOT,state)
        node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+LIMITS))
        scope='Author exact-reader delta review; proposal evidence only'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],
            'reviewer':REVIEWER,'reviewed_reader':report['pdf'],'review_attempt':attempt,
            'acceptance_scope':'proposal_only','scope':scope,'findings':[finding],
            'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,
            limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,
            acceptance_scope='proposal_only',outputs=[ref(output,'Current-reader '+q+' author review')],
            nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt)
        transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','proposal_accepted':False}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['review','record-draft','publish','renew'])
    args=parser.parse_args()
    {'review':review,'record-draft':record_draft,'publish':publish,'renew':renew}[args.command]()
