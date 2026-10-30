"""Focused checks for the editorial successor; no replay of historical campaigns."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
OUT=DOCS/'reading-edition'
STEM='causal_banking_reading_edition_2026-10-29'
PDF=DOCS/(STEM+'.pdf')
BUILD=OUT/'build'
B=chr(92)
AUDIT=DOCS/'program/execution/2026-10-29/panel-runtime-reader-v2/reader/source-audit.json'


def digest(p):
    h=sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def expanded(path, stack=()):
    if path in stack:raise ValueError('Recursive TeX input')
    s=path.read_text()
    def child(m):
        name=m.group(1);p=DOCS/(name if name.endswith('.tex') else name+'.tex')
        return expanded(p,stack+(path,))
    return re.sub(r'\\input\{([^}]+)\}',child,s)


def main():
    issues=[]
    mapping=json.loads((OUT/'source-map.json').read_text())
    for row in mapping:
        for path,hash_key in [(row['original'],'original_sha256'),(row['reading_copy'],'reading_sha256')]:
            if digest(ROOT/path)!=row[hash_key]:issues.append('Changed source: '+path)
    full=expanded(DOCS/(STEM+'.tex'))
    labels=Counter(re.findall(r'\\label\{([^}]+)\}',full))
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',full))
    missing=sorted(refs-set(labels))
    if missing:issues.append('Missing labels: '+str(missing))
    duplicates=[x for x,n in labels.items() if n>1]
    if duplicates:issues.append('Duplicate labels: '+str(duplicates))
    log=(BUILD/(STEM+'.log')).read_text(errors='replace')
    warnings=[l for l in log.splitlines() if any(x in l for x in ['Overfull','undefined','multiply defined'])]
    issues.extend(warnings)
    bib=(BUILD/(STEM+'.bbl')).read_text()
    if 'I couldn' in (BUILD/'pass-2.log').read_text():issues.append('Bibliography failure')
    audit=json.loads(AUDIT.read_text()); keyed={x['integrated_citation_key']:x for x in audit['sources']}
    new_paths=[OUT/'banking-decision.tex',OUT/'software-conclusions.tex',OUT/'assistance-conclusions.tex']
    support=[]
    for p in new_paths:
        keys=set()
        for m in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}',p.read_text()):keys.update(x.strip() for x in m.group(1).split(','))
        for key in sorted(keys):
            if key not in keyed:issues.append('Unaudited new citation '+key);continue
            source=keyed[key]
            for binding in [source.get('local_copy'),{'path':source.get('local_path'),'sha256':source.get('sha256')}]:
                if isinstance(binding,dict) and binding.get('path') and binding.get('sha256'):
                    target=ROOT/binding['path']
                    if not target.is_file() or digest(target)!=binding['sha256']:issues.append('Source identity mismatch '+key)
            support.append(dict(chapter=str(p.relative_to(ROOT)),citation=key,source_audit=str(AUDIT.relative_to(ROOT)),
                                source_record_identity=source.get('source_identity') or source.get('url'),
                                scope='Synthesis of the already inspected comparison; no new source search or package execution'))
    (OUT/'synthesis-source-links.json').write_text(json.dumps(support,indent=2)+'\n')
    # Streaming bounds inspection avoids retaining a second enormous PDF-text archive.
    bbox=Path('/tmp/causal-reading-edition-bbox.html')
    subprocess.run(['pdftotext','-bbox',str(PDF),str(bbox)],check=True)
    # Poppler can emit XML-invalid control characters for mathematical glyphs.
    # Remove only characters XML 1.0 cannot represent; retain text and bounds.
    clean=Path('/tmp/causal-reading-edition-bbox-clean.html')
    invalid_xml_characters=0
    with bbox.open(errors='replace') as src,clean.open('w') as dst:
        for line in src:
            filtered=re.sub('[\x00-\x08\x0b\x0c\x0e-\x1f]','',line)
            invalid_xml_characters+=len(line)-len(filtered)
            dst.write(filtered)
    pages=0;empty=[];outside=[];figures={}; part_pages={}
    ns='{http://www.w3.org/1999/xhtml}'
    figure_phrases=['A deposit campaign must earn','A proposed explanation of selection',
                    'The information date separates','Three stipulated ranges',
                    'Different questions give different averages','measurement error can reverse']
    for _,el in ET.iterparse(clean,events=['end']):
        if el.tag!=ns+'page':continue
        pages+=1;w=float(el.attrib['width']);h=float(el.attrib['height']);words=list(el.iter(ns+'word'))
        if not words:empty.append(pages)
        for word in words:
            a=word.attrib
            if float(a['xMin']) < -1 or float(a['yMin']) < -1 or float(a['xMax'])>w+1 or float(a['yMax'])>h+1:
                outside.append(dict(page=pages,text=word.text,bounds=a))
        text=' '.join(''.join(x.itertext()) for x in words)
        for phrase in figure_phrases:
            if phrase.lower() in text.lower():figures[phrase]=pages
        if text.startswith('Part '):part_pages[pages]=text[:180]
        el.clear()
    if outside:issues.append('Words outside page: '+str(len(outside)))
    if len(figures)!=6:issues.append('Missing new figure captions: '+str(figures))
    toc=(BUILD/(STEM+'.toc')).read_text()
    parts=[l for l in toc.splitlines() if B+'contentsline {part}' in l]
    if len(parts)!=9:issues.append('Wrong part count')
    body=(DOCS/(STEM+'.tex')).read_text().split(B+'mainmatter',1)[1].split(B+'backmatter',1)[0]
    # Verify every original top-level block remains reachable, including split chapters.
    order=json.loads((OUT/'reading-order.json').read_text())
    if set(order['order'])|{int(x) for x in order['split_inputs']}!=set(range(328)):
        issues.append('Original input omitted from reading order')
    result=dict(status='fail' if issues else 'pass',issues=issues,pdf=str(PDF.relative_to(ROOT)),sha256=digest(PDF),
                pages=pages,parts=9,new_figures=6,new_figure_physical_pages=figures,
                bibliography_records=len(re.findall(r'\\bibitem',bib)),missing_references=missing,
                duplicate_labels=duplicates,overfull_boxes=log.count('Overfull'),underfull_boxes=log.count('Underfull'),
                empty_pages=empty,out_of_page_words=outside[:20],
                poppler_xml_controls_removed=invalid_xml_characters,
                original_sources_unchanged=len(mapping),
                edits=len(json.loads((OUT/'editorial-changes.json').read_text())),
                visual_review='Pending: inherited session image allowance exhausted; text bounds do not certify appearance',
                human_voice_acceptance=False,whole_survey_completion=False)
    (OUT/'review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(bool(issues))


if __name__=='__main__':main()
