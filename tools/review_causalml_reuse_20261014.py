#!/usr/bin/env python3
"""Audit a pinned CausalML proposal route without importing upstream code."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import tomllib

import run_program as control
from discovery_journey_20261013 import ROOT, ref, write, now

BASE = ROOT / 'docs/program/execution/2026-10-14/causalml-reuse'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work/SW.DECISION.inherited_causalml/decision.json'
PIN = '49283de921ba66379bab71305d471de6ce893d34'
RAW = ROOT / 'docs/literature/raw'


def exact_examples():
    # A declared two-stratum law, not empirical customer data or a package fit.
    px, propensity = [F(1, 2), F(1, 2)], [F(1, 5), F(4, 5)]
    mu0, mu1 = [F(100), F(120)], [F(105), F(135)]
    tau = [a-b for a, b in zip(mu1, mu0)]
    treated = sum(p*e for p, e in zip(px, propensity))
    ate = sum(p*t for p, t in zip(px, tau))
    att = sum(p*e*t for p, e, t in zip(px, propensity, tau))/treated
    atc = sum(p*(1-e)*t for p, e, t in zip(px, propensity, tau))/(1-treated)
    naive = (sum(p*e*y for p, e, y in zip(px, propensity, mu1))/treated
             - sum(p*(1-e)*y for p, e, y in zip(px, propensity, mu0))/(1-treated))
    targeted_net = sum(p*max(t-F(8), F(0)) for p, t in zip(px, tau))
    assert (ate, att, atc, naive, targeted_net) == (F(10), F(13), F(7), F(25), F(7, 2))
    # The R-loss identity is checked algebraically for every cell of this law.
    residuals = []
    for x, e in enumerate(propensity):
        marginal = (1-e)*mu0[x]+e*mu1[x]
        for treatment in (0, 1):
            y = [mu0, mu1][treatment][x]
            residual = F(treatment)-e
            pseudo = (y-marginal)/residual
            assert pseudo == tau[x]
            residuals.append({'x': x, 'treatment': treatment, 'pseudo_outcome': str(pseudo),
                              'weight': str(residual**2)})
    return {'kind': 'exact_project_reference', 'package_execution': False, 'random_draws': 0,
            'law': {'population_mass': list(map(str, px)), 'propensity': list(map(str, propensity)),
                    'conditional_mean_control_USD': list(map(str, mu0)),
                    'conditional_mean_treatment_USD': list(map(str, mu1))},
            'cate_USD': list(map(str, tau)), 'ate_USD': str(ate), 'att_USD': str(att),
            'atc_USD': str(atc), 'unadjusted_contrast_USD': str(naive),
            'policy': {'cost_USD': '8', 'treat_stratum': 1,
                       'net_gain_per_eligible_account_USD': str(targeted_net),
                       'net_gain_if_treat_all_USD': str(ate-F(8)),
                       'scope': 'Known imposed means and costs; no learned-policy value inference or bank ROI.'},
            'r_loss_cells': residuals,
            'rare_arm_bootstrap': {'treated_fraction': '1/100', 'sample_size': 100,
                                    'probability_no_treated': float(F(99, 100)**100),
                                    'scope': 'Exact row-resampling probability, not an observed upstream exception.'},
            'limitations': ['No finite-sample coverage, hidden-confounding diagnosis, transport or package-runtime claim.',
                            'CATE is a conditional mean contrast, not an identified individual treatment effect.']}


def main():
    assert not OUTPUT.exists(), 'Preserve completed decisions; use a new reviewed attempt for revisions.'
    head = json.loads((RAW/'head_causalml.json').read_text())
    tree = json.loads((RAW/'exec14_causalml_tree.json').read_text())
    assert head['sha'] == tree['sha'] == PIN and tree['truncated'] is False
    assert head['commit']['committer']['date'][:10] <= '2026-10-07'
    indexed = {x['path']: x for x in tree['tree']}
    selection = [
        ('pyproject', 'pyproject.toml', 'lines 1-117: version, Python, required/optional/build dependencies',
         ['Declares version 0.17.0, Python >=3.11 and 18 required dependencies; this is not a resolved environment.']),
        ('license', 'LICENSE', 'complete 13-line license notice',
         ['Root notice declares Apache License 2.0, copyright Uber 2019; dependency and bundled-file rights need their own review.']),
        ('readme', 'README.md', 'lines 15-39, 61-80: scope, documentation and support disclaimer',
         ['Describes CATE/uplift, targeting and experimental APIs; support and result quality are not measured here.']),
        ('tlearner', 'causalml/inference/meta/tlearner.py', 'lines 105-181, 188-242, 316-410',
         ['Fits separate arm means with a shared control model; sorts non-control labels and returns one contrast column per label.',
          'CATE intervals use prediction percentiles; default ATE intervals combine residual variances and fitted-effect variance.',
          'ATE point average is over prediction rows, while multi-arm variance uses each treatment/control subset; restrict the first route to binary treatment.']),
        ('rlearner', 'causalml/inference/meta/rlearner.py', 'lines 102-206: nuisance fitting, residual outcome and weighted effect fit',
         ['Uses out-of-fold outcome residuals and (W-p)^2 weighted regression on (Y-m)/(W-p).',
          'Delegates propensity construction and residual splitting; inspecting this caller alone does not validate nuisance leakage or dependent-data folds.']),
        ('base', 'causalml/inference/meta/base.py', 'lines 25-49, 118-149: bootstrap clone and resampling',
         ['Resamples row indices with replacement; this is not a household, panel or calendar block bootstrap.',
          'Unseeded bootstrap calls use global NumPy state; retained-ensemble seeds do not independently fix stochastic base learners.']),
        ('metrics', 'causalml/metrics/visualize.py', 'lines 118-193: get_cumlift population and observed-outcome branches',
         ['Cumulative lift uses known true effects when supplied, otherwise treated/control observed means with interpolation.',
          'Computability of observational uplift curves is not proof of identification or out-of-sample policy value.']),
        ('chooser', 'docs/choosing_an_estimator.rst', 'lines 12-53, 65-150: assumption branches and capability matrix',
         ['Distinguishes randomized, observational, noncompliance, hidden-confounder and target situations.',
          'The proxy/CEVAE branch does not by itself establish proxy identification; those methods are outside this selected path.']),
        ('changelog', 'docs/changelog.rst', 'Unreleased heading and first dataset/tree entries',
         ['Contains unreleased work; the pinned revision must not be equated to a PyPI release or measured local CI success.'])]
    sources = []
    for key, upstream, anchor, claims in selection:
        path = RAW/f'exec14_causalml_{key}.txt'
        receipt_path = RAW/f'exec14_causalml_{key}.receipt.json'
        receipt = json.loads(receipt_path.read_text())
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert receipt['status'] == 'saved' and receipt['sha256'] == hashlib.sha256(data).hexdigest()
        assert receipt['url'] == f'https://raw.githubusercontent.com/uber/causalml/{PIN}/{upstream}'
        assert indexed[upstream]['sha'] == blob
        sources.append({'source_identity': receipt['url'], 'revision': PIN,
                        'source_date': head['commit']['committer']['date'],
                        'acquired_utc': receipt['accessed_utc'], 'local_copy': ref(path, anchor),
                        'acquisition_receipt': ref(receipt_path, 'Public HTTPS receipt'),
                        'git_blob_sha1': blob, 'tree_identity_verified': True, 'supported_claims': claims})
    project = tomllib.loads((RAW/'exec14_causalml_pyproject.txt').read_text())
    primary = {'reviewed_at': now(), 'cutoff': '2026-10-07', 'revision': PIN,
               'identity': ref(RAW/'head_causalml.json', 'Commit SHA and date; metadata establishes identity only'),
               'tree': ref(RAW/'exec14_causalml_tree.json', 'Complete 278-entry pinned tree and inspected blob hashes'),
               'sources': sources, 'declarations': project['project'],
               'build_requirements': project['build-system']['requires'],
               'maintenance_evidence': {'test_and_workflow_paths': [x['path'] for x in tree['tree'] if x['path'].startswith(('tests/', '.github/workflows/'))],
                                        'limit': 'File existence and changelog are not passing CI, support guarantees or measured maintenance cost.'},
               'uninspected_dependencies': ['causalml.propensity implementation and its fold construction',
                                            'meta.utils input checks, serialization and explainer import chain',
                                            'resolved direct/transitive distributions and per-file notices'],
               'package_execution': False}
    write(BASE/'primary-review.json', primary)
    write(BASE/'oracle-results.json', exact_examples())
    contract = {'status': 'proposal_contract_not_implemented', 'pin': PIN,
                'first_profile': 'Binary-treatment static conditional mean contrast using BaseTRegressor and an explicit simple base regressor; independent whole accounts.',
                'initial_implementation': ['Fit with explicit learner, control_name and keyword arguments.',
                                           'Predict on separately identified target-population rows; preserve original row and feature IDs.',
                                           'Return CATE with its population and treatment-minus-control units. An ATE needs explicit population weights.',
                                           'Expose uncertainty only as the actual method computed; no interval becomes a general coverage guarantee.'],
                'required_context': ['target', 'population/target weights', 'treatment and control labels', 'pre-action feature clock',
                                     'outcome horizon and money units', 'sampling unit', 'identification assumptions',
                                     'data identity', 'source/environment identities', 'learner/fold/bootstrap settings and all seeds'],
                'assumptions': 'Consistency, overlap, supplied randomization or conditional exchangeability, independent units, and estimable conditional outcome means; package predictions cannot certify them.',
                'conversion': ['Require finite aligned arrays, unique IDs, declared pre-treatment features and both treatment arms.',
                               'Use returned t_groups to map every contrast; preserve sign and units; reject unknown/missing/duplicate rows.',
                               'Initial profile rejects multiple treatments, time-varying treatment, latent states, dependent calendars and censoring.',
                               'CATE bounds apply to conditional means; do not emit them as individual effect bounds or policy-value intervals.'],
                'failures': {'missing_arm': 'unavailable; no zero-effect substitute', 'overlap_failure': 'refused or declared unsupported target',
                             'nan_or_infinite': 'unavailable with diagnostics', 'bootstrap_failed_arm': 'retain failure; no silent replicate deletion',
                             'unfitted_or_absent_ensemble': 'invalid_request/unavailable', 'unknown_confounding': 'conditional estimate or refusal, never verified causal truth',
                             'timeout': 'unavailable/cancelled with null result'},
                'bootstrap_rules': 'Declare row resampling and size, save random state for every stochastic component, require both arms and retain failed replicates. Do not silently stratify or substitute blocks.',
                'prospective_oracles': ['Exact two-stratum means and ATE=10, ATT=13, ATC=7 versus raw contrast=25.',
                                        'Permuting row/feature IDs, relabeling binary arms and converting USD to cents preserves the named contrast.',
                                        'Separate target mix changes its weighted mean without changing fitted conditional contrasts.',
                                        'Missing arm, unsupported sampling, stale predictions, missing bootstrap ensemble, nonfinite output and cancellation are explicit failures.',
                                        'Only a registered engine comparison can establish finite-sample interval/availability behavior.'],
                'oracle': ref(BASE/'oracle-results.json', 'Exact imposed-law references; no package execution'),
                'runtime_qualification': False}
    write(BASE/'conversion-contract.json', contract)
    decision = {'operation_id': 'SW.DECISION.inherited_causalml', 'canonical_package': 'Uber CausalML',
                'aliases': ['causalml PyPI distribution', 'uber/causalml source repository'],
                'alias_boundary': 'Causal machine learning is a field; EconML, DoWhy, grf and causal-learn are distinct engines.',
                'decision': 'defer', 'preferred_proposal_route': 'Integrate an optional pinned Python T-learner service after scoped import/dependency review and engine fixtures.',
                'decision_scope': 'Completed proposal selection and reuse review; defer executable admission, not the proposal or all other research.',
                'revision': PIN, 'revision_date': head['commit']['committer']['date'], 'declared_version': project['project']['version'],
                'cutoff': '2026-10-07', 'license': {'declared': 'Apache-2.0', 'source': sources[1]['local_copy'],
                                               'next': 'Preserve the full applicable license/notice chain and review bundled/transitive materials before redistribution.'},
                'direct_dependencies': project['project']['dependencies'],
                'integration_allowed': False, 'runtime_qualification': False, 'original_gap_qualification': False,
                'primary_evidence': ref(BASE/'primary-review.json', 'Nine source blobs matched to one cutoff-eligible revision'),
                'conversion_failure_contract': ref(BASE/'conversion-contract.json', 'Target preservation, initial profile and failure contract'),
                'behavioral_oracle': ref(BASE/'oracle-results.json', 'Exact imposed-law algebra and bootstrap failure probability'),
                'rationale': ['A narrow upstream wrapper reduces duplication of meta-learner and bootstrap maintenance.',
                              'A source review cannot qualify the package import chain, dependency environment or its interval behavior.',
                              'Ranking and flexible regression do not solve confounding, observation errors or temporal dependence.',
                              'Binary treatment avoids the observed multi-arm point/variance population mismatch until separately reviewed.'],
                'alternatives': [{'route': 'adopt entire package', 'disposition': 'not selected', 'reason': 'IV, neural proxies, forests, targeting and static meta-learners have different assumptions and import requirements.'},
                                 {'route': 'port T/R learner implementations', 'disposition': 'not selected', 'reason': 'No demonstrated embedding constraint justifies ownership of upstream API, bootstrap and dependency fixes.'},
                                 {'route': 'native exact stratified baseline', 'disposition': 'retain as comparator', 'reason': 'Transparent small problem behavior supplies an oracle and shows when complex ML is unnecessary.'},
                                 {'route': 'EconML/grf', 'disposition': 'separate comparator decisions', 'reason': 'Use their own pins and uncertainty contracts; do not inherit CausalML admission.'}],
                'costs_to_measure': ['Optional-environment installation/import and disk', 'fit/predict/bootstrap elapsed time and peak memory',
                                     'data conversion and analyst correction', 'failed requests and upgrades', 'dependency and notice maintenance'],
                'owner_obligations': {'adapter_maintainer': 'Own pinned import path, lockfile, notices, conversions and failure preservation.',
                                     'scientific_reviewer': 'Review adjustment and sampling premises, estimator/interval meaning and registered comparator designs.',
                                     'workflow_owner': 'Define eligible accounts, information clock, feasible offers, money horizon and cost scenarios.'},
                'revisit_trigger': 'Inspect the selected import and input-validation path, lock its full environment and license inventory, implement the declared wrapper, and execute target/column/uncertainty/failure oracles before enabling the path.',
                'bank_data_required_for_next_step': False}
    write(OUTPUT, decision)
    evidence = [ref(OUTPUT, 'Scoped reuse decision'), decision['primary_evidence'], decision['conversion_failure_contract'],
                decision['behavioral_oracle'], ref(Path(__file__), 'Exact reference and source-custody reproduction')]
    findings = ['Nine primary blobs and identity receipts match a pre-cutoff commit; version, dependencies, license declaration and maintenance limits are explicit.',
                'CATE/ATE/ATT and uplift meanings, source-level pitfalls, alternatives, owners, costs and concrete revisit steps are documented.',
                'A bounded proposed route, conversion/failure contract and independently computed references exist; executable admission remains withheld.']
    write(BASE/'author-review.json', {'outcome': 'pass', 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
                                     'findings': findings, 'evidence': evidence,
                                     'limitations': ['Static review and exact project algebra only; no executed upstream package or interval qualification.']})
    graph, _, _ = control.combined(ROOT, control.core.read(ROOT, control.core.STATE))
    node = control.ledger.operation(graph, decision['operation_id'])
    receipt = control.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'],
                   reviewer={'name': 'Codex author/coordinator', 'kind': 'author'}, capabilities=[],
                   limitations=['No executed CausalML adapter, locked dependency/rights closure or finite-sample coverage claim.'],
                   outputs=[evidence[0]])
    for criterion, finding in zip(receipt['criteria'], findings):
        criterion.update(verdict='pass', finding=finding, evidence=evidence[:4])
    write(BASE/'operation-receipt.json', receipt)
    print(json.dumps({'outcome': 'pass', 'source_blobs': len(sources), 'dependencies': len(project['project']['dependencies']),
                      'decision': 'defer_executable_admission', 'package_execution': False, 'integration_allowed': False}))


if __name__ == '__main__':
    main()
