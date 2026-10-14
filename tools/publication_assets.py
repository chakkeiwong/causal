#!/usr/bin/env python3
"""Generate publication tables and a fully offline searchable source index."""
from pathlib import Path
import csv
import html
import json
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LIT = DOCS / "literature"


def tex(value):
    substitutions = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
                     "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
                     "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(substitutions.get(c, c) for c in str(value))


def main():
    sources = json.loads((LIT / "sources.json").read_text())
    software = json.loads((LIT / "software-assessment.json").read_text())
    counts = json.loads((LIT / "discovery-counts.json").read_text())
    generated = DOCS / "generated"
    generated.mkdir(exist_ok=True)
    (generated / "counts.tex").write_text(
        "\\newcommand{\\SoftwareCount}{" + str(len(software)) + "}\n"
        "\\newcommand{\\PublicRequestCount}{" + str(counts["requests"]) + "}\n"
        "\\newcommand{\\CandidateCount}{" + str(counts["unique_title_candidates"]) + "}\n"
        "\\newcommand{\\SourceCount}{" + str(len(sources)) + "}\n")
    rows = [r"\begin{longtable}{P{29mm}P{55mm}P{60mm}}",
            r"\toprule Project; license & Documented role and observation & Recommendation and boundary\\\midrule\endhead"]
    for s in software:
        name = s["repository"].split("/")[-1]
        observed = "Last push: " + (s["last_push"] or "unavailable")[:10] + "."
        if s["package_version"]:
            observed += " Observed package declaration: " + s["package_version"] + "."
        rows.append(tex(name) + r" \citep{sw_" + s["id"] + r"}\par " + tex(s["license"])
                    + " & " + tex(s["capabilities"] + ". " + observed)
                    + " & " + tex(s["decision"] + ". " + s["limitation"]) + r"\\")
    rows += [r"\bottomrule", r"\end{longtable}"]
    (generated / "software-table.tex").write_text("\n".join(rows) + "\n")
    rows = [r"\begin{longtable}{P{32mm}P{112mm}}",
            r"\toprule Audit key & Source identity and archived version\\\midrule\endhead"]
    for s in sources:
        rows.append(r"{\scriptsize\texttt{" + tex(s["id"]) + "}} & "
                    + tex(s["title"]) + r" \citep{" + s["id"] + r"}.\par "
                    + tex(s["version_status"]) + r"\\")
    rows += [r"\bottomrule", r"\end{longtable}"]
    (generated / "source-concordance.tex").write_text("\n".join(rows) + "\n")

    index = DOCS / "papers/index.html"
    rows, markdown = [], ["# Saved paper index", "",
        f"{sum(s['kind']=='paper' for s in sources)} scholarly PDFs and three official guidance PDFs. The HTML index also covers software and local documentation.",
        "", "[Search all sources offline](index.html) · [Full audit register](../literature/sources.json)", ""]
    for s in sources:
        local = "../" + s["local_path"].removeprefix("docs/")
        author = s["authors"].replace("{", "").replace("}", "")
        details = "<details><summary>Version, inspected anchors, claims and hash</summary>"
        details += "<p>" + html.escape(s["version_status"]) + "</p><ul>"
        details += "".join("<li>" + html.escape(x) + "</li>" for x in s["inspected"])
        details += "</ul><p>" + html.escape(" ".join(s["claims"])) + "</p>"
        details += "<p><b>Limits:</b> " + html.escape(s["limits"]) + "</p><code>" + s["sha256"] + "</code></details>"
        rows.append("<tr><td>" + html.escape(s["id"]) + "<br>" + str(s["year"])
                    + "<br>" + html.escape(s["kind"]) + "</td><td><a href='" + quote(local, safe="/.")
                    + "'>" + html.escape(s["title"]) + "</a><p>" + html.escape(author)
                    + "</p>" + details + "</td><td><a href='" + html.escape(s["url"], quote=True)
                    + "'>Original source</a></td></tr>")
        if s["kind"] == "paper" or s["local_path"].startswith("docs/papers/"):
            markdown.append("- [" + s["title"] + " (" + str(s["year"]) + ")]("
                            + quote(local, safe="/.") + ") — " + s["id"])
    page = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width"><title>Causal banking source archive</title>
<style>body{font:16px system-ui;max-width:1200px;margin:36px auto;padding:0 22px;color:#17324d;background:#f7f9fc}
h1{font-size:32px}input{font:inherit;padding:12px;width:min(700px,90%);border:1px solid #8298a8;border-radius:6px}
table{border-collapse:collapse;width:100%;background:white;margin-top:24px}td,th{padding:14px;text-align:left;vertical-align:top;border-bottom:1px solid #d4dde4}
td:first-child{width:165px;overflow-wrap:anywhere}a{color:#005f85}details{font-size:14px;line-height:1.5}summary{cursor:pointer}code{overflow-wrap:anywhere;font-size:12px}p{line-height:1.55}tr[hidden]{display:none}
</style><h1>Causal banking source archive</h1>
<p>Publication cutoff: 7 October 2026; source access and inspection continued through 9 October 2026. Every scholarly citation has a saved PDF named by title, first author and year.
Software entries open manifests containing the hashes of their primary documents.
Inspection and limitations are visible in each record. This index works offline.</p>
<p><a href="../mission-control.html">Mission control</a> · <a href="../causal_foundations.pdf">Working foundations draft</a> · <a href="../causal_banking_product.pdf">Withdrawn version 2</a> ·
<a href="../literature/sources.json">Audit register</a> · <a href="../literature/reconstruction-claims.json">Material claims</a> ·
<a href="../literature/coverage-and-omissions.md">Coverage and omissions</a></p>
<label for="search">Search title, author, key, method or claim</label><p><input id="search" type="search" placeholder="For example: POMDP, longitudinal, Mian"></p>
<p id="count" aria-live="polite"></p><table><thead><tr><th>Audit key</th><th>Saved source and inspection</th><th>Provenance</th></tr></thead><tbody>"""
    page += "".join(rows) + """</tbody></table><script>
const search=document.querySelector('#search'),rows=Array.from(document.querySelectorAll('tbody tr'));
function filter(){const q=search.value.toLocaleLowerCase().trim();let n=0;for(const r of rows){r.hidden=!r.textContent.toLocaleLowerCase().includes(q);if(!r.hidden)n++;}document.querySelector('#count').textContent=n+' of '+rows.length+' sources shown';}
search.addEventListener('input',filter);filter();
</script></html>"""
    index.write_text(page)
    (DOCS / "papers/index.md").write_text("\n".join(markdown) + "\n")
    with (LIT / "source-index.csv").open("w", newline="") as f:
        fields = ["id", "kind", "title", "authors", "year", "version_status", "url", "local_path", "sha256"]
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sources)

    # Exact citation occurrences, including generated tables, preserve reconstruction.
    occurrences = []
    for path in DOCS.rglob("*.tex"):
        if "build" in path.parts:
            continue
        for line_no, line in enumerate(path.read_text().splitlines(), 1):
            raw = re.sub(r"(?<!\\)%.*$", "", line)
            for match in re.finditer(r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}", raw):
                for key in match.group(1).split(","):
                    occurrences.append({"id": key.strip(), "path": str(path.relative_to(ROOT)), "line": line_no, "context": raw.strip()})
    (LIT / "citation-occurrences.json").write_text(json.dumps(occurrences, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"sources": len(sources), "software": len(software), "citation_occurrences": len(occurrences), "index": str(index)}))


if __name__ == "__main__":
    main()
