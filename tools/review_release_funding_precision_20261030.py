"""Bind the completed funding/precision review to batch073."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'funding-review-079'


def read(p):
    return json.loads(p.read_text())


def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    audit = read(B / 'deletion-audit.json')
    build = read(B / 'latest-build.json')
    nums = read(B / 'numerical-verification.json')
    assert audit['status'] == 'pass' and audit['edits'] == 217
    assert build['batch'] == 73
    assert read(B / 'source-verification.json')['build_batch'] == 73
    assert nums['status'] == 'pass' and len(nums['checks']) == 65
    assert {'funding_followup_evidence', 'precision_design_evidence'} <= set(nums['checks'])
    for name in ['deletion-audit.json', 'source-verification.json', 'numerical-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    manifest = read(B / 'context-review-217/manifest.json')
    reviews = read(B / 'changed-context-review.json')
    assert len(reviews['reviews']) == 110
    shutil.copy2(B / 'changed-context-review.json', O / 'changed-context-review-before.json')
    rendered = bind(O / 'funding-precision-rendered.txt')
    common = [
        'Complete assembled chapter90 and chapter91 source contexts were read in the current review. The batch073 rendered text on physical1757–1767, and the next chapter opening1768, was read across the continuation checkpoint. This is text inspection, not fresh visual inspection.',
        'Independent retained-data reconstruction passes for126 funding summary cells, all request denominators, conditional shifts, paired gains and four complete-workload comparisons. The later precision comparison reconstructs16000 retained requests,24 marginal cells,24 paired comparisons and four complete-workload comparisons.',
        'No sample, estimator, audit count, simulation draw or adverse result changes. No new empirical experiment or bank qualification is claimed.'
    ]
    findings = {
        90: common + [
            'The fixed-pilot estimand shift and nuisance-rate condition remain explicit. Additional pilot rows require independent relevant history under the stated invariant law; streaming changes the storage of the implemented procedure.',
            'The approximate616-currency-unit conditional shift reconstructs as615.4837275; the text uses approximate precision. The weak-audit127 available requests and121 covers retain the600-request denominator.',
            'Edit217 removes an author-success contrast and retains each institutional evidence requirement: assignment, clocks, audit truth, invariant pilot, precision, interface, platform and matched workflow costs.'
        ],
        91: common + [
            'Edit216 corrects a substantive interpretation: for1880 covers in2000 requests the Wilson upper endpoint is.9495888029, whereas exact binomial inversion ends at.9500067612. Only the Wilson interval excludes.95; ordinary exact and adjusted exact intervals include it.',
            'The small-audit exact simultaneous upper endpoints remain below.95, as does the persistent joint-regression endpoint. Near-rank unavailability and false-exogeneity failures remain. Conservative paired bounds and exact conditional tests are distinguished, including positive uncertainty for zero observed discordance.',
            'Pilot QR norm identities, centered block-moment combination, tie/gap qualification and all-request versus available-request quantities remain explicit. Memory gains do not imply a consistent speed advantage, useful financial width or institutional acceptance.'
        ]
    }
    contexts = []
    for chapter in [90, 91]:
        c = next(x for x in manifest['chapters'] if x['chapter'] == chapter)
        contexts.append(dict(chapter=chapter, extract=c['extract'], sha256=c['sha256']))
        reviews['reviews'].append(dict(
            chapter=chapter, title=c['title'], status='complete_in_author_scope',
            source_bindings=c['source_bindings'], extract=c['extract'], extract_sha256=c['sha256'],
            review_scope='Complete source and complete batch073 rendered chapter-text reading; author scope only.',
            findings=findings[chapter], publication_batch=73, publication=audit['publication']['full'],
            rendered_text=rendered, fresh_visual_acceptance=False, independent_acceptance=False))
    reviews['current_snapshot'] = str((B / 'context-review-217/manifest.json').relative_to(R))
    save(B / 'changed-context-review.json', reviews)
    assert reviews['sponsor_review']['publication']['sha256'] == audit['publication']['sponsor']['sha256']
    review = dict(
        recorded_utc=datetime.now(timezone.utc).isoformat(), batch=73, edits=[216, 217],
        complete_source_contexts=contexts, rendered=[rendered],
        numerical_evidence=bind(O / 'verified-numerical-verification.json'),
        publication=audit['publication'], findings=findings,
        deletion_assessment='Edit216 replaces an incorrect exclusion claim with the exact Wilson/exact distinction; all counts and adverse adjusted findings survive. Edit217 preserves the full institutional requirements in the preceding context and their distinction from local calculations. No substantive assumption, equation, alternative or adverse observation is removed.',
        verification_repairs='Initial checker failures and corrected attempts are retained in check-run.txt, precision-check-run.txt and subsequent logs: approximate rounding was overstrict; result-key names and explicitly documented dense/streaming diagnostics required correct comparison. The repaired independent checks pass.',
        scope='Two renewed complete author contexts, retained-result reconstruction and post-build semantic assessment; no fresh whole-book, visual or independent acceptance.',
        acceptance=dict(author_context=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', review)
    integration = read(O / 'integration.json')
    integration.update(status='verified_in_author_scope', batch=73, review=bind(O / 'contextual-review.json'))
    save(O / 'integration.json', integration)
    subprocess.run(['python3', 'tools/reconcile_release_review_currency_20261029.py'], cwd=R, check=True)
    currency = read(B / 'review-currency-current.json')
    assert currency['status'] == 'pass' and currency['batch'] == 73
    scope = read(B / 'review-scope-current.json')
    scope.update(batch=73, ledger_sha256=audit['ledger_sha256'], publication=audit['publication'],
                 release_edits=217, edits=217, full_context_records=len(reviews['reviews']), numerical_groups=65,
                 latest_contextual_review=str((O / 'contextual-review.json').relative_to(R)),
                 latest_rendered_review=str((O / 'contextual-review.json').relative_to(R)),
                 portable_package_current=False, numerical_package_current=False,
                 scope='112 author records cover101 numbered chapters through95 exact complete-context matches (including two introductions), seven exact-component chains, one chapter47 chain and one preamble. No fresh whole-book, visual or independent acceptance.')
    for p in [B / 'changed-context-review.json', B / 'deletion-audit.json', B / 'source-verification.json',
              B / 'numerical-verification.json', B / 'review-currency-current.json', O / 'contextual-review.json',
              O / 'funding-precision-rendered.txt', O / 'numerical-evidence.json', O / 'precision-evidence.json']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    save(B / 'review-scope-current.json', scope)
    (B / 'review-scope-current.md').write_text(
        '# Current author-review scope\n\nBatch073:217 exact edits;1,940 reader pages and four sponsor pages. '
        'Chapters90/91 have complete source and rendered-text renewal. The Wilson/exact interpretation is corrected; '
        'all observations, procedures and adverse findings survive.65 numerical groups pass.112 author records cover '
        '101 numbered chapters through exact contexts and explicit chains. Fresh visual and independent acceptance remain open.\n')
    p = R / 'docs/program/release-programme-2026-10-29.md'
    s = p.read_text()
    start, end = s.index('## Current continuation'), s.index('## Preserved continuation')
    shutil.copy2(p, O / 'programme-before.md')
    replacement = '''## Current continuation — verified batch073 and precision interpretation

Batch073 contains217 exact edits and a1,940-page reader. Chapters90/91 now have
complete source and rendered-text renewal. Independent reconstruction exposes
and repairs a Wilson-versus-exact interpretation error without changing any
draw, procedure or adverse adjusted finding.126 funding summary cells and16000
precision requests reconstruct;65 numerical groups pass. Source traceability,
post-build preservation and current review coverage pass.

Continue consequential projection and investment reasoning checks, including
availability, finite-width summaries, economic assumptions and serious
alternatives. Retain the semantic deletion assessment and its restored
qualifications. At01:58:35 UTC stop new investigations, freeze the candidate,
renew both packages and actually relocate them. Complete the final checks and
explicit residual dispositions for02:58:35 UTC delivery.

Plan review: exact reconstruction can overturn prose even when tables and
earlier review records pass. Statistical significance is not economic value;
unavailability and infinite sets must remain in the declared denominators.
No fresh visual, independent editorial or institutional acceptance is claimed.
The22 unread frontier originals retain bounded claim-level dispositions.

'''
    p.write_text(s[:start] + replacement + s[end:])
    subprocess.run(['python3', 'tools/refresh_release_controls_20261029.py'], cwd=R, check=True)


if __name__ == '__main__':
    main()
