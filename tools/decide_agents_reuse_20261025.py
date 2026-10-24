#!/usr/bin/env python3
"""Resolve two umbrella leads through six named reference-only component choices."""
import argparse,base64,hashlib,json
from pathlib import Path
from urllib.parse import urlsplit
import agents_reuse_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/agents-reuse-v1'
RAW=ROOT/'docs/literature/raw'
AUDIT=ROOT/'docs/program/execution/2026-10-25/copilot-reuse-reader-v1/reader/source-audit.json'
HIST=ROOT/'docs/program/execution/2026-10-14/iid-discovery'
OPS={'discovery':'SW.DECISION.seed_104','assistants':'SW.DECISION.seed_105'}
read=lambda p:json.loads(p.read_text())
KEYS=['exec14_iid_cd','exec14_iid_gpt','exec14_iid_scd','exec13_data_causalagent_code','exec13_data_oci_code','exec13_data_ontolearner_code']
LIMITS=['Selected immutable static paths only; no installed component, provider call, downloaded code, CLI or MCP service executed.',
 'Root notices do not establish complete dependency, backend, provider, data or deployment rights.',
 'No family-wide survey closure, native capability, current maintenance, measured performance or actual banking costs.',
 'Reference choices are complete proposal dispositions; conditional integration, scientific qualification and institutional acceptance remain open.',
 'Fresh visual, independent and final acceptance remain open.']
PROFILES=[
 dict(id='cd',key=KEYS[0],name='LLM-CD',group='discovery',revision='8ea28948affdab88bee91a8b7858e89dc9424ffe',date='2025-02-15',tree='v12_la_llm_cd_tree.json',role='Language-derived ancestry/order/edge constraints',rights='Root rights unresolved; nested BI-CaMML BSD-style notice is narrower',dependency='Selected requirements include gurobipy10.0.2; backend entitlement/environment unqualified',finding='Selected wrappers distinguish ancestry/direct edges but use shared paths and unchecked shell calls.',route='Resolve root/backend rights; isolate each request, type constraints, check process completion and bind output identity.'),
 dict(id='gpt',key=KEYS[1],name='causal_GPT',group='discovery',revision='2001fb5660d8e5d9a6c3a159b41d739316b8f91a',date='2024-06-12',tree='v12_la_causal_gpt_tree.json',role='Model-answer aggregation for discovery judgments',rights='Retained BSD-3-Clause notice; dependencies/provider rights separate',dependency='OpenAI1.19.0 declaration plus unpinned packages; native environment unqualified',finding='Selected PC interface emits0/1, with unfinished weighted-vote and missing-row returns0.',route='Separate linguistic evidence from data tests; type missingness, retain answer provenance and qualify each scientific claim.'),
 dict(id='scd',key=KEYS[2],name='LLM-and-SCD',group='discovery',revision='5aaeaea89e71e2cff443289e473c06d2f79172c5',date='2024-01-31',tree='v12_la_llm_scd_tree.json',role='Notebook elicitation and backend constraint experiments',rights='No root license in retained complete tree; original API404 retained',dependency='Notebook pip declarations are not an exact environment lock',finding='Selected code uses first-token top-five Yes/yes mass and strict0.05/0.95 thresholds with backend-specific meanings.',route='Resolve source rights; freeze prompts/provider/delegates and relation semantics; use held-out scientific and abstention oracles.'),
 dict(id='causalagent',key=KEYS[3],name='CausalAgent',group='assistants',revision='87a4f6a45e9d77f9b0e8b7796489c47e50af41b8',date='2026-01-28',tree='v12_la_causalagent_tree.json',role='Selected MCP analysis-tool interface',rights='Retained MIT notice; complete dependency/provider rights unresolved',dependency='Selected requirements include mcp1.8.0 and mixed version constraints',finding='Selected module imports PC but calls undefined/unimported OLC; separate malformed-JSON parser returns{}.',route='Verify callable bindings, graph/schema conversions and typed parse/failure/refusal states; qualify a bounded service.'),
 dict(id='oci',key=KEYS[4],name='oci-agent',group='assistants',revision='a978030e2c69cddab235e8737ee0ca527759ac49',date='2026-07-27',tree='v12_la_oci_agent_tree.json',role='Notebook execution and estimator orchestration',rights='Retained Apache-2.0 notice; notebooks/data/providers separately scoped',dependency='Metadata0.2.0,Python>=3.10 and several unlocked dependencies',finding='Spec-selected notebook uses timeout=-1; selected ATO path uniformly averages after trimming.',route='Bound approved notebook execution and result identity; name actual target weights, nuisance fits and uncertainty; qualify against exact oracles.'),
 dict(id='ontology',key=KEYS[5],name='OntoLearner',group='assistants',revision='074a41ba23a85f5b72d4e28da042eab3d50bd90a',date='2026-09-03',tree='v12_la_ontolearner_tree.json',role='Ontology resource and semantic mapping component',rights='Retained MIT code notice does not establish downloaded ontology rights',dependency='Metadata0.0.0,Python>=3.10,<3.14 and wildcard/range dependencies',finding='Selected hub download omits revision; code identity alone does not freeze ontology bytes.',route='Pin data revision/hash/rights and concept mappings; keep ontology relations distinct from causal edges.')]

