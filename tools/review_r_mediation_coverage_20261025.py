#!/usr/bin/env python3
"""Review pinned R mediation sources without executing acquired code."""
import argparse
import hashlib
import json
from pathlib import Path
import r_mediation_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

run=controller.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/r-mediation-coverage-v1'
RAW=ROOT/'docs/literature/raw'
OP='SW.CELL.mediation_sensitivity.R'
read=lambda p:json.loads(p.read_text())
LIMITS=['Four bounded queries expose105 unique leads with unreturned and uninspected tails;no exhaustive coverage claim.',
        'No acquired code,installed R package,Stan sampler or native experiment executed.',
        'Selected pre-cutoff source snapshots and two genuine preprints;not final publisher or installed-artifact certification.',
        'Static inconsistencies and exact authored witnesses are not native failure-rate measurements.',
        'Complete delegates,dependency rights,scientific qualification and public benchmark execution remain open.',
        'Visual,independent and final acceptance remain open;no bank adoption or general identification.']
NEXT='Complete explicit R candidate tails;reconcile conditional and joint mediator draws,survey-weight normalization and BayesGmed mixture/prior/link semantics;resolve license scope;then qualify frozen public known-law fixtures with complete failures,costs and refusal oracles.'
DECISIONS=[
 'CMAverse:conditional method interface;reject automatic equivalence of globally shuffled mediators to baseline-conditioned joint stochastic interventions.',
 'medoutcon:conditional R estimator reference;retain influence-function and target identity;require normalization,constant-outcome and dependent-sampling tests.',
 'regmedint:conditional reference for matched conditional interaction models;do not substitute covariate means for marginal standardization or rare-outcome formulas for arbitrary risks.',
 'causalsens:conditional linear-outcome sensitivity comparator;preserve function sign,target and outcome units;no automatic mediation identification.',
 'tipr:conditional sensitivity interface using inherited sensemakr/EValue work;enforce scale,domain and requested boundary before accepting output.',
 'BayesGmed:defer selected sensitivity implementation pending mixture reconciliation,prior/link contracts and rights review;retain ordinary-model candidate separately.',
 'Port only after a declared target and measured workflow benefit;do not port the observed source inconsistencies.']

