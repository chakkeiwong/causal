#!/usr/bin/env python3
"""Inspect an adjacent simulation-code original without granting causal capability."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib,json
import chronollm_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/census-chronollm-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/census-agent-unlearning-v1'
RAW=ROOT/'docs/literature/raw'
PDF=ROOT/'docs/papers/ChronoLLM Customizing Language Models for Physics-Based Simulation Code Generation Wang(2025).pdf'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected genuine2025preprint and exact authored examples; later journal original not acquired.',
 'Source empirical reports are not independent reproductions; no downloaded code, model, simulator, API or training executed.',
 'Code similarity, judge score, execution correctness, causal identification and bank value remain separate.',
 'Training/task/scorer artifacts, exact rights, total costs and matched native qualification remain unresolved.',
 'Visual, independent and final acceptance remain open; no global blocker for independent work.']

def main():
    assert not (BASE/'review.json').exists()
    identity=read(BASE/'identity-review.json');receipt=read(RAW/'exec24_chronollm_original.receipt.json')
    assert PDF.read_bytes()==(RAW/'exec24_chronollm_original.pdf').read_bytes()
    assert hashlib.sha256(PDF.read_bytes()).hexdigest()==receipt['sha256']==identity['paper']['sha256']
    pages=(BASE/'original.txt').read_text().split(chr(12));assert len([x for x in pages if x.strip()])==52
    assert '2508.13975v1' in pages[0] and '19 Aug 2025' in pages[0]
    specs=[(1,2,'Original identity and scope: generated mechanical-simulation scripts, often requiring expert improvement.'),
      (9,17,'Version changes, continued pretraining, in-context learning, SFT/PEFT and reported expert/model-assisted dataset curation.'),
      (18,20,'Similarity, execution and LLM-judge metrics are distinct; judge correlations are attributed to a companion study.'),
      (21,23,'Tables6-8 have metric-dependent gains/losses; fine-tuning cost example excludes prior data preparation.'),
      (24,24,'Authors acknowledge in-distribution case studies; API, world/axis/units errors distinguished.'),
      (28,28,'Vehicle generation and iterative modification are source-reported demonstrations, not local reproduction.'),
      (36,38,'Brittleness and domain-data limits; unlearning/tool/multi-agent extensions remain future work; artifact availability language differs across sections.')]
    paper=dict(integrated_citation_key='exec24_chronollm_original',kind='paper',title='ChronoLLM: Customizing Language Models for Physics-Based Simulation Code Generation',filename_title='ChronoLLM Customizing Language Models for Physics-Based Simulation Code Generation',author='Jingquan Wang and Andrew Negrut and Harry Zhang and Khailanii Slaton and Shu Wang and Radu Serban and Jinlong Wu and Dan Negrut',first_author='Wang',year=2025,source_identity='https://arxiv.org/abs/2508.13975v1',version_date='v1;19August2025;only revision shown on inspected archive page;before7October2026 cutoff',local_path=str(PDF.relative_to(ROOT)),sha256=receipt['sha256'],local_copy=ref(PDF,'Genuine52-page original'),identity_evidence=[ref(RAW/n,'Archive/acquisition identity') for n in ['exec24_chronollm_abs.html','exec24_chronollm_abs.receipt.json','exec24_chronollm_original.receipt.json']]+[ref(BASE/'identity-review.json','Preprint distinguished from later journal discovery')],inspected_anchors=[dict(anchor=f'PDF pages{a}-{b}',pages=[a,b],finding=f,text_extract=ref(BASE/'original.txt',f'Form-feed pages{a}-{b}')) for a,b,f in specs],supported_claims=[f for _,_,f in specs],limitations=LIMITS)
    result=exact.calculate();write(BASE/'exact-results.json',result)
    assert result['source_table7']['deltas']['gpt4omini']['sft_minus_pre']==['2623/100','812/25','-519/100']
    assert result['source_table7']['deltas']['llama31_8b']['sft_minus_icl'][0]=='-7/25'
    assert result['authored_causal_worlds']['causal10']['effect_usd']=='10' and result['authored_causal_worlds']['causal0']['effect_usd']=='0'
    assert result['stipulated_full_cost']['total_usd']=='33' and result['stipulated_full_cost']['per_accepted_usd']=='33/2'
    project=dict(integrated_citation_key='exec24_chronollm_reference',kind='project_derivation_and_exact_reference',title='Authored metric contrasts, observationally equivalent causal worlds and complete workflow costs',author='Causal banking proposal project',year=2026,source_identity='tools/chronollm_reference_20261024.py',version_date='24October2026;exact Fraction arithmetic',local_copy=ref(Path(exact.__file__),'Independent exact reference'),inspected_anchors=[ref(BASE/'exact-results.json','Table subtractions, two structural worlds and stipulated full costs')],supported_claims=['Reported GPT4omini combined score changes26.23 while documentation score changes-5.19;8B combinedSFT-minusICL=-0.28.','A=U with Y=10A+20U orY=30U yields identical observed pairs but intervention effects10and0USD;stipulatedcost5 yieldsnet5and-5.','StipulatedAPI3plus30expert-minutes at60USD/hour gives33USD;percompiled5.5 andperaccepted16.5.'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[paper,project],cutoff='2026-10-07',native_execution=False))
    omissions=[('empirical_reproduction','Acquire exact task/train/evaluation splits, scorer/judge revision and raw repeated-run artifacts; identify the referenced Hacked SimBench baseline and numerical execution results before stronger claims.'),('companion_original','Acquire and inspect the genuine SimBench companion original before adopting judge-correlation or benchmark details; bibliography is discovery only.'),('source_version','Keep2025preprint and later2026journal identity separate; acquire final original before claiming equivalence.'),('artifact_rights','Resolve on-request model/API access, exact code/data repository revision and licenses; reported availability is not local possession or reuse clearance.'),('public_prototype','Hold out task and API versions, separate code/semantic/causal checks, preserve all failures and expert edits, and use exact generated-world refusal oracles.'),('economics','Include curation, training, inference, expert repairs, failed attempts, storage and maintenance; the source3USD example is not total cost or current quote.'),('candidate27','OpenAlex identifies Agent-guided Causal Discovery with a Small Language Model as closed with no repository fulltext in this response; this is metadata-only, not proof that no accessible original exists.'),('visual','Fresh image allowance and final acceptance remain open; source/math/text work continues.')]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=g,next_action=a,global_blocker=False) for g,a in omissions],discovery_evidence=ref(RAW/'exec24_agentguided_search.json','Candidate27 discovery only'),native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_examples',evidence=[ref(BASE/'exact-results.json','Exact outputs'),ref(Path(exact.__file__),'Enumerated two-point worlds and rational arithmetic'),ref(BASE/'development.tex','Declared model, assumptions and banking costs')],findings=project['supported_claims'],limitations=['No score uncertainty or causal productivity claim inferred from differences.','Latent type and deterministic action yield observational equivalence; intervention changes A while preserving U.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],findings=['Metric-specific adverse results preserved; no blanket model superiority.','Reported cost, illustrative cost and actual prices remain distinct.','Simulation code does not identify an intervention; absence of native execution explicit.','Source availability discrepancies retained without misconduct inference.'],visual_acceptance=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_source_review_and_preserving_integration',evidence=[ref(BASE/'plan-review.json','Acquisition plan'),ref(BASE/'source-audit.json','Primary-supported claims'),ref(BASE/'mathematical-review.json','Exact witnesses')],steps=['Retain genuine original and authenticated archive identity.','Integrate adjacent code-assistance lessons with causal and economic counterexamples.','Preserve1041priorrecords and236papers; add2records and1paper.','Advance onlycandidate120; preserve all other identities and four crosscutting gaps.','Publish paired reader/sponsor, reconcile commercial disposition and census, commit/push and continue.']))
    reg=deepcopy(read(PRIOR/'census-register.json'));old=deepcopy(reg);row=next(x for x in reg['items'] if x['id']=='LA01-candidate-120');assert row['disposition']=='open_original_not_inspected'
    row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key=paper['integrated_citation_key'],primary_source_record=paper,publication_keys=[paper['integrated_citation_key'],project['integrated_citation_key']],task_families=['data_code','agent_architecture','evaluation_cost'],mapping_basis='Adjacent domain-specific code generation, versioned knowledge and evaluation/cost design; no causal discovery capability.',availability='Genuine52-page2025preprint acquired; selected technical sections inspected; no model/code or visual execution.',effect_on_claims='Retain conditional prototype design and source limitations; withhold empirical causal, productivity and native integration claims.',next_action='Resolve exact task/split/scorer artifacts and companion original; register held-out API/task and full-cost semantic/refusal prototype.')
    assert all(x==next(y for y in reg['items'] if y['id']==x['id']) for x in old['items'] if x['id']!=row['id'])
    counts=dict(Counter(x['disposition'] for x in reg['items']));assert counts['inspected_primary_retained_with_limits']==75 and counts['open_original_not_inspected']==38
    reg.update(counts=counts,supersedes=ref(PRIOR/'census-register.json','Preserved74/39census'),changes=['Onlycandidate120 advances;113identities preserved.'],closure=False,interpretation='75of113inspected;38unread;fourcrosscutting obligations open.');write(BASE/'census-register.json',reg)
    mapping=deepcopy(read(PRIOR/'task-map.json'))
    for fam in mapping['task_families']:
        if row['id'] in fam.get('uninspected_candidate_ids',[]):fam['uninspected_candidate_ids'].remove(row['id'])
        if fam['id'] in row['task_families']:
            for field,values in [('inspected_candidate_ids',[row['id']]),('inspected_source_keys',row['publication_keys'])]:
                fam.setdefault(field,[]);fam[field].extend(x for x in values if x not in fam[field])
        fam['coverage_acceptance']=False
    mapping.update(register=ref(BASE/'census-register.json','75/38successor'),supersedes=ref(PRIOR/'task-map.json','Preserved task mapping'));write(BASE/'task-map.json',mapping)
    evidence=[ref(BASE/n,'Reviewed original and authored proposal evidence') for n in ['source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review-v2.json','development.tex','sponsor-addition.md','omissions-register.json','census-register.json','task-map.json']]+[ref(Path(__file__),'Preserving audit logic')]
    review=dict(status='pass_for_scoped_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),candidate=row['id'],evidence=evidence,findings=['Two audited records bind52-page original and exact authored examples.','Source score, availability, execution and full-cost limits retained.','Onlycandidate120advances to75/38;fourcrosscutting tasks remain open.'],limitations=LIMITS,coverage_acceptance=False,native_execution=False,visual_acceptance=False);verify_bindings(review);write(BASE/'review.json',review)
    write(BASE/'progress.json',dict(finding='Candidate120 original reviewed; metric-specific comparisons and exact causal/cost witnesses developed;75/38census.',next_action='Publish preserving ChronoLLM reader/sponsor and refresh all obligations including commercial workflow comparison; continue38unread originals and fourcrosscutting tasks.',yield_reason='Release census for publication; no global stop.',evidence=[ref(BASE/'review.json','Scoped review'),ref(BASE/'census-register.json','75/38census')]))
    print(json.dumps(dict(inspected=75,unread=38,audited_records=2,genuine_new_papers=1,native_execution=False)))

if __name__=='__main__':main()
