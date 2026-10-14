#!/usr/bin/env python3
"""Attach inspected software anchors to the existing source audit.

This performs local provenance work only. It neither imports the reviewed
packages nor treats proposed acceptance tests as executed evidence.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "docs/literature"
RAW = LIT / "raw"
BT = chr(96)


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def artifact(path):
    return {"path": str(path.relative_to(ROOT)),
            "sha256": digest(path), "bytes": path.stat().st_size}


def qualify(spec, snapshot):
    evidence = []
    artifacts = {a["path"]: a for a in snapshot["artifacts"]}
    for old in artifacts.values():
        p = ROOT / old["path"]
        if digest(p) != old["sha256"]:
            raise ValueError("Previously registered artifact changed: " + str(p))
    for entry in spec["evidence"]:
        name, first, last, finding, *kind = entry
        path = RAW / name
        lines = path.read_text().splitlines()
        last = min(last, len(lines))
        if not 1 <= first <= last:
            raise ValueError("Invalid inspection anchor: " + name)
        row = {**artifact(path), "lines": [first, last], "finding": finding,
               "evidence_role": kind[0] if kind else "primary_technical_text",
               "excerpt_sha256": hashlib.sha256(
                   "\n".join(lines[first-1:last]).encode()).hexdigest()}
        artifacts[row["path"]] = artifact(path)
        receipt = path.with_suffix(".receipt.json")
        if receipt.exists() and receipt != path:
            receipt_data = read(receipt)
            row["retrieval_receipt"] = artifact(receipt)
            row["source_url"] = receipt_data["url"]
            if receipt_data.get("path") == row["path"]:
                if receipt_data.get("status") != "saved" or receipt_data["sha256"] != row["sha256"]:
                    raise ValueError("Direct-download receipt mismatch: " + name)
            commit_match = re.search(r"raw\.githubusercontent\.com/[^/]+/[^/]+/([0-9a-f]{40})/", row["source_url"])
            if commit_match:
                row["source_commit"] = commit_match.group(1)
        evidence.append(row)
    # Repository metadata proves the revision's date; it is not technical text.
    for prefix in ("r3g_commit_", "r3g_tree_"):
        path = RAW / (prefix + spec["id"] + ".json")
        if path.exists():
            artifacts[str(path.relative_to(ROOT))] = artifact(path)
            receipt = path.with_suffix(".receipt.json")
            artifacts[str(receipt.relative_to(ROOT))] = artifact(receipt)
    pinned = {e["source_commit"] for e in evidence if "source_commit" in e}
    commit_path = RAW / ("r3g_commit_" + spec["id"] + ".json")
    pin = None
    if pinned:
        commit = read(commit_path)[0]
        pin = {"sha": commit["sha"], "committer_date": commit["commit"]["committer"]["date"],
               "metadata": artifact(commit_path),
               "scope": "Inspected API files at this commit; not an assertion about all README bytes or the published package release."}
        if pinned != {pin["sha"]} or pin["committer_date"][:10] > "2026-10-07":
            raise ValueError("Commit identity/cutoff mismatch: " + spec["id"])
    qualification = {k: v for k, v in spec.items() if k != "evidence"}
    qualification.update(
        evidence=evidence, inspected_at="2026-10-08",
        runtime_status="not_run", acceptance_test_status="proposed",
        pinned_api_revision=pin)
    snapshot["artifacts"] = list(artifacts.values())
    snapshot["scientific_qualification"] = qualification
    return snapshot


def main():
    spec_path = LIT / "software-qualification-spec.json"
    spec = read(spec_path)
    census = read(LIT / "software-assessment.json")
    expected = {x["id"] for x in census}
    actual = [x["id"] for x in spec["projects"]]
    if len(actual) != len(set(actual)) or set(actual) != expected or len(actual) != 44:
        raise ValueError("Qualification must cover exactly the existing 44-project census")
    others = read(LIT / "other-sources.json")
    sources = {s["id"]: s for s in others}
    rows = []
    for project in spec["projects"]:
        path = LIT / "software" / (project["id"] + ".json")
        snapshot = qualify(project, read(path))
        save(path, snapshot)
        q = snapshot["scientific_qualification"]
        source = sources["sw_" + project["id"]]
        source["sha256"] = digest(path)
        source["accessed"] = "2026-10-08"
        source["version_status"] = (
            "Documentation snapshot 7 October 2026, qualified 8 October 2026; "
            "content hashes preserved; selected APIs commit-pinned; runtime untested")
        source["inspected"] = [
            f"{e['path']}, lines {e['lines'][0]}--{e['lines'][1]}: {e['finding']}"
            for e in q["evidence"]]
        source["claims"] = [e["finding"] for e in q["evidence"]]
        source["limits"] = (
            "Source/document inspection only. Proposed adapter: " + q["adapter_rule"] +
            " Scientific restrictions: " + q["assumptions"] +
            " Acceptance tests are proposed and not run. " + snapshot["pin_limit"])
        source["qualification_record"] = "docs/literature/software-qualification.json#" + project["id"]
        rows.append({**q, "repository": snapshot["repository"],
                     "observed_package_version": snapshot["package_version"],
                     "package_version_source": snapshot["package_version_source"],
                     "license_observed": snapshot["license"],
                     "source_snapshot": artifact(path)})
    save(LIT / "other-sources.json", others)
    save(LIT / "software-sources.json", [s for s in others if s["kind"] == "software"])
    output = {k: v for k, v in spec.items() if k != "projects"}
    output.update(specification=artifact(spec_path), projects=rows)
    save(LIT / "software-qualification.json", output)
    md = ["# Mathematical qualification of the software census", "",
          spec["scope"], "", spec["version_policy"], "",
          "Cutoff: 7 October 2026. Inspected: 8 October 2026. "
          "No reviewed package was run by this qualification pass.", ""]
    for row in rows:
        md.extend([f"## {row['id']}: {row['role']}", "",
                   f"Repository: {BT}{row['repository']}{BT}. Observed package version: "
                   f"{BT}{row['observed_package_version'] or 'not established'}{BT}. "
                   f"License observation: {row['license_observed']}.",
                   f"Source snapshot: [{row['id']}.json](software/{row['id']}.json), "
                   f"SHA-256 {BT}{row['source_snapshot']['sha256']}{BT}.", ""])
        if row["pinned_api_revision"]:
            pin = row["pinned_api_revision"]
            md.extend([f"Selected API commit: {BT}{pin['sha']}{BT} ({pin['committer_date']}). "
                       + pin["scope"], ""])
        for key, title in (("input", "Mathematical input"), ("output", "Mathematical output"),
                           ("assumptions", "Scientific restrictions"),
                           ("adapter_rule", "Proposed adapter behavior"),
                           ("acceptance_test", "Proposed acceptance test")):
            md.extend([f"**{title}.** {row[key]}", ""])
        md.extend(["**Inspected support.**", ""])
        for e in row["evidence"]:
            md.append(f"- {BT}{e['path']}{BT} lines {e['lines'][0]}--{e['lines'][1]}, "
                      f"SHA-256 {BT}{e['sha256']}{BT}: {e['finding']} ({e['evidence_role']}).")
        md.append("")
    (LIT / "software-qualification.md").write_text("\n".join(md) + "\n")
    audit = {"date": "2026-10-08", "status": "pass", "projects": len(rows),
             "pinned_api_projects": sum(r["pinned_api_revision"] is not None for r in rows),
             "inspected_anchors": sum(len(r["evidence"]) for r in rows),
             "runtime_qualified": 0, "specification": artifact(spec_path),
             "qualification": artifact(LIT / "software-qualification.json"),
             "scope": "Source-byte, anchor, exact census membership and pinned-revision closure; not package runtime or scientific completeness."}
    save(ROOT / "docs/reviews/software-qualification-audit.json", audit)
    print(json.dumps(audit))


if __name__ == "__main__":
    main()
