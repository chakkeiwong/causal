#!/usr/bin/env python3
"""Preserve the current reader while adding commercial workflow delegate contracts."""
import argparse
import json
import re
from pathlib import Path

import build_network_commercial_reader_20261020 as engine
import workflow_delegate_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-23/workflow-delegates-reader-v1'
OUT = BASE / 'reader'
SOURCE = DOCS / 'program/execution/2026-10-23/workflow-delegates-v2'
PREDECESSOR = DOCS / 'program/execution/2026-10-23/numpyro-reuse-reader-v1'
OLD = DOCS / 'causal_proposal_numpyro_reuse_reviewed_2026-10-23.tex'
PRIOR = PREDECESSOR / 'reader/source-audit.json'
NAME = 'causal_proposal_workflow_delegates_reviewed_2026-10-23'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
DEVELOPMENT = BASE / 'development.tex'
LABELS = ['sec:exec23-workflow-delegates', 'eq:exec23-delegate-time']
read = lambda p: json.loads(p.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-23/workflow-clients-reader-v2/development.tex}'
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
    (BASE / 'integration-plan.md').write_text('Preserve all 1004 predecessor citations, contexts and compiled inputs. Add twelve authenticated SAS, Domino and Posit delegates plus exact project-owned timing, sampling-frame, terminal-cost and finite-observation witnesses. Review client/server, mock/runtime and terminal/scientific-success distinctions. Compile and inspect all-page text; renew exact-byte Q2-Q4, pair the sponsor and refresh every obligation. Record commercial progress without closing the cell. Continue independent work; visual/final acceptance remain open.\n')
    write(BASE / 'plan-review.json', dict(status='pass', issues=[],
        evidence=[ref(BASE / 'integration-plan.md', 'Preserving plan'), ref(SOURCE / 'review.json', 'Source review')],
        findings=['The commercial follow-up does not block other ready branches.', 'No downloaded code executes; no whole-cell or native capability acceptance.']))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_project_owned_contract_witnesses', issues=[],
        evidence=[ref(SOURCE / 'exact-results.json', 'Exact outputs'), ref(Path(exact.__file__), 'Reference source'), ref(DEVELOPMENT, 'Connected argument')],
        findings=['Three supplied refreshes cost 3/2 seconds sleeping and 15/2 seconds including requests; a count bound is not a transport deadline.',
            'Offset pagination after deletion omits initial ID 3; observed mean 1/3 differs from initial 1/2.',
            'Four terminal records have one accepted artifact; stipulated USD 12 gives USD 3 per terminal and USD 12 per accepted artifact.',
            'Two observations of a terminal state cannot prove permanent stability.'], native_execution=False))
    write(BASE / 'copyedit-review.json', dict(status='pass', issues=[],
        evidence=[ref(DEVELOPMENT, 'Connected proposal argument'), ref(BASE / 'sponsor-addition.md', 'Sponsor counterpart')],
        findings=['The SAS generic monitor is not asserted to be the Workflow submission path.',
            'Domino POST retry is unresolved without dependency policy; its reauthentication exception is not RequestException.',
            'Posit Finished includes nonzero exits, omitted network booleans are false and the cancellation skip does not prove a race.',
            'Timings, sampling outcomes and prices are authored witnesses; no vendor measurements or bank ROI claims.',
            'Server schemas, supported versions, entitlement, native tests and market coverage remain explicit.'], visual_acceptance=False))
    bib = []
    for s in read(BASE / 'source-audit.json')['sources']:
        author = '{' + engine.shared.escape(s['author']) + '}'
        bib.append('@misc{' + s['integrated_citation_key'] + ',\n author={' + author + '},\n title={' + engine.shared.escape(s['title']) + '},\n year={' + str(s['year']) + '},\n note={' + engine.shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    paths = [OLD, PRIOR, DEVELOPMENT, Path(__file__), SOURCE / 'review.json', SOURCE / 'conversion-contract.json', Path(exact.__file__), BASE / 'exact-results.json']
    paths += [BASE / n for n in ['source-audit.json', 'integration-plan.md', 'plan-review.json', 'mathematical-review.json', 'copyedit-review.json']]
    write(BASE / 'prepared-inputs.json', dict(inputs=[ref(p, 'Reviewed input') for p in paths],
        generated=[ref(DRIVER, 'Preserving driver'), ref(BASE / 'refs.bib', 'Four audited references')],
        prior_cited_records=1004, expected_cited_records=1008, expected_scholarly_pdfs=232, visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), records=1008)))


def build():
    configure()
    engine.build()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['prepare', 'build'])
    globals()[p.parse_args().command]()
