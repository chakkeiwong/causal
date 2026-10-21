#!/usr/bin/env python3
"""Exact authored missingness/transport counterexamples; no vendor execution."""
from fractions import Fraction as F
import json


def calculate():
    source = [F(4,5), F(1,5)]
    target = [F(1,5), F(4,5)]
    effects = [F(10), F(-10)]
    weights = [t/s for t,s in zip(target,source)]
    pilot = sum(p*t for p,t in zip(source,effects))
    transfer = sum(p*t for p,t in zip(target,effects))
    weighted = sum(p*w*t for p,w,t in zip(source,weights,effects))
    assert pilot == 6 and transfer == weighted == -6
    assert sum(p*w for p,w in zip(source,weights)) == 1
    # Source exchangeability, response MAR and positivity: enumerate X,A,R.
    response = {(0,0):F(1,2),(0,1):F(3,4),(1,0):F(2,3),(1,1):F(1,4)}
    means = {(0,0):F(0),(0,1):F(10),(1,0):F(0),(1,1):F(-10)}
    ipw = []
    for arm in [0,1]:
        value = F(0)
        for x in [0,1]:
            for a in [0,1]:
                for r in [0,1]:
                    rho = response[x,a]
                    mass = source[x]*F(1,2)*(rho if r else 1-rho)
                    value += mass*weights[x]*(a==arm)*r*means[x,a]/(F(1,2)*rho)
        ipw.append(value)
    assert ipw == [0,-6]
    # Identical observed law: randomized A; latent response type H is fair.
    observed, complete = [], []
    for missing_effect in [-10,10]:
        law = {}
        average = F(0)
        for h in [0,1]:
            y1 = F(10 if h else missing_effect)
            average += F(1,2)*y1
            for a in [0,1]:
                key = f'A={a},R={h},Y={a*y1 if h else "missing"}'
                law[key] = law.get(key,F(0))+F(1,4)
        observed.append(law); complete.append(average)
    assert observed[0] == observed[1] and complete == [0,10]
    q = [F(0),F(2),F(4)]; m = len(q)
    qbar = sum(q)/m; within = F(1)
    between = sum((v-qbar)**2 for v in q)/(m-1)
    total = within+(1+F(1,m))*between
    rvi = (1+F(1,m))*between/within
    df = (m-1)*(1+1/rvi)**2
    assert (qbar,between,total,df)==(2,4,F(19,3),F(361,128))
    # Two positive binary full conditionals imply incompatible odds ratios.
    states=[(u,v) for u in [0,1] for v in [0,1]]
    def pv(v,u):
        p=F(1,4) if u==0 else F(3,4)
        return p if v else 1-p
    matrices={
        'U_then_V': [[F(1,2)*pv(v,u) for u,v in states] for old in states],
        'V_then_U': [[pv(v,old[0])*F(1,2) for u,v in states] for old in states]}
    stationary={'U_then_V':[F(3,8),F(1,8),F(1,8),F(3,8)],'V_then_U':[F(1,4)]*4}
    for order,matrix in matrices.items():
        assert all(sum(row)==1 for row in matrix)
        pi=stationary[order]
        assert [sum(pi[i]*matrix[i][j] for i in range(4)) for j in range(4)]==pi
    assert stationary['U_then_V']!=stationary['V_then_U']
    def encode(x):
        if isinstance(x,F):return str(x)
        if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [encode(v) for v in x]
        return x
    return encode(dict(kind='project_authored_exact_examples',vendor_execution=False,empirical_coverage=False,
        transfer=dict(source=source,target=target,effects=effects,weights=weights,pilot=pilot,target_effect=transfer,
            response_adjusted_arm_means=ipw,assumed_cost=2,pilot_margin=pilot-2,target_margin=transfer-2,
            unsupported_stratum_effect_bounds=[-10,10],target_bounds=[-6,10],margin_bounds=[-8,8]),
        missingness=dict(observed_law=observed[0],complete_effects=complete,assumed_cost=4,
            margins=[x-4 for x in complete],sensitivity='tau(delta)=10+delta/2; delta in [-20,0]; margin zero at delta=-12'),
        pooling=dict(estimates=q,mean=qbar,within=within,between=between,total=total,
            old_large_complete_sample_df=df,incorrect_independent_average_variance=within/m,
            odds_ratios=[1,9],exponentiated_mean_log_odds=3,mean_odds_ratio=5),
        fcs=dict(states=states,conditional_odds_ratios=[1,9],transition_matrices=matrices,
            stationary_distributions=stationary,conclusion='Stationarity of a scan does not establish compatible full conditionals.')))


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
