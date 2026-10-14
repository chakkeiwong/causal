#!/usr/bin/env python3
"""Assemble the reviewed LA01 map from preserved source bytes; no networking.

The selections and judgments below are authored review decisions, not automated
paper quality ratings. This tool never imports or executes collected source.
"""
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'docs/program/repair-v12/work/LA01'
RAW = ROOT / 'docs/literature/raw'
DATE = '2026-10-12'
CUTOFF = '2026-10-07'


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (WORK / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': sha(path), 'anchor': anchor}


# Physical PDF pages, inspected in this recovery turn. Later publication dates
# are not inferred from first-version metadata or template journal headers.
NEW = [
    dict(aid='2404.14786', version='v2', date='2024-05-26', year=2024, author='Li',
         title='RealTCD: Temporal Causal Discovery from Interventional Data with Large Language Model',
         pages=[2, 3, 4, 5, 6, 8], families=['latent_temporal_discovery', 'iid_discovery', 'expert_evidence'],
         claims=[
             'RealTCD uses language-derived initial adjacency followed by numerical score optimization over temporal graphs and intervention targets.',
             'The setup assumes causal sufficiency, a known observational regime, finite lag and a DAG on the unrolled variables; Theorem 3.1 is conditional on capacity, intervention faithfulness, positivity and entropy assumptions.',
             'The real cooling-system study lacks a ground-truth DAG and scores selected relationships using expert physical-location rules.'],
         limits=[
             'The theorem is an author-stated population optimization result; local stochastic optimization and an edge threshold are not a finite-sample confidence guarantee.',
             'Anomaly windows are modeled as intervention regimes. An anomaly is not by itself a verified exogenous intervention in a bank.',
             'Useful temporal initialization candidate; not evidence for hidden-confounder identification or arbitrary bank state dynamics.']),
    dict(aid='2407.19638', version='v2', date='2025-10-10', year=2024, author='Feng',
         title='On the Reliability of Large Language Models for Causal Discovery',
         pages=[2, 3, 8, 9], families=['iid_discovery', 'expert_evidence', 'evaluation_cost'],
         claims=[
             'The study compares relation mentions in accessible OLMo/BLOOM pretraining corpora with pairwise causal judgments, and varies synthetic relation frequencies.',
             'Reported relation frequency is positively associated with performance; reversed or negated mentions can reduce affirmative response frequency.',
             'The context study uses GPT-4o-generated positive/negative contexts and human annotation; affirmative response rates vary substantially with context.'],
         limits=[
             'Affirmative response frequency is not a probability that a bank causal edge is true.',
             'The pretraining audit is limited to accessible corpora and mostly commonsense relations; it cannot establish the behavior of every closed model.',
             'Context can legitimately change a causal claim. Context sensitivity alone is not proof of an error; a fixed target and independently adjudicated context are required.']),
    dict(aid='2305.16183', version='v2', date='2023-10-02', year=2023, author='Lampinen',
         title='Passive learning of active causal strategies in agents and language models',
         pages=[3, 8, 10], families=['active_experiments', 'longitudinal_policy', 'evaluation_cost'],
         claims=[
             'The constructive argument trains on expert intervention-and-exploitation demonstrations and allows the learner to intervene in the evaluation system.',
             'A Chinchilla few-shot study reports transfer to a held-out odd-one-out dimension, with explanations and reasoning examples improving transfer.',
             'The authors limit their empirical conclusions to small finite acyclic systems and constrained observation/action spaces.'],
         limits=[
             'Passive training is not purely observational identification of a new system: evaluation interventions supply new causal information.',
             'These experiments do not qualify off-policy value estimation from confounded banking logs or a general longitudinal policy learner.',
             'Prompts and available interventions are part of the experimental condition, not free causal knowledge.']),
    dict(aid='2410.14146', version='v1', date='2024-10-18', year=2024, author='Zhang',
         title='CausalChat: Interactive Causal Model Development and Refinement Using Large Language Models',
         pages=[3, 4, 11, 12], families=['business_translation', 'diagram_construction', 'expert_evidence', 'evaluation_cost'],
         claims=[
             'CausalChat combines optional CPDAG discovery, GPT-4 suggestions, graph editing and SEM coefficient updates, with visual summaries linked to responses.',
             'Prompts ask for 1-to-4 causal-significance ratings, confounders, mediators and actionable latent-factor proposals.',
             'The nonexpert study uses six university students and a fixed sequence of BIC feedback, LLM text and CausalChat Lite; reported edge errors are 5/18, 7/18 and 1/18 respectively.',
             'Expert feedback explicitly raises missing citations and uncertainty about the quality of the model-provided scientific evidence.'],
         limits=[
             'The ordered stages use different self-selected remaining edges; the results do not identify the interface treatment effect under randomized matched conditions.',
             'Ordinal model ratings are not calibrated causal confidence; SEM fitting cannot establish that an added edge or latent variable is true.',
             'Retain the interaction and provenance ideas; require source anchors and preserve CPDAG/PAG ambiguity in our design.']),
    dict(aid='2608.09696', version='v5', date='2026-09-27', year=2026, author='Murphy',
         title='Model Discovery Agent: LLM-assisted Bayesian experiment design for data-efficient discovery of mechanistic world models',
         pages=[4, 5, 7, 8, 9], families=['active_experiments', 'longitudinal_policy', 'latent_temporal_discovery', 'agent_architecture', 'evaluation_cost'],
         claims=[
             'MDA uses an LLM for executable mechanism proposals; numerical methods fit models, approximate evidence and select experimental designs.',
             'The operational design criterion is a model-disagreement approximation to expected information gain, with BIC or SMC evidence and latent-state inference.',
             'Reported studies cover chemistry, glucose ODEs and stochastic neuron dynamics; the paper explicitly states its finite held-out prediction tests do not establish causal identification.',
             'The illustrated experiments use open-loop policies. Chemistry comparisons retain 115 matched evaluable world-seed cells from 171 attempts; inference comparisons share a model archive and histories.'],
         limits=[
             'An adaptively proposed and pruned model pool need not contain the truth. Normalized BIC weights and conditional posterior uncertainty are not uniform causal coverage.',
             'The reported comparisons target sample efficiency and are not compute matched; failed/unavailable cells must remain in the denominator of a bank trial.',
             'Mechanism proposals are an architectural candidate, not evidence of a qualified closed-loop servicing policy or of local reproduction.']),
    dict(aid='2606.23608', version='v1', date='2026-06-22', year=2026, author='Zheng',
         title='Causal Discovery in the Era of Agents',
         pages=[3, 5, 9], families=['agent_architecture', 'diagram_construction', 'latent_temporal_discovery', 'reporting_monitoring', 'data_code'],
         claims=[
             'The paper describes causal-learn+ with agent assistance for data inspection, assumption elicitation, method selection and interpretation around formal discovery algorithms.',
             'It distinguishes agent suggestions, user decisions, algorithm parameters and graph outputs, and explains why CPDAG/PAG ambiguity must remain visible.',
             'It calls for future benchmarks of data diagnosis, method selection and calibrated interpretation.'],
         limits=[
             'This is a design argument and system description, not an independently qualified bank workflow or measured institutional benefit.',
             'User approval does not prove assumption truth, and formal algorithms remain conditional on their sampling and scientific premises.',
             'A declared, separately validated hybrid method is conceptually possible; the paper’s restrictive design preference is not a universal impossibility theorem.']),
]


def augment_sources():
    audit = read(WORK / 'source-audit.json')
    sources = {x['id']: x for x in audit['sources']}
    corpus = []
    for x in NEW:
        key = 'v12_la_' + x['aid'].replace('.', '_')
        raw = RAW / ('v12_la_direct_pdf_' + x['aid'].replace('.', '_') + '.pdf')
        textpath = WORK / 'extracted' / (x['aid'] + '.txt')
        txt = textpath.read_text()
        assert raw.read_bytes().startswith(b'%PDF-')
        assert f"arXiv:{x['aid']}{x['version']}" in txt.split('\f')[0]
        target = ROOT / 'docs/papers' / f"{x['title']} {x['author']}({x['year']}).pdf"
        if target.exists():
            assert sha(target) == sha(raw), target
        else:
            shutil.copyfile(raw, target)
        record = {
            'id': key, 'kind': 'paper', 'title': x['title'], 'filename_title': x['title'],
            'first_author': x['author'], 'year': x['year'],
            'url': f"https://arxiv.org/abs/{x['aid']}{x['version']}",
            'arxiv_version': x['aid'] + x['version'], 'version_date': x['date'],
            'publication_status': 'inspected arXiv preprint; no venue acceptance inferred',
            'identity_basis': 'First PDF page title, first author and exact arXiv version/date stamp; API metadata was not separately acquired in this batch.',
            'accessed': DATE, 'local_path': str(target.relative_to(ROOT)), 'sha256': sha(target),
            'pages': len(txt.rstrip('\f\n').split('\f')), 'extracted_text': str(textpath.relative_to(ROOT)),
            'retrieval_receipt': str((raw.with_suffix('.receipt.json')).relative_to(ROOT)),
            'source_status': 'selected_primary_methods_results_and_limits_inspected',
            'inspection_date': DATE, 'inspection_scope': 'Selected physical PDF pages only; not every page reviewed.',
            'anchors': [{'pdf_page': p, 'section': 'Selected method, evaluation or limitation passage recorded in claims'} for p in x['pages']],
            'task_families': x['families'], 'claims': x['claims'],
            'adverse_findings_and_limits': x['limits'],
            'project_disposition': 'Use the scoped argument with attached limits; package execution and empirical qualification remain separate.',
            'cutoff_status': 'Inspected PDF version stamp is no later than 2026-10-07; access date is later and explicitly recorded.',
            'implementation_qualification': 'none; author-reported results only',
        }
        sources[key] = record
        corpus.append(record)

    oci = sources['v12_la_package_oci_agent']
    notebook = RAW / 'v12_la_oci_notebook.json'
    receipt = read(RAW / 'v12_la_oci_notebook.receipt.json')
    if not any(v['path'] == str(notebook.relative_to(ROOT)) for v in oci['local_sources']):
        oci['local_sources'].append({**bound(notebook, 'Notebook code cells 42 and 43, zero-based indices'),
                                     'url': receipt['url'], 'accessed_utc': receipt['accessed_utc']})
    oci['anchors'] += ['econml.ipynb code cells 42 and 43 (zero-based): trimming, aipw_summary(Y_DR[keep]) and ato_result serialization']
    oci['claims'] += ['The pinned notebook labels a uniformly averaged AIPW pseudo-outcome on a propensity-trimmed subset as ATO; this is not the conventional e(X)(1-e(X))-weighted overlap estimand.']
    oci['adverse_findings_and_limits'] += ['Rename the target to trimmed-population ATE with threshold and selection rule, or implement and qualify actual overlap weighting. Estimated trimming adds target/selection uncertainty.']
    cds = sources['v12_la_package_causalds']
    cds['anchors'] += ['grader.py lines 152–174: missing-identification defaults; 296–370: abstention and malformed answers; 1507–1568: interval score; 3529–3546: capped normalized score and separate coverage']
    cds['claims'] += [
        'The grader gives abstention credit only for an explicitly abstainable task and an intentional null-equivalent response; malformed answers do not earn abstention credit.',
        'The interval grader records width and coverage as well as an interval score; summary normalized interval scores are capped at 10.',
        'The inspected helpers default missing identification metadata toward identifiable/not-nonidentifiable. The ATE interval branch checks ordering but does not explicitly reject every nonfinite endpoint.'
    ]
    cds['adverse_findings_and_limits'] += ['Require an explicit three-state identification oracle and finite interval validation before scorer adoption; missing metadata must stay unknown. Report uncapped tail losses alongside any capped aggregate.']
    cladder = sources['v12_la_package_cladder']
    cladder['adverse_findings_and_limits'] += ['The inspected IV graph/template does not by itself establish homogeneity or monotonicity. Exclude IV-as-population-ATE labels from a trusted local benchmark until the full generator and per-item assumptions have independent verification.']
    for record in sources.values():
        if record['kind'] == 'paper' and 'filename_title' not in record:
            suffix = f" {record['first_author']}({record['year']}).pdf"
            name = Path(record['local_path']).name
            assert name.endswith(suffix)
            record['filename_title'] = name[:-len(suffix)]
        for field in ['anchors', 'claims', 'adverse_findings_and_limits']:
            if field in record:
                record[field] = list({json.dumps(v, sort_keys=True): v for v in record[field]}.values())
    audit.update(status='reviewed_bounded_evidence_map', review_date=DATE,
                 scope='Primary evidence map, not exhaustive literature coverage, package execution or MR02 closure.',
                 sources=list(sources.values()))
    write('source-audit.json', audit)
    write('primary-corpus-extension-p.json', {'cutoff': CUTOFF, 'sources': corpus})
    return audit


INCLUDED = {9:'2607.22443',61:'2606.23608',67:'2402.15301',101:'2305.00050',103:'2602.11527',
105:'2410.14146',106:'2607.08093',121:'2312.04350',129:'2410.06392',151:'2402.01207',
160:'2609.30867',173:'2402.07770',178:'2306.16902',179:'2402.01454',186:'2602.18662',
190:'2405.13551',192:'2407.19118',200:'2402.11068',203:'2406.07378',227:'2608.09696',
228:'2407.15073',236:'2407.19638',238:'2607.01977',243:'2305.16183',250:'2404.14786',262:'2506.16234'}
VERSION_LINKS = {2:1,4:3,11:10,72:71,75:74,111:110,112:110,117:116,132:131,143:142,
145:144,147:146,183:182,197:196,201:200,205:204,220:219,222:221,226:225,230:229,237:238}
RELEVANT = set([10,26,27,31,33,35,40,42,46,48,53,56,58,60,74,104,107,108,109,110,113,114,
115,116,120,122,125,126,128,130,131,136,137,138,139,140,141,148,149,154,157,163,164,165,
166,167,171,172,175,176,180,182,184,194,199,202,206,207,213,214,217,221,225,234,239,241,
242,245,246,252,256,260,261,263,266,269,270,271,273,276,278,282])
BACKGROUND = set([0,12,18,19,20,25,32,41,45,54,118,155,181,185,188,189,191,193,196,204,
218,244,253,254,259,268,277,283,284,285,286])


def screen():
    candidates = read(WORK / 'screening-candidates.json')
    decisions = []
    for n, x in enumerate(candidates):
        row = {'index': n, 'candidate_id': x['id'], 'title': x['title'], 'metadata_date': x['date'],
               'doi': x.get('doi'), 'searches': x['queries'], 'review_date': DATE,
               'screening_basis': 'Individually inspected title and saved metadata; full-text review only where an audit is linked.'}
        urls = list(dict.fromkeys(v['pdf_url'] for v in x['locations'] if v.get('pdf_url')))
        row['acquisition_leads'] = urls or [v['landing_page_url'] for v in x['locations'] if v.get('landing_page_url')]
        if n in INCLUDED:
            row.update(status='selected_primary_inspected', source_id='v12_la_' + INCLUDED[n].replace('.', '_'),
                       reason='Selected to develop a task-family mechanism, adverse finding or evaluation boundary; audited version governs technical claims.')
        elif n in VERSION_LINKS:
            row.update(status='possible_version_duplicate', related_candidate_index=VERSION_LINKS[n],
                       reason='Same normalized title appears in another saved record. Retained as a possible preprint/venue metadata link, not silently merged as identical bytes.')
        elif n in RELEVANT:
            row.update(status='relevant_candidate_deferred',
                       reason='Title indicates a potentially relevant causal-agent, ontology, evaluation or statistical boundary contribution. Original text not inspected in this bounded map; no capability claim drawn.')
        elif n in BACKGROUND:
            row.update(status='adjacent_background_deferred',
                       reason='Potential generic agent, code, retrieval, evaluation or domain background. Does not by its title establish a causal algorithm; defer technical claims until primary inspection.')
        else:
            row.update(status='not_selected_title_scope',
                       reason='Title concerns general causal/statistical foundations, a domain application without an explicit causal-assistant contribution, or general LLM architecture/behavior. Not selected for this bounded LLM-assistance map; may belong in SW or the inherited foundation corpus. This is not a full-text quality exclusion.')
        decisions.append(row)
    write('screening-decisions.json', {'status':'reviewed_title_screen', 'candidates':len(candidates),
          'counts':dict(Counter(v['status'] for v in decisions)),
          'exhaustiveness':'Only the saved bounded searches; no claim of database saturation or comprehensive absence.', 'decisions':decisions})
    return decisions


def searches():
    rows = []
    for p in sorted(RAW.glob('v12_la*.receipt.json')):
        d = read(p)
        if 'search' not in d['id']:
            continue
        params = parse_qs(urlparse(d['url']).query)
        row = {'id':d['id'], 'provider':urlparse(d['url']).hostname, 'url':d['url'],
               'query_parameters':params, 'accessed_utc':d['accessed_utc'], 'status':d['status'],
               'receipt':bound(p,'Original HTTP acquisition receipt'), 'cutoff':CUTOFF}
        if d['status'] == 'saved':
            source = ROOT/d['path']; data = read(source)
            row.update(local_copy=bound(source,'Saved provider response, discovery metadata only'),
                       returned_records=len(data.get('results',[])), provider_total=data.get('meta',{}).get('count'),
                       coverage_limit='First 25 ranked records only; unpaginated. Provider indexing, query vocabulary and date metadata can miss eligible work.')
        else:
            row.update(error=d.get('error'), coverage_limit='Failed query contributes no search coverage or absence evidence.',
                       next_action='Retry a bounded query after provider recovery or use the saved direct author/publisher leads; do not hammer the rate-limited endpoint.')
        rows.append(row)
    write('search-ledger.json', {'schema_version':1, 'status':'reviewed_bounded_search',
          'literature_cutoff':CUTOFF, 'review_date':DATE, 'searches':rows,
          'selection_rule':'Cover all fourteen task families, contrasting mechanisms and adverse evidence; prioritize original technical text and inspect selected methods/results/limits. Do not claim saturation.',
          'screening':bound(WORK/'screening-decisions.json','All 287 candidate dispositions and possible duplicate/version links'),
          'citation_chains':[
              {'from':'v12_la_2606_23608','anchor':'PDF p.9 bibliography entry 5','to':'v12_la_2405_13551','role':'Hybrid-prior alternative to the protected-core position'},
              {'from':'v12_la_2407_19638','anchor':'PDF p.9 related work','to':'v12_la_2402_01207','role':'Breadth-first call-efficiency alternative; call counts versus token cost'},
              {'from':'v12_la_2608_09696','anchor':'PDF pp.8–9 discussion','to':'v12_la_2305_00050','role':'Separating mechanism proposals and interventional prediction from identification'}],
          'acquisition_batches':['K','L','M','N','O','P'],
          'later_delta_policy':'No newly inspected source version in this LA01 map is after cutoff. Later access dates are retained, not backdated.'})


# Every family records what is supported and what remains unknown. A roadmap or
# negative result can inform the map without being labeled a working capability.
FAMILIES = [
('business_translation',['2305.00050','2312.04350','2607.08093','2607.22443','2407.19118'],['pywhy_llm','oci_agent','causalds'],
 'Translate decision, unit, intervention, comparator, population, horizon and loss into explicit alternatives. CausalDS and CLadder expose task definitions; the copilot/OCI sources propose assisted formulation.',
 'A fluent paraphrase can silently change ATE to ATT, a trimmed target, a policy value or a prediction. No source certifies the intended banking estimand.',
 'LA02 must keep unresolved alternatives and obtain scientific ownership before committing to one target.'),
('variable_ontology',['2607.01977','2402.07770','2607.08093'],['ontolearner'],
 'Ontology extraction and quantitative knowledge retrieval can propose variable definitions and semantic relations; benchmark observation models expose conceptual/proxy distinctions.',
 'Taxonomic edges are not causal arrows; extracted labels do not establish ownership, measurement validity or availability time.',
 'LA02 requires measured-versus-latent types, event/availability clocks, units and a link to the original observation record.'),
('expert_evidence',['2402.15301','2402.07770','2405.13551','2609.30867','2410.14146'],['pywhy_llm'],
 'Retrieval, soft priors and assumption-evidence audits support hypothesis elicitation and conflict review.',
 'Retrieval worsens selected discovery cells; source absence and retrieval failure differ; agreement and model ratings are not causal truth.',
 'LA02/LA03 attach citations, counterevidence, disputed alternatives and an explicit refusal state to every claim.'),
('diagram_construction',['2402.01207','2406.07378','2410.14146','2606.23608'],['pywhy_llm','causal_gpt','causalagent'],
 'Pairwise/CI prompts, breadth-first graph proposals and interactive graph editing provide distinct diagram workflows.',
 'Cycle rejection establishes syntax only. Prompt direction or a graph editor must not erase CPDAG/PAG equivalence or latent confounding.',
 'LA02/LA03 preserve endpoint marks, temporal order, graph revisions and separate proposal versus approved-assumption layers.'),
('iid_discovery',['2402.15301','2406.07378','2405.13551','2402.01454','2407.15073','2407.19638'],['causal_gpt','llm_cd','llm_scd'],
 'The corpus contains LLM-only, retrieval, statistical reweighting, soft-prior and multi-agent alternatives with author-reported benchmark comparisons.',
 'Memorization, prompt instability, wrong-domain evidence and model-response tests undermine unqualified discovery claims. Reported small-benchmark gains do not imply effect coverage.',
 'LA03 and LA06 compare data-only baselines and registered label, retrieval and prompt perturbations; preserve every failed case.'),
('latent_temporal_discovery',['2506.16234','2404.14786','2602.18662','2608.09696','2606.23608'],['lcm','causalagent'],
 'Noisy-prior PAG work, sufficient temporal initialization, numerical temporal foundation models and latent mechanism proposals occupy different statistical regimes.',
 'Batch-sequential discovery is not longitudinal policy identification. RealTCD and LCM sufficiency restrictions cannot be removed by language suggestions; MDA finite prediction tests do not identify arbitrary latent mechanisms.',
 'LA03 retains temporal/PAG assumptions and the unresolved R04 effect-set boundary; no blanket latent-temporal qualification.'),
('active_experiments',['2305.16183','2506.16234','2608.09696'],[],
 'The sources cover learned experiment strategies, noisy expert queries and numerical information-gain surrogates over proposed mechanisms.',
 'Querying an LLM is not intervening on a bank. EIG within a misspecified pool is not expected bank profit; pruning can discard a later useful model.',
 'Specify permitted experiments, cost and decision loss; compare random and numerical designs with the same acquisition budget.'),
('identification',['2312.04350','2607.08093','2410.06392','2609.30867','2606.23608'],['cladder','causalds','pywhy_llm'],
 'Formal benchmark generators and algorithm-assisted workflows can separate adjustment, front-door/ID, counterfactual queries and nonidentification.',
 'PyWhy-LLM front-door is unimplemented in the inspected revision; the CLadder IV template needs extra assumptions; LLM-generated counterfactual truth is not an independent oracle.',
 'Use a separate formal engine and a three-state identified/not-identified/unknown result; quarantine unsupported IV labels.'),
('data_code',['2607.01977','2607.22443','2602.11527','2607.08093','2606.23608'],['oci_agent','ontolearner','causalagent','causalds'],
 'Agents can prepare typed specifications, request data summaries and orchestrate fixed causal tools; static sources expose notebook and package boundaries.',
 'Unbounded notebook execution, mutable ontology downloads, unbound tool functions and empty-JSON fallbacks prevent direct adoption as a trustworthy runtime.',
 'LA04/LA05 adapt fixed audited operations with hashed artifacts, bounded jobs and explicit failure rather than running generated code.'),
('longitudinal_policy',['2407.19118','2305.16183','2608.09696','2607.22443'],['oci_agent'],
 'Medical copilot roadmaps discuss complex causal tasks; passive strategy experiments and MDA provide adjacent sequential/latent examples. OCI supplies a static observational workflow.',
 'This inspected corpus provides no locally qualified LLM-assisted longitudinal g-method, off-policy inference or closed-loop bank policy. Alaa is a roadmap, OCI is not longitudinal, and MDA uses open-loop experiments.',
 'Develop the explicit longitudinal target/clock/assignment contract in LA02/LA04, retain missing primary implementation evidence and the failed targeted searches, and do not invent a working package.'),
('estimation_validation',['2607.22443','2607.08093','2407.19118','2609.30867'],['oci_agent','causalds'],
 'OCI and CausalDS connect estimation to diagnostics, target definitions, abstention and interval scoring; ARGUS audits reported identification evidence.',
 'Trimming changes the target; balance and placebo checks cannot verify unconfoundedness; missing identification metadata and capped scores can conceal failure.',
 'Separate target, identification, statistical calibration and diagnostic results; require uncapped losses and explicit unknown states.'),
('reporting_monitoring',['2609.30867','2607.22443','2606.23608','2407.19118'],['oci_agent','causalagent'],
 'Actor/critic reports and evidence audits can expose assumptions, provenance, unmet conditions and required domain review.',
 'These are not validated drift alarms or external acceptance. A retrieved statement of an assumption is not proof that it holds.',
 'LA04 defines assumption/source/version invalidation, explicit monitoring ownership and report generation from fixed result objects.'),
('agent_architecture',['2602.11527','2607.22443','2606.23608','2608.09696'],['causalagent','oci_agent','causalds'],
 'Conversational MCP tools, actor/critic notebooks, a protected discovery core and mechanism-proposal loops are concrete architectural alternatives.',
 'Generic orchestration and transport do not supply identification algorithms, license clearance, error semantics or deployment qualification.',
 'LA04 connects typed handoffs to IN02/IN04; distinguish static source review, local conformance and external platform acceptance.'),
('evaluation_cost',['2312.04350','2607.08093','2407.19638','2410.14146','2608.09696','2407.15073'],['cladder','causalds'],
 'The evidence spans formal causal queries, numerical data-science tasks, contamination probes, interface studies and sample-efficiency experiments.',
 'Small public graphs, shared evaluation models, staged user studies, unmatched compute and selected success denominators prevent broad effectiveness or ROI claims.',
 'LA06 preregisters novel mechanisms/labels, independent oracles, valid abstention, effect loss, full cost and all-request availability.'),
]


def map_and_packages(audit):
    source_ids = {x['id'] for x in audit['sources']}
    families = []
    for name, papers, packages, finding, limit, action in FAMILIES:
        ids = ['v12_la_' + p.replace('.', '_') for p in papers] + ['v12_la_package_' + p for p in packages]
        assert set(ids) <= source_ids
        families.append({'id':name, 'status':'inspected_evidence_with_limits', 'source_ids':ids,
                         'supported_role':finding, 'adverse_findings_and_knowledge_gap':limit,
                         'next_action':action, 'capability_qualification':'none from literature map'})
    write('literature-map.json', {'schema_version':1, 'status':'reviewed', 'literature_cutoff':CUTOFF,
          'review_date':DATE, 'task_families':families,
          'evidence_distinctions':['inherited theoretical claim','author-reported empirical result','project interpretation','static source observation','locally qualified implementation'],
          'source_audit':bound(WORK/'source-audit.json','Identity, exact local sources, inspected primary anchors, supported claims and limits'),
          'scope_limit':'Every required task family is represented; a roadmap or negative result is not mislabeled as a working capability. Uninspected relevant candidates remain in omissions.'})
    cat = read(WORK/'package-catalog.json')
    cat['status'] = 'reviewed_candidate_dispositions'
    cat['review_date'] = DATE
    for x in cat['packages']:
        if x['id'] == 'oci_agent':
            x['integration_constraints'] = [v for v in x['integration_constraints'] if 'remains under notebook' not in v]
            x['integration_constraints'].append('Pinned notebook confirmed: uniform AIPW mean after trimming is a trimmed-population ATE; conventional overlap ATO requires e(X)(1-e(X)) weighting and separate qualification.')
        if x['id'] == 'causalds':
            x['integration_constraints'].append('Scorer review completed at selected branches: guard unknown/missing ID metadata, finite interval endpoints, separate malformed answers from abstention, and report uncapped losses.')
        if x['id'] == 'cladder':
            x['integration_constraints'].append('Exclude IV-as-population-ATE benchmark labels pending generator-level verification of structural assumptions and answer bounds.')
        x['review_scope'] = 'Candidate decision based on pinned static bytes; no installation, trial or compatibility qualification.'
        x['integration_constraints'] = list(dict.fromkeys(x['integration_constraints']))
    cat['paper_systems_without_audited_runtime'] = [
        {'source_id': 'v12_la_' + x['aid'].replace('.', '_'), 'system':name,
         'disposition':'architecture_or_method_evidence_only',
         'next_action':'Locate publisher-linked repository, pin pre-cutoff revision, inspect license/API/environment and register execution before adoption.'}
        for x,name in [(NEW[0],'RealTCD'),(NEW[3],'CausalChat'),(NEW[4],'MDA'),(NEW[5],'causal-learn+')]]
    write('package-catalog.json',cat)


def omissions(decisions):
    items = [dict(id=f"LA01-candidate-{x['index']}", candidate_id=x['candidate_id'], title=x['title'],
                  status=x['status'], reason=x['reason'], acquisition_leads=x['acquisition_leads'],
                  next_action='Acquire a genuine original via an allowed public route or supplied local original; verify title/version/cutoff and inspect technical anchors before use.',
                  effect_on_current_claims='No technical or frontier-superiority claim cites this uninspected candidate.')
             for x in decisions if x['status'] in ['relevant_candidate_deferred','adjacent_background_deferred']]
    items += [
        {'id':'LA01-longitudinal-search','status':'search_incomplete','reason':'Targeted arXiv longitudinal/off-policy searches returned HTTP 429; negative-result search timed out. Saved OpenAlex top-25 family search remains available.',
         'next_action':'Resume bounded specialist search after provider recovery; inspect sequential g-method/policy papers and code. Current map uses inspected roadmap and adjacent methods, without claiming absence.'},
        {'id':'LA01-runtime-licenses','status':'adoption_deferred','reason':'LLM-CD root license unresolved; LLM-and-SCD lacks a root license/README; LCM external weights not audited.',
         'next_action':'Obtain rights/versions for every component and original weights; keep code adoption deferred meanwhile.'},
        {'id':'LA01-benchmark-oracles','status':'qualification_deferred','reason':'CLadder IV assumptions and CausalDS unknown-ID/nonfinite-score branches need independent verification.',
         'next_action':'Quarantine suspect cells; use separately derived synthetic oracle fixtures and register all empirical trials in LA06.'},
        {'id':'LA01-bank-evidence','status':'external_evidence_absent','reason':'No authentic bank semantics, intervention/assignment evidence, accepted interfaces, external review or measured bank ROI.',
         'next_action':'Use master external-input contracts; synthetic or literary evidence cannot replace those inputs.'},
    ]
    write('omissions.json', {'schema_version':1,'status':'reviewed_open_limits','literature_cutoff':CUTOFF,
          'review_date':DATE,'scope':'An omission is not evidence of nonexistence, and a metadata title is not a verified technical work.',
          'items':items,'essential_unverified_capability_claims':[],
          'claims_not_made':['exhaustive literature coverage','qualified autonomous causal discovery','qualified longitudinal agent implementation','qualified package integration','bank ROI or acceptance']})


if __name__ == '__main__':
    audit = augment_sources()
    decisions = screen()
    searches()
    map_and_packages(audit)
    omissions(decisions)
    print(json.dumps({'sources':len(audit['sources']), 'papers':sum(x['kind']=='paper' for x in audit['sources']),
                      'screened':len(decisions), 'families':len(FAMILIES)}))
