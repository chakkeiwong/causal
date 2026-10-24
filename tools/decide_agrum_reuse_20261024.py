#!/usr/bin/env python3
"""aGrUM support/coupling reference decision; no downloaded code execution."""
import argparse,hashlib,json
from pathlib import Path
import agrum_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/agrum-reuse-v1';RAW=ROOT/'docs/literature/raw'
PIN='2ec71906f4108684c5cfb96d1d44f2925e16a32e';OP='SW.DECISION.seed_082';read=lambda p:json.loads(p.read_text())
PRIOR=ROOT/'docs/program/execution/2026-10-24/libdai-reuse-reader-v1/reader/source-audit.json'
LIMITS=['Selected3.2.0sources only;existing discovery/identification reviews remain bounded and inconclusive for native qualification.',
 'No downloaded code or native/Python worker executed;exact examples and conditional deductions are authored.',
 'AST existence does not establish positivity,full ID/IDC correctness or counterfactual coupling.',
 'Complete artifact rights,dependencies,binding behavior,support and actual costs remain unqualified.',
 'Reference only;no native,independent,visual,bank or final acceptance.']
SPECS={
 'exec24_agrum_source_0':[(1,39,'File-specific dual license and authors'),(429,475,'Zero-sum normalization versus CPT refusal'),(961,978,'Direct scalar/empty/dense tensor division')],
 'exec24_agrum_source_1':[(444,466,'Tensorial division and dispatch contract')],
 'exec24_agrum_source_2':[(142,165,'Dense-array ordinary-division macros'),(304,337,'Generic division dispatch'),(355,407,'Operator registrations')],
 'exec24_agrum_source_3':[(79,99,'Array copy,apply and reduction')],
 'exec24_agrum_source_4':[(1,21,'C++/SWIG scope and placeholder badges')],
 'exec24_agrum_delegate_0':[(171,205,'Shared variables by pointer identity'),(289,325,'Direct arithmetic in dense traversal')],
 'exec24_agrum_delegate_1':[(60,109,'Registered operator dispatch without numeric support guard')],
 'exec24_agrum_delegate_2':[(94,169,'Pointer-keyed generic domains'),(265,289,'Generic elementwise arithmetic')],
 'exec19_cxx_id_agrum_2':[(68,110,'Observed and disjoint query-set preconditions'),(134,154,'AST existence and separate evaluation')],
 'exec19_cxx_id_agrum_4':[(77,123,'Separate root posterior replacement'),(173,201,'Intervention slicing and original-variable adaptation')],
 'exec19_cxx_id_agrum_5':[(74,106,'Observational constructor versus causal-model copy')],
 'exec19_cxx_id_agrum_6':[(224,252,'AST division delegates to tensor arithmetic')],
 'exec19_cxx_id_agrum_7':[(139,192,'Python query conversion,model retention and None contract')],
 'exec19_cxx_id_agrum_8':[(150,179,'Constructor mapping and lifetime caveat')],
 'v12_sw2_metadata_agrum_1':[(1,4,'Declared3.2.0')],
 'v12_sw2_metadata_agrum_2':[(41,58,'CMake3.18andC++20')],
 'v12_sw2_metadata_agrum_3':[(1,12,'Root dual-license and third-party notice')],
 'exec13_cxx_agrum_mit':[(1,18,'MIT template and notice requirement')],
 'exec13_cxx_agrum_lgpl':[(1,55,'LGPLversion and combined/header work conditions')]
}

