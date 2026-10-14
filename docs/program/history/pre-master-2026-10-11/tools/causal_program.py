#!/usr/bin/python3
"""Local mission control, inventory and document checks; no privileged actions."""
import argparse
import collections
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs/program/state.json"


def read_json(path):
    return json.loads(path.read_text())


def inventory():
    rows = []
    roots = [Path("/home/ubuntu/google-drive-papers"), Path("/home/ubuntu/workspace/FinMarketing/docs/papers")]
    for root in roots:
        for path in root.rglob("*.pdf"):
            rows.append({"path": str(path), "title_hint": path.stem, "bytes": path.stat().st_size})
    target = ROOT / "docs/literature/local-inventory.json"
    target.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    projects = []
    for folder in sorted(Path("/home/ubuntu/workspace").iterdir()):
        if not folder.is_dir() or folder.name == "causal":
            continue
        row = {"name": folder.name, "path": str(folder), "evidence": []}
        for name in ("README.md", "pyproject.toml", "setup.py"):
            path = folder / name
            if path.is_file():
                raw = path.read_bytes()
                row["evidence"].append({"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "excerpt": raw.decode("utf-8", errors="replace")[:14000]})
        projects.append(row)
    (ROOT / "docs/literature/workspace-inventory.json").write_text(json.dumps(projects, indent=2) + "\n")
    print(json.dumps({"local_pdfs": len(rows), "projects": len(projects)}))


def render():
    state = read_json(STATE)
    gap_review = str(Path(state.get("gap_review", "docs/reviews/remaining-gaps-v4-2026-10-08.md")).relative_to("docs"))
    review = str(Path(state.get("author_review", "docs/reviews/reconstruction-adversarial-review.md")).relative_to("docs"))
    lines = ["# Mission control: causal inference for a banking group", "", f"Updated: {state['updated']} (Asia/Shanghai).", "", state["mission"], "", f"**Current state:** {state['status']}", "", f"**Next action:** {state['next_action']}", "", "[Master program](program/master-program.md) · [Reconstruction review](reviews/reconstruction-adversarial-review.md) · [Source register](literature/sources.json)", "", "| Phase | Status | Deliverable |", "|---|---|---|"]
    if state.get("plan"):
        plan_target = str(Path(state["plan"]).relative_to("docs"))
        lines[10:10] = [f"[Scientific completion plan]({plan_target}) · [Comparative gap review]({gap_review})", ""]
    table = []
    for phase in state["phases"]:
        lines.append(f"| {phase['id']} {phase['name']} | {phase['status']} | {phase['deliverable']} |")
        table.append("<tr>" + "".join(f"<td>{html.escape(str(phase[k]))}</td>" for k in ("id", "name", "status", "deliverable")) + "</tr>")
    lines += ["", "## Deliverables", "",
              f"- [Research monograph](causal_foundations.pdf) · [LaTeX source](causal_foundations.tex) · [Author review]({review})",
              "- [Sponsor proposal](sponsor_reconstruction.pdf) · [LaTeX source](sponsor_reconstruction.tex) · [Substantive repairs](reviews/reconstruction-adversarial-review.md)",
              "- [Source-to-question matrix](literature/source-question-matrix.md) · [Current claim trace](literature/reconstruction-claims.md) · [Source and build audit](reviews/foundations-audit.json)",
              "- [Scholarly reset](reviews/scholarship-reset-2026-10-08.md) · [Theory map](program/theory-map.md)",
              "- [Withdrawn version 2 technical PDF](causal_banking_product.pdf) · [LaTeX source](causal_banking_product.tex)",
              "- [Withdrawn version 2 sponsor PDF](sponsor_proposal.pdf)",
              "- [Searchable paper/source archive](papers/index.html) · [Software assessment](literature/software-assessment.md)",
              "- [Reusable contracts](../contracts/README.md) · [Research components](../src/causalbank/) · [Fitted studies and measurements](derivations/README.md)",
              "- [Scientific completion studies](studies/README.md) · [Installed operation checks](reviews/interface-qualification.json) · [Standalone requests](reviews/standalone-qualification.json)",
              "- [Delivery and remaining obligations](program/delivery.md) · [Rendered inspection](reviews/reconstruction-visual-inspection.md) · [Historical version 2 review](reviews/revision-review.md)",
              "- [Historical author review](reviews/final-review.md) · [Historical archive audit](reviews/archive-audit.json)",
              "- [Coverage and omissions](literature/coverage-and-omissions.md) · [Earlier material claims](literature/claims.md)",
              "", "## Completion boundaries", ""] + [f"- {b}" for b in state["boundaries"]]
    lines += ["", "## Evidence and continuation", "", "Machine state: `docs/program/state.json`. Phase receipts: `docs/program/phase-results.md`.", "This dashboard is a durable record, not a background scheduler.", ""]
    (ROOT / "docs/mission-control.md").write_text("\n".join(lines))
    page = "<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>Causal banking mission control</title><style>body{font:17px system-ui;max-width:1200px;margin:45px auto;padding:0 24px;color:#17324d;background:#f7f9fc}h1{font-size:34px}table{border-collapse:collapse;background:white;width:100%}td,th{padding:16px;border-bottom:1px solid #ccd5df;text-align:left;vertical-align:top}a{color:#005e91}.card{padding:22px;background:#e9f1f6;margin:24px 0;border-left:5px solid #23788a}li{margin:12px 0}</style><h1>Causal inference for a banking group</h1>"
    page += f"<p>{html.escape(state['mission'])}</p><div class='card'><b>{html.escape(state['status'])}</b><p>Next: {html.escape(state['next_action'])}</p></div>"
    if state.get("plan"):
        page += f"<p><a href='{html.escape(plan_target, quote=True)}'>Scientific completion plan</a> · <a href='{html.escape(gap_review, quote=True)}'>Comparative gap review</a></p>"
    page += f"<p><a href='causal_foundations.pdf'>Research monograph</a> · <a href='causal_foundations.tex'>LaTeX source</a> · <a href='sponsor_reconstruction.pdf'>Sponsor proposal</a> · <a href='sponsor_reconstruction.tex'>Sponsor LaTeX source</a> · <a href='{html.escape(review, quote=True)}'>Author review</a></p>"
    page += "<p><a href='reviews/reconstruction-adversarial-review.md'>Substantive review and repairs</a> · <a href='reviews/reconstruction-visual-inspection.md'>Rendered inspection</a> · <a href='literature/source-question-matrix.md'>Source-to-question matrix</a> · <a href='literature/reconstruction-claims.md'>Current claims</a> · <a href='reviews/foundations-audit.json'>Source and build audit</a></p>"
    page += "<p><a href='program/master-program.md'>Active reconstruction program</a> · <a href='reviews/scholarship-reset-2026-10-08.md'>Scholarly reset</a> · <a href='program/theory-map.md'>Theory map</a> · <a href='causal_banking_product.pdf'>Withdrawn version 2 technical PDF</a> · <a href='sponsor_proposal.pdf'>Withdrawn version 2 sponsor PDF</a></p>"
    page += "<p><a href='papers/index.html'>Search the saved source archive</a> · <a href='literature/software-assessment.md'>44-project software assessment</a> · <a href='../contracts/README.md'>Reusable contracts</a> · <a href='derivations/README.md'>Fitted studies and measurements</a></p>"
    page += "<p><a href='studies/README.md'>Scientific completion studies</a> · <a href='reviews/interface-qualification.json'>Installed operation checks</a> · <a href='reviews/standalone-qualification.json'>Standalone requests</a></p>"
    page += "<p><a href='program/delivery.md'>Delivery and remaining obligations</a> · <a href='reviews/revision-review.md'>Seven-question revision review</a> · <a href='../src/causalbank/'>Research components</a></p>"
    page += "<p><a href='reviews/final-review.md'>Historical author review</a> · <a href='reviews/archive-audit.json'>Historical archive audit</a> · <a href='literature/claims.md'>Earlier material claims</a> · <a href='literature/coverage-and-omissions.md'>Coverage and omissions</a> · <a href='program/phase-results.md'>Phase execution record</a></p>"
    page += "<table><tr><th>Phase</th><th>Work</th><th>Status</th><th>Deliverable</th></tr>" + "".join(table) + "</table><h2>Evidence boundaries</h2><ul>"
    page += "".join(f"<li>{html.escape(x)}</li>" for x in state["boundaries"]) + "</ul><p>Updated " + html.escape(state["updated"]) + ". This is a saved dashboard, not a background scheduler.</p></html>"
    (ROOT / "docs/mission-control.html").write_text(page)
    print("Mission control rendered")


def check():
    state = read_json(STATE)
    issues = []
    ids = {p["id"] for p in state["phases"]}
    complete = {p["id"] for p in state["phases"] if p["status"] == "complete"}
    historical = {p["id"] for p in state["phases"] if p["status"] == "historical"}
    if state.get("revision") in ("3.0-reconstruction", "4.0-scientific-completion", "5.0-scope-completion", "6.0-dynamic-construction", "6.1-linkage-inference", "7.0-gap-closure", "8.0-reliability-extension", "9.0-calibration-completion", "10.0-precision-streaming"):
        manifest = read_json(ROOT / "docs/program/delivery-manifest.json")
        if manifest.get("status") != "withdrawn":
            issues.append("Reconstruction requires the version 2 delivery to be withdrawn")
        if any(p["status"] != "historical" for p in state["phases"] if p["id"].startswith(("P", "Q"))):
            issues.append("P/Q phases must be historical during reconstruction")
    for phase in state["phases"]:
        if set(phase["depends"]) - ids:
            issues.append(f"Unknown phase dependency: {phase['id']}")
        if phase["status"] == "complete":
            if set(phase["depends"]) - complete:
                issues.append(f"Incomplete prerequisite: {phase['id']}")
            for path in phase["evidence"]:
                if not (ROOT / path).is_file():
                    issues.append(f"Missing phase evidence: {path}")
            if not phase["evidence"]:
                issues.append(f"No phase evidence: {phase['id']}")
    citations = set()
    labels = []
    refs = set()
    for tex in (ROOT / "docs").rglob("*.tex"):
        if "build" in tex.parts or "history" in tex.parts:
            continue
        raw = re.sub(r"(?m)(?<!\\)%.*$", "", tex.read_text())
        for match in re.finditer(r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}", raw):
            citations.update(k.strip() for k in match.group(1).split(","))
        labels.extend(re.findall(r"\\label\{([^}]+)\}", raw))
        refs.update(re.findall(r"\\(?:ref|eqref|cref|Cref)\{([^}]+)\}", raw))
    sources_path = ROOT / "docs/literature/sources.json"
    sources = read_json(sources_path) if sources_path.exists() else []
    keyed = {s["id"]: s for s in sources}
    for key in citations:
        if key not in keyed:
            issues.append(f"Citation absent from source register: {key}")
            continue
        source = keyed[key]
        for field in ("title", "authors", "year", "url", "local_path", "sha256", "inspected", "claims", "version_status"):
            if not source.get(field):
                issues.append(f"Missing {field}: {key}")
        path = ROOT / source.get("local_path", "MISSING")
        if not path.is_file():
            issues.append(f"Missing source copy: {key}")
        else:
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != source.get("sha256"):
                issues.append(f"Source hash mismatch: {key}")
            if source.get("kind") == "paper":
                expected = f"{source['filename_title']} {source['first_author']}({source['year']}).pdf"
                if path.parent != ROOT / "docs/papers" or path.name != expected or not data.startswith(b"%PDF-"):
                    issues.append(f"Paper naming/content rule violated: {key}")
    for label, n in collections.Counter(labels).items():
        if n > 1:
            issues.append(f"Duplicate label: {label}")
    for ref in refs - set(labels):
        issues.append(f"Missing label: {ref}")
    result = {"status": "pass" if not issues else "fail", "scope": "Internal consistency and cited source identity, not scholarly sufficiency", "phases": len(ids), "completed_phases": len(complete), "historical_phases": len(historical), "cited_works": len(citations), "registered_works": len(sources), "issues": issues}
    (ROOT / "docs/program/consistency-check.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(issues))


def build():
    docs = ROOT / "docs"
    build_dir = docs / "build"
    build_dir.mkdir(exist_ok=True)
    state = read_json(STATE)
    stems = ("causal_foundations", "sponsor_reconstruction") if state.get("revision") in ("3.0-reconstruction", "4.0-scientific-completion", "5.0-scope-completion", "6.0-dynamic-construction", "6.1-linkage-inference", "7.0-gap-closure", "8.0-reliability-extension", "9.0-calibration-completion", "10.0-precision-streaming") else ("causal_banking_product", "sponsor_proposal")
    documents = []
    for stem in stems:
        commands = [["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-output-directory=build", stem + ".tex"], ["bibtex", "build/" + stem]]
        commands.extend([commands[0]] * 3)
        for n, command in enumerate(commands):
            result = subprocess.run(command, cwd=docs, text=True, capture_output=True, timeout=120)
            (build_dir / f"{stem}.step{n}.txt").write_text(result.stdout + result.stderr)
            if result.returncode:
                print((result.stdout + result.stderr)[-7000:])
                raise SystemExit(result.returncode)
        shutil.copyfile(build_dir / (stem + ".pdf"), docs / (stem + ".pdf"))
        documents.append({"path": "docs/" + stem + ".pdf",
                          "sha256": hashlib.sha256((docs / (stem + ".pdf")).read_bytes()).hexdigest()})
        print(f"Built docs/{stem}.pdf")
    if state.get("revision") in ("3.0-reconstruction", "4.0-scientific-completion", "5.0-scope-completion", "6.0-dynamic-construction", "6.1-linkage-inference", "7.0-gap-closure", "8.0-reliability-extension", "9.0-calibration-completion", "10.0-precision-streaming"):
        inputs = [Path(__file__).resolve(), docs / "preamble.tex", docs / "causal_banking_refs.bib"]
        inputs.extend(docs / (stem + ".tex") for stem in stems)
        inputs.extend(sorted((docs / "reconstruction").glob("*.tex")))
        inputs.extend(p for p in sorted((docs / "derivations").iterdir()) if p.suffix in (".tex", ".pdf"))
        receipt = {"status": "pass", "documents": documents,
                   "input_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
                   "scope": "Build input and output identities; layout and scholarship require separate review."}
        (docs / "reviews/reconstruction-build.json").write_text(json.dumps(receipt, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["status", "render", "check", "inventory", "build"])
    command = parser.parse_args().command
    if command == "status":
        s = read_json(STATE)
        print(json.dumps({"status": s["status"], "next_action": s["next_action"], "phases": [{"id": p["id"], "status": p["status"]} for p in s["phases"]]}, indent=2))
    else:
        globals()[command]()


if __name__ == "__main__":
    main()
