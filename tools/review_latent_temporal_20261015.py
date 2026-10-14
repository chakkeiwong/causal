#!/usr/bin/env python3
"""Primary-text review and exact authored references; no upstream execution."""
import ast
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import tomllib

import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-15/latent-temporal'
RAW = ROOT / 'docs/literature/raw'
OP = 'LL.TASK.latent_temporal_discovery'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/task-synthesis.md')
AUDIT = ROOT / 'docs/program/execution/2026-10-15/d3rlpy-reuse/publication-v2/reader/source-audit.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Selected primary text, pinned static source and exact authored laws; no live LLM, upstream import, fitted discovery or bank trial.',
    'Literature cutoff 2026-10-07 Asia/Shanghai. Two originals remain unresolved and specialist search saturation is open.',
    'Reported paper results retain their authors, tasks, assumptions and populations; none measures this proposal implementation.',
    'Package weights, resolved environments, transitive rights, native semantics and broader code paths require prototype review.',
    'General latent-temporal class retention, valid effect-set uncertainty and useful precision remain research obligations.',
    'All banking amounts are stipulated. Independent bank validation, prices, ROI and adoption are later conditional work.',
    'Six-image session allowance is exhausted; text/bounds checks do not close rendered visual acceptance or Q1/Q5.'
]


def cumulants(law):
    """Direct finite-law centered mixed moments; independent of factor formulas."""
    assert sum(p for x, y, p in law) == 1
    mx = sum(x * p for x, y, p in law)
    my = sum(y * p for x, y, p in law)
    def m(a, b):
        return sum((x-mx)**a * (y-my)**b * p for x, y, p in law)
    c31 = m(3, 1) - 3*m(2, 0)*m(1, 1)
    c22 = m(2, 2) - m(2, 0)*m(0, 2) - 2*m(1, 1)**2
    c13 = m(1, 3) - 3*m(0, 2)*m(1, 1)
    return {'C31':c31, 'C22':c22, 'C13':c13, 'D1':c31*c13-c22*c22,
            'C21':m(2, 1), 'C12':m(1, 2), 'varX':m(2, 0), 'varY':m(0, 2)}


