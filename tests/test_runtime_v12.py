"""Subprocess, persistence and replay checks for the local V12 runtime."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))
from causalbank.runtime_v12 import Runtime
from test_operation_service_v12 import context, request


def bounded(q):
    q["budget"] = {"wall_seconds": 10, "memory_bytes": 1024**3,
                   "max_output_bytes": 100000, "model_calls": 0}
    return q


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".runtime").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".runtime")
        self.runtime = Runtime(Path(self.temp.name))

    def tearDown(self):
        self.temp.cleanup()

    def cap_request(self):
        return bounded(request("capabilities.describe", {}, ctx=None))

    def job_request(self, job_id, operation="job.status"):
        return bounded(request(operation, {"job_id": job_id}, ctx=None))

    def wait(self, job_id, seconds=8):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            value = self.runtime.invoke(self.job_request(job_id))["result"]["payload"]
            if value["state"] in {"completed", "failed", "cancelled"}:
                return value
            time.sleep(.03)
        self.fail("Durable job did not reach a terminal state")

    def test_sync_worker_and_exact_capabilities(self):
        r = self.runtime.invoke(self.cap_request())
        self.assertEqual(r["status"], "completed")
        self.assertIn("report.build", r["result"]["payload"]["implemented"])
        self.assertIn("job.cancel", r["result"]["payload"]["implemented"])
        self.assertNotIn("graph.discover", r["result"]["payload"]["implemented"])

    def test_replay_preserves_result_but_rejects_changed_request(self):
        q = self.cap_request(); q["idempotency_key"] = "same-replay"
        first = self.runtime.invoke(q)
        again = copy.deepcopy(q); again["request_id"] = "different-correlation"
        replay = self.runtime.invoke(again)
        self.assertEqual(replay["request_id"], "different-correlation")
        first["request_id"] = "different-correlation"
        self.assertEqual(first, replay)
        again["budget"]["wall_seconds"] = 9
        conflict = self.runtime.invoke(again)
        self.assertEqual((conflict["status"], conflict["error"]["code"]),
                         ("rejected", "idempotency_conflict"))

    def test_report_job_publishes_schema_only_summary(self):
        cap = self.runtime.invoke(self.cap_request())
        ref = self.runtime.store.put(cap, "causalbank.response/1.0.0", "canonical_response")
        q = bounded(request("report.build", {"artifact_ids": [ref["artifact_id"]]}, ctx=None, refs=[ref]))
        q["idempotency_key"] = "same-report"
        first = self.runtime.invoke(q)
        self.assertEqual(first["status"], "queued")
        job_id = first["result"]["payload"]["job_id"]
        self.assertEqual(job_id, self.runtime.invoke(q)["result"]["payload"]["job_id"])
        state = self.wait(job_id)
        self.assertEqual(state["state"], "completed", state["error"])
        report = self.runtime.store.get(state["result_ref"])
        self.assertEqual(report["summaries"][0]["verification"],
                         "schema_only_not_causal_or_external_review")

    def test_report_job_can_cancel_without_false_rollback(self):
        cap = self.runtime.invoke(self.cap_request())
        refs = [self.runtime.store.put({**cap, "request_id": f"cap-{i}"},
                   "causalbank.response/1.0.0", "canonical_response") for i in range(100)]
        q = bounded(request("report.build", {"artifact_ids": [x["artifact_id"] for x in refs]},
                            ctx=None, refs=refs))
        q["budget"]["max_output_bytes"] = 2_000_000
        job_id = self.runtime.invoke(q)["result"]["payload"]["job_id"]
        cancel = self.runtime.invoke(self.job_request(job_id, "job.cancel"))["result"]["payload"]
        state = self.wait(job_id)
        self.assertIn(state["state"], {"cancelled", "completed"})
        if state["state"] == "cancelled":
            self.assertIsNone(state["result_ref"])
        else:
            self.assertIsNotNone(state["result_ref"])
        self.assertEqual(cancel["job_id"], job_id)

    def test_cli_is_same_canonical_service_and_exit_zero_is_not_qualification(self):
        q = self.cap_request()
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src"),
               "CAUSALBANK_STATE_ROOT": str(self.runtime.root)}
        proc = subprocess.run([sys.executable, "-m", "causalbank.cli_v12", "operation",
                               "capabilities.describe"], input=json.dumps(q), text=True,
                              capture_output=True, env=env, timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), self.runtime.invoke(q))
        bad = copy.deepcopy(q); bad["extra_shell"] = "id"
        fail = subprocess.run([sys.executable, "-m", "causalbank.cli_v12", "operation",
                               "capabilities.describe"], input=json.dumps(bad), text=True,
                              capture_output=True, env=env, timeout=10)
        self.assertEqual(fail.returncode, 2)
        self.assertIn("invalid_request", json.loads(fail.stdout)["error"]["code"])


if __name__ == "__main__":
    unittest.main()
