#!/usr/bin/env python3
"""Exact authored laws and abstract control-flow witnesses; no R execution."""
from fractions import Fraction as F
from itertools import product

def calculate():
    d,p=F(1,10),F(2,5)
    risk=d+(1-d-p)*d
    eliminated=d+(1-d)*d
    assert (risk,eliminated)==(F(3,20),F(19,100))
    price,loss=1700,10000
    values=[F(a+b) for a,b in product([-1,1],repeat=2)]
    true_variance=sum(v*v for v in values)/len(values)
    row_independent=F(8,16);subject_independent=F(16,16)
    assert (row_independent,subject_independent,true_variance)==(F(1,2),F(1),F(2))
    dscore=[F(3),F(-1)];m=sum(dscore)/len(dscore)
    unc=sum(v*v for v in dscore)/4
    centered=sum((v-m)**2 for v in dscore)/4
    assert unc-centered==m*m/2==F(1,2)
    counts=[]
    for cap in [1,2,10]:
        updates=0;stored=None;q=F(0)
        for it in range(1,cap+2):
            stored=q
            if it>1:
                if False: break
            elif it>cap: break
            q+=1;updates+=1
        hct=0
        while True and hct<=cap:hct+=1
        assert updates==hct==cap+1 and stored==cap and q==cap+1
        counts.append(dict(cap=cap,stremr_updates=updates,survtmle_updates=hct,preupdate_marker=str(stored),final_marker=str(q)))
    return dict(evidence_class='authored_exact_reference_not_native_execution',
        competing_events=dict(default_hazard=str(d),prepay_hazard=str(p),two_period_default_risk=str(risk),eliminate_prepay_default_risk=str(eliminated),loss_usd=loss,insurance_price_usd=price,actual_law_insurance_margin=str(risk*loss-price),eliminated_law_insurance_margin=str(eliminated*loss-price)),
        covariance=dict(supplied_law='Two independent branch signs; two subjects per branch; two equal visit contributions per subject; estimator is total visit contribution divided by four subjects.',row_independence=str(row_independent),subject_independence=str(subject_independent),true_branch_variance=str(true_variance)),
        influence_centering=dict(scores=['3','-1'],mean=str(m),uncentered_over_n_squared=str(unc),centered_over_n_squared=str(centered),difference=str(unc-centered),statement='Same denominator only; no finite-sample unbiasedness claim.'),
        loop_controls=dict(condition='Persistent failed tolerance; cap integer >=1; abstract update marker only.',cases=counts),
        horizon=dict(observed_event_grid=[2,5],prediction_grid=list(range(1,6)),prediction_rows_per_subject=5,observed_rows_for_late_subject=2,statement='Grid cardinalities differ; no native mismatch or failure is established.'),
        native_execution=False)

if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
