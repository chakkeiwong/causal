"""Record the completed chapter97–99 source/rendered review for batch083."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'qualification-review-086'


def read(p):
    return json.loads(p.read_text())


def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    a, build = read(B / 'deletion-audit.json'), read(B / 'latest-build.json')
    assert a['status'] == 'pass' and a['edits'] == 239 and build['batch'] == 83
    assert read(B / 'source-verification.json')['build_batch'] == 83
    manifest = read(B / 'context-review-239/manifest.json')
    old_pages = (B / 'batches/082/full/rendered.txt').read_text().split('\f')
    new_pages = (B / 'batches/083/full/rendered.txt').read_text().split('\f')
    assert len(old_pages) == len(new_pages)
    changed_pages = [i+1 for i, (x, y) in enumerate(zip(old_pages, new_pages)) if x != y]
    assert changed_pages == [1806, 1811, 1812]
    old_manifest = read(B / 'context-review-237/manifest.json')
    for n in [97, 99]:
        old = next(c for c in old_manifest['chapters'] if c['chapter'] == n)
        current = next(c for c in manifest['chapters'] if c['chapter'] == n)
        assert old['sha256'] == current['sha256']
    for name in ['deletion-audit.json', 'source-verification.json', 'numerical-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    findings = [
        'Complete source chapters97/98 were read in the preceding continuation; chapter99 source was completed in this continuation. Complete batch082 rendered chapters97–99 were read, including the Part X transition. After edits238/239, complete batch083 rendered chapter98 was reread. Only physical pages1806,1811,1812 changed; all other rendered pages and the sponsor are identical.',
        'Chapter97 conditions its finite table on sufficient history, complete-history cohort independence, action and retention positivity, independent evaluation and bounded rewards. The target is the value of the realized training-selected policy; it is neither the unknown optimal policy nor the mean across training samples. Prefix weights, joint probability-error accounting, negative hidden-state/missingness worlds, rare-cell problems and the unusably wide illustrative bound remain explicit.',
        'Chapter98 proves coverage at the true continuous scalar lag and retains it through union, without treating every wrong-lag residual as independent. The covariance enclosure and ratio projection retain disconnected, whole-line and empty outcomes. The direct-intervention route has independent Gaussian episodes, invariant effect and equal variances. The supplied-summary halfwidth calculation is not prospective power. Raw availability and exact lower-bound coverage criteria remain distinct.',
        'Chapter99 states the independent pilot and bounded known finite-dependence law; instrument–outcome and instrument–action nuisance products enter separately. The sparse route requires an actual cone/numerical certificate and population transfer, while calibration needs independent data and justified noise information. Whole-line fallback and the all-request denominator preserve the claimed scope without implying selected conditional coverage or useful width.',
        'The nonlinear Gaussian failure remains outside the bounded approximation theorem. The 7,344,273-row centered planning bound and noise-floor calculation explain economically unattractive precision without recommending those bank sample sizes. Geometric symmetries, hierarchical weighting and altered stabilized functionals remain substantive alternatives with their original source-specific limits.',
        'Eleven supporting citations in chapter98 had bare textual author rendering in non-grammatical positions. Edits238/239 change only cite to citep. All keys, words, equations, values, assumptions, adverse findings and next-experiment conditions remain in order. No new mathematical defect was established by this pass.',
        'Existing qualification_design_laws and associated retained exact inputs cover the relevant arithmetic; no new numerical input, primary-source reading, simulation, native qualification or bank result was introduced. This author reading is not independent scientific review or fresh visual acceptance.'
    ]
    reviews = read(B / 'changed-context-review.json')
    assert len(reviews['reviews']) == 121
    shutil.copy2(B / 'changed-context-review.json', O / 'changed-context-review-before.json')
    contexts, rendered = [], []
    for n, pages in [(97, [1799,1805]), (98, [1806,1812]), (99, [1813,1827])]:
        c = next(c for c in manifest['chapters'] if c['chapter'] == n)
        rb = 83 if n == 98 else 82
        rp = O / f'chapter{n}-rendered-{rb:03d}.txt'
        contexts.append(dict(chapter=n, extract=c['extract'], sha256=c['sha256']))
        rendered.append(dict(**bind(rp), physical_pages=pages, batch=rb))
        reviews['reviews'].append(dict(chapter=n, title=c['title'], status='complete_in_author_scope',
            source_bindings=c['source_bindings'], extract=c['extract'], extract_sha256=c['sha256'],
            review_scope='Complete source context and complete rendered chapter; for unchanged97/99 exact rendered-page identity carries batch082 reading to083. Chapter99 includes Part X transition.',
            findings=findings, publication_batch=83, publication=a['publication']['full'],
            rendered_text=bind(rp), rendered_batch=rb, fresh_visual_acceptance=False, independent_acceptance=False))
    reviews['current_snapshot'] = str((B / 'context-review-239/manifest.json').relative_to(R))
    save(B / 'changed-context-review.json', reviews)
    record = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=83, edits=[238,239],
        complete_source_contexts=contexts, rendered=rendered, changed_physical_pages=changed_pages,
        publication=a['publication'], numerical_evidence=bind(O / 'verified-numerical-verification.json'),
        findings=findings,
        deletion_assessment=[dict(edit=i, disposition='Citation command only: all content and citation keys remain in the same order; no substantive deletion.') for i in [238,239]],
        scope='Complete chapter97–99 author context and rendered-text review with exact unchanged-page transfer. No fresh whole-book, visual, primary-source or independent acceptance.',
        acceptance=dict(author_context=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', record)
    integration = read(O / 'integration.json')
    integration.update(status='verified_in_author_scope', batch=83, review=bind(O / 'contextual-review.json'))
    save(O / 'integration.json', integration)
    subprocess.run(['python3', 'tools/reconcile_release_review_currency_20261029.py'], cwd=R, check=True)
    scope = read(B / 'review-scope-current.json')
    scope.update(batch=83, ledger_sha256=a['ledger_sha256'], publication=a['publication'],
        release_edits=239, edits=239, full_context_records=124,
        latest_contextual_review=str((O / 'contextual-review.json').relative_to(R)),
        latest_rendered_review=str((O / 'contextual-review.json').relative_to(R)),
        portable_package_current=False, numerical_package_current=False,
        scope='124 author records cover101 numbered chapters through complete contexts and explicit component chains; late finite-qualification chapters97–99 renewed. No fresh whole-book, visual or independent acceptance.')
    for p in [B / 'changed-context-review.json', B / 'deletion-audit.json', B / 'source-verification.json',
              B / 'review-currency-current.json', O / 'contextual-review.json', O / 'plan.md'] + [R / x['path'] for x in rendered]:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    save(B / 'review-scope-current.json', scope)
    (B / 'review-scope-current.md').write_text('# Current author-review scope\n\nBatch083:239 exact edits;1,941 reader pages and four sponsor pages.124 author records cover101 numbered chapters. Chapters97–99 have complete source and rendered-text review; eleven chapter98 citations now render parenthetically. All mathematical and financial content remains. Fresh visual and independent acceptance remain open.\n')
    print(json.dumps(dict(status='complete_in_author_scope', batch=83, records=124, changed_pages=changed_pages)))


if __name__ == '__main__':
    main()
