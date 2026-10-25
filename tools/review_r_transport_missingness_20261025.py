#!/usr/bin/env python3
"""Review pinned originals and authored references without running retrieved code."""
import argparse,hashlib,json
from pathlib import Path
import r_transport_missingness_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as fresh_write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/r-transport-missingness-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.transport_missingness.R'
read=lambda p:json.loads(p.read_text())
def write(p,value):
    if p.exists():assert read(p)==value,'Existing evidence differs: '+str(p)
    else:fresh_write(p,value)
LIMITS=['Four bounded discovery queries retain uninspected candidates; no saturation or absence claim.',
 '75 authentic originals across six packages; no downloaded code executed.',
 'Exact authored laws and static source findings are not native package failure frequencies.',
 'Complete learner, variance, imputation, runtime and dependency-rights qualification remains open.',
 'Package references remain discovery leads unless genuine scholarly PDFs and technical anchors are retained.',
 'No visual, independent, bank or final acceptance; mandatory repairs and Q1/Q5 remain open.']
NEXT='Complete R transport/missingness candidate and paper routes; qualify target population, scale, selection odds, normalization, observation laws, joint support, folds, uncertainty delegates, compatible imputation and rejection failures with public fixtures; retain full rights and costs.'
DECISIONS=['generalize: conditional weighting and diagnostic reuse after population, effect-scale, survey and trimming qualification.',
 'transportr: conditional task-interface reuse; defer direct admission until observation, iterated routing and uncertainty delegates are qualified.',
 'causaltransportr: defer selected transport score pending corrected or justified odds/normalization and public parity; preserve other branch distinctions.',
 'mice: conditional method-specific imputation and pooling adoption; reject interpretation as recovery of unobserved causal truth.',
 'smcfcs: conditional compatible-model implementation reuse; unresolved rejected draws must be explicit failures.',
 'causalOT: conditional weighting-component reuse; reject substitution of optimal transport for a population transportability argument.']
