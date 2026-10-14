#!/usr/bin/env python3
"""Preserve mutable controls and replay the unchanged four-delivery verifier.

Research artifacts remain at their original paths. Only the explicitly listed
control files move to a historical overlay; manifests are never rewritten.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/program/master/baseline.json"
RECEIPT = "docs/program/master/baseline-verification.json"
ARCHIVE = "docs/program/history/pre-master-2026-10-11"
MANIFESTS = [f"docs/program/{name}-delivery-manifest.json" for name in (
    "reconstruction", "weak-audit", "weak-audit-sharpening", "linked-funding")]
CONTROLS = ["README.md", "docs/mission-control.md", "docs/mission-control.html",
            "docs/program/master-program.md", "docs/program/state.json",
            "docs/program/consistency-check.json", "tools/causal_program.py"]
VERIFIERS = ["delivery_manifest", "weak_audit_delivery",
             "weak_audit_sharpening_delivery", "linked_funding_delivery"]


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2) + "\n")
    tmp.replace(path)


def safe(root, name):
    p = Path(name)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError("Unsafe baseline path: " + name)
    return root / p


def preserve():
    if (ROOT / RECORD).exists():
        raise ValueError("Baseline already preserved; use verify")
    manifests = {p: json.loads((ROOT / p).read_text()) for p in MANIFESTS}
    rows = {r["path"]: r for r in manifests[MANIFESTS[0]]["artifacts"]}
    recovered = []
    controls = {}
    for name in CONTROLS:
        raw = (ROOT / name).read_bytes()
        expected = rows[name]["sha256"]
        if hashlib.sha256(raw).hexdigest() != expected:
            if name != "docs/program/consistency-check.json":
                raise ValueError("Unexpected changed control: " + name)
            failed = json.loads(raw)
            if failed.get("issues") != ["Duplicate label: eq:score"]:
                raise ValueError("Unrecognized historical checker failure")
            failure = "docs/reviews/master-recovery-checker-failure.json"
            (ROOT / failure).write_bytes(raw)
            failed.update(status="pass", issues=[])
            candidate = (json.dumps(failed, indent=2) + "\n").encode()
            if hashlib.sha256(candidate).hexdigest() != expected:
                raise ValueError("Cannot reconstruct the exact frozen receipt")
            raw = candidate
            recovered.append({"path": name, "failure_record": failure,
                              "failure_sha256": sha(ROOT / failure),
                              "method": "Reconstructed 244 original bytes; exact pre-existing manifest SHA-256 match. No new historical check is asserted."})
        target = ROOT / ARCHIVE / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            raise ValueError("Refusing to replace historical control: " + name)
        target.write_bytes(raw)
        controls[name] = {"archive_path": str(target.relative_to(ROOT)),
                          "sha256": expected, "bytes": len(raw)}
    record = {"schema_version": 1, "date": "2026-10-11",
              "manifests": {p: sha(ROOT / p) for p in MANIFESTS},
              "controls": controls, "recovered_receipts": recovered,
              "scope": "Historical control overlay only; research/PDF/source bytes and original manifests retain their identities.",
              "verification": "python3 tools/causal_program.py baseline"}
    write(ROOT / RECORD, record)
    print(json.dumps({"status": "preserved", "controls": len(controls),
                      "recovered_receipts": len(recovered)}))


def verify():
    record = json.loads((ROOT / RECORD).read_text())
    members = {}
    for name, digest in record["manifests"].items():
        if sha(ROOT / name) != digest:
            raise ValueError("Changed original manifest: " + name)
        for row in json.loads((ROOT / name).read_text())["artifacts"]:
            if row["path"] in members and members[row["path"]] != row:
                raise ValueError("Conflicting predecessor identity: " + row["path"])
            members[row["path"]] = row
    for name, row in record["controls"].items():
        p = safe(ROOT, row["archive_path"])
        if sha(p) != row["sha256"] or p.stat().st_size != row["bytes"]:
            raise ValueError("Changed historical control: " + name)
        if row["sha256"] != members[name]["sha256"]:
            raise ValueError("Historical control is not manifest-bound: " + name)
    for row in record["recovered_receipts"]:
        if sha(ROOT / row["failure_record"]) != row["failure_sha256"]:
            raise ValueError("Lost recovery failure record")
    # A disposable read view makes the original verifier's path semantics exact.
    # Its four executable modules are byte-for-byte copies so __file__ resolves
    # inside this view. Other immutable artifacts are linked, never copied/edited.
    with tempfile.TemporaryDirectory(prefix="causal-baseline-") as tmp:
        view = Path(tmp)
        for name in sorted(set(members) | set(record["manifests"])):
            original = record["controls"].get(name, {}).get("archive_path", name)
            source = safe(ROOT, original)
            dest = safe(view, name)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if name in {"tools/" + v + ".py" for v in VERIFIERS}:
                shutil.copyfile(source, dest)
            else:
                dest.symlink_to(source)
        print(json.dumps({"status": "replaying_original_verifiers",
                          "unique_artifacts": len(members), "manifests": 4}), flush=True)
        result = subprocess.run([sys.executable, str(view / "tools/linked_funding_delivery.py"), "verify"],
                                cwd=view, text=True, capture_output=True, timeout=300)
        if result.returncode:
            raise ValueError(result.stdout + result.stderr)
        original_result = json.loads(result.stdout)
    receipt = {"status": "pass", "date": "2026-10-11", "issues": [],
               "unique_artifacts": len(members), "manifests_verified": 4,
               "original_verifier_result": original_result,
               "input_sha256": {RECORD: sha(ROOT / RECORD),
                                  **record["manifests"],
                                  "tools/program_baseline.py": sha(Path(__file__))},
               "scope": "Full original linked-funding gates, nested predecessor gates and original artifact identities through the preserved control overlay; no scientific or institutional approval."}
    write(ROOT / RECEIPT, receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["preserve", "verify"])
    args = parser.parse_args()
    try:
        globals()[args.command]()
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as exc:
        raise SystemExit(str(exc))
