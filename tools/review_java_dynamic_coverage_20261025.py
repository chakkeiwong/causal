#!/usr/bin/env python3
"""Authenticate pinned R originals and review bounded dynamic inference comparisons."""
import argparse,hashlib,json
from pathlib import Path
import java_dynamic_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/java-dynamic-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.dynamic_panel_timeseries.Java'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected primary paths and bounded searches; uninspected candidates and complete ecosystem coverage remain open.',
 'No downloaded package or upstream test executed; authored exact witnesses are not native results.',
 'Temporal graph discovery, point forecasts, conditional state uncertainty and interventions have distinct assumptions.',
 'Complete solver/dependency delegates, installed artifact equivalence and distribution rights remain unqualified.',
 'Intervention identification, calendar dependence and bank utility require information or restrictions.',
 'No scholarly theorem imported from source comments; visual, independent, bank and final acceptance remain open.']
NEXT='Inspect remaining JVM dynamic-panel and temporal candidates; qualify naming,calendar,graph endpoints,forecast horizon/variance,VARX widths,initial values,information clocks,diffuse failures and installed artifacts on public known-law fixtures before native admission.'
SPECS=read(BASE/'anchor-specifications.json')

def authenticate():
    rows=[];evidence=[]
    for name in ['source-selection.json','delegate-selection.json','final-selection.json','backcast-selection.json']:
        rows.extend(read(BASE/name));evidence.append(ref(BASE/name,'Pinned selected file identities'))
    assert len(rows)==39
    originals=[]
    for x in rows:
        p=RAW/(x['id']+'.txt');data=p.read_bytes();receipt=p.with_suffix('.receipt.json');r=read(receipt)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['git_blob']
        assert len(data)==x['bytes'] and core.sha(p)==r['sha256'] and r['status']=='saved'
        originals.append(dict(repository_path=x['path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(receipt,'URL,date,hash')))
    for key in SPECS:
        c=read(RAW/f'exec25_jdyn_{key}_commit.json');c=c[0] if isinstance(c,list) else c
        assert c['sha']==SPECS[key][2].split(';')[-1] and c['commit']['committer']['date'][:10]<='2026-10-07'
        tree=read(RAW/f'exec25_jdyn_{key}_tree.json');assert tree['truncated'] is False
        evidence.extend([ref(RAW/f'exec25_jdyn_{key}_{kind}.json','Dated pin and complete selected tree') for kind in ['commit','tree']])
    write(BASE/'authenticated-originals.json',dict(status='pass',count=39,originals=originals,evidence=evidence))

def prepare():
    assert not (BASE/'review.json').exists()
    authenticate();fragments=[];sources=[]
    for key,(title,repo,version,checks) in SPECS.items():
        evidence=[ref(RAW/f'exec25_jdyn_{key}_commit.json','Revision and date')];anchors=[];claims=[]
        for suffix,lo,hi,tokens,finding in checks:
            p=RAW/f'exec25_jdyn_{key}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));s='\n'.join(lines[lo-1:hi]);assert all(t in s for t in tokens),(p.name,lo,hi,[t for t in tokens if t not in s])
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=key,source=binding,first_line=lo,last_line=hi,text=s))
        sources.append(dict(integrated_citation_key='exec25_jdyn_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][-4:]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=len(fragments)))
    write(BASE/'exact-results.json',exact.calculate());queries=[];leads={}
    for p in sorted(RAW.glob('exec25_jdyn_search*.json')):
        if 'receipt' in p.name:continue
        d=read(p);receipt=p.with_suffix('.receipt.json')
        for x in d['items']:leads.setdefault(x['full_name'],dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected'))
        queries.append(dict(query=read(receipt)['url'],total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(receipt,'Query identity')))
    for repo in [x[1] for x in SPECS.values()]:
        if repo in leads:leads[repo]['status']='selected_primary_anchors_only'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),additional_named_candidates=[x[1] for x in SPECS.values()],saturation_claim=False,absence_claim=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Original identities and exact anchors') for n in ['authenticated-originals.json','inspected-extracts.json']],groups=4,anchors=len(fragments),native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Exact rational/indexing witnesses'),ref(BASE/'exact-results.json','Replay')],checks=['Positional temporal rows differ from declared calendar offsets.','Colon generated names do not supply a dot delimiter.','VARX width fixture has7 constructed versus4 forged columns.','AR1 forecast variances1 and5/4 differ; second differences restore22 and28.','Missing-state variances2 and3; regression uncertainty adds1 to1.','Costs30/42/60 retain all denominators.'],native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Temporal graph,point forecast and conditional state distribution versus bank intervention',selected=list(SPECS),decisions=['Conditional Tetrad lag/knowledge reference; selected collapse utility needs naming repair.','Conditional Smile point forecast reference; qualify separate uncertainty and rank delegates.','Defer blanket ScalaTion VARX admission pending width,entry-point and information-clock tests.','Conditional JDemetra+ state and forecast reference; independent causal model required.'],limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Declarations and named holder notice')],findings=['Tetrad root GPL3; Smile component-specific declaration; JDemetra+ EUPL1.2; ScalaTion root and historical notices retained.','Full numerical/native dependency rights and binary equivalence remain unqualified.','No commercial entitlement or blanket port/distribution clearance.'],integration_allowed=False))
    tests=['Calendar and temporal variable identity','Graph endpoints and dependent post-discovery uncertainty','Rank-truncated coefficients versus covariance solver','Horizon variance and differencing reconstruction','VARX widths,unfinished entry points,zeros and information clocks','Missing-state propagation,diffuse failures and conditional regression uncertainty','Frozen artifact and dependency rights','All requests,refusals,accepted outputs and complete costs']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,owners=['Scientific author','Adapter owner','Artifact/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded search and tails')],known_routes=['Complete primary delegates and installed artifact provenance.','Freeze public known-law contracts before native experiments.'],unknown_universal_repairs=['Unknown exclusion and shock stability require information or justified restrictions.','No universal latent-identification or arbitrary-dependence repair is promised.'],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_jdyn_choice',kind='project_evidence_not_scholarly_paper',title='Authored JVM temporal graph,forecast and state comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026;cutoff7 October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored exact witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Calendar,naming,width,forecast uncertainty,state propagation and costs',inspection='Author inspection')],supported_claims=['Exact authored witnesses and conditional candidate decisions','Bounded search and proposed public qualification'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=5,new_scholarly_pdfs=0,evidence=[ref(BASE/'authenticated-originals.json','39 authenticated originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed planned and actual evidence') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['39 authentic originals, four collections and one authored comparison.','Trace actual graph,forecast,variance and refusal paths before claims.','Separate source review from native and scientific qualification.','Serial canonical publication after R dynamic delivery.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking targets and substantive alternatives'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Explained model,exact examples and distinct reuse alternatives.','Source predicates,authored calculations and proposed tests separated.','Open coverage,rights,native and final acceptance retained.'],visual_acceptance=False))
    names=['authenticated-originals.json','primary-review.json','mathematical-review.json','comparison-review.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Reviewed bounded comparison') for n in names]+[ref(BASE/'anchor-specifications.json','Exact source predicates'),ref(Path(__file__),'Review logic')],findings=['39 authentic files and exact anchors retain source/native distinction.','Temporal graph,forecast and state contracts explicit.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=39,anchors=len(fragments),unique_leads=len(leads),new_records=5,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Selected JVM candidates identified; search,delegate and native coverage incomplete.','Claims bind authentic dated bytes and exact anchors; no scholarly theorem imported.','Alternatives and public qualification routes retain numerical,rights and native limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='JVM temporal graph,forecast and state source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('R dynamic inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
