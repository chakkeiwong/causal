#!/usr/bin/env python3
"""Retarget an unexecuted benchmark publication to the repaired sponsor."""
import ast,json,re
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'
BASE=ROOT/'docs/program/execution/2026-10-25/benchmark-oracles-v1'
RECOVERY=ROOT/'docs/program/execution/2026-10-28/benchmark-publication-recovery-v1'
def save(name,s):
    p=TOOLS/(name+'_20261028.py');assert not p.exists();ast.parse(s);p.write_text(s);return p
def main():
    assert not RECOVERY.exists();RECOVERY.mkdir()
    s=(TOOLS/'build_benchmark_oracles_sponsor_20261025.py').read_text().replace('sponsor-agent-evaluation-surveys-v1','sponsor-agent-evaluation-surveys-v2')
    builder=save('build_benchmark_oracles_sponsor_v2',s)
    s=(TOOLS/'publish_benchmark_oracles_sponsor_20261025.py').read_text().replace('build_benchmark_oracles_sponsor_20261025','build_benchmark_oracles_sponsor_v2_20261028')
    publisher=save('publish_benchmark_oracles_sponsor_v2',s)
    s=(TOOLS/'refresh_benchmark_oracles_program_20261025.py').read_text().replace('Updated 25 October 2026','Updated 28 October 2026')
    refresher=save('refresh_benchmark_oracles_program_v2',s)
    s=(TOOLS/'execute_benchmark_oracles_publication_v2_20261025.py').read_text().replace('publication-plan-review-v2.json','publication-plan-review-v3.json')
    replacements={'build_benchmark_oracles_sponsor':'build_benchmark_oracles_sponsor_v2_20261028','publish_benchmark_oracles_sponsor':'publish_benchmark_oracles_sponsor_v2_20261028','refresh_benchmark_oracles_program':'refresh_benchmark_oracles_program_v2_20261028'}
    for old,new in replacements.items():s=s.replace(chr(39)+old+chr(39),chr(39)+new+chr(39))
    s=s.replace("'tools/'+stem+'_20261025.py'","'tools/'+(stem if stem.endswith('_20261028') else stem+'_20261025')+'.py'")
    executor=save('execute_benchmark_oracles_publication_v3',s)
    s=(TOOLS/'deliver_benchmark_oracles_publication_v2_20261025.py').read_text().replace('from execute_benchmark_oracles_publication_v2_20261025','from execute_benchmark_oracles_publication_v3_20261028')
    s=s.replace("'tools/*benchmark_oracle*20261025.py'","'tools/*benchmark_oracle*20261025.py','tools/*benchmark*20261028.py','docs/program/execution/2026-10-28/benchmark-publication-recovery-v1','docs/program/execution/2026-10-28/crash-recovery-v1'")
    delivery=save('deliver_benchmark_oracles_publication_v3',s)
    import build_benchmark_oracles_sponsor_v2_20261028 as build
    text=build.manuscript(1723);prior=(build.PRIOR/'proposal.md').read_text()
    cites=lambda t:{k.strip() for g in re.findall(build.engine.shared.CITE,t) for k in g.split(',')}
    old,new=cites(prior),cites(text);assert len(old)==1031 and len(new)==1035 and old<=new
    assert ''.join(text.split())==''.join((BASE/'expected-sponsor.md').read_text().split())
    (RECOVERY/'expected-sponsor.md').write_text(text)
    oldplan=json.loads((BASE/'publication-plan-review-v2.json').read_text());verify_bindings(oldplan)
    plan=dict(status='pass_for_serial_publication_after_consumed_predecessor',client_date='2026-10-28',supersedes=ref(BASE/'publication-plan-review-v2.json','Preserved unexecuted original plan'),evidence=oldplan['evidence']+[ref(p,'Reviewed corrected predecessor successor') for p in [builder,publisher,refresher,executor,delivery,Path(__file__)]]+[ref(RECOVERY/'expected-sponsor.md','Exact nonwhitespace preservation;1035records'),ref(ROOT/'docs/program/execution/2026-10-28/crash-recovery-v1/sponsor-layout-repair.json','Predecessor whitespace-only repair')],steps=oldplan['steps'],expected=oldplan['expected'],checks=oldplan['checks']+['Use repaired survey sponsor v2;preserve all1031source records.','Retargeting changes no nonwhitespace benchmark sponsor content.','Actual delivery exit and predecessor push still required before execution.'],global_blocker=None,phase_boundaries_are_stopping_points=False)
    verify_bindings(plan);write(BASE/'publication-plan-review-v3.json',plan)
    print('Benchmark successor reviewed against the repaired survey sponsor.')
if __name__=='__main__':main()
