"""Fixed-dictionary funding regression with chunked scalar uncertainty.

Eligibility consists of scientific declarations, not facts verified by fitting.
Only the prespecified financial contrast receives the scalar variance below.
"""
import numpy as np
from scipy.signal import lfilter
from scipy.stats import norm

DECLARATIONS = {
    'correct_fixed_action_mean': True,
    'exogenous_structural_innovation': True,
    'finite_innovation_response_horizon': True,
    'independent_noninformative_origin_swaps': True,
    'independent_representative_identity_audit': True,
    'stationary_common_calendar': True,
}


def simulate_rows(base, observation, dates, seed, innovation_correlation=0.):
    """Same aggregate law as the inherited 48-branch Gaussian construction.

    Independent branch noise averages to a Gaussian with SD sigma/sqrt(B).
    Both candidate portfolios share the driver, innovation and aggregate noise.
    """
    rng = np.random.default_rng(seed)
    total = dates + base['burn'] + base['horizon'] + 1
    driver_noise = rng.normal(size=total)
    driver_noise[0] = 0.
    driver = lfilter([np.sqrt(1-base['driver_rho']**2)], [1., -base['driver_rho']], driver_noise)
    innovation = rng.normal(size=total)
    action = .5*driver + .2*(driver*driver-1) + innovation
    action[0] = 0.
    common = innovation_correlation*innovation + np.sqrt(1-innovation_correlation**2)*rng.normal(size=total)
    noise = base['common_noise_sd']*common + base['branch_noise_sd']/np.sqrt(base['branches'])*rng.normal(size=total)
    origin = np.arange(base['burn']+1, base['burn']+dates+1)
    outcomes = []
    for beta in (base['beta'], observation['decoy_beta']):
        forcing = beta*action + 1.2*driver + .4*(driver*driver-1) + noise
        forcing[0] = 0.
        balance = lfilter([1.], [1., -base['rho']], forcing)
        outcomes.append(np.column_stack([balance[origin+h] for h in range(base['horizon']+1)]))
    strata = rng.integers(0, 2, dates)
    correct = rng.random(dates) < np.asarray(observation['correct_pair_probability'])[strata]
    return np.column_stack((strata, action[origin], np.ones(dates), driver[origin], driver[origin]**2-1,
                            np.where(correct[:, None], outcomes[0], outcomes[1]),
                            np.where(correct[:, None], outcomes[1], outcomes[0])))


def pilot_data(rows):
    basic = rows[:, 2:5]
    return dict(x=np.column_stack((basic, basic*rows[:, :1])), action=rows[:, 1],
                outcomes=rows[:, 5:], stratum=rows[:, 0].astype(int))


def stationary_nuisance(base, observation):
    """Coefficients on (1,W,W^2-1), including stationary past and natural future."""
    curves = []
    for beta in (base['beta'], observation['decoy_beta']):
        linear, square = .5*beta+1.2, .2*beta+.4
        a, b = linear/(1-base['rho']*base['driver_rho']), square/(1-base['rho']*base['driver_rho']**2)
        coefficients = []
        for h in range(base['horizon']+1):
            if h:
                a = base['rho']*a + linear*base['driver_rho']**h
                b = base['rho']*b + square*base['driver_rho']**(2*h)
            coefficients.append([0., a, b])
        curves.append(np.asarray(coefficients).T)
    by_stratum = []
    for p in observation['correct_pair_probability']:
        by_stratum.append(np.column_stack(([0., .5, .2], p*curves[0]+(1-p)*curves[1],
                                          (1-p)*curves[0]+p*curves[1])))
    return np.vstack((by_stratum[0], by_stratum[1]-by_stratum[0]))


def conditional_pilot_responses(base, observation, coefficient):
    """Population response ratio conditional on the independent pilot fit."""
    oracle = stationary_nuisance(base, observation)
    metric = np.diag([1., 1., 2.])
    focal = base['beta']*base['rho']**np.arange(base['horizon']+1)
    companion = observation['decoy_beta']*base['rho']**np.arange(base['horizon']+1)
    result = []
    for group, p in enumerate(observation['correct_pair_probability']):
        difference = coefficient[:3] + group*coefficient[3:] - oracle[:3] - group*oracle[3:]
        da, dy = difference[:, 0], difference[:, 1:]
        truth = np.r_[p*focal+(1-p)*companion, (1-p)*focal+p*companion]
        result.append((truth+da@metric@dy)/(1+da@metric@da))
    return np.asarray(result)


