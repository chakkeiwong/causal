#!/usr/bin/env python3
"""Pinned d3rlpy proposal review; never imports or executes upstream code."""
import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-15/d3rlpy-reuse'
RAW = ROOT / 'docs/literature/raw'
PIN = '38c34b6f99fde82875e2ad81d1ba1f7a7da34137'
OP = 'SW.DECISION.inherited_d3rlpy'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/decision.json')
AUDIT = ROOT / 'docs/program/execution/2026-10-14/commercial-survival/v3/reader/source-audit.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
 'Selected pinned source inspection and exact authored algebra; no d3rlpy import, fit or upstream test run.',
 'This decision does not establish whole-package correctness, installed compatibility, full dependency rights or maintained service.',
 'Project amounts, transitions and error laws are stipulated scenarios, not empirical bank value or measured software failure rates.',
 'Cutoff is 2026-10-07 Asia/Shanghai; saved historical metadata and exact commit are distinguished from current maintenance claims.',
 'Reference use is selected; a public/generated prototype must resolve the specified semantics before enabling an adapter.',
 'Whole-manuscript depth, wider software coverage, sponsor and rendered visual acceptance remain open.']


def exact():
    # These references follow explicit mathematics and source control flow.
    lengths = [2048, 1]
    states = [[10] + [0] * 1023 + [30] + [0] * 1023, [20]]
    heads = [[i for i in range(0, n, 1024)] for n in lengths]
    intended = sum(F(s[0]) for s in states) / len(states)
    literal = sum(F(s[i]) for s, h in zip(states, heads) for i in h) / sum(map(len, heads))
    assert intended == 15 and literal == 20
    # Timeout rows need a next observation; terminal rows can use zero padding.
    rows = 3
    terminal_count, truncated_count = rows, rows - 1
    no_terminal_flags = [0] * 6
    timeout_flags = [0, 0, 1, 0, 0, 0]
    emitted = []; start = 0
    for i, (terminal, timeout) in enumerate(zip(no_terminal_flags, timeout_flags)):
        if terminal or timeout:
            emitted.append(list(range(start, i + 1))); start = i + 1
    assert emitted == [[0, 1, 2]] and start == 3
    overlap_terminals, overlap_timeouts = [0, 1], [0, 1]
    resolved = [0 if t else u for t, u in zip(overlap_terminals, overlap_timeouts)]
    assert resolved == [0, 0]
    stochastic = F(1, 4) * 2 + F(3, 4) * 10
    deterministic = F(10)
    assert stochastic == 8
    # Calendar discounting and reward shifts change the estimand.
    gamma = F(9, 10)
    row_return = F(10) + gamma * 20
    calendar_return = F(10) + gamma ** 2 * 20
    assert row_return == 28 and calendar_return == F(131, 5)
    original = F(10) + gamma * 20
    transformed = F(10 - 5, 5) + gamma * F(20 - 5, 5)
    reward_inverse_on_value = 5 * transformed + 5
    correct_inverse = 5 * transformed + 5 * (1 + gamma)
    assert transformed == F(37, 10) and reward_inverse_on_value == F(47, 2)
    assert correct_inverse == original == 28
    unsupported_values = [F(100), F(-100)]
    logged_values = [F(0), F(0)]
    assert logged_values[0] == logged_values[1]
    # Return risk is not estimation uncertainty or selection-adjusted coverage.
    returns = [F(0), F(100)]
    mean = sum(returns) / 2
    variance = sum((r - mean) ** 2 for r in returns) / 2
    variance_mean = variance / 100
    assert (mean, variance, variance_mean) == (50, 2500, 25)
    errors = [-10, 10]
    selected = [max(a, b) for a in errors for b in errors]
    selection_bias = sum(F(x) for x in selected) / len(selected)
    assert selection_bias == 5
    return {
      'scope': 'Exact project constructions and literal control-flow traces; no imported upstream execution.',
      'initial_state_weighting': {'terminated_episode_lengths': lengths, 'window_size': 1024, 'window_heads': heads,
        'stipulated_head_values_USD': [[10, 30], [20]], 'one_start_per_episode_USD': str(intended), 'window_start_average_USD': str(literal),
        'repair': 'Score exactly each declared initial state and apply the stated target-population weights.'},
      'episode_boundaries': {'three_row_terminal_transition_count': terminal_count, 'three_row_timeout_transition_count': truncated_count,
        'six_rows_timeout_flags': timeout_flags, 'emitted_row_indices': emitted, 'unclosed_tail_indices': [3, 4, 5],
        'overlap_terminal_flags': overlap_terminals, 'original_timeout_flags': overlap_timeouts, 'resolved_timeout_flags': resolved,
        'test_fixture_observation': 'The inspected overlap parameter only sets timeouts; terminals are set only by the terminal parameter.'},
      'policy_identity': {'action_rewards_USD': [2, 10], 'stochastic_action_probabilities': ['1/4', '3/4'],
        'stochastic_value_USD': str(stochastic), 'assumed_best_action': 1, 'deterministic_value_USD': str(deterministic)},
      'discount_clock': {'reward_times_in_months': [0, 2], 'rewards_USD': [10, 20], 'monthly_discount': str(gamma),
        'row_clock_value_USD': str(row_return), 'calendar_value_USD': str(calendar_return)},
      'reward_units': {'one_step_affine_map': '(r-5)/5', 'two_step_value_USD': str(original),
        'transformed_value': str(transformed), 'one_step_inverse_applied_to_value': str(reward_inverse_on_value),
        'correct_horizon_adjusted_value_USD': str(correct_inverse),
        'clipped_100_and_1000_at_1': [1, 1], 'inverse_after_clipping': 'not_identifiable_without_original_rewards'},
      'support': {'logging_action': 0, 'logged_rewards_in_two_models': list(map(str, logged_values)),
        'always_action1_values_USD': list(map(str, unsupported_values)), 'conclusion': 'Identical logged law, unidentified unsupported policy value.'},
      'uncertainty': {'return_distribution_USD': [0, 100], 'probabilities': ['1/2', '1/2'], 'mean_USD': str(mean),
        'return_variance_USD2': str(variance), 'iid_mean_variance_at_n100_USD2': str(variance_mean),
        'mean_standard_error_USD': '5', 'two_unbiased_independent_score_errors_USD': errors,
        'selected_error_outcomes_USD': selected, 'expected_selected_optimism_USD': str(selection_bias)}}


