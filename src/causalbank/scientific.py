"""Executable semantics for a bounded scientific protocol, version 0.4.

Semantic validation is separate from JSON syntax. It checks compatibility of
declarations, not truth of causal assumptions. Finite mass kernels provide a
small expression reference; continuous integration/automatic ID is not here.
"""
from dataclasses import dataclass
from itertools import product
import numpy as np


@dataclass(frozen=True)
class MassKernel:
    children: tuple
    parents: tuple
    values: np.ndarray

    def validate(self,domains):
        names=self.parents+self.children
        if not self.children or len(set(names))!=len(names) or any(k not in domains for k in names):
            raise ValueError("distinct declared kernel arguments required")
        if self.values.shape!=tuple(domains[k] for k in names) or not np.all(np.isfinite(self.values)):
            raise ValueError("kernel support/shape mismatch")
        if np.any(self.values<0) or not np.allclose(self.values.sum(axis=tuple(range(len(self.parents),len(names)))),1,atol=1e-12,rtol=0):
            raise ValueError("nonnegative normalized probability mass required")


def finite_law(domains,kernels,replacements=None):
    """Product/sum/substitution reference for ordered finite generative kernels.

    Replacing an action kernel evaluates a supplied SCM/policy factorization;
    it does not establish its identification from observational data.
    """
    replacements=replacements or {}; seen=set(); ordered=[]
    if set(replacements)-set(domains):
        raise ValueError("unknown intervention variable")
    for kernel in kernels:
        if len(kernel.children)!=1:
            raise ValueError("one child per mechanism in this bounded grammar")
        child=kernel.children[0]
        active=replacements.get(child,kernel); active.validate(domains)
        if active.children!=(child,) or child in seen or not set(active.parents)<=seen:
            raise ValueError("cyclic, duplicated or noncausal policy information")
        seen.add(child); ordered.append(active)
    if seen!=set(domains):
        raise ValueError("one mechanism per variable required")
    names=list(domains); probability=np.zeros(tuple(domains[k] for k in names))
    for values in product(*(range(domains[k]) for k in names)):
        assignment=dict(zip(names,values)); mass=1.
        for kernel in ordered:
            mass*=kernel.values[tuple(assignment[k] for k in kernel.parents+kernel.children)]
        probability[values]=mass
    return probability


def marginal(law,names,keep):
    if len(set(keep))!=len(keep) or not set(keep)<=set(names):
        raise ValueError("invalid marginal arguments")
    result=law.sum(axis=tuple(i for i,k in enumerate(names) if k not in keep))
    surviving=[k for k in names if k in keep]
    return np.transpose(result,[surviving.index(k) for k in keep])


REGIMES={
    "A-G":("dynamic_response","time_series","direct_moments","joint_bartlett_and_residual_test_sets"),
    "A-I":("dynamic_response","time_series","stationary_changes_cumulative","joint_bartlett_and_residual_test_sets"),
    "B-H":("history_value","iid_trajectories","crossfit_augmented","trajectory_contrast_score"),
    "B-L":("latent_value","iid_trajectories","em_likelihood_refinement","observed_information_fixed_policy"),
    "C-G":("graph_effect","iid_rows","gaussian_covariance_region","outer_effect_union"),
    "C-T":("temporal_graph_effect","time_series","var1_ols","joint_coefficient_box_image")}

REQUIRED={
    "A-G":{"stable_gaussian_linear_law","external_instrument_exclusion","nonzero_impact"},
    "A-I":{"stationary_gaussian_changes","external_instrument_exclusion","nonzero_impact"},
    "B-H":{"sequential_exchangeability","consistency","policy_support","observed_state_sufficient"},
    "B-L":{"randomized_exogenous_logging","invariant_invertible_emission","invertible_baseline_transition","independent_reward_emission","regular_interior_information"},
    "C-G":{"causal_sufficiency","linear_gaussian_acyclic","positive_definite_covariance"},
    "C-T":{"stable_gaussian_var1","no_contemporaneous_edges","independent_innovations","correct_lag_bound"}}


