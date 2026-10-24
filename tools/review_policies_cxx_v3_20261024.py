#!/usr/bin/env python3
"""Audit bounded C++ policy profiles without admitting native capability."""
import argparse, hashlib, json
from pathlib import Path
import policies_cxx_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base; core=run.core; ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/policies-cxx-v3'; RAW=ROOT/'docs/literature/raw'
OP='SW.CELL.policies_offpolicy.Cxx'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Selected cutoff-pinned source paths and original-paper sections; no downloaded code, native build, model or bank experiment executed.',
 'Search tails, registries, aliases, maintained forks and additional planning families remain; no exhaustive coverage or absence finding.',
 'Direct license declarations do not establish transitive distribution rights; the selected binary, dependencies and data need separate qualification.',
 'Contextual-bandit evaluation, model-conditional planning, learned control and policy selection have distinct targets.',
 'Static algebraic witnesses are not observed native failures; theorem-to-code mapping and numerical certification remain open.',
 'No universal hidden-state identification, arbitrary-dependence guarantee or uncertainty for an unknown optimal policy established.',
 'Mandatory coverage/depth, Q1/Q5, fresh visual, independent and final acceptance remain open.']
SPECS={
 'vw_src_00':[(1,46,'Direct BSD-style license and component boundary')],
 'vw_src_01':[(1,31,'Project identity and repository introduction')],
 'vw_src_02':[(1,57,'Version declarations depend on generated version identity')],
 'vw_version':[(1,1,'Pinned version file declares 9.11.9')],
 'vw_src_03':[(100,103,'IPS delegate'),(194,197,'DR delegate'),(222,225,'Probability clipping'),(423,450,'Estimator options and clip_p default zero')],
 'vw_src_04':[(60,100,'Reward clipping versus adjusted range and dropped-observation handling')],
 'vw_src_05':[(1,81,'Confidence sequence interface and default reward range/adjustment')],
 'vw_src_06':[(313,320,'Nonnegative weight and unit-interval reward assertions; numerical theorem mapping unqualified')],
 'vw_src_07':[(1,100,'Separate empirical-likelihood component; asymptotic chi-square approximation, not an anytime guarantee')],
 'vw_delegate_01':[(212,245,'ADF doubly robust residual divided by clipped probability')],
 'vw_delegate_02':[(13,40,'Safe probability substitution and multiline IPS transformation')],
 'vw_delegate_03':[(56,88,'Separate reporting IPS/DR functions')],
 'vw_delegate_05':[(98,108,'Invalid probability handling'),(174,180,'Test-label convention')],
 'aitoolbox_src_00':[(1,20,'GPL version 3 license identity')],
 'aitoolbox_src_02':[(100,145,'C++20, Boost>=1.67, Eigen>=3.2.92 and LpSolve build declarations')],
 'aitoolbox_src_03':[(149,200,'Supplied-model and policy iteration, horizon/tolerance and zero variation convention')],
 'aitoolbox_src_04':[(37,39,'Control trace ratio uses passed greedy index'),(80,94,'Evaluation trace ratio uses target and behavior probabilities')],
 'aitoolbox_src_05':[(352,389,'Expected-policy versus epsilon-control continuation; next-state maximizing index passed into current-state ratio')],
 'aitoolbox_src_06':[(14,50,'Trace update and explicit clearing'),(68,70,'Discount validation')],
 'aitoolbox_src_07':[(133,142,'QMDP uses MDP solver and observation count')],
 'aitoolbox_src_08':[(1,46,'Construct belief action planes from fully observable solution')],
 'aitoolbox_src_09':[(14,60,'Generative-model and sampled-belief contract; particle depletion caveat')],
 'mlpack_src_00':[(1,38,'Direct BSD three-clause source license and third-party boundary')],
 'mlpack_src_01':[(1,110,'Stable download 4.8.0 and dependencies')],
 'mlpack_src_02':[(1,41,'Pinned version header 4.8.1')],
 'mlpack_src_04':[(134,205,'Ordinary target uses gamma to replay step count and terminal suppression'),(266,284,'Categorical branch single discount and literal exact-atom mass loss'),(355,388,'Episode score is undiscounted reward sum')],
 'mlpack_src_05':[(52,59,'Stored transition fields lack logging propensity'),(103,169,'Full multistep buffer and terminal reward recursion'),(182,197,'Random index sampling contract')],
 'mlpack_src_06':[(220,246,'Priority replay correction differs from causal logging probability')],
}
PAPERS=[
 ('aitoolbox_paper','AI-Toolbox A C++ library for Reinforcement Learning and Planning (with Python Bindings)','Bargiacchi','Bargiacchi, Eugenio and Roijers, Diederik M. and Nowé, Ann',2020,'aitoolbox-original.txt','JMLR21(2020), article and supplement, published May2020',[(1,'Identity; planning with known model versus learning'),(2,'C++17 historical architecture and Python binding context'),(3,'Dependencies, design and licensing as historical declarations')]),
 ('cs2021','Off-policy Confidence Sequences','Karampatziakis','Karampatziakis, Nikos and Mineiro, Paul and Ramdas, Aaditya',2021,'cs2021-original.txt','arXiv2102.09540v1,18 February2021; title-page date19 February2021',[(1,'Identity and scope'),(2,'IID contextual-bandit baseline, support, IPS and moment identities'),(3,'Bounded weights/rewards and distinct asymptotic empirical likelihood'),(4,'Predictable bets and confidence-sequence definition'),(5,'Theorem1 nonnegative martingale and time-uniform inversion')]),
 ('anytime2024','Anytime-valid off-policy inference for contextual bandits','Waudby-Smith','Waudby-Smith, Ian and Wu, Lili and Ramdas, Aaditya and Karampatziakis, Nikos and Mineiro, Paul',2024,'anytime2024-original.txt','arXiv2210.10768v3,15 August2024',[(1,'Identity and claimed framework'),(3,'Absolute continuity, exogenous dependence and longitudinal interpretation boundary'),(4,'Predictable logger protocol and time-uniform coverage definition'),(5,'Unknown/unbounded supremum but finite individual weights'),(7,'Constant conditional policy-value setup'),(9,'Fixed-value inference premises'),(15,'Time-varying target definition'),(31,'Nonnegative martingale proof framework'),(41,'Potential-outcomes consistency, exchangeability and positivity')])
]

