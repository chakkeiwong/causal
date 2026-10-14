"""Bounded local operations, durable evidence reports, and immutable replay."""
from contextlib import contextmanager
import copy
import fcntl
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

import jsonschema

from .artifacts_v12 import ArtifactStore, ROOT, atomic, bounded_read, digest, encode, local_root
from .operation_contract_v12 import validate_response
from .operation_service_v12 import (CONTRACT, OperationService, REQUEST_SCHEMA, RESPONSE_SCHEMA,
                                    SUPPORTED, envelope, request_digest, result, validate_request)

IMPLEMENTED = {**SUPPORTED, "report.build": "durable_canonical_result_summary",
               "job.status": "local_durable_job_status", "job.cancel": "cooperative_report_cancel"}
TERMINAL = {"completed", "failed", "cancelled"}


def execution_identity():
    names = ["artifacts_v12.py", "operation_contract_v12.py", "operation_service_v12.py",
             "runtime_v12.py", "worker_v12.py", "cli_v12.py", "mcp_server_v12.py",
             "responses.py", "causal_workflow.py"]
    source = {n: hashlib.sha256((ROOT / "src/causalbank" / n).read_bytes()).hexdigest() for n in names}
    source.update({n: hashlib.sha256((CONTRACT / n).read_bytes()).hexdigest()
                   for n in ["request-schema.json", "response-schema.json"]})
    versions = {n: importlib.metadata.version(n) for n in ["numpy", "scipy", "scikit-learn", "jsonschema"]}
    return {"source_sha256": digest(source), "python": sys.version, "dependencies": versions,
            "operation_version": "local-runtime/1"}


@contextmanager
def locked(path, nonblocking=False):
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | (fcntl.LOCK_NB if nonblocking else 0))
        yield
    finally:
        os.close(fd)


