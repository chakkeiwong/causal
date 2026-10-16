#!/usr/bin/env python3
"""Exact authored longitudinal error references and separate author checks."""
from fractions import Fraction as F
import json
import math
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-17/s5/depth-extension'
STATES = ('A', 'D', 'P')


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k,v in value.items()}
    if isinstance(value, (tuple,list)):
        return [encode(v) for v in value]
    return value


def histories(d, p, K=3):
    s = 1-d-p
    rows = []
    for t in range(K):
        for event, probability, loss in [('D',d,1000),('P',p,50)]:
            rows.append(dict(history='N'*t+event, probability=s**t*probability,
                             reward=F(20*(t+1)-loss)))
    rows.append(dict(history='N'*K, probability=s**K, reward=F(20*K)))
    assert sum(x['probability'] for x in rows) == 1
    return rows


def backward(d,p,K=3):
    values = [None]*(K+1)
    values[K] = dict(A=F(0),D=F(-1000),P=F(-50))
    for t in reversed(range(K)):
        after = values[t+1]
        values[t] = dict(A=20+(1-d-p)*after['A']+d*after['D']+p*after['P'],
                         D=after['D'],P=after['P'])
    return values


def allocate(weights, ranges, costs, budget, alpha=.05):
    a = [float(w*r) for w,r in zip(weights,ranges)]
    S = sum(x**(2/3)*c**(1/3) for x,c in zip(a,costs))
    continuous = [budget*(x/c)**(2/3)/S for x,c in zip(a,costs)]
    rounded = [math.floor(n) for n in continuous]
    left = budget-sum(c*n for c,n in zip(costs,rounded))
    # A feasible local rounding rule, not a claim of global integer optimality.
    while any(c <= left for c in costs):
        candidates = [(a[j]*(1/math.sqrt(rounded[j])-1/math.sqrt(rounded[j]+1))/c,j)
                      for j,c in enumerate(costs) if c <= left]
        _,j = max(candidates)
        rounded[j] += 1
        left -= costs[j]
    common = math.sqrt(math.log(2*len(a)/alpha)/2)
    radius = lambda ns: common*sum(x/math.sqrt(n) for x,n in zip(a,ns))
    equal = [budget//sum(costs)]*len(a)
    return dict(budget=budget,alpha=alpha,costs=costs,weights=encode(weights),
                ranges=encode(ranges),continuous_counts=continuous,
                rounded_counts=rounded,rounded_cost=budget-left,
                equal_counts=equal,equal_cost=sum(c*n for c,n in zip(costs,equal)),
                continuous_radius=radius(continuous),rounded_radius=radius(rounded),
                equal_radius=radius(equal),
                interpretation='Prospective simultaneous halfwidth, not observed intervals or measured coverage')


def calculate():
    pd,pp,qd,qp = F(1,10),F(1,5),F(11,100),F(19,100)
    pv,qv = backward(pd,pp),backward(qd,qp)
    ph,qh = histories(pd,pp),histories(qd,qp)
    pmean = sum(x['probability']*x['reward'] for x in ph)
    qmean = sum(x['probability']*x['reward'] for x in qh)
    weights = [F(7,10)**t for t in range(3)]
    residuals = [(pd-qd)*qv[t+1]['D']+(pp-qp)*qv[t+1]['P'] for t in range(3)]
    ranges = [max(qv[t+1].values())-min(qv[t+1].values()) for t in range(3)]
    tv = F(1,100)
    occupied = sum(w*tv*r for w,r in zip(weights,ranges))
    restricted = sum(w*tv*950 for w in weights)
    split = [1-(1-tv)**t for t in range(4)]
    uniform = 20*sum(split[:3])+1000*split[3]
    rho, occupancy, residual = [F(99,100),F(1,100)],[F(1,10),F(9,10)],[F(0),F(100)]
    c2 = sum(w*w/r for w,r in zip(occupancy,rho))
    l2 = sum(r*b*b for r,b in zip(rho,residual))
    result = dict(reference_histories=ph,approximate_histories=qh,
                  reference_backward=pv,approximate_backward=qv,
                  reference_value=pmean,approximate_value=qmean,
                  exact_error=pmean-qmean,active_occupancies=weights,
                  continuation_residuals=residuals,continuation_ranges=ranges,
                  telescoped_error=sum(w*b for w,b in zip(weights,residuals)),
                  occupied_span_envelope=occupied,event_support_envelope=restricted,
                  uniform_coupling_envelope=uniform,split_probabilities=split,
                  transport=dict(validation_law=rho,target_occupancy=occupancy,
                      residual=residual,validation_absolute_mean=sum(r*abs(b) for r,b in zip(rho,residual)),
                      target_signed_mean=sum(w*b for w,b in zip(occupancy,residual)),
                      residual_L2_squared=l2,concentrability_squared=c2,
                      bound_squared=c2*l2,zero_support_unseen_envelope=F(900)),
                  equal_cost_allocation=allocate(weights,ranges,[1,1,1],30000),
                  unequal_cost_allocation=allocate(weights,ranges,[1,2,4],60000))
    return encode(result)


def separate(saved):
    # Separate closed-form geometric means and mass-shift identities.
    s=F(7,10); duration=1+s+s*s
    reference=20*duration-1000*F(1,10)*duration-50*F(1,5)*duration
    approximate=20*duration-1000*F(11,100)*duration-50*F(19,100)*duration
    assert F(saved['reference_value']) == reference == F(-1971,10)
    assert F(saved['approximate_value']) == approximate == F(-43581,200)
    assert F(saved['exact_error']) == F(19,2)*duration == F(4161,200)
    assert F(saved['telescoped_error']) == F(saved['exact_error'])
    assert F(saved['occupied_span_envelope']) == F(421,20)
    assert F(saved['event_support_envelope']) == F(saved['exact_error'])
    assert F(saved['uniform_coupling_envelope']) == F(30299,1000)
    # Verify every row of both backward recursions against complete history means.
    for d,p,key in [(F(1,10),F(1,5),'reference_backward'),
                    (F(11,100),F(19,100),'approximate_backward')]:
        for t in range(4):
            remaining=3-t
            z=sum((1-d-p)**u for u in range(remaining))
            direct=(20-1000*d-50*p)*z
            assert F(saved[key][t]['A']) == direct
    tr=saved['transport']
    assert F(tr['validation_absolute_mean']) == 1
    assert F(tr['target_signed_mean']) == 90
    assert F(tr['bound_squared']) == F(802000,99)
    for key in ['equal_cost_allocation','unequal_cost_allocation']:
        a=saved[key]; ns=a['continuous_counts']; costs=a['costs']
        assert abs(sum(c*n for c,n in zip(costs,ns))-a['budget']) < 1e-7
        assert a['rounded_cost'] <= a['budget']
        scores=[float(F(w)*F(r))/(c*n**1.5) for w,r,c,n in
                zip(a['weights'],a['ranges'],costs,ns)]
        assert max(scores)-min(scores) < 1e-10
        assert a['continuous_radius'] <= a['rounded_radius']+1e-8
        assert a['rounded_radius'] < a['equal_radius']
        # Strict convexity and equal KKT marginal costs certify the continuous minimum.
        assert all(n>0 for n in ns)
    return dict(status='pass',checks=['Geometric event means independent of path enumeration',
        'All backward continuation values match direct remaining-horizon means',
        'Signed default/prepayment mass shift and exact telescoping identity',
        'Occupied, restricted-support and uniform bounds with exact fractions',
        'Rare-history transport Cauchy bound and absent-support range',
        'Continuous allocation budget/KKT/convexity and feasible integer rounding'])


def main():
    BASE.mkdir(parents=True,exist_ok=True)
    result=calculate(); checks=separate(result)
    write(BASE/'exact-results.json',result)
    write(BASE/'mathematics-review.json',dict(status='pass',
        reviewer=dict(name='Codex author/coordinator',kind='author'),checks=checks,
        evidence=[ref(BASE/'exact-results.json','Four authored longitudinal reference families'),
                  ref(Path(__file__),'Exact paths and separate closed-form checks')],
        limitations=['Stipulated finite kernels, rewards, transition truth and known occupancies.',
                     'Prospective intervals and allocations; no validation sample was drawn.',
                     'No upstream estimator, bank, coverage or economic qualification.']))
    print(json.dumps(dict(status=checks['status'],reference=result['reference_value'],
        approximate=result['approximate_value'],error=result['exact_error'],
        occupied=result['occupied_span_envelope'],event_support=result['event_support_envelope'],
        uniform=result['uniform_coupling_envelope'],
        allocations={k:result[k] for k in ['equal_cost_allocation','unequal_cost_allocation']})))


if __name__ == '__main__':
    main()
