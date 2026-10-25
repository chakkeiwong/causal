#!/usr/bin/env python3
"""Review pinned Python mediation originals; never execute their code."""
import argparse, hashlib, json
from pathlib import Path
import python_mediation_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/python-mediation-coverage-v1';RAW=ROOT/'docs/literature/raw'
OP='SW.CELL.mediation_sensitivity.Python';read=lambda p:json.loads(p.read_text())
LIMITS=['Bounded repository queries and selected delegates; unreturned and uninspected tails remain, with no absence or exhaustive-coverage claim.',
'No acquired software, model checkpoint or native package executed; static findings and authored exact witnesses are not native failure-rate measurements.',
'Three genuine versioned author papers; publisher editions and selected source dates remain distinct.',
'Neural optimization, dependent uncertainty, complete delegate inspection, installed artifacts and dependency rights require separate qualification.',
'No fresh visual, independent or final acceptance; no bank adoption or general identification.']
NEXT='Complete Python search tails and negative-control/path-specific delegates; reconcile contrast scales, joint resampling, finite-support mass and quadrature boundaries, neural diagnostic signatures and license scope; qualify frozen public known-law fixtures with complete failures, costs and refusal oracles.'
DECISIONS=[
'statsmodels: conditional potential-outcome reference; enforce binary contrast or explicit recoding, rebuilt interactions, joint covariance justification and typed zero-total/sign-tail results.',
'Pingouin: conditional linear-path comparator; reject unqualified causal outcome interpretation of logistic mediator coefficient products and complete-case selection.',
'DoWhy: conditional graph/estimator orchestrator; reject unqualified multiplication of two nonunit contrasts; bind sensitivity parameters to their exact estimands and scales.',
'PyProcessMacro: conditional serial/moderated path comparator; adopt shared-resample and failed-fit accounting ideas, not automatic nonlinear causal semantics.',
'SharpCausalSensitivity: mathematical recursion reference; defer selected implementation pending equality and fractional-boundary reconciliation, supported outcome contracts and rights.',
'NeuralCSA: method candidate; require observational-fit, feasibility and optimization-gap qualification, fix diagnostic signature mismatch and resolve artifact rights.',
'Overcast: conditional continuous-dose sensitivity candidate; a sorted-integration port is proposed only after tie, centering, endpoint and numerical parity tests.',
'No package receives native capability admission or blanket license clearance from this source review.']
ANCHORS={
'statsmodels':[
('03',240,306,'from_formula','Formula interventions rebuild design matrices; matrix route directly changes selected columns.'),
('03',308,378,'rng.integers','Separate bootstrap index generation for the two fits; prefix validation versus exact parametric dispatch.'),
('03',380,418,'for tm in 0, 1','Fixed zero/one contrasts and reuse of mediator realization across outcome exposures.'),
('03',422,469,'prop_med_ctrl','Strict-sign tail arithmetic and unguarded total-effect ratios.')],
'pingouin':[
('03',970,988,'return beta_m * beta_y','Logistic or linear mediator coefficient multiplied by full-model outcome coefficient.'),
('03',991,1040,'does not correct for skewness','Bias-corrected not accelerated interval; explicit zero-estimate sign-tail branch.'),
('03',1219,1249,'dropna','Numeric checks,complete-case deletion and binary mediator detection.'),
('03',1258,1306,'idx[i, :]','Displayed mediator-outcome path differs from full outcome fit; bootstrap shares row indices.')],
'dowhy':[
('04',91,163,'DEFAULT_FIRST_STAGE_MODEL','Stage defaults and separate mediation adjustment sets.'),
('04',187,219,'Only singleton mediator','One-dimensional treatment and singleton mediator restriction.'),
('04',263,309,'natural_indirect_effect =','Same control/treatment forwarded to both stages; product then total subtraction.'),
('12',125,160,'self._do(treatment_value','Regression stage returns an intervention contrast,not merely a slope.'),
('10',409,449,'identify_mediation','Mediation construction and separate stage-confounder searches.'),
('10',944,1016,'return sorted','Directed-path mediator selection and adjustment-set delegates;no automatic truth verification.'),
('06',175,210,'bias_factor','Linear sensitivity uses partial R-squared strengths and finite-degree uncertainty.'),
('07',153,210,'Calpha2','Partial-linear bound and score-variance quantities need independent qualification.'),
('09',96,124,'< 0.15','E-value dispatch by family/link with observed rare-outcome threshold.'),
('09',372,392,'_or_to_rr','OR conversion is distinct from direct risk-ratio sensitivity.')],
'process':[
('07',54,93,'n_fail','Shared resampled rows; retain successful fits with failure counter and cap.'),
('07',114,130,'ConvergenceError','Singularity and convergence failures mark rejected fits.'),
('07',193,240,'Saturated fits','Separation check and matched multi-equation resampling.'),
('08',135,169,'Product of the coefficients','Serial path coefficient products and percentile/bias-corrected intervals.')],
'neuralcsa':[
('06',43,50,'xi_sampled','Abstract sensitivity method requires mixture sample.'),
('06',58,104,'lagrangian','Sampled latent sensitivity constraints and multiplier/penalty updates.'),
('06',129,151,'get_sensitivity_violation(data_test.data, u_sampled)','Public sensitivity helper omits required mixture-sample argument.'),
('06',202,215,'xi_sampled','Unconditional subclass preserves three-argument sensitivity signature.'),
('06',290,305,'xi_sampled','Conditional subclass also requires mixture sample.'),
('03',368,405,'Rosenbaum continuous not implemented','Sampled extrema;continuous Rosenbaum branch explicitly unsupported.'),
('03',420,450,'ratio_msm','Distinct binary odds and continuous density-ratio sensitivity calculations.')],
'sharp':[
('07',9,55,'s_minus','Binary,continuous and weighted sensitivity formulas.'),
('06',151,175,'torch.isnan','Quantile threshold construction and mediator state enumeration.'),
('06',209,241,'y_cum.gather','Inclusive cumulative index and fixed-array normalization witness.'),
('06',244,264,'raise NotImplementedError','Selected discrete/binary outcome path not implemented.'),
('06',269,324,'F_plus > c_plus','Discrete threshold equality omission;normalization assertion protects output.'),
('06',331,366,'reversed','Backward mediator recursion using sorted outcome bounds.'),
('05',19,68,'torch.quantile','Resampled ensemble percentile endpoints;not a universal coverage guarantee.')],
'overcast':[
('02',1,40,'2204.10022','Repository paper citation differs from retained v1 title/author identity.'),
('05',695,765,'log_lambda','Continuous-dose log sensitivity,epsilon and quadratic pairwise arrays.'),
('01',1,26,'Apache License','Selected Apache2 license text;dependency clearance remains separate.')]
}
PAPER_ANCHORS={
'neural':[(3,3,'Independent observations,consistency,positivity,latent unconfoundedness and static causal query.'),(5,7,'Transformation invariance;exact observational push-forward and distribution-space sufficiency theorem;neural instantiation is an approximation.')],
'sharp':[(3,4,'Discrete ordered mediators,causal graph and exclusion of mediator-outcome hidden confounding for path semantics.'),(5,7,'Density-ratio restrictions,weighted formulas,sharpness conditions and explicit longitudinal sharpness limit.')],
'overcast':[(3,4,'Continuous density ratios,endpoint limit,conditional density and mean consistency plus positivity.'),(5,5,'Monte Carlo threshold optimization and bootstrap endpoint proposal.')]
}