def prepare():
    assert not (BASE/'review.json').exists()
    tree=read(RAW/'v12_sw2_tree_agrum.json');assert tree['sha']==PIN and not tree['truncated'];lookup={x['path']:x for x in tree['tree']}
    commit=read(RAW/'v12_sw_cutoff_commit_agrum.json')[0];assert commit['sha']==PIN and commit['commit']['committer']['date']=='2026-10-06T17:21:03Z'
    records=[]
    for key,specs in SPECS.items():
        p=RAW/(key+'.txt');data=p.read_bytes();r=read(RAW/(key+'.receipt.json'));path=r['url'].split('/'+PIN+'/')[1]
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert hashlib.sha256(data).hexdigest()==r['sha256'] and lookup[path]['sha']==blob
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,f in specs:
            assert 1<=lo<=hi<=len(lines),(key,hi,len(lines));anchors.append(dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest()))
        records.append(dict(source_identity=r['url'],repository_path=path,git_blob=blob,version_date='3.2.0;6October2026;'+PIN,local_copy=ref(p,'Authenticated pinned original'),acquisition=ref(RAW/(key+'.receipt.json'),'Original acquisition'),inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
    assert len(records)==19
    inherited=read(PRIOR);keys={'exec13_cxx_agrum','exec14_native_agrum','exec16_ct_agrum','exec19_cxx_identification_source','v12_sw_agrum'};selected=[s for s in inherited['sources'] if s['integrated_citation_key'] in keys];assert len(selected)==5
    for s in selected:verify_bindings(s)
    write(BASE/'inherited-review-bindings.json',dict(source_audit=ref(PRIOR,'Preserved predecessor audit'),records=selected,scope='Existing bounded source findings,not repeated native qualification'))
    write(BASE/'identity-review.json',dict(status='pass_for_selected_pinned_sources',records=records,commit=PIN,date='2026-10-06',version='3.2.0',evidence=[ref(RAW/'v12_sw2_tree_agrum.json','Complete pinned tree'),ref(RAW/'v12_sw_cutoff_commit_agrum.json','Cutoff commit'),ref(BASE/'inherited-review-bindings.json','Prior source work')],native_execution=False))
    tensor=(RAW/'exec24_agrum_source_0.txt').read_text();ops=(RAW/'exec24_agrum_source_2.txt').read_text();ast=(RAW/'exec19_cxx_id_agrum_6.txt').read_text()
    norm=tensor.split('Tensor< GUM_SCALAR >::normalize() const',1)[1].split('Tensor< GUM_SCALAR >::normalizeAsCPT',1)[0]
    assert 'if (s != (GUM_SCALAR)0)' in norm and 'GUM_ERROR' not in norm
    assert 'GUM_MULTI_DIM_OPERATOR(x, y) (x) / (y)' in ops
    assert 'return this->_op1->eval(bn) / this->_op2->eval(bn);' in ast
    write(BASE/'control-flow-review.json',dict(status='pass_for_selected_support_and_identity_paths',findings=['ASTdivision delegates through tensor and ordinary dense/generic division without added support-zero guard in selected paths.','Ordinary zero-sum normalization preserves zero;CPT normalization rejects a zero row.','Native binary templates identify common variables by pointers.','Counterfactual root replacement retains separate marginals,not their joint posterior.','Python identification None and numeric/runtime failures require distinct response types.'],evidence=[ref(RAW/(k+'.txt'),'Concrete source') for k in ['exec24_agrum_source_0','exec24_agrum_source_2','exec24_agrum_delegate_0','exec24_agrum_delegate_1','exec24_agrum_delegate_2','exec19_cxx_id_agrum_4','exec19_cxx_id_agrum_7']],native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',findings=['Unsupported mass1/2and supported mean1/2giveidentified set[1/4,3/4].','Zero/uniform fills select1/4or1/2without identification.','Equality-profile posterior couples roots;counterfactual1versus1/2.','Illustrative campaign net50000versus10000USD.','Shared tensor axis gives4/7,3/7;distinct axes mismatch13/20.','15000USDover500/375/250gives30/40/60USD.'],evidence=[ref(Path(exact.__file__),'Independent exact code'),ref(BASE/'exact-results.json','Rational outputs'),ref(BASE/'development.tex','Connected derivation')],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='selected_declarations_not_complete_clearance',source_license='LGPL-3.0-or-later OR MIT',declarations=['File-specific copyright and dual-license headers','Root third-party notice;complete dependency audit required','MIT file contains template copyright placeholders','CMake3.18andC++20;SWIGwrapper'],evidence=[ref(RAW/(k+'.txt'),'Pinned declaration') for k in ['exec24_agrum_source_0','v12_sw2_metadata_agrum_2','v12_sw2_metadata_agrum_3','exec13_cxx_agrum_mit','exec13_cxx_agrum_lgpl']],unresolved=['Complete binary and third-party rights','Exact build,ABI,wrapper and native environment','Maintenance,support,security and costs'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',inputs=['Target,graph class,observational/interventional model and annotation identity','Observed disjoint query sets and numeric support requirements','Joint exogenous/posterior coupling or explicit restricted counterfactual law','Variable object/name/domain/order and lifetime mappings','Exact artifact,rights,native worker and public oracle'],outputs=['Symbolic identification separate from evaluable supported numeric result','Typed unidentified,support-failure,domain-error,runtime-failure and qualified-value responses','Preserved annotations,coupling,identity,all requests and costs'],refusals=['Unsupported0/0term','Zero/nonfinite probability mass','Unqualified independent-root substitution','Graph annotation or domain loss','Unqualified binding failure or missing identification'],integration_allowed=False))
    next_action='Retain aGrUM3.2.0reference and conditional isolated C++/Python worker. Reconcile complete artifact/third-party rights and preregister separate discovery endpoint,ID/IDC,zero-support/normalization,joint-root counterfactual,latent-annotation,tensor-identity,wrapper-lifetime and CLI/MCPfailure fixtures. Preserve prior reviews and new support findings;no native capability until qualified.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,known_routes=['Public finite graph/formula and support oracles','Restricted or joint-abduction counterfactual tests','Typed adapter/refusal/lifetime trials','Complete build and third-party rights inventory'],remaining=['Uninspected ID/IDCrecursion reachability and theorem/native parity','Other tensor representations and numeric types','Complete binary/wrapper and native tests','Actual support,prices and maintenance'],unknown_without_information=['Unobserved bank stratum responses','Hidden assignment and arbitrary causal graphs','Unrestricted counterfactual coupling from observational data']))
    choice=dict(candidate='aGrUM/pyAgrum',canonical_candidate='agrumery/aGrUM3.2.0pinned native and Python source',decision='reference',selected_revision=PIN,selected_version='3.2.0',alias_boundary='Separate discovery,identification,evaluation and counterfactual layers;not blanket package approval',reason='Concrete support and coupling boundaries strengthen candidate worker contracts;native qualification and complete rights remain open.',alternatives=[dict(route='adopt',decision='defer',reason='Whole-platform scientific/native scope not established'),dict(route='integrate',decision='conditional',reason='Isolated C++/Python worker with layer-specific rights and fixtures'),dict(route='port',decision='defer',reason='No measured benefit against theorem,numeric and maintenance burden'),dict(route='reference',decision='retain',reason='Authenticated source and exact support/coupling witnesses'),dict(route='reject',decision='restricted',reason='Reject unsupported numeric fill,joint-posterior loss and collapsed refusal types')],owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Graph assumptions,support,identification and coupling'),('Numerical','Domains,valid mass and exact oracles'),('Adapter','Names,objects,annotations,lifetimes and failure responses'),('Rights/platform','Complete artifact,dependencies,build/support and costs')]],costs=dict(prices='Unmeasured;15000USD authored illustration',categories=['source/rights','build','conversion','all calls','failures','review','maintenance']),maintenance='Pinned active-source snapshot;actual service/support not verified',revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    source=dict(integrated_citation_key='exec24_agrum_source',kind='software_primary_sources',title='aGrUM3.2.0tensor support,formula evaluation,counterfactual and wrapper contracts',author='aGrUM and pyAgrum contributors',year=2026,source_identity='https://github.com/agrumery/aGrUM/tree/'+PIN,version_date='3.2.0;6October2026;'+PIN,local_copy=ref(RAW/'exec24_agrum_source_0.txt','Tensor evaluation original'),records=records,identity_evidence=[ref(BASE/'identity-review.json','Pinned identity and preserved reviews')],inspected_anchors=[r['local_copy'] for r in records],supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
    authored=dict(integrated_citation_key='exec24_agrum_choice',kind='project_evidence_not_scholarly_paper',title='Authored aGrUM support,counterfactual coupling,tensor identity and cost witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact review'),inspected_anchors=[ref(BASE/n,'Bounded choice') for n in ['choice.json','conversion-contract.json','control-flow-review.json','omissions-register.json']],supported_claims=['Exact unsupported-stratum identified set','Joint versus marginal abduction and monetary consequences','Shared/distinct tensor identity and bounded worker routes'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,authored],new_records=2,new_scholarly_pdfs=0,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_reference_choice',evidence=[ref(BASE/n,'Plan and evidence') for n in ['plan.md','identity-review.json','choice.json','mathematical-review.json']],findings=['Preserve prior discovery/identification findings rather than repeat or upgrade them.','Follow concrete tensor delegates to close selected source-support question.','Differentiate symbolic identification,numeric support,coupling and native behavior.','Public fixtures precede expensive bank work;independent proposal branches remain eligible.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],findings=['Support and posterior notation,assumptions,alternatives and costs explained.','Static branches distinguished from observed native failures.','No new unavailable scholarly source cited.'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed evidence') for n in ['identity-review.json','inherited-review-bindings.json','source-audit.json','control-flow-review.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','choice.json','exact-results.json','mathematical-review.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],findings=['Nineteen selected originals authenticate and five prior source reviews remain preserved.','Exact support,coupling,identity and cost witnesses reproduce.','Reference decision grants no native/causal/bank acceptance.'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(authenticated=19,decision='reference',new_records=2,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed aGrUM layered proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value);evidence=[ref(BASE/n,'Reviewed choice') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Pinned identity,layer aliases,rights and maintenance limits explicit.','Target,conversion,alternatives,owners,costs and revisit conditions reviewed.','Reference only;no native,unrestricted causal or full rights qualification.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('aGrUM reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
