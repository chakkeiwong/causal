#!/usr/bin/env python3
"""Independent rational examples; never imports or executes downloaded synthdid."""
from fractions import Fraction as F
import json

def calculate():
    Y = [[F(v) for v in row] for row in [[10,12,14,16],[20,22,26,28],[15,17,25,27],[18,20,28,30]]]
    omega, lam = [F(3,4), F(1,4)], [F(1,4), F(3,4)]
    def contrast(M, w):
        a = [-x for x in w] + [F(1,2), F(1,2)]
        b = [-x for x in lam] + [F(1,2), F(1,2)]
        return sum(a[i]*M[i][j]*b[j] for i in range(4) for j in range(4))
    tau = contrast(Y, omega)
    shifted = [[v + (100 if j >= 2 else 0) for j,v in enumerate(row)] for row in Y]
    bad = [F(1,2),F(1,4)]
    rejected = 2*F(1,2)**4
    results = dict(
        weighted_block=dict(Y=[[int(v) for v in row] for row in Y],omega=list(map(str,omega)),lambda_weights=list(map(str,lam)),
          fixed_weight_effect=str(tau),cost='4',net=str(tau-4),common_post_shift='100',
          valid_shift_difference=str(contrast(shifted,omega)-tau),
          nonunit_omega=list(map(str,bad)),nonunit_shift_difference=str(contrast(shifted,bad)-contrast(Y,bad))),
        bootstrap=dict(units=4,controls=2,treated=2,homogeneous_group_rejection_probability=str(rejected),
          valid_group_probability=str(1-rejected),expected_draws_per_valid_group=str(1/(1-rejected)),
          scope='Group-composition rejection only; computational NA/errors are separate.'),
        simplex=dict(weights=['3/4','1/4'],effective_controls=str(1/sum(w*w for w in omega))),
        option_reconstruction=dict(saved=['zeta.omega','zeta.lambda','omega.intercept','lambda.intercept','update.omega','update.lambda','min.decrease','max.iter'],
          omitted=['sparsify','max.iter.pre.sparsify']),
        limits=['Fixed supplied weights, not weights fitted by synthdid.',
          'Stipulated banking units/costs; no observed bank return or native output.',
          'No identification, calibration, speed or bootstrap convergence established.'])
    assert tau==F(11,2) and contrast(shifted,omega)==tau
    assert contrast(shifted,bad)-contrast(Y,bad)==25 and rejected==F(1,8)
    assert F(1)/sum(w*w for w in omega)==F(8,5)
    return results

if __name__=='__main__': print(json.dumps(calculate(),indent=2))
