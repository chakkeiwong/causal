#!/usr/bin/env python3
"""Review selected Java originals; retain incomplete ecosystem coverage explicitly."""
import argparse,hashlib,json
from pathlib import Path
import policies_java_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/policies-java-v1';RAW=ROOT/'docs/literature/raw';OP='SW.CELL.policies_offpolicy.Java'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected immutable historical source paths; no downloaded code, build, native worker or bank experiment executed.',
 'Bibliographic and repository search tails, registries, maintained forks and additional policy families remain; no exhaustive coverage or absence claim.',
 'Only selected original-paper sections inspected; original experiments and its separate code distribution not reproduced.',
 'Artifact licenses are inspected declarations, not transitive clearance or legal advice; backend, dependency and data rights remain.',
 'Supplied-model planning, policy learning and causal logged-policy evaluation have distinct targets and evidence.',
 'No universal hidden-state identification, arbitrary-dependence guarantee or calibrated optimal-policy uncertainty established.',
 'Mandatory coverage/depth, Q1/Q5, fresh visual, independent and final acceptance remain open.']
SPECS={
 'burlap_src_00':[(1,176,'Direct Apache2 license text; no transitive clearance')],
 'burlap_src_01':[(1,77,'Project description and README3.0.1 example')],
 'burlap_src_02':[(1,33,'POM3.0.2-SNAPSHOT,Java1.7,license'),(185,300,'Declared numerical/build dependencies only')],
 'burlap_src_05':[(35,180,'Policy-weighted model evaluation, iteration/delta stopping and reachability cache')],
 'burlap_src_07':[(30,67,'LSPI sample reuse, inverse seed100 and terminal warning'),(386,435,'Greedy next features, rank-one inverse update and unguarded denominator'),(442,470,'Weight-change/iteration stopping')],
 'burlap_src_10':[(305,395,'Terminal0, fixed-policy weighted Bellman update, supplied FullModel and option discount distinction')],
 'burlap_src_11':[(24,29,'Fully observed continuation approximation'),(92,177,'Belief averaging, sampled-state action list and underlying planner')],
 'burlap_delegate_00':[(1,144,'SARS state/action/reward/next-state tuple without separate terminal field')],
 'burlap_delegate_01':[(17,140,'Random uniform maximizing ties and policy distribution')],
 'burlap_delegate_02':[(1,70,'Identifier-independent default and relational-state caveat')],
 'chen_src_00':[(1,21,'Direct MIT license')],
 'chen_src_01':[(1,45,'README installation1.0.5')],
 'chen_src_02':[(1,22,'POM1.0.6 and license'),(82,95,'Java1.8 declarations')],
 'chen_src_03':[(85,143,'Maximum next-Q update without terminal argument')],
 'chen_src_04':[(125,169,'Supplied next-action update; max-Q comment differs from expression')],
 'chen_src_05':[(54,104,'Actor preference update uses external V and omits stored gamma from literal TD expression')],
 'chen_delegate_00':[(25,53,'Defaults gamma0.7,alpha0.1,initialQ0.1'),(95,128,'Value and maximum-action delegates')],
 'chen_delegate_01':[(13,86,'Epsilon-greedy selection and shared random-generator copy; action/value return')],
 'rl4j_src_00':[(1,85,'Historical README, preview caveat and advertised families; not native qualification')],
 'rl4j_src_01':[(25,80,'Snapshot parent and module/backend declarations')],
 'rl4j_src_02':[(25,145,'Java1.8,skip-tests and native/media dependencies')],
 'rl4j_src_03':[(25,62,'Snapshot API and ND4J dependency')],
 'rl4j_src_04':[(22,45,'MDP reset,step,done,newInstance interface')],
 'rl4j_src_05':[(40,141,'Next-feature construction, target labels, optional clamp and defaults')],
 'rl4j_src_06':[(28,75,'Standard target-network maximum and terminal suppression')],
 'rl4j_src_07':[(28,80,'Online action selection,target-network evaluation and terminal suppression')],
 'rl4j_src_08':[(29,75,'Transition stores terminal and next observation;dup requires observation objects')],
 'rl4j_src_09':[(34,105,'Distinct-index replay batch,capped size and duplicated transitions')],
 'rl4j_src_10':[(90,141,'DQN choice,target,updater,replay wiring'),(155,202,'Action repetition,reward factor,done and final observation')],
 'rl4j_src_11':[(36,80,'Argmax delegation and serialization boundary')],
 'rl4j_delegate_00':[(33,68,'Online and target network evaluation on next features')],
 'rl4j_delegate_01':[(45,173,'Features constructed before target suppression;recurrent order follows supplied batch;cached metadata')],
 'rl4j_delegate_02':[(35,117,'Pending transitions stored after next observation;reset and episode-end semantics')],
 'rl4j_delegate_03':[(40,48,'Action delegates to ND4J argmax')],
 'rl4j_delegate_04':[(28,74,'Episode-start reset,experience forwarding and final-observation batch')],
 'rl4j_license':[(1,176,'Apache terms'),(203,384,'Additional component notices/terms; bundle not universally cleared')],
 'rl4j_notice':[(1,20,'Root contributor and component notice')],
}

