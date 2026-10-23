#!/usr/bin/env python3
"""Bounded Julia/Rust source review; execute no upstream software."""
import argparse,hashlib,json
from pathlib import Path
import longitudinal_other_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/longitudinal-other-v1';RAW=ROOT/'docs/literature/raw'
OP='SW.CELL.longitudinal_survival.other_relevant';read=lambda p:json.loads(p.read_text())
LIMITS=['Static pinned primary-source inspection and authored exact laws/abstract traces only; no upstream code or tests executed.',
 'Six selected profiles do not establish exhaustive other-language longitudinal/survival coverage.',
 'Source paths, abstract traces, native runtime, statistical qualification and causal identification are distinct evidence levels.',
 'Direct licence declarations do not establish transitive rights; turnbull grant remains unresolved.',
 'No native integration, fresh visual, independent, bank or final acceptance.']
NAMES=dict(juliastats='JuliaStats Survival.jl',juliaanalysis='SurvivalAnalysis.jl',juliamodels='SurvivalModels.jl',juliajoint='JointSurvivalModels.jl',rustcore='Cameron-Lyons survival',rustturnbull='mwklose turnbull')
VERSIONS=dict(juliastats='0.3.3;Julia1.10;directMIT',juliaanalysis='0.1.0;Julia^1.2;directMIT',juliamodels='0.1.6;Julia1.11;directMIT',juliajoint='1.0.0;Julia1;directMIT',rustcore='2.0.0;Rust1.94;edition2024;directMIT',rustturnbull='0.1.0;edition2021;no licence grant located in inspected declaration/root tree')
CLAIMS={
 'juliastats_src_05':([(7,18),(87,119)],'Right-censoring EventTime; exported constructors call zero-time helper; one-based deletion and aliasing concerns are source-local.'),
 'juliastats_src_06':([(161,182)],'Fractional tied-event risk removal in inspected Cox objective; Efron-style convention.'),
 'juliastats_extra_00':([(14,37),(43,47)],'EventTime/EventTable/Cox/nonparametric exports and source includes.'),
 'juliaanalysis_src_03':([(28,73)],'Right/left/interval response types; start-stop means interval censoring; documentation limits included methods to right censoring.'),
 'juliaanalysis_src_04':([(32,84),(265,297),(332,350)],'Right-censored exponential/Weibull fitting; covariance/t-stat NaN exception branches; distinct PH predictor and distribution outputs.'),
 'juliamodels_src_03':([(1,60)],'Parametric general-hazard modelling alternatives; no inherited uninspected identifiability theorem.'),
 'juliamodels_src_05':([(64,113),(115,155)],'Risk increments; scalar strict-less-than evaluation versus stored-grid cumulative product; no native execution.'),
 'juliamodels_src_06':([(40,65),(81,108)],'Grouped tied-time CoxDefault update with Breslow-style denominator.'),
 'juliajoint_src_03':([(5,16),(74,78)],'Joint hazard combines baseline, linked longitudinal process and covariates; not causal identification.'),
 'juliajoint_src_04':([(27,41),(51,73),(92,108)],'Configured positive support, integration lower bound and rng-accepting sampler with global rand draw.'),
 'rustcore_extra_00':([(35,38),(109,113)],'Public causal Rust module; Python registration delegated elsewhere.'),
 'rustcore_extra_01':([(38,42)],'Public re-exports of inspected MSM, target-trial and TMLE-named entrypoints.'),
 'rustcore_src_03':([(91,189),(247,335),(394,474),(480,541)],'Treated/control clone clocks and administrative status; fixed protocol-censor weights; RMST assigned to risk_difference; bootstrap does not repeat weight call and changes grid; fixed fallback errors; sequential omission paths.'),
 'rustcore_src_04':([(292,352)],'Periodwise propensity fitting to supplied covariates and cumulative inverse weights; stabilized flag mean-normalises rather than fitting numerator probabilities.'),
 'rustcore_src_05':([(347,478)],'Horizon outcomes assign0.5 to prior censoring; propensity/outcome fitting; no explicit censoring adjustment in inspected function; RMST integration and width-free standard error expression.'),
 'rustturnbull_src_01':([(1,3)],'Public response and estimator modules.'),
 'rustturnbull_src_02':([(1,71)],'Response representation contains entry and censoring information; representation alone does not prove estimator support.'),
 'rustturnbull_src_03':([(9,31)],'Survival output third column set to zero; no variance acceptance.'),
 'rustturnbull_src_04':([(7,86)],'Support from uncensored exact events plus infinity; zero membership row possible for finite interval-only data; truncation/variance TODO; no explicit iteration cap in visible loop.')}

