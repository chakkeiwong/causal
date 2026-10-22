#!/usr/bin/env python3
"""Preserve the integrated reader while adding reviewed causal/software semantics."""
import argparse
import json
from pathlib import Path
import re
from types import SimpleNamespace

import build_network_commercial_reader_20261020 as engine
import context_conflict_reference_20261023 as context
import lmtp_policy_reference_20261022 as policy
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-23/semantics-reader-v4'
OUT = BASE / 'reader'
PREDECESSOR = DOCS / 'program/execution/2026-10-22/computation-workflow-reader-v1'
OLD = DOCS / 'causal_proposal_workflow_reviewed_2026-10-22.tex'
PRIOR = PREDECESSOR / 'reader/source-audit.json'
NAME = 'causal_proposal_semantics_reviewed_v4_2026-10-23'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
DEVELOPMENT = BASE / 'context-development.tex'
CENSUS = DOCS / 'program/execution/2026-10-23/census-context-conflict-v1'
REVIEWS = [DOCS / ('program/execution/2026-10-22/' + name) for name in
           ['linearmodels-reuse-v1', 'java-iv-rd-preflight-v1', 'lmtp-reuse-v1']]
INSERTIONS = {
    'program/execution/2026-10-22/sensitivity-iv-reader-v1/python-development.tex': 'iv-development.tex',
    'program/execution/2026-10-20/gformula-reuse-v1/publication-v2/development.tex': 'longitudinal-development.tex',
    'program/execution/2026-10-17/l2-review-v1/v2/chapter-corrected.tex': 'context-development.tex',
    'program/comprehensive-v14/work/TEXT.DRAFT.L7/chapter-v3.tex': 'conflict-development.tex',
}
LABELS = ['exec23:' + label for label in ['iv-choice', 'iv-java', 'lmtp-scope', 'lmtp-shift',
    'lmtp-odds', 'lmtp-value', 'lmtp-conversion', 'context-scope', 'context-twins',
    'context-laws', 'context-observed', 'context-net', 'context-evaluation',
    'conflict-scope', 'conflict-identity', 'conflict-decoding', 'conflict-prototype']]
read = lambda p: json.loads(p.read_text())


def calculate():
    return dict(context=context.calculate(), policy=policy.calculate())


exact = SimpleNamespace(calculate=calculate)


def expected_driver():
    text = OLD.read_text()
    for marker_path, addition in INSERTIONS.items():
        marker = r'\input{' + marker_path + '}'
        assert text.count(marker) == 1, marker
        text = text.replace(marker, marker + '\n' + r'\input{' +
                            str((BASE / addition).relative_to(DOCS)) + '}')
    text = text.replace(r'\date{22 October 2026', r'\date{23 October 2026', 1)
    return re.sub(r'\\bibliography\{([^}]+)\}', lambda m:
                  r'\bibliography{' + m.group(1) + ',' +
                  str((BASE / 'refs').relative_to(DOCS)) + '}', text)


def configure():
    for name in ['ROOT', 'DOCS', 'BASE', 'OUT', 'PREDECESSOR', 'OLD', 'PRIOR',
                 'NAME', 'DRIVER', 'PDF', 'DEVELOPMENT', 'LABELS', 'exact', 'expected_driver']:
        setattr(engine, name, globals()[name])


