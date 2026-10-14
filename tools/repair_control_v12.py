"""V12 evidence gates over the preserved V11 controller and its single state.

The legacy assessed_release field is retained for V11 lineage compatibility.
External V12 acceptance additionally binds assessed_current_release to I02.
Importing this module does not change the legacy controller; the CLI installs
the extension only in its own process. Neither validator judges scholarship.
"""
import contextlib
import io
import json
import re
import subprocess
import sys

import master_control as core

DIRECTORY = "docs/program/repair-v12"
REVISION = "12.0-systematic-major-repairs"
REPAIRS = {"MR01": "SW09", "MR02": "LA07", "MR03": "IN06"}
EXTERNAL = {"X01", "X02", "X03", "X04", "F01"}
STUDIES = {"SW08", "LA06", "IN05"}
LEGACY_VALIDATE_STATE = core.validate_state
LEGACY_VALIDATE_RECEIPT = core.validate_receipt
LEGACY_SUMMARY = core.summary


def reference(root, name, anchor):
    return {"path": name, "sha256": core.sha(core.safe(root, name)), "anchor": anchor}


def bound_json(root, ref):
    core.bound(root, ref)
    return core.read(root, ref["path"])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def revision_contract(root, state):
    """Reject scope removal, historical rewriting and stale final dependencies."""
    require(state.get("revision") == REVISION, "V12 revision is required")
    program = state["repair_program"]
    require(program["acceptance_release_task"] == "I02", "V12 acceptance must require I02")
    migration = bound_json(root, program["migration"])
    baseline = bound_json(root, migration["previous_state"])
    for ref in program["documents"].values():
        core.bound(root, ref)
    planned = bound_json(root, program["documents"]["work_packages"])
    repairs = bound_json(root, program["documents"]["major_repairs"])
    chapters = bound_json(root, program["documents"]["chapters"])["chapters"]
    coverage = bound_json(root, program["documents"]["coverage"])
    require(state["major_repairs"] == repairs, "Mandatory repair records changed or omitted")
    require({r["id"]: r["closure_task"] for r in repairs} == REPAIRS,
            "All three required major repairs must remain")
    expected = {t["id"]: t for t in baseline["work_packages"]}
    expected.update({t["id"]: t for t in planned})
    expected.update({t["id"]: t for t in migration["external_contracts"]})
    actual = {t["id"]: t for t in state["work_packages"]}
    require(actual == expected, "Work contracts differ from the reviewed V12 migration")
    require(state["streams"] == baseline["streams"], "Original streams changed")
    require(state["gaps"] == baseline["gaps"], "Original scientific gap obligations changed")
    for key in ("results", "registrations", "input_receipts"):
        for name, value in baseline[key].items():
            require(state[key].get(name) == value, "Historical " + key + " changed: " + name)
    require(state.get("attempts", []) == baseline.get("attempts", []), "Historical attempts changed")
    require(state["baseline_manifest_sha256"] == baseline["baseline_manifest_sha256"],
            "Historical baseline identity changed")
    for item in baseline["deliveries"]:
        require(item in state["deliveries"], "Historical delivery removed")
        core.bound(root, dict(item, anchor="Preserved delivery"))
    for task_id in EXTERNAL | {"I02"}:
        needed = set(REPAIRS.values()) if task_id == "I02" else {"I02"}
        deps = {d["id"] for d in actual[task_id]["depends"] if d["outcomes"] == ["pass"]}
        require(needed <= deps, "Missing mandatory final release gate: " + task_id)
    require(len({c["id"] for c in chapters}) == len(chapters) == 22,
            "V12 requires the 22 reviewed chapter allocations")
    for repair in repairs:
        allocated = [c for c in chapters if c["repair_id"] == repair["id"]]
        for k in ("min", "target", "max"):
            require(sum(c["body_pages"][k] for c in allocated) == repair["page_budget"][k],
                    "Chapter allocation mismatch: " + repair["id"])
    cells = {r["id"] for r in coverage["software_cells"]}
    expected_cells = {a["id"] + "::" + d for a in coverage["software_areas"]
                      for d in coverage["software_dimensions"]}
    require(cells == expected_cells and len(cells) == len(coverage["software_cells"]) == 102,
            "Software coverage matrix is incomplete")
    require(coverage["literature_cutoff"] == "2026-10-07", "Baseline cutoff changed")


