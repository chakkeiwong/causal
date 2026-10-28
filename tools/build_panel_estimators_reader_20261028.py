"""Preserve the reader and integrate panel baselines, targets and weights."""
import argparse
import json
from pathlib import Path

import build_panel_delegates_reader_20261028 as previous
import build_preserving_reader_v2_20261024 as engine
import panel_estimator_reference_20261028 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
DAY = DOCS / 'program/execution/2026-10-28'
BASE = DAY / 'panel-estimators-reader-v1'
OUT = BASE / 'reader'
SOURCE = DAY / 'panel-estimator-contracts-v1'
PREDECESSOR = DAY / 'panel-delegates-reader-v1'
OLD = DOCS / 'causal_proposal_panel_delegates_reviewed_v1_2026-10-28.tex'
PRIOR = PREDECESSOR / 'reader/source-audit.json'
NAME = 'causal_proposal_panel_estimators_reviewed_v1_2026-10-28'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
DEVELOPMENT = BASE / 'development.tex'
LABELS = ['sec:exec28-panel-estimator-contracts']
read = lambda p: json.loads(p.read_text())
display_version = previous.display_version


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-28/panel-delegates-reader-v1/development.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker + '\n' + r'\input{' + str(DEVELOPMENT.relative_to(DOCS)) + '}')
    start = text.index(r'\bibliography{') + len(r'\bibliography{')
    end = text.index('}', start)
    return text[:end] + ',' + str((BASE / 'refs').relative_to(DOCS)) + text[end:]


def expected_development():
    return (SOURCE / 'development.tex').read_text()


def configure():
    for name in ('ROOT', 'DOCS', 'BASE', 'OUT', 'PREDECESSOR', 'OLD', 'PRIOR',
                 'NAME', 'DRIVER', 'PDF', 'DEVELOPMENT', 'LABELS', 'expected_driver'):
        setattr(engine, name, globals()[name])
    engine.exact = exact


def prepare():
    assert not BASE.exists() and not DRIVER.exists() and not PDF.exists()
    for path in (PRIOR, PREDECESSOR / 'release-source-review.json',
                 SOURCE / 'review.json', SOURCE / 'source-audit.json'):
        verify_bindings(read(path))
    prior = {s['integrated_citation_key']: s for s in read(PRIOR)['sources']}
    incoming = read(SOURCE / 'source-audit.json')['sources']
    assert len(prior) == 1447 and len(incoming) == 2
    assert not prior.keys() & {s['integrated_citation_key'] for s in incoming}
    assert exact.calculate() == read(SOURCE / 'exact-results.json')
    BASE.mkdir()
    for name in ('development.tex', 'sponsor-addition.md', 'source-audit.json',
                 'exact-results.json', 'mathematical-review.json', 'copyedit-review.json', 'plan-review.json'):
        (BASE / name).write_bytes((SOURCE / name).read_bytes())
    (BASE / 'integration-plan.md').write_text(
        'Preserve all 1447 prior source records, citation contexts and compiled content inputs. '
        'Add Nine pinned estimator/conversion sources and exact boundary witnesses. '
        'No native, broad coverage, visual or final acceptance is inferred.\n')
    bib = []
    for source in incoming:
        bib.append('\n'.join(['@misc{' + source['integrated_citation_key'] + ',',
            ' author={' + (source['author'] if source['kind']=='paper' else '{'+engine.shared.escape(source['author'])+'}') + '},',
            ' title={' + engine.shared.escape(source['title']) + '},',
            ' year={' + str(source['year']) + '},',
            ' note={' + display_version(source['version_date']) + '}', '}']))
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    paths = [OLD, PRIOR, Path(__file__), Path(exact.__file__), SOURCE / 'review.json',
             PREDECESSOR / 'release-source-review.json']
    paths += [BASE / n for n in ('development.tex', 'source-audit.json', 'exact-results.json',
              'mathematical-review.json', 'copyedit-review.json', 'plan-review.json', 'integration-plan.md')]
    write(BASE / 'prepared-inputs.json', dict(inputs=[ref(p, 'Reviewed preserving input') for p in paths],
          generated=[ref(DRIVER, 'Preserving driver'), ref(BASE / 'refs.bib', 'Two audited additions')],
          prior_cited_records=1447, expected_cited_records=1449, expected_scholarly_pdfs=277,
          visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), records=1449)))


def build():
    configure()
    engine.build()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    globals()[parser.parse_args().command]()