def audit():
    assert not (BASE/'review.json').exists()
    indexes=[]
    for n in ['burlap','chen','delegates','rl4j','rl4j-delegates']:indexes.extend(read(BASE/f'source-index-{n}.json'))
    bykey={x['key'].replace('exec24_policyjava_',''):x for x in indexes}
    records={}
    for k,specs in SPECS.items():
        x=bykey[k];p=ROOT/x['raw_path'];b=p.read_bytes();lines=b.decode().splitlines();rc=RAW/f"{x['key']}.receipt.json";receipt=read(rc)
        assert receipt['sha256']==hashlib.sha256(b).hexdigest()
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob_sha']
        anchors=[]
        for lo,hi,finding in specs:
            hi=min(hi,len(lines));assert lo<=hi
            anchors.append(dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest(),finding=finding))
        records[k]=dict(source_identity=receipt['url'],version_date=x['commit'],upstream_path=x['path'],local_copy=ref(p,'Selected primary source'),receipt=ref(rc,'Public source authentication'),git_blob_sha1=x['blob_sha'],inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False)
    sources=[]
    for family,title,author,year,date,commit,entry in [
      ('burlap','BURLAP finite-model, LSPI and QMDP source profile','BURLAP contributors',2017,'27 November 2017; POM3.0.2-SNAPSHOT; README3.0.1','cc3b09de81f33e6bed8154144a3183dee8595e32','burlap_src_07'),
      ('chen','Chen Java reinforcement-learning update contracts','Chen Java reinforcement-learning contributors',2017,'16 December 2017; POM1.0.6; README1.0.5','f85cb03e5d16512f6bb9e126fa940b9e49d5bde7','chen_src_03'),
      ('rl4j','Historical RL4J DQN, replay and episode semantics','Eclipse Deeplearning4j contributors',2022,'2 February 2022 historical parent;1.0.0-SNAPSHOT;not current release','b8161c793fdf44ac3da3ce537851ba786599aba8','rl4j_src_05')]:
        rec=[v for k,v in records.items() if k.startswith(family+'_')];identity=bykey[entry]
        sources.append(dict(integrated_citation_key='exec24_policyjava_'+family,kind='software_primary_sources',title=title,author=author,year=year,source_identity=f"https://github.com/{identity['repository']}/tree/{commit}",version_date=date+'; '+commit,local_copy=records[entry]['local_copy'],records=rec,inspected_anchors=[dict(anchor=v['upstream_path'],inspection='Selected line ranges in authenticated records') for v in rec],supported_claims=[a['finding'] for v in rec for a in v['inspected_anchors']],limitations=LIMITS))
    paper=ROOT/'docs/papers/Least-Squares Policy Iteration Lagoudakis(2003).pdf';rawpaper=RAW/'exec24_policyjava_lspi_paper.pdf';assert paper.read_bytes()==rawpaper.read_bytes() and paper.read_bytes().startswith(b'%PDF-')
    extract=BASE/'lspi-original.txt';lines=extract.read_text().splitlines();spans=[(1,165,'Title,authors,finite MDP,discount and policy-value definitions'),(225,290,'Approximate policy iteration needs bounded approximation errors'),(708,950,'LSTDQ matrices,sampling law,projection distribution and rank remedies'),(1140,1215,'Theorem7.1 conditional uniform error and oscillation/feature limits'),(1340,1440,'Selected chain experiment and separate original-code noncommercial footnote'),(2370,2470,'Unvisited states,feature choice and future directions')]
    anchors=[dict(anchor=f'Extracted lines{lo}-{hi}',lines=[lo,hi],text_extract=ref(extract,'Authentic PDF text'),excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest(),finding=f) for lo,hi,f in spans]
    sources.append(dict(integrated_citation_key='exec24_policyjava_lspi',kind='paper',title='Least-Squares Policy Iteration',first_author='Lagoudakis',author='Lagoudakis, Michail G. and Parr, Ronald',year=2003,source_identity='https://www.jmlr.org/papers/v4/lagoudakis03a.html',version_date='JMLR4(2003),1107-1149;December2003;genuine43-pageoriginal',local_path=str(paper.relative_to(ROOT)),sha256=core.sha(paper),local_copy=ref(paper,'Genuine original'),identity_evidence=[ref(RAW/n,'Original identity/acquisition') for n in ['exec24_policyjava_lspi_landing.html','exec24_policyjava_lspi_landing.receipt.json','exec24_policyjava_lspi_paper.receipt.json']],inspected_anchors=anchors,supported_claims=[f for _,_,f in spans],limitations=LIMITS))
    query=next(x for x in read(ROOT/'docs/program/repair-v12/work/SW01/search-ledger.json')['queries'] if x['id']=='v12_sw_cell_policies_offpolicy_java');data=read(ROOT/query['local_copy']['path']);assert len(data['results'])==10 and data['meta']['count']==1088
    queries=[]
    for name in ['offpolicy_search','quoted_search','rl_search']:
        p=RAW/f'exec24_policyjava_{name}.json';d=read(p);queries.append(dict(raw=ref(p,'Discovery only'),receipt=ref(p.with_suffix('.receipt.json'),'Query provenance'),reported=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],candidates=[dict(name=x['full_name'],url=x['html_url']) for x in d['items']]))
    identities=[ref(RAW/n,'Pinned identity,history or limited discovery') for n in ['exec24_policyjava_burlap_cutoff.json','exec24_policyjava_burlap_tree.json','exec24_policyjava_chen_cutoff.json','exec24_policyjava_chen_tree.json','exec24_policyjava_dl4j_cutoff.json','exec24_policyjava_dl4j_tree.json','exec24_policyjava_dl4j_parent_identity.json','exec24_policyjava_dl4j_parent_tree.json','exec24_policyjava_rl4j_subtree.json','exec24_policyjava_rl4j_removal.json','exec24_policyjava_rl4j_identity.receipt.json','exec24_policyjava_smarthi_identity.json','exec24_policyjava_smarthi_cutoff.json','exec24_policyjava_smarthi_tree.json']]
    dl=read(RAW/'exec24_policyjava_dl4j_tree.json');hist=read(RAW/'exec24_policyjava_rl4j_subtree.json');assert not dl['truncated'] and not hist['truncated'];assert len(hist['tree'])==453 and not any(x['path']=='rl4j' or x['path'].startswith('rl4j/') for x in dl['tree'])
    write(BASE/'search-screening.json',dict(status='partial_not_exhaustive',cutoff='2026-10-07',inherited_query=query,inherited_returned=10,inherited_reported=1088,repository_queries=queries,identity_evidence=identities,aliases=dict(burlap=['BURLAP','jmacglashan/burlap'],chen=['java-reinforcement-learning','chen0040'],rl4j=['RL4J','deeplearning4j subtree','smarthi separate candidate']),historical_boundary='Inspected parent b8161c... from2022; current cutoff tree lacks rl4j root; truncated300-file commit response cannot prove detailed removal semantics;smarthi is not asserted equivalent.',stopping_rule='Three selected immutable profiles and their necessary target/replay delegates; no saturation/absence claim.'))
    exact_result=exact.calculate();assert exact_result==read(BASE/'exact-results.json')
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_authored_derivations',evidence=[ref(Path(exact.__file__),'Only authored reference executed'),ref(BASE/'exact-results.json','Exact rational outputs'),ref(BASE/'development.tex','Derivations and conditions')],findings=['Bellman residual bound follows contraction only for supplied finite discounted model and complete residual.','Inverse update denominator0 agrees with singular updated scalar A; no native crash claimed.','Q/Sarsa/terminal updates109/25,387/100,19/5;actor6versus18/5.','DQN labels11versus29/10;clamped5versus3;terminal2clamped3.','Information acquisition8versus9/2;QMDPwait9;regret7/2.','Nominal residual0,value10versus20;tievalues5versus10.'],native_execution=False,empirical_coverage=False))
    gaps=[('coverage','Inspect registry/search tails,maintained aliases and additional policy families; bound acquisition before claims.'),('methods','Inspect further original methods before theoretical adoption; LSPI paper alone does not qualify nonlinear control or causal uncertainty.'),('burlap','Bind true state/model/reachability,greedy ties,terminal features and conditioning; compare original worker against exact finite model.'),('chen','Bind terminal absorption,discount/actor convention,random-stream identity and actual action propensities; deliberate repairs need independent oracle.'),('rl4j','Choose maintained artifact and pin native/backend dependencies; qualify features,replay,episode end,reward/clock and target/clamp configuration.'),('rights','Resolve exact original,transitive and task/data licenses; original LSPI code footnote differs from BURLAP source license.'),('causal','Supply justified logging/support/history/transport and selected-policy uncertainty; unrestricted hidden-state identification has no universal promised repair.'),('public','Preregister finite/public task splits,fault/refusal oracles,full denominators and costs; bank truth/economics remain later conditional work.')]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=k,next_action=v,global_blocker=False) for k,v in gaps],limitations=LIMITS))
    write(BASE/'conversion-contract.json',dict(status='proposal_only',integration_allowed=False,choices=dict(burlap='Conditional original worker for supplied finite model or declared linear features; separate causal evaluation',chen='Reference;defer native adoption pending terminal/discount/randomness qualification',rl4j='Historical comparator;defer native adoption until maintained artifact,backend and conformance decision'),reject=['Whole-library port without measured need','Planning or learned Q presented as identified causal value','Training clamp used as monetary output','Random replay called independent causal evaluation','Unavailable logging or latent truth invented by adapter'],request_fields=['target_type','population','history_state_schema','action_feasibility','model_or_logger_identity','support','reward_units','physical_discount_clock','policy_bytes_randomness','terminal_truncation_rule','training_evaluation_groups','uncertainty','source_rights_environment','resource_budget'],refusals=['unbound_logger','unsupported_action','singular_solve','inconsistent_terminal','missing_final_observation','unqualified_runtime'],owners=['Scientific target owner','Adapter/runtime owner','Rights/data owner','Evaluation/cost owner'],native_execution=False))
    synthesis=dict(integrated_citation_key='exec24_policyjava_comparison',kind='project_evidence_not_scholarly_paper',title='Java policy contract comparison, bounded discovery and exact banking witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24 October 2026; source cutoff7 October2026;no native execution',local_copy=ref(BASE/'search-screening.json','Bounded discovery and historical identity'),inspected_anchors=[ref(BASE/n,'Authored comparison evidence') for n in ['mathematical-review.json','conversion-contract.json','omissions-register.json']],supported_claims=['Three selected historical profiles and a genuine LSPI original support distinct roles; coverage is not exhaustive.','Exact authored target,terminal,clamp,information and model-error witnesses reproduce.','Conditional worker/reference/defer decisions carry explicit rights,semantic,uncertainty and full-cost requirements.'],limitations=LIMITS)
    sources.append(synthesis);assert len(sources)==5
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],findings=['Distinguish model,value learning and logged causal evaluation.','Correct comment-versus-expression and inverse-scale-versus-ridge ambiguities.','Original code rights,static witnesses and unexecuted native behavior distinguished.','Keep source and financial assumptions auditable; no length-based completion.'],visual_acceptance=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_primary_review',evidence=[ref(BASE/n,'Reviewed input') for n in ['plan-review.json','source-audit.json','mathematical-review.json','conversion-contract.json','omissions-register.json']],findings=['Four citation source families plus one authored comparison; genuine original locally retained.','Preserve predecessor records,contexts and compiled inputs.','Record inconclusive coverage;publish paired successor and continue independent obligations.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Reviewed Java profile') for n in ['source-audit.json','search-screening.json','conversion-contract.json','omissions-register.json','mathematical-review.json','copyedit-review.json','plan-review-v2.json','development.tex','sponsor-addition.md','exact-results.json']]+[ref(Path(__file__),'Review and receipt logic')]
    review=dict(status='pass_for_bounded_primary_comparison',evidence=evidence,findings=['Three selected source profiles with authenticated blobs,receipts and inspected anchors.','LSPI original assumptions,conditional theorem and sample/feature limitations retained.','Coverage remains inconclusive;no capability admitted.'],limitations=LIMITS);verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(records=5,papers=1,coverage='inconclusive',native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));g,merged,_=run.combined(ROOT,state);node=run.ledger.operation(g,OP)
    evidence=[ref(BASE/n,'Scoped Java policy review') for n in ['review.json','source-audit.json','search-screening.json','conversion-contract.json','omissions-register.json','mathematical-review.json','development.tex']]
    scope='Three selected Java policy source profiles,LSPI original and exact authored witnesses;not exhaustive coverage'
    nxt='Continue registry/search and maintained-fork census;bind BURLAP terminal/tie/conditioning,Chen discount/terminal/randomness and chosen RL4J artifact/backend;preregister exact public/generated causal,clock,replay,refusal and full-cost conformance.'
    out=ROOT/node['outputs'][0];write(out,dict(operation=OP,status='inconclusive',scope=scope,candidates=['BURLAP','chen0040/java-reinforcement-learning','historical RL4J'],evidence=evidence,limitations=LIMITS,next_action=nxt,integration_allowed=False))
    findings=[('inconclusive','Three pinned profiles and bounded search;registry tails,aliases and further families remain.'),('pass','Authenticated primary source bytes and genuine original paper with inspected anchors;static and exact authored evidence distinguished.'),('pass','Connected banking comparison,conditional reuse choices,omissions and prototype route;no native or bank capability.')]
    r=run.ledger.receipt_template(node);r.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Bounded coverage')],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=nxt)
    run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r);print('Java policy receipt prepared: inconclusive.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
