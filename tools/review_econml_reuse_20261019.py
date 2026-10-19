#!/usr/bin/env python3
"""Authenticate selected EconML originals and complete a bounded proposal decision."""
import hashlib
import json
from pathlib import Path
import tomllib

import econml_semantic_reference_20261019 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
RAW = ROOT/'docs/literature/raw'
BASE = ROOT/'docs/program/execution/2026-10-19/econml-reuse-v1'
OP = 'SW.DECISION.inherited_econml'
OUTPUT = ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
PIN = 'd625dd696ea28c62e6e4d8baea6e4154b98c30b4'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())

# Inclusive original line numbers. Full original bytes remain in RAW.
SPANS = {
    'README.md': [(9, 23), (49, 57)],
    'LICENSE': [(1, 60)],
    'pyproject.toml': [(1, 99)],
    'setup.py': [(1, 40)],
    'econml/_version.py': [(1, 4)],
    'econml/dml/dml.py': [(132, 218)],
    'econml/panel/dml/_dml.py': [(17, 26), (43, 145), (193, 208), (264, 346), (603, 682)],
    'econml/_ortho_learner.py': [(930, 989)],
    'econml/inference/_inference.py': [(55, 108)],
    'econml/sklearn_extensions/linear_model.py': [(1815, 1840), (1939, 2008)],
    'econml/_cate_estimator.py': [(25, 46), (62, 78), (126, 143), (194, 221)],
    'econml/tests/test_dynamic_dml.py': [(50, 115), (254, 303)],
    'doc/spec/estimation/dynamic_dml.rst': [(1, 94)],
    'doc/spec/estimation/dml.rst': [(85, 151)],
    'econml/inference/_bootstrap.py': [(73, 132)],
    'econml/dml/_rlearner.py': [(4, 14), (41, 106), (192, 220)],
    'econml/tests/test_bootstrap.py': [(16, 68), (187, 227), (267, 320)],
}

CLAIMS = [
    'The canonical Python repository is py-why/EconML. The selected pre-cutoff commit declares version 0.17.0; the README records its 31 July 2026 release. These are distinct from authentication of a release wheel.',
    'The pinned root license contains MIT conditions and BSD 3-Clause notices for scikit-learn-derived tree/grf code. Python >=3.9, eleven direct dependency declarations, optional extras and native build requirements are recorded; they do not constitute a resolved environment or complete transitive rights audit.',
    'The selected DML documentation and R-learner code residualize Y and treatment using X and W, then fit an effect function of X. Causal interpretation needs the stated identifying assumptions and effect-model specification.',
    'The final linear path fits cross-products of features and treatment residuals. The alternative weighted path divides by signed treatment residuals clipped at 1e-5 and weights by the original squared residual. This numerical convention cannot create overlap.',
    'The base ate API averages predicted effect over supplied X and contrasts; averaging a misspecified constant projection does not transform it into a correctly specified population effect.',
    'Group labels control cross-fitting splits. cv=1 disables cross-fitting. The inspected static linear covariance supports HC0, HC1 and nonrobust options and warns when rank deficiency invalidates inference; it does not automatically supply clustered or calendar covariance.',
    'DynamicDML counts periods by occurrence within each group, requires equal group counts, uses baseline X for heterogeneity and later X as controls, and targets the final-period outcome in the inspected nuisance path. Its warning explicitly says supplied sample_weight and sample_var are ignored.',
    'The dynamic documentation assumes fully observed dynamic confounders and a specified structural family; it does not establish an arbitrary latent-state policy-value result. Backward treatment residual fitting and cross-period within-unit covariance are visible in the selected implementation.',
    'The dynamic covariance assembles within-unit cross-period score products and divides by the number of groups. This is distinct from qualifying cross-unit common-calendar dependence.',
    'The inspected call chain maps bootstrap inference to BootstrapEstimator.fit, takes DynamicDML._strata=groups, and resamples rows with replacement separately inside each fixed group. The row sequence can duplicate or reorder periods under the encounter-order convention. This is a source composition finding, not a fresh native execution or measured coverage defect.',
    'The inspected upstream dynamic tests include shape/inference cases with two bootstrap draws and selected order-preserving panel layouts under auto inference. Bootstrap tests include interval shapes, internal options and treatment stratification. They were read, not executed; these selected tests do not establish the proposed whole-history resampling contract.',
]

