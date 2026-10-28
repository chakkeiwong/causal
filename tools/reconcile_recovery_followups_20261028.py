#!/usr/bin/env python3
"""Attach completed source followups to the current program without false closure."""
from collections import Counter
from copy import deepcopy
import json,subprocess
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings,transition
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-28/recovered-followups-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-25'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();BASE.mkdir(parents=True)
    run=controller.base;core=run.core;state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_benchmark_oracles_reviewed_v1_2026-10-25.pdf'
    push=read(PRIOR/'benchmark-oracles-v1/push-verification.json')
    consume=read(PRIOR/'benchmark-oracles-v1/delivery-consumed-20261028.json')
    assert push['status']=='pass' and consume['exit_code']==0 and consume['commit']==push['commit']
    for rev in ['HEAD','origin/main']:assert subprocess.check_output(['git','rev-parse',rev],cwd=ROOT,text=True).strip()==push['commit']
    sources=[PRIOR/'runtime-artifact-gaps-v1/review.json',PRIOR/'runtime-artifact-gaps-v1/remaining-artifact-register.json',PRIOR/'longitudinal-specificity-v1/search-review.json',PRIOR/'longitudinal-specificity-v1/followup-review.json',PRIOR/'longitudinal-specificity-v1/conference-chain-review-20261028.json']
    for p in sources:verify_bindings(read(p))
    reg=deepcopy(read(PRIOR/'runtime-artifact-gaps-v1/census-register.json'));before=Counter(x['disposition'] for x in reg['items'])
    row=next(x for x in reg['items'] if x['id']=='LA01-longitudinal-search')
    row.update(effect_on_claims='Four bounded metadata queries returned35unique candidates;arXiv exact-title followup returned429;separate preprint and conference forward queries returned0indexed records. No original or technical claim was admitted;no absence or saturation inference.',source_followup=ref(PRIOR/'longitudinal-specificity-v1/search-review.json','Bounded candidate discovery only'),forward_chain=ref(PRIOR/'longitudinal-specificity-v1/conference-chain-review-20261028.json','Distinct conference query and limits'),next_action='Inspect the retained CausalCollab original reference list for a bounded backward chain and resolve the LDPE original through a distinct permitted route. Do not repeat unchanged429or infer absence from zero indexed citations.')
    assert Counter(x['disposition'] for x in reg['items'])==before
    reg.update(supersedes=ref(PRIOR/'runtime-artifact-gaps-v1/census-register.json','Preserved source and component followups'),changes=['Completed longitudinal followup results reconciled on28October2026;no census disposition closed.'],closure=False)
    write(BASE/'census-register.json',reg)
    action='Continue a bounded backward chain from the retained CausalCollab original and seek a distinct permitted LDPE original route. The finite benchmark-oracle derivation,three runtime-artifact inventories,and both forward-identity queries are complete;do not repeat them. Full native benchmark qualification,missing artifact permissions/weights,and31original-source obligations remain open.'
    note=dict(finding='Crash recovery completes survey and independent benchmark publications;three exact runtime-artifact inventories and seven bounded search requests are reconciled. Counts remain82inspected/31unread plus4crosscutting. No native,rights or final acceptance inferred.',next_action=action,yield_reason='Completed source followups are durably recorded;remaining access,artifact and qualification constraints stay explicit.',evidence=[state['execution_program']['progress']['LL.CENSUS'][-1],ref(BASE/'census-register.json','Current original and crosscutting dispositions')]+[ref(p,'Completed bounded followup') for p in sources]+[ref(Path(__file__),'Reviewed serial reconciliation')])
    write(BASE/'integrated-progress.json',note)
    issues=run.validate_state(ROOT,state);assert not issues,issues
    digest=core.sha(ROOT/core.STATE);event=run.apply(ROOT,state,'start','LL.CENSUS',reason='Record recovered source followups and concrete unresolved artifact requirements.');run.commit(ROOT,digest,state,event)
    transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
    state=core.read(ROOT,core.STATE);_,merged,_=run.combined(ROOT,state);saved=merged['execution_program']['progress']['LL.CENSUS'][-1];verify_bindings(saved)
    assert saved['path']==str((BASE/'integrated-progress.json').relative_to(ROOT)) and state['execution_runtime']['active'] is None
    old=read(PRIOR/'program-refresh-benchmark-oracles-v1/remaining-operations.json');remaining=deepcopy(old)
    row=next(x for x in remaining['operations'] if x['id']=='LL.CENSUS');row.update(action=action,action_checkpoint=saved)
    remaining.update(census=ref(BASE/'census-register.json','82/31and4crosscutting retained'),predecessor=ref(PRIOR/'program-refresh-benchmark-oracles-v1/remaining-operations.json','376-obligation reconciliation retained'))
    write(BASE/'remaining-operations.json',remaining)
    current=ROOT/'docs/program/execution/current-program.md';text=current.read_text();(BASE/'prior-current-program.md').write_text(text)
    header='## Recovered execution and remaining evidence\n\n'
    addition=header+'Recovery on 28 October 2026 completed the interrupted survey and the prepared benchmark-oracle publication. The saved failed sponsor build remains preserved; its corrected successor changes only whitespace. Both publication pairs pass their source, arithmetic and all-page text checks. Visual and final acceptance remain open.\n\n'
    addition+='The [current followup register](2026-10-28/recovered-followups-v1/remaining-operations.json) preserves all 376 obligations. The [artifact register](2026-10-25/runtime-artifact-gaps-v1/remaining-artifact-register.json) identifies specific unresolved root/component permissions for LLM-CD and LLM-and-SCD, exact external LCM weights and terms, dependency identities and loader conformance. These are local runtime-adoption limits, not evidence that the scientific literature is unavailable.\n\n'
    addition+='Four specialist queries produced 35 unique metadata candidates. The exact-title arXiv followup returned 429; preprint and conference forward-identity queries returned zero indexed records. These outcomes establish neither technical claims nor search saturation. No new original-source disposition closes.\n\n'
    assert '## Exact continuation' in text and header not in text
    start=text.index('## Exact continuation');text=text[:start]+addition+text[start:]
    start=text.index('Next: LL.CENSUS.');end=text.index('\n\nSerialize canonical mutations',start)
    text=text[:start]+'Next: LL.CENSUS. '+action+text[end:];current.write_text(text)
    review=dict(status='pass_for_recovery_and_followup_reconciliation',evidence=[ref(BASE/'census-register.json','Unchanged dispositions'),ref(BASE/'remaining-operations.json','Complete prior obligations plus updated action'),saved,ref(BASE/'prior-current-program.md','Preserved full program'),ref(current,'Current master and exact continuation')]+[ref(p,'Completed source followup') for p in sources],recorded=350,nonpassing=150,census_inspected=82,census_unread=31,crosscutting=4,native_admission=False,visual_acceptance=False,final_acceptance=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(reconciled=True,recorded=350,nonpassing=150,source_dispositions_changed=0)))
if __name__=='__main__':main()
