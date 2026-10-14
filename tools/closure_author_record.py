#!/usr/bin/env python3
"""Bind the already written author judgment; this does not perform a review."""
from closure_delivery import ROOT, digest, read, REVIEW
import json

NARRATIVE = 'docs/reviews/gap-closure-author-review-2026-10-10.md'
REMAINING = {
    'G1': 'Adverse regular calibration remains; correct reporting is not a statistical repair.',
    'G2': 'D01: old singular mean restrictions remain uninformative; broader calibration and rigorous numerical enclosure remain open.',
    'G3': 'D02: general nonlinear identification, full belief-policy optimization, uniform calibration and global numerical certification remain open.',
    'G4': 'D03: useful general PAG confidence and dependent-history extensions require new arguments and information.',
    'G5': 'D04/D05: unknown audit or semantic errors, endogenous/many-to-many maps and shared calendar shocks remain unsupported.',
    'G6': 'D06/D07/D08: arbitrary learners, general out-of-core fitting, multi-host service levels, independent and bank acceptance and measured savings remain open.'}


def main():
    gaps = {}
    for line in (ROOT / NARRATIVE).read_text().splitlines():
        if not line.startswith('| G'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        key = cells[0].split(':')[0]
        if key in REMAINING:
            gaps[key] = dict(scholarly=cells[1], capability=cells[2], remaining=REMAINING[key])
    assert set(gaps) == set(REMAINING)
    inputs = [NARRATIVE,
              'docs/program/gap-closure-plan-2026-10-10.md',
              'docs/program/gap-closure-execution-2026-10-10.md',
              'docs/program/closure-scientific-specification.md',
              'docs/program/deferred-gaps-2026-10-10.md',
              'docs/reviews/gap-closure-plan-review-2026-10-10.md',
              'docs/reviews/closure-pilot-review.md',
              'docs/reviews/closure-execution-failures.md',
              'docs/reviews/remaining-gaps-v7-2026-10-10.md',
              'docs/reviews/closure-verification.json',
              'docs/reviews/foundations-audit.json',
              'docs/reviews/reconstruction-build.json',
              'docs/reviews/foundations-render-receipt.json',
              'docs/reviews/reconstruction-visual-inspection.json',
              'docs/reviews/reconstruction-visual-inspection.md',
              'docs/reviews/reference-gap-review.md',
              'tools/closure_author_record.py', 'tools/closure_delivery.py']
    inputs += ['docs/reviews/v5-gap-assessment-excerpts/' + name + '.txt'
               for name in ('finmarketing-uplift', 'bayesfilter-score', 'cip-method-choice')]
    inputs += list(read('docs/reviews/closure-verification.json')['input_sha256'])
    for pattern in ('docs/reconstruction/*.tex', 'docs/*.tex', 'docs/*.bib'):
        inputs += [str(p.relative_to(ROOT)) for p in ROOT.glob(pattern)]
    audit = read('docs/reviews/foundations-audit.json')
    assert audit['status'] == 'pass'
    inputs += [d['path'] for d in audit['documents']]
    result = dict(
        status='author_reviewed_with_stated_limits', date='2026-10-10', revision='7.0',
        review=NARRATIVE, blocking_findings=[], gap_dispositions=gaps,
        final_documents=audit['documents'],
        scope='Substantive author judgment of the executed bounded program with separate capability limits. Not independent scientific acceptance, bank validation, deployment or adopted integration.',
        input_sha256={p: digest(p) for p in sorted(set(inputs))})
    (ROOT / REVIEW).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Bound six separate gap dispositions and', len(result['input_sha256']), 'review inputs.')


if __name__ == '__main__':
    main()
