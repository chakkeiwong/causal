#!/usr/bin/env python3
"""Build/check the unified working book without rewriting accepted deliveries.

This successor has its own source namespace and audit. The historical V12
controller retains its frozen bibliography checks; this checker covers the
entire working manuscript and its added sources. No acceptance receipt is issued.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

from enrich_sw01_v12 import verify_local

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE = DOCS / "program/repair-v12"
WORK = BASE / "work"
OUT = BASE / "integrated-reader"
NAME = "causal_integrated_working_2026-10-12"
DRIVER = DOCS / (NAME + ".tex")
PDF = DOCS / (NAME + ".pdf")
CITE = r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}"
LABEL = r"\\label\{([^}]+)\}"
LLM = [WORK / "LA07/frontier-chapter.tex", WORK / "LA07/translation-chapter.tex",
       WORK / "LA07/diagram-chapter.tex", WORK / "LA03/chapter-draft.tex",
       WORK / "LA04/chapter-draft.tex", WORK / "LA05/chapter-draft.tex",
       WORK / "LA07/evaluation-chapter.tex", WORK / "LA07/economics-chapter.tex"]
SUPPLEMENTS = [
    ("weak_audit_projection", "Weak-audit projection for funding value"),
    ("weak_audit_sharpening", "Joint candidate information and calibration limits"),
    ("linked_funding", "Linked outcome audits for a dependent funding decision"),
    ("master_execution", "Information, uncertainty and executable limits")]


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path, anchor):
    return {"path": str(path.relative_to(ROOT)), "sha256": sha(path), "anchor": anchor}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def escape(s):
    return "".join({"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
                    "_": r"\_"}.get(c, c) for c in str(s))


def verify_refs(value):
    """Verify explicit file/hash records, including absolute local originals."""
    if isinstance(value, dict):
        name = value.get("local_path", value.get("path"))
        if not name and isinstance(value.get("local_copy"), str):
            name = value["local_copy"]
        if name and value.get("sha256"):
            path = ROOT / name
            if not path.is_file() or sha(path) != value["sha256"]:
                raise ValueError("Source bytes changed or unavailable: " + str(path))
        if value.get("kind") == "paper" and value.get("local_path"):
            p = ROOT / value["local_path"]
            assert p.parent == DOCS / "papers" and p.read_bytes().startswith(b"%PDF-"), p
            expected = f"{value['filename_title']} {value['first_author']}({value['year']}).pdf"
            assert p.name == expected, p
        for v in value.values():
            verify_refs(v)
    elif isinstance(value, list):
        for v in value:
            verify_refs(v)


def scan(path, stack=()):
    if path in stack:
        raise ValueError("Cyclic input " + str(path))
    assert path.resolve().is_relative_to(ROOT)
    raw = re.sub(r"(?m)(?<!\\)%.*$", "", path.read_text())
    found = [(path, raw)]
    for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", raw):
        child = DOCS / name
        if not child.suffix:
            child = child.with_suffix(".tex")
        found.extend(scan(child, (*stack, path)))
    return found


def prepare():
    (OUT / "chapters").mkdir(parents=True, exist_ok=True)
    original = DOCS / "causal_foundations.tex"
    raw = original.read_text()
    prefix, body = raw.split(r"\mainmatter", 1)
    body = body.split(r"\backmatter", 1)[0]
    prefix = prefix.replace(r"\date{10 October 2026}",
        r"\date{12 October 2026\\Integrated working edition\\Literature cutoff: 7 October 2026}")
    prefix = prefix.replace(r"\input{preamble}", r"\input{preamble}" + "\n" +
        r"\usepackage{placeins}\providecommand{\R}{\mathbb R}" + "\n" +
        r"\setlength{\emergencystretch}{3em}")
    marker = r"\addcontentsline{toc}{chapter}{Reader's contract}"
    note = r"""
This integrated working edition contains the developed software comparisons,
eight draft chapters on language models and agents, and four draft chapters on
library, command-line, MCP and workspace integration. They form part of this
book's continuous argument, contents and references. The source-audited earlier
foundations and four scientific extensions are retained, including negative
calibration and qualification findings. The original delivered PDFs remain
separately preserved.

