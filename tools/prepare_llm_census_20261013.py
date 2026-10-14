#!/usr/bin/env python3
"""Account for inherited candidates and bind a focused primary-source tranche.

This deliberately does not turn unread candidates into exclusions or closure.
No network calls, model execution, or downloaded-code execution.
"""
import collections
import hashlib
import json
from pathlib import Path
import re
import shutil
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/llm-census'
OLD = ROOT / 'docs/program/repair-v12/work/LA01'
PRIOR = ROOT / 'docs/program/execution/2026-10-13/tetrad-reuse/reader/source-audit.json'
CUTOFF = '2026-10-07'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ref(p, anchor):
    return {'path': str(p.relative_to(ROOT)), 'sha256': sha(p), 'anchor': anchor}


def read(p):
    return json.loads(p.read_text())


def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


# Each entry is a primary reading record, not an automated title assessment.
SPECS = [
    dict(key='causaleval', candidate=107, title='CausalEval: Towards Better Causal Reasoning in Language Models',
         filename='CausalEval Towards Better Causal Reasoning in Language Models', first='Yu', year=2025,
         author='Longxuan Yu, Delin Chen, Siheng Xiong, Qingyang Wu, Qingzhen Liu, Dawei Li, Zhikai Chen, Xiaoze Liu and Liangming Pan',
         version='2410.16676v4', date='2025-02-17', pages=29,
         anchors={1:'Title, authors and version stamp; first three authors share equal-contribution credit.',
                  6:'Nine benchmark columns; starred models use 100 examples; each question is queried five times with greedy decoding.',
                  7:'Table 3: GPT-4o CoT/FunctionCall CLADDER 69/76 and e-CARE 90/73; enhancement gains vary by task.',
                  8:'Discussion and adverse task-specific results; prose GPT-3.5 causalCoT values differ from Table 3.',
                  10:'Text-centric coverage and excluded post-training/task-specific enhancements; bibliography leads.',
                  18:'Heterogeneous benchmark taxonomy and units; 500 samples or available maximum; cost-limited models use 100.',
                  19:'Human row mixes original dataset reports and three trained graduate students on 100 examples; answer-format violations count as failures.'},
         role='Retain as a benchmark taxonomy and adverse-evidence source; design matched mechanism-level evaluation.',
         limits='No local model replication; repeated calls are not independent task draws. Benchmark oracles, unequal sample sizes, mixed human provenance and a table/prose discrepancy prevent an undifferentiated superiority claim.'),
    dict(key='graph_validation', candidate=245,
         title='Prompting or Fine-tuning? Exploring Large Language Models for Causal Graph Validation',
         filename='Prompting or Fine-tuning Exploring Large Language Models for Causal Graph Validation',
         first='Susanti', year=2025, author='Yuni Susanti and Nina Holsmoelle',
         version='2406.16899v2', date='2025-04-09', pages=9,
         anchors={1:'Title, authors, arXiv stamp and June 2025 workshop.',
                  4:'BERT and GPT fine-tuning receive labeled training examples; classification and extraction formats.',
                  5:'Table 1 DDI F1: Single-Prompt C 67.4; PubMedBERT 87.9. Four datasets and five-fold means with fold SDs.',
                  6:'Few-shot is not uniformly better; annotation cost acknowledged; evaluation explicitly limited to binary pairwise relations.',
                  8:'References 17–22 provide causal-LLM and evaluation citation leads.'},
         role='Retain supervised small-model extraction as a serious baseline; require graph-level and effect-level evaluation separately.',
         limits='Binary relations extracted from text do not verify a target-population graph. Training budgets differ. Exact splits, Maybe handling and per-arm model versions require code audit.'),
    dict(key='orca', candidate=241, title='ORCA: ORchestrating Causal Agent', filename='ORCA ORchestrating Causal Agent',
         first='Chung', year=2026, author='Joanie Hayoun Chung, Sumin Lee and Sungbin Lim',
         version='2508.21304v3', date='2026-03-18', pages=35,
         anchors={1:'Version identity; abstract claims a 42-percentage-point completion improvement.',
                  3:'Twelve participants, within-subjects counterbalanced design; baseline GPT-4o-mini has tools, step gates and minimal state.',
                  4:'Shared intermediate artifacts; REEF is generated from a predefined SCM with relational complications.',
                  5:'Table 1 completion .75/.83, discovery .67/.83, data selection .75/1 and reported CI coverage .083/.50; plot excludes outliers.',
                  6:'Reference 9 explicitly cites Han et al. Causal Agent arXiv:2408.06849.',
                  10:'Consensus PAG converted into one DAG by rank-based, cycle-safe orientation and edge removal; uncertainty is not carried unchanged into effect estimation.',
                  17:'Completion means producing an ATE irrespective of accuracy. Discovery success means treatment and outcome nodes are present. CI metric wording is nonstandard.',
                  18:'Full-data ATE-error condition test p=.321; after excluding configuration-error outliers, OLS p=.020.'},
         role='Reuse the explicit dataset/graph/estimand state design as an architectural candidate; reject arbitrary orientation as an identifying assumption.',
         limits='No local replication or code/license admission. Abstract completion gain conflicts with Table 1. Reported CI coverage wording needs raw-code clarification and is not silently reinterpreted as nominal frequentist coverage. End-to-end failures must remain in the main comparison.'),
    dict(key='causalsmith', candidate=114,
         title='CausalSmith: A Formally Grounded, Self-Improving Agentic Framework for Automated Research in Causal Inference',
         filename='CausalSmith A Formally Grounded, Self-Improving Agentic Framework for Automated Research in Causal Inference',
         first='Tan', year=2026, author='Jiyuan Tan and Vasilis Syrgkanis', version='2607.22511v4', date='2026-09-15', pages=38,
         anchors={1:'Title, authors, version and reported 8,179 declarations.',
                  2:'Compiler-accepted artifacts can change a hypothesis or assume the hard step as an axiom.',
                  12:'Mechanical scan/build and LLM statement-match audit are distinct layers; Table 4 lists vacuity and statement drift.',
                  14:'Table 5: 144 recorded runs, 14 accepted, 59 downgraded, 71 failed; reruns count separately and legacy runs are excluded.',
                  15:'All 14 accepted runs classified as gap filling; question-type classifications were assigned after runs.',
                  17:'Authors acknowledge no independent human validation of research quality and unknown error rate of LLM statement matching; reference 9 points to ORCA.',
                  38:'Reported Lean toolchain 4.29.0-rc3, axiom audit and source/run records; model lineup changed across the campaign.'},
         role='Retain formal statements, dependency/axiom checks and prose-to-statement review as separate prototype obligations.',
         limits='Paper-reported compilation and run counts were not locally reproduced. Internal acceptance is not independent novelty or significance review. LLM statement matching has an unmeasured error rate; no general autonomous-theorem-solving claim.'),
    dict(key='augur_arxiv', candidate=40,
         title='Augur: Modeling Covariate Causal Associations in Time Series via Large Language Models',
         filename='Augur Modeling Covariate Causal Associations in Time Series via Large Language Models',
         first='Cui', year=2025, author='Zhiqing Cui, Binwu Wang, Qingxiang Liu, Yeqiang Wang, Zhengyang Zhou, Yuxuan Liang and Yang Wang',
         version='2510.07858v2', date='2025-11-26', pages=24,
         anchors={1:'Preprint identity; differs from the metadata lead for a 2026 ACL version.',
                  3:'Target is future trend prediction; teacher/student architecture.',
                  4:'Top-K Spearman pair pruning; LLM direction/confounded/spurious classification; cycle repair.',
                  5:'Stability is agreement between generated graphs; groundedness is summary agreement with the generated graph.',
                  6:'Prediction metrics are F1/AUROC; chronological 7:2:1 split and finance/traffic transfer; language quality scores are separate.',
                  10:'Limitations explicitly assume causal sufficiency and acknowledge missed nonlinear or lagged dependence and teacher bias.'},
         role='Retain as a forecasting and hypothesis-generation comparator; require a separately identified policy-effect target.',
         limits='Inspected author preprint, not the inaccessible publisher version. Graph consensus, acyclicity and predictive improvement do not establish intervention identification or hidden-confounder recovery. No local model run.'),
    dict(key='text_review_arxiv', candidate=269,
         title='Text and Causal Inference: A Review of Using Text to Remove Confounding from Causal Estimates',
         filename='Text and Causal Inference A Review of Using Text to Remove Confounding from Causal Estimates',
         first='Keith', year=2020, author='Katherine A. Keith, David Jensen and Brendan O’Connor',
         version='2005.00649v1', date='2020-05-01', pages=13,
         anchors={1:'Identity and focus on measuring confounders from observed text.',
                  5:'Text can encode confounders, colliders and mediators; measurement error and proxy correction remain open questions.',
                  9:'Constructed observational and semi-synthetic evaluation proposals; warning about researcher-chosen easy-to-recover confounders and unvalidated text adjustment.'},
         role='Retain as methodological foundation for LLM measurement; separate extraction validation from identification and effect validation.',
         limits='A review of text-based adjustment, not proof that modern embeddings remove confounding. Publisher acquisition rejected by collector host policy; author preprint inspected instead. No causal formula in the review was adopted without independent derivation.'),
    dict(key='texts', candidate=175, title='How to Make Causal Inferences Using Texts',
         filename='How to Make Causal Inferences Using Texts', first='Egami', year=2018,
         author='Naoki Egami, Christian J. Fong, Justin Grimmer, Margaret E. Roberts and Brandon M. Stewart',
         version='1802.02163v1', date='2018-02-06', pages=47,
         anchors={1:'Original preprint stamp 6 February 2018; manuscript heading 8 February 2018.',
                  9:'Codebook g defines the text-based target; learning g on the estimation documents risks analyst-induced dependence and overfitting.',
                  11:'Separate codebook discovery and effect estimation using disjoint samples.',
                  14:'Text-as-treatment requires a sufficiency restriction on the representation, beyond sample separation.',
                  16:'Freeze evaluation before test access; no adapting the codebook to test validation; sample splitting has efficiency cost.'},
         role='Adopt the design principle of freezing a measurement rule before held-out effect evaluation, with explicit causal assumptions.',
         limits='Inspected 2018 preprint, not assumed identical to later publication. Sample splitting does not establish construct validity, exchangeability, positivity or invariance of outcomes within text representations.'),
    dict(key='credible', candidate=131,
         title='Credible causal inference beyond toy models: An invitation to graphical models for the skeptic',
         filename='Credible causal inference beyond toy models An invitation to graphical models for the skeptic',
         first='Geraldo Bastías', year=2024, author='Pablo Geraldo Bastías', version='2402.11659v1', date='2024-02-18', pages=31,
         anchors={1:'Title, author and version; argues for explicit extra-statistical assumptions.',
                  17:'Minimal DAG and evidence-generating-process approach; labels for quasi-experiments are not sufficient credibility evidence.',
                  20:'Bottom-up construction starts with assumptions a researcher is actually willing to make.',
                  21:'Table 5 preserves multiple models, checks identification in each, tests implications and revisits missing relationships and variables.'},
         role='Retain as an adjacent methodological source for business formulation and diagram review, not an LLM implementation.',
         limits='Conceptual/methodological argument with worked examples. It does not prove a fully general graph elicitation algorithm or certify assumptions in banking.'),
    dict(key='causal_agent', candidate=56, title='Causal Agent based on Large Language Model',
         filename='Causal Agent based on Large Language Model', first='Han', year=2026,
         author='Kairong Han, Kun Kuang, Ziyu Zhao, Junjian Ye and Fei Wu', version='2408.06849v3', date='2026-08-12', pages=14,
         anchors={1:'arXiv version/date and authors; ACM 2018 venue/DOI text remains an unfilled template and is not used as publication identity.',
                  6:'Graph objects in memory link tools; synthetic 3–10-node nonlinear additive Gaussian mechanisms and randomly named medical/marketing variables.',
                  7:'81 templates and 311-variable pool; yes/no/uncertain answers and graph/effect tasks.',
                  8:'Tool-equipped iterative agent compared with a one-run code-generation baseline; documented wrong-variable, wrong-test and parameter errors.',
                  9:'157/160 effect questions reported correct; 100 sampled cost cases at variable/edge/graph levels, iteration cap 15, mean 3.37s/2.51 iterations/5308 tokens.',
                  10:'RestGPT comparison uses 100 samples and manually adapted tools; multi-agent instability reported; QRData evaluation is a subset.'},
         role='Retain graph-object memory and typed tool interfaces; test matched tools, repair opportunities and full failure costs.',
         limits='No local execution. Synthetic domain words do not establish domain truth. Effect tolerance/oracle needs code review; cost sample excludes the effect-level workflow. Asymmetric tool and retry budgets limit causal attribution of the measured gains.'),
    dict(key='collaboration', candidate=74, title='Causal Inference for Human-Language Model Collaboration',
         filename='Causal Inference for Human-Language Model Collaboration', first='Zhang', year=2024,
         author='Bohan Zhang, Yixin Wang and Paramveer S. Dhillon', version='2404.00207v1', date='2024-03-30', pages=18,
         anchors={1:'Title, authors and version; proposed Incremental Stylistic Effect (ISE) and CausalCollab.',
                  4:'Sequential human edits and model replies; causal target and sequential exchangeability/positivity discussion.',
                  5:'ISE is an infinitesimal change in a text-style functional with a conditional mixture over text versions; Theorem 1 is conditional.',
                  6:'CVAE-derived representations, fitted outcome model and Monte Carlo evaluation; identification assumptions remain explicit.',
                  7:'ChatGPT creates counterfactual edits and labels outcomes; alpha split changes confounding correlation; CoAuthor, self-chat Baize and DIALOCONAN sources differ.',
                  9:'Robustness is measured in the constructed design; paper links dtr-text code, not inspected or executed here.'},
         role='Retain a direct longitudinal human/LM collaboration method; define an implementable editing policy and validate its measurement and support.',
         limits='A low-dimensional representation does not certify overlap, hidden-confounder absence or a unique physical intervention. Generated counterfactuals and model labels are constructed evaluation evidence, not observed alternative human outcomes. Theorem and code have not been independently reproduced.'),
]

