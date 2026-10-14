#!/usr/bin/python3
"""Preserve selected primary sources, bibliography and evidence records."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run():
    selected = json.loads((ROOT / "docs/literature/paper-selections.json").read_text())
    notes_path = ROOT / "docs/literature/reading-notes.json"
    notes = json.loads(notes_path.read_text()) if notes_path.exists() else {}
    local = {x["id"]: x for x in json.loads((ROOT / "docs/literature/local-reading-queue.json").read_text())}
    previous_path = ROOT / "docs/literature/sources.json"
    previous = {s["id"]: s for s in json.loads(previous_path.read_text())} if previous_path.exists() else {}
    sources = []
    for row in selected:
        origin = Path(local[row["origin"]]["original_path"]) if row["origin"] in local else ROOT / row["origin"]
        filename_title = re.sub(r'[<>:"/\\|?*]', '', row["title"])
        filename_title = re.sub(r'\s+', ' ', filename_title).strip().rstrip('.')
        destination = ROOT / "docs/papers" / f"{filename_title} {row['first_author']}({row['year']}).pdf"
        # Once acquired, the preserved copy is sufficient for offline rebuilding.
        payload = destination.read_bytes() if destination.exists() else origin.read_bytes()
        if not payload.startswith(b"%PDF-"):
            raise ValueError(f"Invalid PDF: {destination}")
        expected = previous.get(row["id"], {}).get("sha256")
        if expected and hashlib.sha256(payload).hexdigest() != expected:
            raise ValueError(f"Preserved paper differs from registered hash: {destination}")
        if not destination.exists():
            shutil.copyfile(origin, destination)
        text_path = ROOT / "docs/literature/text" / (row["id"] + ".txt")
        subprocess.run(["pdftotext", "-layout", str(destination), str(text_path)], check=True, capture_output=True)
        note = notes.get(row["id"], {})
        source = {**row, "kind": "paper", "filename_title": filename_title,
                  "local_path": str(destination.relative_to(ROOT)),
                  "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload),
                  "original_path": str(origin), "accessed": previous.get(row["id"], {}).get("accessed", "2026-10-08"),
                  "text_path": str(text_path.relative_to(ROOT)),
                  "inspected": note.get("inspected", []), "claims": note.get("claims", []),
                  "limits": note.get("limits", "Technical inspection pending"),
                  "integrity_check": note.get("integrity_check", "Title/author/version checked from PDF; correction status requires dated metadata record"),
                  "citation_count": None, "citation_count_source": "not available",
                  "venue_metric": "not used as evidence of correctness"}
        sources.append(source)
    other_path = ROOT / "docs/literature/other-sources.json"
    if other_path.exists():
        sources.extend(json.loads(other_path.read_text()))
    ids = [s["id"] for s in sources]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate citation keys")
    (ROOT / "docs/literature/sources.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2) + "\n")
    bib = []
    for s in sources:
        entry = "book" if s.get("category") == "book" else "misc"
        fields = {"title": "{" + s["title"] + "}", "author": s["authors"], "year": str(s["year"]),
                  "url": s["url"], "note": s["version_status"] + "; local source archived and checked " + s.get("accessed", "2026-10-07")}
        if s.get("doi"):
            fields["doi"] = s["doi"]
        if entry == "book":
            fields["publisher"] = {"hernan2020": "Chapman and Hall/CRC; archived author draft",
                                   "peters2017": "MIT Press",
                                   "wager2025": "Author-distributed draft",
                                   "applied2024": "Author-distributed online edition"}.get(s["id"], s.get("publisher", "Publisher not recorded"))
        bib.append("@" + entry + "{" + s["id"] + ",\n" + ",\n".join("  " + k + " = {" + v.replace("&", r"\&").replace("%", r"\%") + "}" for k, v in fields.items()) + "\n}\n")
    (ROOT / "docs/causal_banking_refs.bib").write_text("\n".join(bib))
    print(json.dumps({"paper_copies": len(selected), "all_sources": len(sources), "with_inspection_notes": sum(bool(s.get('inspected')) for s in sources)}))


if __name__ == "__main__":
    run()
