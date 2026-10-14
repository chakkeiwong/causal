#!/usr/bin/env python3
"""Publish data/code scholarship and renew exact-reader proposal reviews."""
import json
from pathlib import Path
import re

import build_data_code_reader_20261013 as builder
import data_code_exact_20261013 as exact
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT=core.ROOT;BASE=builder.BASE;REVIEW=builder.REVIEW;OUT=builder.OUT
OLD=ROOT/'docs/program/execution/2026-10-13/causalimpact-reuse/final'
OP='LL.TASK.data_code'

def main():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    assert state['reader']['path']=='docs/causal_proposal_causalimpact_2026-10-13.pdf'
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    index=json.loads((BASE/'traceability-review.json').read_text());prior_audit=json.loads((OLD/'reader/source-audit.json').read_text())
    prior_index=json.loads((OLD/'traceability-review.json').read_text())
    for obj in [report,audit,index,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((REVIEW/'review-v2.json').read_text()),json.loads((REVIEW/'source-audit-v2.json').read_text())]:
        verify_bindings(obj)
    assert index['status']=='pass' and index['scholarly_pdfs']==153
    assert report['pages']==650 and report['cited_records']==497
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not any('Overfull' in w or 'undefined' in w.lower() for w in report['warnings'])
    assert builder.DRIVER.read_text()==builder.expected_driver()
    previous={s['integrated_citation_key']:s for s in prior_audit['sources']}
    current={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(previous)==487 and all(current[k]==v for k,v in previous.items())
    added=sorted(set(current)-set(previous));assert len(added)==10
    unchanged=[x for x in prior_audit['tex_files'] if x['path']!=str(builder.OLD.relative_to(ROOT))]
    for x in unchanged:core.bound(ROOT,x)
    old_contexts={x['citation_key']:x for x in prior_index['records']}
    contexts={x['citation_key']:x for x in index['records']}
    assert all(contexts[k]['citation_contexts']==old_contexts[k]['citation_contexts'] for k in previous)
    result=exact.calculate();assert result==json.loads((REVIEW/'exact-results.json').read_text())
    extracted=re.sub(r'\s+',' ',(OUT/'reader.txt').read_text())
    for phrase in ['Data and code agents: a fail-closed banking boundary','An exact target-drift oracle','CausalDS','date 11','local conformance checks']:
        assert phrase.lower() in extracted.lower(),phrase
    evidence=[ref(REVIEW/p,'Reviewed data/code source, synthesis or oracle') for p in
        ['task-synthesis.md','source-audit-v2.json','review-v2.json','findings.json','chapter.tex','exact-results.json','plan-review.json'] if (REVIEW/p).exists()]
    evidence.append(ref(ROOT/'docs/program/comprehensive-v14/work/LL.TASK.data_code/task-synthesis.md','Operation synthesis'))
    evidence.extend([ref(BASE/'traceability-review.json','Exact reader citation audit'),
                     ref(ROOT/'docs/program/repair-v12/work/LA05/review.md','Prior executed bounded-controller review'),
                     ref(ROOT/'tools/data_code_exact_20261013.py','Exact target and clock calculator')])
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'scope':'Exact-reader source/claim and mathematical delta for data/code agent scholarship',
        'reviewed_reader':report['pdf'],'prior_review':state['execution_runtime']['results']['PROPOSAL.Q2'],
        'unchanged_prior_source_records':487,'unchanged_prior_citation_context_keys':487,'unchanged_compiled_files':len(unchanged),
        'added_records':[{'citation_key':k,'claims':current[k]['claims'],'anchors':contexts[k]['anchors'],
            'local_copies':contexts[k]['local_copies'],'contexts':contexts[k]['citation_contexts']} for k in added],
        'evidence':evidence,
        'findings':['Five authentic newly cited PDF originals have correct local titles/names and inspected technical anchors; paper results remain source-reported.',
            'Four pinned package paths are statically inspected with code/ontology/benchmark failure modes and explicit limits.',
            'Exact two-stratum target arithmetic and availability-clock refusal replay from independent local arithmetic.',
            'LA05 eighty-case local controller result is credited as conformance only, with zero live model calls and no bank truth.',
            'All inherited text/source records and citation contexts are unchanged except root driver insertion; Q1/Q5 remain open.'],
        'text_review':'New LLM section begins printed379; all650 physical pages pass text/bounds inspection.',
        'visual_acceptance':False,'independent_review':False,'live_model_calls':0,'bank_truth':False,
        'visual_limit':'Inherited six-image allowance exhausted; exact rendered Q5 acceptance remains open.'}
    write(BASE/'release-source-review.json',review)
    release={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','650-page preserving reader'),
        'source_review':ref(BASE/'release-source-review.json','Reviewed scientific/source delta'),
        'text_layout':ref(OUT/'text-layout-review.json','Whole-reader text bounds'),
        'source_artifacts':audit['tex_files']+evidence+[ref(BASE/'release-source-review.json','Exact-release review'),
            ref(OUT/'source-audit.json','497 cited records'),ref(Path(__file__),'Publication and review transitions')],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Integrated data/code agent review into the LLM workflow portion of the monograph.',
            'Compared five primary papers and four pinned packages, including adverse package paths and specific remedies.',
            'Added worked banking target/clock and exact overlap-weight baseline without live-model or bank claims.'],
        'sponsor_binding':'Earlier sponsor document preserved; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',release)
    binding=ref(BASE/'working-release.json','Reviewed data/code working reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_data_code_working_reader','manifest':binding,'final_acceptance':False})
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    output=ROOT/node['outputs'][0];assert output.exists()
    rec=run.ledger.receipt_template(node)
    rec.update(outcome='pass',execution='performed',scope='Primary-source data/code agent synthesis with exact banking target/clock oracle and proposed fixed-operation remedies',
        reviewer=review['reviewer'],limitations=['Source-reported agent evaluations were not reproduced with a live backend.',
            'External packages were inspected but not installed/executed; dependency/license closure remains scoped.',
            'No bank ownership, assignment, prices or independent judgments established.'],
        outputs=[ref(output,'Developed operation synthesis'),binding],nonexecution_reason='',revisit_trigger='',
        criteria=[
            {'index':0,'verdict':'pass','finding':'Five inspected frontier PDFs and four pinned package paths are compared, including adverse behavior, conditional reuse and benchmark/scorer repairs. Existing search coverage limits and code-paper differences are retained.','evidence':[ref(REVIEW/'source-audit-v2.json','Authentic primary sources'),ref(REVIEW/'review-v2.json','Author source review'),ref(output,'Developed synthesis')]},
            {'index':1,'verdict':'pass','finding':'A servicing offer question specifies unit, action, target, horizon and availability clock. The two-stratum 5 versus250/41 weighting oracle and late-available-field refusal reproduce exactly; a structured human workflow is the baseline.','evidence':[ref(REVIEW/'exact-results.json','Exact authored arithmetic/clock fixture'),ref(REVIEW/'chapter.tex','Connected banking argument')]},
            {'index':2,'verdict':'pass','finding':'The chapter labels LA05 local conformance separately from live agent accuracy or bank truth; all package observations are static, and zero live model calls were made.','evidence':[ref(ROOT/'docs/program/repair-v12/work/LA05/verification.json','80 local checks and zero live calls'),ref(BASE/'release-source-review.json','Exact reader limitation review')]}])
    write(BASE/'operation-receipt.json',rec);transition('record',OP,BASE/'operation-receipt.json')
    findings={
        'Q2':'All487 prior source records and citation contexts are unchanged. Ten new cited records include five authentic inspected scholarly PDFs, four pinned software sources and one local controller evidence source. The exact650-page reader has497 cited records and153 scholarly PDFs; source scope and unresolved package claims remain explicit.',
        'Q3':'Earlier portfolio results are preserved. The added 5 versus250/41 target and availability-clock arithmetic replay, while LA05 eighty-case conformance remains local/offline with zero live model calls. No external package run or bank effect is claimed.',
        'Q4':'The prior investment argument is preserved. Data/code agent tasks add cost/risk categories for reviewer effort, source custody, ontology pinning, bounded execution and benchmark construction; no incremental live-model price, bank ROI or claimed measured benefit is inferred from source reports.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q
        current_state=core.read(ROOT,core.STATE);prior=current_state['execution_runtime']['results'][identifier]
        previous_receipt=core.read(ROOT,prior['path']);folder=BASE/q;folder.mkdir(exist_ok=False)
        ev=[prior,binding,ref(BASE/'release-source-review.json','Reviewed exact-reader delta'),
            ref(REVIEW/'exact-results.json','Exact target/clock fixture'),ref(output,'Developed data/code synthesis')]
        write(folder/'reopen.json',{'reason':'New integrated data/code reader requires exact-release author review.',
            'prior_result':prior,'reviewed_reader':report['pdf'],'evidence':ev,
            'next_action':'Record the reviewed preserving delta with all inherited and new scope limits.'})
        transition('reopen',identifier,folder/'reopen.json')
        current_state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,current_state);node=run.ledger.operation(graph,identifier)
        attempt=len(current_state['execution_runtime']['review_history'][identifier]);out=ROOT/run.review_output_paths(node,current_state['reader'],attempt)[0]
        limits=previous_receipt['limitations']+['No live data/code agent performance, external package execution or bank truth.',
            'Q1 coverage/depth and Q5 rendered/sponsor acceptance remain open.']
        reviewed={'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':review['reviewer'],
            'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only',
            'scope':'Exact-reader author review of preserved material plus data/code synthesis',
            'findings':[finding],'evidence':ev,'limitations':limits,'visual_acceptance':False,'bank_ROI_established':False}
        write(out,reviewed)
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=reviewed['scope'],reviewer=review['reviewer'],limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(out,'Current-reader '+q+' review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':ev}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    status=run.status(ROOT,core.read(ROOT,core.STATE))
    print(json.dumps({k:status[k] for k in ['reader','next','recorded_proposal_operations','proposal_gaps']}),flush=True)

if __name__=='__main__':main()
