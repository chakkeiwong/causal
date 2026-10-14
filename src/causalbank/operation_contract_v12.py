"""Reference semantic checks for the V12 design; no causal estimator or server.

The JSON schemas supply structure. These checks preserve scientific meanings
that JSON types alone cannot enforce. Passing validates declarations, not truth.
"""
import hashlib
import json
import math
import re


_ARTIFACT_ID = re.compile(r"(?!.*\.\.)[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


def context_digest(context):
    if context is None:
        return None
    return hashlib.sha256(json.dumps(context, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def finite_json(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Non-finite JSON number; use explicit unbounded set endpoints")
    if isinstance(value, dict):
        for part in value.values():
            finite_json(part)
    elif isinstance(value, list):
        for part in value:
            finite_json(part)


def validate_artifact_ref(ref):
    """Check declared handle identity, not its custody or readable bytes."""
    if not isinstance(ref, dict) or not _ARTIFACT_ID.fullmatch(ref.get("artifact_id", "")):
        raise ValueError("Artifact identity must be an opaque handle")
    if not re.fullmatch(r"[0-9a-f]{64}", ref.get("sha256", "")):
        raise ValueError("Artifact handle needs a SHA-256 identity")


def validate_artifact_refs(value):
    if isinstance(value, dict):
        if "artifact_id" in value:
            validate_artifact_ref(value)
        for part in value.values():
            validate_artifact_refs(part)
    elif isinstance(value, list):
        for part in value:
            validate_artifact_refs(part)


def validate_context(context):
    if context is None:
        return
    finite_json(context)
    variables = context["variables"]
    names = [v["id"] for v in variables]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate variable identity")
    if not {context["target"]["outcome"], context["target"]["treatment"]} <= set(names):
        raise ValueError("Target uses undeclared variables")
    assumptions = [a["id"] for a in context["assumptions"]]
    if len(assumptions) != len(set(assumptions)):
        raise ValueError("Duplicate assumption identity")
    clock = context["observation_clock"]
    if clock["rule"] == "explicit_alternative" and not clock["alternative_justification"]:
        raise ValueError("Alternative clock needs a reviewed justification")
    # Actual timestamp comparison belongs to the observation operation. These
    # are declared column/clock names, not values that can establish chronology.
    graph = context["graph"]
    if graph:
        if graph.get("kind") not in {"DAG", "DAG_set", "ADMG", "CPDAG", "PAG", "temporal_graph_set"}:
            raise ValueError("Unknown graph kind")
        member_refs = graph.get("member_artifacts", [])
        if graph["kind"] in {"DAG_set", "temporal_graph_set"}:
            if not member_refs or graph.get("edges"):
                raise ValueError("Graph set needs exact member artifacts, not flattened edges")
        elif member_refs:
            raise ValueError("A single graph cannot carry undeclared graph-set members")
        for edge in graph.get("edges", []):
            if edge["left_node"] == edge["right_node"]:
                raise ValueError("Self edge is not a valid DAG/graph declaration")
            if edge["left_node"] not in names or edge["right_node"] not in names:
                raise ValueError("Graph endpoint has no variable definition")
            marks = (edge["left_mark"], edge["right_mark"])
            if any(mark not in {"tail", "arrow", "circle"} for mark in marks):
                raise ValueError("Unknown graph endpoint mark")
            if graph["kind"] in {"DAG", "DAG_set"} and marks not in {("tail", "arrow"), ("arrow", "tail")}:
                raise ValueError("Ambiguous/bidirected endpoint cannot become a DAG edge")
        if graph["kind"] == "DAG":
            arcs = [(e["left_node"], e["right_node"]) if e["left_mark"] == "tail"
                    else (e["right_node"], e["left_node"]) for e in graph.get("edges", [])]
            if len(arcs) != len(set(arcs)):
                raise ValueError("Duplicate DAG edge")
            remaining = set(names)
            while remaining:
                roots = {v for v in remaining if not any(w == v and u in remaining for u, w in arcs)}
                if not roots:
                    raise ValueError("DAG declaration contains a directed cycle")
                remaining -= roots
        # Full graph-class recognition is deliberately not claimed here.


def validate_set(value):
    topology, pieces = value["topology"], value["intervals"]
    if topology == "unknown":
        if pieces is not None:
            raise ValueError("Unknown set cannot contain computed intervals")
        return
    if pieces is None:
        raise ValueError("Computed set must explicitly contain its interval union")
    finite_json(pieces)
    last = None
    for i, (lo, hi) in enumerate(pieces):
        if lo is not None and hi is not None and lo > hi:
            raise ValueError("Inverted interval")
        if i and (last is None or lo is None or lo <= last):
            raise ValueError("Interval union must remain disjoint and ordered")
        last = hi
    unbounded = any(lo is None or hi is None for lo, hi in pieces)
    expected = ("empty" if not pieces else "whole_line" if pieces == [[None, None]] else
                "unbounded_union" if unbounded else "finite_interval" if len(pieces) == 1 else "finite_union")
    if topology != expected:
        raise ValueError("Set topology disagrees with its actual intervals")


def validate_response(request, response):
    finite_json(request)
    finite_json(response)
    validate_artifact_refs(request)
    validate_artifact_refs(response)
    validate_context(request["scientific_context"])
    if any(request[k] != response[k] for k in ("request_id", "operation")):
        raise ValueError("Response belongs to another request/operation")
    if context_digest(request["scientific_context"]) != response["context_sha256"]:
        raise ValueError("Target/population/unit/clock/sampling context changed")
    result = response["result"]
    if response["status"] in {"failed", "rejected"}:
        if response["error"] is None or result is not None or response["disposition"] == "computed":
            raise ValueError("Failed invocation must retain its error and withhold scientific result")
    elif response["error"] is not None:
        raise ValueError("Ordinary scientific disposition is not an invocation error")
    if response["status"] in {"queued", "running", "cancelled"} and response["disposition"] == "computed":
        raise ValueError("Incomplete or cancelled job cannot claim computed scientific output")
    if response["status"] in {"queued", "running", "cancelled"} and result is not None and result["kind"] != "job":
        raise ValueError("Incomplete or cancelled job cannot publish a completed scientific result")
    if response["status"] == "completed" and response["disposition"] == "computed" and result is None:
        raise ValueError("Computed disposition requires a typed result")
    if result:
        if response["status"] != "completed" and result["kind"] != "job":
            raise ValueError("Partial job cannot publish a completed scientific result")
        if response["disposition"] != "computed" and (result["estimate"] is not None or result["coordinate_sets"] is not None):
            raise ValueError("Uncomputed/refused disposition cannot carry a numerical result")
        units = result["units"]
        context = request["scientific_context"]
        if result["kind"] == "effect" and context and units != context["units"]:
            raise ValueError("Scientific result changed units")
        if result["kind"] == "effect" and response["disposition"] == "computed" and not units:
            raise ValueError("Computed effect needs a declared coordinate")
        estimate = result["estimate"]
        if estimate is not None and len(estimate) != len(units):
            raise ValueError("Estimate coordinate count differs from declared units")
        sets = result["coordinate_sets"]
        if sets is not None:
            if len(sets) != len(units):
                raise ValueError("One set per coordinate required")
            for value in sets:
                validate_set(value)
        uncertainty = result["uncertainty"]
        if uncertainty:
            meanings = {"pointwise_confidence": "pointwise", "joint_confidence": "simultaneous",
                        "posterior_credible": "posterior", "sensitivity": "none"}
            if meanings[uncertainty["kind"]] != uncertainty["coverage"]:
                raise ValueError("Uncertainty interpretation changed")
            level = uncertainty["level"]
            if uncertainty["kind"] == "sensitivity":
                if level is not None:
                    raise ValueError("Sensitivity does not imply a coverage probability")
            elif not isinstance(level, (int, float)) or isinstance(level, bool) or not 0 < level < 1:
                raise ValueError("Confidence/credible level must be a probability")
            if context and uncertainty["sampling_law"] != context["sampling"]["law"]:
                raise ValueError("Uncertainty changed sampling law")
            if uncertainty["kind"] == "joint_confidence" and not uncertainty["construction_evidence"]:
                raise ValueError("Joint uncertainty needs its declared construction")
    qualification = response["qualification"]
    if qualification["level"] in {"qualified_in_declared_scope", "externally_accepted"} and not qualification["evidence"]:
        raise ValueError("Qualification requires evidence; transport success is insufficient")
    return response
