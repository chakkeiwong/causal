#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.temporal_discovery import fit_temporal_class


def main():
    path=ROOT/"docs/studies/c-temporal-experiment-v1.json"; spec=json.loads(path.read_text()); results=[]
    with threadpool_limits(limits=1):
        for ci,case in enumerate(spec["cases"]):
            f=np.array([[.45,0,0],[.25,.35,0],[0,.3,.4]])
            g=np.zeros((3,3));
            if case=="omitted_lag_two":
                g[2,0]=.45; g[1,1]=.25
            truth=[np.eye(3)]
            for h in range(1,spec["horizon"]+1):
                truth.append(f@truth[-1]+(g@truth[-2] if h>1 else 0))
            covered=[]; edge=[]; start=time.perf_counter()
            for rep in range(spec["repetitions"]):
                rng=np.random.default_rng(np.random.SeedSequence([spec["seed"],ci,rep]))
                state=np.zeros((spec["dates"]+300,3)); noise=rng.normal(size=state.shape)
                for t in range(2,len(state)):
                    state[t]=f@state[t-1]+g@state[t-2]+noise[t]
                fitted=fit_temporal_class(state[300:],spec["horizon"])
                box=np.asarray(fitted["response_bounds"])
                covered.append(bool(np.all((box[:,:,:,0]<=truth)&(np.asarray(truth)<=box[:,:,:,1]))))
                coef=np.asarray(fitted["coefficient_bounds"])
                edge.append(bool(np.all((coef[:,:,0]<=f)&(f<=coef[:,:,1]))))
            coverage=float(np.mean(covered))
            result={"case":case,"response_coverage":coverage,"mc_se":float(np.sqrt(coverage*(1-coverage)/spec["repetitions"])),
                    "coefficient_coverage":float(np.mean(edge)),"seconds":time.perf_counter()-start}
            results.append(result); print(json.dumps(result),flush=True)
    files=[path,Path(__file__),ROOT/"src/causalbank/temporal_discovery.py",ROOT/"src/causalbank/discovery_sets.py"]
    (ROOT/"docs/studies/c-temporal-results.json").write_text(json.dumps({"spec":spec,"results":results,
        "input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+"\n")


if __name__=="__main__":
    main()
