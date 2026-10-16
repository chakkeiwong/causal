#!/usr/bin/env python3
"""Bounded primary-source review and exact references; no upstream execution."""
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-15/java-temporal'
RAW = ROOT / 'docs/literature/raw'
OP = 'SW.CELL.discovery_temporal_interventional.Java'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/coverage-review.json')
AUDIT = ROOT / 'docs/program/execution/2026-10-15/latent-temporal/publication/reader/source-audit.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Cutoff 2026-10-07; four bounded searches are not an exhaustive Java temporal/interventional census.',
    'Thirty-one pinned source/document blobs support selected static findings; no upstream Java build, import or performance trial.',
    'learnDBN/learnDBM algorithm papers, official BANJO release/rights and specialized temporal-FCI originals remain unresolved here.',
    'Historical package notices and selected build files do not close transitive rights, current maintenance, runtime or native equivalence.',
    'Lag construction, score aggregation, dynamic-network likelihood and EM do not establish intervention identification or calibrated dependent-sample uncertainty.',
    'Exact authored examples use stipulated laws and prices; no fitted discovery performance, bank validation or ROI.',
    'Whole-manuscript coverage/depth and sponsor reconciliation remain open; no automatic substantive-page credit.',
    'Six-image session allowance exhausted; text and bounds checks cannot close rendered visual acceptance.'
]

TREES = {
    'tetrad': 'v12_sw2_tetrad_tree', 'banjo': 'v12_exec13_java_banjo_tree',
    'weka': 'v12_exec13_java_weka_tree', 'learndbn': 'exec15_javatemporal_tree_learndbn',
    'learndbm': 'exec15_javatemporal_tree_learndbm', 'builder': 'exec15_javatemporal_tree_builder'}
COMMITS = {
    'tetrad': 'v12_sw_cutoff_commit_tetrad', 'banjo': 'v12_exec13_java_banjo_commit',
    'weka': 'v12_sw_cutoff_commit_weka', 'learndbn': 'exec15_javatemporal_commit_learndbn',
    'learndbm': 'exec15_javatemporal_commit_learndbm', 'builder': 'exec15_javatemporal_commit_builder'}

