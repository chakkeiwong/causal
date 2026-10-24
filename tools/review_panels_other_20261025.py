#!/usr/bin/env python3
"""Selected Julia/MATLAB panel source review; no downloaded code execution."""
import argparse,json,re
from pathlib import Path
import panels_other_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/panels-other-v1';RAW=ROOT/'docs/literature/raw'
OP='SW.CELL.panels_did.other_relevant';read=lambda p:json.loads(p.read_text())
LIMITS=['Selected immutable source and bounded GitHub discovery;not exhaustive language coverage.',
 'No downloaded package or native Julia/MATLAB/Octave/gretl runtime executed.',
 'MIT/GPL notices do not settle dependencies,data or licensed runtimes;DiDToolbox permission unresolved.',
 'Conditional static findings and exact authored witnesses are not observed native failures.',
 'Linked papers not newly admitted;no additional scholarly claim without retained original.',
 'Native public qualification,complete rights,visual,independent and final acceptance remain open.']

def prepare():
    assert not (BASE/'review.json').exists()
    validation=read(BASE/'git-byte-validation.json');verify_bindings(validation);assert len(validation['originals'])==40
    assert read(BASE/'exact-results.json')==exact.calculate()
    checks=[
      ('julia','exec25_panelother_diffindiffs_src_03.txt',['@reexport using DiffinDiffsBase','@reexport using InteractionWeightedDIDs'],'Suite reexports delegates;not an independent second estimator.'),
      ('julia','exec25_panelother_iw_src_00.txt',['This package is moved','this repo is archived'],'Archived standalone alias points to the monorepo.'),
      ('julia','exec25_panelother_mono_src_00.txt',['version = "0.3.2"','FixedEffectModels = "1.10"','Vcov = "0.8"'],'Exact component version and delegate ranges;prior2.1.0FEsource is not this resolved environment.'),
      ('julia','exec25_panelother_mono_src_06.txt',['Specify an absorbing binary treatment','exc::Tuple'],'Absorbing treatment/excluded-period contract;reversal not qualified.'),
      ('julia','exec25_panelother_mono_src_07.txt',['struct NeverTreatedParallel','struct NotYetTreatedParallel','operations for complying with a PTA are suppressed'],'Declared comparison relations and unspecified bypass do not prove assumptions.'),
      ('julia','exec25_panelother_mono_src_02.txt',['Vcov.RobustCovariance()','cwts ./ sum(cwts)',"cf = cweights' * pcf","v = cweights' * view(treatvcov(r), inds, inds) * cweights"],'Robust default;within-relative-time normalization and explicit estimate/covariance transform.'),
      ('julia','exec25_panelother_mono_src_03.txt',['Vcov.ClusterCovariance','esample .&= aux','no convergence of fixed effect solver','treatcounts[i] = length(rs)'],'Missing clusters and singleton/sample changes;convergence information and cell counts retained.'),
      ('didint','exec25_panelother_didint_src_02.txt',['version = "0.9.6"','julia = "1.10"'],'Exact selected version and environment requirements.'),
      ('didint','exec25_panelother_didint_src_04.txt',['use_pre_controls = isnothing(notyet)','edgecase == false','function check_prior_to_ri','n_unique_perms','treatment_times[randperm(k)]'],'Control/inference options,conditional equality branch and permutation support/assignment constraints.'),
      ('didint','exec25_panelother_didint_src_05.txt',['Found missing values','Dropping those rows','function gvar_or_treatment_times'],'Missingness filtering and cohort/date inputs require sample custody.'),
      ('didint','exec25_panelother_didint_src_06.txt',['function safe_solve','return missing',"XXinv = inv(X' * X)",'hc == "hc4"'],'Solve refusal and covariance inversion/HCcorrections have separate rank/leverage conditions.'),
      ('matlab','exec25_panelother_didtoolbox_src_00.txt',['Matlab from Version 2021+','Statistics and Machine Learning Toolbox'],'Independent package/runtime requirements;not native MathWorks or Octave capability.'),
      ('matlab','exec25_panelother_didtoolbox_src_02.txt',['cs = did.cs_estimator(T, nv{:})','unconditional','cohortShare'],'Named IW delegates to unconditional CS;name does not establish identical finite-sample algorithm.'),
      ('matlab','exec25_panelother_didtoolbox_src_03.txt',["find(ds==1, 1, 'first')",'outerjoin'],'First-on summary and mapping need reversal and row-order tests.'),
      ('matlab','exec25_panelother_didtoolbox_src_05.txt',['g - opts.Delta - 1','G > (t + opts.Delta)','G ~= g','if ~any(treat_u) || ~any(comp_u), continue; end'],'Anticipation/baseline/control eligibility and support-driven omissions.'),
      ('matlab','exec25_panelother_didtoolbox_src_08.txt',['opts.preSE','opts.ThetaSE','linprog','theta_lb  = NaN'],'Selected sensitivity LP uses marginal/target SE inputs,not full joint covariance;solver failures remain missing.'),
      ('matlab','exec25_panelother_fdid_src_02.txt',['X_reg = [z, gz, xz, gxz]','varNames = [varNames, "X"','v_ddot = v - v_mean_id(id_idx) - v_mean_time(time_idx) + v_mean_all','XX_inv = pinv(XX)'],'Conditional label ordering and unbalanced one-pass projection require tests;pinv is not identification.')]
    findings=[]
    for group,filename,tokens,claim in checks:
        p=RAW/filename;text=p.read_text();assert all(t in text for t in tokens),(filename,[t for t in tokens if t not in text])
        lines=text.splitlines();findings.append(dict(group=group,finding=claim,source=ref(p,'Inspected original'),anchors=[dict(token=t,lines=[i+1 for i,l in enumerate(lines) if t in l]) for t in tokens]))
    tree=read(RAW/'exec25_panelother_didtoolbox_tree.json');assert not tree['truncated'] and len(tree['tree'])==103
    assert not [x for x in tree['tree'] if re.search(r'(^|/)(licen[cs]e|copying)(\.|$)',x['path'],re.I)]
    for n in ['exec25_panelother_diffindiffs_src_01.txt','exec25_panelother_iw_src_01.txt','exec25_panelother_didint_src_01.txt']:assert 'Permission is hereby granted' in (RAW/n).read_text()
    assert 'GNU GENERAL PUBLIC LICENSE' in (RAW/'exec25_panelother_fdid_src_01.txt').read_text()
    write(BASE/'primary-review.json',dict(status='pass_for_selected_originals',findings=findings,evidence=[ref(BASE/'git-byte-validation.json','Forty original files'),ref(RAW/'exec25_panelother_didtoolbox_tree.json','Complete tree without standalone license file')],native_execution=False))
    candidates={}
    for p in sorted(RAW.glob('exec25_panelother_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        for x in read(p).get('items',[]):
            row=candidates.setdefault(x['full_name'],dict(repository=x['full_name'],description=x.get('description'),queries=[],status='uninspected_discovery_lead',technical_claim_admitted=False));row['queries'].append(ref(p,'Discovery result only'))
    selected={x['repository'] for x in validation['originals']}
    for repo in selected:candidates[repo]['status']='selected_original_subset_inspected'
    candidates['JuliaDiffinDiffs/InteractionWeightedDIDs.jl']['status']='archived_alias_resolved_to_monorepo'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',candidates=list(candidates.values()),stopping_rule='Selected dedicated Julia/MATLAB candidates and delegates inspected;remaining leads retained.No exhaustive pass.',evidence=[ref(BASE/'search-coverage.json','Explicit query limits')],absence_claim=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_algebra',evidence=[ref(Path(exact.__file__),'Independent fraction program'),ref(BASE/'exact-results.json','Exact replay')],findings=['TWFE-1/2despite positive effects averaging2;final clean control absent.','Unbalanced one-pass residual time sums nonzero.','Two-covariate factorial label mismatch at positions4and5.','Target weights5/2versus7/4;anticipation and reversal explicit.','Hypothetical9600/240=40,/160=60,/80=120USD.'],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='incomplete_for_integration',julia='Inspected MIT-style notices;exact delegate and data rights unresolved',fdid='Original GPLv3;MATLAB/runtime rights separate',didtoolbox='No standalone license in complete tree;package-wide permission unestablished',inherited_fixed_effects='Prior2.1.0source not substitute for declared1.10compatibility',integration_allowed=False,evidence=[ref(BASE/'primary-review.json','Original identity and rights anchors')]))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',inputs=['unit_time_order','full_treatment_history','cohort_calendar','anticipation_reversals_spillovers','covariate_timing','target_weights','sample_masks','clusters_dependence','artifact_rights_versions','deadline_budget'],outputs=['cohort_time_and_event_effects','identification_or_refusal','eligible_cell_ledger','weights_covariance_labels','rank_convergence','typed_solver_status','all_attempt_costs'],refusals=['Unjustified trends','Unsupported reversal','Missing control/baseline','Unknown rights','Row/label mismatch','Nonconvergence','Singular uncertainty','Unknown completion'],integration_allowed=False))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',data='Generated adoption/potential outcomes for truth;permitted public panels for workflow realism',arms=['Exact reference','Permitted native estimator','Proposed adapter'],fixtures=[dict(name=n,status='not_run') for n in ['heterogeneous_staggered_twfe','no_final_control','anticipation','reversal','row_permutation','missing_clusters','unequal_weights','unbalanced_projection','covariate_labels','rank_failure','nonconvergence','assignment_exchangeability','infeasible_sensitivity','interruption']],freezes=['Scientific question,assumptions,truth,target','Artifacts and rights','Cohort/time/cluster splits','Scientific/failure oracle','All attempts and costs'],native_execution=False))
    action='Inspect remaining Julia leads and primary gretl/Octave routes;resolve DiDToolbox permission and exact runtime/delegates;qualify matched public/generated panels for targets,anticipation,reversals,clustering,trend sensitivity and semantic fixtures.'
    write(BASE/'omissions-register.json',dict(global_blocker=False,known_routes=[action],unresolved=['Remaining candidates/language coverage','gretl/Octave primary originals','Full package/runtime/dependency rights','Native scientific/failure qualification'],unknown_without_information=['Bank potential outcomes','Unrestricted parallel trends','Assignment exchangeability','Actual value'],next_action=action,absence_claim=False))
    value=dict(operation=OP,status='inconclusive',candidates=[dict(candidate=x,decision='reference_only',integration_allowed=False) for x in sorted(selected)],alternatives=['Adoption deferred','Integration conditional on rights and semantic oracles','Port only under exact rights','Reject silent reversals,algorithm-label equivalence and unsupported uncertainty'],owners=['Scientific','Data/interface','Numerical/inference','Runtime/rights','Evaluation/maintenance'],owner_status='Proposed roles',costs=ref(BASE/'exact-results.json','Hypothetical costs'),next_action=action,capabilities=[],native_execution=False)
    write(BASE/'comparison-review.json',value)
    groups=[('julia','Julia DiffinDiffs suite and interaction-weighted panel contracts',['JuliaDiffinDiffs/DiffinDiffs.jl','JuliaDiffinDiffs/InteractionWeightedDIDs.jl']),('didint','DiDInt0.9.6 covariate,difference and inference contracts',['ebjamieson97/DiDInt.jl']),('matlab','Independent MATLAB DiDToolbox and FDiD panel source comparisons',['relsas/DiDToolbox','Pub-Craig-Researchs/FDiD'])];sources=[]
    for key,title,repos in groups:
        originals=[x for x in validation['originals'] if x['repository'] in repos];identities={x['repository']:x['revision'] for x in originals};rows=[x for x in findings if x['group']==key]
        sources.append(dict(integrated_citation_key='exec25_panelother_'+key,kind='software_primary_sources',title=title,author='Selected repository contributors',year=2026,source_identity='; '.join('https://github.com/'+k+'/tree/'+v for k,v in identities.items()),version_date='Pinned '+','.join(identities.values())+';cutoff7October2026;acquired25October2026',local_copy=originals[0]['local_copy'],local_sources=[x['local_copy'] for x in originals],inspected_anchors=rows,supported_claims=[x['finding'] for x in rows],evidence=[ref(BASE/'git-byte-validation.json','Exact original custody'),ref(BASE/'primary-review.json','Inspected claims')],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec25_panelother_choice',kind='project_evidence_not_scholarly_paper',title='Other-language panel comparison with exact target,projection and identity witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'comparison-review.json','Inconclusive coverage review'),inspected_anchors=[ref(BASE/n,'Authored analysis') for n in ['search-screening.json','mathematical-review.json','conversion-contract.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],supported_claims=['Bounded comparison with explicit search tails','Exact TWFE,projection,label,weight,anticipation,reversal,cost witnesses','Matched public qualification remains proposed'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=4,new_scholarly_pdfs=0,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed plan/evidence') for n in ['plan.md','primary-review.json','comparison-review.json','mathematical-review.json','conversion-contract.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],findings=['Requested dimensions addressed with selected source or explicit gap','Aliases,delegates and rights separate','Exact witnesses independent','No essential-source waiver or unsupported absence']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking question and technical argument'),ref(BASE/'sponsor-addition.md','Investment implications')],findings=['Notation and examples explained','Source findings,derivations and tests separate','Native/coverage/rights limits explicit'],visual_acceptance=False))
    names=['git-byte-validation.json','primary-review.json','comparison-review.json','search-screening.json','mathematical-review.json','exact-results.json','source-audit.json','dependency-license-review.json','conversion-contract.json','qualification-plan.json','omissions-register.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Bounded source evidence') for n in names]+[ref(Path(__file__),'Review/receipt logic')],findings=['Forty original files authenticated','Aliases,delegates and rights differentiated','Other-language cell remains inconclusive'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',outcome='inconclusive',originals=40,new_records=4)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    ev=[ref(BASE/n,'Reviewed bounded coverage') for n in ['review.json','search-screening.json','source-audit.json','omissions-register.json']]
    findings=['Selected candidates and aliases resolved;broader tails remain incomplete','Selected claims bind authentic original/version/hash/anchors;no ungrounded scholarly admission','Alternatives,rights,native limits and continuation explicit;no absence/waiver claim']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Selected Julia/MATLAB panel comparison;language coverage incomplete',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=ev) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['next_action'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Panel inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);a=p.parse_args();prepare() if a.command=='prepare' else receipt()
