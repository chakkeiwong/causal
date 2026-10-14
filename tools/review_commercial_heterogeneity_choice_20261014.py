#!/usr/bin/env python3
"""Review commercial effect pathways against the observed local reference.

Only preserved official-source bytes are compared. No vendor runtime, license
purchase, bank workload or price is represented as observed.
"""
import json
import sys

import commercial_heterogeneity_examples_20261013 as exact
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import (
    ref, transition, verify_bindings, write,
)

ROOT = core.ROOT
sys.path.insert(0, str(ROOT / 'src'))
BASE = ROOT / 'docs/program/execution/2026-10-14/commercial-heterogeneity-choice'
OLD = ROOT / 'docs/program/execution/2026-10-13/commercial-heterogeneity'
OP = 'SW.COMM.effects_heterogeneity'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/vendor-comparison.json')


def main():
    assert not OUTPUT.exists() and (not BASE.exists() or not any(BASE.iterdir()))
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    original = json.loads((OLD / 'candidate-register.json').read_text())
    audit = json.loads((OLD / 'source-audit.json').read_text())
    verify_bindings(audit)
    sources = {s['id']: s for s in audit['sources']}
    fresh = exact.calculate()
    assert fresh == json.loads((OLD / 'exact-results.json').read_text())
    from causalbank.operation_service_v12 import SUPPORTED
    assert SUPPORTED == {
        'capabilities.describe': 'exact_runtime_manifest',
        'graph.review': 'declared_graph_syntax_only',
        'identify.effect': 'supplied_DAG_backdoor_independent_units',
        'estimate.effect': 'supplied_moment_Gaussian_residual_inversion',
        'sensitivity.evaluate': 'deterministic_quadratic_sublevel',
        'audit.observation': 'declared_strict_before_decision_clock',
    }
    BASE.mkdir(exist_ok=True)
    write(BASE / 'exact-replay.json', {
        'status': 'pass', 'replay_matches_preserved_result': True,
        'random_draws': 0, 'targets': fresh['targets'],
        'fixed_policy_net_USD': fresh['policy_net_USD_per_eligible_account'],
        'source': ref(OLD / 'exact-results.json', 'Exact finite-population calculation'),
        'implementation': ref(ROOT / 'tools/commercial_heterogeneity_examples_20261013.py',
                              'Fraction arithmetic and complete treatment-state enumeration'),
        'limits': ['Generated law and authored costs; no fitted estimator or vendor engine.'],
    })
    specs = [
        {
            'vendor': 'StataCorp', 'pathway': 'cate and cate postestimation',
            'keys': ['exec13_ch_stata'],
            'strength': 'Documented binary-treatment/continuous-outcome PO and AIPW paths, nuisance learners, conditional effects, prespecified groups and sorted groups; prespecified-policy evaluation and pointwise effect plots.',
            'edition': 'r19 context; copyright through 2025; saved manual modified 2026-07-29. Exact cutoff bytes and installed entitlement unverified.',
            'banking_use': 'Estimate risk-conditional recovery effects of a single servicing contact, and evaluate a separately specified contact rule.',
            'matching_conditions': ['Retain conditional modifiers separately from nuisance-only controls.',
                'Match eligible population, missing-value exclusions, treatment coding, horizon and target aggregation.',
                'Preserve random-observation cross-fitting, seed, default honesty and option restrictions.',
                'The documented observation folds do not establish repeated-account or shared-calendar validity.'],
            'proposed_route': 'Use an authorized external benchmark before considering a narrow scripted adapter. Compare complete target artifacts and failure behavior, not only point estimates.',
            'deployment': 'Manual documents commands and saved results; selected licensed edition, batch/server entitlement, OS and export behavior remain untested.',
            'rights': 'Proprietary implementation; no porting or redistribution rights established. Current selected license and automation terms need review.',
        },
        {
            'vendor': 'JMP', 'pathway': 'Uplift platform',
            'keys': ['exec13_ch_jmp_uplift'],
            'strength': 'Interaction-driven partitioning for response segmentation; linear/logistic split models and Monte Carlo adjustment for candidate-level multiplicity.',
            'edition': '19.0 overview dated 2025-07-15; JMP16 Consumer Research guide is an explicitly separate historical source.',
            'banking_use': 'Compare transparent response segmentation in a specified servicing experiment before selecting an evaluation policy.',
            'matching_conditions': ['Treatment ordering and validation behavior from the JMP16 guide are not promoted to version19 guarantees.',
                'Candidate-split multiplicity correction does not itself establish external selected-policy inference.',
                'Incremental response, conditional causal effect and realized individual effect retain separate meanings.'],
            'proposed_route': 'Benchmark a frozen segmentation problem and held-out fixed-policy value; obtain current detailed validation/export documentation before adapter work.',
            'deployment': 'Documented interactive platform; unattended CLI/server/MCP integration and result export parity not evaluated.',
            'rights': 'Commercial edition and execution/export rights unverified; no proprietary implementation port approved.',
        },
        {
            'vendor': 'JMP', 'pathway': 'JMP Pro Causal Treatment',
            'keys': ['exec13_ch_jmp_causal'],
            'strength': 'Explicit ATE/ATET targets, binary/continuous treatment and outcome paths, logistic/linear nuisance models, weighting/regression/augmentation and overlap reports.',
            'edition': '19.2 help dated 2026-01-13; source explicitly limits the personality to JMP Pro. Exact cutoff bytes remain unverified.',
            'banking_use': 'Compare average effect of a one-time contact, or a separately specified continuous offer under its required dose-response assumptions.',
            'matching_conditions': ['ATE and ATET are distinct; match target weights and treatment population.',
                'Continuous-treatment normal-density/MSM/GPS paths are separate model commitments.',
                'Inspected prose supports the method descriptions; image-only equations are not treated as inspected.',
                'Overlap displays do not certify exchangeability, consistency or population positivity.'],
            'proposed_route': 'Retain as a specified-model comparator, with explicit target and overlap artifacts; qualify a file-based import before any runtime automation.',
            'deployment': 'JMP Pro personality is documented; installed version, unattended export, custody and production entitlement remain unevaluated.',
            'rights': 'Selected commercial terms and redistribution rights unavailable in inspected evidence; no paid trial or adapter approval.',
        },
        {
            'vendor': 'DataRobot', 'pathway': 'Causal AI for readmission accelerator',
            'keys': ['exec13_ch_datarobot'],
            'strength': 'Official workflow separates propensity prediction, inverse-probability weights and weighted outcome comparison.',
            'edition': 'Overview displays update 2026-09-21; pinned linked notebook, dependencies and license not inspected.',
            'banking_use': 'Potential supplier of versioned nuisance predictions for a declared observational servicing comparison.',
            'matching_conditions': ['Clinical overview is an architectural lead; no bank or native CATE validation is inferred.',
                'Require preprocessing, training population, folds, encoding and prediction provenance.',
                'Identification, weighting, inference and policy selection require separate reviewed methods.'],
            'proposed_route': 'Inspect a pinned notebook and its license first. Consider prediction import only after training/evaluation separation and learner conditions are justified.',
            'deployment': 'Overview does not qualify a selected platform/runtime deployment or hosted-data contract.',
            'rights': 'Notebook license and platform/API entitlement unresolved; direct adoption, code port and production adapter remain undecided.',
        },
    ]
    pathways = []
    for spec in specs:
        entry = {k: v for k, v in spec.items() if k != 'keys'}
        entry.update(
            source_evidence=[{k: sources[key][k] for k in [
                'id', 'source_identity', 'version_date', 'local_records',
                'inspected_anchors', 'supported_claims', 'limits', 'urls',
            ]} for key in spec['keys']],
            observed_current_capability='Six local-runtime/1 reference operations; supplied-DAG checks and supplied-moment Gaussian inversion. No installed CATE, uplift, policy-learning estimator or vendor adapter.',
            current_gap='No matched fitted heterogeneous-effect or fixed-policy estimator is implemented by the reference service.',
            vendor_runtime_executed=False, bank_workload_evaluated=False,
            price={'status': 'unavailable_in_inspected_evidence', 'amount': None,
                   'scope': 'No selected edition/deployment quotation or accepted paid terms.'},
        )
        pathways.append(entry)
    compared = {p['vendor'] for p in pathways}
    unresolved = []
    for family in original['families']:
        if family['vendor'] in compared:
            continue
        unresolved.append({
            'vendor': family['vendor'], 'aliases': family['aliases'],
            'source_status': family['disposition'], 'capability_conclusion': 'unknown_not_absent',
            'observed_current_capability': 'Local service has no matched heterogeneous-effect estimator or vendor adapter.',
            'proposed_route': 'Obtain a complete edition-specific technical source, then map its estimand, identification, inference, interface and rights to the same servicing case.',
            'deployment_and_license': 'Unverified for this matched use case.',
            'price': {'status': 'unknown', 'amount': None}, 'vendor_runtime_executed': False,
        })
    assert len(original['families']) == 17 and len(compared) == 3 and len(unresolved) == 14
    gaps = [
        {'capability': 'Fitted conditional-effect and grouped-effect paths', 'current': 'not_implemented',
         'comparison': ['Stata cate', 'JMP Uplift segmentation'],
         'remedy': 'Choose a small declared estimator family and independent-unit public/generated experiment; review open-source reuse before building a duplicate.'},
        {'capability': 'Target and population provenance', 'current': 'partial_contract_and_exact_examples',
         'comparison': ['ATE4', 'ATET86/11', 'constant residualized target214/43'],
         'remedy': 'Bind modifier/control roles, target weights, retained population and normalization. Reject a requested target unsupported by the selected method.'},
        {'capability': 'Fixed-policy monetary evaluation', 'current': 'exact_generated_examples_only',
         'comparison': ['Stata prespecified policy evaluation', 'explicit project cost convention'],
         'remedy': 'Freeze policy before final evaluation, retain account horizon/currency and incremental cost; handle learned-policy selection separately.'},
        {'capability': 'Missingness, overlap and learner diagnostics', 'current': 'no_fitted_pipeline',
         'comparison': ['Stata method-dependent retained rows and propensity tolerance', 'JMP overlap reports'],
         'remedy': 'Record exclusions, support, transformations and sample splitting; do not use computational tolerance as proof of positivity.'},
        {'capability': 'Dependent accounts and calendar uncertainty', 'current': 'research_and_selected_derivations_only',
         'comparison': [],
         'remedy': 'Justify a declared sampling law and inference method; missing vendor evidence cannot establish that a competitor lacks this capability.'},
    ]
    conclusion = 'Three families/four pathways support bounded comparisons; fourteen essential technical families and edition-specific rights/costs remain unresolved. Complete shortlist acceptance is withheld.'
    comparison = {
        'operation_id': OP, 'status': 'inconclusive', 'cutoff': '2026-10-07',
        'source_scope': 'Saved official originals acquired 2026-10-13; exact cutoff identity qualified by each record.',
        'prototype_reference': ref(ROOT / 'src/causalbank/operation_service_v12.py', 'Actual SUPPORTED mapping'),
        'primary_audit': ref(OLD / 'source-audit.json', 'Inspected official sources and project constructions'),
        'prior_cell': ref(ROOT / 'docs/program/comprehensive-v14/work/SW.CELL.effects_heterogeneity.commercial/coverage-review.json', 'Predecessor inconclusive technical coverage'),
        'original_search': ref(OLD / 'search-protocol.json', 'Declared bounded search and cutoff'),
        'original_candidates': ref(OLD / 'candidate-register.json', 'All17 retained vendor families'),
        'original_omissions': ref(OLD / 'omissions-register.json', 'Essential source, runtime and rights limits'),
        'integrated_argument': ref(OLD / 'comparison.tex', 'Existing connected argument in the current reader'),
        'exact_replay': ref(BASE / 'exact-replay.json', 'Reproduced exact targets and net-policy values'),
        'vendors_with_primary_comparison': pathways,
        'vendors_without_essential_primary': unresolved, 'product_gap_comparison': gaps,
        'matched_banking_case': {'question': 'One-time servicing contact and incremental net recovery over a common fixed horizon',
            'population_ATE_USD': '4', 'treated_population_ATET_USD': '86/11',
            'constant_residualized_target_USD': '214/43', 'oracle_AIPW_mean_USD': '4',
            'best_stipulated_fixed_rule': 'lower_risk_only', 'net_USD_per_eligible_account': '3/4',
            'empirical_performance_claim': False},
        'cost_rule': 'Compare license, integration, preprocessing, execution/failure, analyst review and support costs for the same accepted target and output. No amount or bank ROI is supplied.',
        'no_paid_trial_or_contact': True, 'no_absence_inference_from_missing_source': True,
        'conclusion': conclusion,
        'revisit_trigger': 'Acquire the fourteen named technical families, pinned DataRobot notebook/license, current matched Stata/JMP rights and detailed version evidence; run a matched licensed trial only if prototype evidence makes it decision-relevant.',
    }
    write(OUTPUT, comparison)
    write(BASE / 'author-review.json', {
        'status': 'inconclusive', 'scope': 'Observed/proposed capability and commercial make/adapt/compare decisions',
        'findings': [conclusion,
            'Saved Stata options and postestimation text, JMP Uplift/estimand/model prose, and DataRobot overview were reread; all local source bindings verified.',
            'Exact target differences and policy costs replayed without vendor execution. Highest effect is not highest stipulated net value.',
            'Commercial documentation establishes comparison requirements, not implemented local CATE capability.',
            'Prior guide versions, current-version uncertainty and uninspected image equations retain their limits.'],
        'evidence': [ref(OUTPUT, 'Four detailed pathways, fourteen omissions and five implementation gaps'),
                     ref(BASE / 'exact-replay.json', 'Exact-law replay'),
                     ref(OLD / 'comparison.tex', 'Already integrated substantive chapter argument')],
        'limits': ['Author review only; no commercial runtime, bank data, pricing or independent acceptance.'],
        'manuscript_delta': 'No new technical claim or source is added to the reader; structured comparison develops existing integrated argument and local runtime distinction.',
        'next_action': comparison['revisit_trigger'],
    })
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    receipt.update(
        outcome='inconclusive', execution='performed', scope=conclusion,
        reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
        limitations=['Fourteen families lack complete matched primary evidence.',
                     'Edition-specific rights, prices and runtime behavior remain unverified.'],
        outputs=[ref(OUTPUT, 'Commercial heterogeneous-effect comparison')],
        nonexecution_reason='', revisit_trigger=comparison['revisit_trigger'],
        criteria=[
            {'index': 0, 'verdict': 'inconclusive',
             'finding': 'All17 families are retained, with three evidence-backed families/four pathways and fourteen unresolved technical families. Essential evidence is not waived.',
             'evidence': [ref(OUTPUT, 'Version-scoped cases and explicit omissions'),
                          ref(OLD / 'omissions-register.json', 'Preserved source failures')]},
            {'index': 1, 'verdict': 'pass',
             'finding': 'Unverified capabilities remain unknown, execution and rights are unevaluated, and prices have no fabricated values. The comparison names documented strengths and actual local gaps.',
             'evidence': [ref(OUTPUT, 'Runtime, cost and rights boundaries'),
                          ref(BASE / 'author-review.json', 'Reviewed scope and target arithmetic')]},
        ],
    )
    write(BASE / 'operation-receipt.json', receipt)
    transition('record', OP, BASE / 'operation-receipt.json')


if __name__ == '__main__':
    main()
