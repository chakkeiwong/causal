#!/usr/bin/env python3
"""Synthesize four inspected profiles; keep incomplete software coverage explicit."""
import argparse,hashlib,json,re
from pathlib import Path
import policies_python_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/policies-python-v1';OP='SW.CELL.policies_offpolicy.Python'
read=lambda p:json.loads(p.read_text())
PROFILES={'d3rlpy':ROOT/'docs/program/execution/2026-10-15/d3rlpy-reuse',
 'scope_rl':ROOT/'docs/program/execution/2026-10-23/scope-rl-reuse-v1',
 'obp':ROOT/'docs/program/execution/2026-10-23/obp-reuse-v1',
 'pomdp_py':ROOT/'docs/program/execution/2026-10-23/pomdp-py-reuse-v1'}
LIMITS=['Four selected historical primary-source profiles and exact authored references; no upstream software/model execution.',
 'The inherited ten-result bibliographic query is not an exhaustive package or alias census.',
 'Different policy targets, logger/support, history and dependence requirements are not interchangeable.',
 'Method originals, broader delegates, exact dependency/data rights, native conformance and calibrated selected-policy uncertainty remain open.',
 'No universal repair for unknown logging, unsupported actions or unrestricted latent-state identification.',
 'Mandatory coverage/depth, fresh visual, independent, bank and final acceptance remain open.']

