"""Bounded, explicitly scoped operations under the IN02 canonical contract.

This is a local reference runtime. It does not verify causal premises, graph
truth, financial usefulness, or externally accepted bank interfaces.
"""
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import time

import jsonschema

from .artifacts_v12 import ArtifactStore, ROOT, encode
from .operation_contract_v12 import (context_digest, finite_json,
                                     validate_context, validate_response,
                                     validate_set)

CONTRACT = ROOT / "docs/program/repair-v12/work/IN02"
REQUEST_SCHEMA = json.loads((CONTRACT / "request-schema.json").read_text())
RESPONSE_SCHEMA = json.loads((CONTRACT / "response-schema.json").read_text())
SUPPORTED = {
    "capabilities.describe": "exact_runtime_manifest",
    "graph.review": "declared_graph_syntax_only",
    "identify.effect": "supplied_DAG_backdoor_independent_units",
    "estimate.effect": "supplied_moment_Gaussian_residual_inversion",
    "sensitivity.evaluate": "deterministic_quadratic_sublevel",
    "audit.observation": "declared_strict_before_decision_clock",
}


def request_digest(request):
    payload = {k: v for k, v in request.items() if k not in {"request_id", "idempotency_key"}}
    return hashlib.sha256(encode(payload)).hexdigest()


def topology(intervals):
    if intervals is None:
        return "unknown"
    if not intervals:
        return "empty"
    if intervals == [[None, None]]:
        return "whole_line"
    if any(lo is None or hi is None for lo, hi in intervals):
        return "unbounded_union"
    return "finite_interval" if len(intervals) == 1 else "finite_union"


def result(kind, *, units=None, estimate=None, sets=None, uncertainty=None, payload=None):
    return {"kind": kind, "units": units or [], "estimate": estimate,
            "coordinate_sets": sets, "uncertainty": uncertainty, "payload": payload or {}}


def envelope(request, *, status="completed", disposition="computed", value=None,
             qualification="execution_only", evidence=None, error=None):
    return {"schema_version": "causalbank.response/1.0.0",
            "request_id": request["request_id"], "operation": request["operation"],
            "status": status, "disposition": disposition,
            "context_sha256": context_digest(request.get("scientific_context")),
            "result": value, "error": error, "evidence": evidence or [],
            "qualification": {"level": qualification, "evidence": evidence or []}}


