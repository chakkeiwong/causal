"""Bind the observed semantic deletion review and its two preservation repairs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'preservation-review-076'


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
    assert audit['status'] == 'pass' and audit['edits'] == 213
    assert read(B / 'latest-build.json')['batch'] == 70
    assert read(B / 'source-verification.json')['build_batch'] == 70
    for name in ['deletion-audit.json', 'source-verification.json', 'numerical-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    ledger = read(B / 'edits.json')
    surface = read(O / 'change-surface.json')
    dispositions = []
    for row in surface:
        if not row['substantive_screen']:
            continue
        n = row['edit']
        outcome = 'Meaning retained or corrected in the stated surviving destination.'
        if n == 11:
            outcome = ('Repair required: the old correlation-implementation obligation was only '
                       'implicit in the revised native checks. Edit212 restores correlation-test '
                       'qualification explicitly beside graph mutation and orientation.')
        elif n == 186:
            outcome = ('Repair required: the surviving monetary conclusion retained the two '
                       'incompatible values, but did not explicitly repeat assignment evidence '
                       'and defensible structural restrictions. Edit213 restores both alternatives.')
        elif n in [180, 181]:
            outcome = ('Publication-count history removed from product prose; exact prior counts '
                       'remain in the ledger and assistance-prose-067/semantic-dispositions.json. '
                       'Current coverage, quarantine, scientific findings and limits survive.')
        elif n in [4, 9, 133, 134, 135, 136, 137]:
            outcome = 'Section hierarchy or study-role terminology changes; substantive treatment retained.'
        elif n == 184:
            outcome = 'Complete study inserted; the original transition survives at the end of the addition.'
        elif n == 203:
            outcome = 'Corrects invitation versus completion; q=1 never guarantees selective recovery.'
        elif n == 206:
            outcome = ('Removes authoring-status language while retaining bounded single treatment, '
                       'unresolved bank recovery, unbounded-longitudinal limitation and operating limits.')
        dispositions.append(dict(edit=n, file=row['file'], reason=row['reason'],
                                 surviving_destination=row['destination'], assessment=outcome))
    assert len(dispositions) == 80
    report = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=70,
        status='complete_in_author_scope_with_two_repairs', edits=213,
        basis=[bind(B / 'edits.json'), bind(O / 'change-surface.json'),
               bind(O / 'verified-deletion-audit.json'), bind(O / 'repair.json')],
        scope=('All211 earlier edits were screened. Eighty substantive-word removal candidates '
               'received contextual before/after assessment in the immediately preceding continuation '
               'and this continuation. This report consolidates those observed readings; it does not '
               'claim a new whole-book reading or an independent semantic certification.'),
        limitations=('Character-level removed substrings are a diagnostic, not lost-content totals. '
                     'Equation, numeric, label and citation retention cannot alone establish preservation. '
                     'Citation-only long-line rewrites150/151 preserve scientific prose under exact '
                     'reverse citation normalization. External editorial acceptance remains open.'),
        dispositions=dispositions,
        repaired_findings=[dict(prior_edit=11, repair_edit=212), dict(prior_edit=186, repair_edit=213)],
        final_observation=('The final rendered Java passage on physical302 explicitly names the '
                           'correlation test; the graph-to-effect conclusion on physical1304 explicitly '
                           'names assignment evidence and structural restrictions. Adjacent physical '
                           'pages301–303 and1303–1305 were read as text, not visually inspected.'),
        publication=audit['publication'],
        execution_observations=['Two text-extraction/read commands failed Python parsing before mutation; '
                                'raw-string transport corrected escaping and final extraction succeeded.'],
        acceptance=dict(author_semantic_review=True, fresh_visual=False, independent=False,
                        release_accepted=False))
    save(O / 'semantic-deletion-review.json', report)
    lines = ['# Post-build semantic deletion review', '',
        'Batch070 contains213 exact edits. The review found two qualifications that became less '
        'explicit during rewriting. Edits212 and213 restore them. Both repaired passages were '
        'read in the final compiled text; the exact replay and preservation audit passes.', '',
        report['scope'], '', report['limitations'], '',
        '| Earlier edit | Observed disposition | Surviving material |', '|---|---|---|']
    for row in dispositions:
        lines.append(f"| {row['edit']} | {row['assessment']} | {row['surviving_destination']} |")
    lines.extend(['', report['final_observation'], '',
                  'Fresh visual review and independent editorial acceptance remain open.'])
    (O / 'semantic-deletion-review.md').write_text('\n'.join(lines) + '\n')
    reviews = read(B / 'changed-context-review.json')
    manifest = read(B / 'context-review-213/manifest.json')
    receipts = []
    for chapter, names, rendered in [(35, [212], 'java-rendered.txt'),
                                      (69, [163, 168, 185, 186, 193, 195, 213], 'mechanisms-rendered.txt')]:
        context = next(x for x in manifest['chapters'] if x['chapter'] == chapter)
        if chapter == 35:
            previous = next(x for x in reviews['reviews'] if x['chapter'] == chapter)
            receipt = dict(chapter=35, complete_predecessor=dict(
                extract=previous['extract'], sha256=previous['extract_sha256']))
        else:
            prior = B / 'graph-software-072/component-renewal-069.json'
            receipt = read(prior)
            receipt['prior_component_review'] = bind(prior)
        receipt.update(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=70,
            source_context=dict(extract=context['extract'], sha256=context['sha256']),
            edit_numbers=names, reviewed_source_bindings=context['source_bindings'],
            rendered_text=bind(O / rendered), numerics=bind(O / 'verified-numerical-verification.json'),
            publication=audit['publication']['full'],
            findings=[report['final_observation'],
                      'The exact changed passage and surrounding argument were reread. No new '
                      'mathematics or result is added; previously reviewed components retain their '
                      'recorded scope. The cumulative ledger reconstructs the current complete context.'],
            scope='Preserved complete predecessor plus exact changed-passage renewal, not a fresh full-chapter reading.',
            acceptance=dict(author_component=True, fresh_visual=False, independent=False, release_accepted=False))
        p = O / f'component-renewal-{chapter:03d}.json'
        save(p, receipt)
        found = [i for i, x in enumerate(reviews['exact_component_renewals'])
                 if read(R / x['path'])['chapter'] == chapter]
        if found:
            assert len(found) == 1
            reviews['exact_component_renewals'][found[0]] = bind(p)
        else:
            reviews['exact_component_renewals'].append(bind(p))
        receipts.append(bind(p))
    reviews['current_snapshot'] = str((B / 'context-review-213/manifest.json').relative_to(R))
    save(B / 'changed-context-review.json', reviews)
    assert reviews['sponsor_review']['publication']['sha256'] == audit['publication']['sponsor']['sha256']
    contextual = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=70,
        edits=[212, 213], components=receipts, semantic_review=bind(O / 'semantic-deletion-review.json'),
        rendered=[bind(O / n) for n in ['java-rendered.txt', 'mechanisms-rendered.txt']],
        publication=audit['publication'], scope=report['scope'],
        acceptance=dict(author_component=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', contextual)
    subprocess.run(['python3', 'tools/reconcile_release_review_currency_20261029.py'], cwd=R, check=True)
    currency = read(B / 'review-currency-current.json')
    assert currency['status'] == 'pass'
    scope = read(B / 'review-scope-current.json')
    scope.update(batch=70, ledger_sha256=audit['ledger_sha256'], publication=audit['publication'],
        release_edits=213, edits=213, full_context_records=len(reviews['reviews']), numerical_groups=62,
        latest_contextual_review=str((O / 'contextual-review.json').relative_to(R)),
        latest_rendered_review=str((O / 'contextual-review.json').relative_to(R)),
        portable_package_current=False, numerical_package_current=False,
        scope='109 author records cover101 numbered chapters through95 exact complete-context matches '
              '(including two introductions), seven exact-component chains, one chapter47 chain and '
              'one preamble. This is not109 unique chapters or fresh whole-book/independent acceptance.')
    for p in [B / 'changed-context-review.json', B / 'deletion-audit.json', B / 'source-verification.json',
              B / 'numerical-verification.json', B / 'review-currency-current.json',
              O / 'contextual-review.json', O / 'semantic-deletion-review.json']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    save(B / 'review-scope-current.json', scope)
    (B / 'review-scope-current.md').write_text('# Current author-review scope\n\nBatch070:213 exact edits; '
        '1,940 reader pages and four sponsor pages. The post-build semantic review identifies two '
        'restored qualifications. Chapters35/69 have exact changed-passage renewals; all101 numbered '
        'chapters retain current author coverage through preserved contexts and explicit chains. '
        '62 numerical groups pass. Fresh visual and independent acceptance remain open.\n')
    p = R / 'docs/program/release-programme-2026-10-29.md'
    text = p.read_text(); start = text.index('## Current continuation'); end = text.index('## Preserved continuation', start)
    shutil.copy2(p, O / 'programme-before.md')
    replacement = '''## Current continuation — verified batch070 and semantic preservation

Batch070 contains213 exact edits and a1,940-page reader. The semantic deletion
review assessed80 substantive-word removal candidates and found two weakened
explicit qualifications: correlation-test qualification and the alternatives
of assignment evidence or defensible structural restrictions. Edits212/213
restore them. The compiled passages, post-build audit and current contextual
coverage all verify. Detailed dispositions are in preservation-review-076.

Next, finish the remaining targeted prose review, beginning with chapter89's
authoring-status conclusion. Preserve its institutional and scientific limits.
Review consequential source omissions only where a new admissible route could
change the recommendation. Reserve the final hour for current-package renewal,
actual relocation, final checks and explicit delivery of residual blockers.

Plan review: a mechanical preservation pass missed the loss of explicitness in
two important qualifications; contextual deletion review supplied the repair.
Do not equate retained equations or citation counts with semantic completeness.
No fresh whole-book, visual or independent acceptance is claimed. Final
integration starts01:58:35 UTC; delivery remains02:58:35 UTC on30October2026.

'''
    p.write_text(text[:start] + replacement + text[end:])
    subprocess.run(['python3', 'tools/refresh_release_controls_20261029.py'], cwd=R, check=True)
    print(json.dumps(dict(status='pass', batch=70, semantic_candidates=80, repairs=[212, 213])))


if __name__ == '__main__':
    main()
