#!/usr/bin/env python3
"""Independent rational panel regression example; no package code execution."""
from fractions import Fraction as F
import json
import panel_followup_reference_20261024 as prior


def calculate():
    x=list(map(F,[0,1,0,2]));y=list(map(F,[10,13,20,22]));groups=[0,0,1,1]
    def within(v):
        return [a-sum(b for b,g in zip(v,groups) if g==key)/groups.count(key)
                for a,key in zip(v,groups)]
    dx,dy=within(x),within(y)
    gram=sum(a*a for a in dx)
    beta=sum(a*b for a,b in zip(dx,dy))/gram
    residual=[b-beta*a for a,b in zip(dx,dy)]
    scores=[a*b for a,b in zip(dx,residual)]
    cluster_sums=[sum(s for s,g in zip(scores,groups) if g==key) for key in [0,1]]
    raw_cluster=sum(s*s for s in cluster_sums)/(gram*gram)
    raw_white=sum(s*s for s in scores)/(gram*gram)
    assert gram==F(5,2) and beta==F(7,5)
    assert residual==[F(-4,5),F(4,5),F(2,5),F(-2,5)]
    assert cluster_sums==[F(4,5),F(-4,5)]
    assert (raw_cluster,raw_white)==(F(128,625),F(64,625))
    scale=F(4,3);group_scale=F(3,2)
    assert raw_cluster*scale==F(512,1875)
    assert raw_cluster*scale*group_scale==F(256,625)
    return dict(provenance='Authored exact within-regression and covariance calculations;not native package execution or coverage evidence',
      inherited=prior.calculate(),
      within=dict(x=list(map(str,x)),y_thousand_USD=list(map(str,y)),entities=groups,
        demeaned_x=list(map(str,dx)),demeaned_y=list(map(str,dy)),gram=str(gram),
        beta=str(beta),residuals=list(map(str,residual)),scores=list(map(str,scores)),
        cluster_sums=list(map(str,cluster_sums)),raw_cluster_cov=str(raw_cluster),raw_heteroskedastic_cov=str(raw_white),
        covariance_scale=str(scale),separate_group_scale=str(group_scale),
        debiased_nested_cluster_cov=str(raw_cluster*scale),with_group_scale_cov=str(raw_cluster*scale*group_scale),
        regression_df=1,covariance_denominator=3,
        interpretation='Two entity effects,one slope,four rows;regression df differs from nested-cluster scale denominator'),
      singleton_chain=dict(edges=[['A',1],['A',2],['B',2]],first_remove=[['A',1],['B',2]],then_remove=[['A',2]],
        interpretation='Repeated two-core removal can eliminate all rows;not just initial singleton deletion'),
      costs=dict(illustrative_USD=3600,requested=180,finite=150,accepted=120,
        per_request=str(F(3600,180)),per_finite=str(F(3600,150)),per_accepted=str(F(3600,120))),
      native_execution=False)


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
