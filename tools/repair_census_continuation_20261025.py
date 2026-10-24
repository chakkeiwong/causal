#!/usr/bin/env python3
"""Preserve old census bytes and supersede stale resume and availability text."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings, transition
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/census-continuation-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-25/ecmo-integration-v1/census-register.json'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=read(ROOT/'docs/program/state.json')
    assert state['execution_runtime']['active'] is None
    prior=read(PRIOR);verify_bindings(prior)
    counts=Counter(x['disposition'] for x in prior['items'])
    assert counts['inspected_primary_retained_with_limits']==82 and counts['open_original_not_inspected']==31
    clinical=ROOT/'docs/program/execution/2026-10-24/census-clinical-evaluation-v1/acquisition-review.json'
    workflow=ROOT/'docs/program/execution/2026-10-24/census-energy-workflow-v1/acquisition-review.json'
    for p in [clinical,workflow]:verify_bindings(read(p))
    changes={}
    for x in read(clinical)['items']:
        changes[x['candidate']]=dict(availability='Recorded official PDF route returned a non-PDF client challenge; selected original remains unread. No global unavailability claim.',
            next_action='Seek a distinct legitimate permitted author/repository original or supplied authentic copy; do not repeat the unchanged challenged route.',
            evidence=ref(clinical,'Candidate-specific authentic acquisition failure'))
    for x in read(workflow)['items']:
        changes[x['candidate']]=dict(availability=x['reason'],
            next_action='Seek a legitimate permitted authentic-original route or supplied local original. Preserve the fixed collector boundary and do not repeat unchanged unavailable routes.',
            evidence=ref(workflow,'Candidate-specific identity and allowed-route review'))
    additional=[
        ('LA01-candidate-163','docs/program/execution/2026-10-24/census-causal-compositional-v1/acquisition-review.json',
         'Original repository route is outside the fixed collector; metadata has identity inconsistencies and no exact-title arXiv original was found. Related affordance/fuzzing papers do not replace this original.'),
        ('LA01-candidate-217','docs/program/execution/2026-10-24/census-mdc-bench-v1/route-review.json',
         'Original publisher route is outside the fixed collector; exact cutoff date is unresolved. Retrieved arXiv/GitHub leads were not established as this work.'),
        ('LA01-candidate-27','docs/program/execution/2026-10-17/census-recovery/search-v8/search-v7-observations.json',
         'Recorded DOI, author, metadata and exact-title arXiv routes did not supply a genuine original; Semantic Scholar returned no open-access PDF URL. No global unavailability claim.'),
    ]
    for key,path,finding in additional:
        source=ROOT/path;verify_bindings(read(source))
        changes[key]=dict(availability=finding,
            next_action='Pursue a distinct legitimate permitted original route or supplied authentic copy and resolve identity/date where required; do not repeat unchanged failed routes or substitute a related work.',
            evidence=ref(source,'Preserved candidate-specific access and identity findings'))
    successor=deepcopy(prior)
    for x in successor['items']:
        if x['id'] in changes:
            change=changes[x['id']]
            assert x['disposition']=='open_original_not_inspected'
            x['prior_availability_text']=x.get('availability')
            x['availability']=change['availability'];x['next_action']=change['next_action']
            x['availability_evidence']=change['evidence']
    successor['status']='preserving_continuation_and_availability_reconciliation'
    successor['supersedes']=ref(PRIOR,'Preserved 82/31 census with stale free-text interpretation')
    successor['counts']=dict(counts)
    successor['interpretation']='82 of 113 candidate works have selected originals inspected; 31 remain unread and four crosscutting tasks remain open. Original inspection is not complete version, coverage, native or final acceptance.'
    successor['changes']=['No candidate disposition changes. Correct stale 81/32 interpretation from actual item counts.',
        'Reconcile eight previously recorded local acquisition limits with their candidate availability and continuation fields; preserve earlier text and source records.']
    successor['evidence']=[ref(PRIOR,'Exact predecessor'),ref(clinical,'Three recorded clinical/code challenges'),ref(workflow,'Two recorded workflow/energy route limits')]+[x['evidence'] for x in changes.values()]
    assert Counter(x['disposition'] for x in successor['items'])==counts
    BASE.mkdir();write(BASE/'census-register.json',successor)
    old=state['execution_program']['progress']['LL.CENSUS'][-1]
    note=dict(finding='ECMO selected original and its paired reader/sponsor are published; actual census is 82 inspected, 31 unread and four crosscutting obligations. Earlier 32-unread resume text and eight stale availability descriptions are superseded, with all prior bytes retained.',
        next_action='Continue the 31 unread originals and four crosscutting census tasks using authentic permitted sources. Preserve candidate-specific access/date/final-version omissions and avoid unchanged failed routes. ECMO, judge-bias, Java and C++ integrations are already completed; do not rebuild them. Advance independent software, concrete commercial and agent reuse obligations.',
        yield_reason='Census remains open; corrected durable continuation prevents repetition while independent work proceeds.',
        evidence=[old,ref(BASE/'census-register.json','Reconciled counts and eight acquisition limits'),
                  ref(ROOT/'docs/program/execution/2026-10-25/ecmo-integration-v1/push-verification.json','Completed ECMO delivery'),
                  ref(ROOT/'docs/program/execution/2026-10-25/panels-cxx-v2/push-verification.json','Completed C++ delivery')])
    write(BASE/'integrated-progress.json',note)
    review=dict(status='pass_for_continuation_consistency',
        evidence=[ref(BASE/'census-register.json','No disposition changes'),ref(BASE/'integrated-progress.json','Current exact continuation'),ref(Path(__file__),'Preserving repair')],
        corrected_candidate_ids=sorted(changes),counts=dict(counts),new_originals_inspected=0,new_capabilities=[],
        original_records_preserved=True,global_blocker=False)
    verify_bindings(review);write(BASE/'review.json',review)
    transition('progress','LL.CENSUS',BASE/'integrated-progress.json')
    latest=read(ROOT/'docs/program/state.json')
    view=controller.status(ROOT,latest)
    assert view['next']=='LL.CENSUS' and view['next_action']==note['next_action']
    write(BASE/'verification.json',dict(status='pass',next=view['next'],next_action=view['next_action'],
        checkpoint=latest['execution_program']['progress']['LL.CENSUS'][-1],evidence=[ref(BASE/'review.json','Reviewed preserving correction')]))
    print(json.dumps(dict(repaired='LL.CENSUS continuation',inspected=82,unread=31,acquisition_text_repairs=len(changes),dispositions_changed=0)))


if __name__=='__main__':main()
