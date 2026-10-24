#!/usr/bin/env python3
"""Authenticate pinned R network originals and review bounded dynamic inference comparisons."""
import argparse,hashlib,json
from pathlib import Path
import r_network_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as new_write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/r-network-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.networks_interference.R'
read=lambda p:json.loads(p.read_text())
def write(path,value):
    if path.exists():
        assert read(path)==value, 'Existing evidence differs: '+str(path)
    else:new_write(path,value)

LIMITS=['Bounded R repository searches,selected primary paths and uninspected search tails;no saturation or absence claim.',
 'No downloaded package,compiled binary or upstream test executed;authored exact witnesses are not native results.',
 'Exposure-specific effects,local IV targets,conditional tests,learned policies and model-based simulation have distinct scientific assumptions.',
 'Complete dependencies,installed artifacts,distribution rights,solver entitlement and runtime qualification remain open.',
 'True bank relationships,assignment validity,weak-IV uncertainty and arbitrary network dependence require information or justified restrictions.',
 'No scholarly theorem imported from source comments;visual,independent,bank and final acceptance remain open.']
NEXT='Complete R network search tails and primary delegates;qualify exposure labels,exact assignment support,marginals/joints,graph-distance kernels,weak-IV refusals,randomized near ties,typed failure,solver termination,missing ties/groups and nested simulation on frozen public known-law tasks before native admission.'
SPECS=read(BASE/'anchor-specifications.json')