class LagAccumulator:
    """Centered lag products using O(L) state across arbitrary chunk boundaries."""
    def __init__(self, lags):
        self.lags = int(lags)
        self.n = 0
        self.total = 0.
        self.products = np.zeros(self.lags+1)
        self.first = np.empty(0)
        self.tail = np.empty(0)

    def add(self, scores):
        scores = np.asarray(scores, dtype=float)
        if not len(scores):
            return
        joined = np.r_[self.tail, scores]
        old = len(self.tail)
        self.products[0] += scores@scores
        for lag in range(1, self.lags+1):
            start = max(old, lag)
            if start < len(joined):
                self.products[lag] += joined[start:]@joined[start-lag:len(joined)-lag]
        self.first = np.r_[self.first, scores[:max(0, self.lags-len(self.first))]]
        self.tail = joined[-self.lags:] if self.lags else np.empty(0)
        self.n += len(scores)
        self.total += float(scores.sum())

    def variance_of_mean(self, bartlett=False):
        mean = self.total/self.n
        result = self.products[0]-self.n*mean**2
        for lag in range(1, self.lags+1):
            centered = (self.products[lag]-mean*(2*self.total-self.first[:lag].sum()-self.tail[-lag:].sum())
                        +(self.n-lag)*mean**2)
            weight = 1-lag/(self.lags+1) if bartlett else 1.
            result += 2*weight*centered
        return float(result/self.n**2)


def _prepare(rows, target, successes, sizes, features, covariance, declarations):
    target.validate()
    if declarations != DECLARATIONS:
        raise ValueError('Explicit compatible scientific declarations are required')
    if covariance not in ('innovation_horizon', 'bartlett'):
        raise ValueError('Unknown covariance procedure')
    if tuple(features) not in ((0, 1, 2), (0, 1)):
        raise ValueError('Dictionary must be a supported prespecified fixed basis')
    n = len(rows)
    if np.ndim(rows) != 2 or rows.shape[1] != 5+2*(target.horizon+1) or n <= 2*(target.horizon+2):
        raise ValueError('Wrong history dimensions or insufficient origins')
    counts, sizes = np.asarray(successes, dtype=float), np.asarray(sizes, dtype=float)
    if (counts.shape != (2,) or sizes.shape != (2,) or not np.all(np.isfinite(np.r_[counts, sizes]))
            or np.any(sizes <= 0) or np.any(counts < 0) or np.any(counts > sizes)
            or np.any(counts != np.floor(counts)) or np.any(sizes != np.floor(sizes))):
        raise ValueError('Audit counts must be two independent binomial samples')
    p = counts/sizes
    z = norm.ppf(.975)
    center = (p+z*z/(2*sizes))/(1+z*z/sizes)
    half = z*np.sqrt(p*(1-p)/sizes+z*z/(4*sizes*sizes))/(1+z*z/sizes)
    result = dict(status='unavailable_mapping_rank', audit_probability=p.tolist(),
                  audit_intervals=np.column_stack((center-half, center+half)).tolist(),
                  qualifications=['Conditional on the supplied innovation, dictionary, calendar and audit laws.',
                                  'Scalar fixed financial contrast; no full response covariance qualification.',
                                  'Finite-regime evidence does not establish uniform or bank validity.'])
    if np.any((center-half <= .5) & (center+half >= .5)):
        return result, None
    if np.any((p == 0) | (p == 1)):
        result['status'] = 'unavailable_audit_boundary'
        return result, None
    multipliers = np.array([np.r_[.5*q/(2*q-1)*target.weights(), -.5*(1-q)/(2*q-1)*target.weights()] for q in p])
    return result, (p, sizes, multipliers)


def _finish(result, slopes, covariance, target, audit, origins, algorithm):
    p, sizes, multipliers = audit
    value = float(np.sum(slopes*multipliers)-target.direct_cost())
    d = target.horizon+1
    derivative = np.array([.5*target.weights()@(row[d:]-row[:d])/(2*q-1)**2 for row, q in zip(slopes, p)])
    audit_variance = float(np.sum(derivative**2*p*(1-p)/sizes))
    result.update(estimate=value, response_estimates=slopes.tolist(), calendar_variance=covariance,
                  audit_variance=audit_variance, origins=origins, algorithm=algorithm)
    if not np.isfinite(covariance) or covariance <= 0:
        result['status'] = 'unavailable_calendar_variance'
        return result
    se = float(np.sqrt(covariance+audit_variance))
    result.update(status='computed', standard_error=se, interval=[value-norm.ppf(.975)*se, value+norm.ppf(.975)*se])
    return result


