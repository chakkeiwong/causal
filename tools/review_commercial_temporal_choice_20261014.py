#!/usr/bin/env python3
"""Compare archived commercial temporal paths with the actual local contract."""
import json
from pathlib import Path
import sys

import commercial_temporal_examples_20261013 as exact
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, write

ROOT = core.ROOT
sys.path.insert(0, str(ROOT / 'src'))
BASE = ROOT / 'docs/program/execution/2026-10-14/commercial-temporal-choice'
OLD = ROOT / 'docs/program/execution/2026-10-13/commercial-temporal'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work/SW.COMM.discovery_temporal_interventional/vendor-comparison.json'
OP = 'SW.COMM.discovery_temporal_interventional'


def main():
    assert not OUTPUT.exists() and (not BASE.exists() or not any(BASE.iterdir()))
    BASE.mkdir(exist_ok=True)
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    original = json.loads((OLD / 'candidate-register.json').read_text())
    audited = json.loads((OLD / 'source-audit.json').read_text())
    sources = {s['integrated_citation_key']: s for s in audited['sources']}
    companion = json.loads((ROOT / 'docs/program/execution/2026-10-13/commercial/source-audit.json').read_text())
    for s in companion['sources']:
        sources.setdefault(s['integrated_citation_key'], s)
    assert len(original['candidates']) == 13 and len(original['remaining_families']) if isinstance(original['remaining_families'], list) else original['remaining_families'] == 7
    # Exact reference under the preserved law; no vendor program is run.
    fresh = exact.calculate()
    saved = json.loads((OLD / 'exact-results.json').read_text())
    assert fresh == saved
    assert set(__import__('causalbank.operation_service_v12', fromlist=['SUPPORTED']).SUPPORTED) == {
        'capabilities.describe', 'graph.review', 'identify.effect', 'estimate.effect',
        'sensitivity.evaluate', 'audit.observation'}
    specifications = {
      'BayesFusion': {
        'sources': ['exec13_ct_genie_dbn', 'exec13_ct_genie_learning', 'exec13_ct_smile_tutorial', 'exec13_smile_intro', 'exec13_smile_license'],
        'strength': 'Stationary supplied dynamic Bayesian networks, fixed-structure discrete DBN EM, temporal evidence and inference with explicit slice and state mapping.',
        'current_gap': 'No local DBN fitter or temporal belief-update engine; temporal graph discovery and action-effect uncertainty are also unimplemented.',
        'proposed_route': 'Consider licensed supplied-model inference/parameter-fit adapter, then matched clock/state/lag/initial-transition tests. Do not describe fixed-structure learning as dynamic graph discovery.',
        'deployment': 'Proprietary C++ engine and named Java/Python/R wrappers; wrapper temporal parity unverified; separate development/server/distribution rights described.',
        'license': 'Commercial development and deployment terms require selected configuration; no agreement accepted.',
        'price': 'Unavailable in inspected material.'},
      'Bayesia': {
        'sources': ['exec13_ct_bayesia_inference', 'exec13_ct_bayesia_identification', 'exec13_bayesia_api', 'exec13_bayesia_professional'],
        'strength': 'Asserted-graph intervention analysis; identification and estimation are distinguished. Configuration-specific Java learning versus REST inference is documented.',
        'current_gap': 'No installed graph-surgery or likelihood-matching adapter; the library only supports narrower supplied-DAG checks and deterministic references.',
        'proposed_route': 'Compare one supplied-graph intervention problem after checking selected edition/API semantics, custody, supported unavailable results and temporal restrictions.',
        'deployment': 'Inspected API table places Java configurations on customer servers and REST model storage on vendor servers in France; license validation needs connectivity.',
        'license': 'Development/production and model-instance terms are configuration dependent; current contract not accepted.',
        'price': 'A public price-list link exists, but no version-matched numeric amount was verified.'},
      'StataCorp': {
        'sources': ['exec13_ct_stata_granger', 'exec13_ct_stata_svar', 'exec13_ct_stata_ivsvar'],
        'strength': 'Reduced-form Granger tests; short/long-run SVAR restrictions; single/multiple target IV-SVAR with normalization and GMM cluster/HAC options.',
        'current_gap': 'The library has no VAR/SVAR/IV-SVAR estimation or structural impulse-response workflow and no bank instrument-validation evidence.',
        'proposed_route': 'Use a declared restriction/instrument/normalization benchmark; compare whole answer, identified alternatives, variance interpretation and model-check refusal.',
        'deployment': 'Command-script manuals document estimators; licensed edition, OS, automation/export and target runtime behavior not evaluated.',
        'license': 'Commercial entitlement and automation rights for a selected deployment not inspected here.',
        'price': 'No current version/deployment quotation.'},
      'SAS': {
        'sources': ['exec13_ct_sas_causal', 'exec13_ct_sas_structural'],
        'strength': 'Archived VARMAX groupwise Granger tests and a supplied lower-triangular dynamic representation.',
        'current_gap': 'No local VARMAX or multivariate dynamic fit; triangular decomposition does not select an intervention ordering.',
        'proposed_route': 'Use as a predictive/restricted-model comparator only after a current licensed edition and group/lag/observation map are specified.',
        'deployment': 'SAS/ETS 14.1 archive is technical evidence, not proof of current SAS/Viya syntax, entitlement or export parity.',
        'license': 'Current module and server/seat automation terms unverified.',
        'price': 'No licensed edition quotation.'},
      'IBM': {
        'sources': ['exec13_ct_ibm_tcm'],
        'strength': 'SPSS Statistics 31.0.0 temporal predictive-input selection across column or multidimensional series, with Granger meaning and TCM MODEL syntax.',
        'current_gap': 'No local automated temporal prediction model selection, graphical interactive workflow or matched data-aggregation interface.',
        'proposed_route': 'Retain as a forecasting workflow baseline; inspect detailed lag, time interval, aggregation, missingness and export paths before integration.',
        'deployment': 'GUI-to-syntax route documented; detailed technical option pages were navigation shells in the bounded acquisition.',
        'license': 'Runtime/extension/automation entitlement unverified.',
        'price': 'No selected edition and deployment quotation.'},
      'Mplus': {
        'sources': ['exec13_ct_mplus81'],
        'strength': 'Version 8.1 DSEM/RDSEM syntax, random effects, within/between decomposition and irregular-interval/missing-covariate choices.',
        'current_gap': 'No fitted intensive-longitudinal or latent dynamic model in the local reference service; unknown graph-effect uncertainty remains separate.',
        'proposed_route': 'Consider a specified-model heterogeneity comparator, binding time unit, predictor availability, missingness and supplied response mechanism.',
        'deployment': 'Text specification in archived addendum; selected option package, batch automation, OS and runtime semantics not evaluated.',
        'license': 'Package and production entitlement unverified.',
        'price': 'No selected option/license quotation.'},
    }
    available = []
    for c in original['candidates']:
        vendor = c['vendor']
        if vendor not in specifications:
            continue
        spec = specifications[vendor]
        bound = []
        for key in spec['sources']:
            source = sources[key]
            core.bound(ROOT, source['local_copy'])
            bound.append({'citation_key': key, 'identity': source['source_identity'],
                          'version_date': source['version_date'], 'local_copy': source['local_copy'],
                          'inspected_anchors': source['inspected_anchors'],
                          'supported_claims': source.get('supported_claims', source.get('claims'))})
        available.append({'vendor': vendor, 'aliases': c['aliases'], 'source_edition': [x['version_date'] for x in bound],
            'documented_strength': spec['strength'], 'observed_current_capability': 'Six selected computational operations in local-runtime/1; no temporal model fitting, graph search, live model backend or commercial adapter.',
            'current_gap': spec['current_gap'], 'proposed_capability': spec['proposed_route'],
            'deployment': spec['deployment'], 'license_status': spec['license'],
            'price': {'status': 'unverified', 'amount': None, 'description': spec['price']},
            'vendor_runtime_executed': False, 'bank_workload_evaluated': False,
            'source_evidence': bound})
    assert len(available) == 6
    unavailable = []
    for c in original['candidates']:
        if c['vendor'] in specifications:
            continue
        unavailable.append({'vendor': c['vendor'], 'aliases': c['aliases'],
            'source_status': c['status'], 'observed_limit': c['finding'],
            'capability_conclusion': 'unknown_not_absent', 'price': {'status': 'unknown', 'amount': None},
            'runtime_executed': False, 'next_evidence': c['decision']})
    assert len(unavailable) == 7
    gaps = [
      {'feature': 'Predictive temporal model search', 'current': 'not_implemented', 'vendor_strength': ['IBM','StataCorp','SAS'], 'design': 'Type prediction separately from intervention; use an available tool as a comparator before building another predictor.'},
      {'feature': 'Supplied dynamic/latent fitting', 'current': 'not_implemented', 'vendor_strength': ['BayesFusion','Mplus','SAS'], 'design': 'Compare licensed adapter versus internal selected implementation after matching time grid and observation model.'},
      {'feature': 'Structural intervention restrictions and external instruments', 'current': 'not_implemented', 'vendor_strength': ['StataCorp','Bayesia'], 'design': 'Preserve scientific restriction, instrument validity and normalization as explicit inputs; validate external premises before effect claims.'},
      {'feature': 'Graph/model uncertainty and decision consequences', 'current': 'partial_project_derivations_only', 'vendor_strength': [], 'design': 'Use exact two-world alternatives and robust/refusal results; do not infer another product lacks this feature from unavailable manuals.'},
      {'feature': 'Temporal task data management and UI', 'current': 'local_reference_only', 'vendor_strength': ['BayesFusion','IBM','Mplus'], 'design': 'Measure whole workflow and reviewer corrections, not only kernel wall time.'}]
    comparison = {'operation_id': OP, 'status': 'inconclusive', 'scope': '13 original vendor families; six evidence-backed use-case comparisons and seven unresolved technical families',
        'cutoff': '2026-10-07', 'source_acquisition': 'Preserved originals acquired 2026-10-13; exact cutoff bytes not authenticated',
        'prototype_reference': ref(ROOT / 'src/causalbank/operation_service_v12.py', 'Actual SUPPORTED operation mapping and refusal behavior'),
        'local_execution_reference': ref(ROOT / 'docs/program/execution/2026-10-14/execution-labels/evidence-labels.json', 'Actual local operations versus static/model claims'),
        'prior_cell': ref(ROOT / 'docs/program/comprehensive-v14/work/SW.CELL.discovery_temporal_interventional.commercial/coverage-review.json', 'Inconclusive primary coverage and explicit essential omissions'),
        'original_search': ref(OLD / 'search-protocol.json', '13 families and bounded cutoff search'),
        'original_candidates': ref(OLD / 'candidate-register.json', 'Aliases and technical status'),
        'original_omissions': ref(OLD / 'omissions-register.json', 'Seven unresolved original-source families'),
        'earlier_developed_comparison': ref(OLD / 'comparison.md', 'Temporal method, banking case and exact alternatives'),
        'exact_reference': ref(OLD / 'exact-results.json', 'Replayed funding prediction versus effect and equal-law decisions'),
        'vendors_with_primary_comparison': available, 'vendors_without_essential_primary': unavailable,
        'product_gap_comparison': gaps,
        'matched_banking_case': {'question': 'One-time 25bp deposit-rate increase and three-month balance/expense consequence',
            'same_observations': True, 'same_reduced_form': True,
            'different_structural_restrictions': ['rate_precedes_balance','balance_precedes_rate'],
            'assumed_three_month_net_values_USD': ['137.50','-300.00'],
            'lesson': 'A predictive lag coefficient, supplied triangular factorization or vendor feature label cannot choose the causal ordering.'},
        'cost_rule': 'Compare acquisition, license, integration, custody, execution, failure/retry, analyst review and future support for the same accepted question and output quality. No vendor price or bank loss threshold is supplied.',
        'conclusion': 'Useful shortlist and specific make/adapt/buy decisions, but not complete commercial temporal coverage or a paid/runtime ranking.',
        'no_paid_trial_or_contact': True, 'no_absence_inference_from_missing_source': True,
        'revisit_trigger': 'Obtain edition-matched technical manuals for the seven named gaps, current licensing/deployment terms and a matched trial only if prototype evidence makes it decision-relevant.'}
    write(OUTPUT, comparison)
    write(BASE / 'author-review.json', {'status': 'inconclusive', 'scope': 'Proposal-stage commercial temporal/interventional comparison',
        'findings': ['Every documented strength is tied to preserved official bytes and a specific product configuration.',
                     'Observed local operations are named separately from proposed adapters and vendor source capabilities.',
                     'Seven original-source gaps prevent full shortlist closure; each remains unknown rather than absent.',
                     'No numeric vendor price or runtime advantage was invented; two-world planning values reproduced.'],
        'evidence': [ref(OUTPUT, 'Six matched vendor comparison and seven omissions'),
                     ref(OLD / 'source-audit.json', 'Official primary anchors'),
                     ref(OLD / 'exact-results.json', 'Replayed exact funding alternatives')],
        'limitations': ['Author source review only; no vendor engine, paid terms, target-platform or bank trial.',
                       'After-cutoff acquired bytes do not prove the exact cutoff edition.'],
        'next_action': comparison['revisit_trigger']})
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    receipt.update(outcome='inconclusive', execution='performed',
        scope='Six edition-scoped official-source comparisons, seven explicit missing-source families, observed/proposed capability and conditional economics',
        reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
        limitations=['Seven essential primary technical families remain unresolved.',
                     'Edition-specific current pricing and deployment rights are not verified.',
                     'No vendor software, paid trial or bank data was run.'],
        outputs=[ref(OUTPUT, 'Commercial temporal vendor comparison')], nonexecution_reason='',
        revisit_trigger=comparison['revisit_trigger'],
        criteria=[{'index': 0, 'verdict': 'inconclusive',
                   'finding': 'Six documented vendor families have versioned original-source use-case comparisons; seven retained families lack essential edition-matched technical evidence, so exhaustive shortlist acceptance is withheld.',
                   'evidence': [ref(OUTPUT, 'Vendor/omission table'), ref(OLD / 'omissions-register.json', 'Named acquisition gaps')]},
                  {'index': 1, 'verdict': 'pass',
                   'finding': 'Unverified feature, unavailable source and unevaluated runtime are separate. Prices and deployment terms are scoped; no purchased license, contact, runtime superiority or lack of capability is fabricated.',
                   'evidence': [ref(OUTPUT, 'Cost and deployment boundaries'), ref(BASE / 'author-review.json', 'Author scope review')]}])
    write(BASE / 'operation-receipt.json', receipt)
    transition('record', OP, BASE / 'operation-receipt.json')


if __name__ == '__main__':
    main()
