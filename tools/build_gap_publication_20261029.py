from pathlib import Path
from hashlib import sha256
import argparse
import json
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
OUT=DOCS/'scientific-gap-closure/2026-10-29'
PREFIX='scientific-gap-closure/2026-10-29/'
NAMES={'short':'causal_banking_public_evidence_2026-10-29','integrated':'causal_banking_scientific_progress_2026-10-29'}

def digest(p):return sha256(p.read_bytes()).hexdigest()

def prepare():
    old=DOCS/'causal_banking_developmental_rewrite_2026-10-29.tex'
    original=old.read_text()
    new=original
    for before,addition in [('decision-evidence','public-study'),('assistance-decisions','measurement'),('software-decisions','software-followup')]:
        marker=r'\input{developmental-rewrite/2026-10-29/retained/scientific-synthesis/2026-10-29/'+before+'.tex}'
        assert new.count(marker)==1
        new=new.replace(marker,marker+chr(10)+r'\input{'+PREFIX+addition+'}')
    marker=r'\input{'+PREFIX+'public-study}'
    new=new.replace(marker,marker+''.join(chr(10)+r'\input{'+PREFIX+x+'}' for x in ['servicing','policy-uncertainty','funding','observation']))
    marker=r'\input{'+PREFIX+'measurement}'
    new=new.replace(marker,marker+chr(10)+r'\input{'+PREFIX+'frontier}')
    new=new.replace(r'\large Developmental rewrite',r'\large Scientific continuation of the developmental rewrite')
    new=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+PREFIX+'refs,'+PREFIX+'frontier-refs}',new)
    assert PREFIX+'refs' in new
    (DOCS/(NAMES['integrated']+'.tex')).write_text(new)
    bibliography=re.search(r'\\bibliography\{[^}]+\}',new).group(0)
    short=r'''\documentclass[11pt,a4paper,openany]{book}
\input{preamble}
\raggedbottom
\title{\sffamily\bfseries\color{ink}Causal Inference for Banking\\[12pt]
\Large Public evidence, measurement and defensible decisions}
\author{Research and product proposal}
\date{29 October 2026\\Literature cutoff: 7 October 2026}
\begin{document}
\maketitle\tableofcontents
'''+''.join(r'\input{'+PREFIX+x+'}'+chr(10) for x in ['public-study','servicing','policy-uncertainty','funding','observation','measurement','frontier','software-followup'])+r'\bibliographystyle{plainnat}'+chr(10)+bibliography+chr(10)+r'\end{document}'+chr(10)
    (DOCS/(NAMES['short']+'.tex')).write_text(short)
    protected=['docs/program/master-program.md','docs/program/state.json','README.md','tools/causal_program.py',
        'docs/causal_banking_reading_edition_2026-10-29.pdf','docs/causal_banking_scientific_continuation_2026-10-29.pdf',
        str(old.relative_to(ROOT))]
    protected+=['docs/causal_banking_developmental_rewrite_2026-10-29.pdf',
                'docs/causal_banking_sponsor_rewrite_2026-10-29.pdf']
    previous=json.loads((OUT/'publication-baseline.json').read_text()) if (OUT/'publication-baseline.json').exists() else {}
    assert all(digest(ROOT/p)==h for p,h in previous.items()),'Existing protected baseline changed'
    baseline={**previous,**{p:digest(ROOT/p) for p in protected}}
    (OUT/'publication-baseline.json').write_text(json.dumps(baseline,indent=2)+chr(10))
    print(json.dumps(dict(prepared=list(NAMES.values()),protected=len(protected))))

def build(which):
    name=NAMES[which];folder=OUT/('build-'+which);folder.mkdir(exist_ok=True)
    cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory='+str(folder),name+'.tex']
    commands=[cmd,['bibtex',str((folder/name).relative_to(DOCS))],cmd,cmd,cmd]
    runs=[]
    for i,command in enumerate(commands):
        start=time.monotonic();log=folder/f'pass-{i+1}.txt'
        with log.open('w') as f:p=subprocess.run(command,cwd=DOCS,stdout=f,stderr=subprocess.STDOUT,timeout=180)
        runs.append(dict(command=command,exit_code=p.returncode,seconds=round(time.monotonic()-start,2),log=str(log.relative_to(ROOT))))
        (OUT/('build-'+which+'.json')).write_text(json.dumps(runs,indent=2)+chr(10))
        print(json.dumps(dict(document=which,pass_number=i+1,exit_code=p.returncode,seconds=runs[-1]['seconds'])),flush=True)
        if p.returncode:
            print(chr(10).join(log.read_text(errors='replace').splitlines()[-18:]));raise SystemExit(p.returncode)
    baseline=json.loads((OUT/'publication-baseline.json').read_text())
    assert all(digest(ROOT/p)==h for p,h in baseline.items()),'Protected predecessor changed'
    pdf=DOCS/(name+'.pdf');pdf.write_bytes((folder/(name+'.pdf')).read_bytes())
    print(json.dumps(dict(pdf=str(pdf.relative_to(ROOT)),sha256=digest(pdf),protected_unchanged=True)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','short','integrated']);a=p.parse_args()
    prepare() if a.command=='prepare' else build(a.command)
