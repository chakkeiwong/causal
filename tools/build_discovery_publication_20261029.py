"""Publish the discovery study from a frozen copy of the current reader."""
from pathlib import Path
from collections import Counter
import hashlib, json, os, re, shutil, subprocess, time
import xml.etree.ElementTree as ET
R = Path(__file__).resolve().parents[1]
D = R / 'docs'
O = D / 'discovery-repair/2026-10-29'
S = O / 'publication/snapshot/docs'
ORIGINAL = 'causal_banking_integrated_argument_2026-10-29'
NAMES = {'full': 'causal_banking_discovery_integrated_2026-10-29',
         'short': 'causal_banking_discovery_repair_2026-10-29'}
INPUT = re.compile(r'\\(?:input|include)\{([^}]+)\}')
BIB = re.compile(r'\\bibliography\{([^}]+)\}')
STYLE = re.compile(r'\\bibliographystyle\{([^}]+)\}')
GRAPHIC = re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}')
CHAPTER = 'discovery-repair/2026-10-29/chapter.tex'
ANCHOR = r'\input{writing-repair/2026-10-29/src/715d8b709beaf962.tex}'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2)+'\n')
def path(root,name,suffix='.tex'):
    p=root/name
    if not p.suffix:p=p.with_suffix(suffix)
    assert p.is_file(),str(p)
    return p
def tree(root,p,stack=()):
    assert p not in stack,'Circular input: '+str(p)
    result=[p]
    for name in INPUT.findall(p.read_text()):result+=tree(root,path(root,name),stack+(p,))
    return result
def integrate(raw):
    assert raw.count(ANCHOR)==1
    full=raw.replace(ANCHOR,ANCHOR+'\n'+r'\input{'+CHAPTER+'}')
    return BIB.sub(lambda m:r'\bibliography{'+m[1]+',discovery-repair/2026-10-29/refs}',full)
def prepare():
    assert not (O/'publication/baseline.json').exists(),'Snapshot exists; retain it.'
    root=D/(ORIGINAL+'.tex');sources=tree(D,root);raw=root.read_text()
    files=set(sources);bibs=[]
    for p in sources:
        text=p.read_text()
        for group in BIB.findall(text):
            for name in group.split(','):
                q=path(D,name.strip(),'.bib');bibs.append(q);files.add(q)
        for name in STYLE.findall(text):files.add(path(D,name,'.bst'))
        for name in GRAPHIC.findall(text):
            q=D/name
            choices=[q] if q.suffix else [q.with_suffix(s) for s in ['.pdf','.png','.jpg','.jpeg']]
            selected=next((x for x in choices if x.is_file()),None)
            assert selected,'Missing graphic: '+name
            files.add(selected)
    files.update([D/CHAPTER,O/'refs.bib'])
    fls=D/('writing-repair/2026-10-29/build-full/'+ORIGINAL+'.fls')
    for line in fls.read_text().splitlines():
        if line.startswith('INPUT '):
            p=Path(line[6:]);p=(p if p.is_absolute() else D/p).resolve()
            if p.is_relative_to(D) and p.suffix in {'.tex','.pdf','.png','.jpg','.sty','.cls','.bst'}:files.add(p)
    hashes={}
    for p in sorted(files):
        relative=p.relative_to(D);q=S/relative;q.parent.mkdir(parents=True,exist_ok=True)
        data=p.read_bytes();q.write_bytes(data);hashes[str(relative)]=hashlib.sha256(data).hexdigest()
    changed=[n for n,h in hashes.items() if sha(D/n)!=h]
    assert not changed,'Source changed during snapshot: '+repr(changed)
    (S/(NAMES['full']+'.tex')).write_text(integrate(raw))
    prefix=raw.split(r'\begin{document}',1)[0]
    short=prefix+'\n'+r'''\title{\sffamily\bfseries\color{ink}Causal discovery for banking\\[14pt]\Large Search completeness and adjustment}
\hypersetup{pdftitle={Causal discovery for banking: Search completeness and adjustment}}
\begin{document}
\frontmatter
\maketitle
\mainmatter
\input{discovery-repair/2026-10-29/chapter.tex}
\backmatter
\bibliographystyle{program/execution/2026-10-13/interfaces/causalplainnat}
\bibliography{discovery-repair/2026-10-29/refs}
\end{document}
'''
    (S/(NAMES['short']+'.tex')).write_text(short)
    save(O/'publication/baseline.json',{'source_root':str(root.relative_to(R)),
      'source_pdf_sha256':sha(D/(ORIGINAL+'.pdf')),'source_occurrences':[str(p.relative_to(D)) for p in sources],
      'files':hashes,'bibliographies':[str(p.relative_to(D)) for p in bibs],'snapshot':str(S.relative_to(R)),
      'insertion':'After discovery treatment, before observation-process treatment',
      'scope':'Exact inherited snapshot; one added chapter and bibliography','source_changed_during_capture':changed})
    print(json.dumps({'snapshot_files':len(hashes),'tex_occurrences':len(sources)}),flush=True)
