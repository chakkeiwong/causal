"""Replay every candidate edit against the packaged preserved source bytes."""
from pathlib import Path
import argparse
import hashlib
import json

PREFIX = 'docs/release/2026-10-29/'


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
    report = {'status': 'fail' if issues else 'pass', 'batch': manifest['batch'],
              'edits': len(edits), 'replayed_sources': len(expected), 'issues': issues,
              'scope': 'Exact release-stage source replacement replay against the preserved 505-edit baseline and declared additions. This does not certify scientific adequacy or replay the earlier baseline rewrite.',
              'dispositions': dispositions}
    (args.output / 'preservation-replay.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'dispositions'}, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
