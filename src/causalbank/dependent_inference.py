"""Explicit dependent-score alternatives and short-panel GMM references.

These are model-conditional research operations, not automatic validation of
instruments, dynamics, initial conditions or finite-sample coverage.
"""
import numpy as np
from .responses import bartlett_lrv, moment_test_sets


def prewhitened_lrv(values, bandwidth):
    """VAR(1) prefilter, residual Bartlett covariance, exact zero-frequency map.

    The fixed-dimensional consistency argument requires a stable population
    prefilter and nonsingular I-A. Estimated instability is a reported failure.
    """
    values = np.asarray(values, float)
    centered = values - values.mean(axis=0)
    lag, current = centered[:-1], centered[1:]
    coefficient, _, rank, singular = np.linalg.lstsq(lag, current, rcond=None)
    if rank != lag.shape[1]:
        raise ValueError("rank-deficient score prefilter")
    radius = float(max(abs(np.linalg.eigvals(coefficient))))
    if radius >= 1:
        raise ValueError("unstable estimated score prefilter")
    residual = current - lag @ coefficient
    inverse = np.linalg.solve(np.eye(values.shape[1])-coefficient.T,
                              np.eye(values.shape[1]))
    covariance = inverse @ bartlett_lrv(residual, bandwidth) @ inverse.T
    return (covariance+covariance.T)/2, {
        "prefilter_radius": radius,
        "design_condition": float(singular[0]/singular[-1]),
        "recolor_condition": float(np.linalg.cond(np.eye(len(coefficient))-coefficient)),
        "bandwidth": int(bandwidth), "residual_dates": len(residual),
    }


def response_alternatives(x, z, horizon, outcomes=(1, 2), alpha=.05):
    """Same external-IV target/origins for all preregistered covariance choices."""
    n = len(x)-horizon
    future = np.column_stack([x[h:h+n, j] for j in outcomes for h in range(horizon+1)])
    moments = z[:n, None]*np.column_stack((future, x[:n, 0]))
    mean = moments.mean(axis=0)
    base = int(n**.25)
    output = {}
    for method in ("bartlett_short", "bartlett_long", "prefilter_bartlett"):
        try:
            if method == "prefilter_bartlett":
                lrv, diagnostics = prewhitened_lrv(moments, base)
            else:
                bandwidth = base if method == "bartlett_short" else 4*base
                lrv = bartlett_lrv(moments, bandwidth)
                diagnostics = {"bandwidth": bandwidth}
            output[method] = {
                "status": "computed", "sets": moment_test_sets(mean, lrv, n, alpha),
                "diagnostics": diagnostics,
            }
        except (ValueError, np.linalg.LinAlgError) as exc:
            output[method] = {"status": "failed", "error": str(exc)}
    return output


def lag_augmented_projection(series, horizons, lag_order=1):
    """Scalar innovation responses with EHW covariance, under declared AR(p).

    For p=1 regress y[t+h] on (1,y[t],y[t-1]); the extra lag isolates the
    stationary innovation in the coefficient score. This is NOT an IV route.
    """
    y = np.asarray(series, float)
    estimates, standard_errors = [], []
    for h in horizons:
        t = np.arange(lag_order, len(y)-h)
        design = np.column_stack([np.ones(len(t))]+[y[t-j] for j in range(lag_order+1)])
        coef, _, rank, _ = np.linalg.lstsq(design, y[t+h], rcond=None)
        if rank != design.shape[1]:
            raise ValueError("singular lag-augmented design")
        residual = y[t+h]-design@coef
        bread = np.linalg.inv(design.T@design)
        meat = (design*residual[:, None]).T@(design*residual[:, None])
        covariance = bread@meat@bread
        estimates.append(float(coef[1])); standard_errors.append(float(np.sqrt(max(covariance[1, 1], 0))))
    return np.array(estimates), np.array(standard_errors)


def panel_moments(y, x, system=False, max_lag=3):
    """Collapsed lag moments for y=alpha_i+rho*y[-1]+beta*x+epsilon.

    x is contemporaneously endogenous. Difference-equation instruments start
    at t-2. Optional level moments use differences at t-1 and require the
    additional initial-condition/mean-stationarity restrictions.
    """
    n, total = y.shape
    if x.shape != y.shape or total < max_lag+2:
        raise ValueError("invalid panel arrays")
    k = 2*(max_lag-1)+(2 if system else 0)
    response = np.zeros((n, k)); regressors = np.zeros((n, k, 2))
    for t in range(2, total):
        outcome = y[:, t]-y[:, t-1]
        rhs = np.column_stack((y[:, t-1]-y[:, t-2], x[:, t]-x[:, t-1]))
        for lag in range(2, max_lag+1):
            if t-lag < 0:
                continue
            for j, z in enumerate((y[:, t-lag], x[:, t-lag])):
                col = 2*(lag-2)+j
                response[:, col] += z*outcome
                regressors[:, col] += z[:, None]*rhs
        if system:
            rhs = np.column_stack((y[:, t-1], x[:, t]))
            for j, z in enumerate((y[:, t-1]-y[:, t-2], x[:, t-1]-x[:, t-2])):
                col = k-2+j
                response[:, col] += z*y[:, t]
                regressors[:, col] += z[:, None]*rhs
    # Fixed, observed instrument scaling leaves the implied moments unchanged.
    scale = np.sqrt(np.mean(response**2, axis=0))
    if np.any(scale == 0):
        raise ValueError("zero instrument moment scale")
    return response/scale, regressors/scale[None, :, None]


def linear_gmm(response, regressors, two_step=False):
    n, k = response.shape
    b, g = response.mean(axis=0), regressors.mean(axis=0)
    weight = np.eye(k)

    def solve(w):
        jac = g.T@w@g
        if np.linalg.cond(jac) > 1e12:
            raise ValueError("numerically weak or singular moment Jacobian")
        return np.linalg.solve(jac, g.T@w@b)

    theta = solve(weight)
    if two_step:
        errors = response-np.einsum('nkp,p->nk', regressors, theta)
        omega = np.cov(errors, rowvar=False, ddof=0)
        if np.linalg.cond(omega) > 1e12:
            raise ValueError("singular estimated moment covariance")
        weight = np.linalg.inv(omega)
        theta = solve(weight)
    errors = response-np.einsum('nkp,p->nk', regressors, theta)
    omega = np.cov(errors, rowvar=False, ddof=0)
    influence_map = np.linalg.solve(g.T@weight@g, g.T@weight)
    covariance = influence_map@omega@influence_map.T/n
    return {"estimate": theta, "covariance": covariance,
            "moments": k, "entities": n,
            "jacobian_condition": float(np.linalg.cond(g.T@weight@g)),
            "objective": float(n*(b-g@theta)@weight@(b-g@theta)),
            "two_step": two_step,
            "scope": "Independent-entity fixed-T asymptotic sandwich; no Windmeijer correction or weak-moment guarantee"}
