#!/usr/bin/env python3
"""Bind selected R synthetic-control sources, comparisons and exact witnesses."""
import argparse
import json
from pathlib import Path
import synthetic_r_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/synthetic-r-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.synthetic_controls.R'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Bounded selected-source comparison; complementary search pages and substantive candidates remain uninspected.',
 'No downloaded package, installed R distribution or upstream test executed; source predicates are not native failures.',
 'Package notices, copied-code provenance, transitive rights and resolved solver artifacts require further review.',
 'Assignment exchangeability, counterfactual stability and arbitrary serial dependence are not established by package choice.',
 'No new scholarly work admitted; visual, independent, bank and final acceptance remain open.'
]
NEXT='Inspect remaining R synthetic-control candidates and search tails, resolve copied-code/dependency provenance, complete inference/solver delegates and preregister target-matched public native qualification. Preserve failed-draw denominators, tie rules, donor/spillover assumptions, time/unit resampling and all retained source findings; no universal calibration claim.'


def prepare():
    assert not (BASE/'review.json').exists()
    validation=read(BASE/'git-byte-validation.json');assert validation['status']=='pass' and validation['count']==23
    for row in validation['originals']:
        assert core.sha(ROOT/row['local_path'])==row['sha256']
    write(BASE/'exact-results.json',exact.calculate())
    groups={
      'kernlab':('kernlab 0.9-33 selected ipop termination and diagnostic source','cran/kernlab','0.9-33;14 August 2024;d8f05c9b1b8d220deb98fdf28cd33471f17d5eae',[
        ('exec25_synthr_kernlab_src_0.txt',1,34,['Version: 0.9-33','License: GPL-2','NeedsCompilation: yes'],'Declared version, GPL2 and compilation; selected delegate is not a resolved environment.'),
        ('exec25_synthr_kernlab_src_1.txt',119,154,['while (counter < maxiter)','if (sigfig >= sigf) break'],'Loop computes residuals/objectives and uses a weak inequality to break.'),
        ('exec25_synthr_kernlab_src_1.txt',260,278,["if ((sigfig > sigf) & (counter < maxiter))","how(ret)    <- 'converged'"],'Returned primal/dual/status and stricter final label; conditional equality distinction.'),
        ('exec25_synthr_kernlab_src_2.txt',1,14,['COPYRIGHT STATUS','the C++ code'],'Original copyright distinctions; not full distribution clearance.')]),
      'tidysynth':('tidysynth 0.2.0 selected preparation, shared predictors and placebo rank paths','edunford/tidysynth','0.2.0;20 May 2023;58eda583ea28645a3531cd769b7852ff504656df',[
        ('exec25_synthr_tidysynth_src_0.txt',1,36,['Version: 0.2.0','License: MIT + file LICENSE'],'Declared package metadata and dependencies.'),
        ('exec25_synthr_tidysynth_src_2.txt',1,21,['MIT License','Permission is hereby granted'],'Retained original package notice; dependencies and copied-code provenance separate.'),
        ('exec25_synthr_tidysynth_src_3.txt',148,206,['time <= i_time','unit != i_unit'],'Pretreatment clock includes supplied intervention time.'),
        ('exec25_synthr_tidysynth_src_3.txt',656,716,['data_versions <- unique(data$.id)','custom_variable_weights <- master_nest$.predictor_weights[[2]]$weight'],'First predictor weights reused for later placebo configurations.'),
        ('exec25_synthr_tidysynth_src_4.txt',682,723,['rank = dplyr::row_number()','fishers_exact_pvalue = rank / max(rank)'],'MSE-ratio ordering and sequential ranks; ties need a declared scientific rule.'),
        ('exec25_synthr_tidysynth_src_5.txt',1,8,['commandeered for internal use here','Synth works as the main engine'],'Explicit inherited implementation provenance needs file-level rights review.'),
        ('exec25_synthr_tidysynth_src_5.txt',303,318,['kernlab::ipop','kernlab::primal(res)'],'Numerical delegate and primal extraction; full installed rights/status qualification open.')]),
      'scinference':('scinference development source for null refits, permutation support and grid inversion','kwuthrich/scinference','0.0.0.9000;13 May 2021;567c6889ce0a1d269a62d415b88aa6baf723a3fe',[
        ('exec25_synthr_scinference_src_0.txt',1,23,['Version: 0.0.0.9000','License: use_gpl3_license()'],'Literal development metadata; genuine GPL3 text retained separately.'),
        ('exec25_synthr_scinference_src_1.txt',1,15,['GNU GENERAL PUBLIC LICENSE','Version 3'],'Actual license text; no full dependency clearance.'),
        ('exec25_synthr_scinference_src_2.txt',1,58,['p <- mean(S.vec>=S.vec[T0+1])','p <- 1/(n_perm+1)*(1+sum(S.vec>=Sq))'],'Cyclic versus Monte Carlo null-refit supports and plus-one convention.'),
        ('exec25_synthr_scinference_src_2.txt',60,90,['ci_temp <- ci_grid[ps_temp>alpha]','min(ci_temp,na.rm=TRUE)','max(ci_temp,na.rm=TRUE)'],'Finite grid inversion returns hull; empty and disconnected sets need qualification.'),
        ('exec25_synthr_scinference_src_3.txt',1,32,['limSolve::lsei','CVXR::solve(prob)'],'Selected estimator delegates; coefficient extraction does not settle solver qualification.'),
        ('exec25_synthr_scinference_src_4.txt',74,112,['if(K==1)','df=K-1'],'Cross-fit route and degree-of-freedom calculation; do not treat source comment as theorem.'),
        ('exec25_synthr_scinference_src_5.txt',1,55,['r     <- min(floor(T0/K),T1)','sqrt(1+((K*r)/T1))'],'Pretreatment fold construction and shared post-period scaling.')]),
      'microsynth':('microsynth 2.0.50 matching fallback and finite permutation denominator source','ssdavenport/microsynth','2.0.50;25 April 2025;e707e4bbd23a146f58d839a9f7dcda1c32cc33dd',[
        ('exec25_synthr_microsynth_src_0.txt',1,39,['Version: 2.0.50','License: GPL-3','LowRankQP'],'Declared microdata package and dependencies; full distribution rights open.'),
        ('exec25_synthr_microsynth_src_3.txt',1,80,['qpmeth <- "LowRankQP"','qpmeth <- "ipop"','use.model <- 3'],'Environment-dependent solver route and feasibility-driven matching fallback.'),
        ('exec25_synthr_microsynth_src_3.txt',153,202,['use.model.i <- 2','use.model.i <- 3'],'Replicate-specific fallback models retained.'),
        ('exec25_synthr_microsynth_src_3.txt',397,406,['keep.groups <- mse','keep.groups[!grepl("Perm"'],'Permutation-group matching-error filter and returned model/status records.'),
        ('exec25_synthr_microsynth_src_1.txt',1121,1154,['get.pval','2 * pmin','1 - c(perm.stats'],'Tail-specific caller transformations; helper is not final universal p-value.'),
        ('exec25_synthr_microsynth_src_1.txt',1224,1248,['boot[boot == Inf | boot == -Inf] <- NA','colMeans(synth.tmp > boot, na.rm = TRUE)','colSums(is.na(boot))'],'Infinite-to-missing conversion, finite comparison denominator and missing counts.')]),
      'auginference':('Additional inspected augsynth 0.2.0 time and unit jackknife paths','ebenmichael/augsynth','0.2.0;4 September 2026;7e70072232fe75057aa8b5d7af08c7e1aef53ae8',[
        ('exec24_augsynth_src_07.txt',15,83,['time_jackknife_plus','drop_time_t','shifted_lb <- y1 - out$ub'],'Time deletion, refit, prediction-error bounds and shift to effect scale.'),
        ('exec24_augsynth_src_07.txt',894,951,['round(ascm$weights, 3) != 0','(n - 1) / n * sum'],'Selected unit deletion and full-row-count multiplier are separate from time jackknife.')])}
    primary=[];sources=[]
    for key,(title,repo,version,checks) in groups.items():
        evidence=[];anchors=[];claims=[]
        for filename,lo,hi,tokens,finding in checks:
            p=RAW/filename;lines=p.read_text().splitlines();fragment='\n'.join(lines[lo-1:hi]);assert all(t in fragment for t in tokens),(filename,lo,hi,[t for t in tokens if t not in fragment])
            binding=ref(p,f'Lines {lo}-{min(hi,len(lines))}: {finding}')
            evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,min(hi,len(lines))]],finding=finding));claims.append(finding)
        primary.append(dict(group=key,evidence=evidence,inspected_anchors=anchors,supported_claims=claims))
        sources.append(dict(integrated_citation_key='exec25_synthr_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1].strip()[-4:]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1].strip(),version_date=version,local_copy=evidence[0],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_source_anchors',groups=primary,evidence=[ref(BASE/'git-byte-validation.json','23 original files authenticated'),ref(ROOT/'docs/program/execution/2026-10-24/augsynth-reuse-v1/identity-review.json','Inherited original inference file identity')],native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Independent rational arithmetic'),ref(BASE/'exact-results.json','Exact replay')],checks=['Spillover changes20to10 without weight changes.','Sequential tie ranks differ from inclusive frequencies.','Failed-draw bounds2/19to11/19 are not calibrated p-values.','Plus-one support,grid hull,jackknife multipliers and conditional strict/weak solver predicates checked.','Cost denominators are hypothetical;no observed price or native result.']))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',registered_candidates=['Synth','augsynth','scpi','fect','gsynth','synthdid'],additional_selected=['tidysynth','scinference','microsynth','kernlab delegate'],target='Regional banking untreated revenue and explicit unit/time/exposure aggregation',comparisons=['Constraint versus augmentation versus factor/block targets','gsynth wrapper versus fect engine','Time versus unit resampling and prediction versus effect uncertainty','Solver diagnostics,ties,missing-draw denominators and rights'],limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Original metadata/license/provenance anchors')],rights=['kernlab declaresGPL2 and native compilation','tidysynth retains MIT notice plus explicit Synth-derived internal engine;file provenance and applicable terms unresolved','scinference literal license declaration retained with genuineGPL3text','microsynth declaresGPL3;survey,LowRankQP,kernlab and distribution rights unresolved','No installed artifact or resolved dependency graph established'],integration_allowed=False))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=['Donor identity,spillovers and information-clock consistency','Matched target,weight constraints and aggregation','Tie/zero-prefit/empty-grid/failure-denominator oracles','Requested/resolved solver diagnostics and backup models','Separate unit,time,trajectory and finite-grid inference claims','Rights,artifact identity,full request/cost denominators'],owners=['Scientific author','Adapter owner','Environment and rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,known_routes=['Inspect outstanding search pages and concrete leads','Complete estimator/solver delegates and copied-code provenance','Pin public native environment and preregister exact law-specific qualification'],unknown_universal_repairs=['Untreated trajectory and donor-spillover truth require assumptions or new information','Arbitrary serial dependence and invalid assignment laws have no automatic package repair'],evidence=[ref(BASE/'search-screening.json','40leads with incomplete search tails')],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_synthr_choice',kind='project_evidence_not_scholarly_paper',title='Authored R synthetic-control comparison, source boundaries and public qualification witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; literature cutoff7 October2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored rational witnesses'),evidence=[ref(BASE/n,'Reviewed comparison evidence') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Targets,source boundaries,donor contamination,ties,failed draws and costs',inspection='Author inspection')],supported_claims=['Selected comparisons and exact stipulated witnesses','Bounded search and explicit unresolved coverage'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=6,new_scholarly_pdfs=0,native_execution=False));verify_bindings(read(BASE/'source-audit.json'))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed plan and actual evidence') for n in ['plan.md','plan-review.json','primary-review.json','comparison-review.json','mathematical-review.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],findings=['Six inherited candidates and selected additional sources differentiated','40leads retain uninspected tails;no exhaustive-pass claim','23new original files and inherited inference source authenticated','No native execution,legal clearance,scientific calibration or visual acceptance implied']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking target,notation,alternatives and explicit limitations'),ref(BASE/'sponsor-addition.md','Investment case implications')],findings=['Source observations,authored arithmetic and proposed tests distinguished','Tied ranks and incomplete denominators not overstated as native failures','License metadata and reused-code provenance separate'],visual_acceptance=False))
    names=['git-byte-validation.json','primary-review.json','comparison-review.json','search-screening.json','mathematical-review.json','exact-results.json','source-audit.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Bounded source evidence') for n in names]+[ref(Path(__file__),'Review and receipt logic')],findings=['23new originals authenticated','New comparison does not replace prior package arguments','Coverage remains inconclusive'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',outcome='inconclusive',originals=23,new_records=6)))


def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    ev=[ref(BASE/n,'Reviewed bounded coverage') for n in ['review.json','search-screening.json','source-audit.json','omissions-register.json']]
    findings=['Registered candidates and selected additions identified;search/technical tails remain incomplete','Selected claims bind authentic source/version/hash/anchors;no new scholarly claim','Alternatives,rights,native limits and next actions explicit;no absence or waiver claim']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='R synthetic-control comparison with selected delegates;coverage incomplete',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=ev) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('R synthetic-control inconclusive receipt prepared.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
