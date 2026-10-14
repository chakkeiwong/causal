#!/usr/bin/env python3
"""Bounded local IN04 trial. Only fixed causal workers; no network or sibling writes."""
import asyncio
import copy
from datetime import timedelta
import hashlib
import json
import os
from pathlib import Path
import signal
import selectors
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.shared.exceptions import McpError
from causalbank.artifacts_v12 import atomic, bounded_read
from causalbank.operation_contract_v12 import context_digest
from causalbank.runtime_v12 import Runtime, execution_identity
from test_operation_service_v12 import context, request

OUT = ROOT / "docs/program/repair-v12/work/IN04"


def bound(q):
    q["budget"] = {"wall_seconds": 20, "memory_bytes": 1024**3,
                   "max_output_bytes": 200000, "model_calls": 0}
    return q


def cases(runtime):
    values = [("capabilities", bound(request("capabilities.describe", {}))),
              ("graph", bound(request("graph.review", {"review_kind": "syntax"}, ctx=context()))),
              ("backdoor", bound(request("identify.effect", {"method_id": "backdoor"}, ctx=context())))]
    for name, coeff in [("finite", [1, 0, -1]), ("whole_line", [-1, 0, -1]),
                        ("empty", [1, 0, 1]), ("disconnected_unbounded", [-1, 0, 1])]:
        ref = runtime.store.put({"context_sha256": context_digest(context()), "quadratics": [coeff]},
                                "quadratic-bounds/1", "quadratic_bounds")
        values.append((name, bound(request("sensitivity.evaluate", {"family_id": "quadratic-sublevel"},
                       ctx=context(), refs=[ref]))))
    ref = runtime.store.put({"context_sha256": context_digest(context()), "mean": [1.0, 0.0],
        "lrv": [[.01, 0], [0, 1]], "n": 100, "alpha": .05, "simultaneous": True},
        "moment-summary/1", "moment_summary")
    values.append(("weak_moment", bound(request("estimate.effect", {"engine_id": "reference-moment-sets",
        "estimator_id": "gaussian-residual-inversion"}, ctx=context(), refs=[ref]))))
    values.append(("unsupported_method", bound(request("estimate.effect",
        {"engine_id": "absent-engine", "estimator_id": "none"}, ctx=context()))))
    contradicted = context(); contradicted["assumptions"][0]["status"] = "contradicted"
    values.append(("refused_premise", bound(request("identify.effect", {"method_id": "backdoor"}, ctx=contradicted))))
    ref = runtime.store.put({"context_sha256": context_digest(context()), "rows": [
        {"event_at": "2026-01-01T00:00:00+00:00", "available_at": "2026-01-03T00:00:00+00:00",
         "decision_at": "2026-01-02T00:00:00+00:00"}]}, "observation-rows/1", "observation_rows")
    values.append(("late_observation", bound(request("audit.observation", {"checks": ["clock"]},
                   ctx=context(), refs=[ref]))))
    for i, (name, q) in enumerate(values):
        q["request_id"] = f"conformance-{i}-{name}"
    return values


def environment(runtime):
    return {"PATH": os.environ.get("PATH", ""), "PYTHONPATH": str(ROOT / "src"),
            "CAUSALBANK_STATE_ROOT": str(runtime.root), "OPENBLAS_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "PYTHONUNBUFFERED": "1"}


def cli(runtime, q):
    p = subprocess.run([sys.executable, "-m", "causalbank.cli_v12", "operation", q["operation"]],
        input=json.dumps(q), text=True, capture_output=True, timeout=25, env=environment(runtime), cwd=ROOT)
    return p.returncode, json.loads(p.stdout)


def version_negotiation(runtime):
    rows = []
    for requested in ["2024-11-05", "2026-07-28"]:
        p = subprocess.Popen([sys.executable, "-m", "causalbank.mcp_server_v12"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=environment(runtime), cwd=ROOT, text=True)
        try:
            message = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": requested, "capabilities": {},
                "clientInfo": {"name": "bounded-version-probe", "version": "1"}}}
            p.stdin.write(json.dumps(message) + "\n"); p.stdin.flush()
            with selectors.DefaultSelector() as selector:
                selector.register(p.stdout, selectors.EVENT_READ)
                if not selector.select(timeout=6):
                    raise AssertionError("Initialization response timed out")
                response = json.loads(p.stdout.readline())
            assert response["result"]["protocolVersion"] == "2025-11-25"
            rows.append({"requested": requested, "advertised": "2025-11-25",
                         "meaning": "Legacy negotiation selects only the supported pinned revision; modern-only clients must disconnect"})
        finally:
            p.terminate()
            try:
                p.communicate(timeout=3)
            except subprocess.TimeoutExpired:
                p.kill(); p.communicate()
    return rows


