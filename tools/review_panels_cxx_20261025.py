#!/usr/bin/env python3
"""Bound selected C++ primary paths, explicit survey tails and exact witnesses."""
import argparse,hashlib,json
from pathlib import Path
import panels_cxx_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/panels-cxx-v1';RAW=ROOT/'docs/literature/raw';OP='SW.CELL.panels_did.Cxx'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected fixest kernels and xhdfe paths, plus four scope leads; not exhaustive C++ panel coverage.',
 'No acquired code,upstream test,native benchmark or bank experiment executed.',
 'Algebraic block-replacement witness is not proven reachable package output or observed native failure.',
 'Full absorber,OLS/sandwich,bindings,backend and transitive dependencies remain uninspected.',
 'Scope declarations and root notices do not qualify technical claims,distribution rights or commercial costs.',
 'Unknown untreated trends,arbitrary dependence and economic value need restrictions or further evidence.',
 'Q1/Q5,mandatory coverage/depth,visual,independent and final acceptance remain open.']
SPECS={
 'fixest_0':[(1414,1435,'R-object demeaning entry,weights,iteration,tolerance and slope arguments'),(1645,1674,'Iteration counts and optional means/fixed-effects returned')],
 'fixest_1':[(104,158,'Sequential Cholesky tolerance exclusion and all-removed status'),(199,218,'Inverse Gram,excluded columns and minimum-norm return')],
 'fixest_2':[(132,183,'Panel-kernel comment and contiguous time-block setup'),(205,310,'Zero lag,balanced/unbalanced matched-unit lag accumulation and symmetrization')],
 'fixest_3':[(1,30,'Generated Rcpp exports retain R object and runtime boundary')],
 'fixest_4':[(1,50,'Rcpp/OpenMP dependency and combined absolute-relative stopping rules')],
 'fixest_5':[(1,15,'Author notice and inherited helper origin comment; no full helper rights clearance')],
 'fixest_6':[(1,3,'Build flags and strict R headers')],
 'xhdfe_src_0':[(1,18,'Development version and multi-language C++ scope claims'),(20,48,'Historical performance claims and explicit mode/coverage limits; not reproduced')],
 'xhdfe_src_1':[(1,21,'Root MIT terms and notices only')],
 'xhdfe_src_2':[(1,8,'Version2.29.3.20261007 and C++17'),(44,45,'Optional CUDA declaration'),(73,90,'CUDA toolkit and architecture requirements')],
 'xhdfe_src_3':[(14,103,'Covariance,absorption,convergence,singleton,frequency and degrees-of-freedom options'),(108,185,'Covariance,sample,convergence,cluster and repair fields')],
 'xhdfe_src_4':[(1,27,'Eigen,absorption and OLS dependencies;group aggregation and thread options')],
 'xhdfe_src_5':[(768,815,'Ordinary/wide eigenvalue-clamping paths;ordinary solver failure returns false'),(8239,8310,'Output postcondition checks convergence,shape and finite available entries'),(8441,8476,'Conditional Gram defect check and separate per-row capture gate'),(12340,12424,'Robust and clustered scaling and degrees-of-freedom paths'),(12445,12605,'Recovered intercept,multiway full/slope repair and unavailable-inference path'),(12605,12640,'Postcondition and numerical residual checks with bounded refinement continuation')],
 'xhdfe_src_6':[(11,53,'Wide covariance standardization,eigensolve,negative-value clamping and failure exception')],
 'xhdfe_src_7':[(1,18,'Standalone demeaning source declares helper/native dependencies;integration comment not accepted as qualification')],
 'xhdfe_src_8':[(14,80,'Upstream empty-slope cluster tests,missing labels and one-cluster inference refusal;not executed')],
 'xhdfe_src_9':[(73,132,'Upstream full projection plus separately restored slope block comparator and outputs;not executed')],
 'xhdfe_src_10':[(1,31,'Upstream analytic fixture and covariance-oracle declarations;not independently reproduced')],
 'xhdfe_dep_0':[(1,45,'Two-component precision arithmetic and IEEE helper dependency;full proof not supplied')],
 'xhdfe_dep_1':[(1,18,'Eigen MPL2 and additional third-party license notice;complete artifact not cleared')],
 'sdid_scope_0':[(1,31,'Declared synthetic-DiD R workflow;implementation and cited paper not inspected here')],
 'sdid_scope_1':[(1,12,'Version1.0,GPL3 declaration,Rcpp and RcppArmadillo dependencies')],
 'capybara_scope_0':[(15,51,'README separates earlier paper and2.x work;declared GLM/fixed-effect role and cpp4r/armadillo4r')],
 'capybara_scope_1':[(1,35,'Version2.4.0,declared model scope,Apache>=2 and compiled dependencies;not technical qualification')],
 'gfe_scope_0':[(1,1,'README contains only a project heading')],
 'gfe_scope_1':[(1,37,'Version0.0.1,declared grouped models and Rcpp dependencies;License field retains template')],
 'nnr_scope_0':[(1,30,'Declared nonlinear interactive-effects pipeline,tuning,bias correction and local-MLE route;not theorem evidence')],
 'nnr_scope_1':[(1,26,'Version0.0,dated packaging,GPL3 and RcppEigen dependency declarations')],
 'sdid_license':[(1,17,'Actual GPL3 text identity')],
 'capybara_license':[(1,17,'Actual Apache2.0 text identity')],
 'gfe_license':[(1,21,'Root MIT text differs from unresolved package License field')]
}

