#!/usr/bin/env python3
"""Publish the reviewed CausalImpact reference decision and renew exact-reader reviews."""
import json
from pathlib import Path
import re

import build_causalimpact_reader_v2_20261013 as builder
import causalimpact_examples_20261013 as examples
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT = core.ROOT
BASE = builder.BASE
REVIEW = builder.REVIEW
OUT = builder.OUT
OLD = ROOT/'docs/program/execution/2026-10-13/commercial-iv-rd'
OP = 'SW.DECISION.inherited_causalimpact'


def main():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    assert state['reader']['path']=='docs/causal_proposal_commercial_iv_rd_2026-10-13.pdf'
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    prior_audit=json.loads((OLD/'reader/source-audit.json').read_text())
    prior_index=json.loads((OLD/'traceability-review.json').read_text())
    for obj in [report,audit,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((REVIEW/'manuscript-review.json').read_text()),
                json.loads((REVIEW/'decision-proposal.json').read_text()),
                json.loads((BASE/'preflight-repair.json').read_text())]:
        verify_bindings(obj)
    assert index['status']=='pass' and index['scholarly_pdfs']==148
    assert report['pages']==647 and report['cited_records']==487
    assert not any('Overfull' in w or 'undefined' in w.lower() for w in report['warnings'])
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert builder.DRIVER.read_text()==builder.expected_driver()
    assert builder.NEW_SOFTWARE.read_text().replace(builder.INSERT,'',1)==builder.OLD_SOFTWARE.read_text()
    previous={s['integrated_citation_key']:s for s in prior_audit['sources']}
    current={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(previous)==480 and all(current[k]==v for k,v in previous.items())
    added=sorted(set(current)-set(previous));assert len(added)==7
    replaced={str(builder.OLD.relative_to(ROOT)),str(builder.OLD_SOFTWARE.relative_to(ROOT))}
    unchanged=[x for x in prior_audit['tex_files'] if x['path'] not in replaced]
    for item in unchanged:core.bound(ROOT,item)
    old_contexts={x['citation_key']:x for x in prior_index['records']}
    contexts={x['citation_key']:x for x in index['records']}
    moved=[k for k in previous if contexts[k]['citation_contexts']!=old_contexts[k]['citation_contexts']]
    assert examples.serial(examples.calculate())==json.loads((REVIEW/'exact-results.json').read_text())
    extracted=re.sub(r'\s+',' ',(OUT/'reader.txt').read_text())
    for phrase in ['Bayesian intervention analysis for branch campaigns','same twelve observed rows',
                   'joint predictive law','R 4.1.2','does not denote the aGrUM','no integration capability']:
        assert phrase in extracted,phrase
    evidence=([ref(REVIEW/p,'Reviewed CausalImpact evidence') for p in
        ['source-audit.json','manuscript-review.json','decision-proposal.json','adapter-contract.json',
         'runtime-inventory.json','exact-results.json','omissions-register.json','acquisition-review.json']]+
        [ref(BASE/'traceability-review.json','Exact-reader citation identity/context audit'),
         ref(BASE/'preflight-repair.json','Preserved preflight failures, repairs and explicit diagnostic loss'),
         ref(ROOT/'tools/causalimpact_examples_20261013.py','Exact authored law and reporting calculations')])
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'scope':'Exact-reader source and scientific delta for CausalImpact reference disposition',
        'reviewed_reader':report['pdf'],'prior_review':state['execution_runtime']['results']['PROPOSAL.Q2'],
        'unchanged_prior_source_records':480,'unchanged_compiled_files':len(unchanged),
        'moved_context_keys':moved,
        'context_disposition':'The root driver and software wrapper are preserving successors. Exact text comparison permits only the new section input; all prior source records and scientific prose remain unchanged. File/line contexts move with this copy.',
        'added_records':[{'citation_key':k,'claims':current[k]['claims'],'inspected_anchors':contexts[k]['anchors'],
            'local_copies':contexts[k]['local_copies'],'contexts_reviewed':contexts[k]['citation_contexts']} for k in added],
        'evidence':evidence,
        'findings':['Pinned R and separate TFP source identities, dependency declarations and licenses are inspected; no interchangeable-alias or complete-build approval.',
            'Brodersen2015 authentic correctly named PDF supports the inherited state-space/joint-predictive/stock-flow argument.',
            'Exact identical-observation and dependent-draw examples reproduce; the forecast, costs and artificial draws are explicitly stipulated.',
            'Calendar compression, defaults, predictive noise, relative ratios and finite tail area are source findings, not native-run results.',
            'Reference selection grants no integration_allowed; R runtime mismatch and unresolved TFP/backend/dependency work have exact revisit triggers.'],
        'text_review':'New section printed200–205, physical217–222, inspected extracted prose and constructions; all647 physical-page text bounds pass.',
        'visual_acceptance':False,'independent_review':False,'native_engine_execution':False,
        'visual_limit':'Inherited six-image allowance exhausted; Q5 rendered acceptance remains open.'}
    write(BASE/'release-source-review.json',review)
    release={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','647-page preserving software-survey reader'),
        'source_review':ref(BASE/'release-source-review.json','Reviewed source/scientific delta'),
        'text_layout':ref(OUT/'text-layout-review.json','Whole-reader physical text bounds'),
        'source_artifacts':audit['tex_files']+evidence+[ref(OUT/'source-audit.json','487 audited citations'),
            ref(BASE/'release-source-review.json','Exact-release source review'),ref(Path(__file__),'Publication and review transitions')],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['CausalImpact comparison and reuse reference decision integrated in the panel/synthetic-control chapter.',
            'Control-invariance counterexample, pathwise uncertainty, ratio/units, calendar and failure semantics developed.',
            'R/TFP/aGrUM identities, dependency/runtime constraints, future adapter contract and omissions remain explicit.'],
        'sponsor_binding':'Earlier sponsor document preserved; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',release)
    binding=ref(BASE/'working-release.json','Reviewed CausalImpact working reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_causalimpact_reference_working_reader','manifest':binding,'final_acceptance':False})

    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    output=ROOT/node['outputs'][0]
    decision=json.loads((REVIEW/'decision-proposal.json').read_text())
    decision.update(release=binding,review=ref(BASE/'release-source-review.json','Reviewed integrated disposition'))
    write(output,decision)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope='Primary-source and exact-example reuse review; reference decision with no enabled adapter',
        reviewer=review['reviewer'],limitations=['No native R/TFP engine execution or qualified adapter.',
            'Complete compatible environment and transitive dependency/notice inventory remain future work.',
            'No causal-assumption verification, bank returns or independent acceptance.'],
        outputs=[ref(output,'Reviewed reference decision')],capabilities=[],nonexecution_reason='',
        revisit_trigger=decision['revisit_trigger'],criteria=[
            {'index':0,'verdict':'pass','finding':'Exact R pin, package/dependency license declarations, maintenance/test intent and distinct TFP/aGrUM identities are bound. Unresolved build closure is explicitly deferred rather than borrowed from Apache package terms.','evidence':[ref(REVIEW/'source-audit.json','Inspected primary source/version/license/anchor evidence'),ref(REVIEW/'omissions-register.json','Bounded omissions')]},
            {'index':1,'verdict':'pass','finding':'Target/uncertainty meanings, costs, owner duties, alternatives and revisit triggers are developed in the decision and six printed pages. Exact examples reproduce the limits.','evidence':[ref(REVIEW/'decision-proposal.json','Scoped decision'),ref(REVIEW/'exact-results.json','Executed arithmetic'),binding]},
            {'index':2,'verdict':'pass','finding':'Reference disposition grants no integration_allowed; a future isolated R adapter requires a compatible pinned build, matched native oracle and conversion/failure review. The proposed contract is explicit, not implemented behavior.','evidence':[ref(REVIEW/'adapter-contract.json','Proposed contract and future native oracle'),ref(REVIEW/'runtime-inventory.json','Observed incompatible local runtime')]}])
    write(BASE/'operation-receipt.json',receipt);transition('record',OP,BASE/'operation-receipt.json')

    findings={
        'Q2':'All480 preceding source records are preserved. Seven added records bind pinned primary software/dependency sources, one genuine scholarly PDF and explicitly labeled project review/constructions. Scientific claims and source boundaries were inspected;487 cited records and148 scholarly PDFs are bound to this exact reader.',
        'Q3':'Earlier demonstrated behavior is unchanged. The new twelve-row equal-observation construction and exact dependent-draw, ratio, units and cost calculations replay. No native CausalImpact/TFP execution, fitted performance or adapter was claimed; all prior negative study findings remain.',
        'Q4':'The prior investment case is preserved. Under stated USD1/application value and USD20 campaign cost, observationally identical mechanisms imply +60 or -60 net value. This motivates assessing controls or an experiment, not a bank ROI claim. Native environment, data/calendar, dependency and maintenance costs are identified but unmeasured.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q
        current_state=core.read(ROOT,core.STATE);prior=current_state['execution_runtime']['results'][identifier]
        previous_receipt=core.read(ROOT,prior['path']);folder=BASE/q;folder.mkdir(exist_ok=False)
        ev=[prior,binding,ref(BASE/'release-source-review.json','Exact-reader reviewed source/science delta'),
            ref(REVIEW/'exact-results.json','Exact authored law and reporting transformations'),
            ref(REVIEW/'decision-proposal.json','Reference disposition and unmeasured implementation costs')]
        write(folder/'reopen.json',{'reason':'New integrated CausalImpact reader requires review bound to the exact release.',
            'prior_result':prior,'reviewed_reader':report['pdf'],'evidence':ev,
            'next_action':'Record the inspected preserving delta with all previous and new scope limitations.'})
        transition('reopen',identifier,folder/'reopen.json')
        current_state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,current_state);node=run.ledger.operation(graph,identifier)
        attempt=len(current_state['execution_runtime']['review_history'][identifier])
        out=ROOT/run.review_output_paths(node,current_state['reader'],attempt)[0]
        limits=previous_receipt['limitations']+['CausalImpact is a reference decision: no compatible native run or enabled R/TFP adapter.',
            'No bank donor invariance, prices or ROI established; exact examples are stipulated.',
            'Q1 coverage/depth and Q5 rendered/sponsor acceptance remain open.']
        reviewed={'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':review['reviewer'],
            'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only',
            'scope':'Exact-reader author review of preserved material plus inspected CausalImpact delta',
            'findings':[finding],'evidence':ev,'limitations':limits,'visual_acceptance':False,'bank_ROI_established':False}
        write(out,reviewed)
        rec=run.ledger.receipt_template(node)
        rec.update(outcome='pass',execution='performed',scope=reviewed['scope'],reviewer=review['reviewer'],limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(out,'Current-reader '+q+' review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':ev}])
        write(folder/'operation-receipt.json',rec);transition('record',identifier,folder/'operation-receipt.json')
    status=run.status(ROOT,core.read(ROOT,core.STATE))
    print(json.dumps({k:status[k] for k in ['reader','next','recorded_proposal_operations','proposal_gaps']}),flush=True)


if __name__=='__main__':
    main()