def lower_request(request):
    regime=request["model"]["regime"]
    if regime not in REGIMES:
        return {"status":"unsupported","reason":"No qualified lowering for this regime"}
    operation,sampling,estimator,inference=REGIMES[regime]
    if request["operation"]!=operation or request["sampling"]["kind"]!=sampling:
        raise ValueError("operation/model/sampling mismatch")
    if request["observation"]["availability"]!="strict_before_decision":
        raise ValueError("clock conversion requires a new observation construction")
    if request["population"]["weight_role"]!="population":
        raise ValueError("population weights cannot be replaced by propensity or resampling weights")
    if sampling=="iid_trajectories" and (request["sampling"]["independent_unit"]!=request["population"]["unit"] or request["sampling"]["fold_unit"]!="trajectory"):
        raise ValueError("whole independent trajectories must define sampling/folds")
    if sampling=="time_series" and request["sampling"]["independent_unit"] is not None:
        raise ValueError("dates are not declared independent in a dependent-series experiment")
    if len({v["name"] for v in request["variables"]})!=len(request["variables"]):
        raise ValueError("duplicate variables")
    names={v["name"] for v in request["variables"]}
    if not set(request["target"]["outcomes"])<=names or request["target"]["action"] not in names:
        raise ValueError("undeclared target variables")
    lookup={v["name"]:v for v in request["variables"]}
    if lookup[request["target"]["action"]]["role"]!="action":
        raise ValueError("target action must have an action role")
    if regime in {"B-H","B-L"} and lookup[request["target"]["action"]]["support"]!="binary":
        raise ValueError("finite sequential reference requires binary actions")
    if regime=="B-L" and not any(v["role"]=="signal" and v["support"]=="binary" for v in request["variables"]):
        raise ValueError("controlled identification requires its binary signal")
    if regime in {"A-G","A-I"} and not any(v["role"]=="instrument" for v in request["variables"]):
        raise ValueError("external instrument must be a distinct declared variable")
    if request["target"]["selection"]!="fixed":
        return {"status":"unsupported","reason":"Learned policy/selected horizons require their own evaluation design"}
    missing=REQUIRED[regime]-set(request["model"]["assumptions"])
    if missing:
        return {"status":"unsupported","reason":"Missing model premises", "missing":sorted(missing)}
    if regime=="B-L" and request["model"].get("hidden_states")!=2:
        return {"status":"unsupported","reason":"Unknown-emission identification reference supports two states"}
    if regime=="C-G" and len(request["variables"])!=3:
        return {"status":"unsupported","reason":"Finite DAG reference supports three variables"}
    if regime=="C-T" and request["model"].get("max_lag")!=1:
        return {"status":"unsupported","reason":"Temporal coefficient-box reference supports lag one"}
    return {"status":"specified","estimator":estimator,"inference":inference,
            "assumptions":sorted(REQUIRED[regime]),"scope":"Consequences of supplied premises; declarations are not model validation"}


