#!/usr/bin/env python3
"""Audit two genuine benchmark originals and preserve an incomplete successor census."""
import copy
from collections import Counter
from html import unescape
import json
from pathlib import Path
import re
import subprocess

import benchmark_reference_20261017 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ROOT/'docs/program/execution/2026-10-17/census-recovery'
BASE = RECOVERY/'benchmark-v1'
PRIOR = RECOVERY/'tranche-v1'
AUDIT = PRIOR/'publication-v2/reader/source-audit.json'
LIMITS = [
    'Author primary-text review only; no upstream engine, model call, banking experiment or measured ROI.',
    'The inherited candidate census and complementary literature search remain incomplete.',
    'Paper availability does not establish code, dataset, dependency or deployment rights.',
    'No exclusive substantive-depth or final proposal acceptance awarded.',
    'Visual acceptance remains false under the inherited exhausted image allowance.']

PAPERS = [dict(number=116, key='exec17_benchmark_cello', first='Chen', year=2024,
    title='CELLO: Causal Evaluation of Large Vision-Language Models',
    filename_title='CELLO Causal Evaluation of Large Vision-Language Models',
    author='Meiqi Chen and Bo Peng and Yan Zhang and Chaochao Lu',
    name='cello-final', url='https://aclanthology.org/2024.emnlp-main.1247.pdf',
    doi='10.18653/v1/2024.emnlp-main.1247',
    sha='92edd9dbac95c72e38b85e1885e49972a4e87299ba5fe5bb083ff5ea92127c2c',
    version='EMNLP2024 proceedings, pages22353–22377; published2024; retrieved2026-10-17',
    pages={1:'Title, authors, venue identity and project URL; identity checked against the published original.',
        4:'Visual Genome relation annotations, graph templates and subgraph matching generate the stipulated scene graphs.',
        5:'LLM-generated questions and distractors; original binary questions have nearly equal Yes/No distribution.',
        6:'Four-step CELLO-CoT; experimental test set is1200 questions,100 randomly selected per task.',
        7:'Table2 twelve task accuracies, task averages and ALL; GPT-4o reported ALL .59→.70 and confounder identification .29→.35.',
        8:'Section6.4 reformulated robustness questions always have correct answer No; correct refusals may cite model inability to act rather than the scene mechanism.',
        9:'Limitations: original annotation quality, unclear images and static-image versus dynamic-reasoning boundaries.',
        14:'AppendixB.2 two annotators,120 instances,10/task;91.7% valid and reported Cohen kappa84.1%.',
        15:'Table5 robustness: Qwen-VL .04,BakLlava .03,GPT-4o .57; task differs from the original causal questions.'},
    claims=['A scene-template benchmark tests response consistency against constructed labels, not experimentally established intervention effects.',
        'The all-No robustness label distribution permits a constant-No perfect classifier; original binary task balance is a separate property.',
        'The twelve displayed GPT-4o+CELLO-CoT task accuracies average .6875 under equal100/task, whereas ALL is .70; conventional rounding does not reconcile that interpretation.',
        'Historical author-reported performance and question-validity annotations do not establish present bank accuracy or causal truth.'],
    issues=['Equal-task/ALL aggregation discrepancy remains unresolved in the published original; no raw result reconstruction or cause is asserted.'],
    tasks=['expert_evidence','diagram_construction','iid_discovery','evaluation_cost']),
    dict(number=113, key='exec17_benchmark_cherif', first='Cherif', year=2026,
    title='CausalReasonBench: A Comprehensive Benchmark for Evaluating Causal Reasoning Capabilities of Large Language Models',
    filename_title='CausalReasonBench A Comprehensive Benchmark for Evaluating Causal Reasoning Capabilities of Large Language Models',
    author='Ahmed Cherif', name='causalreasonbench',
    url='https://www.researchsquare.com/article/rs-9181514/v1.pdf',
    doi='10.21203/rs.3.rs-9181514/v1',
    sha='47f002bb835b9996ef2de386a5d12145cb1a1301345591f96e4120bc88adcf7b',
    version='Research Square v1; cover posted2026-04-13, CC-BY4.0; retrieved2026-10-17; preprint, no independent peer-review acceptance established',
    pages={1:'Title, author, DOI, posted date and paper CC-BY4.0 notice.',
        11:'Table2 states12 scenarios, four domains, three difficulties, four tasks, four strategies and two replicates.',
        12:'Illustrative minimum-wage, antibiotic and post-deployment latency scenarios; mechanism assumptions need explicit separation from observational identification.',
        13:'Four causal task types and prompting strategies repeat the underlying scenario grid.',
        14:'Equations1–3 set-overlap CIR, epsilon1e-8, forward/ambiguous/reverse CLP categories.',
        15:'Equations4–5 CCR=CIR outside counterfactual tasks; CAR weights .40/.35/.25; author-defined gold annotation.',
        16:'Three Groq-hosted model identifiers; mostlytemperature0,contrast-case first pass .1.',
        17:'1152 total responses; seed42 where supported; Mann–Whitney and bootstrap descriptions; whitespace/stemming/regex implementation; public-release assertion.',
        30:'Automatic-metric limitations and incomplete human validation.',
        31:'Author gold, small scenario/model coverage, contamination and construct validity limitations.',
        33:'Data Availability Statement says benchmark data, code, gold and raw results are available on reasonable request.',
        34:'Appendix minimum-wage gold structure explicitly notes empirical debate; this is a stipulated mechanism, not a universally identified effect.',
        39:'AppendixB.5 historical zero monetary API charge and about18h rate-limited runtime; not total workflow economics.',
        42:'AppendixD.1 selects .40/.35/.25 weights among15 combinations on24 responses rated by two experts; selected Kendall tau .78.'},
    claims=['The reported1152 outputs repeat12 underlying scenarios; repeated strategies/tasks/models are not1152 independent mechanisms.',
        'Non-counterfactual CAR algebraically reduces to .65CIR+.35CLP.',
        'Set-overlap CIR ignores token order; paper CLP is a separate directional check and no uninspected regex exploit is claimed.',
        'The selected pilot correlation is selection-set agreement, not held-out metric validation.',
        'The paper contains conflicting public-release/on-request availability statements; no public code/data copy or upstream reproduction is established.',
        'Historical free-tier API charge does not price annotation, review, waiting or current inference.' ],
    issues=['Public-release assertions conflict with the on-request Data Availability Statement; executable code/gold/raw results remain uninspected.',
        'The exact response pairing and resampling unit are not established by the inspected methods; do not reconstruct source confidence intervals.',
        'Textbook or author-stipulated gold does not supply general bank causal identification.'],
    tasks=['business_translation','identification','estimation_validation','evaluation_cost'])]