# Inclusive line anchors in unchanged upstream files, not agent summaries.
ANCHORS = {
 'tetrad_1': ([(375,448)], 'Row-position lag construction and temporal knowledge; this method has no physical timestamp or subject-boundary argument.'),
 'tetrad_2': ([(47,61),(80,130)], 'Eligible tabular wrappers lag each dataset before resampling, reset TIME_LAG and restore knowledge; other branches keep inputs and warn.'),
 'tetrad_3': ([(141,180)], 'IMaGES lags separate datasets, constructs component scores and the one-argument ImagesScore, then invokes BOSS with knowledge.'),
 'tetrad_4': ([(110,168),(208,234),(337,351),(374,409)], 'Constructor defaults to DATASET_WEIGHTED despite SAMPLE_UNIFORM comment; inverse-size effective weights, NaN propagation and mean sample-size accessor.'),
 'tetrad_5': ([(25,85)], 'InterventionalColumn stores value/status column metadata; this class alone does not establish target-aware score/identification support.'),
 'tetrad_6': ([(195,238),(499,554)], 'addEdge enforces selected directed temporal constraints and replicates edges; addDirectedEdge delegates directly and does not use that validation path; no PAG conversion guarantee.'),
 'tetrad_7': ([(120,145),(292,354)], 'Single/multiple bootstrap entry points use lag helper; per-dataset resampling and finally restoration do not implement a common-calendar covariance law.'),
 'tetrad_8': ([(101,150)], 'FCI wrapper lags input, applies chosen independence test, knowledge and replication settings; this is not a proof of specialized temporal-FCI validity.'),
 'tetrad_9': ([(90,165)], 'BOSS wrapper provides lag/knowledge/permutation-search configuration; source flags are not intervention truth or uncertainty calibration.'),
 'tetrad_10': ([(18,87)], 'Saved SvarFCI help describes lag order, repeated structure and contemporaneous allowance; a help page is not proof of a matching current algorithm or theorem.'),
 'banjo_1': ([(1,48)], 'Modified gene/pseudotime application, distinct from official BANJO release and physical bank time.'),
 'banjo_2': ([(54,78),(90,97)], 'Example uses discretization i2, lag one only, mandatory identity lag, five parents and five-minute search budget.'),
 'banjo_3': ([(1,16),(563,626),(724,749),(1010,1034)], 'Restrictive Duke notice; discrete parent-configuration count score and positive equivalent sample size setting.'),
 'banjo_4': ([(467,483),(583,619)], 'Usable rows subtract maximum lag per file; lag windows remain inside each source file.'),
 'banjo_5': ([(1,16),(265,324),(357,368)], 'Mandatory identity edges and lag-zero cycle/constraint checks; restrictions are supplied search constraints.'),
 'weka_1': ([(4,38),(45,70)], 'Declared forecasting package1.0.27 dated2019-10-25, GPL3, regression/lag/calendar wrapper and dependency declarations.'),
 'weka_2': ([(24,28),(63,94),(1668,1713)], 'TSLagMaker imports classifiers.timeseries.core translator, copies attributes and invokes negative instance shifts.'),
 'weka_3': ([(118,179)], 'Separate generic unsupervised translator; must not be substituted for the imported forecasting-core class.'),
 'weka_4': ([(124,159)], 'Actual forecasting-core translator copies selected historical values or missing values and retains output-format dataset.'),
 'weka_5': ([(420,479)], 'Actual forecasting-core base shifts history by instance count; selected buffer method has no subject/time argument.'),
 'learndbn_1': ([(1,6)], 'README declares tDBN,cDBN,bcDBN,missing-value support and DBM clustering; performance/theorem qualification not inspected.'),
 'learndbn_2': ([(1,17),(60,98)], 'Apache2 license text; repository license does not close dependency or deployment review.'),
 'learndbn_3': ([(40,97),(104,201)], 'Stationary CLI default,LL/MDL choice and literal true on missing-data EM/score paths; compact display excludes intra-slice edges.'),
 'learndbn_4': ([(241,281),(844,893),(968,985)], 'Subject/time input schema,process exit on malformed headers,combinatorial fill allocation and stationarity-dependent transition selection.'),
 'learndbn_5': ([(95,108),(344,414)], 'Nonstationary scores allocate one matrix per transition; toDBN constructs one network per matrix.'),
 'learndbn_6': ([(61,103),(118,140)], 'Stationary parameter-learning rejects multiple transition networks; EM loops while strict score improvement without explicit step cap in selected method.'),
 'learndbm_1': ([(1,6)], 'Related dynamic multinet implementation and separate project website; not automatically an independent algorithm family.'),
 'learndbm_2': ([(1,17),(60,98)], 'Apache2 license text, byte-identical to selected learnDBN license.'),
 'learndbm_3': ([(27,61),(89,110)], 'Cluster-count CLI calls MultiNet.clust with supplied stationarity flag; inner clustering code uninspected.'),
 'builder_1': ([(1,1)], 'Author describes graduate research code requiring major refactoring/documentation.'),
 'builder_2': ([(43,107)], 'EM parameter-learning entry point takes a supplied model,defaults to1000 steps and tolerance0.0001,logs nonconvergence.'),
}