def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def prepare():
    assert not (BASE/'review.json').exists()
    audit=read(AUDIT);sources=[next(x for x in audit['sources'] if x['integrated_citation_key']==k) for k in KEYS]
    for s in sources:verify_bindings(s)
    historical=read(HIST/'primary-review.json');validation=[];trees={}
    for p in PROFILES:
        t=read(RAW/p['tree']);assert not t['truncated'];trees[p['id']]={x['path']:x['sha'] for x in t['tree'] if x['type']=='blob'}
    for p in historical['packages']:
        tree=trees[p['id']]
        for x in p['records']:
            verify_bindings(x['local_copy']);data=(ROOT/x['local_copy']['path']).read_bytes()
            relative=x['source_identity'].split('/'+p['revision']+'/')[1]
            assert blob(data)==x['git_blob_sha1']==tree[relative]
            validation.append(dict(local_copy=x['local_copy'],git_blob_sha1=blob(data),upstream_path=relative,revision=p['revision']))
    for profile,source in zip(PROFILES[3:],sources[3:]):
        for x in source['additional_sources']:
            p=ROOT/x['local_copy']['path'];data=p.read_bytes();url=x['source_identity']
            if 'raw.githubusercontent.com' in url:
                rel=url.split('/'+profile['revision']+'/')[1];assert blob(data)==trees[profile['id']][rel]
                validation.append(dict(local_copy=x['local_copy'],git_blob_sha1=blob(data),upstream_path=rel,revision=profile['revision']))
    for ident,stem in [('gpt','causal_gpt'),('causalagent','causalagent'),('oci','oci_agent'),('ontology','ontolearner')]:
        path=RAW/('v12_la_'+stem+'_license.json');d=read(path);data=base64.b64decode(d['content'])
        assert blob(data)==d['sha']==trees[ident][d['path']]
        assert (BASE/(stem+'-license.txt')).read_bytes()==data
        validation.append(dict(local_copy=ref(path,'Authentic license API bytes'),decoded=ref(BASE/(stem+'-license.txt'),'Exact decoded original'),git_blob_sha1=d['sha'],upstream_path=d['path']))
    for name,relative in [('v12_la_llm_cd_source_1.txt','requirements.txt'),('v12_la_llm_cd_source_2.txt','BI-CaMML/LICENSE.txt')]:
        path=RAW/name;assert blob(path.read_bytes())==trees['cd'][relative]
        validation.append(dict(local_copy=ref(path,'Selected dependency or nested rights original'),git_blob_sha1=blob(path.read_bytes()),upstream_path=relative))
    for ident,stem in [('cd','llm_cd'),('scd','llm_scd')]:
        assert not any('/' not in p and ('license' in p.lower() or 'copying' in p.lower()) for p in trees[ident])
        assert read(RAW/('v12_la_'+stem+'_license.receipt.json'))['status']=='failed'
    anchors=[('exec14_iid_cd_3.txt',['=>','->','os.system']),('exec14_iid_cd_4.txt',['abs_edge','forb_anc','parse_screen_output']),('v12_la_causal_gpt_source_1.txt',['if self.method == "wvot":','return 0']),('v12_la_causalagent_source_1.txt',['from Agent.causal.causalachieve import run_pc_analysis','analysis_result = run_olc_analysis(csv_data)']),('v12_la_causalagent_source_2.txt',['except json.JSONDecodeError','return {}']),('v12_la_oci_agent_source_3.txt',['NotebookClient(nb, timeout=-1','spec["analysis_notebook"]']),('v12_la_ontolearner_source_1.txt',['hf_hub_download(repo_id=repo_id, filename=filename, repo_type="dataset")'])]
    for name,tokens in anchors:assert all(t in (RAW/name).read_text() for t in tokens),name
    for x in historical['scd_inspected_code']:verify_bindings(x)
    assert 'top_logprobs = 5' in (HIST/'scd-3-code.txt').read_text()
    assert 'probability[i, j]<0.05' in (HIST/'scd-4-code.txt').read_text()
    assert 'aipw_summary(Y_DR[keep])' in (BASE/'oci-code-only.txt').read_text()
    d=read(RAW/'v12_la_oci_notebook.json')
    if 'content' in d:d=json.loads(base64.b64decode(d['content']))
    expected='\n\n'.join(f"CELL {i}\n"+''.join(c.get('source',[])) for i,c in enumerate(d['cells']) if c.get('cell_type')=='code')
    assert (BASE/'oci-code-only.txt').read_text()==expected
    write(BASE/'git-byte-validation.json',dict(status='pass',validated_originals=validation,trees=[ref(RAW/p['tree'],'Complete immutable source tree') for p in PROFILES],native_execution=False))
    write(BASE/'inherited-review-bindings.json',dict(sources=sources,
        authentic_validation=ref(BASE/'git-byte-validation.json','Retained originals authenticated to Git blobs'),
        reviewed_code=[ref(RAW/n,'Selected original source anchor') for n,_ in anchors]+historical['scd_inspected_code']+[ref(BASE/'oci-code-only.txt','Original notebook code only; no saved outputs')],
        original_rights_omissions=[ref(RAW/('v12_la_'+n+'_license.receipt.json'),'Retained unavailable root license') for n in ['llm_cd','llm_scd']],
        cutoff='2026-10-07',native_execution=False))
    write(BASE/'identity-review.json',dict(status='pass_for_named_components',profiles=PROFILES,
        aliases=['causal_GPT license API redirects to IPL-UV/CHG_LLM; same pinned license Git blob, not a second engine'],
        scope='Six selected component profiles resolve two leads; no exhaustive discovery-agent or diagram-assistant family claim.',
        evidence=[ref(BASE/'inherited-review-bindings.json','Versioned authentic source scope')]))
    write(BASE/'capability-comparison.json',dict(rows=[dict(candidate=p['name'],role=p['role'],static_finding=p['finding'],proposal_contract=p['route']) for p in PROFILES],native_execution=False))
    assert exact.calculate()==read(BASE/'exact-results.json')
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_examples',
        evidence=[ref(Path(exact.__file__),'Independent rational arithmetic and graph closure'),ref(BASE/'exact-results.json','Reproduced authored results')],
        checks=['A ancestor of C does not imply a direct edge in A->B->C.','Numeric missing0 lies below1/20; unavailability is a typed status.','Two equally prevalent strata retained by stipulated trim: effect5 versus overlap-weighted45/17.','Population estimand illustration, not finite-sample behavior or a native bug reproduction.','5000/100=50;5000/80=125/2;5000/50=100USD; hypothetical full costs.'],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='bounded_component_specific',profiles=[dict(candidate=p['name'],rights=p['rights'],dependencies=p['dependency']) for p in PROFILES],
        unresolved=['Complete transitive dependency, delegate, data, provider and deployment inventory','Current support and artifact availability','Institutional permission for selected deployment'],agreement_accepted=False,integration_allowed=False,
        evidence=[ref(BASE/'git-byte-validation.json','Selected source and license blobs'),ref(BASE/'inherited-review-bindings.json','Original rights omissions')]))
    contract=dict(status='proposed_reference_only',inputs=['request_id','question_version','data_schema_digests','population','treatment_version','information_outcome_clocks','graph_class','typed_ancestry_order_edge_restrictions','assumption_provenance','model_prompt_environment','rights_profile','deadline_budget'],
        outputs=['scientific_status','typed_execution_status','graph_marks_variable_mapping','edit_authority_and_provenance','estimand_weights','ontology_revision_hash','identified_conditional_set_or_refusal','all_attempt_costs'],
        component_contracts={p['name']:p['route'] for p in PROFILES},refusals=['Lost graph or target semantics','Unsupported data-test calibration','Missing source rights','Stale/unauthorized edit','Malformed response','Unidentified target','Unknown completion after timeout'],integration_allowed=False,native_execution=False)
    write(BASE/'conversion-contract.json',contract)
    fixtures=[('ancestry_only','A->B->C round trip retains no direct A->C'),('missing_cache','Unavailable has no numeric p-value'),('threshold_boundaries','Exact0.05/0.95 retains specified strict-threshold behavior without causal probability claim'),('model_answer_vs_data_test','Evidence types and laws remain separate'),('callable_binding','Each exposed tool resolves its documented callable'),('malformed_json','Invalid parse differs from valid empty result and scientific refusal'),('stale_output','Digest mismatch cannot become fresh success'),('timeout_cancel','Typed failed or unknown completion and complete accounting'),('target_weights','Uniform retained target5 and specified overlap45/17 remain distinct'),('ontology_revision','Changed data bytes require new identity'),('question_rephrase','Population/treatment/clock change requires new question version'),('duplicate_delivery','Logical requests and execution attempts counted separately')]
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',arms=['Fixed conventional workflow','Permitted frozen upstream component','Contract-wrapped workflow','Human-assisted comparator with recorded effort'],
        freezes=['Task/version/train-test split','Generated structural law and target','Provider/model/prompts/settings','Exact environment and permitted rights','Scientific tolerance, precision and sample size','Failure/scoring rules'],fixtures=[dict(name=n,oracle=o,status='not_run') for n,o in fixtures],
        data_scope='Generated SCMs for truth; permitted public observational data for workflow stress without invented assignment truth.',denominators='All logical requests, attempts, completions, refusals, failures, unknown status and full costs',native_execution=False))
    choices={}
    owners=[dict(role=r,responsibility=d) for r,d in [('Scientific','Population, graph restrictions, estimand and uncertainty'),('Adapter','Typed conversion and failure/refusal semantics'),('Platform/rights','Pinned permitted code, data and providers'),('Evaluation','Held-out oracles and complete denominator'),('Maintenance','Model/prompt/data drift and semantic regression')]]
    for group,op in OPS.items():
        candidates=[]
        for p in PROFILES:
            if p['group']!=group:continue
            candidates.append(dict(**p,decision='reference',alternatives=[dict(route='adopt',disposition='defer',reason='Selected rights/environment and native qualification incomplete'),dict(route='integrate',disposition='conditional',reason=p['route']),dict(route='port',disposition='conditional_after_rights_and_specification',reason='Copying rights, delegate meanings and independent semantic tests must be resolved'),dict(route='reference',disposition='retain',reason='Authentic selected source supplies a concrete design comparator'),dict(route='reject',disposition='specific_semantic_paths',reason=p['finding']+' Do not promote the unsupported meaning into a causal result.')],integration_allowed=False))
        revisit='Resolve each selected component rights/environment and contract independently; preregister public scientific, refusal, transport and full-cost comparisons before native admission. Preserve unknown bank truth and unrestricted identification limits.'
        choice=dict(operation=op,candidate='Discovery-agent components' if group=='discovery' else 'Question and diagram assistant components',canonical_candidates=candidates,
            decision='reference',reason='Resolve lead into concrete roles and conditional routes without umbrella approval.',owners=owners,owner_status='Proposed roles, no institutional acceptance',
            costs=dict(measured=False,illustration=ref(BASE/'exact-results.json','Hypothetical complete costs'),actual_costs='Unknown',categories=['preparation','all attempts/providers','review','maintenance']),maintenance='Pinned historical source assessment; current support unknown',revisit_trigger=revisit,integration_allowed=False,capabilities=[],limitations=LIMITS)
        write(BASE/(group+'-choice.json'),choice);choices[group]=choice
    write(BASE/'choice.json',dict(decision='two_umbrella_resolutions_six_named_reference_components',choices=choices,integration_allowed=False,limitations=LIMITS))
    write(BASE/'omissions-register.json',dict(global_blocker=False,known_routes=['Component-specific rights/environment inventory','Typed semantic conversion and failure interfaces','Public/generated preregistered qualification and full costs'],
        unresolved=['Unresolved root rights for LLM-CD/LLM-and-SCD','Native behavior and complete runtime locks','Provider/data permissions and versions','Current maintenance and institutional owners'],unknown_without_information=['Bank assignment truth','Causal meaning of semantic relations without domain evidence','Universal hidden-variable identification or dependent-data calibration'],next_action='Advance permitted component contracts independently; no source omission blocks other proposal obligations.'))
    authored=dict(integrated_citation_key='exec25_agents_choice',kind='project_evidence_not_scholarly_paper',title='Six agent component reference choices and typed causal qualification contracts',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; pinned pre-cutoff revisions and later acquisition limits explicit',local_copy=ref(BASE/'choice.json','Six component reference decisions'),
        inspected_anchors=[ref(BASE/n,'Reviewed authored reasoning') for n in ['identity-review.json','capability-comparison.json','mathematical-review.json','conversion-contract.json','qualification-plan.json','dependency-license-review.json','omissions-register.json']],supported_claims=['Six separate component reference choices within two lead resolutions','Exact graph/missingness/estimand/cost illustrations','Proposed scientific and transport contracts; no native admission'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[authored],new_records=1,new_scholarly_pdfs=0,preserved_original_records=6,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_two_component_reference_resolutions',evidence=[ref(BASE/n,'Reviewed plan') for n in ['plan.md','identity-review.json','choice.json','mathematical-review.json','conversion-contract.json','qualification-plan.json','dependency-license-review.json']],findings=['All three operation criteria addressed; no family-wide approval','Each candidate has routes, rights limits, owners, costs and revisit trigger','Public/generated evaluation proposed without bank truth or executed-code claims','Preserve prior manuscript inputs and citations; serialize canonical publication after commercial delivery']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',evidence=[ref(BASE/'development.tex','Banking argument'),ref(BASE/'sponsor-addition.md','Investment implications')],findings=['Question version precedes diagram/estimate','Static source findings separated from proposed fixes and exact authored examples','Each component role and rights boundary explicit'],visual_acceptance=False))
    review=dict(status='pass_for_two_reference_only_resolutions',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed component evidence') for n in ['git-byte-validation.json','inherited-review-bindings.json','identity-review.json','choice.json','discovery-choice.json','assistants-choice.json','capability-comparison.json','mathematical-review.json','exact-results.json','source-audit.json','conversion-contract.json','qualification-plan.json','dependency-license-review.json','omissions-register.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Validation and receipt logic')],findings=['Six named immutable components assessed','Two proposal lead resolutions complete with no capabilities','Authored exact examples reproduce; originals retained and Git-authenticated'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass',decisions=2,components=6,validated_originals=len(validation),native_execution=False)))

def receipt(role):
    op=OPS[role];state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op)
    value=read(BASE/(role+'-choice.json'));value.update(status='pass',scope='Completed named-component proposal reference resolution; no native admission',evidence=[ref(BASE/'review.json','Author source and semantic review')]);output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed component resolution') for n in ['review.json',role+'-choice.json','conversion-contract.json','dependency-license-review.json','qualification-plan.json']]
    findings=['Distinct pinned components, roles, sources, rights and maintenance limits bound','Targets, uncertainty, alternatives, proposed owners, full costs and revisit trigger explicit','Reference-only choices; conditional contracts and public oracles remain proposed; integration disallowed']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Named component disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/(role+'-operation-receipt.json'),result);print(role+' receipt prepared.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','discovery','assistants']);a=p.parse_args();prepare() if a.command=='prepare' else receipt(a.command)
