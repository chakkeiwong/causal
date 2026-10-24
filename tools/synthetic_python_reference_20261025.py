#!/usr/bin/env python3
"""Exact authored Python synthetic-control comparison witnesses."""
from fractions import Fraction as F
import json

def calculate():
    errors=[F(1),F(1),F(4),F(2)]
    inclusive_pre=sum(x*x for x in errors[:3])/3
    double_boundary=sum(x*x for x in errors[2:])/(4-3)/inclusive_pre
    exclusive_post=errors[3]**2/inclusive_pre
    strict_pre=sum(x*x for x in errors[:2])/2
    strict_split=sum(x*x for x in errors[2:])/2/strict_pre
    return {
      'boundary':dict(errors=[str(x) for x in errors],cutoff=3,overlapping_formula=str(double_boundary),inclusive_pre_exclusive_post=str(exclusive_post),strict_pre_inclusive_post=str(strict_split)),
      'self_inclusion':dict(donors=2,donor_exceedances=0,drop_actual_numerator_keep_denominator='0',include_actual=str(F(1,3))),
      'prediction_target':dict(observed=120,conditional_means=[90,110],predictive_draws=[70,130],conditional_effects=[30,10],predictive_effects=[50,-10],coverage_claim=False),
      'calendar':dict(effects=[2,2],durations=[1,3],row_sum=4,duration_weighted_sum=8,interpretation='Different stipulated targets; neither time weighting follows automatically from a date index.'),
      'horizon':dict(treatment=5,horizon=3,candidate_times=[8,9],strict_after=[8>8,9>8]),
      'rms_aggregation':dict(unit_vectors=[[1,-1],[-1,1]],mean_of_unit_rms='1',rms_of_mean_trajectory='0'),
      'dependent_totals':dict(marginal_variances=[1,1],covariance=1,variance_of_sum=4,independence_shortcut=2),
      'cost':dict(total_usd=12000,attempted=400,conformant=300,useful=200,per_attempt=str(F(12000,400)),per_conformant=str(F(12000,300)),per_useful=str(F(12000,200)),observed=False),
    }

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
