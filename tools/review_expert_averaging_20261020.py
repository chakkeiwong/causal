#!/usr/bin/env python3
"""Bounded review of expert-guided graph averaging and preserving census reconciliation."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

import expert_averaging_reference_20261020 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-20/census-expert-averaging-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-20/census-validity-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=['Bounded primary-paper inspection, not independent reproduction or complete literature coverage.',
        'No released implementation, native engine, supplementary dataset or live model executed or independently authenticated.',
        'Printed pseudocode traces describe the printed specification only; they do not prove runtime defects.',
        'Reported benchmark results, authored witnesses and proposed banking experiments have separate evidence status.',
        'No rendered visual review; inherited image allowance exhausted. Final proposal and bank qualification remain open.']


def main():
    assert not (BASE/'source-audit.json').exists()
    assert exact.calculate()==read(BASE/'exact-results.json')
    write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(BASE/'plan.md','Scope and hazards reviewed')],
        checks=['Select May2026 v2 before cutoff, preserving v1 and metadata title variation.',
                'Separate indirect causal ordering, adjacency, graph frequencies and intervention identification.',
                'Read the real-LLM appendix as well as simulated-expert results; retain cache, exclusions and adverse cases.',
                'Reproduce printed-control-flow discrepancies without alleging uninspected code behavior.',
                'Preserve116 other census records and all prior reader citations and chapters.']))
    for tag in ['abs','v1','v2']:
        suffix='html' if tag=='abs' else 'pdf'
        path=RAW/f'exec20_expert149_{tag}.{suffix}'
        receipt=read(RAW/f'exec20_expert149_{tag}.receipt.json')
        assert receipt['status']=='saved' and receipt['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
    identity=RAW/'exec20_expert149_abs.html';html=identity.read_text()
    assert '7 May 2026 12:30:55 UTC' in html and '23 Jan 2026 13:01:30 UTC' in html
    pages=(BASE/'original-v2.txt').read_text().split(chr(12))
    assert sum(bool(p.strip()) for p in pages)==41 and 'Adrick Tench' in pages[0] and 'Thomas Demeester' in pages[0]
    title='Dynamic Expert-Guided Model-Averaging for Causal Discovery'
    pdf=ROOT/'docs/papers'/f'{title} Tench(2026).pdf';data=(RAW/'exec20_expert149_v2.pdf').read_bytes()
    assert data.startswith(b'%PDF-')
    with pdf.open('xb') as f:f.write(data)
    anchors={1:'v2 title, authors,7May2026 identifier and anonymous code lead.',
        3:'Inputs are learned partially directed graphs; target is an unknown DAG; expert answers existence and direction queries.',
        4:'Competence, diversity, budget and query-value assumptions; expert existence concerns a possibly indirect path.',
        5:'Greedy adjacency counts, separate orientation thresholds, cycle checks and claimed majority fallback after budget exhaustion.',
        6:'Simulated expert answers ancestry rather than direct adjacency; seven categorical benchmark networks and20 column orderings.',
        7:'Simulated accuracy70%/90%,thresholds0/0.9,budget2N; denominators vary with missing/invalid outputs; noisy bidirected scoring limit.',
        9:'Query-budget precision/recall tradeoff; no formal recovery guarantee; only synthetic categorical data; equal model weights and unimplemented complexity optimization.',
        12:'Reported software/data identities and anonymous artifact lead; licenses are author-reported, not independent rights approval.',
        13:'Shared data and algorithm principles correlate votes; the printed probability-approaches-infinity phrase cannot be adopted literally.',
        14:'Empirical correctness and disagreement experiments; adaptive query selection makes a universal linearity claim unsupported here.',
        15:'Helper-function semantics and separate random-network hyperparameter selection.',
        16:'gpt-5-nano-2025-08-07, caching across seeds/sample sizes, two argument orders, consistency fallback; five clean networks after two exclusions.',
        17:'Algorithm1: rejected acceptConnection calls do not reach q increment; no terminal exhausted-budget orientation fallback. Reported43.9% Property existence accuracy violates competence assumption.',
        18:'Table8 mean orientation93.3% and existence66.4%; Property83.9%/43.9%,Alarm82.8%/52.2%;Table9 comparisons are network-specific.',
        19:'Exact prompts ask about plausible direct or indirect relationships, with causal-order assumptions.',
        20:'Extra Alarm prompt restrictions and network recall probe; near reconstruction of Asia supports a memorization concern.',
        21:'Other recall probes, threshold discussion and indirect/direct comparison; failed recall does not prove absence of contamination.',
        22:'Direct-edge expert comparisons are empirical; greedy cycles and budgets prevent a general recall-invariance inference.',
        24:'Full cost categories and excluded outputs from timeouts, memory limits and comparator exceptions; imputation sensitivity is described.'}
    inspected=[]
    for page,finding in anchors.items():
        p=BASE/f'expert-page-{page}.txt'
        with p.open('x') as f:f.write(pages[page-1])
        inspected.append(dict(anchor=f'Physical PDF page {page}',finding=finding,extracted_text=ref(p,'Inspected primary text')))
    write(BASE/'version-selection.json',dict(candidate='LA01-candidate-149',selected='arXiv:2601.16715v2',
        selected_date='2026-05-07T12:30:55Z',earlier_date='2026-01-23T13:01:30Z',cutoff='2026-10-07',
        metadata_title='Dynamic Expert-Guided Model Averaging for Causal Discovery',title_page_title=title,
        reconciliation='Hyphenated Model-Averaging on selected title page; author list and arXiv identity agree.',
        evidence=[ref(identity,'Identity/history only'),ref(RAW/'exec20_expert149_v1.pdf','Preserved earlier genuine original'),ref(pdf,'Selected v2')]))
    claims=['The paper proposes greedy graph aggregation using equal adjacency counts, separate direction thresholds and selective expert requests.',
            'Expert answers concern plausible causal paths; a true indirect path is not a direct edge.',
            'Experiments use seven synthetic categorical networks and simulated expert correctness; hyperparameters are selected on separate generated networks.',
            'A five-clean-network LLM case study uses a named model snapshot and cached answers across seeds/sample sizes.',
            'The paper reports mean orientation/existence accuracy93.3%/66.4% but Property existence43.9% and Alarm52.2%; these are paper reports, not our measurements.',
            'The authors state no formal recovery guarantee and no empirical continuous/mixed-data qualification.']
    source=dict(integrated_citation_key='exec20_expert_averaging',kind='paper',title=title,filename_title=title,
        first_author='Tench',author='Tench, Adrick and Demeester, Thomas',year=2026,source_identity='arXiv:2601.16715v2',
        version_date='7 May2026,12:30:55UTC; v2',cutoff='2026-10-07',local_copy=ref(pdf,'Genuine selected original'),
        local_path=str(pdf.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest(),inspected_anchors=inspected,
        supported_claims=claims,limitations=LIMITS,identity_evidence=[ref(BASE/'version-selection.json','Version/title reconciliation'),
            ref(RAW/'exec20_expert149_v2.receipt.json','Acquisition receipt')])
    authored=dict(integrated_citation_key='exec20_expert_averaging_reference',kind='project_derivation',
        title='Exact graph-voting, query-budget and intervention-equivalence witnesses',author='Causal banking proposal project',year=2026,
        source_identity='tools/expert_averaging_reference_20261020.py',version_date='20 October2026',
        local_copy=ref(ROOT/'tools/expert_averaging_reference_20261020.py','Exact authored reference'),
        inspected_anchors=[ref(BASE/'exact-results.json','All exact calculations')],
        supported_claims=['Eleven independent3/4-correct votes give1012581/1048576 majority correctness; identical votes retain3/4.',
            'Three DAGs can each support two edges while every edge of a directed3-cycle obtains2/3 votes.',
            'A literal printed trace makes three rejected calls with budget1 and counter0; exhausted orientation may remain unassigned.',
            'Two zero-mean Gaussian structural models share covariance but have intervention effects3/5 and0.',
            'With assumed value100 and cost40, compatible margins20 and-40 differ from an unjustified9/10-weighted margin14.'],
        limitations=exact.calculate()['limitations'])
    write(BASE/'source-audit.json',dict(sources=[source,authored],cutoff='2026-10-07',scope='Selected primary paper and exact project witnesses'))
    critical=['Equal algorithm votes are not Bayesian posterior probabilities, independent replications, or graph/effect confidence regions.',
        'Read the printed Algorithm1 literally: existence rejection escapes the counter increment and exhausted orientation lacks the prose fallback. Native behavior is unknown.',
        'Acyclic output does not establish valid latent endpoints, compatibility with every input equivalence class or causal truth.',
        'The five-network LLM appendix is real reported model evidence; cached repeats do not create20 fresh expert realizations.',
        'Selected/excluded networks and model-specific prompts limit transfer. Failed full-network recall does not prove no memorization.',
        'A high average expert accuracy does not ensure accuracy on adaptively selected difficult edges or on each domain.',
        'Do not inherit the probability-approaches-infinity typo, universal linearity of adaptive F1 with expert accuracy, or general recall invariance.',
        'Package names and author-reported licenses are discovery leads; immutable code, complete rights and runtime semantics require separate inspection.']
    omissions=[('Native specification','Obtain immutable source, license, environment and tests; resolve rejected-call counting, majority fallback, ties, cycles and PAG endpoint conversion.'),
        ('Expert cost','Account for both argument orders, retries, invalid responses and cache reuse; record per-request physical calls separately from logical queries.'),
        ('Calibration','Evaluate correctness on the actual selected queries with withheld mechanisms, adverse expert errors and independent truth; no universal graph guarantee.'),
        ('Public experiment','Compare graphs, identified effect sets and full decision losses using generated mechanisms/public scenarios; retain all missing outputs.'),
        ('Coverage','Continue60 unread originals plus complementary searches and citation chaining; preserve14 tasks and4 crosscutting obligations.'),
        ('Visual and final acceptance','Fresh rendered review, Q1/Q5 and mandatory repair completeness remain open.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[dict(item=k,status='open',next_action=v) for k,v in omissions]))
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=claims,source_critical_qualifications=critical,evidence=[ref(BASE/n,'Reviewed primary evidence') for n in
            ['source-audit.json','version-selection.json','exact-results.json','omissions-register.json']],limitations=LIMITS,
        native_execution=False,visual_acceptance=False,coverage_acceptance=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    item=next(i for i in new['items'] if i['id']=='LA01-candidate-149');assert item['disposition']=='open_original_not_inspected'
    item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
        source_key='exec20_expert_averaging',primary_source_record=source,later_primary_review=ref(BASE/'primary-review.json','Primary review'),
        availability='Genuine May2026 v2 acquired; method, real-LLM appendix, adverse cases and limitations inspected.',
        effect_on_claims='Candidate proposal design for discovery assistance; graph identification, native semantics and bank transfer remain unqualified.',
        next_action='Integrate the source-critical discovery argument; obtain pinned code before proposing execution or reuse.')
    assert len(new['items'])==117 and all(a==b for a,b in zip(old['items'],new['items']) if a['id']!='LA01-candidate-149')
    counts=Counter(i['disposition'] for i in new['items']);assert counts['inspected_primary_retained_with_limits']==53 and counts['open_original_not_inspected']==60
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved52/61 census'),
        changes=['Candidate149 receives bounded primary review;116 other records unchanged.'],evidence=[ref(BASE/'primary-review.json','Primary review')],
        closure=False,interpretation='53/113 originals inspected;60 unread. Four crosscutting obligations remain separate.')
    write(BASE/'census-register.json',new)
    tasks=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(tasks['task_families'])==14
    for task in tasks['task_families']:
        if 'LA01-candidate-149' in task['inherited_ids']:
            task['uninspected_candidate_ids'].remove('LA01-candidate-149');task['inspected_candidate_ids'].append('LA01-candidate-149')
            task['inspected_source_keys'].append('exec20_expert_averaging')
        task['coverage_acceptance']=False
    tasks.update(register=ref(BASE/'census-register.json','Current53/60 census'),supersedes=ref(PRIOR/'task-map.json','Preserved task mapping'))
    tasks.setdefault('primary_application_notes',{}).update(expert_evidence='Keep ancestry and adjacency questions separate; audit expert accuracy on selected queries and all physical calls.',
        iid_discovery='Graph voting supports candidate generation, not identified effects or calibrated graph probabilities; preserve equivalence and latent endpoints.')
    write(BASE/'task-map.json',tasks)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=['LA01-candidate-149'],unchanged_other_records=116,
        original_candidates=113,inspected=53,unread=60,task_families=14,coverage_acceptance=False,
        evidence=[ref(BASE/'census-register.json','Preserving census'),ref(BASE/'task-map.json','Preserving task map')]))
    write(BASE/'review.json',dict(status='pass_for_bounded_primary_review',limitations=LIMITS,coverage_acceptance=False,
        evidence=[ref(BASE/'primary-review.json','Source-critical inspection'),ref(BASE/'reconciliation-review.json','Census conservation')]))
    write(BASE/'inspection-progress.json',dict(finding='Candidate149 May2026 v2 reviewed, including cached LLM appendix and printed budget/fallback discrepancies; census53/60.',
        next_action='Integrate expert-guided discovery, preserve source and exact calculation limits, build reader and sponsor successors, then continue other eligible work.',
        evidence=[ref(BASE/n,'Completed bounded review') for n in ['source-audit.json','review.json','census-register.json','task-map.json']]))
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(inspected=53,unread=60,sources=2,coverage_acceptance=False)))


if __name__=='__main__':main()
