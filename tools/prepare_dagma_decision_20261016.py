#!/usr/bin/env python3
"""Prepare the inspected DAGMA reuse disposition and proposed adapter contract."""
import json
from pathlib import Path
import review_dagma_reuse_20261016 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = work.ROOT, work.BASE


def main():
    primary = json.loads((BASE/'source-review.json').read_text())
    runtime = json.loads((BASE/'runtime-probes.json').read_text())
    verify_bindings(primary); verify_bindings(runtime)
    exact = json.loads((BASE/'exact-results.json').read_text())
    assert exact['units_and_paths']['total_original_0_to_2'] == 7
    contract = {
        'status': 'proposed_not_implemented', 'selected_path': 'Original DagmaLinear l2 source at '+work.PIN,
        'scientific_admission': [
            'Independent observational units, fixed variable identities and units, declared additive linear SEM and explicit identifiability restrictions.',
            'No automatic latent, selection, panel, temporal, interventional, PAG or effect-uncertainty interpretation.',
            'Optimization proposal and assumed causal model remain distinct; graph truth and calibration are not established by a fit.'],
        'conversion': [
            'Own a finite floating-point copy; retain row and variable order, centering means, units and scale transforms.',
            'Require validated edge pairs of integer indices, bounds, duplicates and contradiction checks. Empty constraints have explicit meaning.',
            'Distinguish hard exclusions from soft inclusion preferences; never promise included edges without checking returned output.',
            'Clone the schedule and preserve original/effective s, mu, learning rate, iteration and threshold configurations.',
            'Return parent-row/child-column W as a candidate graph; retain raw and thresholded matrices and reconstruct diagnostics for each.',
            'For nonlinear models, adjacency is a nonnegative first-layer norm. Preserve fitted structural functions for any separately justified intervention calculation.'],
        'failure_contract': [
            'Bound total runtime, retries and memory outside the upstream retry loop; record unfinished work as incomplete.',
            'Check spectral-domain membership and determinant sign before interpreting the log-determinant value.',
            'Check self-loops, directed cycles and required constraints on the actual returned support; refuse DAG certification if any fail.',
            'Map malformed inputs, missing dependencies, singular solves, nonfinite results and exhausted budgets to explicit error/refusal dispositions.',
            'Do not repair cycles by silent edge deletion or attach effect confidence intervals to optimizer residuals.'],
        'behavioral_oracle': ref(BASE/'runtime-probes.json', 'Seven actual original-module boundary cases'),
        'mathematical_oracle': ref(BASE/'exact-results.json', 'Domain, derivatives, units and nonlinear meaning'),
        'next_prototype': [
            'Resolve package release/build identity and freeze a complete dependency and notice inventory.',
            'Implement isolated wrapper validation and replay all seven recorded cases plus permutation, scaling and timeout cases.',
            'Predeclare generated identifiable and observationally equivalent mechanisms; compare truth, availability, graph error and downstream decisions.',
            'Compare matched NOTEARS or constraint-based routes only where assumptions and output classes coincide.',
            'If public/generated evidence supports merit, seek independent review and later bank-specific assumptions, inputs and costs.']}
    write(BASE/'proposed-adapter-contract.json', contract)
    omissions = {
        'cutoff': '2026-10-07', 'exhaustive_search': False,
        'items': [
            {'gap': 'Complete distribution identity and dependency/notice closure',
             'observed': 'pyproject references src/VERSION absent from the pinned tree; dependencies have no version bounds; torch/igraph/dagma absent locally.',
             'route': 'Acquire a declared release, compare it to this source pin and lock/review all dependencies before an installed-package trial.'},
            {'gap': 'Maintained build and source-module versus package equivalence',
             'observed': 'Saved latest-before-cutoff commit is January 2024; examples and inline test() are not an executed package CI result.',
             'route': 'Inspect selected release CI/history and supported Python/BLAS versions; revalidate changes without overwriting this evidence.'},
            {'gap': 'Nonlinear, logistic and non-IID qualification',
             'observed': 'Nonlinear source inspected only; probes execute the linear least-squares source module.',
             'route': 'Separate model-specific wrapper, source/runtime oracles and identification/uncertainty arguments.'},
            {'gap': 'General graph/effect uncertainty and bank usefulness',
             'observed': 'Acyclicity does not establish identification or calibrated effect regions.',
             'route': 'Selected model/design research and generated/public comparisons first; no known universal cure for observational equivalence.'}],
        'later_inputs': ['Bank meaning and clocks, acceptance precision/loss, actual costs, independent review and operational owners.']}
    write(BASE/'omissions-register.json', omissions)
    decision = {
        'operation': work.OP, 'candidate': 'dagma', 'decision': 'reference', 'integration_allowed': False,
        'source_identity': 'https://github.com/kevinsbello/dagma', 'revision': work.PIN,
        'canonical_identity': 'Original Python repository; distinct from Tetrad translation and NOTEARS implementations.',
        'reason': 'Retain the method and original implementation as a source and executable boundary reference. A production adapter needs explicit validation, output diagnostics and a complete supported build.',
        'target_and_uncertainty': 'Candidate weighted DAG for a chosen observational SEM/score. Optimization and topology diagnostics are not graph confidence, effect identification or a bank decision.',
        'license': 'Inspected Apache 2.0 root license; dependency/notice closure remains outstanding.',
        'dependency_evidence': ref(BASE/'source-review.json', 'Declared dependency/build and maintenance evidence'),
        'runtime_evidence': ref(BASE/'runtime-probes.json', 'Unchanged original linear-module execution'),
        'alternatives': [
            {'choice': 'adopt entire package', 'disposition': 'defer', 'reason': 'No complete installed distribution, dependency closure or wrapper acceptance.'},
            {'choice': 'integrate selected linear path', 'disposition': 'future candidate', 'reason': 'Retains original method while a wrapper owns validation, units, topology and bounded failures.'},
            {'choice': 'port into core or another language', 'disposition': 'reject for current proposal', 'reason': 'Adds numerical and maintenance obligations without demonstrated benefit; preserve a matched original oracle before reconsidering.'},
            {'choice': 'NOTEARS', 'disposition': 'comparator', 'reason': 'Different acyclicity/optimizer path; require matched assumptions and full output diagnostics before comparing speed or decisions.'},
            {'choice': 'PC/FCI/RFCI or reviewed temporal paths', 'disposition': 'question-dependent alternatives', 'reason': 'Different sufficiency, latent, time and equivalence-class contracts; cannot replace them with a thresholded DAG automatically.'}],
        'costs': ['Environment/build support, input copying and serialization, optimization/retries, graph diagnostics, dependency/notice maintenance and human causal review.',
                  'No observed bank prices, throughput superiority, resource budget or ROI.'],
        'owner_obligations': ['Prototype maintainer owns build/version and failure semantics.',
                              'Scientific reviewer owns assumptions, variable/time definitions and any downstream identification argument.',
                              'Future deployer owns license/notice inventory, platform qualification and change control.'],
        'conversion_failure_contract': ref(BASE/'proposed-adapter-contract.json', 'Proposed bounded adapter and independent oracles'),
        'revisit_trigger': 'A complete permissible pinned distribution, validated wrapper and preregistered matched public/generated results justify reconsidering conditional integration; new source revisions require a preserved successor review.',
        'limitations': work.LIMITS,
        'evidence': [ref(BASE/n, n) for n in ['plan.md', 'source-review.json', 'runtime-probes.json', 'exact-results.json', 'omissions-register.json']]}
    write(BASE/'decision-proposal.json', decision)
    sources = []
    for key, title, kind, name, claims in [
        ('exec16_dagma_primary', 'DAGMA pinned source, primary theorem and reuse review', 'software_primary_sources', 'source-review.json',
         ['Five original source blobs match the pinned tree and acquisition hashes.',
          'Input mutation, soft inclusion, list/tuple validation, prethreshold diagnostics and nonlinear norm semantics are explicit source findings.',
          'The genuine Bello PDF separates model identifiability, M-matrix domain and limiting path guarantees.']),
        ('exec16_dagma_runtime', 'DAGMA original linear-module boundary observations', 'project_execution', 'runtime-probes.json',
         ['Seven deterministic small cases execute the unchanged original module with observed local dependencies.',
          'Input mutation, ignored list exclusion, absent included edge, cyclic short run, diagnostic mismatch and exceptions are retained.',
          'No full package, nonlinear, adapter, performance or statistical qualification is inferred.']),
        ('exec16_dagma_exact', 'DAGMA domain, scaling and signed intervention reference constructions', 'project_derivation_and_exact_reference', 'exact-results.json',
         ['An independent two-variable log-det expression and finite differences check the native derivative inside its domain.',
          'Domain counterexamples, similarity under units, threshold sensitivity and equal norm/opposite derivative examples show conversion obligations.',
          'Stipulated local net derivatives 180 and -220 USD are illustrative calculations, not finite interventions or bank ROI.'])]:
        sources.append({'integrated_citation_key': key, 'title': title, 'kind': kind,
            'author': 'Causal banking research project', 'year': 2026,
            'source_identity': 'https://github.com/kevinsbello/dagma' if key.endswith('primary') else str((BASE/name).relative_to(ROOT)),
            'version_date': work.PIN+'; inspected and probed 2026-10-16; literature cutoff 2026-10-07',
            'local_copy': ref(BASE/name, title), 'inspected_anchors': claims, 'supported_claims': claims,
            'records': primary['sources'] if key.endswith('primary') else [],
            'primary_reread': {'paper': primary['paper']['local_copy'], 'anchors': primary['additional_paper_anchors']} if key.endswith('primary') else {},
            'limitations': work.LIMITS})
    write(BASE/'source-audit.json', {'sources': sources, 'cutoff': '2026-10-07', 'visual_acceptance': False})
    write(BASE/'author-review.json', {'status': 'pass', 'reviewer': work.REVIEWER,
          'scope': 'Reference reuse decision; proposed adapter and bounded actual source-module evidence',
          'findings': [decision['reason'], 'All seven boundary cases are preserved and the independent gradient check passes.',
                       'The proposed route handles observed defects before comparison; incomplete package/build evidence remains in the omissions register.',
                       'No new algorithm theorem, universal qualification, native nonlinear result or market advantage is claimed.'],
          'evidence': [ref(BASE/n, n) for n in ['decision-proposal.json', 'proposed-adapter-contract.json', 'source-review.json', 'runtime-probes.json', 'exact-results.json', 'omissions-register.json', 'development.tex']],
          'limitations': work.LIMITS, 'integration_allowed': False})
    print(json.dumps({'decision': 'reference', 'new_citations': len(sources), 'integration_allowed': False}))


if __name__ == '__main__': main()
