"""Bind citation-only renewal to exact prior author contexts and final output."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'citation-review-087'


def read(p):
    return json.loads(p.read_text())


def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    edits, audit, build = [read(B / f) for f in ['edits.json','deletion-audit.json','latest-build.json']]
    assert len(edits) == 283 and audit['status'] == 'pass' and build['batch'] == 84
    assert read(B / 'source-verification.json')['build_batch'] == 84
    nums = read(B / 'numerical-verification.json')
    assert nums['status'] == 'pass' and len(nums['checks']) == 68
    for name in ['deletion-audit.json','source-verification.json','numerical-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    for e in edits[239:]:
        assert e['after'] == e['before'].replace(r'\cite{', r'\citep{')
    bbl_old = next((B / 'batches/083/full').glob('*.bbl'))
    bbl_new = next((B / 'batches/084/full').glob('*.bbl'))
    assert sha(bbl_old) == sha(bbl_new)
    old_pub = read(O / 'review-currency-before.json')['publication']
    assert old_pub['sponsor']['sha256'] == audit['publication']['sponsor']['sha256']
    locations = read(O / 'rendered-citation-locations.json')
    assert len(locations) == 415 and all('physical_page' in x for x in locations)
    # Correct one manually located snippet whose short anchor also occurred
    # earlier on the same page; the complete relevant paragraph was read.
    for row in locations:
        if row['file'].endswith('5b2599cb1b9953cc.tex') and row['occurrence'] == 4:
            pages = (B / 'batches/084/full/rendered.txt').read_text().split('\f')
            p = pages[1345]
            start = p.index('The inspected identification suggester')
            row['rendered_excerpt_raw'] = p[start:start+650]
            row['manual_anchor'] = 'The inspected identification suggester'
    save(O / 'rendered-citation-locations.json', locations)
    rendered_path = O / 'rendered-citations-reviewed.txt'
    rendered_path.write_text('\n\n'.join(f'{i+1}. Chapter{x["chapter"]}; physical{x["physical_page"]}\n{x["rendered_excerpt_raw"]}' for i,x in enumerate(locations)) + '\n')
    manifest = read(B / 'context-review-283/manifest.json')
    prior_manifest = read(B / 'context-review-239/manifest.json')
    reviews = read(O / 'changed-context-review-before.json')
    integration = read(O / 'integration.json')
    chapters = integration['chapters']
    prior_renewals = {}
    active = []
    for item in reviews['exact_component_renewals']:
        receipt = read(R / item['path'])
        if receipt['chapter'] in chapters:
            prior_renewals[receipt['chapter']] = (item, receipt)
            reviews.setdefault('superseded_component_renewals', []).append(dict(**item,
                superseded_by='Cumulative exact citation-only renewal for batch084; prior immutable receipt retained.'))
        else:
            active.append(item)
    receipts = []
    for chapter in chapters:
        c = next(c for c in manifest['chapters'] if c['chapter'] == chapter)
        oldc = next(c for c in prior_manifest['chapters'] if c['chapter'] == chapter)
        new_indices = [x['edit'] for x in integration['changes'] if x['chapter'] == chapter]
        if chapter in prior_renewals:
            item, prev = prior_renewals[chapter]
            old = prev['complete_predecessor']
            indices = prev['edit_numbers'] + new_indices
            assert prev['source_context']['sha256'] == oldc['sha256']
            prior_evidence = item
        else:
            matches = [r for r in reviews['reviews'] if r['chapter'] == chapter and r['extract_sha256'] == oldc['sha256']]
            assert len(matches) == 1
            old = dict(extract=matches[0]['extract'], sha256=matches[0]['extract_sha256'])
            indices = new_indices
            prior_evidence = None
        text = (R / old['extract']).read_text()
        for i in indices:
            e = edits[i-1]
            assert text.count(e['before']) == 1, (chapter,i)
            text = text.replace(e['before'],e['after'],1)
        current_text = (R / c['extract']).read_text()
        marker_pattern = r'^% SOURCE (.+) CHAR (\d+)$'
        old_markers = re.findall(marker_pattern, text, flags=re.M)
        new_markers = re.findall(marker_pattern, current_text, flags=re.M)
        assert len(old_markers) == len(new_markers)
        marker_updates = []
        for (old_file,old_offset),(new_file,new_offset) in zip(old_markers,new_markers):
            assert old_file == new_file
            if old_offset != new_offset:
                assert any(s['file']==new_file and s['start']==int(new_offset) for s in c['segments'])
                before = f'% SOURCE {old_file} CHAR {old_offset}'
                after = f'% SOURCE {new_file} CHAR {new_offset}'
                assert text.count(before+'\n') == 1
                text = text.replace(before+'\n',after+'\n',1)
                marker_updates.append(dict(before=before,after=after,
                    reason='Generated source-position metadata shifts when prior citation-command length grows; exact manuscript body is unchanged.'))
        assert text == current_text, chapter
        record = dict(chapter=chapter, recorded_utc=datetime.now(timezone.utc).isoformat(), batch=84,
            complete_predecessor=old, source_context=dict(extract=c['extract'],sha256=c['sha256']),
            edit_numbers=indices, citation_only_edit_numbers=new_indices, source_marker_updates=marker_updates,
            predecessor_component_receipt=prior_evidence, reviewed_source_bindings=c['source_bindings'],
            rendered_text=bind(rendered_path), numerics=bind(O/'verified-numerical-verification.json'),
            publication=audit['publication']['full'],
            findings=['All changed citation commands and adjacent source prose were read; selected rendered snippets at every changed occurrence were inspected. Exact cumulative replay proves every other context character unchanged. Existing complete-context and component reviews retain their original scope.',
                      'The command renders supporting author/year attribution parenthetically. No mathematical, numerical, scientific, citation-key or label content changes. Bibliography bytes and sponsor remain identical.'],
            scope='Preserved complete author context plus exact component renewals and citation-only inspection; not a new full-chapter or primary-source reading.',
            acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
        rp = O / f'component-renewal-{chapter:03d}.json'
        save(rp,record)
        receipts.append(bind(rp))
        active.append(bind(rp))
    reviews['exact_component_renewals'] = active
    reviews['current_snapshot'] = str((B / 'context-review-283/manifest.json').relative_to(R))
    save(B / 'changed-context-review.json', reviews)
    report = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=84,
        edits=list(range(240,284)), commands=415, changed_files=43, chapters=chapters,
        publication=audit['publication'], contextual_chains=receipts,
        rendered_text=bind(rendered_path), numerics=bind(O/'verified-numerical-verification.json'),
        inspected_rendered_occurrences=415, inspected_rendered_pages=len({x['physical_page'] for x in locations}),
        bibliography_byte_identical=True, sponsor_byte_identical=True,
        findings=['Every bare supporting cite occurrence in the actual compiled input tree was inspected and converted to citep. Existing citet/citep commands were not globally redefined.',
                  'All415 source-adjacent snippets and corresponding rendered citations were inspected. Full22-chapter rereading and fresh visual inspection are not claimed.',
                  'The first write stopped on chapter35 nested-input segmentation. All39 saved source files were restored exactly before repair; the corrected routine prevalidated all44 unique segment/file replacements before writing. The failed attempt is retained.',
                  'Build, source traceability,68-group numerical reconstruction and exact preservation pass; current full bibliography and all citation labels remain byte-identical.'],
        deletion_assessment=[dict(edit=i,disposition='Only citation-command spelling changes from cite to citep. Every substantive character and citation key is preserved in order.') for i in range(240,284)],
        scope='Source-adjacent and rendered-citation author inspection chained to preserved complete contexts. No fresh whole-book, original-source, visual or independent acceptance.',
        acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
    save(O/'contextual-review.json',report)
    integration.update(status='verified_in_author_scope',batch=84,review=bind(O/'contextual-review.json'))
    save(O/'integration.json',integration)
    subprocess.run(['python3','tools/reconcile_release_review_currency_20261029.py'],cwd=R,check=True)
    scope = read(B/'review-scope-current.json')
    scope.update(batch=84,ledger_sha256=audit['ledger_sha256'],publication=audit['publication'],
        release_edits=283,edits=283,full_context_records=124,
        latest_contextual_review=str((O/'contextual-review.json').relative_to(R)),
        latest_rendered_review=str((O/'contextual-review.json').relative_to(R)),
        portable_package_current=False,numerical_package_current=False,
        scope='124 complete author records plus explicit component chains cover101 numbered chapters. Citation-only renewal covers415 occurrences in22 chapters; no new full-chapter reading is implied. Fresh visual and independent acceptance remain open.')
    for p in [B/'changed-context-review.json',B/'deletion-audit.json',B/'source-verification.json',B/'numerical-verification.json',
              B/'review-currency-current.json',O/'contextual-review.json',O/'plan.md',O/'occurrences-before.json',
              O/'rendered-citation-locations.json',rendered_path,O/'initial-write-failure.json',O/'review-currency-before.json']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    for x in receipts:
        scope['basis'][x['path']] = x['sha256']
    save(B/'review-scope-current.json',scope)
    (B/'review-scope-current.md').write_text('# Current author-review scope\n\nBatch084:283 exact edits;1,941 reader pages and four sponsor pages.124 complete author records with exact component chains cover101 numbered chapters.415 supporting citations in22 chapters have source-adjacent and rendered-text renewal; this is not a fresh reading of those complete chapters. All substantive content remains, and68 numerical groups pass. Fresh visual and independent acceptance remain open.\n')
    print(json.dumps(dict(status='complete_in_author_scope',batch=84,commands=415,chapters=len(chapters),receipts=len(receipts))))


if __name__ == '__main__':
    main()
