"""Audit exact before/after reconstruction and all-page compiled geometry."""
from pathlib import Path
from collections import Counter,defaultdict
import difflib,json,re,subprocess,xml.etree.ElementTree as ET
from rewrite_preservation_20261029 import ROOT,DOCS,OUT,BASE,INPUT,digest,save,tree
from build_developmental_rewrite_20261029 import FULL,SPONSOR
CITE=re.compile(r'\\cite\w*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}')
LABEL=re.compile(r'\\label\{([^}]+)\}')
MATH=re.compile(r'(?s)\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)\$(?!\$).*?(?<!\\)\$|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}.*?\\end\{\1\}')
def citations(t):return Counter(k.strip() for g in CITE.findall(t) for k in g.split(','))
def maths(t):return Counter(m[0] for m in MATH.finditer(t))
def numbers(t):return Counter(re.findall(r'(?<![A-Za-z])\d+(?:[.,]\d+)*',t))
def main():
    issues=[];baseline=json.loads((OUT/'baseline.json').read_text());mapping=json.loads((OUT/'source-map.json').read_text());edits=json.loads((OUT/'edit-ledger.json').read_text())
    inherited={n:(OUT/'baseline'/n).read_text() for n in baseline['source_files']}
    final,counts=tree(DOCS/(FULL+'.tex'));group=defaultdict(list)
    for e in edits:group[e['source']].append(e)
    protected=[]
    for row in baseline['protected']:
        p=ROOT/row['path']
        if not p.is_file() or digest(p)!=row['sha256']:protected.append(row['path'])
        if row.get('snapshot') and digest(ROOT/row['snapshot'])!=row['sha256']:protected.append(row['snapshot'])
    if protected:issues.append('Protected baseline changed')
    reach=[];math_changes=[];numeric_changes=[];edited_body=[]
    for row in mapping:
        source=row['original'];dest=row['destination'];before=inherited[source];after=(ROOT/dest).read_text()
        if dest not in final or counts[dest]!=1:reach.append(dict(source=source,destination=dest,count=counts[dest]))
        if source==str(BASE.relative_to(ROOT)):
            a=before.splitlines(keepends=True);expected=[];pos=0
            for e in group[source]:
                i,j=e['before_line_start'],e['before_line_end'];expected.extend(a[pos:i]);assert ''.join(a[i:j])==e['before'];expected.append(e['after']);pos=j
            expected.extend(a[pos:]);replay=''.join(expected)
        else:
            replay=before
            for e in group[source]:
                if e['before'] not in replay:issues.append('Cannot replay '+source+' '+e['category']);continue
                replay=replay.replace(e['before'],e['after'],1)
            if before!=after:edited_body.append(source)
        if replay!=after:issues.append('Unrecorded text difference '+source)
        if source!=str(BASE.relative_to(ROOT)):
            cleanbefore=INPUT.sub('',before);cleanafter=INPUT.sub('',after)
            for bucket,extract in [(math_changes,maths),(numeric_changes,numbers)]:
                removed=extract(cleanbefore)-extract(cleanafter);added=extract(cleanafter)-extract(cleanbefore)
                if removed or added:bucket.append(dict(source=source,destination=dest,removed=dict(removed),added=dict(added),edit_categories=list({e['category'] for e in group[source]})))
        if Counter(LABEL.findall(before))-Counter(LABEL.findall(after)):issues.append('Label removed '+source)
        if citations(before)-citations(after):issues.append('Citation removed '+source)
    if reach:issues.append('Inherited file missing or duplicate in compiled tree')
    if any(r['source']!='docs/reading-edition/banking-decision.tex' for r in math_changes):issues.append('Unexpected inherited mathematical change')
    fls=(OUT/'build-full'/(FULL+'.fls')).read_text().splitlines();actual=set()
    for line in fls:
        if line.startswith('INPUT '):
            p=Path(line[6:]);p=p if p.is_absolute() else DOCS/p
            try:actual.add(str(p.resolve().relative_to(ROOT)))
            except ValueError:pass
    uncompiled=[r['destination'] for r in mapping if r['destination'] not in actual]
    if uncompiled:issues.append('Mapped sources absent from TeX recorder')
    bib=(OUT/'references.bib').read_text();bibrows=json.loads((OUT/'bibliography-map.json').read_text());bib_fail=[]
    for row in bibrows:
        old=(OUT/'baseline'/row['source']).read_text();m=re.search(r'@\w+\s*\{'+re.escape(row['key'])+r'\s*,',old);i=m.end();depth=1
        while i<len(old) and depth:
            if old[i]=='{' and old[i-1]!='\\':depth+=1
            elif old[i]=='}' and old[i-1]!='\\':depth-=1
            i+=1
        expected=old[m.start():i].strip()
        for e in group[row['source']]:
            if e.get('citation_key')==row['key']:
                if e['before'] not in expected:issues.append('Bibliography replay failure '+row['key'])
                expected=expected.replace(e['before'],e['after'],1)
        if expected not in bib:bib_fail.append(row['key'])
    if bib_fail:issues.append('Bibliography entries changed without disposition')
    inherited_audit=json.loads((DOCS/'scientific-synthesis/2026-10-29/source-audit.json').read_text())
    audpath=ROOT/inherited_audit['inherited_audit'];audit=json.loads(audpath.read_text());checked={};source_issues=[]
    def walk(o):
        if isinstance(o,dict):
            path=o.get('path',o.get('local_path'));h=o.get('sha256')
            if isinstance(path,str) and isinstance(h,str) and len(h)==64:
                p=Path(path) if path.startswith('/') else ROOT/path;key=(str(p),h)
                if key not in checked:
                    checked[key]=p.is_file() and digest(p)==h
                    if not checked[key]:source_issues.append(path)
            for v in o.values():walk(v)
        elif isinstance(o,list):
            for x in o:walk(x)
    walk(audit);walk(inherited_audit)
    if source_issues:issues.append('Source identity check failed')
    records={r.get('integrated_citation_key',r.get('id')):r for r in audit['sources']}
    newtex='\n'.join((OUT/f).read_text() for f in ['journeys.tex','decision-synthesis.tex','software-selection.tex']);newkeys=set(citations(newtex));missing=sorted(newkeys-set(records))
    if missing:issues.append('New synthesis citation missing audited record')
    save('source-support.json',{'cutoff':'2026-10-07','inherited_audit':str(audpath.relative_to(ROOT)),'inherited_sha256':digest(audpath),
        'records':[records[k] for k in sorted(newkeys) if k in records],'source_bindings_checked':len(checked),'source_issues':source_issues,
        'new_project_derivations':{'journeys.tex':'Assignment-weighted means, Student union intervals and affine value map; exact g-formula/IPW enumeration; equivalent Gaussian covariances; measurement moment inversion.',
        'decision-synthesis.tex':'Conditional investment and task recommendations distinguish reported evidence from authored judgment.'},
        'project_evidence':[dict(path=str((OUT/f).relative_to(ROOT)),sha256=digest(OUT/f)) for f in ['example-plan.json','example-results.json','generated-deposit-data.csv']],
        'literature_scope':'Retains inspected sources and omissions. No fresh census, version update or retraction sweep claimed.'})
    import run_rewrite_examples_20261029 as examples
    p,data,report=examples.compute();result=json.loads((OUT/'example-results.json').read_text())
    assert report==result['report'] and examples.exact_checks()==result['exact_checks']
    assert result['plan_sha256']==digest(OUT/'example-plan.json') and result['code_sha256']==digest(ROOT/'tools/run_rewrite_examples_20261029.py')
    assert result['data_sha256']==digest(OUT/'generated-deposit-data.csv')
    cli=json.loads(subprocess.check_output(['python3',str(ROOT/'tools/run_rewrite_examples_20261029.py'),'--report-only'],text=True))
    if cli!=report:issues.append('Example CLI mismatch')
    publications={}
    for kind,stem in [('full',FULL),('sponsor',SPONSOR)]:
        pdf=DOCS/(stem+'.pdf');log=(OUT/('build-'+kind)/(stem+'.log')).read_text();warnings={k:len(re.findall(k,log)) for k in ['undefined','multiply defined','Overfull','Underfull']}
        if any(warnings[k] for k in ['undefined','multiply defined','Overfull']):issues.append(kind+' build warnings requiring repair')
        plain=OUT/(kind+'-rendered.txt');xml=OUT/(kind+'-geometry.xml')
        subprocess.run(['pdftotext','-layout',str(pdf),str(plain)],check=True,capture_output=True,timeout=90)
        subprocess.run(['pdftotext','-bbox',str(pdf),str(xml)],check=True,capture_output=True,timeout=90)
        text=plain.read_text();raw=xml.read_text();cleaned=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',raw)
        pages=ET.fromstring(cleaned).findall('.//{http://www.w3.org/1999/xhtml}page');outside=[];blank=[]
        for i,page in enumerate(pages,1):
            words=page.findall('.//{http://www.w3.org/1999/xhtml}word')
            if not words:blank.append(i)
            for w in words:
                if float(w.get('xMin'))<0 or float(w.get('yMin'))<0 or float(w.get('xMax'))>float(page.get('width'))+.1 or float(w.get('yMax'))>float(page.get('height'))+.1:
                    outside.append(i);break
        if outside or blank or '??' in text:issues.append(kind+' rendered text failure')
        publications[kind]=dict(path=str(pdf.relative_to(ROOT)),sha256=digest(pdf),pages=len(pages),warnings=warnings,empty_pages=blank,outside_page=outside,unresolved_markers='??' in text,xml_controls_removed=len(raw)-len(cleaned),visual_acceptance=False)
    diff=[]
    for row in mapping:
        before=inherited[row['original']];after=(ROOT/row['destination']).read_text()
        if before!=after:diff.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=row['original'],tofile=row['destination']))
    (OUT/'all-inherited-content.diff').write_text(''.join(diff))
    lines=['# Full removal and replacement ledger','','Every inherited edit includes exact removed and replacement text. Relocations are not substantive deletions.','']
    for i,e in enumerate(edits,1):
        lines.extend([f"## {i}. {e['category']}",'',f"Source: {e['source']}. Destination: {e['destination']}.",'',e['reason'],'',e['surviving_claims_and_limits'],'','Before:','','~~~text',e['before'],'~~~','','After:','','~~~text',e['after'],'~~~',''])
    (OUT/'full-deletion-ledger.md').write_text('\n'.join(lines))
    summary=dict(pass_checks=not issues,issues=issues,baseline_protected_files=len(baseline['protected']),protected_changes=protected,inherited_tex_files=len(mapping),reachable_exactly_once=len(mapping)-len(reach),unmapped_or_duplicate=reach,absent_from_tex_recorder=uncompiled,
      exact_edit_replay='pass' if not any('replay' in s or 'difference' in s for s in issues) else 'fail',edit_categories=dict(Counter(e['category'] for e in edits)),
      citation_occurrences_removed=0 if not any('Citation removed' in x for x in issues) else None,labels_removed=0 if not any('Label removed' in x for x in issues) else None,
      bibliography_records=len(bibrows),bibliography_failures=bib_fail,inherited_math_changes=math_changes,inherited_numeric_changes=numeric_changes,source_bindings_checked=len(checked),source_issues=source_issues,example_reproduction=True,publications=publications,
      unaccounted_substantive_loss=any('replay' in x or 'difference' in x or 'removed' in x or 'missing' in x or 'Protected' in x or 'mathematical' in x for x in issues),
      review_limit='Exact preservation is machine checked; corrected target meaning is reviewed separately. No independent scientific or fresh visual acceptance.')
    summary['final_content_hashes']={name:digest(ROOT/name) for name in final}
    summary['final_bibliography_sha256']=digest(OUT/'references.bib')
    summary['edit_ledger_sha256']=digest(OUT/'edit-ledger.json')
    summary['source_map_sha256']=digest(OUT/'source-map.json')
    summary['checks_ran_after_last_content_edit']=all((ROOT/name).stat().st_mtime <= (DOCS/(FULL+'.pdf')).stat().st_mtime for name in final)
    save('deletion-audit.json',summary)
    print(json.dumps({k:summary[k] for k in ['pass_checks','issues','baseline_protected_files','inherited_tex_files','reachable_exactly_once','source_bindings_checked','publications']},indent=2))
    if issues:raise SystemExit(1)
if __name__=='__main__':main()
