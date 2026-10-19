#!/usr/bin/env python3
"""Exact authored initial-condition and common-calendar counterexamples."""
from fractions import Fraction as F
from itertools import product
import json
import math


def calculate():
    rho = F(1, 2)
    moments = {}
    for name in ['unbalanced_initial', 'mean_stationary_initial']:
        values = []
        for nu, eta, eps2, eps3 in product([-1, 1], repeat=4):
            y1 = F(nu) if name == 'unbalanced_initial' else F(nu)/(1-rho)+eta
            y2 = rho*y1+nu+eps2
            values.append((y2-y1)*(nu+eps3))
        moments[name] = sum(values)/len(values)
    assert moments == dict(unbalanced_initial=F(1, 2), mean_stationary_initial=F(0))
    n, periods = 3, 2
    means = []
    for signs in product([-1, 1], repeat=periods+n*periods):
        common, individual = signs[:periods], signs[periods:]
        cells = [common[t]+individual[t*n+i] for t in range(periods) for i in range(n)]
        means.append(F(sum(cells), n*periods))
    mean = sum(means)/len(means)
    variance = sum((m-mean)**2 for m in means)/len(means)
    assert mean == 0 and variance == F(1, periods)+F(1,n*periods) == F(2,3)
    rows_independent = F(2,n*periods)
    assert rows_independent == F(1,3)
    N,T,scale = 100,25,10000
    correct = F(1,T)+F(1,N*T)
    naive = F(2,N*T)
    assert correct == F(101,2500) and naive == F(1,1250)
    # Number of separate lag-level instruments for one endogenous series with
    # period-specific equations at t=3,...,T and all lags2,...,t-1.
    counts = {str(t): sum(range(1,t-1)) for t in [4,10,20]}
    assert counts['20'] == 171
    return dict(kind='project_authored_exact_synthetic_reference',
        assumptions=['nu, eta, eps2 and eps3 are independent fair signs; rho=1/2.',
            'z_it=theta+u_t+epsilon_it; all common calendar shocks and idiosyncratic signs are mutually independent across their distinct indices.',
            'No causal assignment law or confidence-interval coverage is claimed. Monetary scale10000USD is stipulated.'],
        initial_condition_moment={k:str(v) for k,v in moments.items()},
        small_calendar=dict(panels=n,dates=periods,enumerated_states=len(means),mean=str(mean),
            exact_variance=str(variance),independent_row_variance=str(rows_independent)),
        illustrative_calendar=dict(panels=N,dates=T,exact_variance=str(correct),independent_row_variance=str(naive),
            variance_ratio=str(correct/naive),mean_unit_usd=scale,
            exact_sd_usd=scale*math.sqrt(float(correct)),independent_row_sd_usd=scale*math.sqrt(float(naive))),
        full_period_specific_lag_instruments=counts,
        execution='Only authored rational enumeration; no commercial engine or upstream code executed.',
        limits=['The law has independent dates and equal common-shock loadings; arbitrary persistent dependence and heterogeneous loadings need separate analysis.',
            'A covariance option cannot establish an instrument moment. A failed sufficient moment does not establish nonidentification by every alternative method.',
            'Standard deviations are not finite-sample confidence guarantees or measured bank losses.'])


if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))
