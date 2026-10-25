#!/usr/bin/env python3
"""Exact authored fixtures for C++ source contracts; no retrieved code execution."""
from fractions import Fraction as F
import json

def calculate():
    mean=(F(0)+F(2))/2
    second=(F(0)**2+F(2)**2)/2
    selected=F(1,2)*F(3,4)/(F(1,2)*F(3,4)+F(1,2)*F(1,4))
    smoothed=(F(2)+1)/(F(2)+0+2)
    source=F(4,5)*0+F(1,5)*2
    target=F(2,5)*0+F(3,5)*2
    assert selected==F(3,4) and target-source==F(4,5)
    # Explicit latent law U~Bernoulli(1/2), A=U, Y=U. Intervention changes A only.
    joint=[dict(u=u,a=u,y=u,mass=F(1,2)) for u in [0,1]]
    cond=sum(x['mass']*x['y'] for x in joint if x['a']==1)/sum(x['mass'] for x in joint if x['a']==1)
    intervention=sum(x['mass']*x['y'] for x in joint)
    left,right,threshold=F(1,10),F(9,10),F(1,2)
    observed_zero=left if 0<threshold else right
    # Hypothetical stump default is right; no fitted XGBoost output is claimed.
    missing=right
    return dict(kind='authored_exact_laws_not_native_execution',
        completion=dict(mean=str(mean),expected_square=str(second),square_of_mean=str(mean**2),conditional_variance=str(second-mean**2)),
        deletion=dict(population_mean='1/2',observed_mean=str(selected),discrepancy=str(selected-F(1,2))),
        sentinel=dict(true_values=[0,2],true_mean=str(mean),mean_after_zero_removed='2'),
        pseudocount=dict(counts=[2,0],pseudocount_per_state=1,estimated_first_state=str(smoothed),unsmoothed_first_state='1',zero_count_zero_prior_vector=['0','0']),
        conditioning=dict(observed_a1=str(cond),intervention_a1=str(intervention),conditioning_is_intervention=False),
        em_stopping=dict(previous_log_likelihood=-100,current_log_likelihood=-101,decreased=True,selected_termination_returns_true=True,convergence_established=False),
        tree_routing=dict(observed_zero_prediction=str(observed_zero),missing_default_prediction=str(missing),difference=str(missing-observed_zero)),
        transport=dict(source_effect=str(source),target_effect=str(target),difference=str(target-source)),
        economics=dict(hypothetical_accounts=10000,dollars_per_unit=10,discrepancy_usd=str((target-source)*10000*10)),
        native_execution=False)

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
