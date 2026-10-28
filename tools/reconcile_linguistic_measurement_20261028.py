"""Integrate one backward-chain original without closing unrelated census rows."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings,transition
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-28/linguistic-measurement-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-28/recovered-followups-v1'
READER=ROOT/'docs/program/execution/2026-10-28/linguistic-measurement-reader-v1'
read=lambda p:json.loads(p.read_text())


def main():
    for p in [BASE/'review.json',READER/'working-release.json',PRIOR/'census-register.json']:
        verify_bindings(read(p))
    reg=deepcopy(read(PRIOR/'census-register.json'));before=Counter(x['disposition'] for x in reg['items'])
    row=next(x for x in reg['items'] if x['id']=='LA01-longitudinal-search')
    action='Compare the remaining longitudinal candidates against explicit intervention, history, measurement, support and evaluation contracts. The selected Pryzant preprint and three runtime inventories are integrated; do not repeat completed queries or unavailable original routes. Seek distinct permitted originals for the remaining31 census rows and unresolved Taubman/Petersen/LDPE and edition identities. Full native benchmark and component adoption remain separate open obligations.'
    row.update(effect_on_claims='Selected CausalCollab backward-chain Pryzant preprint is retained with inspected technical anchors, version limits and an exact independently authored stochastic-measurement witness. Other selected references remain omissions. No existing census original disposition closes.',
               backward_chain=ref(BASE/'review.json','Primary paper and precise runtime integration'),
               omissions=ref(BASE/'omissions-register.json','Unadmitted originals and edition boundaries'),next_action=action)
    assert Counter(x['disposition'] for x in reg['items'])==before
    reg.update(supersedes=ref(PRIOR/'census-register.json','Preserved82/31and4crosscutting'),
               changes=['Adjacent linguistic measurement preprint inspected; existing census dispositions unchanged.'],closure=False)
    write(BASE/'census-register.json',reg)
    run=controller.base;core=run.core;state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None
    note=dict(finding='Connected linguistic measurement and executable-policy argument is integrated with one genuine preprint, an exact heterogeneous measurement witness and three pinned component-specific adoption findings. Existing census remains82/31plus4crosscutting; no native or rights admission.',
              next_action=action,yield_reason='Reviewed substantive delta integrated; remaining independent obligations continue.',
              evidence=[state['execution_program']['progress']['LL.CENSUS'][-1],ref(BASE/'census-register.json','Unchanged census dispositions'),ref(BASE/'review.json','Source and arithmetic review'),ref(READER/'working-release.json','Exact current monograph'),ref(Path(__file__),'Serial reconciliation')])
    write(BASE/'integrated-progress.json',note)
    digest=core.sha(ROOT/core.STATE);event=run.apply(ROOT,state,'start','LL.CENSUS',reason='Record reviewed backward-chain source and connected intervention argument.');run.commit(ROOT,digest,state,event)
    transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
    state=core.read(ROOT,core.STATE);_,merged,_=run.combined(ROOT,state);saved=merged['execution_program']['progress']['LL.CENSUS'][-1]
    assert saved['path']==str((BASE/'integrated-progress.json').relative_to(ROOT)) and state['execution_runtime']['active'] is None
    verify_bindings(saved)
    write(BASE/'census-reconciliation.json',dict(status='pass',counts=dict(before),evidence=[saved],new_scholarly_originals=1,census_dispositions_changed=0,next_action=action))
    print(json.dumps(dict(census_inspected=82,unread=31,crosscutting=4,new_originals=1)))


if __name__=='__main__':main()
