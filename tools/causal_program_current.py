#!/usr/bin/env python3
"""Current reader/program view over unchanged V12 work and acceptance contracts.

The historical controller and source register are preserved. This entrypoint
adds verification of the complete integrated working document and renders its
current execution addendum. It does not loosen any V12 receipt/coverage gate.
"""
import contextlib
import io
import json
import subprocess
import sys

import master_control as core
import repair_control_v12 as v12
import build_integrated_monograph_v12 as book


def verify_working_document(root, state):
    working = state.get("working_document")
    if not working:
        return None
    for key in ("build_report", "source_audit", "driver", "program_update", "program_update_pdf", "review"):
        core.bound(root, working[key])
    report = core.read(root, working["build_report"]["path"])
    require = v12.require
    require(state["reader"]["path"] == report["pdf"]["path"], "Current reader differs from checked working book")
    require(state["reader"]["pages"] == report["pages"], "Current reader page count differs")
    require(working["status"] == "integrated_working_draft" and report["final_release"] is False,
            "A working reader cannot claim final acceptance")
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        book.check()
    return json.loads(captured.getvalue())


def render(root, state):
    v12.render(root, state)
    working = state.get("working_document")
    if not working:
        return
    md_path = root / "docs/mission-control.md"
    md = md_path.read_text()
    current = working["program_update"]["path"].removeprefix("docs/")
    pdf = working["program_update_pdf"]["path"].removeprefix("docs/")
    review = working["review"]["path"].removeprefix("docs/")
    md = md.replace("(program/master-program-v12.md)", "(" + current + ")")
    md = md.replace("(program/master-program-v12.pdf)", "(" + pdf + ")")
    md = md.replace("(program/repair-v12/plan-review.md)", "(" + review + ")")
    md = md.replace("Current research reader", "Integrated working monograph")
    md = md.replace("python3 tools/causal_program_v12.py", "python3 tools/causal_program_current.py")
    report = core.read(root, working["build_report"]["path"])
    pages = report["physical_body_pages"]
    text = (f"Current book: {report['pages']} pages and {report['numbered_chapters']} numbered chapters, "
            "with one contents page sequence and bibliography. Developed repair material is integrated: "
            f"software {pages['software']} physical body pages (5 drafts), LLMs {pages['llm']} (8 drafts), "
            f"integration {pages['integration']} (4 drafts). These are not accepted substantive-page counts. "
            "The preserved I01 delivery remains available; final visual review and all three repair gates remain open.\n\n")
    md = md.replace("| Mandatory repair |", text + "| Mandatory repair |", 1)
    md_path.write_text(md)
    html = subprocess.run(["pandoc", "--from=gfm", "--to=html"], input=md,
                          capture_output=True, text=True, check=True, timeout=20).stdout
    html_path = root / "docs/mission-control.html"
    old = html_path.read_text()
    html_path.write_text(old.split("<body>")[0] + "<body>" + html + "</body></html>")


def install_hooks():
    v12.install_hooks()
    core.render = render
    def current_summary(state):
        result = v12.summary(state)
        result["controller"] = "python3 tools/causal_program_current.py"
        result["program_view"] = state["repair_program"]["master"]
        return result
    core.summary = current_summary


def main():
    install_hooks()
    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command == "check":
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            try:
                core.cli()
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    print(captured.getvalue(), end="", file=sys.stderr)
                    raise
        result = json.loads(captured.getvalue())
        result["working_document"] = verify_working_document(core.ROOT, core.read(core.ROOT, core.STATE))
        result["scope"] += " Current wrapper also verifies the integrated working manuscript and its complete source audit."
        print(json.dumps(result, indent=2))
    elif command in {"next", "template"}:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            v12.cli()
        # v12.cli installs its own renderer, but these commands are read-only.
        print(captured.getvalue().replace("tools/causal_program_v12.py", "tools/causal_program_current.py"), end="")
    else:
        if command in {"record", "register", "intake", "reopen", "render"}:
            verify_working_document(core.ROOT, core.read(core.ROOT, core.STATE))
        core.cli()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, AssertionError, subprocess.SubprocessError) as exc:
        raise SystemExit(str(exc))
