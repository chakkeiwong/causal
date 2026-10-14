#!/usr/bin/env python3
"""Reexecute a historical verifier in its exact archived project file view."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import traceback
import zipfile

ROOT = Path(__file__).resolve().parents[1]
from replay_proposal_demonstrations_20261013 import compare, ref

CASES = {
    'dynamic': ('v6.1', 'verify_dynamic', 'dynamic-verification'),
    'linkage': ('v6.1', 'verify_linkage', 'linkage-verification'),
    'reliability': ('v8', 'reliability_verify', 'reliability-verification'),
    'calibration': ('v9', 'calibration_verify', 'calibration-verification'),
}


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('program', choices=CASES)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    version, verifier, receipt_name = CASES[args.program]
    preservation = ROOT / f'docs/program/history/{version}-preservation-receipt.json'
    p = json.loads(preservation.read_text())
    archive_path = ROOT / p['archive']
    receipt_path = 'docs/reviews/' + receipt_name + '.json'
    result = {'status': 'running', 'replay_executed_at': datetime.now(timezone.utc).isoformat(),
              'harness': ref(Path(__file__)), 'preservation': ref(preservation),
              'version': version, 'program': args.program,
              'scope': 'Original verifier executes in its original hash-checked file view. Preserved results remain unchanged; historical dates are not this replay date.',
              'limits': ['Retains the verifier scope: saved numerical reconstruction and version-specific checks, not all original simulation draws or timing workloads.']}
    try:
        assert digest(archive_path) == p['sha256'], 'Archive identity mismatch'
        result['archive'] = {'path': str(archive_path.relative_to(ROOT)), 'sha256': p['sha256']}
        with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory(prefix='causal-q3-' + version + '-') as temp:
            view = Path(temp)
            manifest_raw = archive.read('docs/program/reconstruction-delivery-manifest.json')
            assert hashlib.sha256(manifest_raw).hexdigest() == p['manifest_sha256'], 'Manifest identity mismatch'
            manifest = json.loads(manifest_raw)
            members = set(archive.namelist())
            copied = linked = 0
            archived_receipt = None
            for row in manifest['artifacts']:
                name = row['path']
                relative = Path(name)
                assert not relative.is_absolute() and '..' not in relative.parts
                target = view / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                source = ROOT / relative
                # Copy every project Python module so __file__ resolves in this
                # view. Writable receipts are copies; other same-version files
                # can be read through links after verifying their exact bytes.
                must_copy = relative.suffix == '.py' or name == receipt_path
                current_matches = source.is_file() and source.stat().st_size == row['bytes'] and digest(source) == row['sha256']
                if current_matches and not must_copy:
                    target.symlink_to(source)
                    linked += 1
                else:
                    if name in members:
                        raw = archive.read(name)
                        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], name
                        target.write_bytes(raw)
                    else:
                        assert current_matches, 'Missing historical bytes: ' + name
                        shutil.copyfile(source, target)
                    copied += 1
                if name == receipt_path:
                    archived_receipt = json.loads(target.read_text())
            assert archived_receipt is not None
            result['file_view'] = {'manifest_entries': len(manifest['artifacts']), 'linked': linked, 'copied': copied}
            environment = {**os.environ, 'PYTHONPATH': str(view / 'src') + os.pathsep + str(view / 'tools'),
                           'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'}
            with (out / 'execution.log').open('w') as log:
                process = subprocess.run([sys.executable, str(view / 'tools' / (verifier + '.py'))],
                                         cwd=view, env=environment, stdout=log, stderr=subprocess.STDOUT, timeout=180)
            computed = view / receipt_path
            shutil.copyfile(computed, out / (receipt_name + '.json'))
            assert process.returncode == 0, 'Archived verifier exit ' + str(process.returncode)
            value = json.loads(computed.read_text())
            assert value['status'] == 'pass' and not value.get('issues'), str(value.get('issues'))[:1000]
            compare(value, archived_receipt)
            result['recomputed'] = ref(out / (receipt_name + '.json'))
            result['full_receipt_matches_archived_result'] = True
            result['status'] = 'pass'
    except Exception as exc:
        result.update(status='fail', error=type(exc).__name__ + ': ' + str(exc))
        (out / 'failure.txt').write_text(traceback.format_exc())
    (out / 'replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'program': args.program, 'version': version, 'status': result['status'], 'error': result.get('error')}))
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
