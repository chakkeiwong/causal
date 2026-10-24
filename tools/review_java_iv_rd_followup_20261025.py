#!/usr/bin/env python3
"""Authenticate selected Java/JVM originals, anchored claims and exact witnesses."""
import argparse, hashlib, json
from pathlib import Path
import java_iv_rd_followup_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/java-iv-rd-followup-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.iv_rd_design.Java'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Bounded Java/JVM discovery; returned and unreturned candidate tails, Maven coverage and generic RD coverage remain open.',
 'Static original-source review and authored arithmetic only; no downloaded code or installed native package executed.',
 'Selected Tetrad callers do not establish whole-library reachability; public Tsls invocation and concrete branch qualification remain proposed.',
 'Kausaali instrumental forest is a placeholder at the inspected pin; repository metadata does not qualify Maven release bytes.',
 'Selected ScalaTion and historical SuanShu OLS paths do not establish generic IV/RD coverage or current vendor support.',
 'Complete numerical delegates, artifact provenance, dependency rights, scientific assumptions and law-specific uncertainty remain unqualified.',
 'No new scholarly theorem is imported from source comments; visual, independent, bank and final acceptance remain open.'
]
NEXT='Complete JVM/Maven candidate and generic RD discovery; inspect remaining callers, distribution provenance and solver/uncertainty delegates. Preregister public tests for nonsquare indexing, latent normalization, skipped-parameter masks, singularity, weak instruments and weighted-moment semantics. Revisit Kausaali instrumental support only after an implemented revision; compare exact-version R/Python workers without claiming native admission.'

