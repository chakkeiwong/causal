"""Publish scientific additions without editing the reading edition under review."""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
OUT=DOCS/'scientific-synthesis/2026-10-29'
BASE=DOCS/'causal_banking_reading_edition_2026-10-29.tex'
PREFIX='scientific-synthesis/2026-10-29/'
CHAPTERS=['software-decisions','decision-evidence','assistance-decisions','practical-investment']


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def prepare():
    original=BASE.read_text()
    bibliography=re.search(r'\\bibliography\{[^}]+\}',original).group(0)
    supplement=r'''\documentclass[11pt,a4paper,openany]{book}
\input{preamble}
\raggedbottom
\title{\sffamily\bfseries\color{ink}Causal Inference for Banking\\[12pt]
\Large Software choices, decision evidence and the next investment}
\hypersetup{pdftitle={Causal Inference for Banking: Software Choices and Decision Evidence}}
\author{Scientific supplement to the integrated research proposal}
\date{29 October 2026\\Literature cutoff: 7 October 2026}
\begin{document}
\maketitle\tableofcontents
'''
    supplement+='\n'.join(r'\input{'+PREFIX+c+'}' for c in CHAPTERS)
    supplement+='\n'+r'\bibliographystyle{plainnat}'+'\n'+bibliography+'\n'+r'\end{document}'+'\n'
    short=DOCS/'causal_banking_scientific_supplement_2026-10-29.tex'
    short.write_text(supplement)
    successor=original.replace(r'\input{reading-edition/software-conclusions}',
               r'\input{reading-edition/software-conclusions}'+'\n'+r'\input{'+PREFIX+'software-decisions}')
    successor=successor.replace(r'\input{reading-edition/assistance-conclusions}',
               r'\input{reading-edition/assistance-conclusions}'+'\n'+r'\input{'+PREFIX+'assistance-decisions}')
    successor=successor.replace(r'\part{Public evidence and banking studies}',
               r'\part{Public evidence and banking studies}'+'\n'+r'\input{'+PREFIX+'decision-evidence}')
    successor=successor.replace(r'\part{The investment decision}',
               r'\part{The investment decision}'+'\n'+r'\input{'+PREFIX+'practical-investment}')
    successor=successor.replace('Decisions, evidence and the case for a shared analytical service',
                               'Decisions, evidence and the case for a shared analytical service\\\\[8pt]\\large Scientific continuation')
    full=DOCS/'causal_banking_scientific_continuation_2026-10-29.tex'
    full.write_text(successor)
    tracked={str(BASE.relative_to(ROOT)):digest(BASE)}
    for name in re.findall(r'\\input\{(reading-edition/[^}]+)\}',original):
        p=DOCS/(name if name.endswith('.tex') else name+'.tex');tracked[str(p.relative_to(ROOT))]=digest(p)
    for row in json.loads((DOCS/'reading-edition/source-map.json').read_text()):
        for key in ['original','reading_copy']:
            p=ROOT/row[key];tracked[row[key]]=digest(p)
    baseline_pdf=BASE.with_suffix('.pdf')
    tracked[str(baseline_pdf.relative_to(ROOT))]=digest(baseline_pdf)
    (OUT/'integration-baseline.json').write_text(json.dumps(tracked,indent=2)+'\n')
    print(json.dumps({'prepared':[str(short.relative_to(ROOT)),str(full.relative_to(ROOT))],
                      'baseline_files_preserved':len(tracked),'added_chapters':4}))


def build(which):
    stem='causal_banking_scientific_'+('supplement' if which=='supplement' else 'continuation')+'_2026-10-29'
    build_dir=OUT/('build-'+which);build_dir.mkdir(exist_ok=True)
    cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
         '-output-directory='+str(build_dir),stem+'.tex']
    commands=[cmd,['bibtex',str((build_dir/stem).relative_to(DOCS))],cmd,cmd]
    results=[]
    for i,command in enumerate(commands):
        started=time.monotonic();log=build_dir/('pass-'+str(i+1)+'.txt')
        with log.open('w') as f:
            proc=subprocess.run(command,cwd=DOCS,stdout=f,stderr=subprocess.STDOUT,timeout=180)
        results.append({'pass':i+1,'exit_code':proc.returncode,'seconds':round(time.monotonic()-started,2),'log':str(log.relative_to(ROOT))})
        (OUT/('build-'+which+'.json')).write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(results[-1]),flush=True)
        if proc.returncode:
            print('\n'.join(log.read_text(errors='replace').splitlines()[-25:]));raise SystemExit(proc.returncode)
    baseline=json.loads((OUT/'integration-baseline.json').read_text())
    changed=[p for p,h in baseline.items() if digest(ROOT/p)!=h]
    if changed:raise RuntimeError('Editorial baseline changed during build: '+str(changed[:5]))
    target=DOCS/(stem+'.pdf');target.write_bytes((build_dir/(stem+'.pdf')).read_bytes())
    print(json.dumps({'pdf':str(target.relative_to(ROOT)),'sha256':digest(target),'baseline_unchanged':True}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','supplement','integrated']);a=p.parse_args()
    prepare() if a.command=='prepare' else build(a.command)
