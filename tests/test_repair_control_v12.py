"""Behavioral V12 scope/evidence checks; fixtures are not scientific evidence."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import master_control as core
import repair_control_v12 as v12

ROOT = Path(__file__).resolve().parents[1]


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.state = core.read(ROOT, v12.DIRECTORY + "/candidate-state.json")

    def test_complete_reviewed_graph_validates_and_starts_at_installation(self):
        self.assertEqual(v12.validate_state(ROOT, self.state), [])
        self.assertEqual(v12.summary(self.state)["next"], "P12")
        self.assertFalse(v12.summary(self.state)["bounded_product_accepted"])

    def test_dropped_major_repair_is_rejected(self):
        self.state["major_repairs"].pop()
        with self.assertRaisesRegex(ValueError, "repair records"):
            v12.revision_contract(ROOT, self.state)

    def test_dropped_release_dependency_is_rejected(self):
        core.task_by_id(self.state, "X01")["depends"].pop()
        with self.assertRaisesRegex(ValueError, "contracts differ"):
            v12.revision_contract(ROOT, self.state)

    def test_original_gap_obligation_cannot_be_erased(self):
        self.state["gaps"][0]["closure_tasks"].remove("R02")
        with self.assertRaisesRegex(ValueError, "gap obligations"):
            v12.revision_contract(ROOT, self.state)

    def test_historical_result_cannot_be_rewritten(self):
        self.state["results"]["R02"]["outcome"] = "pass"
        with self.assertRaisesRegex(ValueError, "Historical results"):
            v12.revision_contract(ROOT, self.state)

    def test_dependency_cycle_is_rejected(self):
        core.task_by_id(self.state, "SW01")["depends"].append({"id": "I02", "outcomes": ["pass"]})
        self.assertIn("cycle", v12.validate_state(ROOT, self.state)[0])

    def test_negative_study_can_feed_survey_but_cannot_release_it(self):
        task = core.task_by_id(self.state, "SW09")
        for dependency in task["depends"]:
            self.state["results"][dependency["id"]] = {"outcome": "negative"}
        self.assertEqual(core.unmet(self.state, task), [])
        self.assertTrue(core.unmet(self.state, core.task_by_id(self.state, "I02")))

    def test_unavailable_engine_does_not_block_critical_study_disposition(self):
        self.state["results"]["SW07"] = {"outcome": "pass"}
        self.state["results"]["IN03"] = {"outcome": "negative"}
        self.assertEqual(core.unmet(self.state, core.task_by_id(self.state, "SW08")), [])

    def test_generic_transport_does_not_wait_for_llm_research(self):
        self.state["results"]["IN02"] = {"outcome": "pass"}
        self.assertEqual(core.unmet(self.state, core.task_by_id(self.state, "IN04")), [])


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = core.read(ROOT, v12.DIRECTORY + "/candidate-state.json")
        for name in ("coverage", "chapters", "schemas"):
            ref = self.state["repair_program"]["documents"][name]
            p = self.root / ref["path"]
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / ref["path"]).read_bytes())
        (self.root / "evidence.txt").write_text("Inspected temporary control evidence; no scientific claim.")
        self.ref = v12.reference(self.root, "evidence.txt", "Inspected fixture")
        self.task = core.task_by_id(self.state, "SW09")
        contract = core.read(self.root, self.state["repair_program"]["documents"]["coverage"]["path"])
        self.coverage = {"repair_id": "MR01", "status": "pass", "cells": [
            {"id": row["id"], "status": "substantively_reviewed", "essential": True,
             "finding": "Temporary coverage fixture", "evidence": [self.ref]}
            for row in contract["software_cells"]]}
        self.audit = {"status": "pass", "unverified_claims": [], "entries": [
            {"identity": "Fixture official documentation", "version_date": "2026-10-07",
             "inspected_anchors": ["fixture"], "supported_claims": ["fixture"], "local_copy": self.ref}]}
        chapters = core.read(self.root, self.state["repair_program"]["documents"]["chapters"]["path"])["chapters"]
        pdfpath = next(p for p in self.task["outputs"] if p.endswith(".pdf"))
        (self.root / pdfpath).parent.mkdir(parents=True, exist_ok=True)
        (self.root / pdfpath).write_bytes(b"%PDF-fixture-count-is-mocked")
        self.pdf = v12.reference(self.root, pdfpath, "Temporary PDF identity")
        self.review = {"status": "pass", "blocking_findings": [], "chapters": [
            {"id": c["id"], "substantive": True, "finding": "Temporary chapter review"}
            for c in chapters if c["repair_id"] == "MR01"], "pdf_sha256": self.pdf["sha256"],
            "rendered_pages_inspected": list(range(1, 126)), "body_page_numbers": list(range(1, 126))}

    def bind(self, name, obj):
        core.write(self.root / name, obj)
        return v12.reference(self.root, name, "Temporary inspected JSON")

    def acceptance(self):
        return {"repair_acceptance": {"coverage_complete": True, "blocking_findings": [],
            "coverage_review": self.bind("coverage.json", self.coverage),
            "source_audit": self.bind("audit.json", self.audit),
            "chapter_review": self.bind("review.json", self.review),
            "page_count": {"pdf": self.pdf, "body_page_numbers": list(range(1, 126))},
            "page_budget_exception": None}}

    def validate(self, receipt):
        with patch.object(v12, "pdf_pages", return_value=125):
            v12.validate_repair_acceptance(self.root, self.state, self.task, receipt)

    def test_structurally_complete_bound_acceptance_is_supported(self):
        self.validate(self.acceptance())

    def test_page_count_alone_cannot_close_repair(self):
        with self.assertRaisesRegex(ValueError, "structured repair acceptance"):
            self.validate({"repair_acceptance": {"page_count": 125}})

    def test_missing_coverage_cell_is_rejected(self):
        self.coverage["cells"].pop()
        with self.assertRaisesRegex(ValueError, "coverage cells"):
            self.validate(self.acceptance())

    def test_essential_unavailable_cannot_be_waived(self):
        self.coverage["cells"][0].update(status="unavailable_with_recorded_impact", omission_review=self.ref)
        with self.assertRaisesRegex(ValueError, "Essential unavailable"):
            self.validate(self.acceptance())

    def test_padded_or_unreviewed_chapters_are_rejected(self):
        self.review["chapters"][0]["substantive"] = False
        with self.assertRaisesRegex(ValueError, "substantive chapter"):
            self.validate(self.acceptance())

    def test_uninspected_rendered_page_is_rejected(self):
        self.review["rendered_pages_inspected"].pop()
        with self.assertRaisesRegex(ValueError, "Rendered review"):
            self.validate(self.acceptance())

    def test_changed_source_file_is_rejected(self):
        receipt = self.acceptance()
        (self.root / "evidence.txt").write_text("Changed after review")
        with self.assertRaisesRegex(ValueError, "changed evidence"):
            self.validate(receipt)

    def test_source_metadata_without_technical_anchors_is_rejected(self):
        self.audit["entries"][0]["inspected_anchors"] = []
        with self.assertRaisesRegex(ValueError, "inspected_anchors"):
            self.validate(self.acceptance())

    def test_duplicate_body_pages_are_rejected(self):
        receipt = self.acceptance()
        receipt["repair_acceptance"]["page_count"]["body_page_numbers"][1] = 1
        with self.assertRaisesRegex(ValueError, "repeated substantive"):
            self.validate(receipt)

    def test_old_release_cannot_pass_current_assessment(self):
        self.state["results"]["I02"] = {"outcome": "pass"}
        with self.assertRaisesRegex(ValueError, "current I02"):
            v12.validate_current_assessment(self.root, self.state,
                {"assessed_current_release": {"path": "docs/program/master/work/I01/delivery-manifest.json"}})

    def test_current_assessment_binds_the_delivered_manifest(self):
        path = v12.DIRECTORY + "/work/I02/delivery-manifest.json"
        ref = self.bind(path, {"fixture": "I02"})
        receipt_ref = self.bind("I02-receipt.json", {"criteria": [{"evidence": [ref]}]})
        self.state["results"]["I02"] = dict(receipt_ref, outcome="pass")
        receipt = {"assessed_current_release": ref, "scope_release_sha256": ref["sha256"]}
        v12.validate_current_assessment(self.root, self.state, receipt)
        receipt["scope_release_sha256"] = "stale"
        with self.assertRaisesRegex(ValueError, "Signed scope"):
            v12.validate_current_assessment(self.root, self.state, receipt)

    def test_negative_unregistered_empirical_result_cannot_pass(self):
        task = copy.deepcopy(core.task_by_id(self.state, "SW08"))
        task["outputs"] = ["evidence.txt"]
        receipt = {"task_id": "SW08", "task_contract_sha256": core.digest_object(task),
            "outcome": "negative", "reviewer": {"name": "Fixture", "kind": "author"},
            "scope": "Control fixture", "limitations": ["Not empirical evidence"],
            "gap_dispositions": {g: "unresolved" for g in task["gaps"]},
            "criteria": [{"id": c["id"], "verdict": "fail", "finding": "Fixture failed", "evidence": [self.ref]}
                         for c in task["criteria"]]}
        with self.assertRaisesRegex(ValueError, "preregistration"):
            v12.validate_receipt(self.root, self.state, task, receipt)
        receipt.update(outcome="inconclusive", evaluation_status="unavailable", unavailability_evidence=[self.ref])
        for row in receipt["criteria"]:
            row["verdict"] = "inconclusive"
        v12.validate_receipt(self.root, self.state, task, receipt)


if __name__ == "__main__":
    unittest.main()