def exact():
    dates = [0,1,4,5]
    row_pairs = list(zip(dates,dates[1:])); day_pairs = [(a,b) for a,b in row_pairs if b-a==1]
    assert len(row_pairs)==3 and len(day_pairs)==2
    series = [[1,2,3],[10,20,30]]
    separate = [list(pair) for s in series for pair in zip(s,s[1:])]
    joined = sum(series,[]); pooled = [list(x) for x in zip(joined,joined[1:])]
    assert len(separate)==4 and len(pooled)==5 and [3,10] not in separate
    original=[10,20,30]; shuffled=[original[i] for i in [2,0,1]]
    fabricated=list(zip(shuffled,shuffled[1:])); valid=list(zip(original,original[1:]))
    assert (30,10) in fabricated and (30,10) not in valid
    # Independent finite-law enumerations check analytic covariance calculations.
    means=[]
    for eps in itertools.product([-1,1],repeat=5):
        means.append(F(sum(eps[t]+eps[t-1] for t in range(1,5)),4))
    temporal=sum(v*v for v in means)/len(means)
    assert temporal==F(7,8)==F(4*2+2*3,16)
    # Five common Rademacher shocks of amplitude2,20 independent unit shocks.
    calendar_common=sum((F(sum(2*x for x in e),5))**2 for e in itertools.product([-1,1],repeat=5))/32
    calendar=calendar_common+F(1,20)
    assert calendar==F(17,20) and calendar/F(5,20)==F(17,5)
    sizes=[1000,100];mean_size=F(sum(sizes),2)
    unnormalized=[mean_size/n for n in sizes];weights=[x/sum(unnormalized) for x in unnormalized]
    score=sum(w*d for w,d in zip(weights,[100,-20]));assert weights==[F(1,11),F(10,11)] and score==F(-100,11)
    target_volume=F(1000-200,1100);target_branch=F(1-2,2)
    net_volume=20*target_volume-8;net_branch=20*target_branch-8
    assert target_volume==F(8,11) and net_volume==F(72,11) and net_branch==-18
    # Observational treatment choice is associated with hidden risk,with positivity.
    law=[]
    for u in [0,1]:
        for e,p in [(0,F(3,4)),(1,F(1,4))]:law.append((u^e,u,p/2))
    cond=[sum(y*p for a,y,p in law if a==v)/sum(p for a,y,p in law if a==v) for v in [0,1]]
    assert cond==[F(1,4),F(3,4)]
    return {
      'scope':'Exact authored finite laws and selected literal branch reasoning;no upstream Java execution',
      'calendar_lags':{'dates':dates,'row_pairs':[list(x) for x in row_pairs],'one_day_pairs':[list(x) for x in day_pairs]},
      'series_boundaries':{'series':series,'separate_transitions':separate,'pooled_transitions':pooled,'false_boundary':[3,10]},
      'bootstrap_order':{'original':original,'resampled_indices':[2,0,1],'fabricated_pairs':[list(x) for x in fabricated],'valid_pairs':[list(x) for x in valid],'tuple_resampling_guarantees_calibration':False},
      'dependent_mean':{'law':'Z_t=eps_t+eps_(t-1);iid unit-variance Rademacher errors;n4','enumerated_atoms':32,'true_mean_variance':str(temporal),'iid_approximation':'1/2'},
      'common_calendar':{'branches':4,'dates':5,'common_shock_variance':4,'idiosyncratic_variance':1,'true_grand_mean_variance':str(calendar),'iid_20_row_variance':'1/4','variance_ratio':'17/5'},
      'images_weights':{'sample_sizes':sizes,'score_differences':[100,-20],'default_effective_weights':[str(x) for x in weights],'default_difference':str(score),'plain_average':40,'getSampleSize':550,'total_rows':1100,'actual_search_graphs_asserted':False},
      'target_economics':{'branch_effects':[1,-2],'branch_volumes':sizes,'customer_weighted_effect':str(target_volume),'equal_branch_effect':str(target_branch),'USD_per_effect_unit':20,'USD_cost_per_action':8,'customer_target_net_USD':str(net_volume),'branch_target_net_USD':str(net_branch),'observed_bank_prices':False},
      'missing_nonstationary_path':{'requested_stationary':False,'transition_networks_if_two_transitions':2,'missing_path_stationary_argument':True,'learnParameters_when_reached':'IllegalArgumentException','earlier_fill_uses_network':0,'first_runtime_failure_asserted':False},
      'prediction_and_intervention':{'law':'U~Bernoulli(1/2);E~Bernoulli(1/4) independent;A=U xor E;Y=U','joint_A_Y_probability':[{'A':a,'Y':y,'p':str(p)} for a,y,p in law],'conditional_means':[str(v) for v in cond],'conditional_contrast':'1/2','do_contrast':0,'USD_per_outcome':20,'USD_action_cost':8,'conditional_proxy_net_USD':2,'true_intervention_net_USD':-8}
    }


