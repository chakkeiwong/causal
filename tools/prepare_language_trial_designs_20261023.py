#!/usr/bin/env python3
"""Prepare and individually review prospective designs; never run native trials."""
import argparse
from collections import Counter
import json
from pathlib import Path

import language_trial_oracles_20261023 as oracle
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
ROOT = run.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-23/language-trial-designs-v1'
AUDIT = ROOT / 'docs/program/execution/2026-10-23/ltmle-reader-v2/reader/source-audit.json'
read = lambda p: json.loads(p.read_text())


def profiles():
    return {
        'R': dict(engine='pcalg', revision='930fe476875ddc00528dbaacb6f48f2791ab12e3',
            version='2.7-12', contract='docs/program/execution/2026-10-13/pcalg-reuse/adapter-contract-v2.json',
            source_keys=['exec13_pcalg', 'exec13_pcalg_reuse_primary', 'exec13_pcalg_reuse_examples'],
            scope='IID Gaussian PC with strict project CI callback; separate supplied-CPDAG local singleton IDA conformance.',
            settings='Use successor contract v2 unchanged: stable conservative relaxed PC, solve.confl=true, strict CI, no background knowledge; IDA local, y.notparent=false, type=cpdag.',
            exact_cases=[
                'Chain and collider population covariances with X3 isolated, all 24 node permutations; independent exhaustive same-skeleton/same-collider DAG enumeration gives three and one class members.',
                'Supplied three-node chain covariance: local singleton IDA values [0,12/25]; separately labeled global DAG oracle [0,0,12/25]. Do not compare multiplicities as probabilities.',
                'Both inspected matrix accessors: amat.cpdag directed pair 0/1 versus graph adjacency 1/0; named collider, reciprocal 1/1 and conflict 2/2; all six three-node permutations.',
                'Scale treatment by 100 and outcome by 1000: covariance D S D and each derivative by 10; retain original units and no fabricated confidence set.',
                'Use an exact CI callback for population graph conformance; the statistical trial uses the separately admitted strict numerical callback. Never claim an infinite population covariance is a random n-row sample.'
            ],
            stress=[
                dict(case='Duplicate column, constant column, invalid df, nonfinite or non-SPD covariance, and SPD condition number above 1e10 after standardization', expected='Typed numerical/input failure before publishing a graph; no clipping, pseudoinverse or p=0 fallback.'),
                dict(case='Conflict 2/2 or a partial graph with no consistent extension sent to IDA', expected='Typed invalid/unsupported graph, no numeric vector; preserve raw accessor and marks.'),
                dict(case='Declared clustered/repeated rows, missingness, latent/PAG model, nonlinear/binary outcome or background constraints', expected='Unsupported current profile; no silent deletion, graph coercion or confidence label.'),
                dict(case='Replace chain coefficient 3/5 by 1/100; hidden U in both X0 and X2; duplicated latent cluster shocks without a declared cluster flag', expected='Descriptive degradation experiment only; no universal detectable-validity claim. Separate from regular screens.'),
                dict(case='Callback throws or times out mid-search; process cancellation, truncated response, or changed covariance coordinates', expected='No graph/effect publication; retain first attempt failure and exact input identity.')],
            oracle_refs=['docs/program/execution/2026-10-13/pcalg-reuse/exact-results.json',
                         'tools/pcalg_reuse_examples_20261013.py'],
            findings=[
                'Matches the corrected pcalg v2 contract, independent Markov-class enumeration, exact IDA multiplicities, accessor/units and adverse failure cases. Four Gaussian cells have fixed sample sizes, two complete-denominator events, exact binomial power, thresholds and stopping rules.',
                'Pins source identity without pretending to pin an installed environment. Registration requires strict callback and graph validation admission, complete environment and fresh-data custody; passing this proposal design grants no engine execution or statistical capability.'
            ]),
        'Java': dict(engine='Tetrad', revision='b89afaf952a4fd647df0d85b08102250106c6764',
            version='7.6.11-SNAPSHOT', contract='docs/program/comprehensive-v14/work/IN.DESIGN.Java/adapter-contract.json',
            source_keys=['exec13_java_tetrad', 'exec13_java_adapter_source', 'exec13_java_adapter_contract', 'exec13_java_adapter_oracles'],
            scope='Tetrad PC/Fisher-Z on complete IID Gaussian data with failure-transparent test wrapper and explicit CPDAG validation.',
            settings='setDepth(-1), stable FAS, SEPSETS collider rule, DISALLOW bidirected, forbid directed cycles, empty knowledge; complete/FAIL missing policy, shrinkage NONE, ridge=0, pseudoinverse=false; wrapper uses getResult, never singularity-to-p0 checkIndependence.',
            exact_cases=[
                'Same chain/collider four-variable population laws and 24 permutations as R; compare complete named CPDAGs including isolated nodes, not one convenient DAG.',
                'Independent exact original Java covariance [[1,4/5,2/5],[4/5,1,1/2],[2/5,1/2,1]] has three DAGs and effect multiset [0,0,2/5]; this is a downstream illustration only, never a PC effect result.',
                'Endpoint pairs tail/arrow and reversed-node arrow/tail round-trip; unexpected circles or bidirected conflicts fail current profile; graph-class recognition must go beyond syntax.',
                'All CI calls receive unique IDs and terminal records; injected getResult failure sets a persistent job failure latch even if search catches an exception.',
                'Native search with a deterministic exact CI oracle is a separate conformance instrument from the admitted numerical Fisher-Z search. A missing independence-test wrapper/interface is a registration blocker.'
            ],
            stress=[
                dict(case='Singular covariance, |partial correlation|>=1, nonpositive residual variance, insufficient df or condition number above 1e10', expected='Numerical failure with no graph; never p=0 independence-test substitution.'),
                dict(case='Declared missingness, categorical data, latent causes, selection, repeated accounts, background knowledge or bounded search depth', expected='Unsupported initial profile with specific alternative; no complete-CPDAG claim.'),
                dict(case='Every node permutation, isolated-node roundtrip, reversed endpoint ordering and corrupt graph coordinates', expected='Exact named-object preservation or typed invalid output; no undocumented orientation.'),
                dict(case='Weak chain 1/100, unobserved common cause of X0/X2, and undisclosed shared shocks', expected='Descriptive errors outside regular scope, not mandatory detection of unobservable violations.'),
                dict(case='Interrupted FAS, parallel CI race, exception caught by search, parent timeout and cancellation/publication race', expected='All-query terminal audit and atomic publication; missing/failed query withholds graph; first attempt retained.')],
            oracle_refs=['docs/program/execution/2026-10-13/java-integration/oracle-results.json',
                         'tools/java_adapter_oracles_20261013.py'],
            findings=[
                'Matches Tetrad PC settings and retained scientific restrictions, independent exhaustive Gaussian graph classes and endpoint/failure oracles. Four matched cells use fixed n, 2000 replications, complete-denominator graph/availability events, exact power and fixed stopping.',
                'Design does not grant deferred Tetrad integration permission or claim a compiled failure-transparent wrapper. Full interface/build/graph-validator and environment admission precede registration; graph alpha is never reported as graph confidence or effect coverage.'
            ]),
        'Python': dict(engine='y0', revision='cc6644d3b470a1ab2a1eb9da4f0fdb0c843f5d3a',
            version='0.2.12-dev', contract='docs/program/comprehensive-v14/work/IN.DESIGN.Python/adapter-contract.json',
            source_keys=['exec13_y0_api', 'exec13_y0_id', 'exec13_y0_idc', 'exec13_y0_rule2',
                         'exec13_y0_separation', 'exec13_y0_graph', 'exec13_y0_dsl',
                         'exec13_y0_metadata', 'exec13_y0_license', 'exec13_y0_oracles'],
            scope='Single finite-discrete DAG/ADMG unconditional ID and sufficient joint-ID normalization for conditional queries; no native IDC or numeric effect estimation.',
            settings='identify_outcomes with strict=True and validated ordering; conditional queries identify joint (Y,Z) and normalize within typed lexical AST. Pinned native IDC remains disabled.',
            exact_cases=[
                '72 explicit positive rational laws: 48 front-door, 12 back-door and 12 no-treatment-effect. Six variable permutations each give 432 requests, with both treatment coordinates evaluated independently (864 exact values).',
                'For each law evaluate the returned observational AST against the enumerated observed joint, then compare with independent structural intervention enumeration. Preserve lexical bound variables in the inner front-door sum.',
                'Bow graph: one strictly positive observed law shared by two allowed-edge SCMs with effects 3/5 and zero. Two variable permutations must not return an identified functional for the unconditional effect.',
                'Bidirected collider Y<->B<->Z with isolated X: all 24 name permutations preserve conditional P(Y=1|do(X),B=1,Z=1)=9/10. Independent do(Z) conditional equals 1/2, demonstrating why the rejected rule-2 exchange is invalid.',
                'The positive-law corpus plus two bow and 24 collider permutations gives 458 scientific requests; every required behavior must pass. Finite enumeration has no sampling-power or CI claim.'
            ],
            stress=[
                dict(case='Cycle, duplicate symbol, missing treatment/outcome, unknown AST subclass, bound-variable capture or free-variable mismatch', expected='Invalid/unsupported typed request or output; no executable source evaluation.'),
                dict(case='Zero conditional denominator under a boundary law', expected='Unsupported coordinate with support diagnostics; never zero/infinity by convention.'),
                dict(case='Joint ID fails for a conditional query', expected='CONDITIONAL_JOINT_ROUTE_FAILED unsupported; not proof of conditional nonidentification.'),
                dict(case='PAG/CPDAG/graph set, cross-world query, transport, intervention-valued AST or confidence interval request', expected='Unsupported profile; preserve graph and target without a fabricated scalar or set.'),
                dict(case='Dependency error, ordering ValueError, timeout, cancellation or malformed serialization', expected='Typed runtime/input failure distinct from native Unidentifiable; retain all attempts.')],
            oracle_refs=['docs/program/execution/2026-10-13/python-integration/oracle-results.json',
                         'tools/python_identification_oracles_20261013.py'],
            findings=[
                'Independent structural sums and observational functionals agree on 72 rational laws; 458 declared requests include permutations, nonidentification twins and the conditional rule-2 counterexample. Explicit AST/support failures, dollar-transported numeric tolerances and exhaustive fixed stopping replace inapplicable sampling-coverage claims.',
                'Source pin is distinct from an installed environment. Native IDC remains excluded and joint-route failure is not conditional nonidentification. Passing this design neither imports y0 nor qualifies general completeness, estimation or intervals; adapter admission and exact environment remain registration prerequisites.'
            ]),
        'Cxx': dict(engine='grf native core through maintained R frontend', revision='5bee99b51471f76cb2d63acbc8a9b0ffec408ba0',
            version='2.6.1', contract='docs/program/comprehensive-v14/work/IN.DESIGN.Cxx/adapter-contract.json',
            source_keys=['exec13_grf_rpath', 'exec13_grf_native', 'exec13_grf_memory', 'exec13_grf_runtime',
                         'exec13_grf_design', 'exec13_grf_oracle', 'exec21_grf_reuse', 'exec21_grf_reference'],
            scope='Complete independent customer rows, binary action and all-population AIPW ATE through maintained R/native route; no standalone native embedding admission.',
            settings='2000 trees, honesty=true, ci.group.size=2, sample.fraction=.5, min.node.size=5, honesty.fraction=.5, prune=true, alpha=.05, imbalance.penalty=0, stabilize.splits=true, OOB=true, tune.parameters=none, threads=1; mtry=min(ceil(sqrt(p)+20),p)=4; no weights/clusters; target.sample=all, method=AIPW.',
            exact_cases=[
                'Existing project C++ versus rational references: column-major roles, local slope 3, zero local denominator refusal, AIPW aggregation and squared-unit distinction; never call those project examples a grf run.',
                'Use the later exact nuisance-reference grid: correct m and tau with wrong e need not be unbiased; reconstructed outcome surfaces and propensity give the actual score identity. 108 rational cases compare two independent score formulas.',
                'The earlier target witness with group propensities (1/2,1/10) has all/treated/control/overlap effects 4,-4/3,44/7,4/17. Preserve each target label; it is distinct from F2 trial propensities (1/5,4/5).',
                'Native results recompute AIPW scores from exported aligned OOB nuisance/prediction vectors using an independent scalar formula. Mean fitted CATE and mean CATE variances are invalid ATE substitutes.',
                'R residualization, borrowed column-major memory lifetime, consumed forest serialization and reload metadata are conformance requirements. Native/R parity is conditional on an identical execution path, not a claim of a stable standalone ABI.'
            ],
            stress=[
                dict(case='Known propensity 0 or 1, no treated/control support, nonfinite scores or zero local denominator', expected='Explicit refused/unavailable result with target retained; no silent trimming, overlap substitution or zero estimate.'),
                dict(case='Weak positive propensity (.01,.99), rare treatment leaves and true heterogeneous effects', expected='Descriptive width/failure/coverage stress at 200 prespecified replications per cell, n=2000; no tuning or claim of regular-cell power.'),
                dict(case='Declared repeated/cluster rows, sample weights, continuous treatment, IV, longitudinal action or externally fitted nuisance vectors', expected='Unsupported initial profile; a later reviewed profile needs its own target and split/inference argument.'),
                dict(case='Hidden confounding with U affecting both W and Y or post-action covariates mislabeled as baseline', expected='Record scientific violation/degradation; no claim software can detect every unobserved violation.'),
                dict(case='Unit rescaling, treatment label reversal, column-major corruption, OOB/newdata confusion, forest reuse after consuming serialization, timeout/cancellation', expected='Exact target/units preserved or typed failure; no stale-memory or partial-result publication.')],
            oracle_refs=['docs/program/execution/2026-10-13/grf-cxx/reproduction-review.json',
                         'tools/grf_boundary_oracle_20261013.cpp',
                         'tools/grf_reuse_reference_20261021.py',
                         'docs/program/execution/2026-10-21/grf-reuse-v1/exact-results.json'],
            findings=[
                'Three explicit known-law ATE cells have independent analytic truth/score variances, matched baselines, complete interval-failure/useful-width denominators, 2000 replications each, exact screen power and fixed stopping. Existing score/target/memory references and adverse regimes prevent CATE, overlap or native-boundary substitutions.',
                'The reviewed native alias grants no integration permission; this design preserves that dependency and treats a maintained-R/native route as conditional on an explicit admission receipt. No grf run, direct-native ABI, nominal calibration, deployment or bank performance is claimed.'
            ])}


