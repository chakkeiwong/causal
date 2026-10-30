from pathlib import Path
from hashlib import sha256
import collections
import json
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';OUT=DOCS/'scientific-gap-closure/2026-10-29'
def digest(p):return sha256(p.read_bytes()).hexdigest()
def closure(name):
    found=[]
    def visit(path,stack):
        assert path not in stack,'Recursive input'
        found.append(str(path.relative_to(DOCS)))
        for value in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
            p=DOCS/value
            if not p.suffix:p=p.with_suffix('.tex')
            visit(p,stack+[path])
    visit(DOCS/name,[]);return collections.Counter(found)
def main():
    baseline=json.loads((OUT/'publication-baseline.json').read_text())
    assert all(digest(ROOT/p)==h for p,h in baseline.items())
    before=closure('causal_banking_developmental_rewrite_2026-10-29.tex')
    after=closure('causal_banking_scientific_progress_2026-10-29.tex')
    lost={p:n-after[p] for p,n in before.items() if p!='causal_banking_developmental_rewrite_2026-10-29.tex' and after[p]<n}
    assert not lost
    report=dict(protected_files=len(baseline),protected_unchanged=True,inherited_input_occurrences=sum(before.values())-1,inputs_lost=lost,documents={})
    for kind,name in [('short','causal_banking_public_evidence_2026-10-29'),('integrated','causal_banking_scientific_progress_2026-10-29')]:
        pdf=DOCS/(name+'.pdf');xml=OUT/('rendered-'+kind+'.html');txt=OUT/('rendered-'+kind+'.txt')
        subprocess.run(['pdftotext','-bbox',str(pdf),str(xml)],check=True)
        subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True)
        data=xml.read_text();clean=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',data)
        tree=ET.fromstring(clean);pages=[e for e in tree.iter() if e.tag.endswith('page')];outside=[];empty=[]
        for i,page in enumerate(pages,1):
            words=[e for e in page.iter() if e.tag.endswith('word')]
            if not words:empty.append(i)
            for word in words:
                a=word.attrib;W=float(page.attrib['width']);H=float(page.attrib['height'])
                if float(a['xMin']) < -1 or float(a['yMin']) < -1 or float(a['xMax'])>W+1 or float(a['yMax'])>H+1:outside.append(i);break
        log=(OUT/('build-'+kind)/'pass-5.txt').read_text();warnings={w:len(re.findall(w,log,re.I)) for w in ['undefined','multiply defined','Overfull','Label.*changed']}
        text=txt.read_text();markers=['What a public experiment','Repeated decisions','An uncertain customer identity','What a causal reasoning test','existing software already']
        missing=[m for m in markers if m not in text]
        assert not outside and not missing and not any(warnings.values()),(outside,missing,warnings)
        report['documents'][kind]=dict(path=str(pdf.relative_to(ROOT)),pages=len(pages),sha256=digest(pdf),warnings=warnings,outside_page=outside,empty_pages=empty,missing_new_chapters=missing,
            human_acceptance=False,visual_review='Pending representative rendered pages')
    (OUT/'publication-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
