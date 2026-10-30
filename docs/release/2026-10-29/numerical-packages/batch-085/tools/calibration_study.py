#!/usr/bin/env python3
"""Registered nuisance attribution and fresh fixed-dictionary repair comparison."""
import argparse
import json
import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits
from calibration_common import ROOT, SPEC, Journal, summarize
from causalbank.dynamic_funding import FundingTarget, train_pilot
from causalbank.responses import bartlett_lrv
from causalbank.linked_observation import linked_response
from causalbank.funding_calibration import (simulate_rows, pilot_data, stationary_nuisance,
    conditional_pilot_responses, fit_funding, fit_dense, DECLARATIONS)

INPUTS = ['tools/calibration_study.py', 'src/causalbank/funding_calibration.py',
          'src/causalbank/dynamic_funding.py', 'src/causalbank/linked_observation.py',
          'src/causalbank/responses.py', 'docs/studies/dynamic-funding-spec.json',
          'docs/studies/dynamic-observation-spec.json']


def transform(eta, target):
    d, weights = target.horizon+1, target.weights()
    return np.array([z for row in eta for z in (.5*weights@(row[:d]+row[d:]), .5*weights@(row[:d]-row[d:]))])


def primitives(rows, coefficient, target):
    data = pilot_data(rows)
    prediction = data['x']@coefficient
    v, residual = data['action']-prediction[:, 0], data['outcomes']-prediction[:, 1:]
    n, d = len(rows), target.horizon+1
    eta, scores = [], np.zeros((n, 4))
    for group in (0, 1):
        keep = data['stratum'] == group
        denominator = v[keep]@v[keep]
        theta = v[keep]@residual[keep]/denominator
        eta.append(theta)
        first = (residual[keep, :d]-v[keep, None]*theta[:d])@target.weights()
        second = (residual[keep, d:]-v[keep, None]*theta[d:])@target.weights()
        scores[keep, 2*group] = n*v[keep]*(first+second)/(2*denominator)
        scores[keep, 2*group+1] = n*v[keep]*(first-second)/(2*denominator)
    return transform(eta, target), scores


def covariance(scores, rule, horizon):
    n = len(scores)
    if rule == 'bartlett':
        return bartlett_lrv(scores, int(2*n**.2))/n
    scores = scores-scores.mean(axis=0)
    value = scores.T@scores
    for lag in range(1, horizon+1):
        cross = scores[lag:].T@scores[:-lag]
        value += cross+cross.T
    return value/n**2


def regular(m, variance, probability, audits, target, known=False):
    p = np.asarray(probability)
    r = 2*p-1
    c = np.array([.5, .5/r[0], .5, .5/r[1]])
    derivative = -m[[1, 3]]/r**2
    calendar = float(c@variance@c)
    estimate = float(c@m-target.direct_cost())
    if calendar <= 0 or not np.isfinite(calendar):
        return dict(status='unavailable_calendar_variance', estimate=estimate)
    value = calendar+(0 if known else np.sum(derivative**2*p*(1-p)/audits))
    se = float(np.sqrt(value))
    return dict(status='computed', estimate=estimate, standard_error=se,
                interval=[estimate-norm.ppf(.975)*se, estimate+norm.ppf(.975)*se])


def diagnostics(spec, base, observation, pilot):
    config = spec['diagnostics']
    seed = spec['pilot_seed'] if pilot else spec['diagnostic_seed']
    reps = spec['pilot_repetitions'] if pilot else spec['diagnostic_repetitions']
    journal = Journal('diagnostics', INPUTS, pilot)
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    truth = float(target.weights()@(base['beta']*base['rho']**np.arange(target.horizon+1))-target.direct_cost())
    observation = dict(observation, correct_pair_probability=config['probability'])
    p, audits = np.array(config['probability']), config['audit_per_stratum']
    c = np.array([.5, .5/(2*p[0]-1), .5, .5/(2*p[1]-1)])
    oracle = stationary_nuisance(base, observation)
    output = []
    for n in config['dates']:
        sizes = sorted(set(config['pilot_sizes']+[4*n]))
        def one(i):
            data = simulate_rows(base, observation, n, [seed, 1, n, i])
            pilot_rows = simulate_rows(base, observation, max(sizes), [seed, 2, n, i])
            counts = np.random.default_rng([seed, 3, n, i]).binomial(audits, p)
            methods, conditional = {}, {}
            for size in sizes:
                fit = train_pilot(pilot_data(pilot_rows[:size]), base['penalties'])
                for nuisance in config['nuisances']:
                    coefficient = fit['coefficient'].copy()
                    if nuisance in ('known_action', 'known_both'):
                        coefficient[:, 0] = oracle[:, 0]
                    if nuisance in ('known_outcome', 'known_both'):
                        coefficient[:, 1:] = oracle[:, 1:]
                    m, scores = primitives(data, coefficient, target)
                    key = f'M{size}/{nuisance}'
                    population = transform(conditional_pilot_responses(base, observation, coefficient), target)
                    conditional[key] = float(c@population-target.direct_cost()-truth)
                    for rule in config['covariances']:
                        var = covariance(scores, rule, target.horizon)
                        methods[key+'/'+rule+'/estimated_audit'] = regular(m, var, counts/audits, audits, target)
                        methods[key+'/'+rule+'/known_audit'] = regular(m, var, p, audits, target, True)
            return dict(methods=methods, conditional_pilot_bias=conditional, audit_successes=counts)
        rows = [journal.run(f'T{n}/{i}', lambda i=i: one(i)) for i in range(reps)]
        output.append(dict(dates=n, pilot_sizes=sizes, summary=summarize(rows, truth),
            conditional_bias={k:dict(mean=float(np.mean([r['conditional_pilot_bias'][k] for r in rows])),
                rms=float(np.sqrt(np.mean([r['conditional_pilot_bias'][k]**2 for r in rows]))))
                for k in rows[0]['conditional_pilot_bias']}))
        print(json.dumps({'diagnostic_dates': n, 'requests': len(rows)}), flush=True)
    journal.finish(dict(mode='pilot' if pilot else 'final', financial_truth=truth, results=output,
        scope='Known-nuisance and audit arms diagnose a synthetic stationary mechanism; conditional bias is the exact stationary pilot target, not an asserted finite-ratio expectation.'))


