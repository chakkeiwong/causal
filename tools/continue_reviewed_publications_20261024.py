#!/usr/bin/env python3
"""Finite serial completion of already reviewed publications; stop on real failure."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
DAY=ROOT/'docs/program/execution/2026-10-24'
UNITS=[
 ('dose-alias-reconciliation-v1','dose_alias','Reconcile exact dose-response aliases with paired sponsor'),
 ('backend-census-v1','backend_census','Integrate five pinned backend profiles and repair stale continuations'),
 ('interference-reuse-v1','interference_reuse','Review two interference references with target and policy contracts'),
]


def command(base,name,args):
    log=base/(name+'.log')
    assert not log.exists(),log
    with log.open('x') as out:
        result=subprocess.run(args,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
    event=dict(step=name,command=args,exit_code=result.returncode,log=str(log.relative_to(ROOT)))
    with (base/'delivery-sequence.jsonl').open('a') as out:
        out.write(json.dumps(event)+chr(10))
    print(json.dumps(event),flush=True)
    if result.returncode:raise SystemExit(result.returncode)


def stage_commit_push(folder,stem,message):
    base=DAY/folder
    checkpoint=json.loads((base/'publication-checkpoint.json').read_text())
    assert checkpoint['status']=='published_checked'
    paths={'docs/program/state.json','docs/mission-control.md','docs/mission-control.html','docs/program/execution/current-program.md','tools/continue_reviewed_publications_20261024.py'}
    paths.add(str(base.relative_to(ROOT)))
    for pattern in ['tools/*'+stem+'*20261024.py','docs/program/execution/2026-10-24/*'+stem.replace('_','-')+'*','docs/literature/raw/exec24_'+stem.split('_')[0]+'*']:
        paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
    for key in ['reader','sponsor']:
        paths.add(checkpoint[key]['path'])
        tex=ROOT/checkpoint[key]['path'];tex=tex.with_suffix('.tex')
        if tex.exists():paths.add(str(tex.relative_to(ROOT)))
    for old in ['census-judge-bias-v1','dose-alias-reconciliation-v1','backend-census-v1']:
        for name in ['git-commit.log','git-push.log','push-verification.json','delivery-sequence.jsonl','authored-whitespace-check.log']:
            p=DAY/old/name
            if p.exists():paths.add(str(p.relative_to(ROOT)))
    command(base,'stage-publication',['git','add','-f','--',*sorted(paths)])
    command(base,'staging-audit',['python3','tools/audit_release_staging_20261024.py',folder])
    command(base,'authored-whitespace-check',['git','diff','--cached','--check','--','tools','docs/mission-control.md','docs/program/execution/current-program.md'])
    subprocess.run(['git','add','-f','--',str(base.relative_to(ROOT))],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    command(base,'git-commit',['git','-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit','-m',message])
    command(base,'git-push',['git','push'])
    local=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()
    assert local==remote
    p=base/'push-verification.json';assert not p.exists()
    p.write_text(json.dumps(dict(status='pass',commit=local,origin_main=remote,publication_checkpoint=str((base/'publication-checkpoint.json').relative_to(ROOT))),indent=2)+chr(10))
    print(json.dumps(dict(pushed=folder,commit=local)),flush=True)


def main():
    from publish_latent_r_review_v2_20261013 import verify_bindings
    assert (DAY/'dose-alias-reconciliation-v1/publication-checkpoint.json').exists()
    for i,(folder,stem,message) in enumerate(UNITS):
        base=DAY/folder
        if i:
            plan=json.loads((base/'publication-plan-review.json').read_text());verify_bindings(plan)
            command(base,'execute-publication',['python3','tools/execute_'+stem+'_publication_20261024.py'])
        stage_commit_push(folder,stem,message)
    print('All three reviewed publications checked,committed andpushed.',flush=True)


if __name__=='__main__':main()
