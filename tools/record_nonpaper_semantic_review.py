#!/usr/bin/env python3
"""Record manually inspected nonpaper findings; never award Q2 automatically."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path, anchor):
    return {"path": str(path.relative_to(ROOT)), "sha256": digest(path),
            "anchor": anchor}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("findings", type=Path)
    args = parser.parse_args()
    findings_path = (ROOT / args.findings).resolve()
    findings = json.loads(findings_path.read_text())
    prior_path = ROOT / findings["prior_review"]
    prior = json.loads(prior_path.read_text())
    index_path = ROOT / prior["structural_review"]["path"]
    assert digest(index_path) == prior["structural_review"]["sha256"]
    index = json.loads(index_path.read_text())
    indexed = {r["citation_key"]: r for r in index["records"]}
    reader = prior["reader"]
    assert digest(ROOT / reader["path"]) == reader["sha256"]
    assert index["pdf"]["sha256"] == reader["sha256"]
    output = ROOT / findings["review_output"]
    checkpoint_path = ROOT / findings["checkpoint_output"]
    assert not output.exists() and not checkpoint_path.exists()
    records, new_keys = [], []
    for finding in findings["records"]:
        key = finding["citation_key"]
        assert key in prior["remaining_source_keys"] and key not in new_keys
        entry = indexed[key]
        assert entry["kind"] != "paper"
        artifacts = {a["path"]: a for a in entry["local_copies"]}
        for artifact in artifacts.values():
            assert digest(ROOT / artifact["path"]) == artifact["sha256"]
        inspected = finding["inspected_artifacts"]
        assert inspected and finding["finding"].strip()
        for item in inspected:
            assert item["path"] in artifacts and item["anchor"].strip()
            assert (ROOT / item["path"]).stat().st_size > 0
        for context in entry["citation_contexts"]:
            live = (ROOT / context["path"]).read_text()
            normalized = re.sub(r"(?m)(?<!\\)%.*$", "", live)
            assert context["context"] in normalized
        records.append({
            "citation_key": key, "kind": entry["kind"],
            "verdict": finding["verdict"], "finding": finding["finding"],
            "source_identity": entry["source_identity"],
            "version_date": entry["version_date"],
            "source_artifacts": list(artifacts.values()),
            "inspected_artifacts": [dict(artifacts[a["path"]], anchor=a["anchor"])
                                    for a in inspected],
            "contexts_reviewed": entry["citation_contexts"],
            "limits": finding.get("limits", "Author source/context review only; documentation or source inspection does not establish runtime performance, production qualification, or independent acceptance."),
        })
        new_keys.append(key)
    reviewed = sorted(set(prior["reviewed_source_key_list"]) | set(new_keys))
    remaining = sorted(set(indexed) - set(reviewed))
    result = {
        "status": "partial_semantic_review_not_Q2_acceptance",
        "reviewer": {"name": "Codex author/coordinator", "kind": "author"},
        "reader": reader,
        "structural_review": ref(index_path, "Exact reader source/context index"),
        "prior_review": ref(prior_path, "Prior dispositions preserved by hash"),
        "prior_review_continuity": "Identical reader; new contexts remain in the indexed manuscript under original comment normalization.",
        "author_findings": ref(findings_path, "Manually inspected sources and scoped findings"),
        "recording_procedure": ref(Path(__file__).resolve(), "Integrity recording only; no automated semantic judgment"),
        "records": records, "cumulative_reviewed_source_keys": len(reviewed),
        "reviewed_source_key_list": reviewed, "remaining_source_keys": remaining,
        "next_action": findings["next_action"], "proposal_q2_acceptance": False,
    }
    checkpoint = {
        "finding": f'{findings["finding"]} {len(reviewed)}/{len(indexed)} source keys reviewed; {len(remaining)} remain. Whole Q2 remains open.',
        "next_action": findings["next_action"],
        "evidence": [],
    }
    with output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    checkpoint["evidence"] = [ref(output, "New source/context dispositions and cumulative coverage")]
    with checkpoint_path.open("x") as handle:
        json.dump(checkpoint, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(json.dumps({"reviewed_now": len(records), "cumulative": len(reviewed),
                      "remaining": len(remaining), "proposal_q2_acceptance": False}))


if __name__ == "__main__":
    main()
