"""Stage bounded recovery/publication work with transitive custody,commit and push."""
import json,subprocess
from execute_attention_discovery_publication_20261028 import ROOT,BASE as PUBLICATION
BASE=ROOT/'docs/program/execution/2026-10-28/attention-discovery-delivery-v1'

def step(name,command):
    log=BASE/(name+'.log');assert not log.exists(),log
    with log.open('x') as out:r=subprocess.run(command,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
    event=dict(step=name,exit_code=r.returncode,log=str(log.relative_to(ROOT)))
    with (BASE/'delivery-sequence.jsonl').open('a') as out:out.write(json.dumps(event)+chr(10))
    print(json.dumps(event),flush=True)
    if r.returncode:raise SystemExit(r.returncode)


def main():
    assert json.loads((PUBLICATION/'publication-consumed.json').read_text())['actual_exit_code']==0
    BASE.mkdir(exist_ok=True)
    paths={'docs/program/state.json','docs/mission-control.md','docs/mission-control.html','docs/program/execution/current-program.md','docs/program/execution/followup-current.json','docs/literature/fetch-manifest.json'}
    patterns=['tools/*attention*20261028.py','docs/program/execution/2026-10-28/*attention*','docs/program/execution/2026-10-28/followup-runtime-v5','docs/causal_proposal_attention_discovery_reviewed*2026-10-28.*','docs/sponsor_proposal_attention_discovery_reviewed*2026-10-28.pdf','docs/literature/raw/exec28_attention_*','docs/literature/raw/exec28_tcdf_delegate_*','docs/literature/raw/exec28_tacd_delegate_*']
    for pattern in patterns:paths.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
    for title in ['Causal Discovery with Reinforcement Learning Zhu(2020).pdf','Ordering-Based Causal Discovery with Reinforcement Learning Wang(2021).pdf','Causal Discovery with Inverted Self-attention for Multivariate Time Series Liu(2026).pdf']:paths.add('docs/papers/'+title)
    for name in ['delivery-consumed.json','push-verification.json']:paths.add('docs/program/execution/2026-10-28/rl-discovery-delivery-v2/'+name)
    step('stage-publication',['git','add','-f','--',*sorted(paths)])
    step('staging-audit',['python3','tools/audit_recovery_staging_v3_20261028.py',str(BASE.relative_to(ROOT))])
    step('authored-whitespace-check',['git','diff','--cached','--check','--','tools','docs/mission-control.md','docs/program/execution/current-program.md'])
    subprocess.run(['git','add','-f','--',str(BASE.relative_to(ROOT))],cwd=ROOT,check=True)
    step('git-commit',['git','-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit','-m','Integrate attention discovery evidence and record temporal evaluation protocols'])
    step('git-push',['git','push'])
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert commit==remote
    p=BASE/'push-verification.json';assert not p.exists();p.write_text(json.dumps(dict(status='pass',commit=commit,origin_main=remote),indent=2)+'\n')
    print(json.dumps(dict(pushed=commit)),flush=True)

if __name__=='__main__':main()
