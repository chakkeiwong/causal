#!/usr/bin/env python3
"""Reconcile preserved software records without promoting mutable sources."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/program/repair-v12/work/SW01/inherited-reconciliation.json"


def read(path):
    return json.loads((ROOT / path).read_text())


def identity(path, expected):
    actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"Inherited source identity changed: {path}")
    return actual


def main():
    sources = read("docs/literature/software-sources.json")
    qualified = {x["id"]: x for x in read("docs/literature/software-qualification.json")["projects"]}
    if len(sources) != 44 or len(qualified) != 44:
        raise ValueError("The preserved 44-project baseline changed")
    rows = []
    for source in sources:
        key = source["id"].removeprefix("sw_")
        q = qualified[key]
        identity(source["local_path"], source["sha256"])
        evidence = []
        for item in q.get("evidence", []):
            identity(item["path"], item["sha256"])
            receipt = item.get("retrieval_receipt")
            if receipt:
                identity(receipt["path"], receipt["sha256"])
            evidence.append({
                "path": item["path"], "sha256": item["sha256"],
                "source_url": item.get("source_url"),
                "role": item.get("evidence_role"),
                "inspected_lines_inherited": item.get("lines"),
                "finding_inherited": item.get("finding"),
                "revision_pinned": bool(q.get("pinned_api_revision")),
            })
        rows.append({
            "id": key, "repository": q.get("repository"),
            "source_record": {"path": source["local_path"], "sha256": source["sha256"]},
            "observed_package_version": q.get("observed_package_version"),
            "version_source": q.get("package_version_source"),
            "license_observed": q.get("license_observed"),
            "runtime_status_inherited": q.get("runtime_status", "not_run"),
            "acceptance_test_status_inherited": q.get("acceptance_test_status", "proposed"),
            "technical_evidence": evidence,
            "v12_status": "inherited_hash_verified_scope_and_cutoff_reaudit_required",
            "limitation": "Historical source inspection is preserved; current primary text, release-to-source coherence, exact coverage cell and runtime remain to be reassessed.",
        })
    report = {
        "schema_version": "causalbank.sw01-reconciliation/1",
        "cutoff": "2026-10-07", "baseline_records": 44,
        "hash_status": "all_preserved_identities_match",
        "qualification_source": "docs/literature/software-qualification.json",
        "source_register": "docs/literature/software-sources.json",
        "warning": "The 2026-10-08 inspection of mutable pages is a dated observation, not a time-frozen 2026-10-07 technical snapshot. Every V12 comparison needs its own source/version audit.",
        "projects": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"records": len(rows), "technical_records": sum(bool(x["technical_evidence"]) for x in rows),
                      "hash_status": report["hash_status"]}))


if __name__ == "__main__":
    main()