async def transport_trial(runtime, selected):
    transcript = []
    params = StdioServerParameters(command=sys.executable, args=["-m", "causalbank.mcp_server_v12"],
                                    env=environment(runtime), cwd=str(ROOT))
    with (OUT / "mcp-stderr.log").open("w") as errors:
        async with stdio_client(params, errlog=errors) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=25)) as session:
                init = await session.initialize()
                assert init.protocolVersion == "2025-11-25"
                listed = await session.list_tools()
                names = [t.name for t in listed.tools]
                assert len(names) == 9
                for name, q in selected:
                    expected = runtime.invoke(q)
                    code, cmd = cli(runtime, q)
                    tool = "causal_" + q["operation"].replace(".", "_")
                    actual = await session.call_tool(tool, arguments=q)
                    same = expected == cmd == actual.structuredContent
                    text_same = bool(actual.content) and json.loads(actual.content[0].text) == expected
                    assert code == 0 and same and text_same and not actual.isError, (name, code, actual)
                    transcript.append({"case": name, "request": q, "library": expected,
                        "cli": cmd, "mcp": actual.model_dump(mode="json", by_alias=True),
                        "cli_exit": code, "equal": same, "text_equal": text_same})
                bad = copy.deepcopy(selected[0][1]); bad["shell"] = "touch unauthorized"
                rejected = False
                try:
                    runtime.invoke(bad)
                except Exception:
                    rejected = True
                code, cmd = cli(runtime, bad)
                invalid = await session.call_tool("causal_capabilities_describe", arguments=bad)
                assert rejected and code == 2 and invalid.isError
                unknown_code = None
                try:
                    await session.call_tool("causal_unavailable_tool", arguments={})
                except McpError as exc:
                    unknown_code = exc.error.code
                assert unknown_code == -32602
                # Resource reads expose only bounded reports/summaries, never the
                # scientific input data artifacts used by these operations.
                resource_ref = runtime.store.put({"finding": "Local reference evidence only"},
                    "evidence-summary/1", "evidence_summary")
                resources = await session.list_resources()
                assert all("causal-artifact:" in str(r.uri) for r in resources.resources)
                got = await session.read_resource("causal-artifact://" + resource_ref["artifact_id"])
                assert json.loads(got.contents[0].text) == runtime.store.get(resource_ref)
                # Real MCP report submission and terminal status/cancel parity.
                cap = runtime.invoke(selected[0][1])
                ref = runtime.store.put(cap, "causalbank.response/1.0.0", "canonical_response")
                q = bound(request("report.build", {"artifact_ids": [ref["artifact_id"]]}, refs=[ref]))
                q["idempotency_key"] = "transport-report"
                expected = runtime.invoke(q)
                code, cmd = cli(runtime, q)
                rpc = await session.call_tool("causal_report_build", arguments=q)
                assert expected == cmd == rpc.structuredContent and code == 0
                job_id = expected["result"]["payload"]["job_id"]
                terminal = await asyncio.to_thread(wait_job, runtime, job_id)
                assert terminal["state"] == "completed"
                for op in ["job.status", "job.cancel"]:
                    jq = job_query(job_id, op)
                    expected = runtime.invoke(jq)
                    code, cmd = cli(runtime, jq)
                    rpc = await session.call_tool("causal_" + op.replace(".", "_"), arguments=jq)
                    assert expected == cmd == rpc.structuredContent and code == 0
                invalid_resource_ref = selected[3][1]["artifact_inputs"][0]
                raw_resource_denied = False
                try:
                    await session.read_resource("causal-artifact://" + invalid_resource_ref["artifact_id"])
                except McpError:
                    raw_resource_denied = True
                assert raw_resource_denied
                return {"status": "pass", "protocol": init.protocolVersion, "tool_names": names,
                        "scientific_cases": len(transcript), "invalid_request_rejected_all_surfaces": True,
                        "unknown_tool_protocol_error_code": unknown_code, "bounded_resource_read_pass": True,
                        "report_submit_terminal_status_cancel_parity": True,
                        "raw_input_resource_denied": True,
                        "transcript": transcript,
                        "limits": ["Local stdio in approved execution environment; not bank platform acceptance",
                                   "Modern MCP and HTTP transport are not implemented"]}


