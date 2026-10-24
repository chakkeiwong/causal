#!/usr/bin/env python3
"""Authenticate inert Ananke text and record a bounded proposal reference choice."""
import argparse, ast, hashlib, json, zipfile
from pathlib import Path
import ananke_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/ananke-reuse-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-18/python-identification-v1'
SOURCE=PRIOR/'ananke-inert-source'
OP='SW.DECISION.seed_070'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Selected authentic 0.5.0 wheel uploaded5December2023;not newest-release or current-support coverage.',
 'Selected source paths inspected,not exhaustive software,numerical,dependency or theorem qualification.',
 'Apache text and conflicting metadata retained;complete rights and installed environment unresolved.',
 'No downloaded package imported or executed;authored examples and AST inspection are not native trials.',
 'Binary reporting mismatch is conditional source control flow;not an observed native dataset failure.',
 'True-model oracle requires supplied mechanisms;unknown graph,assignment or cross-world truth is not manufactured.',
 'Reference-only disposition;integration false;native,visual,independent and final acceptance remain open.']
SPECS={
 'ananke/identification/one_line.py':[(37,59,'Intervention fixation and relevant outcome ancestors'),
  (90,140,'District fixability,Boolean result,string concatenation and stdout'),
  (197,218,'Experimental preflight helpers'),(250,262,'Ancestral precondition uses NotIdentifiedError'),
  (343,367,'GID precondition uses same exception'),(378,427,'Supplied-model witness comparison')],
 'ananke/identification/oracle.py':[(18,49,'Supplied-model intervention bypasses identification;conditional normalization')],
 'ananke/identification/missing_id.py':[(6,47,'Full-law query and R_/X_ split-name convention')],
 'ananke/estimation/counterfactual_mean.py':[(16,46,'Target and estimator dispatch'),
  (54,151,'Fixability-specific selection'),(1091,1145,'Point reporting flag,state space,ones column and treatment values'),
  (1147,1185,'Binary replicate branch omits reporting flag;row sampling and quantiles')],
 'ananke/graphs/sg.py':[(13,41,'Graph preconditions'),(55,112,'Selected validation with correctness TODOs;no observed failure inferred')],
 'ananke/graphs/admg.py':[(184,225,'Reachable closure'),(227,270,'Fixability loop and returned partial order')],
 'ananke_causal-0.5.0.dist-info/METADATA':[(1,33,'Distribution identity,dependency declarations and conflicting classifiers')],
 'LICENSE':[(1,5,'Apache2.0 text'),(66,121,'Grant,notice and attribution text'),(178,201,'Template appendix notice')],
 'ananke_causal-0.5.0.dist-info/LICENSE':[(1,5,'Duplicate Apache2.0 text')]
}