def main():
    assert not OUTPUT.exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    plan = json.loads((BASE / 'acquisition-plan.json').read_text())
    tree = json.loads((RAW / 'exec15_d3rlpy_tree.json').read_text())
    assert tree['sha'] == PIN and not tree['truncated']
    idx = {r['path']: r for r in tree['tree']}
    head = json.loads((RAW / 'head_d3rlpy.json').read_text())
    date = head['commit']['committer']['date']
    assert head['sha'] == PIN and date <= '2026-10-07T15:59:59Z'
    comments = [
      ([(1, 21)], ['Root MIT text, notice retention and warranty disclaimer; dependency rights are separate.']),
      ([(11, 67), (88, 124)], ['Package scope, v2 breaking changes and declared algorithms; marketing benchmarks are not independently reproduced.']),
      ([(9, 52)], ['Package metadata, Python >=3.9.0, eleven direct requirements and CLI entry point; no resolved environment.']),
      ([(1, 1)], ['Pinned source declares version 2.8.1; matching label does not prove PyPI artifact equivalence.']),
      ([(57, 81), (320, 386)], ['Episode distinguishes terminated from truncated transition count; compute_return sums stored rewards without discount.']),
      ([(41, 91)], ['Overlapping flags prioritize terminal by mutating timeout entries; no boundary raises; unclosed final tail is not emitted.']),
      ([(43, 72), (168, 226)], ['Basic picker sets interval one; multistep picker discounts by row offsets; terminal successor zero padding is explicit.']),
      ([(25, 112), (146, 194), (225, 275)], ['FQE configuration defaults and target-policy object are separate; ensemble count is not a confidence procedure.']),
      ([(73, 119), (127, 152)], ['FQE calls predict_best_action and uses gamma raised to batch interval; it does not integrate sampled policy actions in this update.']),
      ([(31, 68), (191, 271), (274, 327)], ['InitialStateValueEstimationEvaluator averages the first state of every batch, not just each episode; average-value and SoftOPC summaries have distinct targets.']),
      ([(245, 304)], ['Discrete CQL config declares a conservative penalty and DoubleDQN backbone; no banking value guarantee is inferred.']),
      ([(265, 293)], ['Discrete conservative loss is log-sum-exp minus logged-action value added to TD loss.']),
      ([(92, 142), (243, 332), (336, 429)], ['Clipping destroys magnitude information; affine reward inverse is one-step; return-based denominator can be zero without a guard in this path.']),
      ([(1, 82)], ['Overlap test parameter sets timeout flags but never sets terminal flags in that branch; no native test run.']),
      ([(16, 72), (149, 232)], ['Selected tests check terminal and multistep conversion examples; not a bank-data target oracle.']),
      ([(1, 90)], ['FQE tests use dummy encoders and generic tester with selected copy checks disabled; no performance or coverage finding inferred.']),
      ([(1, 54)], ['Pinned CI declares Python3.10 and Ubuntu/macOS, with Windows temporarily omitted; configuration is not evidence of a successful job.']),
      ([(256, 368)], ['Public predict and sample_action differ; predict_value applies observation/action transformations but no inverse reward transformation.'])]
    records = []
    for row, (ranges, claims) in zip(plan['sources'], comments):
        local = RAW / (row['id'] + '.txt'); receipt = RAW / (row['id'] + '.receipt.json')
        data = local.read_bytes(); lines = data.decode().splitlines()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert blob == row['blob_sha1'] == idx[row['source_path']]['sha']
        acquisition = json.loads(receipt.read_text())
        assert acquisition['status'] == 'saved' and acquisition['url'] == row['url'] and acquisition['sha256'] == core.sha(local)
        anchors = []
        for lo, hi in ranges:
            assert 1 <= lo <= hi <= len(lines), (row['source_path'], lo, hi, len(lines))
            excerpt = '\n'.join(lines[lo-1:hi])
            anchors.append({'first_line': lo, 'last_line': hi, 'excerpt_sha256': hashlib.sha256(excerpt.encode()).hexdigest()})
        records.append({'source_identity': row['url'], 'source_path': row['source_path'], 'revision': PIN, 'version_date': date,
            'git_blob_sha1': blob, 'local_copy': ref(local, row['source_path']), 'acquisition': ref(receipt, 'Bounded original source retrieval'),
            'inspected_anchors': anchors, 'supported_claims': claims})
    assert len(records) == 18
    syntax = ast.parse((RAW / 'exec15_d3rlpy_source_3.txt').read_text())
    setup = next(n for n in ast.walk(syntax) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'setup')
    kwargs = {k.arg:k.value for k in setup.keywords}
    deps = ast.literal_eval(kwargs['install_requires']); assert len(deps) == 11
    exact_results = exact(); write(BASE / 'exact-results.json', exact_results)
    primary = {'revision': PIN, 'version_date': date, 'declared_version': '2.8.1', 'cutoff': '2026-10-07 Asia/Shanghai',
      'identity': ref(RAW / 'head_d3rlpy.json', 'Saved exact commit identity'),
      'tree': ref(RAW / 'exec15_d3rlpy_tree.json', 'Complete pinned tree'),
      'maintenance_metadata': ref(RAW / 'repo_d3rlpy.json', 'Historical repository metadata; no service commitment'),
      'pypi_metadata': ref(RAW / 'pypi_d3rlpy.json', 'Separately observed distribution metadata, not artifact equivalence'),
      'sources': records, 'direct_dependencies': deps, 'python_requires': ast.literal_eval(kwargs['python_requires']),
      'upstream_executed': False, 'limitations': LIMITS}
    write(BASE / 'primary-review.json', primary)
    contract = {'status': 'proposed_reference_contract', 'integration_allowed': False,
      'inputs': ['Immutable episode identifiers, time-zero population and predecision histories; no future information in state.',
        'Terminal, administrative cutoff, missing next observation and unclosed tail remain distinct, with row reconciliation.',
        'Action vocabulary, legality, policy identity (greedy versus randomized), reward units and physical discount clock.',
        'Separate policy training, tuning and evaluation episodes by customer and relevant time/group dependence.',
        'Exact source, resolved environment, independent FQE/learner settings, seeds and target-start weights.'],
      'outputs': ['Retain original currency rewards, transformed objectives and horizon-specific value units separately.',
        'Score exactly the declared initial states; preserve excluded episodes and target weights.',
        'Report data support, Bellman residuals, failed fits and bootstrap failures without converting them into causal certification.',
        'Separate return distribution, sampling uncertainty, optimization variability and structural uncertainty.'],
      'failures': {'overlap_without_declared_resolution':'ambiguous_boundary', 'unclosed_tail':'incomplete_episode_requires_disposition',
        'zero_transition_episode':'invalid_for_selected_scorer', 'unsupported_action':'policy_value_not_identified',
        'stochastic_policy_requested_for_greedy_FQE':'policy_target_mismatch', 'physical_time_not_encoded':'discount_clock_mismatch',
        'irreversible_clipping_with_currency_output':'original_reward_required', 'zero_scale_denominator':'invalid_reward_scaling',
        'nonfinite_fit_or_score':'evaluation_unavailable', 'training_score_as_acceptance':'independent_evaluation_required'},
      'proposed_repairs': ['Make a nonmutating input copy and explicit termination policy; retain row disposition counts.',
        'Replace or wrap the initial-state evaluator with one state per target unit, and test 1023/1024/1025/2048-row boundaries.',
        'Actually exercise both terminal and timeout flags in the overlap test; retain caller-array immutability checks.',
        'Reject unsupported stochastic-policy requests or implement and verify a policy-integrated Bellman target.',
        'Provide a clock-aware transition conversion and horizon-aware affine value inverse; retain raw rewards.',
        'Run generated exact references against the pinned native package before any enabled adapter.'],
      'behavioral_oracles': ref(BASE / 'exact-results.json', 'Seven exact banking/semantic reference families'),
      'upstream_acceptance': 'Not executed; the proposed fixtures must verify both native behavior and any repaired wrapper.'}
    write(BASE / 'conversion-contract.json', contract)
    decision = {'operation_id': OP, 'canonical_package': 'd3rlpy', 'canonical_repository': 'takuseno/d3rlpy',
      'aliases': ['d3rlpy PyPI name', 'd3rlpy Python package'], 'distinct_engines': ['SCOPE-RL', 'Open Bandit Pipeline'],
      'decision': 'reference', 'decision_scope': 'Use pinned offline policy-learning and FQE interfaces as proposal challengers; defer enabled integration.',
      'revision': PIN, 'revision_date': date, 'declared_version': '2.8.1',
      'license': {'declared':'MIT', 'source':ref(RAW / 'exec15_d3rlpy_source_1.txt','Exact root license')},
      'direct_dependencies': deps, 'python_requires': primary['python_requires'], 'integration_allowed': False,
      'runtime_qualification': False, 'original_gap_qualification': False,
      'primary_evidence': ref(BASE / 'primary-review.json', 'Eighteen pinned source blobs'),
      'behavioral_oracle': ref(BASE / 'exact-results.json', 'Independent exact constructions'),
      'conversion_failure_contract': ref(BASE / 'conversion-contract.json', 'Proposed target-preserving boundary'),
      'rationale': ['Modular learners, episode objects and FQE provide a useful independently evaluated challenger.',
        'Episode boundaries, scorer population, deterministic-policy target and reward/clock semantics need explicit controls.',
        'Observed source issues have concrete proposed repairs, so rejecting all research use is not justified.',
        'No direct adoption is justified by package naming, README benchmarks or a finite loss alone.'],
      'alternatives': [{'route':'direct adoption','decision':'defer','reason':'Missing native semantic oracle, resolved environment and independent evaluation.'},
        {'route':'narrow integration','decision':'candidate after prototype','reason':'Preserves upstream maintenance while isolating data, target, scorer and failure contracts.'},
        {'route':'port','decision':'not selected','reason':'Recreating neural learners, preprocessing and checkpoint semantics adds equivalence and maintenance cost without a measured benefit.'},
        {'route':'reference','decision':'selected','reason':'Enables a concrete public/generated comparison now without product capability claims.'},
        {'route':'reject all use','decision':'not justified','reason':'Scoped semantic defects can be constrained or repaired and tested.'},
        {'route':'tabular dynamic programming and direct generated rollouts','decision':'reference comparator','reason':'Exact finite model values isolate conversion error before neural approximation.'},
        {'route':'SCOPE-RL or Open Bandit Pipeline','decision':'separate decisions required','reason':'Sequential policy evaluation and contextual-bandit targets cannot inherit this package approval.'}],
      'owner_obligations': {'scientific':'Own history sufficiency, sequential exchangeability, support, censoring and target population.',
        'integration':'Own episode/clock/reward/policy conversions, scorer fixes and no-loss row reconciliation.',
        'runtime':'Own environment locks, dependency notices, checkpoint formats and requalification after updates.',
        'evaluation':'Own independent public/generated episodes, predeclared tuning and failed-fit/uncertainty accounting.'},
      'costs_to_measure':['Environment and dependency review','Episode reconstruction and bank target review','Training plus FQE across configurations and seeds',
        'Failed runs, evaluation splits and clustered uncertainty','Scorer repair, compatibility and regression maintenance'],
      'revisit_trigger':'A pinned public/generated prototype passes the explicit native and wrapper oracles, resolves package/dependency rights and reproduces target-preserving held-out evaluation.'}
    write(OUTPUT, decision)
    def source(key,title,kind,local,claims,related):
        return {'integrated_citation_key':key,'kind':kind,'author':'d3rlpy contributors' if kind=='software' else 'Causal banking proposal',
          'title':title,'year':2025 if kind=='software' else 2026,
          'version_date':date+'; exact commit '+PIN if kind=='software' else 'Project construction, 15 October 2026; exact bytes bound by SHA-256',
          'source_identity':'https://github.com/takuseno/d3rlpy/tree/'+PIN if kind=='software' else 'Project-authored '+kind,
          'local_copy':ref(local,title),'inspected_anchors':[title],'supported_claims':claims,'records':related,'limitations':LIMITS}
    sources = [
      source('exec15_d3rlpy_episode','Pinned d3rlpy episode, transition and test semantics','software',RAW/'exec15_d3rlpy_source_6.txt',
        ['Episode boundary, retained transition and source-test observations'],[records[i-1] for i in [5,6,7,14,15]]),
      source('exec15_d3rlpy_value','Pinned d3rlpy learner, FQE, metric and reward source','software',RAW/'exec15_d3rlpy_source_10.txt',
        ['Specific policy, metric population and reward-scale semantics'],[records[i-1] for i in [8,9,10,11,12,13,16,18]]),
      source('exec15_d3rlpy_package','Pinned d3rlpy package identity, license and dependencies','software',RAW/'exec15_d3rlpy_source_3.txt',
        ['Version, declared requirements, rights and CI configuration'],[records[i-1] for i in [1,2,3,4,17]]),
      source('exec15_d3rlpy_exact','Exact banking references for offline policy evaluation','project_derivation',BASE/'exact-results.json',
        ['Exact state weighting, episode boundaries, policy identity, discount, units, support and uncertainty examples'],[{'local_copy':ref(Path(__file__).resolve(),'Reproducible exact constructions')}]),
      source('exec15_d3rlpy_contract','d3rlpy reference decision and proposed conversion contract','project_design',OUTPUT,
        ['Reuse alternatives, owner obligations, proposed repairs and explicit deferred integration'],[{'local_copy':ref(BASE/'conversion-contract.json','Proposed semantic boundary')}])]
    write(BASE/'source-audit.json',{'sources':sources})
    evidence=[ref(p,a) for p,a in [(BASE/'primary-review.json','Pinned source review'),(BASE/'exact-results.json','Seven exact reference families'),
       (BASE/'conversion-contract.json','Proposed repairs and failure contract'),(BASE/'source-audit.json','Five traceable citation records'),
       (OUTPUT,'Reference decision without integration capability'),(Path(__file__).resolve(),'Review and exact verification')]]
    for p in evidence: verify_bindings(p)
    write(BASE/'author-review.json',{'status':'pass','reviewer':REVIEWER,'scope':decision['decision_scope'],
      'findings':decision['rationale'],'evidence':evidence,'limitations':LIMITS,'integration_allowed':False,'visual_acceptance':False})
    graph,_,_=run.combined(ROOT,state)
    receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    findings=['Eighteen original files match the complete pinned tree; identity, root license, dependencies and historical maintenance are explicit.',
      'Exact banking references separate policy targets, initial populations, clocks, reward units, support and uncertainty; alternatives and ownership are specified.',
      'Reference decision grants no integration capability; proposed repairs, behavioral oracles and conversion/failure contract define the revisit condition.']
    receipt.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,limitations=LIMITS,
      outputs=[ref(OUTPUT,'Scoped reference decision')],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],capabilities=[],
      criteria=[{'index':i,'verdict':'pass','finding':f,'evidence':evidence} for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'decision':'reference','source_blobs':18,'exact_references':'pass','integration_allowed':False}))


if __name__ == '__main__':
    main()