def pdf_pages(root, ref):
    core.bound(root, ref)
    path = core.safe(root, ref["path"])
    with path.open("rb") as stream:
        require(stream.read(5) == b"%PDF-", "Rendered artifact is not a PDF")
    result = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True,
                            check=True, timeout=15)
    match = re.search(r"(?m)^Pages:\s+(\d+)", result.stdout)
    require(match is not None, "Unable to count PDF pages")
    return int(match.group(1))


def coverage_ids(contract, repair_id):
    if repair_id == "MR01":
        return {row["id"] for row in contract["software_cells"]}
    if repair_id == "MR02":
        return {row["id"] for row in contract["llm_tasks"]}
    return set(contract["integration_requirements"])


def validate_repair_acceptance(root, state, task, receipt):
    repair_id = task["repair_closure"]
    repair = next(r for r in state["major_repairs"] if r["id"] == repair_id)
    docs = state["repair_program"]["documents"]
    contract = bound_json(root, docs["coverage"])
    acceptance = receipt.get("repair_acceptance", {})
    fields = bound_json(root, docs["schemas"])["repair_acceptance"]["required_fields"]
    require(set(fields) <= set(acceptance), "Missing structured repair acceptance")
    require(acceptance["coverage_complete"] is True and acceptance["blocking_findings"] == [],
            "Repair has incomplete coverage or blocking findings")
    covered = bound_json(root, acceptance["coverage_review"])
    require(covered.get("repair_id") == repair_id and covered.get("status") == "pass",
            "Coverage review belongs to another repair or failed")
    rows = covered["cells"]
    require(len(rows) == len({r["id"] for r in rows}) and
            {r["id"] for r in rows} == coverage_ids(contract, repair_id),
            "Repair coverage cells are missing or duplicated")
    for row in rows:
        require(row["status"] in contract["accepted_coverage_statuses"] and
                row.get("finding") and row.get("evidence"), "Unsupported coverage disposition")
        require(isinstance(row.get("essential"), bool), "Coverage needs explicit essentiality")
        for ref in row["evidence"]:
            core.bound(root, ref)
        if row["status"] != "substantively_reviewed":
            core.bound(root, row["omission_review"])
        if row["status"] == "unavailable_with_recorded_impact":
            require(not row["essential"], "Essential unavailable coverage cannot close a repair")
    audit = bound_json(root, acceptance["source_audit"])
    require(audit.get("status") == "pass" and audit.get("unverified_claims") == [] and
            audit.get("entries"), "Incomplete primary-source audit")
    for entry in audit["entries"]:
        for key in ("identity", "version_date", "inspected_anchors", "supported_claims"):
            require(entry.get(key), "Source audit lacks " + key)
        core.bound(root, entry["local_copy"])
        if entry.get("kind") == "paper":
            path = core.safe(root, entry["local_copy"]["path"])
            expected = f"{entry['filename_title']} {entry['first_author']}({entry['year']}).pdf"
            require(path.parent == root / "docs/papers" and path.name == expected,
                    "Scholarly PDF naming/location violation")
            with path.open("rb") as stream:
                require(stream.read(5) == b"%PDF-", "Scholarly source is not a genuine PDF file")
    pages = acceptance["page_count"]
    require(pages["pdf"]["path"] in task["outputs"], "Body count must use the promised survey PDF")
    total = pdf_pages(root, pages["pdf"])
    body = pages["body_page_numbers"]
    require(body and all(type(n) is int and 1 <= n <= total for n in body)
            and len(body) == len(set(body)), "Invalid or repeated substantive body pages")
    review = bound_json(root, acceptance["chapter_review"])
    expected_chapters = {c["id"] for c in bound_json(root, docs["chapters"])["chapters"]
                         if c["repair_id"] == repair_id}
    require(review.get("status") == "pass" and review.get("blocking_findings") == [],
            "Chapter review has unresolved findings")
    require({c["id"] for c in review["chapters"]} == expected_chapters and
            len(review["chapters"]) == len(expected_chapters), "Chapter review is incomplete")
    for chapter in review["chapters"]:
        require(chapter.get("substantive") is True and chapter.get("finding"),
                "Page count cannot substitute for a substantive chapter review")
    require(review.get("pdf_sha256") == pages["pdf"]["sha256"] and
            review.get("rendered_pages_inspected") == list(range(1, total + 1)),
            "Rendered review does not cover the delivered PDF")
    require(review.get("body_page_numbers") == body, "Body-page exclusions lack matching review")
    budget = repair["page_budget"]
    if not budget["min"] <= len(body) <= budget["max"]:
        exception = bound_json(root, acceptance["page_budget_exception"])
        require(exception.get("repair_id") == repair_id and exception.get("rationale") and
                exception.get("coverage_unchanged") is True,
                "Page variance needs a reviewed rationale without a coverage waiver")
    elif acceptance["page_budget_exception"] is not None:
        core.bound(root, acceptance["page_budget_exception"])


