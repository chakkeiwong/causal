"""Independent checks for observation bounds and trajectory sufficient statistics."""
from pathlib import Path
from itertools import combinations
import json
import numpy as np
from run_observation_study_20261029 import bounds
from run_policy_uncertainty_20261029 import sufficient,from_sufficient,simulate
from run_servicing_study_20261029 import generate,gfit,direct

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'

def main():
    left=[dict(A=a) for a in [0,0,0,1,1,1]];right=[dict(Y=y) for y in [85,95,110,135,140,150]]
    sets=[[j] for j in range(6)];w=np.array([-1/3]*3+[1/3]*3);y=np.array([r['Y'] for r in right])
    for K in [0,1,2,6]:
        interval,_=bounds(left,right,sets,K);lower=[];upper=[]
        for indexes in combinations(range(6),K):
            yl=y.astype(float).copy();yh=yl.copy()
            for i in indexes:yl[i]=70 if w[i]>0 else 160;yh[i]=160 if w[i]>0 else 70
            lower.append(w@yl);upper.append(w@yh)
        assert np.allclose(interval,[min(lower),max(upper)])
    rng=np.random.default_rng(19261);sc=dict(action_clip=[.2,.8],future_censoring=False)
    d=generate(40,rng,sc);indices=rng.integers(40,size=40);sample={k:v[indices] for k,v in d.items()}
    errors=[]
    for omit in [False,True]:
        b,s=from_sufficient(sufficient(d,omit),np.bincount(indices,minlength=40));bb,ss=gfit(sample,omit)
        errors.append(float(max(np.max(np.abs(b-bb)),abs(s-ss))))
        x=rng.normal(size=100);innov=rng.normal(size=(100,4))
        assert np.allclose(simulate(.5,x,innov,b,s,omit),direct(.5,x,innov,b,s,omit))
    assert max(errors)<1e-10
    exports=list((OUT/'observation-samples').glob('*/analysis/tables.json'))
    for p in exports:
        tables=json.loads(p.read_text())
        assert all(set(row)=={'row_id','name','day','A','X'} for row in tables['left'])
        assert all(set(row)=={'row_id','name','day','Y'} for row in tables['right'])
        assert not ({r['row_id'] for r in tables['left']} & {r['row_id'] for r in tables['right']})
    report=dict(status='pass',bound_exhaustive_cases=4,resampling_errors=errors,
       simulator_equivalence=True,analysis_exports_checked=len(exports),evaluator_truth_absent=True)
    (OUT/'additional-numerical-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
