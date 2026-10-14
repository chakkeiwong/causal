#!/usr/bin/env python3
"""Pinned Causica source review and independent exact semantic references."""
import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import shutil
import tomllib

import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-14/causica-reuse'
RAW = ROOT / 'docs/literature/raw'
OP = 'SW.DECISION.inherited_causica'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/decision.json')
PIN = 'c3b7dd2b09fe0efb543adb05b89716d0dbdee780'
AUDIT = ROOT / 'docs/program/execution/2026-10-14/l7-benchmarking/v3/reader/source-audit.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Selected pinned source and genuine primary-paper review; no Causica import, fit, sampler or upstream test execution.',
    'Exact source-trace references establish specified semantic problems, not their frequency in trained models.',
    'No finite graph/effect coverage, identified bank model, deployment qualification or integration capability is awarded.',
    'Whole dependency rights, compatible installation, model/optimization behavior and adapters require a public/generated prototype.',
    'Broader software coverage, whole-manuscript depth and rendered visual acceptance remain open.']


def exact():
    # Gaussian conditional expectations: X and U_T independent variance 1.
    # Y = 20*T + 10*X + U_Y; U_Y independent, mean 0, variance 100.
    conditioning = F(20) + F(10, 2)
    intervention = F(20)
    ux, ut, uy = F(1), F(1), F(5)
    t, y = ux + ut, 20 * (ux + ut) + 10 * ux + uy
    assert (t, y) == (2, 55)
    cf0, cf1 = 10 * ux + uy, 20 + 10 * ux + uy
    assert (cf0, cf1, cf1 - cf0) == (15, 35, 20)
    # Two-node cycle, simultaneous update, exactly two iterations from zero.
    x = (F(0), F(0)); iterates = [x]
    for _ in range(2):
        x = (1 + x[1] / 2, x[0] / 2); iterates.append(x)
    fixed = (F(4, 3), F(2, 3))
    assert fixed == (1 + fixed[1] / 2, fixed[0] / 2)
    residual = (x[0] - x[1] / 2 - 1, x[1] - x[0] / 2)
    assert x == (1, F(1, 2)) and residual == (F(-1, 4), 0)
    # At zero ENCO logits, each directed off-diagonal Bernoulli has p=1/4.
    p = F(1, 4); cycle_probability = p * p
    assert cycle_probability == F(1, 16)
    # Independent vector target reference, versus the inspected all-axis reduction.
    treated = [(F(2), F(8)), (F(2), F(8))]
    control = [(F(0), F(0)), (F(0), F(0))]
    target = tuple(sum(row[j] for row in treated) / 2 - sum(row[j] for row in control) / 2 for j in range(2))
    scalar = sum(sum(row) for row in treated) / 4 - sum(sum(row) for row in control) / 4
    squared_error = sum((v - scalar) ** 2 for v in target)
    assert target == (2, 8) and scalar == 5 and squared_error == 18
    graph_mean = F(3, 4) * 20 + F(1, 4) * -20
    graph_variance = F(3, 4) * (20 - graph_mean) ** 2 + F(1, 4) * (-20 - graph_mean) ** 2
    assert (graph_mean, graph_variance) == (10, 300)
    return {
        'scope': 'Exact project algebra and finite source-trace counterexamples; no upstream execution.',
        'conditioning': {'model': 'X=U_X; T=X+U_T; Y=20T+10X+U_Y; independent centered Gaussian noises with variances 1,1,100',
            'conditional_mean_slope': str(conditioning), 'interventional_mean_slope': str(intervention),
            'factual_X_T_Y': ['1', str(t), str(y)], 'abducted_noise': [str(v) for v in (ux, ut, uy)],
            'same_unit_cf_T0_T1': [str(cf0), str(cf1)], 'ITE_USD': '20', 'marginal_do_means_T0_T1': ['0', '20'],
            'independent_arm_MC_variance_at_N100': '4', 'common_noise_contrast_variance': '0',
            'variance_scope': 'Exact fixed additive model and ideal independent RNG draws; not measured runtime variance.'},
        'cycle': {'zero_logit_directed_edge_probability': str(p), 'two_cycle_probability': str(cycle_probability),
            'iterations': [[str(v) for v in row] for row in iterates], 'two_pass_output': [str(v) for v in x],
            'equation_residual': [str(v) for v in residual], 'algebraic_fixed_point': [str(v) for v in fixed],
            'scope': 'Initialized independent-Bernoulli law and authored cyclic equations; not a trained failure rate or validated equilibrium causal model.'},
        'vector_ATE_score': {'reference_means': [str(v) for v in target], 'all_axis_reference': str(scalar),
            'exact_prediction_correct_squared_error': '0', 'literal_reduction_squared_error': str(squared_error),
            'literal_reduction_RMSE': 'sqrt(18)', 'source_scope': 'eval_ate_rmse selected reduction; no imported upstream function.'},
        'graph_mixture': {'effects_USD': ['20', '-20'], 'weights': ['3/4', '1/4'], 'mean_USD': str(graph_mean),
            'between_graph_variance_USD2': str(graph_variance), 'MC_mean_variance_for_R_graphs': '300/R',
            'assumed_cost_USD': '8', 'component_net_values_USD': ['12', '-28'], 'weighted_net_USD': '2',
            'scope': 'Stipulated models, weights and cost; more simulation does not validate the chosen graph weights.'}}


