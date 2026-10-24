#!/usr/bin/env python3
"""Authenticate selected Python dynamic originals,anchored claims and exact witnesses."""
import argparse, hashlib, json
from pathlib import Path
import python_dynamic_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/python-dynamic-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.dynamic_panel_timeseries.Python'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Selected primary paths and bounded searches; remaining candidates and complete ecosystem coverage remain open.',
 'No downloaded package or upstream tests executed; source predicates and exact authored examples are not native failures.',
 'Dynamic-panel moments, structural restrictions and forecast-state uncertainty have distinct assumptions and target populations.',
 'Complete solver/covariance delegates,artifact equivalence,dependency rights and supported environments remain unqualified.',
 'Unknown instrument exclusion,assignment truth,calendar dependence and bank utility require added information or restrictions.',
 'No new scholarly guarantee imported from README claims or code comments; visual,independent,bank and final acceptance remain open.'
]
NEXT='Inspect remaining dynamic-panel,VAR/state-space candidates and source delegates; validate calendar and row identity,structural mask objectives,optimizer diagnostics,proxy missingness/multiple instruments,bootstrap attempts/state,innovation and feature clocks. Preregister known-law public tests and preserve all previous pydynpd findings before any native admission.'

SPECS={
 'statsmodels':('statsmodels VAR/SVAR restrictions, likelihood and return contracts','statsmodels/statsmodels','repository pin;6 October 2026;8278e2d218cc85bac2c7af02feb9a19a0e499b04',[
 ('exec25_pydyn_stats_src_0',65,118,['A_mask','B_mask','np.identity'],'Structural mask encoding and default identity restrictions.'),
 ('exec25_pydyn_stats_src_0',188,212,['selections','lags = 1','_get_init_params'],'Lag selection and starting-parameter lifecycle.'),
 ('exec25_pydyn_stats_src_0',343,372,['npl.inv(B)','slogdet(B**2)','b_slogdet'],'Selected likelihood uses elementwise-square determinant expression.'),
 ('exec25_pydyn_stats_src_0',412,480,['if not override','check_order','check_rank','.params','return A, B'],'Optional local order/rank checks and optimizer-parameter-only return.'),
 ('exec25_pydyn_stats_src_0',537,547,['matrix_rank','solution may not be unique'],'Order/rank predicate scope.'),
 ('exec25_pydyn_stats_src_0',580,610,['npl.inv(A_solve)','np.dot(coefs, P)'],'Structural moving-average impact mapping.'),
 ('exec25_pydyn_stats_src_1',437,461,['_chol_sigma_u','ma_rep'],'Ordinary VAR orthogonalization uses Cholesky by default.')]),
 'xtabond':('PyXtabond2 calendar-grid instruments and numerical diagnostics','Kahindo048/pyxtabond2','0.0.4;6 September 2026;b522fe9510b50736a9a73ad83c165d472e7e69a0',[
 ('exec25_pydyn_xtabond_src_0',1,21,['MIT License','Frederick'],'Original MIT notice.'),
 ('exec25_pydyn_xtabond_src_2',1,15,['0.0.4','MIT','>=3.9'],'Package version/runtime metadata.'),
 ('exec25_pydyn_xtabond_src_3',85,132,['scatter_to_grid','searchsorted','t_off[idx] == target'],'Exact calendar-offset lag with contiguous fast path.'),
 ('exec25_pydyn_xtabond_src_3',176,213,['sort_values','dropna','_sort_perm','astype(np.int64)'],'Input sorting,row map and integer time offsets; full validation separate.'),
 ('exec25_pydyn_xtabond_src_5',184,206,['PanelData','scatter_to_grid'],'Instrument builder consumes a dense calendar grid.'),
 ('exec25_pydyn_xtabond_src_4',231,247,['matrix_rank(self.Z.T @ self.Z','self.z_rank = self.n_instruments'],'Gram-rank diagnostic and disabled-check fallback.'),
 ('exec25_pydyn_xtabond_src_4',377,433,['np.linalg.pinv','def estimate_two_step_robust'],'Selected GMM paths use pseudoinverses; moment validity separate.')]),
 'dynapanel':('dynapanel positional instrument arithmetic and numerical fallbacks','Leotaby/dynapanel','0.1.1;12 May 2026;e3afc6ad6da8648f211eb36347420ce381d03aa6',[
 ('exec25_pydyn_dynapanel_src_0',1,21,['MIT License','Hatef'],'Original MIT notice.'),
 ('exec25_pydyn_dynapanel_src_2',1,15,['0.1.1','MIT','>=3.10'],'Package version and runtime metadata.'),
 ('exec25_pydyn_dynapanel_src_3',70,95,['n_unique','cast(pl.Int64)','return df.sort'],'Duplicate check precedes optional integer conversion.'),
 ('exec25_pydyn_dynapanel_src_3',114,140,['positions','out[k:] = v[:-k]','out[1:] = v[1:] - v[:-1]'],'Positional lag and difference semantics.'),
 ('exec25_pydyn_dynapanel_src_5',76,98,['src = p - term.lag','a = p - term.lag','ind.values'],'Actual regressor assembly uses positions.'),
 ('exec25_pydyn_dynapanel_src_5',190,219,['src = p - s','ind.times[p]'],'Instrument values use positions while labels carry calendar times.'),
 ('exec25_pydyn_dynapanel_src_4',319,348,['n_inst < n_reg','n_inst >= N','n_inst > N / 2'],'Instrument-count guards and warnings.'),
 ('exec25_pydyn_dynapanel_src_4',588,604,['except linalg.LinAlgError','linalg.pinv','np.clip(v, 0.0, None)'],'Inverse fallback and clipped variance square root.'),
 ('exec25_pydyn_dynapanel_src_1',20,29,['experimental'],'Retained experimental status, not a general rejection.')]),
 'macroshock':('macroshock structural proxies, impact normalization and bootstrap state','patricioariaslpz/macroshock','repository pin;21 August 2026;ec7b648bbee69d226755094d82d0540315a168da',[
 ('exec25_pydyn_macroshock_src_0',1,21,['MIT License','Patricio'],'Original MIT notice.'),
 ('exec25_pydyn_macroshock_src_2',109,145,['self.iv=self.data[self.iv].values','reshape(-1, 1)'],'Public input conversion and multiple-instrument shape.'),
 ('exec25_pydyn_macroshock_src_2',269,286,['identify_iv','iv=self.iv','self.structural = True'],'Public path delegates arrays to inspected proxy helper.'),
 ('exec25_pydyn_macroshock_src_3',523,567,['mask = ~np.isnan','resid[-len(instrument)','B[:, :] = 0.0','B[:, j] / v'],'Missing instruments select residual suffix and reset impact matrix within instrument loop.'),
 ('exec25_pydyn_macroshock_src_4',9,43,['impact / B[shock - 1,shock - 1]','response = Psi_h @ B @ impulse'],'Impulse scaling is own-variable impact normalization.'),
 ('exec25_pydyn_macroshock_src_5',40,84,['while True','int(reps / 10)','resampled_resid = model.resid','rsigns'],'Bootstrap progress boundary,normal resampling and wild in-place alias.'),
 ('exec25_pydyn_macroshock_src_5',274,334,['Bsim = np.zeros','np.any(Bsim != 0)','if b >= reps'],'Proxy bootstrap reset and successful-draw stopping without separate attempt cap.'),
 ('exec25_pydyn_macroshock_src_3',295,335,['m_accepted >= reps','n_rejected >= 100000','B_zero','_zero_stat_dicts'],'Separate sign-search rejection cap and zero-filled abort summaries.')]),
 'pydlm':('PyDLM missing-step innovation and feature-clock boundaries','wwrechard/pydlm','repository pin;16 August 2026;56773fa1e0ef5fe3e26a8695fcd7b4bfcdcf1b69',[
 ('exec25_pydyn_pydlm_src_0',1,24,['Redistribution','copyright'],'Original BSD-style notice.'),
 ('exec25_pydyn_pydlm_src_2',8,43,['license="BSD"','Development Status :: 3 - Alpha','numpy'],'Setup runtime,license and alpha-status declarations.'),
 ('exec25_pydyn_pydlm_src_5',42,53,['__checkDiscount__','1 / np.sqrt'],'Discount validation precedes reciprocal-root initialization.'),
 ('exec25_pydyn_pydlm_src_5',73,113,['model.prediction.step == 0','model.prediction.sysVar += model.innovation','model.prediction.step += 1'],'First and subsequent prediction branches use different innovation conventions.'),
 ('exec25_pydyn_pydlm_src_5',133,194,['if y is not None','model.prediction.step = 0','model.sysVar = model.prediction.sysVar'],'Observed-data correction and missing-state update lifecycle.'),
 ('exec25_pydyn_pydlm_src_5',308,324,['discount[i] < 0 or discount[i] > 1','model.innovation'],'Local inclusive endpoint guard and innovation formula.'),
 ('exec25_pydyn_pydlm_src_7',68,86,['features','does not support missing data','deepcopy'],'Dynamic feature input; forecast availability remains an external contract.')])
}

