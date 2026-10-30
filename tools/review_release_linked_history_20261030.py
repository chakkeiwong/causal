"""Renew the completed linked-history and navigation review for batch077."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'linked-history-review-081'


def read(p):
    return json.loads(p.read_text())


def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    audit, build, nums = [read(B / f) for f in
                          ['deletion-audit.json', 'latest-build.json', 'numerical-verification.json']]
    assert audit['status'] == 'pass' and audit['edits'] == 227 and build['batch'] == 77
    assert read(B / 'source-verification.json')['build_batch'] == 77
    assert nums['status'] == 'pass' and len(nums['checks']) == 67
    linked = nums['checks']['linked_history_evidence']
    assert linked['retained_requests'] == 4800 and linked['summary_cells'] == 24
    for name in ['deletion-audit.json', 'source-verification.json', 'numerical-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    manifest = read(B / 'context-review-227/manifest.json')
    reviews = read(B / 'changed-context-review.json')
    assert len(reviews['reviews']) == 114
    shutil.copy2(B / 'changed-context-review.json', O / 'changed-context-review-before.json')
    findings = [
        'Chapter94 source and complete batch077 rendered chapter text on physical1777–1782 were read, with the next chapter opening checked. The review does not claim complete rendered chapter95 or a fresh whole-book reading.',
        'Chapters92/93 retain their complete source/rendered review recorded for batch075. Six subsequent navigation replacements were read against their full source contexts and checked on batch077 physical1769–1770 and1774; the scientific content is unchanged.',
        'All4800 retained linked-history requests and24 summary cells independently reconstruct: interval endpoints, stratum averaging, variance, all-request coverage, exact Monte Carlo intervals, bias, dispersion, conditional finite widths, label accounts and paired comparisons.',
        'There are4793 narrower and7 wider linked-augmentation intervals than inverse weighting; the latter are wrong-inclusion requests. The exact-rank559/600 finding and false-exogeneity148/600, wrong-inclusion378/600 and noisy-label528/600 failures remain explicit.',
        'The additional audit-variance derivation distinguishes the shared latent score from fitted nuisance error. Its two stipulated examples demonstrate both variance orderings without attributing them to empirical bank evidence.',
        'The initial600-request schema failure is preserved. Count-set summaries are reaggregated here, not independently reprojected; no original generator or nuisance fit is rerun.180 planning-inequality cases and two exact augmentation examples pass.'
    ]
    contexts = []
    rendered = bind(O / 'funding-rendered-077.txt')
    for chapter in [92, 93, 94]:
        c = next(x for x in manifest['chapters'] if x['chapter'] == chapter)
        contexts.append(dict(chapter=chapter, extract=c['extract'], sha256=c['sha256']))
        scope = ('Complete source and complete batch077 rendered chapter94 text; author scope only.'
                 if chapter == 94 else
                 'Prior complete batch075 context plus all six subsequent navigation changes and batch077 changed-page renewal; author scope only.')
        reviews['reviews'].append(dict(chapter=chapter, title=c['title'], status='complete_in_author_scope',
            source_bindings=c['source_bindings'], extract=c['extract'], extract_sha256=c['sha256'],
            review_scope=scope, findings=findings, publication_batch=77,
            publication=audit['publication']['full'], rendered_text=rendered,
            predecessor_review=bind(B / 'projection-review-080/contextual-review.json') if chapter != 94 else None,
            fresh_visual_acceptance=False, independent_acceptance=False))
    reviews['current_snapshot'] = str((B / 'context-review-227/manifest.json').relative_to(R))
    save(B / 'changed-context-review.json', reviews)
    assert reviews['sponsor_review']['publication']['sha256'] == audit['publication']['sponsor']['sha256']
    review = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=77, edits=list(range(221, 228)),
        complete_source_contexts=contexts, rendered=[rendered], publication=audit['publication'],
        numerical_evidence=bind(O / 'verified-numerical-verification.json'), findings=findings,
        deletion_assessment='Edit221 retains its entire original anchor and adds explanation only. Edits222–227 remove V9/V10 and generic preserved-monograph drafting references, replacing each with the existing execution, pilot, covariance or precision chapter/section. The before/after meanings retain the same procedures, rate/exogeneity premises and disjoint seeds. No equation, data, adverse finding, alternative, citation or substantive qualification is removed.',
        scope='One complete chapter renewal and two prior-complete-context navigation renewals; retained-result reconstruction and post-build semantic deletion assessment. No fresh whole-book, visual or independent acceptance.',
        acceptance=dict(author_context=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', review)
    x = read(O / 'integration.json')
    x.update(status='verified_in_author_scope', batch=77, review=bind(O / 'contextual-review.json'))
    save(O / 'integration.json', x)
    subprocess.run(['python3', 'tools/reconcile_release_review_currency_20261029.py'], cwd=R, check=True)
    currency = read(B / 'review-currency-current.json')
    assert currency['status'] == 'pass' and currency['batch'] == 77
    scope = read(B / 'review-scope-current.json')
    scope.update(batch=77, ledger_sha256=audit['ledger_sha256'], publication=audit['publication'],
        release_edits=227, edits=227, full_context_records=len(reviews['reviews']), numerical_groups=67,
        latest_contextual_review=str((O / 'contextual-review.json').relative_to(R)),
        latest_rendered_review=str((O / 'contextual-review.json').relative_to(R)),
        portable_package_current=False, numerical_package_current=False,
        scope='117 author records cover101 numbered chapters through95 exact complete-context matches (including two introductions), seven exact-component chains, one chapter47 chain and one preamble. No fresh whole-book, visual or independent acceptance.')
    for p in [B / 'changed-context-review.json', B / 'deletion-audit.json', B / 'source-verification.json',
              B / 'numerical-verification.json', B / 'review-currency-current.json', B / 'mathematical-addition-reviews.json',
              O / 'contextual-review.json', O / 'funding-rendered-077.txt', O / 'numerical-evidence.json', O / 'source-scope.json']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    save(B / 'review-scope-current.json', scope)
    (B / 'review-scope-current.md').write_text(
        '# Current author-review scope\n\nBatch077:227 exact edits;1,941 reader pages and four sponsor pages. '
        'Chapter94 has complete source and rendered-text renewal; chapters92/93 retain complete prior review plus all six navigation changes. '
        'All4800 linked-history requests and24 summary cells reconstruct, preserving all adverse findings. '
        '67 numerical groups pass.117 author records cover101 numbered chapters through exact contexts and explicit chains. '
        'Fresh visual and independent acceptance remain open.\n')
    p = R / 'docs/program/release-programme-2026-10-29.md'
    s = p.read_text()
    start, end = s.index('## Current continuation'), s.index('## Preserved continuation')
    shutil.copy2(p, O / 'programme-before.md')
    replacement = '''## Current continuation — verified batch077 and linked-history precision

Batch077 contains227 exact edits and a1,941-page reader. The linked-history
chapter now explains when augmentation reduces audit variance and when it
increases it. Its4800 retained requests and24 summary cells reconstruct;
4793 narrower intervals and7 wider intervals remain descriptive findings.
Six drafting-version references now point to the exact reader arguments.
Post-build semantic review finds no loss of inherited scientific material.
67 numerical groups, source verification, preservation and review currency pass.

Next, independently reconstruct the five retained master-study summaries used
in the investment argument. Read their interpretation with the actual
coverage, finite availability, width, information and comparison denominators.
Do not regenerate experiments, alter qualification thresholds or replace the
protected historical state. Retain substantive counterexamples and failures.
At01:58:35 UTC stop new investigations, freeze the candidate, renew both
packages and actually relocate them. Complete final checks and explicit
residual dispositions for02:58:35 UTC delivery.

Plan review: a narrower interval need not be better calibrated, and additional
audit information has a distinct cost. Reaggregation checks the reported
evidence but does not independently validate every estimator or data law.
Final packaging must bind the exact mathematical, rendered-review and retained
numerical witnesses. Fresh visual, independent editorial and institutional
acceptance remain open;22 unread frontier originals retain their dispositions.

'''
    p.write_text(s[:start] + replacement + s[end:])
    subprocess.run(['python3', 'tools/refresh_release_controls_20261029.py'], cwd=R, check=True)


if __name__ == '__main__':
    main()
