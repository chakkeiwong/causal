#!/usr/bin/env python3
"""Compile selected software chapters with verified source and example records.

This produces an interim reader. It cannot certify SW01/SW09 or visual review.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

from enrich_sw01_v12 import verify_local

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/program/repair-v12"
WORK = BASE / "work/SW01"
OUT = BASE / "software-reader"


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def escape(value):
    return "".join({"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
                    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
                    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}.get(c, c) for c in value)


def binding(path, anchor):
    return {"path": str(path.relative_to(ROOT)), "sha256": digest(path), "anchor": anchor}


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    chapter = WORK / "software-chapters.tex"
    manuscript = chapter.read_text()
    cited = {key.strip() for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", manuscript) for key in group.split(",")}
    records = {x["id"].split(":")[-1]: x for x in load(WORK / "pinned-package-review.json")["records"]}
    assert cited <= records.keys(), cited - records.keys()
    examples = load(WORK / "software-contract-examples.json")
    assert examples["script_sha256"] == digest(ROOT / "tools/software_contract_examples_v12.py")
    assert examples["status"] == "exact_checks_pass" and examples["external_packages_run"] == 0
    catalog = {x["id"]: x for x in load(WORK / "catalog.json")["candidates"]}
    bib = [r"\begin{thebibliography}{99}"]
    for key in sorted(cited):
        entry = records[key]
        verify_local(entry)
        row = catalog[entry["candidate_id"]]
        name = row.get("audited_component", entry.get("display", row["name"]))
        description = escape(name + ". Selected official package documentation and source, version " + entry["observed_version"] + ". ")
        description += r"Revision \nolinkurl{" + entry["commit"] + "}; " + escape(entry["commit_date"] + ". ")
        description += r"\url{" + entry["source_identity"] + "/tree/" + entry["commit"] + "}."
        bib.append(r"\bibitem{" + key + "} " + description)
    bib.append(r"\end{thebibliography}")
    (OUT / "references.tex").write_text("\n".join(bib) + "\n")
    preamble = r"""\documentclass[11pt,openany]{book}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[a4paper,margin=27mm]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array}
\usepackage{xurl}
\usepackage[hidelinks]{hyperref}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\title{Causal software for banking decisions\\\large Selected comparative research chapters}
\author{Causal banking research program}
\date{12 October 2026\\Source cutoff: 7 October 2026}
\begin{document}
\pagestyle{plain}
\raggedbottom
\maketitle
\thispagestyle{empty}
\noindent This interim reader develops selected comparisons across twenty-two
software families and five exact project examples. The sources are genuine
locally archived package documentation and code at recorded revisions. External
package code was inspected, not executed. The banking examples are stipulated
mechanisms and arithmetic, not bank data or package benchmarks. The full
software census, commercial comparison, remaining monograph chapters and final
release remain unfinished. This reader has compilation and text checks; final
visual review requires a fresh session. It does not close the software repair.
\tableofcontents
"""
    driver = OUT / "reader.tex"
    driver.write_text(preamble + r"\input{docs/program/repair-v12/work/SW01/software-chapters.tex}" + "\n" +
                      r"\label{sw:body-end}\clearpage" + "\n" +
                      r"\input{docs/program/repair-v12/software-reader/references.tex}" + "\n" + r"\end{document}" + "\n")
    for i in range(2):
        with (OUT / f"build-{i + 1}.log").open("w") as log:
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                            "-output-directory=" + str(OUT), str(driver)], cwd=ROOT, stdout=log,
                           stderr=subprocess.STDOUT, check=True, timeout=60)
    pdf = OUT / "reader.pdf"
    subprocess.run(["pdftotext", "-layout", str(pdf), str(OUT / "reader.txt")], check=True, timeout=30)
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    log = (OUT / "reader.log").read_text(errors="replace")
    warnings = [line for line in log.splitlines() if any(x in line for x in ["Warning", "Overfull", "Underfull", "Missing character"])]
    text = (OUT / "reader.txt").read_text()
    assert "???" not in text
    aux = (OUT / "reader.aux").read_text()
    labels = {m.group(1): int(m.group(2)) for m in re.finditer(r"\\newlabel\{(sw:[^}]+)\}\{\{[^}]*\}\{(\d+)\}", aux)}
    assert len(re.findall(r"\\chapter\{", manuscript)) == 5
    body_pages = labels["sw:body-end"] - labels["sw:interfaces"] + 1
    audit = {"scope": "Citations in selected software interim reader; not the complete software census",
             "manuscript": binding(chapter, "Five connected comparative chapters"),
             "sources": [records[key] for key in sorted(cited)],
             "project_examples": binding(WORK / "software-contract-examples.json", "Five exact project examples with no external package execution"),
             "example_code": binding(ROOT / "tools/software_contract_examples_v12.py", "Exact rational arithmetic and explicit checks"),
             "citation_identity_status": "all_cited_records_and_local_source_bytes_verified"}
    (OUT / "source-audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
    report = {"status": "compiled_text_checks_only", "pdf": str(pdf.relative_to(ROOT)), "sha256": digest(pdf),
              "pages": pages, "body_pages": body_pages, "chapters": 5, "cited_primary_records": len(cited),
              "project_example_families": 5, "warnings": warnings,
              "manuscript_words_whitespace_count": len(manuscript.split()),
              "source_audit": binding(OUT / "source-audit.json", "All twenty-two cited package/source families"),
              "chapter_pages": labels, "rendered_visual_review": "pending fresh session; current image budget exhausted",
              "full_software_repair_closed": False, "final_release": False}
    (OUT / "build-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    build()
