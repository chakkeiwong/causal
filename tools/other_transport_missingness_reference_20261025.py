#!/usr/bin/env python3
"""Authored cross-language contract fixtures; no downloaded source execution."""
from fractions import Fraction as F
import json

def calculate():
    donor=[F(0),F(1)];mean=sum(donor)/2;variance=sum((x-mean)**2 for x in donor)/2
    numeric_mean=sum([F(1),F(2),F(4)])/3
    source=F(4,5)*0+F(1,5)*2;target=F(2,5)*0+F(3,5)*2
    positional=F(0)+(F(10)-0)/2
    timed=F(0)+(F(10)-0)*F(1,10)
    null_filled=[1,'NaN',0];nan_filled=[1,0,'null']
    return dict(kind='authored_exact_laws_not_native_execution',
        random_donor=dict(mean=str(mean),variance=str(variance),conditional_x_given_y1='1/2',true_x_given_y1='1'),
        knn=dict(requested_k=1,internal_k=2,self_missing_fraction=str(F(1,2)),threshold='1/2',skip_on_excess=False,duplicate_distance=0,inverse_distance_weight='infinite',finite_weight_guard=False),
        integer_completion=dict(input=[1,2,4],mean=str(numeric_mean),truncated_output=int(numeric_mean),mode_tie_smallest=1),
        temporal=dict(times=[0,1,10],values=[0,'missing',10],position_interpolation=str(positional),time_interpolation=str(timed),future_dependency=True),
        population_boundary=dict(customer=['A','B'],observed=[7,'missing'],global_forward=[7,7],within_customer_forward=[7,'missing']),
        masks=dict(input=[1,'NaN','null'],fill_null_zero=null_filled,fill_nan_zero=nan_filled,combined=[1,0,0]),
        quantile=dict(probability='1/2',relative_rank_error='1/1000',n=10000,rank_lower=4990,rank_upper=5010,value_error_bound=None),
        transport=dict(source_effect=str(source),target_effect=str(target),difference=str(target-source)),
        economics=dict(accounts=10000,dollars_per_unit=10,discrepancy_usd=str((target-source)*10000*10)),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
