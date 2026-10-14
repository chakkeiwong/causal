#!/usr/bin/env python3
"""Validate supplied contracts and selected cross-field scientific invariants."""
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


def validate(kind, record):
    schema = json.loads((CONTRACTS / (kind + ".schema.json")).read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)
    if kind == "temporal_event":
        instant = lambda k: datetime.fromisoformat(record[k].replace("Z", "+00:00"))
        if record["role"] in ("historical_covariate", "known_future_schedule"):
            if instant("available_at") > instant("decision_at"):
                raise ValueError("Feature was unavailable at the decision")
        if record["role"] == "historical_covariate" and instant("event_at") > instant("decision_at"):
            raise ValueError("Future event used as historical measurement")
        if record["missingness"] != "observed" and record["value"] is not None:
            raise ValueError("Missingness requires explicit null in this raw-event contract")
    elif kind == "effect_result":
        if record["scientific_status"] in ("unsupported", "not_identified") and record["estimate"] is not None:
            raise ValueError("Unavailable causal estimate must be null")
        if record["interval"] is not None and record["interval"][0] > record["interval"][1]:
            raise ValueError("Reversed interval")
        if (record["interval"] is None) != (record["interval_kind"] == "none"):
            raise ValueError("Interval type and presence disagree")
        if record["scientific_status"] == "partially_identified" and record["interval_kind"] != "identified_set":
            raise ValueError("Partial identification must preserve bound semantics")
        if record["scientific_status"] == "identified_under_assumptions" and not record["assumption_ids"]:
            raise ValueError("Identified claim needs declared assumptions")
    elif kind == "graph":
        nodes = record["nodes"]
        if len(nodes) != len(set(nodes)):
            raise ValueError("Duplicate node")
        adjacency = {n: [] for n in nodes}
        for e in record["edges"]:
            if e["source"] not in nodes or e["target"] not in nodes:
                raise ValueError("Unknown endpoint")
            if e["lag"] > record["max_lag"]:
                raise ValueError("Edge exceeds declared lag window")
            if record["graph_type"] == "DAG":
                if (e["source_endpoint"], e["target_endpoint"]) != ("tail", "arrow"):
                    raise ValueError("Unresolved/latent edge cannot be silently called a DAG edge")
                if e["lag"] == 0:
                    adjacency[e["source"]].append(e["target"])
            if record["graph_type"] == "CPDAG":
                if (e["source_endpoint"], e["target_endpoint"]) not in (("tail", "tail"), ("tail", "arrow"), ("arrow", "tail")):
                    raise ValueError("PAG endpoint is not a CPDAG endpoint")
        if record["graph_type"] == "DAG":
            visited, active = set(), set()
            def visit(node):
                if node in active:
                    raise ValueError("Contemporaneous directed cycle")
                if node not in visited:
                    active.add(node)
                    for other in adjacency[node]:
                        visit(other)
                    active.remove(node)
                    visited.add(node)
            for node in nodes:
                visit(node)
    return True


def main():
    records = {k: json.loads((CONTRACTS / "examples" / (k + ".json")).read_text())
               for k in ("study", "temporal_event", "effect_result", "graph")}
    outcomes = []
    for k, value in records.items():
        validate(k, value)
        outcomes.append({"case": "valid_" + k, "status": "pass"})
    fixtures = []
    def mutation(kind, name, fn):
        record = deepcopy(records[kind])
        fn(record)
        fixtures.append((kind, name, record))
    mutation("temporal_event", "late_information", lambda x: x.update(available_at="2026-02-01T00:00:00Z"))
    mutation("temporal_event", "future_history", lambda x: x.update(event_at="2026-02-01T00:00:00Z"))
    mutation("temporal_event", "missing_as_zero", lambda x: x.update(value=0, missingness="missing"))
    mutation("effect_result", "unsupported_point", lambda x: x.update(scientific_status="unsupported"))
    mutation("effect_result", "reversed_interval", lambda x: x.update(interval=[9, 7]))
    mutation("effect_result", "unlabeled_bound", lambda x: x.update(scientific_status="partially_identified"))
    mutation("effect_result", "no_assumptions", lambda x: x.update(assumption_ids=[]))
    mutation("graph", "PAG_as_DAG", lambda x: x.update(graph_type="DAG"))
    mutation("graph", "unknown_node", lambda x: x["edges"][0].update(target="unregistered"))
    mutation("graph", "lag_overflow", lambda x: x["edges"][0].update(lag=2))
    for kind, name, record in fixtures:
        try:
            validate(kind, record)
        except (ValueError, ValidationError) as error:
            outcomes.append({"case": name, "status": "rejected_as_expected", "error": str(error)})
        else:
            raise AssertionError("Invalid fixture accepted: " + name)
    study_path = CONTRACTS / "examples/study.json"
    assert records["effect_result"]["study_sha256"] == hashlib.sha256(study_path.read_bytes()).hexdigest()
    assert records["effect_result"]["study_id"] == records["study"]["study_id"]
    assert records["effect_result"]["contrast_direction"] == records["study"]["estimand"]["direction"]
    result_path = ROOT / "docs/examples/results.json"
    assert records["effect_result"]["artifact_sha256"] == hashlib.sha256(result_path.read_bytes()).hexdigest()
    out = {"status": "pass", "cases": outcomes, "cross_artifact_checks": "study ID, direction and hashes match",
           "scope": "Schema and selected semantics only; not causal assumption verification or implemented product adapters"}
    (ROOT / "docs/examples/contract-checks.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"status": "pass", "valid": len(records), "invalid_rejected": len(fixtures)}))


if __name__ == "__main__":
    main()