def primary():
    requests=[]
    for name in ['acquisition-plan','candidate-source-plan','callchain-plan','calltarget-repair-plan']:
        requests += [r for r in json.loads((BASE/(name+'.json')).read_text())['requests'] if 'package' in r]
    assert len(requests)==len(ANCHORS)==31
    packages={};records=[]
    for pkg,stem in TREES.items():
        tree=json.loads((RAW/(stem+'.json')).read_text());assert tree.get('truncated') is False
        commit=json.loads((RAW/(COMMITS[pkg]+'.json')).read_text());commit=commit[0] if isinstance(commit,list) else commit
        assert commit['sha']==tree['sha'] and commit['commit']['committer']['date'][:10]<='2026-10-07'
        packages[pkg]={'revision':commit['sha'],'source_date':commit['commit']['committer']['date'],
          'tree':ref(RAW/(stem+'.json'),'Complete pinned tree'),'commit':ref(RAW/(COMMITS[pkg]+'.json'),'Cutoff-compatible revision')}
    for req in requests:
        suffix=req['id'].removeprefix('exec15_javatemporal_');spans,claim=ANCHORS[suffix]
        p=RAW/(req['id']+'.txt');raw=p.read_bytes();sha=hashlib.sha256(raw).hexdigest()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        pkg=req['package'];tree=json.loads((RAW/(TREES[pkg]+'.json')).read_text())
        entry=next(x for x in tree['tree'] if x['path']==req['source_path'])
        assert req['pin']==tree['sha'] and blob==req['blob_sha1']==entry['sha']
        receipt_path=RAW/(req['id']+'.receipt.json');receipt=json.loads(receipt_path.read_text())
        assert receipt['sha256']==sha and receipt['status'] in ['saved','cached'] and receipt['url']==req['url']
        try:lines=raw.decode('utf-8').splitlines();encoding='utf-8'
        except UnicodeDecodeError:lines=raw.decode('latin1').splitlines();encoding='latin1 for inspection; original bytes unchanged'
        spans=[(a,min(b,len(lines))) for a,b in spans];assert all(0<a<=b for a,b in spans)
        anchors=[{'start':a,'end':b,'text':'\n'.join(lines[a-1:b])} for a,b in spans]
        records.append({**req,'version_date':packages[pkg]['source_date'],'local_copy':ref(p,'; '.join(f'lines{a}-{b}' for a,b in spans)),
           'receipt':ref(receipt_path,'Acquisition identity and SHA256'),'git_blob_sha1':blob,'inspection_encoding':encoding,
           'inspected_anchors':anchors,'supported_claims':[claim]})
    a=json.loads((RAW/(TREES['learndbn']+'.json')).read_text());b=json.loads((RAW/(TREES['learndbm']+'.json')).read_text())
    def idx(t):return {x['path']:x['sha'] for x in t['tree'] if x['type']=='blob' and x['path'].startswith('src/dbn/')}
    x,y=idx(a),idx(b);same=sorted(p for p in x.keys()&y.keys() if x[p]==y[p])
    assert len(x)==len(y)==17 and len(same)==15
    overlap={'shared_paths':17,'identical_blobs':15,'identical_paths':same,'nonidentical_paths':sorted((x.keys()&y.keys())-set(same)),
        'interpretation':'Related source families; do not transfer a CLI finding to a different caller or equate the two Observations implementations.'}
    return {'cutoff':'2026-10-07','packages':packages,'sources':records,'dbn_dbm_overlap':overlap,'upstream_execution':False,'limitations':LIMITS}