def prepare():
    assert not (BASE/'review.json').exists()
    acquisition=read(PRIOR/'acquisition.json')
    wheel=ROOT/acquisition['path'];data=wheel.read_bytes()
    assert hashlib.sha256(data).hexdigest()==acquisition['sha256']
    metadata=ROOT/acquisition['metadata_path']
    assert core.sha(metadata)==acquisition['metadata_sha256']
    selected=next(x for x in read(metadata)['releases']['0.5.0'] if x['filename']==wheel.name)
    assert selected['digests']['sha256']==acquisition['sha256']
    assert selected['upload_time_iso_8601']==acquisition['declared_upload']<'2026-10-07T15:59:59Z'
    assert selected['url']==acquisition['source_identity']
    extraction=read(PRIOR/'extraction.json');verify_bindings(extraction)
    extracted={x['member']:x['local_copy'] for x in extraction['records']}
    inherited=read(PRIOR/'source-audit.json');verify_bindings(inherited)
    records=[]
    with zipfile.ZipFile(wheel) as z:
        for name,specs in SPECS.items():
            p=SOURCE/name;raw=p.read_bytes();assert z.read(name)==raw
            if name in extracted:assert core.sha(p)==extracted[name]['sha256']
            lines=raw.decode().splitlines();anchors=[]
            for lo,hi,finding in specs:
                assert 1<=lo<=hi<=len(lines),(name,lo,hi,len(lines))
                anchors.append(dict(lines=[lo,hi],finding=finding,
                    excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest()))
            records.append(dict(source_identity=selected['url']+'#'+name,
                archive_member=name,version_date='0.5.0;5December2023',
                local_copy=ref(p,'Verbatim selected wheel member;never executed'),
                inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
    assert len(records)==9
    assert (SOURCE/'LICENSE').read_bytes()==(SOURCE/'ananke_causal-0.5.0.dist-info/LICENSE').read_bytes()
    tree=ast.parse((SOURCE/'ananke/estimation/counterfactual_mean.py').read_text())
    method=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='compute_effect')
    flag_ifs=[n for n in ast.walk(method) if isinstance(n,ast.If) and 'report_log_odds' in ast.unparse(n.test)]
    assert len(flag_ifs)==1 and flag_ifs[0].lineno==1139
    loop=next(n for n in ast.walk(method) if isinstance(n,ast.For) and n.lineno==1154)
    assert 'report_log_odds' not in ast.unparse(loop)
    write(BASE/'identity-review.json',dict(status='pass_for_selected_wheel_identity',records=records,
        selected_version='0.5.0',date=selected['upload_time_iso_8601'],
        evidence=[ref(wheel,'Authenticated selected wheel'),ref(PRIOR/'acquisition.json','Prior acquisition'),
            ref(PRIOR/'extraction.json','Preserved inert extraction'),ref(metadata,'Identity only;not technical evidence')],
        current_version_claim=False,installed_environment_verified=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'reporting-branch-review.json',dict(status='pass_for_static_control_flow_witness',
        evidence=[ref(SOURCE/'ananke/estimation/counterfactual_mean.py','Selected implementation'),
            ref(Path(__file__),'AST-only inspection')],point_flag_if_line=1139,
        bootstrap_loop_line=1154,bootstrap_loop_references_reporting_flag=False,
        scope='Binary outcome,report_log_odds false,n_bootstraps positive;conditional source inconsistency',
        native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_finite_examples',
        evidence=[ref(Path(exact.__file__),'Independent Fraction and math arithmetic'),
            ref(BASE/'exact-results.json','Exact values and bounded decimal'),ref(BASE/'development.tex','Connected argument')],
        findings=['Risk difference1/5 versus log odds log(8/3);hypothetical same replicate means only.',
            'Distinct token arrays concatenate toABC;not a claim about identical graph outputs.',
            'R_credit_score split maps toX_credit;requires explicit name conversion.',
            '3000USD divided by150/125/100 gives20/24/30.'],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='selected_declarations_inspected_not_clearance',
        evidence=[ref(SOURCE/'LICENSE','Retained Apache text'),ref(SOURCE/'ananke_causal-0.5.0.dist-info/METADATA','Conflicting classifiers and dependencies'),
            ref(PRIOR/'conversion-contract.json','Preserved cross-candidate declared version incompatibilities')],
        python='>=3.9,<4',numpy='>=1.23,<2',pandas='>=1.4.3,<2',statsmodels='>=0.13.2,<0.14',
        pgmpy='>=0.1.21,<0.2',direct_sympy_declaration=False,
        unresolved=['Metadata classifier conflict and component notices','Transitive dependency rights',
            'Lock and installed binary equality','SymPy transitive provision','Platform support and maintenance costs'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',
        inputs=['Graph class,named nodes,edge and query semantics,information clock',
            'Available observational/experimental laws and scientific assumptions',
            'Injective internal-name mapping,treatment values,outcome type and reserved names',
            'Estimator,effect scale,replicate law,RNG and resource limits'],
        outputs=['Typed expression with named tokens and retained fixing diagnostics',
            'Separate invalid,unsupported,nonidentified,engine_failure and identified results',
            'Matching point/replicate/interval scale and probability boundaries',
            'Every replicate status,original denominator and full costs'],
        refusals=['Unresolved graph or experimental preconditions','Ambiguous names or display-string execution',
            'Mismatched effect scales','Zero conditioning probability or invalid odds',
            'Unjustified dependent resampling or unqualified environment'],integration_allowed=False))
    next_action='Retain selected0.5.0 source as reference. Resolve distribution notices and isolated dependency lock; preregister graph/query,experimental-preflight,name-roundtrip,effect-scale,probability-boundary,resampling,failure and full-cost public fixtures before native admission. Inspect newer releases separately if scope changes; do not repeat selected source inspection.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,
        known_routes=['Typed graph/expression and error schema','Explicit reporting correction or restricted wrapper',
            'Isolated environment and rights review','Known-law public fixtures and all-request accounting'],
        remaining=['Complete graph/method implementation review','Scholarly originals before theorem adoption',
            'Native and dependent-data calibration','Current support,complete costs and independent review'],
        unknown_without_information=['True business graph and assignment','Arbitrary individual cross-world law','Universal dependence-valid inference']))
    choice=dict(candidate='Ananke',canonical_candidate='ananke-causal',selected_version='0.5.0',decision='reference',
        reason='Selected identification and oracle interfaces are useful references;typed conversion,reporting,environment and rights obligations precede executable admission.',
        alternatives=[dict(route='adopt',decision='defer',reason='No unrestricted qualified interface or native evidence'),
            dict(route='integrate',decision='conditional',reason='Narrow isolated comparator after registered public qualification'),
            dict(route='port',decision='defer',reason='No measured need for transferred graph/symbolic/numerical maintenance'),
            dict(route='reference',decision='retain',reason='Authenticated selected sources and bounded examples'),
            dict(route='reject',decision='restricted',reason='Reject unrestricted automatic graph truth or cross-world claims;do not reject all scoped uses')],
        comparator_evidence=ref(PRIOR/'candidate-register.json','Inherited DoWhy,y0,pgmpy distinctions and limits'),
        owners=[dict(role=r,responsibility=t) for r,t in [
            ('Scientific','Graph,query,information,estimand and sampling law'),
            ('Adapter','Typed conversion,names,reporting scales and error states'),
            ('Rights/platform','Distribution,notices,dependency lock and support'),
            ('Evaluation','Known-law tasks,oracles,all failures and total costs')]],
        costs=dict(prices='Unmeasured;3000USD authored example',categories=['engineering','rights/scientific review',
            'environment','all-request execution and bootstrap failures','storage','maintenance']),
        maintenance='Selected historical community distribution;future support and service levels unverified',
        revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    source=dict(integrated_citation_key='exec24_ananke_source',kind='software_primary_sources',
        title='Ananke0.5.0 authenticated identification,oracle,naming and effect-reporting source',
        author='Ananke community',year=2023,source_identity=selected['url'],version_date='0.5.0;5December2023;selected historical release',
        local_copy=ref(SOURCE/'ananke/identification/one_line.py','Selected identification original'),records=records,
        identity_evidence=[ref(BASE/'identity-review.json','Wheel identity and cutoff')],
        inspected_anchors=[r['local_copy'] for r in records],supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
    authored=dict(integrated_citation_key='exec24_ananke_choice',kind='project_evidence_not_scholarly_paper',
        title='Authored Ananke reporting-scale,naming,conversion and reuse comparison',author='Causal banking proposal project',year=2026,
        source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no package execution',
        local_copy=ref(BASE/'mathematical-review.json','Authored finite examples'),
        inspected_anchors=[ref(BASE/n,'Bounded decision') for n in ['choice.json','conversion-contract.json','omissions-register.json','reporting-branch-review.json']],
        supported_claims=['Finite scale and naming witnesses','Reference decision and conditional routes','Owners,costs and qualification limits'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,authored],new_records=2,new_scholarly_pdfs=0,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_reference_choice',
        evidence=[ref(BASE/n,'Reviewed plan and constraints') for n in ['plan.md','identity-review.json','choice.json','reporting-branch-review.json','mathematical-review.json']],
        findings=['Historical source selection explicit','Static branch and authored arithmetic separated from native results',
            'Preserve original inconclusive Python coverage','No theorem adopted from package bibliographies',
            'Integrate reader and sponsor before claiming program completion']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_scoped_connected_argument',
        evidence=[ref(BASE/'development.tex','Manuscript'),ref(BASE/'sponsor-addition.md','Sponsor argument')],
        findings=['Banking information problem precedes software choices','Units,assumptions,alternatives and owners explained',
            'Static findings,authored examples and native claims remain separate'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/n,'Reviewed candidate') for n in ['identity-review.json','source-audit.json','dependency-license-review.json',
            'conversion-contract.json','omissions-register.json','choice.json','reporting-branch-review.json','exact-results.json',
            'mathematical-review.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],
        findings=['Nine selected originals authenticate to historical wheel','Point and replicate scale mismatch traced without package execution',
            'Named conversion,scientific,rights,native and cost obligations retained'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated=len(records),decision='reference',new_records=2,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed decision') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Selected distribution,version,rights declarations,dependencies and maintenance limits explicit.',
        'Graph/query,output scales,conversion,alternatives,owners,costs and revisit trigger reviewed.',
        'Reference only;integration false and no capability admission;native qualification remains conditional.']
    result=run.ledger.receipt_template(node)
    result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],
        limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result)
    write(BASE/'operation-receipt.json',result);print('Ananke reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
