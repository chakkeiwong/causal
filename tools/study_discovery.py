#!/usr/bin/env python3
"""Finite graph/effect confidence reference with exact covariance coverage."""
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.discovery_sets import confidence_effects,population_effects


def contains(intervals,value):
    return any((lo is None or lo<=value) and (hi is None or value<=hi) for lo,hi in intervals)


def main():
    path=ROOT/"docs/studies/c-experiment-v1.json"; spec=json.loads(path.read_text()); results=[]
    with threadpool_limits(limits=1):
        for ci,case in enumerate(spec["cases"]):
            b=np.array([[0,0,0],[.8,0,0],[0,.7,0.]])
            if case["id"]=="near_unfaithful":
                b[2,0]=-.8*.7+.01
            inverse=np.linalg.inv(np.eye(3)-b)
            covariance=inverse@inverse.T; truth=.7
            if case["id"]=="hidden_common_cause":
                covariance=np.array([[1.,0,0],[0,2.,.8],[0,.8,1.64]])
                truth=0.
            rows=[]; start=time.perf_counter()
            for rep in range(spec["repetitions"]):
                rng=np.random.default_rng(np.random.SeedSequence([spec["seed"],ci,rep]))
                data=rng.multivariate_normal(np.zeros(3),covariance,size=spec["observations"])
                result=confidence_effects(data,case["order"],spec["alpha"])
                intervals=result["effect_intervals"]
                region=result["covariance_region"]
                region_covers=all(lo<=np.asarray(v)@covariance@np.asarray(v)<=hi for v,(lo,hi) in zip(region["directions"],region["variance_bounds"]))
                rows.append({"coverage":contains(intervals,truth),"covariance_region_coverage":region_covers,
                             "zero_retained":contains(intervals,0),"positive_retained":contains(intervals,.7),
                             "models":len(result["retained_models"]),"width":None if any(lo is None or hi is None for lo,hi in intervals) else sum(hi-lo for lo,hi in intervals)})
                if rep==0:
                    example=result
            coverage=float(np.mean([r["coverage"] for r in rows]))
            widths=[np.inf if r["width"] is None else r["width"] for r in rows]
            result={"case":case,"truth":truth,"population_compatible_effects":population_effects(covariance,case["order"]),
                    "coverage":coverage,"mc_se":float(np.sqrt(coverage*(1-coverage)/spec["repetitions"])),
                    "covariance_region_coverage":float(np.mean([r["covariance_region_coverage"] for r in rows])),
                    "both_zero_positive_fraction":float(np.mean([r["zero_retained"] and r["positive_retained"] for r in rows])),
                    "median_models":float(np.median([r["models"] for r in rows])),"median_width":float(np.median(widths)) if np.isfinite(np.median(widths)) else None,
                    "unbounded_fraction":float(np.mean(np.isinf(widths))),"seconds":time.perf_counter()-start,
                    "example":example,"records":rows}
            results.append(result)
            print(json.dumps({k:v for k,v in result.items() if k not in ("records","example")}),flush=True)
    files=[path,Path(__file__),ROOT/"src/causalbank/discovery_sets.py"]
    (ROOT/"docs/studies/c-results.json").write_text(json.dumps({"spec":spec,
        "input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},"results":results},indent=2)+"\n")


if __name__=="__main__":
    main()
