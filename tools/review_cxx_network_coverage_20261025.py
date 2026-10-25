#!/usr/bin/env python3
"""Authenticate selected C++ originals and review bounded proposal findings."""
import argparse,hashlib,json
from pathlib import Path
import cxx_network_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as write_new,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/cxx-network-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.networks_interference.Cxx'
read=lambda p:json.loads(p.read_text());SPECS=read(BASE/'anchor-specifications.json')
def write(path,value):
    if path.exists():
        assert read(path)==value, 'Preserve differing evidence: '+str(path)
    else:write_new(path,value)
LIMITS=['Six bounded repository searches and selected anchors; no saturation or absence claim.',
 'No acquired source, native C/C++ artifact, upstream test or simulator executed.',
 'Authored arithmetic is not observed native behavior or a validated bank mechanism.',
 'Complete installed artifacts, dependency rights and causal estimator qualification remain open.',
 'Unknown bank graph and assignment truth, latent confounding and unrestricted dependence require information or justified restrictions.',
 'Selected2020paper only;no theorem from source comments;visual,independent and final acceptance remain open.']
NEXT='Complete bounded C++ discovery tails and RGCR rights/old-artifact provenance; qualify exact exposure probabilities,empty-arm refusal,graph-weight roundtrips,thread/rank random ownership and distributed clocks on frozen public known-law tasks before native admission.'
DECISIONS=['RGCR: conditional algorithmic reference; defer adoption until rights,SNAP4.1artifact,assignment law,ratio-empty-arm,probability approximation and replay gates pass.',
 'NetworKit: conditional graph integration; qualify duplicate handling,mappings,weight roundtrips and thread-specific random streams.',
 'SNAP: conditional graph integration; preserve simple/multigraph choice,direction,ID holes and return codes;selected tree is not RGCR SNAP4.1artifact.',
 'Repast HPC: conditional distributed public experiment environment;qualify agent/replica identity,projection freshness,phase ordering and rank-specific streams.',
 'igraph: conditional C-core interoperability;qualify exact interface,ID remapping,RNG ownership and intendedGPLdistribution.',
 'Ports require explicit semantic references and justified runtime benefit;none substitutes for causal identification.']

def authenticated_json(p):
    r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256']
    return read(p)

