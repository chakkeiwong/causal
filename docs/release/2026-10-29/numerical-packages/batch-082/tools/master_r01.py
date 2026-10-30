"""R01 frozen study adapter, with paired inherited estimator on identical rows."""
import json
from pathlib import Path
import numpy as np
from causalbank.dynamic_funding import FundingTarget
from causalbank.linked_funding import LINKED_DECLARATIONS, fit_linked_funding, simulate_linked
from causalbank.replicated_funding import fit_replicates

ROOT = Path(__file__).resolve().parents[1]


def request(spec, cell, index):
    design = spec['designs'][cell]
    base = json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text())
    observation = json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text())
    law = dict(base, rho=design.get('rho', base['rho']))
    obs = dict(observation, correct_pair_probability=design.get('probability', [.55, .515]))
    options = dict(inclusion=design.get('q', .25), actual_inclusion=design.get('actual_q'),
                   label_error=design.get('label_error', 0.), correlation=design.get('correlation', 0.))
    k, length = spec['calendars'], design.get('length', spec['length'])
    pilot, pa = simulate_linked(law, obs, 4*k*length, [spec['seed'], cell, index, 0],
                                [spec['seed'], cell, index, 1], **options)
    calendars, audits = [], []
    for j in range(k):
        rows, audit = simulate_linked(law, obs, length, [spec['seed'], cell, index, 2+j],
                                      [spec['seed'], cell, index, 2+k+j], **options)
        calendars.append(rows); audits.append(audit)
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    primary = fit_replicates(pilot, pa, calendars, audits, target, base['penalties'], spec['alpha'])
    joined, ja = np.concatenate(calendars), tuple(np.concatenate([a[j] for a in audits]) for j in range(3))
    # This challenger is explicitly the old calculation on stacked histories.
    # It does not get a new claim for the artificial calendar boundaries.
    baseline = fit_linked_funding(pilot, joined, target, pa, ja, base['penalties'],
                                  declarations=LINKED_DECLARATIONS)
    truth = float(target.weights()@(base['beta']*law['rho']**np.arange(target.horizon+1))-target.direct_cost())
    return dict(truth=truth, methods=dict(replicated_randomized=primary, inherited_stacked=baseline),
                labels=int(pa[0].sum()+ja[0].sum()), history_rows=5*k*length,
                evaluation_calendars=k, origins_per_calendar=length,
                simulated_burn_dates=(k+1)*base['burn'],
                history_horizon_values=5*k*length*2*(target.horizon+1))
