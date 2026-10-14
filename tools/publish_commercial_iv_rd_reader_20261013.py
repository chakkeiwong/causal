#!/usr/bin/env python3
"""Publish supported IV/RD evidence and retain unresolved commercial coverage."""
import json
from pathlib import Path
import re

import build_commercial_iv_rd_reader_20261013 as builder
import commercial_iv_rd_examples_20261013 as examples
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT = core.ROOT
BASE = builder.BASE
OUT = builder.OUT
OLD = ROOT/'docs/program/execution/2026-10-13/observations-journey'
OP = 'SW.CELL.iv_rd_design.commercial'


def main():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    assert state['reader']['path']=='docs/causal_proposal_observations_2026-10-13.pdf'
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    prior_audit=json.loads((OLD/'reader/source-audit.json').read_text())
    prior_index=json.loads((OLD/'traceability-review.json').read_text())
    for obj in [report,audit,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((BASE/'manuscript-review.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass' and index['scholarly_pdfs']==147
    assert report['pages']==642 and report['cited_records']==480
    assert not any('Overfull' in w or 'undefined' in w.lower() for w in report['warnings'])
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert builder.DRIVER.read_text()==builder.expected_driver()
    prior_sources={s['integrated_citation_key']:s for s in prior_audit['sources']}
    current_sources={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(prior_sources)==468
    assert all(current_sources[k]==s for k,s in prior_sources.items())
    previous_contexts={r['citation_key']:r for r in prior_index['records']}
    contexts={r['citation_key']:r for r in index['records']}
    for key,item in previous_contexts.items():
        assert contexts[key]['citation_contexts']==item['citation_contexts'],key
    unchanged=[r for r in prior_audit['tex_files'] if r['path']!=str(builder.OLD.relative_to(ROOT))]
    for item in unchanged:core.bound(ROOT,item)
    assert examples.calculate()==json.loads((BASE/'exact-results.json').read_text())
    extracted=re.sub(r'\s+',' ',(OUT/'reader.txt').read_text())
    for phrase in ['Commercial instruments and credit eligibility thresholds','7,344,273',
                   'identified single user','disconnected or unbounded answers',
                   'Whether the pilot argument warrants a larger experiment']:
        assert phrase in extracted,phrase
    added=sorted(set(current_sources)-set(prior_sources));assert len(added)==12
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'scope':'Exact-reader supported source, mathematical and investment delta; essential omissions remain coverage gaps',
        'reviewed_reader':report['pdf'],'prior_review':state['execution_runtime']['results']['PROPOSAL.Q2'],
        'unchanged_prior_source_records':468,'unchanged_prior_context_keys':468,'unchanged_compiled_files':len(unchanged),
        'added_records':[{'citation_key':key,'supported_claims':current_sources[key]['claims'],
            'contexts_reviewed':contexts[key]['citation_contexts'],'local_copies':contexts[key]['local_copies'],
            'inspected_anchors':contexts[key]['anchors']} for key in added],
        'evidence':[ref(BASE/p,'Inspected supporting evidence') for p in
            ['manuscript-review.json','source-audit.json','candidate-register.json','omissions-register.json',
             'acquisition-review.json','exact-results.json','traceability-review.json']]+
            [ref(ROOT/'docs/program/execution/2026-10-13/dependent-design/calculations.json','Deterministic feasibility and screen-power calculations'),
             ref(ROOT/'src/causalbank/operation_service_v12.py','Existing supplied-summary service boundary remains unchanged')],
        'findings':['Documented commercial capabilities are not executed integrations; Stata weak-IV topology is correctly credited.',
            'Grid limits, covariance meanings, source dates/editions, package license declarations and three unavailable originals remain explicit.',
            'The RD ratio target uses explicit common limiting population, exclusion, consistency and monotonicity premises.',
            'Exact constructed summary, instrument and discrete-support counterexamples agree with their stated scope.',
            'Dependent-pilot width/noise-floor and binomial calculations do not approve a final study or change old outcomes.'],
        'text_review':'New commercial section printed266–271 and learner feasibility section571–572; whole-reader physical text bounds pass.',
        'commercial_cell_complete':False,'visual_acceptance':False,'independent_review':False,
        'visual_limit':'Inherited image allowance exhausted; exact rendered acceptance remains open.'}
    write(BASE/'release-source-review.json',review)
    release={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving642-page reader'),
        'source_review':ref(BASE/'release-source-review.json','Reviewed source and semantic delta'),
        'text_layout':ref(OUT/'text-layout-review.json','Whole-reader text bounds'),
        'source_artifacts':audit['tex_files']+review['evidence']+
            [ref(BASE/'release-source-review.json','Exact-release review'),ref(OUT/'source-audit.json','480 cited records'),
             ref(Path(__file__),'Preserving publication and review continuation')],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Six commercial IV paths and two pinned RD packages compared with concrete proposed capabilities.',
                   'Three unavailable essential vendor sources remain explicit; full commercial cell remains inconclusive.',
                   'Exact banking examples and negative dependent-learning study feasibility integrated.'],
        'sponsor_binding':'Earlier sponsor document preserved; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',release)
    binding=ref(BASE/'working-release.json','Reviewed commercial IV/RD working monograph')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_commercial_iv_rd_working_reader','manifest':binding,'final_acceptance':False})
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    output=ROOT/node['outputs'][0]
    coverage={'cell':'iv_rd_design::commercial','status':'inconclusive_essential_sources_unavailable',
        'reviewer':review['reviewer'],'cutoff':'2026-10-07','commercial_families_inspected':6,
        'essential_candidates_unresolved':['MATLAB / ivx / iv4','OxMetrics / PcGive','LIMDEP / NLOGIT'],
        'findings':review['findings'],'release':binding,'evidence':review['evidence'],
        'native_execution':False,'whole_cell_qualified':False,
        'next_action':'Obtain edition-matched original manuals and license records for the three omitted families; inspect missing extensions in separate bounded package tasks. No unavailable-source waiver.'}
    write(output,coverage)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',scope='Bounded nine-family IV/RD commercial source comparison with three essential omissions',
        reviewer=review['reviewer'],limitations=['Three essential vendor technical sources remain unavailable.','Exact cutoff bytes and installed entitlements are not fully established.','No vendor runtime, matched performance or licensed integration claim.'],
        outputs=[ref(output,'Partial commercial source comparison and unresolved omissions')],nonexecution_reason='',
        revisit_trigger=coverage['next_action'],criteria=[
            {'index':0,'verdict':'pass','finding':'All nine named candidate families and aliases have bounded discovery/acquisition dispositions; metadata failure and cutoff limits are retained.','evidence':[ref(BASE/'candidate-register.json','Candidate universe and routes')]},
            {'index':1,'verdict':'inconclusive','finding':'Supported claims bind authentic inspected local bytes. Essential MATLAB, PcGive and LIMDEP originals remain unavailable, preventing full-cell closure.','evidence':[ref(BASE/'source-audit.json','Inspected local technical sources'),ref(BASE/'omissions-register.json','Essential sources unresolved')]},
            {'index':2,'verdict':'pass','finding':'Commercial alternatives, RD community packages, license limits and proposed adapters are compared without unsupported absence claims or source waivers.','evidence':[ref(BASE/'manuscript-review.json','Substantive comparison review'),binding]}])
    write(BASE/'operation-receipt.json',receipt)
    transition('record',OP,BASE/'operation-receipt.json')
    q_findings={
        'Q2':'All468 preceding source records and citation contexts are unchanged. Twelve added records have authentic inspected technical text or labeled project derivations/review. The exact reader retains147 scholarly PDFs and480 source records; inaccessible originals are omissions rather than unsupported capability claims.',
        'Q3':'Previously claimed demonstrations are preserved. Added IV/RD finite constructions and deterministic learner planning reproduce their explicit mathematics; no vendor/RD engine or new final learner study ran. The negative design and all prior high-dimension, nonlinear and weak-IV findings remain visible.',
        'Q4':'The prior investment argument is preserved. The new stipulated USD40 threshold example reverses the decision under different exclusion assumptions. Centered oracle planning and calibration noise floors explain why a large qualification campaign is premature; these are not ex ante trial power or recommended bank sample sizes. Actual licensed integration prices and returns remain unknown.'}
    for q,finding in q_findings.items():
        identifier='PROPOSAL.'+q
        current=core.read(ROOT,core.STATE);prior=current['execution_runtime']['results'][identifier]
        old_receipt=core.read(ROOT,prior['path']);folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[prior,binding,ref(BASE/'release-source-review.json',finding),ref(BASE/'exact-results.json','Exact authored examples'),
                  ref(ROOT/'docs/program/execution/2026-10-13/dependent-design/calculations.json','Deterministic feasibility and exact-binomial screen')]
        write(folder/'reopen.json',{'reason':'New commercial IV/RD reader requires exact-release author review.',
            'prior_result':prior,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record the reviewed preserving delta and retain all previous scope limits.'})
        transition('reopen',identifier,folder/'reopen.json')
        current=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,current);node=run.ledger.operation(graph,identifier)
        attempt=len(current['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,current['reader'],attempt)[0]
        limits=old_receipt['limitations']+['Three essential IV/RD commercial originals remain unavailable; coverage is inconclusive.',
            'Vendor runtime, package integration, final learner qualification and actual bank economics remain unclaimed.',
            'Q1 coverage/depth and Q5 rendered/sponsor acceptance remain open.']
        reviewed={'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':review['reviewer'],
            'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only',
            'scope':'Exact current-reader author review through preserving source and claim delta',
            'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False,'bank_ROI_established':False}
        write(output,reviewed)
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=reviewed['scope'],reviewer=review['reviewer'],limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Current-reader '+q+' review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt)
        transition('record',identifier,folder/'operation-receipt.json')
    summary=run.status(ROOT,core.read(ROOT,core.STATE))
    print(json.dumps({k:summary[k] for k in ['reader','next','recorded_proposal_operations','proposal_gaps']}),flush=True)


if __name__=='__main__':
    main()
