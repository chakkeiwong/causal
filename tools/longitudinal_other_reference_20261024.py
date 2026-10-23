#!/usr/bin/env python3
"""Exact authored laws and abstract traces; imports no reviewed package."""
from fractions import Fraction as F
import json

def calculate():
    def q(x): return dict(exact=str(x),decimal=float(x))
    times=[0,1,2];first_nonzero=2;start=1
    deleted=list(range(start,start+first_nonzero))
    remaining=[v for i,v in enumerate(times,1) if i not in deleted]
    assert deleted==[1,2] and remaining==[2]
    before=F(1);after=1-F(1,2)
    breslow=F(1*2,6**2);efron=F(2)/(F(6)*(F(6)-F(3,2)))
    assert breslow==F(1,18) and efron==F(2,27)
    origin_event,treatment,grace,horizon=10,2,3,5
    source_time=min(origin_event-treatment,horizon)
    source_event=1 if treatment<=grace else 0
    origin_observed=min(origin_event,horizon);origin_status=int(origin_event<=horizon)
    assert (source_time,source_event)==(5,1) and (origin_observed,origin_status)==(5,0)
    rmst1=min(4,5);rmst0=min(2,5);riskdiff=int(4<=5)-int(2<=5)
    assert rmst1-rmst0==2 and riskdiff==0
    g=[F(1,2),F(1,4)];weights=[1/x for x in g];mean=sum(weights)/len(weights)
    norm=[x/mean for x in weights];assert norm==[F(2,3),F(4,3)]
    unstabilized=1/(F(1,4)*F(1,2));stabilized=(F(1,2)*F(1,2))*unstabilized
    observed_survivors,unknown,n=1,2,4
    lower=F(observed_survivors,n);upper=F(observed_survivors+unknown,n)
    midpoint=F(observed_survivors,n)+F(unknown,2*n)
    assert (lower,upper,midpoint)==(F(1,4),F(3,4),F(1,2))
    intervals=[[1,2],[2,3]];support=[float('inf')]
    matrix=[[int(a<=s<=b) for s in support] for a,b in intervals]
    assert matrix==[[0],[0]]
    return dict(scope='Authored exact arithmetic and abstract source traces; no native execution',
      zero_time=dict(input=times,one_based_deleted=deleted,remaining=remaining,all_zero_branch='No deletion when findfirst returns nothing'),
      km_boundary=dict(left=q(before),right=q(after)),
      tied_partial_likelihood=dict(breslow=q(breslow),efron=q(efron),risk_scores=[1,2,3],event_indices=[0,1]),
      entry=dict(correct_risk_increment=q(F(1,2)),entry_ignored=q(F(1,3)),interval_censoring='Unknown event time in an interval is not delayed entry'),
      target_trial=dict(origin_event=origin_event,treatment=treatment,grace=grace,horizon=horizon,source_treated_time=source_time,source_event=source_event,origin_clock_time=origin_observed,origin_clock_event=origin_status,untruncated_source_time=origin_event-treatment,untruncated_origin_time=origin_event),
      rmst_units=dict(rmst_treated=rmst1,rmst_control=rmst0,difference_months=2,risk_difference=riskdiff,difference_days=60),
      weights=dict(conditional_probabilities=[q(x) for x in g],inverse_weights=[q(x) for x in weights],mean_normalized=[q(x) for x in norm],constant_10_mean_normalized=[1,1],longitudinal_unstabilized=q(unstabilized),longitudinal_stabilized=q(stabilized),one_row_mean_normalized=1),
      censoring=dict(lower=q(lower),upper=q(upper),half_imputed=q(midpoint)),
      interval_support=dict(intervals=intervals,support=['infinity'],membership=matrix,zero_row_sums=[0,0],required_action='Refuse unsupported support; do not divide by zero'),
      rmst_uncertainty=dict(time_rescaling=30,required_se_rescaling=30,formula_without_time_width_rescaling=1),
      costs=dict(initiated=12,accepted=3,total_usd=36,usd_per_attempt=q(F(36,12)),usd_per_accepted=q(F(36,3))),native_execution=False)

if __name__=='__main__': print(json.dumps(calculate(),indent=2))
