#!/usr/bin/env python3
"""Independent algebraic boundary witnesses; not an upstream implementation run."""
from fractions import Fraction as F
import json

def calculate():
    original=[[F(1),F(2)],[F(2),F(1)]]
    full=[[F(3,2),F(3,2)],[F(3,2),F(3,2)]]
    replaced=[[F(1),F(3,2)],[F(3,2),F(3,2)]]
    det=replaced[0][0]*replaced[1][1]-replaced[0][1]*replaced[1][0]
    contrast=[F(3),F(-2)]
    q=sum(contrast[i]*replaced[i][j]*contrast[j] for i in range(2) for j in range(2))
    assert det==F(-3,4) and q==-3
    scores={'A':[F(1),F(3)],'B':[F(2),F(4)]}
    diagonal=sum(v*v for row in scores.values() for v in row)
    lag=sum(row[0]*row[1] for row in scores.values())
    correct=diagonal+lag
    wrong_zero_weight=2*diagonal+lag
    assert diagonal==30 and lag==11 and correct==41 and wrong_zero_weight==71
    x=[F(1),F(3)];weights=[F(1),F(3)]
    wm=sum(a*w for a,w in zip(x,weights))/sum(weights);assert wm==F(5,2)
    residual=[a-wm for a in x];assert sum(w*a for w,a in zip(weights,residual))==0
    wrong=[a-sum(x)/2 for a in x];assert sum(w*a for w,a in zip(weights,wrong))==2
    return dict(psd_block_replacement=dict(original=[[str(v) for v in row] for row in original],full_projection=[[str(v) for v in row] for row in full],replaced=[[str(v) for v in row] for row in replaced],determinant=str(det),contrast=[3,-2],contrast_variance=str(q),attainable_native_output_proven=False),
        newey_west_contract=dict(sum_squares=str(diagonal),same_unit_lag_product=str(lag),halved_zero_weight_result=str(correct),unhalved_zero_weight_result=str(wrong_zero_weight),calendar_gaps_need_explicit_clock=True),
        weighted_projection=dict(weighted_mean=str(wm),weighted_residual_sum='0',unweighted_demeaning_weighted_residual_sum='2'),
        rank=dict(unit_constant_treatment=[0,0,1,1],within_residual=[0,0,0,0],effect_identified=False,zero_effect_inferred=False),
        cost=dict(illustrative_usd=3600,submitted=120,usable=80,per_submission='30',per_usable='45',observed_price=False),
        native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