# Authored locators refer to source spans already read in the technical review.
ANCHORS={
 'cmaverse':[
 ('src01',1,67,'GPL-3','Version0.1.0,GPL3 and dependencies.'),
 ('src03',134,217,'postc','Methods,intermediate confounders and rare-outcome/inference restrictions.'),
 ('src03',227,276,'rpnde','Natural labels change to randomized analogues with post-treatment confounding.'),
 ('src04',1,54,'single variable','Declared E-value and single-variable measurement-error scope;delegates not fully qualified.'),
 ('src05',125,162,'postcdesign_a','Intermediate confounders simulated conditional on baseline and exposure.'),
 ('src05',215,255,'mdesign_a','Mediator draws depend on baseline,exposure and intermediate confounders.'),
 ('src05',295,342,'sample(mid_a','Global per-column mediator permutation precedes outcome prediction.'),
 ('src11',270,299,'boot(','Selected row-bootstrap and delta uncertainty paths.')],
 'medoutcon':[
 ('src01',1,70,'0.2.5','Version0.2.5,MIT declaration and learner dependencies.'),
 ('src03',1,21,'MIT License','MIT text;separate dependency clearance.'),
 ('src05',125,203,'effect_type','Natural/interventional switch,binary contrast grid and empirical outcome scaling.'),
 ('src05',262,331,'pm_theta_est','Influence-score contrasts and log-ratio proportion mediated.'),
 ('src06',385,415,'two_phase_eif','Two-phase observed-data influence projection.'),
 ('src06',520,596,'os_var','Row folds,weighted mean and unnormalized weighted-score variance.'),
 ('src08',22,61,'qlogis','Different transforms for effects and binary counterfactual means.'),
 ('src08',180,215,'scale_to_unit','Clipping and zero-range outcome scaling boundaries.')],
 'regmedint':[
 ('src01',1,51,'GPL-2','Version1.0.1 and GPL2 declaration.'),
 ('src03',25,46,'c_cond','Conditional covariate values,outcome families and case-control flag.'),
 ('src04',36,66,'data[[yvar]] == 0','Control-only mediator fit with explicit rare-outcome requirement.'),
 ('src05',32,57,'glm(','Linear/logistic mediator model delegates.'),
 ('src09',133,199,'pnde <-','Interaction-aware conditional effects and complementary decompositions.'),
 ('src09',240,249,'bdiag','Block-diagonal covariance across fitted regressions.'),
 ('src09',429,460,'abs(a1 - a0)','Proportion gradient and absolute contrast standard-error scaling.'),
 ('src10',170,205,'exp(te)','Logistic expressions and log-scale effects require scale and approximation checks.')],
 'causalsens':[
 ('src01',1,18,'GPL','Version0.1.3 and GPL-family declaration.'),
 ('src03',74,140,'linear outcome','Selected linear outcome-model scope.'),
 ('src03',160,191,'y.adj <- y - adj','Adjusted-outcome regression and model-based t interval.'),
 ('src03',290,326,'alignment.att','Distinct one-sided,alignment and treated-population functions.')],
 'tipr':[
 ('src01',1,46,'1.0.2.9000','Pinned development version and dependencies.'),
 ('src02',1,21,'MIT License','MIT license text.'),
 ('follow01',1,2,'2022','Named copyright-holder companion.'),
 ('src04',39,78,'sensemakr::adjusted_estimate','Partial-R-squared wrapper delegates estimate and standard error.'),
 ('src05',23,35,'effect_observed -','Linear bias-product adjustment.'),
 ('src05',74,103,'confounding_factor','Binary-prevalence and loglinear adjustment branch.'),
 ('src06',1,19,'sqrt','Numeric E-value formula has no baseline-risk or scale argument.'),
 ('src10',62,84,'confounder_outcome_r2 = 0','Boundary fallback resets outcome partial-R-squared and needs revalidation.'),
 ('src13',24,28,'sensemakr::robustness_value','Robustness-value wrapper.')],
 'bayesgmed':[
 ('src01',1,46,'0.0.3','CRAN0.0.3,MIT declaration and compiled dependencies.'),
 ('src02',1,2,'COPYRIGHT','License holder companion.'),
 ('src11',1,14,'General Public License','Separate Stan include GPL3-or-later notice;scope unresolved.'),
 ('src04',58,117,'link.y','Link arguments do not change fixed selected binary/continuous dispatch.'),
 ('src05',60,117,'scale_gamma','Gaussian bias-prior covariance and sensitivity dispatch.'),
 ('src10',29,91,'ll_1 =','Binary/binary source duplicates log(1-p) across latent states.'),
 ('src08',56,98,'ll_1 =','Continuous/binary source has same duplicated weight.'),
 ('follow04',78,94,'ll_1 =','Binary/continuous source has same duplicated weight.'),
 ('follow05',82,98,'ll_1 =','Continuous/continuous source has same duplicated weight.'),
 ('follow01',1,32,'loadModule','Initialization binds wrappers to named compiled modules.'),
 ('follow02',702,720,'ll_1 =','Generated binary/binary C++ retains duplicated mixture weight.'),
 ('follow03',737,754,'ll_1 =','Generated continuous/binary C++ retains duplicated mixture weight.'),
 ('src10',94,134,'categorical_rng','Generated quantities bootstrap rows and simulate latent states/outcomes.')]
}

