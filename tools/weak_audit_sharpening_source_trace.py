#!/usr/bin/env python3
"""Trace inherited primary papers and the follow-up's new project claims."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRIOR='docs/reviews/weak-audit-source-review.json'
TARGET='docs/reviews/weak-audit-sharpening-source-review.json'


def read(name):return json.loads((ROOT/name).read_text())
def digest(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()


def main():
    previous=read(PRIOR)
    if previous['status']!='pass' or any(digest(p)!=h for p,h in previous['input_sha256'].items()):
        raise ValueError('Prior source audit changed')
    registered={x['id']:x for x in read('docs/literature/sources.json')}
    sources=[]
    for row in previous['cited_primary_works']:
        item=registered[row['id']]
        expected=f"{item['filename_title']} {item['first_author']}({item['year']}).pdf"
        if (Path(row['local_path']).name!=expected or item['sha256']!=row['sha256']
                or digest(row['local_path'])!=row['sha256']
                or (ROOT/row['local_path']).read_bytes()[:5]!=b'%PDF-'):
            raise ValueError('Changed original scholarly PDF: '+row['id'])
        sources.append(row)
    if {x['id'] for x in sources}!={'dml2018','newey1986'}:raise ValueError('Wrong source roles')
    inputs=[PRIOR,'docs/literature/sources.json',
            'docs/supplements/weak_audit_sharpening_2026-10-11.tex',
            'tools/weak_audit_sharpening_source_trace.py']+[x['local_path'] for x in sources]
    receipt=dict(status='pass',date='2026-10-11',publication_cutoff='2026-10-07',
        cited_primary_works=sources,
        project_claims=[
            'AD-R01: transformed observable score and covariance are project algebra and numerical checks; iid DML remains a narrow inherited premise.',
            'AD-R02: exact audit inversion and projection are project work; Newey--West supports only the distinct Bartlett alternative.',
            'AD-R03: repaired fresh paired coverage and width are registered synthetic evidence, not claims from cited works.',
            'AD-R04: pathwise false-exogeneity equivalence is a project derivation restricted to a class allowing adjusted nuisance means.' ],
        search_scope='Two existing original technical copies reverified; no new discovery/version/correction search.',
        scope='Traceable source identity and narrow roles, not independent scientific or bank validation.',
        input_sha256={name:digest(name) for name in sorted(inputs)})
    (ROOT/TARGET).write_text(json.dumps(receipt,indent=2)+'\n')
    print('Follow-up source roles bound to two unchanged primary PDFs.')


if __name__=='__main__':main()