def main():
    assert not OUTPUT.exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    plan = json.loads((BASE / 'acquisition-plan.json').read_text())
    tree_path = RAW / 'v12_exec13_pydisc_causica_canonical_tree.json'
    tree = json.loads(tree_path.read_text()); assert tree['sha'] == PIN and not tree['truncated']
    index = {r['path']: r for r in tree['tree']}
    commit_path = RAW / 'v12_exec13_pydisc_causica_cutoff_cn.json'
    commit = json.loads(commit_path.read_text())[0]
    date = commit['commit']['committer']['date']
    assert commit['sha'] == PIN and date <= '2026-10-07T15:59:59Z'
    paths = plan['source_paths']
    comments = [
        ('Package declaration and pytest configuration', ['Version 0.4.5, Python ~3.10, torch 2.0.0, MIT declaration; integration directory excluded from default recursive pytest collection.']),
        ('Locked package versions and metadata', ['277 locked packages; selected versions are recorded declarations, not a working installed environment.']),
        ('SEM.condition, ite, counterfactual and ate', ['Adjacency [parent,child]; conditioning refuses sets with outside parents; ITE reuses factual noise; ATE draws each arm separately and preserves feature axis.']),
        ('DistributionParametersSEM constructor, noise_to_sample and do', ['One update per node, without a convergence check; selected constructor checks shapes, not DAG validity.', 'Repeated interventions and incompatible batch shapes are rejected.']),
        ('SEMDistribution._create_sems and sample', ['Selected path wraps sampled graphs without a DAG filter; functional and noise modules are shared across graph draws.']),
        ('DoFunctionalRelationships and create_do_functional_relationship', ['Intervened nodes are removed from internal graph and supplied values restored; temporal functions explicitly refuse this intervention path.']),
        ('eval_ate_rmse and eval_ite_rmse', ['ATE reference .mean() has no axis, while predictions preserve node_dim; exact vector counterexample is separately derived.', 'ITE evaluation requires matching factual rows and reference counterfactuals.']),
        ('ENCOAdjacencyDistribution and initialization', ['Independent Bernoulli directed entries; diagonal zeroed but cycles not filtered; zero logits imply probability 1/4 per edge.']),
        ('ConstrainedAdjacencyDistribution, get_graph_constraint', ['0/1/NaN masks encode prohibited/required/free edges; shape checks do not ensure a DAG.']),
        ('calculate_dagness', ['Matrix-exponential DAG penalty is used as a training constraint; it is not an output acceptance check.']),
        ('Selected intervention, batch and conditioning tests', ['Tests specify node grouping, conditioning rejection and batch/abduction identities; not run in this review.']),
        ('test_evaluation_ate and related tests', ['Selected integration tests assert result shape; no multicomponent target-recovery oracle is established by this file.']),
        ('Python environment and pytest CI command', ['Workflow specifies Python 3.10 and runs pytest ./test; configuration still excludes recursive integration collection. No observed CI outcome inferred.'])]
    records = []
    entries = [(p, RAW / f'exec14_causica_source_{i}.txt', RAW / f'exec14_causica_source_{i}.receipt.json', a, c)
               for i, (p, (a, c)) in enumerate(zip(paths, comments), 1)]
    inherited = json.loads((ROOT / 'docs/program/execution/2026-10-13/python-discovery/source-selection-05.json').read_text())
    for r in inherited:
        if r['candidate'] == 'causica':
            entries.append((r['path'], RAW / (r['artifact'] + '.txt'), RAW / (r['artifact'] + '.receipt.json'),
                            'Previously inspected README/license/DECI model/prior path; reread for this decision',
                            ['Pinned alias, rights and selected model context; historical extensions are not enabled capabilities.']))
    for path, local, receipt, anchor, claims in entries:
        data = local.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert index[path]['sha'] == blob, path
        original = json.loads(receipt.read_text()); assert original['sha256'] == core.sha(local)
        ast_anchors = []
        if path.endswith('.py'):
            for node in ast.walk(ast.parse(data)):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    ast_anchors.append({'symbol': node.name, 'first_line': node.lineno, 'last_line': node.end_lineno})
        records.append({'source_identity': 'https://raw.githubusercontent.com/microsoft/causica/' + PIN + '/' + path,
            'revision': PIN, 'version_date': date, 'git_blob_sha1': blob,
            'local_copy': ref(local, anchor), 'acquisition': ref(receipt, 'Actual bounded public-source receipt'),
            'inspected_anchors': [anchor], 'symbol_locations': ast_anchors, 'supported_claims': claims})
    assert len(records) == 18
    package = tomllib.loads((RAW / 'exec14_causica_source_1.txt').read_text())['tool']['poetry']
    lock = tomllib.loads((RAW / 'exec14_causica_source_2.txt').read_text())
    assert package['version'] == '0.4.5' and len(lock['package']) == 277
    paper = ROOT / 'docs/papers/Deep End-to-end Causal Inference Geffner(2022).pdf'
    assert not paper.exists()
    shutil.copyfile(RAW / 'exec14_causica_deci_original.pdf', paper)
    pages = (BASE / 'deci.txt').read_text().split(chr(12))
    assert '20 Jun 2022' in pages[0] and 'Geffner' in pages[0]
    paper_anchors = []
    folder = BASE / 'inspected'; folder.mkdir(exist_ok=False)
    for n, finding in [(1, 'Identity, arXiv v2 and no-latent-confounder model scope'),
                       (5, 'Theorem 1 assumptions and simulation-based ATE/CATE'),
                       (6, 'Conditional regression and practical extensions'),
                       (14, 'Appendix A assumptions 1-5'),
                       (16, 'Infinite-data objective and theorem proof'),
                       (17, 'Theorem excludes mixed-type and missing-value extensions; optimization details')]:
        p = folder / f'deci-page-{n}.txt'; p.write_text(pages[n - 1])
        paper_anchors.append({'pdf_page': n, 'finding': finding, 'extract': ref(p, 'Primary PDF text')})
    paper_record = {
        'integrated_citation_key': 'exec14_causica_geffner', 'id': 'arxiv:2202.02195v2', 'kind': 'paper',
        'title': 'Deep End-to-end Causal Inference', 'filename_title': 'Deep End-to-end Causal Inference',
        'authors': ['Tomas Geffner', 'Javier Antoran', 'Adam Foster', 'Wenbo Gong', 'Chao Ma', 'Emre Kiciman',
                    'Amit Sharma', 'Angus Lamb', 'Martin Kukla', 'Nick Pawlowski', 'Miltiadis Allamanis', 'Cheng Zhang'],
        'first_author': 'Geffner', 'year': 2022, 'url': 'https://arxiv.org/pdf/2202.02195v2',
        'version_date': 'arXiv v2, 20 June 2022; authentic original acquired 14 October 2026',
        'local_path': str(paper.relative_to(ROOT)), 'sha256': core.sha(paper),
        'pages': len([p for p in pages if p.strip()]), 'inspected_anchors': paper_anchors,
        'supported_claims': ['Theorem 1 is an infinite-data maximizing-solution result under minimality, structural identifiability, correct specification, causal sufficiency and integrability.',
            'Appendix A explicitly excludes the mixed-type and missing-value extensions from this theorem.',
            'Section 3.3 separates graph-averaged interventional simulation and conditional-regression CATE.'],
        'acquisition': ref(RAW / 'exec14_causica_deci_original.receipt.json', 'Authentic arXiv PDF acquisition'),
        'limits': ['No finite-sample calibration, trained-solver convergence or current implementation equivalence is inferred.']}
    primary = {'revision': PIN, 'source_date': date, 'declared_version': package['version'],
        'cutoff': '2026-10-07 Asia/Shanghai', 'sources': records,
        'identity': ref(commit_path, 'Local-cutoff commit identity'), 'tree': ref(tree_path, 'Complete pinned source tree'),
        'maintenance_metadata': ref(RAW / 'repo_causica.json', 'Saved repository metadata only; not a service commitment'),
        'direct_dependencies': package['dependencies'], 'lock_package_count': len(lock['package']),
        'selected_locked_versions': {p['name']: p['version'] for p in lock['package'] if p['name'] in
            ['torch', 'pytorch-lightning', 'tensordict', 'numpy', 'mlflow', 'fsspec']},
        'paper': paper_record, 'upstream_executed': False, 'limitations': LIMITS}
    write(BASE / 'primary-review.json', primary)
    write(BASE / 'exact-results.json', exact())
    contract = {
        'status': 'proposed_reference_contract', 'integration_allowed': False,
        'inputs': ['Typed node names, group dimensions, units, scales and parent-to-child adjacency; distinguish graph entries from structural coefficients.',
            'Observational law, causal assumptions, target, intervention values and permitted conditioning set.',
            'Separate observation, graph, function, intervention and noise axes; immutable rows and model/checkpoint identities.',
            'Typed required/prohibited/unknown edges converted explicitly to the internal 1/0/NaN convention.',
            'Resolved environment, random generators, optimization configuration and predeclared output acceptance.'],
        'outputs': ['Model-implied ATE and factual-unit counterfactuals retain separate names and units.',
            'Retain graph draws, weights, cyclic/rejected mass, Monte Carlo error, objective diagnostics and failures.',
            'Do not relabel variational graph samples as a calibrated confidence set or sampled noise as parameter uncertainty.',
            'Preserve component means and declare metric weights before reducing vector outcomes.'],
        'failures': {'cyclic_required_graph': 'invalid_model_constraints', 'cyclic_sample': 'unqualified_graph_draw; retain denominator and any declared reweighting',
            'nonroot_conditioning': 'unsupported_conditioning; do not substitute intervention',
            'temporal_function_do': 'unsupported_by_selected_path', 'repeated_intervention': 'invalid_intervention_composition',
            'shape_or_unit_mismatch': 'invalid_contract', 'nonfinite_output_or_failed_fit': 'unavailable; no zero-effect substitution',
            'unresolved_identification': 'model_conditional_only', 'graph_average_requested_as_coverage': 'unsupported_uncertainty_claim'},
        'behavioral_oracles': ref(BASE / 'exact-results.json', 'Independent algebra and static source-trace references'),
        'upstream_acceptance': 'Must execute pinned native fixtures against these independent oracles before enabling an adapter.'}
    write(BASE / 'conversion-contract.json', contract)
    decision = {
        'operation_id': OP, 'canonical_package': 'Causica', 'canonical_repository': 'microsoft/causica',
        'aliases': ['causica distribution', 'selected DECI implementation'],
        'distinct_historical_or_adjacent_paths': ['DDECI', 'Rhino', 'research_experiments subprojects', 'TemporalSEM classes'],
        'decision': 'reference', 'decision_scope': 'Use the pinned generative-model design as a proposal reference; defer enabled integration.',
        'revision': PIN, 'revision_date': date, 'declared_version': '0.4.5',
        'license': {'declared': 'MIT', 'source': ref(RAW / 'v12_exec13_pydisc_causica_source_2.txt', 'Full pinned root license')},
        'python_requires': package['dependencies']['python'], 'direct_dependencies': package['dependencies'],
        'integration_allowed': False, 'runtime_qualification': False, 'original_gap_qualification': False,
        'primary_evidence': ref(BASE / 'primary-review.json', 'Eighteen pinned original blobs, dependencies and genuine DECI paper'),
        'behavioral_oracle': ref(BASE / 'exact-results.json', 'Four exact reference families; no upstream execution'),
        'conversion_failure_contract': ref(BASE / 'conversion-contract.json', 'Proposed narrow adapter contract'),
        'rationale': ['Useful explicit structural-function, intervention and factual-noise abstractions.',
            'Selected graph sampling needs a DAG acceptance boundary; model conditionality must survive any graph averaging.',
            'Selected vector ATE scoring needs a component-preserving reference and native verification.',
            'Dependencies, test configuration and historical extensions do not establish a qualified current adapter.'],
        'alternatives': [{'route': 'direct adoption', 'decision': 'defer', 'reason': 'Unverified runtime and semantic acceptance conditions.'},
            {'route': 'narrow integration', 'decision': 'candidate after public prototype', 'reason': 'Preserve upstream model while validating explicit scientific and output boundaries.'},
            {'route': 'port', 'decision': 'not selected', 'reason': 'Neural/noise/distribution/training maintenance and numerical equivalence costs are unjustified by a measured advantage.'},
            {'route': 'reference', 'decision': 'selected', 'reason': 'Supports a concrete proposal and exact acceptance examples now.'},
            {'route': 'reject all use', 'decision': 'not justified', 'reason': 'Scoped problems have explicit test/repair routes; no general infeasibility follows.'},
            {'route': 'supplied graph or graph-class effect analysis', 'decision': 'substantive comparator', 'reason': 'Keeps structural uncertainty explicit and can avoid unsupported learned-model certainty.'}],
        'owner_obligations': {'scientific': 'Own structural identifiability, causal sufficiency, variable meaning and declared target.',
            'integration': 'Own dimensions, interventions, DAG checks, rejected draws, unit conversion and failure accounting.',
            'runtime': 'Own resolved installation, dependency notices, reproducibility and update review.',
            'evaluation': 'Own independent public/generated references, correct component scoring and declared uncertainty targets.'},
        'costs_to_measure': ['Dependency resolution and license review', 'CPU/GPU training and failed fits', 'Graph/noise simulation',
            'Conditioning/target review', 'Oracle maintenance, conversion and requalification after updates'],
        'revisit_trigger': 'Resolve an executable pinned environment, verify independent semantic fixtures, repair or constrain vector scoring, and qualify graph acceptance and conversion before enabling a narrow adapter.',
        'bank_data_required_for_next_step': False, 'limitations': LIMITS}
    write(OUTPUT, decision)
    sources = [paper_record]
    for key, title, kind, path, claims, extra in [
        ('exec14_causica_primary', 'Causica 0.4.5 pinned SEM, graph, evaluation and dependency review', 'software_primary_sources', BASE / 'primary-review.json',
         [claim for r in records for claim in r['supported_claims']], records),
        ('exec14_causica_exact', 'Exact intervention, cyclic simulation, vector score and graph-mixture references', 'project_derivation', BASE / 'exact-results.json',
         ['Conditioning25 versus intervention20; same-unit counterfactuals15/35.', 'Positive initialized cyclic mass, nonzero two-pass residual and multicomponent false error.', 'Graph-average numerical precision is separate from graph-model uncertainty.'],
         [ref(Path(__file__).resolve(), 'Independent Fraction arithmetic')]),
        ('exec14_causica_decision', 'Causica scoped reuse and proposed conversion contract', 'project_analysis', OUTPUT,
         ['Reference selected; integration deferred with explicit public/generated prototype remedies.'], [ref(BASE / 'conversion-contract.json', 'Proposed semantic and failure contract')])]:
        sources.append({'integrated_citation_key': key, 'title': title,
            'author': 'Microsoft Causica contributors' if kind == 'software_primary_sources' else 'Causal banking proposal',
            'kind': kind, 'year': 2026, 'version_date': PIN + '; ' + date if kind == 'software_primary_sources' else '2026-10-14',
            'source_identity': 'https://github.com/microsoft/causica/tree/' + PIN if kind == 'software_primary_sources' else 'Project-authored analysis',
            'local_copy': ref(path, 'Reviewed claims and original evidence'), 'inspected_anchors': ['All specifically recorded source and mathematical findings'],
            'supported_claims': claims, 'records': extra, 'limitations': LIMITS})
    write(BASE / 'source-audit.json', {'cutoff': '2026-10-07', 'sources': sources})
    evidence = [ref(p, 'Reviewed evidence') for p in [OUTPUT, BASE / 'plan-review.md', BASE / 'primary-review.json',
        BASE / 'exact-results.json', BASE / 'conversion-contract.json', BASE / 'source-audit.json', Path(__file__).resolve()]]
    verify_bindings(evidence)
    write(BASE / 'author-review.json', {'status': 'pass', 'scope': decision['decision_scope'], 'reviewer': REVIEWER,
        'findings': decision['rationale'], 'evidence': evidence, 'limitations': LIMITS,
        'integration_allowed': False, 'visual_acceptance': False})
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    facts = ['Eighteen source blobs match the local-cutoff tree; root MIT, version, dependencies, lock and saved maintenance metadata are bound.',
             'Paper assumptions, model and uncertainty semantics, alternatives, costs and owner obligations are explicit.',
             'Reference decision grants no integration capability; independent exact references and proposed conversion/failure contract specify what remains.']
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'], reviewer=REVIEWER,
        limitations=LIMITS, outputs=[ref(OUTPUT, 'Scoped reference decision')], nonexecution_reason='',
        revisit_trigger=decision['revisit_trigger'], capabilities=[],
        criteria=[{'index': i, 'verdict': 'pass', 'finding': f, 'evidence': evidence} for i, f in enumerate(facts)])
    write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'decision': 'reference', 'source_blobs': 18, 'paper_pages': paper_record['pages'],
                      'exact_references': 'pass', 'integration_allowed': False}))


if __name__ == '__main__':
    main()
