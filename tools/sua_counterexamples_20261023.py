#!/usr/bin/env python3
"""Project-authored finite counterexamples; no paper code/model execution."""
from fractions import Fraction as F
from math import log

def calculate():
    h=log(2)
    # Eq11: TV divergence, binary zero-one loss, singleton interpretation,
    # constant fair model=true law, psi=0 (concave/nondecreasing), lambda=LD=1.
    constant=dict(sensitivity=0,entropy=h,psi=0,LD=1,lambda_=1,kappa=0,base_risk=.5,worst_risk=.5,claimed_eq11_upper=.5-h)
    assert constant['worst_risk']>constant['claimed_eq11_upper']
    # Eq10: bounded zero-one loss scaled by indicator of an auxiliary event
    # is unnecessary: use a constant loss c for every label/action and psi(h)
    # = c*(1-exp(-h)); valid for ALL finite distributions and fixed actions.
    # LD=1 is a valid (nonminimal) constant since risk differences are zero.
    c=F(1,2);psi=c/2
    eq10=dict(loss='constant1/2 for all labels/actions',psi='(1-exp(-h))/2',LD=1,lambda_=1,entropy=h,divergence=0,kappa=0,base_risk=str(c),worst_risk=str(c),claimed_upper=str(c-psi))
    assert c>c-psi and h>=float(psi)
    # Rare perturbation: model point mass at x, fair at x_bad, true label0;
    # two-point Pi gives positive mass everywhere; expected TV != supremum.
    eps=F(1,100);tv=F(1,2)
    rare=dict(adverse_mass=str(eps),expected_TV=str(eps*tv),supremum_TV=str(tv),base_self_risk='0',worst_self_risk='1/2',kappa='0',psi='0',base_entropy=0)
    # Selection: low-SUA uniform model on hard subgroup accepted at tau0;
    # easy deterministic model has positive perturbation sensitivity rejected.
    mass=F(1,10);hard=F(1,2);global_risk=mass*hard
    selection=dict(hard_mass=str(mass),hard_score=-h,easy_score=.5,threshold=0,coverage=str(mass),global_base_risk=str(global_risk),conditional_base_risk=str(hard),gap=str(hard-global_risk))
    assert hard>global_risk
    # Entropy calibration is not probability calibration or truth.
    entropy=dict(true_probabilities=['9/10','1/10'],model_probabilities=['1/10','9/10'],entropy_gap=0,TV='4/5',model_mode_error='9/10')
    # Two equally likely interpretations map deterministically to SAME label.
    ambiguity=dict(interpretation_entropy=h,label_entropy=0,model_entropy=0,eta=h,miscalibration_gap=0,explanation='Distinct interpretation labels need not induce distinct output labels; eta can remove the claimed positive bound.')
    # Bounded loss versus KL cannot be uniformly linear near equality.
    ratios=[]
    for e in [0.1,0.01,0.001]:
        kl=-.5*log(1-4*e*e);ratios.append(dict(epsilon=e,loss_difference=e,KL=kl,ratio=e/kl))
    assert ratios[-1]['ratio']>400
    return dict(evidence_class='authored_mathematical_counterexamples_not_native_trials',eq11_constant_fair=constant,eq10_constant_loss=eq10,rare_perturbation=rare,conditional_selection=selection,equal_entropy_wrong_labels=entropy,many_to_one_interpretations=ambiguity,KL_linear_constant=ratios,native_execution=False)
if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
