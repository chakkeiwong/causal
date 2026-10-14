#!/usr/bin/env python3
"""Assemble inspected dataset identities and an explicit, bounded survey register."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/public-data-v15'
RAW = ROOT / 'docs/literature/raw'


def ref(path, anchor):
    path = ROOT / path if isinstance(path, str) else path
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    sources = []
    def source(key, title, suffix, anchors, claims, license_note, pin=None, extras=()):
        p = RAW / (key + '.' + suffix)
        receipt = json.loads((RAW / (key + '.receipt.json')).read_text())
        text_path = BASE / (key + '.txt') if suffix == 'html' and (BASE / (key + '.txt')).exists() else p
        text = text_path.read_text()
        inspected = []
        for anchor in anchors:
            index = text.find(anchor)
            if index < 0:
                raise ValueError(key + ': missing inspected anchor ' + anchor)
            inspected.append(ref(text_path, 'Line ' + str(text[:index].count('\n') + 1) + ': ' + anchor))
        version = 'Official/distributor documentation snapshot accessed 2026-10-12; historical page bytes as of 2026-10-07 not established'
        artifacts = [ref(RAW / (key + '.receipt.json'), 'Public GET provenance')]
        if pin:
            h = RAW / ('pd15_' + pin + '_history.json')
            c = json.loads(h.read_text())[0]
            version = 'Git commit ' + c['sha'] + ' dated ' + c['commit']['committer']['date'] + '; selected at/before 2026-10-07 Asia/Shanghai cutoff'
            artifacts.append(ref(h, 'Repository commit identity only; technical claims use the inspected file'))
        for extra, anchor in extras:
            artifacts.append(ref(extra, anchor))
        sources.append({'integrated_citation_key': key, 'id': key, 'kind': 'documentation',
                        'name': title, 'title': title, 'source_identity': receipt['url'],
                        'version_date': version, 'accessed': receipt['accessed_utc'],
                        'local_copy': ref(p, 'Saved primary/distributor documentation bytes'),
                        'inspected_anchors': inspected, 'supported_claims': claims,
                        'license_observation': license_note, 'artifacts': artifacts,
                        'limits': ['Documentation inspection is not dataset execution or causal validation.',
                                   'Repository code license is not automatically a license for every linked dataset.']})
    source('pd15_uci_bank', 'UCI Bank Marketing dataset documentation', 'html',
           ['41188', 'duration: last contact duration', 'Creative Commons Attribution 4.0'],
           ['Two full versions and two smaller versions; bank term-deposit subscription target; contact duration field; stated CC BY 4.0 terms.'],
           'CC BY 4.0 stated on the custodian page; retain attribution.', extras=[('docs/program/public-data-v15/bank-profile.json', 'Actual bytes, shapes, missing-value sentinels and descriptive profile'), ('docs/datasets/public-v15/bank-marketing/ATTRIBUTION.md', 'Required source attribution, license link and no-byte-change extraction notice')])
    source('pd15_uci_credit', 'UCI Default of Credit Card Clients documentation', 'html',
           ['30000', 'April to September, 2005', 'Creative Commons Attribution 4.0'],
           ['30,000 records, 23 predictors, Taiwan payment/bill histories, default label; stated CC BY 4.0 terms.'], 'CC BY 4.0 stated; no archive acquired here.')
    source('pd15_fdic_sod', 'FDIC Summary of Deposits description', 'html',
           ['annual survey of branch office deposits as of June 30', 'institutions with only a main office are exempt'],
           ['Annual branch-office deposit survey with June 30 reference date and stated reporting population.'], 'Public government documentation; per-file redistribution terms not inspected.')
    source('pd15_fdic_api_spec', 'FDIC Bank Data API OpenAPI specification', 'txt',
           ['title: FDIC Bank Data API', '/financials:', '/history:', '/sod:'],
           ['API documents financial, structural-history and deposits routes and filters; an explicit vintage/data-dictionary inspection remains necessary.'], 'Public API documentation; endpoint/schema version 0.1.0, current snapshot; no API data run.')
    source('pd15_y9c', 'Federal Reserve FR Y-9C report description', 'html',
           ['Consolidated Financial Statements for Holding Companies', 'Quarterly, as of the last calendar day of the quarter', 'microdata are considered public information'],
           ['Consolidated holding-company balance sheet/income data; quarterly reporting; microdata public with exceptions.'], 'Public reporting description; access and field-specific disclosure exceptions remain.')
    source('pd15_h8', 'Federal Reserve H.8 release description', 'html',
           ['estimated weekly aggregated balance sheet', 'FRED database'],
           ['Weekly aggregate bank balance-sheet series and downloadable public data routes.'], 'Official government release documentation; no new series acquired.')
    source('pd15_scf', 'Federal Reserve 2022 Survey of Consumer Finances public data', 'html',
           ['10/9/2026', 'five times the number of actual observations', '4,595 families', 'triennial cross-sectional survey'],
           ['Multiple imputation and replicate-weight documentation; 2022 public data describe 4,595 families and 22,975 implicate rows; some summary files were updated after cutoff.'],
           'Public data described; current inflation-adjusted summary files dated 2026-10-09 are outside cutoff and excluded from proposed historical inputs.')
    source('pd15_hmda_schema', 'CFPB public HMDA LAR schema (2020 documentation)', 'md',
           ['activity\\_year', 'action\\_taken', 'interest\\_rate', 'income'],
           ['Historical public application schema includes lender, geography, action, income and loan-pricing fields; no monthly servicing history in this schema.'],
           'CFPB repository license preserved; current-year data privacy specification and downloaded file terms still require inspection.', pin='hmda',
           extras=[('docs/literature/raw/pd15_hmda_faq.md', 'Historical CSV/static-release scope, not a claim about current-year fields'), ('docs/literature/raw/pd15_hmda_license.txt', 'CFPB repository terms')])
    source('pd15_freddie', 'Freddie Mac Single-Family Loan-Level Dataset description', 'html',
           ['register and sign-in', 'Monthly loan performance data', 'free for non-commercial'],
           ['Origination and monthly performance information; registration; free uses are subject to applicable terms; commercial redistribution requires an agreement.'],
           'Registration and terms required; no account created, no terms accepted, no loan data acquired.')
    source('pd15_fannie', 'Fannie Mae Single-Family Loan Performance Data description', 'html',
           ['July 31, 2026', 'dynamic monthly performance', 'register and create a unique username', 'external commercial purposes'],
           ['Selected fixed-rate mortgage population; origination and monthly histories; HARP mapping; registration and commercial/redistribution restrictions.'],
           'No account created or data acquired. Product use and redistribution require a permission determination.')
    source('pd15_criteo', 'Criteo Uplift Modeling Dataset description and terms', 'html',
           ['25M rows', 'original incrementality level cannot be deduced', 'Attribution-NonCommercial-ShareAlike'],
           ['Advertising holdout trials underlying a 25-million-row, 11-feature benchmark; privacy transformation; CC BY-NC-SA 4.0.'],
           'Noncommercial/share-alike restrictions; commercial-proposal eligibility is unresolved, so execution is deferred.')
    source('pd15_nsw_docs', 'causaldata nsw_mixtape dataset documentation', 'txt',
           ['445 rows and 11 variables', 'job-training program experiment'],
           ['445-row NSW experimental job-training extract and earnings variables; distinct from observational comparison variants.'],
           'Distributor documentation inspected; original trial design, archive identity and data-specific rights must be checked before an effect claim.')
    source('pd15_lalonde_pinned', 'MatchIt lalonde comparison-sample documentation', 'txt',
           ['614 observations', 'comparison sample from the'],
           ['614-row data combine NSW treated group and PSID comparison sample; not the all-randomized trial dataset.'],
           'Data-specific reuse rights not established by this documentation alone.', pin='lalonde')
    source('pd15_acic_pinned', 'ACIC 2016 competition repository documentation', 'md',
           ['2016 competition', 'aciccomp2016'],
           ['Competition provides simulation tooling; primary generator/input manuals specify potential outcomes and empirical covariates.'],
           'R package DESCRIPTION states GPL >=2; empirical input-data lineage and rights require separate review.', pin='acic',
           extras=[('docs/literature/raw/pd15_acic_description.txt', 'Version 0.1-0; 2017-05-20; package terms'),
                   ('docs/literature/raw/pd15_acic_dgp.txt', 'Simulation generator, potential outcomes and treatment'),
                   ('docs/literature/raw/pd15_acic_input.txt', 'Covariate inputs')])
    source('pd15_cevae_pinned', 'CEVAE IHDP benchmark documentation', 'md',
           ['IHDP, being a synthetic dataset', 'mu1 and mu0', 'will not be updated'],
           ['This IHDP benchmark contains generated potential outcomes and conditional means; legacy code is unmaintained.'],
           'Data-specific rights unresolved; do not install legacy TensorFlow/Edward merely to read data.', pin='cevae')
    source('pd15_nhefs_pinned', 'causallib NHEFS and ACIC loader source', 'txt',
           ['def load_nhefs(', 'def load_nhefs_survival(', 'real covariates but synthetically simulates'],
           ['NHEFS is observational smoking cessation with follow-up/censoring; the loader explicitly distinguishes ACIC observed covariates from simulated assignments/outcomes.'],
           'Loader/distributor reviewed; upstream data terms and exact cohort exclusions need separate verification.', pin='nhefs')
    source('pd15_mpdta', 'did mpdta county teen employment dataset documentation', 'txt',
           ['2500 rows', '500 counties', 'not a'],
           ['500 counties over 2003-2007; first treatment year; ever-treated indicator is not period-specific exposure.'],
           'Current development documentation snapshot; freeze package release and data terms before executing; no data acquired.')
    source('pd15_causalbench_pinned', 'CausalBench perturbation benchmark documentation', 'md',
           ['Observational and partial interventional', 'over 200 000', 'CC-BY-NC'],
           ['Large biological perturbation benchmarks; several training regimes; component data sources have different licenses.'],
           'Core data and auxiliary knowledge resources have different terms, including a noncommercial resource; inspect only the selected components.', pin='causalbench')
    source('pd15_febrl_source', 'Python Record Linkage Toolkit FEBRL dataset loader', 'txt',
           ['def _febrl_links', '500 original and', '5000 duplicate records'],
           ['Generated identity records, duplicate structure, and true-link labels; FEBRL4 contains two 5,000-row tables.'],
           'Synthetic data supplied by toolkit; verify generator and data-specific attribution/license before redistribution.')
    source('pd15_paysim_pinned', 'PaySim simulator documentation', 'md',
           ['generated synthetic data', 'aggregated transactional data'],
           ['Synthetic mobile-money transactions modeled using a service schema and later aggregate logs; not disclosed bank transactions.'],
           'Code and linked Kaggle dataset may have different terms; dataset terms not acquired; optional simulator only.', pin='paysim')
    source('pd15_cladder_pinned', 'CLadder benchmark documentation', 'md',
           ['Number of questions: 10,112', 'cladder-v1-meta-models.json', 'q-nonsense'],
           ['Generated causal questions with reconstructible model information and semantic variants; suitable for controlled reasoning tasks.'],
           'Source documentation inspected; dataset/generator license must be checked before redistribution or training.', pin='cladder')
    source('pd15_corr2cause_pinned', 'Corr2Cause benchmark documentation', 'md',
           ['data_gen.cpp', 'D-seperation check', 'Markov Equivalence class'],
           ['Generated conditional-independence/causal-relation tasks and variable/paraphrase variants; three-class supplement includes underdetermination.'],
           'Documentation inspected; freeze dataset split and terms before a live benchmark.', pin='corr2cause')
    inherited = json.loads((ROOT / 'docs/program/gap-execution-v13_1/reader/source-audit.json').read_text())
    for k in ['public401k', 'public_macrodata_dynamic']:
        sources.append(next(x for x in inherited['sources'] if x['integrated_citation_key'] == k))
    sources.append({'integrated_citation_key': 'pd15_profile', 'kind': 'project_evidence',
                    'title': 'Public bank-data descriptive profile', 'source_identity': 'Original project inspection',
                    'version_date': '2026-10-12', 'local_copy': ref(BASE / 'bank-profile.json', 'All observed counts'),
                    'inspected_anchors': [ref(ROOT / 'tools/profile_public_bank_data.py', 'No fitting or inference; archive and row parsing')],
                    'supported_claims': ['Only the reported descriptive counts and observed schema.'],
                    'limits': ['Not a new treatment-effect experiment or prototype qualification.']})
    write('source-audit.json', {'status': 'pass', 'issues': [], 'cutoff': '2026-10-07',
                               'access_date': '2026-10-12', 'sources': sources,
                               'scope': 'Inspected dataset/software documentation and preserved project evidence. No newly cited scholarly result or paper has been substituted by a summary.'})
    print(json.dumps({'sources': len(sources), 'status': 'source_anchors_bound'}))


if __name__ == '__main__':
    main()
