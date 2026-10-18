#!/usr/bin/env python3
"""Finish the recovered, unpublished R-identification audit without changing predecessors."""
import hashlib
import json
from pathlib import Path
import shutil

from publish_latent_r_review_v2_20261013 import ref, verify_bindings
import r_identification_reference_20261018 as exact
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-18/r-identification'
READER=BASE.parent/'r-identification-reader'
RAW=ROOT/'docs/literature/raw'
PRIOR=BASE.parent/'bayesian-advice/reader/source-audit.json'

def read(p): return json.loads(p.read_text())
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def bound(p,anchor): return ref(p,anchor)
def span(p,start,end,finding):
    assert 1<=start<=end<=len(p.read_text().splitlines())
    return dict(bound(p,f'Lines {start}-{end}'),line_spans=[[start,end]],finding=finding)


def main():
    assert not (READER/'prepared-inputs.json').exists(), 'Inputs already frozen'
    rows=read(BASE/'selected-source-map-v2.json')['files']
    byname={}
    for r in rows:
        p=RAW/(r['id']+'.txt');b=p.read_bytes();receipt=read(RAW/(r['id']+'.receipt.json'))
        assert hashlib.sha256(b).hexdigest()==receipt['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha1']
        byname.setdefault(r['name'],[]).append(r)
    authors={
        'causaleffect':'Santtu Tikka',
        'dosearch':'Santtu Tikka and Antti Hyttinen and Juha Karvanen',
        'cfid':'Santtu Tikka',
        'causaloptim':'Michael C. Sachs and Erin E. Gabriel and Arvid Sjölander and Gustav Jonzon',
        'bpbounds':'Tom Palmer and Roland Ramsahai and Vanessa Didelez and Nuala Sheehan',
        'causalqueries':'Macartan Humphreys and Till Tietz and Alan Jacobs and Lily Medina and Georgiy Syunyaev'}
    specifications={
        'causaleffect':[(1,1,65,'causal.effect graph/query/options and expression output'),(2,1,65,'ID/IDC dispatch; documented nonidentification error, id=FALSE, empty string and NULL branches')],
        'dosearch':[(2,1,128,'Multiple distributions, target and output contract'),('extra_0',1,125,'Initializer derives identifiable from found target; positive limit returns without timeout result field')],
        'cfid':[(5,1,100,'Parallel worlds share latent variables; default intervention data; id/formula/undefined output and probability-zero inconsistency')],
        'causaloptim':[(2,1,78,'Response-function p=Rq and c0q objective; left/right, latent and nvals graph restrictions'),(3,1,30,'Bound computation for a constructed symbolic optimization object')],
        'bpbounds':[(1,1,79,'Trivariate or specified two-source tables; binary X,Y, two/three-category Z; ordinary and monotonicity bounds and IV inequality diagnostics')],
        'causalqueries':[(2,1,88,'Parameter/prior/posterior query input and mixed confidence/credible interval terminology'),(3,1,47,'Stan update and MAR assumption for missing long-form data')]
    }
    audit=read(BASE/'recovered-drafts/r-identification-source-audit.json')
    for s in audit['sources'][:6]:
        name=s['integrated_citation_key'].removeprefix('exec18_rid_');items=byname[name];pin=items[0]
        s.update(author=authors[name],year=int(pin['commit_date'][:4]),source_identity='https://github.com/'+pin['repository'],
                 commit=pin['commit'],commit_date=pin['commit_date'],retrieval_date='2026-10-18 Asia/Shanghai',
                 software_executed=False,rights_qualified=False)
        s['version_date']+='; full pin '+pin['commit']
        s['acquisition_receipt']=bound(ROOT/s['acquisition_receipt']['path'],'Original acquisition receipt')
        s['identity_evidence']=[bound(RAW/(f'exec18_rid_{kind}_{name}{suffix}'),'Pinned identity/tree; metadata is not technical evidence') for kind in ['commit','tree'] for suffix in ['.json','.receipt.json']]
        s['records']=[]
        for r in items:
            p=RAW/(r['id']+'.txt')
            s['records'].append(dict(upstream_path=r['upstream_path'],git_blob_sha1=r['git_blob_sha1'],
                                    local_copy=bound(p,r['upstream_path']),
                                    receipt=bound(RAW/(r['id']+'.receipt.json'),'Public acquisition and file hash'),
                                    role='acquired_primary_source; inspected claims limited to explicit anchors'))
        s['inspected_anchors']=[]
        for suffix,start,end,finding in specifications[name]:
            p=RAW/(f'exec18_rid_{name}_{suffix}.txt')
            s['inspected_anchors'].append(span(p,start,min(end,len(p.read_text().splitlines())),finding))
        description=RAW/(f'exec18_rid_{name}_0.txt')
        s['inspected_anchors'].append(span(description,1,len(description.read_text().splitlines()),'Package identity, authors, version, declared license and dependencies; no dependency-rights conclusion'))
        s['limits']='Selected primary-source inspection only. Not an installation, runtime, dependency/rights qualification, exhaustive historical release census or bank validation.'
        if name=='causaleffect':
            s['date_discrepancy']='DESCRIPTION Date 2026-09-19 differs from commit timestamp 2025-09-19. Both retained; no silent reconciliation. Selected bytes verified against pinned Git tree.'
        if name=='bpbounds':
            s['upstream_author_repository']='https://github.com/remlapmot/bpbounds'
            s['mirror_identity']='Selected bytes and commit belong to cran/bpbounds; upstream author repository is identified in DESCRIPTION, not the pin source.'
            s['inspected_anchors'][0]['finding']='Binary outcome/treatment, two or three instrument categories; trivariate/two-source data and separate monotonicity/IV inequality outputs.'
        if name=='causalqueries':
            s['supported_claims'].append('The stats argument calls the default interval a confidence interval; cred and output cred.low/cred.high describe credible summaries. Distribution and uncertainty type must be retained explicitly.')
        if name=='dosearch':
            p=RAW/'exec18_rid_dosearch_2.txt';lines=p.read_text().splitlines()
            for i,line in enumerate(lines):
                if 'not complete' in line or 'time_limit' in line:
                    s['inspected_anchors'].append(span(p,max(1,i-1),min(len(lines),i+5),'Documented search incompleteness or limit control'))
    papers={
        'exec18_rid_cfid_paper':('exec18_rid_cfid_paper','Santtu Tikka','arXiv:2210.14745v2, 2023-11-22; published identity DOI 10.32614/RJ-2023-053',[1,2,8],['exec18_rid_cfid_meta.json','exec18_rid_cfid_meta.receipt.json','exec18_rid_cfid_paper.receipt.json']),
        'exec18_rid_dosearch_paper':('exec18_rid_dosearch_paper_arxiv','Santtu Tikka and Antti Hyttinen and Juha Karvanen','arXiv:1902.01073v5, 2021-08-27; JSS 99(5), DOI 10.18637/jss.v099.i05',[1,2,4],['exec18_rid_dosearch_paper_identity.json','exec18_rid_dosearch_paper_identity.receipt.json','exec18_rid_dosearch_paper_arxiv.receipt.json'])}
    for s in audit['sources'][6:8]:
        prefix,author,version,pages,identity=papers[s['integrated_citation_key']]
        s.update(author=author,version_date=version,local_path=s['local_copy']['path'],sha256=s['local_copy']['sha256'])
        s['identity_evidence']=[bound(RAW/x,'Discovery/publication identity or original PDF acquisition') for x in identity]
        s['inspected_anchors']=[dict(anchor=f'Physical PDF page {page}',extracted_text=bound(BASE/'paper-anchors'/f'{prefix}-page{page}.txt','Extracted authentic primary page'),finding=('Counterfactual recursive SCM/data-level/parallel-world scope and examples' if 'cfid' in prefix else 'Do-calculus search, source classes and explicit completeness qualifications; Table 1 separates complete ID/IDC, unknown general multi-source, incomplete missingness')) for page in pages]
    s=audit['sources'][-1]
    s.update(local_copy=bound(ROOT/'tools/r_identification_reference_20261018.py','calculate: exact Fraction enumeration'),results=bound(BASE/'exact-results.json','Executed exact reference'))
    s['inspected_anchors']=[dict(s['local_copy'],finding='Checks response-type probabilities, equal likelihoods, prior-dependent PN, sharp population endpoints and retrospective monetary transformation; observationally equivalent hidden-confounding SCMs have ATE 1 and 0.')]
    audit.update(cutoff='2026-10-07',verification=bound(BASE/'blob-verification-v2.json','38 acquired source files verified against receipts and pinned Git blobs'),source_map=bound(BASE/'selected-source-map-v2.json','Exact upstream paths and pins'),author_review=True,independent_review=False)
    verify_bindings(audit)
    save(BASE/'source-audit.json',audit);save(READER/'source-audit.json',audit)
    assert exact.calculate()==read(BASE/'exact-results.json')
    shutil.copyfile(BASE/'exact-results.json',READER/'exact-results.json')
    prior=read(PRIOR);old={s['integrated_citation_key']:s for s in prior['sources']}
    inherited=[]
    for candidate,name,key,aliases,role in [
      ('seed:045','dagitty','exec13_other_dagitty',['DAGitty','jtextor/dagitty','R/V8 interface'],'graph adjustment/authoring'),
      ('seed:046','pcalg','exec13_pcalg',['IDA','jointIda','CPDAG/PDAG effects'],'Gaussian faithful no-hidden-variable effect multiset'),
      ('seed:047','bnlearn','exec13_bnlearn',['bnlearn R','intervention/counterfactual functions'],'causal Bayesian network query/simulation'),
      ('seed:048','causaleffect','exec18_rid_causaleffect',['causal.effect','ID','IDC'],'symbolic interventional identification'),
      ('seed:051','ivmodel','v12_sw_ivmodel',['AR.test','CLR'],'IV sampling confidence sets')]:
        inherited.append(dict(candidate_id=candidate,name=name,aliases=aliases,citation_key=key,role=role,status='selected_primary_scope_inspected',runtime='not_run_this_review'))
    additions=[dict(candidate_id='exec18:rid:'+name,name=name,aliases=[name,byname[name][0]['repository']],citation_key='exec18_rid_'+name,status='selected_pinned_primary_scope_inspected') for name in ['dosearch','cfid','causaloptim','bpbounds','causalqueries']]
    omissions=[
      dict(name='SEMID',status='discovery_lead_uninspected',action='Obtain pre-cutoff primary original and determine semiparametric/structural identification scope before inclusion.'),
      dict(name='Counterfactual / WhatIf / R6causal',status='citation_chain_leads_uninspected',action='Resolve package identities and pre-cutoff originals; cfid paper page2 distinguishes estimation/simulation from identification. Do not infer package capabilities from the paper alone.'),
      dict(name='Broader IV and mediation neighbours',status='taxonomy_boundary_unresolved',action='Reconcile IV/mediation cells and aliases against the identification taxonomy; record justified exclusions individually.'),
      dict(name='CausalQueries JSS117(1)',status='original_unavailable_on_attempted_route',action='Acquire genuine article through a public permitted route before citing it; current claims use authentic package documentation.',evidence=bound(RAW/'exec18_rid_causalqueries_paper.receipt.json','Failed acquisition; no substitute article')),
      dict(name='Repository search',status='HTTP403',action='Retry bounded repository discovery when access is available; current six pins do not establish exhaustive coverage.',evidence=bound(RAW/'exec18_rid_search_repos.receipt.json','Failed search receipt')),
      dict(name='Historical CRAN task view',status='current_snapshot_only',action='Find pre-cutoff snapshot before making a historical census claim.',evidence=bound(RAW/'exec18_rid_cran_taskview.receipt.json','Post-cutoff discovery snapshot'))]
    register=dict(operation='SW.CELL.identification_counterfactual.R',cutoff='2026-10-07',inherited=inherited,complementary=additions,omissions=omissions,
                  scope='Bounded review of 10 named families, not exhaustive R census',
                  search_execution='Five preserved manifests: identity/discovery, selected files, supplemental source paths, PDF/timeout evidence, and alternate arXiv original. Original two-round wording was underspecified; actual five batches are disclosed. No further retry in this attempt.',
                  stopping_rule='Stop this source attempt after the five saved manifests; unresolved leads retain inconclusive dispositions. Continue independent work.',
                  evidence=[bound(BASE/f'fetch-manifest-0{i}.json','Executed bounded acquisition batch') for i in range(1,6)]+[bound(RAW/'exec18_rid_search_works.json','Scholarly discovery only'),bound(BASE/'cran-taskview-text.txt','Current task-view discovery only'),bound(PRIOR,'Preserved inherited source records'),bound(BASE/'source-audit.json','Selected primary technical evidence')],
                  later_qualification='Native runtime, full dependency/rights closure and bank validation are later work; runtime absence alone is not a proposal-cell blocker.')
    save(BASE/'candidate-omissions-register.json',register)
    manuscript=bound(BASE/'development.tex','Final reviewed section inserted in software chapter S3')
    evidence=[manuscript,bound(BASE/'source-audit.json','Nine new source records'),bound(BASE/'candidate-omissions-register.json','Candidates, aliases and bounded omissions'),bound(BASE/'exact-results.json','Reproduced rational calculations'),bound(ROOT/'tools/r_identification_reference_20261018.py','Exact reference source'),bound(Path(__file__),'Audit construction and review specification')]
    plan=read(BASE/'plan-review.json');plan.update(status='reviewed_proceed',evidence=evidence,next_action='Prepare and compile preserving reader; retain inconclusive source coverage, publish working bytes and record outcome; then continue independent operation.')
    save(READER/'plan-review.json',plan)
    math=dict(status='pass',reviewer={'name':'Codex author/coordinator','kind':'author'},evidence=evidence,findings=[
      'Nonnegativity and fixed marginals give the full one-dimensional fiber, t in [0,1/4]. Constructing a response-type SCM at every t proves sharpness; three executed worlds alone would not prove continuous sharpness.',
      'ATE=1/2; PN=1-4t/3 in [2/3,1]; monotonicity removes q10 and sets t=1/4.',
      'Ordered likelihood (1/4)^2(3/4)^6=729/65536 and aggregate likelihood 16 times this value are constant across stipulated worlds. Posterior weights therefore remain prior weights, yielding means 5/6 and 7/9.',
      '1000*PN-800 has sharp range [-400/3,200]; posterior means 100/3 and -200/9. This is stipulated retrospective accounting, not observed ROI or prospective policy choice.',
      'A=U with Y=A versus Y=U has identical observed distribution and different do effects (1 versus 0). Both lie in the admitted supergraph; no faithfulness assumption is imposed in this counterexample.',
      'Population-risk identification, finite-sample confidence coverage and Bayesian summaries remain distinct; no package runtime or independent review claimed.'],visual_acceptance=False)
    save(READER/'mathematical-review.json',math)
    primary=dict(status='pass_for_cited_claims',reviewer={'name':'Codex author/coordinator','kind':'author'},evidence=evidence+[bound(PRIOR,'Unchanged inherited evidence'),span(BASE/'pcalg-manual.txt',4203,4248,'IDA Gaussian faithfulness, no hidden variables, effect multiset and local/global multiplicity'),span(BASE/'dagitty-manual.txt',86,137,'Adjustment-set contract and criteria'),bound(RAW/'v12_sw2_manual_ivmodel_1.txt','AR interval components'),bound(RAW/'v12_sw2_manual_ivmodel_2.txt','CLR inversion, weak instruments, interval components')],findings=[
      'All38 selected source blobs match acquisition SHA256 and pinned tree SHA1; six full pins and metadata receipts are bound. This verifies identity, not runtime correctness.',
      'causaleffect nonidentification has option-dependent representations, distinct from invalid input failures.',
      'dosearch timed early return and incomplete problem classes cannot support universal negative certificates. Table1 completeness classifications retained.',
      'cfid defaults to interventions; zero formula for inconsistency and actual undefined field preserved without inventing an inconsistency flag.',
      'causaloptim left/right response-function restrictions and bpbounds binary/two-or-three-category IV scope retained; bound endpoints not relabelled sampling intervals.',
      'CausalQueries confidence/credible terminology discrepancy retained and resolved at proposed result-type level; Stan/MAR assumptions documented.',
      'bpbounds mirror versus upstream identity and causaleffect date discrepancy explicitly recorded; paper author lists and arXiv versions repaired.',
      'Broader source coverage remains inconclusive, with no unsupported package-absence or exhaustive-census claim.'],independent_acceptance=False)
    save(READER/'primary-review.json',primary)
    copy=dict(status='pass_source_copyedit_pending_build',reviewer={'name':'Codex author/coordinator','kind':'author'},evidence=evidence,repairs=[
      'Repaired align row terminator; equation labels remain unique and numbered.',
      'Plain citation keys; no escaped underscores inside citation identifiers.',
      'Corrected cfid output-field claim and strengthened IDA assumptions.',
      'Removed acquisition-process prose from narrative and retained failures/omissions in audit.',
      'Explained randomization, population versus sample, prior sensitivity and retrospective monetary units.',
      'Added conditional reuse choices and deferred ports with explicit reasons; process separation confers no license exemption.'],visual_acceptance=False,remaining='Compile and inspect text/page bounds; rendered visual acceptance remains pending under inherited image allowance.')
    save(READER/'copyedit-review.json',copy)
    for p in READER.glob('*review.json'): verify_bindings(read(p))
    print(json.dumps(dict(sources=9,pinned_source_blobs=38,candidates=10,omissions=len(omissions),upstream_runtime=False,visual_acceptance=False)))

if __name__=='__main__': main()