def validate_request(request):
    finite_json(request)
    jsonschema.validate(request, REQUEST_SCHEMA)
    validate_context(request["scientific_context"])
    if request["budget"]["model_calls"] != 0:
        raise ValueError("No model-call backend is authorized in this runtime")
    if len(encode(request)) > min(1_000_000, request["budget"]["memory_bytes"] // 2):
        raise ValueError("Request exceeds declared input memory budget")


class OperationService:
    def __init__(self, root=ROOT / ".runtime/operation-v12"):
        self.store = ArtifactStore(root)

    def _artifact(self, request, role):
        refs = [x for x in request["artifact_inputs"] if x["role"] == role]
        if len(refs) != 1:
            raise ValueError("Exactly one authorized " + role + " artifact is required")
        if refs[0]["bytes"] > min(8 * 1024 * 1024, request["budget"]["memory_bytes"] // 2):
            raise ValueError("Artifact exceeds declared read memory budget")
        schema = {"moment_summary": "moment-summary/1",
                  "quadratic_bounds": "quadratic-bounds/1",
                  "observation_rows": "observation-rows/1"}[role]
        if refs[0]["schema_version"] != schema:
            raise ValueError("Unsupported input artifact schema")
        data = self.store.get(refs[0], limit=request["budget"]["memory_bytes"] // 2)
        if not isinstance(data, dict) or data.get("context_sha256") != context_digest(request["scientific_context"]):
            raise ValueError("Input artifact belongs to another scientific context")
        return refs[0], data

    def invoke(self, request):
        validate_request(request)
        started = time.monotonic()
        name = request["operation"]
        context = request["scientific_context"]
        if name in {"identify.effect", "estimate.effect"} and context and any(
                x["status"] == "contradicted" for x in context["assumptions"]):
            response = envelope(request, disposition="refused", value=None, qualification="none")
        elif name == "capabilities.describe":
            response = self._capabilities(request)
        elif name == "graph.review":
            response = self._graph(request)
        elif name == "identify.effect":
            response = self._identify(request)
        elif name == "estimate.effect":
            response = self._estimate(request)
        elif name == "sensitivity.evaluate":
            response = self._sensitivity(request)
        elif name == "audit.observation":
            response = self._audit(request)
        else:
            response = envelope(request, disposition="unsupported", value=None,
                qualification="none")
        if time.monotonic() - started > request["budget"]["wall_seconds"]:
            response = envelope(request, status="failed", disposition="unavailable", value=None,
                qualification="none", error={"code": "wall_budget", "message": "Operation exceeded wall budget", "retryable": False})
        if len(encode(response)) > request["budget"]["max_output_bytes"]:
            response = envelope(request, status="failed", disposition="unavailable", value=None,
                qualification="none", error={"code": "output_budget", "message": "Canonical output exceeds budget", "retryable": False})
        jsonschema.validate(response, RESPONSE_SCHEMA)
        validate_response(request, response)
        return response

    def _capabilities(self, request):
        payload = {"runtime": "local_reference_v12", "request_schema": "causalbank.request/1.0.0",
                   "response_schema": "causalbank.response/1.0.0", "mcp_protocol": "2025-11-25",
                   "implemented": SUPPORTED,
                   "unimplemented": [x for x in REQUEST_SCHEMA["properties"]["operation"]["enum"] if x not in SUPPORTED],
                   "limitations": ["No LLM, causal discovery, bank acceptance or platform-scale claim",
                                   "Only listed method IDs and a local operator artifact store are available"]}
        return envelope(request, value=result("capabilities", payload=payload))

    def _graph(self, request):
        context = request["scientific_context"]
        if context is None or context["graph"] is None:
            return envelope(request, disposition="unavailable", value=None, qualification="none")
        if request["parameters"]["review_kind"] != "syntax":
            return envelope(request, disposition="unsupported", value=None, qualification="none")
        graph = context["graph"]
        return envelope(request, value=result("graph", payload={
            "graph": graph, "node_count": len(context["variables"]),
            "edge_count": len(graph["edges"]),
            "member_artifact_count": len(graph.get("member_artifacts", [])),
            "reviewed": "declared_syntax_only; causal truth and full graph class not tested"}))

    def _identify(self, request):
        context = request["scientific_context"]
        if request["parameters"]["method_id"] != "backdoor" or context["graph"] is None or context["graph"]["kind"] != "DAG":
            return envelope(request, disposition="unsupported", value=None, qualification="none")
        if context["sampling"]["law"] != "independent_units":
            return envelope(request, disposition="unsupported", value=None, qualification="none")
        # The selected reference implementation only handles an explicitly
        # supplied DAG and a binary 1-vs-0 action contrast.
        if context["target"]["contrast"] != "1-versus-0" or len(context["units"]) != 1:
            return envelope(request, disposition="unsupported", value=None, qualification="none")
        from .causal_workflow import AdjustmentQuery, adjustment_expression
        edges = [(e["left_node"], e["right_node"]) if e["left_mark"] == "tail"
                 else (e["right_node"], e["left_node"]) for e in context["graph"]["edges"]]
        controls = tuple(v["id"] for v in context["variables"] if v["role"] == "adjustment")
        observed = [v["id"] for v in context["variables"] if v["role"] != "latent"]
        query = AdjustmentQuery(action=context["target"]["treatment"],
                                outcome=context["target"]["outcome"], controls=controls,
                                unit=context["population"]["unit"],
                                outcome_unit=context["units"][0], sampling="independent_units")
        try:
            expression = adjustment_expression(query, edges, observed)
        except ValueError as exc:
            return envelope(request, disposition="unsupported", value=result("identification",
                units=context["units"], payload={"reason": str(exc),
                "boundary": "Failed this supplied-DAG back-door attempt, not general nonidentification"}),
                qualification="none")
        return envelope(request, value=result("identification", units=context["units"],
            payload={"expression": expression, "scope": "Conditional on supplied DAG, consistency, positivity and independent units"}),
            qualification="conditional_inference")

    def _estimate(self, request):
        context = request["scientific_context"]
        p = request["parameters"]
        if (p["engine_id"], p["estimator_id"]) != ("reference-moment-sets", "gaussian-residual-inversion"):
            return envelope(request, disposition="unsupported", value=None, qualification="none")
        ref, data = self._artifact(request, "moment_summary")
        import numpy as np
        from .responses import moment_test_sets
        mean = np.asarray(data["mean"], dtype=float)
        lrv = np.asarray(data["lrv"], dtype=float)
        n, alpha = data["n"], data["alpha"]
        simultaneous = data["simultaneous"]
        if (mean.ndim != 1 or not 2 <= len(mean) <= 64 or len(mean) - 1 != len(context["units"])
                or lrv.shape != (len(mean), len(mean)) or not np.isfinite(mean).all()
                or not np.isfinite(lrv).all() or not np.allclose(lrv, lrv.T, atol=1e-10)
                or np.linalg.eigvalsh(lrv).min() < -1e-10
                or isinstance(n, bool) or not isinstance(n, int) or n < 3
                or isinstance(alpha, bool) or not isinstance(alpha, (float, int)) or not 0 < alpha < 1
                or not isinstance(simultaneous, bool)):
            raise ValueError("Invalid finite moment summary or declared units")
        raw = moment_test_sets(mean, lrv, n, alpha=alpha, simultaneous=simultaneous)
        sets = [{"topology": topology(x), "intervals": x} for x in raw]
        for item in sets:
            validate_set(item)
        kind = "joint_confidence" if simultaneous else "pointwise_confidence"
        uncertainty = {"kind": kind, "coverage": "simultaneous" if simultaneous else "pointwise",
                       "level": 1 - alpha, "sampling_law": context["sampling"]["law"],
                       "assumptions": [x["id"] for x in context["assumptions"]],
                       "numerical_error": "Double-precision numerical inversion; no finite-sample or uniform guarantee",
                       "construction_evidence": [ref]}
        return envelope(request, value=result("effect", units=context["units"], sets=sets,
            uncertainty=uncertainty, payload={"estimator": p["estimator_id"],
            "n": n, "model_boundary": "Gaussian moment approximation and supplied covariance/causal premises"}),
            qualification="conditional_inference", evidence=[ref])

    def _sensitivity(self, request):
        context = request["scientific_context"]
        if request["parameters"]["family_id"] != "quadratic-sublevel":
            return envelope(request, disposition="unsupported", value=None, qualification="none")
        ref, data = self._artifact(request, "quadratic_bounds")
        items = data["quadratics"]
        if len(items) != len(context["units"]) or len(items) > 1000:
            raise ValueError("One bounded quadratic per declared coordinate required")
        from .responses import quadratic_sublevel
        sets = []
        for coeff in items:
            if (not isinstance(coeff, list) or len(coeff) != 3 or
                    any(isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x) for x in coeff)):
                raise ValueError("Quadratic coefficients must be three finite numbers")
            intervals = quadratic_sublevel(*coeff)
            record = {"topology": topology(intervals), "intervals": intervals}
            validate_set(record)
            sets.append(record)
        uncertainty = {"kind": "sensitivity", "coverage": "none", "level": None,
                       "sampling_law": context["sampling"]["law"],
                       "assumptions": [x["id"] for x in context["assumptions"]],
                       "numerical_error": "IEEE-754 double-precision quadratic roots; numerical boundary cases require independent review",
                       "construction_evidence": [ref]}
        return envelope(request, value=result("effect", units=context["units"], sets=sets,
            uncertainty=uncertainty, payload={"scope": "Deterministic inequality set, not sampling confidence"}),
            qualification="execution_only", evidence=[ref])

    def _audit(self, request):
        context = request["scientific_context"]
        if request["parameters"]["checks"] != ["clock"] or context["observation_clock"]["rule"] != "strict_before_decision":
            return envelope(request, disposition="unsupported", value=None, qualification="none")
        ref, data = self._artifact(request, "observation_rows")
        rows = data["rows"]
        if not isinstance(rows, list) or len(rows) > 10000:
            raise ValueError("Observation audit needs a bounded row array")
        fields = context["observation_clock"]
        failures = []
        for i, row in enumerate(rows):
            try:
                event, available, decision = (datetime.fromisoformat(row[fields[k]]) for k in
                    ["event_time", "available_time", "decision_time"])
                valid = all(x.tzinfo is not None for x in [event, available, decision]) and event <= available < decision
            except (KeyError, TypeError, ValueError):
                valid = False
            if not valid:
                failures.append(i)
        return envelope(request, value=result("diagnostics", payload={
            "rows": len(rows), "clock_failures": failures,
            "all_declared_clocks_pass": not failures,
            "boundary": "Timestamp consistency only; source ownership, inclusion and truth remain unverified"}),
            qualification="execution_only", evidence=[ref])
