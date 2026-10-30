"""Bind the two reviewed reference corrections to the exact successor."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'closing-review-092'

def read(p): return json.loads(p.read_text())
def save(p, x): p.write_text(json.dumps(x, indent=2) + '\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p): return dict(path=str(p.relative_to(R)), sha256=sha(p))

def main():
    audit, build, edits = [read(B / f) for f in ['deletion-audit.json', 'latest-build.json', 'edits.json']]
    assert audit['status'] == 'pass' and build['batch'] == 86 and len(edits) == 292
    assert audit['ledger_sha256'] == build['ledger_sha256'] == sha(B / 'edits.json')
    assert read(B / 'source-verification.json')['build_batch'] == 86
    numerics = read(B / 'numerical-verification.json')
    assert numerics['status'] == 'pass' and len(numerics['checks']) == 68
    assert all(sha(R / p) == digest for p, digest in numerics['bindings'].items())
    assert all(e['before'].replace('Section~', 'Chapter~', 1) == e['after'] for e in edits[290:])
    old = (B / 'batches/085/full/rendered.txt').read_text().split('\f')
    new = (B / 'batches/086/full/rendered.txt').read_text().split('\f')
    changed = [i + 1 for i, (x, y) in enumerate(zip(old, new)) if x != y]
    assert len(old) == len(new) and changed == [11, 1033], changed
    pages = read(O / 'changed-pages.json')
    combined = ''
    for item in pages:
        assert sha(R / item['path']) == item['sha256']
        combined += f"PHYSICAL PAGE {item['page']}\n" + (R / item['path']).read_text() + '\n'
    (O / 'reviewed-changed-rendered.txt').write_text(combined)
    for name in ['deletion-audit.json', 'source-verification.json', 'numerical-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    reviews = read(O / 'before/changed-context-review.json')
    manifest = read(B / 'context-review-292/manifest.json')
    prior = read(B / 'context-review-290/manifest.json')
    previous, active = {}, []
    for item in reviews['exact_component_renewals']:
        rec = read(R / item['path'])
        if rec['chapter'] in [1, 60]:
            previous[rec['chapter']] = (item, rec)
            reviews.setdefault('superseded_component_renewals', []).append(dict(**item, superseded_by='Exact reference-noun renewal at batch086.'))
        else:
            active.append(item)
    receipts = []
    for n, index in [(1, 291), (60, 292)]:
        c = next(x for x in manifest['chapters'] if x['chapter'] == n)
        oldc = next(x for x in prior['chapters'] if x['chapter'] == n)
        if n in previous:
            item, rec = previous[n]
            complete, indices = rec['complete_predecessor'], rec['edit_numbers'] + [index]
            assert rec['source_context']['sha256'] == oldc['sha256']
            markers = rec.get('source_marker_updates', [])
        else:
            matches = [r for r in reviews['reviews'] if r['chapter'] == n and r['extract_sha256'] == oldc['sha256']]
            assert len(matches) == 1
            complete = dict(extract=matches[0]['extract'], sha256=matches[0]['extract_sha256'])
            indices, markers, item = [index], [], None
        text = (R / complete['extract']).read_text()
        for i in indices:
            e = edits[i - 1]
            assert text.count(e['before']) == 1, (n, i)
            text = text.replace(e['before'], e['after'], 1)
        for m in markers:
            text = text.replace(m['before'] + '\n', m['after'] + '\n', 1)
        assert text == (R / c['extract']).read_text(), n
        record = dict(chapter=n, recorded_utc=datetime.now(timezone.utc).isoformat(), batch=86,
            complete_predecessor=complete, source_context=dict(extract=c['extract'], sha256=c['sha256']),
            edit_numbers=indices, source_marker_updates=markers, predecessor_component_receipt=item,
            reviewed_source_bindings=c['source_bindings'], rendered_text=bind(O / 'reviewed-changed-rendered.txt'),
            numerics=bind(O / 'verified-numerical-verification.json'), publication=audit['publication']['full'],
            findings=[
                'The exact changed rendered passage and its source context were read; the destination is a numbered chapter. Only the reference noun changes.',
                ('The complete current opening chapter was read, including the financial rule, selection example, clock, uncertainty and common-service conclusion.' if n == 1 else
                 'The commercial-discovery component was read through graph semantics, interface restrictions, alternatives and rights. This is a component renewal, not a fresh reading of the entire commercial chapter.'),
                'Every other character reconstructs from the attributed complete predecessor and cumulative exact edits.'],
            acceptance=dict(author_component=True, fresh_visual=False, independent=False, release_accepted=False))
        path = O / f'component-renewal-{n:03d}.json'
        save(path, record)
        receipts.append(bind(path))
        active.append(bind(path))
    reviews['exact_component_renewals'] = active
    reviews['current_snapshot'] = str((B / 'context-review-292/manifest.json').relative_to(R))
    save(B / 'changed-context-review.json', reviews)
    report = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=86, edits=[291, 292],
        publication=audit['publication'], changed_physical_pages=changed, contextual_chains=receipts,
        rendered_text=bind(O / 'reviewed-changed-rendered.txt'), numerics=bind(O / 'verified-numerical-verification.json'),
        findings=['Two section/chapter reference nouns repaired. Both destination labels and the arguments, equations, numbers and qualifications are retained.',
                  'Only two physical pages change. Sponsor bytes and page counts are unchanged. No fresh visual or independent review is claimed.'],
        deletion_assessment=[dict(edit=i, disposition='Section changes to Chapter; the exact reference key and surrounding scientific material remain.') for i in [291, 292]],
        acceptance=dict(author_component=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', report)
    integration = read(O / 'integration.json')
    integration.update(status='verified_in_author_scope', batch=86, review=bind(O / 'contextual-review.json'))
    save(O / 'integration.json', integration)
    subprocess.run(['python3', 'tools/reconcile_release_review_currency_20261029.py'], cwd=R, check=True)

    predecessor = B / 'preservation-review-089/semantic-deletion-review.json'
    prior_review = read(predecessor)
    prefix = (json.dumps(edits[:290], indent=2) + '\n').encode()
    assert hashlib.sha256(prefix).hexdigest() == prior_review['ledger']['sha256']
    assert sha(O / 'before/edits.json') == prior_review['ledger']['sha256']
    assert audit['exact_replay'] and audit['checks_after_final_edit']
    assert not any(audit[k] for k in ['math_removed', 'missing_citation_keys', 'missing_labels', 'distinct_numeric_loss'])
    semantic = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), status='complete_in_author_scope',
        batch=86, edits=292, ledger=bind(B / 'edits.json'), publication=audit['publication'],
        predecessor_review=bind(predecessor), predecessor_prefix_verified=290,
        preserved_predecessor_ledger=bind(O / 'before/edits.json'),
        dispositions=[dict(edit=i, file=edits[i-1]['file'], exact_transformation='Section~ to Chapter~ only',
                           assessment=report['deletion_assessment'][i-291]['disposition'],
                           observed_context_review=bind(O / 'contextual-review.json')) for i in [291,292]],
        mechanical_audit=bind(O / 'verified-deletion-audit.json'),
        conclusion='No unaccounted removal of important scientific material is identified in the assessed 292 edits. The first 290 have an identical preserved prefix and prior attributed semantic review. The last two correct reference nouns without deleting scientific material.',
        scope='Cumulative attributed author assessment with exact predecessor preservation; no fresh whole-book or independent semantic guarantee.',
        acceptance=dict(author_semantic_review=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'semantic-deletion-review.json', semantic)
    save(B / 'semantic-deletion-review-current.json', semantic)
    (B / 'semantic-deletion-review-current.md').write_text('# Current semantic deletion review\n\n' + semantic['conclusion'] + '\n\n' + semantic['scope'] + '\n\nThe immutable 290-edit review and preserved prefix remain bound in the JSON. Both later dispositions are recorded with their exact source and rendered-context review.\n')
    scope = read(B / 'review-scope-current.json')
    scope.update(batch=86, ledger_sha256=audit['ledger_sha256'], publication=audit['publication'], release_edits=292, edits=292,
        latest_contextual_review=str((O / 'contextual-review.json').relative_to(R)),
        latest_rendered_review=str((O / 'contextual-review.json').relative_to(R)),
        portable_package_current=False, numerical_package_current=False,
        semantic_deletion_review=bind(B / 'semantic-deletion-review-current.json'))
    for p in [B / 'changed-context-review.json', B / 'deletion-audit.json', B / 'source-verification.json',
              B / 'numerical-verification.json', B / 'review-currency-current.json', B / 'semantic-deletion-review-current.json',
              O / 'contextual-review.json', O / 'semantic-deletion-review.json', O / 'integration.json',
              O / 'reviewed-changed-rendered.txt', O / 'before/edits.json', predecessor]:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    for item in receipts:
        scope['basis'][item['path']] = item['sha256']
    save(B / 'review-scope-current.json', scope)
    (B / 'review-scope-current.md').write_text('# Current author-review scope\n\nBatch 086: 292 exact edits, 1,941 reader pages and four sponsor pages. The 124 complete author records and explicit component chains cover 101 numbered chapters. The latest renewal corrects two reference nouns and preserves their scientific contexts. Fresh visual and independent acceptance remain open.\n')
    print(json.dumps(dict(status='complete_in_author_scope', batch=86, edits=292, changed_pages=changed)))

if __name__ == '__main__':
    main()
