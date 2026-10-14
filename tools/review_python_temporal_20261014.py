#!/usr/bin/env python3
"""Review bounded Python temporal/interventional sources; no upstream execution."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import run_program as control
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = control.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-14/python-temporal'
RAW = ROOT / 'docs/literature/raw'
OP = 'SW.CELL.discovery_temporal_interventional.Python'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'coverage-review.json'
AUDIT = ROOT / 'docs/program/execution/2026-10-14/iid-discovery/publication/reader/source-audit.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Bounded nine-repository technical review plus inherited LiNGAM; all discovered candidates and aliases are recorded but wider family coverage is incomplete.',
    'Present repository-search metadata may postdate the cutoff; only dated pinned originals support technical claims.',
    'Selected static paths, primary literature and exact authored calculations are not upstream runtime, empirical calibration or bank evidence.',
    'Root license declarations do not settle dependencies, distribution rights or maintenance costs.',
    'No adapter is enabled; complete finite-sample graph/effect confidence and matched public/generated comparisons remain proposed.',
    'Whole-manuscript depth and sponsor coherence remain open; rendered visual acceptance is unavailable under the exhausted session image allowance.'
]

def exact():
    b0 = [[F(0), F(0)], [F(1, 2), F(0)]]
    b1 = [[F(1, 2), F(0)], [F(1, 4), F(1, 2)]]
    inverse = [[F(1), F(0)], [F(1, 2), F(1)]]
    def mm(a,b):
        return [[sum((a[i][k]*b[k][j] for k in range(2)), F(0)) for j in range(2)] for i in range(2)]
    phi = mm(inverse,b1)
    assert phi == [[F(1,2),0],[F(1,2),F(1,2)]]
    shock = [[F(1)],[F(1,2)]]
    responses=[]
    for h in range(5):
        responses.append([str(v[0]) for v in shock])
        shock=[[sum((phi[i][j]*shock[j][0]for j in range(2)),F(0))] for i in range(2)]
    assert [r[1]for r in responses[:3]] == ['1/2','3/4','5/8']
    cumulative = [F(2),F(3)]
    assert [sum((([F(1,2),0],[-F(1,2),F(1,2)])[i][j]*cumulative[j]for j in range(2)),F(0))for i in range(2)]==[1,F(1,2)]
    index=[1,2,2,3,6,7]
    cuts=[0]+[i+1 for i,(a,b)in enumerate(zip(index,index[1:]))if b-a>1]+[len(index)]
    segments=[index[a:b]for a,b in zip(cuts,cuts[1:])]
    folded=[(a,b)for segment in segments for a,b in zip(segment,segment[1:])]
    assert len(folded)==4 and sum(b-a==1 for a,b in folded)==3
    columns={'rate':0,'liquidity':1}
    masks={}
    for label in ['rate','raet']:
        targets={columns[x]for x in label.split(',')if x in columns}
        masks[label]=[0 if i in targets else 1 for i in range(2)]
    assert masks=={'rate':[0,1],'raet':[1,1]}
    scores={'A':(3,5),'B':(4,0)}
    assert min(scores,key=scores.get)=='A' and min(scores,key=lambda k:sum(scores[k]))=='B'
    rho=[F(1,2),-F(1,2)];sigma2=F(3,4)
    assert [r*r for r in rho]==[F(1,4)]*2
    assert [sigma2*(1+r*r)for r in rho]==[F(15,16)]*2
    assert [sigma2/(1-r*r)for r in rho]==[F(1)]*2
    # Independent Gaussian innovations H,U,W,Z, variances1,1,1,2.
    loadings={'perfect':[[1,0,0,0],[0,0,0,1],[1,0,1,2]],
              'soft':[[1,0,0,0],[1,1,0,0],[3,2,1,0]]}
    covariances={}
    for kind,rows in loadings.items():
        covariances[kind]=[[sum(F(a)*F(b)*v for a,b,v in zip(x,y,[1,1,1,2]))for y in rows]for x in rows]
    assert [covariances[k][1][1]for k in ['perfect','soft']]==[2,2]
    assert [covariances[k][0][1]for k in ['perfect','soft']]==[0,1]
    assert [covariances[k][1][2]for k in ['perfect','soft']]==[4,5]
    return {'kind':'exact_project_references','upstream_execution':False,'random_draws':0,
        'dynamics':{'convention':'column vector x_t=B0*x_t+B1*x_(t-1)+epsilon_t; B[target,source]',
            'B0':[[str(x)for x in row]for row in b0],'B1':[[str(x)for x in row]for row in b1],
            'reduced_form':[[str(x)for x in row]for row in phi],
            'unit_funding_innovation_responses':responses,'cumulative_response':list(map(str,cumulative)),
            'assumptions':'Stable coefficients, acyclic within-slice B0, independent centered innovations; zero initial deviations; no discounting in illustrative infinite-horizon sum.',
            'stipulated_value_USD_per_liquidity_unit':100,'one_time_action_cost_USD':60,
            'immediate_net_USD':str(100*F(1,2)-60),'cumulative_net_USD':str(100*cumulative[1]-60)},
        'subsampling':{'daily_rho':['1/2','-1/2'],'daily_innovation_variance':'3/4','stationary_variance':'1',
            'every_second_day_rho':'1/4','two_step_innovation_variance':'15/16',
            'one_day_impulse_response':['1/2','-1/2'],'two_day_impulse_response':['1/4','1/4'],
            'conclusion':'Identical stationary even-date Gaussian laws do not identify the sign of the intervening one-day impulse.'},
        'interventions':{'observed_variables':['H','A','Y'],'baseline':'H,U,W independent N(0,1); A=H+U;Y=2A+H+W',
            'perfect':'A=delta+Z;Z independent N(0,2)','soft':'A=H+U+delta',
            'common_A_mean':'delta','common_A_variance':'2','common_Y_mean':'2*delta',
            'perfect_cov_H_A':str(covariances['perfect'][0][1]),'soft_cov_H_A':str(covariances['soft'][0][1]),
            'perfect_cov_A_Y':str(covariances['perfect'][1][2]),'soft_cov_A_Y':str(covariances['soft'][1][2]),
            'interpretation':'Both targets are A, but parent removal differs; hiding H adds confounding and invalidates sufficient-graph claims.'},
        'duplicate_clock':{'indices':index,'source_style_segments':segments,'retained_pairs':folded,
            'strict_unit_step_count':3,'interpretation':'Sorted integer indices alone admit duplicates; adapter must reject duplicate observation clocks.'},
        'label_mapping':{'authored_labels_to_retention_mask':masks,'interpretation':'Unknown spelling is not an observational regime; refuse before upstream helper.'},
        'search_score':{'candidate_counts':{k:list(v)for k,v in scores.items()},'tuple_prefers':'A','sum_prefers':'B',
            'scope':'Arithmetic ordering counterexample only, not a claim that these DAGs are reachable under a specific oracle.'}}

ANCHORS = {
 'tigramite':['README18-35 method/test assumptions;111-120 GPL declaration','Complete GPLv3 text',
 'JPCMCIplus16-104 node classes;413-453 enforced exogenous contexts and removed links',
 'RPCMCI19-159 regime stationarity, mask replacement, scalar single-series restriction and stopping parameters',
 'DataFrame19-158 data/mask/reference/time-offset contract; construct_array548 onwards'],
 'causalai':['README28-39 declared features,49-66 task distinction','Complete BSD-3-Clause terms',
 'PCSingle87-233 greedy conditioning then testing; PC261-298 per-variable runs',
 'Granger67-92 LassoCV coefficients, residual formula, t-tail and rank-failure ones',
 'VARLINGAM71-137 one-series assertion, dependency matrix conversion and p-value reconstruction',
 'TimeSeriesData30-115 per-array lag extraction and complete-case deletion',
 'BaseTimeSeriesAlgo57-68 candidates only negative lags;86-114 thresholded parents'],
 'gies':['README8-12 identity and42-44 target lists','Complete BSD-3-Clause terms',
 'fit_bic61-138 I-essential matrix conventions and score;fit141-218 search phases',
 'GaussIntL0Pen48-107 centering, conservative targets and nonintervention covariance;146-175 score'],
 'causaldag':['README identity and license','Complete BSD-3-Clause terms','__init__33-36 reexports external libraries',
 'UTIGSP docs7-9 stale implementation link;50-62 two testers and returned targets','Tutorial pointer only',
 'requirements delegates to requirements/default.txt','setup18-36 unpinned external dependency names'],
 'dcdi':['README exact research command and perfect/known example','Complete MIT terms',
 'BaseModel29-64 implemented intervention combinations;118-176 masks/regime-specific parameters',
 'DataManagerFile29-60 observational regime0 and known/unknown settings;164-201 retention-mask construction',
 'compute_loss38-59 known-perfect retention mask versus regime-specific likelihood; training optimizer below'],
 'enco':['README97-102 single-target indexed intervention arrays;117-122 paper identity','Complete BSD-style three-condition terms',
 'GraphFitting207-258 edge/orientation gradients and targeted-variable masking',
 'InterventionalDataset53-159 variable-indexed sampling and batches'],
 'sdcd':['README3-4 labeled interventions and paper;12-15 identity','Complete MIT terms',
 'SDCD84-318 two-stage train;319-366 threshold and greedy cycle removal',
 'reconstruction_loss353-366 masks Gaussian likelihood;loss405 onwards',
 'dataset helper87-134 unknown label conversion and retention mask'],
 'causalnex':['DYNOTEARS158-250 arrays and threshold;389-428 within-slice acyclicity and structural loss',
 'Transformer152-208 integer nondecreasing index;210-282 split gaps greater1 and per-realisation lagging'],
 'gml':['Complete BSD-3-Clause terms','gsp770-815 defaults;861-873 score switch;890-909 tuple/sum comparisons',
 'setup dependency declarations; not a solved compatible environment']
}
CLAIMS = {
 'tigramite':['PCMCI, PCMCI+, LPCMCI, RPCMCI and JPCMCI+ have distinct assumptions and graph classes.',
 'JPCMCI+ classifies system, time/space context and dummy nodes; its helper enforces exogenous context-to-system orientation.',
 'RPCMCI assumes finite persistent stationary regimes; constructor requires scalar single-series input and replaces the supplied mask with all-false values.'],
 'causalai':['Selected PC/Granger parent candidates are negative lags; the VARLiNGAM wrapper separately includes lag0.',
 'Lag construction concatenates within-array slices and can remove rows with NaNs; it has no physical timestamp argument.',
 'Granger fits LassoCV then computes a t-tail expression; both inspected Granger/VARLiNGAM rank-failure paths substitute p-values of1.',
 'The selected code alone supplies no selection- and dependence-adjusted justification for these p-values.'],
 'gies':['fit_bic returns an estimated I-essential graph; bidirectional nonzero entries represent an undirected edge, not two structural arrows.',
 'The Gaussian score centers each environment, counts nonintervened observations per node, checks conservative target coverage and uses the declared BIC penalty.'],
 'causaldag':['The selected facade reexports three external packages; the old UTIGSP page links to a source path absent from this pinned tree.',
 'The documentation distinguishes CI and conditional-invariance testers and returns a DAG plus estimated target sets; a compatible resolved environment is not supplied.'],
 'dcdi':['The constructor accepts perfect known, perfect unknown and imperfect known regimes; imperfect unknown raises Not implemented.',
 'Known perfect targets are removed from the mechanism likelihood by a retention mask; other implemented branches use regime-specific parameters.',
 'The paper global-optimum equivalence-class theorem does not establish that the finite nonconvex training run reaches that optimum.'],
 'enco':['The documented array interface indexes interventional samples by the single targeted variable.',
 'Selected gradients zero incoming-edge updates for the intervened variable and separately control orientation updates; this is not graph confidence.'],
 'sdcd':['The helper maps unmatched labels to -1 then drops them; a wholly unmatched label becomes an all-ones retention mask.',
 'get_adjacency_matrix can apply sorted-edge thresholding and reject edges forming cycles; returned DAG is distinct from raw learned weights.',
 'Numerical constraint stability and a population/exact stage-one guarantee are not finite-run graph recovery.'],
 'causalnex':['DYNOTEARS optimizes X(I-W)-Xlags*A with an acyclicity constraint on W only; thresholded weights return a chosen structure.',
 'The transformer splits integer index gaps greater than1 and lags each realisation separately; nondecreasing duplicate indices pass its inspected checks.'],
 'gml':['UTIGSP defaults to search depth4, five starts and tuple scoring; no_targets can discard supplied known target information.',
 'Tuple scoring orders edge/variant counts lexicographically; the paper inspected on page5 defines their sum. Equivalence is not established by this source review.']
}

def main():
    assert not (BASE/'author-review.json').exists()
    plans=[json.loads((BASE/n).read_text()) for n in ['acquisition-03-plan.json','acquisition-06-plan.json']]
    pins=plans[0]['pins'];gml=json.loads((BASE/'acquisition-05-plan.json').read_text())['gml']
    pins['gml']=dict(gml,repo='uhlerlab/graphical_model_learning')
    packages=[];sources=[]
    for key in ANCHORS:
        files=[f for p in plans for f in p['files']if f['package']==key];assert len(files)==len(ANCHORS[key])
        records=[]
        for f,anchor in zip(files,ANCHORS[key]):
            local=RAW/(f['id']+'.txt');data=local.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==f['blob']
            tree=json.loads((ROOT/f['tree']).read_text());assert tree['sha']==pins[key]['sha']and not tree['truncated']
            records.append({'source_identity':f['url'],'upstream_path':f['upstream_path'],'local_copy':ref(local,anchor),
                'receipt':ref(local.with_suffix('.receipt.json'),'Observed original acquisition'),'git_blob_sha1':blob,'tree_identity_verified':True})
        pin=pins[key];assert pin['date']<='2026-10-07T15:59:59Z'
        package={'package':key,'revision':pin['sha'],'date':pin['date'],'records':records,'claims':CLAIMS[key],
            'tree':ref(ROOT/files[0]['tree'],'Complete pinned tree'),'runtime':'not executed in this review'}
        packages.append(package)
        sources.append({'integrated_citation_key':'exec14_pt_'+key,'kind':'software_primary_sources','title':pin['repo']+' temporal/interventional selected source review',
            'author':pin['repo']+' contributors','year':int(pin['date'][:4]),'source_identity':'https://github.com/'+pin['repo'],
            'version_date':pin['sha']+'; '+pin['date']+'; acquired14 October2026', 'local_copy':records[0]['local_copy'],
            'records':records,'inspected_anchors':ANCHORS[key],'supported_claims':CLAIMS[key],'limitations':LIMITS})
    meta=json.loads((BASE/'acquisition-05-plan.json').read_text())['papers']
    meta.append({'key':'gies','title':'Characterization and Greedy Learning of Interventional Markov Equivalence Classes of Directed Acyclic Graphs',
        'authors':['Alain Hauser','Peter Bühlmann'],'published':'2012-08','updated':'2012-08','source_identity':'https://jmlr.org/papers/volume13/hauser12a/hauser12a.pdf'})
    meta.append({'key':'dynotears','title':'DYNOTEARS Structure Learning from Time-Series Data','authors':['Roxana Pamfil','Nisara Sriwattanaworachai','Shaun Desai','Philip Pilgerstorfer','Paul Beaumont','Konstantin Georgatzis','Bryan Aragam'],
        'published':'2020','updated':'2020','source_identity':'https://proceedings.mlr.press/v108/pamfil20a.html',
        'existing':'docs/papers/DYNOTEARS Structure Learning from Time-Series Data Pamfil(2020).pdf'})
    pages={'jpcmci':[1,3,4,5],'rpcmci':[1,3,4],'gies':[1,4,5,6],'dcdi':[1,2,3,5,6],
           'enco':[1,6,21],'sdcd':[1,3,5,6,7,15,16],'utigsp':[1,4,5,6],'dynotears':[1,2,3]}
    paper_claims={
      'jpcmci':'Joint acyclic SCM; context exogeneity, no context-system confounding, context determinism and complete system observation delimit latent-context scope.',
      'rpcmci':'Regime-stationary discrete-time SCM with independent stationary innovations, finite persistent regimes and selected lagged model.',
      'gies':'Perfect stochastic interventions remove incoming arrows; independent observations and conservative target families support interventional equivalence definitions.',
      'dcdi':'Theorem1 is a population global score optimum under capacity, positivity, entropy and I-faithfulness assumptions; finite optimization may reach only a stationary point.',
      'enco':'Theorem3.1 and AppendixB require informative interventions, accurate conditionals and regularization restrictions; fewer-target extension lacks the same convergence guarantee.',
      'sdcd':'Spectral-radius stability is numerical; stage1 theorem assumes exact population optimization and appropriate model/faithfulness/positivity conditions.',
      'utigsp':'Unknown-target recovery requires observational data and I-faithfulness; page5 sum score differs from inspected default tuple ordering.',
      'dynotears':'Stationary independent realisations; independent innovations and non-Gaussian or standard-Gaussian identifiable regimes; W acyclic and lag matrices separate.'}
    paper_records=[];(BASE/'inspected').mkdir(exist_ok=True)
    for m in meta:
        k=m['key'];year=int(m['updated'][:4]);surname=m['authors'][0].split()[-1]
        local=ROOT/m['existing']if 'existing'in m else ROOT/'docs/papers'/(m['title']+' '+surname+'('+str(year)+').pdf')
        origin=local if 'existing'in m else RAW/f'exec14_pt_paper_{k}.pdf';data=origin.read_bytes();assert data.startswith(b'%PDF-')
        if local.exists():assert local.read_bytes()==data
        else:local.write_bytes(data)
        txt=BASE/'papers'/(k+'.txt');page_text=txt.read_text().split(chr(12));inspected=[]
        if 'arxiv'in m:assert m['arxiv']in page_text[0],(k,'PDF version identity')
        for page in pages[k]:
            out=BASE/'inspected'/f'{k}-page-{page}.txt';out.write_text(page_text[page-1]);inspected.append(ref(out,f'Physical PDF page{page}'))
        identity=m.get('source_identity')or'https://arxiv.org/abs/'+m['arxiv']
        s={'integrated_citation_key':'exec14_pt_paper_'+k,'kind':'paper','title':m['title'],'filename_title':m['title'],
            'author':' and '.join(m['authors']),'authors':m['authors'],'first_author':surname,'year':year,
            'source_identity':identity,'url':identity,'local_path':str(local.relative_to(ROOT)),
            'sha256':hashlib.sha256(data).hexdigest(),'version_date':m.get('arxiv','published original')+'; '+m['updated']+'; acquired14 October2026',
            'version_status':m.get('arxiv','published original'),'local_copy':ref(local,'Genuine primary PDF'),
            'inspected_anchors':inspected,'supported_claims':[paper_claims[k]],'claims':[paper_claims[k]],
            'inspected':['Physical pages '+','.join(map(str,pages[k]))],'limitations':'Selected methods/assumptions review; no exhaustive correction/retraction review or reproduced upstream benchmarks.'}
        if 'arxiv'in m:
            s['identity_evidence']=[ref(RAW/f'exec14_pt_paper_meta_{k}.xml','Original author/title/version/date metadata'),
                ref(RAW/f'exec14_pt_paper_{k}.receipt.json','Observed original PDF acquisition')]
        elif k=='gies':s['identity_evidence']=[ref(RAW/'exec14_pt_paper_gies.receipt.json','Publisher original acquisition; first page states2012 publication')]
        sources.append(s);paper_records.append(s)
    search_files=sorted(p for p in RAW.glob('exec14_pt_search_*.json')if not p.name.endswith('.receipt.json'));candidates={}
    for p in search_files:
        d=json.loads(p.read_text())
        for c in d['items']:
            name=c['full_name'];candidates.setdefault(name,{'repository':name,'description':c.get('description'),'queries':[],
                'status':'unreviewed discovery lead; eligibility and relevance not established'})['queries'].append(ref(p,'Repository-search result; metadata only'))
    for name in ['salesforce/causalai','slachapelle/dcdi','juangamella/gies']:
        if name in candidates:candidates[name]['status']='selected pinned primary path reviewed; coverage/runtime incomplete'
    priority=['bloomberg/causal-ts','loeweX/AmortizedCausalDiscovery','lmz123321/proxy_causal_discovery','CausalML-Lab/PCMCI-Omega','CausalML-Lab/CausalCPD','haeggee/bacadi','Mamba413/CausalGraphCut','EyringMLClimateGroup/debeire24clear_Bagged_TimeSeries_Causality']
    omissions={'coverage_complete':False,'candidates':list(candidates.values()),'priority_followups':priority,
        'aliases':[{'alias':'quantumblacklabs/causalnex','result':'HTTP404; resolved through inherited mckinsey/causalnex pinned originals'},
                   {'alias':'causaldag UTIGSP old path','result':'Not in pinned tree; resolve graphical_model_learning plus conditional_independence/graphical_models dependencies'},
                   {'alias':'CUTS / CUTS+','result':'Query CUTS causal discovery returned0; CUTS causal returned17 mostly unrelated hits. Mamba413/CausalGraphCut is unqualified lead; original identity still requires resolution.'},
                   {'alias':'CD-NOD / CDNOD / causal-learn','result':'Repository name queries miss embedded algorithm; inspect inherited causal-learn tree in follow-up, not an absence finding.'}],
        'search_scope':'Eight queries plus page2 completing37 returned temporal repositories; two broad rounds, finite first30 results per query, recorded totals. Public index is not exhaustive.',
        'pending':'Irregular/subsampled, event/Hawkes, periodic/nonstationary, Bayesian intervention and amortized-discovery families need primary review; candidate rights/versions and paper/code correspondences remain scoped.',
        'no_unavailable_source_waiver':True,'source_failures':[ref(RAW/'exec14_pt_commit_causalnex.receipt.json','Original404 retained')]}
    choices={
      'tigramite':('integrate','Distinct PCMCI+/LPCMCI/JPCMCI+/RPCMCI contracts; preserve endpoint, context and mask semantics; compare generated hidden/shared-calendar regimes.'),
      'causalai':('reference','Use as benchmark/interface reference; defer inferred p-value service; refuse rank failure, verify centering/intercept and time-aware validation.'),
      'gies':('integrate','Candidate known-perfect intervention baseline with I-essential endpoints and conservative-target admission.'),
      'causaldag':('defer','Resolve facade dependencies and historic API mismatch; do not promise the documented import works.'),
      'gml':('reference','Retain explicit score mode, search depth/restarts and CI/invariance contracts; verify theory/code score agreement before enabling.'),
      'dcdi':('integrate','Research comparator with three implemented intervention combinations; reject imperfect-unknown on this pin; retain optimizer outcomes.'),
      'enco':('reference','Compare known single-target intervention settings; no general temporal or hidden-variable claim from the selected path.'),
      'sdcd':('integrate','Candidate numerical baseline after strict target validation; retain raw and cycle-pruned adjacency and optimization diagnostics.'),
      'causalnex':('reference','Reference DYNOTEARS and discontinuity-aware folding; inherited discontinuation notice prevents default maintained-dependency adoption.'),
      'lingam':('integrate','Inherit separate structural matrix orientation and fixed-lag residual bootstrap limits; compare under explicit non-Gaussian innovation law.')}
    decisions=[{'package':k,'decision':v[0],'reason_and_route':v[1],'integration_allowed':False,
        'direct_adoption':'Deferred until environment, rights and semantic acceptance cases pass.',
        'port':'Not selected: compare adapter cost with numerical equivalence and independent maintenance burden.',
        'reject':'Reject substitution of prediction, numerical convergence or one selected graph for identified intervention effects.'}for k,v in choices.items()]
    write(BASE/'exact-results.json',exact());write(BASE/'omissions-register.json',omissions);write(BASE/'reuse-decisions.json',{'decisions':decisions})
    write(BASE/'primary-review.json',{'packages':packages,'papers':paper_records,'upstream_execution':False,'limitations':LIMITS})
    sources += [{'integrated_citation_key':'exec14_pt_exact','kind':'project_derivation','title':'Exact dynamics, intervention and semantic reference cases','author':'Causal banking proposal','year':2026,
        'source_identity':'Project-authored exact algebra','version_date':'2026-10-14','local_copy':ref(BASE/'exact-results.json','Seven exact scoped constructions'),
        'records':[ref(Path(__file__),'exact() rational arithmetic')],'inspected_anchors':['exact()'],'supported_claims':['Structural/reduced-form difference; horizon-dependent value; subsampling sign ambiguity; perfect/soft covariance; duplicate clock; label and score distinctions.']},
        {'integrated_citation_key':'exec14_pt_contract','kind':'project_analysis','title':'Python temporal and interventional reuse proposal','author':'Causal banking proposal','year':2026,
        'source_identity':'Project-authored proposal','version_date':'2026-10-14','local_copy':ref(BASE/'reuse-decisions.json','Ten proposed dispositions'),
        'records':[ref(BASE/'omissions-register.json','Explicit candidates/aliases and coverage limits')],'inspected_anchors':['decisions and priority_followups'],'supported_claims':['No enabled integration; distinct temporal, context and intervention contracts and public/generated acceptance cases.']}]
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07 Asia/Shanghai','sources':sources})
    evidence=[ref(p,'Reviewed bounded Python temporal/interventional evidence')for p in[BASE/'primary-review.json',BASE/'source-audit.json',BASE/'exact-results.json',BASE/'omissions-register.json',BASE/'reuse-decisions.json',BASE/'plan-review.md',BASE/'development.tex',Path(__file__)]]
    verify_bindings(evidence)
    write(OUTPUT,{'operation':OP,'status':'inconclusive','coverage_complete':False,'packages':list(choices),'verified_blobs':42,
        'findings':CLAIMS,'decisions':decisions,'evidence':evidence,'limitations':LIMITS,
        'next_action':'Integrate preserving reader; then continue independent queue. Expand priority candidate originals and matched public prototype plans in follow-up.'})
    write(BASE/'author-review.json',{'status':'pass','scope':'Author review of bounded comparison; coverage inconclusive','reviewer':REVIEWER,
        'evidence':evidence+[ref(OUTPUT,'Contracted coverage output')],'limitations':LIMITS,'visual_acceptance':False,'substantive_page_credit':0,
        'findings':['42 source blobs match complete pinned trees; seven recovered primary PDFs plus inherited DYNOTEARS original.',
                    'Intervention types, target knowledge, endpoint classes, stationarity and clock semantics remain separate.',
                    'Paper/code scoring, masks, rank failure and cycle processing have proposed remedies; no upstream failure rates claimed.']})
    graph,_,_=control.combined(ROOT,control.core.read(ROOT,control.core.STATE));node=control.ledger.operation(graph,OP);receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',scope='Bounded Python temporal/interventional proposal coverage',reviewer=REVIEWER,outputs=[ref(OUTPUT,'Required reviewed coverage output')],limitations=LIMITS)
    facts=[('inconclusive','Nine repositories plus inherited LiNGAM reviewed; all search results preserved but broader family/alias coverage remains incomplete.'),
           ('pass','42 verified source blobs, eight authentic named scholarly originals and exact authored examples have inspected anchors and hashes.'),
           ('pass','Explicit proposed reuse, omissions and prototype routes; missing search matches are not absence claims.') ]
    for c,(v,f)in zip(receipt['criteria'],facts):c.update(verdict=v,finding=f,evidence=evidence)
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'review':'pass','coverage':'inconclusive','verified_blobs':42,'paper_records':len(paper_records),'new_sources':len(sources),'candidates':len(candidates)}))

if __name__=='__main__':main()
