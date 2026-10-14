#!/usr/bin/env python3
"""Bind inspected primary roles and the separate V9 project claim groups."""
import json
from closure_common import ROOT, save, digest


def main():
    sources = {s['id']: s for s in json.loads((ROOT/'docs/literature/sources.json').read_text())}
    roles = {
        'dml2018': dict(
            anchor='Section 4.1, printed pp.31--32, equation (4.4), Assumption 4.1(ii); local extracted lines 1590--1658 reinspected',
            supported='Orthogonal partialling-out score and joint nuisance-product/action-square rate requirement.',
            limit='The iid theorem does not establish this project\'s dependent-calendar pilot rate, finite-horizon covariance, or finite-sample coverage.'),
        'newey1986': dict(
            anchor='Printed p.4 / PDF p.6, Bartlett weights, Theorem 1 and its positive-semidefinite proof; original scanned page visually inspected',
            supported='Bartlett covariance weighting and positive-semidefinite construction.',
            limit='Not a proof of the project\'s innovation-filtration truncation, untapered scalar variance, or finite-sample calibration; these bytes are the April 1986 NBER technical working paper.')}
    records = []
    for key, role in roles.items():
        source = sources[key]
        assert digest(source['local_path']) == source['sha256']
        records.append(dict(id=key, title=source['title'], version_status=source['version_status'],
            local_path=source['local_path'], sha256=source['sha256'], **role))
    claims = [
        dict(id='F-R01', claim='The stationary funding nuisance recursions and exact conditional-on-pilot response ratio attribute a real pilot shift; known action means eliminate that shift without eliminating all finite-sample error.',
            manuscript_anchor='v9:pilot', sources=['dml2018'], evidence_class='project_derivation_and_synthetic_diagnostics',
            artifacts=['src/causalbank/funding_calibration.py', 'docs/studies/calibration-diagnostics-results.json', 'docs/reviews/calibration-independent-checks.json']),
        dict(id='F-R02', claim='A correct fixed dictionary with root-M nuisance rates needs sqrt(T)/M tending to zero; a growing Bartlett window also admits the sufficient fitted-score control L/sqrt(M) tending to zero under the stated moment conditions.',
            manuscript_anchor='v9:pilot', sources=['dml2018','newey1986'], evidence_class='project_rate_derivation',
            artifacts=['docs/program/calibration-scientific-specification.md', 'src/causalbank/funding_pilot_rates.py']),
        dict(id='F-R03', claim='Joint fixed regression has a finite innovation covariance horizon under the stated exogeneity and noninformative origin-swap law; untapered scalar variance and independent binomial audit propagation remain conditional, with nonpositive variance and weak mapping refused.',
            manuscript_anchor='v9:covariance', sources=['newey1986'], evidence_class='project_derivation_and_independent_finite_witnesses',
            artifacts=['src/causalbank/funding_calibration.py', 'docs/reviews/calibration-independent-checks.json', 'docs/studies/calibration-validation-results.json']),
        dict(id='F-R04', claim='The 720-date joint-regression comparison fails nominal coverage; the fresh fourfold-pilot comparison is compatible with nominal coverage in three tested laws but does not establish superiority, and additional pilot history has real cost.',
            manuscript_anchor='v9:results', sources=[], evidence_class='registered_synthetic_comparison_with_negative_results',
            artifacts=['docs/studies/calibration-validation-results.json', 'docs/studies/calibration-followup-spec.json', 'docs/studies/calibration-followup-results.json', 'docs/reviews/calibration-followup-checks.json', 'docs/reviews/calibration-table-generation.json']),
        dict(id='F-R05', claim='Two-pass grouped QR and globally centered cross-boundary scalar lag accounting give bounded working state and dense-equivalent joint-regression inference; growing-pilot arrays do not inherit this property.',
            manuscript_anchor='v9:execution', sources=[], evidence_class='verified_implementation_and_project_algebra',
            artifacts=['src/causalbank/funding_calibration.py', 'docs/reviews/calibration-independent-checks.json']),
        dict(id='F-R06', claim='Corrected complete local workloads use about 43 percent of dense peak memory and 83--84 percent of dense elapsed time at 1.2 million dates; inherited-RSS contamination and request-level restart limits are retained.',
            manuscript_anchor='v9:execution', sources=[], evidence_class='matched_local_workload_and_recovery_measurement',
            artifacts=['docs/studies/calibration-workloads-results.json', 'docs/studies/calibration-workload-remeasurement-results.json', 'tools/calibration_worker_launcher.py', 'docs/reviews/calibration-execution-notes.md', 'docs/reviews/calibration-recovery-rehearsal.json']),
        dict(id='F-R07', claim='Explicit method/input identities and two local consumers retain qualifications and withhold unavailable amounts; independent, bank, interface, platform and economic acceptance still require external evidence.',
            manuscript_anchor='v9:external', sources=[], evidence_class='verified_local_contract_and_external_protocol',
            artifacts=['src/causalbank/calibrated_funding_operations.py', 'docs/reviews/calibration-local-rehearsal.json', 'contracts/calibrated-funding.md', 'docs/program/external-validation-v9.md'])]
    path = ROOT/'docs/literature/reconstruction-claims.json'
    old = [c for c in json.loads(path.read_text()) if not c['id'].startswith('F-R')]
    path.write_text(json.dumps(old+claims, indent=2, ensure_ascii=False)+'\n')
    save('docs/literature/calibration-source-review.json', dict(status='pass', date='2026-10-10',
        publication_cutoff='2026-10-07', inspected=records, claims=[c['id'] for c in claims],
        search_scope='Reinspection of two registered local primary works; no new comprehensive discovery, version or correction search is claimed.',
        scope='Source identity and narrow inherited roles; rate, filtration, workload and integration claims remain project work.'),
        ['tools/calibration_source_trace.py', 'docs/literature/sources.json', 'docs/literature/reconstruction-claims.json',
         'docs/literature/text/dml2018.txt']+[r['local_path'] for r in records])
    print('Registered seven V9 project claim groups and two narrow primary-source roles.')


if __name__ == '__main__':
    main()
