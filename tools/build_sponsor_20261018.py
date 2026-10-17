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
BASE = ROOT / 'docs/program/execution/2026-10-18/sponsor'
OUT = BASE / 'reader'
READER_AUDIT = ROOT / 'docs/program/execution/2026-10-18/bayesian-advice/reader/source-audit.json'
NAME = 'sponsor-proposal'
ref = shared.ref


def write_new(path, value):
    if path.exists():
        raise ValueError('Preserve existing evidence: ' + str(path))
    core.write(path, value)


def prepare():
    from publish_latent_r_review_v2_20261013 import verify_bindings
    OUT.mkdir(parents=True, exist_ok=False)
    state = core.read(ROOT, core.STATE)
    assert state['reader']['path'] == 'docs/causal_proposal_bayesian_advice_reviewed_2026-10-18.pdf'
    write_new(BASE / 'economics-results.json', economics.calculate())
    prior=ROOT/'docs/program/execution/2026-10-13/sponsor/source-audit.json'
    original=json.loads(prior.read_text());verify_bindings(original)
    entries={s['integrated_citation_key']:s for s in original['sources']}
    inherited=json.loads(READER_AUDIT.read_text());verify_bindings(inherited)
    for s in inherited['sources']:
        if s['integrated_citation_key'] not in entries:entries[s['integrated_citation_key']]=s
    records=[
      ('sp18_reader','October18 integrated working monograph: reviewed delivery','docs/program/execution/2026-10-18/bayesian-advice/working-release.json','Exact1060-page reader,751 audited records,197 genuine scholarly PDFs and limited acceptance'),
      ('sp18_commercial','Commercial purchasing comparison and retained omissions','docs/program/execution/2026-10-17/s8/omissions.json','Edition,scope,rights,prices and historical-byte limits'),
      ('sp18_clients','Standalone local library and CLI reference checks','docs/program/execution/2026-10-17/standalone-clients/run-1/results.json','Six actual calls, four replayed set replies, five rejected malformed replies and explicit nonexecution limits'),
      ('sp18_retention','Publication and retention invariant review','docs/program/execution/2026-10-17/integration-review-v1/v3/release-source-review.json','Ten finite orders,three stale-snapshot violations,nine coordinated publications and one safe rejection; no running collector'),
      ('sp18_progress','Current proposal coverage and acceptance boundaries','docs/program/execution/2026-10-18/sponsor/progress-evidence.json','Software and reuse gaps,chapter outcomes,scope and absence of final acceptance'),
      ('sp18_census','Original-candidate primary source census','docs/program/execution/2026-10-18/census-successor/census-register.json','40 inspected,73 unread of113;source-specific limitations and separate citation-chain denominator')]
    for key,title,path,claim in records:
        entries[key]=dict(integrated_citation_key=key,title=title,kind='project_evidence_not_scholarly_paper',author='Causal banking proposal project',year=2026,source_identity=path,version_date='Preserved local project artifact inspected 2026-10-18',local_copy=ref(ROOT/path,claim),inspected_anchors=[dict(anchor=claim,inspection='Author read of the cited artifact and its scoped evidence')],supported_claims=[claim],limits=['Project evidence, not independent review or bank acceptance.'])
    manuscript=(BASE/'proposal.md').read_text()
    cited={key.strip() for group in re.findall(shared.CITE,manuscript) for key in group.split(',')}
    assert cited <= entries.keys(),cited-entries.keys()
    sources=[entries[k] for k in sorted(cited)]
    audit=dict(sources=sources,cutoff='2026-10-07',reader_audit=ref(READER_AUDIT,'Current monograph source audit'),predecessor_audit=ref(prior,'Preserved original sponsor sources'),manuscript=ref(BASE/'proposal.md','Reconciled sponsor argument'),plan_review=ref(BASE/'plan-review.json','Reviewed reconciliation plan'),economics_code=ref(ROOT/'tools/sponsor_economics_20261013.py','Unchanged independent exact arithmetic'),economics_results=ref(BASE/'economics-results.json','Fresh exact replay'))
    verify_bindings(audit);write_new(BASE/'source-audit.json',audit)
    bib=[]
    for source in sources:
        author='Videira, Bruna Bazaluk Machado' if source['integrated_citation_key']=='exec18_videira_thesis' else '{'+shared.escape(source['author'])+'}'
        bib.append('@misc{'+source['integrated_citation_key']+',\n author={'+author+'},\n title={'+shared.escape(source['title'])+'},\n year={'+str(source['year'])+'},\n note={'+shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
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
\fancyhead[R]{18 October 2026}\fancyfoot[C]{\thepage}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\setlength{\emergencystretch}{3em}\raggedbottom
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\begin{document}
\begin{center}{\LARGE\bfseries A shared causal-analysis service\par}\vspace{3mm}
{\large Product and investment proposal\par}\vspace{2mm}
18 October 2026\par Working proposal for review
\end{center}
\input{program/execution/2026-10-18/sponsor/proposal.tex}
\clearpage
\bibliographystyle{plainnat}
\bibliography{program/execution/2026-10-18/sponsor/refs}
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
        with (OUT / name).open('x') as stream:
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
    mirror = docs / 'sponsor_proposal_2026-10-18.pdf'
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
              'paired_monograph': ref(docs / 'causal_proposal_bayesian_advice_reviewed_2026-10-18.pdf', 'Exact 1060-page working reader'),
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
