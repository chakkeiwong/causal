#!/usr/bin/env python3
"""Exact authored qualification/planning laws; no package performance data."""
from fractions import Fraction as F
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import write

BASE=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-16/s10'

def calculate():
    table=[[600,20,10],[10,5,5],[190,75,85]]
    rows=[sum(x) for x in table];cols=[sum(row[j] for row in table) for j in range(3)]
    n=sum(rows);assert n==1000 and rows==[630,20,350] and cols==[800,100,100]
    paired_better=sum(table[i][0] for i in [1,2]);paired_worse=sum(table[0][j] for j in [1,2])
    delta=F(paired_better-paired_worse,n)
    paired_variance=F(paired_better+paired_worse,n)-delta*delta
    unpaired=F(rows[0],n)*(1-F(rows[0],n))+F(cols[0],n)*(1-F(cols[0],n))
    covariance=F(table[0][0],n)-F(rows[0]*cols[0],n*n)
    assert paired_variance==F(2011,10000) and unpaired==F(3931,10000)
    assert paired_variance==unpaired-2*covariance
    loss=F(40);value=F(10);costs=[F(1),F(2)]
    totals=[rows[0]*value-rows[1]*loss-n*costs[0],cols[0]*value-cols[1]*loss-n*costs[1]]
    threshold=(F(cols[0]-rows[0])*value-n*(costs[1]-costs[0]))/(cols[1]-rows[1])
    assert totals==[4500,2000] and threshold==F(35,4)
    upper=lambda m:1-.05**(1/m)
    def zero_failure_n(k):
        target=F(1,20*k);survival=F(99,100);power=F(1);j=0
        while power>target:power*=survival;j+=1
        assert survival**j<=target<survival**(j-1)
        return j
    single,multiple=zero_failure_n(1),zero_failure_n(8)
    assert single==299 and multiple==505
    weights=[F(3,4),F(1,4)];approx=[F(24),F(-8)];errors=[F(2),F(4)];truth=[F(23),F(-10)]
    net=sum(w*t for w,t in zip(weights,approx))-15
    error=sum(abs(w)*e for w,e in zip(weights,errors))
    true_net=sum(w*t for w,t in zip(weights,truth))-15
    assert net==1 and error==F(5,2) and true_net==F(-1,4)
    fixed=[100000,300000];variable=[3,1];maintenance=[20000,80000];years=3
    naive=F(fixed[1]-fixed[0],variable[0]-variable[1])
    full=F(fixed[1]-fixed[0]+years*(maintenance[1]-maintenance[0]),variable[0]-variable[1])
    assert naive==100000 and full==190000
    return {'classification':'Exact project constructions;all case counts,losses,costs and errors stipulated;zero random draws',
      'paired_trial':{'state_order':['correct','wrong','unavailable'],'joint_count_table_A_rows_B_columns':table,
        'requested':n,'A_counts':rows,'B_counts':cols,
        'conditional_correctness':[str(F(rows[0],sum(rows[:2]))),str(F(cols[0],sum(cols[:2])))],
        'requested_correctness':[str(F(rows[0],n)),str(F(cols[0],n))],
        'B_only_correct':paired_better,'A_only_correct':paired_worse,
        'mean_indicator_difference':str(delta),'paired_indicator_variance':str(paired_variance),
        'incorrect_independent_variance':str(unpaired),'covariance':str(covariance),
        'net_value_at_loss40_USD':[str(x) for x in totals],'loss_indifference_USD':str(threshold),
        'scope':'Hypothetical joint law with probabilities counts/1000;sampling variance formula requires independent draws of paired requests.'},
      'zero_failure':{'scope':'Independent Bernoulli failures in one declared workload distribution;fixed sample size;one-sided exact inversion',
        'n100_upper95_float':upper(100),'n_for_at_most_one_percent_upper':single,
        'n_per_profile_for_eight_simultaneous_bounds':multiple,'alpha_allocation':'1/(20*8)',
        'independence_across_profiles_required_by_union_bound':False,
        'universal_graph_or_method_certificate':False},
      'numerical_acceptance':{'weights':[str(x) for x in weights],'approximate_effects':[str(x) for x in approx],
        'certified_coordinate_error_bounds':[str(x) for x in errors],'fixed_cost_USD':15,'approximate_net_USD':str(net),
        'net_error_bound_USD':str(error),'net_enclosure_USD':[str(net-error),str(net+error)],
        'independent_reference':[str(x) for x in truth],'reference_net_USD':str(true_net),
        'scope':'Deterministic numerical-error propagation only;not statistical uncertainty or causal identification.'},
      'bridge_port_planning':{'choices':['bridge','port'],'fixed_USD':fixed,'per_request_USD':variable,'annual_maintenance_USD':maintenance,
        'years':years,'nominal_no_discount':True,'break_even_requests_ignoring_maintenance':str(naive),
        'break_even_total_requests_with_maintenance':str(full),
        'costs_at_150000_requests':[fixed[i]+years*maintenance[i]+150000*variable[i] for i in range(2)],
        'scope':'Hypothetical planning arithmetic conditional on both alternatives satisfying scientific and operational requirements;no vendor quote or ROI.'}}

if __name__=='__main__':
    data=calculate();write(BASE/'exact-results.json',data)
    print(json.dumps({'saved':str(BASE/'exact-results.json'),'families':4,'single_failure_bound_n':data['zero_failure']['n_for_at_most_one_percent_upper']}))
