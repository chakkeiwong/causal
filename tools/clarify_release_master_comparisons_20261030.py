"""Explain the critical-level contribution without changing frozen studies."""
from pathlib import Path
import hashlib
import json
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'master-study-review-082'


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 227
    evidence = json.loads((O / 'numerical-evidence.json').read_text())
    assert evidence['report']['retained_requests'] == 22528
    p = B / 'source/docs/writing-repair/2026-10-29/src/456bea026851b50a.tex'
    text = p.read_text()
    shutil.copy2(p, O / 'before-chapter095.tex')
    patches = [
        ('''False exogeneity, wrong inclusion and label errors fail visibly. Wider critical values cannot repair those population errors.''',
         r'''The coverage contrast also changes the critical value. As a retrospective
diagnostic, applying the primary method's 95\% Student critical value to its
saved baseline estimates gives 488 covers, compared with the inherited
method's 484. Applying a 99\% normal critical value to the inherited saved
estimates gives 506 covers, the same total as the registered primary interval.
The two procedures still have different estimates and variance constructions;
equal cover totals do not make their intervals equivalent. These calculations
use the same completed requests and do not qualify a revised procedure.
They show why the registered difference of 506 versus 484 cannot be credited
entirely to the change in information. The exact conditional-mean argument
establishes what the supplied randomization removes; the reported coverage
reflects that design, its estimator and its more conservative critical value.

False exogeneity, wrong inclusion and label errors fail visibly. Wider critical values cannot repair those population errors.''',
         'Separate the added-information mean argument from the confounded empirical coverage comparison.'),
        ('''A successor needs a justified stronger variance law, independent calendar information or enough pair/date/gold growth to control finite errors.''',
         r'''The paired coverage table changes both the variance formula and the
critical value. On the saved balanced requests, using a 99\% normal critical
value for the inherited double-counted variance also gives 508 covers. In
the persistent-calendar cell it gives 442, matching the adjusted method's
total while preserving the calibration failure. At a common 95\% level the
adjusted calculation covers 377 persistent requests and the inherited one
379. Subtracting the duplicated interaction corrects the variance account
under the stated law, but these observations do not show that the correction
caused the larger coverage counts in the table. They are retrospective
comparisons of the retained estimates, with no new draws or qualification.

A successor needs a justified stronger variance law, independent calendar information or enough pair/date/gold growth to control finite errors.''',
         'Explain why correcting double counting and increasing a critical value have different inferential roles.'),
        ('''Direct weighting has no filter or optimizer approximation.''',
         r'''Here the comparison isolates the price of a more conservative critical
value: both columns use exactly the same estimate and standard error on
each available request. At baseline the wider interval covers 508 rather
than 483 targets, with median width about USD 735 rather than USD 559.
The additional coverage therefore demonstrates the reported width--coverage
tradeoff, not a gain from a different estimator or a richer information set.
Truthful logger probabilities and audited states justify the weighting
identity itself. Their institutional cost and credibility must be evaluated
separately from a choice between these two critical levels.

Direct weighting has no filter or optimizer approximation.''',
         'Interpret the same-estimator servicing comparison as a critical-value tradeoff.')
    ]
    for before, after, reason in patches:
        assert text.count(before) == 1
        text = text.replace(before, after, 1)
        ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
            reason=reason,
            substantive_destination='The complete original anchor, all tables, equations, assumptions, adverse cases and conclusions remain. Added prose explains independently reconstructed retrospective comparisons and explicitly denies new qualification.'))
    p.write_text(text)
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    record = dict(status='written_pending_build_review', edits=[228, 229, 230],
        support_class='PROJECT_DERIVATION_AND_RETAINED_SYNTHETIC_EVIDENCE',
        witness=dict(path=str((O / 'numerical-evidence.json').relative_to(R)),
                     sha256=hashlib.sha256((O / 'numerical-evidence.json').read_bytes()).hexdigest()),
        new_citations=False, new_draws=False, new_qualification=False,
        deleted_scientific_material='none; all three original anchors remain verbatim',
        caveat='Changing nominal levels on the retained requests is a retrospective diagnostic; equal coverage counts do not imply equal intervals or isolate every information/estimator difference.')
    (O / 'integration.json').write_text(json.dumps(record, indent=2) + '\n')
    print('Added edits228–230: fair interpretation of master-study comparisons.')


if __name__ == '__main__':
    main()
