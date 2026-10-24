#!/usr/bin/env python3
"""Preserve census dispositions and record four new original-route limits."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings, transition
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/census-route-followup-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-25/census-continuation-v1/census-register.json'
SEARCH=ROOT/'docs/program/execution/2026-10-25/census-route-search-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists()
    state=read(ROOT/'docs/program/state.json');assert state['execution_runtime']['active'] is None
    source=read(SEARCH/'acquisition-review.json');verify_bindings(source)
    prior=read(PRIOR);verify_bindings(prior);counts=Counter(x['disposition'] for x in prior['items'])
    assert counts['inspected_primary_retained_with_limits']==82 and counts['open_original_not_inspected']==31
    successor=deepcopy(prior);updates={x['candidate']:x for x in source['items']}
    assert set(updates)=={f'LA01-candidate-{n}' for n in [157,199,202,206]}
    for x in successor['items']:
        if x['id'] not in updates:continue
        y=updates[x['id']];assert x['disposition']=='open_original_not_inspected'
        x['prior_availability_text']=x.get('availability');x['availability']=y['availability'];x['next_action']=y['next_action']
        x['availability_evidence']=ref(SEARCH/'acquisition-review.json','Candidate-specific permitted route findings')
        x['metadata_type_qualification']=y['metadata_type']
    successor.update(status='preserving_four_route_followup',supersedes=ref(PRIOR,'Preserved eight-limit correction'),
        changes=['No disposition changes; four further metadata/original-route limits recorded.','Candidate199 metadata identifies a conference abstract; candidate202 search returned different works; no substitute admitted.'],
        evidence=[ref(PRIOR,'Preserved census'),ref(SEARCH/'acquisition-review.json','Four reviewed route results')])
    assert Counter(x['disposition'] for x in successor['items'])==counts
    BASE.mkdir();write(BASE/'census-register.json',successor)
    note=dict(finding='Census remains82 inspected/31 unread plus four crosscutting tasks. Four bounded identity/title searches for157,199,202,206 did not supply an identity-matched original via the fixed collector; metadata and different works were not admitted as technical evidence.',
        next_action='Continue the 31 unread originals and four crosscutting tasks. Preserve all recorded source/date/identity limits, including157/199/202/206, and seek distinct permitted genuine originals without repeating unchanged blocked routes. Copilot and the commercial network reference decisions are published; continue independent software cells and remaining concrete reuse candidates.',
        yield_reason='Local source-route limits do not block independent proposal obligations.',
        evidence=[state['execution_program']['progress']['LL.CENSUS'][-1],ref(BASE/'census-register.json','Current census and local limits'),ref(SEARCH/'acquisition-review.json','No technical claims from metadata')])
    write(BASE/'integrated-progress.json',note)
    review=dict(status='pass_for_preserving_route_reconciliation',evidence=[ref(BASE/'census-register.json','Unchanged dispositions'),ref(BASE/'integrated-progress.json','Exact continuation'),ref(Path(__file__),'Serial reconciliation')],
        counts=dict(counts),new_originals_inspected=0,claims_admitted=False,global_blocker=False)
    verify_bindings(review);write(BASE/'review.json',review)
    run=controller.base;before=run.core.sha(ROOT/run.core.STATE)
    event=run.apply(ROOT,state,'start','LL.CENSUS',reason='Record four reviewed local source-route limits and continue independent work.')
    run.commit(ROOT,before,state,event)
    transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
    view=controller.status(ROOT,read(ROOT/'docs/program/state.json'));assert view['next_action']==note['next_action']
    write(BASE/'verification.json',dict(status='pass',next=view['next'],next_action=view['next_action'],evidence=[ref(BASE/'review.json','Reviewed followup')]))
    print(json.dumps(dict(route_limits=4,inspected=82,unread=31,dispositions_changed=0)))

if __name__=='__main__':main()