def authenticate():
    rows=[];evidence=[]
    for name in ['statsmodels-source-selection.json','pydlm-source-selection.json','candidate-source-selection.json']:
        d=read(BASE/name);rows.extend(d['sources'] if isinstance(d,dict) else d);evidence.append(ref(BASE/name,'Pinned file identities'))
    assert len(rows)==38
    originals=[]
    for x in rows:
        p=RAW/(x['id']+'.txt');data=p.read_bytes();receipt=p.with_suffix('.receipt.json');r=read(receipt)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['git_blob']
        assert len(data)==x['bytes'] and core.sha(p)==r['sha256'] and r['status']=='saved'
        originals.append(dict(repository_path=x['path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original bytes'),retrieval=ref(receipt,'URL,date and SHA256')))
    for key in ['statsmodels','pydlm','macroshock','xtabond','dynapanel']:
        evidence.append(ref(RAW/f'exec25_pydyn_{key}_commit.json','Pinned revision and date'))
        if key!='statsmodels':evidence.append(ref(RAW/f'exec25_pydyn_{key}_tree.json','Complete pinned tree'))
    evidence.extend([ref(RAW/'exec20_pyfx_statsmodels_tree.json','Matching complete statsmodels tree'),ref(ROOT/'docs/program/execution/2026-10-24/pydynpd-reuse-v1/review.json','Preserved dynamic-panel source/paper review')])
    result=dict(status='pass',count=38,originals=originals,evidence=evidence)
    verify_bindings(result);write(BASE/'authenticated-originals.json',result)

