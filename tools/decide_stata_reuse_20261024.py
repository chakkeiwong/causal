#!/usr/bin/env python3
"""Stata command-specific reference decision; no licensed software executed."""
import argparse,hashlib,json,re
from pathlib import Path
import stata_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/stata-reuse-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/smile-reuse-reader-v2/reader/source-audit.json'
OP='SW.DECISION.seed_085';read=lambda p:json.loads(p.read_text())
LIMITS=['Retained command manuals and pinned third-party sources; mutable version declarations do not authenticate exact cutoff bytes or current installed build.',
 'No Stata binary, third-party package, native worker, CLI or MCP service executed; no agreement accepted.',
 'Authored finite examples do not qualify native behavior or finite-sample calibration.',
 'Supported edition/service profile, entitlement, complete dependencies, actual prices and performance remain unresolved.',
 'No unrestricted causal, independent, bank, visual or final acceptance.']

def prepare():
    assert not (BASE/'review.json').exists()
    text=(BASE/'development.tex').read_text()
    cited={k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',text) for k in group.replace('\n','').split(',')}
    keys=cited-{'exec24_stata_choice'}
    selected=[s for s in read(PRIOR)['sources'] if s['integrated_citation_key'] in keys]
    assert len(selected)==len(keys),(keys-{s['integrated_citation_key'] for s in selected})
    for s in selected:verify_bindings(s)
    write(BASE/'inherited-review-bindings.json',dict(prior_audit=ref(PRIOR,'Preserved complete predecessor audit'),sources=selected,scope='Existing inspected primary originals retain exact identity,anchors,claims and limitations',cutoff='2026-10-07',native_execution=False))
    specs={
      'exec13_ci_stata_causal_intro':[(8,18,'ATE,ATET,POM and estimation families'),(77,95,'Covariate conditioning and target distinctions')],
      'exec18_gp_stata_xthdid':[(140,153,'Assignment grouping and control groups'),(190,206,'Command-specific robust and cluster equivalence')],
      'exec18_gp_stata_post':[(274,324,'Target weights and pointwise/simultaneous distinction'),(417,430,'Weighted cohort-period target equation')],
      'exec19_dynamic_stata_ab':[(8,14,'Many-panel few-period regime and innovation assumptions'),(104,114,'One/two-step covariance choices'),(239,270,'Sargan and differenced autocorrelation interpretation')],
      'exec21_transport_stata_estimate':[(205,218,'Failed estimation and varying-sample override contracts')],
      'exec22_state_stata_sspace_post':[(97,120,'Prediction information sets and RMSE excludes parameter uncertainty')],
      'exec13_ivrd_license':[(307,337,'Concurrent user and network scope declarations')]
    }
    anchors=[]
    for key,ranges in specs.items():
        p=BASE/(key+'.txt');lines=p.read_text().split('\n')
        for lo,hi,finding in ranges:
            assert 1<=lo<=hi<=len(lines)
            anchors.append(dict(citation_key=key,text_copy=ref(p,'Fresh inert primary extraction'),lines=[lo,hi],excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest(),finding=finding))
    for item in read(BASE/'source-preflight.json'):
        verify_bindings(item['source']);p=ROOT/item['text'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['text_sha256']
    def normalized(key):return ' '.join((BASE/(key+'.txt')).read_text().split())
    assert 'Specifying vce(robust) is equivalent' in normalized('exec18_gp_stata_xthdid')
    assert 'timecohort, the default' in normalized('exec18_gp_stata_post')
    assert 'do not account for estimation error' in normalized('exec22_state_stata_sspace_post')
    assert 'errorok specifies' in normalized('exec21_transport_stata_estimate')
    write(BASE/'identity-review.json',dict(status='pass_for_retained_command_specific_sources',evidence=[ref(BASE/'inherited-review-bindings.json','Full prior primary bindings'),ref(BASE/'source-preflight.json','Ten fresh extracted originals')],inspected_anchors=anchors,selected_records=len(selected),scope='Commercial Stata command families and separately pinned extensions; not one universal estimator',date_limit=LIMITS[0]))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Independent rational arithmetic'),ref(BASE/'exact-results.json','Exact outputs'),ref(BASE/'development.tex','Connected derivations')],findings=['Heterogeneous effects 10,-5 with reversed target weights give7and-2USD; portfolio70000and-20000USD.','Ten shared branch shocks repeated100times give variance1/10versus1/1000under false independence;no finite-cluster calibration asserted.','Two imputations yield pooled1,within1,between2,total4;within-only uncertainty is incomplete.','Gaussian later observation changes state mean0to1;not information available earlier.','Independent level innovations have first-difference lag1correlation-1/2and lag2covariance0.','Hypothetical30000USDover1000/750/500gives30/40/60USD.'],native_execution=False))
    rows=[
      ('business_and_discovery','Supplied SEM and command-defined targets','Business information clock,assumptions,diagram ambiguity and identification;no inferred automated-discovery absence'),
      ('treatment_heterogeneity','ATE/ATET/POM,cate group and conditional means','Exact target,sampling law,support and independent/grouped fold contracts'),
      ('panel_did','Panel/cohort/control-group and aggregation commands','Assignment clusters,weights,estimable cells,pointwise/simultaneous target'),
      ('longitudinal_survival','Specific survival-treatment family with documented exclusions','Separate sequential/censoring/support regime for changing treatments'),
      ('dynamic_and_iv','AB/system dynamic panels,VAR and external-instrument paths','Moment/exclusion/lag assumptions and appropriate diagnostic interpretation'),
      ('mediation','One/two-mediator scope and StataNow-specific feature','Model/type/interaction and unmeasured-confounding restrictions'),
      ('spatial','SAR weighting and impact conventions','Graph/normalization identity and causal-interference assumptions'),
      ('missingness','MI pooling and chained-model controls','Proper imputation,analysis compatibility,samples,all failures and MNAR sensitivity'),
      ('bayesian_state','MCMC and one-step/filter/smoother outputs','Propriety,simulation versus inferential error,frequency and information-time preservation'),
      ('cli_mcp','Proposed isolated licensed command worker','Explicit API/entitlement/artifact,request provenance,typed failures and full costs')]
    write(BASE/'capability-comparison.json',dict(rows=[dict(area=a,documented=b,proposal_obligation=c) for a,b,c in rows],evidence=[ref(BASE/'inherited-review-bindings.json','Retained primary scope'),ref(BASE/'identity-review.json','Fresh concrete anchor review')],scope='Matched command comparison; no product-wide absence or native equivalence claimed'))
    write(BASE/'dependency-license-review.json',dict(status='documented_license_classes_not_service_entitlement',evidence=[ref(BASE/'identity-review.json','Selected official license declaration'),ref(BASE/'inherited-review-bindings.json','Bundled versus separately pinned sources')],unresolved=['Exact installed edition and StataNow features','Agent-facing server/batch/concurrency rights','Third-party package/native plugin rights and support','Actual quote,maintenance and full costs'],agreement_accepted=False,integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',inputs=['Command/build/package identity and supported entitlement','Target population,contrast,units and information clock','Estimation sample,cohorts,control groups,weights and clusters','Nuisance/cross-fitting and covariance/uncertainty definitions','Imputation roles,complete-data model,all failures and overrides','Exact public oracle and restricted native environment'],outputs=['Estimate with explicit target,scale and contributing sample','Uncertainty components and justified sampling regime','Diagnostics distinct from proofs of assumptions','Typed unsupported regime,numeric/estimation failure and partial output','All submitted,completed,qualified requests and costs'],refusals=['Brand-level estimator substitution','Default robust mapped without command-specific meaning','Untracked target weights or dropped cells','Future smoothing used at past decision','Failed imputation omitted silently','Unsupported causal or universal dependence guarantee'],integration_allowed=False))
    next_action='Retain Stata command-specific reference; identify entitled supported edition,service/concurrency profile and separately licensed packages. Preregister public target-weight,assignment-cluster,heterogeneous-DiD,survival-regime,dynamic-moment,MI pooling/failure and prediction-information fixtures. Qualify exact CLI/MCP command outputs and all-request costs;no native or universal causal admission.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,known_routes=['Exact artifact and entitlement/quote inquiry','Finite public command-specific target and covariance oracles','Failure/sample/weight and information-time round trips','Restricted regime native comparison before bank experiments'],remaining=['Current supported commercial service/API profile','All separately installed extensions and rights','Native public fixtures and costs','Exhaustive current command/package search tail'],unknown_without_information=['Unobserved bank treatment assignment and censoring','Unrestricted MNAR mechanisms','Universal calibration under arbitrary dependence','Actual institutional value and acceptance']))
    choice=dict(candidate='Stata',canonical_candidate='Command-specific Stata worker; bundled commands distinct from third-party extensions',decision='reference',selected_revision='Retained exact official/manual and pinned-extension bytes;no binary selected',selected_version='Mixed documented release19/StataNow command context;exact installed edition unresolved',reason='Broad documented methods need target-,regime- and artifact-specific integration,not brand-level causal approval.',alternatives=[dict(route='adopt',decision='defer',reason='No blanket causal,sampling,artifact or entitlement qualification'),dict(route='integrate',decision='conditional',reason='Isolated explicitly entitled command worker with public fixtures'),dict(route='port',decision='unavailable_without_separate_authorization',reason='Proprietary implementation is not open-source reuse;public methods and separate packages need separate reviews'),dict(route='reference',decision='retain',reason='Authenticated prior sources and exact contract witnesses'),dict(route='reject',decision='restricted',reason='Reject unsupported regimes,target substitutions and collapsed uncertainty/failures')],owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Target,causal identification and information clock'),('Statistical','Sampling,weights,clusters,nuisance and uncertainty components'),('Adapter','Versioned command,samples,units,failures and recovery'),('Platform/procurement','Artifact,concurrency,rights,support and actual costs')]],costs=dict(prices='Unmeasured;30000USD authored example',categories=['entitlement','artifact','data conversion','all calls','failed work','review','maintenance']),maintenance='Exact supported edition and service profile unresolved',revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    authored=dict(integrated_citation_key='exec24_stata_choice',kind='project_evidence_not_scholarly_paper',title='Stata command-specific targets,dependence,pooling,information-clock and reuse witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;retained primary manuals;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact authored review'),inspected_anchors=[ref(BASE/n,'Reviewed scope') for n in ['identity-review.json','inherited-review-bindings.json','capability-comparison.json','choice.json','conversion-contract.json','omissions-register.json']],supported_claims=['Command-specific matched scope comparison and conditional licensed-worker route','Exact heterogeneous target and dependence witnesses','Pooling and information-clock consequences','Explicit public fixtures,rights and all-request cost limits'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[authored],new_records=1,new_scholarly_pdfs=0,preserved_primary_records=len(selected),native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_command_specific_reference_choice',evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan.md','identity-review.json','capability-comparison.json','choice.json','mathematical-review.json']],findings=['Preserve broad prior survey and re-inspect concrete unresolved interface semantics.','Do not equate commands or bundled/third-party packages.','Public finite fixtures precede expensive bank validation.','Commercial support/rights unknowns remain local gates.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',evidence=[ref(BASE/'development.tex','Connected comparison'),ref(BASE/'sponsor-addition.md','Sponsor implications')],findings=['Targets,notation,assumptions,alternatives and monetary consequences connected.','Finite mathematics distinguished from native testing and general calibration.','Date,artifact and rights limits retained.'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed evidence') for n in ['identity-review.json','inherited-review-bindings.json','capability-comparison.json','source-audit.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','choice.json','exact-results.json','mathematical-review.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],findings=['Every cited inherited source rebound;ten selected originals freshly extracted.','Exact target,dependence,pooling,information-time and cost witnesses reproduce.','Reference choice grants no native,unrestricted causal or service entitlement.'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(primary_records=len(selected),decision='reference',new_records=1,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed Stata command-specific proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value);evidence=[ref(BASE/n,'Reviewed choice') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Command/artifact identity,rights and maintenance boundaries explicit.','Targets,conversion,alternatives,owners,costs and revisit conditions reviewed.','Reference only;no native,unrestricted causal or deployment entitlement inferred.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Stata reference receipt prepared.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
