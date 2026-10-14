#!/usr/bin/env python3
"""Versioned main-book integration of V13 source reviews and worked arguments."""
import argparse
import collections
import contextlib
import io
import json
import os
import re
import subprocess
from pathlib import Path

import master_control as core
import build_integrated_monograph_v12 as old

ROOT=core.ROOT
DOCS=ROOT/'docs'
BASE=ROOT/'docs/program/gap-repair-v13'
OUT=BASE/'reader'
NAME='causal_integrated_working_v13_2026-10-12'
DRIVER=DOCS/(NAME+'.tex')
PDF=DOCS/(NAME+'.pdf')


def ref(path,anchor):return {'path':str(path.relative_to(ROOT)),'sha256':core.sha(path),'anchor':anchor}


def relative(path):return str(path.relative_to(DOCS))


def sources():
    audit=json.loads((BASE/'work/SW01/source-audit.json').read_text())
    entries=[dict(e,integrated_citation_key=e['citation_key']) for e in audit['new_entries']]
    entries.append({'kind':'project_evidence','integrated_citation_key':'v13_project_exact',
                    'source_identity':'Original causal banking project deterministic derivations',
                    'version_date':'12 October 2026','local_copy':ref(ROOT/'tools/gap_design_checks_v13.py','Exact binomial and finite-arithmetic calculations'),
                    'inspected_anchors':[ref(BASE/'work/RG1/design-checks.json','All deterministic outputs'),
                                         ref(BASE/'work/RG1/feasibility.md','Assumptions, derivations and scope limits')],
                    'supported_claims':['Exact stipulated dose and network values, equal-law binary counterexample, policy selection illustration and binomial-screen probabilities.'],
                    'limits':['Not a live or bank experiment; no causal estimator qualified.']})
    return entries


def prepare():
    state=core.read(ROOT,core.STATE)
    if any(r['path']==str(PDF.relative_to(ROOT)) for r in state['deliveries']):
        raise ValueError('Delivered bytes are frozen; create another version')
    OUT.mkdir(parents=True,exist_ok=True)
    raw=(DOCS/'causal_integrated_working_2026-10-12.tex').read_text()
    raw=raw.replace('Integrated working edition','Integrated working edition, revision 13',1)
    marker='The systematic software survey, full depth of the language-model treatment,'
    raw=raw.replace(marker,
        'This revision adds source-grounded comparisons of functional discovery, symbolic identification, estimating equations, longitudinal regimes, continuous doses and network allocation policies. Worked examples extend the treatment of business translation, diagram ambiguity and evaluation. These are developed comparisons and exact illustrative calculations; the newly inspected packages have not been benchmarked here.\n\n'+marker,1)
    software=[BASE/'work/SW01'/p for p in ['discovery-identification.tex','longitudinal-doses.tex','networks-adoption.tex']]
    raw=raw.replace(r'\label{integrated:software-end}',
                    '\n'.join('\\input{'+relative(p)+'}' for p in software)+'\n'+r'\label{integrated:software-end}',1)
    for slug in ['translation','diagram','evaluation']:
        token='\\input{program/repair-v12/work/LA07/'+slug+'-chapter.tex}'
        assert token in raw
        raw=raw.replace(token,token+'\n\\input{'+relative(BASE/'work/LA07'/(slug+'-extension.tex'))+'}',1)
    raw=raw.replace('program/repair-v12/integrated-reader/repair-refs}',
                    'program/repair-v12/integrated-reader/repair-refs,program/gap-repair-v13/reader/new-refs}',1)
    DRIVER.write_text(raw)
    bibliography=[]
    for entry in sources():
        key=entry['integrated_citation_key']
        if entry['kind']=='project_evidence':
            author='{Causal banking research project}'
            title='Deterministic causal decision examples and qualification-design calculations'
            url=''
            note='Original project derivations; no package, live model or bank qualification'
        else:
            author='{'+old.escape(entry['name'])+' project}'
            title=old.escape(entry['name']+': inspected technical source and licensing record')
            url=entry['source_identity']
            note=old.escape('Commit '+entry['version_date']['commit']+'; '+entry['version_date']['commit_date'][:10]+
                            '; retrieved '+entry['version_date']['retrieved'][:10]+'. Selected source inspection; runtime untested')
        bibliography.append('@misc{'+key+',\n  author = {'+author+'},\n  title = {'+title+'},\n  year = {2026},\n  note = {'+note+'}'+
                            (',\n  url = {'+url+'}' if url else '')+'\n}\n')
    (OUT/'new-refs.bib').write_text('\n'.join(bibliography))


