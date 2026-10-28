"""Execute a finite reconciliation of all unresolved proposal obligations."""
import json
from collections import Counter
from pathlib import Path
from run_followup_program_20261028 import ROOT,BASE,append,bound,load
from prepare_followup_program_20261028 import ref,write


def main():
    key='GAP.ROUTES';node=load()['nodes'][key]
    source=ROOT/'docs/program/execution/2026-10-28/program-refresh-delegate-contract-v1/remaining-operations.json'
    evidence=[ref(source,'All150current nonpassing obligations')]
    start=BASE/'gap-routes-start.json'
    write(start,dict(task=key,awards_acceptance=False,next_action=node['action'],evidence=evidence))
    append('start',key,str(start.relative_to(ROOT)))
    data=json.loads(source.read_text());rows=[]
    for old in data['operations']:
        identifier=old['id'];basis=old.get('action_basis') or old.get('evidence')
        if basis:bound(ROOT,basis)
        route='bounded_primary_source_and_comparison_successor'
        if old.get('continuation_status')=='blocked_local':route='local_original_access_dependency'
        elif identifier.startswith('SCI.'):route='restricted_research_design_without_promised_universal_solution'
        elif identifier.startswith('SW.REVIEW.'):route='depends_on_explicit_language_coverage_dispositions'
        elif identifier.startswith('SW.DECISION.'):route='artifact_specific_conditional_reuse_review'
        elif identifier=='LL.CENSUS':route='task_specific_original_edition_and_essentiality_review'
        elif identifier=='TEXT.REVIEW.L1':route='preserving_chapter_successor_after_task_coverage_review'
        elif identifier=='TEXT.REVIEW.L6':route='bounded_service_model_artifact_and_migration_profiles'
        elif identifier=='RELEASE.VISUAL':route='fresh_safe_image_allowance_and_release_prerequisites'
        elif identifier.startswith(('RELEASE.','PROPOSAL.')):route='original_acceptance_prerequisites_retained'
        rows.append(dict(id=identifier,original_status=old['status'],route=route,owner='Current author/coordinator',bound_predecessor=basis,exact_original_next_action=old['action'],original_prerequisites=old['prerequisites'],original_outputs=old['outputs'],proposal_work='Primary source,scope,derivation,comparison or manuscript review within the retained contract',later_gate='Native adapter/model effectiveness,bank truth and adoption are separate when mentioned; not invented evidence or a global proposal prerequisite',requires_new_source=route in ['local_original_access_dependency','bounded_primary_source_and_comparison_successor'],awards_acceptance=False))
    assert len(rows)==150 and len({r['id'] for r in rows})==150
    out=BASE/'gap-routes.json'
    write(out,dict(status='performed_route_reconciliation',rows=rows,counts=dict(Counter(r['route'] for r in rows)),evidence=evidence+[ref(Path(__file__),'Exact route classification')],unchanged_original_outcomes=True,scope_limit='Route classification does not establish source availability,scientific feasibility or acceptance.'))
    receipt=BASE/'gap-routes-receipt.json'
    write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'All150routes')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='All150ids retained once with exact prior action and bound evidence when available.'),dict(index=1,verdict='pass',finding='Local access,coverage prerequisites,restricted research and later qualification remain distinct; no original outcome changes.')],next_action='Continue independent L6 profiles,L1 essentiality and software tails; do not rerun route reconciliation.'))
    append('record',key,str(receipt.relative_to(ROOT)))
    print(json.dumps(dict(reconciled=len(rows),routes=Counter(r['route'] for r in rows),next=load()['next'])))


if __name__=='__main__':main()
