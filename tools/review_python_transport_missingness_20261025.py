#!/usr/bin/env python3
"""Review pinned originals and authored references without running retrieved code."""
import argparse,hashlib,json
from pathlib import Path
import python_transport_missingness_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as fresh_write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/python-transport-missingness-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.transport_missingness.Python'
read=lambda p:json.loads(p.read_text())
def write(p,value):
    if p.exists():assert read(p)==value,'Existing evidence differs: '+str(p)
    else:fresh_write(p,value)
LIMITS=['Six bounded discovery queries retain uninspected candidates; no saturation or absence claim.',
 '36 authentic originals across six packages; no downloaded code executed.',
 'Exact authored laws and static source findings are not native package failure frequencies.',
 'Complete learner, variance, imputation, runtime and dependency-rights qualification remains open.',
 'Package references remain discovery leads unless genuine scholarly PDFs and technical anchors are retained.',
 'No visual, independent, bank or final acceptance; mandatory repairs and Q1/Q5 remain open.']
NEXT='Complete Python transport/missingness candidate and primary-paper routes; qualify stabilization, observed versus counterfactual weights, clipping, seed boundaries, imputation law, row identity, full covariance and missingness-correction dispatch with public fixtures and complete rights/costs.'
DECISIONS=['zEpid: conditional explicit transport targets and response-model reuse; qualify augmentation, stabilization and missingness.',
 'causallib: conditional treatment-weighting component reuse after matrix semantics and population mapping.',
 'miceforest: conditional flexible imputation engine; preserve draw law, seed scope, resources and new-data requirements.',
 'statsmodels: conditional imputation-analysis-pooling reuse; preserve row identity, donor settings and full covariance.',
 'causal-learn: conditional missingness-aware discovery; qualify actual test dispatch, information threshold and correction law.']
