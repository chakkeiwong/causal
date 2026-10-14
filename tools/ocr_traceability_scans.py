#!/usr/bin/env python3
"""Extract selected saved primary pages locally; never award semantic review."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13'
OUT = BASE / 'traceability/primary-scans-01'
OCR_ROOT = Path('/tmp/causal-ocr/unpacked')
SELECTED = {'newey1986': [1, 4, 5, 6, 7, 8, 9],
            'staiger1994': [1, 5, 6, 7, 8, 9, 17, 18, 19, 20, 21]}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    OUT.mkdir(exist_ok=False)
    index_path = BASE / 'identification-review/traceability-review.json'
    index = json.loads(index_path.read_text())
    records = {r['citation_key']: r for r in index['records']}
    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = str(OCR_ROOT / 'usr/lib/x86_64-linux-gnu')
    env['TESSDATA_PREFIX'] = str(OCR_ROOT / 'usr/share/tesseract-ocr/4.00/tessdata')
    env['OMP_THREAD_LIMIT'] = '1'
    binary = OCR_ROOT / 'usr/bin/tesseract'
    version = subprocess.run([str(binary), '--version'], env=env, check=True,
                             capture_output=True, text=True).stdout
    manifest = {'procedure_sha256': sha(Path(__file__)), 'index_sha256': sha(index_path),
                'tool_version': version, 'binary_sha256': sha(binary),
                'packages': [{'name': p.name, 'sha256': sha(p)}
                             for p in sorted(Path('/tmp/causal-ocr').glob('*.deb'))],
                'limit': 'OCR is a fallible reading aid, not an agent-authored replacement paper or visual acceptance.',
                'records': []}
    for key, pages in SELECTED.items():
        source = records[key]['local_copies'][0]
        pdf = ROOT / source['path']
        assert sha(pdf) == source['sha256']
        for page in pages:
            prefix = OUT / f'{key}-p{page:03}'
            subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', '220',
                            '-singlefile', '-png', str(pdf), str(prefix)],
                           check=True, capture_output=True)
            subprocess.run([str(binary), str(prefix) + '.png', str(prefix),
                            '-l', 'eng', '--psm', '3'],
                           env=env, check=True, capture_output=True)
            image, text = Path(str(prefix) + '.png'), Path(str(prefix) + '.txt')
            assert len(text.read_text().strip()) > 100
            manifest['records'].append({'citation_key': key, 'pdf_page': page,
                'source': source, 'image': {'path': str(image.relative_to(ROOT)), 'sha256': sha(image)},
                'text': {'path': str(text.relative_to(ROOT)), 'sha256': sha(text)}})
            print(key, page, len(text.read_text()), flush=True)
            (OUT / 'progress.json').write_text(json.dumps(manifest, indent=2) + '\n')
    with (OUT / 'manifest.json').open('x') as handle:
        json.dump(manifest, handle, indent=2)
        handle.write('\n')

if __name__ == '__main__':
    main()
