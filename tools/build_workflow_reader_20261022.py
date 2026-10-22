#!/usr/bin/env python3
"""Preserve prior reader while integrating temporally qualified workflow evidence."""
import argparse
import json
from pathlib import Path
import re

import build_network_commercial_reader_20261020 as engine
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
import workflow_replay_reference_20261022 as exact

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-22/computation-workflow-reader-v1'
OUT = BASE / 'reader'
PREFLIGHT = DOCS / 'program/execution/2026-10-22/computation-commercial-preflight-v1'
PREDECESSOR = DOCS / 'program/execution/2026-10-22/factuality-weighted-reader-v1/publication-v2'
OLD = DOCS / 'causal_proposal_factuality_targets_reviewed_v2_2026-10-22.tex'
PRIOR = PREDECESSOR / 'reader/source-audit.json'
NAME = 'causal_proposal_workflow_reviewed_2026-10-22'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
DEVELOPMENT = BASE / 'development.tex'
LABELS = ['exec22:workflow-' + s for s in ['scope', 'target', 'duplicates', 'cost', 'manifest']]
read = lambda p: json.loads(p.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/comprehensive-v14/work/TEXT.DRAFT.S10/chapter.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker + '\n' + r'\input{' + str(DEVELOPMENT.relative_to(DOCS)) + '}')
    text = text.replace(r'\date{14 October 2026', r'\date{22 October 2026', 1)
    return re.sub(r'\\bibliography\{([^}]+)\}',
        lambda m: r'\bibliography{' + m.group(1) + ',' + str((BASE / 'refs').relative_to(DOCS)) + '}', text)


def configure():
    for name in ['ROOT', 'DOCS', 'BASE', 'OUT', 'PREDECESSOR', 'OLD', 'PRIOR',
            'NAME', 'DRIVER', 'PDF', 'DEVELOPMENT', 'LABELS']:
        setattr(engine, name, globals()[name])
    engine.exact = exact
    engine.expected_driver = expected_driver


