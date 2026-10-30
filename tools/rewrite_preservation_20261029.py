"""Freeze and audit the developmental rewrite; never edit protected sources."""
from pathlib import Path
from hashlib import sha256
import argparse
import collections
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUT = DOCS / 'developmental-rewrite/2026-10-29'
BASE = DOCS / 'causal_banking_scientific_continuation_2026-10-29.tex'
INPUT = re.compile(r'\\(?:input|include)\{([^}]+)\}')

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def resolve(name, suffix='.tex'):
    p = DOCS / name
    if not p.suffix:
        p = p.with_suffix(suffix)
    if not p.is_file():
        raise FileNotFoundError(p)
    return p

def tree(root):
    files, occurrences = {}, collections.Counter()
    def walk(p):
        name = str(p.relative_to(ROOT))
        occurrences[name] += 1
        if name in files:
            return
        t = p.read_text()
        files[name] = t
        for v in INPUT.findall(t):
            walk(resolve(v))
    walk(root)
    return files, occurrences

def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT/'baseline.json').exists():
        raise RuntimeError('Baseline already frozen; use verify rather than recapture.')
    sources, occurrences = tree(BASE)
    protected = {ROOT/p for p in sources}
    bibliography = []
    assets = []
    for t in sources.values():
        for entry in re.findall(r'\\bibliography\{([^}]+)\}', t):
            for name in entry.split(','):
                p = resolve(name, '.bib'); protected.add(p); bibliography.append(str(p.relative_to(ROOT)))
        for name in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}', t):
            p = DOCS/name
            candidates = [p] if p.suffix else [p.with_suffix(s) for s in ['.pdf','.png','.jpg','.jpeg']]
            found = next((q for q in candidates if q.is_file()), None)
            if not found: raise FileNotFoundError(name)
            protected.add(found); assets.append(str(found.relative_to(ROOT)))
    for row in json.loads((DOCS/'reading-edition/source-map.json').read_text()):
        for key in ['original','reading_copy']:
            protected.add(ROOT/row[key])
    for folder in ['scientific-synthesis/2026-10-29','reading-edition','reviews/monograph-gap-review-2026-10-29']:
        for p in (DOCS/folder).rglob('*'):
            if p.is_file() and p.suffix in ['.json','.md','.py','.tex','.bib','.bst']:
                protected.add(p)
    for p in (DOCS/'papers').rglob('*.pdf'): protected.add(p)
    for name in ['causal_banking_reading_edition_2026-10-29','causal_banking_scientific_continuation_2026-10-29',
                 'causal_banking_scientific_supplement_2026-10-29','causal_proposal_panel_runtime_reviewed_v2_2026-10-29',
                 'sponsor_proposal_panel_runtime_reviewed_v2_2026-10-29']:
        for suffix in ['.tex','.pdf']:
            p=DOCS/(name+suffix)
            if p.exists(): protected.add(p)
    for p in [DOCS/'causalplainnat.bst', DOCS/'program/state.json', DOCS/'program/master-program.md',
              DOCS/'reading-edition/source-map.json']:
        if p.exists(): protected.add(p)
    rows=[]
    for p in sorted(protected):
        name=str(p.relative_to(ROOT))
        row={'path':name,'sha256':digest(p),'bytes':p.stat().st_size}
        if name in sources or p.suffix in ['.bib','.bst']:
            dest=OUT/'baseline'/name; dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
            row['snapshot']=str(dest.relative_to(ROOT))
        rows.append(row)
    save('baseline.json',{'date':'2026-10-29','active_root':str(BASE.relative_to(ROOT)),
         'active_pdf_sha256':digest(BASE.with_suffix('.pdf')),'source_files':list(sources),
         'occurrences':dict(occurrences),'bibliography_files':bibliography,'assets':assets,'protected':rows})
    save('state.json',{'phase':'baseline_frozen','plan':'docs/program/monograph-rewrite-2026-10-29.md',
          'plan_review':'docs/reviews/monograph-rewrite-plan-review-2026-10-29.md',
          'candidate_delivered':False,'substantive_preservation_pass':False,
          'fresh_visual_acceptance':False,'independent_scientific_acceptance':False,
          'failures_and_repairs':[], 'next':'Write the complete banking argument and reproduce its examples.'})
    print(json.dumps({'frozen_files':len(rows),'tex_files':len(sources),'bibliography_files':len(bibliography),'assets':len(assets)}))

def verify():
    b=json.loads((OUT/'baseline.json').read_text())
    failures=[]
    for row in b['protected']:
        p=ROOT/row['path']
        if not p.is_file() or digest(p)!=row['sha256']: failures.append(row['path'])
        if row.get('snapshot') and digest(ROOT/row['snapshot'])!=row['sha256']: failures.append(row['snapshot'])
    result={'protected_files':len(b['protected']),'failures':failures,'pass':not failures}
    save('protected-verification.json', result)
    print(json.dumps(result))
    if failures: raise SystemExit(1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','verify']);a=p.parse_args()
    freeze() if a.command=='freeze' else verify()
