#!/usr/bin/env python3
"""Freeze or verify the local proposal delivery, including audited source bytes."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "docs/program/delivery-manifest.json"
RECONSTRUCTION_TARGET = ROOT / "docs/program/reconstruction-delivery-manifest.json"


def read(path):
    return json.loads((ROOT / path).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(target=None):
    target = target or (RECONSTRUCTION_TARGET if RECONSTRUCTION_TARGET.is_file() else TARGET)
    manifest = json.loads(target.read_text())
    if manifest.get("status") == "withdrawn":
        historical = ROOT / manifest["historical_archive"]["path"]
        intact = historical.is_file() and digest(historical) == manifest["historical_archive"]["sha256"]
        print(json.dumps({
            "status": "withdrawn",
            "version": manifest["version"],
            "historical_archive_intact": intact,
            "current_delivery": False,
            "scope": "The historical archive preserves withdrawn work; this is not a passing current delivery."
        }, indent=2))
        return False
    issues = []
    seen = set()
    for row in manifest["artifacts"]:
        path = ROOT / row["path"]
        if row["path"] in seen:
            issues.append("Duplicate: " + row["path"])
        seen.add(row["path"])
        if not path.is_file():
            issues.append("Missing: " + row["path"])
        elif path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            issues.append("Changed: " + row["path"])
    result = {"status": "pass" if not issues else "fail",
              "version": manifest["version"], "artifacts": len(seen),
              "issues": issues,
              "scope": "Delivered file identity; not scientific or bank validation."}
    print(json.dumps(result, indent=2))
    return not issues


def freeze_reconstruction():
    state = read('docs/program/state.json')
    linkage_phases = [p for p in state['phases'] if p['id'].startswith('W')]
    dynamic_phases = [p for p in state['phases'] if p['id'].startswith('U')]
    scope_phases = [p for p in state['phases'] if p['id'].startswith('T')]
    scientific_phases = [p for p in state['phases'] if p['id'].startswith('S')]
    if linkage_phases:
        if ({p['id'] for p in linkage_phases} != {f'W{i:02d}' for i in range(5)}
                or any(p['status'] != 'complete' for p in linkage_phases)):
            raise SystemExit('Cannot freeze before all linkage-inference exit tests are complete')
        if any(p['status'] != 'historical' for p in state['phases'] if not p['id'].startswith('W')):
            raise SystemExit('Linkage revision requires preserved prior phases to remain historical')
    elif dynamic_phases:
        if ({p['id'] for p in dynamic_phases} != {f'U{i:02d}' for i in range(9)}
                or any(p['status'] != 'complete' for p in dynamic_phases)):
            raise SystemExit('Cannot freeze before all dynamic-construction exit tests are complete')
        if any(p['status'] != 'historical' for p in state['phases'] if not p['id'].startswith('U')):
            raise SystemExit('Dynamic revision requires preserved prior phases to remain historical')
    elif scope_phases:
        if ({p['id'] for p in scope_phases} != {f'T{i:02d}' for i in range(9)}
                or any(p['status'] != 'complete' for p in scope_phases)):
            raise SystemExit('Cannot freeze before all scope-completion exit tests are complete')
        if any(p['status'] != 'historical' for p in state['phases'] if p['id'].startswith(('R', 'S'))):
            raise SystemExit('Scope revision requires preserved R/S phases to remain historical')
    elif scientific_phases:
        expected = {f'S{i:02d}' for i in range(9)}
        if ({p['id'] for p in scientific_phases} != expected
                or any(p['status'] != 'complete' for p in scientific_phases)):
            raise SystemExit('Cannot freeze before all scientific-completion exit tests are complete')
    phases = [p for p in state['phases'] if p['id'].startswith('R')]
    if not scope_phases and (len(phases) != 10 or any(p['status'] != 'complete' for p in phases)):
        raise SystemExit('Cannot freeze before all reconstruction exit tests are complete')
    audit = read('docs/reviews/foundations-audit.json')
    for name in ('docs/reviews/foundations-audit.json', 'docs/reconstruction/checks.json',
                 'docs/reviews/revision-verification.json', 'docs/reviews/scientific-contract-checks.json',
                 'docs/reviews/reconstruction-build.json', 'docs/program/consistency-check.json'):
        result = read(name)
        if result['status'] != 'pass':
            raise SystemExit('Cannot freeze failed check: ' + name)
        for path, expected in result.get('input_sha256', {}).items():
            if digest(ROOT / path) != expected:
                raise SystemExit('Stale check input: ' + path)
    if scientific_phases:
        for name in ('docs/reviews/scientific-completion-verification.json',
                     'docs/reviews/interface-qualification.json',
                     'docs/reviews/standalone-qualification.json'):
            receipt = read(name)
            if receipt['status'] != 'pass':
                raise SystemExit('Scientific completion evidence failed: ' + name)
            for path, expected in receipt['input_sha256'].items():
                if digest(ROOT / path) != expected:
                    raise SystemExit('Stale scientific completion evidence: ' + path)
    if scope_phases:
        receipt = read('docs/reviews/scope-verification.json')
        if receipt['status'] != 'pass':
            raise SystemExit('Scope verification failed')
        for path, expected in receipt['input_sha256'].items():
            if digest(ROOT / path) != expected:
                raise SystemExit('Stale scope evidence: ' + path)
    if scope_phases or dynamic_phases:
        review_path = ('docs/reviews/linkage-author-review.json' if linkage_phases else
                      ('docs/reviews/dynamic-construction-author-review.json' if dynamic_phases
                       else 'docs/reviews/scope-completion-author-review.json'))
        review = read(review_path)
        if review['status'] != 'author_reviewed_with_stated_limits' or review['blocking_findings']:
            raise SystemExit('Substantive scope review has unresolved blocking findings')
        expected_dispositions = {f'W{i}' for i in range(1, 5)} if linkage_phases else {f'G{i}' for i in range(1, 8)}
        if set(review['gap_dispositions']) != expected_dispositions:
            raise SystemExit('Missing comparative gap dispositions')
        for path, expected in review['input_sha256'].items():
            if digest(ROOT / path) != expected:
                raise SystemExit('Manuscript/evidence changed after substantive review: ' + path)
    if dynamic_phases:
        for name in ('docs/reviews/dynamic-verification.json',
                     'docs/reviews/dynamic-scientific-checks.json',
                     'docs/reviews/dynamic-graph-oracle.json'):
            receipt = read(name)
            if receipt['status'] != 'pass':
                raise SystemExit('Dynamic evidence failed: ' + name)
            for path, expected in receipt['input_sha256'].items():
                if digest(ROOT / path) != expected:
                    raise SystemExit('Stale dynamic evidence: ' + path)
    if linkage_phases:
        for name in ('docs/reviews/linkage-verification.json','docs/reviews/linkage-scientific-checks.json'):
            receipt = read(name)
            if receipt['status'] != 'pass':
                raise SystemExit('Linkage evidence failed: ' + name)
            for path, expected in receipt['input_sha256'].items():
                if digest(ROOT / path) != expected:
                    raise SystemExit('Stale linkage evidence: ' + path)
    rendered = {r['pdf']: r for r in read('docs/reviews/foundations-render-receipt.json')}
    visual = read('docs/reviews/reconstruction-visual-inspection.json')
    inspected = {r['pdf']: r for r in visual['documents']}
    paths = set()
    for path, expected in visual.get('input_sha256', {}).items():
        if digest(ROOT / path) != expected:
            raise SystemExit('Visual inspection input changed: ' + path)
        paths.add(path)
    if dynamic_phases:
        # The final wording repair reuses actually viewed images only where
        # their rendered bytes match. Preserve the original inspected bytes
        # as well as the final images and their comparison receipt.
        prior_visual = read('docs/reviews/dynamic-visual-before-wording-repair.json')
        for path, expected in prior_visual['image_sha256'].items():
            if digest(ROOT / path) != expected:
                raise SystemExit('Previously inspected image changed: ' + path)
            paths.add(path)
    if linkage_phases:
        prior_visual = read('docs/reviews/linkage-visual-before-toc-repair.json')
        for path, expected in prior_visual['image_sha256'].items():
            if digest(ROOT / path) != expected:
                raise SystemExit('Pre-spacing-repair inspected image changed: ' + path)
            paths.add(path)
    for document in audit['documents']:
        path = document['path']
        if digest(ROOT / path) != document['sha256']:
            raise SystemExit('PDF changed after audit: ' + path)
        if rendered[path]['sha256'] != document['sha256'] or inspected[path]['sha256'] != document['sha256']:
            raise SystemExit('Render/inspection applies to another PDF: ' + path)
        if set(inspected[path]['contact_sheets_viewed']) != set(rendered[path]['contact_sheets']):
            raise SystemExit('Final layout overview has uninspected contact sheets: ' + path)
        if inspected[path]['blocking_findings']:
            raise SystemExit('Unresolved visual findings: ' + path)
        for sheet in rendered[path]['contact_sheets']:
            paths.update(str(p.relative_to(ROOT)) for p in (ROOT / sheet).parent.iterdir() if p.is_file())
    for source in read('docs/literature/sources.json'):
        if digest(ROOT / source['local_path']) != source['sha256']:
            raise SystemExit('Changed registered source: ' + source['id'])
    if not (ROOT / 'docs/reviews/reconstruction-adversarial-review.md').is_file():
        raise SystemExit('Missing substantive author review')
    if scientific_phases and not (ROOT / 'docs/reviews/scientific-completion-author-review.md').is_file():
        raise SystemExit('Missing scientific completion author review')
    for pattern in (
        'README.md', 'AGENTS.md', 'pyproject.toml', '.gitignore', 'tools/*.py',
        'src/causalbank/*.py', 'contracts/**/*.json', 'contracts/**/*.md',
        'security/*.json', 'security/*.rules', 'security/*.md',
        'docs/*.tex', 'docs/*.pdf', 'docs/*.bib', 'docs/mission-control.*',
        'docs/reconstruction/*.tex', 'docs/reconstruction/*.json',
        'docs/derivations/*', 'docs/examples/*', 'docs/generated/*', 'docs/literature/**/*',
        'docs/papers/*', 'docs/reviews/*.json', 'docs/reviews/*.md',
        'docs/reviews/reference-excerpts-2026-10-08/*',
        'docs/reviews/banking-excerpts-2026-10-08/*',
        'docs/reviews/reconstruction-source-excerpts/*',
        'docs/reviews/dynamic-source-excerpts/*', 'docs/reviews/v5-gap-assessment-excerpts/*',
        'docs/reviews/linkage-source-excerpts/*',
        'docs/reviews/interface-snapshots/*', 'docs/studies/**/*',
        'docs/program/*.json', 'docs/program/*.md', 'docs/program/history/**/*',
        'docs/build/causal_foundations.*', 'docs/build/sponsor_reconstruction.*'):
        paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern) if p.is_file())
    paths.discard(str(RECONSTRUCTION_TARGET.relative_to(ROOT)))
    sources = read('docs/literature/sources.json')
    manifest = {
        'version': '6.1' if linkage_phases else ('6.0' if dynamic_phases else ('5.0' if scope_phases else ('4.0' if scientific_phases else '3.0'))),
        'status': 'author_reviewed_proposal', 'date': '2026-10-09' if scope_phases else '2026-10-08',
        'publication_cutoff': '2026-10-07', 'documents': audit['documents'],
        'review': ('docs/reviews/linkage-author-review.md' if linkage_phases else ('docs/reviews/dynamic-construction-author-review.md' if dynamic_phases else
                  ('docs/reviews/scope-completion-author-review.md' if scope_phases else
                   ('docs/reviews/scientific-completion-author-review.md' if scientific_phases else
                    'docs/reviews/reconstruction-adversarial-review.md')))),
        'program_state': 'docs/program/state.json',
        'rendered_review': 'docs/reviews/reconstruction-visual-inspection.json',
        'source_trace': 'docs/literature/reconstruction-source-trace.json',
        'source_closure': {'registered_works': len(sources),
                           'scholarly_pdfs': sum(s['kind'] == 'paper' for s in sources),
                           'active_cited_works': audit['cited_works'], 'claims': audit['claims']},
        'historical_withdrawal': 'docs/program/delivery-manifest.json',
        'scope': 'Author-reviewed scholarly survey and product construction/investment proposal with selected local runtime evidence. Not user acceptance, independent review, bank validation, deployed product or accepted sibling adoption.',
        'verification': 'python3 tools/delivery_manifest.py verify',
        'note': 'Manifest excludes itself. File identity is necessary evidence, not independent scientific verification.',
        'artifacts': [{'path': path, 'sha256': digest(ROOT / path), 'bytes': (ROOT / path).stat().st_size}
                      for path in sorted(paths)]}
    RECONSTRUCTION_TARGET.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return verify(RECONSTRUCTION_TARGET)


def freeze():
    if read('docs/program/state.json').get('revision') in ('3.0-reconstruction', '4.0-scientific-completion', '5.0-scope-completion', '6.0-dynamic-construction', '6.1-linkage-inference'):
        return freeze_reconstruction()
    audit = read("docs/reviews/archive-audit.json")
    consistency = read("docs/program/consistency-check.json")
    state = read("docs/program/state.json")
    render = read("docs/reviews/render-receipt.json")
    for label, result in (("archive audit", audit), ("program consistency", consistency),
                          ("numerical verification", read("docs/reviews/revision-verification.json")),
                          ("example replay", read("docs/examples/replay-check.json")),
                          ("contracts", read("docs/examples/contract-checks.json"))):
        if result["status"] != "pass":
            raise SystemExit("Cannot freeze failed " + label)
    active = [p for p in state["phases"] if p["id"].startswith("R")]
    if not active or any(p["status"] != "complete" for p in active):
        raise SystemExit("Cannot freeze incomplete reconstruction phases")
    paths = set()
    for path, expected in read("docs/reviews/checked-files.json").items():
        if digest(ROOT / path) != expected:
            raise SystemExit("Changed since archive audit: " + path)
        paths.add(path)
    rendered = {r["pdf"]: r for r in render}
    for doc in audit["documents"]:
        if digest(ROOT / doc["path"]) != doc["sha256"]:
            raise SystemExit("Changed audited document: " + doc["path"])
        r = rendered[doc["path"]]
        if r["sha256"] != doc["sha256"] or r["pages"] != doc["pages"]:
            raise SystemExit("Stale render receipt: " + doc["path"])
        for sheet in r["contact_sheets"]:
            paths.update(str(p.relative_to(ROOT)) for p in (ROOT / sheet).parent.iterdir() if p.is_file())
    for pattern in (
        "README.md", "AGENTS.md", "pyproject.toml", ".gitignore",
        "tools/*.py", "src/causalbank/*.py", "contracts/**/*.json", "contracts/*.md",
        "security/*.json", "security/*.rules", "security/*.md",
        "docs/*.tex", "docs/*.pdf", "docs/*.bib", "docs/mission-control.*",
        "docs/chapters/*.tex", "docs/generated/*", "docs/figures/*",
        "docs/examples/*", "docs/derivations/*", "docs/literature/*.json",
        "docs/literature/*.md", "docs/literature/*.csv", "docs/papers/index.*",
        "docs/reviews/*.json", "docs/reviews/*.md", "docs/program/*.json",
        "docs/program/*.md", "docs/program/history/*.zip",
        "docs/build/*.log", "docs/build/*.blg", "docs/build/*.aux", "docs/build/*.bbl",
    ):
        paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern) if p.is_file())
    paths.discard(str(TARGET.relative_to(ROOT)))
    artifacts = [{"path": path, "sha256": digest(ROOT / path),
                  "bytes": (ROOT / path).stat().st_size} for path in sorted(paths)]
    manifest = {
        "version": state["revision"], "cutoff": "2026-10-07",
        "scope": "Author-reviewed research proposal, preserved sources, synthetic studies and narrow reusable components. Full bank product implementation is future work.",
        "documents": audit["documents"],
        "source_closure": {"register": "docs/literature/sources.json",
                           "checked_files": "docs/reviews/checked-files.json",
                           "registered_works": audit["registered_works"],
                           "scholarly_pdfs": audit["scholarly_pdfs"],
                           "all_preserved_pdfs": audit["all_preserved_pdfs"],
                           "audited_file_count": audit["hashed_files_checked"]},
        "program_state": "docs/program/state.json",
        "review": "docs/reviews/revision-review.md",
        "history": "docs/program/history/v1-rejected-delivery.zip",
        "reconstruction": "python3 tools/delivery_manifest.py verify",
        "note": "The manifest excludes itself. It records file identity and does not independently validate the claims.",
        "artifacts": artifacts,
    }
    TARGET.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return verify()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("freeze", "verify"))
    command = parser.parse_args().command
    raise SystemExit(0 if (freeze() if command == "freeze" else verify()) else 1)
