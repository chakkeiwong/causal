"""Record a reviewed later search lead and preserve exact census contract scope."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings,transition
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'causal-modeling-lead-v1';PRIOR=DAY/'linguistic-measurement-v1';READER=DAY/'causal-modeling-reader-v1';SCOPE=DAY/'census-acceptance-scope-v1'
read=lambda p:json.loads(p.read_text())

def main():
    for p in [BASE/'review.json',READER/'working-release.json',PRIOR/'census-register.json',SCOPE/'review.json']:verify_bindings(read(p))
    reg=deepcopy(read(PRIOR/'census-register.json'));counts=Counter(x['disposition'] for x in reg['items'])
    rows=deepcopy(read(SCOPE/'followup-lead-register.json'));changed=0
    for x in rows['rows']:
        if x['title']=='Evaluating Large Language Models for Causal Modeling':
            x.update(disposition='primary_original_reviewed_with_limits',source_key='exec28_cm_razouk',original_review=ref(BASE/'review.json','Versioned original inspected; no native qualification'),next_action='Use only source-specific tasks, generated-label evaluation and qualified claims; code/data rights and runtime remain separate.');changed+=1
    assert changed==2
    rows.update(predecessor=ref(SCOPE/'followup-lead-register.json','All95rows preserved'),reviewed_original_rows=changed,all_identities_reconciled=False)
    write(BASE/'followup-lead-register.json',rows)
    action='Reconcile the remaining93 followup-search rows against retained source identities, versions and explicit acquisition limits; two rows now bind the inspected Razouk preprint. Preserve all113 original census candidates,31unread and14task mappings. Apply the actual literature-disposition criteria: explicit unavailable-source impacts and two complementary bounded routes plus citation chains; do not require native product qualification or claim exhaustive search. Address accessible direct leads first, preserve distinct local blockers, and do not repeat completed publications or unchanged failed requests.'
    row=next(x for x in reg['items'] if x['id']=='LA01-longitudinal-search')
    row.update(effect_on_claims='Retained two-provider search routes, backward/forward chains and95later metadata rows are now distinguished. One direct causal-modeling original is inspected and integrated;93later rows still require explicit current-identity reconciliation. Native adoption and bank validation are not literature-search criteria.',scope_review=ref(SCOPE/'review.json','Contract diagnosis without acceptance change'),later_leads=ref(BASE/'followup-lead-register.json','All95rows with2original-review bindings'),next_action=action)
    assert Counter(x['disposition'] for x in reg['items'])==counts
    reg.update(supersedes=ref(PRIOR/'census-register.json','Unchanged113candidate dispositions'),changes=['One later original source integrated; scope and later-search reconciliation queue explicit.'],interpretation='82of113 inherited candidate originals inspected;31unread;4crosscutting records. Additional related and later-search originals have separate identities; no denominator substitution.',closure=False)
    write(BASE/'census-register.json',reg)
    run=controller.base;core=run.core;state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
    note=dict(finding='Causal-variable modeling original,generated-label limits and exact semantic/interaction/cancellation examples integrated. Contract audit separates bounded literature disposition from native qualification;95later search rows retained,2bound to this inspected original.',next_action=action,yield_reason='Reviewed publication complete;remaining source-identity reconciliation has an explicit finite queue.',evidence=[state['execution_program']['progress']['LL.CENSUS'][-1],ref(BASE/'review.json','Source/math review'),ref(BASE/'census-register.json','Preserved counts and precise scope'),ref(BASE/'followup-lead-register.json','Complete followup queue'),ref(READER/'working-release.json','Exact reader'),ref(SCOPE/'review.json','Actual acceptance requirements'),ref(Path(__file__),'Serial reconciliation')])
    write(BASE/'integrated-progress.json',note);digest=core.sha(ROOT/core.STATE);event=run.apply(ROOT,state,'start','LL.CENSUS',reason='Record causal-variable original and correct literature-disposition scope.');run.commit(ROOT,digest,state,event)
    transition('yield','LL.CENSUS',BASE/'integrated-progress.json');state=core.read(ROOT,core.STATE);_,merged,_=run.combined(ROOT,state);saved=merged['execution_program']['progress']['LL.CENSUS'][-1]
    assert saved['path']==str((BASE/'integrated-progress.json').relative_to(ROOT)) and state['execution_runtime']['active'] is None;verify_bindings(saved)
    write(BASE/'census-reconciliation.json',dict(status='pass',counts=dict(counts),evidence=[saved],new_scholarly_originals=1,census_dispositions_changed=0,remaining_later_rows=93,next_action=action));print(json.dumps(dict(census=82,unread=31,followup_rows=95,reviewed_later_rows=2)))

if __name__=='__main__':main()