def prepare():
    configure()
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    inputs = []
    records = []
    for folder in [CENSUS] + REVIEWS:
        for name in ['source-audit.json', 'primary-review.json' if folder == CENSUS else 'review.json',
                     'plan-review.json', 'omissions-register.json']:
            verify_bindings(read(folder / name))
            inputs.append(ref(folder / name, 'Inspected primary-source review'))
        records += read(folder / 'source-audit.json')['sources']
    for source in records:
        if source['kind'] == 'paper':
            suffix = f" {source['first_author']}({source['year']}).pdf"
            filename = Path(source['local_path']).name
            assert filename.endswith(suffix)
            source['filename_title'] = filename[:-len(suffix)]
            assert source['filename_title'] and Path('docs/papers', filename).is_file()
    assert len(records) == 5
    assert context.calculate() == read(CENSUS / 'exact-results.json')
    assert policy.calculate() == read(REVIEWS[2] / 'exact-policy-results.json')
    extra_paths = [CENSUS / n for n in ['completion-generator-attempt-1.py', 'completion-failure.json',
        'reconciliation-review.json', 'census-register.json', 'task-map.json', 'inspection-progress.json']]
    extra_paths = [BASE / 'traceability-failure.json'] + extra_paths
    extra_paths += [ROOT / 'tools/complete_census_context_conflict_20261023.py']
    extra_paths += [DOCS / ('literature/raw/' + name + '.receipt.json') for name in
                    ['exec23_context_identity', 'exec23_conflict_identity']]
    extra_paths += [DOCS / 'program/execution/2026-10-23/refresh-preservation-v1/correction-review.json']
    for path in extra_paths:
        if path.suffix == '.json':
            verify_bindings(read(path))
    write(BASE / 'source-completion-review.json', dict(status='pass_with_limits',
        evidence=inputs + [ref(p, 'Preserved acquisition, failure or completion identity') for p in extra_paths],
        checks=['Two selected pre-cutoff PDF identities and original acquisition receipts are bound.',
            'Archive-latest metadata is distinguished from the selected v1 bytes.',
            'Completion failure remains preserved; the corrected generator is bound.',
            'Only two census rows changed; 63 inspected, 50 unread, four crosscutting searches remain.',
            'Survey attribution, printed contradictions, source flags and native outcomes remain distinct.'],
        independent_review=False, coverage_acceptance=False, visual_acceptance=False))
    for key, title, module, claims in [
        ('exec23_context_reference', 'Exact authored causal twins, prediction identity and printed-table arithmetic',
         context, ['Identical observed laws yield all-contact versus no-contact incremental net90 and-10 USD.',
                   'Flip-minus-accuracy-gap identity concerns predictions, not latent knowledge.',
                   'Four selected Table5 subtractions disagree; Table4 gain mean2.24pp and one tie.']),
        ('exec23_policy_reference', 'Exact authored two-period servicing policies and monetary values',
         policy, ['Natural, risk-style shift and odds tilt values are184/25,456/25,107/9 USD.',
                  'Full trajectory enumeration agrees with a separate moment calculation.'])]:
        code = Path(module.__file__)
        records.append(dict(integrated_citation_key=key, kind='project_evidence_not_scholarly_paper',
            title=title, author='Causal banking proposal project', year=2026,
            source_identity=str(code.relative_to(ROOT)), version_date='23 October 2026; exact authored reference',
            local_copy=ref(code, 'Executable exact authored construction'),
            inspected_anchors=[dict(anchor='calculate(): defined law and exact checks', inspected_text=code.read_text())],
            supported_claims=claims, limitations=['Stipulated mathematics or transcription; no native model/package or bank execution.']))
    write(BASE / 'source-audit.json', dict(sources=records, cutoff='2026-10-07',
        source_reviews=inputs, completion_review=ref(BASE / 'source-completion-review.json', 'Bounded author review')))
    write(BASE / 'exact-results.json', calculate())
    write(BASE / 'plan-review.json', dict(status='pass', issues=[],
        evidence=[ref(BASE / 'integration-plan.md', 'Reviewed integration and preservation plan')],
        findings=['Four additions develop existing chapter arguments; no separate supplement replaces integration.',
            'All prior sources, contexts and content inputs must survive.',
            'Each numerical result retains its assumptions and exact authored status.',
            'Only exact-reader author gates can renew; mandatory repairs and visual acceptance remain open.']))
    manuscript = [BASE / name for name in INSERTIONS.values()]
    write(BASE / 'mathematical-review.json', dict(status='pass_for_exact_authored_arguments', issues=[],
        evidence=[ref(p, 'Defined argument and assumptions') for p in manuscript] +
            [ref(BASE / 'exact-results.json', 'Reproduced arithmetic'),
             ref(Path(context.__file__), 'Twin laws and correctness partition'),
             ref(Path(policy.__file__), 'Trajectory and moment cross-check')],
        findings=['Twins compare fixed all-contact and no-contact policies, not the natural rule.',
            'Measuring U alone does not restore treatment overlap in A=U.',
            'Prediction partition yields2P(textwrong,visualcorrect)+P(bothwrong,disagree).',
            'Two-period probability maps change history probabilities and net policy values.',
            'No inferential coverage, causal knowledge attribution or native package outcome follows.'],
        empirical_calibration=False, native_execution=False))
    write(BASE / 'copyedit-review.json', dict(status='pass',
        evidence=[ref(p, 'Connected scholarly banking argument') for p in manuscript],
        findings=['Defined quantities, units, comparators and finite-law premises.',
            'Source/edition limits and unresolved conversions are stated beside claims.',
            'No controller or acquisition process is presented as product behavior.'], visual_acceptance=False))
    bib = []
    for s in records:
        author = s.get('author', s.get('authors'))
        assert isinstance(author, str)
        if s['kind'] == 'paper':
            author = author.replace(', ', ' and ')
        else:
            author = '{' + engine.shared.escape(author) + '}'
        identity = s['source_identity']
        note = (r'\url{' + identity + '}; ' if identity.startswith('https://') else engine.shared.escape(identity) + '; ')
        note += engine.shared.escape(s['version_date'])
        bib.append('@misc{' + s['integrated_citation_key'] + ',\n author={' + author + '},\n title={' +
            engine.shared.escape(s['title']) + '},\n year={' + str(s['year']) + '},\n note={' + note + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    entries = engine.sources()
    paths = [BASE / 'prepare-failure.json', BASE / 'source-schema-correction.json', BASE / 'prepare-correction.json', OLD, PRIOR, Path(__file__), ROOT / 'tools/build_network_commercial_reader_20261020.py'] + manuscript
    paths += [BASE / name for name in ['integration-plan.md', 'source-audit.json', 'source-completion-review.json',
        'plan-review.json', 'mathematical-review.json', 'copyedit-review.json', 'exact-results.json']]
    write(BASE / 'prepared-inputs.json', dict(inputs=[ref(p, 'Preserving reviewed input') for p in paths],
        generated=[ref(DRIVER, 'Preserving driver'), ref(BASE / 'refs.bib', 'Added audited citations')],
        prior_cited_records=len(read(PRIOR)['sources']), expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR / 'traceability-review.json')['scholarly_pdfs'] + 2,
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), records=len(entries), added=len(records))))


def build():
    configure()
    engine.build()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