def candidates():
    items=[];queries=[]
    for name in ['repos_temporal','repos_dynamic','papers_svar','papers_java']:
        p=RAW/('exec15_javatemporal_'+name+'.json');data=json.loads(p.read_text())
        receipt=RAW/('exec15_javatemporal_'+name+'.receipt.json');meta=json.loads(receipt.read_text())
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
        rows=data.get('items',data.get('results',[]));assert len(rows)<=10
        queries.append({'name':name,'query':meta['url'],'accessed_utc':meta['accessed_utc'],'returned':len(rows),
          'reported_total':data.get('total_count',data.get('meta',{}).get('count')),'raw':ref(p,'Complete saved bounded search page'),
          'receipt':ref(receipt,'Search access date and bytes'),'stop_rule':'One page, at most10 results; no saturation or absence claim.'})
        for row in rows:
            identity=row.get('full_name',row.get('display_name'));disposition='Unreviewed candidate; acquire cutoff-compatible primary source and rights before any capability claim.'
            if identity in ['SSamDav/learnDBN','SSamDav/learnDBM','selrach/BayesNetBuilder']:
                disposition='Selected pinned source review below; native and wider rights closure remain open.'
            elif identity in ['microsoft/reliableAI','jdellert/aitiotita']:
                disposition='Inherited Java discovery review exists; a temporal or target-aware interventional path is not established by this search hit.'
            elif identity=='kvb2univpitt/causal-experiment':disposition='Experiment-collection lead; no independent Java temporal backend qualification.'
            elif identity=='tyler-lovelace1/tetrad-censored':disposition='Tetrad derivative alias; censoring and temporal/interventional code delta require independent inspection.'
            elif identity.startswith('LUCID:'):disposition='Authentic original already reviewed in latent-temporal synthesis; this metadata hit does not establish Java implementation.'
            elif not name.startswith('repos'):disposition='Scholarly discovery lead only; genuine original and Java linkage not established in this cell; no technical citation added.'
            items.append({'identity':identity,'source_url':row.get('html_url',row.get('doi') or row.get('id')),
              'date':row.get('publication_date',row.get('created_at')),'query':name,'disposition':disposition})
    for repo,aliases in [('cmu-phil/tetrad',['TETRAD','py-tetrad bridge','IMaGES','BOSS','FCI','SvarFCI help']),
        ('daniel-315/slingshot-modified-banjo',['BANJO derivative','original Duke BANJO is a distinct release/rights question']),
        ('Waikato/weka-3.8',['Weka','timeseriesForecasting','TSLagMaker','core and generic TimeSeriesTranslate are distinct classes'])]:
        items.append({'identity':repo,'aliases':aliases,'query':'Inherited Java evidence and complete pinned tree',
            'disposition':'Selected temporal source review; do not infer modern release completeness or runtime qualification.'})
    assert len(items)==19
    return {'cutoff':'2026-10-07','queries':queries,'items':items,'coverage_closed':False,
      'omissions':['Uninspected search leads remain candidates, not rejected software or evidence of absence.',
        'Official BANJO original distribution/license and algorithm papers for learnDBN/learnDBM require acquisition before theorem/performance claims.',
        'Saved SvarFCI help and current FCI wrapper are not automatically the same algorithm; original temporal theorem and matched implementation unresolved.',
        'OpenMarkov,UnBBayes,Bayes Server and other commercial Java interfaces are adjacent discovery leads; not covered by these four queries or erased by an empty result.',
        'No general target-aware interventional Java absence claim; pooled observational scores and metadata are insufficient positive evidence.',
        'Dynamic-network maintenance,complete dependencies,missing-data law,EM initialization/termination and scale require prototype review.']}


