#!/usr/bin/env python3
"""Authenticate selected Java source profiles and retain bounded panel coverage."""
import argparse, hashlib, json
from pathlib import Path
import panels_java_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/panels-java-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.panels_did.Java'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Selected dated regression paths and iMetrica scope; not exhaustive Java or JVM panel coverage.',
 'No acquired code, package, upstream test, native worker or bank experiment executed.',
 'Static numerical and variance paths do not qualify causal targets or panel uncertainty.',
 'Root notices and build declarations do not clear complete distribution rights, support, prices or runtime compatibility.',
 'Unknown untreated trends and arbitrary dependence require restrictions or new information.',
 'Q1/Q5, mandatory coverage/depth, visual, independent and final acceptance remain open.']
SPECS={
 'smile_src_0':[(1,10,'Project identity and declared Java version scope; not BayesFusion SMILE')],
 'smile_src_1':[(1,55,'Core GPLv3/commercial declaration and distinct server terms; no legal clearance')],
 'smile_src_2':[(11,20,'Declared version 6.3.0'),(102,120,'GPL declaration and Java 25 preview compile target')],
 'smile_src_3':[(1,4,'Core module identity')],
 'smile_src_4':[(27,65,'OLS assumptions and diagnostic limitations stated in Javadoc'),(125,202,'Formula, rank guard, QR/SVD coefficient routes, later Cholesky and residual-scaled standard errors')],
 'smile_src_5':[(160,205,'Residual sum of squares, scale RSS/(n-p), degrees of freedom and F diagnostic')],
 'smile_src_6':[(58,103,'Longley coefficient-inference, residual and serialization tests present; not locally executed')],
 'commons_src_0':[(43,78,'Development modularization and stated historical release support limitations')],
 'commons_src_1':[(1,27,'Apache License 2.0 root text; complete distribution not cleared')],
 'commons_src_2':[(1,9,'ASF and Orekit notices')],
 'commons_src_3':[(22,68,'4.0-SNAPSHOT, Java 8 target and component dependency versions')],
 'commons_src_4':[(21,30,'Legacy module describes unsupported or not-yet-modularized code')],
 'commons_src_5':[(29,54,'OLS QR design and default intercept'),(242,291,'Coefficient QR solver and unscaled inverse-Gram parameter variance')],
 'commons_src_6':[(280,302,'Public variance return and separately scaled standard-error method'),(345,367,'Residual variance divides residual sum of squares by n-k')],
 'commons_src_7':[(117,185,'Longley coefficient,residual,standard-error and variance-consistency test bodies; not executed')],
 'imetrica_src_0':[(1,44,'GUI time-series and filtering role, native C/Fortran libraries, Linux and dependency declarations')],
 'imetrica_src_1':[(1,20,'Root GPLv3 text identity; no full native distribution clearance')]
}

