#!/usr/bin/env python3
"""Assemble authored discovery comparisons and exact response-count checks."""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'docs/program/repair-v12/work/LA03'
AUDIT=ROOT/'docs/program/repair-v12/work/LA01/source-audit.json'


def ref(p,anchor):
    return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'anchor':anchor}


def save(n,x):
    (WORK/n).write_text(json.dumps(x,indent=2)+'\n')


# Mechanism, primary IDs, statistical role, counterexample, candidate remedy and
# limitation: authored decisions, not a claim of executed package comparison.
ROWS=[
('language_relations',['2305.00050','2407.19638'],'Predict pairwise causal assertions from variable descriptions.',
 'A familiar word pair may be recalled from training while the target bank has a different assignment mechanism.',
 'Test unfamiliar mechanism/label combinations and context-specific evidence; preserve abstention.',
 'Novel labels reduce a shortcut but do not establish true mechanisms.'),
('breadth_first_proposals',['2402.01207'],'Propose graph neighborhoods with fewer model calls.',
 'The acyclic reverse graph in LA02 has the same observed table and a different causal effect.',
 'Keep equivalent graph alternatives and measure tokens/latency as well as calls.',
 'Syntactic DAG validity and lower call count do not establish scientific truth or full cost.'),
('language_response_tests',['2406.07378'],'Use distributions of YES/NO model responses as discovery input.',
 'Same-batch category proportions have negative covariance; an independent-proportion standard error can reject too often even under a simple response null.',
 'Use a correct declared response-sampling model, independent numerical CI tests and type-separated result fields.',
 'Calibrated response uncertainty still says nothing by itself about bank conditional independence.'),
('retrieval_guidance',['2402.15301','2609.30867'],'Retrieve evidence for relationships and assumption audits.',
 'LACR documents reduce ASIA skeleton F1 in the inspected reported experiment; a retrieval miss can masquerade as evidence absence.',
 'Adversarial/wrong-domain retrieval ablations, exact anchors and separate retrieval-failure labels.',
 'A relevant citation may still be inapplicable or scientifically wrong.'),
('ancestral_constraints',['2306.16902'],'Turn metadata and language judgments into ancestral path constraints or penalties.',
 'A->M->Y makes A an ancestor of Y without an A->Y direct edge; an importer can silently change the constraint.',
 'Represent path and adjacency constraints with different types and test their conversion.',
 'Correct type conversion does not validate the elicited constraint or its independence approximation.'),
('soft_graph_prior',['2405.13551','2306.16902'],'Combine data score with a language-derived soft preference over graphs.',
 'A wrong high-weight prior can dominate a weak likelihood even when every DAG keeps positive prior support.',
 'Predeclare prior strength, compare the zero-prior baseline and inspect contradictory evidence.',
 'Soft support is not calibrated graph coverage, especially after pruning.'),
('statistical_prompting',['2402.01454'],'Feed numerical discovery summaries to an LLM and threshold its responses into method-specific constraints.',
 'The same dataset can drive both the initial evidence and the generated restriction; treating them as independent multiplies the same information.',
 'Track reuse, validate the actual joint procedure and preserve forced/forbidden/unknown states.',
 'Sample splitting does not establish prior truth or all downstream assumptions.'),
('agent_debate',['2407.15073'],'Assign causal-discovery roles and aggregate debate among models.',
 'Agents sharing a model, corpus or retrieved text can agree on the same erroneous collider orientation.',
 'Compare to one-agent and no-language baselines; cluster perturbations by mechanism and shared source.',
 'Agent diversity does not supply independent scientific observations.'),
('temporal_initialization',['2404.14786'],'Initialize numerical temporal graph/intervention-target optimization from textual system information.',
 'An anomaly produced by an unobserved market shock is not necessarily a verified intervention regime.',
 'Audit regime/clock assumptions and compare random, language and expert initialization with identical data.',
 'Population optimization claims do not certify a stochastic optimizer or finite-sample uncertainty.'),
('noisy_expert_pag',['2506.16234'],'Allocate language queries across successive contemporaneous observation batches while retaining PAG outputs.',
 'A confident answer histogram can orient the wrong edge; successive batches are not dynamic treatment histories.',
 'Preserve circle endpoints and model the query channel separately; evaluate downstream effect sets.',
 'No general simultaneous graph or temporal policy confidence follows from response entropy.'),
('numerical_temporal_foundation',['2602.18662'],'Use a pretrained numerical transformer to estimate temporal graphs.',
 'A hidden common cause violates the inspected sufficient, lagged-only model class even if predictions are accurate.',
 'Use regime-specific assumption screens and compare numerical baselines; acquire exact weights before execution.',
 'This adjacent model is not an LLM and cannot diagnose every violated assumption.'),
('mechanism_and_experiment',['2305.16183','2608.09696'],'Propose mechanisms/strategies, fit them numerically and acquire new intervention information.',
 'An adaptively pruned model pool can omit a policy-relevant mechanism, while finite prediction remains good.',
 'Retain residual checks and alternative pools; compare acquisitions under matched intervention and total-cost budgets.',
 'Open-loop finite predictive success is not closed-loop bank-policy identification.'),
('protected_core_orchestration',['2606.23608','2602.11527'],'Use an assistant for data review, assumption elicitation and fixed tool calls around a formal core.',
 'A valid tool can still receive a wrong variable mapping, target or scientific assumption.',
 'Bind full semantic context and preserve algorithm outputs/refusals; test altered targets and missing sources.',
 'Transport and schema conformance do not verify causal premises.'),
]

