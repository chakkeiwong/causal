"""Authenticate recorded author-review coverage; never certify fresh acceptance."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
INPUT = re.compile(r'\\(?:input|include)\{([^}]+)\}')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    reviews = read(BASE / 'changed-context-review.json')
    manifest_path = ROOT / reviews['current_snapshot']
    manifest = read(manifest_path)
    audit = read(BASE / 'deletion-audit.json')
    build = read(BASE / 'latest-build.json')
    renewal_path = BASE / 'review-currency-063/contextual-review.json'
    renewal = read(renewal_path)
    issues, basis = [], {}

    def bind(name, expected=None):
        path = Path(name)
        path = path if path.is_absolute() else ROOT / path
        if not path.is_file():
            issues.append(f'Missing evidence: {path}')
            return
        actual = sha(path)
        if expected is not None and expected != actual:
            issues.append(f'Changed evidence: {path}')
        basis[str(path.relative_to(ROOT))] = actual

    for path in [BASE / 'changed-context-review.json', manifest_path, renewal_path]:
        bind(path)
    if not (audit['status'] == 'pass' and audit['ledger_sha256'] ==
            manifest['ledger_sha256'] == build['ledger_sha256'] == sha(BASE / 'edits.json')):
        issues.append('Build, audit and context ledger disagree')
    for publication in audit['publication'].values():
        if sha(ROOT / publication['path']) != publication['sha256']:
            issues.append('Publication identity differs from audit')
    for record in reviews['reviews']:
        bind(record['extract'], record['extract_sha256'])
        if record['status'] != 'complete_in_author_scope':
            issues.append(f'Incomplete record: {record["extract"]}')
    chain = []
    for item in renewal['chapter47']['renewals']:
        bind(item['path'], item['sha256'])
        receipt = read(ROOT / item['path'])
        context = receipt['source_context']
        bind(context['extract'], context['sha256'])
        if not receipt['acceptance']['author_context']:
            issues.append(f'Incomplete component: {item["path"]}')
        chain.append(context)
    predecessor = [r for r in reviews['reviews'] if r['chapter'] == 47 and
                   r['extract'] == renewal['chapter47']['complete_predecessor']]
    if len(predecessor) != 1 or len(chain) != 2:
        issues.append('Chapter47 predecessor or two renewals absent')

    component_renewals = {}
    edits = read(BASE / 'edits.json')
    for item in reviews.get('exact_component_renewals', []):
        bind(item['path'], item['sha256'])
        receipt = read(ROOT / item['path'])
        chapter = receipt['chapter']
        old = receipt['complete_predecessor']
        current = receipt['source_context']
        bind(old['extract'], old['sha256'])
        bind(current['extract'], current['sha256'])
        matching = [r for r in reviews['reviews'] if r['chapter'] == chapter
                    and r['extract_sha256'] == old['sha256']]
        if len(matching) != 1 or not receipt['acceptance']['author_component']:
            issues.append(f'Unreviewed component predecessor or renewal: {chapter}')
        reconstructed = (ROOT / old['extract']).read_text()
        for index in receipt['edit_numbers']:
            edit = edits[index - 1]
            if reconstructed.count(edit['before']) != 1:
                issues.append(f'Component edit not unique in predecessor: {chapter}:{index}')
            else:
                reconstructed = reconstructed.replace(edit['before'], edit['after'], 1)
        for update in receipt.get('source_marker_updates', []):
            old_marker = re.fullmatch(r'% SOURCE (.+) CHAR (\d+)', update['before'])
            new_marker = re.fullmatch(r'% SOURCE (.+) CHAR (\d+)', update['after'])
            context_segments = next(c['segments'] for c in manifest['chapters'] if c['chapter'] == chapter)
            if not (old_marker and new_marker and old_marker[1] == new_marker[1]
                    and any(s['file'] == new_marker[1] and s['start'] == int(new_marker[2]) for s in context_segments)
                    and reconstructed.count(update['before']+'\n') == 1):
                issues.append(f'Invalid source-position metadata renewal: {chapter}')
            else:
                reconstructed = reconstructed.replace(update['before']+'\n', update['after']+'\n', 1)
        if reconstructed != (ROOT / current['extract']).read_text():
            issues.append(f'Component renewal does not reconstruct current context: {chapter}')
        for name, digest in receipt['reviewed_source_bindings'].items():
            if sha(ROOT / name) != digest:
                issues.append(f'Component source changed after review: {name}')
        for field in ['rendered_text', 'numerics']:
            row = receipt[field]
            bind(row['path'], row['sha256'])
        if chapter in component_renewals:
            issues.append(f'Duplicate component renewal: {chapter}')
        component_renewals[chapter] = receipt

    cache, coverage, chunks, drift = {}, [], [], set()
    segment_count = 0
    for context in manifest['chapters']:
        bind(context['extract'], context['sha256'])
        chunks.append(re.sub(r'^% SOURCE .+ CHAR \d+\n', '',
                            (ROOT / context['extract']).read_text(), flags=re.M))
        for segment in context['segments']:
            name = segment['file']
            if name not in cache:
                cache[name] = (ROOT / name).read_text()
            actual = cache[name][segment['start']:segment['start'] + segment['characters']]
            if hashlib.sha256(actual.encode()).hexdigest() != segment['sha256']:
                issues.append(f'Stale segment: {context["title"]}: {name}')
            segment_count += 1
        matches = [i for i, r in enumerate(reviews['reviews'])
                   if r['extract_sha256'] == context['sha256'] and
                   r['chapter'] == context['chapter'] and r['title'] == context['title']]
        if matches:
            mode = 'exact_complete_context'
            supporting = [reviews['reviews'][i]['extract'] for i in matches]
            for i in matches:
                for name, expected in reviews['reviews'][i]['source_bindings'].items():
                    if sha(ROOT / name) != expected:
                        drift.add(name)
        elif context['chapter'] == 47 and chain and chain[-1]['sha256'] == context['sha256']:
            mode = 'complete_predecessor_plus_component_renewals'
            supporting = [renewal['chapter47']['complete_predecessor']] + [v['extract'] for v in chain]
        elif (context['chapter'] in component_renewals and
              component_renewals[context['chapter']]['source_context']['sha256'] == context['sha256']):
            mode = 'complete_predecessor_plus_exact_component_replay'
            receipt = component_renewals[context['chapter']]
            supporting = [receipt['complete_predecessor']['extract'], receipt['source_context']['extract']]
        elif context['title'] == 'Preamble' and renewal['preamble']['context']['sha256'] == context['sha256']:
            mode = 'explicit_preamble_review'
            supporting = [str(renewal_path.relative_to(ROOT))]
        else:
            mode, supporting = 'uncovered', []
            issues.append(f'No current review: {context["chapter"]}: {context["title"]}')
        coverage.append(dict(chapter=context['chapter'], title=context['title'],
                             extract=context['extract'], sha256=context['sha256'],
                             mode=mode, supporting=supporting))

    source_root = BASE / 'source/docs'
    def expand(path, ancestors=()):
        if path in ancestors:
            raise ValueError(f'Input cycle: {path}')
        def substitute(match):
            child = source_root / match.group(1)
            child = child if child.suffix else child.with_suffix('.tex')
            return expand(child, ancestors + (path,))
        return INPUT.sub(substitute, path.read_text())
    compiled = ''.join(expand(source_root / 'causal_banking_release_candidate_2026-10-29.tex').split())
    extracted = ''.join('\n'.join(chunks).split())
    if compiled != extracted:
        issues.append('Review extracts differ from expanded compiled input tree')
    sponsor = reviews['sponsor_review']
    for name, expected in sponsor['source_bindings'].items():
        if sha(ROOT / name) != expected:
            issues.append(f'Sponsor source changed: {name}')
    if sponsor['publication']['sha256'] != audit['publication']['sponsor']['sha256']:
        issues.append('Sponsor PDF changed since complete review')
    bind(renewal['rendered_text']['path'], renewal['rendered_text']['sha256'])
    bind(renewal['sponsor']['rendered']['path'], renewal['sponsor']['rendered']['sha256'])
    if sponsor.get('rendered_text'):
        bind(sponsor['rendered_text']['path'], sponsor['rendered_text']['sha256'])
    if sponsor.get('review_record'):
        bind(sponsor['review_record']['path'], sponsor['review_record']['sha256'])
    numbered = [row for row in coverage if row['chapter'] > 0]
    if [row['chapter'] for row in numbered] != list(range(1, 102)):
        issues.append('Numbered chapters are not exactly1 through101')
    report = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
        status='pass' if not issues else 'fail', batch=build['batch'],
        ledger_sha256=audit['ledger_sha256'], publication=audit['publication'],
        author_record_count=len(reviews['reviews']), numbered_chapters=len(numbered),
        current_contexts=len(coverage), source_segments_checked=segment_count,
        coverage_modes=dict(Counter(row['mode'] for row in coverage)),
        expanded_manuscript_matches=compiled == extracted,
        expanded_nonwhitespace_characters=len(compiled),
        expanded_nonwhitespace_sha256=hashlib.sha256(compiled.encode()).hexdigest(),
        unrelated_whole_file_hash_drift=sorted(drift),
        whole_file_drift_interpretation='Shared files changed elsewhere; exact extract and source-segment identity establishes coverage of each reviewed passage.',
        contexts=coverage, basis=basis, issues=issues,
        scope='Authenticates recorded complete-context author readings and explicit component renewals against the complete current compiled manuscript. Not a fresh whole-book reread, source-claim correctness theorem, independent review or visual acceptance.',
        acceptance=dict(fresh_visual=False, independent=False, release_accepted=False))
    (BASE / 'review-currency-current.json').write_text(json.dumps(report, indent=2) + '\n')
    (BASE / 'review-currency-current.md').write_text(
        '# Current chapter-review coverage\n\n' +
        f'Batch{build["batch"]:03d}: {report["status"]}. There are{len(reviews["reviews"])} author records for101 numbered chapters, two introductory contexts and the separately reviewed preamble. Coverage modes: {report["coverage_modes"]}. Exact component replay does not assert a fresh full-chapter reread.\n\n' +
        f'All{segment_count} source segments match current text. Expansion of the actual manuscript input tree matches the combined review extracts after whitespace normalization. The current sponsor retains its separately attributed source and rendered-text review.\n\n' +
        report['scope'] + '\n')
    print(json.dumps({k: report[k] for k in ['status','batch','author_record_count',
        'numbered_chapters','current_contexts','source_segments_checked','coverage_modes','issues']}))
    if issues:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