The systematic software survey, full depth of the language-model treatment,
commercial comparison, cross-language adapters and consumer qualification are
unfinished. Local interface demonstrations and exact project examples are not
live model evaluations or accepted bank integrations. This working edition has
compilation, source-identity and extracted-text checks; final rendered visual
review remains pending. It is not the final repaired release or an accepted
bank product.

"""
    prefix = prefix.replace(marker, marker + "\n" + note)
    prefix = prefix.replace("The 44-project source/document survey is supplemented",
        "The inherited 44-project source/document survey, retained as a bounded\n"
        "baseline alongside the new pinned comparisons, is supplemented")
    records = [ref(original, "Original main driver; body reused and front matter extended")]
    sw = WORK / "SW01/software-chapters.tex"
    sw_raw = re.sub(CITE, lambda m: m.group(0).replace(m.group(1),
        ",".join("v12_sw_" + k.strip() for k in m.group(1).split(","))), sw.read_text())
    sw_generated = OUT / "chapters/software.tex"
    sw_generated.write_text(sw_raw)
    records.append({"original": ref(sw, "Five software chapters"),
                    "generated": ref(sw_generated, "Citation-key prefix only"),
                    "transform": "Prefix every software citation with v12_sw_; preserve prose/equations/labels"})
    body = body.replace(r"\input{reconstruction/17_software}",
        r"\input{reconstruction/17_software}" + "\n" +
        "\\input{" + str(sw_generated.relative_to(DOCS)) + "}\n" +
        "\\label{integrated:software-end}\n" +
        "\n".join("\\input{" + str(p.relative_to(DOCS)) + "}" for p in LLM) +
        "\n\\label{integrated:llm-end}\n")
    integration = WORK / "IN06/integration-chapters.tex"
    body = body.replace(r"\input{reconstruction/18_product}",
        r"\input{reconstruction/18_product}" + "\n\\input{" +
        str(integration.relative_to(DOCS)) + "}\n\\label{integrated:integration-end}\n")
    generated_supplements = []
    for slug, title in SUPPLEMENTS:
        source = DOCS / "supplements" / (slug + "_2026-10-11.tex")
        content = source.read_text().split(r"\end{center}", 1)[1]
        content = content.split(r"\begin{thebibliography}", 1)[0]
        # Some article drivers insert a references-page break. Preserve body,
        # discard that terminal break only; all scientific tables remain.
        content = content.rstrip().removesuffix(r"\clearpage").rstrip()
        dependencies = []
        def table(m):
            p = DOCS / "supplements" / (m.group(1) + ".tex")
            dependencies.append(ref(p, "Preserved scientific table"))
            return p.read_text()
        content = re.sub(r"\\input\{([^}]+)\}", table, content)
        labels = set(re.findall(LABEL, content))
        for label in sorted(labels, key=len, reverse=True):
            content = content.replace("{" + label + "}", "{integrated:" + slug + ":" + label + "}")
        content = content.replace(r"\begin{abstract}", r"\begin{quote}\small")
        content = content.replace(r"\end{abstract}", r"\end{quote}")
        if slug == "master_execution":
            before = "V=\\tfrac12(\\theta_0+\\theta_1)-C,\\quad \\theta_s=w'\\beta_s,\\quad\n w_h=48"
            after = "\\begin{aligned}\n V&=\\tfrac12(\\theta_0+\\theta_1)-C,\\qquad \\theta_s=w'\\beta_s,\\\\\n w_h&=48"
            assert before in content
            content = content.replace(before, after, 1).replace(
                "C=400{,}000.\n\\]", "C=400{,}000.\n\\end{aligned}\n\\]", 1)
        generated = OUT / "chapters" / (slug + ".tex")
        generated.write_text("\\chapter{" + title + "}\n\\label{integrated:" + slug + "}\n" + content + "\n")
        records.append({"original": ref(source, "Scientific supplement including original article wrapper"),
            "tables": dependencies, "generated": ref(generated, "Integrated chapter body"),
            "transform": "Remove article title/preamble/bibliography; abstract to quote; add chapter; inline tables; namespace labels; split master funding display into two aligned lines"})
        generated_supplements.append("\\input{" + str(generated.relative_to(DOCS)) + "}")
    body = body.replace(r"\input{reconstruction/21_investment}",
        "\n".join(generated_supplements) + "\n" + r"\input{reconstruction/21_investment}")
    end = r"""