def authenticate():
    rows=[];evidence=[]
    for name in ['source-selection.json','delegate-selection.json','final-selection.json']:
        rows.extend(read(BASE/name));evidence.append(ref(BASE/name,'Pinned selected file identities'))
    assert len(rows)==62
    originals=[]
    for x in rows:
        p=RAW/(x['id']+'.txt');data=p.read_bytes();receipt=p.with_suffix('.receipt.json');r=read(receipt)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['git_blob']
        assert len(data)==x['bytes'] and core.sha(p)==r['sha256'] and r['status']=='saved'
        originals.append(dict(repository_path=x['path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(receipt,'URL,date,hash')))
    for key in SPECS:
        c=read(RAW/f'exec25_rnet_{key}_commit.json');c=c[0] if isinstance(c,list) else c
        assert c['sha']==SPECS[key][2].split(';')[-1] and c['commit']['committer']['date'][:10]<='2026-10-07'
        tree=read(RAW/f'exec25_rnet_{key}_tree.json');assert tree['truncated'] is False
        evidence.extend([ref(RAW/f'exec25_rnet_{key}_{kind}.json','Dated pin and complete selected tree') for kind in ['commit','tree']])
    write(BASE/'authenticated-originals.json',dict(status='pass',count=62,originals=originals,evidence=evidence))

def prepare():
    assert not (BASE/'review.json').exists()
    authenticate();fragments=[];sources=[]
    for key,(title,repo,version,checks) in SPECS.items():
        evidence=[ref(RAW/f'exec25_rnet_{key}_commit.json','Revision and date')];anchors=[];claims=[]
        for suffix,lo,hi,tokens,finding in checks:
            p=RAW/f'exec25_rnet_{key}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));s='\n'.join(lines[lo-1:hi]);assert all(t in s for t in tokens),(p.name,lo,hi,[t for t in tokens if t not in s])
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=key,source=binding,first_line=lo,last_line=hi,text=s))
        sources.append(dict(integrated_citation_key='exec25_rnet_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][-4:]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=len(fragments)))
    write(BASE/'exact-results.json',exact.calculate());queries=[];leads={}
    for p in sorted(RAW.glob('exec25_rnet_search*.json')):
        if 'receipt' in p.name:continue
        d=read(p);receipt=p.with_suffix('.receipt.json')
        for x in d['items']:leads.setdefault(x['full_name'],dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected'))
        queries.append(dict(query=read(receipt)['url'],total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(receipt,'Query identity')))
    for repo in [x[1] for x in SPECS.values()]:
        if repo in leads:leads[repo]['status']='selected_primary_anchors_only'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),additional_named_candidates=[x[1] for x in SPECS.values()],saturation_claim=False,absence_claim=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Original identities and exact anchors') for n in ['authenticated-originals.json','inspected-extracts.json']],groups=8,anchors=len(fragments),native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Exact rational and enumeration witnesses'),ref(BASE/'exact-results.json','Replay'),ref(BASE/'source-correction-review.json','Symmetry misreading corrected before binding')],checks=['Mixed neighborhood is not all-control.','Four corrected marginals2/5 sum8/5 versus exact1/4 each.','Heterogeneous exposure probability16/25 differs from selected4/25.','Adjacent-pair joint1/4 differs from helper1/16;actual variance pair filter separately inspected.','Actual symmetry guard rejects two unequal transpose entries.','Centered path score quadratic is-2/9.','Overlapping approximate ties and strict tails yield21/16 and derived-5/8;nondegeneracy condition passes.','Candidate graph intersection can have zero structural support despite smoothing1/10.','Available-group mean5 differs from fixed-denominator arithmetic10/3;missing truth unknown.','Full collection of six equiprobable vectors has expected147/10 draws,no fixed bound.','Hypothetical costs30/50/75 retain denominators.'],native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='R network targets,assignment laws,exposure semantics and complete uncertainty',selected=list(SPECS),decisions=['interference: conditional design-based adapter after label,probability and covariance tests.','latenetwork: bounded IV reference and adapter candidate after support,kernel and weak-stage qualification.','BicliqueRT: conditional test candidate after typed failure,near-tie and assignment-law repair/qualification.','NetworkTargeting: reference only until rights,solver termination,focal population and missing-edge contracts resolved.','NetworkCausalTree: defer native admission pending induced-graph,marginal,joint and pair-selection qualification.','MisspecifiedInterference: reference study;structural support and rights unresolved.','autognet: conditional network-model integration after native-index,Monte Carlo and convergence tests.','clusteredinterference: conditional group-policy reference after failure typing,group accounting and sampling qualification.'],limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Declarations and selected native boundaries')],findings=['interference,latenetwork,NetworkCausalTree and autognet have MIT declarations and holder sources.','BicliqueRT and clusteredinterference declare GPL3.','NetworkTargeting has root GPL3 text but placeholder DESCRIPTION and Gurobi dependency;full coherent rights/entitlement not cleared.','MisspecifiedInterference has an unevaluated license helper in DESCRIPTION and no license original in complete inspected tree.','Native bimax registration and Rcpp simulation paths inspected;complete installed/dependency distribution remains unqualified.'],integration_allowed=False))
    tests=['Exact design enumeration and exposure labels,orientation and two-hop semantics','Structural support versus corrected simulation frequencies','Heterogeneous and adjacent-pair assignment probabilities','Discovery/estimation split and cross-cluster background ties','Weak-IV support and graph HAC versus bootstrap law','Near ties,randomized tails,nonfinite statistics and typed p-value failures','Solver status,tolerance propagation and imputed graph/focal changes','Missing group denominator and quadrature error versus zero probability','Nested simulation burnin,thinning,individual intervention and Monte Carlo error','Installed artifact,rights,complete requests and full costs']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,owners=['Scientific author','Adapter owner','Artifact/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded search and tails')],known_routes=['Complete primary delegates and installed artifact provenance.','Freeze public known-law contracts before native experiments.'],unknown_universal_repairs=['Unknown graph truth,assignment validity and exclusion require information or justified restrictions.','No universal latent-identification or arbitrary-dependence repair is promised.'],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_rnet_choice',kind='project_evidence_not_scholarly_paper',title='Authored R network exposure,probability,uncertainty and failure comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026;cutoff7 October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored exact witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Exposure,design probabilities,network scores,randomized tails,missing groups,simulation and costs',inspection='Author inspection')],supported_claims=['Exact authored witnesses and conditional candidate decisions','Bounded search and proposed public qualification'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=9,new_scholarly_pdfs=0,evidence=[ref(BASE/'authenticated-originals.json','62 authenticated originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed planned and actual evidence') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['62 authenticated retrievals representing61 unique original files,eight collections and one authored comparison.','Trace exposure/probability helpers,callers,variance pair selection,randomization tails,solver paths,quadrature and native simulation before claims.','Separate source review from native and scientific qualification.','Serial canonical publication after consumed remaining-language dynamic delivery.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking targets and substantive alternatives'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Eight distinct network targets with exact authored examples and candidate-specific reuse decisions.','Source predicates,authored calculations and proposed tests separated.','Open coverage,rights,native and final acceptance retained.'],visual_acceptance=False))
    names=['source-correction-review.json','authenticated-originals.json','primary-review.json','mathematical-review.json','comparison-review.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Reviewed bounded comparison') for n in names]+[ref(BASE/'anchor-specifications.json','Exact source predicates'),ref(Path(__file__),'Review logic')],findings=['62 authentic files and exact anchors retain source/native distinction.','Network targets,exposure probabilities,uncertainty,failure and population contracts explicit.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=62,anchors=len(fragments),unique_leads=len(leads),new_records=9,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Selected R network candidates identified; search,delegate and native coverage incomplete.','Claims bind authentic dated bytes and exact anchors; no scholarly theorem imported.','Alternatives and public qualification routes retain numerical,rights and native limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='R network targets,assignment,exposure,uncertainty and failure source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('R network dynamic inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
