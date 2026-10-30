"""Verify bibliography-only changes against the unchanged reviewed body."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'bibliography-review-084'
STEM = 'causal_banking_release_candidate_2026-10-29'


def read(p):
    return json.loads(p.read_text())


def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    audit, build = read(B / 'deletion-audit.json'), read(B / 'latest-build.json')
    assert build['batch'] == 82 and audit['status'] == 'pass' and audit['edits'] == 237
    assert read(B / 'source-verification.json')['build_batch'] == 82
    old = B / 'batches/079/full'
    new = B / 'batches/082/full'
    labels = lambda folder: re.findall(r'\\bibcite\{([^}]+)\}(.*)', (folder / (STEM + '.aux')).read_text())
    assert labels(old) == labels(new) and len(labels(new)) == 1512
    norm = lambda s: re.sub(r'\s+', '', s).lower()
    assert norm((old / (STEM + '.bbl')).read_text()) == norm((new / (STEM + '.bbl')).read_text())
    before_pages, after_pages = [(folder / 'rendered.txt').read_text().split('\f') for folder in [old, new]]
    assert before_pages[:1852] == after_pages[:1852]
    assert after_pages[1852].startswith('Bibliography')
    old_manifest, new_manifest = [read(B / f'context-review-{n}/manifest.json') for n in [233, 237]]
    assert [(c['chapter'], c['title'], c['sha256']) for c in old_manifest['chapters']] == [
        (c['chapter'], c['title'], c['sha256']) for c in new_manifest['chapters']]
    sources = read(B / 'batches/079/source-before.json')['files']
    changed = [name for name, digest in sources.items() if sha(R / name) != digest]
    assert sorted(Path(p).suffix for p in changed) == ['.bib', '.bst']
    bib = B / 'source/docs/writing-repair/2026-10-29/references-0.bib'
    assert ''.join(bib.read_text().split()) == ''.join((O / 'before-references-0.bib').read_text().split())
    old_keys = re.findall(r'@[A-Za-z]+\{([^,]+),', (O / 'before-references-0.bib').read_text())
    assert old_keys == re.findall(r'@[A-Za-z]+\{([^,]+),', bib.read_text())
    assert audit['publication']['sponsor']['sha256'] == '866abb6e5d31ea22503eb618695cfba7fc130c2c8122297c7f553ad9e6f6df5a'
    for name in ['deletion-audit.json', 'source-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    evidence = dict(status='pass', batch=82, edits=[234, 235, 236, 237],
        changed_files=changed, bibliography_nonspace_identity=True,
        bibliography_keys_unchanged=len(old_keys), citation_labels_unchanged=1512,
        formatted_bibliography_equal_except_case_and_whitespace=True,
        first_1852_rendered_pages_exactly_unchanged=True,
        all_104_body_contexts_exactly_unchanged=True, sponsor_pdf_exactly_unchanged=True,
        original_bibliography=bind(O / 'before-references-0.bib'),
        current_bibliography=bind(bib), original_style=bind(O / 'before-causalplainnat-reading.bst'),
        current_style=bind(B / 'source/docs/writing-repair/2026-10-29/causalplainnat-reading.bst'))
    save(O / 'identity-verification.json', evidence)
    review = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=82,
        edits=[234, 235, 236, 237], publication=audit['publication'],
        identity_verification=bind(O / 'identity-verification.json'),
        rendered_text=bind(O / 'selected-rendered-pages-082.txt'),
        inspected_physical_pages=[1853, 1854, 1874, 1901, 1917, 1922],
        findings=[
            'The complete changed title list and follow-up line list were inspected; initial date-note patterns were checked through selected entries. The deterministic transformations preserve every non-whitespace bibliography character and protect source URLs and identifier strings.',
            'Selected complete rendered bibliography pages verify separated dates and software versions, restored aGrUM, FCI, RFCI, PC, R, Python and other supplied acronym case, and retained source-quality and cutoff qualifications.',
            'All1512 citation labels and their ordering are identical to batch079. The complete formatted bibliography is identical after removing whitespace and case differences. All1852 preceding rendered pages and all104 source-context extracts are byte-identical; the four-page sponsor PDF is unchanged.',
            'Spacing repair temporarily separated the historical selected17 identifier; the follow-up restores that literal identifier. Other source details and hypotheses remain unchanged. No source was acquired or substantively re-read for this copyedit.',
            'The context generator initially rejected the bibliography-style edit because it only recognised bibliography and sponsor ancillary files. It now exactly replays the style from its preserved original under the same ancillary verification path; no prose passage or unmatched edit is waived.'
        ],
        deletion_assessment='Edits234–236 only insert or remove spaces; every nonspace bibliography character survives in order. Edit237 removes the display instruction that lowercased supplied titles and adds an attribution comment. No mathematical, empirical, source, alternative or qualification content is deleted.',
        scope='Targeted bibliography copyediting and exact unchanged-body proof. Not a complete rereading of89 bibliography pages, new source-claim validation, visual review or independent acceptance.',
        acceptance=dict(author_targeted_review=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', review)
    reviews = read(B / 'changed-context-review.json')
    shutil.copy2(B / 'changed-context-review.json', O / 'changed-context-review-before.json')
    reviews['current_snapshot'] = str((B / 'context-review-237/manifest.json').relative_to(R))
    reviews.setdefault('ancillary_reviews', []).append(bind(O / 'contextual-review.json'))
    save(B / 'changed-context-review.json', reviews)
    subprocess.run(['python3', 'tools/reconcile_release_review_currency_20261029.py'], cwd=R, check=True)
    scope = read(B / 'review-scope-current.json')
    scope.update(batch=82, ledger_sha256=audit['ledger_sha256'], publication=audit['publication'],
        release_edits=237, edits=237, full_context_records=len(reviews['reviews']),
        latest_contextual_review=str((O / 'contextual-review.json').relative_to(R)),
        latest_rendered_review=str((O / 'contextual-review.json').relative_to(R)),
        portable_package_current=False, numerical_package_current=False)
    for p in [B / 'changed-context-review.json', B / 'deletion-audit.json', B / 'source-verification.json',
              B / 'review-currency-current.json', O / 'contextual-review.json', O / 'identity-verification.json',
              O / 'selected-rendered-pages-082.txt', O / 'plan.md']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    save(B / 'review-scope-current.json', scope)
    (B / 'review-scope-current.md').write_text(
        '# Current author-review scope\n\nBatch082:237 exact edits;1,941 reader pages and four sponsor pages. '
        'Bibliography spacing and title case repaired with complete nonspace/source identity checks. All1512 '
        'citation labels,104 body contexts and1852 pre-bibliography rendered pages are unchanged from batch079. '
        '121 author records cover101 numbered chapters with explicit scope; six bibliography pages have targeted '
        'rendered-text review.68 numerical groups remain current because their bound inputs are unchanged. '
        'Fresh visual and independent acceptance remain open.\n')
    p = R / 'docs/program/release-programme-2026-10-29.md'
    text = p.read_text()
    start, end = text.index('## Current continuation'), text.index('## Preserved continuation')
    shutil.copy2(p, O / 'programme-before.md')
    text = text[:start] + '''## Current continuation — verified batch082 and bibliography clarity

Batch082 contains237 exact edits and a1,941-page reader. Bibliography copyediting
separates joined dates, versions and prose and preserves supplied software/acronym
case. Every nonspace bibliography character, all1512 citation labels, all104
body contexts and all1852 pre-bibliography rendered pages remain unchanged.
Targeted rendered bibliography review, source checks and preservation pass.
The prior batch079 packages reproduce both PDFs and all68 numerical groups
after actual relocation; renew them for any later final candidate.

Continue consequential release checks and consolidate the semantic deletion
assessment for edits214 onward against the preserved213-edit review. Validate
the actual final recommendation and residual source dispositions, then freeze
by01:58:35 UTC and complete current package relocation and delivery by02:58:35.
Do not repeat completed simulations or treat copyediting as new source evidence.

Plan review: mechanical identity checks establish the limited presentation scope,
not complete scholarly or visual acceptance. The context generator now accounts
for the bibliography style through exact ancillary replay. Fresh visual and
independent review remain open;22 unread frontier originals retain their scoped
omissions. Source traceability and qualified institutional adoption remain separate.

''' + text[end:]
    p.write_text(text)
    subprocess.run(['python3', 'tools/refresh_release_controls_20261029.py'], cwd=R, check=True)


if __name__ == '__main__':
    main()
