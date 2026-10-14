#!/usr/bin/env python3
"""Render selected V10 pages; actual viewing requires a separate receipt."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    records = json.loads((ROOT / 'docs/reviews/foundations-render-receipt.json').read_text())
    selected = {'docs/causal_foundations.pdf': [2, 3, 8, 223, 224, 225, 226, 227],
                'docs/sponsor_reconstruction.pdf': [7, 8, 9]}
    output = []
    for record in records:
        path = ROOT / record['pdf']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256']
        folder = ROOT / Path(record['contact_sheets'][0]).parent
        for page in selected[record['pdf']]:
            assert 1 <= page <= record['pages']
            prefix = folder / f'precision-detail-{page:03d}'
            subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page),
                            '-scale-to', '1800', '-singlefile', '-png', str(path), str(prefix)],
                           check=True, capture_output=True)
            output.append(dict(pdf=record['pdf'], pdf_sha256=record['sha256'], page=page,
                               image=str(prefix.relative_to(ROOT)) + '.png'))
    (ROOT / 'docs/reviews/precision-detail-render.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(rendered=len(output), inspection='pending actual image viewing')))


if __name__ == '__main__':
    main()
