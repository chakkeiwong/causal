#!/usr/bin/env python3
"""Independent authored tmle contracts; no R or downloaded implementation execution."""
from fractions import Fraction as F
from math import exp
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def q(x):
 x=F(x);return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))
def quantile7(values,p):
 values=sorted(map(F,values));h=(len(values)-1)*F(p);j=h.numerator//h.denominator;f=h-j
 return values[j] if j==len(values)-1 else values[j]*(1-f)+values[j+1]*f

def calculate():
 w=[F(1),F(3)];q0=[F(1,10),F(4,10)];q1=[F(2,10),F(5,10)]
 mu0=sum(a*b for a,b in zip(w,q0))/sum(w);mu1=sum(a*b for a,b in zip(w,q1))/sum(w)
 assert (mu0,mu1,mu1-mu0,mu1/mu0)==(F(13,40),F(17,40),F(1,10),F(17,13))
 rr=F(2);rd=F(1,10);wrong=exp(float(rd));assert abs(wrong-2)>F(4,5)
 full=[F(0),F(1),F(100)];draws=full[:-1];ci=[quantile7(full,p) for p in [F(1,40),F(39,40)]];drawci=[quantile7(draws,p) for p in [F(1,40),F(39,40)]]
 assert ci==[F(1,20),F(1901,20)] and drawci==[F(1,40),F(39,40)]
 return dict(weighted_target=dict(weights=[1,3],q0=[q(x) for x in q0],q1=[q(x) for x in q1],mu0=q(mu0),mu1=q(mu1),risk_difference=q(mu1-mu0),risk_ratio=q(mu1/mu0),odds_ratio=q(mu1*(1-mu0)/(mu0*(1-mu1)))),population=dict(cluster_sizes=[1,3],cluster_effects=[0,10],row_average=q(F(15,2)),customer_average=q(F(5))),cluster_score=dict(ids=[1,2,2,2],row_scores=[-3,1,1,1],cluster_means=[-3,1],variance_cluster_means_over_two=q(4),cluster_sums=[-3,3],scaled_cluster_sums=[q(F(-3,2)),q(F(3,2))],variance_ratio_score_over_two=q(F(9,4)),claim='Deterministic score arithmetic; statistical validity depends on the sampling law and estimand.'),interval_column=dict(columns=['EY0','EY1','ATE','logRR','logOR'],constant_risk0=q(F(1,10)),constant_risk1=q(F(1,5)),risk_difference=q(rd),correct_rr=q(rr),exponentiated_rd=wrong,source_variance_column=4,source_cde_rr_interval_column=3,ordinary_rr_interval_column=4,native_execution=False),bootstrap=dict(B=3,resampled_rows=2,original_sample_rows=1,full_vector=[q(x) for x in full],quantiles_including_original=[q(x) for x in ci],draw_only_quantiles=[q(x) for x in drawci],missing_replicate_vector=[1,None,3],finite_quantile_endpoints=[q(F(21,20)),q(F(59,20))],variance_without_na_removal='NA',requested_rows=3,finite_rows=2),support=dict(untruncated_probability=q(F(1,100)),truncated_probability=q(F(1,10)),inverse_weights=[100,10],claim='Truncation controls arithmetic; it does not manufacture missing support.'),economics=dict(total_usd=2400,requested=120,conformant=100,useful=80,per_requested=20,per_conformant=24,per_useful=30,illustrative=True),native_execution=False)
if __name__=='__main__':
 p=ROOT/'docs/program/execution/2026-10-24/tmle-reuse-v1/exact-results.json';assert not p.exists();p.write_text(json.dumps(calculate(),indent=2)+chr(10));print('Authored exact tmle semantic witnesses saved.')
