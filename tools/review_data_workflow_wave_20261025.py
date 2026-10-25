#!/usr/bin/env python3
"""Review authentic source evidence; keep ten software outcomes separate."""
import argparse
import hashlib
import json
from pathlib import Path
import data_workflow_wave_reference_20261025 as exact
from data_workflow_wave_anchors_20261025 import ANCHORS, REUSE, NEW_GROUPS, FAMILIES
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/data-workflow-wave-v1'
RAW=ROOT/'docs/literature/raw'
PRIOR=ROOT/'docs/program/execution/2026-10-25/bayesian-state-wave-reader-v1/reader/source-audit.json'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Nine selected repositories and five bounded queries do not establish ecosystem saturation.',
 'Reused sources retain original dates, scope and limitations; not new acquisition.',
 'Development metadata and source pins are not installed supported-release identities.',
 'No downloaded implementation executed; authored examples are not measured package failures or bank losses.',
 'Complete dependencies, native qualification, artifact rights, commercial profiles and full costs remain open.',
 'Package-mentioned scholarly works remain leads without admitted genuine originals.',
 'Q1/Q5, mandatory coverage/depth and fresh visual/independent/final acceptance remain open.',
]
NEXT='Complete search tails and primary delegates; qualify public join,linkage,time,null,cache,RNG,retry,effect,numeric and full-cost fixtures for named artifacts/runners. Unknown assignment or availability truth requires information or justified restrictions.'
DECISIONS={
 'R':['Conditionally adopt data.table with cardinality,type,clock and linkage contracts.','Conditionally adopt targets with explicit cues,seeds,error modes and attempt provenance.','Retain audited DuckDB alternative;port finite oracles/schema checks,not whole engines.'],
 'Python':['Retain audited DuckDB,Polars,Feast,Pandera and Splink roles under original limits.','Compare Dask graphs,Snakemake file workflows and prior Ray with artifact,error and attempt contracts.','Reject arbitrary serialized-object payloads and task-token-only scientific provenance.'],
 'Java':['Compare Beam and prior Spark using named runners,windows,clocks,state stores and sinks.','Retain OpenLineage and historical SAS job-state comparator within prior scope.','Reject perpetual deduplication and transactional effects inferred from API availability.'],
 'Cxx':['Conditionally adopt Arrow representation/asof role with explicit tolerance and two-clock policy.','Conditionally adopt Taskflow local executor with consumed futures/errors and attempt accounting.','Do not infer distributed persistence,causal identification or sink rollback from these components.'],
 'other_relevant':['Conditionally adopt DataFrames.jl with explicit key validation and missing modes.','Qualify Dagger fault recovery;retain documented robustness caveat.','Retain prior Scala Spark/Rust Polars scope;uninspected ecosystems are not absent.'],
}
REUSE['Java']=REUSE['Java']+['exec24_workflow_contracts_sas']
TESTS=[
 'Enumerate join cardinality,missing identities and known uncertain linkage assignments.',
 'Qualify event/availability revisions and forward/backward asof direction.',
 'Bind scientific inputs,models and versions independently of task tokens and filenames.',
 'Separate retry reproducibility from independent Monte Carlo replication.',
 'Inject failures before effects,after commit before acknowledgement,and during output/recovery.',
 'Consume future/error/partial-output evidence and retain all attempt denominators.',
 'Compare exact numeric oracles under dtype,partition and reduction changes.',
 'Bind complete artifacts,rights,resource budgets and full costs before admission.',
]

