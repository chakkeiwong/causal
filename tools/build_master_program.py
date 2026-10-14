#!/usr/bin/env python3
"""Build the integrated program reader, without rebuilding frozen research PDFs."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "docs/program/master"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    state = json.loads((ROOT / "docs/program/state.json").read_text())
    contracts = {key: state[key] for key in ("revision", "streams", "gaps", "work_packages", "external_inputs")}
    (FOLDER / "contracts.json").write_text(json.dumps(contracts, indent=2) + "\n")
    cards = ["# Work-package execution cards", "",
             "These cards are generated from the canonical machine contracts. Live dispositions are in Mission Control. "
             "A positive package result does not automatically close its assigned gaps; each has a separate reviewed disposition.", ""]
    for task in sorted(state["work_packages"], key=lambda x: x["priority"]):
        cards += ["## " + task["id"] + ": " + task["name"], "",
                  "Owner: " + task["owner"] + ". Gaps: " + ", ".join(task["gaps"]) + ".", "",
                  "Prerequisites: " + ("; ".join(d["id"] + " (" + "/".join(d["outcomes"]) + ")" for d in task["depends"]) or "none") + ".", ""]
        if task["requires_inputs"]:
            cards += ["External inputs: " + ", ".join(task["requires_inputs"]) + ".", ""]
        cards += ["Execution:", ""] + [f"{i}. {s}" for i, s in enumerate(task["steps"], 1)]
        cards += ["", "Acceptance:", ""] + ["- " + c["id"] + ": " + c["statement"] for c in task["criteria"]]
        cards += ["", "Outputs:", ""] + ["- " + p for p in task["outputs"]]
        cards += ["", "Failure or inconclusive result: " + task["failure_action"], ""]
    (FOLDER / "work-packages.md").write_text("\n".join(cards))
    sources = [ROOT / "docs/program/master-program.md",
               FOLDER / "capability-contracts.md", FOLDER / "evaluation-protocol.md",
               FOLDER / "external-inputs.md", FOLDER / "work-packages.md"]
    content = "\n\n".join(p.read_text() for p in sources)
    # The appendix is read from subdirectories; make its local PDF links agree
    # with the final PDF location at docs/program/.
    content = content.replace("](../external-validation-", "](external-validation-")
    (FOLDER / "master-reader.md").write_text(content)
    header = FOLDER / "pdf-header.tex"
    header.write_text("\\usepackage{microtype}\n\\usepackage{xurl}\n\\setlength{\\emergencystretch}{3em}\n\\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}\n")
    command = ["pandoc", str(FOLDER / "master-reader.md"), "--from=markdown+pipe_tables+raw_tex",
               "--standalone", "--to=latex", "--top-level-division=section",
               "-V", "documentclass=article", "-V", "fontsize=11pt", "-V", "papersize=a4",
               "-V", "geometry:margin=22mm", "-V", "linestretch=1.05",
               "--include-in-header", str(header), "-o", str(FOLDER / "master-reader.tex")]
    subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True, timeout=30)
    for step in range(2):
        run = subprocess.run(["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "master-reader.tex"],
                             cwd=FOLDER, capture_output=True, text=True, timeout=60)
        (FOLDER / f"build-{step}.txt").write_text(run.stdout + run.stderr)
        if run.returncode:
            raise RuntimeError((run.stdout + run.stderr)[-4000:])
    log = (FOLDER / "master-reader.log").read_text()
    warnings = re.findall(r"(?m)^.*(?:Overfull|Undefined|LaTeX Warning|Package .* Warning|! LaTeX Error).*$", log)
    target = ROOT / "docs/program/master-program.pdf"
    target.write_bytes((FOLDER / "master-reader.pdf").read_bytes())
    info = subprocess.run(["pdfinfo", str(target)], capture_output=True, text=True, check=True, timeout=10).stdout
    pages = int(re.search(r"(?m)^Pages:\s+(\d+)", info).group(1))
    inputs = sources + [Path(__file__), header, FOLDER / "contracts.json", FOLDER / "master-reader.tex"]
    receipt = {"status": "pass" if not warnings else "needs_layout_review", "issues": warnings,
               "path": str(target.relative_to(ROOT)), "pages": pages, "sha256": sha(target),
               "input_sha256": {str(p.relative_to(ROOT)): sha(p) for p in inputs},
               "scope": "Program compilation and input identities only; actual rendered inspection is separate."}
    (ROOT / "docs/reviews/master-program-build.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "input_sha256"}, indent=2))


if __name__ == "__main__":
    main()
