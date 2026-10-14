#!/usr/bin/env python3
"""Build a versioned sponsor proposal with traceable evidence and bounded logs."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

import build_integrated_monograph_v12 as shared
import master_control as core
import sponsor_economics_20261013 as economics

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/sponsor'
OUT = ROOT / 'docs/program/comprehensive-v14/work/RELEASE.SPONSOR'
READER_AUDIT = ROOT / 'docs/program/execution/2026-10-13/commercial-latent/reader/source-audit.json'
NAME = 'sponsor-proposal'
ref = shared.ref


def write_new(path, value):
    if path.exists():
        raise ValueError('Preserve existing evidence: ' + str(path))
    core.write(path, value)


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    state = core.read(ROOT, core.STATE)
    assert state['reader']['sha256'] == '021111a38ac7ccb53cf0a6dc5a39bfc9ae1be6afd213bd99fad0ffe0eaf9b351'
    write_new(BASE / 'economics-results.json', economics.calculate())
    interfaces = [ROOT / f'docs/program/comprehensive-v14/work/IN.DESIGN.{lang}/adapter-contract.json'
                  for lang in ['R', 'Python', 'Java']]
    interfaces += [ROOT / state['results'][key]['path'] for key in ['IN01', 'IN04', 'LA05', 'LA06']]
    write_new(BASE / 'interface-evidence.json', {
        'scope': 'Selected adapter designs and earlier local prototypes; no sibling adoption or general runtime admission',
        'evidence': [ref(p, 'Inspected contract or scoped author receipt') for p in interfaces]})
    designs = [ROOT / f'docs/program/public-data-v15/studies/P{i}/design.json' for i in range(1, 7)]
    write_new(BASE / 'public-design-evidence.json', {
        'scope': 'Six author-reviewed designs, not final study registration or new empirical results',
        'final_study_executed': False, 'bank_inputs_required': False,
        'evidence': [ref(p, 'Actual public/generated study design') for p in designs]})
    choices = [ROOT / f'docs/program/comprehensive-v14/work/SW.DECISION.{key}/decision.json'
               for key in ['inherited_dowhy', 'seed_071']]
    write_new(BASE / 'reuse-evidence.json', {
        'scope': 'Source-backed reuse decisions; installed engines not admitted by design completion',
        'evidence': [ref(p, 'Scoped engine reuse decision') for p in choices]})
    records = [
        ('sp13_scope', 'Current proposal scope and public-evidence portfolio',
         'docs/program/master-program-proposal.md', 'Proposal standard, three repairs and later conditional evidence'),
        ('sp13_reader', '475-page integrated causal banking working monograph: delivery evidence',
         'docs/program/execution/2026-10-13/commercial-latent/working-release.json', 'Reader identity and incomplete proposal acceptance'),
        ('sp13_interfaces', 'Selected causal interfaces and prototype evidence',
         'docs/program/execution/2026-10-13/sponsor/interface-evidence.json', 'Adapter design boundaries, local prototypes and absence of sibling adoption'),
        ('sp13_funding', 'Independent-calendar funding construction: author review',
         'docs/program/master/work/R01/review.md', 'Six valid-law coverage outcomes, supplied information and adverse cases'),
        ('sp13_persistence', 'Persistent-map confidence-region argument: author review',
         'docs/program/execution/2026-10-13/research/argument-author-review.json', 'Restricted conservative argument, precision limit and no numerical qualification'),
        ('sp13_servicing', 'Selected nonlinear fixed-policy servicing: author review',
         'docs/program/master/work/R03/review.md', 'Selected17 information law, fixed policy and wrong-logger/leakage failures'),
        ('sp13_servicing_successor', 'Finite-history servicing argument: author review',
         'docs/program/execution/2026-10-13/servicing/argument-author-review.json', 'Estimated probabilities, bounded proof, exact examples and incompatible continuous design'),
        ('sp13_public', 'Six public and generated study designs: evidence index',
         'docs/program/execution/2026-10-13/sponsor/public-design-evidence.json', 'Six study families and actual versus proposed behavior'),
        ('sp13_choices', 'Selected symbolic-engine reuse decisions: evidence index',
         'docs/program/execution/2026-10-13/sponsor/reuse-evidence.json', 'Restricted y0 integration and deferred DoWhy executable admission'),
        ('sp13_commercial', 'Commercial latent-variable coverage: omissions and revisit actions',
         'docs/program/execution/2026-10-13/commercial-latent/omissions-register.json', 'Five essential unresolved vendor leads and no market-wide absence finding'),
        ('sp13_economics', 'Decision value and the cost of resolving uncertainty',
         'docs/program/comprehensive-v14/work/ECON.DESIGN/argument.md', 'Assumed investment and information values; costs and decision rules'),
        ('sp13_economics_sensitivity', 'Exact sponsor planning arithmetic and sensitivities',
         'docs/program/execution/2026-10-13/sponsor/economics-results.json', 'Independent rational replay and volume/review-cost break-even values')]
    sources = []
    for key, title, path, claim in records:
        sources.append({'integrated_citation_key': key, 'title': title,
                        'kind': 'project_evidence_not_scholarly_paper',
                        'author': 'Causal banking proposal project', 'year': 2026,
                        'source_identity': path, 'version_date': 'Preserved local project artifact inspected 2026-10-13',
                        'local_copy': ref(ROOT / path, claim),
                        'inspected_anchors': [{'anchor': claim, 'inspection': 'Author read of the cited artifact and its scoped evidence'}],
                        'supported_claims': [claim], 'limits': ['Project evidence, not independent review or bank acceptance.']})
    manuscript = (BASE / 'proposal.md').read_text()
    cited = {key.strip() for group in re.findall(shared.CITE, manuscript) for key in group.split(',')}
    inherited = {s['integrated_citation_key']: s for s in json.loads(READER_AUDIT.read_text())['sources']}
    present = {s['integrated_citation_key'] for s in sources}
    assert cited - present <= inherited.keys()
    sources += [inherited[key] for key in sorted(cited - present)]
    assert cited == {s['integrated_citation_key'] for s in sources}
    audit = {'sources': sources, 'cutoff': '2026-10-07',
             'reader_audit': ref(READER_AUDIT, 'Preserved source records; imported vendor entries unchanged'),
             'manuscript': ref(BASE / 'proposal.md', 'Sponsor argument'),
             'economics_code': ref(ROOT / 'tools/sponsor_economics_20261013.py', 'Independent exact arithmetic'),
             'preserved_economics_code': ref(ROOT / 'tools/proposal_economics_example.py', 'Existing assumed scenario'),
             'preserved_economics_results': ref(ROOT / 'docs/program/comprehensive-v14/work/ECON.DESIGN/illustration.json', 'Existing planning values')}
    shared.verify_refs(audit)
    write_new(BASE / 'source-audit.json', audit)
    bib = []
    for source in sources:
        bib.append('@misc{' + source['integrated_citation_key'] + ',\n author={{' + shared.escape(source['author']) +
                   '}},\n title={' + shared.escape(source['title']) + '},\n year={' + str(source['year']) +
                   '},\n note={' + shared.escape(source['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash', '--to=latex',
                    '--top-level-division=section', '--wrap=auto', str(BASE / 'proposal.md'),
                    '-o', str(BASE / 'proposal.tex')], check=True, timeout=20)
    driver = r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,amsmath,amssymb,booktabs,array,longtable,microtype,xcolor}
\usepackage[margin=24mm,headheight=15pt]{geometry}
\usepackage[round,authoryear]{natbib}
\usepackage{xurl,hyperref,fancyhdr}
\hypersetup{colorlinks=true,urlcolor=blue!50!black,citecolor=blue!50!black,
pdftitle={A shared causal-analysis service: product and investment proposal},pdfauthor={Causal banking proposal project}}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{Causal banking: product proposal}
\fancyhead[R]{13 October 2026}\fancyfoot[C]{\thepage}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\setlength{\emergencystretch}{3em}\raggedbottom
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\begin{document}
\begin{center}{\LARGE\bfseries A shared causal-analysis service\par}\vspace{3mm}
{\large Product and investment proposal\par}\vspace{2mm}
13 October 2026\par Working proposal for review
\end{center}
\input{program/execution/2026-10-13/sponsor/proposal.tex}
\clearpage
\bibliographystyle{plainnat}
\bibliography{program/execution/2026-10-13/sponsor/refs}
\end{document}
'''
    (OUT / (NAME + '.tex')).write_text(driver)
    print(json.dumps({'prepared': str(OUT.relative_to(ROOT)), 'citations': len(cited)}))


def build():
    if (BASE / 'build-report.json').exists():
        raise ValueError('Preserve recorded build; use a successor for changes')
    docs = ROOT / 'docs'
    driver = OUT / (NAME + '.tex')
    command = ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-no-shell-escape',
               '-output-directory', str(OUT), str(driver)]
    def execute(args, name):
        with (OUT / name).open('w') as stream:
            subprocess.run(args, cwd=docs, stdout=stream, stderr=subprocess.STDOUT,
                           check=True, timeout=55)
    execute(command, 'pass-1.log')
    execute(['bibtex', str((OUT / NAME).relative_to(docs))], 'bibtex-pass.log')
    for i in range(2, 5):
        execute(command, f'pass-{i}.log')
        log = (OUT / (NAME + '.log')).read_text(errors='replace')
        if i >= 3 and not any(token in log for token in ['Label(s) may have changed', 'Rerun to get']):
            break
    tokens = ['undefined citations', 'undefined references', 'multiply defined', 'Missing character', 'Overfull']
    assert not any(token in log for token in tokens), 'Review build warnings'
    pdf = OUT / (NAME + '.pdf')
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    subprocess.run(['pdftotext', '-layout', str(pdf), str(BASE / 'reader.txt')], check=True, timeout=20)
    subprocess.run(['pdftotext', '-bbox', str(pdf), str(BASE / 'reader-bbox.html')], check=True, timeout=20)
    tree = ET.fromstring((BASE / 'reader-bbox.html').read_text())
    ns = {'h': 'http://www.w3.org/1999/xhtml'}
    bad, empty = [], []
    for i, page in enumerate(tree.findall('.//h:page', ns), 1):
        words = page.findall('.//h:word', ns)
        if not words:
            empty.append(i)
        for w in words:
            if (float(w.attrib['xMin']) < 0 or float(w.attrib['yMin']) < 0
                    or float(w.attrib['xMax']) > float(page.attrib['width'])
                    or float(w.attrib['yMax']) > float(page.attrib['height'])):
                bad.append({'page': i, 'word': w.text})
    assert not bad and not empty
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    assert json.loads((BASE / 'economics-results.json').read_text()) == economics.calculate()
    mirror = docs / 'sponsor_proposal_2026-10-13.pdf'
    if mirror.exists():
        raise ValueError('Preserve existing sponsor delivery')
    mirror.write_bytes(pdf.read_bytes())
    report = {'status': 'compiled_source_and_text_checked_working_proposal', 'pages': pages,
              'pdf': ref(pdf, 'Declared sponsor operation output'),
              'reader_copy': ref(mirror, 'Convenient exact-byte sponsor copy'),
              'source_audit': ref(BASE / 'source-audit.json', 'All cited identities'),
              'driver': ref(driver, 'Sponsor LaTeX driver'),
              'manuscript': ref(BASE / 'proposal.md', 'Reviewed sponsor source'),
              'compiled_content': ref(BASE / 'proposal.tex', 'Compiled sponsor source'),
              'bibliography': ref(BASE / 'refs.bib', 'Source and project-evidence bibliography'),
              'builder': ref(Path(__file__), 'Bounded preserving sponsor build'),
              'paired_monograph': ref(docs / 'causal_proposal_latent_commercial_2026-10-13.pdf', 'Exact 475-page working reader'),
              'cited_records': len(audit['sources']), 'text_bounds_issues': bad, 'empty_pages': empty,
              'warnings': [line for line in log.splitlines() if any(t in line for t in ['Warning', 'Underfull'])],
              'visual_acceptance': False, 'visual_limit': 'Inherited six-preview session allowance exhausted',
              'final_proposal_acceptance': False, 'bank_product_acceptance': False}
    write_new(BASE / 'build-report.json', report)
    print(json.dumps({'pages': pages, 'cited_records': len(audit['sources']),
                      'pdf': str(mirror.relative_to(ROOT)), 'warnings': report['warnings'],
                      'visual_acceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