\backmatter
\clearpage\phantomsection
\addcontentsline{toc}{chapter}{Bibliography}
\bibliographystyle{plainnat}
\bibliography{causal_banking_refs,program/repair-v12/integrated-reader/repair-refs}
\end{document}
"""
    DRIVER.write_text(prefix + "\\mainmatter\n" + body + end)
    write_json(OUT / "transformations.json", {"status": "explicit_source_integration", "records": records})


def project_source(key, title, files, claims):
    return {"id": key, "kind": "project_evidence", "title": title,
            "authors": ["Causal banking research project"], "year": 2026,
            "version_date": "Recorded local work, 12 October 2026; not backdated literature",
            "local_records": [ref(ROOT / p, a) for p, a in files],
            "inspected_anchors": [a for p, a in files], "supported_claims": claims,
            "limits": "Author project evidence; no independent or bank acceptance"}


def sources():
    original = {s["id"]: s for s in load(DOCS / "literature/sources.json")}
    all_sources = dict(original)
    for name in ("LA01", "LA04"):
        for entry in load(WORK / name / "source-audit.json")["sources"]:
            if entry["id"] in original:
                assert entry.get("sha256") == original[entry["id"]]["sha256"], entry["id"]
            else:
                all_sources[entry["id"]] = entry
    catalog = {x["id"]: x for x in load(WORK / "SW01/catalog.json")["candidates"]}
    for row in load(WORK / "SW01/pinned-package-review.json")["records"]:
        key = "v12_sw_" + row["id"].split(":")[-1]
        entry = dict(row)
        entry["bibliographic_id"] = key
        c = catalog[row["candidate_id"]]
        entry["title"] = c.get("audited_component", row.get("display", c["name"])) + ": selected official documentation and source"
        all_sources[key] = entry
    for row in load(WORK / "IN02/source-audit.json")["entries"]:
        all_sources[row["id"]] = row
    all_sources["v12_in_contract"] = project_source("v12_in_contract", "Common causal operation contract and semantic checks", [
        ("docs/program/repair-v12/work/IN02/receipt.json", "Reviewed design criteria and frozen evidence"),
        ("docs/program/repair-v12/work/IN02/review.md", "Scientific states, target digest, set topology and limits"),
        ("docs/program/repair-v12/work/IN02/request-schema.json", "Canonical request fields"),
        ("docs/program/repair-v12/work/IN02/response-schema.json", "Canonical response and set fields")],
        ["Specified target and set semantics; reference checks, not scientific truth."])
    all_sources["v12_in_runtime"] = project_source("v12_in_runtime", "Local library, CLI and MCP runtime qualification", [
        ("docs/program/repair-v12/work/IN04/receipt.json", "Frozen scoped acceptance and evidence"),
        ("docs/program/repair-v12/work/IN04/review.md", "Implemented scope, eleven transport cases, nine faults and environment limitation"),
        ("docs/program/repair-v12/work/IN04/transport-checks.json", "Actual matched transport outcomes"),
        ("docs/program/repair-v12/work/IN04/fault-trials.json", "Local fault/restart outcomes"),
        ("docs/program/repair-v12/work/IN04/runtime-source-audit.json", "Observed installed SDK source identities and anchors"),
        ("src/causalbank/cli_v12.py", "main and read_request: input, output, exit codes"),
        ("src/causalbank/runtime_v12.py", "Runtime, IMPLEMENTED, job/replay/budget boundaries"),
        ("src/causalbank/mcp_server_v12.py", "build_server: version, tools, result parity, resources")],
        ["Selected real local execution and faults; no arbitrary discovery, modern MCP, bank service or distributed acceptance."])
    all_sources["v12_in_inventory"] = project_source("v12_in_inventory", "Dated read-only workspace consumer inspection", [
        ("docs/program/repair-v12/work/IN01/workspace-inventory.json", "Eighteen directories and 53 original source identities, anchors and claims"),
        ("docs/program/repair-v12/work/IN01/consumer-map.json", "Four proposed workflows and consumer alternatives"),
        ("docs/program/repair-v12/work/IN01/read-only-audit.json", "Recorded zero sibling writes, executions and source copies"),
        ("docs/program/repair-v12/work/IN01/review.md", "Dated inspected declarations, licensing boundaries and deferred acceptance")],
        ["Source-inspected interfaces and proposed connections; not executed sibling integrations."])
    return original, all_sources


def audit_and_bibliography():
    original, entries = sources()
    files = scan(DRIVER)
    combined = "\n".join(t for _, t in files)
    cited = {k.strip() for g in re.findall(CITE, combined) for k in g.split(",")}
    labels = re.findall(LABEL, combined)
    references = set(re.findall(r"\\(?:ref|eqref|cref|Cref)\{([^}]+)\}", combined))
    duplicates = [k for k, n in collections.Counter(labels).items() if n > 1]
    assert not duplicates, duplicates
    assert not references - set(labels), references - set(labels)
    assert cited <= entries.keys(), cited - entries.keys()
    original_keys = set(re.findall(r"@\w+\{([^,]+),", (DOCS / "causal_banking_refs.bib").read_text()))
    assert cited & original.keys() <= original_keys
    graphics = []
    for name in sorted(set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", combined))):
        candidates = [DOCS / name] if Path(name).suffix else [DOCS / (name + x) for x in (".pdf", ".png", ".jpg", ".jpeg")]
        available = [p for p in candidates if p.is_file()]
        assert len(available) == 1, (name, available)
        graphics.append(ref(available[0], "Inherited figure included in the unified book"))
    bib = []
    for key in sorted(cited):
        e = entries[key]
        verify_refs(e)
        if key.startswith("v12_sw_"):
            verify_local(e)
        if key in original:
            continue
        if e.get("kind") == "paper":
            authors = e.get("authors") or [e["first_author"]]
            author = " and ".join(escape(x) for x in authors)
            title = escape(e["title"])
            year = str(e["year"])
            note = escape(e.get("arxiv_version", ""))
            url = e["url"]
        elif e.get("kind") == "project_evidence":
            author = "{Causal banking research project}"
            title = escape(e["title"])
            year = "2026"
            note = "Author project evidence, 12 October 2026. Source and claim bindings in the integrated manuscript audit."
            url = None
        elif key.startswith("v12_mcp_"):
            author = "{Model Context Protocol contributors}"
            title = escape(e["id"].replace("v12_mcp_", "MCP ").replace("_", " "))
            year = "2026"
            note = escape(e["version_date"])
            url = e["source_identity"]
        else:
            identity = e.get("repository", e.get("source_identity"))
            author = "{" + escape(identity.split("/")[-1] + " contributors") + "}"
            title = escape(e.get("title", identity + ": inspected software source"))
            year = e["commit_date"][:4]
            note = "Revision " + r"\nolinkurl{" + e["commit"] + "}; " + escape(e["commit_date"])
            if e.get("observed_version"):
                note += "; version " + escape(e["observed_version"])
            url = e.get("url", e.get("source_identity", "https://github.com/" + identity))
        fields = [f"author = {{{author}}}", f"title = {{{{{title}}}}}", f"year = {{{year}}}", f"note = {{{note}}}"]
        if url:
            fields.append("url = {" + url + "}")
        bib.append("@misc{" + key + ",\n  " + ",\n  ".join(fields) + "\n}")
    (OUT / "repair-refs.bib").write_text("\n\n".join(bib) + "\n")
    # Assert the inspected sibling originals still exist with their recorded
    # identities. Read only; no source is copied or executed here.
    inventory = load(WORK / "IN01/workspace-inventory.json")
    excluded = {"/home/ubuntu/workspace/FinMarketing/AGENTS.md",
                "/home/ubuntu/workspace/MOONeural/README.md",
                "/home/ubuntu/workspace/MOONeural/pyproject.toml",
                "/home/ubuntu/workspace/MacroFinance-dz5-neutra/AGENTS.md"}
    verified, drift = [], []
    for entry in inventory["sources"]:
        p = Path(entry["local_copy"])
        current = sha(p) if p.is_file() else None
        if current == entry["sha256"]:
            verify_refs(entry)
            verified.append(entry)
        else:
            assert str(p) in excluded, "New source drift requires claim review: " + str(p)
            drift.append({"source_identity": str(p), "historical_sha256": entry["sha256"],
                          "sha256_observed_now": current,
                          "disposition": "Changed after inventory; not used for technical claims in new integration chapters"})
    write_json(OUT / "workspace-source-drift.json", {
        "date": "2026-10-12", "preserved_inventory": ref(WORK / "IN01/workspace-inventory.json", "Historical inspection retained unchanged"),
        "verified_count": len(verified), "verified_sources": verified, "changed_count": len(drift), "changed_sources": drift,
        "claim_review": "New chapter claims about FinMarketing's toolkit, MacroFinance's numerical authority, BayesFilter, CardNPV, DynareMCP and MathDevMCP use unchanged technical originals. No current MOONeural interface or changed agent-instruction claim is made.",
        "sibling_writes": 0, "sibling_code_executions": 0})
    examples = load(WORK / "LA07/decision-examples.json")
    assert examples["script_sha256"] == sha(ROOT / "tools/integrated_decision_examples_v12.py")
    assert examples["status"] == "exact_checks_pass"
    project_files = [WORK / "LA02/receipt.json", WORK / "LA02/oracles.json",
                     WORK / "LA06/receipt.json", WORK / "LA06/protocol.json",
                     WORK / "LA05/receipt.json", WORK / "SW01/software-contract-examples.json",
                     WORK / "LA07/decision-examples.json", ROOT / "tools/integrated_decision_examples_v12.py",
                     DOCS / "program/master/work/I01/delivery-manifest.json",
                     DOCS / "program/master/work/I01/source-audit.json"]
    audit = {"status": "all_cited_source_bytes_verified", "scope": "Entire integrated working manuscript; source identity is not scientific or external acceptance",
        "cited_records": len(cited), "sources": [dict(entries[k], integrated_citation_key=k) for k in sorted(cited)],
        "manuscript_inputs": [ref(p, "Included TeX source") for p in dict.fromkeys(p for p, _ in files)],
        "figure_inputs": graphics,
        "bibliographies": [ref(DOCS / "causal_banking_refs.bib", "Frozen baseline bibliography"),
                           ref(OUT / "repair-refs.bib", "Added references in one bibliography")],
        "project_records": [ref(p, "Preserved or reproduced project evidence") for p in project_files],
        "transformations": ref(OUT / "transformations.json", "Original-to-chapter source transformations"),
        "sibling_original_hashes_verified": len(verified),
        "workspace_drift": ref(OUT / "workspace-source-drift.json", "49 unchanged originals; four changed records excluded from new technical claims"),
        "source_scope_limits": "Only previously inspected anchors support inherited technical claims. Current workspace/runtime observations are dated separately from the literature cutoff."}
    write_json(OUT / "source-audit.json", audit)
    return len(cited), files


def run(command, log_name, env=None):
    with (OUT / log_name).open("w") as log:
        p = subprocess.run(command, cwd=DOCS, stdout=log, stderr=subprocess.STDOUT,
                           env=env, timeout=60)
    if p.returncode:
        raise RuntimeError(f"Build failed: {log_name}; inspect the bounded log tail")


def build():
    if PDF.exists():
        state = load(DOCS / "program/state.json")
        if any(d["path"] == str(PDF.relative_to(ROOT)) for d in state["deliveries"]):
            raise ValueError("Published working PDF is frozen; create a versioned successor before rebuilding")
    prepare()
    cited, files = audit_and_bibliography()
    latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-recorder",
             "-output-directory=" + str(OUT), str(DRIVER)]
    env = os.environ.copy()
    env["BIBINPUTS"] = str(DOCS) + ":"
    if (OUT / (NAME + ".aux")).exists():
        run(["bibtex", str((OUT / NAME).relative_to(DOCS))], "bibtex-recovery.log", env)
    run(latex, "pass-1.log")
    run(["bibtex", str((OUT / NAME).relative_to(DOCS))], "bibtex-build.log", env)
    for i in range(2, 6):
        run(latex, f"pass-{i}.log")
        log = (OUT / (NAME + ".log")).read_text(errors="replace")
        if i >= 3 and not any(x in log for x in ("Label(s) may have changed", "Rerun to get", "Rerun to get citations")):
            break
    built = OUT / (NAME + ".pdf")
    PDF.write_bytes(built.read_bytes())
    subprocess.run(["pdftotext", "-layout", str(PDF), str(OUT / "reader.txt")], check=True, timeout=30)
    info = subprocess.check_output(["pdfinfo", str(PDF)], text=True, timeout=15)
    pages = int(re.search(r"(?m)^Pages:\s+(\d+)", info).group(1))
    aux = (OUT / (NAME + ".aux")).read_text()
    page_labels = {m.group(1): int(m.group(2)) for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}", aux)}
    warnings = [l for l in log.splitlines() if any(s in l for s in ("Warning", "Overfull", "Underfull", "Missing character"))]
    assert not any("undefined" in w.lower() or "multiply defined" in w.lower() for w in warnings), warnings
    body_pages = {"software": page_labels["integrated:software-end"] - page_labels["sw:interfaces"] + 1,
                  "llm": page_labels["integrated:llm-end"] - page_labels["la:frontier"] + 1,
                  "integration": page_labels["integrated:integration-end"] - page_labels["in:semantics"] + 1}
    toc = (OUT / (NAME + ".toc")).read_text()
    chapters = len(re.findall(r"\\contentsline \{chapter\}\{\\numberline", toc))
    text = (OUT / "reader.txt").read_text()
    assert "???" not in text
    report = {"status": "compiled_source_and_text_checks_only", "pdf": ref(PDF, "Unified working book"),
              "pages": pages, "numbered_chapters": chapters, "new_draft_chapters": {"software": 5, "llm": 8, "integration": 4},
              "physical_body_pages": body_pages, "body_count_scope": "Physical spans at inherited monograph typography; not accepted substantive/duplication counts",
              "cited_records": cited, "source_files": len(set(p for p, _ in files)), "warnings": warnings,
              "chapter_pages": {k: v for k, v in page_labels.items() if k.startswith(("la:", "sw:", "in:", "integrated:"))},
              "source_audit": ref(OUT / "source-audit.json", "Whole-book citations, input bytes and project evidence"),
              "driver": ref(DRIVER, "Main manuscript source"), "builder": ref(Path(__file__), "Deterministic source assembly and bounded LaTeX passes"),
              "rendered_visual_review": "pending fresh session under exhausted parent AGENTS.md image budget",
              "mandatory_repairs_closed": [], "final_release": False}
    write_json(OUT / "build-report.json", report)
    print(json.dumps({k: report[k] for k in ("status", "pages", "numbered_chapters", "physical_body_pages", "cited_records", "warnings")}))


def check():
    report = load(OUT / "build-report.json")
    verify_refs(report)
    audit = load(OUT / "source-audit.json")
    verify_refs(audit)
    verify_refs(load(OUT / "transformations.json"))
    # Inspection records may include several nested byte identities.
    for entry in audit["sources"]:
        if entry["integrated_citation_key"].startswith("v12_sw_"):
            verify_local(entry)
    old = load(DOCS / "program/master/work/I01/delivery-manifest.json")
    verify_refs(old)
    _, entries = sources()
    combined = "\n".join(t for _, t in scan(DRIVER))
    citations = {k.strip() for g in re.findall(CITE, combined) for k in g.split(",")}
    assert citations == {x["integrated_citation_key"] for x in audit["sources"]}
    labels = re.findall(LABEL, combined)
    assert len(labels) == len(set(labels))
    assert set(re.findall(r"\\(?:ref|eqref|cref|Cref)\{([^}]+)\}", combined)) <= set(labels)
    assert citations <= entries.keys()
    print(json.dumps({"status": "pass", "pages": report["pages"], "cited_records": len(citations),
                      "numbered_chapters": report["numbered_chapters"], "predecessor_preserved": True,
                      "scope": "Whole-book source, reference and output identity; visual and final repair acceptance remain open"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check"))
    args = parser.parse_args()
    build() if args.command == "build" else check()