def job_query(job, op="job.status"):
    return bound(request(op, {"job_id": job}))


def wait_job(runtime, job, seconds=24):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        payload = runtime.invoke(job_query(job))["result"]["payload"]
        if payload["state"] in {"completed", "failed", "cancelled"}:
            return payload
        time.sleep(.03)
    raise AssertionError("Job deadline exceeded")


def report_request(runtime, number=100):
    cap = runtime.invoke(bound(request("capabilities.describe", {})))
    refs = [runtime.store.put({**cap, "request_id": f"saved-result-{i}"},
        "causalbank.response/1.0.0", "canonical_response") for i in range(number)]
    q = bound(request("report.build", {"artifact_ids": [x["artifact_id"] for x in refs]}, refs=refs))
    q["budget"]["max_output_bytes"] = 2_000_000
    return q


def faults(runtime, selected):
    results = []
    q = copy.deepcopy(selected[3][1]); q["idempotency_key"] = "replay-check"
    first = runtime.invoke(q); second = runtime.invoke(q)
    assert first == second
    q["budget"]["wall_seconds"] -= 1
    collision = runtime.invoke(q)
    assert collision["error"]["code"] == "idempotency_conflict"
    results.append({"case": "replay_and_conflicting_budget", "status": "pass"})
    q = copy.deepcopy(selected[3][1]); q["budget"]["wall_seconds"] = .000001
    expired = runtime.invoke(q)
    assert expired["status"] == "failed"
    results.append({"case": "bounded_timeout", "status": "pass", "response": expired})
    q = copy.deepcopy(selected[3][1]); q["budget"]["max_output_bytes"] = 1
    output = runtime.invoke(q)
    assert output["status"] == "failed" and output["error"]["code"] == "output_budget"
    results.append({"case": "bounded_output", "status": "pass", "response": output})
    q = copy.deepcopy(selected[3][1]); q["budget"]["memory_bytes"] = 64 * 1024 * 1024
    memory = runtime.invoke(q)
    assert memory["status"] == "failed"
    results.append({"case": "worker_memory_limit", "status": "pass", "response": memory})
    q = report_request(runtime); sub = runtime.invoke(q)
    job = sub["result"]["payload"]["job_id"]; path = runtime._job_path(job)
    killed = None
    for _ in range(700):
        state = json.loads(bounded_read(path))
        if state["state"] == "running" and 1 <= len(state["completed_work_ids"]) < 100:
            killed = {"pid": state["worker_pid"], "completed": len(state["completed_work_ids"]),
                      "checkpoint_sha256": state["checkpoint_sha256"]}
            os.kill(killed["pid"], signal.SIGKILL)
            break
        if state["state"] in {"completed", "failed", "cancelled"}:
            break
        time.sleep(.01)
    assert killed is not None, "No mid-report worker fault injected"
    time.sleep(.22)
    recovered = wait_job(runtime, job)
    assert recovered["state"] == "completed", recovered
    assert len(recovered["completed_work_ids"]) == 100 and len(set(recovered["completed_work_ids"])) == 100
    report = runtime.store.get(recovered["result_ref"])
    assert len(report["summaries"]) == 100
    results.append({"case": "kill_restart_checkpoint", "status": "pass",
                    "fault": killed, "terminal": recovered})
    q = report_request(runtime); q["idempotency_key"] = "cancel-check"
    job = runtime.invoke(q)["result"]["payload"]["job_id"]
    cancel = runtime.invoke(job_query(job, "job.cancel"))
    terminal = wait_job(runtime, job)
    assert terminal["state"] == "cancelled" and terminal["result_ref"] is None
    results.append({"case": "cooperative_cancellation", "status": "pass",
                    "response": cancel, "terminal": terminal})
    ref = runtime.store.put({"x": 1}, "test/1", "test")
    path = runtime.store.folder / (ref["artifact_id"] + ".json")
    original = path.read_bytes(); path.write_text('{"x":2}')
    refused = False
    try:
        runtime.store.get(ref)
    except ValueError:
        refused = True
    finally:
        path.write_bytes(original)
    assert refused
    results.append({"case": "artifact_mutation", "status": "pass"})
    q = copy.deepcopy(selected[3][1]); q["scientific_context"]["sign_convention"] = "inverted_target"
    mismatch = runtime.invoke(q)
    assert mismatch["status"] == "failed" and mismatch["result"] is None
    results.append({"case": "artifact_context_mismatch", "status": "pass", "response": mismatch})
    # Hold the worker lease so the submitted job cannot advance, then alter a
    # checkpoint. Restart must fail instead of treating altered state as truth.
    q = report_request(runtime, number=2); q["idempotency_key"] = "tampered-checkpoint"
    job = "j" + hashlib.sha256(q["idempotency_key"].encode()).hexdigest()[:32]
    from causalbank.runtime_v12 import locked
    with locked(runtime.jobs / (job + ".worker")):
        runtime.invoke(q)
        time.sleep(.25)
        p = runtime._job_path(job); state = json.loads(bounded_read(p))
        state["checkpoint_sha256"] = "0" * 64
        atomic(p, state)
    terminal = wait_job(runtime, job)
    assert terminal["state"] == "failed" and "Checkpoint" in terminal["error"], terminal
    results.append({"case": "changed_checkpoint_refused", "status": "pass", "terminal": terminal})
    return {"status": "pass", "cases": results, "limits":
        ["Single-host author fixtures; no scientific calibration, authentic bank inputs or external acceptance",
         "Report job retry is capped at three attempts with original wall deadline"]}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prior = OUT / "qualification-checkpoint.json"
    if prior.exists():
        archive = OUT / "attempts" / ("run-" + uuid.uuid4().hex[:10])
        archive.mkdir(parents=True)
        for name in ["qualification-checkpoint.json", "transport-checks.json", "fault-trials.json", "mcp-stderr.log"]:
            p = OUT / name
            if p.exists():
                (archive / name).write_bytes(p.read_bytes())
    runtime = Runtime(ROOT / ".runtime" / ("in04-qualification-" + uuid.uuid4().hex[:10]))
    selected = cases(runtime)
    checkpoint = {"status": "running", "runtime_root": str(runtime.root),
                  "execution_identity": execution_identity()}
    atomic(OUT / "qualification-checkpoint.json", checkpoint)
    print("Running local library/CLI/MCP parity", flush=True)
    try:
        transports = asyncio.run(asyncio.wait_for(transport_trial(runtime, selected), timeout=75))
        transports["version_negotiation"] = version_negotiation(runtime)
        atomic(OUT / "transport-checks.json", transports)
        print("Transport parity passed; running bounded worker faults", flush=True)
        fault_results = faults(runtime, selected)
        atomic(OUT / "fault-trials.json", fault_results)
        checkpoint.update(status="pass", transport_cases=transports["scientific_cases"],
                          fault_cases=len(fault_results["cases"]))
    except BaseException as exc:
        checkpoint.update(status="failed", error=type(exc).__name__ + ": " + str(exc)[:1200])
        atomic(OUT / "qualification-checkpoint.json", checkpoint)
        raise
    atomic(OUT / "qualification-checkpoint.json", checkpoint)
    print(json.dumps({k: v for k, v in checkpoint.items() if k != "execution_identity"}), flush=True)


if __name__ == "__main__":
    main()
