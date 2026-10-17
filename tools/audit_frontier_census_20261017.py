#!/usr/bin/env python3
"""Bind three recovered originals and reconcile the still-incomplete census."""
import copy
from collections import Counter
import json
from pathlib import Path
import frontier_census_exact_20261017 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-17/census-recovery'
OUT=BASE/'tranche-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-17/s9/publication-v4/reader/source-audit.json'
LIMITS=['Bounded original-text review; no model calls, upstream runtime, bank experiment or measured ROI.',
        'The inherited113-candidate corpus remains incomplete; complementary searches and additional citation leads remain open.',
        'No complete dependency, code, data or model reuse permission review is supplied.',
        'Rendered visual acceptance remains false under the inherited exhausted image allowance.']

PAPERS=[dict(number=137,key='exec17_frontier_chang',first='Chang',
 title='Diagnosing and Mitigating Sycophancy and Skepticism in LLM Causal Judgment',
 filename_title='Diagnosing and Mitigating Sycophancy and Skepticism in LLM Causal Judgment',author='Edward Y. Chang',
 url='https://aclanthology.org/2026.findings-acl.427.pdf',
 version='ACL Findings2026, pages8769–8789; conference July2–7,2026; retrieved2026-10-17',
 pages={1:'Title, author, venue, dates and gold-label-free judge.',
 4:'Judge checks schema, internal consistency, trace-output entailment and hint non-dominance; consistent incorrect reasoning can pass.',
 6:'454 cases; L2 binary VALID/FLAWED versus three-label L3; historical calls through January2026. L1 N50 per-class/N100 overall conflicts with Table7.',
 8:'Table4 is binary L2; switching an incorrect label equals correction in that two-label setting. Source-reported rounded initial/final accuracies and bad/good flips.',
 10:'Subjectivity, protocol dependence, black-box attribution, absent component ablation and non-certification limitations.',
 13:'Table7 totals L1=50,L2=304,L3=100. Confounding vignette labels causal claim NO and describes association as spurious.'},
 claims=['RCA checks consistency without a gold scientific oracle; this does not certify a true causal model.',
 'Binary Table4 transitions are distinct from a generalized three-label correction metric.',
 'The L1 denominator inconsistency prevents defensible pooled reconstruction without further evidence.'],
 limits=['The recovery summary suggested a three-label flaw in Table4; reinspection resolves Table4 as binary L2. Do not attribute the authored multiclass failure to that table.',
 'Do not infer zero treatment effect merely from the vignette identifying confounding; label NO can instead mean an unsupported causal assertion.',
 'Historical model findings are protocol-specific reported results, not current model rankings.'],
 tasks=['business_translation','expert_evidence','identification','evaluation_cost']),
 dict(number=242,key='exec17_frontier_yang',first='Yang',
 title='OrcheCause Agent: From Textual Knowledge to End-to-End Causal Inference',
 filename_title='OrcheCause Agent From Textual Knowledge to End-to-End Causal Inference',
 author='Jinseok Yang and Jung-Hee Kim and Juhyun Lyu and Soonyoung Lee and Woohyung Lim',
 url='https://ojs.aaai.org/index.php/AAAI/article/download/42397/46358',
 version='AAAI26, pages41733–41735; saved discovery metadata2026-03-14; inspected proceedings PDF2026; retrieved2026-10-17',
 pages={1:'Title, authors and four-module architecture; citations to Causal-Copilot and Le et al.',
 2:'User text as hard constraints and external database text as soft constraints; preprocessing, BIC tuning, library names, Table1 and future work.',
 3:'Primary reference list identifies Le2024 and Causal-Copilot2025; citation identity does not substitute for original inspection.'},
 claims=['Reported orchestration spans discovery, structural models, root-cause attribution and effect estimation.',
 'Sachs SHD21→23 worsens under HPO alone although F1 .323→.343 improves; later knowledge-assisted settings have lower SHD.',
 'The demonstrations use ALARM and Sachs, with domain knowledge taken from their original papers; temporal and high-dimensional robustness are future work.'],
 limits=['No independent execution, statistical uncertainty, held-out bank comparison or complete code/license audit.',
 'BIC is an observed-fit criterion; a favorable score does not by itself resolve intervention direction.',
 'Exact publication day is metadata-derived; the inspected PDF confirms proceedings year rather than an independently verified day.'],
 tasks=['business_translation','diagram_construction','iid_discovery','identification','agent_architecture','evaluation_cost']),
 dict(number=31,key='exec17_frontier_liu',first='Liu',
 title='An AI Agent for Automated Causal Inference in Epidemiology',
 filename_title='An AI Agent for Automated Causal Inference in Epidemiology',
 author='Haochen Liu and Ke Shi and Ang Li and Xinyu Li and Jiali Chu and Yingqian Xue and Sihui Cen and Yuting Wang and Tianxiao Zhang',
 url='https://www.medrxiv.org/content/medrxiv/early/2026/02/06/2026.02.06.26345723.full.pdf',
 version='medRxiv DOI10.64898/2026.02.06.26345723; posted February6,2026; not peer reviewed; retrieved2026-10-17',
 pages={1:'Title, authors, preprint status, date and rights notice.',
 7:'Regex association/causal extraction, heuristic directions, Hill criteria and topology-based exposure/outcome labels; acyclicity check.',
 9:'Functional demonstrations and described testing; no calibrated causal-effect coverage study established by this passage.',
 11:'Usability12 participants in two groups of6; average task initiation within2 rounds, not identification validation.',
 12:'Illustrative literature-to-causal conclusion workflow; observational evidence needs explicit assumptions rather than automatic causal promotion.',
 17:'Systematic expert review, real-world functional validation, larger user tests and comparisons with manual analysis listed as future work.',
 18:'Future open-source release after initial validation; current runtime and software reuse permission not established.'},
 claims=['EpiCausalX describes retrieval, heuristic relationship extraction and interactive diagrams.',
 'Graph-root/sink typing is a source heuristic and not a general definition of exposure and outcome.',
 'Usability evidence and future validation plans must be separated from causal identification or confidence-interval performance.'],
 limits=['Original is a non-peer-reviewed preprint; no present open-source release established by its future-tense statement.',
 'PDF states all rights reserved/no reuse without permission; a local research copy is not evidence of software/data integration permission.',
 'No health-effect assertion is adopted from the demonstration.'],
 tasks=['business_translation','variable_ontology','diagram_construction','identification','estimation_validation','agent_architecture'])]

