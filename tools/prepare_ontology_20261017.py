#!/usr/bin/env python3
"""Review ontology synthesis, exact laws and the proposed extraction contract."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import review_ontology_sources_20261017 as work
import ontology_reference_v2_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT,BASE=work.ROOT,work.BASE
FINDINGS=[
    'Ten primary papers, five additional pinned code originals, inherited loader review and current local declaration paths distinguish variable meaning, formal ontology and causal identification. All eight pending candidates have dispositions; six originals acquired, two routes unresolved.',
    'The thirty-day support-offer target connects measured/latent variables, original observation links, aggregation, units and clocks to six exact authored families and a typed public/generated comparison.',
    'Published model findings, static implementation observations, executed exact arithmetic and proposed capability remain distinct; no live-model, upstream-runtime, causal-truth or bank validation claim.'
]


def main():
    primary=work.read(BASE/'source-review.json');verify_bindings(primary)
    omissions=work.read(BASE/'omissions-register.json');verify_bindings(omissions)
    results=work.read(BASE/'exact-results-v2.json');assert results==examples.calculate()
    # Independent 100-person-per-arm counts, separate from the generating algebra.
    literal_counts=[[16,4,4,76],[18,2,12,68]]
    for a,(tp,fn,fp,tn) in enumerate(literal_counts):
        r=results['differential_measurement']
        assert sum([tp,fn,fp,tn])==100
        assert F(r['measured_risks'][a])==F(tp+fp,100)
        assert F(r['accuracies'][a])==F(tp+tn,100)
        assert F(r['true_risks'][a])==F(tp+fn,100)
    assert F(r['pooled_accuracy_equal_arms'])==F(178,200)
    assert r['spurious_usd_per_account']==100
    assert r['known_law_corrected_risks']==['1/5','1/5']
    assert results['aggregation']['household_uniform_usd']=='0'
    assert results['aggregation']['account_weighted_household_usd']=='8'
    assert results['units']['matched_period_ratio']==results['units']['converted_period_ratio']=='1/2'
    assert F(results['units']['unconverted_period_ratio'])*12==F(1,2)
    assert not results['availability']['available_by_decision']
    assert not results['availability']['derived_declaration_valid']
    assert F(results['selective_notes']['observed_treated_risk'])==F(20,40)
    assert F(results['selective_notes']['selected_contrast'])==F(30,100)
    assert F(results['metric_identity']['jaccard'])==F(9,11)>F(4,5)
    assert not results['metric_identity']['exact_document_match']
    write(BASE/'arithmetic-review.json',{'status':'pass','reviewer':work.REVIEWER,
        'scope':'Literal contingency counts, weighted targets, period conversion, clock ordering and finite token sets',
        'independence':'Alternative mathematical checks by the author, not external independent review',
        'evidence':[ref(BASE/'exact-results-v2.json','Six exact authored families'),
                    ref(ROOT/'tools/ontology_reference_20261017.py','Original algebra'),
                    ref(ROOT/'tools/ontology_reference_v2_20261017.py','Clarified field name'),
                    ref(Path(__file__),'Independent literal-count and semantic checks')],
        'claim_limits':['Measurement and selection rates stipulated, not inferred.',
                        'No finite-sample performance, upstream execution or true bank measurement asserted.']})
    contract={
        'status':'proposed_not_implemented','integration_allowed':False,
        'target':'Thirty-day missed-payment ATE for an explicitly eligible and weighted population; coded-note effect is distinct.',
        'observation_fields':['original record hash and exact document/span identity','entity and grouping identities',
            'construct and operational definition','measured/derived/latent type','value domain, unit and period',
            'event, availability and decision clocks','missingness status and observation indicator',
            'transformation parents and revision','extractor/model/prompt/vocabulary identity','source and review status'],
        'relations':['taxonomy','synonym or equivalence','ownership/entity linkage','data lineage',
            'observed association','candidate directed causal relation'],
        'states':['supported_observation','derived_measurement','proposed_mapping','contradicted',
            'unresolved','missing','not_applicable','not_collected','redacted','delayed','model_imputed'],
        'required_preservation':['Original evidence immutable','Recoding creates a new derived variable',
            'Different constructs not merged by renaming','Latent construct not upgraded to observed value',
            'No relation direction or endpoint loss','Exact source identity checked before lexical similarity',
            'Historical values use actual availability; derived availability no earlier than all inputs',
            'Target unit, assignment unit, grouping and weights retained',
            'CLI, MCP and library carry identical typed meanings and refusal states'],
        'package_choices':[
            {'name':'OntoLearner','choice':'reference and prospective adapted benchmark component',
             'reason':'MIT code with inspected document linkage and task interfaces; existing metrics do not establish causal semantics.',
             'reject':'Direct use of concatenated-document Jaccard as a causal observation acceptance gate.',
             'before_runtime':['Complete dependency/data/model rights','Dataset/model revision pins',
                'Fail or mark incomplete required import/split omissions','Inspect concrete learner paths',
                'Run separate identity/unit/clock/direction and original-metric checks']},
            {'name':'OntoBioStat','choice':'formal design reference',
             'reason':'Context, recoding and uncertain relations are useful; supplied relations and general causal correctness still need validation.',
             'before_runtime':['Original code/license/distribution and reasoner premises','Compare returned adjustment suggestions with justified graph-specific procedure']},
            {'name':'OntoURL','choice':'candidate public benchmark, not causal-effect gold',
             'reason':'Separate recognition, reasoning and generation; inconsistent L1 scales and unequal evaluation sets unresolved.',
             'before_runtime':['Pinned code/data/license review','Resolve raw score scale and denominators','Preserve adverse outputs and task-specific scores']},
            {'name':'text_treat','choice':'public-treatment/code lead only',
             'reason':'Sociology article gives code/data links; GIP respondent text is onsite-only.',
             'before_runtime':['Inspect actual source and data terms','Verify unit/assignment and target','Do not substitute synthetic respondents for observed participants']}],
        'public_generated_comparison':{
            'status':'design_only; six separate exact mathematical families already executed',
            'baselines':['Deterministic dictionary/schema','Ontology-assisted typed mapping','Later permitted constrained language-model extraction'],
            'families':['Differential label error and equivalent observed laws','Household/account aggregation',
                'Units and incompatible constructs','Historical and derived clocks','Selective notes and retained missingness',
                'Exact document links and relation direction','Negation/conflicting evidence','Malformed/absent evidence and justified refusal'],
            'truth':'Generated mechanisms and original passages, with unresolved causal alternatives kept as sets; later independent meaning adjudication if needed.',
            'split':'Group entity/document families and paraphrases; freeze extractor before effect evaluation; retain fresh held-out cases after development.',
            'predeclare':['Case generator, source and data revisions','Labels, semantic scoring and tolerances','Model/prompt/tool versions and rights',
                'Call/retry/context/latency budget','All-request denominator','Stopping and adjudication rules'],
            'metrics':['Exact identity, unit, clock and typed relation preservation','Correct acceptance/refusal/unresolved output',
                'Conditional and all-request performance','Measurement error by arm/time/source','Downstream target distortion','Full cost'],
            'finite_gate':'All stipulated mandatory semantic cases correct; no population-wide guarantee or integration permission.',
            'costs':['Retrieval','Extraction','Human review','Correction/adjudication','Failures/retries','Maintenance'],
            'bank_stage':'Only after a permitted prototype demonstrates merit; obtain representative validation, actual ownership and prices.'},
        'remaining_research':['Unknown arm-specific measurement law','Nonignorable selection','Construct validity and causal sufficiency',
            'Availability/entity truth in real records','Generalization and contamination','Uncertainty from learned measurement'],
        'evidence':[ref(BASE/'source-review.json','Primary literature and static implementations'),
                    ref(BASE/'exact-results-v2.json','Six exact reference families'),
                    ref(BASE/'omissions-register.json','Source/version/rights and scientific gaps')],
        'limitations':work.LIMITS}
    write(BASE/'proposed-contract.json',contract)
    sources=copy.deepcopy(work.read(BASE/'new-paper-audit.json')['sources'])
    ontourl=next(s for s in sources if s['integrated_citation_key']=='exec17_ontology_ontourl')
    for page,finding in [(6,'Table1 maps tasks: U1/U2 class definitions/relations, R4/R5 rule and description logic, L2-L4 Triple-F1 and L5 Tuple-F1.'),
                         (7,'Accuracy for choice tasks, BERTScore for L1 and F1 for structures; regex extracts valid triples/tuples.')]:
        ontourl['inspected_anchors'].append({'anchor':f'Physical PDF page {page}','finding':finding,
            'extracted_text':ref(BASE/f'ontourl-v3-page-{page}.txt','Inspected task and metric definition')})
        ontourl['supported_claims'].append(finding)
    def source(key,title,path,kind,claims,records):
        return {'integrated_citation_key':key,'title':title,'author':'Causal banking proposal','kind':kind,'year':2026,
            'source_identity':'Project-authored evidence with bound primary originals','version_date':'2026-10-17; inspected upstream revisions retained',
            'local_copy':ref(path,title),'inspected_anchors':claims,'supported_claims':claims,'records':records,'limitations':work.LIMITS}
    sources += [
        source('exec17_ontology_sources','Variable meaning primary literature and pinned implementation review',
            BASE/'source-review.json','project_source_review',FINDINGS[:1],primary['records']),
        source('exec17_ontology_oracle','Exact measurement, aggregation, unit, clock, selection and document-link examples',
            BASE/'exact-results-v2.json','project_derivation',
            ['Six exact authored semantic families; no upstream execution','Same observed label law can have different true effects'],
            [{'local_copy':ref(BASE/'arithmetic-review.json','Alternative literal-count checks')}]),
        source('exec17_ontology_contract','Proposed typed observation and ontology comparison contract',
            BASE/'proposed-contract.json','project_design',
            ['Typed observations, relation distinctions and unresolved meanings','Public/generated comparison and prototype-before-bank investment'],
            [{'local_copy':ref(BASE/'omissions-register.json','Remaining concrete evidence and research routes')}])]
    write(BASE/'source-audit.json',{'sources':sources,'prior':ref(work.PRIOR,'677 preserved source records'),
        'cutoff':'2026-10-07','paper_count_added':6,'record_count_added':9})
    work.OUTPUT.parent.mkdir(parents=True,exist_ok=True);assert not work.OUTPUT.exists()
    subprocess.run(['pandoc','--from=latex','--to=markdown','--wrap=auto',str(BASE/'development.tex'),'-o',str(work.OUTPUT)],check=True)
    write(BASE/'recovery-review.json',{'status':'recovered_and_continuing','findings':[
        'Controller check passed after crash;117/376 proposal operations, variable ontology active,862-page reader intact.',
        'Six acquired originals, five pinned code files and previous reporting publication receipt preserved.',
        'Initial manuscript tool invocation failed before mutation because LaTeX quotation backticks terminated a JavaScript template; repaired with emphasis/plain prose.',
        'Original exact receipt field pooled_balanced_accuracy was ambiguous; successor names it pooled_accuracy_equal_arms. Values and original evidence unchanged.',
        'No image previews used; inherited visual allowance remains exhausted.'],
        'evidence':[ref(BASE/'exact-results.json','Preserved original field naming'),
                    ref(BASE/'exact-results-v2.json','Clarified equal-arm accuracy field'),
                    ref(ROOT/'docs/program/execution/2026-10-16/reporting-monitoring/publication-v2/git-publication-d5b281ad.json','Verified predecessor publication')]})
    evidence=[ref(BASE/n,n) for n in ['plan.md','source-review.json','candidate-reassessment.json','omissions-register.json',
              'exact-results-v2.json','arithmetic-review.json','proposed-contract.json','source-audit.json','development.tex','recovery-review.json']]
    evidence += [ref(work.OUTPUT,'Connected contracted synthesis'),ref(Path(__file__),'Criterion-specific author review')]
    for row in evidence:verify_bindings(row)
    write(BASE/'author-review.json',{'status':'pass','reviewer':work.REVIEWER,
        'scope':'Bounded proposal task; not exhaustive census, independent, visual or capability acceptance',
        'findings':FINDINGS,'evidence':evidence,'limitations':work.LIMITS,'integration_allowed':False,'visual_acceptance':False,
        'plan_review':['Causal truth cannot follow from vocabulary consistency or model confidence.',
            'Refusal and unresolved labels need separate scoring; missing outputs remain in the denominator.',
            'Public/generated examples precede expensive authentic measurement work.',
            'Source failures and visual allowance do not block other proposal branches.'],
        'depth_credit':'No automatic mandatory-repair or chapter-depth acceptance; inherited examples receive no duplicate credit.'})
    write(BASE/'progress.json',{'finding':'Recovered and completed ten-paper ontology synthesis, six exact families and pinned static code review; integration is next.',
        'next_action':'Prepare successor reader, compile and inspect text/bounds; record task, publish, renew Q2-Q4, commit/push and continue next eligible operation.',
        'evidence':[ref(BASE/'author-review.json','Reviewed completed author work'),ref(BASE/'recovery-review.json','Crash recovery and observed repairs')]})
    print(json.dumps({'new_records':9,'new_papers':6,'author_review':'pass','synthesis':str(work.OUTPUT.relative_to(ROOT))}))


if __name__=='__main__':main()
