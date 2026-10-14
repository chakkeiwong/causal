#!/usr/bin/env python3
"""Render the current release links and gap summaries after canonical state changes."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import master_control as mc

state = mc.read(ROOT, mc.STATE)
mc.render(ROOT, state)
md_path = ROOT / "docs/mission-control.md"
md = md_path.read_text()
reader = state["reader"]
brief = "docs/sponsor_execution_2026-10-11.pdf"
if not (ROOT / reader["path"]).is_file() or not (ROOT / brief).is_file():
    raise SystemExit("Current release PDFs are missing")
md = md.replace(
    "[Current research reader — 259 pages](causal_foundations_with_linked_audits_2026-10-11.pdf) · "
    "[Sponsor proposal — V10 baseline](sponsor_reconstruction.pdf)",
    f"[Current research reader — {reader['pages']} pages](../{reader['path'][5:]}) · "
    f"[Current sponsor decision brief — 3 pages]({Path(brief).name})",
)
# The dashboard is under docs/, so release links are relative to that directory.
md = md.replace(
    f"](../{reader['path'][5:]})",
    f"]({reader['path'][5:]})",
)
md = md.replace(
    "Next: **None**.",
    "Next: **blocked pending external inputs or a reviewed scientific successor**.",
)
gap = json.loads((ROOT / "docs/program/master/work/I01/gap-dispositions.json").read_text())
rows = ["## Current gap dispositions", "", "| Gap | Author status | Next evidence |", "|---|---|---|"]
for key, value in gap["dispositions"].items():
    rows.append(f"| {key} | {value['status']} | {value['next']} |")
rows += ["", "[Detailed I01 review](program/master/work/I01/review.md) · "
         "[Hash-bound release manifest](program/master/work/I01/delivery-manifest.json)", ""]
marker = "External input contracts: "
md = md.replace(marker, "\n".join(rows) + "\n" + marker)
md_path.write_text(md)
body = subprocess.run(
    ["pandoc", "--from=gfm", "--to=html"], input=md, text=True,
    capture_output=True, check=True, timeout=20
).stdout
html = (
    "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
    "<meta name='viewport' content='width=device-width'>"
    "<title>Causal banking master</title>"
    "<style>body{font:17px system-ui;max-width:1200px;margin:3rem auto;"
    "padding:0 1.5rem;color:#183047}table{border-collapse:collapse;width:100%}"
    "td,th{padding:.7rem;border-bottom:1px solid #d4dde5;text-align:left}"
    "a{color:#075f87}code{font-size:.85em}</style></head><body>"
    + body + "</body></html>"
)
(ROOT / "docs/mission-control.html").write_text(html)
print("Current integrated dashboard rendered")