LIMITS = [
    'Author source and exact-reference review only; no installed EconML fit, upstream test or bootstrap execution.',
    'Only selected DML and DynamicDML paths are covered; forest, IV, DR, policy and other estimators need separate profiles.',
    'A source commit with version 0.17.0 is not authenticated identity for every artifact carrying that version.',
    'Resolved wheel/native build, complete dependency notices, numerical conformance and inference calibration remain future prototype admission work.',
    'The projection counterexample deliberately misspecifies a constant effect; it is not a library error under a correctly specified effect model.',
    'Exact panel, resampling and shared-score examples are project constructions, not measured upstream behavior.',
    'No bank truth, measured prices, independent acceptance, visual acceptance or final proposal acceptance is inferred.',
    'Cutoff is 7 October 2026; no unusable web-search output is admitted as evidence.',
]


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    commit = read(RAW/'exec19_econml_cutoff.json')[0]
    assert commit['sha'] == PIN
    date = commit['commit']['committer']['date']
    assert date == '2026-10-01T19:06:40Z'
    tree = read(RAW/'exec19_econml_tree.json')
    assert tree['sha'] == commit['commit']['tree']['sha'] and not tree['truncated']
    blobs = {x['path']: x['sha'] for x in tree['tree'] if x['type'] == 'blob'}
    records, extracts = [], []
    rows = read(BASE/'authenticated-contract-files.json')
    assert len(rows) == len(SPANS) == 17
    folder = BASE/'inspected-excerpts'
    folder.mkdir(exist_ok=False)
    for i, row in enumerate(rows):
        path = ROOT/row['path']
        data = path.read_bytes()
        receipt_path = path.with_suffix('.receipt.json')
        receipt = read(receipt_path)
        url = f'https://raw.githubusercontent.com/py-why/EconML/{PIN}/'+row['upstream']
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert core.sha(path) == row['sha256'] == receipt['sha256']
        assert blob == row['git_blob_sha1'] == blobs[row['upstream']]
        assert receipt['status'] == 'saved' and receipt['url'] == url
        lines = path.read_text().splitlines()
        spans = [dict(first=lo, last=min(hi, len(lines))) for lo, hi in SPANS[row['upstream']]]
        excerpt = folder/f'{i:02d}.txt'
        excerpt.write_text('\n\n'.join('\n'.join(f'{j+1}: {lines[j]}'
            for j in range(s['first']-1, s['last'])) for s in spans)+'\n')
        extracts.append(dict(upstream=row['upstream'], spans=spans, excerpt=ref(excerpt, 'Exact numbered original excerpts')))
        records.append(dict(source_identity=url, upstream_path=row['upstream'],
            version_date=date+'; '+PIN, local_copy=ref(path, 'Selected primary source; see inspected line spans'),
            receipt=ref(receipt_path, 'Original public HTTPS receipt'), git_blob_sha1=blob,
            inspected_anchors=spans, excerpt=extracts[-1]['excerpt'], executed=False))
    write(BASE/'inspected-extracts.json', dict(records=extracts))
    metadata = tomllib.loads((RAW/'exec19_econml_source_2.txt').read_text())
    assert len(metadata['project']['dependencies']) == 11
    assert exact.calculate() == read(BASE/'exact-results.json')

    contract = dict(status='proposed_not_implemented', integration_allowed=False,
        requirements=[
            'Name the contrast, population, effect-function class, units, identifying adjustment assumptions and X/W roles. Distinguish CATE, marginal derivative, population average and misspecified projection.',
            'Preserve keyed rows, treatment categories/reference category and dose scale across nuisances, folds, outcomes and prediction populations; reject positional joins and post-action adjustment without a causal argument.',
            'Require explicit unit/time keys, unique unit-period rows, canonical chronological unit-major order and identical unit alignment across period slices. Refuse unbalanced, missing or duplicate histories until their scientific treatment is declared; padding is not an automatic repair.',
            'Refuse nontrivial requested sample weights or sample variances for this DynamicDML path instead of treating the source warning as successful weighted estimation.',
            'Keep fold grouping, resampling units and covariance law separate. Require a whole-history cluster bootstrap only under its justified independent-unit law; common calendar shocks need a different covariance/design argument.',
            'Capture rank, convergence, support and clipping warnings. Separate a returned number from identified target, supported uncertainty, numerical failure and unsupported input.',
            'Lock exact package and native artifacts, dependencies, optional extras and notices before runnable admission. Preserve source pin, seed, folds, inference choice and every failed run in the returned evidence.',
        ],
        native_oracles=[
            dict(id='target', trial='Recover a correctly specified heterogeneous finite effect and average over a declared population; retain the 450/17 versus 50 misspecification contrast.', failure='Reject relabelling a projection or subgroup effect as population ATE.'),
            dict(id='clock', trial='Reorder keyed inputs, include duplicate/missing periods and compare canonical histories before fitting.', failure='Refuse chronology or cross-period unit misalignment.'),
            dict(id='bootstrap', trial='Instrument the actual pinned resampler with row/unit/time identifiers; compare selected paths to whole-history draws under a declared panel law.', failure='Disable the dynamic bootstrap profile when histories are not preserved; retain evidence before proposing a repair.'),
            dict(id='weights', trial='Supply nonconstant weights and sample variances and inspect warnings and actual fit arguments.', failure='Return unsupported-weight status, not an unweighted answer labelled weighted.'),
            dict(id='uncertainty', trial='Predeclare independent-unit, within-unit serial and common-shock cases with all-request coverage, availability and width.', failure='Qualify only passing declared regimes; do not select a covariance after observing final outcomes.'),
        ])
    write(BASE/'conversion-contract.json', contract)
    omissions = dict(status='recorded_for_prototype_and_other_profiles', candidate_absence_claim=False,
        proposal_decision_complete=True, integration_allowed=False,
        remaining=['Exact wheel/build/dependency identity and complete transitive notice inventory',
            'Matched theorem/regularity review for each admitted estimator and sampling law',
            'Actual pinned bootstrap call-path and chronological-history conformance',
            'Native warnings, missingness, dose/shape/weight and rank trials',
            'Inference calibration and public-data usefulness after a declared prototype',
            'Separate forest, IV, DR and policy-learning source/target profiles'],
        later_bank_gates=['Assignment and audit truth', 'Independent scientific/operating acceptance', 'Observed costs and investment decision'],
        next_step='Build and test one narrowly specified public/synthetic static profile first; dynamic admission waits for chronology, weights and sampling-law resolution.')
    write(BASE/'omissions-register.json', omissions)
    primary = dict(status='pass_for_source_review', reviewer=REVIEWER, claims=CLAIMS,
        evidence=records, limitations=LIMITS, fresh_native_execution=False)
    write(BASE/'primary-review.json', primary)

    source = dict(integrated_citation_key='exec19_econml_source', kind='software_primary_sources',
        title='EconML 0.17.0 selected DML, dynamic-panel, bootstrap, package and test contracts',
        author='PyWhy contributors', year=2026, source_identity='https://github.com/py-why/EconML/tree/'+PIN,
        version_date='0.17.0 declaration; '+date+'; '+PIN,
        local_copy=ref(RAW/'exec19_econml_source_6.txt', 'Dynamic target, ordering, covariance and weight contract'),
        records=records, identity_evidence=[ref(RAW/n, 'Pinned historical repository identity') for n in
            ['exec19_econml_cutoff.json', 'exec19_econml_cutoff.receipt.json', 'exec19_econml_tree.json', 'exec19_econml_tree.receipt.json']],
        inspected_anchors=[dict(anchor=c, inspection='Authenticated primary implementation/documentation') for c in CLAIMS],
        supported_claims=CLAIMS, limitations=LIMITS)
    reference = dict(integrated_citation_key='exec19_econml_reference', kind='project_authored_exact_reference',
        title='Exact effect-projection, panel-clock, history-resampling and common-shock references',
        author='Causal banking proposal project', year=2026,
        source_identity='tools/econml_semantic_reference_20261019.py', version_date='19 October 2026; SHA-256-bound source',
        local_copy=ref(ROOT/'tools/econml_semantic_reference_20261019.py', 'calculate(): exact finite rational enumeration'),
        records=[dict(local_copy=ref(BASE/'exact-results.json', 'Executed exact results'))],
        inspected_anchors=[dict(anchor='calculate()', inspection='Exact arithmetic reproduced without calling EconML')],
        supported_claims=['Constant residual slope 450/17 differs from population effect 50 under the declared misspecification.',
            'Assumed cost 35 gives population net 15 and mislabelled projection net -145/17.',
            'Encounter order can disagree with timestamps despite equal group sizes.',
            'Uniform two-row resampling within a fixed unit preserves the original ordered history with probability 1/4, or 1/16 for two units.',
            'Four perfectly shared fair scores have mean variance 1, versus independent-group working variance 1/4.'],
        limitations=LIMITS[4:7])
    audit = dict(sources=[source, reference], cutoff='2026-10-07', native_execution=False)
    write(BASE/'source-audit.json', audit)
    evidence = [ref(BASE/n, 'Reviewed bounded proposal evidence') for n in
        ['plan-review.json', 'crash-recovery-checkpoint.json', 'authenticated-contract-files.json',
         'inspected-extracts.json', 'primary-review.json', 'source-audit.json', 'exact-results.json',
         'conversion-contract.json', 'omissions-register.json']]+[ref(Path(__file__), 'Exact authentication and decision construction')]
    decision = dict(operation_id=OP, status='pass', decision='reference', integration_allowed=False,
        decision_scope='Completed proposal choice for selected static DML and dynamic-panel comparators; no runnable adapter admission',
        identity=dict(canonical_repository='py-why/EconML', selected_commit=PIN, commit_date=date,
            declared_version='0.17.0', distinct_from='DoubleML, generic PyWhy umbrella, and other EconML estimator families'),
        license=dict(root='MIT plus explicit BSD 3-Clause notices for specified derived code',
            required='Preserve applicable copyright, permission, redistribution, disclaimer and nonendorsement notices',
            complete_transitive_rights=False),
        dependencies=dict(python=metadata['project']['requires-python'], direct=metadata['project']['dependencies'],
            optional=metadata['project']['optional-dependencies'], build=metadata['build-system'], resolved_environment=False),
        maintenance=dict(selected_commit=date, readme_release='31 July 2026', support_guarantee=False),
        target='Conditional effect under declared observed-confounding and effect-function assumptions; dynamic final-outcome effects under the selected fully observed structural family.',
        uncertainty='Estimator- and sampling-law-specific; fold grouping does not supply calendar covariance and the inspected dynamic bootstrap path does not preserve ordered whole histories.',
        rationale=['Reference is useful for transparent residual learning and matched effect-function alternatives.',
            'Direct adoption or a port is premature while target, chronology, weight and resampling conversions are unresolved.',
            'A process-isolated Python adapter is the preferred prototype candidate once the contract passes; no reason currently justifies porting all estimators.',
            'Known static target misspecification and dynamic source-composition risks have reproducible counterexamples and concrete next tests.',
            'The proposal decision is complete without claiming execution, dependency qualification or bank acceptance.'],
        alternatives=['Transparent exact residual-moment implementation under the same target and sampling law',
            'Separately reviewed DoubleML profiles with matched target, weights, nuisance folds and inference',
            'A longitudinal estimator with an explicitly justified history and covariance contract when the dynamic structural family is unsuitable',
            'Refusal or identified-set output when scientific identification is unsupported'],
        costs_to_measure=['Environment/native build and notice inventory', 'History reconstruction and target review',
            'Nuisance fitting, repeated folds and bootstrap refits', 'Diagnostics, failed runs and held-out assessment',
            'Version migration and conformance maintenance'],
        owner_obligations=dict(scientific='Own adjustment, target, sampling and effect-model assumptions',
            engineering='Own keyed conversion, chronological histories, warning/refusal mapping and exact artifacts',
            evaluation='Own public/generated held-out designs and all-request reporting',
            product='Own permissible distribution and later bank thresholds and costs'),
        revisit_trigger=omissions['next_step'], evidence=evidence, limitations=LIMITS,
        capabilities=[], reviewer=REVIEWER)
    write(OUTPUT, decision)
    write(BASE/'review.json', dict(status='pass', reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT, 'Completed reference decision'), findings=CLAIMS,
        evidence=evidence, limitations=LIMITS, integration_allowed=False,
        criterion_interpretation='The contract requires a justified proposal choice and evidence. A reference choice can pass with no integration capability; later native admission is not a bank-data prerequisite for this proposal decision.'))
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    findings = ['Seventeen selected originals authenticate to the pre-cutoff tree; canonical identity, observed notices, dependencies and maintenance are explicit.',
        'Targets, uncertainty, alternatives, costs, ownership and revisit trigger are explained; exact projection, clock, resampling and common-shock constructions reproduce.',
        'Reference decision grants no integration capability. Proposed conversion/failure contract and native oracles make future admission reviewable without pretending the adapter exists.']
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'], reviewer=REVIEWER,
        capabilities=[], outputs=[ref(OUTPUT, 'Scoped reference decision')], limitations=LIMITS,
        nonexecution_reason='', revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i, verdict='pass', finding=f, evidence=evidence+[ref(BASE/'review.json', 'Author decision review')])
            for i, f in enumerate(findings)])
    write(BASE/'operation-receipt.json', receipt)
    verify_bindings([audit, decision, receipt])
    print(json.dumps(dict(operation=OP, outcome='pass', decision='reference', integration_allowed=False,
        authenticated_originals=len(records), native_execution=False)))


if __name__ == '__main__':
    main()
