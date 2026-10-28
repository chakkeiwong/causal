"""Deliver verified publication, source originals and exact reviewed scripts."""
import json,subprocess
from execute_linguistic_publication_20261028 import ROOT,BASE,step

def main():
    checkpoint=json.loads((BASE/'publication-checkpoint.json').read_text());assert checkpoint['status']=='published_checked'
    paths={'docs/program/state.json','docs/mission-control.md','docs/mission-control.html','docs/program/execution/current-program.md','docs/literature/fetch-manifest.json','tools/audit_recovery_staging_v3_20261028.py','docs/papers/Causal Effects of Linguistic Properties Pryzant(2020).pdf'}
    for pattern in ['tools/*linguistic*20261028.py','docs/program/execution/2026-10-28/*linguistic*','docs/program/execution/2026-10-28/longitudinal-backward-chain-v1','docs/literature/raw/exec28_lbc*']:
        paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
    for key in ['reader','sponsor']:
        paths.add(checkpoint[key]['path']);tex=(ROOT/checkpoint[key]['path']).with_suffix('.tex')
        if tex.exists():paths.add(str(tex.relative_to(ROOT)))
    for name in ['push-verification.json','delivery-consumed.json','git-commit.log','git-push.log']:
        p=BASE.parent/'recovered-followups-v1'/name
        if p.exists():paths.add(str(p.relative_to(ROOT)))
    step('stage-publication',['git','add','-f','--',*sorted(paths)])
    step('staging-audit',['python3','tools/audit_recovery_staging_v3_20261028.py',str(BASE.relative_to(ROOT))])
    step('authored-whitespace-check',['git','diff','--cached','--check','--','tools','docs/mission-control.md','docs/program/execution/current-program.md'])
    subprocess.run(['git','add','-f','--',str(BASE.relative_to(ROOT))],cwd=ROOT,check=True)
    step('git-commit',['git','-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit','-m','Integrate linguistic intervention assumptions and component-specific adoption evidence'])
    step('git-push',['git','push'])
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert commit==remote
    p=BASE/'push-verification.json';assert not p.exists();p.write_text(json.dumps(dict(status='pass',commit=commit,origin_main=remote),indent=2)+chr(10))
    print(json.dumps(dict(pushed=commit)),flush=True)

if __name__=='__main__':main()