def build():
    with contextlib.redirect_stdout(io.StringIO()):old.check()
    prepare()
    env=dict(os.environ)
    env['TEXINPUTS']=str(DOCS)+'//:'+env.get('TEXINPUTS','')
    env['BIBINPUTS']=str(DOCS)+'//:'+env.get('BIBINPUTS','')
    latex=['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
           '-output-directory='+str(OUT),str(DRIVER)]
    def run(cmd,logname):
        with (OUT/logname).open('w') as stream:
            p=subprocess.run(cmd,cwd=DOCS,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=90)
        if p.returncode:raise ValueError('Build failed; inspect '+str(OUT/logname))
    run(latex,'pass-1.log')
    run(['bibtex',str((OUT/NAME).relative_to(DOCS))],'bibtex-pass.log')
    for i in range(2,6):
        run(latex,'pass-'+str(i)+'.log')
        log=(OUT/(NAME+'.log')).read_text(errors='replace')
        if i>=3 and not any(s in log for s in ['Label(s) may have changed','Rerun to get']):break
    PDF.write_bytes((OUT/(NAME+'.pdf')).read_bytes())
    warnings=[l for l in log.splitlines() if any(w in l for w in ['Warning','Overfull','Underfull','Missing character'])]
    if any(w in log for w in ['undefined citations','undefined references','multiply defined','Missing character']):
        raise ValueError('Unresolved reference or character warning')
    files=old.scan(DRIVER)
    combined='\n'.join(t for p,t in files)
    labels=re.findall(old.LABEL,combined)
    if len(labels)!=len(set(labels)):raise ValueError('Duplicate labels')
    refs=set(re.findall(r'\\(?:ref|eqref|cref|Cref)\{([^}]+)\}',combined))
    if refs-set(labels):raise ValueError('Unresolved labels '+str(refs-set(labels)))
    citations={k.strip() for g in re.findall(old.CITE,combined) for k in g.split(',')}
    inherited=json.loads((old.OUT/'source-audit.json').read_text())
    entries={e['integrated_citation_key']:e for e in inherited['sources']}
    entries.update({e['integrated_citation_key']:e for e in sources()})
    if not citations<=entries.keys():raise ValueError('Missing source audit '+str(citations-entries.keys()))
    audit={'predecessor_audit':ref(old.OUT/'source-audit.json','Unchanged inherited citation, figure and source identities'),
           'sources':[entries[k] for k in sorted(citations)],
           'tex_files':[ref(p,'Complete integrated TeX source') for p in sorted({p for p,t in files})],
           'new_bibliography':ref(OUT/'new-refs.bib','Eleven new source/project records'),
           'survey_audit':ref(BASE/'work/SW01/source-audit.json','Ten new scoped primary source reviews'),
           'survey_builder':ref(ROOT/'tools/inspect_gap_sources_v13.py','Authored claim and evidence records'),
           'cutoff':'2026-10-07','visual_acceptance':False}
    old.verify_refs(audit)
    core.write(OUT/'source-audit.json',audit)
    subprocess.run(['pdftotext','-layout',str(PDF),str(OUT/'reader.txt')],check=True,timeout=30)
    info=subprocess.check_output(['pdfinfo',str(PDF)],text=True,timeout=15)
    pages=int(re.search(r'(?m)^Pages:\s+(\d+)',info).group(1))
    aux=(OUT/(NAME+'.aux')).read_text()
    page_labels={m.group(1):int(m.group(2)) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux)}
    body={'software':page_labels['integrated:software-end']-page_labels['sw:interfaces']+1,
          'llm':page_labels['integrated:llm-end']-page_labels['la:frontier']+1,
          'integration':page_labels['integrated:integration-end']-page_labels['in:semantics']+1}
    toc=(OUT/(NAME+'.toc')).read_text()
    chapters=len(re.findall(r'\\contentsline \{chapter\}\{\\numberline',toc))
    report={'status':'compiled_source_and_text_checked_working_draft','pdf':ref(PDF,'Unified successor main monograph'),
            'driver':ref(DRIVER,'Versioned integrated driver'),'source_audit':ref(OUT/'source-audit.json','Whole successor audit'),
            'builder':ref(Path(__file__),'Versioned main-book builder and checker'),
            'predecessor_pdf':ref(old.PDF,'Preserved 345-page predecessor'),
            'pages':pages,'numbered_chapters':chapters,'cited_records':len(citations),'physical_body_pages':body,
            'source_files':len(audit['tex_files']),'warnings':warnings,'final_release':False,'mandatory_repairs_closed':[],
            'body_page_status':'Physical spans; accepted substantive counts remain pending coverage and duplication review',
            'visual_review':'Pending fresh session under exhausted inherited image allowance'}
    core.write(OUT/'build-report.json',report)
    print(json.dumps({k:report[k] for k in ['status','pages','numbered_chapters','cited_records','physical_body_pages','warnings']}))


def check(binding=None):
    if binding:core.bound(ROOT,binding)
    report=core.read(ROOT,binding['path'] if binding else str((OUT/'build-report.json').relative_to(ROOT)))
    old.verify_refs(report)
    audit=core.read(ROOT,report['source_audit']['path']);old.verify_refs(audit)
    raw='\n'.join(t for _,t in old.scan(ROOT/report['driver']['path']))
    cited={k.strip() for g in re.findall(old.CITE,raw) for k in g.split(',')}
    if cited!={e['integrated_citation_key'] for e in audit['sources']}:raise ValueError('Citation/audit mismatch')
    actual_info=subprocess.check_output(['pdfinfo',str(ROOT/report['pdf']['path'])],text=True,timeout=15)
    actual_pages=int(re.search(r'(?m)^Pages:\s+(\d+)',actual_info).group(1))
    if actual_pages!=report['pages']:raise ValueError('Reader page count mismatch')
    current=core.read(ROOT,core.STATE)
    if current.get('successor_document') and current['successor_document']['path']==str((OUT/'build-report.json').relative_to(ROOT)):
        if (current['reader']['path']!=report['pdf']['path'] or current['reader']['pages']!=report['pages'] or
                current['reader']['sha256']!=report['pdf']['sha256']):
            raise ValueError('Current reader differs from checked successor')
    return {'status':'pass','pages':report['pages'],'cited_records':len(cited),'final_acceptance':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['build','check'])
    if p.parse_args().command=='build':build()
    else:print(json.dumps(check()))
