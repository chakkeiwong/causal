"""Prepare a bounded immutable gfoRmula source acquisition for the next reuse decision."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-20/gformula-reuse-v1'
RAW=ROOT/'docs/literature/raw'
assert not BASE.exists()
BASE.mkdir()
commit=json.loads((RAW/'r3g_commit_gformula.json').read_text())[0]
sha=commit['sha'];tree=commit['commit']['tree']['sha']
assert sha=='86653ca1315f24a96a41b0ef590af13228f90ab4'
assert commit['commit']['committer']['date']=='2025-11-03T16:01:40Z'
entries=json.loads((RAW/'r3g_tree_gformula.json').read_text())
assert entries['truncated'] is False
paths=['DESCRIPTION','NAMESPACE','README.md','NEWS.md','R/gformula.R','R/bootstrap.R','R/comparisons.R',
       'R/helper.R','R/histories.R','R/interventions.R','R/pred.R','R/restrictions.R','R/simulate.R',
       'tests/testthat/test-gformula.R','vignettes/Intervention-Specification.Rmd',
       'vignettes/Custom-Outcome-Models.Rmd','.github/workflows/R-CMD-check.yaml']
by={x['path']:x for x in entries['tree']}
assert all(p in by for p in paths)
manifest=dict(requests=[dict(id='exec20_gformula_root_tree',
 url=f'https://api.github.com/repos/CausalInference/gfoRmula/git/trees/{tree}?recursive=1',extension='json')])
manifest['requests'] += [dict(id=f'exec20_gformula_source_{i:02d}',
 url=f'https://raw.githubusercontent.com/CausalInference/gfoRmula/{sha}/{p}',extension='txt') for i,p in enumerate(paths)]
(BASE/'previous-fetch-manifest.json').write_bytes((ROOT/'docs/literature/fetch-manifest.json').read_bytes())
for target in [BASE/'acquisition-manifest.json',ROOT/'docs/literature/fetch-manifest.json']:
 target.write_text(json.dumps(manifest,indent=2)+'\n')
(BASE/'source-selection.json').write_text(json.dumps(dict(commit=sha,commit_date=commit['commit']['committer']['date'],
 root_tree=tree,selected=[dict(index=i,path=p,blob=by[p]['sha']) for i,p in enumerate(paths)],
 inherited_api_sha256=hashlib.sha256((RAW/'r3g_api_gformula.txt').read_bytes()).hexdigest()),indent=2)+'\n')
(BASE/'plan.md').write_text('''# gfoRmula reuse decision

Resolve inherited:gformula and seed:061 as the same CausalInference/gfoRmula project.
Verify the inherited November2025 commit against its explicit root tree; authenticate
selected source bytes and inspect version, rights, dependencies and maintenance.
Trace survival versus terminal outcomes, interventions/time order, histories,
competing events, censoring diagnostics, simulation truncation, bootstrap unit,
failure handling and uncertainty. Compare exact two-period discrete integration
with mean-path substitution, and competing-event targets with censoring targets.
Separate simulation precision, fitted-model uncertainty and identification.

Choose a reasoned proposal disposition among reference, integrate, port, defer or
reject. No runtime admission from documentation alone; do not execute downloaded R
code, package tests or models. Preserve aliases, source/version discrepancies,
missing full rights and uninspected dependencies as obligations. Specify a typed
library/CLI/MCP worker and public qualification oracle before any implementation.
If scholarly papers are cited, acquire genuine PDFs and inspect primary anchors;
source references alone do not supply theorem authority.

Plan review: source identity and primary control flow precede technical claims.
An original R worker is a candidate to compare with a port, not a preapproved
integration. One incomplete acquisition must not stop independent proposal work.
''')
print(json.dumps(dict(prepared=len(manifest['requests']),commit=sha,root_tree=tree)))

