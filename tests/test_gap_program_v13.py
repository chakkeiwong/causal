"""Meaningful mutation checks for the successor program's evidence boundaries."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import master_control as core
import causal_program_v13 as control


class ProgramTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = json.loads((ROOT / control.BASE / "candidate-state.json").read_text())
        control.install_hooks()

    def test_valid_candidate(self):
        self.assertEqual(control.validate_state(ROOT, self.state), [])

    def test_historical_failure_cannot_be_rewritten(self):
        state=copy.deepcopy(self.state);state["results"]["R02"]["outcome"]="pass"
        self.assertTrue(any("Historical" in x or "historical" in x for x in control.validate_state(ROOT,state)))

    def test_successor_cannot_be_dropped(self):
        state=copy.deepcopy(self.state)
        state["work_packages"]=[t for t in state["work_packages"] if t["id"]!="R03S"]
        self.assertTrue(control.validate_state(ROOT,state))

    def test_old_terminal_gate_cannot_be_silently_restored(self):
        state=copy.deepcopy(self.state);state["gaps"][0]["closure_tasks"]=["R01","R02","X02"]
        self.assertTrue(control.validate_state(ROOT,state))

    def test_live_dependencies_enforced(self):
        task=core.task_by_id(self.state,"LA06S")
        missing=core.unmet(self.state,task)
        for name in task["requires_inputs"]:
            self.assertIn("missing external input "+name,missing)

    def test_live_input_cannot_be_removed(self):
        state=copy.deepcopy(self.state);state["external_inputs"].pop()
        self.assertTrue(control.validate_state(ROOT,state))

    def test_all_old_task_contracts_preserved_except_unresolved_final(self):
        prior=json.loads((ROOT/self.state["gap_execution"]["predecessor"]["path"]).read_text())
        for task in prior["work_packages"]:
            if task["id"]!="F01":self.assertEqual(task,core.task_by_id(self.state,task["id"]))

    def test_f01_requires_all_successors(self):
        deps={d["id"] for d in core.task_by_id(self.state,"F01")["depends"] if d["outcomes"]==["pass"]}
        self.assertTrue({"R02S","R03S","R04S","R05S","E01S","LA06S"}<=deps)

    def test_blocked_successor_design_cannot_be_registered(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);task=core.task_by_id(self.state,"R02S")
            review={"task_id":"R02S","design_approved":False,
                    "unresolved_design_blockers":["Calendar covariance remains unknown"],
                    "scope_matches_contract":True,"retained_predecessor_failures":True}
            core.write(root/"review.json",review)
            ref={"path":"review.json","sha256":core.sha(root/"review.json"),"anchor":"Unresolved proof"}
            spec={k:"Declared" for k in core.PROTOCOL_FIELDS}
            spec.update(task_id="R02S",task_contract_sha256=core.digest_object(task),
                        replications=512,seed=2026101201,stopping_rule="fixed_design_no_outcome_stopping",
                        derivation_review=ref,successor_review=ref,input_sha256={"review.json":ref["sha256"]})
            core.write(root/"protocol.json",spec)
            registration={"path":"protocol.json","sha256":core.sha(root/"protocol.json"),
                          "anchor":"Proposed design","registered_at":"2026-10-12T10:00:00+00:00"}
            with self.assertRaisesRegex(ValueError,"approved successor"):
                control.validate_protocol(root,task,registration)

    def test_author_cannot_fill_external_intake(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            core.write(root/"intake.json",{"input_id":"live_backend_custody","origin":"external",
                        "owner":{"name":"author","role":"owner","organization":"repo"}})
            ref={"path":"intake.json","sha256":core.sha(root/"intake.json"),"anchor":"Unowned packet"}
            with self.assertRaisesRegex(ValueError,"identified owner"):
                core.validate_intake(root,self.state,"live_backend_custody",ref)


if __name__ == "__main__":
    unittest.main()
