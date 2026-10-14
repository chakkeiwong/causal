"""Temporal graph class study with exact finite member and outer set oracle."""
import numpy as np
from causalbank.temporal_graph_v11 import simulate, infer, exact_class


def request(spec, cell, index):
    d = spec['designs'][cell]
    graph = dict(tau=d.get('tau', .8), y_lag=d.get('y_lag', .55), u_to_a=d.get('u_to_a', .55),
                 u_to_y=d.get('u_to_y', .5), z_to_y=d.get('z_to_y', .0), phi=d.get('y_lag', .55))
    data = simulate(graph, d.get('episodes', 160), spec['horizon'], [spec['seed'], cell, index],
                    selection=d.get('selection', False), weak=d.get('weak', False))
    info = d.get('information', 'observational_latent')
    primary = infer(data, info, spec['alpha'])
    low, high = primary['components'][0] if len(primary['components']) == 1 else (-np.inf, np.inf)
    primary['interval'] = [None if not np.isfinite(low) else low, None if not np.isfinite(high) else high]
    primary.pop('components', None)
    primary['estimate'] = float(np.mean(data[:, :, 2]))
    exact = exact_class(graph)
    oracle = dict(status='oracle_diagnostic', interval=[exact, exact], estimate=exact,
                  scope='Exact structural member value, not available to procedure')
    return dict(truth=exact, methods=dict(outer_temporal_set=primary, exact_member_oracle=oracle),
                history_rows=int(np.prod(data.shape)), labels=0,
                retained_graphs=primary['retained_graphs'], effect_set=primary['effect_set'])
