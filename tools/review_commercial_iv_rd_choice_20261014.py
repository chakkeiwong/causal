#!/usr/bin/env python3
"""Make source-bounded IV/RD commercial decisions against the local reference."""
import json
import sys

import commercial_iv_rd_examples_20261013 as exact
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT = core.ROOT
OLD = ROOT / 'docs/program/execution/2026-10-13/commercial-iv-rd'
BASE = ROOT / 'docs/program/execution/2026-10-14/commercial-iv-rd-choice'
OP = 'SW.COMM.iv_rd_design'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/vendor-comparison.json')


def main():
    assert not OUTPUT.exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    audit = json.loads((OLD / 'source-audit.json').read_text())
    verify_bindings(audit)
    sources = {s['integrated_citation_key']: s for s in audit['sources']}
    candidates = json.loads((OLD / 'candidate-register.json').read_text())
    observed = exact.calculate()
    assert observed == json.loads((OLD / 'exact-results.json').read_text())
    sys.path.insert(0, str(ROOT / 'src'))
    from causalbank.operation_service_v12 import SUPPORTED
    assert SUPPORTED == {
        'capabilities.describe': 'exact_runtime_manifest',
        'graph.review': 'declared_graph_syntax_only',
        'identify.effect': 'supplied_DAG_backdoor_independent_units',
        'estimate.effect': 'supplied_moment_Gaussian_residual_inversion',
        'sensitivity.evaluate': 'deterministic_quadratic_sublevel',
        'audit.observation': 'declared_strict_before_decision_clock',
    }
    write(BASE / 'exact-replay.json', {
        'status': 'pass', 'all_results_match': True, 'random_draws': 0,
        'results': observed, 'source': ref(OLD / 'exact-results.json', 'Preserved exact constructions'),
        'code': ref(ROOT / 'tools/commercial_iv_rd_examples_20261013.py', 'Exact rational enumeration'),
        'scope': 'Project examples only; no commercial engine or fitted-data study.'})
    specs = [
        ('StataCorp', 'Stata 19 / earlier StataNow feature; installed update unverified', 'stata',
         'ivregress and estat weakrobust',
         'Documented 2SLS/LIML/GMM and AR/CLR tests; one-endogenous-regressor confidence sets include disconnected, unbounded, whole-line and empty outputs.',
         'Credit encouragement with weak uptake; preserve the declared coefficient target, instrument origin, covariance and local versus population interpretation.',
         'License-authorized external comparator, then a narrow adapter; no proprietary port. Preserve every interval component, grid bounds/iterations and simulation seed/replications.',
         'Single-user and concurrent-network distinctions are documented. Unattended service accounts, embedding, MCP redistribution and installed entitlement are unresolved.'),
        ('SAS Institute', 'SAS/ETS 14.1; later partial manual excluded', 'sas', 'PROC SYSLIN',
         'Documented simultaneous-equation methods, explicit instruments and endogenous regressors, first-stage output and system restrictions.',
         'Supplied credit supply/demand equations with equation-specific targets and declared exclusion restrictions.',
         'Compare a supplied equation-system export first; preserve all instruments used in every first-stage regression, sample and covariance specification.',
         'Commands are documented; selected installation, batch/server entitlement and export parity are untested. No current commercial rights record inspected.'),
        ('EViews', 'Official help updated 12 March 2025; exact edition/update unresolved', 'eviews', 'IV Diagnostics and Tests',
         'Documented instrument summary and collinearity drops, subset orthogonality/endogeneity tests and qualified weak-instrument diagnostics.',
         'Audit which instruments actually entered a funding equation and whether a diagnostic applies to its estimator and covariance.',
         'Preserve diagnostic applicability and dropped-instrument identities in a proposed import. Do not map a relevance diagnostic to a weak-IV confidence set.',
         'Manual views are documented, while exact edition, unattended API/export behavior and deployment rights remain unknown. Image-only equations were not inferred.'),
        ('IBM', 'SPSS Statistics 30.0.0; Standard edition or Regression option', 'spss', 'Two-Stage Least-Squares Regression',
         'Documented explanatory/instrumental lists, coefficients, covariance output and syntax under a supplied linear model.',
         'A guided eligibility-instrument analysis with exogenous variables explicitly included in the intended lists.',
         'Compare a frozen supplied-model syntax/export workflow; retain assumptions and covariance meaning, with no all-version weak-IV or RD absence claim.',
         'Procedure entitlement is documented. Actual license, production automation, file export and server rights remain unevaluated.'),
        ('Estima', 'RATS 11 User’s Guide, copyright 2025', 'rats', 'INSTRUMENTS / INST',
         'Programmable IV in regression and GMM in systems; explicit instrument list and covariance controls. Even the constant is not automatically an instrument.',
         'Reproducible funding equation with explicit calendar/sample window and instrument definitions.',
         'Consider a licensed script adapter with a conversion check for constant, exogenous regressors, excluded instruments and covariance options.',
         'Script semantics are documented; target OS, installed version, unattended license and output parser are untested.'),
        ('JMP', 'JMP 19 Multivariate Methods, September 2025; installed entitlement unresolved', 'jmp', 'SEM MIIV-2SLS',
         'Model-implied instruments and equation-level Sargan diagnostics, instrument tables and supplied structural-model estimation.',
         'A declared credit structural model whose implied instruments and equation assumptions can be inspected.',
         'Compare supplied-model results and equation/instrument exports. Do not equate model-implied instruments with discovering a valid real-world encouragement.',
         'Documented platform behavior is not a verified unattended adapter; selected edition, scripting/export rights and costs require specific evidence.'),
    ]
    current = ('The six-operation local reference service accepts supplied DAGs, moments and deterministic sets. '
               'It exposes no fitted IV/RD, AR/CLR, SEM/system estimator or commercial adapter. '
               'Other research constructions in the repository do not enlarge this service contract.')
    pathways = []
    for vendor, edition, key, method, strength, use, route, rights in specs:
        keys = ['exec13_ivrd_' + key] + (['exec13_ivrd_license'] if key == 'stata' else [])
        pathways.append({
            'vendor': vendor, 'edition': edition, 'pathway': method,
            'documented_strength': strength, 'banking_use': use, 'proposed_route': route,
            'deployment_and_rights': rights, 'source_evidence': [sources[k] for k in keys],
            'observed_reference_capability': current,
            'remaining_local_gap': 'Fitted estimation, procedure-specific uncertainty, result conversion and licensed runtime qualification.',
            'price': {'status': 'unavailable_in_inspected_evidence', 'amount': None,
                      'scope': 'No matched edition/deployment quotation or accepted paid terms.'},
            'vendor_runtime_executed': False, 'performance_superiority_claim': False})
    unresolved = [{
        'candidate': c['candidate'], 'state': 'essential_primary_unavailable',
        'capability_conclusion': 'unknown_not_absent', 'price': {'status': 'unknown', 'amount': None},
        'comparison': 'Same declared target, instrument semantics, covariance, uncertainty topology and export contract required.',
        'next_action': c['decision'] + ' Obtain an accessible edition-specific original and intended deployment license; then compare the same banking case.'}
        for c in candidates['candidates'] if c['evidence_state'] == 'Essential primary source unavailable']
    assert len(candidates['candidates']) == 9 and len(pathways) == 6 and len(unresolved) == 3
    companions = []
    for key, route in [('rdrobust', 'Prefer a reviewed pinned adapter or direct use in an already licensed Stata workflow; defer porting until numerical semantics and redistribution obligations are reviewed.'),
                       ('rddensity', 'Adopt as a diagnostic candidate with explicit bandwidth, mass-point and test-family outputs; never turn nonrejection into causal-design certification.')]:
        companions.append({
            'package': key, 'primary_evidence': sources['exec13_ivrd_' + key],
            'proposed_route': route, 'host_rights_separate': True,
            'license_evidence': 'Inspected upstream files declare GPL version 3; actual use/distribution obligations remain to be assessed.',
            'source_cutoff_limit': 'rdrobust commit is 2026-10-07 22:36 UTC, after that calendar day in Asia/Shanghai; historical review explicitly uses UTC end-of-day. Re-pin if client cutoff is interpreted as local end-of-day.',
            'native_runtime_executed': False})
    gaps = [
        {'gap': 'Fitted IV and weak-IV inference', 'route': 'Start with one declared scalar target and a serious Stata AR/CLR baseline. A quadratic-set API does not establish equivalence or novelty.', 'acceptance': 'Target, sample, covariance, test family and all interval components survive export, including empty and unbounded results.'},
        {'gap': 'Threshold design and RD inference', 'route': 'Separate sharp/fuzzy targets, bandwidth bias correction, weak local uptake and score support; review pinned upstream reuse before building a duplicate.', 'acceptance': 'Retain cutoff, units, side convention, unique scores, bandwidths, bias/variance choice and first-stage diagnostics; reject unsupported interpretation.'},
        {'gap': 'Model and instrument provenance', 'route': 'Carry included/excluded variables, constants, equation restrictions and actual retained instruments. Require scientific reasons for exclusion.', 'acceptance': 'Equal observed moments with opposite stipulated decisions remain unresolved unless added assumptions are declared.'},
        {'gap': 'Numerical status and failures', 'route': 'Distinguish scientific empty set, unidentified target, numerical search exhaustion and unsupported operation.', 'acceptance': 'A narrow grid missing both components must not become an accepted empty confidence set; all requests remain in denominators.'},
        {'gap': 'Economics and deployment', 'route': 'Use public/generated reference cases first; obtain matched rights and costs before a licensed trial becomes necessary.', 'acceptance': 'Compare license, conversion, fitting, retries, review and support cost for the same accepted scientific output. No price or ROI is imputed.'},
    ]
    conclusion = ('Six documented commercial families and two pinned RD companions support concrete comparisons; '
                  'three essential vendor originals, EViews edition identity and matched rights/cost/runtime evidence remain open.')
    comparison = {
        'operation_id': OP, 'status': 'inconclusive', 'cutoff': '2026-10-07',
        'scope': 'Nine inherited shortlisted families, preserved documented versions and two open-source companions.',
        'primary_audit': ref(OLD / 'source-audit.json', 'Official source identities, hashes, versions and anchors'),
        'original_candidates': ref(OLD / 'candidate-register.json', 'Bounded nine-family shortlist'),
        'original_omissions': ref(OLD / 'omissions-register.json', 'Source failures and extension limits'),
        'integrated_argument': ref(OLD / 'comparison.tex', 'Already integrated connected IV/RD comparison'),
        'prototype_reference': ref(ROOT / 'src/causalbank/operation_service_v12.py', 'Observed SUPPORTED declaration'),
        'exact_replay': ref(BASE / 'exact-replay.json', 'Reproduced four exact construction families'),
        'vendors_with_primary_comparison': pathways, 'vendors_without_essential_primary': unresolved,
        'open_source_companions': companions, 'product_gaps_and_acceptance': gaps,
        'matched_banking_case': {'decision': 'Credit extension near an eligibility threshold',
            'same_summary_ratio_USD': '50', 'assumed_cost_USD': '40', 'compatible_net_values_USD': ['10', '-10'],
            'discrete_support': [-2, -1, 1, 2], 'compatible_cutoff_effects_USD': ['20', '-20'],
            'scope': 'Exact authored examples; first pair matches summary moments, not asserted full observed laws.'},
        'next_experiment': 'Develop public/generated target and export references first. A later licensed comparison requires chosen edition, deployment rights, budget and complete failure accounting; no paid execution is performed here.',
        'no_absence_inference_from_missing_source': True, 'no_paid_trial_or_contact': True,
        'conclusion': conclusion,
        'revisit_trigger': 'Acquire MATLAB, PcGive and LIMDEP originals; settle EViews edition and cutoff pins; inspect matched licenses/prices. A later prototype must qualify actual estimation and conversion before any superiority claim.'}
    write(OUTPUT, comparison)
    evidence = [ref(OUTPUT, 'Six commercial comparisons, three omissions and two separate reuse decisions'),
                ref(BASE / 'plan-review.md', 'Reviewed bounded continuation'),
                ref(BASE / 'exact-replay.json', 'Exact constructions replayed'),
                ref(OLD / 'comparison.tex', 'Substantive argument already in the current reader')]
    write(BASE / 'author-review.json', {
        'status': 'inconclusive', 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'findings': [conclusion,
            'Reinspected official Stata options/topology, SAS instruments, EViews diagnostics, SPSS entitlement, RATS list/covariance, JMP equation output and RD help.',
            'Stata already offers documented weak-instrument sets; no unsupported local novelty or statistical superiority is claimed.',
            'Actual local service scope and exact examples are distinguished from fitted estimator and vendor execution.',
            'No technical source is added to the manuscript. This structured decision records and qualifies its already integrated argument.'],
        'evidence': evidence, 'visual_acceptance': False,
        'manuscript_delta': 'None; existing integrated source and claim identities remain unchanged.',
        'next_action': comparison['revisit_trigger']})
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    receipt.update(
        outcome='inconclusive', execution='performed', scope=comparison['scope'],
        reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
        limitations=[conclusion, 'No commercial engine, bank experiment, price quotation or independently accepted adapter.'],
        outputs=[ref(OUTPUT, 'Version-scoped IV/RD vendor decisions')], nonexecution_reason='',
        revisit_trigger=comparison['revisit_trigger'],
        criteria=[
            {'index': 0, 'verdict': 'inconclusive', 'finding': conclusion, 'evidence': evidence},
            {'index': 1, 'verdict': 'pass',
             'finding': 'Unknown capabilities and prices stay unknown; documented strengths, actual local gaps, proposed adapters, rights and unperformed trials are separate.',
             'evidence': evidence + [ref(BASE / 'author-review.json', 'Reviewed conclusions and limits')]}])
    write(BASE / 'operation-receipt.json', receipt)
    transition('record', OP, BASE / 'operation-receipt.json')
    print(json.dumps({'families_compared': 6, 'families_unresolved': 3, 'rd_companions': 2,
                      'outcome': 'inconclusive', 'manuscript_changed': False}))


if __name__ == '__main__':
    main()