def prepare():
    assert not (BASE/'review.json').exists()
    pins={x['key']:x for x in read(BASE/'pins.json')}
    rows=read(BASE/'selected-originals.json')+read(BASE/'followup-originals.json')
    assert len(rows)==66
    originals=[];identities=[]
    for group,pin in pins.items():
        cp=RAW/('exec25_rmed_'+group+'_commit.json');tp=RAW/('exec25_rmed_'+group+'_tree.json')
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        assert read(cp)[0]['sha']==pin['commit'] and pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha']==pin['commit'] and not tree['truncated']
        blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned revision/date'),ref(tp,'Complete selected tree')])
        for row in [x for x in rows if x['group']==group]:
            p=ROOT/row['local_path'];r=read(ROOT/row['receipt']);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p) and r['url']==row['url']
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['git_blob']==blobs[row['upstream_path']]
            originals.append(dict(group=group,upstream_path=row['upstream_path'],git_blob=row['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(ROOT/row['receipt'],'Bound retrieval')))
    write(BASE/'authenticated-originals.json',dict(status='pass',count=66,originals=originals,evidence=identities))
    sources=[];fragments=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[ref(RAW/('exec25_rmed_'+group+'_commit.json'),'Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/('exec25_rmed_'+group+'_'+suffix+'.txt');lines=p.read_text().splitlines();excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,lo,token)
            binding=ref(p,'Lines{}-{}:{}'.format(lo,min(hi,len(lines)),finding));evidence.append(binding)
            anchors.append(dict(path=binding['path'],line_spans=[[lo,min(hi,len(lines))]],finding=finding));claims.append(finding)
            fragments.append(dict(group=group,source=binding,first_line=lo,last_line=min(hi,len(lines)),text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_rmed_'+group,kind='software',title=group+' pinned causal mediation and sensitivity source review',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['commit'],version_date=pin['date']+';'+pin['commit'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=len(fragments)))
    paper_anchors={'diaz':[(3,5,'i.i.d. data,interventional versus natural effects,conditioning choice and identification formula'),(6,9,'Efficient influence representation,multiple robustness,cross-fitting,positivity and nuisance-product rates')], 'yimer':[(5,7,'Natural and controlled effects,cross-world,consistency and positivity assumptions'),(8,10,'Independent observations,parametric g-computation,bootstrap integration and uniform sensitivity-prior description')]}
    for p in read(BASE/'paper-identities.json'):
        pp=ROOT/p['local_path'];assert core.sha(pp)==p['sha256'];pages=(ROOT/p['text_path']).read_text().split(chr(12));anchors=[]
        for lo,hi,claim in paper_anchors[p['tag']]:
            excerpt=chr(12).join(pages[lo-1:hi]);anchors.append(dict(physical_pages=list(range(lo,hi+1)),anchor='Physical pages{}-{}'.format(lo,hi),text_extract=ref(ROOT/p['text_path'],'Genuine PDF text'),excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest(),finding=claim))
        limits=LIMITS+(['PDF sidebar/abstract identity2019 and title-page/creation2022 differ;both pre-cutoff;no final-edition claim.'] if p['tag']=='diaz' else ['Paper uniform sensitivity prior differs from selected2024Gaussian source prior.'])
        source={k:p[k] for k in ['title','filename_title','first_author','author','year','source_identity','version_date','local_path','sha256']}
        source.update(integrated_citation_key='exec25_rmed_'+p['tag']+'_paper',kind='paper',local_copy=ref(pp,'Genuine primary preprint'),identity_evidence=[ref(ROOT/p['identity_path'],'Primary identity'),ref(ROOT/p['retrieval_path'],'PDF retrieval')],inspected_anchors=anchors,supported_claims=[x['finding'] for x in anchors],limitations=limits)
        sources.append(source)
    write(BASE/'paper-review.json',dict(status='pass_for_selected_primary_anchors',papers=[x for x in sources if x['kind']=='paper'],all_theorems_independently_verified=False,limitations=LIMITS))
    results=exact.calculate();write(BASE/'exact-results.json',results)
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_rmed_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only'),receipt=ref(p.with_suffix('.receipt.json'),'Identity'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],language=x.get('language'),status='uninspected_discovery')
    assert len(queries)==4 and len(leads)==105
    for pin in pins.values():
        if pin['repository'] in leads:leads[pin['repository']]['status']='selected_primary_anchors'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=105,leads=list(leads.values()),saturation_claim=False,absence_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals.json','Declarations and originals')],findings=['CMAverseGPL3,regmedintGPL2,causalsensGPL>=2;medoutcon andtiprMIT.','BayesGmedDESCRIPTION saysMIT;retained separate Stan license include saysGPL3-or-later. Applicability requires artifact-specific clarification.','Selected source and generated C++ do not certify an installed binary or full dependency chain.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Independent finite reference'),ref(BASE/'exact-results.json','Exact replay'),ref(BASE/'paper-review.json','Primary assumptions'),ref(BASE/'inspected-extracts.json','Static source paths')],findings=['Conditional mediator target3/8 versus global shuffle1/4;dependent mediator product1/2 versus independent shuffle1/4.','Stochastic direct3/32 plus indirect1/16 equals5/32;ordinary ATE3/16 differs.','Interaction-aware effects8,18,18,8 and total26;coefficient product8 alone is insufficient.','Bayesian source mixture mass2/5;event13/100 versus intended49/100;renormalizing gives13/40 and still changes model.','Generated C++ preserves selected mixture expression;no native failure-rate claim.','Weighted-mean score example keeps estimate2 but selected variance changes1to4 under doubled weights.','OR2 at baseline risk1/2 implies RR4/3;E-values3.4142 versus2;scale substitution is material.','Sensitivity sign,measured-mediator inclusion and hypothetical USD30000 denominators reproduce.'],native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='R mediation estimands,sensitivity and source-to-equation contracts',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    tests=['Declare target population,causal graph,information times and intervention conditioning.','Verify natural versus stochastic total and common mediator distribution.','Check interactions,rare-outcome approximations,marginal standardization and zero-total ratios.','Enumerate binary mixture normalization and match Stan to generated and installed artifacts.','Reconcile prior family,link dispatch,parameter scales and rights.','Verify weight-rescaling invariance,contrast covariance,two-phase measurement weights and constants.','Freeze folds,bootstrap unit,positivity thresholds,simulation integration and refusal conditions.','Use public synthetic known-law fixtures,complete request/failure denominators and full costs before bank work.']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,independent_branches=True,native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Explicit tails'),ref(BASE/'dependency-license-review.json','Rights limits')],known_routes=tests,unavailable_primary_route=ref(RAW/'exec25_rmed_paper_identities.receipt.json','Original failed identity request retained;distinct abstract/PDF routes succeeded'),uninspected_method_papers=['Blackwell selection-bias original','Original regression-mediation approximation papers','General sensitivity delegate papers beyond inherited reviewed records'],unknown_universal_repairs=['Unobserved mediator-outcome confounding and cross-world assumptions cannot be established by software outputs.','Arbitrary dependent sampling requires additional assumptions and uncertainty theory.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals.json','paper-review.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','mathematical-review.json','comparison-review.json']]
    sources.append(dict(integrated_citation_key='exec25_rmed_choice',kind='project_evidence_not_scholarly_paper',title='Authored R mediation target,mixture and qualification comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence,inspected_anchors=[dict(anchor='Selected comparison and proposed qualification',inspection='Author inspection')],supported_claims=['66authenticated software originals and two genuine primary preprints.','Explicit use,port,defer and reject decisions grounded in targets and source expressions.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=9,new_scholarly_pdfs=2,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Extend inherited mediation,medflex,sensemakr and EValue records without repeating completed reuse decisions.','Six new comparisons,two genuine preprints,exact target and source witnesses.','Keep search,native,rights,visual and final gates open;canonical publication serial.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Explained causal targets,conditioning,uncertainty,source issues and alternatives.','No source defect is generalized to an entire methodology or measured native failure rate.','Process custody remains outside product narrative.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=66,scholarly_originals=2,limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(review='pass_for_selected_work',originals=66,anchors=len(fragments),new_records=9,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Six selected R comparisons inspected;bounded search and native coverage remain incomplete.','Claims bind dated authentic originals,two genuine primary papers and exact authored witnesses.','Integration,port,defer and rejection routes retain scientific,rights,artifact and acceptance limits.']
    result=run.ledger.receipt_template(node)
    result.update(outcome='inconclusive',execution='performed',scope='R mediation and sensitivity source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result)
    print('R mediation coverage receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
