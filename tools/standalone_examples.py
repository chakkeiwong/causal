#!/usr/bin/env python3
"""Produce executable requests/results and test the local sibling mappings."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
from threadpoolctl import threadpool_limits
from causal_study import execute
from study_responses import generate
from study_response_extensions import integrated_sample
from revision_studies import coll_sim
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.controlled import simulate
from causalbank.scientific import REGIMES,REQUIRED
from causalbank.adapters import finmarketing_snapshot,dataml_lineage_payload,bayesfilter_problem,macrofinance_measurement


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folder=ROOT/"docs/studies/standalone"; folder.mkdir(exist_ok=True); checks={}; rng=np.random.default_rng(2026100881)
    for regime,(operation,sampling,_,_) in REGIMES.items():
        columns=["A","Y","W"]; horizon=4; policies={}; family="reference"
        variables=[{"name":k,"support":"real","unit":"pp" if k=="A" else "USD","role":"action" if k=="A" else "outcome"} for k in columns]
        if regime in {"A-G","A-I"}:
            settings={"origins":500,"horizon":horizon,"instrument_persistence":.4,"spectral_radius":.6,"strength":1.,"invalid_loading":0.}
            x,z,_=(generate(settings,horizon,rng) if regime=="A-G" else integrated_sample(settings,rng))
            data={"x":x,"z":z}; variables.append({"name":"Z","support":"real","unit":"index","role":"instrument"}); contrast="external_shock_response"; normalization="one_unit_impact"
        elif regime=="C-G":
            columns=["X","A","Y"]; variables=[{"name":k,"support":"real","unit":"index","role":"action" if k=="A" else "outcome" if k=="Y" else "control"} for k in columns]
            b=np.array([[0.,0,0],[.8,0,0],[0,.7,0]]); data={"x":rng.normal(size=(600,3))@np.linalg.inv(np.eye(3)-b).T}
            contrast="unit_intervention_derivative"; normalization="one_unit"; horizon=0
        elif regime=="C-T":
            f=np.array([[.4,0,0],[.2,.3,0],[0,.2,.4]]); x=np.zeros((800,3)); noise=rng.normal(size=x.shape)
            for t in range(1,len(x)): x[t]=f@x[t-1]+noise[t]
            data={"x":x[300:]}; contrast="additive_state_intervention"; normalization="one_unit"
        else:
            horizon=8; contrast="fixed_policy_value_difference"; normalization="USD_discount_0.99"
            variables=[{"name":"A","support":"binary","unit":"assist","role":"action"},{"name":"Y","support":"real","unit":"USD","role":"outcome"},{"name":"O","support":"binary" if regime=="B-L" else "finite","unit":"state_category","role":"signal"}]
            if regime=="B-H":
                s,a,r=coll_sim(rng,1000); data={"state":s,"action":a,"reward":r}; family="servicing_three_state_v1"
                policies={"reference_policy":[0,.2,.4],"evaluation_policy":[0,.5,.8]}
            else:
                model={"mu":np.array([.65,.35]),"emission":np.array([[.8,.2],[.2,.8]]),"transition":np.array([[[.9,.1],[.2,.8]],[[.92,.08],[.48,.52]]]),"reward":np.array([[.85,.3],[.88,.48]])}
                o,a,r=simulate(model,800,8,rng); data={"signal":o,"action":a,"reward":r}; family="binary_repayment_v1"
                policies={"reference_policy":[0,0],"evaluation_policy":[0,1]}
                problem,observed=bayesfilter_problem(o,a,r,model_id="causal-binary-repayment")
                checks["BayesFilter_time_first_observation_and_action_identity"]=observed.shape==(8,800,2) and problem["model_manifest"]["logger"]=="exogenous_randomized"
                (folder/"BayesFilter-problem.json").write_text(json.dumps(problem,indent=2)+"\n")
        path=folder/(regime+"-data.npz"); np.savez(path,**data)
        request={"version":"0.4","id":regime+"-standalone","operation":operation,"variables":variables,
            "model":{"regime":regime,"assumptions":sorted(REQUIRED[regime]),"family":family,"hidden_states":2,"max_lag":1,"time_order":None},
            "observation":{"availability":"strict_before_decision","clock_unit":"decision" if sampling=="iid_trajectories" else "month","step":1,"revision":"latest_eligible_before_event_filter","view_sha256":sha(path)},
            "population":{"unit":"customer" if sampling=="iid_trajectories" else "date","weight_role":"population","definition":"frozen synthetic fixture"},
            "sampling":{"kind":sampling,"independent_unit":"customer" if sampling=="iid_trajectories" else "row" if sampling=="iid_rows" else None,"fold_unit":"trajectory" if sampling=="iid_trajectories" else "none"},
            "target":{"action":"A","outcomes":["Y"],"horizons":[8] if sampling=="iid_trajectories" else list(range(horizon+1)),"selection":"fixed","contrast":contrast,"normalization":normalization,**policies},
            "data":{"path":str(path.relative_to(ROOT)),"sha256":sha(path),"columns":columns}}
        req=folder/(regime+"-request.json"); req.write_text(json.dumps(request,indent=2)+"\n")
        result,diagnostics=execute(request,data,sha(req))
        (folder/(regime+"-result.json")).write_text(json.dumps(result,indent=2)+"\n")
        (folder/(regime+"-diagnostics.json")).write_text(json.dumps(diagnostics,indent=2)+"\n")
        checks["execute_"+regime]=result["scope"]["computation"]=="completed"
    command=[sys.executable,str(ROOT/"tools/causal_study.py"),str(folder/"A-G-request.json"),"--output",str(folder/"A-G-cli-result.json")]
    process=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
    checks["standalone_cli_parity"]=process.returncode==0 and json.loads((folder/"A-G-cli-result.json").read_text())==json.loads((folder/"A-G-result.json").read_text())
    snapshot={"snapshot_id":"fixture","content_sha256":"a"*64,"entity_type":"customer","dependence_unit":"household","feature_names":["balance"],"outcome_names":["profit"],"max_available_at":"2026-01-01T00:00:00Z","max_available_sequence":0,"cutoff":"2026-01-01T00:00:00Z","cutoff_sequence":0,"decision_at":"2026-01-01T00:00:00Z","decision_sequence":1,"label_horizon_days":30,"permission_id":"synthetic-local"}
    mapped=finmarketing_snapshot(snapshot); checks["FinMarketing_sequence_and_group_preserved"]=mapped["sampling_unit"]=="household" and mapped["horizon_days"]==30
    late=copy.deepcopy(snapshot); late["max_available_sequence"]=1
    try: finmarketing_snapshot(late)
    except ValueError: checks["FinMarketing_late_feature_rejected"]=True
    else: checks["FinMarketing_late_feature_rejected"]=False
    payload=dataml_lineage_payload({"status":"abstain","survivors":[]},run_id="example",dataset="synthetic",partition="one",assumption_ids=["finite-grammar-v1"])
    checks["dataml_abstention_is_lineage_not_confident_correction"]=not payload["metadata"]["correction_proposed"] and "confidence" not in payload["metadata"]
    measurement={"source":"USD","target":"EUR","maturity":1.,"rho":.01,"chi":.002,"market_residual":-.002}
    checks["MacroFinance_quote_units_and_sign"]=macrofinance_measurement(measurement,rate_scale=10000)["chi"]==20
    for name,payload in (("FinMarketing-observation",mapped),("dataml-lineage",payload),("MacroFinance-observation",macrofinance_measurement(measurement))):
        (folder/(name+".json")).write_text(json.dumps(payload,indent=2)+"\n")
    inputs=[Path(__file__),ROOT/"tools/causal_study.py",ROOT/"tools/study_longitudinal.py",ROOT/"tools/revision_studies.py",ROOT/"tools/study_responses.py",ROOT/"tools/study_response_extensions.py"]+list((ROOT/"src/causalbank").glob("*.py"))+list(folder.iterdir())
    receipt={"status":"pass" if all(checks.values()) else "fail","checks":{k:bool(v) for k,v in checks.items()},"input_sha256":{str(p.relative_to(ROOT)):sha(p) for p in inputs},"scope":"Executed local reference requests and mappings from inspected sibling contracts; no sibling code execution or accepted adoption."}
    (ROOT/"docs/reviews/standalone-qualification.json").write_text(json.dumps(receipt,indent=2)+"\n"); print(json.dumps({"status":receipt["status"],"checks":receipt["checks"]},indent=2))
    return not all(checks.values())


if __name__=="__main__":
    with threadpool_limits(limits=1): raise SystemExit(main())
