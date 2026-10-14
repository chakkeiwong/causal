#!/usr/bin/env python3
"""Bounded package operations and local sibling contract mappings; no sibling writes."""
import copy
import hashlib
import importlib.metadata as metadata
import inspect
import json
from pathlib import Path
import shutil
import sys

import duckdb
import jsonschema
import numpy as np
import polars as pl
import scipy
from scipy.optimize import minimize
from sklearn.linear_model import Lasso
import sklearn
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.organization import Candidate,materialize
from causalbank.scientific import MassKernel,finite_law,marginal,REGIMES,REQUIRED,lower_request,validate_result,scale_result


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_snapshots():
    destination=ROOT/"docs/literature/runtime"; destination.mkdir(exist_ok=True)
    output=[]
    for name,api in [("duckdb",duckdb.connect),("polars",pl.DataFrame.filter),("scikit-learn",Lasso.fit),("scipy",minimize),("numpy",np.linalg.solve)]:
        dist=metadata.distribution(name); artifacts=[]
        for path in dist.files or []:
            if path.name in {"METADATA","LICENSE","LICENSE.txt","LICENSE.md","LICENSE-3RD-PARTY.txt"} or "licenses/" in str(path):
                original=Path(dist.locate_file(path))
                if not original.is_file(): continue
                target=destination/(name+"-"+str(path).replace("/","_"))
                shutil.copyfile(original,target)
                artifacts.append({"path":str(target.relative_to(ROOT)),"sha256":sha(target),"original":str(original)})
        try:
            source=Path(inspect.getfile(api))
            target=destination/(name+"-api-"+source.name); shutil.copyfile(source,target)
            artifacts.append({"path":str(target.relative_to(ROOT)),"sha256":sha(target),"original":str(source)})
        except (TypeError,OSError): pass
        doc=destination/(name+"-api.txt")
        doc.write_text((getattr(api,"__doc__","") or "Compiled API; operation demonstrated by the executable probe.")+"\n")
        artifacts.append({"path":str(doc.relative_to(ROOT)),"sha256":sha(doc)})
        output.append({"distribution":name,"version":dist.version,"accessed":"2026-10-08","api":str(api.__module__)+"."+api.__name__,
                       "artifacts":artifacts,"scope":"Installed-operation feasibility on this host; distinct from the cutoff source/document snapshots"})
    return output


def sibling_snapshots():
    items=[("FinMarketing","src/finmarketing/estimators/causal/data.py",[27,173],
            "CausalData.from_record: strict preassignment features, mature outcomes, independent groups; dynamic curves require a separate payload, not scalar coercion."),
           ("FinMarketing","src/finmarketing/toolkit/contracts.py",[151,256],"FeatureSnapshot clocks and Estimate scalar/result boundary."),
           ("dataml","src/clearwater/core/lineage.py",[123,200],"LineageGraph.append records metadata, dataset, partition and assumptions; hash chaining is provenance, not scientific identification."),
           ("dataml","src/clearwater/overlay/schema.py",[16,78],"Correction confidence requires a numeric probability-like field; uncalibrated candidate scores cannot populate it."),
           ("BayesFilter","bayesfilter/ssm/contracts.py",[91,196],"SSMStaticShape, SSMDataSignature, BayesianSSMProblem: retain observation masks and coordinate semantics; causal action/logger/reward model remains additional manifest content."),
           ("MacroFinance","three_currency_measurement.py",[39,162],"DirectedPairMeasurement, ObservationContract and reverse_directed_pair_measurement preserve quoted pair direction and observed/derived roles."),
           ("MacroFinance","bayesfilter_macrofinance_migration_adapter.py",[1,167],"Facade pins existing import contract to /home/ubuntu/python/BayesFilter; do not infer runtime compatibility with the inspected workspace checkout.")]
    folder=ROOT/"docs/reviews/interface-snapshots"; folder.mkdir(exist_ok=True); output=[]
    for repo,name,lines,claim in items:
        original=Path("/home/ubuntu/workspace")/repo/name; destination=folder/(repo+"-"+name.replace("/","_"))
        shutil.copyfile(original,destination)
        output.append({"repository":repo,"source_path":str(original),"copy":str(destination.relative_to(ROOT)),"sha256":sha(destination),
                       "inspected_lines":lines,"supported_claim":claim,"version":"Working-tree bytes inspected 2026-10-08; no accepted integration or commit equivalence asserted"})
    return output