def build(kind):
    assert (O/'publication/baseline.json').is_file()
    stem=NAMES[kind];folder=O/('publication/build-'+kind);folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'passes.json').exists(),'Retain old build; inspect before retry.'
    cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder',
         '-output-directory='+str(folder),stem+'.tex']
    commands=[cmd,['bibtex',stem],cmd,cmd];results=[]
    env=dict(os.environ,BIBINPUTS=str(S)+'//:',BSTINPUTS=str(S)+'//:')
    for i,command in enumerate(commands,1):
        log=folder/f'pass-{i}.txt';start=time.monotonic()
        with log.open('w') as f:p=subprocess.run(command,cwd=folder if command[0]=='bibtex' else S,
          env=env,stdout=f,stderr=subprocess.STDOUT,timeout=300)
        row={'pass':i,'returncode':p.returncode,'seconds':round(time.monotonic()-start,2),'log':str(log.relative_to(R))}
        results.append(row);save(folder/'passes.json',results);print(json.dumps(row),flush=True)
        if p.returncode:
            print('\n'.join(log.read_text(errors='replace').splitlines()[-25:]));raise SystemExit(p.returncode)
    target=D/(stem+'.pdf');assert not target.exists(),'Do not overwrite published PDF.'
    shutil.copyfile(folder/(stem+'.pdf'),target)
    print(json.dumps({'pdf':str(target.relative_to(R)),'sha256':sha(target)}),flush=True)
def audit():
    base=json.loads((O/'publication/baseline.json').read_text());issues=[]
    changed=[n for n,h in base['files'].items() if sha(S/n)!=h]
    if changed:issues.append('Snapshot files changed')
    if (S/(NAMES['full']+'.tex')).read_text()!=integrate((S/(ORIGINAL+'.tex')).read_text()):issues.append('Unexpected root edit')
    inherited=Counter(base['source_occurrences'][1:])
    actual=Counter(str(p.relative_to(S)) for p in tree(S,S/(NAMES['full']+'.tex'))[1:])
    missing=dict(inherited-actual);added=dict(actual-inherited)
    if missing or added!={CHAPTER:1}:issues.append('Unexpected input difference')
    reports={}
    for kind,stem in NAMES.items():
        folder=O/('publication/build-'+kind);pdf=D/(stem+'.pdf');log=(folder/(stem+'.log')).read_text(errors='replace')
        warnings={w:len(re.findall(w,log,re.I)) for w in ['undefined','multiply defined','Overfull','Underfull','Label.*changed']}
        if any(v for k,v in warnings.items() if k!='Underfull'):issues.append(kind+' build warning')
        txt=folder/'rendered.txt';xml=folder/'geometry.xml'
        subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True)
        subprocess.run(['pdftotext','-bbox',str(pdf),str(xml)],check=True)
        clean=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',xml.read_text())
        pages=[x for x in ET.fromstring(clean).iter() if x.tag.endswith('page')];outside=[];empty=[]
        for i,page in enumerate(pages,1):
            words=[x for x in page.iter() if x.tag.endswith('word')]
            if not words:empty.append(i)
            for w in words:
                a=w.attrib
                if float(a['xMin'])<0 or float(a['yMin'])<0 or float(a['xMax'])>float(page.get('width'))+.1 or float(a['yMax'])>float(page.get('height'))+.1:
                    outside.append(i);break
        text=txt.read_text()
        if outside or empty or '??' in text:issues.append(kind+' page geometry/unresolved marker')
        compiled=set()
        for line in (folder/(stem+'.fls')).read_text().splitlines():
            if line.startswith('INPUT '):
                p=Path(line[6:]);compiled.add((p if p.is_absolute() else S/p).resolve())
        uncompiled=[str(p.relative_to(S)) for p in tree(S,S/(stem+'.tex')) if p.resolve() not in compiled]
        if uncompiled:issues.append(kind+' uncompiled input')
        reports[kind]={'path':str(pdf.relative_to(R)),'sha256':sha(pdf),'pages':len(pages),'warnings':warnings,
          'outside_page':outside,'empty_pages':empty,'uncompiled_inputs':uncompiled,
          'chapter_pdf_pages':[i for i,p in enumerate(text.split('\f'),1) if 'A faster graph search can' in p]}
    report={'status':'pass' if not issues else 'fail','issues':issues,'snapshot_files':len(base['files']),
      'snapshot_changes':changed,'inherited_input_occurrences':sum(inherited.values()),'missing_inputs':missing,
      'added_inputs':added,'publications':reports,'visual_review':'pending','independent_acceptance':False}
    save(O/'publication/verification.json',report);print(json.dumps(report,indent=2),flush=True)
    if issues:raise SystemExit(1)
def settle(kind):
    stem=NAMES[kind];folder=O/('publication/build-'+kind)
    records=json.loads((folder/'passes.json').read_text())
    cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder',
         '-output-directory='+str(folder),stem+'.tex']
    for _ in range(2):
        logtext=(folder/(stem+'.log')).read_text(errors='replace')
        if not re.search('Label.*changed',logtext,re.I):break
        i=len(records)+1;log=folder/f'pass-{i}.txt';start=time.monotonic()
        shutil.copyfile(folder/(stem+'.log'),folder/f'pre-pass-{i}.log')
        with log.open('w') as f:p=subprocess.run(cmd,cwd=S,stdout=f,stderr=subprocess.STDOUT,timeout=300)
        records.append({'pass':i,'returncode':p.returncode,'seconds':round(time.monotonic()-start,2),
                        'log':str(log.relative_to(R))})
        save(folder/'passes.json',records);print(json.dumps(records[-1]),flush=True)
        assert p.returncode==0
    assert not re.search('Label.*changed',(folder/(stem+'.log')).read_text(),re.I)
    target=D/(stem+'.pdf')
    shutil.copyfile(target,folder/'before-reference-settling.pdf')
    shutil.copyfile(folder/(stem+'.pdf'),target)
    if (O/'publication/verification.json').exists():
        shutil.copyfile(O/'publication/verification.json',O/'publication/verification-before-settling.json')
if __name__=='__main__':
    import sys
    for action in sys.argv[1:]:
        if action=='prepare':prepare()
        elif action=='audit':audit()
        elif action.startswith('settle-'):settle(action[7:])
        elif action in NAMES:build(action)
        else:raise SystemExit('Unknown action: '+action)
