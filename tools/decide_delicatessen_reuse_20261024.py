#!/usr/bin/env python3
"""Review pinned estimating-equation sources without running downloaded code."""
import argparse,ast,hashlib,json,re
from pathlib import Path
import delicatessen_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/delicatessen-reuse-v1'
RAW=ROOT/'docs/literature/raw';PIN='8962bf0cb21a41873c708e1c8d64e692e95e9b58'
OP='SW.DECISION.seed_074';read=lambda p:json.loads(p.read_text())
LIMITS=['Selected pinned version4.3 source;installed distribution equivalence unverified.',
 'Seven originals inspected;full derivative,regression,GMM and dependency internals remain outside selected review.',
 'Top-level MIT inspected;complete transitive rights and supported numerical environment remain open.',
 'No downloaded package executed;conditional control-flow deductions and rational witnesses are not native measurements.',
 'Reference-only decision;no capability,visual,independent,bank or final acceptance.']
SPECS={
 'v12_gap3_delicatessen_technical':('delicatessen/estimating_equations/causal.py',[(703,776,'AIPW parameter,shape and counterfactual-design contract'),(836,899,'Nuisance score stack,clipping,link selection and pseudo-outcomes')]),
 'v12_gap4_delicatessen_estimation':('delicatessen/estimation.py',[(430,445,'Initial NaN validation'),(497,516,'Subset changes root solving but not full sandwich'),(614,654,'Solver,derivative and pseudoinverse options'),(664,755,'Shape,count,subset,normalization and final covariance'),(815,865,'Built-in success checks and custom callable contract')]),
 'v12_gap4_delicatessen_sandwich':('delicatessen/sandwich.py',[(18,59,'Standalone function and array contract'),(80,89,'Asymptotic covariance requires caller division'),(104,135,'One-parameter shape-dependent count and normalization'),(140,221,'Derivative dispatch and negative Jacobian'),(225,288,'Contribution outer product and pseudoinverse'),(292,326,'HC1 count and finite correction')]),
 'v12_gap3_delicatessen_license':('LICENSE',[(1,21,'MIT permission,notice and disclaimer')]),
 'exec24_delicatessen_meta_0':('setup.py',[(12,46,'Version loading,license,classifiers and NumPy/SciPy dependencies')]),
 'exec24_delicatessen_meta_1':('delicatessen/__init__.py',[(12,15,'Version and public estimator/covariance imports')]),
 'exec24_delicatessen_meta_2':('delicatessen/version.py',[(1,2,'Version4.3 declaration')])}