def prepare():
    configure()
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    evidence = []
    for name in ['source-audit.json', 'review.json', 'acquisition-review.json',
            'omissions-register.json', 'exact-results.json', 'comparison.md']:
        if name.endswith('.json'):
            verify_bindings(read(PREFLIGHT / name))
        evidence.append(ref(PREFLIGHT / name, 'Reviewed source preflight'))
    assert exact.calculate() == read(PREFLIGHT / 'exact-results.json')
    records = read(PREFLIGHT / 'source-audit.json')['sources']
    assert len(records) == 6 and not any(s['cutoff_eligible'] for s in records)
    code = ROOT / 'tools/workflow_replay_reference_20261022.py'
    records.append(dict(integrated_citation_key='exec22_workflow_reference',
        kind='project_evidence_not_scholarly_paper', title='Exact finite-table causal-batch replay reference',
        author='Causal banking proposal project', year=2026, source_identity=str(code.relative_to(ROOT)),
        version_date='22 October 2026; exact authored rational reference',
        local_copy=ref(code, 'Executable authored construction, no external runtime'),
        inspected_anchors=[dict(anchor='calculate(): finite units, append and keyed replay, target/vintage and manifest checks',
            inspected_text=code.read_text())],
        supported_claims=['Effects4 and14/3, append bias2/3, keyed recovery4, changed-target net-1, changed-vintage effect2.',
            'Semantic manifest detects declared data, target and environment changes in the authored example.'],
        limitations=['Stipulated values, not observed bank effects or vendor executions.',
            'Byte/declaration equality does not establish complete dependencies or causal validity.']))
    write(BASE / 'source-audit.json', dict(sources=records, cutoff='2026-10-07',
        temporal_scope='Six explicitly current later observations, none accepted as cutoff-era capability.',
        source_reviews=evidence))
    write(BASE / 'exact-results.json', exact.calculate())
    write(BASE / 'plan-review.json', dict(status='pass',
        evidence=[ref(BASE / 'integration-plan.md', 'Reviewed preserving integration plan')],
        checks=['Preserve all earlier identities, contexts and content inputs.',
            'Keep all six current manual observations outside cutoff-era acceptance.',
            'Separate exact authored arithmetic, proposed public trials and native qualification.',
            'Integrate in existing computation chapter and pair sponsor; no duplicate coverage credit.']))
    write(BASE / 'review.json', dict(status='pass_for_connected_current_source_synthesis', evidence=evidence,
        findings=['Current settings, procedure versions, cache declarations and redrive budgets matter for semantic replay.',
            'Current AWS named payload-limit handling differs from States.ALL wildcard semantics.',
            'Dataiku index claims are limited to topic scope; other families and historical revisions remain open.',
            'Public fixtures can test computational preservation before costly commercial or bank studies.'],
        cutoff_coverage_acceptance=False, native_execution=False, visual_acceptance=False))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_exact_authored_construction', issues=[],
        evidence=[ref(DEVELOPMENT, 'Defined target, duplicate weights, cost and manifest'),
            ref(code, 'Exact rational arithmetic'), ref(BASE / 'exact-results.json', 'Reproduced values')],
        checks=exact.calculate()['checks'],
        findings=['Duplicate A outputs change group weight3/4 to5/6 and mean4 to14/3.',
            'Keyed result recovers four units but retains six attempts; same semantic manifest is required.',
            'Alternative target net-1 and changed-vintage net1 differ from baseline net3.',
            'Hash equality, replay equivalence, identification and sampling coverage are different claims.'],
        statistical_calibration=False, vendor_execution=False))
    write(BASE / 'copyedit-review.json', dict(status='pass',
        evidence=[ref(DEVELOPMENT, 'Connected banking argument')],
        findings=['All quantities, units and finite-population assumptions are stated.',
            'Vendor mechanisms support design requirements without unsupported absence or superiority claims.',
            'Temporal boundaries, proposed versus performed experiments and later acceptance remain explicit.',
            'No internal acquisition/checkpoint procedure is presented as product behavior.'], rendered_review=False))
    write(BASE / 'manuscript-plan-review.json', dict(status='pass',
        evidence=[ref(BASE / 'plan-review.json', 'Reviewed plan')],
        checks=['Place after matched qualification; retain all earlier sources.',
            'Develop library/CLI/MCP preservation alongside commercial reuse alternatives.',
            'Preserve census61/52, Q1/Q5 and all mandatory repairs as open.']))
    bib = []
    for s in records:
        note = (r'\url{' + s['source_identity'] + '}; ' + engine.shared.escape(s['version_date'])
            if s['source_identity'].startswith('https://') else engine.shared.escape(s['source_identity'] + '; ' + s['version_date']))
        bib.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + engine.shared.escape(s['author']) + '}},\n title={'
            + engine.shared.escape(s['title']) + '},\n year={' + str(s['year']) + '},\n note={' + note + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    entries = engine.sources()
    paths = [OLD, PRIOR, DEVELOPMENT, Path(__file__), code, ROOT / 'tools/build_network_commercial_reader_20261020.py']
    paths += [BASE / n for n in ['integration-plan.md', 'source-audit.json', 'review.json', 'plan-review.json',
        'mathematical-review.json', 'copyedit-review.json', 'manuscript-plan-review.json', 'exact-results.json']]
    write(BASE / 'prepared-inputs.json', dict(inputs=[ref(p, 'Reviewed preserving input') for p in paths],
        generated=[ref(DRIVER, 'Preserving driver'), ref(BASE / 'refs.bib', 'Audited additions')],
        prior_cited_records=len(read(PRIOR)['sources']), expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR / 'traceability-review.json')['scholarly_pdfs'],
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), records=len(entries), scholarly_pdfs=221)))


def build():
    configure()
    engine.build()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
