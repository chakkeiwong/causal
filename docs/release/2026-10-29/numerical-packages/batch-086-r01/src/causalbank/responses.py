"""Fixed-horizon external-IV response inference for an explicitly stationary law.

Research implementation of A-G. No automatic causal-validity or unit-root test.
Rows share a common origin window; HAC acts on scores, not response residuals.
"""
from dataclasses import dataclass

import numpy as np
from scipy.stats import norm


@dataclass
class ResponseFit:
    estimate: np.ndarray
    covariance: np.ndarray  # sampling covariance, already divided by origins
    iid_covariance: np.ndarray
    denominator: float
    origins: int
    bandwidth: int
    moment_mean: np.ndarray | None = None
    moment_lrv: np.ndarray | None = None


def bartlett_lrv(scores, bandwidth):
    """Biased lag denominator n gives a positive semidefinite Bartlett estimate."""
    a = np.asarray(scores, dtype=float)
    if a.ndim != 2 or not np.all(np.isfinite(a)):
        raise ValueError("scores must be a finite matrix")
    n = len(a)
    if not 0 <= bandwidth < n:
        raise ValueError("bandwidth must lie in [0, n)")
    a = a - a.mean(axis=0)
    out = a.T @ a / n
    for lag in range(1, bandwidth + 1):
        gamma = a[lag:].T @ a[:-lag] / n
        out += (1 - lag / (bandwidth + 1)) * (gamma + gamma.T)
    return (out + out.T) / 2


def direct_response(x, z, horizon, outcomes=(1, 2), bandwidth=None):
    x, z = np.asarray(x), np.asarray(z)
    n = len(x) - horizon
    if x.ndim != 2 or len(z) != len(x) or n < 30 or horizon < 0:
        raise ValueError("invalid series length or horizon")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(z)):
        raise ValueError("nonfinite input")
    bandwidth = int(n ** 0.25) if bandwidth is None else bandwidth
    future = np.column_stack([x[h:h+n, j] for j in outcomes
                              for h in range(horizon + 1)])
    # Last moment is the common impact-normalization denominator.
    moments = z[:n, None] * np.column_stack((future, x[:n, 0]))
    mean = moments.mean(axis=0)
    d = mean[-1]
    if d == 0:
        raise ValueError("zero sample denominator; use moment_test_sets directly")
    theta = mean[:-1] / d
    derivative = np.column_stack((np.eye(len(theta)), -theta)) / d
    lrv = bartlett_lrv(moments, bandwidth)
    iid = bartlett_lrv(moments, 0)
    return ResponseFit(theta, derivative @ lrv @ derivative.T / n,
                       derivative @ iid @ derivative.T / n, d, n, bandwidth,
                       mean, lrv)


def propagation_value_jacobian(f,kappa,horizon,outcomes=(1,2)):
    p=len(kappa); d=kappa[0]
    powers=[np.linalg.matrix_power(f,h) for h in range(horizon+1)]
    estimates, jacobian=[],[]
    for j in outcomes:
        for h in range(horizon+1):
            theta=(powers[h]@kappa)[j]/d
            df=np.zeros((p,p))
            for r in range(h):
                df+=np.outer(powers[r][j],powers[h-1-r]@kappa)/d
            dk=powers[h][j].copy()/d
            dk[0]-=theta/d
            estimates.append(theta); jacobian.append(np.r_[df.ravel(),dk])
    return np.asarray(estimates),np.asarray(jacobian)


def proxy_var_response(x, z, horizon, outcomes=(1, 2), bandwidth=None):
    """OLS VAR(1), proxy impact and analytic propagation derivative.

    Uses the same origins as direct_response except date zero (lag unavailable).
    The score for kappa uses E[Z_t X_{t-1}]=0, an A-G assumption.
    """
    x, z = np.asarray(x), np.asarray(z)
    n = len(x) - horizon - 1
    p = x.shape[1]
    lag, current, instrument = x[:n], x[1:n+1], z[1:n+1]
    q = lag.T @ lag / n
    f = np.linalg.solve(q, lag.T @ current / n).T
    u = current - lag @ f.T
    kappa = (instrument[:, None] * u).mean(axis=0)
    d = kappa[0]
    if d == 0:
        raise ValueError("zero proxy denominator")
    f_score = (u[:, :, None] * (lag @ np.linalg.inv(q))[:, None, :]).reshape(n, -1)
    k_score = instrument[:, None] * u - kappa
    scores = np.column_stack((f_score, k_score))
    estimates,derivative=propagation_value_jacobian(f,kappa,horizon,outcomes)
    bandwidth = int(n ** 0.25) if bandwidth is None else bandwidth
    return ResponseFit(np.asarray(estimates),
                       derivative @ bartlett_lrv(scores, bandwidth) @ derivative.T / n,
                       derivative @ bartlett_lrv(scores, 0) @ derivative.T / n,
                       d, n, bandwidth)


