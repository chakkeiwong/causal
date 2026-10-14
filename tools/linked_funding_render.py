#!/usr/bin/env python3
"""Assemble original PDFs and render the exact new pages for author inspection."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = 'docs/causal_foundations.pdf'
FIRST = 'docs/supplements/weak_audit_projection_2026-10-11.pdf'
SECOND = 'docs/supplements/weak_audit_sharpening_2026-10-11.pdf'
NEW = 'docs/supplements/linked_funding_2026-10-11.pdf'
READER = 'docs/causal_foundations_with_linked_audits_2026-10-11.pdf'
FOLDER = 'docs/reviews/linked-funding-rendered'


def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True)


def digest(p):
    with (ROOT/p).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def pages(p):
    output = run(['pdfinfo',str(ROOT/p)]).stdout
    return int(re.search(r'(?m)^Pages:\s+(\d+)',output).group(1))


def main():
    log_path = 'docs/supplements/linked_funding_2026-10-11.log'
    log = (ROOT/log_path).read_text()
    if re.search(r'Overfull|Undefined|LaTeX Warning|Package .* Warning|! LaTeX Error',log):
        raise ValueError('Blocking final LaTeX warning')
    assert [pages(p) for p in (BASE,FIRST,SECOND,NEW)] == [245,4,4,6]
    merge = run(['pdfunite']+[str(ROOT/p) for p in (BASE,FIRST,SECOND,NEW,READER)])
    if merge.stderr.strip():
        raise ValueError('Merge emitted diagnostics: '+merge.stderr[:200])
    assert pages(READER) == 259
    def texts(path):
        value = run(['pdftotext','-layout',str(ROOT/path),'-']).stdout.split('\f')
        if not value[-1].strip(): value.pop()
        return [x.strip() for x in value]
    source_text = sum([texts(p) for p in (BASE,FIRST,SECOND,NEW)],[])
    final_text = texts(READER)
    assert len(source_text) == len(final_text) == 259 and source_text == final_text
    folder = ROOT/FOLDER
    folder.mkdir(exist_ok=True)
    images = []
    for page in range(1,7):
        prefix = folder/f'page-{page}'
        run(['pdftoppm','-f',str(page),'-l',str(page),'-r','120','-singlefile','-png',str(ROOT/NEW),str(prefix)])
        images.append(str(prefix.with_suffix('.png').relative_to(ROOT)))
    thumbs = []
    for path in images:
        im = Image.open(ROOT/path).convert('RGB')
        im.thumbnail((620,877))
        thumbs.append(im)
    sheet = Image.new('RGB',(1280,2760),'#dddddd')
    draw = ImageDraw.Draw(sheet)
    for i,im in enumerate(thumbs):
        x,y = 10+640*(i%2), 20+920*(i//2)
        sheet.paste(im,(x,y))
        draw.text((x,y+880),f'Follow-up page {i+1}',fill='black')
    contact = FOLDER+'/contact.png'
    sheet.save(ROOT/contact)
    images.append(contact)
    pairs = []
    mapping = [(1,BASE,1),(245,BASE,245)]
    mapping += [(245+i,FIRST,i) for i in range(1,5)]
    mapping += [(249+i,SECOND,i) for i in range(1,5)]
    mapping += [(253+i,NEW,i) for i in range(1,7)]
    for final,source,local in mapping:
        for side,pdf,page in [('source',source,local),('final',READER,final)]:
            prefix = folder/f'assembly-{side}-{final}'
            run(['pdftoppm','-f',str(page),'-l',str(page),'-r','90','-singlefile','-png',str(ROOT/pdf),str(prefix)])
            images.append(str(prefix.with_suffix('.png').relative_to(ROOT)))
        assert digest(FOLDER+f'/assembly-source-{final}.png') == digest(FOLDER+f'/assembly-final-{final}.png')
        pairs.append(final)
    inputs = [BASE,FIRST,SECOND,NEW,READER,log_path,'tools/linked_funding_render.py',
              'docs/supplements/linked_funding_2026-10-11.tex','docs/supplements/linked-funding-tables.tex']
    result = dict(status='pass',date='2026-10-11',issues=[],
                  documents=[dict(path=p,pages=pages(p),sha256=digest(p)) for p in (NEW,READER)],
                  merge_diagnostics=merge.stderr,all_page_text_matches=259,
                  assembly_pixel_matches=pairs,
                  rendered_for_inspection=[FOLDER+f'/page-{i}.png' for i in range(1,7)]+[contact],
                  images_sha256={p:digest(p) for p in images},
                  scope='Build and rendering evidence only. Actual viewing must be recorded separately.',
                  input_sha256={p:digest(p) for p in inputs})
    (ROOT/'docs/reviews/linked-funding-build.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',pages=259,new_pages=6,all_page_text_matches=259,pixel_matches=len(pairs)),indent=2))


if __name__ == '__main__': main()
