#!/usr/bin/env python3
"""Bind inspected commercial identification sources and unresolved comparisons."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-identification'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    assert not (BASE / 'source-audit.json').exists(), 'Preserve the completed audit'
    acquisition = json.loads((BASE / 'acquisition-review.json').read_text())
    assert len(acquisition['requests']) == 27
    records = {r['id']: r for r in acquisition['requests']}
    specifications = [
        ('bayesia_criteria', 'BayesiaLab: Graphical Identification Criteria', 'Bayesia',
         'Mutable official e-book section, edition unspecified, acquired 2026-10-13',
         ['The Adjustment Criterion (Shpitser', 'Unobserved Confounders', 'Given that UUU is hidden'],
         ['The vendor explains path-based adjustment in a supplied DAG and the obstruction in its specific unobserved-common-cause example.'],
         'This example is not a complete ID/IDC implementation specification, nor a proof that every graph with hidden confounding is nonidentified.'),
        ('bayesia_surgery', 'BayesiaLab: Causal Effect Estimation with Graph Surgery', 'Bayesia',
         'Mutable official e-book technical walkthrough, edition unspecified, acquired 2026-10-13',
         ['We have already defined a causal graph', 'BayesiaLab can help us review the paths', 'In BayesiaLab, Graph Surgery is automated.', 'By intervening on Treatment'],
         ['The walkthrough documents supplied-graph/data association, parameter estimation, path display and menu-driven intervention by removing inbound arcs.'],
         'No vendor runtime executed. Identification of a latent-confounded observed law is not obtained merely by applying this menu.'),
        ('bayesia_matching', 'BayesiaLab: Causal Effect Estimation with Likelihood Matching', 'Bayesia',
         'Mutable official e-book technical walkthrough, edition unspecified, acquired 2026-10-13',
         ['With BayesiaLab’s Likelihood Matching', 'How can we overcome this?', 'For now, Likelihood Matching'],
         ['The documented example matches confounder distributions with probabilistic evidence and Fix Probabilities, giving the same example effect as graph surgery.'],
         'A documented adjustment workflow, not certified general identification, statistical calibration or an executed adapter.'),
        ('bayesia_counterfactual', 'BayesiaLab: Calculating Contributions Using Causal Counterfactuals', 'Bayesia',
         'Mutable webinar technical description with linked 2019-06-26 slides; page acquired 2026-10-13',
         ['Both types rely on computing', 'From this generated data', 'In this webinar, we perform'],
         ['The page describes contribution calculations from factual/intervention contrasts using generated data, expert confounder assumptions and Likelihood Matching.'],
         'Slides and recording were not inspected. The text does not specify an arbitrary individual-level abduction model or establish its cross-world coupling.'),
        ('stata_causal_intro', 'Stata Causal Inference and Treatment-Effects Reference: teffects intro', 'StataCorp',
         'Manual copyright 1985–2025, r19 example data; acquired 2026-10-13, exact cutoff bytes unauthenticated',
         ['The teffects command estimates', 'The independent and identically distributed', 'The conditional-independence (CI)', 'the third assumption, overlap'],
         ['Manual documents ATE/ATET/potential-outcome means and RA/IPW/AIPW/IPWRA/matching families.',
          'Its caveats describe IID sampling, conditional independence and overlap; a command fit alone cannot verify those assumptions.'],
         'No software execution, entitlement, unknown-confounding robustness, generic graph ID or individual counterfactual inference inferred.'),
        ('stata_mediate', 'Stata Causal Inference and Treatment-Effects Reference: mediate, one mediator', 'StataCorp',
         'Manual copyright 1985–2025, r19 example data; acquired 2026-10-13, exact cutoff bytes unauthenticated',
         ['mediate fits causal mediation models', 'There are no confounders in the mediator', 'Assumptions for causal identification', 'The first assumption states that treatment assignment'],
         ['Manual documents natural direct/indirect/total effects, modeled potential-outcome means, treatment–mediator interaction and variance options.',
          'The causal interpretation requires treatment/mediator ignorability, overlap and no treatment-induced mediator–outcome confounder under the stated model.'],
         'Nested population mediation targets differ from an individual’s realized alternative outcome. No general graph discovery or ID/IDC API established.'),
        ('bayesserver_causality', 'Bayes Server: Introduction to Causal AI', 'Bayes Server',
         'Official page copyright 2025; specific helpers described for version 10+, calculations 9.4+; acquired 2026-10-13',
         ['Bayes Server supports both discrete and continuous', 'Use the Abduction dialog', 'You can perform the same calculations with 9.4', 'Popular approaches are listed below'],
         ['Guide documents interventions and an explicit evidence→abduction→intervention workflow with characteristic variables.',
          'Guide names back-door, front-door, instruments and do-calculus as approaches, saying many are available from version 10 onward.'],
         'The general list does not establish exactly which algorithms, completeness domains, counterfactual identifiers or API contracts are implemented; technical followup remains essential.'),
        ('mplus_mediation', 'Mplus: Mediation Analysis resource index', 'Muthen and Muthen',
         'Mutable official index, acquired 2026-10-13; page shows 2026-10-12 and links Version 7.2 syntax',
         ['using the Version 7.2 MODEL INDIRECT language', 'Counterfactual causal effects for mediation modeling', 'View Mplus inputs, data, and outputs'],
         ['Official index supplies specific counterfactual-mediation and MODEL INDIRECT leads requiring original technical inspection.'],
         'Discovery/identity only. Linked scholarly works were not newly acquired or cited as inspected papers; no theorem or software completeness awarded.')]
    sources = []
    for key, title, author, version, markers, claims, limits in specifications:
        r = records[key]
        assert r['status'] == 'extracted_primary_candidate'
        text_path = ROOT / r['text_copy']['path']
        lines = text_path.read_text().splitlines()
        anchors = []
        for marker in markers:
            found = [i for i, line in enumerate(lines) if marker in line]
            assert found, (key, marker)
            i = found[-1] if marker == 'Assumptions for causal identification' else found[0]
            anchors.append({'anchor': f'Extracted technical text lines {i+1}–{min(i+3,len(lines))}',
                            'quote': '\n'.join(lines[i:i+3])})
        raw = ROOT / r['raw_copy']['path']
        sources.append({'integrated_citation_key': 'exec13_ci_' + key,
                        'kind': 'official_documentation', 'title': title, 'author': author, 'year': 2026,
                        'source_identity': r['url'], 'version_date': version, 'cutoff': '2026-10-07',
                        'accessed_utc': datetime.fromtimestamp(raw.stat().st_mtime, timezone.utc).isoformat(),
                        'cutoff_limit': 'Acquisition after cutoff; described version dates do not authenticate exact historical page bytes.',
                        'local_copy': ref(raw, 'Authentic vendor primary bytes'),
                        'text_copy': ref(text_path, 'Extracted text; raw bytes authoritative'),
                        'inspected_anchors': anchors, 'supported_claims': claims, 'limits': limits})
    protocol = json.loads((BASE / 'search-protocol.json').read_text())
    details = {
        'BayesFusion': ('adjacent_primary_only', 'Preserved GeNIe/SMILE structure/pattern/license manuals; new causal URL failed and index is navigation only.', 'Acquire exact causal evidence/query method, supported graph class and wrapper/edition contract. Do not infer an absence from the failed URL.'),
        'Bayesia': ('documented_adjustment_workflow', 'Supplied-DAG path analysis, graph surgery, likelihood matching and contribution walkthrough; edition/API uncertainty remains.', 'Inspect versioned API/export and complete identification/counterfactual semantics; compare prices and deployment rights later.'),
        'HUGIN Expert': ('essential_source_unavailable', 'Preserved manual acquisition failed; no new vendor claim.', 'Obtain accessible official inference/decision and causal-identification technical manuals with version and license.'),
        'Norsys': ('adjacent_primary_only', 'Preserved Netica learning manuals cover adjacent supplied-model/structure topics.', 'Acquire exact intervention/counterfactual semantics, method boundaries and license; never substitute learning/inference for identification.'),
        'StataCorp': ('documented_treatment_and_mediation', 'Primary treatment-effect and one-mediator manuals contain targets, algorithms and assumptions.', 'Review versioned identification/extensibility and other endogeneity commands separately; generic ID/IDC and individual abduction remain unknown.'),
        'SAS': ('essential_source_unavailable', 'CAUSALTRT/CAUSALMED PDF transfers incomplete; HTML followups failed. Earlier CALIS/VARMAX sources do not answer this query.', 'Acquire genuine versioned CAUSALTRT/CAUSALMED technical text, execution/API terms and assumptions. Partial response bytes are not evidence.'),
        'IBM': ('essential_source_unavailable', 'Earlier SPSS temporal/SEM sources do not establish this cell; dynamic help routes had returned documentation shells.', 'Acquire edition-specific SPSS causal/Amos identification/counterfactual methods and distinguish latent SEM from causal identification.'),
        'Mplus': ('technical_leads_only', 'Official index names counterfactual mediation, Version 7.2 MODEL INDIRECT and originals/examples.', 'Acquire genuine named PDFs plus syntax/technical appendices before causal-theorem or API claims; keep these scholarly candidates uncited pending audit.'),
        'MathWorks': ('essential_source_unavailable', 'Earlier public documentation access returned 403; no treatment-identification manual inspected here.', 'Obtain accessible official target/assumption/runtime documentation; arbitrary fitted prediction cannot count as intervention identification.'),
        'causaLens': ('login_required', 'Documentation redirects to a login page; HTTP 200 does not mean technical access.', 'Use openly available technical documentation or authorized material if later supplied; no login, terms acceptance or paid trial attempted.'),
        'EViews': ('adjacent_primary_only', 'Preserved structural VAR navigation does not establish arbitrary intervention/counterfactual identification.', 'Obtain model-specific identification, scenario and API/edition documentation.'),
        'OxMetrics': ('essential_source_unavailable', 'Preserved PcGive/PcGets/Autometrics leads lack the matched current technical texts.', 'Acquire versioned structural-equation identification and intervention documentation, including restrictions and variance scope.'),
        'Scientific Software International': ('essential_source_unavailable', 'LISREL is retained as a SEM candidate without a matched technical identification audit.', 'Inspect the versioned primary manual, latent model restrictions, fit/identification distinctions and licensed embedding rights.'),
        'Bayes Server': ('documented_intervention_and_abduction', 'Official guide documents supplied-model interventions and characteristic-variable abduction with explicit version thresholds.', 'Inspect linked Advanced Causal Query and Abduction manuals, exact API/graph classes and edition/license; approach list does not prove complete ID/IDC.'),
        'JMP': ('essential_source_unavailable', 'Two bounded official routes returned 404.', 'Locate authentic versioned treatment/causal manuals and entitlements; failed guesses are not a negative capability finding.'),
        'Lumina': ('essential_source_unavailable', 'Two bounded Analytica routes returned 404.', 'Locate influence-diagram/intervention and Analytica Decision Engine documentation, and distinguish supplied decisions from causal identification.')}
    corpus = sorted(set([ROOT / r['text_copy']['path'] for r in records.values() if r.get('text_copy')]
                        + [ROOT / x['path'] for x in json.loads((BASE / 'local-search.json').read_text())['corpus']]))
    candidates = []
    for candidate in protocol['candidate_universe']:
        vendor = candidate['vendor']; status, finding, action = details[vendor]
        searches = []
        for alias in dict.fromkeys([vendor] + candidate['aliases']):
            hits = []
            for p in corpus:
                lines = p.read_text(errors='replace').splitlines()
                numbers = [i for i, line in enumerate(lines, 1) if re.search(re.escape(alias), line, re.I)]
                if numbers:
                    hits.append({'path': str(p.relative_to(ROOT)), 'count': len(numbers), 'first_lines': numbers[:4]})
            searches.append({'alias': alias, 'matches': hits})
        candidates.append({**candidate, 'status': status, 'finding': finding, 'next_action': action,
                           'alias_searches': searches, 'world_market_absence_claim': False,
                           'runtime_executed': False, 'edition_price_verified': False})
    write('candidate-register.json', {'cutoff': '2026-10-07', 'families': candidates,
                                      'public_gets': 27, 'corpus': [ref(p, 'Literal alias search corpus') for p in corpus],
                                      'limit': 'Declared finite corpus and official routes; no exhaustive web/market or exact-cutoff coverage claim'})
    omissions = [{'vendor': c['vendor'], 'gap': c['next_action'], 'essential_to_full_cell': True,
                  'revisit_trigger': 'Authentic versioned technical/rights material becomes accessible under the existing research authorization.'} for c in candidates]
    write('omissions-register.json', {'entries': omissions, 'unavailable_original_policy': 'Do not cite the linked Mplus originals as read or replace missing papers with summaries.',
                                      'later_optional': ['Licensed vendor runtime parity', 'Actual price/entitlement comparison'],
                                      'proposal_route': 'Use documented comparisons with explicit unknowns; recommend exact public fixtures and bounded open-source prototype; no bank experiment required for this survey.'})
    examples = BASE / 'exact-results.json'
    sources.append({'integrated_citation_key': 'exec13_ci_examples', 'kind': 'project_derivation',
                    'title': 'Exact lending identification, counterfactual coupling and monetary-bound constructions',
                    'author': 'Causal banking proposal project', 'year': 2026,
                    'source_identity': 'Project stipulated finite probability laws with exact rational verification',
                    'version_date': '2026-10-13, no random draws or vendor execution',
                    'local_copy': ref(examples, 'Four exact examples and hypothetical monetary mapping'),
                    'code': ref(ROOT / 'tools/commercial_identification_examples_20261013.py', 'Exact enumeration and independent front-door/structural evaluation'),
                    'inspected_anchors': ['observational_equivalence', 'partial_identification: 16 vertices', 'frontdoor', 'cross_world', 'planning_economics'],
                    'supported_claims': ['Equal positive observed laws have effects 0 and 1/2.', 'Sharp consistency-only ATE bounds are [-1/4,3/4].',
                                         'Specified front-door law gives 6/25 versus naive 11/25.', 'Equal randomized margins leave a selected individual counterfactual probability 0 or 1.',
                                         'Hypothetical USD 1000 value and USD 20 cost imply net bounds [-270,730] per offer.'],
                    'limits': 'No fitted vendor results, sampled calibration, bank data, external prices or measured ROI.'})
    sources.append({'integrated_citation_key': 'exec13_ci_scope', 'kind': 'project_evidence',
                    'title': 'Bounded commercial identification and counterfactual coverage register',
                    'author': 'Causal banking proposal project', 'year': 2026,
                    'source_identity': 'Declared sixteen-family search and preserved acquisition records',
                    'version_date': '2026-10-13 with 2026-10-07 cutoff limitations',
                    'local_copy': ref(BASE / 'candidate-register.json', 'All candidate/alias dispositions'),
                    'omissions': ref(BASE / 'omissions-register.json', 'Essential unclosed comparisons'),
                    'acquisition': ref(BASE / 'acquisition-review.json', '27 bounded reads including failed transfers and login page'),
                    'inspected_anchors': ['families', 'public_gets', 'corpus'],
                    'supported_claims': ['Scope, unavailable material and proposed evidence-sensitive comparison routes are explicit.'],
                    'limits': 'No market-wide absence or current/cutoff completeness claim.'})
    write('source-audit.json', {'sources': sources, 'cutoff': '2026-10-07', 'original_gap_qualification': False,
                               'runtime_executed': False, 'acquisition_review': ref(BASE / 'acquisition-review.json', 'Observed results'),
                               'normalizer': ref(ROOT / 'tools/normalize_commercial_identification_20261013.py', 'Extraction code'),
                               'audit_preparer': ref(Path(__file__), 'Inspected claims/anchors and explicit omissions')})
    print(json.dumps({'sources': len(sources), 'families': len(candidates), 'public_gets': 27, 'cell_coverage': 'inconclusive'}))


if __name__ == '__main__':
    main()
