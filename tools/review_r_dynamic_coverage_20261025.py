#!/usr/bin/env python3
"""Authenticate pinned R originals and review bounded dynamic inference comparisons."""
import argparse,hashlib,json
from pathlib import Path
import r_dynamic_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/r-dynamic-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.dynamic_panel_timeseries.R'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected primary paths and bounded searches; uninspected candidates and complete ecosystem coverage remain open.',
 'No downloaded package or upstream test executed; authored exact witnesses are not native results.',
 'Calendar moments, structural restrictions and nonlinear perturbations have distinct targets and assumptions.',
 'Complete solver/dependency delegates, installed artifact equivalence and distribution rights remain unqualified.',
 'Instrument exclusion, stable shock mechanisms, calendar dependence and bank utility require information or restrictions.',
 'No scholarly theorem imported from source comments; visual, independent, bank and final acceptance remain open.']
NEXT='Inspect remaining R dynamic-panel and structural/nonlinear time-series candidates and delegates. Freeze artifacts and qualify complete calendar/formula/instrument paths, covariance units, optimizer custody, fractional tolerance transport, curvature, failed-resample counts and seeded history/shock experiments on public known-law fixtures before native admission.'
SPECS={
 'plm':('plm panel calendars, GMM instruments and covariance contracts','cran/plm','2.6-7;13 November 2025;d9b431acb4efefa0144c4e7eb55e963a5b83f629',[
 ('src_0',1,34,['2.6-7','GPL (>= 2)'],'Version, runtime and license declaration.'),
 ('src_1',339,359,['un.time','outer(un.id, un.time'],'Unbalanced preparation uses observed labels.'),
 ('src_1',378,396,['makegmm','xd <- diff(x)'],'Actual GMM matrix transformation uses adjacent differences.'),
 ('src_1',758,779,['range(g)','y - rg[2L]'],'Instrument selection uses extracted vector positions.'),
 ('dep_0',762,780,['shift == "time"','lagt.pseries','collapse::flag'],'Public time/row shift and optional fast delegate.'),
 ('dep_0',906,919,['as.numeric','match(x - ak, x'],'Time helper uses numeric offsets, with level fallback.'),
 ('src_1',538,575,['minevA1','1E-9','ginv(A1)','B1 <- solve','ginv(A2)'],'Weight fallback differs from coefficient solve.'),
 ('src_3',1197,1234,['min(abs(Re(eigen(A2)$values)))','vcovr1s','vcovr2s'],'Separate covariance inverse and two-step correction expression.')]),
 'vars':('vars structural likelihood, diagnostics and covariance units','cran/vars','1.6-1;21 March 2024;593f875399eaf4733fdcfe0ab294bf99fba84c7e',[
 ('src_0',1,20,['1.6-1','GPL (>= 2)'],'Version and license declaration.'),
 ('src_1',57,95,['log(det(Bmat)^2)','opt <- optim','opt$par'],'Direct objective and optimization result.'),
 ('src_1',203,220,['Convergence not achieved','break','opt <- NULL'],'Scoring warns at iteration limit and continues.'),
 ('src_1',230,280,['Normalize sign','Sigma.U = Sigma.U * 100','opt = opt'],'Sign convention, output covariance scaling and diagnostic custody.'),
 ('src_3',1,17,['P <- t(chol(sigma.u))','Phi[, , i] %*% P'],'Ordinary orthogonalization uses Cholesky.')]),
 'svars':('svars volatility restrictions, native tolerance and resampling diagnostics','cran/svars','1.3.12;24 August 2025;6fa6b8536a6c3a53b0f0c0beaf43c7659bf1e2a5',[
 ('src_0',1,28,['1.3.12','MIT + file LICENSE','RcppArmadillo'],'Version, declared rights and native dependencies.'),
 ('dep_0',1,3,['2018','COPYRIGHT HOLDER'],'Named original MIT holder notice.'),
 ('src_2',120,139,['crit = 0.001','unrestricted VARs only','get_restriction_matrix'],'Input VAR restrictions differ from impact restrictions.'),
 ('src_2',279,292,['IdentifyVolatility(crit = crit','maxIter = max.iter'],'Public route passes declared tolerance to native routine.'),
 ('bridge',90,114,['input_parameter< int >::type crit','Rcpp::wrap(IdentifyVolatility'],'Registered bridge has integer tolerance type.'),
 ('dep_2',59,79,['stats["nlm"]','iterlim','150'],'Inner optimizer limit and returned object.'),
 ('dep_2',109,145,['int crit','while (Exit > crit && count < maxIter)'],'Native outer stopping predicate uses integer tolerance.'),
 ('dep_2',214,248,['HESS = HESS.i()','HESS.col(i) = HESS.col(i) * (-1)','Named("iteration")'],'Column alteration and selected return lack full inner convergence object.'),
 ('dep_3',41,58,['maxL <- nlm','HESS <- solve','HESS[,i] <- -HESS[,i]'],'Non-Gaussian path also changes inverse-Hessian columns.'),
 ('src_4',132,161,['blocks <- array','runif','1:nboot'],'Overlapping residual blocks and requested replications.'),
 ('src_4',197,223,['tryCatch(id.cv_boot','error = function(e) NULL','id.ngml_boot'],'Method-specific bootstrap error handling differs.'),
 ('src_4',260,314,['return(NA)','delnull','length(bootstraps)','cov(v.b)'],'Failed results removed before survivor covariance summary.')]),
 'panelvar':('panelvar observed-period grid, transformations and numerical delegates','cran/panelvar','0.5.6;25 November 2024;5e7b205f8ceb5d49b6dcaed902d1d6170f310f71',[
 ('src_0',1,26,['0.5.6','GPL (>= 2)'],'Version and license declaration.'),
 ('src_1',167,213,['sort(unique','expand.grid','factor(Set_Vars$period)','panel_lag'],'Observed-period grid feeds positional helper.'),
 ('dep_0',4,28,['x[1:(nrow(x) - 1), -1]','res[rep(is.na'],'Actual row lag and missing-value mask.'),
 ('dep_0',64,98,['mean(x[-(1:t)], na.rm','apply(x[, -(1:2)], 2, diff)','helmert'],'Future-available mean and adjacent difference transformations.'),
 ('src_1',839,854,['min(abs(eigen(sum_Lambda)$values)) < tol','MASS::ginv(as.matrix(sum_Lambda_vec))','inv.Phi_firststep'],'Tolerance predicate and selected ginv calls are separate.'),
 ('src_1',1005,1013,['var_first_step <- solve','%*% solve'],'Variance path still contains direct solves.')]),
 'tsdyn':('tsDyn history-conditioned shock definitions and simulation law','cran/tsDyn','11.0.5.2;31 October 2024;db7f30e39a7fbc878823912aedc805772bd2ae06',[
 ('src_0',1,23,['11.0.5.2','GPL (>= 2)'],'Version and license declaration.'),
 ('src_1',60,69,['shock_both = TRUE','seed = NULL'],'Low-level helper also defaults to additive shocks.'),
 ('src_1',97,144,['replace = FALSE','innov_1 <- rbind(shock_M','if(shock_both)','sim_2 <- model.gen'],'Residual sampling, shock replacement/addition and paired simulation.'),
 ('src_1',170,186,['if(!is.null(seed)) set.seed(seed)','out <- replicate(R','shock_both  =shock_both'],'Seed set once by averaging helper; not forwarded to low-level replicate.'),
 ('src_1',225,261,['size = n.hist, replace = FALSE','size = n.shock, replace = FALSE','expand.grid','R = R, seed = seed'],'Public history/shock combinations each pass seed to averaging helper.'),
 ('dep_0',30,41,['TVAR.gen','starting=starting, innov = innov'],'Concrete TVAR simulation delegate.'),
 ('dep_1',70,110,['Yb[1:p,] <- as.matrix(starting)','innov','round(z2[i-thDelay]','round(Yb[i,]'],'Starting values, supplied innovations and threshold rounding.')])}

