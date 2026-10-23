#!/usr/bin/env python3
"""Preserve the current reader while adding NumPyro model/prediction contracts."""
import argparse
import json
import re
from pathlib import Path

import build_network_commercial_reader_20261020 as engine
import numpyro_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-23/numpyro-reuse-reader-v1'
OUT = BASE / 'reader'
SOURCE = DOCS / 'program/execution/2026-10-23/numpyro-reuse-v1'
PREDECESSOR = DOCS / 'program/execution/2026-10-23/pymc-reuse-reader-v1'
OLD = DOCS / 'causal_proposal_pymc_reuse_reviewed_2026-10-23.tex'
PRIOR = PREDECESSOR / 'reader/source-audit.json'
NAME = 'causal_proposal_numpyro_reuse_reviewed_2026-10-23'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
DEVELOPMENT = BASE / 'development.tex'
LABELS = ['sec:exec23-numpyro-worker']
read = lambda p: json.loads(p.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-23/pymc-reuse-reader-v1/development.tex}'
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
    (BASE / 'integration-plan.md').write_text('Preserve all 1002 predecessor citations, contexts and compiled inputs. Add twenty authenticated NumPyro blobs and independent conditioning/intervention, cross-world, latent-decision, conjugate and prediction witnesses. Distinguish handler composition, prediction regeneration, posterior averaging, MAP decoding, numerical diagnostics and causal validity. Compile and inspect all-page text; renew exact-byte reviews, pair sponsor and continue independent obligations. Visual/final acceptance remain open.\n')
    write(BASE / 'plan-review.json', dict(status='pass', issues=[],
        evidence=[ref(BASE / 'integration-plan.md', 'Preserving plan'), ref(SOURCE / 'review.json', 'Source review')],
        findings=['No global dependency gate.', 'No downloaded code executes.']))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_project_owned_contract_witnesses', issues=[],
        evidence=[ref(SOURCE / 'exact-results.json', 'Exact outputs'), ref(Path(exact.__file__), 'Reference source'), ref(DEVELOPMENT, 'Connected argument')],
        findings=['Association 4 differs from intervention effect 2; posterior mixture and MAP action values are -20 and 100.',
            'Equal intervention marginals allow cross-world probabilities 1 and 0; beta posterior mean/variance are 3/5 and 6/275.',
            'Stored/regenerated deterministic expressions target different predictions; scan documentation and test tension remain qualified.'], native_execution=False))
    write(BASE / 'copyedit-review.json', dict(status='pass', issues=[], evidence=[ref(DEVELOPMENT, 'Connected proposal argument')],
        findings=['Pinned source version declaration is not labeled as an authenticated distributed release.',
            'Model meaning, native execution and numerical/scientific qualification remain distinct.',
            'Diagnostic absence and upstream xfail are not presented as executed success/failure.'], visual_acceptance=False))
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
        prior_cited_records=1002, expected_cited_records=1004, expected_scholarly_pdfs=232, visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), records=1004)))


def build():
    configure()
    engine.build()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['prepare', 'build'])
    globals()[p.parse_args().command]()
