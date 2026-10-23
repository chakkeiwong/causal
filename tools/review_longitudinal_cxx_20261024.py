#!/usr/bin/env python3
"""Bounded primary-source review; do not execute upstream code or tests."""
import argparse, hashlib, json
from pathlib import Path
import longitudinal_cxx_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base; core=run.core; ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/longitudinal-cxx-v1'
RAW=ROOT/'docs/literature/raw'; OP='SW.CELL.longitudinal_survival.Cxx'
read=lambda p:json.loads(p.read_text())
LIMITS=['Static primary-source inspection and authored finite-law/abstract traces only; no upstream package or test executed.',
 'Four selected lineages do not establish exhaustive C++ longitudinal/survival coverage.',
 'Objective derivatives, caller dispatch, wrapper validation and native behavior remain distinct evidence levels.',
 'Causal identification, cluster-calibrated uncertainty, complete environments/rights and costs remain unqualified.',
 'No native integration, fresh visual, independent, bank or final acceptance.']
CLAIMS={
 'xgboost_00':([(1,12)],'Direct root Apache-2.0 declaration; no transitive clearance.'),
 'xgboost_03':([(34,71),(102,108),(154,168)],'AFT distribution/scale and censoring bounds; documented native data-matrix versus sklearn limitation.'),
 'xgboost_04':([(73,168)],'Cox signed time labels, unweighted risk denominator, row-weighted final derivatives, tie loop and exponentiated score.'),
 'xgboost_06':([(35,60),(74,118),(170,234)],'AFT distributions, scale, clipped derivatives and censor-specific limiting branches; not calibration evidence.'),
 'xgboost_extra_00':([(23,74),(85,129)],'CPU AFT objective dispatch, weighted derivatives, bound lengths, exponentiated location and untransformed evaluation margin.'),
 'xgboost_extra_01':([(20,86)],'CUDA AFT kernels call common derivative helpers and weight results; no runtime or parity result.'),
 'xgboost_extra_02':([(1,34)],'Root build declares3.5.0 and selected build prerequisites; not a supported-release statement.'),
 'catboost_00':([(1,12)],'Root Apache-2.0 declaration; no transitive clearance.'),
 'catboost_01':([(1,1)],'Declared Python package version1.2.10.'),
 'catboost_02':([(299,337),(375,377)],'Cox/AFT equations, ambiguous hazard-rate wording, distributions and documented no-GPU rows.'),
 'catboost_03':([(116,255),(360,450)],'Stable absolute-time order, event-triggered Cox denominator decrement, unused local weight arguments, AFT -1 endpoint branches and derivative clipping.'),
 'catboost_04':([(257,277),(427,444)],'AFT positive scale check and Cox raw-margin requirement.'),
 'catboost_05':([(1,16)],'AFT inverse transform is (log target - margin)/scale.'),
 'catboost_extra_00':([(274,339),(392,407)],'Dedicated Cox caller passes weights to the derivative function and subsequent leaf accumulation; no whole-training ignores-weights inference.'),
 'ranger_00':([(1,27)],'R package0.18.0 and GPL-3 with Rcpp/Eigen dependencies.'),
 'ranger_01':([(1,9)],'Standalone C++ COPYING declares MIT.'),
 'ranger_02':([(145,208)],'Mean tree CHF prediction and OOB concordance on summed CHF; no causal interval.'),
 'ranger_03':([(1,10),(63,74),(331,357)],'Explicit C++MIT/RGPL distinction; Nelson-Aalen leaf increments; terminal-time/event columns.'),
 'ranger_04':([(121,121),(998,1018)],'Documented case weights sample rows; binary-event guard in selected wrapper path.'),
 'ranger_05':([(118,144),(317,328),(429,436)],'Selected survival standard-error routes reject; survival is exp(-CHF).'),
 'ranger_07':([(1,10),(52,78)],'Standalone C++14 library and CLI targets; not a compiled binary.'),
 'aorsf_00':([(1,30),(42,44)],'0.1.6 MIT declaration and R/Rcpp/RcppArmadillo environment dependencies.'),
 'aorsf_01':([(1,21)],'MIT notice and warranty limitations; no transitive clearance.'),
 'aorsf_02':([(171,177),(410,425)],'Cox split delegate has separate one-step and iterative paths.'),
 'aorsf_04':([(396,435),(534,550),(590,647),(723,729)],'Weighted product-limit survival and additive hazard maintained separately; horizon selection and risk complement; split delegate.'),
 'aorsf_05':([(26,45),(229,238)],'Time/status response, accelerated one-iteration control and documented weight normalization.'),
 'aorsf_06':([(13,45),(67,70),(88,97)],'Separate prediction types and documented mean aggregation; boundary bypass carries terminal value rather than estimating unobserved tail.')
}

