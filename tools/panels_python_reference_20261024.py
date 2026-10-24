#!/usr/bin/env python3
"""Authored finite arithmetic; never imports or executes upstream package code."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    phi=[F(3),F(-1),F(-1),F(-1)]
    groups=[phi[:1],phi[1:]]; n=len(phi); c=len(groups)
    sums=[sum(g) for g in groups]; means=[sum(g)/len(g) for g in groups]
    unit=[sum(s*u for s,u in zip(sign,sums))/n for sign in product([-1,1],repeat=c)]
    equal_cluster=[sum(s*u for s,u in zip(sign,means))/c for sign in product([-1,1],repeat=c)]
    unit_var=sum(x*x for x in unit)/len(unit); mean_var=sum(x*x for x in equal_cluster)/len(equal_cluster)
    assert unit_var==F(9,8) and mean_var==F(5,2)
    iid=sum(x*x for x in phi)/n**2; assert iid==F(3,4)
    cells=[F(2),F(4),F(10)]; shares=[F(3,4),F(3,4),F(1,4)]
    simple=sum(x*w for x,w in zip(cells,shares))/sum(shares)
    cohort=F(3,4)*F(3)+F(1,4)*10; event=(F(4)+4)/2; calendar=(F(2)+F(11,2))/2
    assert [simple,cohort,event,calendar]==[F(4),F(19,4),F(4),F(15,4)]
    # An array with dimensions (1,2) has one outer element; zipping with
    # two worker chunks schedules only the first. This is shape arithmetic,
    # not execution of numpy/joblib/tqdm or the inspected package.
    jobs=2; iterations=10; chunks=[iterations//jobs]*jobs
    scheduled=chunks[:1]; assert sum(scheduled)==5
    return dict(kind='authored_exact_reference_not_package_output',
      aggregation={k:str(v) for k,v in zip(['simple','cohort','event','calendar'],[simple,cohort,event,calendar])},
      unequal_clusters=dict(unit_influences=list(map(str,phi)),sizes=[1,3],cluster_sums=list(map(str,sums)),cluster_means=list(map(str,means)),unit_multiplier_draws=list(map(str,unit)),equal_cluster_multiplier_draws=list(map(str,equal_cluster)),unit_multiplier_variance=str(unit_var),equal_cluster_multiplier_variance=str(mean_var),iid_variance=str(iid),returned_package_iqr_se_claim=False),
      worker_shape=dict(jobs=jobs,requested_iterations=iterations,chunks=chunks,mask_shape=[1,2],outer_length=1,potential_scheduled_iterations=sum(scheduled),native_execution=False),
      seed_branch=dict(seed_zero_truth=False,nonzero_truth=True,global_rng_state_required_if_zero=True),
      cluster_list=dict(requested=['unit','region'],aggregate_first_only='unit',extra_region_retained=False),
      band_label=dict(bstrap=True,cband_after_fallback=False,formatter_label='Simult.',actual_cutoff='pointwise_normal'),
      control=dict(time=2,anticipation=1,next_cohort3_eligible=False,next_cohort4_eligible=True),
      illustrative_cost_usd={k:str(F(3600,v)) for k,v in [('requested',180),('conformant',150),('useful',120)]},
      limitations=['No native package output,coverage,performance or scientific identification claimed.','Finite multiplier variances describe constructed laws,not the packages returned IQR estimates.'])

if __name__=='__main__': print(json.dumps(calculate(),indent=2))