def prepare():
    assert not (BASE/'review.json').exists()
    rows=read(BASE/'source-index.json')+read(BASE/'imetrica-source-index.json')
    assert len(rows)==17
    records=[]
    for row in rows:
        p=ROOT/row['raw_path'];data=p.read_bytes();receipt=p.with_suffix('.receipt.json');rc=read(receipt)
        assert row['commit_date']<='2026-10-07T15:59:59Z'
        assert hashlib.sha256(data).hexdigest()==rc['sha256']
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
        assert blob==row['blob_sha']
        tree=read(RAW/f'exec25_paneljava_{row["role"]}_tree.json');assert not tree['truncated']
        assert next(x['sha'] for x in tree['tree'] if x['path']==row['path'])==blob
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,finding in SPECS[row['key'].removeprefix('exec25_paneljava_')]:
            assert 1<=lo<=hi<=len(lines),(row['key'],lo,hi,len(lines))
            anchors.append(dict(lines=[lo,hi],finding=finding,excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest()))
        records.append(dict(candidate=row['role'],source_identity=row['url'],upstream_path=row['path'],version_date=row['commit_date']+'; '+row['commit'],local_copy=ref(p,'Authenticated original'),receipt=ref(receipt,'Bounded public acquisition'),git_blob_sha1=blob,inspected_anchors=anchors,supported_claims=[x['finding'] for x in anchors],executed=False))
    write(BASE/'identity-review.json',dict(status='pass',authenticated_files=17,records=records,native_execution=False,evidence=[ref(BASE/n,'Acquired source inventory') for n in ['source-index.json','imetrica-source-index.json']]+[ref(RAW/f'exec25_paneljava_{role}_{part}.json','Pinned pre-cutoff identity') for role in ['smile','commons','imetrica'] for part in ['cutoff','tree']]))
    searches=[]
    for i in range(3):
        p=RAW/f'exec25_paneljava_search_{i}.json';d=read(p)
        searches.append(dict(source=ref(p,'Discovery only'),receipt=ref(p.with_suffix('.receipt.json'),'Query and retrieval time'),total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],repositories=[x['full_name'] for x in d['items']]))
    write(BASE/'search-screening.json',dict(status='bounded_not_exhaustive',searches=searches,selected=['haifengl/smile','apache/commons-math','clisztian/iMetrica'],screening='Two exact panel/DiD repository queries returned zero. A broader econometrics query returned 15 leads; iMetrica was inspected for declared scope. Other leads remain uninspected.',limits=['GitHub repository search is mutable discovery, not a historical census or full-text code search.','No ecosystem-wide absence claim; package registries, additional JVM bridges and dedicated panel/synthetic-control candidates remain.','Filename matches containing Panel can denote GUI widgets; filenames alone do not establish econometric capability.']))
    assert exact.calculate()==read(BASE/'exact-results.json')
    findings=['Exact staggered 2x3 design has weights 1,-1/2,1/2, coefficient -7/2 versus equal-treated-cell effect4.','Two-cluster repeated-row mean variance1/2 differs from independent-row variance1/4 under exact stipulated laws.','Inverse Gram1/2 differs from residual-scaled covariance9/2.','Identical observed DiD3 is compatible with effect3 or0 under different untreated trends.','Illustrative2400/100=24 and2400/60=40; not observed costs.']
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_witnesses',evidence=[ref(Path(exact.__file__),'Independent exact construction'),ref(BASE/'exact-results.json','Exact enumeration and rational arithmetic'),ref(BASE/'development.tex','Explained notation and assumptions')],findings=findings,native_execution=False,empirical_coverage=False))
    write(BASE/'comparison-review.json',dict(status='bounded_reference_comparison',profiles=[
        dict(candidate='Smile',version='6.3.0 declaration at pinned commit',decision='Retain numerical reference; defer direct panel adoption and port',strength='Formula-based OLS with QR/SVD and ordinary coefficient diagnostics',gap='No inspected panel/cohort/control/cluster contract; rank fallback and later inverse paths need native tests'),
        dict(candidate='Apache Commons Math',version='4.0-SNAPSHOT pinned development tree',decision='Retain numerical reference; defer panel admission and port',strength='Explicit QR and variance/standard-error source paths and numerical tests',gap='Legacy support, unscaled covariance interface, cluster sampling and causal target require explicit contract'),
        dict(candidate='iMetrica',version='Pinned 2016 source',decision='Defer as a panel delegate; retain time-series scope lead',strength='Declared interactive financial time-series/filtering scope',gap='README and license do not establish a dedicated panel estimator; C/Fortran native components unqualified')],native_execution=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',inputs=['Panel and row IDs,event and observation clocks,treatment history,cohorts and controls','Target,anticipation,reversals,weights,missingness and supported horizons','Design/intercept/rank convention,covariance scaling,cluster IDs and sampling regime','Requested native environment,dependency/rights profile and failure policy'],outputs=['Resolved target and comparisons,coefficients and covariance units','Complete requested/eligible/estimated/refused/failed denominators','Rank and missingness decisions,uncertainty type,independent-unit counts and full costs'],public_tests=['Known linear covariance and intercept fixtures','Constructed staggered heterogeneous effect and absent-control horizon','Reversed and anticipated treatment histories','Unequal and repeated clusters,unbalanced panels,missing groups and conversion failures'],integration_allowed=False,oracle=ref(BASE/'exact-results.json','Independent exact witnesses')))
    write(BASE/'dependency-license-review.json',dict(status='declarations_only',evidence=[r['local_copy'] for r in records if any(x in r['upstream_path'] for x in ['LICENSE','NOTICE','build.sbt','pom.xml','README'])],declarations=['Smile core GPLv3/commercial and Java25 preview; separate server/studio terms must not be conflated.','Apache2.0 root material and third-party notice;4.0-SNAPSHOT legacy profile and component dependencies;Java8 target.','iMetrica rootGPLv3 and native GSL,Fortran and f2c declarations.'],unresolved=['Complete exact distribution and transitive rights','Supported runtime and deployment profile','Entitlement,maintenance,full prices and measured costs'],legal_clearance=False,integration_allowed=False))
    next_action='Inspect further dedicated Java/JVM panel, synthetic-control and bridge candidates; qualify only a pinned numerical or typed cross-language public profile with target,control,cluster,covariance,rank and failure oracles. Resolve exact distribution rights and full costs. Unknown counterfactual trends remain assumption or information gaps.'
    write(BASE/'omissions-register.json',dict(known_routes=['Broaden primary-text panel and JVM bridge survey beyond three repository searches.','Inspect remaining candidate implementations and complete dependencies.','Preregister generated public trials with known causal truth and required refusals before native work.','Compare a typed R/Python delegate while preserving its reviewed limits.'],no_universal_solution=['Unknown counterfactual trends','Arbitrary dependence without sampling restrictions'],next_action=next_action,global_blocker=False))
    prior=read(ROOT/'docs/program/execution/2026-10-25/ecmo-reader-v1/reader/source-audit.json');old={s['integrated_citation_key']:s for s in prior['sources']}
    sources=[]
    for role,author in [('smile','Haifeng Li and Smile contributors'),('commons','Apache Software Foundation'),('imetrica','iMetrica contributors')]:
        rs=[r for r in records if r['candidate']==role]
        sources.append(dict(integrated_citation_key='exec25_paneljava_'+role,kind='software_primary_sources',title=role+' dated Java regression or econometrics source profile',author=author,year=2026,source_identity=rs[0]['source_identity'],version_date=rs[0]['version_date'],local_copy=rs[0]['local_copy'],records=rs,identity_evidence=[ref(BASE/'identity-review.json','Authenticated originals')],inspected_anchors=[r['local_copy'] for r in rs],supported_claims=[f for r in rs for f in r['supported_claims']],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec25_paneljava_reference',kind='project_evidence_not_scholarly_paper',title='Authored Java panel target,covariance,trend and cost comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact authored examples'),inspected_anchors=[ref(BASE/n,'Proposed scoped contract') for n in ['comparison-review.json','conversion-contract.json','omissions-register.json','search-screening.json']],supported_claims=findings,limitations=LIMITS))
    inherited=['exec24_panelpy_differences','exec24_panelpy_csdid']
    write(BASE/'source-audit.json',dict(sources=sources+[old[k] for k in inherited],cutoff='2026-10-07',new_records=4,new_scholarly_pdfs=0,unchanged_inherited_keys=inherited,native_execution=False))
    evidence=[ref(BASE/n,'Reviewed source or comparison') for n in ['identity-review.json','source-audit.json','search-screening.json','comparison-review.json','conversion-contract.json','dependency-license-review.json','omissions-register.json','mathematical-review.json','development.tex','sponsor-addition.md']]
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_inconclusive_review',evidence=evidence,steps=['Authenticate17selected originals against receipt SHA and Git blobs.','Inspect full selected numeric and variance paths before making claims.','Reproduce exact authored panel and cost witnesses.','Integrate connected argument preserving1192prior records and258PDFs.','Record Java coverage as inconclusive; broaden remaining survey and public qualification independently.'],coverage_pass=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Sponsor implication')],findings=['Source behavior, exact examples and proposed native trials distinguished.','No universal absence, legal clearance, observed native failure or counterfactual truth inferred.','No process text in product narrative.'],visual_acceptance=False))
    review=dict(status='pass_for_scoped_review_not_coverage_closure',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence+[ref(BASE/'plan-review.json','Reviewed execution plan'),ref(BASE/'copyedit-review.json','Argument review'),ref(Path(__file__),'Review logic')],findings=findings,limitations=LIMITS,coverage_outcome='inconclusive',next_action=next_action,capabilities=[],native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated=17,new_records=4,papers_added=0,coverage='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    review=read(BASE/'review.json');verify_bindings(review);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    evidence=[ref(BASE/n,'Bounded Java panel review') for n in ['review.json','source-audit.json','search-screening.json','comparison-review.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','exact-results.json']]
    out=ROOT/node['outputs'][0]
    value=dict(operation=OP,status='inconclusive',scope='Selected Java regression and econometrics profiles; no exhaustive panel or native qualification',candidates=['haifengl/smile','apache/commons-math','clisztian/iMetrica'],source_review=ref(BASE/'source-audit.json','Pinned source review'),evidence=evidence,next_action=review['next_action'],limitations=LIMITS,capabilities=[],integration_allowed=False)
    write(out,value);result=run.ledger.receipt_template(node)
    findings=[('inconclusive','Three bounded profiles inspected; wider Java/JVM panel and bridge search remains.'),('pass','17 pre-cutoff originals authenticated; selected numerical and variance call paths inspected; exact project witnesses reproduce.'),('pass','Panel targets,controls,sampling,covariance,rights,failure,cost and public qualification routes explicit without native admission.')]
    result.update(outcome='inconclusive',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Bounded Java panel coverage')],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['next_action'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result)
    print('Bounded Java panel receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
