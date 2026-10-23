#!/usr/bin/env python3
"""Exact authored intervention and prediction witnesses; no upstream execution."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def calculate():
    # U fair, A agrees with U with probability 3/4; Y=2A+4U.
    joint=[(u,a,2*a+4*u,F(1,2)*(F(3,4) if a==u else F(1,4)))
           for u in [0,1] for a in [0,1]]
    conditional=[]
    for a in [0,1]:
        mass=sum(p for u,aa,y,p in joint if aa==a)
        conditional.append(sum(p*y for u,aa,y,p in joint if aa==a)/mass)
    observational=conditional[1]-conditional[0]
    intervention=sum(F(1,2)*((2+4*u)-(4*u)) for u in [0,1])
    assert observational==4 and intervention==2
    # Equal observational laws: A=U,Y=A versus A=U,Y=U.
    obs1=[(u,u,F(1,2)) for u in [0,1]]
    obs2=[(u,u,F(1,2)) for u in [0,1]]
    assert obs1==obs2
    effects=[sum(F(1,2)*(model(1,u)-model(0,u)) for u in [0,1])
             for model in [lambda a,u:a,lambda a,u:u]]
    assert effects==[1,0]
    # Conjugate probability under beta(1,1), six successes, four failures.
    alpha,beta=7,5
    mean=F(alpha,alpha+beta);variance=F(alpha*beta,(alpha+beta)**2*(alpha+beta+1))
    assert mean==F(7,12) and variance==F(35,1872)
    old_x=[1,2];old_det=[x*x for x in old_x];new_det=[x*x*x for x in old_x]
    raw=ROOT/'docs/literature/raw'
    conditioning=(raw/'exec23_pymc_03.txt').read_text()
    forward=(raw/'exec23_pymc_06.txt').read_text()
    basic=(raw/'exec23_pymc_04.txt').read_text()
    mcmc=(raw/'exec23_pymc_07.txt').read_text()
    assert 'make_interventions_shared: bool = True' in conditioning
    assert 'name = f"do_{op.name}"' in conditioning
    assert 'Controls only which variables appear in the output; does not trigger' in forward
    assert 'frozen_vars.update(auto_frozen_vars)' in forward
    assert 'The effect of Potentials on other parameters is ignored during posterior predictive sampling.' in forward
    assert 'Pruning not implemented for models with Potentials' in basic
    assert 'nuts_sampler = "nutpie" if can_use_nutpie else "pymc"' in mcmc
    return dict(kind='authored_exact_reference_not_native_execution',
        conditioning_vs_intervention=dict(conditional_means=list(map(str,conditional)),association=str(observational),effect=str(intervention),stipulated_unit_value='100',stipulated_action_cost='250',association_based_net=str(100*observational-250),causal_net=str(100*intervention-250)),
        observational_equivalence=dict(observed_laws_equal=True,effects=list(map(str,effects)),model_weight_after_equal_likelihood='unchanged from prior'),
        conjugate_posterior=dict(alpha=alpha,beta=beta,mean=str(mean),variance=str(variance)),
        frozen_rv=dict(trace_x='1',trace_y='1',intervention_x='3',frozen_y='1',regenerated_y_mean='3'),
        deterministic_replacement=dict(trace_x=old_x,trace_x_squared=old_det,new_x_cubed=new_det,old_mean=str(F(sum(old_det),2)),new_mean=str(F(sum(new_det),2))),
        predictive_constraint=dict(binary_prior_probability='1/2',hard_positive_weight_probability='1',unconstrained_forward_probability='1/2',caveat='Posterior ancestors can already reflect a Potential; do not claim all posterior consequences disappear.'),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