def level_response_from_changes(x, z, horizon, outcomes=(1, 2), bandwidth=None):
    """Level response to a one-time shock, identified by stationary changes.

    Drops the first instrument with the differenced first observation. Retains
    all cross-horizon covariance, including for residual-test inversion.
    """
    fit = direct_response(np.diff(x, axis=0), np.asarray(z)[1:], horizon,
                          outcomes, bandwidth)
    cumulative = np.kron(np.eye(len(outcomes)), np.tril(np.ones((horizon+1, horizon+1))))
    transform = np.zeros((len(fit.estimate)+1, len(fit.estimate)+1))
    transform[:-1, :-1] = cumulative
    transform[-1, -1] = 1
    return ResponseFit(cumulative @ fit.estimate,
                       cumulative @ fit.covariance @ cumulative.T,
                       cumulative @ fit.iid_covariance @ cumulative.T,
                       fit.denominator, fit.origins, fit.bandwidth,
                       transform @ fit.moment_mean,
                       transform @ fit.moment_lrv @ transform.T)


def quadratic_sublevel(a, b, c):
    """Closed real set solving a*x^2+b*x+c <= 0; None is an infinite endpoint."""
    if not np.all(np.isfinite([a, b, c])):
        raise ValueError("nonfinite quadratic")
    if a == 0:
        if b == 0:
            return [[None, None]] if c <= 0 else []
        return [[None, -c / b]] if b > 0 else [[-c / b, None]]
    disc = b*b - 4*a*c
    if disc < 0:
        return [[None, None]] if a < 0 else []
    if disc == 0:
        return [[None, None]] if a < 0 else [[-b/(2*a), -b/(2*a)]]
    # Stable quadratic roots; avoid subtracting two nearly equal numbers.
    q = -0.5 * (b + np.copysign(np.sqrt(disc), b))
    low, high = sorted((q/a, c/q))
    return [[low, high]] if a > 0 else [[None, low], [high, None]]


def moment_test_sets(mean, lrv, n, alpha=0.05, simultaneous=True):
    """Bonferroni residual-test inversion, without dividing by normalization.

    Asymptotic Gaussian moment inference under A-G, also along weak-IV
    sequences with a nondegenerate residual-score variance.
    """
    m = len(mean) - 1
    critical = norm.ppf(1 - alpha / (2 * (m if simultaneous else 1)))
    d = mean[-1]
    sets = []
    for j in range(m):
        a = n*d*d - critical**2 * lrv[-1, -1]
        b = -2*n*mean[j]*d + 2*critical**2 * lrv[j, -1]
        c = n*mean[j]**2 - critical**2 * lrv[j, j]
        sets.append(quadratic_sublevel(a, b, c))
    return sets


def set_contains(intervals, value):
    return any((lo is None or lo <= value) and (hi is None or value <= hi)
               for lo, hi in intervals)


def gaussian_max_critical(covariance, rng, draws=8192, alpha=0.05):
    """Numerical Gaussian maximum quantile; caller reports simulation precision."""
    scale = np.sqrt(np.maximum(np.diag(covariance), 0))
    if np.any(scale == 0):
        raise ValueError("degenerate coordinate")
    correlation = covariance / np.outer(scale, scale)
    eigen, vectors = np.linalg.eigh((correlation + correlation.T) / 2)
    if eigen.min() < -1e-8:
        raise ValueError("covariance not positive semidefinite")
    gaussian = rng.normal(size=(draws, len(scale))) @ (vectors * np.sqrt(np.maximum(eigen, 0))).T
    return float(np.quantile(np.abs(gaussian).max(axis=1), 1-alpha, method="higher"))
