#!/usr/bin/env python3
"""Preserve two primary inspections, exact reference and a census successor."""
import copy
from collections import Counter
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import evaluation_code_reference_20261019 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-19/census-evaluation-code-v1'
PRIOR = ROOT/'docs/program/execution/2026-10-18/census-biomedical-reasoning-v1'
RAW = ROOT/'docs/literature/raw'


def read(p):
    return json.loads(p.read_text())


def main():
    verify_bindings(read(BASE/'plan-review.json'))
    metadata = RAW/'exec19_census_evaluation_code_identity.xml'
    ns={'a':'http://www.w3.org/2005/Atom'}
    entries={e.findtext('a:id',namespaces=ns).rsplit('/',1)[-1]:e
        for e in ET.parse(metadata).getroot().findall('a:entry',ns)}
    definitions=[dict(name='evaluation',id='2307.03109v1',candidate='LA01-candidate-18',
        key='exec19_surveys_evaluation',title='A Survey on Evaluation of Large Language Models',
        first='Chang',author='Chang, Yupeng and Wang, Xu and Wang, Jindong and Wu, Yuan and others',
        date='6 July 2023',year=2023,pages=23,anchors={
            1:'Title/authors and6July2023v1 stamp; evaluation organized around what, where and how.',
            14:'Sections5.1-5.2 distinguish automated and human evaluation, costs and human variance; benchmark/API performance reports are secondary.',
            15:'Section6 states success/failure summaries depend on specific datasets; human-in-loop, dynamic and challenging protocols are proposed alternatives.',
            16:'Sections7.2-7.7: complete behavior, prompt robustness, static/public contamination risk, dynamic evaluation and evaluation-system validity; dynamic does not prove out-of-distribution status.'},
        claims=['The survey organizes evaluation by tasks, benchmarks and protocols, with distinct automated and human assessment roles.',
            'Its historical success/failure synthesis is explicitly dataset-dependent and reports constituent studies rather than current model qualification.',
            'Static public contamination, prompt robustness and trustworthiness of the evaluation system are unresolved design concerns; dynamic generation alone does not establish novelty.'],
        limits=['Selected historical v1, not a current comprehensive frontier census or model ranking.',
            'Constituent benchmark/tool performance needs its original primary sources; no model trial or causal capability is established.',
            'Extracted technical text inspected; rendered tables/figures not reviewed under exhausted image allowance.']),
        dict(name='code',id='2406.00515v1',candidate='LA01-candidate-20',
        key='exec19_surveys_code',title='A Survey on Large Language Models for Code Generation',
        first='Jiang',author='Jiang, Juyong and Wang, Fan and Shen, Jiasi and Kim, Sungju and Kim, Sunghun',
        date='1 June 2024',year=2024,pages=49,anchors={
            1:'Actual title, five authors and1June2024v1 stamp; template footer separately says September2024, not verified journal-publication identity.',
            3:'Lifecycle taxonomy: data curation, adaptation/advanced topics, evaluation and applications; prospective claims and scaling qualifications.',
            29:'Agent planning/memory/tools/actions and secondary framework examples; historical reported successes do not qualify current packages.',
            30:'Section4.10 distinguishes token/structural matching and execution metrics; table compiles cited historical model results, not a harmonized local rerun.',
            31:'Equation19 uses1-C(n-c,k)/C(n,k), but surrounding prose calls c correct samples within selected k; selected-pool and full-pool counts conflict. Unit-test quality and broader code attributes limit metric meaning.',
            32:'Human cost/variance/reproducibility and LLM-as-judge scope; historical MBPP compilation is secondary.',
            33:'Position, verbosity, self-enhancement and reasoning limitations of model judges; application claims need current vendor originals.',
            36:'Data coverage, real-workflow metrics, underrepresented languages, evolving dependencies, retrieval-quality limits and safety remain open challenges.',
            37:'Conclusion describes survey and empirical comparison; inspected tables remain source-reported compilation, not a newly reproduced matched experiment.'},
        claims=['The survey provides a lifecycle taxonomy for code-generation data, methods, evaluation and applications.',
            'Execution-based success depends on test quality and does not cover all maintainability, efficiency, stability or repository-level obligations.',
            'Human and model judging introduce separate variance, cost and bias; a score alone does not establish causal-target fidelity.',
            'The selected pass@k paragraph mislocates c within the selected k even though its finite-pool formula needs the total successful count among n.',
            'Historical compiled model scores and framework descriptions are secondary evidence, not present benchmark parity or causal capability.'],
        limits=['Selected2024v1 is distinct from the later2025 discovery metadata/DOI; no journal-version equivalence or present frontier completeness.',
            'The selected PDF has a September2024 template footer despite June2024v1 archive identity; preserve rather than normalize it.',
            'The metric inconsistency is resolved only for our own exact combinatorial construction; no uninspected original theorem is silently attributed.',
            'No live model, package installation, framework execution or visual table verification.'])]
    sources=[]
    for d in definitions:
        raw=RAW/('exec19_census_'+d['name']+'_selected.pdf')
        receipt=read(raw.with_suffix('.receipt.json'))
        assert receipt['status']=='saved' and receipt['sha256']==ref(raw,'Authentic original')['sha256']
        entry=entries[d['id']]
        assert ' '.join(entry.findtext('a:title',namespaces=ns).split())==d['title']
        assert entry.findtext('a:published',namespaces=ns)[:10] < '2026-10-08'
        target=ROOT/'docs/papers'/(d['title']+' '+d['first']+'('+str(d['year'])+').pdf')
        if target.exists():
            assert target.read_bytes()==raw.read_bytes()
        else:
            target.write_bytes(raw.read_bytes())
        pages=(BASE/(d['name']+'-selected.txt')).read_text().split('\f')
        assert sum(bool(p.strip()) for p in pages)==d['pages']
        anchors=[]
        for page,finding in d['anchors'].items():
            path=BASE/(d['name']+'-page-'+str(page)+'.txt')
            if path.exists():
                assert path.read_text()==pages[page-1]
            else:
                path.write_text(pages[page-1])
            anchors.append(dict(anchor='Physical PDF page'+str(page),finding=finding,
                extracted_text=ref(path,'Inspected technical text; no new visual acceptance')))
        sources.append(dict(integrated_citation_key=d['key'],kind='paper',title=d['title'],
            filename_title=d['title'],first_author=d['first'],author=d['author'],year=d['year'],
            source_identity='arXiv:'+d['id'],version_date='Selected v1 submitted '+d['date']+'; retrieved19October2026',
            cutoff='2026-10-07',local_copy=ref(target,'Authentic selected original'),
            local_path=str(target.relative_to(ROOT)),sha256=ref(target,'Original')['sha256'],
            inspected_anchors=anchors,supported_claims=d['claims'],limitations=d['limits'],
            identity_evidence=[ref(raw.with_suffix('.receipt.json'),'Actual acquisition'),
                ref(metadata,'Submission/version identity only'),
                ref(RAW/('exec19_census_'+d['name']+'_history.html'),'Preserved archive history; selected historical version')]))
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec19_surveys_reference',kind='project_derivation',
        title='Exact code-evaluation sampling, acceptance and economic denominators',author='Causal banking proposal project',year=2026,
        source_identity='Authored finite combinatorial and nested-outcome reference',version_date='19October2026',
        local_copy=ref(ROOT/'tools/evaluation_code_reference_20261019.py','Exact calculate function'),
        inspected_anchors=[ref(BASE/'exact-results.json','45 candidate pairs; nested20-attempt outcomes and assumed costs')],
        supported_claims=['Withn10,c3,k2 the at-least-one success probability is8/15, while random selection yields3/10.',
            'Incorrectly substituting the selected-subset success count yields16/135 on average.',
            'Stipulated12/16 test success differs from5/20 accepted requests; assumed cost120USD gives24USD per accepted and30USD net.'],
        limitations=['No observed model trial, causal validity, vendor pricing or bank ROI; no independent-task calibration.']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',
        scope='Two selected historical survey originals and one authored exact reference; constituent performance and current-frontier completeness not established'))
    write(BASE/'primary-review.json',dict(status='pass',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/'source-audit.json','Original identities and inspected technical scope'),
            ref(BASE/'exact-results.json','Exact authored reference'),ref(Path(__file__),'Preserving census review')],
        findings=[dict(candidate=d['candidate'],claims=d['claims'],limitations=d['limits']) for d in definitions],
        repairs_required_before_reuse=['Resolve pass@k full-pool versus selected-subset count before adopting a benchmark implementation.',
            'Inspect original constituent protocols before quoting comparable model or tool performance.',
            'Freeze task eligibility, attempts, selectors, causal-target acceptance and all-request costs; test contamination and judge validity separately.'],
        visual_acceptance=False,independent_acceptance=False,coverage_acceptance=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    changed={d['candidate']:d for d in definitions}; by_key={s['integrated_citation_key']:s for s in sources}
    for item in new['items']:
        if item['id'] not in changed:continue
        d=changed[item['id']]; assert item['disposition']=='open_original_not_inspected'
        item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',
            technical_source_review_open=False,source_key=d['key'],primary_source_record=by_key[d['key']],
            later_primary_review=ref(BASE/'primary-review.json','Inspected selected original and explicit adverse findings'),
            availability='Authentic selected v1 acquired and technically inspected; fixed public-source collector receipts retained.',
            effect_on_claims='Supports historical evaluation taxonomy and source-critical metric limitations; no current model, code-agent or causal qualification.',
            next_action='Integrate bounded discussion and exact denominator reference; inspect constituent originals and validate protocols before benchmark adoption.')
    assert all(a==b for a,b in zip(old['items'],new['items']) if a['id'] not in changed)
    counts=Counter(i['disposition'] for i in new['items']);assert counts['open_original_not_inspected']==67 and counts['inspected_primary_retained_with_limits']==46
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved44/69 original census'),
        changes=['Only candidate18 and20 receive selected-original primary inspections.'],
        evidence=[ref(BASE/'primary-review.json','Source-critical review'),ref(BASE/'source-audit.json','Authentic sources')],
        closure=False,interpretation='46/113 original candidates inspected;67 unread. Four crosscutting records and three separate citation-chain leads keep separate denominators.')
    write(BASE/'census-register.json',new)
    taskmap=copy.deepcopy(read(PRIOR/'task-map.json'))
    assert len(taskmap['task_families'])==14
    for task in taskmap['task_families']:
        for identifier,d in changed.items():
            if identifier not in task['inherited_ids']:continue
            assert identifier in task['uninspected_candidate_ids']
            task['uninspected_candidate_ids'].remove(identifier);task['inspected_candidate_ids'].append(identifier);task['inspected_source_keys'].append(d['key'])
        task['coverage_acceptance']=False
    taskmap.update(register=ref(BASE/'census-register.json','Current46/67 census'),supersedes=ref(PRIOR/'task-map.json','Preserved14-task mapping'))
    write(BASE/'task-map.json',taskmap)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=sorted(changed),unchanged_other_records=True,
        original_candidates=113,inspected=46,unread=67,task_families=14,coverage_acceptance=False,
        evidence=[ref(BASE/'census-register.json','Preserving successor'),ref(BASE/'task-map.json','Reconciled mapping')]))
    write(BASE/'inspection-progress.json',dict(finding='Two selected originals inspected;46/113 inspected and67unread. Source-critical limitations and exact authored evaluation reference recorded.',
        next_action='Integrate historical evaluation/code surveys, metric-definition critique and exact acceptance/selection distinctions into a preserving monograph and sponsor successor; retain L1/L6 and final coverage obligations.',
        evidence=[ref(BASE/n,'Inspected evidence') for n in ['primary-review.json','source-audit.json','census-register.json','task-map.json','reconciliation-review.json']]))
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'primary-review.json'))
    print(json.dumps(dict(inspected=46,unread=67,source_records=3,coverage_acceptance=False)))


if __name__=='__main__':
    main()