def prepare():
    assert not (BASE/'review.json').exists()
    tree=read(RAW/'v12_sw2_tree_delicatessen.json');assert tree['sha']==PIN and not tree['truncated']
    lookup={r['path']:r for r in tree['tree']};cutoff=read(RAW/'v12_sw2_cutoff_delicatessen.json')
    if isinstance(cutoff,list):cutoff=cutoff[0]
    assert cutoff['sha']==PIN and cutoff['commit']['committer']['date']<'2026-10-07T15:59:59Z'
    records=[]
    for key,(name,specs) in SPECS.items():
        p=RAW/(key+'.txt');raw=p.read_bytes();receipt=read(RAW/(key+'.receipt.json'))
        digest=hashlib.sha256(raw).hexdigest();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
        assert receipt['sha256']==digest and lookup[name]['sha']==blob and '/'+PIN+'/' in receipt['url']
        lines=raw.decode().splitlines();anchors=[]
        for lo,hi,finding in specs:
            assert 1<=lo<=hi<=len(lines),(name,hi,len(lines))
            anchors.append(dict(lines=[lo,hi],finding=finding,excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest()))
        records.append(dict(source_identity=receipt['url'],repository_path=name,git_blob=blob,
            version_date='4.3;11August2026;'+PIN,local_copy=ref(p,'Authenticated pinned original'),
            acquisition=ref(RAW/(key+'.receipt.json'),'Public acquisition receipt'),inspected_anchors=anchors,
            supported_claims=[a['finding'] for a in anchors],executed=False))
    assert len(records)==7 and '__version__ = "4.3"' in (RAW/'exec24_delicatessen_meta_2.txt').read_text()
    write(BASE/'identity-review.json',dict(status='pass_for_selected_pinned_sources',records=records,
        commit=PIN,date=cutoff['commit']['committer']['date'],version='4.3',
        evidence=[ref(RAW/'v12_sw2_tree_delicatessen.json','Pinned source tree'),ref(RAW/'v12_sw2_cutoff_delicatessen.json','Cutoff identity')],installed_release_equivalence=False))
    tree_ast=ast.parse((RAW/'v12_gap4_delicatessen_sandwich.txt').read_text())
    standalone=next(n for n in ast.walk(tree_ast) if isinstance(n,ast.FunctionDef) and n.name=='compute_sandwich')
    shape_branch=next(n for n in standalone.body if isinstance(n,ast.If) and ast.unparse(n.test)=='len(theta) == 1')
    assert ast.unparse(shape_branch.body[0].value)=='evald_theta.shape[0]'
    assert ast.unparse(shape_branch.orelse[0].value)=='evald_theta.shape[1]'
    estimation=ast.parse((RAW/'v12_gap4_delicatessen_estimation.txt').read_text())
    cls=next(n for n in estimation.body if isinstance(n,ast.ClassDef) and n.name=='MEstimator')
    solver=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='_solve_coefficients_')
    calls=[n for n in ast.walk(solver) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='method']
    assert len(calls)==1 and {k.arg for k in calls[0].keywords}=={'stacked_equations','init'}
    write(BASE/'control-flow-review.json',dict(status='pass_for_conditional_static_deductions',
        standalone_single_parameter_n='shape[0]',standalone_multi_parameter_n='shape[1]',
        custom_solver_keywords=['stacked_equations','init'],
        evidence=[ref(RAW/'v12_gap4_delicatessen_sandwich.txt','Original normalization'),ref(RAW/'v12_gap4_delicatessen_estimation.txt','Original solver'),ref(Path(__file__),'AST-only inspection')],native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_finite_and_population_witnesses',
        evidence=[ref(Path(exact.__file__),'Exact rational oracle'),ref(BASE/'exact-results.json','Reproduced results'),ref(BASE/'development.tex','Connected derivation')],
        findings=['Mean residual rejects0;root1.','Individual variance1/4 versus cluster-sum1/2;two clusters not calibration evidence.',
            'Standalone row normalization plus documented division gives1/16 versus1/4;conditional static deduction.',
            'Singular moment leaves coordinate2 unidentified despite projected zero variance.',
            'Population nuisance scores solved;clipping changes3/5 to27/80,bias-21/80.',
            'Stipulated bank net10000USD versus-16250USD;cost denominators20,24,30.'],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='selected_declarations_not_clearance',
        evidence=[ref(RAW/(k+'.txt'),'Original declaration') for k in ['v12_gap3_delicatessen_license','exec24_delicatessen_meta_0','exec24_delicatessen_meta_1','exec24_delicatessen_meta_2']],
        version='4.3',numpy='>=1.18.5',scipy='>=1.9.0',python_classifiers='3.8 through3.14;not enforced or tested',
        top_level_license='MIT',unresolved=['Installed release equality','Full numerical environment and dependencies','Transitive redistribution notices','Derivative/regression delegates'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',
        inputs=['Target,units,clock,causal assumptions and full equation stack','Canonical p-by-n contribution shape and independent-unit or cluster definition',
            'Nuisance source,subset,design matrices,link and clipping policy','Solver,actual limits,derivative settings,rank policy and complete environment'],
        outputs=['All coordinates and full scaled residuals','Equation and contribution counts,rank/condition and derivative diagnostics',
            'Asymptotic versus estimator covariance,normalization and finite correction','All failure states,request denominators and full costs'],
        refusals=['Unsupported identification or dependence law','Unverified root or held nuisance equations','Unidentified contrast despite pseudoinverse',
            'Ambiguous shape or covariance scaling','Invalid propensity domain or counterfactual coding','Unqualified derivative,environment or rights'],integration_allowed=False))
    next_action='Retain pinned Delicatessen4.3 source and rational witnesses as reference. Resolve full derivative/regression/environment/rights review; preregister root,subset,rank,vector-row normalization,HC1,cluster,clipping and full-cost native public fixtures. Do not repeat selected source inspection;no general causal or covariance admission.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,
        known_routes=['Locked isolated worker and exact shape/scaling fixtures','Scientific equation and sampling-law review','Known-law public coverage and refusal study','Transitive rights and numerical dependency review'],
        remaining=['Native package qualification','GMM and other estimating-equation families','Full derivative and regression internals','General nuisance-learning rates','Complete software coverage and acceptance'],
        unknown_without_information=['Hidden assignment or outcome truth','Unrestricted latent-state identification','Universal arbitrary-dependence uncertainty']))
    choice=dict(candidate='Delicatessen',canonical_candidate='pzivich/Delicatessen',selected_revision=PIN,selected_version='4.3',decision='reference',
        reason='Explicit estimating-equation reference with meaningful solver,rank,shape and sampling-law obligations;native qualification remains open.',
        alternatives=[dict(route='adopt',decision='defer',reason='No general causal or bank-service qualification'),
            dict(route='integrate',decision='conditional',reason='Narrow isolated worker after science,rights,environment and native fixtures'),
            dict(route='port',decision='defer',reason='No demonstrated benefit for assuming solver and covariance maintenance'),
            dict(route='reference',decision='retain',reason='Authenticated original source plus independent exact witnesses'),
            dict(route='reject',decision='restricted',reason='Reject automatic identification or arbitrary-dependence claims;retain scoped use')],
        owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Target,identification,equations,nuisance rates and units'),
            ('Adapter','Residuals,shape,rank,normalization and refusals'),('Rights/platform','Dependencies,distribution and resource contract'),
            ('Evaluation','Known-law public tasks,all failures and costs')]],
        costs=dict(prices='Unmeasured;4800USD authored illustration',categories=['scientific review','adapter','rights','environment','all solves and failures','evaluation','maintenance']),
        maintenance='Pinned contributor-maintained project;future support and service levels unverified',revisit_trigger=next_action,
        integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    source=dict(integrated_citation_key='exec24_delicatessen_source',kind='software_primary_sources',
        title='Delicatessen4.3 pinned estimating-equation,solver,sandwich and environment contracts',author='Paul Zivich and Delicatessen contributors',year=2026,
        source_identity='https://github.com/pzivich/Delicatessen/tree/'+PIN,version_date='4.3;11August2026;'+PIN,
        local_copy=ref(RAW/'v12_gap4_delicatessen_estimation.txt','Selected estimator original'),records=records,
        identity_evidence=[ref(BASE/'identity-review.json','Byte authentication')],inspected_anchors=[r['local_copy'] for r in records],
        supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
    authored=dict(integrated_citation_key='exec24_delicatessen_choice',kind='project_evidence_not_scholarly_paper',
        title='Authored Delicatessen root,rank,shape,cluster,clipping and reuse witnesses',author='Causal banking proposal project',year=2026,
        source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no native execution',
        local_copy=ref(BASE/'mathematical-review.json','Authored witnesses'),
        inspected_anchors=[ref(BASE/n,'Explicit reviewed choice') for n in ['choice.json','conversion-contract.json','omissions-register.json','control-flow-review.json']],
        supported_claims=['Exact root,rank,shape and dependence examples','Population clipping witness with solved nuisance scores','Conditional worker,owners,costs and limits'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,authored],new_records=2,new_scholarly_pdfs=0,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_reference_choice',evidence=[ref(BASE/n,'Reviewed plan') for n in ['plan.md','identity-review.json','choice.json','mathematical-review.json']],
        findings=['Root,rank and causal identification kept distinct.','Standalone shape issue and sampling-unit normalization derived explicitly.',
            'Clipping witness uses solved population nuisance scores;no native failure assertion.','Sources,public qualification routes,owners,costs and unknowns explicit.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_scoped_connected_argument',evidence=[ref(BASE/'development.tex','Technical argument'),ref(BASE/'sponsor-addition.md','Sponsor argument')],
        findings=['Notation,banking units and assumptions stated.','Static deductions and authored examples distinguished from native results.',
            'No new scholarly citation or invented paper.','Reference choice does not grant final acceptance.'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/n,'Reviewed candidate') for n in ['identity-review.json','source-audit.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','choice.json',
            'control-flow-review.json','exact-results.json','mathematical-review.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],
        findings=['Seven originals authenticate to pinned tree before cutoff.','Independent rational witnesses reproduce.','Reference-only disposition;no native or exhaustive coverage admission.'],
        limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated=len(records),decision='reference',new_records=2,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed decision') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Pinned source,version,license,environment and maintenance limits explicit.',
        'Targets,root/rank/shape/covariance contracts,alternatives,owners,costs and revisit trigger reviewed.',
        'Reference only;no native capability or general scientific qualification.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],
        limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result)
    print('Delicatessen reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