def prepare():
    assert not (BASE/'review.json').exists()
    pins=read(BASE/'pins.json');selected=read(BASE/'selected-paths.json')+read(BASE/'delegate-paths.json')
    assert len(selected)==83
    originals=[];identities=[]
    for group,pin in pins.items():
        cp=RAW/f'exec25_dww_{group}_commit.json';tp=RAW/f'exec25_dww_{group}_tree.json'
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        commit=read(cp)[0];tree=read(tp)
        assert commit['sha']==pin['sha'] and commit['commit']['committer']['date']==pin['date']<='2026-10-07T15:59:59Z'
        assert tree['sha']==pin['tree_sha'] and not tree['truncated']
        blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities += [ref(cp,'Pinned identity'),ref(tp,'Complete selected tree')]
        for item in [x for x in selected if x['group']==group]:
            p=RAW/(item['id']+'.txt');rp=p.with_suffix('.receipt.json');r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and core.sha(p)==r['sha256']
            assert r['url']=='https://raw.githubusercontent.com/'+pin['repository']+'/'+pin['sha']+'/'+item['upstream_path']
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
            assert blob==blobs[item['upstream_path']]==item['git_blob']
            originals.append(dict(**item,local_copy=ref(p,'Authentic original'),receipt=ref(rp,'Public receipt')))
    write(BASE/'authenticated-originals-v3.json',dict(count=83,groups=9,originals=originals,identities=identities,native_execution=False,predecessor=ref(BASE/'authenticated-originals-v2.json','Earlier identity verification preserved')))
    fragments=[];sources=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[ref(RAW/f'exec25_dww_{group}_commit.json','Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_dww_{group}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,token)
            binding=ref(p,f'Lines{lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=group,source=binding,first_line=lo,last_line=hi,text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_dww_'+group,kind='software',title=group+' pinned observation-data and computation-workflow contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['sha'],version_date=pin['date']+';'+pin['sha'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));write(BASE/'exact-results.json',exact.calculate())
    prior=read(PRIOR);verify_bindings(prior);entries={s['integrated_citation_key']:s for s in prior['sources']};keys=set(sum(REUSE.values(),[]));assert keys<=entries.keys()
    inherited=[entries[k] for k in sorted(keys)];sources+=inherited
    write(BASE/'reused-evidence.json',dict(records=len(inherited),by_language=REUSE,source_audit=ref(PRIOR,'Unchanged predecessor identities'),limitations='Retain original scope,date and bindings;no new acquisition or native qualification.'))
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_dww_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        receipt=read(p.with_suffix('.receipt.json'));assert receipt['status']=='saved' and receipt['sha256']==core.sha(p);d=read(p)
        queries.append(dict(source=ref(p,'Discovery only;not historical search reconstruction'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==5
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals-v3.json','Authentic source declarations')],findings=['data.table MPL2 with file alternative;Dask BSD3;Beam/Arrow Apache2;targets,Snakemake,Taskflow,DataFrames,Dagger MIT-style.','Installed artifacts,toolchains,plugins,connectors and transitive rights remain unqualified.']))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Scientific,data,integration and operations owners to be appointed',tests=TESTS,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,known_routes=TESTS,uninspected=['Residual query tails and other languages.','Full distributed schedulers,runners,state stores,connectors,serialization and numerical delegates.','Installed artifacts,dependency rights,native experiments and full costs.','Current commercial profiles/prices;MATLAB/HUGIN original-source limits remain local.','Package-mentioned scholarly originals not admitted.'],unknown_universal_repairs=['Unknown assignment and inclusion truth cannot be inferred from data-engine success.','Missing historical availability and uncalibrated linkage probabilities require information or restrictions.','Universal dependent-data uncertainty has no promised scheduler repair.'],next_action=NEXT))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Finite project constructions'),ref(BASE/'exact-results.json','Replayed arithmetic'),ref(BASE/'inspected-extracts.json','Primary anchors')],findings=['Two-by-two join doubles300USD to600USD while equaling row limit4.','Decision5admits20,not event-only200 available8.','Linkage mean280/variance129600;10000hypothetical accounts understate expected loss1.8millionUSD.','Four attempts cost8for2completions;success-only accounting reports2.','Repeated100draws are not200independent draws;binary64 grouping differs1versus0.','Ambiguous100USD effect retry can produce200USD without qualified sink idempotency.'],native_execution=False))
    for family in FAMILIES:
        for language in REUSE:
            folder=BASE/family/language;folder.mkdir(parents=True)
            write(folder/'comparison-review.json',dict(operation='SW.CELL.'+family+'.'+language,status='inconclusive',family=family,selected_new_groups=NEW_GROUPS[language],reused_records=REUSE[language],decisions=DECISIONS[language],limitations=LIMITS,next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals-v3.json','inspected-extracts.json','reused-evidence.json','search-screening.json','dependency-license-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_dww_choice',kind='project_evidence_not_scholarly_paper',title='Authored observation-data and computation-workflow comparison and public qualification',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact authored witnesses'),evidence=evidence+[ref(Path(exact.__file__),'Authored reference')],inspected_anchors=[dict(anchor='Identity,cardinality,clocks,linkage,cache,RNG,retry,effects,numerics and costs',inspection='Author inspection')],supported_claims=['83 authentic originals and retained prior records ground bounded language decisions.','Finite public fixtures motivate qualification before bank experiments.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=10,reused_records=len(inherited),new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Scientific identity/information separate from data movement and job completion.','Adoption,adapter,port and rejection choices are candidate-specific.','Ten cells remain independent;publish one preserving wave after consumed Bayesian delivery.','No claim exceeds inspected branches;delegate and coverage limits retained.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected scholarly comparison'),ref(BASE/'sponsor-addition.md','Sponsor argument')],findings=['Explained notation,assumptions,finite banking examples and substantive alternatives.','Development pins,license scopes,static/native and event/availability distinctions retained.','Proposal CLI/MCP contract does not imply implemented integration.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer'),ref(ROOT/'tools/data_workflow_wave_anchors_20261025.py','Inspected spans')]
    verify_bindings(dict(evidence=evidence))
    write(BASE/'review.json',dict(status='pass_for_bounded_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=83,scholarly_originals=0,language_cells=[f+'.'+l for f in FAMILIES for l in REUSE],limitations=LIMITS,native_execution=False))
    print(json.dumps(dict(review='pass',outcomes='ten_inconclusive',originals=83,anchors=len(fragments),new_records=10,reused_records=len(inherited))))

def receipt(family,language):
    verify_bindings(read(BASE/'review.json'));assert exact.calculate()==read(BASE/'exact-results.json')
    op='SW.CELL.'+family+'.'+language;state=core.read(ROOT,core.STATE);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);folder=BASE/family/language;output=ROOT/node['outputs'][0]
    assert not output.exists();write(output,read(folder/'comparison-review.json'))
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]+[ref(folder/'comparison-review.json','Separate language/family decision')]
    findings=['Selected sources inspected;ecosystem,artifact and native coverage remain incomplete.','Pinned originals and unchanged prior records ground bounded claims;authored exact examples reproduce.','Conditional adoption,adapter,port/reject choices retain scientific,rights and cost qualification.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope=language+' '+family+' source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(folder/'operation-receipt.json',result);print(op+' receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);p.add_argument('family',nargs='?',choices=FAMILIES);p.add_argument('language',nargs='?',choices=list(REUSE));a=p.parse_args()
    if a.command=='prepare':prepare()
    else:assert a.family and a.language;receipt(a.family,a.language)