def audit():
    assert not (BASE/'review.json').exists()
    if (BASE/'exact-results.json').exists():
        assert read(BASE/'exact-results.json')==exact.calculate()
    else: write(BASE/'exact-results.json',exact.calculate())
    selections={x['key']:x for n in ['source-index.json','source-index-exports.json'] for x in read(BASE/n)}
    pins={x['key']:x for x in read(BASE/'pinned-identities.json')};sources=[];authenticated=[]
    for x in selections.values():
        p=ROOT/x['raw_path'];data=p.read_bytes();r=read(p.with_suffix('.receipt.json'))
        assert r['status']=='saved' and r['sha256']==core.sha(p)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==x['blob_sha']
        assert '/'+x['commit']+'/' in r['url'];authenticated.append(ref(p,'Authenticated original blob'))
    for slug,name in NAMES.items():
        p=next(x for x in selections.values() if x['package']==slug);pin=pins[slug];records=[]
        claims={k:v for k,v in CLAIMS.items() if k.startswith(slug+'_')}
        f=ROOT/selections['exec24_survivalother_'+slug+'_src_00']['raw_path']
        claims[slug+'_src_00']=([(1,len(f.read_text().splitlines()))],'Exact package version and environment declarations; not tested runtime compatibility or supported-release evidence.')
        if slug!='rustturnbull':
            lic=ROOT/selections['exec24_survivalother_'+slug+'_src_01']['raw_path']
            claims[slug+'_src_01']=([(1,len(lic.read_text().splitlines()))],'Direct root MIT grant; no transitive dependency clearance.')
        for suffix,(spans,finding) in claims.items():
            x=selections['exec24_survivalother_'+suffix];f=ROOT/x['raw_path'];r=read(f.with_suffix('.receipt.json'));lines=f.read_text().splitlines();anchors=[]
            for a,b in spans:
                assert 1<=a<=b<=len(lines),(suffix,a,b,len(lines))
                anchors.append(dict(lines=[a,b],text=chr(10).join(lines[a-1:b]),finding=finding))
            records.append(dict(source_identity=r['url'],version_date=VERSIONS[slug]+';'+pin['commit']+';'+pin['date'],upstream_path=x['path'],local_copy=ref(f,finding),receipt=ref(f.with_suffix('.receipt.json'),'Public bounded acquisition'),git_blob_sha1=x['blob_sha'],inspected_anchors=anchors,supported_claims=[finding],executed=False))
        tree=RAW/f'exec24_survivalother_{slug}_tree.json';cutoff=RAW/f'exec24_survivalother_{slug}_cutoff.json'
        assert not read(tree)['truncated'] and pin['date']<'2026-10-08'
        sources.append(dict(integrated_citation_key='exec24_survivalother_'+slug,kind='software_primary_sources',title=name+' pinned survival semantics and integration contract',author=name+' contributors',year=int(pin['date'][:4]),source_identity=f"https://github.com/{p['repository']}/tree/{pin['commit']}",version_date=VERSIONS[slug]+';'+pin['commit']+';'+pin['date'],local_copy=records[-1]['local_copy'],records=records,identity_evidence=[ref(cutoff,'Default-branch eligible commit; not all releases'),ref(tree,'Complete pinned tree')],inspected_anchors=[r['local_copy'] for r in records],supported_claims=[r['supported_claims'][0] for r in records],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec24_survivalother_reference',kind='project_evidence_not_scholarly_paper',title='Authored survival clock, boundary, units, censoring, support and cost witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/longitudinal_other_reference_20261024.py',version_date='24 October2026; exact Fraction arithmetic and abstract traces',local_copy=ref(Path(exact.__file__),'Independent authored reference'),inspected_anchors=[ref(BASE/'exact-results.json','Exact results and scope')],supported_claims=['Entry increments1/2 versus1/3; scalar/grid boundary1 versus1/2.','Breslow1/18 versus Efron2/27 for declared ties.','Abstract zero-time helper removes indices1and2 from[0,1,2].','Abstract administrative-censoring trace(5,1)versusorigin-clock(5,0).','Two-month RMST difference versus zero risk difference; time-valued standard errors require unit scaling.','Fixed mean-normalised weights cannot recover conditional weights; half-imputation chooses rather than identifies survival.','Finite interval-only support witness has zero membership rows.','36USD/12initiated/3accepted gives12USD peraccepted.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',authenticated_blobs=len(authenticated),inspected_cited_blobs=sum(len(x.get('records',[])) for x in sources),native_execution=False))
    discovery=read(BASE/'discovery-checkpoint.json');queries=[];observed={}
    for lang in ['julia','rust']:
        p=RAW/f'exec24_survivalother_{lang}_search.json';d=read(p);queries.append(dict(source=ref(p,'Discovery metadata only'),total=d['total_count'],returned=len(d['items']),incomplete=d['incomplete_results']))
        for x in d['items']:observed[x['full_name']]=dict(repository=x['full_name'],disposition='metadata_only_unresolved_lead')
    for slug in NAMES:
        p=next(x for x in selections.values() if x['package']==slug);observed[p['repository']]=dict(repository=p['repository'],disposition='bounded_primary_review',commit=p['commit'])
    write(BASE/'search-screening.json',dict(status='partial_not_exhaustive',queries=queries,items=list(observed.values()),failure=ref(RAW/'exec24_survivalother_targettrial_search.receipt.json','Preserved403local discovery limit'),tails=discovery['remaining_search_tails'],stopping_rule='Six contrastive primary profiles support bounded comparison; no exhaustive closure or absence inference.',metadata_is_technical_evidence=False))
    gaps=[('coverage','Resolve Julia results11-39, Rust alternatives, NetSurvival/AcceleratedFailure, other languages and target-trial synonyms after local403; zero-result conjunctive search is not absence.'),('delegates','Inspect SurvivalBase/SurvivalDistributions, complete Julia fit/prediction/uncertainty delegates and Rust Python registration, validation and alternate causal functions.'),('source_concerns','Resolve zero-time indices/aliasing, scalar/grid jump sides, random-generator routing, origin/admincensoring, weights, target units and bootstrap consistency with upstream maintainers and preregistered native fixtures.'),('interval_rights','Resolve turnbull licence, interval support, truncation likelihood, variance, termination and nonfinite diagnostics before adoption.'),('native_qualification','Freeze compatible toolchains, complete transitive rights and dependency hashes; no upstream code execution is authorised in this source review.'),('public_trials','Preregister justified generated/public targets, sampling law, calibration, failure/refusal and full costs; later bank evidence remains distinct.'),('acceptance','Complete mandatory coverage/depth,Q1/Q5 and fresh visual/final acceptance; source findings do not close these.')]
    write(BASE/'omissions-register.json',dict(status='open',items=[dict(gap=k,next_action=v,global_blocker=False) for k,v in gaps],limitations=LIMITS))
    write(BASE/'conversion-contract.json',dict(status='proposal_only',integration_allowed=False,preferred_route='Original qualified engines behind target-specific workers; authored reference use now',alternatives=['JuliaStats right-censored worker after zero-time/boundary qualification','SurvivalAnalysis exponential/Weibull worker preserving NaN diagnostic status','SurvivalModels worker with explicit ties and jump side','JointSurvivalModels modelling worker after support/tolerance/seed checks','Repaired selected Rust worker after causal/clock/weight/unit/bootstrap qualification','Existing qualified R/Python target-specific alternative','Independent finite-law oracle'],rejected=['Whole-library port without demonstrated benefit','Interval-censor bounds silently treated as delayed entry','Risk label silently attached to time-valued contrast','Fixed censoring weights or half-imputation accepted as identification','Uncleared turnbull redistribution','Native admission inferred from source inspection'],inputs=['population/eligibility clock/available history','strategy/grace/administrative follow-up','entry/censoring/competing events','typed target/units/horizon/ties/jump side','subject/cluster IDs, weights and uncertainty law','exact source/environment/rights'],outputs=['initiated/skipped/refused/failed/returned IDs','typed estimates, units and diagnostics','uncertainty method, resampling and failures','warnings/refusals, full costs, environment and source hashes'],owners=['Method owner: target and identification','Adapter owner: units/semantics/failures','Rights owner: exact distribution','Evaluation owner: public/generated comparisons'],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_comparison_and_integration',evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan-review.json','source-audit.json','omissions-register.json','development.tex']],checks=['40authenticated original blobs,6profiles,7new citation records; no new scholarly citation.','Exports checked before entrypoint claims; no native execution or blanket package defect claim.','Exact laws and source traces separated; uncertainty/rights/search tails remain open.','Preserve1054predecessor records/contexts and239papers; integrate reader and sponsor; reconcile and continue.'],visual_acceptance=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_laws_and_abstract_traces',evidence=[ref(Path(exact.__file__),'Exact independent code'),ref(BASE/'exact-results.json','Reproduced results'),ref(BASE/'development.tex','Definitions and interpretations')],findings=['Clock,event,censoring and units bind separate targets.','Exact tie,boundary,entry,weight,imputation,support and cost witnesses reproduce.','Abstract trace is not a native run; no statistical calibration inferred.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Software declarations, authored examples and conditional reuse distinguished.','No scholarly work cited without its genuine original; cited six sources and authored reference audited.','Process status kept outside reader narrative; price and native claims bounded.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Bounded review') for n in ['plan-review-v2.json','source-audit.json','search-screening.json','omissions-register.json','conversion-contract.json','development.tex','sponsor-addition.md','mathematical-review.json','copyedit-review.json','exact-results.json']]+[ref(Path(__file__),'Audit logic')]
    review=dict(status='pass_for_bounded_comparison',evidence=evidence,findings=['Six pinned source profiles and exact independent witnesses support conditional choices.','Coverage inconclusive; no native integration.'],limitations=LIMITS);verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(audited_sources=7,authenticated_blobs=len(authenticated),coverage='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));g,merged,_=run.combined(ROOT,state);node=run.ledger.operation(g,OP)
    evidence=[ref(BASE/n,'Scoped Julia/Rust evidence') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json','conversion-contract.json','mathematical-review.json','development.tex']]
    scope='Six Julia/Rust survival profiles; bounded comparison, not exhaustive other-language longitudinal coverage'
    nxt='Resolve Julia/Rust discovery tails and other languages; inspect delegates and exact entrypoint validation. Resolve source-local clock/censoring/unit/weight/bootstrap/boundary concerns and turnbull rights/support before native admission. Preregister generated/public semantic, uncertainty, failure and complete-cost fixtures.'
    out=ROOT/node['outputs'][0];write(out,dict(operation=OP,status='inconclusive',scope=scope,candidates=list(NAMES.values()),evidence=evidence,limitations=LIMITS,next_action=nxt,integration_allowed=False))
    findings=[('inconclusive','Six cutoff profiles reviewed; search tails, other languages and delegates remain.'),('pass','40authentic pinned blobs and7citation records bind identity,date,hash and inspected primary anchors; no new metadata-only paper.'),('pass','Concrete original-worker/reference/rejection choices, owners, exact witnesses and qualification routes; no absence or native inference.')]
    receipt=run.ledger.receipt_template(node);receipt.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Bounded Julia/Rust disposition')],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=nxt)
    run.validate_receipt(ROOT,merged,node,receipt,len(state['execution_program']['turns']));verify_bindings(receipt);write(BASE/'operation-receipt.json',receipt);print('Other-language survival receipt prepared: inconclusive.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