def prepare():
    assert not (BASE/'review.json').exists()
    fragments=[];sources=[]
    for key,(title,repo,version,checks) in SPECS.items():
        evidence=[];anchors=[];claims=[]
        for stem,lo,hi,tokens,finding in checks:
            p=RAW/(stem+'.txt');lines=p.read_text().splitlines();hi=min(hi,len(lines));s='\n'.join(lines[lo-1:hi]);assert all(t in s for t in tokens),(stem,lo,hi,[t for t in tokens if t not in s])
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=key,source=binding,first_line=lo,last_line=hi,text=s))
        sources.append(dict(integrated_citation_key='exec25_pydyn_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][-4:]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[0],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    authenticate();write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=len(fragments)))
    write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_pydyn_search*.json')):
        if 'receipt' in p.name:continue
        d=read(p);r=p.with_suffix('.receipt.json');q=read(r)
        for x in d['items']:leads.setdefault(x['full_name'],dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected'))
        queries.append(dict(query=q['url'],total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(r,'Query identity'),reliance='No absence or saturation; abbreviated SVAR search includes unrelated structural-variation/classification results.'))
    for name in ['patricioariaslpz/macroshock','Kahindo048/pyxtabond2','Leotaby/dynapanel']:
        if name in leads:leads[name]['status']='selected_primary_anchors_only'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),additional_named_candidates=['statsmodels/statsmodels','wwrechard/pydlm','dazhwu/pydynpd'],saturation_claim=False,absence_claim=False,excluded_metadata_lead='bth-dipt-research/SVAR selected tree concerns classifiers,not structural vector autoregression; no technical causal claim imported'))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Authenticated originals and exact anchors') for n in ['authenticated-originals.json','inspected-extracts.json']],groups=5,anchors=len(fragments),native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Independent rational/indexing reference'),ref(BASE/'exact-results.json','Exact replay')],checks=['Calendar lag differs from previous-observation lag at a gap.','Orthogonal rational rotation preserves covariance while changing shock responses.','Dense B squared determinant9/16 differs from elementwise-square determinant15/16.','Matched proxy dot70 differs from suffix dot80; matrix reset trace retains last column.','Own-variable impact1 with diagonal2 requires structural amplitude1/2.','Missing-state variance2 differs from separately stipulated fixed-innovation variance3.','Hypothetical costs40/60/80 retain all denominators.'],native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Branch dynamic-panel intervention,aggregate funding shock and adjacent state forecast',selected=['pydynpd inherited','statsmodels VAR/SVAR','PyXtabond2','dynapanel','macroshock','PyDLM'],decisions=['Conditional panel references require explicit calendar and instrument law.','Use reduced-form VAR as baseline; structural paths require independently justified restrictions/objective.','Defer macroshock integration pending proxy,normalization and bootstrap-state qualification.','Treat PyDLM as adjacent forecasting under a declared innovation and feature-clock law.'],limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Retained original notices'),ref(ROOT/'docs/program/execution/2026-10-24/statsmodels-reuse-v1/review.json','Inherited distribution audit')],findings=['PyXtabond2,dynapanel and macroshock original MIT notices retained.','PyDLM BSD source/setup retained.','statsmodels distribution review preserved.','No wheel,all-dependency or current commercial-support qualification.'],integration_allowed=False))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=['Calendar gaps,duplicates,fractional times and panel-row identity','Dynamic-panel moment validity,instrument count/rank and shared shocks','Structural mask objective,rotations,optimizer diagnostics and weak identification','Missing proxy rows,multiple instruments and own-variable shock normalization','Bootstrap attempt caps,small requests,seed,state mutation and unavailable zero summaries','Missing-step innovation and future-feature availability','Numerical fallback,clipped variance and exact artifact/dependency custody','Complete request,completion,accepted-output and cost denominators'],owners=['Scientific author','Adapter owner','Environment/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded searches and tails')],known_routes=['Complete primary delegates and exact package artifact provenance.','Preregister matched public known-law trials before expensive bank experiments.','Preserve unsupported-target and numerical/refusal states.'],unknown_universal_repairs=['Instrument exclusion and bank assignment truth require information or restrictions.','No universal repair for unrestricted dynamic dependence or latent identification.'],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_pydyn_choice',kind='project_evidence_not_scholarly_paper',title='Authored Python dynamic-panel,structural-shock and state-forecast comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026;cutoff7 October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Calendar,shock identification,numerical objective,proxy alignment,innovation and costs',inspection='Author inspection')],supported_claims=['Exact authored witnesses and bounded candidate decisions','Explicit incomplete coverage and proposed public qualification'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=6,new_scholarly_pdfs=0,evidence=[ref(BASE/'authenticated-originals.json','38 authenticated new originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed planned and actual evidence') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['Preserve completed pydynpd and statsmodels reference work; authenticate38 new files.','Five software collections and one authored comparison; no scholarly theorem imported.','Separate predictive,structural and panel targets; retain calendar,proxy and innovation boundaries.','Serial canonical publication after Java IV/RD delivery.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking targets and substantive alternatives'),ref(BASE/'sponsor-addition.md','Investment decision')],findings=['Source predicates, authored witnesses and proposed native evidence separated.','Declared innovation law and structural restrictions remain part of the target.','Search tails and whole-ecosystem coverage remain open.'],visual_acceptance=False))
    names=['authenticated-originals.json','primary-review.json','comparison-review.json','mathematical-review.json','exact-results.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Reviewed bounded coverage') for n in names]+[ref(Path(__file__),'Review logic')],findings=['38 new originals and inherited dynamic-panel references authenticated.','Five source collections and one authored comparison preserve scientific and implementation limits.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=38,anchors=len(fragments),unique_leads=len(leads),new_records=6,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Selected Python dynamic candidates identified; search/delegate and native coverage incomplete.','Technical claims bind authentic dated bytes and exact inspected anchors; no new scholarly theorem.','Alternatives and concrete public qualification routes retain numerical,rights and native limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Python dynamic-panel/time-series source comparison and public qualification contracts',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Python dynamic inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
