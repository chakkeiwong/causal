#!/usr/bin/env python3
"""Build a preserving commercial-capability successor to the S7 reader."""
import argparse
import json
import re
from contextlib import redirect_stdout
from pathlib import Path

import audit_reader_traceability_v2_20261013 as trace
import build_integrated_monograph_v12 as shared
import build_java_temporal_engine_20261016 as engine
import s8_examples_20261017 as examples
import prepare_s8_20261017 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "docs/program/execution/2026-10-17/s8"
BASE = WORK / "publication-v1"
OUT = BASE / "reader"
PRIOR = ROOT / "docs/program/execution/2026-10-17/s7/publication-v2/reader/source-audit.json"
OLD = ROOT / "docs/causal_proposal_observation_reviewed_v2_2026-10-17.tex"
CANONICAL_OLD = ROOT / "docs/causal_proposal_observation_reviewed_v2_2026-10-17.pdf"
CHAPTER = work.CHAPTER
NAME = "causal_proposal_commercial_gap_reviewed_2026-10-17"
DRIVER = ROOT / "docs" / (NAME + ".tex")
PDF = DRIVER.with_suffix(".pdf")
INSERT = r"\input{program/comprehensive-v14/work/TEXT.DRAFT.S8/chapter.tex}"
LABELS = ["s8", "s8-question", "s8-map", "s8-journeys", "s8-discovery", "s8-effects", "s8-temporal",
          "s8-policy", "s8-information", "s8-boundary", "s8-editions", "s8-scheduling", "s8-cost", "s8-signal",
          "s8-decision", "s8-protocol", "s8-end"]


def read(path):
    return json.loads(path.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r"\input{program/execution/2026-10-17/s7/publication-v2/chapter.tex}"
    assert text.count(marker) == 1
    text = text.replace(marker, marker + "\n" + INSERT)
    pattern = re.compile(r"\\bibliography\{([^}]+)\}")
    assert len(pattern.findall(text)) == 1
    return pattern.sub(lambda m: r"\bibliography{" + m.group(1) +
                       ",program/execution/2026-10-17/s8/publication-v1/refs}", text)


def verify_exact():
    for name in ['primary-review.json', 'prototype-design.json', 'source-audit.json',
                 'precompile-author-review.json', 'mathematics-review.json']:
        verify_bindings(read(WORK/name))
    exact=read(WORK/'exact-results.json')
    assert examples.calculate()==exact and examples.separate(exact)['status']=='pass'
    assert CHAPTER.read_text()==(WORK/'chapter.tex').read_text()


def prepare():
    assert not BASE.exists() and not DRIVER.exists() and not PDF.exists()
    verify_bindings(read(PRIOR)); verify_exact()
    sources=read(WORK/'source-audit.json')['sources']; assert len(sources)==3
    cited={k.strip() for group in re.findall(shared.CITE,CHAPTER.read_text()) for k in group.split(',')}
    assert cited <= ({s['integrated_citation_key'] for s in read(PRIOR)['sources']} |
                     {s['integrated_citation_key'] for s in sources})
    BASE.mkdir()
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',prior=ref(PRIOR,'721 unchanged audited records')))
    bib=[]
    for source in sources:
        bib.append('@misc{'+source['integrated_citation_key']+',\n author={{'+
                   shared.escape(source['author'])+'}},\n title={'+shared.escape(source['title'])+
                   '},\n year={2026},\n note={'+shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    write(BASE / "prepared-inputs.json", {
        "inputs": [ref(p, "Preserved or reviewed S8 input") for p in
                   [OLD, PRIOR, CHAPTER, WORK/'plan.md', WORK/'primary-review.json',
                    WORK/'mathematics-review.json', WORK/'prototype-design.json',
                    WORK/'precompile-author-review.json', WORK/'source-audit.json', Path(__file__)]],
        "generated": [ref(p, "S8 preserving successor") for p in [DRIVER, BASE/'source-audit.json', BASE / "refs.bib"]],
        "transformation": "Insert one S8 chapter after S7 publication copy; append one bibliography namespace.",
        "credit_policy": "Only new commercial acquisition, boundary, scheduling, cost, regret and signal synthesis receives S8 credit; inherited vendor catalogs and mathematics receive no duplicate credit.",
        "visual_acceptance": False
    })
    print(json.dumps({"prepared": str(DRIVER.relative_to(ROOT)), "new_records": 3,
                      "expected_pages": "successor exceeds 977"}))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert DRIVER.read_text() == expected_driver()
    verify_bindings(read(BASE / "prepared-inputs.json"))
    verify_exact()
    for key, value in {"BASE": BASE, "OUT": OUT, "OLD": OLD, "NAME": NAME,
                       "DRIVER": DRIVER, "PDF": PDF, "PRIOR_AUDIT": PRIOR}.items():
        setattr(engine, key, value)
    engine.layout.OUT = OUT
    with (BASE / "compile-summary.log").open("x") as stream:
        with redirect_stdout(stream):
            engine.build()
    report = read(OUT / "build-report.json")
    aux = (OUT / (NAME + ".aux")).read_text()
    sections = {}
    for label in LABELS:
        match = re.search(re.escape(r"\newlabel{exec17:" + label + r"}{{") +
                          r"[^}]*\}{([0-9]+)", aux)
        assert match, label
        sections[label] = int(match.group(1))
    report.update(pdf=ref(PDF, "Preserving commercial capability working reader"),
                  driver=ref(DRIVER, "Preserving S8 driver"),
                  builder=ref(Path(__file__), "Bounded S8 source/audit builder"),
                  predecessor_pdf=ref(CANONICAL_OLD, "977-page canonical predecessor"),
                  commercial_sections=sections)
    audit = trace.audit(DRIVER, OUT / "source-audit.json")
    write(BASE / "traceability-review.json", audit)
    assert report["pages"] > 977 and report["cited_records"] == 724
    assert audit["status"] == "pass" and not audit["issues"] and audit["scholarly_pdfs"] == 188
    # Complete this new, as-yet unbound report before any review binds it.
    engine.core.write(OUT / "build-report.json", report)
    print(json.dumps({"pages": report["pages"], "cited_records": report["cited_records"],
                      "sections": sections, "scholarly_pdfs": audit["scholarly_pdfs"],
                      "material_warnings": [w for w in report["warnings"] if "Underfull" not in w]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "build"])
    args = parser.parse_args()
    prepare() if args.command == "prepare" else build()
