"""Exact authored panel witnesses; never executes acquired package code."""
from fractions import Fraction as F
import json


def calculate():
    gap = lambda t: F(50*t)
    mean_pre = sum(gap(t) for t in range(-4,1))/5
    baseline = [dict(t=t,event_time=t-1,common_base=str(gap(t)-gap(0)),
        varying_base=str(gap(t)-gap(t-1) if t<=0 else gap(t)-gap(0)),
        asymmetric_imputation=str(gap(t)-gap(-4) if t<=0 else gap(t)-mean_pre),
        symmetric_mean=str(gap(t)-mean_pre)) for t in range(-3,3)]
    treated,controls=[10,30],[90,10]
    pt=[F(n,sum(treated)) for n in treated];pc=[F(n,sum(controls)) for n in controls]
    tau,trend=[F(20),F(60)],[F(0),F(100)]
    theta=sum(w*x for w,x in zip(pt,tau))
    naive=sum(w*(x+d) for w,x,d in zip(pt,tau,trend))-sum(w*d for w,d in zip(pc,trend))
    q=[a/b for a,b in zip(pt,pc)]
    corrected=sum(w*(x+d) for w,x,d in zip(pt,tau,trend))-sum(w*z*d for w,z,d in zip(pc,q,trend))
    assert theta==corrected==50 and naive==115 and sum(w*z for w,z in zip(pc,q))==1
    yt=[tau[a]+trend[a] for a in range(2) for _ in range(treated[a])]
    yc=[(trend[a],q[a]) for a in range(2) for _ in range(controls[a])]
    row_est=sum(yt)/len(yt)-sum(y*w for y,w in yc)/sum(w for y,w in yc)
    assert row_est==theta
    omitted=F(40)+F(-30)*(F(3,4)-F(1,4))
    interaction=omitted+F(20)*F(3,4)
    anchor,donor_base,donor_now,joint=map(F,[40,45,55,85])
    first=anchor+donor_now-donor_base
    literal=joint+donor_now-donor_base
    second=F(95)-F(20)-(F(55)-F(20))
    assert (omitted,interaction,first,literal,second)==(25,40,50,95,40)
    return dict(evidence_class='project-derived synthetic arithmetic, not native or bank evidence',normalization=baseline,
        stacked=dict(treated=treated,controls=controls,treated_shares=list(map(str,pt)),control_shares=list(map(str,pc)),
            control_sample_weights=list(map(str,q)),target=str(theta),naive=str(naive),bias=str(naive-theta),
            corrected=str(corrected),row_level=str(row_est),zero_effect_false_signal=str(naive-theta)),
        composition=dict(both_cohorts='40',early_only='20',constant_cohort_effects=['20','60']),
        multiple_events=dict(target='40',other_effect='-30',exposure_gap='1/2',omitted_event_result=str(omitted),
            interaction='20',interaction_cancellation=str(interaction),target_then_other=str(first),
            selected_v3_equation11_literal=str(literal),other_then_target=str(second),
            simultaneous_target='not_identified_by_this_design'),native_execution=False,empirical_coverage=False)


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