def read(path):
    return json.loads(path.read_text())


def prepare():
    assert not BASE.exists()
    BASE.mkdir()
    acquisition = RECOVERY/'benchmark-acquisition'
    sources = []
    for paper in PAPERS:
        original = acquisition/(paper['name']+'.pdf')
        assert ref(original, 'original')['sha256'] == paper['sha']
        dest = ROOT/'docs/papers'/(paper['filename_title']+' '+paper['first']+f"({paper['year']}).pdf")
        assert not dest.exists()
        dest.write_bytes(original.read_bytes())
        text = BASE/(paper['name']+'-full.txt')
        subprocess.run(['pdftotext','-layout',str(dest),str(text)],check=True,timeout=20)
        pages = text.read_text().split(chr(12))
        anchors = []
        for page, finding in paper['pages'].items():
            excerpt = BASE/f"candidate{paper['number']}-page-{page}.txt"
            excerpt.write_text(pages[page-1])
            anchors.append(dict(anchor=f'Physical PDF page{page}',finding=finding,
                extracted_text=ref(excerpt,'Inspected genuine primary page')))
        source = dict(integrated_citation_key=paper['key'],kind='paper',title=paper['title'],
            filename_title=paper['filename_title'],first_author=paper['first'],author=paper['author'],year=paper['year'],
            source_identity=paper['url'],doi=paper['doi'],version_date=paper['version'],
            cutoff='2026-10-07',retrieved_date='2026-10-17',local_copy=ref(dest,'Authentic original; exact retrieved version'),
            local_path=str(dest.relative_to(ROOT)),sha256=paper['sha'],inspected_anchors=anchors,
            supported_claims=paper['claims'],candidate_id=f"LA01-candidate-{paper['number']}",
            related_primary_bytes=[ref(original,'Preserved genuine retrieval'),
                ref(acquisition/(paper['name']+'-retrieval.json'),'Retrieval identity, failures and hashes'),
                ref(acquisition/(paper['name']+'-elevated.headers'),'Successful public HTTPS retrieval headers')],
            unresolved_source_issues=paper['issues'],limitations=LIMITS)
        if paper['number']==116:
            source['earlier_version']=ref(ROOT/'docs/literature/raw/exec17_census_search2_paper_cello.pdf',
                'Earlier arXiv2406.19131v1; not substituted for published original')
        verify_bindings(source)
        sources.append(source)
    write(BASE/'exact-results.json',exact.serial(exact.calculate()))
    sources.append(dict(integrated_citation_key='exec17_benchmark_exact',kind='project_derivation',
        title='Benchmark aggregation, token-set, loss and mechanism-clustering reference',
        author='Causal banking proposal',year=2026,source_identity='Project-authored exact deductions and stipulated banking laws',
        version_date='2026-10-17',local_copy=ref(BASE/'exact-results.json','Exact Fraction results and independent enumerations'),
        inspected_anchors=['Equal-task rounding envelopes and integer denominator',
            'Confusion-count monetary example and constant-answer baselines',
            'Set-overlap invariance and non-counterfactual score reduction',
            'Common-mechanism covariance count'],
        supported_claims=['The displayed table values have disjoint conventional-rounding envelopes under equal-task aggregation.',
            'Higher accuracy can give lower monetary value under the stipulated20/80 payoff.',
            'Eight within-mechanism paired variants give design effect4.5 in the specified random-effects example.'],
        records=[ref(ROOT/'tools/benchmark_reference_20261017.py','Exact formulas and separate enumeration')],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=sources,prior=ref(AUDIT,'735 preserved records')))
    write(BASE/'primary-review.json',dict(status='pass',issues=[],scope='Primary identity and bounded supported-claim review',
        reviewer=dict(name='Codex author/coordinator',kind='author'),sources=sources[:2],
        unresolved_source_issues=[dict(candidate=p['number'],issues=p['issues']) for p in PAPERS],
        interpretation='Source issues are explicitly retained and bound; no unresolved source claim is promoted to a verified experimental result.',
        evidence=[ref(BASE/'source-audit.json','Two genuine originals and exact reference'),
            ref(BASE/'exact-results.json','Reviewed exact deductions'),ref(RECOVERY/'benchmark-plan.md','Reviewed continuation plan')],
        final_acceptance=False,visual_acceptance=False))
    rows=copy.deepcopy(read(PRIOR/'census-register.json')['items'])
    by_id={r['id']:r for r in rows}
    changes=[]
    for p,s in zip(PAPERS,sources):
        row=by_id[s['candidate_id']]
        assert row['disposition']=='open_original_not_inspected'
        changes.append(dict(id=row['id'],previous_disposition=row['disposition'],source_key=p['key']))
        row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',
            technical_source_review_open=False,source_key=p['key'],primary_source_record=s,
            later_primary_review=ref(BASE/'primary-review.json','Inspected original '+row['id']),
            availability='Genuine exact-version PDF acquired and inspected; source experimental/code limitations retained.',
            task_families=p['tasks'],mapping_basis='Inspected primary text, not title or abstract alone.',
            effect_on_claims='Only the audited bounded claims may be used; no implementation or comparative bank merit established.',
            next_action='Retain stated source discrepancies and qualify executable artifacts independently if obtained.')
    counts=dict(Counter(r['disposition'] for r in rows))
    assert len(rows)==117 and counts['inspected_primary_retained_with_limits']==37 and counts['open_original_not_inspected']==76
    write(BASE/'census-register.json',dict(status='incomplete_reconciled_primary_dispositions',cutoff='2026-10-07',
        counts=counts,items=rows,supersedes=ref(PRIOR/'census-register.json','35-inspected78-unread predecessor'),
        changes=changes,closure=False,
        interpretation='37/113 inherited original candidates inspected;76 unread;4 cross-cutting records. Additional citation leads tracked separately.'))
    tasks=[]
    for previous in read(PRIOR/'task-map.json')['task_families']:
        task=copy.deepcopy(previous)
        ids={r['id'] for r in rows if task['id'] in r.get('task_families',[])}
        task['inherited_ids']=sorted(ids)
        for disposition,field in [('open_original_not_inspected','uninspected_candidate_ids'),
                                  ('inspected_primary_retained_with_limits','inspected_candidate_ids')]:
            task[field]=[r['id'] for r in rows if r['id'] in ids and r['disposition']==disposition]
        task['inspected_source_keys']=sorted(set(task.get('inspected_source_keys',[]))|
            {r['source_key'] for r in rows if r['id'] in ids and 'source_key' in r})
        task['coverage_acceptance']=False
        tasks.append(task)
    write(BASE/'task-map.json',dict(task_families=tasks,register=ref(BASE/'census-register.json','Successor117-item corpus'),
        mapping_does_not_establish_depth_or_completeness=True))
    write(BASE/'census-progress.json',dict(
        finding='Two genuine benchmark originals inspected and retained with explicit aggregation, label, metric, sampling and availability limits. Census37 inspected/76 unread; no closure.',
        next_action='Integrate the reviewed benchmark comparison and exact banking evaluation reference into a preserving successor. Continue resolved Causal-Copilot primary acquisition independently; candidate27 and complementary search remain open.',
        evidence=[ref(p,'Reviewed progress') for p in [BASE/'primary-review.json',BASE/'source-audit.json',
            BASE/'exact-results.json',BASE/'census-register.json',BASE/'task-map.json',Path(__file__)]]))
    print(json.dumps(dict(inspected=37,unread=76,added_sources=3,census_closed=False)))


