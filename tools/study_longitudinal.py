#!/usr/bin/env python3
"""Whole-trajectory fitting and covariance for two fixed observed-history policies."""
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import brentq
from scipy.special import expit,logit
from threadpoolctl import threadpool_limits
from revision_studies import (P_COLL,INIT_COLL,E_COLL,REWARD_COLL,TERMINAL_COLL,
                              GAMMA,coll_sim,coll_fit,coll_q)

ROOT=Path(__file__).resolve().parents[1]


def propensity(s,a):
    out=np.zeros(3)
    for state in (1,2):
        selected=s[:,:-1]==state
        out[state]=(a[selected].sum()+.5)/(selected.sum()+1)
    return out


def evaluate(data,transition,logging,policy,target=False):
    s,a,r=data; n,h=a.shape
    q,v=coll_q(transition,policy,h)
    weights=np.ones((n,h))
    for t in range(h):
        probability=np.where(a[:,t],logging[s[:,t]],1-logging[s[:,t]])
        target_probability=np.where(a[:,t],policy[s[:,t]],1-policy[s[:,t]])
        weights[:,t]=(weights[:,t-1] if t else 1)*target_probability/probability
    max_residual=0.
    if target:
        for t in range(h-1,-1,-1):
            q[t]=np.column_stack([transition[action]@(REWARD_COLL+GAMMA*v[t+1])-12*action for action in (0,1)])
            lo=sum(GAMMA**k*(-172) for k in range(h-t))+GAMMA**(h-t)*(-100)
            hi=sum(GAMMA**k*20 for k in range(h-t))
            scaled=np.clip((q[t]-lo)/(hi-lo),1e-8,1-1e-8)
            offset=logit(scaled)
            y=(r[:,t]+GAMMA*v[t+1,s[:,t+1]]-lo)/(hi-lo)
            def equation(epsilon):
                return np.mean(weights[:,t]*(y-expit(offset[s[:,t],a[:,t]]+epsilon)))
            epsilon=brentq(equation,-40,40,xtol=1e-12)
            max_residual=max(max_residual,abs(equation(epsilon))*(hi-lo))
            q[t]=lo+(hi-lo)*expit(offset+epsilon)
            v[t]=(1-policy)*q[t,:,0]+policy*q[t,:,1]
    augmented=v[0,s[:,0]].copy()
    ips=np.zeros(n)
    for t in range(h):
        augmented+=GAMMA**t*weights[:,t]*(r[:,t]+GAMMA*v[t+1,s[:,t+1]]-q[t,s[:,t],a[:,t]])
        ips+=GAMMA**t*weights[:,t]*r[:,t]
    ips+=GAMMA**h*weights[:,-1]*TERMINAL_COLL[s[:,-1]]
    return {"score":augmented,"plugin":v[0,s[:,0]],"ips":ips,
            "target_equation_max":max_residual,
            "final_weight_ess":float(weights[:,-1].sum()**2/np.sum(weights[:,-1]**2))}


def crossfit(data,policies):
    n=len(data[0]); output={name:np.empty((n,2)) for name in ("augmented","targeted","direct","ips")}
    folds=[np.arange(n//2),np.arange(n//2,n)]
    residual=0.; ess=[]
    for k,evaluation in enumerate(folds):
        training=folds[1-k]; s,a,_=data
        transition=coll_fit(s[training],a[training]); logging=propensity(s[training],a[training])
        for j,policy in enumerate(policies):
            subset=tuple(d[evaluation] for d in data)
            initial=evaluate(subset,transition,logging,policy)
            targeted=evaluate(subset,transition,logging,policy,True)
            output["augmented"][evaluation,j]=initial["score"]
            output["targeted"][evaluation,j]=targeted["score"]
            output["direct"][evaluation,j]=initial["plugin"]
            output["ips"][evaluation,j]=initial["ips"]
            residual=max(residual,targeted["target_equation_max"])
            ess.append(initial["final_weight_ess"])
    return output,{"target_equation_max":residual,"minimum_fold_policy_ess":min(ess)}


def main():
    path=ROOT/"docs/studies/b-history-experiment-v1.json"
    spec=json.loads(path.read_text()); results=[]
    with threadpool_limits(limits=1):
        for ci,case in enumerate(spec["cases"]):
            policies=[np.asarray(v) for v in case["policies"]]
            truth=float(INIT_COLL@(coll_q(P_COLL,policies[1])[1][0]-coll_q(P_COLL,policies[0])[1][0]))
            rows=[]; start=time.perf_counter()
            for rep in range(spec["repetitions"]):
                rng=np.random.default_rng(np.random.SeedSequence([spec["seed"],ci,rep]))
                data=coll_sim(rng,spec["trajectories"])
                try:
                    scores,diagnostics=crossfit(data,policies)
                    record={"rep":rep,"diagnostics":diagnostics,"methods":{}}
                    for name,values in scores.items():
                        contrast=values[:,1]-values[:,0]
                        error=float(contrast.mean()-truth)
                        se=float(contrast.std(ddof=1)/np.sqrt(len(contrast))) if name in ("augmented","targeted") else None
                        record["methods"][name]={"estimate":float(contrast.mean()),"error":error,"se":se,
                                                  "coverage":abs(error)<=1.95996398454*se if se else None}
                    rows.append(record)
                except (ValueError,FloatingPointError) as error:
                    rows.append({"rep":rep,"failure":str(error)})
            summaries={}
            for name in ("augmented","targeted","direct","ips"):
                estimates=[r["methods"][name] for r in rows if "methods" in r]
                coverage=(sum(v["coverage"] for v in estimates)/spec["repetitions"]) if name in ("augmented","targeted") else None
                summaries[name]={"bias":float(np.mean([r["error"] for r in estimates])),
                                 "rmse":float(np.sqrt(np.mean([r["error"]**2 for r in estimates]))),
                                 "coverage":coverage,"mc_se":float(np.sqrt(coverage*(1-coverage)/spec["repetitions"])) if coverage is not None else None}
            result={"case":case,"truth":truth,"seconds":time.perf_counter()-start,"methods":summaries,
                    "failures":sum("failure" in r for r in rows),"records":rows}
            results.append(result)
            print(json.dumps({k:v for k,v in result.items() if k!="records"}),flush=True)
    files=[path,Path(__file__),ROOT/"tools/revision_studies.py"]
    (ROOT/"docs/studies/b-history-results.json").write_text(json.dumps({"spec":spec,
        "input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},"results":results},indent=2)+"\n")


if __name__=="__main__":
    main()