# Manual provisional mapping by title and original discovery provenance.
# Unread titles retain an explicit open technical disposition.
GROUPS = {
 'business_translation': [26,31,35,42,54,131,165,206,273,286],
 'variable_ontology': [41,166,175,180,189,204,239,269,270,283],
 'expert_evidence': [10,12,26,33,48,53,116,126,137,149,155,166,176,182,184,185,189,194,199,207,213,214,245,254,268,283,285],
 'diagram_construction': [10,26,33,41,53,108,125,131,176,184,214,245],
 'iid_discovery': [10,27,46,53,56,58,104,108,110,137,149,176,182,184,194,199,213,234,241,242],
 'latent_temporal_discovery': [40,60,110,148,180,199,263],
 'active_experiments': [12,42,139,141,165,234,271],
 'identification': [31,56,107,114,128,130,131,136,140,154,157,163,167,171,202,206,221,242,260,263,271,278],
 'data_code': [12,20,32,56,120,136,172,175,188,191,204,241,266,277],
 'longitudinal_policy': [74,122,148],
 'estimation_validation': [25,31,48,136,175,193,206,241,256,261,266,269,270,276,278],
 'reporting_monitoring': [35,110,138,196,246,259,273,282],
 'agent_architecture': [0,12,19,27,31,45,46,56,110,114,122,130,136,138,139,140,141,164,172,181,196,202,241,242,252,253,254,282,284],
 'evaluation_cost': [0,10,18,25,45,54,74,104,107,108,109,110,113,114,115,116,118,125,126,128,137,154,155,157,163,164,167,181,191,193,207,217,218,221,225,239,244,245,246,252,253,259,261,268,276,284,285,286],
}


