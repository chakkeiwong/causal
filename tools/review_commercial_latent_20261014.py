#!/usr/bin/env python3
"""Edition/capability and deployment comparison from preserved original sources."""
from copy import deepcopy
from html.parser import HTMLParser
import json
from pathlib import Path

import run_program as control
from discovery_journey_20261013 import ROOT, ref, write, now

BASE = ROOT / 'docs/program/execution/2026-10-14/commercial-latent-comparison'
PRIOR = ROOT / 'docs/program/execution/2026-10-13/commercial-latent'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work/SW.COMM.discovery_latent/vendor-comparison.json'


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.row = None; self.cell = None; self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        if tag in ('td', 'th'):
            self.cell = {'text': '', 'attrs': dict(attrs), 'symbols': []}
        if tag in ('img', 'svg') and self.cell is not None:
            self.cell['symbols'].append(dict(attrs))

    def handle_data(self, text):
        if self.cell is not None:
            self.cell['text'] += text + ' '

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.cell['text'] = ' '.join(self.cell['text'].split())
            if self.row is not None:
                self.row.append(self.cell)
            self.cell = None
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row); self.row = None


def api_matrix():
    source = ROOT / 'docs/literature/raw/exec13_vendor_bayesia_api.html'
    parser = TableParser(); parser.feed(source.read_text())
    assert len(parser.rows) == 13
    columns = [cell['text'] for cell in parser.rows[1][1:]]
    assert len(columns) == 4
    matrix = []
    for row in parser.rows[2:6]:
        values = [c['symbols'][0]['aria-label'] for c in row[1:]]
        assert len(values) == 4 and set(values) <= {'yes', 'no'}
        matrix.append({'function': row[0]['text'], 'by_configuration': dict(zip(columns, values))})
    assert list(matrix[2]['by_configuration'].values()) == ['no', 'yes', 'no', 'no']
    assert list(matrix[3]['by_configuration'].values()) == ['no', 'yes', 'no', 'no']
    # Colspans explicitly associate the first three Java configurations with
    # customer-hosted .xbl files and the fourth REST configuration with France.
    assert parser.rows[7][1]['attrs']['colspan'] == '3'
    deployment = {column: {'model_location': parser.rows[7][1 if i < 3 else 2]['text'],
                           'installation': parser.rows[9][1 if i < 3 else 2]['text'],
                           'license_management': parser.rows[10][1 if i < 3 else 2]['text']}
                  for i, column in enumerate(columns)}
    result = {'source': ref(source, 'API Overview HTML table: four configurations, SVG aria-label yes/no and column spans'),
        'extracted_at': now(), 'method': 'stdlib HTMLParser; preserved source bytes; no downloaded code execution',
        'columns': columns, 'matrix': matrix, 'deployment': deployment,
        'pricing_observation': 'Table links Fees for 12-Month License Rental (USD); it supplies no numeric price in the inspected cells.',
        'limitation': 'Mutable unnumbered vendor page; configurations are not demonstrated runtime performance or authenticated cutoff bytes.'}
    write(BASE / 'bayesia-api-matrix.json', result)
    return result