def prepare():
    assert not (BASE/'review.json').exists()
    rows=read(BASE/'source-selection.json')+read(BASE/'delegate-selection.json')+read(BASE/'follow-selection.json');assert len(rows)==64
    originals=[];identity=[];trees={}
    for x in read(BASE/'pins.json'):
        prefix='exec25_cnet_'+x['key']
        cp=RAW/(prefix+'_commit.json');tp=RAW/(prefix+'_tree.json')
        c=authenticated_json(cp);c=c[0] if isinstance(c,list) else c;t=authenticated_json(tp)
        assert c['sha']==x['commit'] and c['commit']['committer']['date']==x['date']
        assert x['date']<='2026-10-07T15:59:59Z' and not t['truncated'] and t['sha']==x['commit']
        trees[x['key']]={y['path']:y for y in t['tree'] if y['type']=='blob'}
        identity.extend([ref(cp,'Pinned revision and date'),ref(tp,'Complete selected tree')])
    for x in rows:
        p=RAW/(x['id']+'.txt');data=p.read_bytes();rp=p.with_suffix('.receipt.json');r=read(rp)
        assert len(data)==x['bytes'] and r['status']=='saved' and core.sha(p)==r['sha256']
        assert x['commit'] in r['url'] and r['url'].endswith('/'+x['path'])
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['git_blob']
        assert trees[x['group']][x['path']]['sha']==x['git_blob']
        originals.append(dict(repository_path=x['path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'URL,date,hash')))
    write(BASE/'authenticated-originals.json',dict(status='pass',count=64,technical_license_configuration=64,originals=originals,evidence=identity))
    fragments=[];sources=[]
    for key,(title,repo,version,checks) in SPECS.items():
        evidence=[ref(RAW/f'exec25_cnet_{key}_commit.json','Revision and date')];anchors=[];claims=[]
        for suffix,lo,hi,tokens,finding in checks:
            p=RAW/f'exec25_cnet_{key}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));s='\n'.join(lines[lo-1:hi]);assert all(t in s for t in tokens),(p,lo,hi)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=key,source=binding,first_line=lo,last_line=hi,text=s))
        sources.append(dict(integrated_citation_key='exec25_cnet_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][:4]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    assert len(fragments)==58
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=58))
    assert exact.calculate()==read(BASE/'exact-preflight.json');write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_cnet_search*.json')):
        if 'receipt' in p.name:continue
        d=authenticated_json(p);rp=p.with_suffix('.receipt.json')
        for x in d['items']:leads.setdefault(x['full_name'],dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected'))
        queries.append(dict(query=read(rp)['url'],total=d['total_count'],returned=len(d['items']),unreturned_count=max(0,d['total_count']-len(d['items'])),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(rp,'Query identity')))
    assert len(queries)==6 and len(leads)==52
    for repo in [x[1] for x in SPECS.values()]:
        if repo in leads:leads[repo]['status']='selected_primary_anchors_only'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',cutoff_utc='2026-10-07T15:59:59Z',queries=queries,unique_leads=52,leads=list(leads.values()),additional_named_candidates=[x[1] for x in SPECS.values()],saturation_claim=False,absence_claim=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Original identities and exact anchors') for n in ['authenticated-originals.json','inspected-extracts.json','search-screening.json']],groups=5,anchors=58,scholarly_originals=1,native_execution=False))
    checks=['Path3one-hop-max six score orderings and20weighted assignments give pi(5/12,1/3,5/12)in each arm.',
      'HT target and exact mean1;variance2242/75matches independent joint-probability expansion.',
      'Zero-extended Hajek mean1/2for constant true effect1;positive node probabilities do not guarantee realized nonempty arms.',
      'Two conditional probabilities1/4and1/2have inverse marginal8/3versus mean inverse3.',
      'Atp1/5two-cluster exposure is1/25treated,16/25control,not1/4.',
      'Selected weight-restoration expression changes authored exposure9/10to1/2;native test remains open.',
      'Independent versus identical Bernoulli draws have mean variance1/8versus1/4.',
      'Sparse IDs0and2are two units;zero-filled ID-bound average2/3is not population mean1.',
      'Hypothetical USD30000 denominators reproduce30,50,75.']
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored enumeration and arithmetic'),ref(BASE/'exact-results.json','Exact replay')],checks=checks,native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='C++ assignment,exposure,ratio failures,graph identity and distributed-state contracts',selected=list(SPECS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    rgcrtree=authenticated_json(RAW/'exec25_cnet_rgcr_tree.json');license_names=[x['path'] for x in rgcrtree['tree'] if any(t in x['path'].lower() for t in ['license','licence','copying','copyright'])];assert license_names==[]
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Selected declarations'),ref(BASE/'authenticated-originals.json','License/configuration originals')],findings=['RGCR complete selected tree has no license-named original;rights not inferred.','RGCR build references user-specificSNAP4.1,C++11,DNDEBUG;selected2023SNAPtree is not that installed artifact.','NetworKit MIT,source metadata11.2.1,C++20,CMake3.14;SNAP andRepastHPC BSD-style;igraphGPL2-or-later.','MPI,Boost,NetCDF,OpenMP and complete distribution artifacts need independent qualification.'],integration_allowed=False))
    tests=['Tiny exact partition and assignment enumeration,marginal/joint exposure and support','HT moments and covariance formula versus enumeration','Ratio exposed-arm counts,empty-denominator refusal and altered sampling laws','Probability approximation,reciprocal error and pair-dependent simulation uncertainty','Graph cache identity,consecutive IDs,connectivity,self-loops and multiplicity','Compaction/restore node maps,weights,directions and attributes','Seed and draw allocation,finite-score ties,zero uniform draws,positive weights','Public input validation with assertions disabled,count bounds and finite positive intervals','Threads/ranks,replicas,migration,projection freshness and deterministic phases','Exact C/C++ABI,memory ownership,custom RNG lifetime and concurrency','Complete artifacts,licenses,attempts,failures,refusals and costs']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,owners=['Scientific author','Graph/adapter owner','Artifact/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded search tails and candidate dispositions')],known_routes=['Inspect bounded discovery tails,missing delegates and direct causal alternatives.','Resolve RGCR rights and exact historical dependency;qualify finite-law native experiments.','Inspect final publisher paper through permitted routes;preserve selected2020authorversion.','Qualify graph roundtrips,RNG ownership,distributed synchronization and complete artifacts.'],unknown_universal_repairs=['Bank graph truth,latent confounding and arbitrary dependent uncertainty have no universal promised repair.'],next_action=NEXT))
    paper=read(BASE/'paper-identity.json');pp=ROOT/paper['local_copy']['path'];assert core.sha(pp)==paper['local_copy']['sha256']
    pr=read(BASE/'paper-review.json');pa=read(BASE/'paper-inspected-extracts.json');assert pa['source']==paper['local_copy']
    anchors=[dict(anchor='Physical PDF pages '+','.join(map(str,x['pages'])),physical_pages=x['pages'],text_extract=ref(BASE/'paper-v1.txt','Authentic PDF text'),excerpt_sha256=hashlib.sha256(x['text'].encode()).hexdigest(),finding=x['claim']) for x in pa['anchors']]
    sources.append(dict(integrated_citation_key='exec25_cnet_paper',kind='paper',title=paper['title'],filename_title=paper['title'],first_author='Ugander',author='Ugander, Johan and Yin, Hao',year=2020,source_identity='https://arxiv.org/pdf/2009.02297v1',version_date=paper['version'],local_path=str(pp.relative_to(ROOT)),sha256=core.sha(pp),local_copy=ref(pp,'Genuine59-pageauthororiginal'),identity_evidence=[ref(RAW/n,'Original identity/acquisition') for n in ['exec25_cnet_rgcr_arxiv_identity.html','exec25_cnet_rgcr_arxiv_identity.receipt.json','exec25_cnet_rgcr_paper_v1.receipt.json']],inspected_anchors=anchors,supported_claims=pr['supported_claims'],limitations=pr['limitations'],evidence=[ref(BASE/'paper-review.json','Bounded primary review'),ref(BASE/'paper-access-omissions.json','Publisher limitation'),ref(BASE/'paper-version-recovery.json','Preserved version-selection failure')]))
    sources.append(dict(integrated_citation_key='exec25_cnet_choice',kind='project_evidence_not_scholarly_paper',title='Authored C++ network design and component qualification comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October2026;cutoff7 October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored exact witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','paper-review.json']],inspected_anchors=[dict(anchor='Assignment,ratio support,graph,random-state,distributed ownership and cost comparisons',inspection='Author inspection')],supported_claims=['64selected originals,58software anchors and genuine2020authorpaper;52bounded search leads.','Finite exact assignment examples,conditional component decisions and native qualification routes.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=7,new_scholarly_pdfs=1,evidence=[ref(BASE/'authenticated-originals.json','64authentic originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['64authenticated originals,58software anchors,fivecollections,onepaper and authored comparison.','Preserve explicit multiplicity and return-code alternatives;bound negative helper findings to inspected branches.','Paper positivity and ratio proof do not establish zero-arm extension;native and theorem claims remain separate.','Keep search tails,native,rights,visual and final gates open;serialize publication after JVM delivery exit.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking argument'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Separate component decisions and explicit direct-use/port/reject criteria.','Notation and authored examples explain exposure,assignment,clocks,randomness and costs.','Genuine2020paper inspected;no2023publisher or native qualification inferred.'],visual_acceptance=False))
    names=['authenticated-originals.json','primary-review.json','mathematical-review.json','comparison-review.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md','anchor-specifications.json','paper-review.json','paper-identity.json']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Reviewed bounded comparison') for n in names]+[ref(Path(__file__),'Review logic')],findings=['64authentic originals,58verified software anchors and a genuine59-pageauthorpaper.','Graph,simulation and causal qualification are explicit distinct contracts.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=64,anchors=58,unique_leads=52,new_records=7,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Selected C++ assignment implementation,primarypaper and graph/simulation components inspected;search and native coverage incomplete.','Claims bind authentic dated bytes and selected2020paper;zero-arm convention has authored exact witness.','Alternatives and public qualification routes retain graph,clock,assignment,rights and native limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='C++ network assignment,ratio support,graph and distributed-state comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('C++ network inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