def prepare():
    assert not (BASE / 'oracle-results.json').exists()
    result = oracle.calculate()
    write(BASE / 'oracle-results.json', result)
    sources = {s['integrated_citation_key']: s for s in read(AUDIT)['sources']}
    common = [ref(BASE / 'plan.md', 'Reviewed sequential preparation plan'),
              ref(BASE / 'common-contract.md', 'Fixed laws, screens, denominators and stopping'),
              ref(ROOT / 'tools/language_trial_oracles_20261023.py', 'Independent exact oracle and rational power calculations'),
              ref(BASE / 'oracle-results.json', 'No native execution or random draws')]
    for language, profile in profiles().items():
        target = BASE / language
        target.mkdir()
        audited = [sources[k] for k in profile['source_keys']]
        for source in audited:
            verify_bindings(source)
            assert source.get('source_identity') and source.get('version_date')
        write(target / 'source-audit.json', dict(cutoff='2026-10-07', sources=audited,
            inherited_audit=ref(AUDIT, 'Unchanged authenticated primary and project records'), new_sources=False))
        if language in ['R', 'Java']:
            cells = [dict(id=f'{language}.{kind}.n{n}', law=kind, n=n, replications=2000,
                events=['graph_mismatch', 'unavailable_or_useless'])
                for kind in ['chain', 'collider'] for n in [500, 2000]]
        elif language == 'Cxx':
            cells = [dict(id=f'Cxx.{v["cell"]}', n=2000, replications=2000,
                population_ATE=v['population_ATE'], oracle_score_variance=v['oracle_score_variance'],
                events=['interval_failure', 'unavailable_or_useless']) for v in result['forest']]
        else:
            cells = []
        design = dict(schema_version='1.0', operation=f'SW.DESIGN.{language}',
            status='reviewed_prospective_proposal_design_not_registered_or_executed',
            language=language, scope=profile['scope'],
            engine=dict(name=profile['engine'], revision=profile['revision'], version=profile['version'],
                        installed=False, environment_lock=None),
            adapter_contract=ref(ROOT / profile['contract'], 'Applicable preserved source-reviewed contract'),
            settings=profile['settings'], deterministic_cases=profile['exact_cases'],
            adverse_regimes=profile['stress'], regular_cells=cells,
            screen_rules={k: result['screens'][k] for k in sorted({e for v in cells for e in v['events']})},
            active_screen_count=sum(len(v['events']) for v in cells),
            all_source_records=ref(target / 'source-audit.json', 'Original inspected evidence; no new coverage claim'),
            independent_references=[ref(ROOT / p, 'Preserved independent finite reference') for p in profile['oracle_refs']],
            common_contract=common,
            registration_prerequisites=[
                'Existing reuse decision permits the actual route; no new permission or capability is granted by design.',
                'Actual named engine and adapter satisfy IN.ADAPTER admission with source/binary and all dependency identities.',
                'Freeze complete source/runtime/compiler/OS/BLAS/options/thread/rights environment; missing lock blocks registration.',
                'Independently review and freeze generator/evaluator implementations, final seed custody and exact stream derivation before any final data draw.',
                'Engineering resource preflight and available prototype compute allocation support the frozen request budget.',
                'Register hashes, complete request schedule, exact thresholds, first-attempt rule, adverse cases and fixed stopping.'
            ],
            deterministic_acceptance='Every prescribed valid and typed adverse conformance case must pass; any failure blocks conformance. No probabilistic claim from finite enumeration.',
            fixed_stopping='No favorable early stop or seed/sample replacement. Complete frozen schedule; integrity/resource catastrophe yields incomplete with no passing gate. New design means a preserved successor and fresh data.',
            result_fields=['request_id', 'first_attempt_id', 'input_and_context_hash', 'engine_and_environment',
                'actual_options', 'status', 'result_or_null', 'target', 'units', 'raw_warnings',
                'failure_reason', 'attempt_count', 'wall_cpu_memory', 'complete_workflow_cost_components'],
            native_execution=False, integration_allowed=False, proposal_accepted=False,
            limitations=['Design is not engine conformance, statistical qualification or final proposal acceptance.',
                'Fixed public/generated laws do not establish bank assumptions or broad software coverage.',
                'Graph sets and symbolic expressions have no fabricated sampling-confidence or width metric.',
                'Exact pins establish source identity; installed environment and final-trial randomness are not supplied.'],
            criterion_findings=profile['findings'])
        verify_bindings(design)
        write(target / 'trial-design.json', design)
    write(BASE / 'preparation-review.json', dict(status='pass_for_individual_review',
        evidence=common+[ref(Path(__file__), 'Design preparation and review logic')],
        active_screen_count=22, reserved_screens=24, exact_family_bound='22/480',
        findings=['R successor contract corrects old accessor and CI assumptions.',
            'Cxx and Java source choices retain missing integration capabilities.',
            'Different tasks are not ranked as generic language performance.',
            'R/Java graph error and Cxx interval error have different meanings and thresholds.',
            'Rational screen calculations preceded all native results; no random data generated.'],
        native_execution=False, final_acceptance=False))
    print(json.dumps(dict(prepared=list(profiles()), exact_finite_laws=72, active_screens=22, native_runs=0)))


