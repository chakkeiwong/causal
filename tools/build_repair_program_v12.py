#!/usr/bin/env python3
"""Build a standalone governance reader; do not rebuild any research release."""
import json
from pathlib import Path
import re
import subprocess

import master_control as core

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/program/repair-v12"


def main():
    chapters = core.read(ROOT, "docs/program/repair-v12/chapter-plan.json")["chapters"]
    tasks = core.read(ROOT, "docs/program/repair-v12/work-packages.json")
    content = (ROOT / "docs/program/master-program-v12.md").read_text()
    content += "\n\n\\newpage\n\n# Appendix: chapter allocations\n\n"
    for rid, title in (("MR01", "Software: 100–150 substantive pages"),
                       ("MR02", "LLMs and agents: approximately 100 pages"),
                       ("MR03", "Integration: indicative 40–60 pages")):
        content += "\n## " + title + "\n\n| ID | Chapter | Range | Target |\n|---|---|---|---|\n"
        for row in chapters:
            if row["repair_id"] != rid:
                continue
            b = row["body_pages"]
            content += f"| {row['id']} | {row['title']} | {b['min']}–{b['max']} | {b['target']} |\n"
    content += "\n\\newpage\n\n# Appendix: execution cards at a glance\n\n"
    content += "Full steps, versioned outputs, criteria and failure actions are in the bound work-packages.json register. "
    content += "The table identifies the executable dependency order; P/N/I means pass, negative or inconclusive may feed the next investigation.\n\n"
    content += "| ID | Work package | Prerequisites |\n|---|---|---|\n"
    for task in tasks:
        deps = "; ".join(d["id"] + (" (P/N/I)" if len(d["outcomes"]) > 1 else " (pass)") for d in task["depends"])
        content += f"| {task['id']} | {task['name']} | {deps} |\n"
    content += "\n# How to resume\n\nThe dashboard is docs/mission-control.md. "
    content += "Read the current state and use the successor controller:\n\n"
    content += "    python3 tools/causal_program_v12.py status\n    python3 tools/causal_program_v12.py check\n    python3 tools/causal_program_v12.py next\n\n"
    content += "Installation completes P12 only. No planned chapter, live model benchmark or consumer adoption is completed by this plan.\n"
    (BASE / "plan-reader.md").write_text(content)
    (BASE / "pdf-header.tex").write_text("\\usepackage{microtype}\n\\usepackage{xurl}\n\\setlength{\\emergencystretch}{3em}\n\\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}\n")
    command = ["pandoc", "plan-reader.md", "--from=markdown+pipe_tables+raw_tex", "--standalone", "--to=latex",
               "-V", "documentclass=article", "-V", "fontsize=11pt", "-V", "papersize=a4",
               "-V", "geometry:margin=22mm", "-V", "linestretch=1.05",
               "--include-in-header", "pdf-header.tex", "-o", "plan-reader.tex"]
    subprocess.run(command, cwd=BASE, capture_output=True, text=True, check=True, timeout=30)
    for i in range(2):
        run = subprocess.run(["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "plan-reader.tex"],
                             cwd=BASE, capture_output=True, text=True, timeout=60)
        (BASE / f"build-{i}.txt").write_text(run.stdout + run.stderr)
        if run.returncode:
            raise RuntimeError((run.stdout + run.stderr)[-3000:])
    log = (BASE / "plan-reader.log").read_text()
    warnings = re.findall(r"(?m)^.*(?:Overfull|Undefined|LaTeX Warning|Package .* Warning|! LaTeX Error).*$", log)
    target = ROOT / "docs/program/master-program-v12.pdf"
    target.write_bytes((BASE / "plan-reader.pdf").read_bytes())
    import repair_control_v12 as v12
    ref = v12.reference(ROOT, str(target.relative_to(ROOT)), "Rendered V12 governance plan")
    receipt = {"status": "pass" if not warnings else "needs_layout_review", "warnings": warnings,
        **ref, "pages": v12.pdf_pages(ROOT, ref),
        "input_sha256": {str(p.relative_to(ROOT)): core.sha(p) for p in [
            ROOT / "docs/program/master-program-v12.md", BASE / "chapter-plan.json", BASE / "work-packages.json",
            BASE / "plan-reader.md", BASE / "plan-reader.tex", Path(__file__)]},
        "scope": "Compilation and identities only; rendered inspection is recorded separately."}
    core.write(BASE / "build.json", receipt)
    print(json.dumps({k: v for k, v in receipt.items() if k != "input_sha256"}, indent=2))


if __name__ == "__main__":
    main()
