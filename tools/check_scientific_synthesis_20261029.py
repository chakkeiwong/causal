"""Check only the scientific continuation and its immediate evidence."""
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-synthesis/2026-10-29'


def digest(p):return sha256(p.read_bytes()).hexdigest()


def main():
    issues=[];checked=set()
    baseline=json.loads((OUT/'integration-baseline.json').read_text())
    for p,h in baseline.items():
        if digest(ROOT/p)!=h:issues.append('Baseline changed: '+p)
    audit=json.loads((OUT/'source-audit.json').read_text())
    def source_files(obj):
        if isinstance(obj,dict):
            path=obj.get('path',obj.get('local_path'));h=obj.get('sha256')
            if isinstance(path,str) and isinstance(h,str):
                p=Path(path) if path.startswith('/') else ROOT/path
                if not p.is_file():issues.append('Missing source: '+path)
                elif digest(p)!=h:issues.append('Source hash mismatch: '+path)
                checked.add(path)
            for v in obj.values():source_files(v)
        elif isinstance(obj,list):
            for x in obj:source_files(x)
    for r in audit['sources']:source_files(r)
    records={x['integrated_citation_key']:x for x in audit['sources']}
    chapter_files=list(OUT.glob('*.tex'));text='\n'.join(p.read_text() for p in chapter_files)
    cited={k.strip() for g in re.findall(r'\\cite\w*\{([^}]+)\}',text) for k in g.split(',')}
    if cited-set(records):issues.append('Missing citations: '+str(cited-set(records)))
    for k in cited:
        r=records[k]
        if r.get('kind')=='paper':
            p=ROOT/r['local_path']
            if not str(p.relative_to(ROOT)).startswith('docs/papers/') or p.read_bytes()[:4]!=b'%PDF':
                issues.append('Not a genuine local PDF: '+k)
    checks=[('study','study-plan.json','run_scientific_synthesis_20261029.py'),
            ('uncertainty','uncertainty-plan.json','run_sparse_support_20261029.py'),
            ('public-timing','public-timing-plan.json','run_public_timing_20261029.py')]
    for name,plan,script in checks:
        r=json.loads((OUT/(name+'-results.json')).read_text())
        if r['plan_sha256']!=digest(OUT/plan):issues.append(name+' plan changed after execution')
        if r['code_sha256']!=digest(ROOT/'tools'/script):issues.append(name+' code changed after execution')
    r=json.loads((OUT/'walkthrough-results.json').read_text())
    if r['runner_sha256']!=digest(ROOT/'tools/run_banking_walkthrough_20261029.py'):
        issues.append('Walkthrough code changed after execution')
    for p,h in r['source_hashes'].items():
        if digest(ROOT/p)!=h:issues.append('Walkthrough source changed: '+p)
    if not all(x['library']==x['cli']==x['mcp'] for x in r['results']):
        issues.append('Interface results differ')
    public=json.loads((OUT/'public-timing-results.json').read_text())
    if digest(ROOT/public['data']['path'])!=public['data']['sha256']:
        issues.append('Public data changed after execution')
    if len(public['results'])!=6 or any(x['warnings'] for x in public['results']):
        issues.append('Incomplete public comparison or fitting warning')
    if len(re.findall(r'\\section\{Public banking records:',text))!=1:
        issues.append('Missing or duplicated public-data section')
    area_ids=re.findall(r'\\subsection\{(\d+)\.',(OUT/'software-decisions.tex').read_text())
    if area_ids!=[str(i) for i in range(1,18)]:issues.append('Seventeen-area comparison incomplete')
    publications={}
    for kind,suffix in [('supplement','supplement'),('integrated','continuation')]:
        stem='causal_banking_scientific_'+suffix+'_2026-10-29'
        pdf=ROOT/'docs'/(stem+'.pdf');build=OUT/('build-'+kind)
        log=(build/(stem+'.log')).read_text()
        counts={k:len(re.findall(k,log)) for k in ['undefined','Overfull','multiply defined','Underfull']}
        if any(counts[k] for k in ['undefined','Overfull','multiply defined']):issues.append(kind+' LaTeX issue')
        with tempfile.TemporaryDirectory(prefix='causal-pdf-check-') as tmp:
            bbox=Path(tmp)/'pages.xml';plain=Path(tmp)/'pages.txt'
            subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True,timeout=60,capture_output=True)
            subprocess.run(['pdftotext','-layout',str(pdf),str(plain)],check=True,timeout=60,capture_output=True)
            extracted=bbox.read_text()
            # Some inherited mathematical glyphs extract as XML-forbidden
            # control characters; discard only those in the inspection copy.
            cleaned=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',extracted)
            controls_removed=len(extracted)-len(cleaned)
            root=ET.fromstring(cleaned);ns={'x':'http://www.w3.org/1999/xhtml'}
            pages=root.findall('.//x:page',ns);outside=[];blank=[]
            for i,page in enumerate(pages,1):
                words=page.findall('.//x:word',ns)
                if not words:blank.append(i)
                for word in words:
                    if (float(word.get('xMin'))<0 or float(word.get('yMin'))<0
                        or float(word.get('xMax'))>float(page.get('width'))+.1
                        or float(word.get('yMax'))>float(page.get('height'))+.1):
                        outside.append(i);break
            rendered=plain.read_text()
            if '??' in rendered:issues.append(kind+' unresolved PDF reference')
            if outside:issues.append(kind+' out-of-page text')
            if blank:issues.append(kind+' empty pages')
            publications[kind]={'path':str(pdf.relative_to(ROOT)),'sha256':digest(pdf),'pages':len(pages),
                'warnings':counts,'blank_pages':blank,'out_of_page_text':outside,
                'rendered_text_inspected':True,'xml_control_characters_removed':controls_removed,'visual_acceptance':False,
                'visual_review':'Delegated by user; no additional image previews in exhausted session.'}
    result={'status':'pass' if not issues else 'fail','issues':issues,
            'preserved_baseline_files':len(baseline),'cited_sources':len(cited),
            'authenticated_local_files':len(checked),'software_areas':len(area_ids),
            'publications':publications,'scientific_scope':'Two generated studies, public archived-contact prediction and selected local interface cases; no bank causal-effect or external causal-package qualification',
            'proposal_complete':False,'editorial_acceptance':False}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if issues:raise SystemExit(1)


if __name__=='__main__':main()
