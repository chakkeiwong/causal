"""Preserve release batch 015 and integrate the financing identification study."""
from pathlib import Path
from collections import Counter
import hashlib, json, os, re, shutil, subprocess, sys, time
import xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
D = R / 'docs'
O = D / 'twelve-hour-closure/2026-10-29'
P = D / 'release/2026-10-29/packages/batch-015'
S = O / 'publication-1/snapshot/docs'
OLD = 'causal_banking_release_candidate_2026-10-29'
NAMES = {'full': 'causal_banking_closure_integrated_2026-10-30',
         'short': 'causal_banking_financing_identification_2026-10-30'}
CHAPTER = 'twelve-hour-closure/2026-10-29/formulation.tex'
SECTION = 'twelve-hour-closure/2026-10-29/formulation-section.tex'
REFS = 'twelve-hour-closure/2026-10-29/refs'
ANCHOR = r'\input{writing-repair/2026-10-29/src/26ee80caee96ff30.tex}'
INPUT = re.compile(r'\\(?:input|include)\{([^}]+)\}')
BIB = re.compile(r'\\bibliography\{([^}]+)\}')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, indent=2) + chr(10))
def tree(p):
    result = [p]
    for n in INPUT.findall(p.read_text()):
        q = S / n
        if not q.suffix: q = q.with_suffix('.tex')
        result += tree(q)
    return result
def integrate(raw):
    assert raw.count(ANCHOR) == 1
    result = raw.replace(ANCHOR, r'\input{' + SECTION + '}' + chr(10) + ANCHOR)
    result = BIB.sub(lambda m: r'\bibliography{' + m[1] + ',' + REFS + '}', result)
    result = result.replace('Release candidate: integrated argument and comparative evidence',
                            'Integrated argument, comparative evidence and financing identification')
    return result.replace(r'\date{29 October 2026', r'\date{30 October 2026')
def as_section(raw):
    return re.sub(r'\\(chapter|section)\{',
        lambda m: '\\' + {'chapter':'section', 'section':'subsection'}[m[1]] + '{', raw)
def prepare():
    assert not (O/'publication-1/baseline.json').exists(), 'Preserve existing snapshot'
    manifest = json.loads((P/'manifest.json').read_text())
    hashes = {}
    for n, h in manifest['source_hashes'].items():
        source = P/n
        assert sha(source) == h, n
        relative = Path(n).relative_to('source/docs')
        target = S/relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target); hashes[str(relative)] = h
    raw = (S/(OLD+'.tex')).read_text()
    for n in [CHAPTER, REFS+'.bib']:
        target = S/n; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(D/n, target)
    (S/SECTION).write_text(as_section((S/CHAPTER).read_text()))
    (S/(NAMES['full']+'.tex')).write_text(integrate(raw))
    prefix = raw.split(r'\begin{document}', 1)[0]
    prefix = re.sub(r'\\title\{.*?\\author', lambda _: r'\title{\sffamily\bfseries\color{ink}Financing constraints, language assistance and causal evidence}\author', prefix, flags=re.S)
    short = prefix + r'''
\begin{document}
\frontmatter\maketitle\mainmatter
\input{twelve-hour-closure/2026-10-29/formulation.tex}
\backmatter
\bibliographystyle{writing-repair/2026-10-29/causalplainnat-reading}
\bibliography{twelve-hour-closure/2026-10-29/refs}
\end{document}
'''
    (S/(NAMES['short']+'.tex')).write_text(short.replace(r'\date{29 October 2026',r'\date{30 October 2026'))
    save(O/'publication-1/baseline.json', {'source_package':str(P.relative_to(R)),
       'package_manifest_sha256':sha(P/'manifest.json'), 'baseline_files':hashes,
       'baseline_pdf':manifest['publications']['full'],
       'source_occurrences':[str(p.relative_to(S)) for p in tree(S/(OLD+'.tex'))],
       'new_files':{n:sha(S/n) for n in [CHAPTER, SECTION, REFS+'.bib']},
       'insertion':'End of the existing business-formulation chapter; section/subsection hierarchy preserves every inherited chapter number.'})
    print(json.dumps({'snapshot_files':len(hashes),'status':'prepared'}),flush=True)
