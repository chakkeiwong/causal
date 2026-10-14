import json
from pathlib import Path

edges = [
    {"left_node": a, "right_node": b,
     "left_mark": "tail", "right_mark": "arrow",
     "evidence_type": "assumption", "evidence_refs": [],
     "review_status": "unverified"}
    for a, b in [("risk", "offer"), ("risk", "net_value"),
                 ("offer", "net_value")]
]
context = {
    "target": {"kind": "average_effect", "outcome": "net_value",
               "treatment": "offer", "contrast": "1-versus-0"},
    "population": {"definition": "Generated eligible accounts at decision",
                   "unit": "account"},
    "variables": [
        {"id": "offer", "role": "action", "unit": "binary"},
        {"id": "net_value", "role": "outcome", "unit": "USD"},
        {"id": "risk", "role": "adjustment", "unit": "score"}],
    "intervention": {"kind": "set", "value": "offer=1"},
    "horizon": {"value": 12, "unit": "months"}, "units": ["USD"],
    "sign_convention": "offer-minus-no-offer",
    "observation_clock": {
        "event_time": "event_at", "available_time": "available_at",
        "decision_time": "decision_at", "rule": "strict_before_decision",
        "alternative_justification": None},
    "sampling": {"law": "independent_units", "unit": "account",
                 "fold_unit": "account"},
    "assumptions": [{
        "id": "graph_truth",
        "statement": "The supplied graph represents this generated example",
        "status": "unverified", "evidence": []}],
    "graph": {"kind": "DAG", "edges": edges}, "source_evidence": []
}
request = {
    "schema_version": "causalbank.request/1.0.0", "request_id": "backdoor",
    "operation": "identify.effect", "artifact_inputs": [],
    "budget": {"wall_seconds": 12, "memory_bytes": 1073741824,
               "max_output_bytes": 100000, "model_calls": 0},
    "parameters": {"method_id": "backdoor"},
    "scientific_context": context, "idempotency_key": None
}
Path("request.json").write_text(json.dumps(request, indent=2) + "\n")