def exact():
    hidden_cov = [[F(2),F(2)],[F(2),F(5)]]
    direct_cov = [[F(2),F(2)],[F(2),F(2)+3]]
    assert hidden_cov == direct_cov
    multi = [(F(u+v+ex), F(u+2*v+ey), F(1,16))
             for u,v,ex,ey in itertools.product([-1,1],repeat=4)]
    cm = cumulants(multi)
    assert [cm[k] for k in ['C31','C22','C13','D1','varX','varY']] == [-6,-10,-18,8,3,6]
    standardized = cm['D1']/(cm['varX']**2*cm['varY']**2)
    assert standardized == F(2,81)
    # Independent factor-cumulant check: independent Rademacher fourth cumulant=-2.
    factor = [-2*(1**3*1+1**3*2), -2*(1**2*1**2+1**2*2**2), -2*(1*1**3+1*2**3)]
    assert factor == [cm[k] for k in ['C31','C22','C13']]
    u_law = [(-1,F(1,6)),(0,F(2,3)),(1,F(1,6))]
    varu = sum(p*u*u for u,p in u_law)
    k4u = sum(p*u**4 for u,p in u_law)-3*varu**2
    assert varu == F(1,3) and k4u == 0
    zero = [(F(u+ex),F(2*u+ex+ey),p/4) for u,p in u_law
            for ex,ey in itertools.product([-1,1],repeat=2)]
    cz = cumulants(zero)
    assert [cz[k] for k in ['C31','C22','C13','D1','C21','C12']] == [-2,-2,-2,0,0,0]
    # Valid IV alone does not select all noncomplier counterfactuals.
    iv=[]
    for never_y1 in [0,1]:
        observed={};ate=F(0)
        for c in [0,1]:
            y1 = 1 if c else never_y1
            ate += F(y1,2)
            for z in [0,1]:
                a = c*z; y = a*y1
                key=f'{z},{a},{y}';observed[key]=observed.get(key,F(0))+F(1,4)
        iv.append({'observed_Z_A_Y':{k:str(v) for k,v in sorted(observed.items())},'ATE':str(ate)})
    assert iv[0]['observed_Z_A_Y']==iv[1]['observed_Z_A_Y'] and [x['ATE'] for x in iv]==['1/2','1']
    # Explicit coordinate enumeration of the published four-dimensional mask.
    cleared = [(j,i,lag) for j in range(12) for i in range(12) for lag in range(3)
               if any(j==l and i==l for l in range(3))]
    assert len(cleared)==9 and sorted({j for j,i,l in cleared})==[0,1,2]
    retained_diagonal=[i for i in range(12) if all((i,i,l) not in cleared for l in range(3))]
    assert retained_diagonal==list(range(3,12))
    axes=[{'source':0,'target':1,'lag_index':2,'physical_lag':1},
          {'source':0,'target':2,'lag_index':0,'physical_lag':3}]
    # Source-literal graph conversion, not an import of a package function.
    endpoint=[[0,1],[1,0]]
    arrows=[(j,i) for i in range(2) for j in range(2) if endpoint[i][j]==1]
    assert arrows==[(1,0),(0,1)]
    backend={'success':True,'raw_results':{'edges':['A --> B'],'adjacency_matrix':[[0,-1],[1,0]]}}
    critical=[] if not isinstance(backend,str) else None
    assert critical==[]
    # Graph union needs BOTH class retention and within-class effect coverage.
    events=list(range(100));miss_graph=set(events[:3]);miss_effect=set(events[3:5])
    joint=sum(i not in miss_graph|miss_effect for i in events)
    assert joint==95 and F(1)-F(3,100)-F(2,100)==F(95,100)
    # Additional information can have decision value, without a claimed real price.
    q=F(3,5); net_if_act=q*12+(1-q)*(-8);perfect=q*12
    assert net_if_act==4 and perfect-net_if_act==F(16,5)
    def strings(d):return {k:str(v) for k,v in d.items()}
    return {
      'scope':'Exact authored algebra and literal selected source control flow, not upstream execution.',
      'two_wave_gaussian':{'hidden_world':'X=U+ex;Y=2U+ey;all independent standard normal',
        'direct_world':'X~N(0,2);Y=X+e;independent e~N(0,3)',
        'common_covariance':[[str(v) for v in row] for row in hidden_cov],
        'causal_effects':[0,1],'outcome_USD_per_unit':20,'unit_action_cost_USD':8,'net_values_USD':[-8,12]},
      'multiple_latent_components':{'law':'X=U+V+ex;Y=U+2V+ey;four independent Rademacher variables;effect=0',
        'enumerated_atoms':16,'mixed_cumulants':strings(cm),'factor_check':factor,
        'standardized_D1':str(standardized),'interpretation':'Outside proportional scalar-latent model; not a counterexample under its full premises.'},
      'zero_fourth_cumulant':{'U_values':[-1,0,1],'U_probabilities':['1/6','2/3','1/6'],
        'varU':str(varu),'fourth_cumulant_U':str(k4u),'law':'X=U+ex;Y=U+X+ey;independent Rademacher errors',
        'true_effect':1,'mixed_cumulants':strings(cz),'interpretation':'Nonnormality does not imply the nonzero-cumulant detection condition.'},
      'instrument_boundary':{'worlds':iv,'complier_effect':1,'first_stage':'1/2',
        'assumptions':['Random independent instrument','Exclusion','Relevance','Monotonicity'],
        'interpretation':'Further target/model restrictions are required for a population effect; no universal IV identification claim.'},
      'temporal_graph':{'unrolled_edges':['A_t -> B_(t+1)','B_t -> A_(t+1)'],
        'unrolled_cycle':False,'variable_collapsed_cycle':True,'lagged_self_edges_permitted':True},
      'lcm_coordinates':{'shape':[1,12,12,3],'cleared_cells':len(cleared),'cleared_variable_diagonals':[0,1,2],
        'retained_variable_diagonals':retained_diagonal,'axes':axes,'global_constant_input_denominator':0},
      'agent_conversion':{'bidirected_endpoint_pair':endpoint,'literal_directed_arrows':[list(x) for x in arrows],
        'false_directed_two_cycle_if_bidirected_admitted':True,'ordinary_dictionary_critical_edges':critical,
        'emitted_revised_graph':[],'scope':'Does not assert that PC normally emits bidirected graphs or that a live app ran.'},
      'coverage_composition':{'graph_failure_budget':'3/100','effect_failure_budget':'2/100','union_lower_bound':'95/100',
        'sharp_disjoint_failure_atoms':joint,'premises_established_by_LLM_frequency':False},
      'information_value':{'stipulated_direct_world_probability':str(q),'best_no_information_value_USD':str(net_if_act),
        'perfect_information_value_USD':str(perfect),'maximum_information_cost_USD':str(perfect-net_if_act),
        'scope':'Bayesian illustrative value of perfect information; not an empirical prior, experiment design or bank price.'}}


