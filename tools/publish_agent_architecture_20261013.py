#!/usr/bin/env python3
"""Bind the architecture synthesis to its reviewed preserving reader."""
import json
from pathlib import Path
import re
import build_agent_architecture_reader_20261013 as b
import master_control as core
import run_program as control

BASE,OUT,ROOT,ref=b.BASE,b.OUT,b.ROOT,b.ref

def main():
    assert not (BASE/'working-release.json').exists()
    state=core.read(ROOT,core.STATE)
    build=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(b.PRIOR_AUDIT.read_text())
    trace=json.loads((BASE/'traceability-review.json').read_text())
    bounds=json.loads((OUT/'text-layout-review.json').read_text())
    assert trace['status']==bounds['status']=='pass' and not trace['issues']
    assert trace['pdf']['sha256']==build['pdf']['sha256']
    assert state['reader']['sha256']==build['predecessor_pdf']['sha256']
    assert build['pages']==bounds['pages']==620
    assert not any(any(t in w.lower() for t in ['overfull','undefined','missing character']) for w in build['warnings'])
    assert b.DRIVER.read_text()==b.expected_driver()
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==455 and len(new)==457 and all(new[k]==v for k,v in old.items())
    for item in prior['tex_files']:core.bound(ROOT,item)
    b.shared.verify_refs(audit)
    text=(OUT/'reader.txt').read_text();flat=re.sub(r'\s+',' ',text)
    for term in ['48200','.05762','11.83','400-unit','.6415','same joint distribution']:
        assert term in flat,term
    pages=text.split('\f')
    first=next(i+1 for i,p in enumerate(pages) if 'A bank considering assisted causal analysis' in p)
    physical={'first':first,'last':first+7}
    artifacts=['plan-review.md','architecture.tex','exact-results.json','primary-review.json','mathematical-review.json','source-audit.json','refs.bib','prepared-inputs.json','traceability-review.json']
    evidence=[ref(BASE/p,p) for p in artifacts]
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'scope':'Connected architecture synthesis, formal/numerical baselines and exact-reader preservation',
        'prior_citation_records_unchanged':455,'new_project_records':2,'physical_pages':physical,
        'printed_pages':build['agent_architecture'],
        'findings':[
            'Servicing offer, uptake, population, horizon, information clock and costs are distinct; sequential decisions are not reduced to the point-treatment example.',
            'The true-nuisance score derivation, three target measures and financial sign reversal agree with exact finite calculations.',
            'Shared critic error and observational equivalence prevent consensus from being credited as new causal evidence.',
            'Six architecture families and selected package call paths are compared with favorable uses, adverse findings and scoped reuse decisions.',
            'ORCA discrepancy, notebook target mismatch, compilation versus statement fidelity and failed source searches remain explicit.',
            'Local offline replay, static review and future live/platform claims stay separate.',
            'All455 earlier citation records and source artifacts remain unchanged;457-record traceability and620-page bounds pass.'],
        'repairs':[{'failure':'Preparation expected extracted_text to be a path string; an inherited source used a hash-bound dictionary.','remedy':'Accept both preserved representations; retain original source records.','verification':'Preparation, compilation and whole-reader traceability pass.'}],
        'evidence':evidence+[ref(OUT/'build-report.json','Compiled successor'),ref(OUT/'text-layout-review.json','All-page text bounds')],
        'visual_acceptance':False,'independent_review':False,'live_calls':0}
    core.write(BASE/'release-source-review.json',review)
    release={'kind':'working_monograph','final_acceptance':False,'pdf':build['pdf'],'pages':build['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Compiled preserving architecture reader'),
        'source_review':ref(BASE/'release-source-review.json','Substantive author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page physical bounds'),
        'source_artifacts':audit['tex_files']+evidence+[ref(BASE/'release-source-review.json','Reviewed source and mathematical meaning')]+[ref(ROOT/'tools'/p,'Frozen exact-example/build/publication source') for p in ['agent_architecture_examples_20261013.py','build_agent_architecture_reader_20261013.py','publish_agent_architecture_20261013.py']],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Integrated eight pages on servicing architecture, target drift, correlated critics, information limits, typed recovery and full-request economics.'],
        'sponsor_binding':'Prior sponsor preserved; final exact-reader coherence remains Q5 work.'}
    core.write(BASE/'working-release.json',release)
    control.ledger.validate_working_release(ROOT,ref(BASE/'working-release.json','Reviewed architecture reader'))
    identifier='LL.TASK.agent_architecture'
    graph,_,_=control.combined(ROOT,state);node=next(n for n in graph['nodes'] if n['id']==identifier)
    path=ROOT/node['outputs'][0];assert not path.exists();path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text('''# Agent architecture synthesis

Author-reviewed proposal operation,13 October2026; literature cutoff7 October2026.

The integrated argument is in the620-page working monograph, printed pages353–360
(physical370–377). It develops the decision to offer early restructuring review:
eligible account, pretreatment information clock, offer versus uptake, fixed
recovery horizon and explicit incremental costs. The AIPW conditional-expectation
argument is conditional on consistency, exchangeability, positivity and the
sampling law; an agent does not certify these premises.

Six architecture families are compared: conversational tools, actor/critic
notebooks, a protected discovery core, relational shared state, formal proof
workflows and numerical mechanism-proposal loops. Named systems retain their
distinct source identities and reported evaluation limits. Selected CausalAgent,
oci-agent, LangGraph, Pydantic AI and AutoGen paths are reinspected. Reuse favors
typed intermediate artifacts and fixed verified operations; general notebook
execution, unchecked graph orientation and empty successful parse results are
not accepted as scientific handoffs.

The exact generated reference has population, trimmed and overlap effects of
125,700/3 and48200/283 USD. It shows why relabeling a changed population can
reverse a full-population decision. Three critics with marginal error.1 have
majority error.028 under independence and approximately.05762 under the
stipulated common-shock mixture. An equal-law Gaussian construction and
transcript-kernel induction show the limit of repeating the same information.
The economics reference includes failed-request costs and gives an11.83-minute
review break-even under explicitly authored prices and usable fractions.

The proposed remedy is a plain controller baseline with version-bound decision,
graph, target-measure and result objects; application-owned permissions; typed
refusal/unsupported/backend/malformed outcomes; and replay-aware durable request
identities. Compare template, single-assistant and critic arms with identical
tools, information and repair budgets. Freeze generated/public task provenance,
held-out splits, ambiguity rubric and full denominators before final studies.

No new live model or external framework was run. Existing six-case offline
replay supports only selected local semantics and recovery. Primary-source
search saturation,101 uninspected census candidates, live semantic quality,
target-platform behavior and bank truth remain open with their respective
acquisition/experiment triggers. These do not prevent the architecture proposal.

Evidence: docs/program/execution/2026-10-13/agent-architecture/ contains
primary-review.json, mathematical-review.json, exact-results.json,
release-source-review.json and working-release.json. The preceding455 citation
records remain unchanged;457-record traceability and620-page physical text
bounds pass. Visual acceptance and whole-proposal acceptance remain open.
''')
    receipt={'operation_id':identifier,'operation_contract_sha256':core.digest_object(node),
        'outcome':'pass','execution':'performed','scope':'Source-grounded architecture synthesis and exact authored baselines; proposal only',
        'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'limitations':['No live-model performance, new external framework execution, bank truth or target-platform acceptance.','Bounded corpus reinspection does not close all frontier omissions or MR02 depth/coverage.','Whole-reader visual review remains open under inherited image allowance.'],
        'original_gap_qualification':False,'capabilities':[],'outputs':[ref(path,'Architecture task synthesis')],
        'nonexecution_reason':'','revisit_trigger':'Relevant newly inspected original, package revision, or prospectively registered matched live/public experiment.',
        'criteria':[
            {'index':0,'verdict':'pass','finding':'Six research architectures and selected software paths compared, with conflicting results, reuse boundaries and preserved search omissions.','evidence':[ref(BASE/p,p) for p in ['primary-review.json','architecture.tex']]},
            {'index':1,'verdict':'pass','finding':'Servicing target/clock, causal assumptions, target drift, critic dependence, equal-law information limit and cost baselines are derived and exactly calculated.','evidence':[ref(BASE/p,p) for p in ['exact-results.json','mathematical-review.json','architecture.tex']]},
            {'index':2,'verdict':'pass','finding':'Paper findings, selected static paths, exact project examples and inherited local conformance are distinguished; no live/bank claim. Integrated preserving620-page reader checked.','evidence':[ref(BASE/p,p) for p in ['release-source-review.json','working-release.json']]}]}
    core.write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'pages':build['pages'],'citations':len(new),'physical_pages':physical,'outcome':'pass','receipt':str((BASE/'operation-receipt.json').relative_to(ROOT))}))

if __name__=='__main__':main()
