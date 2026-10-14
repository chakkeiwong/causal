#!/usr/bin/env python3
"""Normalize saved primary text without modifying acquired bytes."""
from pathlib import Path
import json
import subprocess
from vendor_text_20261013 import Document

BASE = Path(__file__).resolve().parents[1] / 'docs/program/execution/2026-10-13/commercial-iv-rd'

def main():
    for name in ['stata_iv', 'stata_post', 'rats11', 'jmp19']:
        output = BASE / (name + '.txt')
        if not output.exists():
            result = subprocess.run(['pdftotext', '-layout', str(BASE / (name + '.pdf')), str(output)],
                                    capture_output=True, text=True, timeout=20)
            assert result.returncode == 0, result.stderr
        print(json.dumps({'source': name, 'text_lines': len(output.read_text().splitlines())}))
    for name in ['stata19_feature', 'stata18now', 'eviews_iv', 'spss30_iv', 'rdpackages', 'stata_license']:
        output = BASE / (name + '.txt')
        if not output.exists():
            parser = Document()
            parser.feed((BASE / (name + '.html')).read_text())
            output.write_text(parser.text + chr(10))
            (BASE / (name + '.links.json')).write_text(json.dumps(parser.links, indent=2) + chr(10))
        lines = output.read_text().splitlines()
        print(json.dumps({'source': name, 'text_lines': len(lines), 'first': lines[:2]}))
    for name in ['rdrobust_cutoff', 'rddensity_cutoff']:
        rows = json.loads((BASE / (name + '.json')).read_text())
        print(json.dumps({'source': name, 'commit': rows[0]['sha'], 'date': rows[0]['commit']['committer']['date']}))

if __name__ == '__main__':
    main()