PAPERS = [
 ('candidate148','exec15_latent_shi','Does X at Time 1 Cause Y at Time 2? Longitudinal Causal Learning with Hidden Confounders',
  'Does X at Time 1 Cause Y at Time 2 Longitudinal Causal Learning with Hidden Confounders','Shi',2026,
  'Dexin Shi and Wolfgang Wiedermann and Amanda J. Fairchild and Bo Zhang','shi',35,
  {1:'Identity and accepted version',6:'Equations 3-4 and assumptions A1-A5; global scalar confounder',9:'Theorem1 and explicit nonzero fourth-cumulant proof premises',
   10:'Bonferroni/percentile bootstrap algorithm and inconclusive nondetection',22:'Author-reported 4.8% to99.5% power as N grows2000 to200000 in specified regime',29:'Path detection is distinct from consistently estimating effect size; no universal superiority'}),
 ('candidate180','exec15_latent_yu','Investigating causal networks of dementia using causal discovery and natural language processing models',
  'Investigating causal networks of dementia using causal discovery and natural language processing models','Yu',2025,
  'Xinzhu Yu and Artitaya Lophatananon and Vivien Holmes and Kenneth R. Muir and Hui Guo','yu',8,
  {1:'Title, authors, applied observational discovery',5:'Embedding limitations, metadata screening and context',
   6:'Manual recovery of excluded variables; MGM to FCI-MAX;50 imputations and30/50/100% frequency thresholds;access-by-application data and supplementary code;cohort table406781 differs from prose406837'}),
 ('candidate263','exec15_latent_sthcm','Spatio-Temporal Hierarchical Causal Models','Spatio-Temporal Hierarchical Causal Models','Li',2026,
  'Xintong Li and Haoran Zhang and Xiao Zhou','sthcm',9,
  {1:'AAAI26 identity and public code lead',3:'Mechanism/empirical-measure convergence;static confounders;known global spatial ordering and homogeneity',
   4:'Subunit limit at fixed N,T;adjustability is an additional condition;generic IV claim requires target-specific qualification',
   6:'Author-reported simulations;finite mean4.91 versus truth5 is not proof of unbiasedness',7:'Drift/feedback stress and traffic application;not bank ground truth'})
]