def review(language):
    state = run.core.read(ROOT, run.core.STATE)
    graph, merged, _ = run.combined(ROOT, state)
    key = f'SW.DESIGN.{language}'
    node = run.ledger.operation(graph, key)
    assert key not in merged['execution_program']['results']
    assert not run.ledger.blockers(merged, node)
    assert state['execution_runtime']['active'] is None
    base = BASE / language
    design = read(base / 'trial-design.json')
    verify_bindings(design)
    assert oracle.calculate() == read(BASE / 'oracle-results.json')
    assert design['engine']['environment_lock'] is None and not design['native_execution']
    assert len(design['criterion_findings']) == len(node['criteria']) == 2
    if language == 'Python':
        assert not design['regular_cells'] and not design['screen_rules']
        import python_identification_oracles_20261013 as py
        expected = read(ROOT / 'docs/program/execution/2026-10-13/python-integration/oracle-results.json')
        for field, function in [('frontdoor', py.frontdoor), ('bow', py.bow), ('bidirected_collider', py.collider)]:
            assert function() == expected[field]
    elif language == 'R':
        import pcalg_reuse_examples_20261013 as pc
        actual = json.loads(json.dumps(pc.run(), default=str))
        assert actual == read(ROOT / 'docs/program/execution/2026-10-13/pcalg-reuse/exact-results.json')
    elif language == 'Cxx':
        import grf_reuse_reference_20261021 as grf
        assert grf.calculate() == read(ROOT / 'docs/program/execution/2026-10-21/grf-reuse-v1/exact-results.json')
    else:
        import java_adapter_oracles_20261013 as java
        actual = json.loads(json.dumps(java.chain_class(), default=str))
        assert actual == read(ROOT / 'docs/program/execution/2026-10-13/java-integration/oracle-results.json')['gaussian_equivalence_class']
    for cell in design['regular_cells']:
        assert cell['replications'] == 2000
        assert set(cell['events']) <= design['screen_rules'].keys()
    output = ROOT / node['outputs'][0]
    assert not output.exists()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes((base / 'trial-design.json').read_bytes())
    evidence = [ref(base / 'trial-design.json', 'Individually authored prospective design'),
        ref(output, 'Contracted trial design'), ref(BASE / 'preparation-review.json', 'Scientific plan review'),
        ref(Path(__file__), 'Individual validation with oracle replay')]
    evidence += design['common_contract'] + design['independent_references'] + [design['all_source_records']]
    review_ = dict(status='pass_for_prospective_design_only', operation=key,
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        findings=design['criterion_findings'], evidence=evidence,
        source_pin=design['engine'], active_screen_count=design['active_screen_count'],
        native_execution=False, registration_complete=False, integration_allowed=False,
        original_gap_qualification=False, limitations=design['limitations'])
    verify_bindings(review_)
    write(base / 'review.json', review_)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope=design['scope']+' Prospective design only.',
        reviewer=review_['reviewer'], limitations=design['limitations'],
        original_gap_qualification=False, capabilities=[], nonexecution_reason='',
        revisit_trigger='Engine/route admission, a complete frozen environment and reviewed generator/evaluator with fresh randomness permit registration. Any changed law/target/settings needs a preserved successor design.',
        outputs=[ref(output, 'Required language-specific design')],
        criteria=[dict(index=i, verdict='pass', finding=f,
            evidence=evidence+[ref(base / 'review.json', 'Individual author review')])
            for i, f in enumerate(design['criterion_findings'])])
    run.validate_receipt(ROOT, merged, node, receipt, len(state['execution_program']['turns']))
    write(base / 'operation-receipt.json', receipt)
    print(json.dumps(dict(operation=key, outcome='pass_for_design', native_execution=False,
        active_screens=design['active_screen_count'], registration_complete=False)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'review'])
    parser.add_argument('language', nargs='?', choices=['R', 'Java', 'Python', 'Cxx'])
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    else:
        assert args.language
        review(args.language)


if __name__ == '__main__':
    main()