def read(p):return json.loads(p.read_text())

def main():
    recovery=read(OUT/'recovery.json');sources=[]
    for p in PAPERS:
        n=p['number'];row=next(r for r in recovery['papers'] if r['candidate']==n)
        pdf=ROOT/row['path'];assert pdf.name==p['filename_title']+' '+p['first']+'(2026).pdf'
        assert ref(pdf,'original')['sha256']==row['sha256']
        pages=(BASE/f'candidate{n}.txt').read_text().split(chr(12));anchors=[]
        for page,finding in p['pages'].items():
            dest=OUT/f'candidate{n}-page-{page}.txt';assert not dest.exists();dest.write_text(pages[page-1])
            anchors.append(dict(anchor=f'Physical PDF page{page}',finding=finding,extracted_text=ref(dest,'Inspected primary page')))
        source=dict(integrated_citation_key=p['key'],kind='paper',title=p['title'],filename_title=p['filename_title'],
            first_author=p['first'],author=p['author'],year=2026,source_identity=p['url'],version_date=p['version'],
            cutoff='2026-10-07',retrieved_date='2026-10-17',local_copy=ref(pdf,'Authentic original, exact retrieved bytes'),
            local_path=str(pdf.relative_to(ROOT)),sha256=row['sha256'],inspected_anchors=anchors,supported_claims=p['claims'],
            related_primary_bytes=[ref(BASE/f'candidate{n}-elevated.response','Genuine public PDF response'),
                ref(BASE/f'candidate{n}-elevated.headers','Successful bounded public retrieval headers')],
            candidate_id=f'LA01-candidate-{n}',limitations=LIMITS+p['limits'])
        verify_bindings(source);sources.append(source)
    write(OUT/'exact-results.json',exact.serial(exact.calculate()))
    sources.append(dict(integrated_citation_key='exec17_frontier_exact',kind='project_derivation',
        title='Answer-transition and equal-observation causal judgment counterexamples',author='Causal banking proposal',year=2026,
        source_identity='Project-authored finite transition and structural threshold laws',version_date='2026-10-17',
        local_copy=ref(OUT/'exact-results.json','Exact laws with independent finite enumeration'),
        inspected_anchors=['Three-label transition identity','Binary published-table rounding check','Three positive observationally equal confounded models'],
        supported_claims=['Wrong-label switching need not correct a multiclass answer.',
                          'Confounding and a positive observed association permit positive, zero and negative intervention effects in the authored examples.',
                          'Stipulated USD100 outcome value and USD5 action cost give netUSD5,-5,-15 in those three worlds.'],
        records=[ref(ROOT/'tools/frontier_census_exact_20261017.py','Exact Fraction calculations and separate threshold enumeration')],limitations=LIMITS))
    write(OUT/'source-audit.json',dict(cutoff='2026-10-07',sources=sources,prior=ref(PRIOR,'731 preserved records')))
    write(OUT/'primary-review.json',dict(status='pass',issues=[],reviewer=dict(name='Codex author/coordinator',kind='author'),
        sources=sources[:3],source_correction='Table4 is binary L2; the multiclass concern is a prospective extension, not a demonstrated source defect.',
        unresolved_source_issue='Chang L1 N100 in narrative versus50 in Table7; no fabricated denominator reconciliation.',
        evidence=[ref(OUT/'source-audit.json','Three primary and one authored record'),ref(OUT/'exact-results.json','Reproducible examples')],
        final_acceptance=False,visual_acceptance=False))
    prior=read(BASE/'census-register.json');rows=copy.deepcopy(prior['items']);byid={r['id']:r for r in rows};changes=[]
    for p,s in zip(PAPERS,sources):
        r=byid[s['candidate_id']];assert r['technical_source_review_open']
        changes.append(dict(id=r['id'],prior_disposition=r['disposition'],source_key=p['key']))
        r.update(prior_disposition=r['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
            source_key=p['key'],primary_source_record=s,later_primary_review=ref(OUT/'primary-review.json','Inspected original '+r['id']),
            availability='Genuine original acquired and inspected; retrieved response and failed routes retained.',
            task_families=p['tasks'],mapping_basis='Primary text inspected; methodological limits do not establish successful capability.',
            effect_on_claims='Only audited original claims with listed limitations are retained.',
            next_action='Keep unresolved scientific, version, rights and evaluation limits; do not treat source inspection as capability qualification.')
    counts=dict(Counter(r['disposition'] for r in rows));assert len(rows)==117 and counts['inspected_primary_retained_with_limits']==35 and counts['open_original_not_inspected']==78
    write(OUT/'census-register.json',dict(status='incomplete_reconciled_primary_dispositions',cutoff='2026-10-07',counts=counts,items=rows,
        supersedes=ref(BASE/'census-register.json','Preserved32-inspected81-unread checkpoint'),changes=changes,closure=False,
        interpretation='35/113 inherited candidate originals inspected;78 unread;4 cross-cutting records. New citation leads are separate and remain open.'))
    tasks=[]
    for previous in read(BASE/'task-map.json')['task_families']:
        t=copy.deepcopy(previous);ids={r['id'] for r in rows if t['id'] in r.get('task_families',[])}
        t['inherited_ids']=sorted(ids)
        t['uninspected_candidate_ids']=[r['id'] for r in rows if r['id'] in ids and r['disposition']=='open_original_not_inspected']
        t['inspected_candidate_ids']=[r['id'] for r in rows if r['id'] in ids and r['disposition']=='inspected_primary_retained_with_limits']
        t['inspected_source_keys']=sorted(set(t.get('inspected_source_keys',[]))|{r['source_key'] for r in rows if r['id'] in ids and 'source_key' in r})
        t['coverage_acceptance']=False;tasks.append(t)
    assert len(tasks)==14
    write(OUT/'task-map.json',dict(task_families=tasks,register=ref(OUT/'census-register.json','Successor117-item corpus'),
        mapping_does_not_establish_depth_or_completeness=True))
    write(OUT/'citation-chains.json',dict(cutoff='2026-10-07',chains=[
        dict(from_key='exec17_frontier_yang',anchor='Physical page3 references',to_key='v12_la_2407_15073',
             disposition='Existing inspected original; reuse exact prior record, no new acquisition',evidence=ref(PRIOR,'Existing Le2024 source record')),
        dict(from_key='exec17_frontier_yang',anchor='Physical page3 references',title='Causal-Copilot: An Autonomous Causal Analysis Agent',
             authors='Wang et al.',year=2025,disposition='Additional uninspected citation lead outside the inherited113 candidates',
             next_action='Resolve original report identity/version and acquire genuine primary text before technical claims.')],
        exhaustive_search=False))
    write(OUT/'search-observations.json',dict(status='incomplete',cutoff='2026-10-07',
        attempted_queries=[p['title'] for p in PAPERS],provider_result='Built-in search returned no visible source results.',
        counted_as_coverage=False,acquisition_basis='Saved primary URL leads; actual successful original bytes and headers are bound.',
        remaining=['Candidate27 primary original','Complementary longitudinal and off-policy searches','Negative-result search','Causal-Copilot citation lead','78 inherited unread originals']))
    print(json.dumps(dict(source_records=4,inspected_candidates=35,unread_candidates=78,task_families=14,closure=False)))

if __name__=='__main__':main()