SPECS={
 'tetrad':('Tetrad latent-IV data axes, parameter lifecycle and numerical boundary','cmu-phil/tetrad','7.6.11-SNAPSHOT;22 September 2026;b89afaf952a4fd647df0d85b08102250106c6764',[
 ('exec22_javaiv_tetrad_tsls',52,100,['public Tsls','new SemIm','estimateCoeffs'],'Public construction and estimate lifecycle.'),
 ('exec22_javaiv_tetrad_tsls',110,164,['lexicographical','fixedLoadings'],'Explicit or name-selected latent measurement normalization.'),
 ('exec22_javaiv_tetrad_tsls',376,432,['this.nodeName','if (c == 0)','getDouble(colIndex, i)'],'Node restriction, skipped measurement and swapped-axis source path.'),
 ('exec25_javaiv_src_0',908,921,['getDouble(int row, int column)','this.dataBox.get(row, column)'],'Concrete data wrapper preserves row/column roles.'),
 ('exec25_javaiv_src_1',134,145,['get(int row, int col)','this.data[row][col]'],'Row-major data box access.'),
 ('exec25_javaiv_src_2',160,168,['get(int row, int col)','this.data[col][row]'],'Column-major storage preserves public row/column contract.'),
 ('exec25_javaiv_src_3',208,272,['public SemIm(SemPm semPm)','initializeValues()'],'New model constructs parameter mappings and initializes them.'),
 ('exec25_javaiv_src_3',2145,2174,['fixedMappings','freeMappings','getStandardError','sampleCovar == null'],'Initial values and distinct standard-error missing-covariance guard.'),
 ('exec25_javaiv_src_3',2540,2575,['isInitializedRandomly','nextUniform','getStartingValue'],'Configured/random initial values are not fitted-value evidence.'),
 ('exec25_javaiv_src_4',183,225,['new SemIm(getSemPm(), getCovMatrix())','optimize(semIm)','setEstimated(true)'],'Separate SemEstimator explicitly runs optimizer and marks estimation.'),
 ('exec22_javaiv_tetrad_tsls',473,485,['asymptLCovar','sigma_ui'],'Local covariance helper has no outward assignment in this method.'),
 ('exec22_javaiv_tetrad_matrix_backend',343,362,['Matrix inverse()','CommonOps_DDRM.invert','return new Matrix(inverse)'],'Matrix wrapper discards the inversion boolean.'),
 ('exec25_javaiv_src_7',148,162,['org.ejml','0.44.0'],'Declared EJML dependency version.'),
 ('exec25_javaiv_src_0',1,23,['GNU General Public License','either version 3'],'Original GPL notice; complete distribution rights separate.')]),
 'ejml':('EJML 0.44.0 completion, singularity and direct-inverse contracts','lessthanoptimal/ejml','0.44.0;22 March 2025;7d47450d8451ee081a77fe304d9984ceb27e6fa7',[
 ('exec25_javaiv_ejml_src_1',28,36,["version = '0.44.0'"],'Pinned build version.'),
 ('exec25_javaiv_ejml_src_2',775,825,['results could still be bad','public static boolean invert','solver.setA(mat)','return true'],'Completion boolean does not establish nonsingularity or conditioning.'),
 ('exec25_javaiv_ejml_src_6',34,77,['MAX = 5','double det','m11 / det'],'Small-matrix route divides cofactors by determinant.'),
 ('exec25_javaiv_ejml_delegate_0',30,42,['extends LinearSolverLuBase_DDRM','super(decomp)'],'Concrete LU solver inherits the inspected base.'),
 ('exec25_javaiv_ejml_src_3',33,72,['decomp.decompose(A)','void invert','_solveVectorInternal'],'LU setup/decomposition and inverse loop.'),
 ('exec25_javaiv_ejml_src_4',168,181,['almost singular','isSingular','UtilEjml.EPS'],'Separate singularity predicate and near-singularity warning.'),
 ('exec25_javaiv_ejml_src_5',99,114,['lujj != 0','return true'],'Selected decomposition returns completion after zero-pivot-sensitive loop.'),
 ('exec25_javaiv_ejml_src_0',1,16,['Apache License','Version 2.0'],'Original Apache terms.')]),
 'kausaali':('Kausaali instrumental-forest placeholder and actual public factories','vilhomaa/kausaali','repository pin;7 September 2026;257f4b9c3caff72d0ea7c3bb3da17c2569b69db1',[
 ('exec25_javaiv_kausaali_src_3',1,30,['PLACEHOLDER','not implemented','Wald ratio'],'Instrumental estimator is explicitly unimplemented; comments describe intended contracts.'),
 ('exec25_javaiv_kausaali_src_4',1,22,['unimplemented stub','in pending'],'Three pending tests are not passed native evidence.'),
 ('exec25_javaiv_kausaali_delegate_0',93,112,['def causal','def regression'],'Inspected public factories expose causal and regression paths.'),
 ('exec25_javaiv_kausaali_src_2',8,17,['3.3.5','Apache-2.0'],'Scala version and declared license metadata.'),
 ('exec25_javaiv_kausaali_src_1',1,29,['Maven Central','<latest>'],'README distribution claims; exact published artifact unresolved.'),
 ('exec25_javaiv_kausaali_src_0',1,15,['Apache License','Version 2.0'],'Original Apache terms.')]),
 'scalation':('ScalaTion 2 regression scope and retained provenance notices','scalation/scalation2','2.0 repository pin;6 May 2026;3aa581e7a5aefaf1d9bbf6528e20b387ec67ca2d',[
 ('exec25_javaiv_scalation2_src_3',52,100,['private def solver','Fac_QR','def train','ordinary least squares'],'Selected regression is OLS with declared factorization branches.'),
 ('exec25_javaiv_scalation2_src_2',4,21,['3.8.3','scala-parallel-collections'],'Source build and dependency declarations.'),
 ('exec25_javaiv_scalation2_src_0',1,21,['MIT License','Youseffekri'],'Root license notice retained without replacing provenance.'),
 ('exec25_javaiv_scalation2_delegate_0',1,26,['John A. Miller','University of Georgia','Permission is hereby granted'],'Separate README-linked historical notice retained.')]),
 'suan':('Historical SuanShu mirror OLS scope and source identity','aaiyer/SuanShu','20120606 mirror;15 May 2021;ed9829aed161112e4d5fb5e2a1ab5ae05d99a491',[
 ('exec25_javaiv_suan_src_2',74,97,['OLSRegression(LMProblem problem)','OLSSolver','problem.wA','diagnostics'],'Selected constructor solves weighted OLS and builds diagnostics.'),
 ('exec25_javaiv_suan_src_1',1,16,['suanshu-20120606','1.0-SNAPSHOT'],'Historical artifact identity; not current vendor edition evidence.'),
 ('exec25_javaiv_suan_src_0',178,201,['NUMERICAL METHOD','Apache License'],'Retained dated license application notice.'),
 ('exec25_javaiv_suan_src_2',1,22,['Numerical Method Inc.','LICENSED, NOT SOLD'],'Original source notice retained; no present commercial rights conclusion.')])
}

