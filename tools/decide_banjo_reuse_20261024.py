#!/usr/bin/env python3
"""Authenticate selected Banjo derivative sources; record reference-only choice."""
import argparse,hashlib,json
from pathlib import Path
import banjo_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/banjo-reuse-v1';RAW=ROOT/'docs/literature/raw'
PIN='0c42b02ac2b452fc782ea8cff4c92f1cd11f8e6b';OP='SW.DECISION.seed_079';read=lambda p:json.loads(p.read_text())
LIMITS=['Selected 2026 application derivative only;official release and complete derivative changes unresolved.',
 'No downloaded code or Java compilation executed;exact witnesses and conditional deductions are authored.',
 'Pseudotime,predictive score,mandatory edges and retained networks do not establish causal identification or calibrated uncertainty.',
 'Complete rights,artifact dependencies,native behavior,maintenance and costs remain unqualified.',
 'Reference only;no native,causal,independent,visual,bank or final acceptance.']
SPECS={
 'v12_exec13_java_banjo_readme':[(1,42,'Pseudotime,gold-standard subset selection and reported settings'),(896,910,'Derivative notice and redistribution uncertainty')],
 'v12_exec13_java_banjo_settings':[(994,1055,'Base seed plus thread index;time-based default possible'),(3233,3251,'Random-sequence access')],
 'v12_exec13_java_banjo_greedy':[(64,154,'Time,iteration and restart termination'),(520,598,'Retained graph filtering and replacement')],
 'exec15_javatemporal_banjo_2':[(1,100,'Application settings and time budget')],
 'exec15_javatemporal_banjo_3':[(121,138,'Log-gamma provider'),(563,750,'Compact score counts,domains and gamma terms'),(1011,1053,'Positive equivalent sample size validation')],
 'exec15_javatemporal_banjo_4':[(365,429,'Preparation then effective count and cardinalities'),(470,515,'Combined raw observations and window count'),(521,628,'Combined discretization and within-file lag windows'),(656,693,'Current-slice cardinality scan')],
 'exec15_javatemporal_banjo_5':[(265,332,'Mandatory self-lag and contemporaneous-cycle validation')],
 'exec24_banjo_source_0':[(1,33,'Java8 compilation target;not executed')],
 'exec24_banjo_source_1':[(1,16,'Rights-holder and conditional license notice'),(182,214,'Fit to all loaded raw points'),(237,307,'Discretizer dispatch and absent-value refusal')],
 'exec24_banjo_source_2':[(42,120,'Distinct-value shortcut and interval boundaries')],
 'exec24_banjo_source_3':[(275,304,'Termination settings'),(468,476,'Non-equivalent versus skipped equivalence branch')],
 'exec24_banjo_source_4':[(48,74,'Greedy acceptance of equal scores')],
 'exec24_banjo_source_5':[(48,108,'Check then apply;positive lags exempt from cycle test')],
 'exec24_banjo_source_6':[(48,92,'Apply then check;undo rejected contemporaneous cycle')],
 'exec24_banjo_source_7':[(90,179,'Local proposals,parent bounds and lag-zero reversals')],
 'exec24_banjo_source_8':[(124,193,'Random move and constrained lag-zero reversal'),(307,321,'Parent-count rejection')],
 'exec24_banjo_source_9':[(59,68,'Declared Banjo2.2.0 April2008 identity')],
 'exec24_banjo_delegate_0':[(103,120,'Zero-initialized cardinality array')],
 'exec24_banjo_delegate_1':[(45,80,'Observed extrema and bin count')],
 'exec24_banjo_delegate_2':[(55,80,'Skipped equivalence returns false')],
 'exec24_banjo_delegate_3':[(264,334,'Score,parent-count,identity and asymmetric final tie branch')]
}