def main():
    assert not OUTPUT.exists(), 'Preserve completed comparison'
    matrix = api_matrix()
    audits = [PRIOR / 'source-audit.json', ROOT / 'docs/program/execution/2026-10-13/commercial/source-audit.json']
    selected = {'exec13_latent_genie_structure', 'exec13_latent_genie_parameters', 'exec13_latent_bayesia_data',
        'exec13_latent_bayesia_variables', 'exec13_latent_netica_algorithms', 'exec13_latent_netica_structure',
        'exec13_latent_sas_calis', 'exec13_latent_stata_lca', 'exec13_latent_mplus', 'exec13_genie_readme',
        'exec13_smile_intro', 'exec13_smile_license', 'exec13_bayesia_api', 'exec13_bayesia_professional'}
    sources = []
    for path in audits:
        for source in json.loads(path.read_text())['sources']:
            if source['integrated_citation_key'] not in selected:
                continue
            source = deepcopy(source)
            for key in ['local_copy', 'text_copy', 'acquisition_receipt']:
                if key in source:
                    control.core.bound(ROOT, source[key])
            source['reinspection'] = {'reviewed_at': now(), 'prior_audit': ref(path, 'Preserved primary source identity and inspected anchors'),
                'scope': 'Selected documented method and current proposal capability; no new vendor execution'}
            if source['integrated_citation_key'] == 'exec13_bayesia_api':
                source['reinspection']['additional_anchor'] = ref(BASE / 'bayesia-api-matrix.json', 'Recovered yes/no symbols and per-configuration deployment columns')
                source['supported_claims'] += [
                    'Only the listed Java Network Learning configuration has yes for parameter estimation and structure learning in this table.',
                    'All four listed configurations have yes for inference; the REST column has no for building/modifying models.',
                    'The inspected table associates the three Java configurations with customer model storage and the REST configuration with Bayesia servers in France.']
            sources.append(source)
    assert {s['integrated_citation_key'] for s in sources} == selected
    write(BASE / 'source-audit.json', {'sources': sources, 'cutoff': '2026-10-07',
        'coverage_limit': 'Reinspection of preserved original public bytes acquired after cutoff; no new market census or historical-byte authentication.',
        'table_extraction': ref(BASE / 'bayesia-api-matrix.json', 'Primary HTML structure preserved'),
        'runtime_executed': False})
    src = {s['integrated_citation_key']: s for s in sources}
    def bindings(keys):
        return [src[k]['local_copy'] for k in keys]
    specs = [
        ('BayesFusion', 'GeNIe manual 5.0.R2; separate SMILE manual 2.2.4.R1',
         ['exec13_latent_genie_structure', 'exec13_latent_genie_parameters', 'exec13_genie_readme', 'exec13_smile_intro', 'exec13_smile_license'],
         'Supplied-network EM, initialization and missingness controls; categorical structure learning and a Gaussian-PC option with specified restrictions.',
         'Fixed-model latent fitting is a documented reuse candidate; FCI/PAG under hidden confounding is unverified in this evidence.',
         'C++ compiled library with documented Java/Python/R/.NET/COM wrappers; platform and wrapper equivalence remain untested.',
         'Development and deployment licenses are distinct; server and end-user distribution licenses are described. Academic eligibility cannot be assumed for a bank.',
         'vendor_requests_contact_for_pricing', 'No price quotation obtained; no number invented.',
         'Investigate a licensed supplied discrete latent-model adapter; preserve node/state maps, missingness, initialization, fixed structure, fit statistic and license scope.'),
        ('Bayesia', 'Unnumbered preserved BayesiaLab help and named Engine API configurations',
         ['exec13_latent_bayesia_data', 'exec13_latent_bayesia_variables', 'exec13_bayesia_api', 'exec13_bayesia_professional'],
         'Naive/Multinet latent representations, soft/hard assignments and API configuration alternatives.',
         'Representation learning does not by itself identify confounded effects. Only Java Network Learning in the inspected table supplies fitting and structure learning.',
         'Three Java configurations use customer model storage; REST inference uses vendor model storage in France. License validation connectivity is described.',
         'Purchase/rental, seat/floating/elastic options; API development and production are separate and simultaneous loaded-model instances affect production licensing.',
         'public_price_link_not_numeric_price', 'Inspected page links a USD 12-month price list; amount, taxes, edition and complete terms remain unverified.',
         'Compare representation learning through the documented learning configuration. Do not route graph discovery to the inference-only REST configuration.'),
        ('StataCorp', 'SEM Example 50g copyright 2025, release-19 example data; purchased edition unverified',
         ['exec13_latent_stata_lca'], 'gsem two-class measurement model, class proportions, posterior membership and separate initialization/full-fit diagnostics.',
         'Supplied latent-class estimation is documented; causal latent-confounded graph discovery is not established by the example.',
         'Command-script fitting is demonstrated by the manual; target OS, seat/core limits, external invocation and export behavior are untested.',
         'Commercial edition entitlement and redistribution/automation terms not established by this technical example.',
         'unavailable_in_inspected_sources', 'No source-grounded numeric license or deployment price.',
         'Use as a matched supplied latent-class baseline after pinning model, class count, starts, missingness, optimizer settings, edition and output extraction.'),
        ('Mplus', 'Official guide linked as Version 8, Chapter 7; licensed option package unverified',
         ['exec13_latent_mplus'], 'Mixture models, complex-sampling options and randomized-trial CACE examples with membership and exclusion restrictions.',
         'A documented causal compliance use case is stronger than generic clustering; it remains different from arbitrary hidden-confounder discovery.',
         'Text input/output specification is documented; licensed package, OS, automation and runtime numerical behavior untested.',
         'Required mixture/multilevel option entitlement and distribution terms must be pinned from licensing sources.',
         'unavailable_in_inspected_sources', 'No inspected package-specific price or quotation.',
         'Compare CACE only under the same offer/receipt/compliance information and noncomplier exclusion; compare mixture likelihood separately.'),
        ('Norsys', 'Mutable Netica help; TAN introduction references 5.00, current edition unverified',
         ['exec13_latent_netica_algorithms', 'exec13_latent_netica_structure'], 'CPT counting/EM/gradient fitting and predictive TAN structure learning.',
         'Latent/incomplete CPT fitting is useful; predictive link orientation is not an identified intervention or PAG contract.',
         'GUI case-file workflow described; current application/API binary, platform and wrapper contract unverified.',
         'License and redistribution scope not established by inspected learning help.',
         'unavailable_in_inspected_sources', 'No verified current product/API price.',
         'Candidate fixed-CPT/latent-model baseline after pinning priors, objective, initialization and release; reject TAN arrows as substitutes for causal directions.'),
        ('SAS', 'SAS/STAT 14.1 archived CALIS documentation', ['exec13_latent_sas_calis'],
         'Supplied latent SEM, multiple model languages, constraints, FIML and diagnostics.',
         'A mature specified-model comparison exists; arbitrary latent discovery and a current HPBNET/PAG contract are unverified.',
         'PROC CALIS program specification; current target environment, automation rights and export equivalence untested.',
         'Archived technical manual does not establish present SAS/STAT/Viya entitlement or deployment terms.',
         'unavailable_in_inspected_sources', 'No version/deployment-specific price quotation.',
         'Compare a supplied measurement/structural model under identical constraints, likelihood and observation law; retain archived edition boundary.')]
    vendors = []
    for vendor, edition, keys, strength, boundary, deployment, license_scope, price_kind, price_detail, decision in specs:
        vendors.append({'vendor': vendor, 'edition_evidence': edition, 'documented_strength': strength,
            'latent_discovery_boundary': boundary, 'deployment': deployment, 'license_scope': license_scope,
            'price': {'status': price_kind, 'amount': None, 'detail': price_detail, 'quoted': False},
            'runtime_status': 'not_evaluated', 'comparison_decision': decision,
            'our_current': 'Canonical runtime preserves supplied graph syntax/context and explicit unsupported discovery; no installed commercial latent fitter or general PAG effect inference.',
            'our_proposed': 'Evidence-linked problem/graph/effect contract and licensed optional adapters with explicit assumptions, ambiguity, uncertainty and costs.',
            'gap_to_documented_vendor': 'The documented fitting/representation workflow is not provided by our canonical service. Proposed semantic controls do not prove superiority.',
            'source_keys': keys, 'original_evidence': bindings(keys)})
    prior = json.loads((PRIOR / 'candidate-register.json').read_text())
    for item in prior['candidates']:
        if any(v['vendor'] == item['vendor'] for v in vendors):
            continue
        vendors.append({'vendor': item['vendor'], 'edition_evidence': 'Essential technical/version source unresolved',
            'documented_strength': 'Not established by inspected technical sources',
            'latent_discovery_boundary': item['finding'], 'deployment': 'Not evaluated; navigation or licensing lead alone does not establish the algorithm contract.',
            'license_scope': 'No selected engine/version/license scope accepted or validated',
            'price': {'status': 'unavailable_for_selected_engine', 'amount': None, 'quoted': False,
                      'detail': 'No authenticated technical-edition plus licensing/price combination in this review'},
            'runtime_status': 'not_evaluated', 'comparison_decision': 'Hold ranking/adoption claim; acquire the missing authentic technical and edition/license evidence.',
            'our_current': 'No vendor engine installed or qualified', 'our_proposed': 'Optional adapter only after documented semantic/rights review and a justified matched test',
            'gap_to_documented_vendor': 'Unknown, not absent', 'original_evidence': item['primary_or_navigation_artifacts']})
    assert len(vendors) == 11
    comparison = {'operation_id': 'SW.COMM.discovery_latent', 'outcome': 'inconclusive',
        'scope': 'Six substantive documented-method comparisons and five explicitly unresolved vendor leads; incomplete edition-specific commercial landscape.',
        'cutoff': '2026-10-07', 'vendors': vendors,
        'source_audit': ref(BASE / 'source-audit.json', '14 verified original source records with prior versions/hashes/anchors'),
        'api_configuration_matrix': ref(BASE / 'bayesia-api-matrix.json', 'Original SVG and colspan data recovered'),
        'narrative': ref(BASE / 'comparison.md', 'Use-case comparison, adoption choices, deployment and evidence needed'),
        'inherited_omissions': ref(PRIOR / 'omissions-register.json', 'Five essential technical followups and recorded acquisition failures'),
        'current_implementation': [ref(ROOT / 'src/causalbank/operation_service_v12.py', 'SUPPORTED and unsupported graph.discover dispatch'),
            ref(ROOT / 'docs/program/master/work/R04/review-v2.md', 'Preserved restricted graph/effect research disposition')],
        'known_routes': ['Pin accessible versioned technical and licensing texts, including optional package entitlement.',
            'Implement separate fixed-model, representation, graph-class and intervention adapters only when the chosen input/output semantics match.',
            'Use common generated observations and hidden truth reserved for evaluation; compare the same targets, assumptions, denominators and full costs.'],
        'unknown_or_unavailable': ['Edition-specific latent-confounded discovery contract for all shortlisted vendors',
            'Five essential technical sources', 'Current numerical prices for selected deployments',
            'Runtime equivalence, scaling and accepted customer integration'],
        'contacts': 0, 'purchases': 0, 'vendor_runtime_runs': 0, 'market_absence_claim': False, 'original_gap_qualification': False}
    write(OUTPUT, comparison)
    graph, _, _ = control.combined(ROOT, control.core.read(ROOT, control.core.STATE))
    node = control.ledger.operation(graph, comparison['operation_id'])
    review = {'outcome': 'inconclusive', 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'findings': ['All eleven inherited candidates retained; no omission was converted into product absence.',
            'Four API configurations were recovered from original markup, preventing an inference-only endpoint from being credited with fitting.',
            'Current local execution, proposed capabilities and documented vendor strengths are compared separately.',
            'No authenticated numerical price or vendor execution is present. License categories are documented only where the originals support them.',
            'Five essential sources and several numbered release/package mappings are unresolved; complete edition-specific acceptance is withheld.'],
        'evidence': [ref(OUTPUT, 'Complete comparison with explicit unknowns'), comparison['source_audit'], comparison['api_configuration_matrix'],
                     ref(Path(__file__), 'Deterministic extraction and hash verification')], 'independent_review': False}
    write(BASE / 'author-review.json', review)
    receipt = control.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed', scope=comparison['scope'], reviewer=review['reviewer'],
        limitations=comparison['unknown_or_unavailable'], outputs=[ref(OUTPUT, 'Reviewed commercial comparison')])
    for i, verdict, finding in [(0, 'inconclusive', 'Six original technical comparisons are developed; five vendor technical/edition sources and several licensing mappings remain unresolved.'),
        (1, 'pass', 'Not evaluated, unknown, documented restriction and current implementation gaps are distinct; prices have explicit evidence statuses and no trial/contact/purchase was fabricated.')]:
        receipt['criteria'][i].update(verdict=verdict, finding=finding,
            evidence=[ref(OUTPUT, 'All candidate outcomes'), ref(BASE / 'author-review.json', 'Author review'), comparison['source_audit']])
    write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'outcome': 'inconclusive', 'vendors': len(vendors), 'verified_sources': len(sources),
                      'recovered_api_configurations': len(matrix['columns']), 'essential_source_gaps': 5}))


if __name__ == '__main__':
    main()
