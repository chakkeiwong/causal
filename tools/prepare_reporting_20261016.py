#!/usr/bin/env python3
"""Review reporting proposal and bind its primary and exact evidence."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import review_reporting_sources_20261016 as work
import reporting_reference_20261016 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = work.ROOT, work.BASE
FINDINGS = [
    'Nine primary papers, two inherited pinned packages and current local report paths separate evidence auditing, interpretation, workflow repair, triage and causal monitoring. Seven pending task candidates were reassessed: four originals inspected and three specific retrieval gaps retained.',
    'Thirty-day servicing value, population, policy, clocks and identification premises connect to five exact authored reference families covering finite sets, denominators, selection, repeated testing and dependency invalidation.',
    'Reported literature findings, static source observations, executed exact arithmetic and proposed public/generated comparisons remain distinct. No live-model performance, implemented scientific monitor or bank truth is claimed.'
]


def main():
    primary = work.read(BASE/'source-review.json'); verify_bindings(primary)
    omissions = work.read(BASE/'omissions-register.json'); verify_bindings(omissions)
    results = work.read(BASE/'exact-results.json'); assert results == examples.calculate()
    # Independent closed forms, literal case counts and hand-specified reachability.
    assert results['set_reporting']['net_usd'] == [-40, 60]
    assert not results['set_reporting']['midpoint_in_set']
    assert F(results['denominators']['conditional_accuracy']) == F(4,5)
    assert F(results['denominators']['all_request_computed_correct']) == F(12,25)
    assert F(results['selection']['marginal_coverage']) == F(19,20)
    assert F(results['selection']['coverage_given_acceptance']) == F(1,2)
    assert abs(results['repeated_looks']['independent_any_alarm_decimal'] - (1 - .95**12)) < 1e-14
    assert F(results['repeated_looks']['spending_sum']) == F(3,65)
    assert results['dependency_invalidation']['affected'] == {
        'clock':['design','economics','estimate','report'],
        'assignment':['design','economics','estimate','report'],
        'price':['economics','report'], 'other_cohort':['other_estimate']}
    write(BASE/'arithmetic-review.json', {'status':'pass','reviewer':work.REVIEWER,
        'scope':'Closed-form comparison, finite counts and hand-specified dependency closure',
        'independence':'Alternative mathematical checks by the same author; not external independent review',
        'evidence':[ref(BASE/'exact-results.json','Five executed authored reference families'),
                    ref(ROOT/'tools/reporting_reference_20261016.py','Exact finite law and binomial enumeration'),
                    ref(Path(__file__),'Alternative closed forms and expected closures')],
        'claim_limits':['No confidence law on finite set', 'Selection is a stipulated joint law',
                        'Product false-alarm formula assumes independence', 'Spending requires valid per-look tests',
                        'Dependency graph is a proposed review oracle, not an implemented service']})
    contract = {
        'status':'proposed_not_implemented','integration_allowed':False,
        'scientific_object':['Population and eligibility','Frozen policy/comparator and treatment versions',
            'Event, availability, decision and outcome clocks','Graph/class and identification assumptions',
            'Estimate, finite set, interval or refusal with original type and units',
            'Sampling, identification, numerical and selection uncertainty distinguished'],
        'evidence_object':['Data/code/environment/source hashes','Claim-to-field or claim-to-passage links',
            'Supportive, adverse, missing-retrieval, conflicting and externally unknown dispositions',
            'Diagnostics, reviewer role and unresolved obligations'],
        'decision_object':['Cash contrast and separate price conversion','Declared loss criterion',
            'Alternatives, useful precision and costs','No automatic bank-action authority'],
        'proposed_interfaces':{
            'report_request':'Immutable result references, audience, template revision, presentation budget',
            'report_response':'Narrative, deterministic rendering, verified links, unresolved statements',
            'change_review':'Versioned event, effect/observation clocks, affected fields, dependency closure, reasons and owner',
            'same_semantics':'Library, CLI and MCP preserve identical scientific result identities and dispositions'},
        'applicability_states':['current','review_required','superseded','unknown'],
        'immutability':'Keep historical artifacts; separate applicability records, each supersession linked and reasoned.',
        'monitor_contract':['Null/target and population','Independent or dependent observation unit',
            'Valid error allocation across times and monitor families','Adaptive selection and restart rules',
            'Delay, detectable change, support and useful width','Scientific/data/operator owner and escalation route'],
        'package_choices':[
            {'package':'oci-agent','choice':'adapt artifact ideas; execution deferred',
             'reason':'Pinned runner serializes per-estimand results but permits notebooks with timeout disabled; actual target and resource contract need separate checks.'},
            {'package':'CausalAgent','choice':'reference parser failure; reject empty-success conversion',
             'reason':'Static parsing failure returns empty dict; typed error and original response must survive conversion.'},
            {'package':'FlowFixer','choice':'methodological reference; integration deferred',
             'reason':'Workflow assertions and dynamic repair do not establish bank identification; full package, rights and independent semantic cases still needed.'},
            {'package':'PSEBench','choice':'adapt case-card idea; benchmark transfer unqualified',
             'reason':'Medical policy truth, synthetic narrative and idealized retrieval do not supply banking causal truth.'},
            {'package':'CausalPulse','choice':'reference separate operation and diagnosis metrics',
             'reason':'Manufacturing completion and causal attribution have different denominators; package path still unreviewed.'}],
        'public_generated_prototype':{
            'status':'design_only; exact reference examples executed separately',
            'baseline':'Deterministic rendering of frozen source/result cards',
            'comparators':['Constrained language renderer','Optional evidence retrieval assistant'],
            'cases':['Finite nonprobabilistic set','Wrong unit','Selected confidence interval',
                'Conflicting passage','Missing passage','Late feature','Changed price',
                'Unchanged observed law with causal ambiguity','Malformed model output','Stale dependency','Correct refusal'],
            'truth':'Explicit authored facts/statuses, source passages and independently reviewed semantic labels',
            'split':'Hold related variants together; preserve fresh held-out cases after tuning',
            'predeclare':['Generator/source versions','Case truth and scoring','Budgets, prompts and model revision',
                'Units, numerical tolerances, disposition accuracy','Adjudication and stopping rules'],
            'finite_gate':'Every required number/unit/type/mandatory limitation survives the selected exact cases; no population-general guarantee.',
            'metrics':['All-request and conditional accuracy','Correct/incorrect abstention',
                'Invented numerical confidence','Lost ambiguity','Unsupported citation','Cost','Latency'],
            'costs':['Generation','Retrieval','Review/adjudication','Failures/retries','Storage','Maintenance'],
            'live_model_execution':'Not performed or required to finish this proposal synthesis',
            'bank_followup':'Only after a permitted prototype demonstrates sufficient merit for expensive authentic data/owner studies'},
        'remaining_research':['Selective inference for the actual critic-estimator joint law',
            'Sequential validity under adaptive and dependent monitoring','Detectability limits under causal nonidentification',
            'Evidence sufficiency and source changes','Semantic correctness and useful precision under new populations'],
        'evidence':[ref(BASE/'source-review.json','Nine primary papers and static implementation review'),
                    ref(BASE/'exact-results.json','Five exact authored families'),
                    ref(BASE/'omissions-register.json','Concrete remaining source/implementation gaps')],
        'limitations':work.LIMITS}
    write(BASE/'proposed-contract.json',contract)
    new = copy.deepcopy(work.read(BASE/'new-paper-audit.json')['sources'])
    pse = next(s for s in new if s['integrated_citation_key']=='exec16_report_psebench')
    extra_claim = 'Physical page5: joint expert review90 generated cases;28/30,29/30,30/30 agreement; idealized information oracle and metric definitions.'
    pse['inspected_anchors'].append({'anchor':'Physical PDF page5','finding':extra_claim,
        'extracted_text':ref(BASE/'psebench-v2-page-5.txt','Inspected expert review and oracle/metric definitions')})
    pse['supported_claims'].append(extra_claim)
    def source(key,title,kind,path,claims,records):
        return {'integrated_citation_key':key,'title':title,'author':'Causal banking proposal',
            'kind':kind,'year':2026,'source_identity':'Project-authored proposal evidence with bound originals',
            'version_date':'2026-10-16; inherited upstream revisions retained in source review',
            'local_copy':ref(path,title),'inspected_anchors':claims,'supported_claims':claims,
            'records':records,'limitations':work.LIMITS}
    new += [
        source('exec16_report_sources','Reporting and monitoring primary rereads and pinned implementation review',
            'project_source_review',BASE/'source-review.json',FINDINGS[:1],
            primary['records']+[{'local_copy':ref(BASE/'candidate-reassessment.json','Seven source-specific candidate dispositions')}]),
        source('exec16_report_oracle','Exact reporting, selection, alarm and applicability examples',
            'project_derivation',BASE/'exact-results.json',
            ['Finite set, request denominators and selected coverage','Repeated-alarm calculation and telescoping error budget','Selective dependency invalidation with immutable history'],
            [{'local_copy':ref(BASE/'arithmetic-review.json','Alternative mathematical checks')},
             {'local_copy':ref(ROOT/'tools/reporting_reference_20261016.py','Reproducible exact calculations')}]),
        source('exec16_report_contract','Proposed causal report and monitoring contract with public evidence comparison',
            'project_design',BASE/'proposed-contract.json',
            ['Typed result preservation, claim links, version applicability and explicit monitoring ownership',
             'Public/generated comparison, cost and unresolved research; no integration permission'],
            [{'local_copy':ref(BASE/'omissions-register.json','Three unresolved candidates and broader evidence limits')}])]
    write(BASE/'source-audit.json',{'sources':new,'prior':ref(work.PRIOR,'670 inherited records'),
          'cutoff':'2026-10-07','paper_count_added':4,'record_count_added':7})
    work.OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    assert not work.OUTPUT.exists()
    subprocess.run(['pandoc','--from=latex','--to=markdown','--wrap=auto',
                    str(BASE/'development.tex'),'-o',str(work.OUTPUT)],check=True)
    write(BASE/'authoring-recovery.json',{
        'observed_error':'TypeError: String.raw(...) is not a function',
        'stage':'Initial manuscript apply_patch invocation',
        'cause':'LaTeX opening double-backtick quote ended JavaScript raw template.',
        'effect':'No mutation occurred in the failed call.',
        'repair':'Removed the quote syntax and applied manuscript successfully.',
        'scope':'No original evidence changed.'})
    evidence=[ref(BASE/n,n) for n in ['plan.md','source-review.json','candidate-reassessment.json',
        'omissions-register.json','exact-results.json','arithmetic-review.json','proposed-contract.json',
        'source-audit.json','development.tex','authoring-recovery.json']]
    evidence += [ref(work.OUTPUT,'Connected task synthesis'),ref(Path(__file__),'Criterion and mathematical review')]
    for row in evidence: verify_bindings(row)
    write(BASE/'author-review.json',{'status':'pass','reviewer':work.REVIEWER,
        'scope':'Bounded proposal synthesis; no census, capability, independent or rendered acceptance',
        'findings':FINDINGS,'evidence':evidence,'limitations':work.LIMITS,
        'integration_allowed':False,'visual_acceptance':False,
        'plan_review':['Missing and ambiguous outcomes require separate truth labels.',
            'Faithful reporting cannot establish causal validity.',
            'Bank experiments deferred until prototype merit warrants the cost.',
            'Source failures affect their branches; independent proposal work continues.'],
        'depth_credit':'No automatic chapter-depth or mandatory-repair closure; integrated arguments reviewed separately.'})
    print(json.dumps({'new_citations':len(new),'new_papers':4,'synthesis':str(work.OUTPUT.relative_to(ROOT)),'author_review':'pass'}))


if __name__ == '__main__': main()