def audit():
    assert not (BASE/'review.json').exists()
    indexes=read(BASE/'source-index-with-delegates.json'); bykey={x['key'].replace('exec24_policycxx_',''):x for x in indexes}
    tree=read(RAW/'exec24_policycxx_vw_tree.json'); entry=next(x for x in tree['tree'] if x['path']=='version.txt')
    version=dict(bykey['vw_src_02'],key='exec24_policycxx_vw_version',path='version.txt',blob_sha=entry['sha'],raw_path='docs/literature/raw/exec24_policycxx_vw_version.txt')
    indexes.append(version);bykey['vw_version']=version; records={}; authenticated=[]
    for x in indexes:
        k=x['key'].replace('exec24_policycxx_','');p=ROOT/x['raw_path'];b=p.read_bytes();rc=RAW/(x['key']+'.receipt.json');r=read(rc)
        assert r['sha256']==hashlib.sha256(b).hexdigest()
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==x['blob_sha']
        authenticated.append(dict(identity=x,local_copy=ref(p,'Authenticated pinned source'),receipt=ref(rc,'Public-source receipt'),used_for_claim=k in SPECS))
        if k not in SPECS:continue
        lines=b.decode().splitlines();anchors=[]
        for lo,hi,f in SPECS[k]:
            hi=min(hi,len(lines));assert lo<=hi
            anchors.append(dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest(),finding=f))
        records[k]=dict(source_identity=r['url'],version_date=x['date']+'; '+x['commit'],upstream_path=x['path'],local_copy=ref(p,'Primary source'),receipt=ref(rc,'Acquisition authentication'),git_blob_sha1=x['blob_sha'],inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False)
    assert len(authenticated)==37
    authenticated_index=dict(records=authenticated,ancillary_rule='Acquired auxiliary files outside SPECS are authenticated only, not assigned inspected capability claims.')
    if (BASE/'authenticated-source-index.json').exists():
        assert read(BASE/'authenticated-source-index.json')==authenticated_index
    else:
        write(BASE/'authenticated-source-index.json',authenticated_index)
    sources=[]
    for family,title,author,entry,version_date in [
      ('vw','Vowpal Wabbit contextual-bandit and inference source contracts','Vowpal Wabbit contributors','vw_src_03','28 September2026; version9.11.9'),
      ('aitoolbox','AI-Toolbox policy evaluation, traces and partial-observation contracts','AI-Toolbox contributors','aitoolbox_src_03','18 March2025; selected source requires C++20'),
      ('mlpack','mlpack learned control, replay and categorical projection contracts','mlpack contributors','mlpack_src_04','6 October2026; header4.8.1; README stable4.8.0')]:
        x=bykey[entry]; rec=[v for k,v in records.items() if k.startswith(family+'_')]
        sources.append(dict(integrated_citation_key='exec24_policycxx_'+family,kind='software_primary_sources',title=title,author=author,year=int(x['date'][:4]),source_identity=f"https://github.com/{x['repository']}/tree/{x['commit']}",version_date=version_date+'; '+x['commit'],local_copy=records[entry]['local_copy'],records=rec,inspected_anchors=[dict(anchor=v['upstream_path'],inspection='Authenticated line anchors in records') for v in rec],supported_claims=[a['finding'] for v in rec for a in v['inspected_anchors']],limitations=LIMITS))
    for key,title,surname,author,year,extract,version_date,spans in PAPERS:
        paper=ROOT/'docs/papers'/f'{title} {surname}({year}).pdf'; rawkey='exec24_policycxx_'+key+('' if key=='aitoolbox_paper' else '_pdf');raw=RAW/(rawkey+'.pdf');rc=RAW/(rawkey+'.receipt.json')
        assert paper.read_bytes()==raw.read_bytes() and paper.read_bytes().startswith(b'%PDF-') and core.sha(paper)==read(rc)['sha256']
        txt=BASE/extract;pages=txt.read_text().split(chr(12));anchors=[]
        for n,f in spans:
            assert pages[n-1].strip();anchors.append(dict(anchor=f'Physical PDF page {n}',physical_page=n,text_extract=ref(txt,'Original PDF extraction'),excerpt_sha256=hashlib.sha256(pages[n-1].encode()).hexdigest(),finding=f))
        sources.append(dict(integrated_citation_key='exec24_policycxx_'+key,kind='paper',title=title,filename_title=title,first_author=surname,author=author,year=year,source_identity=read(rc)['url'],version_date=version_date,local_path=str(paper.relative_to(ROOT)),sha256=core.sha(paper),local_copy=ref(paper,'Genuine scholarly original'),identity_evidence=[ref(rc,'Original acquisition receipt'),ref(txt,'Identity and inspected original')],inspected_anchors=anchors,supported_claims=[f for _,f in spans],limitations=LIMITS))
    queries=[]
    for n in ['ope','rl']:
        p=RAW/f'exec24_policycxx_search_{n}.json';d=read(p);queries.append(dict(raw=ref(p,'Discovery only'),receipt=ref(p.with_suffix('.receipt.json'),'Discovery provenance'),reported=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],candidates=[x['full_name'] for x in d['items']]))
    query=next(x for x in read(ROOT/'docs/program/repair-v12/work/SW01/search-ledger.json')['queries'] if x['id']=='v12_sw_cell_policies_offpolicy_cpp')
    trees=[]
    for family in ['vw','aitoolbox','mlpack']:
        p=RAW/f'exec24_policycxx_{family}_tree.json';d=read(p);assert not d['truncated'];trees.append(dict(tree=ref(p,'Complete pinned Git tree'),entries=len(d['tree']),cutoff_identity=ref(RAW/f'exec24_policycxx_{family}_cutoff.json','Cutoff revision identity')))
    write(BASE/'search-screening.json',dict(status='partial_not_exhaustive',cutoff='2026-10-07T15:59:59Z',inherited_query=query,repository_queries=queries,pinned_trees=trees,authenticated_sources=ref(BASE/'authenticated-source-index.json','37 authenticated files'),tails=['RLLib','OpenSpiel','rl-tools','smarties','registries','maintained forks','additional policy and planning families'],stopping_rule='Three selected primary profiles and original papers; no saturation or absence claim.'))
    assert exact.calculate()==read(BASE/'exact-results.json')
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_authored_derivations',evidence=[ref(Path(exact.__file__),'Authored exact arithmetic'),ref(BASE/'exact-results.json','Reproduced rational witnesses'),ref(BASE/'development.tex','Connected conditional derivations')],findings=['Truth/IPS/DR84 versus clipped IPS44 and DR76 under stipulated two-action law.','One-step10 versus infinite100; error90 equals residual9 divided by contraction gap0.1.','Terminal10 versus55; fixed-policy8 versus maximum20.','Three-step10.29 versus single-discount12; literal exact-atom projection mass0 versus1.','Next-state greedy-index ratio0.1 versus current-state ratio1.9.','Unsupported-action worlds0/100 and time-average0.5 versus latest0.8 retain target/information limits.','Cost900 USD divided by100/75/45 gives9/12/20.'],native_execution=False,empirical_coverage=False))
    gaps=[('coverage','Inspect search tails, aliases, registries and additional original methods before ecosystem completeness.'),('vw','Bind training/reporting estimator, truthful logger, support, clipping, reward normalization and exact theorem-to-code mapping; independently check roots and dropped-observation/restart semantics.'),('aitoolbox','Verify target/control trace index, current-state ties, terminal absorption, trace clearing and supplied-model/observation identities.'),('mlpack','Resolve categorical exact-atom mass and multistep discount configuration; verify short terminal tails, episode separation, empty sampling and logged propensity retention.'),('rights','Choose exact distributions and qualify dependencies, data and direct/transitive rights; process boundary alone is not clearance.'),('public','Preregister finite/public logged models, held-out splits, semantic/fault/refusal oracles, every request denominator and full costs.'),('science','Hidden-state identification, unknown logger and unknown optimal-policy uncertainty require specific new information or research; no universal repair is promised.'),('acceptance','Complete mandatory coverage/depth and fresh visual review; native, independent, bank and economic qualification remain separate later gates.')]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=k,next_action=v,global_blocker=False) for k,v in gaps],limitations=LIMITS))
    write(BASE/'conversion-contract.json',dict(status='proposal_only',integration_allowed=False,choices=dict(vw='Conditional original worker for supported fixed-policy contextual-bandit evaluation with separately verified inference.',aitoolbox='Conditional supplied-model planning/reference; defer native control branch pending trace/terminal conformance.',mlpack='Conditional learned-control/simulator comparator; defer categorical/multistep configuration until conformance resolved.'),reject=['Whole-library port without measured need','Probability defaults presented as truthful support','Model score or learned Q presented as identified bank value','Replay weights substituted for action propensities','Unrestricted hidden-state or selected-optimum guarantee'],request_fields=['target_type','population_history','action_eligibility','feature_action_clocks','logger_or_model_identity','support','policy_bytes','reward_units','physical_discount_duration','terminal_truncation','sampling_unit','uncertainty_method','source_runtime_rights','resource_budget'],refusals=['unbound_logger','unsupported_action','invalid_probability','unqualified_terminal','categorical_mass_loss','unqualified_runtime'],owners=['Scientific target owner','Adapter/runtime owner','Rights/data owner','Evaluation/cost owner'],native_execution=False))
    sources.append(dict(integrated_citation_key='exec24_policycxx_comparison',kind='project_evidence_not_scholarly_paper',title='C++ policy contract comparison, bounded search and exact banking witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24 October2026; source cutoff7 October2026; no native execution',local_copy=ref(BASE/'search-screening.json','Bounded discovery and authenticated identities'),inspected_anchors=[ref(BASE/n,'Authored reference') for n in ['mathematical-review.json','conversion-contract.json','omissions-register.json']],supported_claims=['Three selected profiles and three authentic originals establish scoped contracts, not exhaustive coverage.','Exact authored clipping, residual, terminal, trace, categorical, target and cost witnesses reproduce.','Conditional worker/reference/defer choices specify semantic, rights, uncertainty and full-cost requirements.'],limitations=LIMITS))
    assert len(sources)==7
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07T15:59:59Z',native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass_for_scoped_argument',evidence=[ref(BASE/'development.tex','Connected monograph argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],findings=['Differentiate learning, planning, causal evaluation and selection.','Keep probability clipping, terminal and distributional findings scoped to literal inspected expressions.','Retain original theorem premises, historical/current version differences and explicit native uncertainty.'],visual_acceptance=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_primary_review',evidence=[ref(BASE/n,'Reviewed input') for n in ['plan-review.json','source-audit.json','mathematical-review.json','conversion-contract.json','omissions-register.json']],findings=['Seven new citation records include three genuine originals.','Preserve predecessor records, contexts and compiled inputs; publish paired successor.','Record inconclusive coverage and continue independent obligations.'],visual_acceptance=False))
    review=dict(status='pass_for_bounded_primary_comparison',evidence=[ref(BASE/n,'Reviewed C++ profile') for n in ['source-audit.json','search-screening.json','authenticated-source-index.json','conversion-contract.json','omissions-register.json','mathematical-review.json','copyedit-review.json','plan-review-v2.json','development.tex','sponsor-addition.md','exact-results.json']]+[ref(Path(__file__),'Review and receipt logic')],findings=['37 source blobs authenticated; selected technical anchors inspected.','Three genuine originals and exact authored witnesses retain assumptions and target boundaries.','Coverage remains inconclusive; no native capability admitted.'],limitations=LIMITS);verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(records=7,papers=3,authenticated_files=37,coverage='inconclusive',native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));g,merged,_=run.combined(ROOT,state);node=run.ledger.operation(g,OP)
    evidence=[ref(BASE/n,'Scoped C++ policy review') for n in ['review.json','source-audit.json','search-screening.json','conversion-contract.json','omissions-register.json','mathematical-review.json','development.tex']]
    scope='Three selected C++ profiles, three genuine originals and exact authored witnesses; ecosystem coverage remains inconclusive'
    nxt='Complete registry/search tails; bind VW logger/clipping/inference, AI-Toolbox trace/terminal/model and mlpack categorical/multistep/replay semantics; preregister exact public/generated conformance, refusals and full costs.'
    out=ROOT/node['outputs'][0];write(out,dict(operation=OP,status='inconclusive',scope=scope,candidates=['Vowpal Wabbit','AI-Toolbox','mlpack'],evidence=evidence,limitations=LIMITS,next_action=nxt,integration_allowed=False))
    findings=[('inconclusive','Three pinned profiles and bounded search; registries, aliases, tails and further families remain.'),('pass','Authenticated primary bytes and three genuine original PDFs with inspected anchors; static and exact authored evidence distinguished.'),('pass','Connected banking comparison, conditional reuse decisions and explicit public qualification route; no native or bank capability.')]
    r=run.ledger.receipt_template(node);r.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Bounded coverage')],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=nxt)
    run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r);print('C++ policy receipt prepared: inconclusive.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
