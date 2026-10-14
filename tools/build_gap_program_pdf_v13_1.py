#!/usr/bin/env python3
"""Compile the refreshed program with explicitly wrapped table columns."""
import json
import re
import subprocess
from pathlib import Path

import master_control as core
import review_gap_reader_v13 as layout

ROOT = core.ROOT
OUT = ROOT/'docs/program/gap-execution-v13_1/program-pdf'
SOURCE = ROOT/'docs/program/master-program-v13_1.md'
PDF = SOURCE.with_suffix('.pdf')


def main():
    if PDF.exists():
        raise ValueError('Preserve published plan bytes; create a successor')
    OUT.mkdir(parents=True, exist_ok=True)
    header = (r'\usepackage{array,microtype,xurl}'+'\n'+
        r'\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}'+'\n'+
        r'\DeclareUnicodeCharacter{03B5}{\ensuremath{\varepsilon}}'+'\n'+
        r'\DeclareUnicodeCharacter{2212}{\ensuremath{-}}'+'\n'+r'\emergencystretch=4em'+'\n')
    (OUT/'header.tex').write_text(header)
    tex = OUT/'master-program.tex'
    subprocess.run(['pandoc', str(SOURCE), '--from=gfm', '--standalone', '--to=latex',
        '-H', str(OUT/'header.tex'), '-V', 'geometry:margin=18mm', '-V', 'fontsize=10pt',
        '-o', str(tex)], check=True, timeout=30)
    raw = tex.read_text()
    for n, widths in [(2, [.24,.76]), (4,[.15,.29,.28,.28]), (3,[.18,.41,.41])]:
        token = r'\begin{longtable}[]{@{}'+'l'*n+r'@{}}'
        assert raw.count(token) == 1, (n, 'Unexpected program table shape')
        cols = ''.join(r'>{\raggedright\arraybackslash}p{\dimexpr '+str(w)+r'\linewidth-2\tabcolsep\relax}' for w in widths)
        raw = raw.replace(token, r'\begin{longtable}[]{@{}'+cols+r'@{}}', 1)
    tex.write_text(raw)
    cmd = ['pdflatex', '-no-shell-escape', '-interaction=batchmode', '-halt-on-error',
           '-output-directory='+str(OUT), str(tex)]
    for i in range(2):
        with (OUT/f'pdflatex-{i+1}.stdout').open('w') as stream:
            subprocess.run(cmd, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True, timeout=40)
    log = (OUT/'master-program.log').read_text()
    warnings = [x for x in log.splitlines() if any(w in x for w in ['Overfull', 'Underfull', 'Warning', 'Missing character'])]
    if any(w in log for w in ['Overfull', 'Missing character', 'undefined references']):
        raise ValueError('Program PDF has unresolved layout/reference findings')
    PDF.write_bytes((OUT/'master-program.pdf').read_bytes())
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    report = {'pages': pages, 'pdf': {'path': str(PDF.relative_to(ROOT)), 'sha256': core.sha(PDF), 'anchor': 'Execution refresh'},
              'warnings': warnings, 'visual_acceptance': False}
    core.write(OUT/'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    print(json.dumps({'pages': pages, 'warnings': warnings}))


if __name__ == '__main__':
    main()