ANCHORS={
 'zepid':[
 ('LICENSE_txt',1,25,'MIT','Selected MIT rights declaration.'),
 ('zepid_causal_generalize_estimators_py',11,62,'Confidence intervals','Declared generalize/transport distinction and bootstrap requirement.'),
 ('zepid_causal_generalize_estimators_py',151,179,'if self.generalize','Inverse selection probability/odds with optional stabilization and bounds.'),
 ('zepid_causal_generalize_estimators_py',216,250,'np.average','Missingness placeholder and normalized arm means.'),
 ('zepid_causal_generalize_estimators_py',435,471,'self.target.copy','Population-specific counterfactual averaging.'),
 ('zepid_causal_generalize_estimators_py',598,610,'currently unavailable','AIPSW explicitly refuses supplied optional weights.'),
 ('zepid_causal_generalize_estimators_py',622,665,'stabilized=True','Selected AIPSW selection stabilization.'),
 ('zepid_causal_generalize_estimators_py',667,699,'iptw_calculator','Default treatment stabilization delegates to common weights.'),
 ('zepid_causal_utils_py',300,340,'n / d','Exact stabilized and unstabilized treatment weights.'),
 ('zepid_causal_generalize_estimators_py',763,800,'np.sum(1 - self.df[self.selection])','Augmented residual and target denominators; no arm-specific residual renormalization.')],
 'causallib':[
 ('LICENSE',1,6,'Apache License','Selected Apache2 declaration; transitive rights separate.'),
 ('causallib_estimation_ipw_py',103,145,'prevalence_per_subject','Weight matrix stabilization uses observed-treatment prevalence per row; observed diagonal differs from general counterfactual semantics.'),
 ('causallib_estimation_ipw_py',176,202,'probabilities.clip','Componentwise clipped probabilities are not renormalized here.'),
 ('causallib_estimation_ipw_py',66,102,'compute_weight_matrix','Selected observed treatment weights extracted from matrix.'),
 ('causallib_estimation_standardization_py',84,109,'Standardization','Separate response-standardization component; transport mapping not inferred.')],
 'miceforest':[
 ('pyproject_toml',1,23,'license = "MIT"','Version6.0.5 and metadata MIT declaration; no license-named file in selected tree.'),
 ('miceforest_imputation_kernel_py',78,141,'random_seed_array','Donor strategies, deterministic zero-candidate branch, saved-data and seed conditions.'),
 ('miceforest_imputation_kernel_py',585,624,'workers=-1','Nearest-neighbor donor draw, worker request and hashed-seed selection.'),
 ('miceforest_imputation_kernel_py',626,655,'np.random.seed','Binary modal/stochastic branch and global RNG mutation under record seeds.'),
 ('miceforest_imputation_kernel_py',928,952,'_impute_with_predictions','Zero-candidate path bypasses donor matching.'),
 ('miceforest_imputation_kernel_py',1583,1614,'assert self.save_all_iterations_data','Record-level conditions and explicit new-data refusal without retained models.')],
 'statsmodels':[
 ('LICENSE_txt',1,26,'Redistribution','Selected BSD-style rights declaration.'),
 ('statsmodels_imputation_mice_py',190,219,'reset_index','All-missing rows dropped and row index reset.'),
 ('statsmodels_imputation_mice_py',335,418,'self.k_pmm = k_pmm','Common donor count set by per-variable configuration method.'),
 ('statsmodels_imputation_mice_py',1004,1048,'cov_params','Bootstrap and Gaussian model-parameter perturbation delegates.'),
 ('statsmodels_imputation_mice_py',1111,1179,'imputed_miss','Donor matching and retained observed values.'),
 ('statsmodels_imputation_mice_py',1316,1331,'self.results_list = []','Repeated fit resets analysis pool.'),
 ('statsmodels_imputation_mice_py',1333,1387,'cov_between = np.cov','Full within/between covariance pooling and fraction of missing information.')],
 'causallearn':[
 ('LICENSE',1,25,'MIT','Selected MIT declaration.'),
 ('causallearn_utils_cit_py',444,489,'sqrt(len(test_wise','Per-test complete rows, singularity refusal and sample-size multiplier.'),
 ('causallearn_utils_cit_py',491,555,'Helper.cond_perm_c','Correction conditions, fallback, predictor extraction and virtual sample.'),
 ('causallearn_search_ConstraintBased_PC_py',417,443,'mc_fisherz','Both accepted correction names dispatch to mc_fisherz.'),
 ('causallearn_utils_PCUtils_Helper_py',521,552,'np.random.shuffle','Common predictor shuffle and original residual-vector addition.'),
 ('causallearn_utils_PCUtils_Helper_py',662,686,'LinearRegression','Separate linear regressions and retained residual vectors.')]
}
def prepare():
    assert not (BASE/'review.json').exists()
    rows=read(BASE/'selected-originals.json');assert len(rows)==36
    pins=read(BASE/'pins.json');identities=[];originals=[]
    for group,pin in pins.items():
        cp=RAW/f'exec25_ptm_{group}_commit.json';tp=RAW/f'exec25_ptm_{group}_tree.json'
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        commit=read(cp)[0];assert commit['sha']==pin['sha'] and commit['commit']['committer']['date']==pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha']==pin['sha'] and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned original identity'),ref(tp,'Complete selected repository tree')])
        for row in [x for x in rows if x['group']==group]:
            p=ROOT/row['local_path'];rp=ROOT/row['receipt'];r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p)==row['sha256'] and r['url']==row['url']
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['git_blob']==blobs[row['upstream_path']]
            originals.append(dict(group=group,upstream_path=row['upstream_path'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'Bound public receipt'),git_blob=row['git_blob']))
    write(BASE/'authenticated-originals.json',dict(count=36,groups=5,originals=originals,identities=identities,native_execution=False))
    sources=[];fragments=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[ref(RAW/f'exec25_ptm_{group}_commit.json','Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_ptm_{group}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,lo,token)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=group,source=binding,first_line=lo,last_line=hi,text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_ptm_'+group,kind='software',title=group+' pinned transport and missingness implementation contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['sha'],version_date=pin['date']+';'+pin['sha'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_ptm_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only; current search filtered by creation date, not a historical search snapshot'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==6
    for pin in pins.values():
        if pin['repository'] in leads:leads[pin['repository']]['status']='selected_primary_anchors'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals.json','Selected original declarations')],findings=['zEpid and causal-learn retain MIT declarations; causallib Apache2; statsmodels BSD-style; miceforest MIT metadata without a license-named file in selected tree.','Full runtime, compiled components and transitive dependencies remain unqualified.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored finite-law arithmetic'),ref(BASE/'exact-results.json','Exact replay'),ref(BASE/'inspected-extracts.json','Primary delegates')],findings=['Selected zEpid stabilization gives2for transport and2/5for generalize under supplied nuisance law; unstabilized reference gives1.','Observed-diagonal weights can agree while counterfactual matrix columns differ.','Clipped multiclass denominators sum to11/10; fixed modal completion removes conditional draw variance.','Full pooling covariance gives contrast variance2versus38/3if cross-covariance is dropped.','Fisher multiplier at three unconditional rows is zero; typed information refusal is required.','Hypothetical transport discrepancyUSD100000; no native or bank evidence.'],native_execution=False))
    tests=['Freeze target population, sampling law, treatment and outcome scale.','Compare exact population scores and normalize by the declared sampling denominator.','Verify augmented residual stabilization separately from normalized IPW means.','Test joint support, retained population, survey weights and clipping.','Verify observed versus counterfactual matrices and clipped-denominator semantics.','Qualify each imputation method, mask, ignore policy and substantive model.','Retain seed state, row identity, donor settings, full covariance and every missingness-correction refusal.','Resolve complete rights and runtime versions before distribution.','Replay typed CLI/MCP requests and record full public-prototype costs.']
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Python transport, missingness, compatibility and uncertainty contracts',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Prototype implementation owner to be appointed',tests=tests,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Explicit candidate tail'),ref(BASE/'dependency-license-review.json','Complete rights unresolved')],known_routes=tests,uninspected=['Remaining returned repositories and broader package catalog coverage.','Complete learner, imputation, native sampling and graph-correction qualification.','Package-mentioned scholarly references without newly retained genuine originals.'],unknown_universal_repairs=['Unrestricted MNAR and causal assignment truth are not recovered by filling cells.','Unsupported target strata require information or justified extrapolation restrictions.','Arbitrary dependence and learner uncertainty have no promised universal repair.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','mathematical-review.json','comparison-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_ptm_choice',kind='project_evidence_not_scholarly_paper',title='Authored Python transport and missingness derivations and qualification decisions',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; cutoff 7 October 2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence+[ref(Path(exact.__file__),'Authored reference')],inspected_anchors=[dict(anchor='Population score, finite-law references and source choices',inspection='Author inspection')],supported_claims=['36 originals support five component comparisons and conditional adoption decisions.','Authored population identities and finite laws distinguish scientific targets and implementation assumptions.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=6,new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Population transport, treatment weighting, imputation and discovery remain distinct.','Static witnesses and exact laws do not assert native failures.','Public qualification is eligible before expensive bank trials; other branches continue.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Bank population through scores, weighting semantics, imputation laws, covariance, graph correction and economics.','All five source collections and authored witnesses are cited with explicit scope.','No new scholarly citation without original; no native or visual acceptance.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    verify_bindings(dict(evidence=evidence));write(BASE/'review.json',dict(status='pass_for_bounded_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=36,scholarly_originals=0,limitations=LIMITS,native_execution=False));print(json.dumps(dict(review='pass',outcome='inconclusive',originals=36,anchors=len(fragments))))

def receipt():
    review=read(BASE/'review.json');verify_bindings(review);assert exact.calculate()==read(BASE/'exact-results.json')
    state=core.read(ROOT,core.STATE);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);output=ROOT/node['outputs'][0]
    write(output,read(BASE/'comparison-review.json'))
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Five component roles inspected; bounded ecosystem and native coverage remain incomplete.','Pinned authentic originals and exact authored laws support claims; scholarly metadata is discovery only.','Conditional adoption, port, defer and reject routes preserve scientific, rights and qualification conditions.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Python transport and missingness primary-source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Python transport/missingness coverage receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
