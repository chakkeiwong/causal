#!/usr/bin/env python3
"""Text and physical bounds review; this does not inspect rendered images."""
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/program/gap-repair-v13/reader'


def main():
    report=json.loads((OUT/'build-report.json').read_text())
    pdf=ROOT/report['pdf']['path']
    target=OUT/'reader-bbox.html'
    subprocess.run(['pdftotext','-bbox',str(pdf),str(target)],check=True,timeout=30)
    raw=target.read_text()
    controls=re.findall(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',raw)
    clean=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',raw)
    root=ET.fromstring(clean);ns={'x':'http://www.w3.org/1999/xhtml'}
    pages=root.findall('.//x:page',ns);outside=[];empty=[];count=0
    for i,page in enumerate(pages,1):
        words=page.findall('.//x:word',ns);count+=len(words)
        if not words:empty.append(i)
        for w in words:
            x0,y0,x1,y1=[float(w.attrib[k]) for k in ['xMin','yMin','xMax','yMax']]
            if x0 < -1 or y0 < -1 or x1 > float(page.attrib['width'])+1 or y1 > float(page.attrib['height'])+1:
                outside.append({'page':i,'word':w.text,'bbox':[x0,y0,x1,y1]})
    result={'scope':'Extracted text and physical page bounds only; not rendered visual inspection',
            'pages':len(pages),'words':count,'empty_pages':empty,'out_of_bounds':outside,
            'visual_review':'Pending fresh session under inherited image allowance',
            'status':'pass' if len(pages)==report['pages'] and not empty and not outside else 'fail',
            'extraction_controls_removed_for_xml_parsing':len(controls),
            'extraction_note':'Controls emitted for some mathematical glyphs were removed only from the in-memory XML parser input. Original extraction retained; no glyph/visual acceptance inferred.',
            'build_warnings':report['warnings']}
    (OUT/'text-layout-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'pages':len(pages),'empty_pages':len(empty),
                      'outside_bounds':len(outside),'extraction_controls':len(controls),'visual_acceptance':False}))


if __name__=='__main__':main()