def norm(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower())


def primary_sources():
    sources = []
    for spec in SPECS:
        raw = ROOT / ('docs/literature/raw/exec13_census_' + spec['key'] + '.pdf')
        receipt = raw.with_name(raw.stem + '.receipt.json')
        acq = read(receipt)
        assert acq['status'] == 'saved' and acq['sha256'] == sha(raw)
        assert raw.read_bytes().startswith(b'%PDF-') and spec['date'] <= CUTOFF
        text_path = BASE / (spec['key'] + '.txt')
        pages = text_path.read_text().split('\f')
        assert len(pages) - 1 == spec['pages']
        assert spec['version'] in pages[0]
        target = ROOT / 'docs/papers' / f"{spec['filename']} {spec['first']}({spec['year']}).pdf"
        if target.exists():
            assert sha(target) == sha(raw), 'Never overwrite a distinct original'
        else:
            shutil.copyfile(raw, target)
        anchors = []
        for number, finding in spec['anchors'].items():
            extract = BASE / 'inspected' / f"{spec['key']}-page-{number}.txt"
            extract.parent.mkdir(exist_ok=True)
            extract.write_text(pages[number - 1])
            anchors.append({'pdf_page': number, 'finding': finding, 'extract': ref(extract, 'Inspected physical PDF page')})
        sources.append({
            'integrated_citation_key': 'exec13_census_' + spec['key'], 'kind': 'paper',
            'title': spec['title'], 'filename_title': spec['filename'], 'first_author': spec['first'],
            'author': spec['author'], 'year': spec['year'], 'pages': spec['pages'],
            'source_identity': 'https://arxiv.org/abs/' + spec['version'],
            'version_date': 'arXiv:' + spec['version'] + '; ' + spec['date'],
            'accessed_utc': acq['accessed_utc'], 'cutoff': CUTOFF,
            'cutoff_basis': 'Inspected first-page version stamp; acquisition is later, not backdated.',
            'local_path': str(target.relative_to(ROOT)), 'sha256': sha(target),
            'local_copy': ref(raw, 'Authentic downloaded PDF; identical to named scholarly original'),
            'acquisition_receipt': ref(receipt, 'Original public acquisition receipt'),
            'extracted_text': ref(text_path, 'Searchable primary text; no replacement for PDF'),
            'inspected_anchors': anchors,
            'supported_claims': list(spec['anchors'].values()),
            'project_disposition': spec['role'], 'limits': spec['limits'],
            'source_status': 'selected_primary_identity_methods_results_and_limits_inspected',
            'execution': 'literature_inspection_only_no_local_replication',
            'reconciles': f"LA01-candidate-{spec['candidate']}",
        })
    inherited = read(PRIOR)['sources']
    for key in ['exec13_hallucination', 'exec13_pulse']:
        source = next(s for s in inherited if s['integrated_citation_key'] == key)
        assert sha(ROOT / source['local_path']) == source['sha256']
        sources.append(source)  # exact preservation avoids conflicting current-reader citation records
    write(BASE / 'source-audit.json', {'cutoff': CUTOFF, 'inspection_date': '2026-10-13',
          'status': 'bounded_primary_tranche_not_census_closure', 'sources': sources,
          'inherited_source_audit': ref(PRIOR, 'Preserved audit for two reconciled later acquisitions'),
          'technical_claim_scope': 'Only the inspected anchors; paper-reported findings are not locally reproduced implementations.'})
    return sources


