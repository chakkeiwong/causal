#!/usr/bin/env python3
"""Preserve recovery evidence and register bounded inert primary-source reads."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-22/r-iv-rd-v1'
RAW = ROOT/'docs/literature/raw'
MANIFEST = ROOT/'docs/literature/fetch-manifest.json'


def main():
    assert not (BASE/'prior-fetch-manifest.json').exists()
    (BASE/'prior-fetch-manifest.json').write_bytes(MANIFEST.read_bytes())
    for source, destination in [
        ('/tmp/causal-oct22-riv-runtime-check.json', 'baseline-runtime-check.json'),
        ('/tmp/causal-oct22-riv-master-check.json', 'baseline-master-check.json'),
        ('/tmp/causal-oct22-riv-next.json', 'baseline-next.json')]:
        (BASE/destination).write_bytes(Path(source).read_bytes())
    (BASE/'baseline-state.json').write_bytes((ROOT/'docs/program/state.json').read_bytes())
    requests = [
        dict(id='exec22_riv_aer_cutoff', url='https://api.github.com/repos/cran/AER/commits?until=2026-10-07T15%3A59%3A59Z&per_page=1', extension='json'),
        dict(id='exec22_riv_rdrobust_history', url='https://api.github.com/repos/cran/rdrobust/commits?path=DESCRIPTION&per_page=30', extension='json'),
        dict(id='exec22_riv_gpl2', url='https://cran.r-project.org/web/licenses/GPL-2', extension='txt'),
        dict(id='exec22_riv_gpl3', url='https://cran.r-project.org/web/licenses/GPL-3', extension='txt')]
    audit=json.loads((ROOT/'docs/program/repair-v12/work/SW01/source-audit.json').read_text())
    for pkg, paths in {'ivreg':['man/summary.ivreg.Rd','man/ivreg.fit.Rd','NEWS.md'],
                       'ivmodel':['LICENSE','man/ivmodel.Rd','man/ARsens.test.Rd']}.items():
        entry=next(s for s in audit['entries'] if s['id']=='v12:pinned-package:'+pkg)
        for i,path in enumerate(paths):
            requests.append(dict(id=f'exec22_riv_{pkg}_{i}',
                url=f'https://raw.githubusercontent.com/cran/{pkg}/{entry["commit"]}/{path}',extension='txt'))
    value=dict(requests=requests)
    write(BASE/'identity-manifest.json',value)
    MANIFEST.write_text(json.dumps(value,indent=2)+'\n')
    write(BASE/'plan-review.json',dict(status='pass_for_execution',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/'plan.md','Seven-step scientific and preserving-publication plan'),
                  ref(BASE/'baseline-runtime-check.json','Recovered passing runtime check'),
                  ref(BASE/'baseline-master-check.json','Recovered passing master check')],
        checks=['No global or phase blocker; package and publication transitions remain sequential.',
            'Resolve umbrella aliases; freeze source pins; retain incomplete coverage and runtime limitations.',
            'Inspect official technical originals; no new scholarly paper claim without genuine PDF.',
            'Use exact authored laws as semantic references, not native package or empirical-coverage results.',
            'Current source retrieval is later than the client cutoff; distinguish dated commit evidence from mutable rights pages.']))
    print(json.dumps(dict(requests=len(requests),manifest=str((BASE/'identity-manifest.json').relative_to(ROOT)))))


if __name__=='__main__':
    main()
