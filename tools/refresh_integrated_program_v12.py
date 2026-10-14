#!/usr/bin/env python3
"""Prepare a reviewed program-view successor, then register its working reader."""
import argparse
import contextlib
import io
import json
import re
import subprocess
from pathlib import Path

import master_control as core
import causal_program_current as current
import build_integrated_monograph_v12 as book

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/program/repair-v12"
OUT = BASE / "integrated-reader"
PLAN = ROOT / "docs/program/master-program-v12.1.md"
PLAN_PDF = PLAN.with_suffix(".pdf")


def binding(path, anchor):
    return book.ref(path, anchor)


def prepare():
    current.install_hooks()
    report = book.load(OUT / "build-report.json")
    assert report["pages"] == 345 and report["numbered_chapters"] == 45
    assert report["physical_body_pages"] == {"software": 18, "llm": 39, "integration": 12}
    original = ROOT / "docs/program/master-program-v12.md"
    content = original.read_text()
    content = content.replace("# Master program V12:", "# Master program V12.1 execution view:", 1)
    content = content.replace("11 October 2026. Baseline literature cutoff: 7 October 2026.",
        "12 October 2026. Literature cutoff: 7 October 2026. Work and acceptance contracts remain V12; this is a reviewed execution and publication update.", 1)
    content = content.replace("The current research reader\nis still the 268-page I01 release, not a completed version of these repairs. Its\nthree-page sponsor brief remains available.",
        "The current research reader is the [345-page integrated working monograph](../causal_integrated_working_2026-10-12.pdf), with 45 numbered chapters and one bibliography. The preserved [268-page I01 delivery](../causal_master_execution_reader_2026-10-11.pdf) and its three-page sponsor brief remain historical author deliveries.")
    content = content.replace("The saved canonical state has eleven dispositions among sixteen V11 packages.",
        "The canonical state has 21 dispositions among 40 packages. P12, IN01, IN02, IN04 and LA01–LA05 have scoped passing receipts. LA06 is inconclusive because its final live study inputs are unavailable. The original eleven V11 dispositions remain preserved.")
    update = """## Integrated document and current execution

All currently developed repair material is inside the main TeX manuscript and
PDF. It is source integration with continuous numbering and references, not a
collection of appended standalone PDFs. All four earlier scientific supplements
are also integrated; their individual sources and deliveries remain preserved.

| Repair | Current material in the main book | Required depth and remaining execution |
|---|---|---|
| MR01 | Five comparative chapter drafts; 18 physical body pages; 22 new pinned package/source reviews | Ten chapters and 100–150 substantive pages; 102 reviewed search cells; vendor originals/comparison; adoption decisions and matched package trials |
| MR02 | Eight chapter drafts; 39 physical body pages; frontier synthesis and exact banking economics added | 96–112 substantive pages with full task coverage, stronger cases and independent evidence review; live evaluation needs its five missing input classes |
| MR03 | Four chapter drafts; 12 physical body pages; completed local interface evidence and dated consumer designs incorporated | Indicative 40–60 pages; actual cross-language adapters and consumer workflows, operator/environment qualification and ownership |

These physical spans exclude the inherited software chapter and are not accepted
substantive-page counts. The full duplication/coverage review and rendered visual
inspection remain open. **All three repairs remain open; no I02 receipt is issued.**

The complete book cites 228 source records and binds its TeX, bibliography,
figures, project examples and original sources in its own audit. The historical
source register remains frozen. Forty-nine sibling source originals still match
their saved identities; four changed records are documented and excluded from
new technical claims. Sibling interfaces remain inspected/proposed connections,
not accepted adoption. The new decision example is exact stipulated arithmetic,
not a live model trial, bank price or ROI estimate.

### Executable continuation, in order

1. Run `python3 tools/causal_program_current.py check`. This retains the V12
   evidence gates and adds full working-book verification. Use its `status` and
   `next` commands for the current view; the V12 and original compatibility
   checks remain available and unchanged.
2. Continue SW01: inspect already saved LiNGAM, delicatessen, y0, pygformula,
   statsmodels, grf and network/transport leads; keep identity and technical
   evidence distinct. Deepen the 23 partial cell reviews and inspect the other
   79 cells. No cell is closed. Do not repeat rate-limited provider requests in
   a loop or treat unavailable vendor documents as missing vendor features.
3. Continue LA07 from the integrated eight-chapter sequence. Expand each mapped
   task and banking case, retaining matched targets, counterexamples, source
   limits and all-request denominators. New chapter topics do not satisfy the
   required depth by their existence. Do not rerun or overwrite frozen LA03–LA06
   evidence; new empirical evaluation requires a reviewed successor.
4. After SW01 passes, execute SW02–SW07 comparisons and reuse choices, then IN03
   adapters and SW08/IN05 qualification in dependency order. The four current
   integration chapters are drafts from completed IN01/IN02/IN04 work; they do
   not close IN06 or bypass these dependencies.
5. Reconcile the 22 required chapter allocations with the whole book, review
   duplication and substantive depth, and inspect rendered pages in a fresh
   session. Only then can the repair closure receipts and I02 be considered.
   The sponsor proposal must be revised for that actual accepted author scope.

The program is 21/40 dispositions and 0/10 original gaps fully qualified.
These counts are not a percentage estimate of product completion. Negative
R02/R04/R05 results and external scientific, bank, platform and economics gates
remain exactly as recorded. Source access failures, five unavailable live-study
inputs and the exhausted image budget are explicit limits; they do not justify
claiming completed coverage.

[Integration plan/review](repair-v12/integration-plan-2026-10-12.md) ·
[Execution review](repair-v12/integrated-reader/review.md) ·
[Chapter progress](repair-v12/integrated-reader/chapter-progress.json) ·
[Frozen V12 scope](master-program-v12.md)

"""
    content = content.replace("## The recovered state and the standard", update + "## The recovered state and the standard", 1)
    content = content.replace("SW01 begins with 110 unverified search leads, including inherited\nsoftware, commercial products, agent frameworks and protocol references.",
        "SW01 retains 110 original search leads and one discovered pgmpy row: 111 catalog entries, 77 audit entries of differing scopes, and 22 new pinned technical reviews. Its 285 acquisition registrations include 239 saved, 24 failed and 22 unexecuted. Twenty-three of 102 cells have partial individual reviews; none is closed.")
    content = content.replace("The first ready package after P12 is SW01; LA01 and IN01 are also eligible.",
        "The current ready packages are SW01 and LA07. LA01 and IN01 have completed their scoped work.")
    content = content.replace("The successor command is `python3 tools/causal_program_v12.py`; use its status,",
        "The current view command is `python3 tools/causal_program_current.py`; use its status,")
    content = content.replace("The successor adds mandatory repair records, exact new contracts, retained",
        "The unchanged V12 controller supplies mandatory repair records, exact contracts, retained")
    content += "\n\nThe current view wraps the unchanged V12 controller and verifies the integrated manuscript independently of the frozen historical bibliography. It adds no waiver, changes no task prerequisite and records no new package completion. State updates use the original locked, history-preserving writer.\n"
    PLAN.write_text(content)
    # Make local PDF links relative to the final plan's own directory. Pandoc
    # does not require opening the targets to typeset these links.
    header = OUT / "program-header.tex"
    header.write_text("\\usepackage{microtype,xurl}\n\\setlength{\\emergencystretch}{3em}\n")
    tex = OUT / "current-program.tex"
    subprocess.run(["pandoc", str(PLAN), "--from=markdown+pipe_tables+raw_tex", "--standalone", "--to=latex",
                    "-V", "documentclass=article", "-V", "fontsize=11pt", "-V", "papersize=a4",
                    "-V", "geometry:margin=22mm", "--include-in-header", str(header), "-o", str(tex)],
                   cwd=ROOT, capture_output=True, text=True, check=True, timeout=30)
    for i in range(2):
        with (OUT / f"program-pass-{i+1}.log").open("w") as log:
            subprocess.run(["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                           cwd=OUT, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=60)
    PLAN_PDF.write_bytes((OUT / "current-program.pdf").read_bytes())
    info = subprocess.check_output(["pdfinfo", str(PLAN_PDF)], text=True, timeout=15)
    pages = int(re.search(r"(?m)^Pages:\s+(\d+)", info).group(1))
    log = (OUT / "current-program.log").read_text(errors="replace")
    warnings = [l for l in log.splitlines() if any(x in l for x in ("Warning", "Overfull", "Underfull"))]
    book.write_json(OUT / "program-build.json", {
        "status": "compiled_text_checks_only", "program": binding(PLAN, "Complete current scope plus execution update"),
        "pdf": binding(PLAN_PDF, "Current program reader"), "pages": pages, "warnings": warnings,
        "base_scope": binding(original, "Frozen V12 contract scope preserved"),
        "builder": binding(Path(__file__), "Program-view and state publisher"), "visual_review": "pending fresh session"})
    print(json.dumps({"status": "program_prepared", "pages": pages, "warnings": warnings}))


def publish():
    current.install_hooks()
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    if state.get("working_document"):
        raise ValueError("Working reader already published; use a reviewed successor")
    issues = core.validate_state(ROOT, state)
    if issues:
        raise ValueError(str(issues))
    with contextlib.redirect_stdout(io.StringIO()):
        book.check()
    report = book.load(OUT / "build-report.json")
    plan_report = book.load(OUT / "program-build.json")
    book.verify_refs(plan_report)
    review = OUT / "review.md"
    assert review.is_file() and (OUT / "text-layout-review.json").is_file()
    reader = {"path": report["pdf"]["path"], "sha256": report["pdf"]["sha256"],
              "pages": report["pages"], "status": "Integrated working draft; all three repairs and final visual review remain open; not I02 acceptance"}
    working = {"status": "integrated_working_draft", "build_report": binding(OUT / "build-report.json", "Whole-book build report"),
        "source_audit": report["source_audit"], "driver": report["driver"],
        "program_update": binding(PLAN, "Reviewed current program and continuation"),
        "program_update_pdf": binding(PLAN_PDF, "Compiled current program"),
        "review": binding(review, "Author integration review with remaining blockers"),
        "predecessor_reader": state["reader"], "acceptance_release": "I02", "acceptance_claim": False}
    state["reader"] = reader
    state["working_document"] = working
    state["repair_program"]["master"] = str(PLAN.relative_to(ROOT))
    state["repair_program"]["controller"] = "python3 tools/causal_program_current.py"
    for key, p, anchor in [
        ("current_program", PLAN, "Current execution view; V12 gates unchanged"),
        ("current_program_pdf", PLAN_PDF, "Current execution plan PDF"),
        ("current_view_controller", ROOT / "tools/causal_program_current.py", "Additional full-book checks and current dashboard rendering"),
        ("current_book_builder", ROOT / "tools/build_integrated_monograph_v12.py", "Full-book integration, source audit and verification"),
        ("current_view_publisher", Path(__file__), "Reviewed state update through original locked writer"),
        ("current_integration_review", review, "Scope and unresolved blockers"),
        ("current_book_report", OUT / "build-report.json", "Exact integrated working PDF and inputs"),
        ("current_chapter_progress", OUT / "chapter-progress.json", "All 22 original allocations retained and partial"),
        ("current_text_layout_review", OUT / "text-layout-review.json", "Extracted text and bounds, not visual acceptance")]:
        state["repair_program"]["documents"][key] = binding(p, anchor)
    state["deliveries"].append({k: reader[k] for k in ("path", "sha256", "pages")} | {"status": "working_draft_not_I02"})
    state["deliveries"].append({"path": str(PLAN_PDF.relative_to(ROOT)), "sha256": core.sha(PLAN_PDF),
                               "pages": plan_report["pages"], "status": "execution_view_not_scope_reduction"})
    current.verify_working_document(ROOT, state)
    core.commit_state(ROOT, before, state, {"action": "integrate_working_monograph_and_refresh_execution_view",
        "working_reader": reader, "program_update": working["program_update"],
        "scope": "Source integration and new eligible chapter work; no task completion or acceptance criterion changed"})
    print(json.dumps({"status": "published_current_working_reader", "pages": reader["pages"],
                      "disposed": len(state["results"]), "contracts": len(state["work_packages"]),
                      "mandatory_repairs_closed": []}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "publish"))
    args = parser.parse_args()
    prepare() if args.command == "prepare" else publish()