def build(kind):
    stem=NAMES[kind]; folder=O/('publication-1/build-'+kind); folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'passes.json').exists(), 'Retain previous passes before a deliberate repair'
    env=dict(os.environ, BIBINPUTS=str(S)+'//:', BSTINPUTS=str(S)+'//:', SOURCE_DATE_EPOCH='1793293200', FORCE_SOURCE_DATE='1')
    latex=['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory='+str(folder),stem+'.tex']
    records=[]
    for i,command in enumerate([latex,['bibtex',stem],latex,latex,latex],1):
        start=time.monotonic(); log=folder/f'pass-{i}.txt'
        with log.open('w') as f:
            p=subprocess.run(command,cwd=folder if command[0]=='bibtex' else S,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=300)
        records.append({'pass':i,'returncode':p.returncode,'seconds':round(time.monotonic()-start,2),'log':str(log.relative_to(R))})
        save(folder/'passes.json',records);print(json.dumps(records[-1]),flush=True)
        if p.returncode:
            print(chr(10).join(log.read_text(errors='replace').splitlines()[-18:]));raise SystemExit(p.returncode)
        if i==4 and not re.search(r'Label.*changed|Rerun to get', (folder/(stem+'.log')).read_text(),re.I): break
    target=D/(stem+'.pdf'); assert not target.exists(), 'Preserve published PDF'
    shutil.copyfile(folder/(stem+'.pdf'),target)
    print(json.dumps({'published':str(target.relative_to(R)),'sha256':sha(target)}),flush=True)
def audit():
    b=json.loads((O/'publication-1/baseline.json').read_text());issues=[]
    changed=[n for n,h in b['baseline_files'].items() if sha(S/n)!=h]
    if changed:issues.append('Changed inherited files')
    if (S/(NAMES['full']+'.tex')).read_text()!=integrate((S/(OLD+'.tex')).read_text()):issues.append('Unexpected root edit')
    inherited=b['source_occurrences'][1:]
    actual=[str(p.relative_to(S)) for p in tree(S/(NAMES['full']+'.tex'))][1:]
    if [n for n in actual if n!=SECTION]!=inherited:issues.append('Inherited source order differs')
    if actual.count(SECTION)!=1:issues.append('New section multiplicity')
    if (S/SECTION).read_text()!=as_section((S/CHAPTER).read_text()):issues.append('Section conversion differs')
    reports={}
    for kind,stem in NAMES.items():
        f=O/('publication-1/build-'+kind); pdf=D/(stem+'.pdf'); log=(f/(stem+'.log')).read_text(errors='replace')
        warnings={w:len(re.findall(w,log,re.I)) for w in ['undefined','multiply defined','Overfull','Underfull','Label.*changed']}
        if any(v for k,v in warnings.items() if k!='Underfull'):issues.append(kind+' warnings')
        txt=f/'rendered.txt';xml=f/'geometry.xml'
        subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True)
        subprocess.run(['pdftotext','-bbox',str(pdf),str(xml)],check=True)
        clean=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',xml.read_text())
        pages=[p for p in ET.fromstring(clean).iter() if p.tag.endswith('page')];outside=[];empty=[]
        for i,p in enumerate(pages,1):
            words=[w for w in p.iter() if w.tag.endswith('word')]
            if not words:empty.append(i)
            if any(float(w.get('xMin'))<0 or float(w.get('yMin'))<0 or float(w.get('xMax'))>float(p.get('width'))+.1 or float(w.get('yMax'))>float(p.get('height'))+.1 for w in words):outside.append(i)
        text=txt.read_text()
        if outside or empty or '??' in text:issues.append(kind+' page or reference defect')
        reports[kind]={'path':str(pdf.relative_to(R)),'sha256':sha(pdf),'pages':len(pages),'warnings':warnings,'outside_page':outside,'empty_pages':empty,'formulation_pages':[i for i,p in enumerate(text.split(chr(12)),1) if 'A convincing explanation' in p or 'The two constructed mechanisms' in p]}
    out={'status':'pass' if not issues else 'fail','issues':issues,'inherited_files':len(b['baseline_files']),'changed_inherited_files':changed,'inherited_input_occurrences':len(inherited),'inherited_order_preserved':True,'new_input':SECTION,'publications':reports,'visual_review':'pending','independent_acceptance':False}
    save(O/'publication-1/verification.json',out);print(json.dumps(out,indent=2),flush=True)
    if issues:raise SystemExit(1)
if __name__=='__main__':
    for action in sys.argv[1:]:
        if action=='prepare':prepare()
        elif action=='audit':audit()
        elif action in NAMES:build(action)
        else:raise SystemExit(action)
