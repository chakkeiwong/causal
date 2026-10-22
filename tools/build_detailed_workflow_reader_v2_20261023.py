#!/usr/bin/env python3
"""Preserve the complete reader and develop its existing commercial-workflow chapter."""
import argparse
import json
from pathlib import Path
import re
from types import SimpleNamespace

import build_network_commercial_reader_20261020 as engine
import workflow_denominator_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-23/detailed-workflow-reader-v2'
OUT = BASE / 'reader'
PREDECESSOR = DOCS / 'program/execution/2026-10-23/semantics-reader-v4'
OLD = DOCS / 'causal_proposal_semantics_reviewed_v4_2026-10-23.tex'
PRIOR = PREDECESSOR / 'reader/source-audit.json'
NAME = 'causal_proposal_detailed_workflow_reviewed_2026-10-23'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
SOURCE = DOCS / 'program/execution/2026-10-23/dataiku-workflow-v1'
DEVELOPMENT = BASE / 'development.tex'
INSERTIONS = {'program/execution/2026-10-22/computation-workflow-reader-v1/development.tex': 'development.tex'}
LABELS = ['exec23:dss-' + x for x in ['scope', 'target', 'full-net', 'bounds', 'cutoff']]
read = lambda p: json.loads(p.read_text())


def calculate():
    return json.loads(json.dumps(exact.calculate()))


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{' + next(iter(INSERTIONS)) + '}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker + '\n' + r'\input{' + str(DEVELOPMENT.relative_to(DOCS)) + '}')
    return re.sub(r'\\bibliography\{([^}]+)\}', lambda m:
        r'\bibliography{' + m.group(1) + ',' + str((BASE / 'refs').relative_to(DOCS)) + '}', text)


def configure():
    for name in ['ROOT', 'DOCS', 'BASE', 'OUT', 'PREDECESSOR', 'OLD', 'PRIOR',
                 'NAME', 'DRIVER', 'PDF', 'DEVELOPMENT', 'LABELS', 'expected_driver']:
        setattr(engine, name, globals()[name])
    engine.exact = SimpleNamespace(calculate=calculate)


def prepare():
    configure()
    assert not BASE.exists() and not DRIVER.exists() and not PDF.exists()
    for path in [PRIOR, PREDECESSOR / 'working-release.json', SOURCE / 'review.json', SOURCE / 'source-audit.json']:
        verify_bindings(read(path))
    assert calculate() == read(SOURCE / 'exact-results.json')
    BASE.mkdir()
    DEVELOPMENT.write_bytes((SOURCE / 'development.tex').read_bytes())
    (BASE / 'sponsor-addition.md').write_bytes((SOURCE / 'sponsor-addition.md').read_bytes())
    (BASE / 'integration-plan.md').write_text('''# Integrate detailed workflow semantics into the existing chapter

Preserve every previous source identity, citation context and compiled content
input. Insert the reviewed Dataiku development immediately after the earlier
six-manual workflow argument, within the existing chapter. Preserve source
temporal omissions, exact financial assumptions, proposal status and all prior
negative/inconclusive results. Compile without shell escape and review the
entire citation audit and text bounds. Renew only exact-reader author gates
Q2-Q4, pair the sponsor to the new bytes, and leave visual/final acceptance
open. This release does not close commercial coverage or the mandatory repairs.
''')
    write(BASE / 'source-audit.json', dict(sources=read(SOURCE / 'source-audit.json')['sources'],
        cutoff='2026-10-07', primary_review=ref(SOURCE / 'review.json', 'Six inspected originals and exact construction'),
        omissions=ref(SOURCE / 'omissions-register.json', 'Historical and candidate-specific limits')))
    write(BASE / 'source-completion-review.json', dict(status='pass_with_limits',
        evidence=[ref(SOURCE / n, 'Bounded inspected primary evidence') for n in
            ['review.json', 'extraction-review.json', 'source-audit.json', 'inspection-progress.json', 'omissions-register.json']],
        checks=['Detailed technical pages support failure and trigger claims.',
            'DSS 15 predates cutoff; exact patch bytes remain unauthenticated.',
            'Native execution, rights, price and broader market coverage remain open.']))
    write(BASE / 'exact-results.json', calculate())
    write(BASE / 'plan-review.json', dict(status='pass', issues=[],
        evidence=[ref(BASE / 'integration-plan.md', 'Reviewed preserving plan'), ref(DEVELOPMENT, 'Chapter development')],
        checks=['Preserve earlier source identities, contexts and all content inputs.',
            'Integrate into the existing workflow chapter and retain monetary assumptions.',
            'Keep source acquisition, governance and controller details outside the product narrative.',
            'Leave visual/final acceptance and broader commercial obligations open.']))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_exact_authored_argument', issues=[],
        evidence=[ref(DEVELOPMENT, 'Defined target and finite examples'), ref(BASE / 'exact-results.json', 'Exact replay'),
            ref(Path(exact.__file__), 'Fraction arithmetic and independent cents accounting')],
        findings=['Both cohort weights remain one half in the declared target.',
            'Full net -11 and available-only +9 differ by20 USD and reverse the sign.',
            'Assumed [-50,50] missing-effect bounds imply [-21,29] net bounds, not a confidence interval.',
            'An unchanged count/max-date proxy can accompany changed net value19.',
            'Missing-return dispositions illustrate an authored ledger, not vendor runtime behavior.'],
        native_execution=False, empirical_coverage=False))
    write(BASE / 'copyedit-review.json', dict(status='pass', evidence=[ref(DEVELOPMENT, 'Connected argument')],
        findings=['Weights, costs, policy, information clock and assumptions are explicit.',
            'Documentation findings, source-version limits and proposed prototype are distinguished.',
            'An adequate stronger SQL query remains possible; no absence claim follows.'], visual_acceptance=False))
    bibliography = []
    for source in read(BASE / 'source-audit.json')['sources']:
        identity = source['source_identity']
        note = (r'\url{' + identity + '}; ' if identity.startswith('https://') else engine.shared.escape(identity) + '; ')
        note += engine.shared.escape(source['version_date'])
        bibliography.append('@misc{' + source['integrated_citation_key'] + ',\n author={{' +
            engine.shared.escape(source['author']) + '}},\n title={' + engine.shared.escape(source['title']) +
            '},\n year={2026},\n note={' + note + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bibliography))
    DRIVER.write_text(expected_driver())
    entries = engine.sources()
    paths = [OLD, PRIOR, DEVELOPMENT, Path(__file__), Path(exact.__file__)]
    paths += [BASE / n for n in ['integration-plan.md', 'source-audit.json', 'source-completion-review.json',
        'exact-results.json', 'plan-review.json', 'mathematical-review.json', 'copyedit-review.json']]
    write(BASE / 'prepared-inputs.json', dict(inputs=[ref(p, 'Reviewed preserving input') for p in paths],
        generated=[ref(DRIVER, 'Preserving driver'), ref(BASE / 'refs.bib', 'Seven audited additional citations')],
        prior_cited_records=len(read(PRIOR)['sources']), expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR / 'traceability-review.json')['scholarly_pdfs'],
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), records=len(entries), added=7)))


def build():
    configure()
    engine.build()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