def census(sources):
    old = read(OLD / 'omissions.json')
    candidates = {c['id']: c for c in read(OLD / 'screening-candidates.json')}
    source_by_candidate = {s['reconciles']: s for s in sources if s.get('reconciles')}
    source_by_candidate['LA01-candidate-10'] = next(s for s in sources if s['integrated_citation_key'] == 'exec13_hallucination')
    source_by_candidate['LA01-candidate-110'] = next(s for s in sources if s['integrated_citation_key'] == 'exec13_pulse')
    items = []
    for original in old['items']:
        item = {'id': original['id'], 'inherited_record': original,
                'inherited_evidence': ref(OLD / 'omissions.json', 'items[id=' + original['id'] + ']')}
        if 'candidate_id' in original:
            number = int(original['id'].rsplit('-', 1)[-1])
            c = candidates[original['candidate_id']]
            tasks = [t for t, ids in GROUPS.items() if number in ids]
            assert tasks, original['id']
            item.update(candidate_identity=c['id'], title=c['title'], discovery_date=c.get('date'),
                        discovery_doi=c.get('doi'), search_provenance=c['queries'], task_families=tasks,
                        mapping_basis='Manual provisional mapping from title and original search provenance; primary support limited to explicit inspected source claims.',
                        metadata=ref(OLD / 'screening-candidates.json', 'id=' + c['id']))
            if original['id'] in source_by_candidate:
                s = source_by_candidate[original['id']]
                item.update(disposition='inspected_primary_retained_with_limits', source_key=s['integrated_citation_key'],
                            source=ref(ROOT / s['local_path'], 'Inspected version; no assumption of identity with later publisher version'),
                            primary_review=ref(BASE / 'source-audit.json', 'sources[integrated_citation_key=' + s['integrated_citation_key'] + ']'),
                            effect_on_claims=s.get('limits'),
                            next_action='Use only inspected claims and version; execute separate code/license/oracle or target-assumption review before empirical capability claims.',
                            technical_source_review_open=False, runtime_admission=False)
            else:
                lead = next((u for u in original.get('acquisition_leads', []) if u.startswith('https://')), None)
                item.update(disposition='open_original_not_inspected', technical_source_review_open=True,
                            availability='Not newly tested in this tranche; no assertion of unavailability or exclusion.',
                            effect_on_claims='No technical or completeness claim may rely on this title; its affected task family remains bounded.',
                            next_action=('Acquire the authentic original via ' + lead + '; ' if lead else 'Resolve an authentic original source identity; ') +
                            'verify version against cutoff, inspect method and adverse-result anchors, then retain, justify exclusion, or record a real acquisition failure.')
        else:
            cross = {
                'LA01-longitudinal-search': (['longitudinal_policy','latent_temporal_discovery','evaluation_cost'], 'open_search_specificity_and_saturation',
                    'Six complementary searches completed; broad relevance and top-ten bounds prevent specialist saturation. CausalCollab is a directly inspected longitudinal candidate.',
                    'Use tighter title/abstract queries and backward/forward chains from CausalCollab, with a new declared batch budget.'),
                'LA01-runtime-licenses': (['agent_architecture','data_code'], 'open_runtime_adoption',
                    'No new package license, weights or executable dependency audit was performed by primary-paper inspection.',
                    'Audit exact LLM-CD, LLM-and-SCD and LCM source/weights/dependency identities before proposing executable admission.'),
                'LA01-benchmark-oracles': (['identification','evaluation_cost','estimation_validation'], 'open_benchmark_qualification',
                    'CLadder IV and CausalDS unknown-ID/nonfinite-score issues survive; new benchmark scores cannot resolve them.',
                    'Verify benchmark equations and code branches against independent causal oracles and preserve failing cases.'),
                'LA01-bank-evidence': (list(GROUPS), 'conditional_later_bank_product_evidence',
                    'Current proposal scope permits public/generated evidence. Authentic bank truth and adoption remain necessary only for later bank/product claims.',
                    'Revisit after a bounded prototype identifies a decision-relevant bank uncertainty and a justified experiment; continue proposal work now.'),
            }
            tasks,status,reason,action = cross[original['id']]
            item.update(task_families=tasks, mapping_basis='Explicit inherited cross-cutting issue and current proposal scope',
                        disposition=status, effect_on_claims=reason, next_action=action,
                        scope=ref(ROOT / 'docs/program/master-program-proposal.md', 'Proposal now versus conditional bank/product evidence'))
        items.append(item)
    assert len(items) == 117 and len({x['id'] for x in items}) == 117
    counts = dict(collections.Counter(x['disposition'] for x in items))
    write(BASE / 'census-register.json', {'status':'incomplete_explicit_dispositions', 'cutoff': CUTOFF,
          'counts': counts, 'items': items, 'closure': False,
          'interpretation':'All inherited IDs accounted for; accounting is not technical closure. 101 titles still require primary review. No unread title was excluded.'})
    tasks = []
    for task in GROUPS:
        rows = [x for x in items if task in x['task_families']]
        tasks.append({'id':task, 'inherited_ids':[x['id'] for x in rows],
                      'inspected_source_keys':[x['source_key'] for x in rows if x.get('source_key')],
                      'uninspected_candidate_ids':[x['id'] for x in rows if x['disposition']=='open_original_not_inspected'],
                      'coverage_acceptance':False})
    write(BASE / 'task-map.json', {'task_families':tasks, 'mapping_does_not_establish_depth_or_completeness':True,
                                 'register':ref(BASE / 'census-register.json','All 117 dispositions')})
    return items


