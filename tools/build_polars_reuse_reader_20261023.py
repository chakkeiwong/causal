#!/usr/bin/env python3
"""Preserve the current reader while adding Polars population/clock/execution contracts."""
import argparse
import json
import re
from pathlib import Path

import build_network_commercial_reader_20261020 as engine
import polars_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-23/polars-reuse-reader-v1'
OUT = BASE / 'reader'
SOURCE = DOCS / 'program/execution/2026-10-23/polars-reuse-v1'
PREDECESSOR = DOCS / 'program/execution/2026-10-23/workflow-delegates-reader-v1'
OLD = DOCS / 'causal_proposal_workflow_delegates_reviewed_2026-10-23.tex'
PRIOR = PREDECESSOR / 'reader/source-audit.json'
NAME = 'causal_proposal_polars_reuse_reviewed_2026-10-23'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
DEVELOPMENT = BASE / 'development.tex'
LABELS = ['sec:exec23-polars-worker', 'eq:exec23-polars-fanout', 'eq:exec23-polars-overlap']
read = lambda p: json.loads(p.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-23/workflow-delegates-reader-v1/development.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker + '\n' + r'\input{' + str(DEVELOPMENT.relative_to(DOCS)) + '}')
    return re.sub(r'\\bibliography\{([^}]+)\}', lambda m: r'\bibliography{' + m.group(1) + ',' + str((BASE / 'refs').relative_to(DOCS)) + '}', text)


def configure():
    for k in ['ROOT', 'DOCS', 'BASE', 'OUT', 'PREDECESSOR', 'OLD', 'PRIOR', 'NAME', 'DRIVER', 'PDF', 'DEVELOPMENT', 'LABELS', 'expected_driver']:
        setattr(engine, k, globals()[k])
    engine.exact = exact


def prepare():
    configure()
    assert not BASE.exists()
    for p in [PRIOR, PREDECESSOR / 'working-release.json', SOURCE / 'review.json', SOURCE / 'source-audit.json']:
        verify_bindings(read(p))
    assert exact.calculate() == read(SOURCE / 'exact-results.json')
    BASE.mkdir()
    write(BASE / 'exact-results.json', exact.calculate())
    DEVELOPMENT.write_bytes((SOURCE / 'development.tex').read_bytes())
    (BASE / 'sponsor-addition.md').write_bytes((SOURCE / 'sponsor-addition.md').read_bytes())
    write(BASE / 'source-audit.json', read(SOURCE / 'source-audit.json'))
    (BASE / 'integration-plan.md').write_text('Preserve all 1008 predecessor citations, contexts and compiled inputs. Add twenty-one authenticated Polars files and independent join-population, missingness, information-clock and overlapping-window witnesses. Distinguish dataframe execution from sampling law, causal validity and information availability; retain checked-join in-memory fallback. Compile and inspect all-page text; renew exact-byte reviews, pair sponsor and continue independent obligations. Visual/final acceptance remain open.\n')
    write(BASE / 'plan-review.json', dict(status='pass', issues=[],
        evidence=[ref(BASE / 'integration-plan.md', 'Preserving plan'), ref(SOURCE / 'review.json', 'Source review')],
        findings=['No global dependency gate.', 'No downloaded code executes.']))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_project_owned_contract_witnesses', issues=[],
        evidence=[ref(SOURCE / 'exact-results.json', 'Exact outputs'), ref(Path(exact.__file__), 'Reference source'), ref(DEVELOPMENT, 'Connected argument')],
        findings=['Fanout changes descriptive contrast5 to15/2; stipulated cost6 yields margins-1 and3/2 without identifying causal effects.',
            'Missing observed value permits complete means2 and14/3; event-backward, nearest and availability-aware matches give0,10,4.',
            'Eight sign triples yield window covariance1/4 and mean variance3/8, versus incorrect independence1/4.'], native_execution=False))
    write(BASE / 'copyedit-review.json', dict(status='pass', issues=[], evidence=[ref(DEVELOPMENT, 'Connected argument'), ref(BASE/'sponsor-addition.md','Sponsor counterpart')],
        findings=['Python2.0.0 and Rust0.55.1 remain source declarations, not authenticated releases.',
            'Missing-data, null-key identity, event/availability and overlap uncertainty remain separate contracts.',
            'Checked joins can lower to an in-memory node; neither discarded validation nor native success is claimed.',
            'All costs/populations are supplied examples; no package benchmark, bank ROI or native approval.'], visual_acceptance=False))
    bib = []
    for s in read(BASE / 'source-audit.json')['sources']:
        author = '{' + engine.shared.escape(s['author']) + '}'
        bib.append('@misc{' + s['integrated_citation_key'] + ',\n author={' + author + '},\n title={' + engine.shared.escape(s['title']) + '},\n year={' + str(s['year']) + '},\n note={' + engine.shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    paths = [OLD, PRIOR, DEVELOPMENT, Path(__file__), SOURCE / 'review.json', SOURCE / 'static-contract-check.json', Path(exact.__file__), BASE / 'exact-results.json']
    paths += [BASE / n for n in ['source-audit.json', 'integration-plan.md', 'plan-review.json', 'mathematical-review.json', 'copyedit-review.json']]
    write(BASE / 'prepared-inputs.json', dict(inputs=[ref(p, 'Reviewed input') for p in paths],
        generated=[ref(DRIVER, 'Preserving driver'), ref(BASE / 'refs.bib', 'Two references')],
        prior_cited_records=1008, expected_cited_records=1010, expected_scholarly_pdfs=232, visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), records=1010)))


def build():
    configure()
    engine.build()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['prepare', 'build'])
    globals()[p.parse_args().command]()