def prepare():
    assert not (BASE/'review.json').exists()
    pins={x['key']:x for x in read(BASE/'pins.json')};rows=read(BASE/'selected-originals.json');assert len(rows)==60
    originals=[];identities=[]
    for group,pin in pins.items():
        cp=RAW/('exec25_pymed_'+group+'_commit.json');tp=RAW/('exec25_pymed_'+group+'_tree.json')
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        assert read(cp)[0]['sha']==pin['commit'] and pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha']==pin['commit'] and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned revision/date'),ref(tp,'Complete selected tree')])
        for row in [x for x in rows if x['group']==group]:
            p=ROOT/row['local_path'];r=read(ROOT/row['receipt']);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p) and r['url']==row['url']
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['git_blob']==blobs[row['upstream_path']]
            originals.append(dict(group=group,upstream_path=row['upstream_path'],git_blob=row['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(ROOT/row['receipt'],'Bound retrieval')))
    write(BASE/'authenticated-originals-final.json',dict(status='pass',count=60,originals=originals,evidence=identities))
    sources=[];fragments=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[ref(RAW/('exec25_pymed_'+group+'_commit.json'),'Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/('exec25_pymed_'+group+'_src'+suffix+'.txt');lines=p.read_text().splitlines();excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,lo,token)
            binding=ref(p,'Lines{}-{}:{}'.format(lo,min(hi,len(lines)),finding));evidence.append(binding)
            anchors.append(dict(path=binding['path'],line_spans=[[lo,min(hi,len(lines))]],finding=finding));claims.append(finding)
            fragments.append(dict(group=group,source=binding,first_line=lo,last_line=min(hi,len(lines)),text=excerpt))
        for row in [x for x in rows if x['group']==group and any(t in x['upstream_path'].lower() for t in ['license','pyproject','requirements','environment','setup.py'])]:evidence.append(ref(ROOT/row['local_path'],'Selected rights/dependency declaration;not complete clearance'))
        sources.append(dict(integrated_citation_key='exec25_pymed_'+group,kind='software',title=group+' pinned Python mediation and sensitivity source review',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['commit'],version_date=pin['date']+';'+pin['commit'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=len(fragments)))
    for p in read(BASE/'paper-identities.json'):
        pp=ROOT/p['local_path'];assert core.sha(pp)==p['sha256'];pages=(ROOT/p['text_path']).read_text().split(chr(12));anchors=[]
        for lo,hi,claim in PAPER_ANCHORS[p['tag']]:
            excerpt=chr(12).join(pages[lo-1:hi]);assert len(excerpt)>200
            anchors.append(dict(physical_pages=list(range(lo,hi+1)),anchor='Physical pages{}-{}'.format(lo,hi),text_extract=ref(ROOT/p['text_path'],'Genuine PDF text'),excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest(),finding=claim))
        s={k:p[k] for k in ['title','filename_title','first_author','author','year','source_identity','version_date','local_path','sha256']}
        s.update(integrated_citation_key='exec25_pymed_'+p['tag']+'_paper',kind='paper',local_copy=ref(pp,'Genuine primary preprint'),identity_evidence=[ref(ROOT/p['identity_path'],'Primary identity'),ref(ROOT/p['retrieval_path'],'PDF retrieval')],inspected_anchors=anchors,supported_claims=[x['finding'] for x in anchors],limitations=LIMITS+p['limitations']);sources.append(s)
    write(BASE/'paper-review.json',dict(status='pass_for_selected_primary_anchors',papers=[x for x in sources if x['kind']=='paper'],all_theorems_independently_verified=False,limitations=LIMITS))
    write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_pymed_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only'),receipt=ref(p.with_suffix('.receipt.json'),'Identity'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==4
    for pin in pins.values():
        if pin['repository'] in leads:leads[pin['repository']]['status']='selected_primary_anchors'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),saturation_claim=False,absence_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals-final.json','Authentic declarations and trees')],findings=['Selected statsmodels BSD-style,DoWhy and PyProcessMacro MIT,Pingouin GPL3,Overcast Apache2 declarations.','No license-named file in selected complete NeuralCSA or SharpCausalSensitivity trees;rights unresolved,not inferred from public access.','Installed artifacts,complete dependencies and usage-specific rights require separate review.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Independent reference'),ref(BASE/'exact-results.json','Exact replay'),ref(BASE/'paper-review.json','Primary assumptions'),ref(BASE/'inspected-extracts.json','Static source paths')],findings=['Binary mediator effect2 versus mixed-scale4log9.','Paired versus independent perturbations differ in product mean and sum variance;no universal invalidity claim.','Nonunit linear contrast intended indirect16,direct6;selected two-contrast product32,residual-10.','Strict-sign tail on four zeros returns0;statistical validity is not thereby established.','Discrete equality mass3/4 and constant-sample quadrature7/8 versus5/4 are exact expression witnesses,not native failure rates.','Neural sample feasibility and optimizer extremality are separate obligations.','Pairwise tensor storage and hypothetical net interval[-30000,30000] reproduce.'],native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Python mediation targets,resampling and sensitivity bound contracts',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    tests=['Freeze causal graph,clock,target population,intervention contrast,outcome scale and missingness policy.','Enumerate nested means,interactions,binary mediators and nonunit treatment contrasts.','Compare shared versus separate resampling,complete failed-fit denominators,zero totals and exact sign ties.','Enumerate discrete probability masses at equality boundaries and analytic/finite-support quadrature oracles.','Separate density fit,latent feasibility,optimization gap,integration error and sampling uncertainty.','Test helper signatures,unsupported outcomes,sensitivity domains and artifact rights.','Evaluate dependent customer/calendar laws separately;retain refusals and full costs.','Use public known-law fixtures before expensive authentic bank experiments.']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,independent_branches=True,native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Explicit search tails'),ref(BASE/'identity-omissions.json','Failed repository identity'),ref(BASE/'dependency-license-review.json','Rights limits')],known_routes=tests,unavailable_sources=['Named PySensemakr repository404;no absence claim.','Crossref sharp-title request failed;distinct genuine arXiv original obtained.','Selected final publisher editions not acquired;versioned author originals retained.'],uninspected=['Negative-control candidates,search tails and general path-specific delegates.','Complete sensitivity learner delegates and installed packages.'],unknown_universal_repairs=['Unobserved assignment and mediator-outcome truth cannot be inferred from package output.','Arbitrary dependent sampling and unrestricted hidden-state identification need additional assumptions or information.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals-final.json','paper-review.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','mathematical-review.json','comparison-review.json']]
    sources.append(dict(integrated_citation_key='exec25_pymed_choice',kind='project_evidence_not_scholarly_paper',title='Authored Python mediation target,resampling and sensitivity qualification comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence,inspected_anchors=[dict(anchor='Selected comparison and public qualification',inspection='Author inspection')],supported_claims=['60authenticated software originals and three genuine primary papers.','Explicit conditional integration,port,defer and reject decisions with scientific,numerical,rights and cost qualifications.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=11,new_scholarly_pdfs=3,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Seven concrete source comparisons,three genuine papers and exact independent witnesses.','Distinct causal targets and model restrictions;no broad inherited package admission.','Search,native,rights,visual and final gates remain open;canonical publication serial.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Notation,assumptions,derivations and alternatives connect to a banking decision.','Static expression findings are not generalized to native failure rates or all versions.','Process custody remains outside the product narrative.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=60,scholarly_originals=3,limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=60,anchors=len(fragments),new_records=11,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Seven selected Python comparisons inspected;bounded search and native coverage remain incomplete.','Dated authentic sources,three genuine papers and independent exact witnesses support the claims.','Integration,port,defer and rejection routes retain scientific,numerical,rights and acceptance limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Python mediation and sensitivity source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Python mediation coverage receipt prepared.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