def authenticate():
    rows=[];evidence=[]
    for name in ['source-selection.json','complementary-source-selection.json','ejml-source-selection.json','candidate-source-selection.json','final-source-selection.json']:
        d=read(BASE/name);rows.extend(d['sources'] if isinstance(d,dict) else d);evidence.append(ref(BASE/name,'Pinned file identities'))
    assert len(rows)==36
    originals=[]
    for x in rows:
        p=RAW/(x['id']+'.txt');b=p.read_bytes();receipt=p.with_suffix('.receipt.json');r=read(receipt)
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
        assert len(b)==x['bytes'] and core.sha(p)==r['sha256'] and r['status']=='saved'
        originals.append(dict(repository_path=x['path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original bytes'),retrieval=ref(receipt,'URL, date and SHA256')))
    for key in ['ejml','kausaali','scalation2','suan','scalationold']:
        for suffix in ['tree','commit']:
            evidence.append(ref(RAW/f'exec25_javaiv_{key}_{suffix}.json','Pinned repository identity, date and tree'))
    evidence.extend([ref(RAW/'v12_sw2_tetrad_tree.json','Preserved complete Tetrad tree'),ref(ROOT/'docs/program/execution/2026-10-22/java-iv-rd-preflight-v1/review.json','Four inherited originals')])
    result=dict(status='pass',count=36,originals=originals,evidence=evidence)
    verify_bindings(result);write(BASE/'authenticated-originals.json',result)

