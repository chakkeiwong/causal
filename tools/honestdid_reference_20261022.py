#!/usr/bin/env python3
"""Authored three-period identification and Gaussian projection oracle.

This executes no upstream software and is not an implementation of HonestDiD.
"""
from fractions import Fraction as F
import json
from math import isclose, log, sqrt
from statistics import NormalDist


def population(x, y, magnitude, smoothness):
    assert magnitude >= 0 and smoothness >= 0
    return dict(relative_magnitude=[y-magnitude*abs(x), y+magnitude*abs(x)],
                smoothness=[y+x-smoothness, y+x+smoothness])


def project(xhat, yhat, magnitude, sxx, sxy, syy, alpha):
    assert magnitude >= 0 and sxx > 0 and sxx*syy-sxy*sxy > 0
    assert 0 < alpha < 1
    r2 = -2*log(alpha)  # Exact chi-square_2 quantile.
    records = []
    det = sxx*syy-sxy*sxy
    for sign in [-1, 1]:
        ax = sign*magnitude
        variance = syy+magnitude*magnitude*sxx+2*sign*magnitude*sxy
        center = yhat+ax*xhat
        radius = sqrt(r2*variance)
        witnesses = []
        for direction in [-1, 1]:
            dx = direction*sqrt(r2/variance)*(sxx*ax+sxy)
            dy = direction*sqrt(r2/variance)*(sxy*ax+syy)
            ellipse = (syy*dx*dx-2*sxy*dx*dy+sxx*dy*dy)/det
            objective = yhat+dy+ax*(xhat+dx)
            assert isclose(ellipse, r2, rel_tol=1e-12)
            assert isclose(objective, center+direction*radius, rel_tol=1e-12, abs_tol=1e-12)
            witnesses.append(dict(x=xhat+dx,y=yhat+dy,ellipse_quadratic=ellipse,objective=objective))
        records.append(dict(sign=sign,center=center,variance=variance,
                            lower=center-radius,upper=center+radius,witnesses=witnesses))
    return dict(alpha=alpha,r_squared=r2,components=records,
                interval=[min(a['lower'] for a in records),max(a['upper'] for a in records)])


def calculate():
    p0 = population(F(-2),F(4),F(0),F(0))
    p1 = population(F(-2),F(4),F(1),F(1))
    assert p0 == dict(relative_magnitude=[F(4),F(4)],smoothness=[F(2),F(2)])
    assert p1 == dict(relative_magnitude=[F(2),F(6)],smoothness=[F(1),F(3)])
    # The two-period covariance is stipulated known, not estimated from a bank.
    known = project(0,4,1,1,1.5,4,.05)
    diagonal = project(0,4,1,1,0,4,.05)
    assert [a['variance'] for a in known['components']] == [2,8]
    assert F(1)*F(4)-F(3,2)**2 == F(7,4)
    z = NormalDist().inv_cdf(.975)
    plugin = [4-2*z,4+2*z]
    assert plugin[0] > 0 > known['interval'][0]
    assert diagonal['interval'][0] > known['interval'][0]
    # Exact grid witnesses: no upstream test or package behavior is simulated.
    coarse = [F(-1),F(1)]
    accepted = [v for v in coarse if F(-1,5) <= v <= F(1,5)]
    assert accepted == []
    nodes = [F(-2),F(-1),F(0),F(1),F(2)]
    membership = [abs(v) >= 1 for v in nodes]
    assert membership == [True,True,False,True,True]
    # Linear outcome-unit change rescales both target and an absolute SD bound.
    scaled = population(F(-200),F(400),F(1),F(100))
    assert scaled == {k:[100*v for v in a] for k,a in p1.items()}
    return dict(status='pass_for_authored_known_law_reference',native_execution=False,
        population=dict(x='-2',y='4',zero_tuning={k:list(map(str,v)) for k,v in p0.items()},
                        unit_tuning={k:list(map(str,v)) for k,v in p1.items()}),
        covariance=dict(matrix=[[1,1.5],[1.5,4]],determinant='7/4',known=True),
        gaussian_projection=known,diagonal_counterfactual=diagonal,
        plugin_pretrend_zero_ordinary_post_interval=plugin,
        net_value=dict(cost_per_exposure=1,population_example_x0_y4=3,
                       projection_interval=[v-1 for v in known['interval']]),
        grid_witnesses=dict(coarse_grid=list(map(str,coarse)),true_set=['-1/5','1/5'],
            accepted_nodes=[],disconnected_nodes=list(map(str,nodes)),membership=membership,
            hull=['-2','2'],hull_contains_rejected_zero=True,edge_acceptance=True),
        limits=['Known bivariate Gaussian law and positive-definite covariance are stipulated.',
            'Projection is conservative for every allowed target on the joint ellipse event.',
            'No optimized HonestDiD inference, package trial, empirical coverage or bank return is claimed.'])


if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))
