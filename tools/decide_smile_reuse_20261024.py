#!/usr/bin/env python3
"""Separate SMILE engine and GeNIe ecosystem reference choices; no native run."""
import argparse,hashlib,json
from pathlib import Path
from html.parser import HTMLParser
import smile_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/smile-reuse-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/opengm-reuse-reader-v1/reader/source-audit.json'
read=lambda p:json.loads(p.read_text())
OPS={'engine':'SW.DECISION.seed_084','offering':'SW.DECISION.seed_094'}
KEYS=['exec13_smile_intro','exec13_smile_license','exec13_smile_pattern','exec13_smile_pc','exec13_genie_readme','exec13_genie_pattern','exec13_genie_pc','exec13_ct_smile_tutorial','exec13_ct_genie_learning','exec16_cp_bayesfusion']
LIMITS=['Official manual version declarations are not immutable cutoff-byte or current-release evidence.',
 'No licensed binary, native wrapper, GUI, CLI or MCP service executed; no agreement accepted.',
 'Public authored examples are not vendor failures or observed bank results.',
 'Server/API profiles, wrapper parity, deployment rights, actual prices and maintenance remain unresolved.',
 'No unrestricted causal, independent, bank, visual or final acceptance.']

class Text(HTMLParser):
    def __init__(self):super().__init__();self.out=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ['script','style']:self.skip+=1
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip-=1
    def handle_data(self,d):
        if not self.skip and d.strip():self.out.append(d.strip())