# Manual metadata relevance screening for each provider/rank. This is discovery
# triage only; the candidate originals are not excluded by these labels.
TRIAGE = {
 'crossref_longitudinal':['direct','direct','direct','adjacent','direct','adjacent','adjacent','adjacent','peripheral','peripheral'],
 'crossref_negative':['direct','direct','adjacent','direct','direct','adjacent','direct','adjacent','adjacent','adjacent'],
 'crossref_offpolicy':['direct','direct','direct','direct','adjacent','adjacent','adjacent','direct','adjacent','adjacent'],
 'openalex_longitudinal':['direct','adjacent','adjacent','adjacent','adjacent','adjacent','adjacent','adjacent','adjacent','adjacent'],
 'openalex_negative':['adjacent','adjacent','adjacent','direct','adjacent','adjacent','direct','adjacent','direct','direct'],
 'openalex_offpolicy':['direct','adjacent','direct','adjacent','adjacent','direct','adjacent','adjacent','adjacent','adjacent'],
}


def searches(items, sources):
    prior_sources = read(PRIOR)['sources'] + sources
    candidates = read(OLD / 'screening-candidates.json')
    searches, leads = [], []
    for suffix, labels in TRIAGE.items():
        p = ROOT / ('docs/literature/raw/exec13_census_' + suffix + '.json')
        receipt = p.with_name(p.stem + '.receipt.json')
        acq, data = read(receipt), read(p)
        assert acq['status']=='saved' and acq['sha256']==sha(p)
        is_oa = suffix.startswith('openalex')
        rows = data['results'] if is_oa else data['message']['items']
        assert len(rows)==10
        for rank,(row,label) in enumerate(zip(rows, labels),1):
            title = row['title'] if is_oa else ' '.join(row['title'])
            doi = row.get('doi') if is_oa else row.get('DOI')
            title_key = norm(title)
            title_matches = [c['id'] for c in candidates if norm(c['title']) == title_key]
            arxiv_ids = set(re.findall(r'\d{4}\.\d{4,5}', doi or ''))
            existing = sorted({s['integrated_citation_key'] for s in prior_sources
                               if norm(s.get('title',''))==title_key or arxiv_ids.intersection(re.findall(r'\d{4}\.\d{4,5}', str(s.get('source_identity',''))))})
            reason = {'direct':'Title describes causal analysis using language models, or evaluation of that capability; retain as a primary-inspection lead.',
                      'adjacent':'Title concerns general causal methods or general language-model evaluation/architecture; retain as contextual lead, with specialist relevance unverified.',
                      'peripheral':'Title concerns poetic analogy or hyperparameter optimization without a declared causal-inference task; low priority at metadata stage, not a full-text exclusion.'}[label]
            leads.append({'id':suffix + '-rank-' + str(rank), 'title':title,'doi':doi,
                          'provider_identity':row.get('id',row.get('URL')), 'rank':rank,
                          'date_metadata':row.get('publication_date', row.get('published')),
                          'source':ref(p, ('results' if is_oa else 'message.items') + '[' + str(rank-1) + ']'),
                          'disposition':'metadata_only_' + label + '_lead','reason':reason,
                          'inherited_identity_matches':title_matches,'existing_source_identity_leads':existing,
                          'version_equality_established':False,
                          'next_action':'Resolve exact original/version and inspect primary anchors; a title/DOI match does not establish version equality.'})
        searches.append({'id':suffix, 'provider':'OpenAlex' if is_oa else 'Crossref',
                         'request_url':acq['url'],'accessed_utc':acq['accessed_utc'],
                         'cutoff':CUTOFF,'returned':len(rows),
                         'provider_total':data['meta']['count'] if is_oa else data['message']['total-results'],
                         'local_copy':ref(p,'Saved discovery metadata only'),'receipt':ref(receipt,'Original request outcome'),
                         'limit':'First ten ranked results only, no pagination. Broad lexical matching has weak specialist relevance; provider dates may be incomplete. No saturation or absence claim.'})
    unique = {norm(x['doi'] or x['title']) for x in leads}
    write(BASE / 'new-search-leads.json',{'leads':leads,'raw_count':60,'unique_doi_or_title_keys':len(unique),
          'interpretation':'Unique keys are discovery deduplication only, not source-version reconciliation.',
          'triage_counts':dict(collections.Counter(x['disposition'] for x in leads))})
    chains = [
        {'from':'exec13_census_causalsmith','page':17,'entry':'9','to':'exec13_census_orca',
         'basis':'ORCA arXiv identifier in bibliography; v3 primary inspected separately.'},
        {'from':'exec13_census_orca','page':6,'entry':'9','to':'exec13_census_causal_agent',
         'basis':'Han et al. arXiv identifier 2408.06849; inspected v3, later than the citing March 2026 ORCA version; citation does not endorse v3 results.'},
        {'from':'exec13_census_graph_validation','page':8,'entry':'17',
         'to':'v12_la_2305_00050','basis':'Kiciman et al. title/author identity; already local genuine original and audit. No transfer of secondary summary claims.'},
    ]
    old_by_key = {s['integrated_citation_key']:s for s in prior_sources}
    for chain in chains:
        for side in ['from','to']:
            s = old_by_key[chain[side]]
            local = ROOT / s['local_path']
            assert sha(local)==s['sha256']
            chain[side+'_original'] = ref(local,'Authentic version actually inspected in this or inherited audited work')
    requests = []
    for batch in ['fetch-search-01.json','fetch-02.json','fetch-03.json','fetch-04.json','fetch-05.json']:
        for req in read(BASE / batch)['requests']:
            rp = ROOT / ('docs/literature/raw/' + req['id'] + '.receipt.json')
            requests.append({'id':req['id'],'batch':ref(BASE / batch,'Submitted bounded request manifest'),
                             'receipt':ref(rp,'Preserved success or failure'), 'status':read(rp)['status'],
                             'error':read(rp).get('error')})
    assert len(requests)==18 and len({r['id'] for r in requests})==18
    write(BASE / 'search-ledger.json',{'status':'complementary_routes_and_chains_performed_specialist_closure_open',
          'searches':searches,'citation_chains':chains,'requests':requests,
          'budget':{'metadata_attempts':6,'primary_attempts':12,'primary_cap':16,'primary_successes':10,'primary_failures':2},
          'source_failures':'ACL host outside fixed collector allowlist. Preserved receipts; registered arXiv author-preprint alternatives used. Collector and permission boundaries unchanged.',
          'remaining_limits':['101 inherited candidate originals unread','Specialist search precision and saturation unresolved',
                              'Publisher versus preprint versions not presumed equal','Sixty leads individually screened only as metadata',
                              'No current-model benchmark, executable package adoption or bank validation performed']})


def main():
    sources = primary_sources()
    items = census(sources)
    searches(items, sources)
    print(json.dumps({'primary_records':len(sources),'new_originals':len(SPECS),
                      'inherited_items':len(items),'primary_reviewed_candidates':12,
                      'candidate_originals_still_open':101,'census_closed':False}))


if __name__ == '__main__':
    main()
