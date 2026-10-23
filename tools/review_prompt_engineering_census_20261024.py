#!/usr/bin/env python3
"""Review one original survey; preserve the census and all empirical limits."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib,json
import prompt_engineering_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write as immutable_write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/census-prompt-engineering-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/census-llm-challenges-v1'
RAW=ROOT/'docs/literature/raw'
PDF=ROOT/'docs/papers/Unleashing the potential of prompt engineering for large language models Chen(2025).pdf'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected58-page May2025arXivv6;initial2023v1 and journal identity are separate.',
 'Survey is primary evidence of its taxonomy/examples/caveats; underlying method/empirical originals are not silently adopted.',
 'Exact authored probability/decision/authorization examples; no model, downloaded code, native integration or bank experiment executed.',
 'Prompt selection needs held-out tasks; generated premises, oracle assistance and computational graphs do not supply causal identification.',
 'Visual, independent and final acceptance and mandatory coverage/depth remain open.']

def write(path,data):
    if path.exists():
        assert read(path)==data, 'Existing artifact differs; use a successor: '+str(path)
    else:
        immutable_write(path,data)

def main():
    assert not (BASE/'review.json').exists()
    ident=read(BASE/'identity.json');receipt=read(RAW/'exec24_promptengineering_v6.receipt.json')
    assert PDF.read_bytes()==(RAW/'exec24_promptengineering_v6.pdf').read_bytes()
    assert hashlib.sha256(PDF.read_bytes()).hexdigest()==receipt['sha256']==ident['sha256']
    pages=(BASE/'original-v6.txt').read_text().split(chr(12))
    assert len([x for x in pages if x.strip()])==58 and '2310.14735v6' in pages[0] and '11 May 2025' in pages[0]
    specs=[(1,4,'v6identity, scope and illustrated GPT4 examples; provider parameter and sampling claims not adopted.'),
      (8,12,'Prompt/generated-context examples introduce unstated premises; supplied-solution caveat retained;zero-shot does not prove pretraining absence.'),
      (13,19,'Computational graph/decomposition, example selection and optimization taxonomy; underlying methods/packages remain unqualified.'),
      (26,31,'Human/automatic/task evaluation, noncomparable metrics and reported limits of automated prompts; no inherited ranking.'),
      (32,38,'Synthetic-data applications, security threats, proposed defenses and prospective agents; no security or optimality guarantee adopted.'),
      (39,39,'Selected bibliography identities are discovery only, not inspected underlying technical originals.')]
    paper=dict(integrated_citation_key='exec24_promptengineering_original',kind='paper',title='Unleashing the potential of prompt engineering for large language models',filename_title=ident['title'],author=' and '.join(ident['authors']),first_author='Chen',year=2025,source_identity='https://arxiv.org/abs/2310.14735v6',version_date='v6;11May2025;latest of6listed revisions;before7October2026cutoff;archive and final journal bytes not equated',local_path=str(PDF.relative_to(ROOT)),sha256=ident['sha256'],local_copy=ref(PDF,'Genuine58-page original'),identity_evidence=[ref(RAW/n,'Archive identity and acquisition') for n in ['exec24_promptengineering_abs.html','exec24_promptengineering_abs.receipt.json','exec24_promptengineering_v6.receipt.json']]+[ref(BASE/'identity.json','Preserved acquisition identity')],inspected_anchors=[dict(anchor=f'PDF pages{a}-{b}',pages=[a,b],finding=f,text_extract=ref(BASE/'original-v6.txt',f'Form-feed pages{a}-{b}')) for a,b,f in specs],supported_claims=[f for _,_,f in specs],limitations=LIMITS)
    result=exact.calculate();write(BASE/'exact-results.json',result)
    assert result['missing_premises']['net_lower_usd']=='-120'
    assert result['authority']['admitted']==1 and result['pipeline']['independent_all_success']=='2476099/3200000'
    project=dict(integrated_citation_key='exec24_promptengineering_reference',kind='project_derivation_and_exact_reference',title='Authored prompt-selection, missing-premise, pipeline and tool-authority witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/prompt_engineering_reference_20261024.py',version_date='24October2026;exact rational arithmetic, binomial sums and Boolean enumeration',local_copy=ref(Path(exact.__file__),'Exact authored reference'),inspected_anchors=[ref(BASE/'exact-results.json','Complete exact outputs'),ref(BASE/'development.tex','Assumptions, equations and banking meaning')],supported_claims=['20equally accurate independent prompts on4tasks yield expectedbest93.1096%development but50%fresh accuracy; probabilitysomeperfect72.4941%.','Netvalue1000d-20 with d in[-.1,.1] ranges[-120,80]USD; assumed.05 gives30 andbreak-even.02.','Five correctness events with marginals.95 imply allcorrect between.75and.95; independence gives2476099/3200000.','Trustedrequest AND allowedaction AND matchingartifact admits1of8Boolean cases; not a native security guarantee.','Stipulated30USD for10attempts and3accepted yields3perattempt and10peraccepted.'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[paper,project],cutoff='2026-10-07',native_execution=False))
    omissions=[('underlying_originals','Inspect genuine originals for prompting/search/decomposition frameworks and benchmarks before technical adoption; verify possible PromptAgent/PromptSource conflation and causal-transformer claims.'),('provider_specifications','Do not inherit unsupported GPT4 parameter-size or sampling/API claims from the survey; resolve exact provider/model revisions through primary specifications if needed.'),('search_coverage','Complete the remaining original census and cutoff-bounded coverage; broad survey does not supply our saturation or completeness criteria.'),('prototype_protocol','Register held-out task/version splits, prompt search/repair budget, independent causal/refusal oracles and failure-complete costs before a new native run.'),('security_implementation','Qualify actual trust boundaries, policy/parser/hash binding and execution atomicity; Boolean predicate and prompting do not establish deployment security.'),('journal_version','Acquire final journal original before claiming byte or substantive equivalence with arXivv6.'),('visual','Figure text contains replacement glyphs;fresh visual and independent/final acceptance remain open.')]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=g,next_action=a,global_blocker=False) for g,a in omissions],native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_examples',evidence=[ref(BASE/'exact-results.json','Exact rational outputs'),ref(Path(exact.__file__),'Binomial selection, decision bounds and Boolean enumeration'),ref(BASE/'development.tex','Assumptions and interpretation')],findings=project['supported_claims'],limitations=['No empirical error rates, task uncertainty, pricing or transport claim inferred.','Prompt-selection and stage-independence assumptions are explicit; logical admission does not test a live security boundary.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected scholarly argument'),ref(BASE/'sponsor-addition.md','Investment implications')],findings=['Survey findings separated from underlying empirical claims.','Historical scope and both favorable/adverse reports retained.','Public/generated test merit distinguished from bank truth.','Equations explain clocks, shared errors, mixture sensitivity, interaction and denominators.'],visual_acceptance=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_scoped_review_and_preserving_integration',evidence=[ref(BASE/'plan-review.json','Original reviewed plan'),ref(BASE/'inspection-checkpoint-v2.json','Text-inspection successor'),ref(BASE/'source-audit.json','Source/claim boundaries'),ref(BASE/'mathematical-review.json','Exact witnesses')],steps=['Preserve acquired original, audit version and claim anchors.','Keep secondary references out of inherited technical adoption.','Integrate exact authored witnesses and conditional implementation alternatives.','Preserve1052predecessor records and238papers; add2records and1paper.','Advance onlycandidate284; preserve every other census identity/disposition and crosscutting gap.','Publish preserving reader and paired sponsor, reconcile, commit/push and continue eligible work.']))
    reg=deepcopy(read(PRIOR/'census-register.json'));old=deepcopy(reg)
    row=next(x for x in reg['items'] if x['id']=='LA01-candidate-284');assert row['disposition']=='open_original_not_inspected'
    row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key=paper['integrated_citation_key'],primary_source_record=paper,publication_keys=[paper['integrated_citation_key'],project['integrated_citation_key']],task_families=['business_translation','diagram_construction','data_code','agent_architecture','evaluation_cost'],mapping_basis='Prompting taxonomy informs question preservation, held-out evaluation, composition and authority contracts; no causal algorithm or native capability.',availability='Genuine58-page2025preprint acquired; selected text sections inspected; no visual/model/native execution.',effect_on_claims='Retain survey critique and exact authored witnesses; withhold method rankings, native/security and bank-value claims.',next_action='Complete underlying-original and task/version coverage, then preregister justified public/generated comparison with semantic/refusal oracles and full costs.')
    assert len(reg['items'])==117 and sum(x['id'].startswith('LA01-candidate-') for x in reg['items'])==113 and all(x==next(y for y in reg['items'] if y['id']==x['id']) for x in old['items'] if x['id']!=row['id'])
    counts=dict(Counter(x['disposition'] for x in reg['items']));assert counts['inspected_primary_retained_with_limits']==77 and counts['open_original_not_inspected']==36
    reg.update(counts=counts,supersedes=ref(PRIOR/'census-register.json','Preserved76/37census'),changes=['Onlycandidate284 advances;113identities and fourcrosscutting obligations preserved.'],closure=False,interpretation='77of113inspected;36unread;fourcrosscutting obligations open.');write(BASE/'census-register.json',reg)
    mapping=deepcopy(read(PRIOR/'task-map.json'))
    for fam in mapping['task_families']:
        if row['id'] in fam.get('uninspected_candidate_ids',[]):fam['uninspected_candidate_ids'].remove(row['id'])
        if fam['id'] in row['task_families']:
            for field,values in [('inspected_candidate_ids',[row['id']]),('inspected_source_keys',row['publication_keys'])]:
                fam.setdefault(field,[]);fam[field].extend(x for x in values if x not in fam[field])
        fam['coverage_acceptance']=False
    mapping.update(register=ref(BASE/'census-register.json','77/36successor'),supersedes=ref(PRIOR/'task-map.json','Preserved task mapping'));write(BASE/'task-map.json',mapping)
    evidence=[ref(BASE/n,'Reviewed original and authored proposal evidence') for n in ['source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review-v2.json','development.tex','sponsor-addition.md','omissions-register.json','census-register.json','task-map.json']]+[ref(Path(__file__),'Preserving audit logic')]
    review=dict(status='pass_for_scoped_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),candidate=row['id'],evidence=evidence,findings=['Two audited records bind58-page original and exact authored witnesses.','Versioned survey, underlying originals and authored examples remain distinct.','Onlycandidate284 advances to77/36;fourcrosscutting obligations stayopen.'],limitations=LIMITS,coverage_acceptance=False,native_execution=False,visual_acceptance=False);verify_bindings(review);write(BASE/'review.json',review)
    write(BASE/'progress.json',dict(finding='Candidate284 original reviewed with source boundaries and exact authored witnesses;77inspected/36unread originals.',next_action='Publish preserving prompt-engineering reader and paired sponsor, reconcile all obligations and continue36unread originals plus fourcrosscutting tasks; independent software/reuse branches remain eligible.',yield_reason='Release source review for preserving publication; no global stop.',evidence=[ref(BASE/'review.json','Scoped source review'),ref(BASE/'census-register.json','77/36census')]))
    print(json.dumps(dict(inspected=77,unread=36,audited_records=2,genuine_new_papers=1,native_execution=False)))

if __name__=='__main__':main()
