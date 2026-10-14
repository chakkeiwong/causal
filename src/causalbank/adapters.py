"""Local mappings of inspected sibling contracts; no sibling import or writes."""
from datetime import datetime
import hashlib
import json
import numpy as np


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def instant(value):
    out=datetime.fromisoformat(value.replace("Z","+00:00"))
    if out.tzinfo is None: raise ValueError("timezone required")
    return out


def finmarketing_snapshot(snapshot):
    """FeatureSnapshot fields -> observation descriptor, retaining sequence ties."""
    available=(instant(snapshot["max_available_at"]),snapshot["max_available_sequence"])
    cutoff=(instant(snapshot["cutoff"]),snapshot["cutoff_sequence"])
    decision=(instant(snapshot["decision_at"]),snapshot["decision_sequence"])
    if not available<=cutoff<decision: raise ValueError("information not available before decision")
    if set(snapshot["feature_names"])&set(snapshot["outcome_names"]): raise ValueError("outcome included as feature")
    return {"snapshot_id":snapshot["snapshot_id"],"view_sha256":snapshot["content_sha256"],
            "population_unit":snapshot["entity_type"],"sampling_unit":snapshot["dependence_unit"],
            "clock":{"order":"timestamp_then_sequence","availability":"strict_before_decision","decision":[snapshot["decision_at"],snapshot["decision_sequence"]]},
            "horizon_days":snapshot["label_horizon_days"],"permission_id":snapshot["permission_id"],
            "scope":"Observation mapping; causal assumptions and curve/policy result import need separate contracts"}


def dataml_lineage_payload(organization,*,run_id,dataset,partition,assumption_ids):
    if not assumption_ids: raise ValueError("candidate constraints require resolvable assumption references")
    return {"run_id":run_id,"component":"causal.observation_candidates","dataset":dataset,"partition":partition,
            "metadata":{"schema":"causal-observation.v1","status":organization["status"],"assumption_ids":assumption_ids,
                        "candidate_views":[{"view_sha256":c["view_sha256"],"interpretation":c["candidate"],"inspection_score":c["evidence_score"]} for c in organization["survivors"]],
                        "correction_proposed":False,"reason":"Ranking scores have no calibrated confidence interpretation"}}


def bayesfilter_problem(signal,action,reward,*,model_id):
    if signal.ndim!=2 or any(x.shape!=signal.shape for x in (action,reward)):
        raise ValueError("complete equally shaped trajectories required")
    n,h=signal.shape
    manifest={"model_id":model_id,"state_space":{"kind":"finite","cardinality":2},
              "logger":"exogenous_randomized","action_hash":digest(action.tolist()),
              "clock":"signal_then_action_then_reward_then_transition","reward":"100*repayment-12*assist",
              "parameterization":"11 Bernoulli logits","likelihood":"conditional on randomized actions",
              "policy_information":"observed history only"}
    manifest["model_hash"]=digest(manifest)
    observed=np.stack((signal,reward),axis=-1).transpose(1,0,2)
    return {"problem_id":model_id,"static_shape":{"horizon":h,"state_dim":1,"observation_dim":2,"innovation_dim":1,"parameter_dim":11},
            "data_signature":{"dataset_id":"causal-controlled-trajectories","observation_shape":list(observed.shape),"mask_shape":None,"data_hash":digest(observed.tolist())},
            "target_coordinate_convention":"unconstrained","model_manifest":manifest},observed


def macrofinance_measurement(payload,*,rate_scale=1.):
    if payload["source"]==payload["target"] or payload["maturity"]<=0 or not np.isfinite(rate_scale) or rate_scale<=0:
        raise ValueError("directed pair, positive maturity and fixed rate scaling required")
    if not np.allclose(payload["market_residual"],-np.asarray(payload["chi"]),atol=1e-12,rtol=0):
        raise ValueError("MacroFinance residual convention x_m=-chi violated")
    return {"pair":[payload["source"],payload["target"]],"maturity_years":payload["maturity"],
            "rho":(np.asarray(payload["rho"])*rate_scale).tolist(),"chi":(np.asarray(payload["chi"])*rate_scale).tolist(),
            "observed_role":"supplied_measurement","causal_role":"requires separate identification model"}