def prepare():
    assert not (BASE/'review.json').exists()
    tree=read(RAW/'v12_exec13_java_banjo_tree.json');assert tree['sha']==PIN and not tree['truncated']
    lookup={x['path']:x for x in tree['tree']};cutoff=read(RAW/'v12_exec13_java_banjo_commit.json')[0]
    assert cutoff['sha']==PIN and cutoff['commit']['committer']['date']=='2026-08-13T14:07:19Z'
    records=[]
    for key,specs in SPECS.items():
        p=RAW/(key+'.txt');data=p.read_bytes();r=read(RAW/(key+'.receipt.json'));path=r['url'].split('/'+PIN+'/')[1]
        digest=hashlib.sha256(data).hexdigest();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
        assert digest==r['sha256'] and lookup[path]['sha']==blob
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,f in specs:
            assert 1<=lo<=hi<=len(lines),(key,hi,len(lines))
            anchors.append(dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest()))
        records.append(dict(source_identity=r['url'],repository_path=path,git_blob=blob,version_date='13August2026 derivative;'+PIN,
            local_copy=ref(p,'Authenticated derivative original'),acquisition=ref(RAW/(key+'.receipt.json'),'Acquisition receipt'),
            inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
    assert len(records)==21
    access=read(RAW/'exec24_banjo_official_identity.receipt.json');assert access['status']=='failed' and 'allowlist' in access['error']
    write(BASE/'official-access-limit.json',dict(status='local_collector_policy_limit_not_server_unavailability',evidence=[ref(RAW/'exec24_banjo_official_identity.receipt.json','Exact failure')],official_identity=False,policy_changed=False))
    write(BASE/'identity-review.json',dict(status='pass_for_selected_derivative_sources',records=records,commit=PIN,date='2026-08-13',declared_version='Banjo2.2.0;15April2008',
        evidence=[ref(RAW/'v12_exec13_java_banjo_tree.json','Complete derivative tree'),ref(RAW/'v12_exec13_java_banjo_commit.json','Cutoff identity'),ref(BASE/'official-access-limit.json','Official identity limit')],official_current_identity=False,native_execution=False))
    obs=(RAW/'exec15_javatemporal_banjo_4.txt').read_text();comp=(RAW/'exec24_banjo_delegate_3.txt').read_text()
    cardinal=obs.split('public void computeMaxValueCounts()',1)[1].split('public String toString()',1)[0]
    assert '0*offsetLags' in cardinal and 'lagIndex' not in cardinal
    tie=comp.split('public int compareTo(',1)[1].split('// Output in string form',1)[0]
    assert 'hasIdenticalEntries' in tie and tie.rsplit('return ',1)[1].startswith('1;')
    assert 'if (newScore >= currentScore)' in (RAW/'exec24_banjo_source_4.txt').read_text()
    write(BASE/'control-flow-review.json',dict(status='pass_for_conditional_static_findings',findings=['Combined fit but within-file windows.','Current-only category scan may omit an initial lag-only state.','Selected equal-score/equal-parent-count distinct-graph comparator returns1bothways.','Greedy equal-score moves and retained subset are not calibrated posterior draws.'],evidence=[ref(RAW/(k+'.txt'),'Inspected source') for k in ['exec15_javatemporal_banjo_4','exec24_banjo_delegate_3','exec24_banjo_source_4','exec24_banjo_source_3','exec24_banjo_delegate_2']]+[ref(Path(__file__),'Bounded assertions')],native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',findings=['Bayes factor135/32changes to385875/8192after duplicate counts.','Five valid windows versus six concatenated;one false cross-file transition.','Training value1changes interval label after inclusion of held-out100.','Conditional cardinality and comparison witnesses reproduce;no native failure claim.','Identical observational laws givecausal0or1andnet-10000or40000USD.','9000USDover300/225/150gives30/40/60USD.'],evidence=[ref(Path(exact.__file__),'Independent authored oracle'),ref(BASE/'exact-results.json','Exact and log-gamma checks'),ref(BASE/'development.tex','Explained derivations')],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='selected_notice_not_clearance',declared_version='2.2.0;15April2008 inside2026derivative',compile_target='Java8;not executed',license='All rights reserved;noncommercial use may be licensed;commercial contact required',evidence=[ref(RAW/(k+'.txt'),'Primary declaration') for k in ['exec24_banjo_source_1','exec24_banjo_source_0','exec24_banjo_source_9','v12_exec13_java_banjo_readme']],unresolved=['Authentic official grant and distribution','Complete derivative permissions and dependencies','Native environment,support and maintenance'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',inputs=['Physical/pseudo/event clock,entity/file boundaries and missing intervals','Train/evaluation split,frozen categories and out-of-range rule','Lag-inclusive domains,support,weights and dependence assumptions','Positive prior,constraints,parent budget,seed,threads and stop rules','Rights-cleared binary and worker identity'],outputs=['Typed lagged edges and supplied-versus-learned provenance','Score,rank,retained subset and uncertainty separately','Termination,rollback,all failures and full costs','Causal identification result or explicit refusal'],refusals=['No authentic rights/artifact','Unsupported category or irregular clock','Causal target without identifying information','Tied-ordering inconsistency','Evaluation leakage or unavailable probability interpretation'],integration_allowed=False))
    next_action='Retain Banjo derivative reference;obtain permitted authentic official identity and rights,review full derivative/dependencies and preregister native file-window,train-only-discretization,lag-only-category,score-duplication,constraint/rollback,tie-order,seed/budget and retained-graph fixtures. Do not repeat selected source review;no native integration until qualified.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,known_routes=['Authentic official source and granted terms','Public generated domain/clock/graph/score fixtures','Rights-cleared isolated worker and all-cost trials'],remaining=['Official host outside collector scope','Full derivative and dependency/rights inventory','Remaining preprocessing,score-cache and export paths','Native runtime,maintenance and prices'],unavailable_scholarly_candidates=['No new Banjo methodological paper cited without a genuine original PDF'],unknown_without_information=['Actual bank assignment and hidden causes','Physical meaning of inferred pseudotime','Unique causal graph or calibrated uncertainty from top-k scores']))
    choice=dict(candidate='Banjo',canonical_candidate='daniel-315/slingshot-modified-banjo application derivative;official release unresolved',decision='reference',selected_revision=PIN,selected_version='Declared2.2.0;2026derivative',alias_boundary='Selected discrete temporal-network source;not official distribution or unrestricted causal identification',reason='Concrete temporal reference and conversion witnesses;rights,native behavior and causal meaning require qualification.',alternatives=[dict(route='adopt',decision='defer',reason='Authentic license and full artifact unqualified'),dict(route='integrate',decision='conditional',reason='Isolated Java worker after rights and native public fixtures'),dict(route='port',decision='defer',reason='No measured benefit against independent correctness and maintenance burden'),dict(route='reference',decision='retain',reason='Authenticated source and exact scientific/interface witnesses'),dict(route='reject',decision='restricted',reason='Reject causal arrows,posterior frequencies and silent conversion loss without support')],owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Target,clock,identification and support'),('Adapter','Domains,windows,graph order and refusal'),('Rights/platform','Grant,artifact,dependencies and maintenance'),('Evaluation','Frozen public oracles,all requests and costs')]],costs=dict(prices='Unmeasured;9000USD authored illustration',categories=['source/rights','environment','conversion','all searches','failures','review','maintenance']),maintenance='Official maintenance and derivative support not verified',revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    source=dict(integrated_citation_key='exec24_banjo_source',kind='software_primary_sources',title='Pinned Banjo derivative lag,discretization,score,search and graph contracts',author='Duke University Banjo authors and application derivative contributors',year=2026,source_identity='https://github.com/daniel-315/slingshot-modified-banjo/tree/'+PIN,version_date='13August2026 derivative;declaredBanjo2.2.0;'+PIN,local_copy=ref(RAW/'exec15_javatemporal_banjo_3.txt','Selected evaluator'),records=records,identity_evidence=[ref(BASE/'identity-review.json','Full-byte/tree identity')],inspected_anchors=[r['local_copy'] for r in records],supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
    authored=dict(integrated_citation_key='exec24_banjo_choice',kind='project_evidence_not_scholarly_paper',title='Authored Banjo clock,score,domain,graph-order,identification and cost witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),inspected_anchors=[ref(BASE/n,'Bounded choice') for n in ['choice.json','conversion-contract.json','control-flow-review.json','omissions-register.json']],supported_claims=['Exact score,clock,category and graph-order witnesses','Observational equality with different intervention effects','Reference alternatives,owners,costs and unresolved questions'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,authored],new_records=2,new_scholarly_pdfs=0,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_reference_choice',evidence=[ref(BASE/n,'Plan and evidence') for n in ['plan.md','identity-review.json','choice.json','mathematical-review.json']],findings=['Derivative identity and conditional rights do not become official/native approval.','Inspect concrete delegates for domain and graph-set claims.','Require exact scientific witnesses and conditional native fixtures;preserve all prior text and evidence.','Official access does not block independent source and proposal work.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',evidence=[ref(BASE/'development.tex','Connected technical argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],findings=['Clocks,counts,score notation,alternatives and banking consequences explained.','Static conditions separated from observed native failures.','No unavailable scholarly original replaced by an authored summary.'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed evidence') for n in ['identity-review.json','source-audit.json','control-flow-review.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','choice.json','exact-results.json','mathematical-review.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],findings=['Twenty-one originals authenticate to derivative tree.','Independent exact witnesses and numerical cross-checks reproduce.','Reference decision grants no rights or native/causal capability.'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(authenticated=21,decision='reference',new_records=2,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed Banjo derivative proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value);evidence=[ref(BASE/n,'Reviewed choice') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Pinned derivative identity,alias,conditional rights and maintenance limits explicit.','Target,conversion,alternatives,owners,costs and revisit conditions reviewed.','Reference only;no native,causal,official-release or rights qualification.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Banjo reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
