"""Replay the packaged arithmetic from hash-checked retained inputs, without draws."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(actual, expected, path='checks'):
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys(), path
        for key in expected:
            compare(actual[key], expected[key], path + '.' + key)
    elif isinstance(expected, list):
        assert len(actual) == len(expected), path
        for i, (a, e) in enumerate(zip(actual, expected)):
            compare(a, e, path + '[' + str(i) + ']')
    elif isinstance(expected, float):
        assert math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-7), path
    else:
        assert actual == expected, path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--external-root', type=Path, required=True,
                        help='Locally supplied retained public inputs in repository-relative paths')
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    manifest = json.loads((package / 'manifest.json').read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'fail', 'scope': manifest['scope'], 'package': str(package),
              'reference_batch': manifest['reference_batch'], 'issues': []}
    resolved = {}
    try:
        for name, expected in manifest['files'].items():
            assert sha(package / name) == expected, 'Changed package file: ' + name
        for name, row in manifest['inputs'].items():
            if row['external']:
                assert not (package / name).exists(), 'External input unexpectedly bundled: ' + name
            path = (args.external_root if row['external'] else package) / name
            assert path.is_file(), 'Missing retained input: ' + name
            assert sha(path) == row['sha256'], 'Changed retained input: ' + name
            resolved[name] = path
        original = 'tools/release_numerical_verification_20261029.py'
        spec = importlib.util.spec_from_file_location('retained_release_arithmetic', package / original)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.ROOT = package
        module.OUT = args.output
        # Resolve project-authored verifier helpers from this relocated bundle.
        # Manifest checks above bind their exact bytes before any import.
        sys.path.insert(0, str(package / 'tools'))
        def checked_raw(name):
            assert name in resolved, 'Undeclared numerical input: ' + name
            value = resolved[name].read_bytes()
            digest = hashlib.sha256(value).hexdigest()
            assert digest == manifest['inputs'][name]['sha256'], name
            module.bindings[name] = digest
            return value
        module.raw = checked_raw
        module.main()
        actual = json.loads((args.output / 'numerical-verification.json').read_text())
        reference = json.loads((package / 'evidence/numerical-verification.json').read_text())
        compare(actual['checks'], reference['checks'])
        assert actual['bindings'] == reference['bindings'], 'Numerical binding mismatch'
        assert all(sha(path) == manifest['inputs'][name]['sha256'] for name, path in resolved.items())
        assert all(sha(package / name) == digest for name, digest in manifest['files'].items())
        report.update(status='pass', reconstructed_checks=list(actual['checks']),
                      input_count=len(resolved), inputs_unchanged=True,
                      packaged_files_unchanged=True, versions=actual['versions'],
                      reference_versions=reference['versions'],
                      environment_matches_reference=actual['versions'] == reference['versions'],
                      external_inputs=[k for k, v in manifest['inputs'].items() if v['external']],
                      reconstructed_report_sha256=sha(args.output / 'numerical-verification.json'))
    except Exception as exc:
        report['issues'].append(type(exc).__name__ + ': ' + str(exc))
    (args.output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    if report['status'] != 'pass':
        sys.exit(1)


if __name__ == '__main__':
    main()