def audit():
    assert not (BASE/'review.json').exists()
    results=exact.calculate();write(BASE/'exact-results.json',results)
    selections={x['id']:x for n in ['source-selection.json','source-selection-delegates.json','source-selection-validation.json'] for x in read(BASE/n)}
    profiles={s:next(x for x in selections.values() if x['slug']==s) for s in ['xgboost','catboost','ranger','aorsf']}
    versions=dict(xgboost='3.5.0 root development build',catboost='1.2.10 package declaration',ranger='0.18.0 R package; distinct MIT C++ core',aorsf='0.1.6 R package with C++ core')
    names=dict(xgboost='XGBoost',catboost='CatBoost',ranger='ranger',aorsf='aorsf');sources=[]
    for slug,p in profiles.items():
        records=[]
        for suffix,(spans,finding) in CLAIMS.items():
            key='exec24_longcxx_'+suffix;x=selections[key]
            if x['slug']!=slug:continue
            f=RAW/(key+'.txt');data=f.read_bytes();receipt=read(f.with_suffix('.receipt.json'))
            assert receipt['status']=='saved' and receipt['sha256']==core.sha(f)
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==x['blob']
            assert '/'+x['commit']+'/' in receipt['url'];lines=f.read_text().splitlines();anchors=[]
            for a,b in spans:
                assert 1<=a<=b<=len(lines),(key,a,b,len(lines))
                anchors.append(dict(lines=[a,b],text=chr(10).join(lines[a-1:b]),finding=finding))
            records.append(dict(source_identity=receipt['url'],version_date=f"{versions[slug]};{p['commit']};{p['date']}",upstream_path=x['path'],local_copy=ref(f,finding),receipt=ref(f.with_suffix('.receipt.json'),'Bounded public acquisition'),git_blob_sha1=x['blob'],inspected_anchors=anchors,supported_claims=[finding],executed=False))
        cutoff=RAW/f'exec24_longcxx_{slug}_cutoff.json';tree=RAW/f'exec24_longcxx_{slug}_tree.json'
        assert not read(tree)['truncated'] and p['date']<'2026-10-08'
        sources.append(dict(integrated_citation_key='exec24_longcxx_'+slug,kind='software_primary_sources',title=names[slug]+' pinned survival objectives, outputs and integration contracts',author=names[slug]+' contributors',year=2026,source_identity=f"https://github.com/{p['repository']}/tree/{p['commit']}",version_date=f"{versions[slug]};{p['commit']};{p['date']}",local_copy=records[-1]['local_copy'],records=records,identity_evidence=[ref(cutoff,'Default-branch cutoff identity; not all releases'),ref(tree,'Complete pinned tree')],inspected_anchors=[r['local_copy'] for r in records],supported_claims=[r['supported_claims'][0] for r in records],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec24_longcxx_reference',kind='project_evidence_not_scholarly_paper',title='Authored survival event, entry, AFT, aggregation and derivative witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/longitudinal_cxx_reference_20261024.py',version_date='24 October2026; exact rational and high-precision analytic reference',local_copy=ref(Path(exact.__file__),'Independent authored arithmetic and abstract traces'),inspected_anchors=[ref(BASE/'exact-results.json','Reproducible outcomes and scope')],supported_claims=['Default cumulative incidence1/5 differs from net default functional1/3.','Delayed-entry increment1/2 differs from1/3.','Equal AFT location2 with scales1and2 gives horizon8probabilities4/5and2/3.','Product-limit versus exponentiated hazard changes constructed margin from-50to56.53USD.','Hazard versus survival averaging gives1/2versus5/8.','Specified tied-event loop traces differ from analytic Breslow gradient; native reachability and full runtime remain untested.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',authenticated_blobs=len(selections),inspected_cited_blobs=len(CLAIMS),native_execution=False))
    queries=[];observed={}
    for name in ['survival','cox']:
        f=RAW/f'exec24_longcxx_search_{name}.json';d=read(f);queries.append(dict(source=ref(f,'Repository metadata discovery only'),total=d['total_count'],returned=len(d['items']),incomplete=d['incomplete_results']))
        for x in d['items']:observed[x['full_name']]=dict(repository=x['full_name'],description=x.get('description'),disposition='metadata_only_unresolved_lead')
    for p in profiles.values():observed[p['repository']]=dict(repository=p['repository'],disposition='bounded_primary_review',commit=p['commit'])
    write(BASE/'search-screening.json',dict(status='partial_not_exhaustive',cutoff='2026-10-07',queries=queries,items=list(observed.values()),alias_followup=['MLSurvival/TransferCox','bcjaeger/obliqueRSF: relationship to aorsf unresolved','ColinCrooks/SurvivalSupervisedLDA'],stopping_rule='Four contrastive primary profiles sufficient for bounded comparison, not exhaustive closure; resolve relevant aliases and query tails.',metadata_is_technical_evidence=False))
    gaps=[('coverage','Resolve C++ longitudinal/causal candidates, surviving search tails and named aliases; broad survival search contains unrelated games.'),('boosted_objectives','Inspect complete dispatch, target validation, weighting, public prediction and metric delegates. Register independent tie/permutation/finite-difference/weight fixtures before native admission.'),('forest_validation','Inspect aorsf response validation, all-censored leaves and complete aggregation/normalization paths; inspect ranger malformed response/entry handling. Source-local concern is not a runtime defect finding.'),('targets_uncertainty','Specify event/censoring/entry/competing-event law, treatment identification and sampling-unit uncertainty; no general cure from a faster predictor.'),('rights_environments','Freeze selected wrapper/core distribution and transitive dependencies; preserve ranger C++MIT versus R GPL-3 distinction.'),('public_trials','Preregister justified generated/public-data target, calibration, failure, memory, latency and complete-cost criteria; no upstream execution in this review.'),('visual','Fresh visual review, Q1/Q5 and mandatory coverage/depth remain open.')]
    write(BASE/'omissions-register.json',dict(status='open',items=[dict(gap=k,next_action=v,global_blocker=False) for k,v in gaps],limitations=LIMITS))
    write(BASE/'conversion-contract.json',dict(status='proposal_only',integration_allowed=False,preferred_route='Original engines behind target-specific typed workers; reference use now',alternatives=['XGBoost objective-specific native worker','CatBoost objective-specific native worker','ranger standalone C++ library/CLI or separate R worker','Original aorsf R worker retaining C++ engine','Dedicated longitudinal R/Python estimator','Independent finite-law oracle'],rejected=['Whole-library port without a demonstrated requirement','Censoring bounds reused as delayed-entry intervals','Score or AFT location converted silently to probability','Causal or uncertainty acceptance inferred from exit status'],inputs=['population/time-zero/availability','event and competing-event target','entry/censoring/treatment representation','weights and sampling units','horizon/output/distribution/baseline contract','locked environment/options/artifact hashes'],outputs=['row identities and exclusions','typed objective and output','baseline/distribution/scale/horizon','warnings/numerical status/refusal','uncertainty method and sampling unit','complete request costs'],owners=['Method owner: identification and target','Adapter owner: conversions and faults','Rights owner: exact distribution','Evaluation owner: generated/public trials'],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_comparison_and_integration',evidence=[ref(BASE/'plan-review.json','Preserved acquisition plan'),ref(BASE/'source-audit.json','Primary source audit'),ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'omissions-register.json','Independent unresolved routes')],checks=['Four contrastive profiles; no exhaustive or native claim.','Inspect callers before inferring whole-training weighting behavior.','Analytic law, abstract source trace and runtime behavior kept separate.','Preserve1043prior citations and237papers; add5audited records.','Publish preserving reader, pair sponsor, reconcile and continue.'],preserved_prewrite_failures=['First source read escaped newline failed before mutation; raw transport succeeded.','First manuscript transport contained LaTeX backticks and failed before patch application; corrected manuscript applied.'],visual_acceptance=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_laws_and_abstract_traces',evidence=[ref(Path(exact.__file__),'Independent Fraction/Decimal reference'),ref(BASE/'exact-results.json','Computed outcomes'),ref(BASE/'development.tex','Definitions and scope')],findings=['Risk-set, competing-event, AFT and aggregation arithmetic reproduce.','Analytic tied Breslow scores are symmetric and sum0; inspected abstract loops differ under stated ordering.','Native execution, calibrated uncertainty and empirical behavior remain untested.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected section'),ref(BASE/'sponsor-addition.md','Investment implications')],findings=['Definitions precede software comparison; alternatives and conditions explicit.','Direct declarations are not complete rights clearance.','No upstream bibliography work cited without original; no new scholarly citation.','Source concerns are not asserted as native failures.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Bounded C++ comparison') for n in ['plan-review-v2.json','source-audit.json','search-screening.json','omissions-register.json','conversion-contract.json','development.tex','sponsor-addition.md','mathematical-review.json','copyedit-review.json','exact-results.json']]+[ref(Path(__file__),'Audit logic')]
    review=dict(status='pass_for_bounded_comparison',evidence=evidence,findings=['Four pinned primary profiles and independent target/output/derivative witnesses.','Coverage remains inconclusive; no native integration.'],limitations=LIMITS);verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(audited_sources=5,inspected_blobs=len(CLAIMS),authenticated_blobs=len(selections),coverage='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));g,merged,_=run.combined(ROOT,state);node=run.ledger.operation(g,OP)
    evidence=[ref(BASE/n,'Scoped C++ evidence') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json','conversion-contract.json','mathematical-review.json','development.tex']]
    scope='Four pinned C++ survival lineages; bounded comparison, not exhaustive longitudinal coverage'
    nxt='Resolve C++ longitudinal discovery tails and named aliases; inspect complete objective/wrapper/weight delegates. Preregister generated/public entry, competing-event, tie/permutation, typed-output, uncertainty, failure and full-cost fixtures; retain original-worker alternatives.'
    out=ROOT/node['outputs'][0];write(out,dict(operation=OP,status='inconclusive',scope=scope,candidates=['dmlc/xgboost','catboost/catboost','imbs-hl/ranger','ropensci/aorsf'],evidence=evidence,limitations=LIMITS,next_action=nxt,integration_allowed=False))
    findings=[('inconclusive','Four cutoff profiles and discovery leads inspected; aliases and search tails remain.'),('pass','Authentic local technical bytes bind cutoff identity, version, hash and inspected anchors; five citation records, no new metadata-only paper.'),('pass','Concrete original-worker alternatives, rejected silent conversions, owners and qualification routes documented; no absence inference.')]
    receipt=run.ledger.receipt_template(node);receipt.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Bounded C++ disposition')],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=nxt)
    run.validate_receipt(ROOT,merged,node,receipt,len(state['execution_program']['turns']));verify_bindings(receipt);write(BASE/'operation-receipt.json',receipt);print('C++ coverage receipt prepared: inconclusive.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