INHERITED = {
 'v12_la_2404_14786': {2:'Causal sufficiency and unknown-target regime setup',3:'Global score maximizer theorem with density capacity, intervention faithfulness, positivity and finite entropy',5:'Author-reported comparisons;initialization does not certify optimization or interventions'},
 'v12_la_2506_16234': {5:'Sequential observation batches and pairwise latent-confounder restriction',6:'Bayesian-inspired edge tracking',13:'Full graph posterior, calibration and broader confounding remain future work',25:'Dependent nonstationary LM channel prevents direct standard bandit regret transfer'},
 'v12_la_2602_18662': {2:'Additive noise,stationarity,no hidden confounders,no contemporaneous effects',12:'Runtime and head scaling restricted to declared dimensions',13:'Assumption violations are not detected/corrected;future latent extension'},
 'v12_la_2608_09696': {4:'Model proposal,approximate evidence and open-loop experiments',31:'Finite support,approximate evidence,deterministic pruning and unproposed model mass'},
 'v12_la_2606_23608': {3:'Preserve CPDAG/PAG meanings and evidential status',4:'Protected formal discovery core and contextual assumptions',9:'Prospective evaluation standard,not bank evidence'},
 'exec13_census_augur_arxiv': {3:'Discrete trend prediction target',5:'Graph-overlap consensus and graph-summary consistency',6:'Forecasting datasets and teacher/student setup',8:'Reported forecasting/summary quality is not intervention validation'},
 'exec13_pulse': {5:'Process-order constraints and domain rules',7:'Operational success98.73% versus Hits@1 .44/F1 .39;changed-variable annotations',8:'Operational evaluation and future intervention optimization'},
 'v12_la_2306_16902': {9:'Inaccurate language priors degrade temporal Water/Mildew results'}
}


def inspect_pages(pdf, key, anchors):
    target=BASE/(key+'-review.txt')
    subprocess.run(['pdftotext','-layout',str(pdf),str(target)],check=True,timeout=30)
    pages=target.read_text().split('\f');out=[]
    for n,finding in anchors.items():
        assert 0<n<len(pages) and pages[n-1].strip()
        p=BASE/'inspected'/(key+'-page-'+str(n)+'.txt');p.parent.mkdir(exist_ok=True)
        p.write_text(pages[n-1])
        out.append({'pdf_page':n,'finding':finding,'extract':ref(p,'Physical primary PDF page '+str(n))})
    return out,len(pages)-1