def validate_current_assessment(root, state, receipt):
    require(state["results"].get("I02", {}).get("outcome") == "pass",
            "External acceptance requires completed I02")
    ref = receipt.get("assessed_current_release", {})
    expected = DIRECTORY + "/work/I02/delivery-manifest.json"
    require(ref.get("path") == expected, "External acceptance must assess current I02 manifest")
    core.bound(root, ref)
    delivered = bound_json(root, state["results"]["I02"])
    refs = [r for c in delivered["criteria"] for r in c["evidence"]]
    require(any(r["path"] == expected and r["sha256"] == ref["sha256"] for r in refs),
            "Assessed I02 is not the author-delivered manifest")
    require(receipt.get("scope_release_sha256") == ref["sha256"],
            "Signed scope must identify the current release")


def validate_receipt(root, state, task, receipt):
    LEGACY_VALIDATE_RECEIPT(root, state, task, receipt)
    if state.get("revision") != REVISION:
        return
    if task["id"] in EXTERNAL:
        validate_current_assessment(root, state, receipt)
    if task["id"] in STUDIES and not receipt.get("experiment"):
        require(receipt["outcome"] == "inconclusive" and
                receipt.get("evaluation_status") == "unavailable" and
                receipt.get("unavailability_evidence"),
                "Final study needs preregistration or explicit unavailable evidence")
        for ref in receipt["unavailability_evidence"]:
            core.bound(root, ref)
    if task.get("repair_closure") and receipt["outcome"] == "pass":
        validate_repair_acceptance(root, state, task, receipt)
    if task["id"] == "I02" and receipt["outcome"] == "pass":
        manifest = core.read(root, DIRECTORY + "/work/I02/delivery-manifest.json")
        require(manifest.get("repair_receipts") == {k: state["results"][v]["sha256"]
                                                   for k, v in REPAIRS.items()},
                "I02 manifest lacks all accepted repair receipts")
        for item in manifest["documents"]:
            core.bound(root, item)
        paths = {item["path"] for item in manifest["documents"]}
        require({p for p in task["outputs"] if p.endswith(".pdf")} <= paths,
                "I02 manifest lacks delivered PDFs")


def validate_state(root, state):
    issues = LEGACY_VALIDATE_STATE(root, state)
    if issues:
        return issues
    try:
        revision_contract(root, state)
        for name, ref in state["results"].items():
            task = core.task_by_id(state, name)
            if name in EXTERNAL | STUDIES | {"I02"} or task.get("repair_closure"):
                validate_receipt(root, state, task, core.read(root, ref["path"]))
    except (ValueError, KeyError, TypeError, OSError, StopIteration, subprocess.SubprocessError) as exc:
        issues.append(str(exc))
    return issues


def summary(state):
    result = LEGACY_SUMMARY(state)
    result["major_repairs"] = [{**r, "status": "author_coverage_complete" if
        state["results"].get(r["closure_task"], {}).get("outcome") == "pass" else "open"}
        for r in state.get("major_repairs", [])]
    result["acceptance_release"] = "I02"
    result["bounded_product_accepted"] = result["bounded_product_accepted"] and all(
        r["status"] == "author_coverage_complete" for r in result["major_repairs"])
    result["controller"] = "python3 tools/causal_program_v12.py"
    return result