FAILURES=[
('memorization','Public benchmark names disclose familiar edges.','Unfamiliar labels crossed with familiar and novel mechanisms.','Use independent mechanism truth; label novelty alone is insufficient.'),
('context_shift','A retrieved relation belongs to another population or intervention.','Hold target fixed while substituting relevant, irrelevant and contradicted documents.','Some context changes legitimately change the causal claim.'),
('ancestor_as_edge','An ancestral path constraint is imported as adjacency.','A->M->Y fixture with no direct A->Y edge.','Algorithm-specific constraint syntax still needs source review.'),
('collider_orientation','An explanation favors a common-cause story when selection creates association.','Matched chain, fork and collider fixtures with missing/selected records.','Discovery depends on faithfulness, sampling and measured-variable assumptions.'),
('cycle_repair','A cycle is removed by arbitrarily deleting a scientifically important edge.','Conflicting prompt proposals with different deletion priorities.','Acyclicity is a representation constraint, not a truth criterion.'),
('latent_omission','All alternatives assume sufficiency although an unmeasured cause changes effects.','Equivalent observed laws with distinct latent/causal mechanisms.','Additional scientific information may be necessary; more language calls cannot supply it.'),
('clock_leakage','Post-decision information is used as a baseline feature.','Delayed L1 fixture and revised event-time records.','Timestamp declarations need authentic process audit.'),
('response_miscalibration','Response votes are called CI-test p-values or edge probabilities.','Exact same-batch multinomial variance and binary-tail calculations.','Even a correct response test is not a bank sampling-law test.'),
('double_use','Data enters a language prior and a likelihood with an assumed independence that does not hold.','Track identical data hashes across initial analysis, prompt and final fit.','The actual joint procedure needs a proof or registered calibration study.'),
('set_collapse','A PAG or disconnected effect union becomes a single confident number.','Preserve {0,0.8}, circle marks and unrestricted sets across all surfaces.','An outer set still needs true-model retention and within-model validity.'),
('selected_denominator','Only successful graphs, tool calls or evaluable worlds enter reported accuracy.','All-request outcome ledger including invalid, refused, failed and unavailable cases.','Conditional accuracy remains useful only with its denominator explicit.'),
('adaptive_threshold','The prompt, prior weight or pruning rule is tuned on the reported test cells.','Freeze tuning splits, rule versions and complete stopping policy before LA06.','New drift or out-of-class mechanisms remain an external-validity limitation.'),
('unaudited_runtime','Generated code or an unbounded notebook crosses the fixed-operation boundary.','Malformed output, stale artifact, timeout and unauthorized-tool fixtures.','Local conformance does not establish platform security or bank acceptance.'),
]


def build():
    WORK.mkdir(parents=True,exist_ok=True)
    known={s['id'] for s in json.loads(AUDIT.read_text())['sources']}
    methods=[]
    for name,ids,role,counter,remedy,limit in ROWS:
        sources=['v12_la_'+x.replace('.','_') for x in ids]
        assert set(sources)<=known
        methods.append({'id':name,'source_ids':sources,'scientific_role':role,'counterexample':counter,
                        'candidate_remedy':remedy,'remaining_limit':limit,'qualification':'literature/static comparison only'})
    save('methods-matrix.json',{'status':'reviewed','literature_cutoff':'2026-10-07',
         'source_audit':ref(AUDIT,'Frozen LA01 primary claims and anchors'),'methods':methods,
         'scope':'No matched package/LLM experiment was executed.'})
    save('failure-remedies.json',{'status':'reviewed','failures':[{'id':n,'failure':f,'proposed_test':t,'limit':l,
         'execution_status':'proposed for LA06; exact analytical examples separately recorded'} for n,f,t,l in FAILURES]})
    # Exact probability summation under a stated iid binary-response law, not
    # calls to the collected implementation and not a Monte Carlo experiment.
    n=100; alpha=0.01; z=norm.isf(alpha)
    rejected=[k for k in range(n+1) if (2*k/n-1)/math.sqrt(0.5/n)>=z]
    probability=sum(Fraction(math.comb(n,k),2**n) for k in rejected)
    assert float(probability)>alpha
    example={'status':'pass','kind':'project exact analytical counterexample',
       'response_law':'100 independent binary responses; P(NO)=P(YES)=1/2; both counts from the same sample',
       'variance_identity':'Var(p_NO-p_YES)=[p_NO+p_YES-(p_NO-p_YES)^2]/n',
       'true_null_variance':1/n,'inspected_formula_null_variance':0.5/n,
       'one_sided_nominal_alpha':alpha,'first_rejecting_no_count':min(rejected),
       'exact_rejection_probability_fraction':str(probability),'rejection_probability':float(probability),
       'scope':'The independent-proportion denominator is too small for these mutually exclusive same-sample counts. No claim that real model responses are iid; no bank CI-test validity follows from correcting it.'}
    save('response-count-derivation.json',example)
    source=ROOT/'docs/literature/raw/v12_la_causal_gpt_source_1.txt'
    save('source-addendum.json',{'status':'reviewed','sources':[{
       'identity':'IPL-UV/causal_GPT','version':'2001fb5660d8e5d9a6c3a159b41d739316b8f91a','version_date':'2024-06-12',
       'local_copy':ref(source,'lines 197–306 response aggregation; 565–579 test_prop; 606–637 binary pvalue conversion'),
       'supported_claims':['The response aggregation supplies nNO and nYES to the pooled-proportion test from the same response collection.','The inspected denominator is sqrt(p*(1-p)*2/n), with p=(nNO+nYES)/(2*n).','The PC-style interface converts the decision to 0 or 1.'],
       'project_derivation':ref(WORK/'response-count-derivation.json','Separate exact same-batch binary-response counterexample'),
       'qualification':'Static inspection and project mathematics; no package or model execution'}]})
    print(json.dumps({'methods':len(methods),'failure_modes':len(FAILURES),'analytical_response_null_rejection':float(probability)}))


if __name__=='__main__':
    build()