ANCHORS={
 'generalize':[
 ('DESCRIPTION',1,30,'License:','Version and selected MIT declaration; dependencies separate.'),
 ('R_weighting_R',56,95,'sampsize = 454','Missing-row removal, survey normalization, row expansion and fixed random-forest sample size.'),
 ('R_weighting_R',108,150,'quasibinomial','Zero-probability adjustment, disjoint/nested weights, clipping and binary odds-ratio output.'),
 ('R_generalize_R',18,32,'trimpop = TRUE','TMLE dispatch forces population trimming.'),
 ('R_trim_pop_R',31,64,'trial_bounds','Coordinate range and factor support screening; retained population recorded.')],
 'transportr':[
 ('DESCRIPTION',1,38,'License:','Version and GPL declaration with external dependencies.'),
 ('R_transport_ate_R',12,63,'Currently not used','Population, observation and cluster declarations; unused sampling weights and one-fold default.'),
 ('R_TransportTask_R',139,165,'cluster_ids','One-fold training/validation identity and separate cluster-aware fold construction.'),
 ('R_influence_function_R',6,29,'ife::ife','Selected standard score, inverse selection odds and row-contribution delegation.'),
 ('R_helpers_R',28,32,'res[is.na(res)] <- 0','All missing products replaced by zero; structural missingness and errors need distinction.'),
 ('R_outcome_mechanism_R',1,29,'obs()','Outcome fitting restricted to observed source rows.'),
 ('R_outcome_mechanism_R',32,72,'.outcome_eps1','Both arm-specific iterated fits route to eps1 despite eps0 also being carried.')],
 'causaltransportr':[
 ('DESCRIPTION',1,27,'License: MIT','Version and selected MIT declaration.'),
 ('R_ateGT_R',6,20,'hajekize','Declared population modes, estimator families and normalization interpretation.'),
 ('R_nuis_R',62,98,'cv.glmnet(X, s','Selection model fits S; resulting probabilities are source membership.'),
 ('R_nuis_R',180,193,'rhomat =','Selection probability expanded into the score matrix.'),
 ('R_ateGT_R',197,231,'nuis$smat * nuis$rhomat','No-surrogate augmented transport odds differ from unaugmented transport branch.'),
 ('R_ateGT_R',130,155,'colSums(nuis$pihat)','Selected optional normalization uses sums of treatment probabilities.'),
 ('R_estQOIs_R',1,43,'sqrt(n)','Target denominator changes sums and standard-error denominator; row distribution requires derivation.')],
 'mice':[
 ('DESCRIPTION',103,114,'License:','Selected GPL declaration and native dependencies.'),
 ('R_mice_R',153,198,'do not honour','Per-method ignore/where limitations and unchecked monotone shortcut.'),
 ('R_sampler_R',266,282,'!ignore','Observed complete fitting rows and imputation masks.'),
 ('R_mice_impute_pmm_R',153,224,'return(y[ry][idx])','Donor exclusions, matching options and observed-value output.'),
 ('R_mice_impute_mnar_norm_R',147,173,'u$delta','User-specified unidentifiable contribution added to normal draw.'),
 ('R_pool_R',1,22,'pool the','Fit scientific models before pooling estimates; do not pool completed data.'),
 ('R_pool_vector_R',47,92,'robust.se','Robust variance extraction; different missing-data and synthetic-data pooling rules.'),
 ('R_barnard_rubin_R',1,9,'dfcom','Finite complete-data degrees-of-freedom calculation.')],
 'smcfcs':[
 ('DESCRIPTION',1,28,'License: GPL-3','Selected version, rights declaration and dependencies.'),
 ('R_smcfcs_r',1003,1044,'outcomeDens','Discrete update combines covariate and substantive likelihood information.'),
 ('R_smcfcs_r',1080,1108,'rowSums(outcomeDensCovDens)','Product normalization and discrete draw.'),
 ('R_smcfcs_r',1114,1147,'firstTryLimit <- 25','Initial rejection loop permits at most 24 attempts and updates stored proposals.'),
 ('R_smcfcs_r',1195,1224,'rjlimit','Finite per-subject proposal batch after initial attempts.'),
 ('R_smcfcs_r',1289,1298,'rjFailCount <- rjFailCount + 1','All-rejected batch increments failure count without successful replacement.'),
 ('R_smcfcs_r',1398,1423,'return(res)','Warnings accompany returned datasets; passive terms evaluated from declared expressions.')],
 'causalOT':[
 ('DESCRIPTION',1,25,'License:','Selected version and GPL declaration.'),
 ('R_calc_weight_R',1,23,'"ATT","ATC", or "ATE"','Weighting estimands and optimal-transport interpretation are distinct from population transportability.'),
 ('R_treatment_effect_R',30,76,'likelihood_methods','Optional normalization is method-conditional; outcome model and augmentation dispatch.'),
 ('R_treatment_effect_R',130,172,'tau    <- switch','Different ATT/ATC/ATE targets and weighted residual augmentation.'),
 ('R_ESS_R',3,35,'1/sum(x^2)','Numeric effective sample size assumes normalized weights.')]
}
def prepare():
    assert not (BASE/'review.json').exists()
    rows=read(BASE/'selected-originals.json');assert len(rows)==75
    pins=read(BASE/'pins.json');identities=[];originals=[]
    for group,pin in pins.items():
        cp=RAW/f'exec25_rtm_{group}_commit.json';tp=RAW/f'exec25_rtm_{group}_tree.json'
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        commit=read(cp)[0];assert commit['sha']==pin['sha'] and commit['commit']['committer']['date']==pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha']==pin['sha'] and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned original identity'),ref(tp,'Complete selected repository tree')])
        for row in [x for x in rows if x['group']==group]:
            p=ROOT/row['local_path'];rp=ROOT/row['receipt'];r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p)==row['sha256'] and r['url']==row['url']
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['git_blob']==blobs[row['upstream_path']]
            originals.append(dict(group=group,upstream_path=row['upstream_path'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'Bound public receipt'),git_blob=row['git_blob']))
    write(BASE/'authenticated-originals.json',dict(count=75,groups=6,originals=originals,identities=identities,native_execution=False))
    sources=[];fragments=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[ref(RAW/f'exec25_rtm_{group}_commit.json','Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_rtm_{group}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,lo,token)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=group,source=binding,first_line=lo,last_line=hi,text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_rtm_'+group,kind='software',title=group+' pinned transport and missingness implementation contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['sha'],version_date=pin['date']+';'+pin['sha'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_rtm_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only; current search filtered by creation date, not a historical search snapshot'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==4
    for pin in pins.values():
        if pin['repository'] in leads:leads[pin['repository']]['status']='selected_primary_anchors'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals.json','Selected original declarations')],findings=['generalize and causaltransportr declare MIT; transportr GPL>=3; mice GPL>=2; smcfcs GPL-3; causalOT GPL==3.0.','Full runtime, compiled components and transitive dependencies remain unqualified.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored finite-law arithmetic'),ref(BASE/'exact-results.json','Exact replay'),ref(BASE/'inspected-extracts.json','Primary delegates')],findings=['Correct inverse odds give target effect1; selected reversed odds give16 under the supplied finite law.','Binary risk difference1/10 differs from odds ratio9/4; marginal support does not imply joint support.','Missing-data variance19/3 differs from synthetic-data variance7/3.','Compatible binary update gives4/5; MNAR delta2 with missing fraction3/10 shifts mean3/5.','Finite rejection law and normalized effective-sample-size witnesses remain distinct from native measured behavior.','Hypothetical transport discrepancy is USD1500000; no empirical bank value claimed.'],native_execution=False))
    tests=['Freeze target population, sampling law, treatment and outcome scale.','Compare exact population scores and normalize by the declared sampling denominator.','Verify source/target structural missingness separately from failures and censoring.','Test joint support, retained population, survey weights and clipping.','Verify folds, cluster units and the complete uncertainty delegate.','Qualify each imputation method, mask, ignore policy and substantive model.','Retain rejected proposals, warnings and all failures; test pooling and covariance contracts.','Resolve complete rights and runtime versions before distribution.','Replay typed CLI/MCP requests and record full public-prototype costs.']
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='R transport, missingness, compatibility and uncertainty contracts',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Prototype implementation owner to be appointed',tests=tests,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Explicit candidate tail'),ref(BASE/'dependency-license-review.json','Complete rights unresolved')],known_routes=tests,uninspected=['Remaining returned repositories and broader package catalog coverage.','Complete learner, ife, imputation, optimal-transport solver and native sampling implementations.','Package-mentioned scholarly references without newly retained genuine originals.'],unknown_universal_repairs=['Unrestricted MNAR and causal assignment truth are not recovered by filling cells.','Unsupported target strata require information or justified extrapolation restrictions.','Arbitrary dependence and learner uncertainty have no promised universal repair.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','mathematical-review.json','comparison-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_rtm_choice',kind='project_evidence_not_scholarly_paper',title='Authored R transport and missingness derivations and qualification decisions',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; cutoff 7 October 2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence+[ref(Path(exact.__file__),'Authored reference')],inspected_anchors=[dict(anchor='Population score, finite-law references and source choices',inspection='Author inspection')],supported_claims=['75 originals support six component comparisons and conditional adoption decisions.','Authored population identities and finite laws distinguish scientific targets and implementation assumptions.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=7,new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Population transport, optimal transport and imputation remain separate.','Static witnesses and exact laws do not assert native failures.','Public qualification is eligible before expensive bank trials; other branches continue.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Bank population through assumptions, scores, missingness, compatibility, diagnostics and economic consequence.','All six source collections and authored witnesses are cited with explicit scope.','No new scholarly citation without original; no native or visual acceptance.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    verify_bindings(dict(evidence=evidence));write(BASE/'review.json',dict(status='pass_for_bounded_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=75,scholarly_originals=0,limitations=LIMITS,native_execution=False));print(json.dumps(dict(review='pass',outcome='inconclusive',originals=75,anchors=len(fragments))))

def receipt():
    review=read(BASE/'review.json');verify_bindings(review);assert exact.calculate()==read(BASE/'exact-results.json')
    state=core.read(ROOT,core.STATE);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);output=ROOT/node['outputs'][0]
    write(output,read(BASE/'comparison-review.json'))
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Six component roles inspected; bounded ecosystem and native coverage remain incomplete.','Pinned authentic originals and exact authored laws support claims; scholarly metadata is discovery only.','Conditional adoption, port, defer and reject routes preserve scientific, rights and qualification conditions.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='R transport and missingness primary-source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('R transport/missingness coverage receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