def run():
    checks={}; rng=np.random.default_rng(2026100861)
    # Same revision semantics in SQL, Polars and the small explicit reference.
    rows=[{"source":"s","entity":"a","record_id":"r","version":1,"event":2,"available":3,"value":8.,"currency":"USD"},
          {"source":"s","entity":"a","record_id":"r","version":2,"event":2,"available":10,"value":99.,"currency":"USD"},
          {"source":"s","entity":"a","record_id":"q","version":1,"event":4,"available":5,"value":3.,"currency":"USD"},
          {"source":"s","entity":"a","record_id":"q","version":2,"event":-5,"available":6,"value":7.,"currency":"USD"}]
    reference=materialize(rows,[{"decision_id":"d","entity":"a","at":10}],Candidate("event","available","latest_available","flow","account"),begin=0)[0]["value"]
    frame=pl.DataFrame(rows); conn=duckdb.connect(); conn.execute("SET threads=1")
    conn.register("events",frame.to_arrow())
    sql=conn.execute("WITH eligible AS (SELECT *, row_number() OVER (PARTITION BY source,entity,record_id ORDER BY version DESC) AS rn FROM events WHERE available < 10) SELECT sum(value) FROM eligible WHERE rn=1 AND event>=0 AND event<10").fetchone()[0]
    columnar=(frame.filter(pl.col("available")<10).sort("version").unique(subset=["source","entity","record_id"],keep="last")
              .filter((pl.col("event")>=0)&(pl.col("event")<10))["value"].sum())
    checks["duckdb_revision_window_against_reference"]=abs(sql-reference)<1e-12 and reference==8
    checks["polars_revision_window_against_reference"]=abs(columnar-reference)<1e-12
    # Orthogonal design has an independent closed-form Lasso soft threshold.
    q,_=np.linalg.qr(rng.normal(size=(80,5))); design=q*np.sqrt(80); truth=np.array([1.,-.5,0,.2,0]); penalty=.1
    fit=Lasso(alpha=penalty,fit_intercept=False,tol=1e-12).fit(design,design@truth)
    checks["sklearn_lasso_loss_normalization"]=np.max(abs(fit.coef_-np.sign(truth)*np.maximum(abs(truth)-penalty,0)))<1e-10
    fit=minimize(lambda v:(float(((v-[.3,-.4])**2).sum()),2*(v-[.3,-.4])),[1.,1.],jac=True,method="L-BFGS-B",bounds=[(-2,2)]*2)
    checks["scipy_bound_optimizer_value_score"]=fit.success and np.max(abs(fit.x-[.3,-.4]))<1e-10
    # A confounded binary SCM. Intervention replacement differs from conditioning.
    domains={"X":2,"A":2,"Y":2}
    kernels=[MassKernel(("X",),(),np.array([.5,.5])),MassKernel(("A",),("X",),np.array([[.8,.2],[.2,.8]])),
             MassKernel(("Y",),("X","A"),np.array([[[.9,.1],[.7,.3]],[[.5,.5],[.3,.7]]]))]
    law=finite_law(domains,kernels)
    do=finite_law(domains,kernels,{"A":MassKernel(("A",),(),np.array([0.,1.]))})
    checks["finite_kernel_product_marginal_intervention"]=abs(law.sum()-1)<1e-12 and abs(marginal(do,list(domains),["Y"])[1]-.5)<1e-12
    try: finite_law(domains,kernels,{"A":MassKernel(("A",),("Y",),np.array([[.5,.5],[.5,.5]]))})
    except ValueError: checks["future_policy_information_rejected"]=True
    else: checks["future_policy_information_rejected"]=False
    requests=[]
    for regime,(operation,sampling,_,_) in REGIMES.items():
        request={"version":"0.4","id":regime,"operation":operation,
          "variables":[{"name":"A","support":"real","unit":"pp","role":"action"},{"name":"Y","support":"real","unit":"USD","role":"outcome"},{"name":"Z","support":"real","unit":"index","role":"instrument"}],
          "model":{"regime":regime,"assumptions":sorted(REQUIRED[regime]),"hidden_states":2,"max_lag":1,"time_order":None},
          "observation":{"availability":"strict_before_decision","clock_unit":"month","step":1,"revision":"latest_eligible_before_event_filter","view_sha256":"0"*64},
          "population":{"unit":"customer" if sampling=="iid_trajectories" else "date","weight_role":"population","definition":"synthetic fixture"},
          "sampling":{"kind":sampling,"independent_unit":"customer" if sampling=="iid_trajectories" else "row" if sampling=="iid_rows" else None,"fold_unit":"trajectory" if sampling=="iid_trajectories" else "none"},
          "target":{"action":"A","outcomes":["Y"],"horizons":[0,1,2],"selection":"fixed","contrast":"specified policy or unit intervention","normalization":"one declared action unit"},
          "data":{"path":"fixture.npz","sha256":"0"*64}}
        if regime in {"B-H","B-L"}:
            request["variables"][0].update(support="binary",unit="assist")
            request["variables"][2].update(name="O",support="binary" if regime=="B-L" else "finite",unit="category",role="signal")
            request["target"]["horizons"]=[8]
            request["observation"]["clock_unit"]="decision"
        jsonschema.validate(request,json.loads((ROOT/"contracts/scientific/v04-request.schema.json").read_text()))
        checks["lower_"+regime]=lower_request(request)["status"]=="specified"; requests.append(request)
    result={"version":"0.4","request_id":"A-G","request_sha256":"0"*64,"kind":"response_curve",
       "axes":[{"name":"outcome","labels":["Y"]},{"name":"horizon","labels":[0,1]}],"units":["USD/pp"]*2,
       "estimate":[1.,2.],"covariance":[[1.,.3],[.3,2.]],"uncertainty":{"kind":"joint_confidence_set","level":.95,"coverage":"simultaneous","method":"fixture inversion","coordinate_sets":[[[None,-2.],[1.,None]],[[-1.,5.]]]},
       "graph":None,"numerical_error":[.001,.002],"scope":{"computation":"completed","identification":"conditional_functional","inference":"asymptotic_model_conditional","assumptions":["fixture"],"limitations":["schema example, not estimated data"]}}
    jsonschema.validate(result,json.loads((ROOT/"contracts/scientific/v04-result.schema.json").read_text())); validate_result(result)
    changed=scale_result(result,[-.01,-.01],["USD/bp_reversed"]*2)
    checks["sign_and_unit_transform_covariance_and_unbounded_sets"]=changed["uncertainty"]["coordinate_sets"][0]==[[None,-.01],[.02,None]] and abs(changed["covariance"][0][1]-.00003)<1e-12
    for defect in ("clock","weight","sampling","policy"):
        request=copy.deepcopy(requests[0])
        if defect=="clock": request["observation"]["availability"]="inclusive"
        elif defect=="weight": request["population"]["weight_role"]="propensity"
        elif defect=="sampling": request["sampling"]["kind"]="iid_rows"
        else: request["target"]["selection"]="learned"
        try: rejected=lower_request(request)["status"]=="unsupported"
        except ValueError: rejected=True
        checks["reject_"+defect]=rejected
    wrong=copy.deepcopy(result); wrong["uncertainty"]["coverage"]="pointwise"
    try: validate_result(wrong)
    except ValueError: checks["reject_pointwise_to_joint"]=True
    else: checks["reject_pointwise_to_joint"]=False
    runtime=runtime_snapshots(); siblings=sibling_snapshots()
    folder=ROOT/"contracts/scientific/v04-examples"; folder.mkdir(exist_ok=True)
    for request in requests: (folder/(request["id"]+"-request.json")).write_text(json.dumps(request,indent=2)+"\n")
    (folder/"curve-result.json").write_text(json.dumps(result,indent=2)+"\n")
    inputs=[Path(__file__),ROOT/"src/causalbank/scientific.py",ROOT/"src/causalbank/organization.py",ROOT/"contracts/scientific/v04-request.schema.json",ROOT/"contracts/scientific/v04-result.schema.json"]+list(folder.glob("*.json"))
    inputs+=[ROOT/a["path"] for row in runtime for a in row["artifacts"]]+[ROOT/r["copy"] for r in siblings]
    receipt={"status":"pass" if all(checks.values()) else "fail","checks":{k:bool(v) for k,v in checks.items()},"runtime":runtime,"sibling_inspections":siblings,
       "input_sha256":{str(p.relative_to(ROOT)):sha(p) for p in inputs},"scope":"Selected package operations and local protocol semantics; sibling snapshots inspected read-only, no sibling runtime/adoption claimed."}
    (ROOT/"docs/reviews/interface-qualification.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"status":receipt["status"],"checks":receipt["checks"],"versions":{r["distribution"]:r["version"] for r in runtime}},indent=2))
    return not all(checks.values())


if __name__=="__main__":
    with threadpool_limits(limits=1): raise SystemExit(run())
