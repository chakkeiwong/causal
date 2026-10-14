#!/usr/bin/env python3
"""Execute the matched controlled-model fitting and fixed-policy experiment."""
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.controlled import pack,fit,contrast,information_interval,simulate


def main():
    path = ROOT/"docs/studies/b-latent-experiment-v1.json"
    spec = json.loads(path.read_text())
    results = []
    bootstrap_source = None
    with threadpool_limits(limits=1):
        for ci,case in enumerate(spec["cases"]):
            gap = case["emission_gap"]
            model = {"mu":np.array([.65,.35]),
                     "emission":np.array([[.5+gap/2,.5-gap/2],[.5-gap/2,.5+gap/2]]),
                     "transition":np.array([[[.9,.1],[.2,.8]],[[.92,.08],[.48,.52]]]),
                     "reward":np.array([[.85,.3],[.88,.48]])}
            truth = contrast(pack(model))
            records=[]
            start=time.perf_counter()
            for rep in range(case["repetitions"]):
                rng=np.random.default_rng(np.random.SeedSequence([spec["seed"],ci,rep]))
                data=simulate(model,spec["trajectories"],spec["horizon"],rng,case["private_logger"])
                parameter,diagnostics=fit(data,spec["seed"]+1000*ci+rep,spec["starts"],spec["em_iterations"],spec["optimizer_iterations"])
                uncertainty=information_interval(parameter,data)
                estimate=contrast(parameter)
                accepted=(uncertainty["se"] is not None and diagnostics["optimizer_success"] and not diagnostics["on_boundary"])
                coverage=bool(accepted and abs(estimate-truth)<=1.95996398454*uncertainty["se"])
                records.append({"rep":rep,"estimate":estimate,"error":estimate-truth,
                                "interval_reported":accepted,"coverage":coverage,"fit":diagnostics,"uncertainty":uncertainty})
                if ci==0 and rep==0:
                    bootstrap_source=data,parameter.copy()
                if rep%20==19:
                    print(json.dumps({"case":case["id"],"completed":rep+1,"seconds":time.perf_counter()-start}),flush=True)
            coverage=float(np.mean([r["coverage"] for r in records]))
            row={"case":case,"truth":truth,"seconds":time.perf_counter()-start,
                 "coverage":coverage,"mc_se":float(np.sqrt(coverage*(1-coverage)/len(records))),
                 "interval_failure_rate":float(np.mean([not r["interval_reported"] for r in records])),
                 "bias":float(np.mean([r["error"] for r in records])),
                 "rmse":float(np.sqrt(np.mean([r["error"]**2 for r in records]))),"records":records}
            results.append(row)
            print(json.dumps({k:v for k,v in row.items() if k!="records"}),flush=True)
        data,parameter=bootstrap_source
        rng=np.random.default_rng(spec["seed"]+991)
        bootstrap=[]
        for rep in range(spec["bootstrap_repetitions"]):
            idx=rng.integers(0,len(data[0]),len(data[0]))
            fitted,diag=fit(tuple(v[idx] for v in data),spec["seed"]+5000+rep,spec["starts"],spec["em_iterations"],spec["optimizer_iterations"])
            bootstrap.append({"estimate":contrast(fitted),"fit":diag})
            if rep%20==19:
                print(json.dumps({"bootstrap_completed":rep+1}),flush=True)
    files=[path,Path(__file__),ROOT/"src/causalbank/controlled.py"]
    receipt={"spec":spec,"input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
             "results":results,"bootstrap":{"point":contrast(parameter),"percentile_interval":np.quantile([v["estimate"] for v in bootstrap],[.025,.975]).tolist(),"records":bootstrap}}
    (ROOT/"docs/studies/b-latent-results.json").write_text(json.dumps(receipt,indent=2)+"\n")


if __name__=="__main__":
    main()
