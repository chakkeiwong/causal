"""Integrate sampling evidence without changing the preserved financing edition."""
from pathlib import Path
import json,shutil,re,sys
import build_closure_publication_20261030 as base

ROOT=base.O
PRIOR=ROOT/'publication-1/snapshot/docs'
base.O=ROOT/'sampling-publication'
base.S=base.O/'publication-1/snapshot/docs'
base.OLD='causal_banking_closure_integrated_2026-10-30'
base.NAMES={'full':'causal_banking_closure_integrated_v2_2026-10-30',
            'short':'causal_banking_discovery_sampling_2026-10-30'}
base.CHAPTER='twelve-hour-closure/2026-10-29/discovery-sampling.tex'
base.SECTION='twelve-hour-closure/2026-10-29/discovery-sampling-section.tex'
base.REFS='twelve-hour-closure/2026-10-29/sampling-refs'
base.ANCHOR=r'\input{writing-repair/2026-10-29/src/f3b8a7764b223a39.tex}'
original_integrate=base.integrate
def integrate(raw):
    # Reuse the exact inherited citation identities in the integrated book.
    result=original_integrate(raw)
    return result.replace(','+base.REFS+'}', '}')
base.integrate=integrate

def prepare():
    manifest=base.O/'publication-1/baseline.json';assert not manifest.exists(),'Preserve existing snapshot'
    prior=json.loads((ROOT/'publication-1/verification.json').read_text());assert prior['status']=='pass'
    files={}
    for p in PRIOR.rglob('*'):
        if not p.is_file():continue
        n=p.relative_to(PRIOR);q=base.S/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);files[str(n)]=base.sha(p)
    additions=[base.CHAPTER,base.REFS+'.bib','twelve-hour-closure/2026-10-29/sampling-figures/coverage.pdf','twelve-hour-closure/2026-10-29/sampling-figures/skeleton.pdf','twelve-hour-closure/2026-10-29/sampling-complete-table.tex']
    for n in additions:
        p=base.D/n;q=base.S/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    raw=(base.S/(base.OLD+'.tex')).read_text();(base.S/base.SECTION).write_text(base.as_section((base.S/base.CHAPTER).read_text()))
    (base.S/(base.NAMES['full']+'.tex')).write_text(base.integrate(raw))
    prefix=raw.split(r'\begin{document}',1)[0]
    prefix=re.sub(r'\\title\{.*?\\author',lambda _:r'\title{\sffamily\bfseries\color{ink}Causal discovery, sampling error and lending comparisons}\author',prefix,flags=re.S)
    short=prefix+r'''
\begin{document}
\frontmatter\maketitle\mainmatter
\input{twelve-hour-closure/2026-10-29/discovery-sampling.tex}
\appendix
\chapter{Complete first-study comparisons}
Each row contains 200 independent simulated samples. Wrong counts incorrect
skeletons; unfinished counts searches with unexamined larger sets. Coverage
is the percentage of ordinary 95 per cent intervals containing the stipulated
effect under the naive selected-control rule. The cancellation case violates
faithfulness. Both thresholds and all three search rules are retained.
\small
\input{twelve-hour-closure/2026-10-29/sampling-complete-table.tex}
\normalsize
\backmatter
\bibliographystyle{writing-repair/2026-10-29/causalplainnat-reading}
\bibliography{twelve-hour-closure/2026-10-29/sampling-refs}
\end{document}
'''
    (base.S/(base.NAMES['short']+'.tex')).write_text(short)
    base.save(manifest,dict(source_package=str(PRIOR.relative_to(base.R)),baseline_files=files,baseline_pdf=prior['publications']['full'],source_occurrences=[str(p.relative_to(base.S)) for p in base.tree(base.S/(base.OLD+'.tex'))],new_files={n:base.sha(base.S/n) for n in additions+[base.SECTION]},insertion='End of existing discovery-repair chapter before observation-process chapter; section hierarchy preserves inherited chapter numbers.'))
    print(json.dumps({'snapshot_files':len(files),'added_files':len(additions)+1}),flush=True)

if __name__=='__main__':
    actions=sys.argv[1:]
    if actions and actions[0] in ['revision2','revision3']:
        revision=2 if actions[0]=='revision2' else 3
        actions=actions[1:]
        base.O=ROOT/f'sampling-publication/revision-{revision}'
        base.S=base.O/'publication-1/snapshot/docs'
        base.NAMES={'full':f'causal_banking_closure_integrated_v{revision+1}_2026-10-30',
                    'short':f'causal_banking_discovery_sampling_v{revision}_2026-10-30'}
    for action in actions:
        if action=='prepare':prepare()
        elif action=='audit':base.audit()
        elif action in base.NAMES:base.build(action)
        else:raise SystemExit(action)
