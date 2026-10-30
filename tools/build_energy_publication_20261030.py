"""Preserve scientific v13 and add the useful-answer energy study."""
from pathlib import Path
import json,re,shutil,sys
import build_closure_publication_20261030 as base
ROOT=base.O
PRIOR=ROOT/'outcome-publication/revision-3/publication-1/snapshot/docs'
base.O=ROOT/'energy-publication'
base.S=base.O/'publication-1/snapshot/docs'
base.OLD='causal_banking_closure_integrated_v13_2026-10-30'
base.NAMES={'full':'causal_banking_closure_integrated_v14_2026-10-30','short':'causal_banking_useful_answer_cost_2026-10-30'}
base.CHAPTER='twelve-hour-closure/2026-10-29/energy-study.tex'
base.SECTION='twelve-hour-closure/2026-10-29/energy-study-section.tex'
base.REFS='twelve-hour-closure/2026-10-29/energy-refs'
base.ANCHOR='\\input{writing-repair/2026-10-29/investment.tex}'
def prepare():
    manifest=base.O/'publication-1/baseline.json'
    assert not manifest.exists(),'Preserve existing snapshot'
    prior=json.loads((ROOT/'outcome-publication/revision-3/publication-1/verification.json').read_text())
    assert prior['status']=='pass'
    files={}
    for p in PRIOR.rglob('*'):
        if not p.is_file():continue
        n=p.relative_to(PRIOR);q=base.S/n;q.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,q);files[str(n)]=base.sha(p)
    additions=[base.CHAPTER,base.REFS+'.bib','twelve-hour-closure/2026-10-29/energy-figures/energy-waiting.pdf']
    for n in additions:
        p=base.D/n;q=base.S/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    raw=(base.S/(base.OLD+'.tex')).read_text()
    (base.S/base.SECTION).write_text(base.as_section((base.S/base.CHAPTER).read_text()))
    (base.S/(base.NAMES['full']+'.tex')).write_text(base.integrate(raw))
    prefix=raw.split('\\begin{document}',1)[0]
    prefix=re.sub(r'\\title\{.*?\\author',lambda _:'\\title{\\sffamily\\bfseries\\color{ink}The cost of a useful answer}\\author',prefix,flags=re.S)
    short=prefix+'''
\\begin{document}
\\frontmatter\\maketitle\\mainmatter
\\input{twelve-hour-closure/2026-10-29/energy-study.tex}
\\backmatter
\\bibliographystyle{writing-repair/2026-10-29/causalplainnat-reading}
\\bibliography{twelve-hour-closure/2026-10-29/energy-refs}
\\end{document}
'''
    (base.S/(base.NAMES['short']+'.tex')).write_text(short)
    base.save(manifest,dict(source_package=str(PRIOR.relative_to(base.R)),baseline_files=files,baseline_pdf=prior['publications']['full'],
      source_occurrences=[str(p.relative_to(base.S)) for p in base.tree(base.S/(base.OLD+'.tex'))],
      new_files={n:base.sha(base.S/n) for n in additions+[base.SECTION]},
      insertion='At the end of the inherited financial-economics chapter,before the final investment decision. Every inherited source and chapter order preserved.'))
    print(json.dumps(dict(snapshot_files=len(files),added_files=len(additions)+1)),flush=True)
if __name__=='__main__':
    actions=sys.argv[1:]
    if actions and actions[0].startswith('revision'):
        revision=int(actions.pop(0).replace('revision',''))
        base.O=ROOT/f'energy-publication/revision-{revision}';base.S=base.O/'publication-1/snapshot/docs'
        base.NAMES={'full':f'causal_banking_closure_integrated_v{13+revision}_2026-10-30','short':f'causal_banking_useful_answer_cost_v{revision}_2026-10-30'}
    for action in actions:
        if action=='prepare':prepare()
        elif action=='audit':base.audit()
        elif action in base.NAMES:base.build(action)
        else:raise SystemExit(action)
