#!/usr/bin/env python3
"""Record text and physical-page checks; never assert visual acceptance."""
import json
import re
import subprocess
import xml.etree.ElementTree as ET

import build_integrated_monograph_v12 as book

ROOT, OUT = book.ROOT, book.OUT


def main():
    report = book.load(OUT / "build-report.json")
    pdf = ROOT / report["pdf"]["path"]
    subprocess.run(["pdftotext", "-bbox", str(pdf), str(OUT / "layout-bounds.xml")], check=True, timeout=30)
    raw = (OUT / "layout-bounds.xml").read_text()
    controls = re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", raw)
    clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", raw)
    ns = {"x": "http://www.w3.org/1999/xhtml"}
    pages = ET.fromstring(clean).findall(".//x:page", ns)
    outside, empty = [], []
    for i, page in enumerate(pages, 1):
        width, height = float(page.attrib["width"]), float(page.attrib["height"])
        words = page.findall(".//x:word", ns)
        if not words:
            empty.append(i)
        for word in words:
            a = word.attrib
            if float(a["xMin"]) < 0 or float(a["yMin"]) < 0 or float(a["xMax"]) > width + .5 or float(a["yMax"]) > height + .5:
                outside.append({"page": i, "text": word.text, "bounds": a})
    assert len(pages) == report["pages"] and not outside and not empty
    text = (OUT / "reader.txt").read_text()
    flat = " ".join(text.split())
    required = ["What language models contribute to causal knowledge",
                "Banking decisions, review effort and the value of assistance",
                "Preserving a causal result across software boundaries",
                "The library, command line and MCP service",
                "Workspace consumers and complete banking workflows",
                "Operating the local causal service and qualifying its limits",
                "2,500", "zero live model calls", "fails finite calibration", "whole real line"]
    checks = {s: s in flat for s in required}
    assert all(checks.values()), checks
    aux = (OUT / (book.NAME + ".aux")).read_text()
    labels = {m.group(1): int(m.group(2)) for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}", aux)}
    allocation = book.load(book.BASE / "chapter-plan.json")["chapters"]
    mapping = {
        "S1": (["sw:interfaces"], "Survey methods and search stopping rules need full development."),
        "S2": (["sw:interfaces"], "Expand IID/latent/temporal/experimental discovery and remaining candidates."),
        "S3": (["sw:interfaces"], "Develop a full identification/counterfactual chapter and typed numerical failure comparisons."),
        "S4": (["sw:design"], "Broaden effects/heterogeneity, quasi-experiments and matched examples."),
        "S5": (["sw:longitudinal"], "Expand survival, dynamic regimes and uncertainty comparisons."),
        "S6": (["sw:panels"], "Expand dynamic panels/time series and inferential alternatives."),
        "S7": (["sw:design", "sw:longitudinal"], "No dedicated full observation/transport/network chapter yet."),
        "S8": ([], "Vendor original manuals, edition comparisons and costs missing; no superiority claim."),
        "S9": (["sw:agents"], "Bridge decisions are provisional; actual cross-language paths unqualified."),
        "S10": (["sw:agents"], "Qualification discussion only; package/bridge trial dependencies remain."),
        "L1": (["la:frontier"], "New frontier synthesis; deepen evidence comparisons and current-source coverage."),
        "L2": (["la:translation"], "Expand four banking translations and independent semantic review."),
        "L3": (["la:diagrams"], "Expand ontology, elicitation, hidden-variable and disagreement cases."),
        "L4": (["ch:la03-discovery"], "Expand comparisons and failure regimes without changing frozen evidence."),
        "L5": (["ch:la04-workflow"], "Expand longitudinal/panel/observation pathways and matched alternatives."),
        "L6": (["ch:la05-prototype", "sw:agents"], "Prototype/package draft coverage; full backend/framework comparison incomplete."),
        "L7": (["la:evaluation"], "Prospective design only; five live-study input classes absent."),
        "L8": (["la:economics"], "Exact stipulated accounting; authentic prices/value and deeper cases missing."),
        "I1": (["in:semantics"], "Short draft needs deeper interchange and adapter derivations."),
        "I2": (["in:surfaces"], "Actual local surfaces; modern protocol/external client paths unqualified."),
        "I3": (["in:consumers"], "Inspected designs; actual adapter/consumer conformance missing."),
        "I4": (["in:operations"], "Real local faults; target-platform, ownership and whole-cost evidence missing.")}
    rows = []
    for c in allocation:
        keys, remaining = mapping[c["id"]]
        rows.append({"id": c["id"], "repair_id": c["repair_id"], "required_title": c["title"],
                     "required_body_pages": c["body_pages"], "main_labels": keys,
                     "printed_start_pages": [labels[k] for k in keys],
                     "status": "partial_draft" if keys else "not_developed",
                     "remaining": remaining, "accepted_substantive_pages": None})
    book.write_json(OUT / "chapter-progress.json", {"date": "2026-10-12",
        "scope": "All 22 frozen allocations retained. Shared chapter mappings are not additive page credit.",
        "main_pdf": report["pdf"], "physical_body_pages": report["physical_body_pages"],
        "all_repairs_open": True, "chapters": rows})
    review = {"date": "2026-10-12", "status": "text_and_bounds_pass_visual_pending", "pdf": report["pdf"],
        "physical_pages": len(pages), "numbered_chapters": report["numbered_chapters"],
        "one_bibliography": (OUT / (book.NAME + ".bbl")).read_text().count(r"\begin{thebibliography}") == 1
                            and sum(bool(re.match(r"^Bibliography\s*\n", page.lstrip())) for page in text.split("\f")) == 1,
        "text_inclusion_checks": checks, "words_outside_physical_page": outside, "empty_text_pages": empty,
        "latex_findings": report["warnings"], "extraction_control_characters_removed_for_xml_parsing": len(controls),
        "extraction_note": "pdftotext emits controls for some mathematical glyphs; stripped only for XML parsing. Original extraction retained. No visual-glyph acceptance inferred.",
        "source_and_reference_check": "python3 tools/build_integrated_monograph_v12.py check",
        "author_review_scope": ["New arguments and source claim roles", "Exact decision/set arithmetic",
            "No invented live/bank results", "Continuous TOC/numbering/references", "Historical negative findings"],
        "rendered_pages_inspected": [],
        "visual_review": "Pending fresh session; recovered conversation exhausted parent AGENTS.md image budget.",
        "review_script": book.ref(book.ROOT / "tools/review_integrated_reader_v12.py", "Text and page-bounds checks")}
    assert review["one_bibliography"]
    book.write_json(OUT / "text-layout-review.json", review)
    print(json.dumps({"status": review["status"], "pages": len(pages), "chapter_allocations": len(rows),
                      "outside_bounds": len(outside), "xml_controls": len(controls)}))


if __name__ == "__main__":
    main()