def contract():
    return {'status':'proposed_not_implemented','native_execution':False,
      'reuse':{
        'tetrad':'Retain backend-adapter candidate; preserve endpoint pairs,lags,knowledge and weights. Defer code port pending GPL/dependency review and native comparison; general PAG/effect promises rejected.',
        'banjo':'Reference-only modified mirror; no direct commercial adoption or source port under unresolved restrictive rights. Independent boundary/configuration ideas are useful; resolve official version and discreteness assumptions.',
        'weka':'Forecast/preprocessing comparator under declared package/GPL scope; retain original clocks,series and transformations. Do not register as causal temporal/interventional estimator.',
        'learndbn':'Conditional isolated-worker prototype for discrete longitudinal structure learning after license/dependency review. Reject default adoption until stationarity flag,process exit,EM budget and graph export defects/limits are addressed.',
        'learndbm':'Related clustering comparator,not an independently qualified causal regime learner; inspect MultiNet internals and membership/uncertainty before enabling.',
        'builder':'Reference candidate for model-supplied EM only; direct integration/port deferred for unresolved rights,maintenance and native behavior.'},
      'request':['Unit and series identity,event/availability clocks,calendar and timezone,lag units and admissible windows',
        'Variables,categories,missingness law,train-only transformation policy,stationarity and contemporaneous restrictions',
        'Regime identity,known intervention target/type,assignment evidence,unchanged-mechanism assumptions and estimand population',
        'Pinned source/runtime/dependency identities,score mode/effective weights,randomization and computational budgets'],
      'response':['Typed lagged graph with original endpoint pairs; separate visualization projection',
        'Actual window/series/calendar counts,component sample sizes and weights; never invent total sample size from mean accessor',
        'Selected graph versus graph-family uncertainty versus effect identification/coverage separately',
        'Warnings,unsupported conditions,nonconvergence and backend process failure retained in result denominator'],
      'failures':{'irregular_or_cross_series_lag':'temporal_contract_mismatch','unknown_intervention_assignment':'intervention_unverified',
        'missing_nonstationary_unsupported':'unsupported_regime_combination','process_exit':'backend_failed',
        'unbounded_or_exhausted_EM':'budget_exhausted','nonfinite_score':'score_undefined','PAG_to_directed_graph':'lossy_graph_conversion',
        'unknown_rights':'reuse_not_cleared','no_dependent_coverage':'uncertainty_unqualified'},
      'repair_sequence':['Write a clock/series/regime validator and lossless endpoint/lag contract before connecting backends.',
        'Make Tetrad weighting explicit; verify individual sample-size fields and calibrated uncertainty independently.',
        'For learnDBN propagate the actual stationarity flag through all missing-data calls or refuse that combination; replace System.exit at library boundary or isolate worker.',
        'Add iteration,allocation,timeout and numerical-status limits to EM; preserve intra-slice edges outside compact display.',
        'Review licenses and complete environments before source adoption/port; run native golden cases only in a prospective prototype.'],
      'public_generated_comparison':{'status':'prospective_design_not_registered_or_executed','independent_units':'Entire generated mechanisms/trajectories; shared-calendar clusters kept together',
        'arms':['Restricted native Tetrad','Repaired restricted learnDBN','Forecast-only Weka','Exact small oracle','No-discovery conservative decision'],
        'strata':['Regular/irregular clocks','One/multiple series','Common shocks','Stationary/changed mechanisms','Missingness/positivity','Observed/hidden common causes','Documented versus guessed intervention targets'],
        'public_data_role':'Realistic calendars,missingness and documented public assignments; a public observation or forecast label is not causal gold.',
        'metrics':['Window and endpoint fidelity','Failure/refusal counts','Graph-class retention where known','Identified-set/effect coverage and width under a justified law','Decision loss and full cost'],
        'freeze_before_study':['Source/env/settings/input identities','Pilot-informed fixed replications and stopping rule','Separate tuning/evaluation mechanisms','All failed requests retained','Actual cost and uncertainty estimands']},
      'open_research':['Dependent graph-family retention with shared calendars and hidden causes','Useful effect bounds across observationally equivalent models','Intervention invariance/assignment truth and selection; public evidence only resolves documented cases'],
      'integration_allowed':False}


