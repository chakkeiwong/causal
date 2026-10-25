#!/usr/bin/env python3
"""Authenticate remaining-language source comparisons; execute only the authored exact reference."""
import argparse,hashlib,json
from pathlib import Path
import other_mediation_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as fresh_write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/other-mediation-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.mediation_sensitivity.other_relevant'
read=lambda p:json.loads(p.read_text())
def write(p,value):
    if p.exists():assert read(p)==value,'Existing evidence differs: '+str(p)
    else:fresh_write(p,value)
LIMITS=['Four bounded queries retain irrelevant,uninspected and unreturned candidates;no saturation or absence claim.','55authentic originals across six groups;no downloaded code executed.','Static findings and authored exact-law witnesses are not native failure rates.','Complete runtime,learner,parser,rights and law-specific uncertainty qualification remain open.','Package/coded scholarly references are discovery only until genuine PDFs and technical anchors are retained.','No visual,independent,bank or final acceptance;Q1/Q5 and mandatory repairs remain open.']
NEXT='Complete remaining-language candidate and primary-paper routes;qualify CANlab resample acceptance,CI probability and cluster laws,Julia covariance/index/runtime contracts,Gaussian joint mediator law and policy influence derivations,and Stata external learner/survey/failure contracts with public fixtures and full rights/costs.'
DECISIONS=['CANlab:conditional path/equation reuse;defer direct adapter pending resampling,CI,dependence and toolbox/runtime rights.','Paramed.jl:defer direct admission;repair covariance permutation,tail calculation and runtime schema before any port.','Mediation.jl:defer bootstrap admission until index use and uncertainty target are qualified;rights unresolved.','CausalMediation.jl:conditional typed-interface reuse;qualify each effect/treatment-support and joint-law combination separately.','CausalTargeted.jl:compatibility facade to same mediator engine;do not count as independent estimator.','Stata cmed:conditional equation comparison;qualify exact estimator,external learner,survey and runtime/source rights.']
ANCHORS={
 'canlab':[
 ('02',201,215,'fast_ols_ab','Fast-path dispatch and weighted second-level helper.'),
 ('02',270,290,'nanremove','Joint current-variable missing-row removal changes analysis population.'),
 ('02',355,432,'bootbca_ci(0.25','First-level bootstrap branch;alpha.025 without covariates versus.25 with covariates;built-in alternative commented.'),
 ('02',1569,1620,'inv(xx','Fast normal-equation path regressions and coefficient product.'),
 ('03',24,60,'maxiter = 500','Clock reseed,constant-predictor rejection,replacement and capped attempts.'),
 ('05',49,105,'jackknife','BCa bias/acceleration and percentile diagonal extraction.'),
 ('20',49,103,'Robust multi-level not implemented','Explicit unsupported regression combinations.'),
 ('02',785,835,'whgood','Between-subject bootstrap and missing-subject filtering.')],
 'paramed':[
 ('01',1,30,'port','Declared Stata parametric mediation port and contrast interface.'),
 ('02',1,21,'Expat','MIT source license;runtime/transitive rights separate.'),
 ('03',9,24,'vcov2 = vcov','In-place alias permutation overwrites input covariance.'),
 ('03',29,78,'Stella.formula','Typed logfile default,formula construction and selected outcome-family dispatch.'),
 ('03',90,122,'sigma =','At-mean covariates and block-diagonal covariance combination.'),
 ('03',234,245,'ptwoside','Signed statistic used without absolute value in selected two-sided tail.')],
 'mediationjl':[
 ('01',1,4,'version','Selected Julia package identity;dependency completeness remains open.'),
 ('04',25,46,'cholesky','Asymptotic parameter covariance factor and normal perturbation.'),
 ('04',48,63,'pt.x[ii','Sampled ix not used in deterministic parameter refit.'),
 ('04',86,166,'genrand','Normal,binomial,Poisson prediction simulation distinct from parameter bootstrap.'),
 ('04',198,285,'yy[ii, 1]','Separate model draws,counterfactual values,observed-outcome substitution and simulation intervals.')],
 'causalmediation':[
 ('01',1,21,'MIT License','Selected MIT declaration.'),
 ('07',185,198,'Natural effects require empty moc','Natural-effect admissibility refusal for declared intermediate confounding.'),
 ('07',272,333,'require::Bool = false','Relation declarations checked only when supplied or required;no inference of causal truth.'),
 ('08',21,46,'semantic_fingerprint','Certificate bridge conditionally requires edge kinds and merges selected fields.'),
 ('09',37,95,'n_mc <= 1','Mean substitution at low MonteCarlo count and independent Gaussian mediator residuals otherwise.'),
 ('09',98,139,'moc','Intermediate-confounder nested Gaussian branch.'),
 ('20',40,59,'resid_m','Displayed uncentred influence helper terms.'),
 ('20',61,88,'r[i] *= clamp','Per-coordinate Gaussian ratios truncated then multiplied.'),
 ('05',142,175,'trunc = 10.0','Binary propensity and continuous policy weight construction and truncation.'),
 ('05',207,238,'zeros_h','Continuous branch omits mediator-residual contribution;separate derivation required.'),
 ('10',10,43,'_interventional_effects','Natural helper delegates with empty intermediate-confounder list.'),
 ('21',63,96,'sqrt(n)','Unweighted row-standard-error summary and separate weighted delegate.'),
 ('06',1,40,'factor recode','Separate categorical-treatment implementation remains distinct.')],
 'targeted':[
 ('01',1,21,'MIT License','Selected MIT declaration.'),
 ('04',1,39,'Base.get_extension','Mediation facade resolves extension or errors;delegates same implementation.'),
 ('20',1,70,'CausalMediation','Extension calls CausalMediation delegates;not independent capability.')],
 'cmedstata':[
 ('03',1,65,'cmed','Common interface advertises separate method families;not proof of all delegates.'),
 ('04',25,88,'bootstrap','Linear wrapper delegates bootstrap,parallel and survey paths.'),
 ('05',76,149,'nie_summand','Linear effect decomposition multiplies contrast once;interaction branch retained.'),
 ('07',30,119,'sampwts','Stabilized weighting,optional percentile clipping,sample weights and mean decomposition.'),
 ('11',30,110,'mr1forest','Selected learner/type validation,binary restrictions and external delegate dispatch.')]
}
def prepare():
    assert not (BASE/'review.json').exists()
    rows=read(BASE/'selected-originals-final.json');assert len(rows)==55
    pins={x['key']:x for x in read(BASE/'pins.json')};originals=[];identities=[]
    for g,pin in pins.items():
        cp=RAW/f'exec25_omed_{g}_commit.json';tp=RAW/f'exec25_omed_{g}_tree.json'
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        assert read(cp)[0]['sha']==pin['commit'] and pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha']==pin['commit'] and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned identity'),ref(tp,'Complete selected tree')])
        for row in [x for x in rows if x['group']==g]:
            p=ROOT/row['local_path'];rp=ROOT/row['receipt'];r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p) and r['url']==row['url']
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['git_blob']==blobs[row['upstream_path']]
            originals.append(dict(group=g,upstream_path=row['upstream_path'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'Bound receipt'),git_blob=row['git_blob']))
    verify_bindings(read(BASE/'authenticated-originals-final.json'));assert len(originals)==read(BASE/'authenticated-originals-final.json')['count']==55
    sources=[];fragments=[]
    for g,checks in ANCHORS.items():
        pin=pins[g];evidence=[ref(RAW/f'exec25_omed_{g}_commit.json','Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_omed_{g}_src{suffix}.txt';lines=p.read_text().splitlines();excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(g,suffix,lo,token)
            binding=ref(p,f'Lines{lo}-{min(hi,len(lines))}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,min(hi,len(lines))]],finding=finding));claims.append(finding);fragments.append(dict(group=g,source=binding,first_line=lo,last_line=min(hi,len(lines)),text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_omed_'+g,kind='software',title=g+' pinned remaining-language mediation and inference contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['commit'],version_date=pin['date']+';'+pin['commit'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));assert exact.calculate()==read(BASE/'exact-results.json')
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_omed_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==4
    for pin in pins.values():
        if pin['repository'] in leads:leads[pin['repository']]['status']='selected_primary_anchors'
    if 'belayb/BayesGmed' in leads:leads['belayb/BayesGmed']['status']='earlier_R_component_review_preserved'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals-final.json','Selected original declarations')],findings=['Paramed,CausalMediation and CausalTargeted selected MIT declarations.','CANlab has a geometry subcomponent license-named file;no toolbox-wide license inferred.','Mediation.jl and cmed selected complete trees lack license-named files;rights unresolved.','MATLAB/Stata runtime entitlement and complete dependencies are separate from source availability.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored exact finite arithmetic'),ref(BASE/'exact-results.json','Replayed exact laws'),ref(BASE/'inspected-extracts.json','Selected delegate chains')],findings=['Unused bootstrap index gives zero deterministic parameter-resampling variance versus1/2 in exact two-row mean oracle.','Aliased covariance permutation turns positive-definite determinant500 into singular matrix.','Signed normal tail at-1 exceeds1;absolute-value reference is approximately.317.','Constant-predictor bootstrap rejection changes sampling law;CI alpha.25 versus.025 differs.','Nonlinear mean substitution and independent mediator residuals change exact target1or1/2to0.','Coordinate caps multiply to125 for3mediators;exposure factor10 permits1250.','Linear contrast0to2gives direct6,indirect16,total22;hypothetical omitted half-unit worthUSD50000.'],native_execution=False))
    tests=['Freeze effect family,contrast,units,target population,mediator joint law and sampling design.','Verify covariance permutation and unchanged linear-combination variance.','Verify bootstrap indices actually reach each fit;keep parameter and predictive randomness distinct.','Report all rejected/replaced/failed resamples and capture exact indices and seeds.','Test confidence-level branches,BCa degeneracies and signed two-sided tails.','Qualify joint Gaussian and nonlinear mediator integration under exact known laws.','Derive the exact policy influence function and retain sampling dependence and MonteCarlo error.','Measure joint weights,positivity,clipping and complete effective sample sizes.','Qualify named Stata learner,bootstrap,survey and estimation-sample semantics.','Resolve source/runtime/dependency rights before distribution.','Replay common typed CLI/MCP requests and retain all failure and full-cost records.']
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='remaining-language mediation computation,translation and sensitivity qualification',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Proposal implementation owner to be appointed for native trials',tests=tests,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Explicit query tail'),ref(BASE/'dependency-license-review.json','Unresolved complete rights')],known_routes=tests,uninspected=['Unreturned MATLAB/other-language search pages and uninspected Julia,Stata,MATLAB and other candidates.','External CANlab helpers,Stata learners,CausalDynamics and weighted-influence delegates remain separate qualification.','Scholarly references mentioned in package metadata remain unadmitted without genuine original PDFs.'],unknown_universal_repairs=['Numerical solves do not identify unrestricted hidden causal assignment or mediation truth.','Arbitrary dependent-data mediation uncertainty needs justified assumptions and theory.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed source comparison') for n in ['authenticated-originals-final.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','mathematical-review.json','comparison-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_omed_choice',kind='project_evidence_not_scholarly_paper',title='Authored remaining-language mediation translation and numerical qualification comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence,inspected_anchors=[dict(anchor='Source choices and exact public qualification',inspection='Author inspection')],supported_claims=['55authentic originals,six component roles and exact authored arithmetic.','Conditional adoption,port,defer and reject decisions with scientific and artifact limits.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=7,new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Six component roles compared;none admitted as complete mediation product.','Declared public fixtures precede expensive bank trials.','Keep successful source work separate from incomplete coverage and native qualification.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Bank decision through effect contracts,resampling,covariance,nested mediator laws,rights and economic consequence.','Conditional source findings do not assert native failures or universal causal identification.','Distinct treatment families,continuous delegates and facade boundaries explicitly retained.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=55,scholarly_originals=0,limitations=LIMITS,native_execution=False);verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(review='pass_for_selected_work',originals=55,anchors=len(fragments),new_records=7,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Six component roles inspected;bounded search and native coverage remain incomplete.','Pinned authentic originals and exact authored witnesses support claims;no scholarly metadata admitted as technical paper evidence.','Conditional adoption,port,defer and reject routes retain scientific,rights,artifact and acceptance conditions.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='remaining-language mediation computation and translation source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('remaining-language coverage receipt prepared.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
