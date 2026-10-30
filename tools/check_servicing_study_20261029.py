from pathlib import Path
import json
import sys
import numpy as np
from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'
sys.path.insert(0,str(ROOT/'tools'))
from run_servicing_study_20261029 import generate,ipw,gfit

d=json.loads((OUT/'servicing-results.json').read_text());rows=json.loads((OUT/'servicing-replications.json').read_text())
assert d['complete'] and d['completed_scenarios']==4 and len(rows)==4*200*6
rng=np.random.default_rng(9917);sample=generate(150,rng,dict(action_clip=[.2,.8],future_censoring=False))
score,_,_=ipw(sample,.5)
manual=[]
for i in range(150):
    weight=1.;value=0.
    for t in range(3):
        pa=sample['p'][i,t] if sample['A'][i,t] else 1-sample['p'][i,t]
        weight*=int(sample['A'][i,t]==int(sample['L'][i,t]>.5))*int(sample['observed'][i,t])/(pa*sample['g'][i,t])
        value+=weight*sample['R'][i,t]
    manual.append(value)
assert np.allclose(score,manual)
# Values hidden by dropout do not affect either estimator.
changed={k:v.copy() for k,v in sample.items()};changed['R'][~changed['observed']]=1e8;changed['N'][~changed['observed']]=-1e8
assert np.allclose(ipw(changed,.5)[0],score)
assert np.allclose(gfit(changed,False)[0],gfit(sample,False)[0])
checks=[]
for row in d['scenarios']:
    rs=[r for r in rows if r['scenario']==row['scenario'] and r['policy']==row['policy']]
    p=row['reference_point_coverage'];n=len(rs);z=norm.ppf(.975)
    centre=(p+z*z/(2*n))/(1+z*z/n);half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    ambiguous=sum(r['ambiguous_reference_boundary'] for r in rs)
    covered=sum(r['reference_covered'] for r in rs)
    certainly=sum(r['reference_covered'] and not r['ambiguous_reference_boundary'] for r in rs)
    paired_positive=sum(r['paired_vs_zero']-z*r['paired_se']>0 for r in rs)
    checks.append(dict(scenario=row['scenario'],policy=row['policy'],coverage_wilson_95=[centre-half,centre+half],
                      reference_uncertainty_coverage_bounds=[certainly/n,min(1.,(covered+ambiguous)/n)],
                      positive_paired_lower_bound_frequency=paired_positive/n,
                      interpretation='Wilson interval describes Monte Carlo sampling at point reference; reference bands are separate, not exact coverage certification'))
out=dict(status='pass',rows=len(rows),manual_prefix_score='matches vectorised calculation',
         hidden_rewards_and_next_states='mutation does not change fitted estimates',
         checks=checks,rankings='No empirical method-superiority certification. Simulated bias is conditional on supplied law.',
         additional_limit='g-computation receives the known initial-state distribution and reward function; its simulation uncertainty does not include parameter uncertainty')
(OUT/'servicing-verification.json').write_text(json.dumps(out,indent=2)+chr(10))
print(json.dumps(dict(status='pass',replication_rows=len(rows),checks='manual prefix arithmetic and hidden-outcome masking')))
