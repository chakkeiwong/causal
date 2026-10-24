#!/usr/bin/env python3
"""Authenticate selected JVM originals and review bounded proposal findings."""
import argparse,hashlib,json
from pathlib import Path
import java_network_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as write_new,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/java-network-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.networks_interference.Java'
read=lambda p:json.loads(p.read_text());SPECS=read(BASE/'anchor-specifications.json')
def write(path,value):
    if path.exists():
        assert read(path)==value, 'Preserve differing evidence: '+str(path)
    else:write_new(path,value)
LIMITS=['Eight bounded repository searches and selected anchors; no saturation or absence claim.',
 'No acquired source, native JVM artifact, upstream test or simulator executed.',
 'Authored arithmetic is not observed native behavior or a validated bank mechanism.',
 'Complete installed artifacts, dependency rights and causal estimator qualification remain open.',
 'Unknown bank graph and assignment truth, latent confounding and unrestricted dependence require information or justified restrictions.',
 'No theorem imported from source comments; fresh visual, independent and final acceptance remain open.']
NEXT='Complete bounded JVM discovery tails and missing primary delegates; freeze known-law public graph, assignment, exposure, update-clock, random-state and failure contracts before artifact-specific native experiments.'
DECISIONS=['JGraphT: conditional integration for explicit graph operators; qualify direction,multiplicity,hop/weight distinctions,live views and artifact rights.',
 'GraphStream: conditional event-ingestion component; bind strict/auto-create modes,edge receipts,graph snapshots and business/availability clocks.',
 'MASON: conditional public-simulation reference; qualify shared state,scheduling,effective seeds,checkpoint failure paths and headless distribution.',
 'Repast: conditional alternative public-simulation environment; qualify priority mapping,named random states,reset paths and plugin rights.',
 'Port only after executable semantic contracts and a concrete target-runtime benefit; no component alone identifies borrower interference.']

def authenticated_json(p):
    r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256']
    return read(p)

