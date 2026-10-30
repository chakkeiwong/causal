#!/usr/bin/env python3
"""Fresh, frozen fourfold-pilot comparison after the retained OLS shortfall."""
import argparse
import json
import time
import numpy as np
from threadpoolctl import threadpool_limits
from calibration_common import ROOT, SPEC, Journal, summarize
from causalbank.dynamic_funding import FundingTarget, train_pilot
from causalbank.funding_calibration import simulate_rows, pilot_data, DECLARATIONS
from causalbank.funding_pilot_rates import fit_growing_pilot
from causalbank.linked_observation import linked_response

FOLLOWUP = 'docs/studies/calibration-followup-spec.json'


def main(pilot):
    s = json.loads((ROOT/FOLLOWUP).read_text())
    parent = json.loads((ROOT/SPEC).read_text())
    base = json.loads((ROOT/parent['base']).read_text())
    observation = json.loads((ROOT/parent['observation']).read_text())
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    truth = float(target.weights()@(base['beta']*base['rho']**np.arange(target.horizon+1))-target.direct_cost())
    seed = s['pilot_seed'] if pilot else s['seed']
    repetitions = s['pilot_repetitions'] if pilot else s['repetitions']
    inputs = [FOLLOWUP, 'tools/calibration_followup.py', 'src/causalbank/funding_pilot_rates.py',
        'src/causalbank/funding_calibration.py', 'src/causalbank/dynamic_funding.py',
        'src/causalbank/linked_observation.py', 'src/causalbank/responses.py', parent['base'], parent['observation']]
    journal = Journal('followup', inputs, pilot)
    results = []
    for ci, design in enumerate(s['designs']):
        observation['correct_pair_probability'] = design['probability']
        def one(i):
            data = simulate_rows(base, observation, design['dates'], [seed, 1, ci, i])
            prior = simulate_rows(base, observation, 4*design['dates'], [seed, 2, ci, i])
            counts = np.random.default_rng([seed, 3, ci, i]).binomial(design['audit_per_stratum'], design['probability'])
            started = time.perf_counter()
            fit = train_pilot(pilot_data(prior[:design['old_pilot_dates']]), base['penalties'])
            old = linked_response(pilot_data(data), fit, counts, [design['audit_per_stratum']]*2,
                target, int(2*design['dates']**.2))
            old_seconds = time.perf_counter()-started
            inherited = dict(status=old['status'])
            if old['status'] == 'computed':
                inherited.update(estimate=old['financial_value'], standard_error=old['financial_se'], interval=old['financial_interval'])
            methods = dict(inherited_pilot_bartlett=inherited)
            durations = dict(inherited_pilot_bartlett=old_seconds)
            for rule in ('bartlett', 'innovation_horizon'):
                started = time.perf_counter()
                result = fit_growing_pilot(prior, data, target, counts, [design['audit_per_stratum']]*2,
                    base['penalties'], covariance=rule, declarations=DECLARATIONS)
                result.pop('coefficient', None)
                methods['fourfold_pilot_'+rule] = result
                durations['fourfold_pilot_'+rule] = time.perf_counter()-started
            return dict(methods=methods, fit_inference_seconds=durations, audit_successes=counts)
        rows = [journal.run(f'{design["name"]}/{i}', lambda i=i: one(i)) for i in range(repetitions)]
        summary = summarize(rows, truth)
        results.append(dict(design=design, financial_truth=truth, summary=summary,
            mean_fit_inference_seconds={k:float(np.mean([r['fit_inference_seconds'][k] for r in rows])) for k in rows[0]['fit_inference_seconds']},
            pilot_history_multiplier=4*design['dates']/design['old_pilot_dates']))
        print(json.dumps({'case': design['name'], 'fourfold_horizon': summary['fourfold_pilot_innovation_horizon']['coverage_all']}), flush=True)
    journal.finish(dict(mode='pilot' if pilot else 'final', results=results,
        scope='Fresh selected-law fourfold-pilot comparison; prior OLS shortfall retained. Acquisition excluded from paired fit timings and reported as extra required history.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pilot', action='store_true')
    with threadpool_limits(limits=1):
        main(parser.parse_args().pilot)
