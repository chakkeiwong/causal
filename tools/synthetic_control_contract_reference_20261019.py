#!/usr/bin/env python3
"""Exact authored donor contamination and selection example, not a vendor trial."""
from fractions import Fraction as F
import json


def calculate():
    donor1=[F(90),F(110),F(120)];donor2=[F(110),F(130),F(140)];treated=[F(100),F(120),F(150)]
    original=[(x+y)/2 for x,y in zip(donor1,donor2)]
    assert original[:2]==treated[:2]
    true_gap=treated[2]-original[2]
    contaminated=donor2[:2]+[F(160)]
    contaminated_synthetic=(donor1[2]+contaminated[2])/2
    apparent_gap=treated[2]-contaminated_synthetic
    # Choosing weights using the treated postintervention outcome fits away the gap.
    w=F(1,4);selected=[w*x+(1-w)*y for x,y in zip(donor1,contaminated)]
    assert true_gap==20 and apparent_gap==10 and treated[2]-selected[2]==0
    assert selected[:2]==[F(105),F(125)]
    return dict(kind='authored_exact_regional_portfolio_reference',units='thousand_USD',upstream_execution=False,
        uncontaminated=dict(weights=['1/2','1/2'],pre_fit_exact=True,post_counterfactual=str(original[2]),post_gap=str(true_gap)),
        spillover=dict(donor2_increment='20',synthetic_increment='10',apparent_gap=str(apparent_gap)),
        post_outcome_selection=dict(donor1_weight=str(w),donor2_weight=str(1-w),selected_pre_values=[str(x) for x in selected[:2]],selected_post_gap='0'),
        illustrative_rank_count=dict(including_treated_total=5,as_extreme=1,ratio='1/5',after_retaining_only_two_units='1/2',validity='Counting alone is not a calibrated p-value; exchangeability, eligibility, pre-fit selection and null protocol must be justified.'),
        assumptions=['The untreated treated-unit trajectory equals the original half-half donor average by stipulation.','The treated outcome is150 while its stipulated untreated outcome is130.','Donor2 receives a20-unit spillover in the separate contaminated scenario.'],
        limitations=['No estimation, native optimizer execution, institutional data or inference calibration.','These exact scenarios demonstrate donor and tuning-contract failures; they do not identify a real effect.'])


if __name__=='__main__': print(json.dumps(calculate(),indent=2))
