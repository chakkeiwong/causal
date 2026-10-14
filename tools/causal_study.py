#!/usr/bin/env python3
"""Standalone bounded scientific study runner. No external writes or bank services."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import jsonschema
import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.scientific import lower_request,validate_result
from causalbank.responses import direct_response,level_response_from_changes,moment_test_sets
from causalbank.discovery_sets import confidence_effects
from causalbank.temporal_discovery import fit_temporal_class
from causalbank.controlled import fit,contrast,information_interval
from study_longitudinal import crossfit
from revision_studies import REWARD_COLL


def execute(request,data,request_sha):
    jsonschema.validate(request,json.loads((ROOT/"contracts/scientific/v04-request.schema.json").read_text()))
    plan=lower_request(request)
    if plan["status"]!="specified": raise ValueError(plan)
    regime=request["model"]["regime"]; target=request["target"]; horizon=max(target["horizons"])
    result={"version":"0.4","request_id":request["id"],"request_sha256":request_sha,
       "kind":"scalar_effect","axes":[{"name":"target","labels":["contrast"]}],"units":["USD"],
       "estimate":None,"covariance":None,"uncertainty":None,"graph":None,"numerical_error":None,
       "scope":{"computation":"completed","identification":"conditional_functional","inference":"asymptotic_model_conditional",
                "assumptions":plan["assumptions"],"limitations":["Research reference; synthetic qualification only","No certified numerical error bound"]}}
    diagnostics={"plan":plan}
    variable={v["name"]:v for v in request["variables"]}
    if regime in {"A-G","A-I","C-G","C-T"}:
        columns=request["data"].get("columns",[])
        x=data["x"]
        if x.ndim!=2 or x.shape[1]!=len(columns) or len(set(columns))!=len(columns) or not np.all(np.isfinite(x)):
            raise ValueError("finite x array and exact column layout required")
        if not set(columns)<=set(variable): raise ValueError("unknown data columns")
    if regime in {"A-G","A-I"}:
        if target["action"]!=columns[0] or target["normalization"]!="one_unit_impact" or target["contrast"]!="external_shock_response":
            raise ValueError("first x column must be the impact-normalized action; exact shock-response target required")
        if target["horizons"]!=list(range(horizon+1)):
            raise ValueError("reference requires the complete fixed horizon grid")
        outcomes=tuple(columns.index(v) for v in target["outcomes"])
        fitted=(direct_response if regime=="A-G" else level_response_from_changes)(x,data["z"],horizon,outcomes)
        result.update(kind="response_curve",axes=[{"name":"outcome","labels":target["outcomes"]},{"name":"horizon","labels":target["horizons"]}],
             units=[variable[v]["unit"]+"/"+variable[target["action"]]["unit"] for v in target["outcomes"] for h in target["horizons"]],
             estimate=fitted.estimate.tolist(),covariance=fitted.covariance.tolist())
        sets=moment_test_sets(fitted.moment_mean,fitted.moment_lrv,fitted.origins)
        diagnostics.update(origins=fitted.origins,bandwidth=fitted.bandwidth,denominator=fitted.denominator)
        result["uncertainty"]={"kind":"joint_confidence_set","level":.95,"coverage":"simultaneous","method":"Bonferroni HAC residual-test inversion","coordinate_sets":sets}
        result["scope"]["limitations"].append("Finite-sample undercoverage under persistence remains in the study record; fixed stability/rate assumptions required")
    elif regime=="C-G":
        if len(columns)!=3 or target["action"]!=columns[1] or target["outcomes"]!=[columns[2]] or target["contrast"]!="unit_intervention_derivative":
            raise ValueError("reference graph query is columns[1] to columns[2]")
        fitted=confidence_effects(x,request["model"].get("time_order"))
        result.update(kind="effect_outer_set",units=[variable[columns[2]]["unit"]+"/"+variable[columns[1]]["unit"]],
             graph={"kind":"DAG_set","nodes":columns,"marks":["tail","arrow"],"models":[r["graph"] for r in fitted["retained_models"]]})
        result["uncertainty"]={"kind":"joint_confidence_set","level":.95,"coverage":"simultaneous","method":"Gaussian covariance region outer image","coordinate_sets":[fitted["effect_intervals"]]}
        result["scope"].update(identification="conditional_model_set",inference="exact_model_conditional")
        result["scope"]["limitations"].append(fitted["scope"]); diagnostics["covariance_region"]=fitted["covariance_region"]
    elif regime=="C-T":
        if target["contrast"]!="additive_state_intervention" or target["horizons"]!=list(range(horizon+1)):
            raise ValueError("fixed-grid additive state intervention required")
        fitted=fit_temporal_class(x,horizon); a=columns.index(target["action"]); outcomes=[columns.index(v) for v in target["outcomes"]]
        bounds=np.asarray(fitted["response_bounds"]); coefficient=np.asarray(fitted["coefficient"])
        estimates=[float(np.linalg.matrix_power(coefficient,h)[i,a]) for i in outcomes for h in range(horizon+1)]
        sets=[[bounds[h,i,a,:].tolist()] for i in outcomes for h in range(horizon+1)]; box=np.array(fitted["coefficient_bounds"])
        result.update(kind="graph_response_set",axes=[{"name":"outcome","labels":target["outcomes"]},{"name":"horizon","labels":target["horizons"]}],
          units=[variable[v]["unit"]+"/"+variable[target["action"]]["unit"] for v in target["outcomes"] for h in target["horizons"]],estimate=estimates,
          graph={"kind":"temporal_coefficient_box","nodes":columns,"marks":sum(fitted["edge_marks"],[]),"models":[box[:,:,0].tolist(),box[:,:,1].tolist()]})
        result["uncertainty"]={"kind":"joint_confidence_set","level":.95,"coverage":"simultaneous","method":"VAR1 joint coefficient-box image","coordinate_sets":sets}
    else:
        if target["normalization"]!="USD_discount_0.99" or target["contrast"]!="fixed_policy_value_difference":
            raise ValueError("the reference servicing families require their USD discounted reward target")
        if regime=="B-L":
            if request["model"].get("family")!="binary_repayment_v1" or target.get("reference_policy")!=[0,0] or target.get("evaluation_policy")!=[0,1]:
                raise ValueError("binary repayment reference supports the declared fixed never/reactive policy contrast")
            observed=tuple(data[k] for k in ("signal","action","reward"))
            if any(a.shape!=observed[0].shape or a.ndim!=2 or not np.all(np.isin(a,[0,1])) for a in observed) or observed[0].shape[1]<3:
                raise ValueError("complete binary trajectories of length at least three required")
            parameter,diagnostics["fit"]=fit(observed,20261008)
            diagnostics["information"]=information_interval(parameter,observed,horizon=horizon)
            estimate=contrast(parameter,horizon=horizon); se=diagnostics["information"]["se"]
            if not diagnostics["fit"]["optimizer_success"] or diagnostics["fit"]["on_boundary"]:
                se=None
        else:
            if request["model"].get("family")!="servicing_three_state_v1" or horizon!=8:
                raise ValueError("observed-history implementation supports the eight-decision servicing reference")
            observed=tuple(data[k] for k in ("state","action","reward"))
            s,a,r=observed
            if a.ndim!=2 or a.shape[1]!=8 or s.shape!=(len(a),9) or r.shape!=a.shape or not np.all(np.isin(s,[0,1,2])) or not np.all(np.isin(a,[0,1])):
                raise ValueError("invalid three-state complete trajectories")
            if np.any(a[s[:,:-1]==0]) or not np.allclose(r,REWARD_COLL[s[:,1:].astype(int)]-12*a):
                raise ValueError("infeasible action or different servicing reward law")
            policies=[np.asarray(target[k]) for k in ("reference_policy","evaluation_policy")]
            if any(p.shape!=(3,) or p[0]!=0 for p in policies): raise ValueError("three-state feasible fixed policies required")
            scores,diagnostics["fit"]=crossfit(observed,policies)
            contrast_scores=scores["augmented"][:,1]-scores["augmented"][:,0]
            estimate=float(contrast_scores.mean()); se=float(contrast_scores.std(ddof=1)/np.sqrt(len(contrast_scores)))
        result.update(kind="policy_value_contrast",estimate=[estimate],covariance=None if se is None else [[se*se]])
        if se is not None:
            result["uncertainty"]={"kind":"joint_confidence_set","level":.95,"coverage":"simultaneous","method":plan["inference"],"coordinate_sets":[[[estimate-norm.ppf(.975)*se,estimate+norm.ppf(.975)*se]]]}
        else: result["scope"]["inference"]="unavailable"
    validate_result(result); jsonschema.validate(result,json.loads((ROOT/"contracts/scientific/v04-result.schema.json").read_text()))
    return result,diagnostics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("request",type=Path); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args()
    raw=args.request.read_bytes(); request=json.loads(raw); data_path=ROOT/request["data"]["path"]
    if hashlib.sha256(data_path.read_bytes()).hexdigest()!=request["data"]["sha256"]: raise ValueError("data identity mismatch")
    with np.load(data_path,allow_pickle=False) as data,threadpool_limits(limits=1):
        result,diagnostics=execute(request,data,hashlib.sha256(raw).hexdigest())
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    args.output.with_suffix(".diagnostics.json").write_text(json.dumps(diagnostics,indent=2)+"\n")
    print(json.dumps({"result":str(args.output),"scope":result["scope"]}))


if __name__=="__main__": main()