def validate_result(result):
    axes=result["axes"]; length=1
    for axis in axes:
        if not axis["labels"] or len(set(map(str,axis["labels"])))!=len(axis["labels"]):
            raise ValueError("nonempty unique coordinate labels required")
        length*=len(axis["labels"])
    if len(result["units"])!=length:
        raise ValueError("one declared unit per flattened coordinate required")
    numerical=result["numerical_error"]
    if numerical is not None and (len(numerical)!=length or not np.all(np.isfinite(numerical)) or np.any(np.asarray(numerical)<0)):
        raise ValueError("invalid numerical error bounds")
    estimate=result["estimate"]
    if estimate is not None and (len(estimate)!=length or not np.all(np.isfinite(estimate))):
        raise ValueError("estimate does not match flattened declared axes")
    covariance=result["covariance"]
    if covariance is not None:
        c=np.asarray(covariance)
        if c.shape!=(length,length) or not np.all(np.isfinite(c)) or not np.allclose(c,c.T,atol=1e-10) or np.linalg.eigvalsh(c).min()<-1e-10:
            raise ValueError("invalid sampling covariance")
    uncertainty=result["uncertainty"]
    if uncertainty is not None:
        sets=uncertainty["coordinate_sets"]
        if len(sets)!=length:
            raise ValueError("one interval union per coordinate required")
        if uncertainty["kind"]=="joint_confidence_set" and uncertainty["coverage"]!="simultaneous":
            raise ValueError("pointwise intervals cannot be relabeled joint")
        meanings={"joint_confidence_set":"simultaneous","pointwise_confidence_set":"pointwise","posterior_credible_set":"posterior","sensitivity_set":"none"}
        if uncertainty["coverage"]!=meanings[uncertainty["kind"]] or (uncertainty["level"] is None)!=(uncertainty["kind"]=="sensitivity_set"):
            raise ValueError("uncertainty meaning/level mismatch")
        for union in sets:
            last=None
            for j,(lo,hi) in enumerate(union):
                if (lo is not None and not np.isfinite(lo)) or (hi is not None and not np.isfinite(hi)):
                    raise ValueError("use null for infinite endpoints")
                if lo is not None and hi is not None and lo>hi:
                    raise ValueError("inverted interval")
                if j and (last is None or lo is None or lo<=last):
                    raise ValueError("interval union must be disjoint and ordered")
                last=hi
    graph=result.get("graph")
    if graph is not None:
        if graph["kind"] not in {"DAG_set","CPDAG","PAG","temporal_coefficient_box"}:
            raise ValueError("unknown graph semantics")
        if any(mark not in {"tail","arrow","circle","zero_or_nonzero","present"} for mark in graph["marks"]):
            raise ValueError("unknown endpoint mark")
        if graph["kind"]=="DAG_set" and "circle" in graph["marks"]:
            raise ValueError("PAG uncertainty cannot be serialized as a DAG")
        p=len(graph["nodes"])
        if len(set(graph["nodes"]))!=p or not p:
            raise ValueError("unique declared graph nodes required")
        for model in graph["models"]:
            a=np.asarray(model)
            if a.shape!=(p,p) or not np.all(np.isfinite(a)):
                raise ValueError("graph matrix must match node ordering")
            if graph["kind"]=="DAG_set":
                if not np.all((a==0)|(a==1)) or any(np.trace(np.linalg.matrix_power(a,h)) for h in range(1,p+1)):
                    raise ValueError("DAG matrix is not binary acyclic")
            elif graph["kind"] in {"CPDAG","PAG"}:
                if not np.all(np.isin(a,[0,1,2] if graph["kind"]=="CPDAG" else [0,1,2,3])) or np.any(np.diag(a)) or np.any((a==0)!=(a.T==0)):
                    raise ValueError("invalid endpoint matrix; full graph-class recognition is a separate qualification")
        if graph["kind"]=="temporal_coefficient_box" and (len(graph["models"])!=2 or np.any(np.asarray(graph["models"][0])>np.asarray(graph["models"][1]))):
            raise ValueError("temporal class requires lower/upper coefficient matrices")
    return result


def scale_result(result,factors,units):
    """Fixed nonzero coordinate scaling. Nonlinear FX/clock changes are excluded."""
    import copy
    output=copy.deepcopy(validate_result(result)); factors=np.asarray(factors,dtype=float)
    n=int(np.prod([len(a["labels"]) for a in result["axes"]]))
    if factors.shape!=(n,) or not np.all(np.isfinite(factors)) or np.any(factors==0) or len(units)!=n:
        raise ValueError("one finite nonzero scale/unit per coordinate required")
    if output["estimate"] is not None:
        output["estimate"]=(factors*np.asarray(output["estimate"])).tolist()
    if output["covariance"] is not None:
        output["covariance"]=(np.asarray(output["covariance"])*np.outer(factors,factors)).tolist()
    if output["uncertainty"] is not None:
        converted=[]
        for factor,union in zip(factors,output["uncertainty"]["coordinate_sets"]):
            items=[]
            for lo,hi in union:
                pair=[None if v is None else float(factor*v) for v in (lo,hi)]
                items.append(pair if factor>0 else pair[::-1])
            converted.append(items if factor>0 else items[::-1])
        output["uncertainty"]["coordinate_sets"]=converted
    output["units"]=list(units)
    if output["numerical_error"] is not None:
        output["numerical_error"]=(abs(factors)*np.asarray(output["numerical_error"])).tolist()
    return validate_result(output)
