#!/usr/bin/env python3
"""Compile available LLM repair chapters as an explicitly interim reader.

No final release claim or rendered visual acceptance is made by this builder.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/program/repair-v12/llm-reader'
WORK=ROOT/'docs/program/repair-v12/work'


def escape(s):
    return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$',
                    '#':r'\#','_':r'\_','{':r'\{','}':r'\}'}.get(c,c) for c in s)


def verify_sources(value):
    if isinstance(value,dict):
        path=value.get('local_path',value.get('path'))
        if path and value.get('sha256'):
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==value['sha256'],path
        for item in value.values():
            verify_sources(item)
    elif isinstance(value,list):
        for item in value:
            verify_sources(item)


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    sources={x['id']:x for x in json.loads((WORK/'LA01/source-audit.json').read_text())['sources']}
    if (WORK/'LA04/source-audit.json').exists():
        sources.update({x['id']:x for x in json.loads((WORK/'LA04/source-audit.json').read_text())['sources']})
    chapters=[WORK/'LA07/translation-chapter.tex',WORK/'LA07/diagram-chapter.tex',
              WORK/'LA03/chapter-draft.tex',WORK/'LA04/chapter-draft.tex',
              WORK/'LA05/chapter-draft.tex',WORK/'LA07/evaluation-chapter.tex']
    assert all(p.exists() for p in chapters)
    # Retain the previously supplied 24-page reader, whose hash is in the
    # recovery record, before extending this mutable interim output.
    old=OUT/'reader.pdf'
    previous=OUT/'reader-after-LA05.pdf'
    if old.exists() and not previous.exists():
        assert hashlib.sha256(old.read_bytes()).hexdigest()=='f2ab8e21d21f2b5b82b372a10edced4fdda0d22815aaef1c0206d4900e6f53d7'
        previous.write_bytes(old.read_bytes())
        (OUT/'build-report-after-LA05.json').write_bytes((OUT/'build-report.json').read_bytes())
    cited=set()
    for chapter in chapters:
        for match in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',chapter.read_text()):
            cited.update(k.strip() for k in match.split(','))
    assert cited<=sources.keys(),cited-sources.keys()
    bib=['\\begin{thebibliography}{99}']
    for key in sorted(cited):
        s=sources[key]
        verify_sources(s)
        if s['kind']=='paper':
            authors=s.get('authors',[])
            author_text=', '.join(authors) if authors else s['first_author']
            desc=escape(s['title'])+'. '+escape(author_text)+' ('+str(s['year'])+'). '
            desc+=escape(s.get('arxiv_version',''))+'. '
        else:
            desc=escape(s['repository'])+r'. Pinned revision \nolinkurl{'+s['commit']+'}. '
            desc+='Revision date '+escape(s['commit_date'])+'. '
        bib.append('\\bibitem{'+key+'} '+desc+'\\url{'+s['url']+'}.')
    bib.append('\\end{thebibliography}')
    (OUT/'references.tex').write_text('\n'.join(bib)+'\n')
    title=r'''\documentclass[11pt,openany]{book}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[a4paper,margin=27mm]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array}
\usepackage{xurl}
\usepackage[hidelinks]{hyperref}
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\title{Language assistance in causal banking\\\large Interim research chapters}
\author{Causal banking research program}
\date{12 October 2026\\Literature cutoff: 7 October 2026}
\begin{document}
\pagestyle{plain}
\raggedbottom
\maketitle
\thispagestyle{empty}
\noindent This reader contains the currently developed business-translation,
diagram, discovery, workflow, prototype and evaluation chapters.
It is an interim author draft, not the completed V12 monograph or a
qualified banking product. Original sources are locally archived and audited;
reported external experiments are distinguished from project analytical examples.
The software survey, full LLM repair, integration chapters and final release
reviews remain separate program obligations. Compilation and text checks do
not constitute final visual review.
\tableofcontents
'''
    content=title+'\n'.join('\\input{'+str(p.relative_to(ROOT))+'}' for p in chapters)
    content+='\n\\label{la:body-end}\\clearpage\n\\input{docs/program/repair-v12/llm-reader/references.tex}\n\\end{document}\n'
    driver=OUT/'reader.tex';driver.write_text(content)
    for i in range(4):
        with (OUT/f'build-{i+1}.log').open('w') as log:
            subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                            '-output-directory='+str(OUT),str(driver)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
        current_log=(OUT/'reader.log').read_text(errors='replace')
        if i>=1 and 'Label(s) may have changed' not in current_log:
            break
    pdf=OUT/'reader.pdf'; txt=OUT/'reader.txt'
    subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True,timeout=30)
    info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
    pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    log=(OUT/'reader.log').read_text(errors='replace')
    warnings=[l for l in log.splitlines() if any(s in l for s in ['Warning','Overfull','Underfull','Missing character'])]
    aux=(OUT/'reader.aux').read_text()
    page_labels={m.group(1):int(m.group(2)) for m in re.finditer(r'\\newlabel\{(la:[^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux)}
    body_pages=page_labels['la:body-end']-page_labels['la:translation']+1
    project_paths=[WORK/'LA02/receipt.json',WORK/'LA02/oracles.json',WORK/'LA02/formalization.md',
                   WORK/'LA02/case-design.md',WORK/'LA06/receipt.json',WORK/'LA06/protocol.json']
    project_records=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in project_paths]
    verify_sources(project_records)
    source_audit={'scope':'Citations and project constructions in six interim chapters; no completed LA07 claim',
                  'sources':[sources[key] for key in sorted(cited)],'project_records':project_records,
                  'chapters':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in chapters]}
    (OUT/'source-audit.json').write_text(json.dumps(source_audit,indent=2)+'\n')
    report={'status':'compiled_text_checks_only','pdf':str(pdf.relative_to(ROOT)),
       'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':pages,'body_pages':body_pages,
       'chapters':[str(p.relative_to(ROOT)) for p in chapters],'cited_primary_records':len(cited),
       'warnings':warnings,'rendered_visual_review':'pending fresh session; current session image budget exhausted',
       'source_audit_sha256':hashlib.sha256((OUT/'source-audit.json').read_bytes()).hexdigest(),
       'chapter_pages':page_labels,'required_body_pages':[96,112],'completed_llm_repair':False,
       'body_count_scope':'Physical body pages; substantive coverage and duplication review still incomplete',
       'final_release':False}
    (OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    build()
