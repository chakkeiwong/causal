"""Actual local dispatcher and artifact semantics, distinct from IN02 design."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from causalbank.artifacts_v12 import ArtifactStore
from causalbank.operation_service_v12 import OperationService
from causalbank.operation_contract_v12 import context_digest


def context():
    return {"target": {"kind": "average_effect", "outcome": "value", "treatment": "offer",
                       "contrast": "1-versus-0"},
            "population": {"definition": "Eligible accounts at decision", "unit": "account"},
            "variables": [{"id": "offer", "role": "action", "unit": "binary"},
                          {"id": "value", "role": "outcome", "unit": "USD"}],
            "intervention": {"kind": "set", "value": "offer=1"},
            "horizon": {"value": 12, "unit": "months"}, "units": ["USD"],
            "sign_convention": "offer-minus-no-offer",
            "observation_clock": {"event_time": "event_at", "available_time": "available_at",
                                  "decision_time": "decision_at", "rule": "strict_before_decision",
                                  "alternative_justification": None},
            "sampling": {"law": "independent_units", "unit": "account", "fold_unit": "account"},
            "assumptions": [{"id": "graph_truth", "statement": "Supplied graph is valid",
                             "status": "unverified", "evidence": []}],
            "graph": {"kind": "DAG", "edges": [{"left_node": "offer", "right_node": "value",
                       "left_mark": "tail", "right_mark": "arrow", "evidence_type": "assumption",
                       "evidence_refs": [], "review_status": "unverified"}]},
            "source_evidence": []}


def request(op, params, *, ctx=None, refs=None):
    return {"schema_version": "causalbank.request/1.0.0", "request_id": "case-1",
            "operation": op, "artifact_inputs": refs or [],
            "budget": {"wall_seconds": 20, "memory_bytes": 100_000_000,
                       "max_output_bytes": 100_000, "model_calls": 0},
            "parameters": params, "scientific_context": ctx, "idempotency_key": None}


class ServiceTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".runtime").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".runtime")
        self.service = OperationService(Path(self.temp.name))

    def tearDown(self):
        self.temp.cleanup()

    def test_capabilities_exactly_advertise_implemented_subset(self):
        r = self.service.invoke(request("capabilities.describe", {}, ctx=None))
        self.assertEqual(r["result"]["payload"]["implemented"]["identify.effect"],
                         "supplied_DAG_backdoor_independent_units")
        self.assertIn("graph.discover", r["result"]["payload"]["unimplemented"])

    def test_graph_review_keeps_declared_edges(self):
        q = request("graph.review", {"review_kind": "syntax"}, ctx=context())
        r = self.service.invoke(q)
        self.assertEqual(r["result"]["payload"]["graph"], q["scientific_context"]["graph"])

    def test_backdoor_is_conditional_and_rejects_dependent_sampling(self):
        q = request("identify.effect", {"method_id": "backdoor"}, ctx=context())
        r = self.service.invoke(q)
        self.assertEqual(r["disposition"], "computed")
        self.assertEqual(r["qualification"]["level"], "conditional_inference")
        self.assertEqual(r["result"]["payload"]["expression"]["operator"], "adjustment_contrast")
        q["scientific_context"]["sampling"]["law"] = "dependent_months"
        self.assertEqual(self.service.invoke(q)["disposition"], "unsupported")

    def test_weak_moment_set_keeps_two_unbounded_components(self):
        ref = self.service.store.put({"context_sha256": context_digest(context()),
                                      "mean": [1.0, 0.0], "lrv": [[.01, 0], [0, 1]],
                                      "n": 100, "alpha": .05, "simultaneous": True},
                                     "moment-summary/1", "moment_summary")
        q = request("estimate.effect", {"engine_id": "reference-moment-sets",
                                        "estimator_id": "gaussian-residual-inversion"},
                    ctx=context(), refs=[ref])
        r = self.service.invoke(q)
        self.assertEqual(r["result"]["coordinate_sets"][0]["topology"], "unbounded_union")
        self.assertIsNone(r["result"]["coordinate_sets"][0]["intervals"][0][0])
        self.assertIsNone(r["result"]["coordinate_sets"][0]["intervals"][1][1])
        self.assertEqual(r["result"]["uncertainty"]["kind"], "joint_confidence")

    def test_quadratic_empty_and_whole_line_remain_distinct(self):
        for coeff, expected in [([1, 0, 1], "empty"), ([-1, 0, -1], "whole_line")]:
            ref = self.service.store.put({"context_sha256": context_digest(context()),
                                          "quadratics": [coeff]}, "quadratic-bounds/1", "quadratic_bounds")
            q = request("sensitivity.evaluate", {"family_id": "quadratic-sublevel"},
                        ctx=context(), refs=[ref])
            r = self.service.invoke(q)
            self.assertEqual(r["result"]["coordinate_sets"][0]["topology"], expected)
            self.assertEqual(r["result"]["uncertainty"]["kind"], "sensitivity")

    def test_clock_audit_flags_late_or_missing_available_timestamp(self):
        ref = self.service.store.put({"context_sha256": context_digest(context()), "rows": [
            {"event_at": "2026-01-01T00:00:00+00:00", "available_at": "2026-01-02T00:00:00+00:00", "decision_at": "2026-01-03T00:00:00+00:00"},
            {"event_at": "2026-01-01T00:00:00+00:00", "available_at": "2026-01-04T00:00:00+00:00", "decision_at": "2026-01-03T00:00:00+00:00"},
            {"event_at": "2026-01-01T00:00:00+00:00", "decision_at": "2026-01-03T00:00:00+00:00"},
        ]}, "observation-rows/1", "observation_rows")
        q = request("audit.observation", {"checks": ["clock"]}, ctx=context(), refs=[ref])
        r = self.service.invoke(q)
        self.assertEqual(r["result"]["payload"]["clock_failures"], [1, 2])

    def test_missing_engine_is_honestly_unsupported(self):
        q = request("graph.discover", {"algorithm_id": "oracle", "algorithm_version": "1"}, ctx=context())
        r = self.service.invoke(q)
        self.assertEqual((r["status"], r["disposition"], r["result"]),
                         ("completed", "unsupported", None))

    def test_moment_artifact_cannot_change_target_context(self):
        ref = self.service.store.put({"context_sha256": context_digest(context()),
            "mean": [1, 1], "lrv": [[1, 0], [0, 1]], "n": 100,
            "alpha": .05, "simultaneous": False}, "moment-summary/1", "moment_summary")
        changed = context(); changed["sign_convention"] = "no-offer-minus-offer"
        q = request("estimate.effect", {"engine_id": "reference-moment-sets",
            "estimator_id": "gaussian-residual-inversion"}, ctx=changed, refs=[ref])
        with self.assertRaisesRegex(ValueError, "another scientific context"):
            self.service.invoke(q)

    def test_contradicted_assumption_refuses_identification(self):
        ctx = context(); ctx["assumptions"][0]["status"] = "contradicted"
        r = self.service.invoke(request("identify.effect", {"method_id": "backdoor"}, ctx=ctx))
        self.assertEqual((r["disposition"], r["result"]), ("refused", None))

    def test_mutated_artifact_bytes_are_rejected(self):
        ref = self.service.store.put({"x": 1}, "test/1", "test")
        p = self.service.store.folder / (ref["artifact_id"] + ".json")
        p.write_text('{"x":2}')
        with self.assertRaisesRegex(ValueError, "changed"):
            self.service.store.get(ref)

    def test_artifact_root_symlink_escape_is_rejected(self):
        link = Path(self.temp.name) / "outside"
        link.symlink_to("/tmp", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "nonsymlink"):
            ArtifactStore(link)


if __name__ == "__main__":
    unittest.main()