def prepare():
    assert not (BASE/'review.json').exists()
    prior=read(PRIOR);selected=[s for s in prior['sources'] if s['integrated_citation_key'] in KEYS];assert len(selected)==len(KEYS)
    records=[]
    for s in selected:
        verify_bindings(s)
        originals=s.get('records') or [s]
        for i,original in enumerate(originals):
            p=ROOT/original['local_copy']['path'];data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==original['local_copy']['sha256']
            parser=Text();parser.feed(data.decode('utf-8-sig'));txt='\n'.join(parser.out)+'\n'
            out=BASE/(s['integrated_citation_key']+'-'+str(i)+'.txt');out.write_text(txt)
            records.append(dict(citation_key=s['integrated_citation_key'],source_identity=original.get('source_identity',s.get('source_identity')),version_date=original.get('version_date',s.get('version_date')),local_copy=original['local_copy'],text_copy=ref(out,'Fresh inert primary extraction'),inspected_anchors=original.get('inspected_anchors',s.get('inspected_anchors',[])),supported_claims=original.get('supported_claims',s.get('supported_claims',[])),cutoff_limit='Mutable later acquisition; declared manual family is not exact cutoff byte',executed=False))
    write(BASE/'inherited-review-bindings.json',dict(prior_audit=ref(PRIOR,'Preserved predecessor audit'),sources=selected,records=records,cutoff='2026-10-07',native_execution=False))
    def text(k):return ' '.join((BASE/(k+'-0.txt')).read_text().split())
    assert '2.2.4.R1' in text('exec13_smile_intro') and '4/27/2024' in text('exec13_smile_intro')
    assert '5.0.R2' in text('exec13_genie_readme')
    assert 'source code of SMILE is proprietary' in text('exec13_smile_intro')
    assert 'Server license' in text('exec13_smile_license') and 'end-user program license' in text('exec13_smile_license')
    assert 'uniform probability distributions' in text('exec13_smile_pc') and 'DSL_INTERRUPTED' in text('exec13_smile_pc')
    assert 'randomly' in text('exec13_genie_pattern') and 'uniform distributions' in text('exec13_genie_pattern')
    assert 'do not allow for learning the structure of dynamic models' in text('exec13_ct_genie_learning')
    assert 'Existing evidence in the network is ignored' in text('exec13_ct_genie_learning')
    assert 'sliceIdx * outcomeCount + i' in text('exec13_ct_smile_tutorial')
    write(BASE/'identity-review.json',dict(status='pass_for_retained_official_documents',evidence=[ref(BASE/'inherited-review-bindings.json','Exact prior audit and original bytes')],canonical_vendor='BayesFusion, LLC',engine='SMILE compiled proprietary C++ library',offering='GeNIe GUI with SMILE engine/API',versions=['SMILE manual 2.2.4.R1 declared 27 April 2024','GeNIe manual 5.0.R2 declared 23 November 2024'],two_decisions_not_two_engines=True,cutoff_limit=LIMITS[0]))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Independent exact examples'),ref(BASE/'exact-results.json','Rational calculations'),ref(BASE/'development.tex','Connected derivation')],findings=['Two causal models produce exactly the same positive observed table but effects 3/5 and zero; not claimed exhaustive identified set.','Illustrative incremental net values 80000 and minus40000 USD.','Uniform initialization is not estimated response.','Slice-major versus outcome-major mapping changes a second-slice hypothetical value by40000 USD.','Predecision perfect information raises expected utility50to100USD; later information cannot be used earlier.','24000USD divided by800/600/400 gives30/40/60USD.'],native_execution=False))
    matrix=[
      ('business_to_model','Documented GUI decision framing and supplied-model utility','Information clock, target, assumption provenance, competing causal diagrams and review'),
      ('discovery','PC pattern and background knowledge; GUI DAG conversion','Preserve unresolved endpoints and graph assumptions; qualify native recovery and no orientation invention'),
      ('identification','Selected sources execute/convert supplied networks','Demonstrate target-specific identification or identified sets; do not infer universal ID support from API breadth'),
      ('estimation','Structure-only conversion gives uniform tables','Explicit fitted/elicited/default table status and data provenance'),
      ('longitudinal','Fixed-structure DBN learning and temporal CPT/evidence interfaces','Assignment, censoring, support, sequential identification, dependent uncertainty and counterfactual regime'),
      ('panels_did','No matched panel/DiD contract established in these inspected pages','Compare separate estimator/design evidence; do not claim vendor feature absence from this source subset'),
      ('decision_policy','Expected utility conditional on supplied influence diagram','Logged-history causal justification, information timing and uncertainty'),
      ('agents_cli_mcp','Compiled engine and wrappers documented; C++ manual excludes most interoperability','Entitled artifact, typed graph/query results, bounded cancellation, recovery and all-request denominators')]
    write(BASE/'capability-comparison.json',dict(rows=[dict(area=a,documented=b,proposal_obligation=c) for a,b,c in matrix],evidence=[ref(BASE/'inherited-review-bindings.json','Official scope'),ref(BASE/'mathematical-review.json','Independent examples')],scope='Matched documentation comparison, not exhaustive vendor feature inventory or native qualification'))
    write(BASE/'dependency-license-review.json',dict(status='documented_classes_not_entitlement',evidence=[ref(BASE/'inherited-review-bindings.json','Official introduction and licensing')],declarations=['Proprietary compiled engine; C++ and listed wrappers','Academic and commercial development rights distinct','Server and end-user deployment rights distinct','Personalized license key required; pricing obtained from vendor'],unresolved=['Exact banking server/service/API use rights','Wrapper and binary ABI/support profile','Redistribution, cancellation and resource terms','Actual quote, maintenance and costs'],agreement_accepted=False,integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',inputs=['Named vendor artifact, platform, wrapper and entitlement','Graph class and unresolved endpoint semantics','Variable/order/outcome map and parameter status','Query target, assumptions and information clock','Temporal slice/lag and utility indexing','Declared cancellation and request-recovery policy'],outputs=['Qualified model result distinct from causal claim','Preserved unresolved pattern, assumptions and default/fitted status','Typed failure, interruption, refusal and request provenance','Declared units and full request/cost denominator'],refusals=['Undocumented endpoint conversion','Uniform tables masquerading as fitted response','Future information used before decision','GUI orientation treated as identified causal direction','Missing supported deployment profile or collapsed failure'],integration_allowed=False))
    next_engine='Retain SMILE engine reference; obtain exact supported artifact/wrapper and deployment entitlement/quote before isolated native trials. Preregister pattern,uniform-parameter,dataset-order,temporal-index,utility-unit,interruption and CLI/MCP recovery fixtures. Preserve graph/causal ambiguity; no native admission.'
    next_offering='Retain GeNIe/SMILE ecosystem reference; qualify GUI-to-engine export and graph marks,parameter provenance,temporal state and information timing under a supported entitled profile. Compare expert/agent elicitation and public scientific oracles without counting GUI and engine as independent capabilities.'
    write(BASE/'omissions-register.json',dict(next_action=next_engine,offering_next_action=next_offering,global_blocker=False,known_routes=['Entitled supported-profile and price inquiry','Finite public graph/model and interface fixtures','GUI/export/wrapper parity tests','Assumption and information-clock review'],remaining=['Exact cutoff snapshots and current release/support','Proprietary native source behavior and all wrappers','Complete server API entitlement and actual economics','Panel, longitudinal and universal identification contracts not established by selected pages'],unknown_without_information=['True bank assignment and omitted causes','Orientation of observationally equivalent causal models without restrictions','Universal uncertainty across arbitrary dependent data']))
    choices={}
    for role,operation,next_action in [('engine',OPS['engine'],next_engine),('offering',OPS['offering'],next_offering)]:
        choice=dict(operation=operation,candidate='SMILE' if role=='engine' else 'BayesFusion GeNIe/SMILE',canonical_candidate='BayesFusion shared engine; '+role+' interface scope',decision='reference',selected_revision='Retained official manual bytes; no binary selected',selected_version='SMILE manual2.2.4.R1 / GeNIe manual5.0.R2',alias_boundary='Distinct engine and GUI decisions; no duplicate engine or runtime qualification',reason='Official scope and exact semantic examples support reference use with separately gated integration.',alternatives=[dict(route='adopt',decision='defer',reason='No blanket causal,platform,wrapper or entitlement qualification'),dict(route='integrate',decision='conditional',reason='Entitled isolated worker' if role=='engine' else 'Reviewed GUI/export/engine workflow with ambiguity and parameter provenance'),dict(route='port',decision='unavailable_without_separate_authorization',reason='Engine source proprietary; independent implementation of public methods is a different proposal'),dict(route='reference',decision='retain',reason='Authentic official manuals and explicit matched-scope comparison'),dict(route='reject',decision='restricted',reason='Reject unsupported causal directions,default probabilities and collapsed failures')],owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Target,causal assumptions,uncertainty and information clock'),('Adapter','Graph marks,names,parameters,temporal/utility mapping and recovery'),('Platform/procurement','Supported artifact,rights,price and maintenance'),('Review','Expert/agent elicitation provenance and public fixture interpretation')]],costs=dict(prices='Unmeasured;24000USD authored example',categories=['entitlement','artifact','conversion','all calls','failed work','review','maintenance']),maintenance='Supported current artifact and quote unconfirmed',revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
        write(BASE/(role+'-choice.json'),choice);choices[role]=choice
    write(BASE/'choice.json',dict(decision='two_reference_choices_one_vendor_engine',choices=choices,integration_allowed=False,limitations=LIMITS))
    authored=dict(integrated_citation_key='exec24_smile_choice',kind='project_evidence_not_scholarly_paper',title='SMILE engine and GeNIie ecosystem scope,causal ambiguity,temporal and cost reference decisions',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;retained official manuals;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact authored review'),inspected_anchors=[ref(BASE/n,'Reviewed scope') for n in ['identity-review.json','inherited-review-bindings.json','capability-comparison.json','choice.json','conversion-contract.json','omissions-register.json']],supported_claims=['Two distinct reference choices share vendor engine and primary evidence','Matched capability and entitlement comparison','Exact observational ambiguity,uniform-initialization,temporal and information-clock witnesses','Conditional public worker,GUI and all-request cost routes'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[authored],new_records=1,new_scholarly_pdfs=0,preserved_official_records=len(selected),native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_two_distinct_reference_choices',evidence=[ref(BASE/n,'Reviewed plan and evidence') for n in ['plan.md','identity-review.json','capability-comparison.json','choice.json','mathematical-review.json']],findings=['One vendor evidence base supports two explicitly different interface decisions.','No duplicate native capability or repeated source-acquisition credit.','Public finite models and interface tests precede costly bank experiments.','Commercial unknowns remain local gates; independent branches continue.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',evidence=[ref(BASE/'development.tex','Connected comparison'),ref(BASE/'sponsor-addition.md','Sponsor decision implications')],findings=['Official scope,causal limitations,alternatives,public routes and costs distinguished.','Mutable documentation and wrapper/date limits explicit.','No native failure or unrestricted identified-set assertion.'],visual_acceptance=False))
    review=dict(status='pass_for_two_reference_only_decisions',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed evidence') for n in ['identity-review.json','inherited-review-bindings.json','capability-comparison.json','source-audit.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','choice.json','engine-choice.json','offering-choice.json','exact-results.json','mathematical-review.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],findings=['Ten retained official audit records rebound to authentic bytes;new authored record only.','Engine and GUI reuse choices remain separate without duplicate implementation claim.','Exact examples and scope matrix preserve causal,parameter,temporal and rights limits.'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(official_records=10,decisions=2,new_records=1,native_execution=False)))

def receipt(role):
    operation=OPS[role];state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==operation
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,operation)
    value=read(BASE/(role+'-choice.json'));value.update(status='pass',scope='Completed '+role+' proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Shared bounded author review')])
    output=ROOT/node['outputs'][0];write(output,value);evidence=[ref(BASE/n,'Reviewed distinct choice') for n in ['review.json',role+'-choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Canonical vendor,distinct interface scope,rights and maintenance limits explicit.','Target,conversion,alternatives,owners,costs and revisit conditions reviewed.','Reference only;no native,unrestricted causal or deployment entitlement inferred.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Distinct reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/(role+'-operation-receipt.json'),result);print(role+' receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','engine','offering']);a=p.parse_args();prepare() if a.command=='prepare' else receipt(a.command)
