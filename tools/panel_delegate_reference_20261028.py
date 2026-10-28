"""Independent exact witnesses of selected source contracts; no R/Stata execution."""
from fractions import Fraction as F
import json


def ratios(t,c):
    return [F(a,sum(t))/F(b,sum(c)) for a,b in zip(t,c)]


def calculate():
    triangular=lambda n:n*(n+1)//2
    balanced=ratios([10,30],[90,10])
    balanced_tri=ratios([10*triangular(3),30*triangular(3)],[90*triangular(3),10*triangular(3)])
    assert balanced==balanced_tri==[F(5,18),F(15,2)]
    unequal_tri=ratios([triangular(2),triangular(3)],[triangular(2),triangular(2)])
    unequal_rows=ratios([2,3],[2,2])
    common_period=ratios([1,1],[1,1])
    assert unequal_tri==[F(2,3),F(4,3)] and unequal_rows==[F(4,5),F(6,5)]
    # Independent transcription of the selected numeric inclusion predicates.
    focal,horizon=5,2
    cases=[]
    for date in [1,3,5,7,8,None]:
        intended=date is None or date==focal or date>focal+horizon
        selected=intended or date==1
        cases.append(dict(adoption=date,intended=intended,selected_R_expression=selected))
    assert [c['adoption'] for c in cases if c['intended']!=c['selected_R_expression']]==[1]
    n,k=8,4
    penalty=2*k+F(2*k*(k+1),n-k-1)
    assert penalty==F(64,3)
    # Same-cohort intersection avoids changes in donor composition.
    donor_base={'A':F(10),'B':F(20)};donor_now={'B':F(25),'C':F(60)}
    separate=sum(donor_now.values())/2-sum(donor_base.values())/2
    common=donor_now['B']-donor_base['B']
    assert separate==F(55,2) and common==5
    return dict(evidence_class='authored exact source-contract witnesses',
        balanced_weights=list(map(str,balanced)),balanced_triangular_weights=list(map(str,balanced_tri)),
        unequal=dict(treated_lengths=[2,3],control_lengths=[2,2],triangular_weights=list(map(str,unequal_tri)),
            pooled_row_weights=list(map(str,unequal_rows)),common_period_weights=list(map(str,common_period)),
            implication='Different counting conventions outside balance; no unbalanced causal equivalence claimed'),
        numeric_adoption_cases=cases,donor_intersection=dict(separate_normalization=str(separate),common_cohort=str(common)),
        pampe=dict(requested_pre_rows=list(range(5,13)),robustness_reconstructed_pre_rows=list(range(1,9)),
            aicc_n=n,aicc_k=k,aicc_penalty=str(penalty),zero_denominator=dict(n=4,k=3)),
        native_execution=False,empirical_coverage=False)


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