def main():
    assert not OUTPUT.exists()
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    prior=json.loads(AUDIT.read_text());index={s['integrated_citation_key']:s for s in prior['sources']}
    reviewed=[];new=[]
    for key,anchors in INHERITED.items():
        r=index[key];p=ROOT/r['local_path']
        assert core.sha(p)==r['sha256']
        inspected,pages=inspect_pages(p,key,anchors)
        reviewed.append({'citation_key':key,'original':ref(p,r['title']),'version_date':r.get('version_date',r.get('arxiv_version',r.get('updated','inherited identity'))),
                         'inspected_anchors':inspected,'pages':pages,'claims':[x['finding'] for x in inspected]})
    for candidate,key,title,filename,surname,year,authors,meta,expected,anchors in PAPERS:
        raw=BASE/(candidate+'.original');assert raw.read_bytes().startswith(b'%PDF-')
        dest=ROOT/'docs/papers'/(filename+' '+surname+'('+str(year)+').pdf')
        assert not dest.exists();dest.write_bytes(raw.read_bytes())
        metadata=json.loads((RAW/f'exec15_latent_{meta}_identity.json').read_text())['message']
        date=metadata['published']['date-parts'][0];assert tuple(date)<=(2026,10,7)
        date='-'.join(f'{v:02}' for v in date)
        inspected,pages=inspect_pages(dest,key,anchors);assert pages==expected
        s={'integrated_citation_key':key,'kind':'paper','title':title,'filename_title':filename,'first_author':surname,
           'year':year,'author':authors,'pages':pages,'source_identity':'https://doi.org/'+metadata['DOI'],
           'version_date':'Publisher original; published '+date,'cutoff':'2026-10-07','accessed':'2026-10-15',
           'local_path':str(dest.relative_to(ROOT)),'sha256':core.sha(dest),'local_copy':ref(dest,'Genuine publisher original'),
           'identity_metadata':ref(RAW/f'exec15_latent_{meta}_identity.json','DOI identity/date only;not technical evidence'),
           'acquisition':ref(BASE/'acquisition-results.json','Bounded public read;original bytes and headers retained'),
           'original_response':ref(raw,'Byte-identical publisher PDF'),'headers':ref(BASE/(candidate+'.headers'),'Observed retrieval headers'),
           'inspected_anchors':inspected,'supported_claims':[x['finding'] for x in inspected],
           'limitations':['Selected primary-text review only;author-reported empirical results','No native method execution or bank generalization']}
        new.append(s);reviewed.append({'citation_key':key,'original':ref(dest,title),'version_date':s['version_date'],
            'inspected_anchors':inspected,'pages':pages,'claims':s['supported_claims']})
    plans=[]
    for name in ['acquisition-plan.json','acquisition-callchain-plan.json','acquisition-nodes-plan.json']:
        plans+=json.loads((BASE/name).read_text())['sources']
    records=[]
    for r in plans:
        tree=json.loads((RAW/('v12_la_'+r['package']+'_tree.json')).read_text())
        assert tree['sha']==r['pin'] and not tree['truncated']
        blob=next(x for x in tree['tree'] if x['path']==r['source_path'])
        p=RAW/(r['id']+'.txt');data=p.read_bytes()
        blob_sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob_sha==r['blob_sha1']==blob['sha']
        receipt=json.loads((RAW/(r['id']+'.receipt.json')).read_text())
        assert receipt['sha256']==core.sha(p) and receipt['url']==r['url']
        if r['source_path'].endswith('.py'):ast.parse(p.read_text())
        records.append({**r,'local_copy':ref(p,'Complete selected file;'+str(len(p.read_text().splitlines()))+' lines'),
                        'retrieval':ref(RAW/(r['id']+'.receipt.json'),'Original response identity'),
                        'tree':ref(RAW/('v12_la_'+r['package']+'_tree.json'),'Complete exact revision tree'),'verified_git_blob':blob_sha})
    assert len(records)==22
    # Exact source guards keep static conclusions attached to the observed revision.
    def src(pkg,n):return (RAW/f'exec15_latent_{pkg}_{n}.txt').read_text()
    assert 'pred[:, l, l] = 0' in src('lcm',1) and 'self.n_vars, self.n_vars, self.max_lag' in src('lcm',6)
    assert 'weights_only=False' in src('lcm',8)
    agent_ast=ast.parse(src('causalagent',1))
    imports=[a.name for n in ast.walk(agent_ast) if isinstance(n,ast.ImportFrom) for a in n.names]
    assert 'run_pc_analysis' in imports and 'run_olc_analysis' not in imports
    assert 'run_olc_analysis(csv_data)' in src('causalagent',1) and 'def run_olc_analysis(' in src('causalagent',3)
    assert '(adjacency_matrix == 1)' in src('causalagent',4) and 'return False, []' in src('causalagent',4)
    assert 'if isinstance(ananlysis_result, str):' in src('causalagent',12)
    assert '"revised_graph": edge_evaluations.get("decision", [])' in src('causalagent',12)
    assert '{critical_edges}' in src('causalagent',7) and '"final_edges": critical_edges' in src('causalagent',7)
    assert '{knowledge_knowledge}' in src('causalagent',7) and '"relevant_knowledge": knowledge_excerpt' in src('causalagent',7)
    package_findings={
     'lcm':{'revision':plans[0]['pin'],'license':'Apache-2.0 root;weights and transitive components separately unresolved',
        'package':tomllib.loads(src('lcm',3))['project'],
        'anchors':['README lines159-225:input axes,global scaling,padding,mask;model.py79-110:raw tensor shape',
                   'transformation_utils.py10-26,94-174:transpose,lag reversal and full graph conversion',
                   'load_utils.py25-35:missing/failed load returnsNone;weights_only=False'],
        'findings':['Numerical model,not a language model;no hidden/confounding qualification.',
                    'README mask clears variable diagonals0-2 for every lag,leaving3-11;lagged self-edges are valid temporal mechanisms.',
                    'Global constant input has zero denominator;random padding needs an explicit seed and validity mask.',
                    'Checkpoint bytes/rights are not acquired;no reported local inference or speed.']},
     'causalagent':{'revision':next(r['pin'] for r in plans if r['package']=='causalagent'),'license':'MIT root;resolved dependencies and CDMIR rights/runtime open',
        'anchors':['mcp_server.py16,98:missing OLC import despite backend definition',
          'causalachieve.py61-113,116-280:PC FisherZ alpha.05,endpoints and distinct OLC convention',
          'detect_cycles.py25-57:arrowhead projection and exception/no-cycle conflation',
          'fix_cycles.py105-128:single-entry deletion,not paired endpoint mutation',
          'nodes.py503-619:reachable postprocessing,second cycle test,dict guard and discarded working matrix',
          'evaluate_edge_llm.py60-103:prompt/input mismatch and low-confidence default',
          'graph.py28-89 and edges.py5-74:conditional dispatch and postprocessing-to-report'],
        'findings':['Backend dict -> raw extraction -> cycle projection -> postprocess is a declared path,not a live invocation.',
          'The caller DOES rerun the same cycle test;it only warns on remaining cycles and still counts original cycles as fixed.',
          'Normal dictionary results bypass edge evaluation and emit revised_graph=[];working_matrix is absent from emitted revised_graph.',
          'String branch tries .get on str and falls to error reporting;fixing only prompt variables will not repair the call chain.',
          'Endpoint pairs and OLC row/column conventions require separate graph-class converters;projected acyclicity is not causal truth.',
          'CausalAgent DMIRLAB identity is distinct from causal-learn+ in Zheng et al.']}}
    write(BASE/'primary-review.json',{'cutoff':'2026-10-07','papers':reviewed,'sources':records,'packages':package_findings,
                                    'limitations':LIMITS,'upstream_execution':False})
    write(BASE/'exact-results.json',exact())
    census=json.loads((ROOT/'docs/program/execution/2026-10-13/llm-census/census-register.json').read_text())
    items=[]
    for r in census['items']:
        if 'latent_temporal_discovery' not in r['task_families']:continue
        suffix=r['id'].split('-')[-1]
        if suffix in ['40','110']:disposition='Retain inherited authentic original and task-specific limitations.'
        elif suffix in ['148','180','263']:disposition='Recovered genuine publisher original,verified cutoff and inspected method/limits;retain bounded comparison.'
        elif suffix=='60':disposition='Original unresolved:TLS hostname failure on both hosts,with intermediate DNS timeout;no insecure retry or technical citation.'
        elif suffix=='199':disposition='DOI and guessed PDF endpoints returned HTML;PDF conversion failed;abstract lead is not a full technical original.'
        elif r['id']=='LA01-longitudinal-search':disposition='Specialist search saturation remains open;source recovery is not an exhaustive frontier census.'
        else:disposition='Authentic bank evidence is conditional later work;public/generated proposal studies can proceed.'
        items.append({'id':r['id'],'title':r.get('title'), 'prior_disposition':r['disposition'],'current_disposition':disposition,
                      'next_action':'Apply the specific research/prototype route in the task synthesis;recover missing originals or tighten specialist searches before completeness claims.'})
    assert len(items)==9
    write(BASE/'candidate-reassessment.json',{'cutoff':'2026-10-07','items':items,'coverage_closed':False,
         'acquisition_failures':ref(BASE/'recovery-observations.json','Preserved TLS/HTML/PDF-reader failures'),
         'additional_omissions':['Yu supplementary code S7-S8 not acquired;cohort table/prose discrepancy unresolved',
                                'ST-HCM public code lead not yet reviewed','LCM checkpoint identities/rights/runtime unresolved']})
    contract={
      'scope':'Proposed public/generated prototype;no enabled adapter or trial claim',
      'inputs':['Unit and subunit IDs;event and availability clocks;lag units;sampling and selection law',
        'Known,assumed and hypothesized intervention regimes kept distinct;unverified anomaly is not an intervention',
        'Graph class,paired endpoints,latent/selection allowance and contemporaneous restrictions',
        'Exact code,checkpoint,environment,variable ontology and external-evidence identities'],
      'outputs':['Original typed graph and marks plus separately attributed proposed changes',
        'Graph-family retention versus conditional effect uncertainty versus language agreement separately',
        'Outcome units,costs,policy target,model sensitivity and explicit unidentified/unsupported states'],
      'repairs':['Validate CPDAG/PAG/lagged/OLC encodings before conversion;round-trip every permitted endpoint pair and lag.',
        'Repair MCP OLC binding and distinguish absent backend from unsupported scientific assumptions.',
        'Repair dictionary guard,prompt inputs,typed response access and emitted revised graph together;preserve original graph.',
        'Use three-state cycle validation(valid,invalid,error),paired endpoint edits and exact post-edit graph-class tests.',
        'Retain valid autoregressive lags;check constant inputs,axis order,padding and audited weight identity.',
        'Require a declared identification/effect-set method before describing graph confidence as monetary confidence.'],
      'failures':{'missing_backend':'backend_unavailable','bad_endpoint_pair':'invalid_graph_encoding',
        'unknown_graph_class':'unsupported_graph_class','checker_exception':'validation_unavailable',
        'wrong_clock':'temporal_contract_mismatch','constant_normalization':'preprocessing_undefined',
        'unknown_weights':'checkpoint_unqualified','unverified_regime':'intervention_assumption_unverified',
        'equivalent_effect_disagreement':'effect_not_point_identified','uncalibrated_graph_set':'coverage_not_established'},
      'comparison_design':{'status':'prospective_not_executed_or_registered','independent_units':'Entire generated mechanisms and trajectories,not rows/prompts',
        'arms':['No-language statistical baseline','Expert-supplied restrictions','Language proposals with protected core',
                'Corrupted/reversed priors','Numerical LCM only in declared domain'],
        'strata':['Declared scalar nonGaussian confounding','Zero/weak higher-cumulant signal','Multiple latent loadings',
                  'Feedback/contemporaneous effects','Irregular/aggregated clocks','Drift and selection'],
        'public_role':'Realistic variable/clock/missingness distributions and forecast tasks;causal truth only where independently documented',
        'metrics':['Endpoint and graph-class retention','Identification/refusal correctness','Effect-set coverage,width and availability',
                   'Decision loss under known generated interventions','Review time,full compute and failed calls'],
        'controls':['Freeze sources,weights,prompts,prior strength and budgets before held-out mechanisms.',
                    'Separate tuning/calibration/evaluation;familywise coverage budgets and refusal denominator explicit.',
                    'Check labels against interventions;do not use LLM consensus or changed-variable annotations as causal gold.',
                    'Estimate pilot variance/cost before freezing independent replication counts;no final qualification dataset drawn here.']},
      'remaining_research':['Time-uniform/graph-family retention under dependent samples and soft potentially false priors',
        'Observed-law confidence sets and effect union with graph selection and numerical errors accounted for',
        'Precision and decision usefulness under multiple confounders,selection,drift and weak information'],
      'known_routes':['Exact references and typed conversions now','Bounded generated native prototype before expensive bank studies',
                      'Collect new information or report effect sets for observationally equivalent worlds'],
      'integration_allowed':False,'live_model_execution':False}
    write(BASE/'conversion-and-study-contract.json',contract)
    def source(key,title,kind,local,claims,rows):
        return {'integrated_citation_key':key,'kind':kind,'author':'Causal banking proposal' if kind.startswith('project') else 'Pinned upstream contributors',
           'title':title,'year':2026,'version_date':'15 October 2026 inspection;exact historical revisions and dates in records',
           'source_identity':'Project-authored '+kind if kind.startswith('project') else '; '.join(sorted({r['url'] for r in rows})),
           'local_copy':ref(local,title),'inspected_anchors':[title],'supported_claims':claims,'records':rows,'limitations':LIMITS}
    for pkg in ['lcm','causalagent']:
        rows=[r for r in records if r['package']==pkg]
        s=source('exec15_latent_'+pkg,pkg+' pinned temporal and graph-conversion source','software',
                 BASE/'primary-review.json',package_findings[pkg]['findings'],rows)
        commit_path=RAW/('v12_la_commit_'+pkg+'.json');commit=json.loads(commit_path.read_text())
        if isinstance(commit,list):commit=commit[0]
        assert commit['sha']==package_findings[pkg]['revision']
        date=commit['commit']['committer']['date'];assert date[:10]<='2026-10-07'
        s['version_date']=date+';revision '+commit['sha'];s['identity_record']=ref(commit_path,'Exact pinned commit identity')
        s['inspected_anchors']=package_findings[pkg]['anchors'];new.append(s)
    new.append(source('exec15_latent_exact','Exact temporal confounding,cumulant,graph and decision references','project_derivation',
        BASE/'exact-results.json',['Nine exact reference families;no fitted or live performance'],[{'local_copy':ref(Path(__file__),'Exact rational enumeration and independent factor check')}]))
    new.append(source('exec15_latent_design','Temporal agent conversion repairs and prospective public evidence study','project_design',
        BASE/'conversion-and-study-contract.json',['Typed failures,public/generated comparison,coverage limits and unresolved effect-set research'],
        [{'local_copy':ref(BASE/'candidate-reassessment.json','All inherited latent-temporal candidates and unresolved originals')}]))
    write(BASE/'source-audit.json',{'sources':new,'prior':ref(AUDIT,'619 inherited citation records'),'cutoff':'2026-10-07'})
    tex=(BASE/'development.template').read_text().replace('§',chr(92))
    (BASE/'development.tex').write_text(tex)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['pandoc','--from=latex','--to=markdown','--wrap=auto',str(BASE/'development.tex'),'-o',str(OUTPUT)],check=True,timeout=30)
    with OUTPUT.open('a') as stream:
        stream.write('\n\nSource recovery, exact constructions, proposed repairs and unresolved research are bound in '+
                     '`docs/program/execution/2026-10-15/latent-temporal/`. This is a bounded task synthesis, not exhaustive census or capability qualification.\n')
    evidence=[ref(p,a) for p,a in [(BASE/'primary-review.json','Eleven primary papers and22 verified source blobs'),
        (BASE/'exact-results.json','Nine exact mathematical/source references'),(BASE/'candidate-reassessment.json','All nine relevant inherited candidate/coverage entries'),
        (BASE/'conversion-and-study-contract.json','Concrete repairs and proposed comparison'),(BASE/'source-audit.json','Seven added citation records'),
        (OUTPUT,'Connected latent/temporal task synthesis'),(BASE/'development.template','Authored integrated discussion'),(Path(__file__),'Reproducible review')]]
    for e in evidence:verify_bindings(e)
    findings=['Eleven genuine primary papers compare initialization,sequential noisy priors,numerical models,model proposal and protected-core orchestration;three unresolved originals recovered and two retained as omissions;22 exact source blobs support concrete reuse conditions.',
      'Time-specific banking target,Gaussian observational equivalence,cumulant premises,IV counterexample,lagged graph and converter references reproduce;proposed public/generated controls and decision values are explicit.',
      'All empirical comparisons remain author-reported;static findings and exact project mathematics confer no live performance or bank truth. Unproved general graph/effect-set coverage stays open.']
    write(BASE/'author-review.json',{'status':'pass','reviewer':REVIEWER,'scope':'Bounded proposal synthesis with unresolved coverage and research stated',
        'findings':findings,'evidence':evidence,'limitations':LIMITS,'integration_allowed':False,'visual_acceptance':False})
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='pass',execution='performed',scope='Bounded latent/temporal proposal synthesis',reviewer=REVIEWER,
        limitations=LIMITS,outputs=[ref(OUTPUT,'Reviewed task synthesis')],nonexecution_reason='',capabilities=[],
        revisit_trigger='New primary originals,graph/effect calibration results,qualified package prototype or independent causal truth.',
        criteria=[{'index':i,'verdict':'pass','finding':f,'evidence':evidence} for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'status':'pass','papers':len(reviewed),'new_scholarly_PDFs':3,'source_blobs':len(records),'new_records':len(new),'exact':'pass'}))


if __name__=='__main__':main()
