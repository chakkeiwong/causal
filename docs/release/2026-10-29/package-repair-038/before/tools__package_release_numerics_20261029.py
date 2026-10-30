"""Freeze a numerical reconstruction package; keep public data intake separate."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
EXTERNAL = {'docs/literature/raw/gap29_nsw_treated.txt',
            'docs/literature/raw/gap29_nsw_control.txt'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    build = json.loads((BASE / 'latest-build.json').read_text())
    audit = json.loads((BASE / 'deletion-audit.json').read_text())
    receipt = json.loads((BASE / 'numerical-verification.json').read_text())
    assert receipt['status'] == audit['status'] == 'pass'
    assert build['ledger_sha256'] == audit['ledger_sha256'] == sha(BASE / 'edits.json')
    for name, digest in receipt['bindings'].items():
        assert sha(ROOT / name) == digest, name
    package = BASE / 'numerical-packages' / ('batch-%03d' % build['batch'])
    package.mkdir(parents=True, exist_ok=False)
    inputs = {}
    for name, digest in receipt['bindings'].items():
        if name not in EXTERNAL:
            target = package / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)
        if not name.startswith('tools/'):
            inputs[name] = {'sha256': digest, 'bytes': (ROOT / name).stat().st_size,
                            'external': name in EXTERNAL,
                            'provenance': ('Retained public experimental subset; data-specific commercial redistribution rights unresolved.'
                                           if name in EXTERNAL else 'Retained project-authored design, synthetic evidence or arithmetic; original bindings preserved.')}
    evidence = package / 'evidence'
    evidence.mkdir()
    for name in ['numerical-verification.json', 'source-verification.json']:
        shutil.copy2(BASE / name, evidence / name)
    for name in ['gap29_nsw_treated.receipt.json', 'gap29_nsw_control.receipt.json']:
        shutil.copy2(ROOT / 'docs/literature/raw' / name, evidence / name)
    shutil.copy2(ROOT / 'tools/release_portable_numerics_20261029.py', package / 'reconstruct.py')
    (package / 'README.md').write_text('''# Retained numerical reconstruction

This local review package reconstructs the release-critical arithmetic groups listed in manifest.json
from the retained data. It draws no new samples and makes no new causal, native
package, bank-validation or independent-acceptance claim. It does not regenerate
every original simulation or reproduce every number in the monograph.

Run with Python and the NumPy/SciPy versions in manifest.json:

    python3 /path/to/package/reconstruct.py --external-root /path/to/supplied-inputs --output /path/to/new-result

The output directory must not exist. The external root must contain the two
repository-relative public-data paths listed in manifest.json. Supply the
retained originals whose hashes match the provenance receipts; the runner makes
no network requests. These public experimental files are excluded because their
data-specific commercial redistribution terms are unresolved. This package
grants no rights over them. No papers or vendor documents are bundled.

All project data, the unchanged numerical verifier, expected results and their
hashes are included. The runner verifies bytes before reconstruction, compares
all result structures with the reference using declared numerical tolerances,
and checks that inputs remain unchanged. The original verifier itself checks
claims against retained results and exact rational constructions. Environment
differences are reported. The surrounding assignment, observation, selection and
transport assumptions require scientific evidence beyond arithmetic agreement.
''')
    manifest = {'schema_version': 1, 'reference_batch': build['batch'],
                'reader_sha256': audit['publication']['full']['sha256'],
                'ledger_sha256': audit['ledger_sha256'],
                'scope': str(len(receipt['checks'])) + ' retained arithmetic groups; external public-input intake required; no new experimental qualification.',
                'check_groups': list(receipt['checks']),
                'versions': receipt['versions'], 'inputs': inputs,
                'tolerance': {'absolute': 1e-7, 'relative': 1e-10},
                'files': {str(p.relative_to(package)): sha(p) for p in sorted(package.rglob('*')) if p.is_file()}}
    (package / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'package': str(package.relative_to(ROOT)), 'files': len(manifest['files']),
                      'project_inputs': sum(not v['external'] for v in inputs.values()),
                      'external_inputs': sorted(EXTERNAL), 'manifest_sha256': sha(package / 'manifest.json')}))


if __name__ == '__main__':
    main()
