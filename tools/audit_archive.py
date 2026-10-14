#!/usr/bin/env python3
"""Audit source bytes, nested manifests, claims and actual compiled citations."""
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "docs/literature"


def read(path):
    return json.loads((ROOT / path).read_text())


def main():
    issues = []
    checked = {}
    def check_file(path, expected=None):
        p = ROOT / path
        if not p.is_file():
            issues.append("Missing: " + path)
            return
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        checked[path] = actual
        if expected and actual != expected:
            issues.append("Hash mismatch: " + path)

    sources = read("docs/literature/sources.json")
    keyed = {s["id"]:s for s in sources}
    manuscript_labels = set()
    for path in (ROOT / "docs").rglob("*.tex"):
        if "build" not in path.parts:
            manuscript_labels.update(re.findall(r"\\label\{([^}]+)\}", path.read_text()))
    if len(keyed) != len(sources):
        issues.append("Duplicate source IDs")
    paper_paths = set()
    pdf_pages = {}
    for s in sources:
        for field in ("title","authors","year","kind","version_status","url","local_path","sha256","inspected","claims","limits"):
            if not s.get(field):
                issues.append("Incomplete source "+s["id"]+": "+field)
        check_file(s["local_path"], s["sha256"])
        for a in s.get("auxiliary_artifacts", []):
            check_file(a["path"], a["sha256"])
        if s["kind"] == "paper":
            expected = f"{s['filename_title']} {s['first_author']}({s['year']}).pdf"
            if Path(s["local_path"]).name != expected or Path(s["local_path"]).parent != Path("docs/papers"):
                issues.append("Paper filename mismatch: "+s["id"])
            paper_paths.add(s["local_path"])
        if s["local_path"].endswith(".pdf"):
            p = ROOT/s["local_path"]
            if not p.read_bytes().startswith(b"%PDF-"):
                issues.append("Not PDF: "+str(p))
            info = subprocess.run(["pdfinfo",str(p)],text=True,capture_output=True)
            match = re.search(r"(?m)^Pages:\s+(\d+)", info.stdout)
            if info.returncode or not match:
                issues.append("Unreadable PDF: "+s["id"])
            else:
                pdf_pages[s["id"]] = int(match.group(1))
        if s["kind"] == "software":
            for a in read(s["local_path"])["artifacts"]:
                check_file(a["path"],a["sha256"])
        if s["id"] == "localrepos":
            for a in read(s["local_path"]):
                check_file(a["snapshot_path"],a["sha256"])
    for r in read("docs/literature/request-ledger.json"):
        if r.get("status") == "saved":
            check_file(r["path"],r["sha256"])
    for row in read("docs/literature/claims.json"):
        if row["manuscript_anchor"] not in manuscript_labels:
            issues.append("Missing claim manuscript anchor: " + row["id"])
        for s in row["sources"]:
            if s["id"] not in keyed or not s["inspected"]:
                issues.append("Claim source incomplete: "+row["id"])
        for a in row["artifacts"]:
            check_file(a["path"],a["sha256"])
    for row in read("docs/literature/omissions.json"):
        if row.get("path"):
            # Noncited local exclusions retain extracted evidence so the archive
            # remains auditable without access to the original sibling library.
            if Path(row["path"]).is_absolute():
                check_file(row["evidence_path"],row["evidence_sha256"])
            else:
                check_file(row["path"],row["sha256"])
            if row["sha256"] in {s["sha256"] for s in sources}:
                issues.append("Excluded source entered bibliography: "+row["id"])
    cited = set()
    for row in read("docs/literature/citation-occurrences.json"):
        if row["id"] not in keyed:
            issues.append("Unknown citation "+row["id"])
        path = ROOT/row["path"]
        line = path.read_text().splitlines()[row["line"]-1]
        if row["id"] not in line:
            issues.append("Stale citation occurrence: "+row["id"])
        cited.add(row["id"])

    documents = []
    for stem in ("causal_banking_product","sponsor_proposal"):
        base = ROOT/"docs/build"/stem
        aux = base.with_suffix(".aux").read_text()
        keys = set(k.strip() for block in re.findall(r"\\citation\{([^}]+)\}",aux) for k in block.split(","))
        bbl = base.with_suffix(".bbl").read_text()
        bibliography = set(re.findall(r"\\bibitem(?:\[[^]]*\])?\{([^}]+)\}", bbl))
        if keys != bibliography:
            issues.append("Compiled bibliography closure mismatch: "+stem+" "+str(keys ^ bibliography))
        if keys-set(keyed):
            issues.append("Compiled unregistered citation: "+stem)
        log = base.with_suffix(".log").read_text()
        findings = re.findall(r"(?m)^.*(?:Overfull|LaTeX Warning|Package natbib Warning|undefined).*$",log)
        if findings:
            issues += [stem+": "+x for x in findings]
        blg = base.with_suffix(".blg").read_text()
        if "Warning--" in blg or "error message" in blg:
            issues.append("BibTeX warning/error: "+stem)
        pdf = ROOT/"docs"/(stem+".pdf")
        info = subprocess.run(["pdfinfo",str(pdf)],capture_output=True,text=True,check=True).stdout
        pages = int(re.search(r"(?m)^Pages:\s+(\d+)",info).group(1))
        documents.append({"path":str(pdf.relative_to(ROOT)),"pages":pages,"cited_works":len(keys),"sha256":hashlib.sha256(pdf.read_bytes()).hexdigest(),"layout_log_findings":findings})
    actual_papers = {str(p.relative_to(ROOT)) for p in (ROOT/"docs/papers").glob("*.pdf")}
    registered_pdfs = {s["local_path"] for s in sources if s["local_path"].endswith(".pdf")}
    if actual_papers != registered_pdfs:
        issues.append("Unregistered or missing archive PDFs: "+str(actual_papers ^ registered_pdfs))

    class LinkParser(HTMLParser):
        def handle_starttag(self,tag,attrs):
            for name,link in attrs:
                if name != "href" or urlsplit(link).scheme or link.startswith("#"):
                    continue
                p = (ROOT/"docs/papers"/unquote(link.split("#")[0])).resolve()
                if not p.is_file():
                    issues.append("Broken index link: "+link)
    LinkParser().feed((ROOT/"docs/papers/index.html").read_text())
    checks = read("docs/examples/contract-checks.json")
    if checks["status"] != "pass":
        issues.append("Contract checks failed")
    revision = read("docs/reviews/revision-verification.json")
    if revision["status"] != "pass":
        issues.append("Revision numerical verification failed")
    for path, expected in revision["input_sha256"].items():
        check_file(path, expected)
    environment = read("docs/derivations/environment.json")
    check_file("tools/revision_studies.py", environment["script_sha256"])
    scale = read("docs/derivations/data-scale.json")
    check_file("tools/run_data_scale.py", scale["script_sha256"])
    for path, expected in scale["component_sha256"].items():
        check_file(path, expected)
    receipt = read("security/installation-receipt.json")
    check_file("tools/public_sources.py", receipt["collector_sha256"])
    check_file("security/causal-research.rules", receipt["sha256"])
    for rule in read("security/rule-check.json"):
        if rule["expected"] != rule["actual"]:
            issues.append("Approval-rule check mismatch")
    result = {"status":"pass" if not issues else "fail","cutoff":"2026-10-07",
              "registered_works":len(sources),"source_kinds":dict(Counter(s["kind"] for s in sources)),
              "scholarly_pdfs":len(paper_paths),"all_preserved_pdfs":len(actual_papers),
              "cited_works":len(cited),"hashed_files_checked":len(checked),
              "pdf_pages":pdf_pages,"documents":documents,"issues":issues,
              "scope":"Byte/citation/metadata/selected-contract closure, not independent scholarly review or production validation."}
    (ROOT/"docs/reviews/archive-audit.json").write_text(json.dumps(result,indent=2)+"\n")
    (ROOT/"docs/reviews/checked-files.json").write_text(json.dumps(checked,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="pdf_pages"},indent=2))
    raise SystemExit(bool(issues))


if __name__ == "__main__":
    main()