class Runtime:
    def __init__(self, root=ROOT / ".runtime/operation-v12"):
        self.store = ArtifactStore(root)
        self.root = self.store.root
        self.jobs = local_root(self.root / "jobs")
        self.cache = local_root(self.root / "replay")

    def _verify_refs(self, value, limit):
        if isinstance(value, dict):
            if "artifact_id" in value:
                self.store.get(value, limit=limit)
            for part in value.values():
                self._verify_refs(part, limit)
        elif isinstance(value, list):
            for part in value:
                self._verify_refs(part, limit)

    def _failure(self, request, code, message, *, rejected=False):
        return envelope(request, status="rejected" if rejected else "failed",
                        disposition="unavailable", qualification="none",
                        error={"code": code, "message": message, "retryable": False})

    def _validate(self, request, response):
        response = copy.deepcopy(response)
        response["request_id"] = request["request_id"]
        jsonschema.validate(response, RESPONSE_SCHEMA)
        validate_response(request, response)
        if len(encode(response)) > request["budget"]["max_output_bytes"]:
            return self._failure(request, "output_budget", "Canonical output exceeds budget; control error envelope is exempt")
        return response

    def invoke(self, request):
        validate_request(request)
        budget = request["budget"]
        if budget["wall_seconds"] > 300 or not 64 * 1024 * 1024 <= budget["memory_bytes"] <= 4 * 1024**3:
            return self._failure(request, "unsupported_budget", "Local bounds are 0-300 seconds and 64 MiB-4 GiB", rejected=True)
        try:
            self._verify_refs(request, min(8 * 1024 * 1024, budget["memory_bytes"] // 2))
        except (OSError, ValueError) as exc:
            return self._failure(request, "artifact_access", type(exc).__name__ + ": " + str(exc)[:150])
        op = request["operation"]
        if op in {"job.status", "job.cancel"}:
            response = self._job_query(request, cancel=op == "job.cancel")
        elif op == "report.build":
            response = self._submit_report(request)
        else:
            response = self._replay_or_run(request)
        return self._validate(request, response)

    def _replay_or_run(self, request):
        key = request.get("idempotency_key")
        if key is None:
            return self._run_sync(request)
        slot = hashlib.sha256(key.encode()).hexdigest()
        path = self.cache / (slot + ".json")
        identity = {"request_digest": request_digest(request), "execution": execution_identity()}
        with locked(self.cache / (slot + ".lock")):
            if path.exists() or path.is_symlink():
                saved = json.loads(bounded_read(path))
                if saved["identity"] != identity:
                    return self._failure(request, "idempotency_conflict", "Idempotency key refers to another request or code environment", rejected=True)
                self._verify_refs(saved["response"], 8*1024*1024)
                return saved["response"]
            response = self._run_sync(request)
            atomic(path, {"identity": identity, "response": response})
            return response

    def _command(self, request, wall_override=None):
        b = request["budget"]
        return [sys.executable, "-m", "causalbank.worker_v12",
                "--root", str(self.root), "--memory-bytes", str(b["memory_bytes"]),
                "--wall-seconds", str(wall_override if wall_override is not None else b["wall_seconds"])]

    def _env(self):
        return {"PATH": os.environ.get("PATH", ""), "PYTHONPATH": str(ROOT / "src"),
                "PYTHONUNBUFFERED": "1", "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1",
                "MKL_NUM_THREADS": "1"}

    def _run_sync(self, request):
        if request["operation"] == "capabilities.describe":
            response = OperationService(self.root).invoke(request)
            if response["result"] is None:
                return response
            payload = response["result"]["payload"]
            payload["implemented"] = IMPLEMENTED
            payload["unimplemented"] = [op for op in REQUEST_SCHEMA["properties"]["operation"]["enum"] if op not in IMPLEMENTED]
            payload["resource_bounds"] = {"max_wall_seconds": 300, "max_artifact_bytes": 8*1024*1024,
                "min_memory_bytes": 64*1024*1024, "max_memory_bytes": 4*1024**3,
                "small_control_errors_exempt_from_output_limit": True}
            return response
        b = request["budget"]
        process = subprocess.Popen(self._command(request), stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT, env=self._env())
        try:
            output, stderr = process.communicate(encode(request), timeout=b["wall_seconds"] + 1)
        except subprocess.TimeoutExpired:
            process.kill(); process.communicate()
            return self._failure(request, "wall_budget", "Worker exceeded bounded wall time and was terminated")
        if process.returncode != 0:
            return self._failure(request, "worker_failure", "Worker exited without a complete result (resource/import/runtime failure)")
        try:
            response = json.loads(output)
            return self._validate(request, response)
        except (ValueError, jsonschema.ValidationError, KeyError, TypeError):
            return self._failure(request, "worker_protocol", "Worker did not return a valid canonical result")

    def _job_path(self, job_id):
        if not isinstance(job_id, str) or not re.fullmatch(r"j[0-9a-f]{32}", job_id):
            raise ValueError("Invalid opaque job ID")
        return self.jobs / (job_id + ".json")

    def _submit_report(self, request):
        ids = request["parameters"]["artifact_ids"]
        refs = {r["artifact_id"]: r for r in request["artifact_inputs"]}
        if not ids or len(ids) > 100 or len(ids) != len(set(ids)) or not set(ids) <= set(refs):
            return self._failure(request, "report_inputs", "Report requires 1-100 distinct authorized input artifacts", rejected=True)
        for aid in ids:
            if refs[aid]["role"] != "canonical_response":
                return self._failure(request, "report_inputs", "Reports summarize typed canonical responses only", rejected=True)
            try:
                jsonschema.validate(self.store.get(refs[aid]), RESPONSE_SCHEMA)
            except jsonschema.ValidationError:
                return self._failure(request, "report_inputs", "Input is not a typed canonical response", rejected=True)
        key = request.get("idempotency_key")
        job_id = "j" + (hashlib.sha256(key.encode()).hexdigest()[:32] if key else uuid.uuid4().hex)
        path = self._job_path(job_id)
        identity = {"request_digest": request_digest(request), "execution": execution_identity(),
                    "input_hashes": [refs[x]["sha256"] for x in ids], "seed": None, "budget": request["budget"]}
        with locked(self.jobs / (job_id + ".lock")):
            if path.exists():
                state = json.loads(bounded_read(path))
                if state["identity"] != identity:
                    return self._failure(request, "idempotency_conflict", "Report job key belongs to changed inputs/code/budget", rejected=True)
            else:
                state = {"job_id": job_id, "identity": identity, "request": request,
                         "state": "queued", "cancel_requested": False, "completed_work_ids": [],
                         "summaries": [], "result_ref": None, "error": None, "created": time.time(),
                         "heartbeat": None, "worker_pid": None, "checkpoint_sha256": None,
                         "spawn_attempts": 0, "last_spawned": None}
                atomic(path, state)
        if state["state"] not in TERMINAL:
            self.resume(job_id)
        # A submission always returns a handle. Client polls its authoritative
        # state, so scheduling races cannot change the submit response.
        return envelope(request, status="queued", disposition="not_applicable",
            value=result("job", payload={"job_id": job_id, "poll_operation": "job.status"}))

    def resume(self, job_id):
        path = self._job_path(job_id)
        with locked(self.jobs / (job_id + ".lock")):
            state = json.loads(bounded_read(path))
            if state["state"] in TERMINAL:
                return state["state"]
            if state["cancel_requested"]:
                state["state"] = "cancelled"; atomic(path, state); return "cancelled"
            if state["identity"]["execution"] != execution_identity():
                raise ValueError("Cannot resume job after code or environment change")
            completed = state["completed_work_ids"]
            if completed != state["request"]["parameters"]["artifact_ids"][:len(completed)]:
                raise ValueError("Checkpoint work IDs are not a prefix of the frozen request")
            expected_checkpoint = digest({"identity": state["identity"],
                "completed": completed, "summaries": state["summaries"]}) if completed else None
            if (state["checkpoint_sha256"] != expected_checkpoint or
                    len(completed) != len(state["summaries"])):
                raise ValueError("Checkpoint content identity changed")
            if state["spawn_attempts"] >= 3:
                state.update(state="failed", error="Worker retry limit reached")
                atomic(path, state)
                return "failed"
            remaining = state["created"] + state["request"]["budget"]["wall_seconds"] - time.time()
            if remaining <= 0:
                state.update(state="failed", error="Job wall budget elapsed")
                atomic(path, state)
                return "failed"
            if state["last_spawned"] is not None and time.time() - state["last_spawned"] < .2:
                return "already_spawned"
            self._verify_refs(state["request"], 8*1024*1024)
            # A separate process-wide lease prevents overlapping workers.
            process = subprocess.Popen(self._command(state["request"], remaining) + ["--job", job_id],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                cwd=ROOT, env=self._env(), start_new_session=True)
            state["last_spawned_pid"] = process.pid
            state["last_spawned"] = time.time()
            state["spawn_attempts"] += 1
            atomic(path, state)
        return "resume_requested"

    def _job_query(self, request, cancel=False):
        job_id = request["parameters"]["job_id"]
        path = self._job_path(job_id)
        try:
            with locked(self.jobs / (job_id + ".lock")):
                state = json.loads(bounded_read(path))
                if cancel and state["state"] not in TERMINAL:
                    state["cancel_requested"] = True
                    if state["state"] == "queued":
                        state["state"] = "cancelled"
                    atomic(path, state)
        except FileNotFoundError:
            return self._failure(request, "unknown_job", "Job does not exist in this operator store", rejected=True)
        if state["state"] not in TERMINAL:
            try:
                with locked(self.jobs / (job_id + ".worker"), nonblocking=True):
                    orphaned = True
            except BlockingIOError:
                orphaned = False
            if orphaned:
                if state["cancel_requested"]:
                    with locked(self.jobs / (job_id + ".lock")):
                        state = json.loads(bounded_read(path))
                        if state["state"] not in TERMINAL:
                            state["state"] = "cancelled"
                            atomic(path, state)
                else:
                    try:
                        self.resume(job_id)
                    except (ValueError, OSError) as exc:
                        with locked(self.jobs / (job_id + ".lock")):
                            state = json.loads(bounded_read(path))
                            if state["state"] not in TERMINAL:
                                state.update(state="failed", error="Resume refused: " + str(exc)[:150])
                                atomic(path, state)
                state = json.loads(bounded_read(path))
        payload = {k: state[k] for k in ["job_id", "state", "cancel_requested", "completed_work_ids",
                                       "result_ref", "error", "checkpoint_sha256", "spawn_attempts"]}
        return envelope(request, value=result("job", payload=payload))

    def run_report_job(self, job_id):
        try:
            with locked(self.jobs / (job_id + ".worker"), nonblocking=True):
                self._report_worker(job_id)
        except BlockingIOError:
            return
        except Exception as exc:
            path = self._job_path(job_id)
            with locked(self.jobs / (job_id + ".lock")):
                state = json.loads(bounded_read(path))
                if state["state"] not in TERMINAL:
                    state.update(state="failed", error=type(exc).__name__ + ": " + str(exc)[:180])
                    atomic(path, state)

    def _report_worker(self, job_id):
        path = self._job_path(job_id)
        with locked(self.jobs / (job_id + ".lock")):
            state = json.loads(bounded_read(path))
            if state["state"] in TERMINAL:
                return
            if state["identity"]["execution"] != execution_identity():
                raise ValueError("Job execution identity changed")
            if state["completed_work_ids"]:
                expected = digest({"identity": state["identity"],
                    "completed": state["completed_work_ids"], "summaries": state["summaries"]})
                if state["checkpoint_sha256"] != expected:
                    raise ValueError("Checkpoint digest mismatch")
            if state["cancel_requested"]:
                state["state"] = "cancelled"; atomic(path, state); return
            state.update(state="running", worker_pid=os.getpid(), heartbeat=time.time())
            atomic(path, state)
        req = state["request"]
        refs = {r["artifact_id"]: r for r in req["artifact_inputs"]}
        for aid in req["parameters"]["artifact_ids"]:
            with locked(self.jobs / (job_id + ".lock")):
                state = json.loads(bounded_read(path))
                if state["cancel_requested"]:
                    state["state"] = "cancelled"; atomic(path, state); return
                if aid in state["completed_work_ids"]:
                    continue
            response = self.store.get(refs[aid])
            jsonschema.validate(response, RESPONSE_SCHEMA)
            summary = {"operation": response["operation"],
                       "declared_status": response["status"],
                       "declared_disposition": response["disposition"],
                       "declared_context_sha256": response["context_sha256"],
                       "declared_qualification": response["qualification"],
                       "verification": "schema_only_not_causal_or_external_review"}
            summary["source"] = refs[aid]
            with locked(self.jobs / (job_id + ".lock")):
                state = json.loads(bounded_read(path))
                if state["cancel_requested"]:
                    state["state"] = "cancelled"; atomic(path, state); return
                state["summaries"].append(summary); state["completed_work_ids"].append(aid)
                state["heartbeat"] = time.time()
                state["checkpoint_sha256"] = digest({"identity": state["identity"],
                    "completed": state["completed_work_ids"], "summaries": state["summaries"]})
                atomic(path, state)
        with locked(self.jobs / (job_id + ".lock")):
            state = json.loads(bounded_read(path))
            if state["cancel_requested"]:
                state["state"] = "cancelled"; atomic(path, state); return
            report = {"schema_version": "causalbank.report/1", "request_digest": request_digest(req),
                      "summaries": state["summaries"],
                      "limitation": "Operator-supplied results summarized as declarations; no independent scientific validation or promotion"}
            if len(encode(report)) > req["budget"]["max_output_bytes"]:
                raise ValueError("Report exceeds declared output byte budget")
            ref = self.store.put(report, "causalbank.report/1", "report")
            state.update(state="completed", result_ref=ref, heartbeat=time.time())
            atomic(path, state)
