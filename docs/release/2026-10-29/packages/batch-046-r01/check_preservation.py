"""Replay every candidate edit against the packaged preserved source bytes."""
from pathlib import Path
from collections import Counter
import argparse
import copy
import hashlib
import json
import re

from math_review import validate_additions

PREFIX = 'docs/release/2026-10-29/'
MATH = re.compile(r'(?s)(?<!\\)\\\[.*?(?<!\\)\\\]|(?<!\\)\\\(.*?(?<!\\)\\\)|(?<!\\)\$(?!\$).*?(?<!\\)\$|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}.*?\\end\{\1\}')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((package / 'manifest.json').read_text())
    mapping = json.loads((package / 'evidence/source-map.json').read_text())
    additions = json.loads((package / 'evidence/additions.json').read_text())
    edits = json.loads((package / 'evidence/edits.json').read_text())
    issues = []
    for group in ['evidence_hashes', 'verifier_hashes']:
        for name, digest in manifest.get(group, {}).items():
            p = package / name
            if not p.is_file() or sha(p) != digest:
                issues.append('Packaged verification evidence changed: ' + name)
    expected = {}
    for name, digest in manifest['preserved_source_hashes'].items():
        if not (package / name).is_file() or sha(package / name) != digest:
            issues.append('Preserved source identity changed: ' + name)
    for target, row in {**mapping, **{r['path']: r for r in additions}}.items():
        original = package / 'preserved' / row['original']
        if not original.is_file() or sha(original) != row['sha256']:
            issues.append('Missing or changed original for: ' + target)
            continue
        expected[target] = original.read_bytes()
    initial = dict(expected)
    dispositions = []
    for i, edit in enumerate(edits, 1):
        name = edit['file']
        if name not in expected:
            issues.append('Edit has no preserved source: ' + str(i))
            continue
        before, after = edit['before'].encode(), edit['after'].encode()
        if expected[name].count(before) != 1:
            issues.append('Edit anchor is not unique: ' + str(i))
            continue
        if not edit.get('reason') or not edit.get('substantive_destination'):
            issues.append('Missing change disposition: ' + str(i))
        expected[name] = expected[name].replace(before, after, 1)
        dispositions.append({'edit': i, 'file': name, 'replaced_bytes': len(before),
                             'replacement_bytes': len(after), 'reason': edit.get('reason'),
                             'substantive_destination': edit.get('substantive_destination')})
    for name, content in expected.items():
        if not name.startswith(PREFIX + 'source/'):
            issues.append('Unexpected target mapping: ' + name)
            continue
        final = package / name[len(PREFIX):]
        if not final.is_file() or final.read_bytes() != content:
            issues.append('Final source differs from exact replay: ' + name)
    actual = {str(p.relative_to(package)): sha(p) for p in (package / 'source').rglob('*') if p.is_file()}
    if actual != manifest['source_hashes']:
        issues.append('Final source inventory differs from package manifest')
    if sha(package / 'evidence/edits.json') != manifest['ledger_sha256']:
        issues.append('Edit ledger identity changed')
    # The source reviews retain repository paths. Only evidence lookup paths
    # are translated for a portable review; edit identity fields stay exact.
    math_path = package / 'evidence/mathematical-addition-reviews.json'
    math_reviews = copy.deepcopy(json.loads(math_path.read_text())['reviews']) if math_path.exists() else []
    for review in math_reviews:
        for field in ['witness', 'source_audit']:
            name = review.get(field, {}).get('path', '')
            if not name.startswith(PREFIX):
                issues.append('Review evidence is outside packaged release scope: ' + name)
            else:
                review[field]['path'] = 'evidence/' + name[len(PREFIX):]
    approved, math_issues = validate_additions(math_reviews, edits, package, MATH)
    issues.extend(math_issues)
    def math_counts(files):
        result = Counter()
        for name, content in files.items():
            if name.endswith('.tex'):
                result.update(re.sub(r'\s+', ' ', m[0]) for m in MATH.finditer(content.decode()))
        return result
    before_math, after_math = math_counts(initial), math_counts(expected)
    if before_math - after_math:
        issues.append('Mathematical removal from preserved originals')
    if after_math - before_math != approved:
        issues.append('Mathematical additions differ from reviewed exact edits')
    relocated = []
    relocation_path = package / 'evidence/protected-relocations.json'
    if relocation_path.exists():
        registry = json.loads(relocation_path.read_text())['relocations']
        audit = json.loads((package / 'evidence/deletion-audit.json').read_text())
        if registry != audit.get('protected_preserved_elsewhere', []):
            issues.append('Protected relocation registry differs from final audit')
        for row in registry:
            for name, digest in [(row['preserved'], row['expected_sha256']),
                                 (row['review_record']['path'], row['review_record']['sha256'])]:
                if not name.startswith(PREFIX):
                    issues.append('Relocated evidence outside declared release scope: ' + name)
                    continue
                p = package / 'evidence' / name[len(PREFIX):]
                if not p.is_file() or sha(p) != digest:
                    issues.append('Protected relocation evidence missing or changed: ' + name)
            relocated.append(row['original'])
    review_files = 0
    review_index_path = package / 'evidence/author-review-index.json'
    if review_index_path.exists():
        index = json.loads(review_index_path.read_text())
        contexts = json.loads((package / 'evidence/changed-context-review.json').read_text())
        if index['full_context_records'] != len(contexts['reviews']):
            issues.append('Author-review record count differs from packaged contexts')
        for name, row in index['files'].items():
            target = (package / row['path']).resolve()
            if not target.is_relative_to((package / 'evidence').resolve()) or not target.is_file() or sha(target) != row['sha256']:
                issues.append('Author-review evidence missing or changed: ' + name)
            review_files += 1
        for row in contexts['reviews']:
            binding = index['files'].get(row['extract'])
            if not binding or binding['sha256'] != row['extract_sha256']:
                issues.append('Context extract missing from author-review index: ' + row['extract'])
    report = {'status': 'fail' if issues else 'pass', 'batch': manifest['batch'],
              'edits': len(edits), 'replayed_sources': len(expected), 'issues': issues,
              'mathematical_removals': dict(before_math - after_math),
              'reviewed_added_expressions': len(approved),
              'protected_relocations_checked': relocated,
              'author_review_files_checked': review_files,
              'scope': 'Exact release-stage source replacement replay against the preserved 505-edit baseline and declared additions. This does not certify scientific adequacy or replay the earlier baseline rewrite.',
              'dispositions': dispositions}
    (args.output / 'preservation-replay.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'dispositions'}, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
