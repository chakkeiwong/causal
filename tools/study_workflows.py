#!/usr/bin/env python3
"""Fresh-process complete synthetic workloads, including data reconstruction and inference."""
import argparse
import hashlib
import json
import os
import platform
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time

os.environ["POLARS_MAX_THREADS"]="1"

import duckdb
import numpy as np
import polars as pl
from scipy.stats import norm
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.responses import direct_response,proxy_var_response,moment_test_sets
from causalbank.temporal_discovery import fit_temporal_class
from causalbank.controlled import pack,simulate,fit,information_interval,contrast
from study_responses import generate
from study_response_extensions import learning_sample,learned_fit


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def io_counts():
    return {k:int(v.strip()) for k,v in (line.split(":") for line in Path("/proc/self/io").read_text().splitlines())}


def parquet_roundtrip(frame,path):
    frame.write_parquet(path)
    return pl.read_parquet(path)


def worker(spec,index,repeat,destination):
    config=spec["cases"][index]; rng=np.random.default_rng(np.random.SeedSequence([spec["seed"],index,repeat]))
    clock=time.perf_counter(); stages={}; begin_io=io_counts(); result={"case":config,"repeat":repeat,"failures":[]}
    def stage(name):
        nonlocal clock
        now=time.perf_counter(); stages[name]=now-clock; clock=now
    with tempfile.TemporaryDirectory(prefix="causal-workload-",dir="/tmp") as temp:
        path=Path(temp)/"raw.parquet"
        if config["kind"]=="response":
            scenario={"origins":config["dates"],"instrument_persistence":.85,"spectral_radius":.81,"strength":1.,"invalid_loading":0.}
            x,z,truth=generate(scenario,config["horizon"],rng); t=len(x); banks=config["entities"]
            deviations=rng.normal(scale=.5,size=(banks,t,2)); deviations-=deviations.mean(axis=0)
            values=x[None,:,1:]+deviations; base=np.arange(banks*t)
            # Three versions; v3 is never eligible at the historical release cutoff.
            frame=pl.DataFrame({"record_id":np.tile(base,3),"entity":np.tile(np.repeat(np.arange(banks),t),3),
                 "date":np.tile(np.tile(np.arange(t),banks),3),"version":np.repeat([1,2,3],banks*t),
                 "available":np.tile(np.tile(np.arange(t),banks),3)+np.repeat([.1,.5,2.],banks*t),
                 "deposit":np.r_[values[:,:,0].ravel()-.1,values[:,:,0].ravel(),values[:,:,0].ravel()+1],
                 "lending":np.r_[values[:,:,1].ravel()-.2,values[:,:,1].ravel(),values[:,:,1].ravel()+2]})
            frame.write_parquet(path); result["raw_records"]=frame.height; result["parquet_bytes"]=path.stat().st_size
            stage("generate_and_write_raw")
            conn=duckdb.connect(); conn.execute("SET threads=1")
            conn.read_parquet(str(path)).create_view("raw")
            reconstructed=conn.execute("WITH eligible AS (SELECT *, row_number() OVER (PARTITION BY record_id ORDER BY version DESC) rn FROM raw WHERE available<date+1) SELECT date, avg(deposit),avg(lending) FROM eligible WHERE rn=1 GROUP BY date ORDER BY date").fetchnumpy()
            columns=list(reconstructed.values()); fitted_x=np.column_stack((x[:,0],columns[1],columns[2]))
            result["reconstruction_max_error"]=float(np.max(abs(fitted_x-x))); stage("read_reconstruct_aggregate")
            direct=direct_response(fitted_x,z,config["horizon"]); proxy=proxy_var_response(fitted_x,z,config["horizon"])
            larger=direct_response(fitted_x,z,config["horizon"],bandwidth=4*direct.bandwidth)
            sets=moment_test_sets(direct.moment_mean,direct.moment_lrv,direct.origins)
            critical=norm.ppf(1-.05/(2*len(truth)))
            result.update(estimate=direct.estimate.tolist(),truth=truth.tolist(),
                mse_direct=float(np.mean((direct.estimate-truth)**2)),mse_proxy=float(np.mean((proxy.estimate-truth)**2)),
                whole_curve_covered=bool(np.all(abs(direct.estimate-truth)<=critical*np.sqrt(np.diag(direct.covariance)))),
                weak_sets=sets,bandwidth=direct.bandwidth,bandwidth_width_ratio=float(np.mean(np.sqrt(np.diag(larger.covariance)))/np.mean(np.sqrt(np.diag(direct.covariance)))))
            oracle=direct_response(x,z,config["horizon"])
            result["fit_max_reference_error"]=float(np.max(abs(direct.estimate-oracle.estimate)))
            stage("two_estimators_covariance_inversion_sensitivity_reference")
        elif config["kind"]=="learning":
            settings={**config,"sparse_penalty_multiplier":.1,"factor_rank":3}
            c,y,d,z,oracle=learning_sample(settings,rng); n=len(y)
            columns={"date":np.tile(np.arange(n),2),"version":np.repeat([1,2],n),"available":np.r_[np.arange(n)+.1,np.arange(n)+2.]}
            for j in range(c.shape[1]): columns["c"+str(j)]=np.r_[c[:,j],c[:,j]+1]
            for name,values in (("y",y),("d",d),("z",z)): columns[name]=np.tile(values,2)
            raw=parquet_roundtrip(pl.DataFrame(columns),path); result["raw_records"]=raw.height; result["parquet_bytes"]=path.stat().st_size
            view=raw.filter(pl.col("available")<pl.col("date")+1).sort("date")
            data=(view.select(["c"+str(j) for j in range(c.shape[1])]).to_numpy(),view["y"].to_numpy(),view["d"].to_numpy(),view["z"].to_numpy(),oracle)
            result["reconstruction_max_error"]=float(np.max(abs(data[0]-c))); stage("generate_write_read_reconstruct")
            result["methods"]={}
            for method in ("sparse","factor3","oracle"):
                theta,se=learned_fit(data,settings,method)
                result["methods"][method]={"estimate":float(theta),"se":float(se),"error":float(theta-1.2),"covered":bool(abs(theta-1.2)<=1.95996398454*se)}
            stage("blocked_fits_and_covariance")
        elif config["kind"]=="latent":
            model={"mu":np.array([.65,.35]),"emission":np.array([[.8,.2],[.2,.8]]),
                   "transition":np.array([[[.9,.1],[.2,.8]],[[.92,.08],[.48,.52]]]),"reward":np.array([[.85,.3],[.88,.48]])}
            data=simulate(model,config["trajectories"],config["horizon"],rng); n,h=data[0].shape
            raw=pl.DataFrame({"customer":np.repeat(np.arange(n),h),"date":np.tile(np.arange(h),n),
                             "signal":data[0].ravel(),"action":data[1].ravel(),"reward":data[2].ravel()})
            raw=parquet_roundtrip(raw,path).sort(["customer","date"])
            restored=tuple(raw[name].to_numpy().reshape(n,h).astype(int) for name in ("signal","action","reward"))
            result["raw_records"]=raw.height; result["parquet_bytes"]=path.stat().st_size
            result["reconstruction_max_error"]=float(max(np.max(abs(a-b)) for a,b in zip(restored,data))); stage("generate_write_read_trajectories")
            parameter,diagnostics=fit(restored,rng,starts=3,em_iterations=70,optimizer_iterations=180)
            interval=information_interval(parameter,restored,horizon=h)
            result["fit"]={"parameter":parameter,"diagnostics":diagnostics}; result["interval"]=interval
            result["estimate"]=contrast(parameter,horizon=h); result["truth"]=float(contrast(pack(model),horizon=h)); stage("multistart_fit_observed_information_value")
            bootstrap=[]
            for b in range(config["bootstrap"]):
                selected=rng.integers(0,n,n)
                refit,diagnostics=fit(tuple(a[selected] for a in restored),rng,starts=3,em_iterations=70,optimizer_iterations=180)
                bootstrap.append({"value":float(contrast(refit,horizon=h)),"diagnostics":diagnostics})
            result["bootstrap"]=bootstrap; stage("whole_trajectory_bootstrap_refits")
        else:
            n,p=config["dates"],config["variables"]
            f=.4*np.eye(p)+.15*np.eye(p,k=-1); x=np.zeros((n+300,p)); noise=rng.normal(size=x.shape)
            for t in range(1,len(x)): x[t]=f@x[t-1]+noise[t]
            raw=parquet_roundtrip(pl.DataFrame(x[300:],schema=["x"+str(j) for j in range(p)]),path)
            result["raw_records"]=raw.height; result["parquet_bytes"]=path.stat().st_size; stage("generate_write_read_series")
            fitted=fit_temporal_class(raw.to_numpy(),config["horizon"])
            bounds=np.asarray(fitted["response_bounds"]); truth=np.array([np.linalg.matrix_power(f,h) for h in range(config["horizon"]+1)])
            result["coefficient_max_error"]=float(np.max(abs(np.array(fitted["coefficient"])-f)))
            result["response_covered"]=bool(np.all(bounds[:,:,:,0]<=truth) and np.all(truth<=bounds[:,:,:,1]))
            result["mean_outer_width"]=float(np.mean(bounds[:,:,:,1]-bounds[:,:,:,0])); result["result"]=fitted
            stage("graph_box_and_response_propagation")
        result["raw_sha256"]=sha(path)
        if result.get("reconstruction_max_error",0)>1e-9 or result.get("fit_max_reference_error",0)>1e-9:
            raise ValueError("reconstruction/reference numerical tolerance failed")
        def plain(value):
            if isinstance(value,np.ndarray): return value.tolist()
            if isinstance(value,np.generic): return value.item()
            raise TypeError(type(value).__name__)
        destination.write_text(json.dumps(result,default=plain,indent=2)+"\n"); stage("serialize_report")
    end_io=io_counts()
    result.update(stages=stages,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
                  io_delta={k:end_io[k]-begin_io[k] for k in end_io},pid=os.getpid())
    destination.write_text(json.dumps(result,default=plain,indent=2)+"\n")


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--pilot",action="store_true"); parser.add_argument("--worker",type=int); parser.add_argument("--repeat",type=int,default=0); parser.add_argument("--output")
    args=parser.parse_args(); path=ROOT/"docs/studies/workflow-v1.json"; spec=json.loads(path.read_text())
    if args.worker is not None:
        with threadpool_limits(limits=spec["threads"]): worker(spec,args.worker,args.repeat,Path(args.output))
        return
    folder=ROOT/"docs/studies/workflow-runs"; folder.mkdir(exist_ok=True); results=[]
    for index,case in enumerate(spec["cases"]):
        if args.pilot and not case["id"].endswith("small"): continue
        for repeat in range(1 if args.pilot else spec["repeats"]):
            destination=folder/(("pilot-" if args.pilot else "")+case["id"]+"-"+str(repeat)+".json")
            start=time.perf_counter()
            process=subprocess.run([sys.executable,str(Path(__file__)),"--worker",str(index),"--repeat",str(repeat),"--output",str(destination)],cwd=ROOT,capture_output=True,text=True)
            row={"case":case["id"],"repeat":repeat,"process_seconds":time.perf_counter()-start,"exit_code":process.returncode}
            if process.returncode:
                row["error"]=process.stderr[-5000:]
            else:
                row.update(path=str(destination.relative_to(ROOT)),sha256=sha(destination))
            results.append(row); print(json.dumps(row),flush=True)
    files=[path,Path(__file__),ROOT/"tools/study_responses.py",ROOT/"tools/study_response_extensions.py"]+[ROOT/"src/causalbank"/name for name in ("responses.py","controlled.py","temporal_discovery.py","discovery_sets.py")]
    files+=[ROOT/r["path"] for r in results if "path" in r]
    receipt={"status":"pass" if all(r["exit_code"]==0 for r in results) else "fail","spec":spec,"results":results,
        "host":{"machine":platform.machine(),"logical_cpus":os.cpu_count(),"python":platform.python_version(),"cpu_model":next((r.split(":",1)[1].strip() for r in Path("/proc/cpuinfo").read_text().splitlines() if r.startswith("model name")),"unavailable"),"polars_threads":pl.thread_pool_size(),"blas_threads":1,"duckdb_threads":1,"versions":{"duckdb":duckdb.__version__,"polars":pl.__version__,"numpy":np.__version__}},
        "input_sha256":{str(p.relative_to(ROOT)):sha(p) for p in files},"scope":"Complete fresh-process synthetic workloads on one host; not bank scale acceptance, distributed throughput or repeated-sample coverage from three timings."}
    (ROOT/"docs/studies"/("workflow-pilot.json" if args.pilot else "workflow-results.json")).write_text(json.dumps(receipt,indent=2)+"\n")


if __name__=="__main__": main()