def fit_funding(rows, target, successes, sizes, *, chunk_size=4096, features=(0, 1, 2),
                covariance='innovation_horizon', declarations=None):
    result, audit = _prepare(rows, target, successes, sizes, features, covariance, declarations)
    if audit is None:
        return result
    if not isinstance(chunk_size, int) or chunk_size < 1:
        raise ValueError('Positive integer chunk size required')
    n, p = len(rows), len(features)
    factors = [None, None]
    for begin in range(0, n, chunk_size):
        block = np.asarray(rows[begin:begin+chunk_size])
        if not np.isfinite(block).all() or not np.isin(block[:, 0], [0, 1]).all() or not np.all(block[:, 2] == 1):
            raise ValueError('Nonfinite history, invalid stratum or missing intercept')
        for group in (0, 1):
            selected = block[block[:, 0] == group]
            if not len(selected):
                continue
            augmented = np.column_stack((selected[:, 2:5][:, features], selected[:, 1], selected[:, 5:]))
            if factors[group] is not None:
                augmented = np.vstack((factors[group], augmented))
            factors[group] = np.linalg.qr(augmented, mode='r')
    coefficients, action_means, residual_sums = [], [], []
    for factor in factors:
        if factor is None or factor.shape[0] < p+1 or np.linalg.matrix_rank(factor[:p+1, :p+1]) < p+1:
            raise ValueError('Missing stratum or rank-deficient action/dictionary')
        coefficients.append(np.linalg.solve(factor[:p+1, :p+1], factor[:p+1, p+1:]))
        action_means.append(np.linalg.solve(factor[:p, :p], factor[:p, p]))
        residual_sums.append(factor[p, p]**2)
    lag = target.horizon if covariance == 'innovation_horizon' else int(2*n**.2)
    accumulator = LagAccumulator(lag)
    for begin in range(0, n, chunk_size):
        block = np.asarray(rows[begin:begin+chunk_size])
        score = np.empty(len(block))
        for group in (0, 1):
            keep = block[:, 0] == group
            x = block[keep, 2:5][:, features]
            action = block[keep, 1]
            residual_action = action-x@action_means[group]
            design = np.column_stack((x, action))
            monetary_residual = block[keep, 5:]@audit[2][group]-design@(coefficients[group]@audit[2][group])
            score[keep] = n*residual_action*monetary_residual/residual_sums[group]
        accumulator.add(score)
    slopes = np.array([c[-1] for c in coefficients])
    return _finish(result, slopes, accumulator.variance_of_mean(covariance == 'bartlett'),
                   target, audit, n, 'two_pass_grouped_qr')


def fit_dense(rows, target, successes, sizes, *, features=(0, 1, 2),
              covariance='innovation_horizon', declarations=None):
    """Independent dense SVD and direct centered-lag calculation for comparison."""
    result, audit = _prepare(rows, target, successes, sizes, features, covariance, declarations)
    if audit is None:
        return result
    if not np.isfinite(rows).all() or not np.isin(rows[:, 0], [0, 1]).all() or not np.all(rows[:, 2] == 1):
        raise ValueError('Invalid history')
    n = len(rows)
    score = np.empty(n)
    slopes = []
    for group in (0, 1):
        keep = rows[:, 0] == group
        x, action, outcome = rows[keep, 2:5][:, features], rows[keep, 1], rows[keep, 5:]
        design = np.column_stack((x, action))
        coefficient, _, rank, _ = np.linalg.lstsq(design, outcome, rcond=None)
        if rank != design.shape[1]:
            raise ValueError('Rank-deficient action/dictionary')
        residual_action = action-x@np.linalg.lstsq(x, action, rcond=None)[0]
        residual = outcome-design@coefficient
        score[keep] = n*residual_action*(residual@audit[2][group])/(residual_action@residual_action)
        slopes.append(coefficient[-1])
    score -= score.mean()
    lag = target.horizon if covariance == 'innovation_horizon' else int(2*n**.2)
    variance = score@score
    for k in range(1, lag+1):
        variance += 2*(1-k/(lag+1) if covariance == 'bartlett' else 1)*(score[k:]@score[:-k])
    return _finish(result, np.asarray(slopes), float(variance/n**2), target, audit, n, 'dense_svd')