def render(root, state):
    s = summary(state)
    open_repairs = sum(r["status"] == "open" for r in s["major_repairs"])
    reader = state["reader"]
    reader_path = str(reader["path"]).removeprefix("docs/")
    lines = ["# Mission control: causal banking master program V12", "", state["mission"], "",
        ("Bounded product accepted in its declared scope." if s["bounded_product_accepted"] else "The full product is unfinished.") +
        f" {open_repairs}/3 mandatory repairs remain open.", "",
        f"{s['completed_work_packages']}/{s['total_work_packages']} packages have dispositions; "
        f"{len(s['qualified_gaps_in_declared_scope'])}/10 original gaps fully qualified. Next: **{s['next']}**.", "",
        "[Current master program](program/master-program-v12.md) · [Repair plan PDF](program/master-program-v12.pdf) · "
        "[Plan review](program/repair-v12/plan-review.md) · [Machine state](program/state.json)", "",
        f"[Current research reader — {reader['pages']} pages]({reader_path}) · "
        "[Delivered sponsor brief — 3 pages](sponsor_execution_2026-10-11.pdf) · "
        "[Preserved V11 plan](program/master-program.md)", "",
        "| Mandatory repair | Status | Substantive body allocation | Closure |", "|---|---|---|---|"]
    for r in s["major_repairs"]:
        b = r["page_budget"]
        lines.append(f"| {r['id']} {r['name']} | {r['status']} | {b['min']}–{b['max']} pages | {r['closure_task']} |")
    lines += ["", "Software: 10 chapters. LLMs/agents: 8 chapters. Integration: 4 chapters; its 40–60 pages are an indicative allocation. "
              "These allocations are not completed pages. I02 cannot pass before all three coverage gates pass.", "",
              "| Package | Disposition | Dependency or missing input |", "|---|---|---|"]
    lines += [f"| {r['id']} {r['name']} | {r['status']} | {'; '.join(r['blockers']) or '—'} |"
              for r in s["work_packages"]]
    lines += ["", "## Original scientific and institutional gaps", "",
              "| Gap | Current evidence | Next route |", "|---|---|---|"]
    lines += [f"| {g['id']} {g['name']} | {g['current']} | {g['route']} |" for g in state["gaps"]]
    lines += ["", "V12 execution: `python3 tools/causal_program_v12.py next`; integrity: "
        "`python3 tools/causal_program_v12.py check`. Compatibility: `python3 tools/causal_program.py status` "
        "and `python3 tools/causal_program.py check`. Use the V12 command for all mutations and dashboard rendering.", "",
        "[Versioned work cards](program/repair-v12/work-packages.json) · "
        "[Coverage contract](program/repair-v12/coverage-contract.json) · "
        "[Next continuation](program/repair-v12/continuation.md) · "
        "[External input requirements](program/master/external-inputs.md)", "",
        "One canonical state governs this program. Negative studies can inform scholarship while leaving capabilities unqualified. "
        "External review must assess I02. Independent acceptance, bank truth, platform acceptance and measured institutional ROI remain absent.", ""]
    md = "\n".join(lines)
    (root / "docs/mission-control.md").write_text(md)
    body = subprocess.run(["pandoc", "--from=gfm", "--to=html"], input=md, text=True,
                          capture_output=True, check=True, timeout=20).stdout
    page = "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>Causal banking V12</title><style>body{font:17px system-ui;max-width:1200px;margin:3rem auto;padding:0 1.5rem;color:#183047}table{border-collapse:collapse;width:100%}td,th{padding:.65rem;border-bottom:1px solid #d4dde5;text-align:left}a{color:#075f87}code{font-size:.85em}</style></head><body>" + body + "</body></html>"
    (root / "docs/mission-control.html").write_text(page)


def install_hooks():
    core.validate_state = validate_state
    core.validate_receipt = validate_receipt
    core.summary = summary
    core.render = render


def cli():
    install_hooks()
    if len(sys.argv) > 1 and sys.argv[1] in {"next", "template"}:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            core.cli()
        result = json.loads(captured.getvalue())
        if result.get("completion_command"):
            result["completion_command"] = result["completion_command"].replace(
                "tools/causal_program.py", "tools/causal_program_v12.py")
        if sys.argv[1] == "template":
            result["v12_instructions"] = (
                "Closure tasks require repair_acceptance; final studies require registered evidence or explicit unavailable evidence. "
                "External tasks require legacy I01 lineage plus assessed_current_release and scope_release_sha256 for I02. "
                "See docs/program/repair-v12/receipt-contract.md.")
        print(json.dumps(result, indent=2))
    else:
        core.cli()