def validation(spec, base, observation, pilot):
    seed = spec['pilot_seed'] if pilot else spec['validation_seed']
    reps = spec['pilot_repetitions'] if pilot else spec['validation_repetitions']
    journal = Journal('validation', INPUTS, pilot)
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    output = []
    for index, case in enumerate(spec['validation']):
        law = dict(base, rho=case.get('rho', base['rho']))
        obs = dict(observation, correct_pair_probability=case['probability'])
        truth = float(target.weights()@(law['beta']*law['rho']**np.arange(target.horizon+1))-target.direct_cost())
        def one(i):
            correlation = case.get('innovation_correlation', 0.)
            data = simulate_rows(law, obs, case['dates'], [seed, 4, index, i], correlation)
            prior = simulate_rows(law, obs, case['pilot_dates'], [seed, 5, index, i], correlation)
            audit = np.random.default_rng([seed, 6, index, i]).binomial(case['audit_per_stratum'], case['probability'])
            prepared, training = pilot_data(data), pilot_data(prior)
            features = tuple(case.get('features', [0, 1, 2]))
            if len(features) == 2:
                prepared['x'] = prepared['x'][:, [0, 1, 3, 4]]
                training['x'] = training['x'][:, [0, 1, 3, 4]]
            fit = train_pilot(training, base['penalties'])
            baseline = linked_response(prepared, fit, audit, [case['audit_per_stratum']]*2, target, int(2*case['dates']**.2))
            old = dict(status=baseline['status'])
            if old['status'] == 'computed':
                old.update(estimate=baseline['financial_value'], standard_error=baseline['financial_se'], interval=baseline['financial_interval'])
            kwargs = dict(features=features, declarations=DECLARATIONS)
            new = fit_funding(data, target, audit, [case['audit_per_stratum']]*2, **kwargs)
            bartlett = fit_dense(data, target, audit, [case['audit_per_stratum']]*2, covariance='bartlett', **kwargs)
            comparison = None
            if i in (0, 1, reps-1):
                dense = fit_dense(data, target, audit, [case['audit_per_stratum']]*2, **kwargs)
                assert dense['status'] == new['status']
                if new['status'] == 'computed':
                    comparison = max(abs(dense[k]-new[k]) for k in ('estimate', 'standard_error'))
                    assert comparison < 1e-6
            return dict(methods=dict(inherited_pilot_bartlett=old, joint_ols_bartlett=bartlett,
                joint_ols_innovation_horizon=new), audit_successes=audit, dense_comparison_error=comparison)
        rows = [journal.run(f'{case["name"]}/{i}', lambda i=i: one(i)) for i in range(reps)]
        summary = summarize(rows, truth)
        output.append(dict(case=case, financial_truth=truth, summary=summary))
        print(json.dumps({'case': case['name'], 'coverage': summary['joint_ols_innovation_horizon']['coverage_all']}), flush=True)
    journal.finish(dict(mode='pilot' if pilot else 'final', results=output,
        scope='Prespecified fresh fixed-dictionary and structural-innovation comparison. False declarations and unavailable outcomes retained; no uniform or bank qualification.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('study', choices=['diagnostics', 'validation'])
    parser.add_argument('--pilot', action='store_true')
    args = parser.parse_args()
    specification = json.loads((ROOT/SPEC).read_text())
    base = json.loads((ROOT/specification['base']).read_text())
    observation = json.loads((ROOT/specification['observation']).read_text())
    with threadpool_limits(limits=1):
        globals()[args.study](specification, base, observation, args.pilot)
