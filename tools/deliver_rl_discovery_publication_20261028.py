"""Stage bounded recovery/publication work with transitive custody,commit and push."""
import json,subprocess
from execute_rl_discovery_publication_20261028 import ROOT,BASE,step

def main():
    assert json.loads((BASE/'publication-consumed.json').read_text())['actual_exit_code']==0
    paths={'docs/program/state.json','docs/mission-control.md','docs/mission-control.html','docs/program/execution/current-program.md','docs/program/execution/followup-current.json','docs/literature/fetch-manifest.json'}
    patterns=['tools/*rl_discovery*20261028.py','tools/dispatch_rl_followup_20261028.py','tools/*attention*20261028.py','docs/program/execution/2026-10-28/*rl-discovery*','docs/causal_proposal_rl_discovery_reviewed*2026-10-28.*','docs/sponsor_proposal_rl_discovery_reviewed*2026-10-28.pdf','docs/literature/raw/exec28_attention_*','docs/literature/raw/exec28_tcdf_*','docs/literature/raw/exec28_inverted_*','tools/*boundary*20261028.py','tools/*followup*20261028.py','tools/*cdt*20261028.py','tools/*l1_successor*20261028.py','tools/review_local_server_profile_20261028.py','tools/review_python_tail_delta_20261028.py','tools/review_rl_discovery_tail_20261028.py','docs/program/execution/2026-10-28/*boundary*','docs/program/execution/2026-10-28/followup-runtime-v*','docs/program/execution/2026-10-28/l1-current-criterion-v1','docs/causal_proposal_boundary_profile_reviewed*2026-10-28.*','docs/sponsor_proposal_boundary_profile_reviewed*2026-10-28.pdf','docs/literature/raw/exec28_cdt_*','docs/literature/raw/exec28_ollama_server_*','docs/literature/raw/exec28_rl_*','docs/literature/raw/exec28_corl_*']
    for pattern in patterns:paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
    for title in ['Causal Discovery with Reinforcement Learning Zhu(2020).pdf','Ordering-Based Causal Discovery with Reinforcement Learning Wang(2021).pdf','Causal Discovery with Inverted Self-attention for Multivariate Time Series Liu(2026).pdf']:paths.add('docs/papers/'+title)
    for name in ['delivery-consumed.json','push-verification.json']:paths.add('docs/program/execution/2026-10-28/boundary-profile-review-v2/'+name)
    step('stage-publication',['git','add','-f','--',*sorted(paths)])
    step('staging-audit',['python3','tools/audit_recovery_staging_v3_20261028.py',str(BASE.relative_to(ROOT))])
    step('authored-whitespace-check',['git','diff','--cached','--check','--','tools','docs/mission-control.md','docs/program/execution/current-program.md'])
    subprocess.run(['git','add','-f','--',str(BASE.relative_to(ROOT))],cwd=ROOT,check=True)
    step('git-commit',['git','-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit','-m','Preserve RL discovery publication and recover attention source reviews'])
    step('git-push',['git','push'])
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert commit==remote
    p=BASE/'push-verification.json';assert not p.exists();p.write_text(json.dumps(dict(status='pass',commit=commit,origin_main=remote),indent=2)+'\n')
    print(json.dumps(dict(pushed=commit)),flush=True)

if __name__=='__main__':main()
