"""Semantic edge cases for the V12 operation design; no transport is claimed."""
import copy
import json
from pathlib import Path
import sys
import unittest

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from causalbank.operation_contract_v12 import context_digest, validate_response, validate_set

BASE = ROOT / "docs/program/repair-v12/work/IN02"


def fixture():
    context = {"target": {"kind": "finite_horizon_value", "outcome": "value", "treatment": "offer",
                          "contrast": "offer versus no offer"},
               "population": {"definition": "Eligible accounts at decision time", "unit": "account"},
               "variables": [{"id": "offer", "role": "action", "unit": "binary"},
                             {"id": "value", "role": "outcome", "unit": "USD"}],
               "intervention": {"kind": "fixed_policy", "value": "offer=1"},
               "horizon": {"value": 12, "unit": "months"}, "units": ["USD"],
               "sign_convention": "offer-minus-no-offer", "observation_clock": {
                   "event_time": "event_at", "available_time": "available_at", "decision_time": "decision_at",
                   "rule": "strict_before_decision", "alternative_justification": None},
               "sampling": {"law": "independent_accounts", "unit": "account", "fold_unit": "account"},
               "assumptions": [{"id": "exchangeability", "statement": "No unmeasured confounding",
                                "status": "unverified", "evidence": []}],
               "graph": {"kind": "DAG", "edges": [{"left_node": "offer", "right_node": "value",
                  "left_mark": "tail", "right_mark": "arrow", "evidence_type": "assumption",
                  "evidence_refs": [], "review_status": "unverified"}]}, "source_evidence": []}
    request = {"schema_version": "causalbank.request/1.0.0", "request_id": "case-1",
               "operation": "estimate.effect", "artifact_inputs": [], "budget": {"wall_seconds": 20,
               "memory_bytes": 1000000, "max_output_bytes": 100000, "model_calls": 0},
               "parameters": {"engine_id": "reference-selected", "estimator_id": "declared-mean"},
               "scientific_context": context, "idempotency_key": None}
    response = {"schema_version": "causalbank.response/1.0.0", "request_id": "case-1",
                "operation": "estimate.effect", "status": "completed", "disposition": "computed",
                "context_sha256": context_digest(context),
                "result": {"kind": "effect", "estimate": [0],
                    "coordinate_sets": [{"topology": "whole_line", "intervals": [[None, None]]}],
                    "units": ["USD"], "uncertainty": {"kind": "pointwise_confidence",
                    "coverage": "pointwise", "level": .95, "sampling_law": "independent_accounts",
                    "assumptions": ["exchangeability"], "numerical_error": None,
                    "construction_evidence": []}, "payload": {}},
                "error": None, "evidence": [],
                "qualification": {"level": "conditional_inference", "evidence": []}}
    return request, response


class OperationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request_schema = json.loads((BASE / "request-schema.json").read_text())
        cls.response_schema = json.loads((BASE / "response-schema.json").read_text())
        jsonschema.Draft202012Validator.check_schema(cls.request_schema)
        jsonschema.Draft202012Validator.check_schema(cls.response_schema)

    def valid(self, request, response):
        jsonschema.validate(request, self.request_schema)
        jsonschema.validate(response, self.response_schema)
        validate_response(request, response)

    def test_whole_line_conditional_result_is_structurally_valid(self):
        self.valid(*fixture())

    def test_unknown_set_is_distinct_from_empty(self):
        validate_set({"topology": "empty", "intervals": []})
        validate_set({"topology": "unknown", "intervals": None})
        with self.assertRaisesRegex(ValueError, "explicitly contain"):
            validate_set({"topology": "empty", "intervals": None})

    def test_disconnected_and_unbounded_union_preserved(self):
        validate_set({"topology": "unbounded_union", "intervals": [[None, -1], [2, None]]})
        with self.assertRaisesRegex(ValueError, "topology"):
            validate_set({"topology": "finite_interval", "intervals": [[None, None]]})

    def test_overlapping_intervals_rejected(self):
        with self.assertRaisesRegex(ValueError, "disjoint"):
            validate_set({"topology": "finite_union", "intervals": [[0, 2], [1, 3]]})

    def test_refusal_cannot_carry_numeric_effect(self):
        q, r = fixture(); r["disposition"] = "refused"
        with self.assertRaisesRegex(ValueError, "cannot carry"):
            self.valid(q, r)

    def test_context_clock_or_target_change_is_rejected(self):
        q, r = fixture(); q["scientific_context"]["sign_convention"] = "no-offer-minus-offer"
        with self.assertRaisesRegex(ValueError, "context changed"):
            self.valid(q, r)

    def test_unit_change_is_rejected(self):
        q, r = fixture(); r["result"]["units"] = ["EUR"]
        with self.assertRaisesRegex(ValueError, "changed units"):
            self.valid(q, r)

    def test_sampling_law_change_is_rejected(self):
        q, r = fixture(); r["result"]["uncertainty"]["sampling_law"] = "independent_dates"
        with self.assertRaisesRegex(ValueError, "sampling law"):
            self.valid(q, r)

    def test_pointwise_cannot_become_joint(self):
        q, r = fixture(); r["result"]["uncertainty"]["kind"] = "joint_confidence"
        with self.assertRaisesRegex(ValueError, "interpretation"):
            self.valid(q, r)

    def test_unverified_joint_requires_construction(self):
        q, r = fixture(); u = r["result"]["uncertainty"]
        u.update(kind="joint_confidence", coverage="simultaneous")
        with self.assertRaisesRegex(ValueError, "construction"):
            self.valid(q, r)

    def test_pag_endpoint_cannot_be_serialized_as_dag(self):
        q, r = fixture(); q["scientific_context"]["graph"]["edges"][0]["left_mark"] = "circle"
        r["context_sha256"] = context_digest(q["scientific_context"])
        with self.assertRaisesRegex(ValueError, "cannot become a DAG"):
            self.valid(q, r)

    def test_dag_cycle_is_rejected(self):
        q, r = fixture(); q["scientific_context"]["graph"]["edges"].append({
            "left_node": "value", "right_node": "offer", "left_mark": "tail",
            "right_mark": "arrow", "evidence_type": "assumption", "evidence_refs": [],
            "review_status": "unverified"})
        r["context_sha256"] = context_digest(q["scientific_context"])
        with self.assertRaisesRegex(ValueError, "directed cycle"):
            self.valid(q, r)

    def test_graph_set_requires_exact_member_artifact(self):
        q, r = fixture(); q["scientific_context"]["graph"] = {"kind": "DAG_set", "edges": []}
        r["context_sha256"] = context_digest(q["scientific_context"])
        with self.assertRaisesRegex(ValueError, "exact member artifacts"):
            self.valid(q, r)
        q["scientific_context"]["graph"]["member_artifacts"] = [{
            "artifact_id": "graph-set-1", "sha256": "a" * 64, "media_type": "application/json",
            "schema_version": "graph-set/1", "role": "graph_set", "bytes": 10,
            "custody": "local"}]
        r["context_sha256"] = context_digest(q["scientific_context"])
        self.valid(q, r)

    def test_nested_artifact_path_is_rejected(self):
        q, r = fixture(); q["scientific_context"]["source_evidence"].append({
            "artifact_id": "../secret", "sha256": "a" * 64, "media_type": "application/json",
            "schema_version": "source/1", "role": "observation", "bytes": 1,
            "custody": "local"})
        r["context_sha256"] = context_digest(q["scientific_context"])
        with self.assertRaises(jsonschema.ValidationError):
            self.valid(q, r)

    def test_cancelled_job_cannot_return_effect(self):
        q, r = fixture(); r.update(status="cancelled", disposition="unavailable")
        with self.assertRaisesRegex(ValueError, "cannot publish"):
            self.valid(q, r)

    def test_invocation_error_is_separate_from_scientific_disposition(self):
        q, r = fixture(); r.update(status="failed", error={"code": "runtime", "message": "crash", "retryable": True})
        with self.assertRaisesRegex(ValueError, "withhold"):
            self.valid(q, r)
        r["result"] = None; r["disposition"] = "unavailable"
        self.valid(q, r)

    def test_pending_job_cannot_publish_computed_result(self):
        q, r = fixture(); r["status"] = "running"; r["result"] = None
        with self.assertRaisesRegex(ValueError, "cannot claim computed"):
            self.valid(q, r)

    def test_qualification_needs_bound_evidence(self):
        q, r = fixture(); r["qualification"]["level"] = "qualified_in_declared_scope"
        with self.assertRaisesRegex(ValueError, "requires evidence"):
            self.valid(q, r)

    def test_schema_rejects_undeclared_transport_field(self):
        q, _ = fixture(); q["arbitrary_shell"] = "run"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(q, self.request_schema)

    def test_program_operation_mappings_are_one_to_one(self):
        core = json.loads((BASE / "operation-contract.json").read_text())
        cli = json.loads((BASE / "cli-contract.json").read_text())
        mcp = json.loads((BASE / "mcp-contract.json").read_text())
        identities = [row["id"] for row in core["operations"]]
        self.assertEqual(len(identities), len(set(identities)))
        self.assertEqual(identities, [row["id"] for row in cli["mapping"]])
        self.assertEqual(identities, [row["id"] for row in mcp["tool_mapping"]])
        self.assertEqual(mcp["protocol_version"], "2025-11-25")
        self.assertEqual(mcp["current_standard_comparison"]["version"], "2026-07-28")


if __name__ == "__main__":
    unittest.main()