def prepare():
    assert not (BASE/'review.json').exists()
    rows=sum([read(BASE/n) for n in ['source-index.json','xhdfe-source-index.json','scope-source-index.json','license-source-index.json']],[])
    assert len(rows)==31
    records=[]
    for row in rows:
        role=row.get('role',row['key'].removeprefix('exec25_panelcxx_').split('_')[0])
        treepath=RAW/('exec20_fixest_tree.json' if role=='fixest' else f'exec25_panelcxx_{role}_tree.json')
        cutoff=RAW/('exec20_fixest_cutoff_commit.json' if role=='fixest' else f'exec25_panelcxx_{role}_cutoff.json')
        cd=read(cutoff);cd=cd[0] if isinstance(cd,list) else cd
        assert cd['sha']==row['commit'] and cd['commit']['committer']['date']<='2026-10-07T15:59:59Z'
        p=ROOT/row['raw_path'];data=p.read_bytes();rc=p.with_suffix('.receipt.json')
        assert hashlib.sha256(data).hexdigest()==read(rc)['sha256']
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==row['blob_sha']
        tree=read(treepath);assert not tree['truncated'];assert next(x['sha'] for x in tree['tree'] if x['path']==row['path'])==blob
        ls=data.decode().splitlines();anchors=[]
        for lo,hi,f in SPECS[row['key'].removeprefix('exec25_panelcxx_')]:
            assert 1<=lo<=hi<=len(ls),(row['key'],lo,hi,len(ls))
            anchors.append(dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256(chr(10).join(ls[lo-1:hi]).encode()).hexdigest()))
        records.append(dict(candidate=role,source_identity=row['url'],version_date=cd['commit']['committer']['date']+';'+row['commit'],upstream_path=row['path'],local_copy=ref(p,'Authenticated original'),receipt=ref(rc,'Acquisition'),identity=[ref(treepath,'Git tree'),ref(cutoff,'Pre-cutoff commit')],git_blob_sha1=blob,inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
    wrapper=[]
    for name,spans in [('exec20_fixest_tech_0.txt',[(2187,2245,'R OLS caller preserves exclusions and all-removed status')]),('exec20_fixest_tech_2.txt',[(2150,2195,'R caller sorts time then unit,reorders scores,rejects duplicate keys and halves zero-lag weight')])]:
        p=RAW/name;ls=p.read_text().splitlines();wrapper.append(dict(local_copy=ref(p,'Previously authenticated original R caller'),inspected_anchors=[dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256(chr(10).join(ls[lo-1:hi]).encode()).hexdigest()) for lo,hi,f in spans]))
    write(BASE/'identity-review.json',dict(status='pass',authenticated_files=31,records=records,additional_wrapper_inspection=wrapper,native_execution=False))
    searches=[]
    for i in range(2):
        p=RAW/f'exec25_panelcxx_search_{i}.json';d=read(p);searches.append(dict(source=ref(p,'Mutable discovery only'),receipt=ref(p.with_suffix('.receipt.json'),'Query and retrieval'),total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],repositories=[x['full_name'] for x in d['items']]))
    write(BASE/'search-screening.json',dict(status='bounded_not_exhaustive',searches=searches,selected_detailed=['fixest selected C++kernels with Rcallers','xhdfe selected API and covariance paths'],scope_only=['elakkis/SDID','pachadotdev/capybara','jrive/gfe','wszhang-econ/NNRPanel'],excluded=['Audio effects hit unrelated to econometric fixed effects','metaBMA meta-analysis not selected as panel delegate','cran/capybara mirror not counted as a separate package'],limits=['Repository searches are mutable discovery;not historical/full-text/exhaustive census.','Four scope leads require technical implementation,original-paper and full license review.']))
    assert exact.calculate()==read(BASE/'exact-results.json')
    findings=['Full PSD projection followed by separately projected block replacement can yield determinant-3/4 and contrast variance-3;native reachability unproved.','Two-period scalar panel score witness gives41withhalved zero lag versus71without halving.','Weighted projection produces zero weighted residual sum;unweighted substitution gives2.','Unit-constant treatment is fully absorbed;unavailable effect is not zero.','Illustrative3600/120=30 versus3600/80=45;not measured prices.']
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Independent rational arithmetic'),ref(BASE/'exact-results.json','Exact results'),ref(BASE/'development.tex','Explained assumptions')],findings=findings,native_execution=False,native_reachability_proved=False))
    next_action='Inspect full xhdfe OLS/sandwich/absorption/binding/dependency paths and concrete SDID,capybara,gfe,NNRPanel kernels and genuine methodological originals. Resolve license discrepancy and exact distributions. Preregister public weighted/rank/time-order/cluster/full-covariance/failure tests before native admission;unknown causal trends require restrictions or new information.'
    profiles=[dict(candidate='fixest C++kernels',decision='Reference;prefer original typed Rworker, defer bare port',reason='Rcpp object and caller-dependent sample,time,rank,covariance semantics'),dict(candidate='xhdfe',decision='Reference/candidate for narrow public profile;defer adoption and port',reason='Useful observable API;partial source review,backend/precision/full covariance and rights need qualification')]+[dict(candidate=x,decision='Defer;scope lead only',reason='Primary README/descriptor retained;technical source and methodological originals not yet reviewed') for x in ['SDID','capybara','gfe','NNRPanel']]
    write(BASE/'comparison-review.json',dict(status='bounded_reference_comparison',profiles=profiles,evidence=[ref(BASE/'identity-review.json','Source andwrapper paths')],native_execution=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',inputs=['Panel/case IDs,calendar,time ordering,treatment/cohort/control target','Weight type and normalization,missingness,singleton selection,rank and tolerance','Requested/resolved backend,threads,mode and compiler','Cluster counts,sampling regime,small-sample settings and covariance normalization'],outputs=['Coefficients including unavailable targets,exact selection and transformed-design diagnostics','Full raw/repaired covariance,scaling/repair/eigensolver status and supported contrasts','Complete requests,failures,refusals,backend status and costs'],tests=['Weighted dummy/projection equality','Absorbed treatment cannot become zero causal effect','Sorted/unsorted/time-gap/duplicate fixtures','Empty slopes,few clusters,nonfinite and full PSD/contrast failures','Attainability test before attributing block-replacement witness to native implementation'],integration_allowed=False,oracle=ref(BASE/'exact-results.json','Exact independent witnesses')))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',declarations=['fixest inherited GPL/Rcpp/OpenMP and Rruntime boundary','xhdfe rootMIT,C++17,optional CUDA,EigenMPL2 plus additional third-party notice','SDID rootGPL3,Rcpp/RcppArmadillo','capybara Apache2.0 root,cpp4r/armadillo4r','gfe rootMIT versus placeholder License field','NNRPanel GPL3 field;no root license original acquired'],evidence=[r['local_copy'] for r in records if any(t in r['upstream_path'] for t in ['LICENSE','DESCRIPTION','COPYING','CMakeLists','Makevars'])],rights_clearance=False,native_execution=False))
    write(BASE/'omissions-register.json',dict(next_action=next_action,known_routes=['Complete matched C++delegate and wrapper paths','Acquire genuine methodological PDFs for retained scope candidates before technical citation','Resolve gfe metadata discrepancy and distribution rights','Qualify independently authored public fixtures and all costs'],unresolved=['Full-matrix covariance attainability and scientific calibration','Complete native backend parity','Unknown counterfactual trends and unrestricted dependence'],global_blocker=False))
    prior=read(ROOT/'docs/program/execution/2026-10-25/panels-java-reader-v1/reader/source-audit.json');old={s['integrated_citation_key']:s for s in prior['sources']};sources=[]
    for role in ['fixest','xhdfe','sdid','capybara','gfe','nnr']:
        rs=[r for r in records if r['candidate']==role]
        sources.append(dict(integrated_citation_key='exec25_panelcxx_'+role,kind='software_primary_sources',title=role+' pinned C++panel source or scoped candidate review',author=role+' contributors',year=int(rs[0]['version_date'][:4]),source_identity=rs[0]['source_identity'],version_date=rs[0]['version_date'],local_copy=rs[0]['local_copy'],records=rs,identity_evidence=[ref(BASE/'identity-review.json','Identity and call boundaries')],inspected_anchors=[r['local_copy'] for r in rs],supported_claims=[f for r in rs for f in r['supported_claims']],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec25_panelcxx_reference',kind='project_evidence_not_scholarly_paper',title='Authored C++panel projection,time,covariance and cost witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact independent examples'),inspected_anchors=[ref(BASE/n,'Scoped proposal contract') for n in ['comparison-review.json','conversion-contract.json','omissions-register.json','search-screening.json']],supported_claims=findings,limitations=LIMITS))
    inherited=['exec20_fixest_source','exec25_paneljava_reference']
    write(BASE/'source-audit.json',dict(sources=sources+[old[k] for k in inherited],cutoff='2026-10-07',new_records=7,new_scholarly_pdfs=0,unchanged_inherited_keys=inherited,native_execution=False))
    evidence=[ref(BASE/n,'Bounded review') for n in ['identity-review.json','source-audit.json','search-screening.json','comparison-review.json','conversion-contract.json','dependency-license-review.json','omissions-register.json','mathematical-review.json','development.tex','sponsor-addition.md']]
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_inconclusive_review',evidence=evidence,steps=['Authenticate31new originals and inspect selected wrapper call paths.','Preserve declared scopes and complete technical survey tails.','Verify exact algebra independently;do not assert native failure without attainability.','Preserve1196prior records and258scholarlyPDFs;add7software/project records.','Record only bounded inconclusive C++coverage, pair sponsor,renew reviews,reconcile all obligations,check and deliver.'],coverage_pass=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected product argument'),ref(BASE/'sponsor-addition.md','Sponsor comparison')],findings=['Wrapper/body discrepancies are distinguished from observed native failures.','No benchmark,law,underlying paper or adoption claim borrowed from discovery.','Exact covariance witness states reachability limitation and separate sampling qualification.'],visual_acceptance=False))
    review=dict(status='pass_for_scoped_review_not_coverage_closure',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence+[ref(BASE/'plan-review.json','Plan review'),ref(BASE/'copyedit-review.json','Argument review'),ref(Path(__file__),'Review logic')],findings=findings,limitations=LIMITS,coverage_outcome='inconclusive',next_action=next_action,capabilities=[],native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(authenticated=31,new_records=7,papers_added=0,coverage='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    review=read(BASE/'review.json');verify_bindings(review);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    evidence=[ref(BASE/n,'Bounded C++panel review') for n in ['review.json','source-audit.json','search-screening.json','comparison-review.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','exact-results.json']]
    out=ROOT/node['outputs'][0];value=dict(operation=OP,status='inconclusive',scope='Selected C++kernels and xhdfe paths plus four scope leads;not exhaustive/native panel qualification',candidates=['fixest C++','xhdfe','SDID','capybara','gfe','NNRPanel'],source_review=ref(BASE/'source-audit.json','Pinned sources'),evidence=evidence,next_action=review['next_action'],limitations=LIMITS,capabilities=[],integration_allowed=False)
    write(out,value);result=run.ledger.receipt_template(node);findings=[('inconclusive','Two selected source profiles and four scope leads;full delegates and wider coverage remain.'),('pass','31new originals authenticated;caller/body boundaries inspected;exact algebra reproduced without downloaded-code execution.'),('pass','Explicit targets,time/rank/weight/covariance contracts,rights,alternatives and public trial route;no native capability.')]
    result.update(outcome='inconclusive',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Scoped C++coverage')],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['next_action'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Bounded C++ panel receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
