#!/usr/bin/env python3
"""Author review of pinned R temporal sources and exact calendar references."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import run_program as control
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT=control.core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-14/r-temporal'
OP='SW.CELL.discovery_temporal_interventional.R'
SYN=ROOT/'docs/program/comprehensive-v14/work'/OP/'coverage-review.json'
AUDIT=ROOT/'docs/program/execution/2026-10-14/llm-identification/v2/reader/source-audit.json'
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
LIMITS=['Bounded four-package extension plus inherited pcalg; broader R temporal coverage remains incomplete.',
    'Static original-source inspection and exact project calculations; no upstream R runtime, empirical calibration or bank validation.',
    'Declared package licenses do not close dependency, distribution or deployment rights.',
    'causalDisco help/source output-class disagreement requires pinned dependency runtime and endpoint round-trip qualification.',
    'Rendered visual acceptance remains open under the exhausted inherited image allowance.']

def exact():
    worlds=[]
    for structural in [False,True]:
        joint=defaultdict(F)
        for c,e in product([-1,1],repeat=2):
            a=c; y=2*(a if structural else c)+e
            joint[a,y]+=F(1,4)
        means=[]
        for intervention in [-1,1]:
            means.append(sum(F(2*(intervention if structural else c)+e,4)for c,e in product([-1,1],repeat=2)))
        effect=means[1]-means[0]
        worlds.append({'assignment':'A_t=C_t; Y_(t+1)=2*A_t+E_(t+1)'if structural else'A_t=C_t; Y_(t+1)=2*C_t+E_(t+1)',
            'observed_joint':{str(k):str(v)for k,v in sorted(joint.items())},'mean_under_minus_plus':list(map(str,means)),
            'effect_thousand_USD':str(effect),'net_thousand_USD':str(effect-1)})
    assert worlds[0]['observed_joint']==worlds[1]['observed_joint']
    assert [w['effect_thousand_USD']for w in worlds]==['0','4']
    aa=ay=lagy=F(0)
    for am3,am2,am1,a0 in product([-1,1],repeat=4):
        prev=F(am3+am2,2);current=F(am1+a0,2);response=F(am2+am1,2)
        aa+=current**2/16;ay+=current*response/16;lagy+=prev*response/16
    assert aa==F(1,2)and ay==lagy==F(1,4)
    series=[('A',1,1),('A',2,2),('A',3,3),('B',1,101),('B',2,102),('B',3,103)]
    folded=[{'prior':a,'current':b,'same_bank':a[0]==b[0],'unit_step':b[1]-a[1]==1}for a,b in zip(series,series[1:])]
    valid=[x for x in folded if x['same_bank']and x['unit_step']]
    assert len(folded)==5 and len(valid)==4
    # Calendar peers are perfectly dependent within each day under the declared law.
    banks,days=100,20
    return {'kind':'exact_project_reference','upstream_execution':False,'random_draws':0,
        'calendar_worlds':worlds,'calendar_law':'Independent Rademacher C_t and E_t across all days; C is unobserved. The full stationary observed process agrees in both worlds.',
        'economics':'Y is stipulated next-day funding contribution in thousand USD; changing A from -1 to +1 costs1 thousand USD. Not bank ROI.',
        'aggregation':{'daily_law':'A_t iid Rademacher; Y_t=A_(t-1)',
            'block_means':'Abar_k=(A_(2k-1)+A_(2k))/2; Ybar_k=(A_(2k-2)+A_(2k-1))/2',
            'var_Abar':str(aa),'same_block_covariance':str(ay),'prior_block_covariance':str(lagy),
            'linear_projection_coefficients':[str(ay/aa),str(lagy/aa)],
            'two_unit_impulse_first_day':['1','0'],'two_unit_impulse_second_day':['0','1'],
            'impulse_order':'changes in current and next block mean Y; both have current Abar change1'},
        'boundaries':{'raw_pairs':folded,'folded_rows':5,'same_bank_unit_step_rows':4,
            'irregular_time_counterexample':{'bank':['A','A'],'time':[1,3],'id_filter_accepts':True,'one_day_lag_valid':False}},
        'shared_calendar':{'banks':banks,'days':days,'law':'All bank residuals at date t equal common C_t; independent dates.',
            'true_mean_variance':str(F(1,days)),'iid_row_variance':str(F(1,banks*days)),
            'standard_error_understatement_factor':'10','scope':'Exact design variance under stipulated law; no claimed general effective sample size.'}}

def main():
    assert not(BASE/'primary-review.json').exists()
    anchors={
        'causalDisco':{'DESCRIPTION':'Version, dependency and declared GPL-2 fields',
            'man/tpc.Rd':'Complete API, PDAG return description and tier example',
            'man/tfci.Rd':'Complete API; PAG stored with UNKNOWN description',
            'man/tges.Rd':'Complete tiered score-search API and PDAG return description',
            'R/tpc-run.R':'65-145: runner returns UNKNOWN; 547-575: future-tier tests return0 without invoking CI test',
            'R/tfci-run.R':'40-175: skeleton/pdsep/orientation and as_caugi(class=PAG); 177-210: arrowhead at later tier'},
        'dbnR':{'DESCRIPTION':'Version, compiled dependency and declared GPL-3 fields',
            'man/learn_dbn_struc.Rd':'Complete API: size includes present slice; f_dt permits supplied folds',
            'R/dbn_learn.R':'1-32: structure wrapper forwards dt/f_dt to selected method; parameter fitting below',
            'R/dt_modification.R':'47-57 positional fold; 77-88 ID filter; 111-129 filtered fold; 145-157 ordinary fold; 183-205 row-batch averaging'},
        'seqICP':{'DESCRIPTION':'Version, dependencies and declared GPL-3 fields',
            'man/seqICP.Rd':'Complete target, iid/ar lag settings, max.parents and stopIfEmpty cautions',
            'man/seqICPnl.Rd':'Complete nonlinear iid-noise model, regression function and coverage cautions',
            'R/seqICP.R':'170-300: defaults, empty-set test, stop rule, strict p>alpha accepted intersection and all-reject flag; 300-370: interval paths'},
        'tpc':{'DESCRIPTION':'Version, pcalg dependency and declared GPL>=3 fields',
            'man/tpc.Rd':'Complete tier/context API, conditioning restrictions and pcAlgo return',
            'R/tpc.R':'230-367: forced context edges, conflict precedence, skeleton choice, tiers and orientation'}}
    claims={
        'causalDisco':['TPC, TGES and TFCI take tiered background knowledge; tiered independent-subject data is distinct from a stationary single series.',
            'TFCI help says PAG stored as UNKNOWN but the same pinned runner calls as_caugi with PAG; TPC help says PDAG while runner uses UNKNOWN. Actual dependency behavior is untested.',
            'dir_test returns0 for a conditioning variable later than both endpoints; this is a constraint sentinel, not a measured statistical p-value.',
            'TPC/TFCI rely on pcalg and caugi pathways; chosen source scope does not qualify temporal dependence or effect uncertainty.'],
        'dbnR':['size counts current plus historical slices; size2 is first-order, Gaussian DBN structure is a prediction-oriented candidate.',
            'Ordinary fold shifts rows; filtered_fold_dt and filter_same_cycle explicitly provide separate-series safeguards.',
            'Selected folding and ID-filter source does not sort by timestamp or validate equal physical intervals.',
            'reduce_freq averages batches using ceiling(obj_freq/curr_freq), optionally grouped by IDs; arbitrary requested intervals and irregular calendars need adapter validation.',
            'The structure wrapper forwards supplied folds; downstream search engines are not audited or run in this review.'],
        'seqICP':['The API separates iid and autoregressive models; nonlinear routine assumes iid additive noise and a suitable regression class.',
            'Reducing max.parents and default stopIfEmpty limit stated confidence-interval coverage; selected source retains all-rejected-model flag.',
            'The accepted-set intersection uses p>alpha despite misleading adjacent comments saying rejected sets.',
            'AIC-selected lag count, finite Monte CarloB and nonlinear residual permutation do not automatically inherit the original fixed-lag linear theorem.'],
        'tpc':['Partial node ordering and explicit context/forbidden edges are supported; no stationary lag process is established by tier labels alone.',
            'context.all and context.tier force particular adjacency structures, so calendar-context encoding is a scientific assertion.',
            'Forbidden edges can override context constraints with a printed conflict note; adapter must retain the effective constraints.',
            'Package identity is separate from causalDisco; matching TPC names are not proof of implementation equivalence.']}
    packages=[];sources=[]
    for name,files in anchors.items():
        tree=json.loads((BASE/(name+'-tree.json')).read_text());assert not tree['truncated']
        pin=tree['sha'];cut=json.loads((BASE/(name+'-cutoff.json')).read_text())[0]
        assert cut['sha']==pin;date=cut['commit']['committer']['date'];assert date<='2026-10-07T15:59:59Z'
        idx={r['path']:r['sha']for r in tree['tree']};records=[]
        desc=(BASE/(name+'__DESCRIPTION')).read_text()
        fields={l.split(':',1)[0]:l.split(':',1)[1].strip()for l in desc.splitlines()if ':'in l and not l.startswith(' ')}
        for upstream,anchor in files.items():
            path=BASE/(name+'__'+upstream.replace('/','__'));data=path.read_bytes()
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==idx[upstream]
            records.append({'source_identity':'https://raw.githubusercontent.com/cran/'+name+'/'+pin+'/'+upstream,
                'upstream_path':upstream,'revision':pin,'source_date':date,'local_copy':ref(path,anchor),
                'git_blob_sha1':blob,'tree_identity_verified':True,'inspected_anchors':[anchor]})
        pkg={'package':name,'version':fields['Version'],'revision':pin,'source_date':date,
            'declared_license':fields['License'],'dependency_qualification':False,'upstream_execution':False,
            'cutoff_query':ref(BASE/(name+'-cutoff.json'),'Last mirror commit before Shanghai cutoff'),
            'tree':ref(BASE/(name+'-tree.json'),'Untruncated original tree'),'records':records,'supported_claims':claims[name]}
        packages.append(pkg)
        sources.append({'integrated_citation_key':'exec14_rtime_'+name.lower(),'kind':'software_primary_sources',
            'title':name+' temporal and interventional source inspection','author':name+' contributors',
            'year':int(date[:4]),'source_identity':'https://github.com/cran/'+name,'version_date':fields['Version']+'; '+pin+'; '+date,
            'local_copy':records[0]['local_copy'],'records':records,'inspected_anchors':[v for v in files.values()],
            'supported_claims':claims[name],'limitations':LIMITS})
    # Preserve original conflicting date fields rather than silently inventing a version date.
    ns={'a':'http://www.w3.org/2005/Atom'};e=ET.fromstring((BASE/'sequential-version.xml').read_text()).find('a:entry',ns)
    assert e.findtext('a:id',namespaces=ns).endswith('1706.08058v1')
    paper=ROOT/'docs/papers/Invariant Causal Prediction for Sequential Data Pfister(2017).pdf'
    data=(BASE/'sequential-paper-v1.pdf').read_bytes();assert data.startswith(b'%PDF-')
    if paper.exists():assert paper.read_bytes()==data
    else:paper.write_bytes(data)
    page_text=(BASE/'sequential-paper-v1.txt').read_text().split(chr(12));assert '1706.08058v1'in page_text[0]
    inspected=[];(BASE/'inspected').mkdir(exist_ok=True)
    for page in [1,3,4,5,6,7,15,16,17]:
        p=BASE/'inspected'/f'sequential-page-{page}.txt';p.write_text(page_text[page-1]);inspected.append(ref(p,f'Physical PDF page{page}'))
    paper_claims=['Definition2.1 assumes a fixed linear Gaussian target mechanism with iid innovations; causal interpretation requires additional structural independence.',
        'Proposition2.4 bounds false included parents by a subset guarantee if the relevant tests have level alpha; it is not full-graph/effect coverage.',
        'Propositions3.1 and6.1 describe level as Monte CarloB tends to infinity; Section6 fixes a sufficient lag order and warns about post-selection.',
        'Remark3.2 calls nonlinear/non-Gaussian residual permutation heuristic; Section6 targets instantaneous parents after adding all variable lags.',
        'Heterogeneity in predictor mechanisms can provide power while the target mechanism is held fixed.']
    scholarly={'integrated_citation_key':'exec14_rtime_pfister','kind':'paper','title':'Invariant Causal Prediction for Sequential Data',
        'author':'Niklas Pfister and Peter Bühlmann and Jonas Peters','first_author':'Pfister','year':2017,
        'source_identity':'https://arxiv.org/pdf/1706.08058v1','version_date':'arXiv1706.08058v1; API and margin2017-06-25; internal title date2018-09-25',
        'identity_discrepancy':'The original returned by the explicitv1 URL has a2017 margin/API and a2018 internal title date. Both predate cutoff; do not silently call these identical dates.',
        'local_path':str(paper.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),'local_copy':ref(paper,'Genuine original PDF; version/date discrepancy retained'),
        'metadata':ref(BASE/'sequential-version.xml','Identity only'),'extracted_text':ref(BASE/'sequential-paper-v1.txt','Original technical text'),
        'inspected_anchors':inspected,'supported_claims':paper_claims}
    sources.append(scholarly)
    # Reinspect genuine inherited pcalg originals without altering their citation records.
    old={s['integrated_citation_key']:s for s in json.loads(AUDIT.read_text())['sources']}
    inherited=[]
    pp=Path('/tmp/causal-pcalg-manual.txt').read_text().split(chr(12))
    for page in [63,78,79,80,104]:
        p=BASE/'inspected'/f'pcalg-page-{page}.txt';p.write_text(pp[page-1]);inherited.append(ref(p,f'Physical pcalg manual page{page}'))
    pcalg={'preserved_source':old['exec13_pcalg'],'additional_anchors':inherited,
        'fci_jci':ref(ROOT/'docs/literature/raw/exec13_latentr_man_fci.txt','244-267: context assumptions and defaults'),
        'claims':['GIES requires intervention targets and row-to-target indices and returns an interventional essential graph plus a representative.',
            'Essential-graph undirected adjacency must not be recoded as a latent-PAG bidirected edge despite plotting conventions.',
            'FCI-JCI context variables encode declared exogeneity/randomized-context assumptions; a calendar label alone supplies none of that truth.']}
    search=json.loads((BASE/'tsgfci-search.json').read_text());assert search['total_count']==0
    omissions={'cutoff':'2026-10-07 Asia/Shanghai','new_public_GETs':28,'bound':28,
        'search_scope':'Four named CRAN mirrors pinned before cutoff; one current GitHub repository-name search for tsGFCI; inherited pcalg originals.',
        'search_result':ref(BASE/'tsgfci-search.json','Zero indexed repository-name matches; not a historical census or proof of absence'),
        'open':[{'candidate':'tsGFCI','reason':'Repository-name query gives zero; Tetrad engine/interface aliases and historical releases not exhausted.',
            'route':'Review pinned Tetrad tsGFCI implementation, actual R bridges and citations; compare endpoint/lag semantics.'},
            {'candidate':'Wider R temporal ecosystem','reason':'Additional nonlinear, mixed-frequency, continuous-time and panel discovery families are not exhaustively screened.',
             'route':'Expand primary registry/method-index queries under a separately reviewed bounded acquisition plan.'},
            {'candidate':'causalDisco output conversions','reason':'Source/help disagree; pinned caugi and execution not inspected.',
             'route':'Pin dependencies, read conversion constructors, then run marked-edge round trips if a prototype is justified.'},
            {'candidate':'Package release/rights and theorem versions','reason':'Declared licenses and selected originals do not establish all dependencies or all later theorem revisions.',
             'route':'Resolve dependency/redistribution matrix, inspect current-within-cutoff paper revisions, predeclare runtime regimes.'}],
        'unavailable_source_waiver':False,'coverage_complete':False}
    decisions=[]
    for name,choice,reason,route in [
        ('causalDisco','integrate','Potential R facade for tier-aware graph work; documentation/source discrepancy prevents enabling output conversion.',
         'Prototype separate tier metadata, CI-test sentinels and endpoint round trips; compare pcalg and original tpc in declared sampling laws.'),
        ('tpc','reference','Maintain a separate comparator for cohort-wave ordering and explicit context assumptions.',
         'Preserve context/forbidden-edge precedence; verify graph matrix direction before considering an adapter.'),
        ('dbnR','integrate','Potential lag/forecast baseline with an existing ID boundary filter; no causal effect service is justified.',
         'Validate chronological group ordering and physical intervals; use supplied verified folds and train/test separation.'),
        ('seqICP','integrate','Candidate target-parent/invariance service under its declared mechanism and testing restrictions.',
         'Return parent-set semantics, modelReject, lag selection and Monte Carlo settings; qualify generated linear cases before nonlinear extensions.'),
        ('pcalg','reference','Retain inherited GIES/FCI-JCI candidate with intervention/context semantics, not an automatic temporal estimator.',
         'Carry known target membership and context assumption IDs; return equivalence-class endpoints and graph-to-effect obligations.')]:
        decisions.append({'package':name,'decision':choice,'status':'proposed_only','integration_allowed':False,'reason':reason,'prototype_route':route,
            'direct_adopt':'Deferred until semantics/runtime/rights review.','port':'No port selected; compare the upstream R behavior before incurring equivalence and maintenance cost.',
            'reject':'Reject substitution of temporal order or predictive fit for identified intervention effects.'})
    write(BASE/'primary-review.json',{'packages':packages,'scholarly_original':scholarly,'pcalg':pcalg,
        'acquisitions':[ref(p,'Bounded original HTTP receipt')for p in sorted(BASE.glob('acquisition-*.json'))],
        'limitations':LIMITS})
    write(BASE/'exact-results.json',exact());write(BASE/'omissions-register.json',omissions);write(BASE/'reuse-decisions.json',{'decisions':decisions})
    sources += [{'integrated_citation_key':'exec14_rtime_exact','kind':'project_derivation','title':'Exact calendar, aggregation and series-boundary references',
        'author':'Causal banking proposal','year':2026,'source_identity':'Project-authored exact finite laws','version_date':'2026-10-14',
        'local_copy':ref(BASE/'exact-results.json','Stationary equal laws, aggregation, boundaries and calendar variance'),
        'records':[ref(Path(__file__),'exact() rational enumeration')],'inspected_anchors':['exact()'],
        'supported_claims':['Effects0/4 and net-1/3 thousandUSD; aggregate projection0.5/0.5;4 valid boundary pairs; calendar SE factor10.']},
        {'integrated_citation_key':'exec14_rtime_contract','kind':'project_analysis','title':'R temporal sampling and reuse proposal',
        'author':'Causal banking proposal','year':2026,'source_identity':'Project-authored adapter proposal','version_date':'2026-10-14',
        'local_copy':ref(BASE/'reuse-decisions.json','Five bounded reuse dispositions'),'records':[ref(BASE/'omissions-register.json','Explicit search limits')],
        'inspected_anchors':['decisions and open routes'],'supported_claims':['Proposed integrations require temporal and graph semantics, public/generated prototypes and rights review.']}]
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources})
    evidence=[ref(p,'Reviewed R temporal evidence')for p in[BASE/'primary-review.json',BASE/'source-audit.json',BASE/'exact-results.json',
        BASE/'omissions-register.json',BASE/'reuse-decisions.json',BASE/'plan-review.md',BASE/'development.template',Path(__file__)]]
    verify_bindings(evidence)
    write(SYN,{'operation':OP,'status':'inconclusive','coverage_complete':False,'packages':[p['package']for p in packages]+['pcalg'],
        'findings':claims,'paper_findings':paper_claims,'decisions':decisions,'evidence':evidence,'limitations':LIMITS,
        'next_action':'Integrate reviewed argument, preserve omissions, then continue independent queue; proposed engines remain disabled.'})
    write(BASE/'author-review.json',{'status':'pass','scope':'Author review of bounded technical comparison; coverage inconclusive',
        'reviewer':REVIEWER,'evidence':evidence+[ref(SYN,'Required coverage outcome')],'limitations':LIMITS,'substantive_page_credit':0,
        'findings':['All17 inspected CRAN blobs match pinned trees. Genuine sequential original inspected with date discrepancy retained.',
            'Help/code class mismatch, existing DBN boundary safeguard, finiteB/lag selection and graph/effect distinctions retained.',
            'Exact examples reproduce; no runtime, finite empirical coverage, exhaustive search or bank return is asserted.']})
    graph,_,_=control.combined(ROOT,control.core.read(ROOT,control.core.STATE));node=control.ledger.operation(graph,OP)
    receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',scope='Bounded R temporal/interventional proposal coverage',reviewer=REVIEWER,
        outputs=[ref(SYN,'Required reviewed coverage output')],limitations=LIMITS)
    facts=[('inconclusive','Four pinned additional families and inherited pcalg inspected; tsGFCI aliases and broader temporal families remain open.'),
        ('pass','17 selected original blobs, a genuine convention-named scholarly PDF, exact reference and primary manual anchors are hash-bound.'),
        ('pass','Explicit reuse, omissions and prototype routes; zero repository matches are not treated as package absence.')]
    for c,(v,f)in zip(receipt['criteria'],facts):c.update(verdict=v,finding=f,evidence=evidence)
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'review':'pass','coverage':'inconclusive','packages':5,'verified_blobs':sum(len(p['records'])for p in packages),'new_sources':len(sources),'exact':exact()['aggregation']}))

if __name__=='__main__':main()