def main():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    assert not (BASE/'primary-review.json').exists()
    p=primary();c=candidates();d=contract()
    write(BASE/'primary-review.json',p);write(BASE/'candidate-register.json',c)
    write(BASE/'exact-results.json',exact());write(BASE/'reuse-and-prototype-contract.json',d)
    added=[]
    for pkg,info in p['packages'].items():
        rows=[r for r in p['sources'] if r['package']==pkg];repo=rows[0]['repository']
        added.append({'integrated_citation_key':'exec15_javatemporal_'+pkg,'kind':'software_primary_sources','author':repo,
          'title':repo+' pinned temporal data,learning and reuse source review','year':int(info['source_date'][:4]),
          'version_date':info['source_date']+';revision '+info['revision']+';inspected2026-10-15',
          'source_identity':'https://github.com/'+repo,'local_copy':ref(BASE/'primary-review.json','Package '+pkg+' and explicit line anchors'),
          'inspected_anchors':[r['source_path']+': '+r['local_copy']['anchor'] for r in rows],
          'supported_claims':[r['supported_claims'][0] for r in rows],'records':rows,'identity_record':info,'limitations':LIMITS})
    for key,title,kind,local,claims in [
      ('exact','Exact Java temporal calendar,dependence,weighting and decision references','project_derivation',BASE/'exact-results.json',
       ['Nine exact reference families;original finite-law enumeration and source-branch reasoning;no upstream execution']),
      ('design','Java temporal reuse decisions and proposed public/generated comparison','project_design',BASE/'reuse-and-prototype-contract.json',
       ['Conditional retain,reference-only and reject-default decisions;typed temporal/regime failures and prototype route;not an enabled integration'])]:
        added.append({'integrated_citation_key':'exec15_javatemporal_'+key,'kind':kind,'author':'Causal banking proposal','title':title,
          'year':2026,'version_date':'2026-10-15','source_identity':'Project-authored '+kind,'local_copy':ref(local,title),
          'inspected_anchors':[title],'supported_claims':claims,'records':[{'local_copy':ref(Path(__file__),'Exact calculation and review logic')},
             {'local_copy':ref(BASE/'candidate-register.json','All19 candidates/aliases and bounded omissions')}],'limitations':LIMITS})
    write(BASE/'source-audit.json',{'sources':added,'prior':ref(AUDIT,'626 preserved citation records'),'cutoff':'2026-10-07'})
    tex=(BASE/'development.template').read_text().replace('§',chr(92));(BASE/'development.tex').write_text(tex)
    evidence=[ref(path,anchor) for path,anchor in [
      (BASE/'primary-review.json','31 source blobs match exact complete trees and acquisition hashes'),
      (BASE/'candidate-register.json','Four bounded searches,19 candidates/aliases and explicit omissions'),
      (BASE/'exact-results.json','Nine exact reference families'),(BASE/'reuse-and-prototype-contract.json','Concrete reuse and repair decisions'),
      (BASE/'source-audit.json','Eight new citation records'),(BASE/'development.template','Connected proposal development'),
      (BASE/'inspection-repairs.json','Preserved class-selection and encoding repairs'),(Path(__file__),'Reproducible primary review and exact calculations')]]
    for e in evidence:verify_bindings(e)
    findings=[
      'All19 returned/inherited candidates and aliases have bounded dispositions;four searches and selected trees do not close wider temporal/interventional Java census.',
      '31 authentic source/document blobs match Git tree and fetch identities with cutoff-compatible dates and technical anchors;no new scholarly technical result is cited without an original.',
      'Six repository decisions distinguish lag construction,forecasting,structure learning,clustering and intervention identification. Exact laws and source paths motivate typed repairs;rights,theorem,runtime and coverage omissions remain explicit.']
    write(OUTPUT,{'operation':OP,'outcome':'inconclusive','scope':'Bounded Java temporal/interventional software coverage and proposal synthesis',
      'findings':findings,'evidence':evidence,'candidate_count':19,'source_blob_count':31,'upstream_execution':False,
      'coverage_closed':False,'integration_allowed':False,'limitations':LIMITS})
    write(BASE/'author-review.json',{'status':'pass','scope':'Author technical review;coverage outcome remains inconclusive',
      'reviewer':REVIEWER,'findings':findings,'evidence':evidence+[ref(OUTPUT,'Contracted scoped coverage output')],
      'limitations':LIMITS,'visual_acceptance':False})
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope='Bounded primary-source Java temporal/interventional proposal comparison',
      reviewer=REVIEWER,limitations=LIMITS,outputs=[ref(OUTPUT,'Reviewed bounded coverage')],nonexecution_reason='',capabilities=[],
      revisit_trigger='Broader candidate search,missing originals,official release/rights or qualified native prototype supplies additional evidence.',
      criteria=[{'index':i,'verdict':'inconclusive' if i==0 else 'pass','finding':f,'evidence':evidence} for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'technical_review':'pass','coverage':'inconclusive','source_blobs':31,'candidates':19,'new_records':8,'exact_references':9}))


if __name__=='__main__':main()