def prepare():
    assert not (BASE/'review.json').exists()
    fragments=[];sources=[]
    for key,(title,repo,version,checks) in SPECS.items():
        evidence=[];anchors=[];claims=[]
        for stem,lo,hi,tokens,finding in checks:
            p=RAW/(stem+'.txt');lines=p.read_text().splitlines();hi=min(hi,len(lines));s='\n'.join(lines[lo-1:hi]);assert all(t in s for t in tokens),(stem,lo,hi,[t for t in tokens if t not in s])
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=key,source=binding,first_line=lo,last_line=hi,text=s))
        sources.append(dict(integrated_citation_key='exec25_javaiv_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][-4:]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[0],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    authenticate();write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=len(fragments)))
    write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_javaiv_search*.json'))+[RAW/'exec25_javaiv_scalation.json']:
        if 'receipt' in p.name:continue
        d=read(p);r=p.with_suffix('.receipt.json');q=read(r)
        for x in d['items']:leads.setdefault(x['full_name'],dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected'))
        queries.append(dict(query=q['url'],total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(r,'Query identity'),reliance='No absence or saturation; broad scalation search includes fuzzy unrelated results.'))
    for name in ['vilhomaa/kausaali','scalation/scalation2','aaiyer/SuanShu']:
        if name in leads:leads[name]['status']='selected_primary_anchors_only'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),additional_named_candidates=['cmu-phil/tetrad','lessthanoptimal/ejml','scalation/scalation2','aaiyer/SuanShu'],limits=ref(BASE/'external-route-limits.json','No usable server web/Maven content'),saturation_claim=False,absence_claim=False))
    caller_names=['exec25_javaiv_src_4','exec25_javaiv_src_5','exec25_javaiv_src_6','exec25_javaiv_call_0','exec25_javaiv_call_1','exec25_javaiv_call_2']
    callers=[dict(source=ref(RAW/(n+'.txt'),'Selected caller candidate'),matches=[i+1 for i,s in enumerate((RAW/(n+'.txt')).read_text().splitlines()) if 'Tsls' in s]) for n in caller_names]
    write(BASE/'caller-review.json',dict(scope='Selected files only; public Tsls construction/estimate directly inspected',files=callers,whole_repository_callers_complete=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Authenticated originals and exact anchors') for n in ['authenticated-originals.json','inspected-extracts.json','caller-review.json']],groups=5,anchors=len(fragments),native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Independent rational/indexing reference'),ref(BASE/'exact-results.json','Exact replay')],checks=['5x3 table distinguishes row and column; outside columns3/4 retained.','Latent coordinate scale4 changes coefficient2 to1/2.','Singular 2x2 determinant zero.','Mean ratios3/2 differs from ratio sums6/5.','Hypothetical costs30/40/60 retain all denominators.'],native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='External-IV and credit-score RD versus latent measurement coefficient',selected=['Tetrad latent Tsls and EJML','Kausaali instrumental placeholder','ScalaTion selected OLS','Historical SuanShu selected OLS'],decisions=['Tetrad conditional measurement-model reference pending source-path qualification.','Kausaali instrumental path deferred until actual implementation.','Do not equate selected OLS with generic IV/RD.','Consider matched R/Python worker candidates with all prior scientific and operating gates.'],limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Retained source notices')],findings=['Tetrad GPL and EJML Apache source notices retained.','Kausaali Apache metadata and original retained; Maven binary equivalence open.','ScalaTion root and HTML notices both retained.','Historical SuanShu mirror identity and source notices do not establish current vendor edition terms.'],integration_allowed=False))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=['Nonsquare case/variable mapping and missing values','Latent normalization and renamed indicators','Per-parameter fitted mask and skipped branches','Direct inverse, singular/near-singular matrices, nonfinite values and residuals','Complete public caller and installed dependency identities','Weak first stages and explicit weighted-moment operator','IV/RD target, observation clock, population and uncertainty serialization','All requested/returned/accepted counts, failure costs and reproducible environment'],owners=['Scientific author','Adapter owner','Environment/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded searches and tails')],known_routes=['Complete named original delegates and artifact provenance.','Preregister matched public native cases before expensive bank experiments.','Preserve missing implementation and unsupported-target refusals.'],unknown_universal_repairs=['Exclusion, continuity and bank assignment truth require information or restrictions.','No universal repair for unrestricted weak identification or dependence.'],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_javaiv_choice',kind='project_evidence_not_scholarly_paper',title='Authored Java/JVM IV and RD comparison, witnesses and qualification decision',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026;cutoff7 October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Shape,scale,numerical state,placeholder,targets and costs',inspection='Author inspection')],supported_claims=['Exact authored witnesses and bounded candidate decisions','Explicit incomplete coverage and proposed public qualification'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=6,new_scholarly_pdfs=0,evidence=[ref(BASE/'authenticated-originals.json','36 authenticated new originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed planned and actual evidence') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['Preserve four prior Tetrad originals and record36 new authentic files.','Five software collections and one authored comparison; no scholarly theorem imported.','Resolve selected data/init/inverse paths and distinguish actual placeholder from capability.','Serial canonical publication after Python IV/RD delivery.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking targets and substantive alternatives'),ref(BASE/'sponsor-addition.md','Investment decision')],findings=['Source predicates, authored witnesses and proposed native evidence separated.','Uncertainty methods are not claimed absent from whole library.','Maven and whole-ecosystem coverage remain open.'],visual_acceptance=False))
    names=['authenticated-originals.json','primary-review.json','comparison-review.json','mathematical-review.json','exact-results.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Reviewed bounded coverage') for n in names]+[ref(Path(__file__),'Review logic')],findings=['36 new originals and inherited Tetrad anchors authenticated.','Five source collections and one authored comparison preserve scientific and implementation limits.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=36,anchors=len(fragments),unique_leads=len(leads),new_records=6,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Selected Java/JVM candidates identified; Maven and generic-IV/RD search/delegate coverage incomplete.','Technical claims bind authentic dated bytes and exact inspected anchors; no new scholarly theorem.','Alternatives and concrete public qualification routes retain numerical,rights and native limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Java/JVM IV/RD source comparison and public qualification contracts',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Java IV/RD inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
