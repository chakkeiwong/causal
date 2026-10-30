"""Bind the financial and investment contextual review to batch079."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'investment-review-083'


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
    assert audit['status'] == 'pass' and audit['edits'] == 233 and build['batch'] == 79
    assert read(B / 'source-verification.json')['build_batch'] == 79
    assert nums['status'] == 'pass' and len(nums['checks']) == 68
    for name in ['deletion-audit.json', 'source-verification.json', 'numerical-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    manifest = read(B / 'context-review-233/manifest.json')
    reviews = read(B / 'changed-context-review.json')
    assert len(reviews['reviews']) in [119, 121]
    if len(reviews['reviews']) == 119:
        shutil.copy2(B / 'changed-context-review.json', O / 'changed-context-review-before.json')
    else:
        shutil.copy2(B / 'review-currency-current.json', O / 'currency-superseded-component-failure.json')
    findings = [
        'Complete source chapters100/101 were read in the preceding continuation and completed here against their changed passages. Complete batch078 rendered chapters100/101 were read; after edits231–233 the complete batch079 rendered chapter101, physical1840–1852 (printed1834–1846), was read again. Bibliography opening was inspected but is not a complete bibliography review.',
        'Chapter100 distinguishes gross information value, its cost, analyst savings, added error loss, selective automation, retries, minimax regret, pilot option value and changing deployment mixture. All numerical examples remain explicitly stipulated. Existing financial_information_laws verifies these calculations, including the conditions under which advice or a pilot changes the decision.',
        'Chapter101 separates the initial minimal offer-study comparison from the broader shared-product construction account. The26.74 annual-study threshold, USD1.14m tranche included within USD4m, adoption ramp and unpriced participation remain conditional planning inputs, not current vendor prices or observed demand. Existing investment_account reconstructs the values.',
        'The stage-probability product now explicitly denotes expected planning volume for a fixed cohort. Conditional stage probabilities obey the chain rule; neither independent stages nor independent study outcomes are assumed. Failed-study costs remain included, and correlated outcomes can change dispersion without changing a correctly specified expectation.',
        'The three-workspace comparison remains intact but follows favourable evidence from the initial narrow comparison. Matched outputs, expertise, sources, data access, task order, correction costs, review quality, institutional variation and stop/narrow/defer alternatives remain.',
        'The energy study retains its benchmark correctness defect, missing measurement boundaries, synthetic power trace,900000 generated arrival batches and useful-answer denominator. Full workflow cost and waiting remain distinct. The experiment tests a consequential question, but funding now requires expected improvement in the investment decision to justify full cost.',
        'No new financial inputs, scholarly citations, original-source reading, simulator draws, sensor experiments, native qualification or bank evidence were introduced. The initial comparison still requires its own operational design and costing; this manuscript review does not authorize or claim an actual paid trial.'
    ]
    contexts = []
    for chapter in [100, 101]:
        c = next(x for x in manifest['chapters'] if x['chapter'] == chapter)
        rendered = bind(O / ('chapters100-101-rendered-078.txt' if chapter == 100 else 'chapter101-rendered-079.txt'))
        contexts.append(dict(chapter=chapter, extract=c['extract'], sha256=c['sha256']))
        record = dict(chapter=chapter, title=c['title'], status='complete_in_author_scope',
            source_bindings=c['source_bindings'], extract=c['extract'], extract_sha256=c['sha256'],
            review_scope=('Complete unchanged source chapter100 and batch078 rendered text; exact current-context match.' if chapter == 100 else 'Complete source chapter101 and complete batch079 rendered chapter text; author scope only.'),
            findings=findings, publication_batch=79, publication=audit['publication']['full'],
            rendered_text=rendered, rendered_batch=78 if chapter == 100 else 79,
            fresh_visual_acceptance=False, independent_acceptance=False)
        if not any(r['chapter'] == chapter and r.get('publication_batch') == 79 for r in reviews['reviews']):
            reviews['reviews'].append(record)
    active = []
    for item in reviews['exact_component_renewals']:
        prior = read(R / item['path'])
        if prior['chapter'] == 101:
            reviews.setdefault('superseded_component_renewals', []).append(dict(
                **item, superseded_by='Complete chapter101 author reading at batch079; historical evidence retained unchanged.'))
        else:
            active.append(item)
    reviews['exact_component_renewals'] = active
    reviews['current_snapshot'] = str((B / 'context-review-233/manifest.json').relative_to(R))
    save(B / 'changed-context-review.json', reviews)
    review = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=79, edits=[231, 232, 233],
        complete_source_contexts=contexts,
        rendered=[bind(O / 'chapters100-101-rendered-078.txt'), bind(O / 'chapter101-rendered-079.txt')],
        publication=audit['publication'], numerical_evidence=bind(O / 'verified-numerical-verification.json'),
        findings=findings,
        deletion_assessment=[
            dict(edit=231, disposition='Both original sentences remain verbatim. Added explanation changes no equation, input or cost category and corrects the interpretation of the expected planning volume.'),
            dict(edit=232, disposition='The phrase first tranche is replaced by subsequent construction tranche conditional on favourable initial evidence. All three workspaces and every matching, fairness, measurement and stopping requirement remain. No important programme scope is removed.'),
            dict(edit=233, disposition='The unsupported inference that a testable question makes an experiment worth funding is removed. The empirical question, full-attempt expenses, energy, waiting, useful-output definition and adverse findings remain. A value-of-information condition is added, consistent with the existing decision framework.')],
        verification_repair='The first currency check rejected the older chapter101 component chain because current files changed. Its immutable evidence is retained under superseded_component_renewals; the new complete source-context review replaces that chain as current coverage. No checker condition was weakened.',
        scope='Two complete author contexts with rendered-text scope stated separately. No fresh whole-book, visual, independent or bank acceptance.',
        acceptance=dict(author_context=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', review)
    x = read(O / 'integration.json')
    x.update(status='verified_in_author_scope', batch=79, review=bind(O / 'contextual-review.json'))
    save(O / 'integration.json', x)
    subprocess.run(['python3', 'tools/reconcile_release_review_currency_20261029.py'], cwd=R, check=True)
    currency = read(B / 'review-currency-current.json')
    assert currency['status'] == 'pass'
    scope = read(B / 'review-scope-current.json')
    scope.update(batch=79, ledger_sha256=audit['ledger_sha256'], publication=audit['publication'],
        release_edits=233, edits=233, full_context_records=len(reviews['reviews']), numerical_groups=68,
        latest_contextual_review=str((O / 'contextual-review.json').relative_to(R)),
        latest_rendered_review=str((O / 'contextual-review.json').relative_to(R)),
        portable_package_current=False, numerical_package_current=False,
        scope='121 author records cover101 numbered chapters through exact complete contexts and explicit component chains. Complete late-chapter financial and investment synthesis reviewed. No fresh whole-book, visual or independent acceptance.')
    for p in [B / 'changed-context-review.json', B / 'deletion-audit.json', B / 'source-verification.json',
              B / 'numerical-verification.json', B / 'review-currency-current.json', O / 'contextual-review.json',
              O / 'chapters100-101-rendered-078.txt', O / 'chapter101-rendered-079.txt', O / 'plan.md']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    save(B / 'review-scope-current.json', scope)
    (B / 'review-scope-current.md').write_text(
        '# Current author-review scope\n\nBatch079:233 exact edits;1,941 reader pages and four sponsor pages. '
        'Chapters100/101 have complete source review; chapter100 rendered text is unchanged from the read batch078, '
        'and chapter101 has complete batch079 rendered-text renewal. Three prose repairs clarify expected usable '
        'volume and conditional investment.68 numerical groups pass.121 author records cover101 numbered chapters '
        'through exact contexts and explicit chains. Fresh visual and independent acceptance remain open.\n')
    p = R / 'docs/program/release-programme-2026-10-29.md'
    s = p.read_text()
    start, end = s.index('## Current continuation'), s.index('## Preserved continuation')
    shutil.copy2(p, O / 'programme-before.md')
    replacement = '''## Current continuation — verified batch079 and investment synthesis

Batch079 contains233 exact edits and a1,941-page reader. The late-chapter
financial and investment argument has complete source-context review, with
the rendered-text scope recorded exactly. Three bounded prose repairs clarify
expected usable-study volume, the condition for a broader construction tranche,
and the distinction between a useful experiment and justified funding. All
equations, financial inputs, alternatives and adverse findings remain.
68 numerical groups, source verification, preservation and review currency pass.

Renew the portable candidate now to resolve any packaging defects while time
remains, including the new master-study helper and22528 retained requests.
Continue only consequential cross-chapter and publication checks after that
checkpoint. At01:58:35 UTC stop new investigations, freeze the final candidate,
renew any affected packages and actually relocate them. Complete final semantic
deletion review, residual dispositions and delivery by02:58:35 UTC.

Plan review: investment arithmetic is not observed bank value. The initial
comparison still needs its own detailed design and costing before expenditure.
Package replay must use its own declared inputs and reject missing evidence.
Fresh visual and independent acceptance remain open;22 unread frontier originals
retain their claim-specific dispositions. A verified candidate is deliverable
without converting these unresolved requirements into completed gates.

'''
    p.write_text(s[:start] + replacement + s[end:])
    subprocess.run(['python3', 'tools/refresh_release_controls_20261029.py'], cwd=R, check=True)


if __name__ == '__main__':
    main()
