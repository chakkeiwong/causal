#!/usr/bin/env python3
"""Preserving primary inspection and census successor for two acquired originals."""
from collections import Counter
import copy
import json
from pathlib import Path
import subprocess

import framework_evaluation_reference_20261018 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-18/census-frameworks-v1'
PRIOR = ROOT/'docs/program/execution/2026-10-18/census-successor'


def read(path):
    return json.loads(path.read_text())


def main():
    sources = []
    definitions = [
        dict(name='promptbench', raw='exec18_framework_promptbench_v3',
             key='exec18_framework_promptbench', candidate='LA01-candidate-244',
             title='PromptBench: A Unified Library for Evaluation of Large Language Models',
             first='Zhu', author='Zhu, Kaijie and Zhao, Qinlin and Chen, Hao and Wang, Jindong and Xie, Xing',
             year=2024, identity='arXiv:2312.07910v3; Journal of Machine Learning Research25(2024)1–22',
             version='arXiv v3, 20 August 2024; journal header submitted1/24, revised6/24, published8/24; retrieved18 October2026',
             pages=23, anchors={
                 1: 'Actual title, five authors, selected v3 date and CC-BY4.0 paper notice; paper notice is not package licensing.',
                 2: 'Figure1 and Section2 define modular components and research scope; author comparison is a dated paper claim.',
                 3: 'Section2.1: model/data/prompt interfaces, four attack levels, standard/dynamic/semantic protocols;12 tasks and22 datasets are source-reported.',
                 4: 'Section2.2 four-stage evaluation pipeline and explicit Section3 limits: scenario coverage, metric nuance, dataset and prompt quality.',
                 13: 'AppendixA Table1 is the authors\' historical comparison, not an independent current product ranking.',
                 18: 'Prompt types, general prompt-engineering choices and express exclusion of some task-specific methods.',
                 19: 'Attack definitions, Figure2 pipeline and AppendixC.1 qualitative vulnerability finding; no numeric graph values transcribed.',
                 22: 'Printed21: C.2 no prompt method beats baseline on every dataset; C.3 dynamic-evaluation limits; AppendixD dataset/model extension hooks.',
                 23: 'Printed22: AppendixD method registration and custom metric/input/output extension hooks.'},
             claims=[
                 'The paper presents a modular Python evaluation library with customizable datasets, models, prompts, attacks, protocols and metrics.',
                 'Its source-reported results describe adversarial vulnerability, task-dependent prompt-engineering gains and remaining dynamic-evaluation weaknesses.',
                 'Custom evaluation hooks are relevant to a prospective causal-contract evaluator, but the paper does not validate causal targets or supply a qualified integration.'
             ],
             limits=[
                 'Historical source-reported qualitative results, not a local rerun or a current model ranking.',
                 'The selected PDF has23 physical pages; final printed pages21–22 are physical22–23. No visual or numeric-plot acceptance is claimed.',
                 'No pinned repository, distribution, dependency license or adapter was inspected in this tranche. Do not infer package licensing from the paper CC-BY4.0 notice.'
             ]),
        dict(name='agents-survey', raw='exec18_framework_agents_survey_v7',
             key='exec18_framework_agents_survey', candidate='LA01-candidate-19',
             title='A Survey on Large Language Model based Autonomous Agents',
             first='Wang', author='Wang, Lei and Ma, Chen and Feng, Xueyang and Zhang, Zeyu and Yang, Hao and Zhang, Jingsen and Chen, Zhi-Yuan and Tang, Jiakai and Chen, Xu and Lin, Yankai and Zhao, Wayne Xin and Wei, Zhewei and Wen, Ji-Rong',
             year=2025, identity='arXiv:2308.11432v7; DOI10.1007/s11704-024-40231-1',
             version='Selected arXiv v7, 2 March 2025; initial preprint22 August2023; selected PDF header2025,0(0):1–42 with placeholder received/accepted dates; retrieved18 October2026',
             pages=42, anchors={
                 1: 'Actual title,13 authors, v7 date, DOI and2025 header; placeholder issue and received dates retained without inventing journal details.',
                 3: 'Construction, application and evaluation taxonomy; architecture/capability-acquisition distinction.',
                 4: 'Figure2 taxonomy: profile, memory, planning and action; synthesis of prior systems rather than a qualified package.',
                 27: 'Section4.1 subjective human evaluation, population bias, cost and efficiency limitations.',
                 28: 'Section4.2 task success, human similarity and efficiency metrics; protocol/evaluation distinction; model judges discussed without causal validity guarantee.',
                 29: 'Table3 historical task/evaluation map and software-testing protocols; table rows mostly date2022–2023, not a2026 census.',
                 30: 'Benchmark examples and explicit limitation that objective techniques cannot perfectly measure every capability.',
                 31: 'Combined subjective/objective evaluation and beginning of challenge taxonomy; compiling100 relevant works is not a reproducible pre-cutoff saturation certificate.',
                 32: 'Section6.3 prompt robustness across interacting modules; start of hallucination discussion.',
                 33: 'Sections6.4–6.6 hallucination, user-unknown knowledge leakage in simulations and repeated-call efficiency.'},
             claims=[
                 'The survey organizes agent architecture into profile, memory, planning and action, and distinguishes architecture from capability acquisition.',
                 'It separates subjective evaluation from objective metrics, protocols and benchmarks, including efficiency.',
                 'It discusses prompt fragility, hallucination, knowledge boundaries and inference cost as unresolved design challenges.'
             ],
             limits=[
                 'A primary source for the survey authors\' taxonomy and discussion; secondary evidence for each constituent framework or experiment.',
                 'The2025 revision and largely2022–2023 Table3 do not establish search completeness through7 October2026.',
                 'No causal identification theorem, calibrated causal-agent performance, package license or working bank integration is established.'
             ]),
    ]
    for definition in definitions:
        raw = ROOT/'docs/literature/raw'/(definition['raw']+'.pdf')
        receipt = raw.with_suffix('.receipt.json')
        acquisition = read(receipt)
        assert acquisition['status'] == 'saved'
        assert acquisition['sha256'] == ref(raw, 'Authentic acquisition')['sha256']
        target = ROOT/'docs/papers'/(definition['title']+' '+definition['first']+'('+str(definition['year'])+').pdf')
        assert not target.exists()
        target.write_bytes(raw.read_bytes())
        text = BASE/(definition['name']+'-selected.txt')
        pages = text.read_text().replace('\0', '').split('\f')
        assert sum(bool(p.strip()) for p in pages) == definition['pages']
        anchors = []
        for page, finding in definition['anchors'].items():
            extracted = BASE/(definition['name']+'-page-'+str(page)+'.txt')
            assert not extracted.exists()
            extracted.write_text(pages[page-1])
            anchors.append(dict(anchor='Physical PDF page'+str(page), finding=finding,
                extracted_text=ref(extracted, 'Inspected original page; text extraction only')))
        source = dict(integrated_citation_key=definition['key'], kind='paper',
            title=definition['title'], filename_title=definition['title'], first_author=definition['first'],
            author=definition['author'], year=definition['year'], source_identity=definition['identity'],
            version_date=definition['version'], cutoff='2026-10-07',
            local_copy=ref(target, 'Authentic selected original'), local_path=str(target.relative_to(ROOT)),
            sha256=ref(target, 'Authentic original')['sha256'], inspected_anchors=anchors,
            supported_claims=definition['claims'], limitations=definition['limits'],
            identity_evidence=[ref(receipt, 'Actual original acquisition'),
                ref(ROOT/'docs/literature/raw/exec18_framework_arxiv_identity.xml', 'Revision identity; metadata does not establish technical claims')])
        sources.append(source)
    write(BASE/'exact-results.json', exact.calculate())
    sources.append(dict(integrated_citation_key='exec18_framework_reference', kind='project_derivation',
        title='Exact paired-contract evaluation accounting reference', author='Causal banking proposal project', year=2026,
        source_identity='Authored exact rational enumeration; no framework, model or bank observations',
        version_date='18 October2026', local_copy=ref(ROOT/'tools/framework_evaluation_reference_20261018.py', 'Exact calculate function'),
        inspected_anchors=[dict(anchor='calculate(): two systems,20 paired contract families,40 planned requests and two assumed error prices',
            evidence=ref(BASE/'exact-results.json', 'Exact counts and conditional assumed economics'))],
        supported_claims=['All-planned and completion-conditional accuracy can rank differently; stipulated error costs can reverse net value.',
            'Two identical wordings per contract do not produce40 independent sampling units.'],
        limitations=['A project bookkeeping example, not simulated LLM behavior, estimated accuracy, confidence intervals or bank economics.']))
    write(BASE/'source-audit.json', dict(sources=sources, cutoff='2026-10-07', author_review=True,
        independent_review=False, verification='Actual selected PDFs, inspected page texts, authentic receipt hashes and exact authored enumeration'))
    primary = dict(status='pass', reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Two selected originals and exact authored evaluation accounting; no census or package-qualification acceptance',
        evidence=[ref(BASE/'source-audit.json', 'Three bounded source records'),
            ref(BASE/'plan-review.md', 'Reviewed scope, source and cutoff controls'),
            ref(BASE/'exact-results.json', 'Exact arithmetic')],
        source_findings=[dict(candidate=d['candidate'], claims=d['claims'], limitations=d['limits']) for d in definitions],
        checks=dict(actual_pdf_identity=True, selected_revisions_predate_cutoff=True,
            paper_vs_package_rights_distinguished=True, exact_results_reproduced=True,
            causal_validation_inferred=False, new_runtime_integration_inferred=False),
        unresolved=['Historical/model benchmarks need new primary originals and matched protocols for fresh performance claims.',
            'Pinned PromptBench source, transitive rights and environment review precede executable reuse.',
            'The remaining71 original candidates, search specificity/saturation, L1/L6 coverage and later qualification remain open.'],
        visual_acceptance=False)
    verify_bindings(read(BASE/'source-audit.json'))
    write(BASE/'primary-review.json', primary)
    baseline=read(PRIOR/'census-register.json'); successor=copy.deepcopy(baseline)
    by_key={s['integrated_citation_key']:s for s in sources}
    changed={d['candidate']:d for d in definitions}
    for item in successor['items']:
        if item['id'] not in changed:
            continue
        definition=changed[item['id']]
        assert item['disposition']=='open_original_not_inspected'
        item.update(prior_disposition=item['disposition'], disposition='inspected_primary_retained_with_limits',
            technical_source_review_open=False, source_key=definition['key'],
            primary_source_record=by_key[definition['key']],
            later_primary_review=ref(BASE/'primary-review.json', 'Selected original technical anchors and scope limits'),
            availability='Authentic selected pre-cutoff revision acquired and inspected; earlier revision and failed route receipts retained.',
            effect_on_claims='Supports only the explicitly inspected taxonomy, interface design and source-reported qualitative evaluation claims; no causal validation or current coverage closure.',
            next_action='Use bounded source-critical argument; inspect pinned upstream code and rights before executable reuse, and inspect remaining original candidates separately.')
    assert all(a==b for a,b in zip(baseline['items'],successor['items']) if a['id'] not in changed)
    successor['counts']['open_original_not_inspected']-=2
    successor['counts']['inspected_primary_retained_with_limits']+=2
    successor.update(supersedes=ref(PRIOR/'census-register.json','Preserved40-inspected/73-unread baseline'),
        changes=['Only candidate19 and244 receive completed selected-original primary inspections; all other records remain identical.'],
        evidence=[ref(BASE/'primary-review.json','Actual source findings'),ref(BASE/'source-audit.json','Bound source identities')],
        closure=False, interpretation='42/113 original candidates inspected;71 unread. Four cross-cutting records and three citation-chain leads retain their own denominators. No full2026 frontier or framework coverage claim.')
    counts=Counter(i['disposition'] for i in successor['items'])
    assert counts['open_original_not_inspected']==71 and counts['inspected_primary_retained_with_limits']==42
    write(BASE/'census-register.json',successor)
    taskmap=copy.deepcopy(read(PRIOR/'task-map.json'))
    assert len(taskmap['task_families'])==14
    for task in taskmap['task_families']:
        for identifier,definition in changed.items():
            if identifier not in task['inherited_ids']:
                continue
            assert identifier in task['uninspected_candidate_ids']
            task['uninspected_candidate_ids'].remove(identifier)
            task['inspected_candidate_ids'].append(identifier)
            task['inspected_source_keys'].append(definition['key'])
        task['coverage_acceptance']=False
    taskmap.update(register=ref(BASE/'census-register.json','Current preserving42/71 census'),
        supersedes=ref(PRIOR/'task-map.json','Preserved14-family mapping'))
    write(BASE/'task-map.json',taskmap)
    write(BASE/'reconciliation-review.json',dict(status='pass', unchanged_other_records=True,
        changed_ids=sorted(changed), original_candidates=113, inspected=42, unread=71, task_families=14,
        coverage_acceptance=False, evidence=[ref(BASE/'census-register.json','Preserving successor'),ref(BASE/'task-map.json','Reconciled task map'),ref(Path(__file__),'Exact preserving census builder')]))
    write(BASE/'inspection-progress.json',dict(
        finding='Two authentic selected originals inspected: PromptBench v3 and autonomous-agent survey v7. Original census42 inspected/71 unread of113. No complete-frontier, package licensing, live performance or causal validity claim. All other records preserved.',
        next_action='Integrate the bounded framework/evaluation discussion into a preserving working reader, review sources/math/text and renew exact-reader Q2-Q4; reconcile sponsor pairing, then inspect the next unread original or an independent software decision.',
        evidence=[ref(BASE/'census-register.json','Current42/71 census'),ref(BASE/'task-map.json','Fourteen-task source mapping'),ref(BASE/'primary-review.json','Actual source review'),ref(BASE/'reconciliation-review.json','Exact changed-record reconciliation')]))
    print(json.dumps(dict(inspected=42,unread=71,changed_ids=sorted(changed),coverage_acceptance=False,source_records=3)))


if __name__=='__main__':
    main()
