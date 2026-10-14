#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from scipy.signal import lfilter
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.responses import bartlett_lrv


def variance_mean(rho,t):
    k=np.arange(1,t)
    return (t+2*np.sum((t-k)*rho**k))/t**2


def main():
    path=ROOT/"docs/studies/a-panel-v1.json"; spec=json.loads(path.read_text()); results=[]
    with threadpool_limits(limits=1):
        for t in spec["dates"]:
            rows=[]; n=spec["banks"]
            for rep in range(spec["repetitions"]):
                rng=np.random.default_rng(np.random.SeedSequence([spec["seed"],t,rep]))
                c=lfilter([np.sqrt(1-spec["common_ar"]**2)],[1,-spec["common_ar"]],rng.normal(size=t+300))[300:]
                e=lfilter([np.sqrt(1-spec["idio_ar"]**2)],[1,-spec["idio_ar"]],rng.normal(size=(n,t+300)),axis=1)[:,300:]
                x=spec["theta"]+c+e; dates=x.mean(axis=0); estimate=float(dates.mean())
                se={"row_iid":float(x.std(ddof=1)/np.sqrt(n*t)),
                    "date_HAC":float(np.sqrt(bartlett_lrv(dates[:,None],int(t**.25))[0,0]/t)),
                    "exact_finite_Gaussian_variance":float(np.sqrt(variance_mean(spec["common_ar"],t)+variance_mean(spec["idio_ar"],t)/n))}
                rows.append({"estimate":estimate,"se":se,"coverage":{name:abs(estimate-spec["theta"])<=1.95996398454*v for name,v in se.items()}})
            summary={name:{"coverage":float(np.mean([r["coverage"][name] for r in rows])),"mean_se":float(np.mean([r["se"][name] for r in rows]))} for name in spec["comparisons"]}
            results.append({"dates":t,"methods":summary,"records":rows}); print(json.dumps({"dates":t,"methods":summary}),flush=True)
    files=[path,Path(__file__),ROOT/"src/causalbank/responses.py"]
    (ROOT/"docs/studies/a-panel-results.json").write_text(json.dumps({"spec":spec,"results":results,"input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+"\n")


if __name__=="__main__": main()