def authenticate():
    rows=[];evidence=[]
    for name in ['source-selection.json','delegate-selection.json','bridge-selection.json']:
        rows.extend(read(BASE/name));evidence.append(ref(BASE/name,'Pinned selected file identities'))
    assert len(rows)==35
    originals=[]
    for x in rows:
        p=RAW/(x['id']+'.txt');data=p.read_bytes();receipt=p.with_suffix('.receipt.json');r=read(receipt)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['git_blob']
        assert len(data)==x['bytes'] and core.sha(p)==r['sha256'] and r['status']=='saved'
        originals.append(dict(repository_path=x['path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(receipt,'URL,date,hash')))
    for key in SPECS:
        c=read(RAW/f'exec25_rdyn_{key}_commit.json');c=c[0] if isinstance(c,list) else c
        assert c['sha']==SPECS[key][2].split(';')[-1] and c['commit']['committer']['date'][:10]<='2026-10-07'
        tree=read(RAW/f'exec25_rdyn_{key}_tree.json');assert tree['truncated'] is False
        evidence.extend([ref(RAW/f'exec25_rdyn_{key}_{kind}.json','Dated pin and complete selected tree') for kind in ['commit','tree']])
    write(BASE/'authenticated-originals.json',dict(status='pass',count=35,originals=originals,evidence=evidence))

def prepare():
    assert not (BASE/'review.json').exists()
    authenticate();fragments=[];sources=[]
    for key,(title,repo,version,checks) in SPECS.items():
        evidence=[ref(RAW/f'exec25_rdyn_{key}_commit.json','Revision and date')];anchors=[];claims=[]
        for suffix,lo,hi,tokens,finding in checks:
            p=RAW/f'exec25_rdyn_{key}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));s='\n'.join(lines[lo-1:hi]);assert all(t in s for t in tokens),(p.name,lo,hi,[t for t in tokens if t not in s])
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=key,source=binding,first_line=lo,last_line=hi,text=s))
        sources.append(dict(integrated_citation_key='exec25_rdyn_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][-4:]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=len(fragments)))
    write(BASE/'exact-results.json',exact.calculate());queries=[];leads={}
    for p in sorted(RAW.glob('exec25_rdyn_search*.json')):
        if 'receipt' in p.name:continue
        d=read(p);receipt=p.with_suffix('.receipt.json')
        for x in d['items']:leads.setdefault(x['full_name'],dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected'))
        queries.append(dict(query=read(receipt)['url'],total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(receipt,'Query identity')))
    for repo in [x[1] for x in SPECS.values()]:
        if repo in leads:leads[repo]['status']='selected_primary_anchors_only'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),additional_named_candidates=[x[1] for x in SPECS.values()],saturation_claim=False,absence_claim=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Original identities and exact anchors') for n in ['authenticated-originals.json','inspected-extracts.json','prebinding-source-correction.json']],groups=5,anchors=len(fragments),native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Exact rational/indexing witnesses'),ref(BASE/'exact-results.json','Replay')],checks=['Global missing periods differ from adjacent rows.','Fractional tolerance and a stipulated integer surrogate give different stopping decisions.','Column flips can destroy covariance symmetry.','Proportional volatility regimes retain rotation ambiguity.','Replacement/addition and threshold histories yield different contrasts.','Costs30/45/60 retain all denominators.'],native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Branch dynamic intervention, aggregate structural funding shock and nonlinear residual perturbation',selected=list(SPECS),decisions=['Conditional plm/panelvar references need complete calendar and moment contracts.','Conditional vars reference needs optimizer, covariance unit and restriction custody.','Defer svars admission until bridge,curvature,identification and resample behavior qualify.','Use tsDyn only for declared histories and perturbation law; no automatic causal identification.'],limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Declarations and named holder notice')],findings=['Four selected packages declare GPL>=2; svars declares MIT plus its retained named holder file.','Rcpp,Armadillo,MASS,collapse and other installed dependencies remain separately unqualified.','No complete distribution, port or binary-equivalence decision.'],integration_allowed=False))
    tests=['Calendar gaps,duplicate rows,time formats,formula transformations and realized moment rows','Instrument validity,strength,proliferation and shared calendar dependence','Structural restrictions,volatility separation and break selection','Fractional tolerance bridge and nested optimizer convergence custody','Curvature symmetry,sign normalization,covariance units and numerical fallbacks','Bootstrap attempts,failures,survivors,block length and alignment','Seed ownership,history/shock weighting,threshold rounding and additive/replacement semantics','Known-law uncertainty and complete request/cost denominators']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,owners=['Scientific author','Adapter owner','Artifact/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded search and tails')],known_routes=['Complete primary delegates and installed artifact provenance.','Freeze public known-law contracts before native experiments.'],unknown_universal_repairs=['Unknown exclusion and shock stability require information or justified restrictions.','No universal latent-identification or arbitrary-dependence repair is promised.'],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_rdyn_choice',kind='project_evidence_not_scholarly_paper',title='Authored R dynamic panel and structural shock comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026;cutoff7 October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored exact witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Calendar,structural ambiguity,curvature,shock semantics and costs',inspection='Author inspection')],supported_claims=['Exact authored witnesses and conditional candidate decisions','Bounded search and proposed public qualification'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=6,new_scholarly_pdfs=0,evidence=[ref(BASE/'authenticated-originals.json','35 authenticated originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed planned and actual evidence') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['35 authentic originals, five collections and one authored comparison.','Corrected unbound seed/default interpretation before claims were bound.','Separate source review from native and scientific qualification.','Serial canonical publication after Python dynamic delivery.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking targets and substantive alternatives'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Explained model,exact examples and distinct reuse alternatives.','Source predicates,authored calculations and proposed tests separated.','Open coverage,rights,native and final acceptance retained.'],visual_acceptance=False))
    names=['authenticated-originals.json','primary-review.json','mathematical-review.json','comparison-review.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Reviewed bounded comparison') for n in names]+[ref(Path(__file__),'Review logic')],findings=['35 authentic files and exact anchors retain source/native distinction.','Calendar,structural,curvature,resampling and simulation contracts explicit.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=35,anchors=len(fragments),unique_leads=len(leads),new_records=6,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Selected R candidates identified; search,delegate and native coverage incomplete.','Claims bind authentic dated bytes and exact anchors; no scholarly theorem imported.','Alternatives and public qualification routes retain numerical,rights and native limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='R dynamic-panel and structural/nonlinear time-series source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('R dynamic inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
