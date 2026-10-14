#!/usr/bin/env python3
"""Bind manually inspected primary-paper findings to an unchanged reader.

This only records the supplied author findings. It does not perform semantic
review or award proposal acceptance.
"""
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
    records = []
    new_keys = []
    for finding in findings["records"]:
        key = finding["citation_key"]
        assert key in prior["remaining_source_keys"] and key not in new_keys
        entry = indexed[key]
        assert entry["kind"] == "paper" and len(entry["local_copies"]) == 1
        pdf_ref = entry["local_copies"][0]
        pdf = ROOT / pdf_ref["path"]
        assert pdf.suffix == ".pdf" and digest(pdf) == pdf_ref["sha256"]
        extracted = ROOT / findings["primary_text_directory"] / (key + ".txt")
        pages = finding["inspected_pdf_pages"]
        assert pages and min(pages) > 0
        assert max(pages) <= len(extracted.read_text().split("\f")) - 1
        for context in entry["citation_contexts"]:
            live_tex = (ROOT / context["path"]).read_text()
            # Same comment normalization as build_integrated_monograph_v12.scan.
            indexed_tex = re.sub(r"(?m)(?<!\\)%.*$", "", live_tex)
            assert context["context"] in indexed_tex
        assert finding["finding"].strip()
        records.append({
            "citation_key": key,
            "verdict": finding["verdict"],
            "finding": finding["finding"],
            "primary_source": dict(ref(pdf, "Genuine saved primary scholarly PDF"),
                                   inspected_pdf_pages=pages),
            "extracted_text": ref(extracted, "Local pdftotext -layout extraction from the hash-verified primary PDF"),
            "source_identity": entry["source_identity"],
            "version_date": entry["version_date"],
            "contexts_reviewed": entry["citation_contexts"],
            "limits": finding.get("limits", "Author source/context review; no independent acceptance, package execution, bank validation or verification of theorem premises in bank data implied."),
        })
        new_keys.append(key)
    reviewed = sorted(set(prior["reviewed_source_key_list"]) | set(new_keys))
    assert set(reviewed) <= set(indexed)
    remaining = sorted(set(indexed) - set(reviewed))
    result = {
        "status": "partial_semantic_review_not_Q2_acceptance",
        "reviewer": {"name": "Codex author/coordinator", "kind": "author"},
        "reader": reader,
        "structural_review": ref(index_path, "Exact reader source/context index"),
        "prior_review": ref(prior_path, "Prior reviewed dispositions preserved by hash"),
        "prior_review_continuity": "Identical reader; every newly reviewed context remains present under the original index comment normalization.",
        "author_findings": ref(findings_path, "Manually inspected primary passages and explicit scoped findings"),
        "recording_procedure": ref(Path(__file__).resolve(), "Integrity and continuity checks only; not an automatic semantic reviewer"),
        "records": records,
        "cumulative_reviewed_source_keys": len(reviewed),
        "reviewed_source_key_list": reviewed,
        "remaining_source_keys": remaining,
        "next_action": findings["next_action"],
        "proposal_q2_acceptance": False,
    }
    with output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    checkpoint = {
        "finding": f'{findings["finding"]} {len(reviewed)}/{len(indexed)} source keys reviewed; {len(remaining)} remain. Whole Q2 remains open.',
        "next_action": findings["next_action"],
        "evidence": [ref(output, "New primary-paper/context dispositions and cumulative coverage")],
    }
    with checkpoint_path.open("x") as handle:
        json.dump(checkpoint, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(json.dumps({"reviewed_now": len(records), "cumulative": len(reviewed),
                      "remaining": len(remaining), "proposal_q2_acceptance": False}))


if __name__ == "__main__":
    main()