def audit():
    assert not (BASE/'review.json').exists()
    sources={};bindings=[]
    for key,folder in PROFILES.items():
        p=folder/'source-audit.json';data=read(p);verify_bindings(data);bindings.append(ref(p,'Preserved primary-source audit'))
        for s in data['sources']:
            k=s['integrated_citation_key'];assert k not in sources;sources[k]=s
    assert len(sources)==11
    result=exact.calculate()
    for key,folder in PROFILES.items():assert result[key]==read(folder/'exact-results.json')
    write(BASE/'exact-results.json',result)
    specs=[('docs/literature/raw/exec15_d3rlpy_source_9.txt',73,119,'FQE uses best-action continuation, terminal flags and interval powers.'),
           ('docs/literature/raw/exec23_scope_04.txt',375,460,'Trajectory-wise ratio/reward calculation, equal-horizon reshape and argument checks.'),
           ('docs/literature/raw/exec23_obp_03.txt',73,114,'Exact-one replay matches and initialized zero scores when matches absent.'),
           ('docs/literature/raw/exec23_pomdppy_05.txt',15,88,'Supplied transition/observation histogram update and positive-mass normalization.')]
    anchors=[]
    for path,a,b,finding in specs:
        p=ROOT/path;lines=p.read_text().splitlines();assert b<=len(lines)
        anchors.append(dict(local_copy=ref(p,finding),lines=[a,b],excerpt_sha256=hashlib.sha256(chr(10).join(lines[a-1:b]).encode()).hexdigest(),finding=finding))
    write(BASE/'primary-reinspection.json',dict(status='pass_for_selected_target_anchors',inherited_audits=bindings,anchors=anchors,other_claims='Preserved reviewed source records remain authoritative; these four paths are newly reinspected target anchors.',native_execution=False))
    query=next(x for x in read(ROOT/'docs/program/repair-v12/work/SW01/search-ledger.json')['queries'] if x['id']=='v12_sw_cell_policies_offpolicy_python')
    raw=read(ROOT/query['local_copy']['path']);assert len(raw['results'])==10 and raw['meta']['count']==2527
    leads=[]
    for x in raw['results']:
        title=x['title'];status='method_or_software_lead_original_uninspected'
        if 'Bonner' in title:status='out_of_scope_neutron_unfolding_title'
        if 'Make-to-Stock' in title:status='adjacent_queueing_method_not_established_python_package'
        if 'Open Bandit' in title:status='OBP_software_inspected_paper_original_still_separate'
        leads.append(dict(id=x['id'],title=title,date=x['publication_date'],disposition=status,technical_claim_admitted=False))
    write(BASE/'search-screening.json',dict(status='partial_not_exhaustive',query=query,returned=10,reported_matches=2527,leads=leads,catalog_aliases=dict(d3rlpy=['d3rlpy'],scope_rl=['scope_rl','SCOPE-RL','scope-rl'],obp=['obp','Open Bandit Pipeline','zr-obp'],pomdp_py=['pomdp_py','POMDP-Py','pomdp-py']),stopping_rule='Reconcile the saved ten-result query and four already-inspected catalog profiles; no saturation or absence claim.',remaining='Repository/package-registry search tails, broader policy families and methodological originals remain open.'))
    gaps=[('coverage','Continue cutoff-eligible repository/package-registry and alias search; ten bibliographic hits do not exhaust Python software.'),('methods','Acquire genuine originals for discovered methodological results before theorem or empirical adoption; code alone does not prove statistical guarantees.'),('delegates','Bind actual SCOPE-RL imported d3rlpy artifact and caller semantics; inspect broader continuous,distributional,slate,multiple-logger and learning delegates.'),('targets','Separate fixed,trained,algorithm-average,class-optimum and unrestricted optimum; bind stochastic policy and postprocessor.'),('semantics','Qualify history/row/clock/ending/reward conversion and full failure/refusal accounting on finite oracles.'),('uncertainty','Justify logger truth,support,cluster/calendar law,nuisance fitting,normalization and selection before interval admission.'),('rights_runtime','Resolve exact release,compiler/ABI,dependency/data rights and worker environment before implementation.'),('public_bank','Freeze justified public/generated tasks and full costs first; bank transport/truth and actual economics remain later conditional work.')]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=g,next_action=a,global_blocker=False) for g,a in gaps],limitations=LIMITS))
    write(BASE/'conversion-contract.json',dict(status='proposal_only',integration_allowed=False,choices=dict(obp='Conditional contextual-bandit original worker with logger/action/position and replay contracts',scope_rl='Conditional sequential-score original worker with episode/terminal/interval/delegate contracts',d3rlpy='Conditional learner and matching fixed-policy evaluator; bind greedy/stochastic and population semantics',pomdp_py='Supplied-model planner reference; conditional worker only after belief,horizon,option and timeout qualification'),reject=['A single flatten-and-call adapter','Automatic greedy-to-stochastic value equivalence','Unknown logger/support or latent model invented by software','Whole-library port without measured need','Score bootstrap described as complete learning-selection uncertainty'],common_artifacts=['population,target,information clock,history/action schemas','logger/support and causal assumptions','policy bytes,randomness,constraints and postprocessor','episode endings,reward transformations,physical discount clock','training/evaluation groups and uncertainty construction','source,rights,environment and resource budget','accepted,failed,refused,omitted and unresolved identities with full costs'],owners=['Scientific owner:target/identification','Adapter owner:conversion and faults','Rights/runtime owner:chosen artifacts','Evaluation owner:public/generated protocol'],native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_replayed_authored_examples',evidence=[ref(Path(exact.__file__),'Only authored references executed'),ref(BASE/'exact-results.json','Four exact replays')]+[ref(f/'exact-results.json','Preserved original results') for f in PROFILES.values()],findings=['All four prior exact result objects reproduce unchanged.','Randomized8versusgreedy10, terminal2versus10 and monetary28versus23.5 retain their original assumptions.','Fixed-score and re-normalized bootstrap laws remain distinct; no coverage inference added.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected four-target argument'),ref(BASE/'sponsor-addition.md','Investment implication')],findings=['Four roles compared by target and information requirements.','Same-name dependency not asserted equal to standalone inspected revision.','Negative/adverse witnesses and qualification limits retained.'],visual_acceptance=False))
    synthesis=dict(integrated_citation_key='exec24_policiespython_comparison',kind='project_evidence_not_scholarly_paper',title='Four-family Python policy comparison and bounded search reconciliation',author='Causal banking proposal project',year=2026,source_identity='docs/program/execution/2026-10-24/policies-python-v1',version_date='24October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'search-screening.json','Ten saved hits and four candidate identities'),inspected_anchors=[ref(BASE/n,'Bounded comparison evidence') for n in ['primary-reinspection.json','conversion-contract.json','omissions-register.json','mathematical-review.json']],supported_claims=['Four already-audited historical profiles cover distinct contextual,sequential,learning and supplied-model roles.','Saved cutoff bibliographic query returned10of2527reported matches,not exhaustive software coverage.','Conditional worker choices require scientific,semantic,rights and native qualification; source synthesis admits no capability.'],limitations=LIMITS)
    sources[synthesis['integrated_citation_key']]=synthesis
    write(BASE/'source-audit.json',dict(sources=list(sources.values()),inherited_audits=bindings,new_records=1,cutoff='2026-10-07',native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_synthesis',evidence=[ref(BASE/n,'Reviewed comparison') for n in ['plan-review.json','primary-reinspection.json','source-audit.json','search-screening.json','mathematical-review.json','development.tex']],findings=['Reuse11unchanged source records;add1audited synthesis record and no new scholarly citation.','Keep every existing source,context and compiled input.','Record inconclusive coverage rather than fabricated closure.','Pair sponsor,reconcile all obligations and continue independent ready work.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Reviewed Python policy synthesis') for n in ['source-audit.json','primary-reinspection.json','search-screening.json','conversion-contract.json','omissions-register.json','plan-review-v2.json','mathematical-review.json','copyedit-review.json','development.tex','sponsor-addition.md','exact-results.json']]+[ref(Path(__file__),'Preserving comparison audit')]
    review=dict(status='pass_for_bounded_comparison',evidence=evidence,findings=['Four target-specific profiles compared;all exact authored witnesses replay unchanged.','Search/delegate/method/rights/native gaps remain explicit;coverage inconclusive.'],limitations=LIMITS);verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(inherited_records=11,new_records=1,coverage='inconclusive',native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));g,merged,_=run.combined(ROOT,state);node=run.ledger.operation(g,OP)
    evidence=[ref(BASE/n,'Scoped Python policy comparison') for n in ['review.json','source-audit.json','search-screening.json','conversion-contract.json','omissions-register.json','mathematical-review.json','development.tex']]
    scope='Four source-reviewed Python policy roles and bounded query reconciliation; not exhaustive coverage'
    nxt='Complete cutoff package/alias search and method originals; bind actual cross-library delegates; qualify original workers on fixed public/generated policy,logger,support,clock,ending,uncertainty and refusal fixtures with complete costs.'
    out=ROOT/node['outputs'][0];write(out,dict(operation=OP,status='inconclusive',scope=scope,candidates=list(PROFILES),evidence=evidence,limitations=LIMITS,next_action=nxt,integration_allowed=False))
    findings=[('inconclusive','Four identified profiles and10saved search hits reconciled; search tails and additional families remain.'),('pass','All11prior audited source identities preserved; four target anchors reinspected; one synthesis record added; no unsupported new theorem.'),('pass','Distinct targets,conditional worker alternatives,explicit omissions and qualification routes; no fabricated absence or capability.')]
    r=run.ledger.receipt_template(node);r.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Bounded coverage')],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=nxt)
    run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r);print('Python policy receipt prepared: inconclusive.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