def prepare():
    assert not (BASE/'review.json').exists()
    rows=read(BASE/'source-selection.json')+read(BASE/'delegate-selection.json');assert len(rows)==50
    leadrows=read(BASE/'lead-selection.json');assert len(leadrows)==2
    originals=[];identity=[];trees={}
    for x in read(BASE/'pins.json')+read(BASE/'lead-pins.json'):
        prefix='exec25_jnet_'+('lead_' if x['key'] in ['gray','solar'] else '')+x['key']
        cp=RAW/(prefix+'_commit.json');tp=RAW/(prefix+'_tree.json')
        c=authenticated_json(cp);c=c[0] if isinstance(c,list) else c;t=authenticated_json(tp)
        assert c['sha']==x['commit'] and c['commit']['committer']['date']==x['date']
        assert x['date']<='2026-10-07T15:59:59Z' and not t['truncated'] and t['sha']==x['commit']
        trees[x['key']]={y['path']:y for y in t['tree'] if y['type']=='blob'}
        identity.extend([ref(cp,'Pinned revision and date'),ref(tp,'Complete selected tree')])
    for x in rows+leadrows:
        p=RAW/(x['id']+'.txt');data=p.read_bytes();rp=p.with_suffix('.receipt.json');r=read(rp)
        assert len(data)==x['bytes'] and r['status']=='saved' and core.sha(p)==r['sha256']
        assert x['commit'] in r['url'] and r['url'].endswith('/'+x['path'])
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['git_blob']
        assert trees[x['group']][x['path']]['sha']==x['git_blob']
        originals.append(dict(repository_path=x['path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'URL,date,hash')))
    write(BASE/'authenticated-originals.json',dict(status='pass',count=52,technical_license_configuration=50,candidate_screening=2,originals=originals,evidence=identity))
    fragments=[];sources=[]
    for key,(title,repo,version,checks) in SPECS.items():
        evidence=[ref(RAW/f'exec25_jnet_{key}_commit.json','Revision and date')];anchors=[];claims=[]
        for suffix,lo,hi,tokens,finding in checks:
            p=RAW/f'exec25_jnet_{key}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));s='\n'.join(lines[lo-1:hi]);assert all(t in s for t in tokens),(p,lo,hi)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=key,source=binding,first_line=lo,last_line=hi,text=s))
        sources.append(dict(integrated_citation_key='exec25_jnet_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][:4]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    assert len(fragments)==41
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=41))
    assert exact.calculate()==read(BASE/'exact-preflight.json');write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_jnet_search*.json')):
        if 'receipt' in p.name:continue
        d=authenticated_json(p);rp=p.with_suffix('.receipt.json')
        for x in d['items']:leads.setdefault(x['full_name'],dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected'))
        queries.append(dict(query=read(rp)['url'],total=d['total_count'],returned=len(d['items']),unreturned_count=max(0,d['total_count']-len(d['items'])),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(rp,'Query identity')))
    assert len(queries)==8 and len(leads)==71
    gray=RAW/'exec25_jnet_lead_gray_readme_0.txt';solar=RAW/'exec25_jnet_lead_solar_readme_0.txt'
    for token in ['Metrics Collector','co-locating','SLA violation','states of servers and workloads']:assert token in gray.read_text()
    assert solar.stat().st_size==0
    dispositions=[dict(repository='tjulym/gray',status='screened_out_for_selected_borrower_causal_estimator',finding='README concerns server-workload resource interference,model training and SLA scheduling;no general absence claim.',original=ref(gray,'Whole original README inspected'),inspected_anchors=[dict(line_spans=[[1,len(gray.read_text().splitlines())]],finding='Server metrics,workloads and scheduler')]),dict(repository='cvhu/ee380l-ghosh-project',status='unresolved_without_technical_inspection',finding='Empty authentic root README cannot support an absence claim.',original=ref(solar,'Authenticated zero-byte README'),inspected_anchors=[dict(byte_span=[0,0],finding='Zero-byte README only')])]
    for x in dispositions:
        if x['repository'] in leads:leads[x['repository']]['status']=x['status']
    for repo in [x[1] for x in SPECS.values()]:
        if repo in leads:leads[repo]['status']='selected_primary_anchors_only'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',cutoff_utc='2026-10-07T15:59:59Z',queries=queries,unique_leads=71,leads=list(leads.values()),candidate_dispositions=dispositions,additional_named_candidates=[x[1] for x in SPECS.values()],saturation_claim=False,absence_claim=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Original identities and exact anchors') for n in ['authenticated-originals.json','inspected-extracts.json','search-screening.json']],groups=4,anchors=41,candidate_screening_originals=2,native_execution=False))
    checks=['Directed incoming,incident-list and unique-neighbor means are1,2/3,1/2.',
      'Authored BFS and weighted shortest-path enumeration distinguish1hop,direct weight10,minimum weight2;induced graph removes two-hop background path.',
      'Two sequential update orders give network means0and1;equal-order mixture mean1/2,variance1/4;simultaneous mean1/2,variance0.',
      'Narrowing7and7+2^32 gives the same effective signed32bit seed.',
      'Independent versus single-cluster Bernoulli assignments have different support;atp1/5mixed independent assignment probability4/25.',
      'Hypothetical USD30000 denominators reproduce30,50,75.']
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored enumeration and arithmetic'),ref(BASE/'exact-results.json','Exact replay')],checks=checks,native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='JVM graph,ingestion,simulation,assignment and clock contracts',selected=list(SPECS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Selected source declarations'),ref(BASE/'authenticated-originals.json','License and configuration originals')],findings=['JGraphT dual LGPL2.1-or-later/EPL2.0;selected1.6.0-SNAPSHOT requiresJava21.','GraphStream dual CeCILL-C/LGPL3-or-later;selected2.1.0-SNAPSHOT.','MASON principal AFL3 with named component exceptions,including RNG BSD.','Repast BSD-style core conditions plus separately licensed dependencies;core manifest2.12.0.','No installed distribution,complete dependency clearance or native artifact qualification.'],integration_allowed=False))
    tests=['Frozen node identity,direction,multiplicity,self-edges,weights and exposure normalization','Hop distance,hop-path weight,minimum-weight path and unreachable outcomes','Induced versus background paths,live-view mutation and deep scenario copies','Ingestion strictness,automatic nodes,duplicates,null returns and immutable snapshots','Business,event,ingestion and availability clocks;late-arriving corrections','Simultaneous read-old/write-new versus sequential updates and priority mapping','Effective seeds,named streams,draw allocation,thread model and independent replicates','Restart versus checkpoint continuation,restore hooks and typed failure','Exact assignment spaces,joint exposure probabilities and zero-support refusals','Known-law public mechanism with frozen oracles before native comparison','Complete selected artifacts,distribution rights,requests,failures and cost denominators']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,owners=['Scientific author','Graph/adapter owner','Artifact/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded search tails and candidate dispositions')],known_routes=['Inspect search tails,solar technical sources and additional network-causal candidates.','Trace missing graph/scheduling delegates and qualify frozen known-law public experiments.','Inspect complete intended artifacts and dependency rights before deployment.'],unknown_universal_repairs=['Bank graph truth,latent confounding and arbitrary dependent uncertainty have no universal promised repair.'],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_jnet_choice',kind='project_evidence_not_scholarly_paper',title='Authored JVM network component comparison and public qualification design',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October2026;cutoff7 October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored exact witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Graph,clock,assignment,random-state and economic comparisons',inspection='Author inspection')],supported_claims=['50selected technical/license/configuration originals plus2candidate-screening originals;41technical anchors;71bounded search leads.','Exact authored graph,scheduling,seed,assignment and cost arithmetic;conditional integration decisions.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=5,new_scholarly_pdfs=0,evidence=[ref(BASE/'authenticated-originals.json','52authentic originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['52authenticated originals,41technical anchors,fourcollections and authored comparison.','Preserve positive alternatives,in/out accessors,multigraph support and explicit seeds;avoid blanket absence claims.','Underlying graph representations and simulation are distinct from causal identification.','Keep search tails,native,rights,visual and final gates open;serialize publication after Python delivery exit.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking argument'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Separate component decisions and explicit direct-use/port/reject criteria.','Notation and authored examples explain exposure,assignment,clocks,randomness and costs.','No new scholarly claim without original paper;no native qualification inferred.'],visual_acceptance=False))
    names=['authenticated-originals.json','primary-review.json','mathematical-review.json','comparison-review.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md','anchor-specifications.json']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Reviewed bounded comparison') for n in names]+[ref(Path(__file__),'Review logic')],findings=['52authentic originals,41verified technical anchors and2candidate-screening originals.','Graph,simulation and causal qualification are explicit distinct contracts.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=52,anchors=41,unique_leads=71,new_records=5,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Selected JVM graph and simulation components inspected;network-causal search and native coverage incomplete.','Claims bind authentic dated bytes and anchors;no scholarly theorem imported.','Alternatives and public qualification routes retain graph,clock,assignment,rights and native limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='JVM network graph,simulation,assignment and clock source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('JVM network inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
