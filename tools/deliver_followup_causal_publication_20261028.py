"""Deliver verified publication, source originals and exact reviewed scripts."""
import json,subprocess
from execute_followup_causal_publication_20261028 import ROOT,BASE,step

def main():
    checkpoint=json.loads((BASE/'publication-checkpoint.json').read_text());assert checkpoint['status']=='published_checked'
    paths={'docs/program/state.json','docs/mission-control.md','docs/mission-control.html','docs/program/execution/current-program.md','docs/literature/fetch-manifest.json','tools/audit_recovery_staging_v3_20261028.py','tools/audit_census_acceptance_scope_20261028.py','docs/papers/Causal Inference with Large Language Model A Survey Ma(2024).pdf','docs/papers/Causal-LLaVA Causal Disentanglement for Mitigating Hallucination in Multimodal Large Language Models Hu(2025).pdf','tools/reconcile_followup_identities_20261028.py','tools/prepare_followup_publication_20261028.py','tools/prepare_followup_execution_20261028.py'}
    for pattern in ['tools/*followup_causal*20261028.py','docs/program/execution/2026-10-28/*followup-causal*','docs/program/execution/2026-10-28/followup-identity-reconciliation-v1','docs/program/execution/2026-10-28/census-acceptance-scope-v1','docs/literature/raw/exec28_followup*']:
        paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
    for key in ['reader','sponsor']:
        paths.add(checkpoint[key]['path']);tex=(ROOT/checkpoint[key]['path']).with_suffix('.tex')
        if tex.exists():paths.add(str(tex.relative_to(ROOT)))
    for name in ['push-verification.json','delivery-consumed.json','git-commit.log','git-push.log']:
        p=BASE.parent/'causal-modeling-lead-v1'/name
        if p.exists():paths.add(str(p.relative_to(ROOT)))
    step('stage-publication',['git','add','-f','--',*sorted(paths)])
    step('staging-audit',['python3','tools/audit_recovery_staging_v3_20261028.py',str(BASE.relative_to(ROOT))])
    step('authored-whitespace-check',['git','diff','--cached','--check','--','tools','docs/mission-control.md','docs/program/execution/current-program.md'])
    subprocess.run(['git','add','-f','--',str(BASE.relative_to(ROOT))],cwd=ROOT,check=True)
    step('git-commit',['git','-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit','-m','Integrate causal task survey and representation assumptions with reconciled source queue'])
    step('git-push',['git','push'])
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert commit==remote
    p=BASE/'push-verification.json';assert not p.exists();p.write_text(json.dumps(dict(status='pass',commit=commit,origin_main=remote),indent=2)+chr(10))
    print(json.dumps(dict(pushed=commit)),flush=True)

if __name__=='__main__':main()
