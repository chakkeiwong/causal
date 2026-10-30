"""Independent raw-data and score-distribution checks; no package execution."""
from pathlib import Path
from fractions import Fraction as F
import csv,json,math
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'docs/twelve-hour-closure/2026-10-29'
def main():
    out=O/'partial-recovery-attempt-1/independent-check.json';assert not out.exists()
    checks=[]
    for name in ['standard','intensive','complete','unstable']:
        folder=out.parent/name;rows=list(csv.DictReader((folder/'replications.csv').open()))
        summaries=json.loads((folder/'result.json').read_text())['summaries']
        for rep in [0,249,499]:
            d=np.load(folder/f'data-{rep}.npz')
            for q in [.1,.25,.5,1.]:
                estimates=[]
                for a in [0,1]:
                    y=d[f'a{a}_y'];r=d[f'a{a}_r'];s=d[f'a{a}_s'];u=d[f'a{a}_u'];reported=d[f'a{a}_reported']
                    recovered=(~r)&(u<q)&s
                    lower=(sum(float(x)for x in y[r])+sum(float(x)for x in reported[recovered])/q)/len(y)
                    upper=(sum(float(x)for x in y[r])+int((~r).sum())-sum(float(1-x)for x in reported[recovered])/q)/len(y)
                    estimates.append((lower,upper))
                target=next(x for x in rows if int(x['rep'])==rep and float(x['q'])==q)
                assert abs(estimates[1][0]-estimates[0][1]-float(target['lower']))<1e-12
                assert abs(estimates[1][1]-estimates[0][0]-float(target['upper']))<1e-12
        for s in summaries:
            rr=[r for r in rows if float(r['q'])==s['q']]
            for key in ['hoeffding_covers_truth','normal_covers_truth','normal_covers_region','hoeffding_covers_region']:
                assert sum(r[key]=='True'for r in rr)/len(rr)==s[key]
            for meth in ['normal','hoeffding']:
                assert abs(sum(float(r[meth+'_upper'])-float(r[meth+'_lower'])for r in rr)/len(rr)-s[meth+'_mean_width'])<1e-12
        checks.append(dict(regime=name,raw_dataset_endpoint_checks=12,summary_checks=True,
           raw_crossings=sum(r['crossing_raw']=='True'for r in rows),
           confidence_empty={m:sum(float(r[m+'_lower'])>float(r[m+'_upper'])for r in rows)for m in ['normal','hoeffding']}))
    # Recovered treated records in the violated case: mass .38, reported
    # success mass .245; unchanged historical success mass .11.
    rec=F(19,50);reported=F(49,200)/rec;historical=F(11,100)/rec
    required=reported-historical;assert required==F(27,76)
    sensitivity=[]
    for gamma in [F(0),F(1,10),F(1,5),F(3,10),required,F(2,5),F(1)]:
        # Control recovered outcomes stipulated stable, treated drift bounded.
        lo=F(11,25)+rec*max(F(0),reported-gamma)-F(9,20)
        hi=F(11,25)+rec*min(F(1),reported+gamma)-F(9,20)
        sensitivity.append(dict(gamma=float(gamma),lower=float(lo),upper=float(hi),contains_truth=lo<=F(1,10)<=hi))
    out.write_text(json.dumps(dict(status='pass',checks=checks,
       identified_sets={'routine_only':[-.12,.64],'standard':[-.087,.154],'intensive':[.056,.1108],'complete':[.1,.1]},
       stability_sensitivity=sensitivity,required_gamma=float(required),
       caveat='Gamma is a stated external limit on mean change among recovered treated records,not estimated from these data andnotattritiondelta.'),indent=2)+'\n')
    print(json.dumps(dict(status='pass',datasets=12,endpoint_reconstructions=48,checks=checks,required_gamma=float(required))))
if __name__=='__main__':main()