def search():
    raw=ROOT/'docs/literature/raw'
    prior=RECOVERY/'search-v4'
    html=raw/'exec17_census_search4_copilot_arxiv.html'
    text=html.read_text()
    entries=[]
    for entry in text.split('class="arxiv-result"')[1:]:
        identity=re.search(r'href="https://arxiv.org/abs/([^\"]+)',entry).group(1)
        title=re.search(r'<p class="title is-5 mathjax">(.*?)</p>',entry,re.S).group(1)
        title=unescape(re.sub('<[^>]+>','',title)).strip()
        entries.append(dict(arxiv=identity,title=' '.join(title.split()),technical_support=False))
    hit=next(r for r in entries if r['arxiv']=='2504.13263')
    assert hit['title']=='Causal-Copilot: An Autonomous Causal Analysis Agent'
    observations=dict(cutoff='2026-10-07',searches=[ref(html,'Three actual title-search results'),
        ref(raw/'exec17_census_search4_copilot_openalex.json','Five OpenAlex title-query results; no exact hit')],
        arxiv_results=entries,exact_copilot_identity=hit,
        earlier_failure='Sandbox DNS failures preserved; elevated registered collector returned both responses.',
        coverage='Bounded title queries only, not saturation; metadata and abstracts support identity only.',
        citation_chain=ref(PRIOR/'candidate242-page-3.txt','OrcheCause original reference-list lead'),
        census_closed=False)
    assert not (prior/'search-observations.json').exists()
    write(prior/'search-observations.json',observations)
    out=RECOVERY/'search-v5'
    out.mkdir(exist_ok=False)
    requests=[dict(id='exec17_census_search5_copilot_abs',url='https://arxiv.org/abs/2504.13263',extension='html'),
        dict(id='exec17_census_search5_copilot_v1',url='https://arxiv.org/pdf/2504.13263v1',extension='pdf')]
    manifest=ROOT/'docs/literature/fetch-manifest.json'
    write(out/'previous-fetch-manifest.json',read(manifest))
    write(out/'acquisition-manifest.json',dict(requests=requests,cutoff='2026-10-07',
        evidence=[ref(prior/'search-observations.json','Exact-title identity established without guessing')],
        stopping_rule='Two bounded public original/version reads; inspect PDF title and version history before technical use.',
        technical_support=False))
    write(manifest,dict(requests=requests))
    print(json.dumps(dict(exact_title_identity=hit,new_requests=2)))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','search'])
    {'prepare':prepare,'search':search}[p.parse_args().command]()
