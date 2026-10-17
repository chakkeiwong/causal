#!/usr/bin/env python3
"""Exact acquisition laws and distinct finite enumerations; no empirical claims."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-17/s8'
ROUTES = ('build', 'licensed', 'hybrid')


def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serial(v) for v in x]
    return x


def costs(n):
    return dict(zip(ROUTES,[420000+F(9,5)*n,190000+F(28,5)*n,285000+F(3)*n]))


def calculate():
    crossings=dict(licensed_build=F(1150000,19),licensed_hybrid=F(475000,13),hybrid_build=F(112500))
    table={n:costs(n) for n in (10000,50000,150000)}
    regrets={r:[row[r]-min(row.values()) for row in table.values()] for r in ROUTES}
    state_costs=dict(good=dict(build=F(510000),licensed=F(470000),hybrid=F(435000)),
                     bad=dict(build=F(510000),licensed=F(720000),hybrid=F(535000)))
    prior,sensitivity,false_positive=F(3,5),F(19,20),F(1,20)
    joint={'good+':prior*sensitivity,'bad+':(1-prior)*false_positive,
           'good-':prior*(1-sensitivity),'bad-':(1-prior)*(1-false_positive)}
    prior_cost={r:prior*state_costs['good'][r]+(1-prior)*state_costs['bad'][r] for r in ROUTES}
    posterior,decisions,conditional={},{},{}
    for sig in ('+','-'):
        posterior[sig]=joint['good'+sig]/(joint['good'+sig]+joint['bad'+sig])
        conditional[sig]={r:posterior[sig]*state_costs['good'][r]+(1-posterior[sig])*state_costs['bad'][r] for r in ROUTES}
        decisions[sig]=min(conditional[sig],key=conditional[sig].get)
    with_signal=sum(joint[s+sig]*state_costs[s][decisions[sig]] for s in ('good','bad') for sig in ('+','-'))
    no_signal=min(prior_cost.values())
    perfect=prior*min(state_costs['good'].values())+(1-prior)*min(state_costs['bad'].values())
    jobs=(7,5,4);schedule={}
    for m in (1,2,3):
        assignments=list(product(range(m),repeat=3))
        score=lambda a:max(sum(d for d,j in zip(jobs,a) if j==k) for k in range(m))
        witness=min(assignments,key=score)
        schedule[m]=dict(makespan=score(witness),assignment=witness,loads=[sum(d for d,j in zip(jobs,witness) if j==k) for k in range(m)])
    utility=[[F(0),F(10)],[F(0),F(-30)]]
    policies={''.join(map(str,a)):sum(utility[h][a[h]]/2 for h in (0,1)) for a in product((0,1),repeat=2)}
    return serial(dict(costs=table,crossings=crossings,regrets=regrets,
        max_regret={r:max(v) for r,v in regrets.items()},minimax_regret='hybrid',minimax_absolute_cost='build',
        quote_ceiling_at_50000=min(costs(50000)['build'],costs(50000)['licensed'])-costs(50000)['hybrid'],maximum_quote_ceiling=F(1185000,19),
        signal=dict(state_costs=state_costs,joint=joint,prior_costs=prior_cost,posterior=posterior,
            conditional_costs=conditional,decisions=decisions,without_signal=no_signal,with_signal_before_test=with_signal,
            gross_value=no_signal-with_signal,net_at_5000=no_signal-with_signal-5000,
            net_at_15000=no_signal-with_signal-15000,perfect_information_value=no_signal-perfect),
        scheduling=dict(jobs=jobs,optimal=schedule),
        indexed_utility=dict(table=utility,policy_values=policies,full_information=max(policies.values()),
                             no_information=F(0),unconditional_contact=F(-10),invalid_flattened_max=F(10)),
        limitations=['Exact authored acquisition scenarios; no vendor run or sampled study.',
            'All costs, volumes, durations, priors and signal errors are stipulated.',
            'Failure costs fund remedy to matched scientific acceptance; wrong answers are not admitted.',
            'A shared engine compatibility state is not independent across wrappers.']))


def separate(value):
    assert F(value['crossings']['licensed_build'])*F(19,5)==230000
    assert F(value['crossings']['licensed_hybrid'])*F(13,5)==95000
    assert F(value['crossings']['hybrid_build'])*F(6,5)==135000
    assert value['max_regret']==dict(build='192000',licensed='340000',hybrid='69000')
    # Evaluate the two quote margins at the middle-volume point and at their
    # unique intersection; increasing/decreasing slopes prove the envelope peak.
    n=F(1150000,19)
    assert F(135000)-F(6,5)*n == F(-95000)+F(13,5)*n == F(1185000,19)
    assert min(135000-F(6,5)*50000,-95000+F(13,5)*50000)==35000
    assert F(value['maximum_quote_ceiling'])==F(1185000,19)
    maxima={r:max(F(row[r]) for row in value['costs'].values()) for r in ROUTES}
    assert min(maxima,key=maxima.get)=='build'
    c=[[510000,510000],[470000,720000],[435000,535000]]
    refs=[]
    for pos,neg in product(range(3),repeat=2):
        total=F(57,100)*c[pos][0]+F(2,100)*c[pos][1]+F(3,100)*c[neg][0]+F(38,100)*c[neg][1]
        refs.append((total,pos,neg))
    assert min(refs)==(F(467750),2,0)
    assert F(value['signal']['with_signal_before_test'])==min(x[0] for x in refs)
    assert F(value['signal']['gross_value'])==7250
    assert F(value['signal']['net_at_5000'])==2250
    assert F(value['signal']['net_at_15000'])==-7750
    assert F(value['signal']['perfect_information_value'])==10000
    sums={7*a+5*b+4*c for a,b,c in product((0,1),repeat=3)}
    assert min(max(s,16-s) for s in sums)==9
    assert value['scheduling']['optimal']['2']['loads']==[7,9]
    assert value['scheduling']['optimal']['3']['makespan']==7
    assert value['indexed_utility']['policy_values']=={'00':'0','01':'-15','10':'5','11':'-10'}
    assert F(value['indexed_utility']['full_information'])==5
    assert max(F(value['indexed_utility']['policy_values'][x]) for x in ('00','11'))==0
    assert 10*F(3,4)-30*F(1,4)==0
    assert 535000-100000*F(1,4)==510000
    assert min(185000,185000-150000)>0
    assert sum(F(v) for v in value['signal']['joint'].values())==1
    return dict(status='pass',scope='Same-author checks using distinct finite enumerations',
        checks=['Exact affine differences, quote-envelope peak, worst regrets and absolute-cost objective','All nine contingent choices under four signal atoms',
                'All eight subset sums and scheduling lower bounds','Four information-dependent utility policies'],
        limitations=['No independent acceptance or evidence of actual vendor or bank performance.'])


if __name__=='__main__':
    result=calculate()
    print(json.dumps(dict(checks=separate(result),signal=result['signal'],scheduling=result['scheduling']),indent=2))
