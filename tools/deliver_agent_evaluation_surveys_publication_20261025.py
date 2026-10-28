#!/usr/bin/env python3
"""Deliver the checked survey pair and its preserving source evidence."""
import json,subprocess
from execute_agent_evaluation_surveys_publication_20261025 import ROOT,BASE,step

def main():
    checkpoint=json.loads((BASE/'publication-checkpoint.json').read_text());assert checkpoint['status']=='published_checked'
    paths={'docs/program/state.json','docs/mission-control.md','docs/mission-control.html','docs/program/execution/current-program.md','tools/audit_release_staging_20261025.py','tools/run_with_verified_hash_cache_20261025.py'}
    for pattern in ['tools/*agent_evaluation*20261025.py','docs/program/execution/2026-10-25/*agent-evaluation*','docs/program/execution/2026-10-25/census-observation-workflow-v1','docs/literature/raw/exec25_cow*']:
        paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
    for key in ['reader','sponsor']:
        paths.add(checkpoint[key]['path']);tex=(ROOT/checkpoint[key]['path']).with_suffix('.tex')
        if tex.exists():paths.add(str(tex.relative_to(ROOT)))
    for name in ['publication-sequence.jsonl','git-commit.log','git-push.log','push-verification.json','deliver-publication.log']:
        p=BASE.parent/'data-workflow-wave-v1'/name
        if p.exists():paths.add(str(p.relative_to(ROOT)))
    step('stage-publication',['git','add','-f','--',*sorted(paths)])
    step('staging-audit',['python3','tools/audit_release_staging_20261025.py','agent-evaluation-surveys-v1'])
    step('authored-whitespace-check',['git','diff','--cached','--check','--','tools','docs/mission-control.md','docs/program/execution/current-program.md'])
    subprocess.run(['git','add','-f','--',str(BASE.relative_to(ROOT))],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    step('git-commit',['git','-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit','-m','Integrate primary agent-evaluation surveys and preserve unresolved census obligations'])
    step('git-push',['git','push'])
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert commit==remote
    p=BASE/'push-verification.json';assert not p.exists()
    p.write_text(json.dumps(dict(status='pass',commit=commit,origin_main=remote,publication_checkpoint=str((BASE/'publication-checkpoint.json').relative_to(ROOT))),indent=2)+chr(10))
    print(json.dumps(dict(pushed=commit)),flush=True)

if __name__=='__main__':main()
