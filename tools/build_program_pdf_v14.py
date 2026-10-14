#!/usr/bin/env python3
"""Compile a self-contained program and audit; leave actual visual acceptance open."""
import json
import re
import subprocess

import master_control as core
import review_gap_reader_v13 as layout

ROOT = core.ROOT
BASE = ROOT / 'docs/program/comprehensive-v14'
OUT = BASE / 'program-pdf'
SOURCE = ROOT / 'docs/program/master-program-v14.md'
PDF = SOURCE.with_suffix('.pdf')


def main():
    state = core.read(ROOT, core.STATE)
    if state.get('revision') == '14.0-scoped-dependency-program':
        raise ValueError('Published program is frozen; preserve its PDF bytes')
    OUT.mkdir(parents=True, exist_ok=True)
    body = SOURCE.read_text() + '\n\n\\newpage\n\n' + (BASE / 'gap-audit.md').read_text().replace('# Comprehensive evidence and gap audit', '# Appendix: complete evidence and gap audit', 1)
    # Break prose slash lists in narrow table columns; source files remain exact.
    body = '\n'.join(line.replace('/', '/ ') if line.startswith('|') else line for line in body.splitlines()) + '\n'
    combined = OUT / 'program-and-audit.md'
    combined.write_text(body)
    header = '\n'.join([r'\usepackage{array,microtype,xurl}', r'\emergencystretch=4em',
                        r'\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}',
                        r'\DeclareUnicodeCharacter{2212}{\ensuremath{-}}',
                        r'\DeclareUnicodeCharacter{03B5}{\ensuremath{\varepsilon}}']) + '\n'
    (OUT / 'header.tex').write_text(header)
    tex = OUT / 'master-program.tex'
    subprocess.run(['pandoc', str(combined), '--from=markdown+pipe_tables+raw_tex', '--standalone', '--to=latex',
                    '-H', str(OUT / 'header.tex'), '-V', 'geometry:margin=19mm', '-V', 'fontsize=10pt',
                    '-V', 'colorlinks=true', '-o', str(tex)], check=True, timeout=30)
    raw = tex.read_text()
    for count, widths in [(2, [.22, .78]), (3, [.22, .39, .39]), (4, [.18, .16, .16, .50])]:
        token = r'\begin{longtable}[]{@{}' + 'l' * count + r'@{}}'
        columns = ''.join(r'>{\raggedright\arraybackslash}p{\dimexpr ' + str(w) + r'\linewidth-2\tabcolsep\relax}' for w in widths)
        raw = raw.replace(token, r'\begin{longtable}[]{@{}' + columns + r'@{}}')
    # Source register identifiers remain exact text while offering safe line breaks.
    raw = raw.replace(r'\_', r'\_\allowbreak{}')
    # This pandoc version emits fixed-width minipages inside otherwise natural
    # table columns. After setting column widths, use each cell's own line width.
    raw = re.sub(r'(\\begin\{minipage\}\[[bt]\])\{[0-9.]+\\columnwidth\}', r'\1{\\linewidth}', raw)
    tex.write_text(raw)
    command = ['pdflatex', '-no-shell-escape', '-interaction=batchmode', '-halt-on-error', '-output-directory=' + str(OUT), str(tex)]
    for index in range(2):
        with (OUT / f'pdflatex-{index + 1}.stdout').open('w') as stream:
            subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True, timeout=55)
    log = (OUT / 'master-program.log').read_text()
    warnings = [line for line in log.splitlines() if any(w in line for w in ('Overfull', 'Underfull', 'Warning', 'Missing character'))]
    if any(word in log for word in ('Overfull', 'Missing character', 'undefined references')):
        raise ValueError('Program PDF has unresolved text/layout warnings; inspect saved log')
    PDF.write_bytes((OUT / 'master-program.pdf').read_bytes())
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    report = {'pages': pages, 'pdf': {'path': str(PDF.relative_to(ROOT)), 'sha256': core.sha(PDF), 'anchor': 'Program plus full gap-audit appendix'},
              'warnings': warnings, 'visual_acceptance': False,
              'sources': [{'path': str(p.relative_to(ROOT)), 'sha256': core.sha(p)} for p in (SOURCE, BASE / 'gap-audit.md')]}
    core.write(OUT / 'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    print(json.dumps({'pages': pages, 'warnings': warnings, 'visual_acceptance': False}))


if __name__ == '__main__':
    main()
