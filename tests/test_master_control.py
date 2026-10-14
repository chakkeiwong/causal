"""Behavioral regression checks for scientific program controls, using temp files."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import master_control as m


class MasterControlTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = m.read(m.ROOT, m.STATE)
        self.state.update(results={}, registrations={}, input_receipts={}, events=[], attempts=[])
        (self.root / "evidence.txt").write_text("Independent fixture and inspected finding.\n")
        self.ref = self.reference("evidence.txt")

    def reference(self, name):
        return dict(path=name, sha256=m.sha(self.root / name), anchor="Inspected finding")

    def task(self, name="M00"):
        t = copy.deepcopy(m.task_by_id(self.state, name))
        t["outputs"] = ["evidence.txt"]
        return t

    def receipt(self, task, outcome="pass"):
        return dict(task_id=task["id"], task_contract_sha256=m.digest_object(task),
            outcome=outcome, reviewer=dict(name="Test author", kind="author"),
            scope="Temporary control fixture only", limitations=["Not research evidence"],
            gap_dispositions={} if task["kind"] == "control" else {g: "conditional_progress" for g in task["gaps"]},
            criteria=[dict(id=c["id"], verdict="fail" if i == 0 and outcome == "negative" else
                ("inconclusive" if i == 0 and outcome == "inconclusive" else "pass"),
                finding="Inspected fixture finding", evidence=[self.ref])
                for i, c in enumerate(task["criteria"])])

    def register_fixture(self, task):
        spec = {k: "Declared before evaluation" for k in m.PROTOCOL_FIELDS}
        spec.update(task_id=task["id"], task_contract_sha256=m.digest_object(task),
            replications=100, seed=123, stopping_rule="fixed_design_no_outcome_stopping",
            derivation_review=self.ref, input_sha256={"evidence.txt": self.ref["sha256"]})
        m.write(self.root / "protocol.json", spec)
        registration = dict(self.reference("protocol.json"), registered_at="2026-10-11T01:00:00+00:00")
        self.state["registrations"][task["id"]] = registration
        return registration

    def test_initial_state_has_one_ready_recovery_task(self):
        self.assertEqual(m.validate_state(self.root, self.state), [])
        summary = m.summary(self.state)
        self.assertEqual(summary["next"], "M00")
        self.assertFalse(summary["bounded_product_accepted"])
        self.assertEqual(summary["qualified_gaps_in_declared_scope"], [])

    def test_missing_original_gap_is_rejected(self):
        self.state["gaps"].pop()
        self.assertTrue(m.validate_state(self.root, self.state))

    def test_cycle_is_rejected(self):
        m.task_by_id(self.state, "M00")["depends"] = [{"id": "M03", "outcomes": ["pass"]}]
        self.assertIn("cycle", m.validate_state(self.root, self.state)[0])

    def test_unknown_dependency_is_rejected(self):
        m.task_by_id(self.state, "M00")["depends"] = [{"id": "UNKNOWN", "outcomes": ["pass"]}]
        self.assertIn("Unknown", m.validate_state(self.root, self.state)[0])

    def test_negative_result_permits_integration_but_not_acceptance(self):
        for name in ("R01", "R02", "R03", "R04", "R05", "E01"):
            self.state["results"][name] = {"outcome": "negative"}
        self.assertEqual(m.unmet(self.state, m.task_by_id(self.state, "I01")), [])
        self.assertTrue(m.unmet(self.state, m.task_by_id(self.state, "F01")))
        self.assertFalse(m.summary(self.state)["bounded_product_accepted"])

    def test_passing_packages_do_not_automatically_qualify_gaps(self):
        for task in self.state["work_packages"]:
            self.state["results"][task["id"]] = {"outcome": "pass",
                "gap_dispositions": {g: "conditional_progress" for g in task["gaps"]}}
        self.assertEqual(m.summary(self.state)["qualified_gaps_in_declared_scope"], [])
        self.assertTrue(m.unmet(self.state, m.task_by_id(self.state, "F01")))

    def test_negative_work_cannot_qualify_a_gap(self):
        t = self.task("R01")
        r = self.receipt(t, "negative")
        r["gap_dispositions"]["D09"] = "qualified_in_declared_scope"
        with self.assertRaisesRegex(ValueError, "cannot qualify"):
            m.validate_receipt(self.root, self.state, t, r)

    def test_passing_receipt_needs_every_promised_output(self):
        t = self.task()
        t["outputs"].append("missing-output.json")
        with self.assertRaisesRegex(ValueError, "promised outputs"):
            m.validate_receipt(self.root, self.state, t, self.receipt(t))

    def test_evidence_tampering_is_rejected(self):
        t = self.task()
        r = self.receipt(t)
        (self.root / "evidence.txt").write_text("Replaced after review")
        with self.assertRaisesRegex(ValueError, "changed evidence"):
            m.validate_receipt(self.root, self.state, t, r)

    def test_changed_contract_invalidates_receipt(self):
        t = self.task()
        r = self.receipt(t)
        t["criteria"][0]["statement"] = "A weaker post-hoc standard"
        with self.assertRaisesRegex(ValueError, "another work-package"):
            m.validate_receipt(self.root, self.state, t, r)

    def test_empty_or_duplicate_criteria_cannot_complete(self):
        t = self.task()
        r = self.receipt(t)
        r["criteria"][-1] = r["criteria"][0]
        with self.assertRaisesRegex(ValueError, "criterion"):
            m.validate_receipt(self.root, self.state, t, r)

    def test_research_pass_requires_registered_evaluation(self):
        t = self.task("R01")
        with self.assertRaisesRegex(ValueError, "registered evaluation"):
            m.validate_receipt(self.root, self.state, t, self.receipt(t))

    def test_analytical_negative_does_not_require_fake_draws(self):
        t = self.task("R01")
        m.validate_receipt(self.root, self.state, t, self.receipt(t, "negative"))

    def test_evaluation_before_registration_is_rejected(self):
        t = self.task("R01")
        registration = self.register_fixture(t)
        r = self.receipt(t)
        r["experiment"] = dict(registration_sha256=registration["sha256"],
            started_at="2026-10-11T00:59:59+00:00", journal=self.ref, retained_failures=True)
        with self.assertRaisesRegex(ValueError, "before registration"):
            m.validate_receipt(self.root, self.state, t, r)

    def test_registered_evaluation_with_preserved_journal_is_accepted(self):
        t = self.task("R01")
        registration = self.register_fixture(t)
        r = self.receipt(t)
        r["experiment"] = dict(registration_sha256=registration["sha256"],
            started_at="2026-10-11T01:00:01+00:00", journal=self.ref, retained_failures=True)
        m.validate_receipt(self.root, self.state, t, r)
        r["experiment"]["retained_failures"] = False
        with self.assertRaisesRegex(ValueError, "retain failed"):
            m.validate_receipt(self.root, self.state, t, r)

    def test_author_cannot_complete_external_review(self):
        t = self.task("X01")
        with self.assertRaisesRegex(ValueError, "Author review"):
            m.validate_receipt(self.root, self.state, t, self.receipt(t))

    def test_placeholder_external_owner_is_rejected(self):
        row = dict(input_id="bank_truth", origin="external",
            owner=dict(name="unassigned", role="Source owner", organization="Bank"),
            baseline_manifest_sha256=self.state["baseline_manifest_sha256"],
            scope="Fake fixture", agreed_criteria=["Eligibility"], signed_evidence=self.ref,
            input_sha256={"evidence.txt": self.ref["sha256"]})
        m.write(self.root / "intake.json", row)
        with self.assertRaisesRegex(ValueError, "identified owner"):
            m.validate_intake(self.root, self.state, "bank_truth", self.reference("intake.json"))

    def test_receipt_cannot_escape_repository(self):
        with self.assertRaisesRegex(ValueError, "relative"):
            m.safe(self.root, "../other-repo/secrets")
        (self.root / "outside").symlink_to(Path("/etc/passwd"))
        with self.assertRaisesRegex(ValueError, "escapes"):
            m.safe(self.root, "outside")

    def tex_fixture(self, a, b):
        (self.root / "docs/literature").mkdir(parents=True)
        m.write(self.root / "docs/literature/sources.json", [])
        (self.root / "docs/a.tex").write_text(a)
        (self.root / "docs/b.tex").write_text(b)
        return m.source_check(self.root, ["docs/a.tex", "docs/b.tex"])

    def test_same_equation_label_in_separate_documents_is_valid(self):
        result = self.tex_fixture(r"\label{eq:score}\eqref{eq:score}", r"\label{eq:score}\eqref{eq:score}")
        self.assertEqual(result["issues"], [])

    def test_duplicate_label_in_one_document_is_rejected(self):
        result = self.tex_fixture(r"\label{x}\label{x}", "")
        self.assertTrue(any("Duplicate label" in i for i in result["issues"]))

    def test_reference_cannot_leak_from_another_document(self):
        result = self.tex_fixture(r"\label{x}", r"\eqref{x}")
        self.assertTrue(any("Missing label" in i for i in result["issues"]))

    def test_repeated_input_is_not_silently_deduplicated(self):
        self.tex_fixture("", "")
        (self.root / "docs/part.tex").write_text(r"\label{x}")
        (self.root / "docs/a.tex").write_text(r"\input{part}\input{part}")
        result = m.source_check(self.root, ["docs/a.tex"])
        self.assertTrue(any("Duplicate label" in i for i in result["issues"]))

    def test_reopen_retains_negative_attempt_and_resets_only_that_task(self):
        t = m.task_by_id(self.state, "R01")
        r = self.receipt(t, "negative")
        m.write(self.root / "negative.json", r)
        self.state["results"]["R01"] = dict(self.reference("negative.json"), outcome="negative")
        replacement = copy.deepcopy(t)
        replacement["outputs"] = ["attempt2/" + Path(p).name for p in t["outputs"]]
        revision = dict(task_id="R01", prior_contract_sha256=m.digest_object(t),
            reason="Retained counterexample", new_information_or_argument="Revised observation design",
            review=self.ref, new_contract=replacement)
        m.write(self.root / "revision.json", revision)
        m.reopen_task(self.root, self.state, "R01", self.reference("revision.json"))
        self.assertNotIn("R01", self.state["results"])
        self.assertEqual(self.state["attempts"][0]["result"]["outcome"], "negative")
        self.assertEqual(m.validate_state(self.root, self.state), [])

    def test_reopen_cannot_invalidate_resolved_downstream_work(self):
        self.state["results"] = {"R01": {"outcome": "negative"}, "I01": {"outcome": "pass"}}
        with self.assertRaisesRegex(ValueError, "downstream"):
            m.reopen_task(self.root, self.state, "R01", {})

    def test_atomic_update_rejects_a_stale_state_without_writing(self):
        m.write(self.root / m.STATE, self.state)
        before = (self.root / m.STATE).read_bytes()
        with self.assertRaisesRegex(ValueError, "State changed"):
            m.commit_state(self.root, "0" * 64, self.state, {"action": "test"})
        self.assertEqual(before, (self.root / m.STATE).read_bytes())


if __name__ == "__main__":
    unittest.main()
