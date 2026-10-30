"""Selected growing-independent-pilot funding route; no oracle nuisance input."""
import numpy as np
from scipy.stats import norm
from .dynamic_funding import train_pilot
from .funding_calibration import pilot_data, DECLARATIONS, LagAccumulator, _prepare


def fit_growing_pilot(pilot_rows, rows, target, successes, sizes, penalties,
                      *, covariance='innovation_horizon', declarations=None):
    if len(pilot_rows) < 4*len(rows):
        raise ValueError('Selected growing-pilot route requires at least four pilot dates per evaluation date')
    if declarations != DECLARATIONS:
        raise ValueError('Explicit compatible scientific declarations are required')
    result, audit = _prepare(rows, target, successes, sizes, (0, 1, 2), covariance, declarations)
    if audit is None:
        return result
    if not np.isfinite(pilot_rows).all() or not np.isfinite(rows).all():
        raise ValueError('Nonfinite histories')
    for data in (pilot_rows, rows):
        if not np.isin(data[:, 0], [0, 1]).all() or not np.all(data[:, 2] == 1):
            raise ValueError('Invalid stratum or intercept')
    if any(not np.isfinite(p) or p < 0 for p in penalties) or not penalties:
        raise ValueError('Nonnegative fixed pilot penalties required')
    pilot = pilot_data(pilot_rows)
    fit = train_pilot(pilot, penalties)
    data = pilot_data(rows)
    prediction = data['x']@fit['coefficient']
    action = data['action']-prediction[:, 0]
    outcomes = data['outcomes']-prediction[:, 1:]
    n = len(rows)
    slopes, scores = [], np.empty(n)
    for group in (0, 1):
        keep = data['stratum'] == group
        qsum = action[keep]@action[keep]
        if qsum <= 0:
            raise ValueError('Missing stratum/action variation')
        slope = action[keep]@outcomes[keep]/qsum
        slopes.append(slope)
        residual = (outcomes[keep]-action[keep, None]*slope)@audit[2][group]
        scores[keep] = n*action[keep]*residual/qsum
    lag = target.horizon if covariance == 'innovation_horizon' else int(2*n**.2)
    accumulator = LagAccumulator(lag)
    accumulator.add(scores)
    calendar = accumulator.variance_of_mean(covariance == 'bartlett')
    from .funding_calibration import _finish
    result = _finish(result, np.array(slopes), calendar, target, audit, n, 'fourfold_independent_pilot')
    result.update(pilot_dates=len(pilot_rows), pilot_penalty=fit['penalty'],
                  pilot_rate='M >= 4 T; fixed dictionary and stable-law coefficient rates required',
                  coefficient=fit['coefficient'].tolist())
    result['qualifications'].append('Requires an independent invariant pilot with the stated growing information; its acquisition and fitting are additional costs.')
    return result
