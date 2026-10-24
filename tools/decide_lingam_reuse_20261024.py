#!/usr/bin/env python3
"""Inspect pinned LiNGAM originals as inert text; admit no native capability."""
import argparse,ast,hashlib,json
from pathlib import Path
import lingam_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/lingam-reuse-v1'
RAW=ROOT/'docs/literature/raw';PIN='0f089670dbb2a470c3ef43bc0f34ef823ae59a0a'
OP='SW.DECISION.seed_072';read=lambda p:json.loads(p.read_text())
LIMITS=['Selected pinned1.13.0 repository source;installed wheel equality unverified.',
 'Original2006 model assumptions are inherited;not a proof of current DirectLiNGAM options or all families.',
 'Top-level MIT inspected;complete dependency,binary and platform rights remain open.',
 'No downloaded package or upstream tests executed;all finite examples are authored.',
 'Static edge cases and bootstrap summaries do not establish native failure,coverage or causal truth.',
 'Reference-only decision;integration false;visual,independent,bank and final acceptance open.']
SPECS={
 'v12_gap3_lingam_technical':('lingam/direct_lingam.py',[(25,64,'Constructor,prior,measure and pruning options'),
   (66,123,'Ordering,residualization and dispatch'),(125,158,'Partial-order and residual helper'),
   (160,248,'Entropy,prior candidate selection and variance normalization'),(249,281,'Optional GPU import and route')]),
 'v12_gap4_lingam_base':('lingam/base.py',[(23,33,'Stored RNG setting'),(51,91,'Parent-adjusted regression;warning does not prevent result'),
   (93,121,'Residual HSIC diagnostic'),(123,167,'Target-row predictor-column adjacency and pruning/refit dispatch')]),
 'v12_gap4_lingam_bootstrap':('lingam/bootstrap.py',[(17,65,'Row resampling,fitted-object mutation,indices and matrix-path total effects'),
   (278,310,'Threshold frequency and nonfinite conversion'),(312,370,'Threshold frequency versus nonzero-effect median')]),
 'v12_gap4_lingam_var':('lingam/var_lingam.py',[(67,114,'VAR fitting and residual DirectLiNGAM'),
   (132,195,'Criterion disabled,residual resampling,sequence reconstruction and normal-path restoration'),
   (314,366,'Lag-model selection without trend and structural lag coefficient conversion')]),
 'v12_exec13_pydisc_lingam_extra_1':('lingam/utils/__init__.py',[(109,158,'Path-prior matrix orientation'),
   (756,794,'Standardized BIC selection and original-unit refit'),(797,872,'Directed paths and nonfinite conversion'),
   (1084,1156,'Matrix path-product total effects and continuity gates')]),
 'v12_gap3_lingam_license':('LICENSE',[(1,21,'MIT terms and retained copyright notice')]),
 'exec24_lingam_meta_0':('pyproject.toml',[(1,49,'Build,Python,dependencies,license and dynamic version source')]),
 'exec24_lingam_meta_1':('requirements.txt',[(1,14,'Version compatibility comments and optional GPU dependency')]),
 'exec24_lingam_meta_2':('lingam/__init__.py',[(1,64,'Broad imports and version1.13.0')])}

def prepare():
    assert not (BASE/'review.json').exists()
    tree=read(RAW/'v12_sw2_tree_lingam.json');assert tree['sha']==PIN and not tree['truncated']
    lookup={r['path']:r for r in tree['tree']};cutoff=read(RAW/'v12_sw2_cutoff_lingam.json')
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
            version_date='1.13.0;8September2026;'+PIN,local_copy=ref(p,'Authenticated pinned original'),
            acquisition=ref(RAW/(key+'.receipt.json'),'Public acquisition receipt'),inspected_anchors=anchors,
            supported_claims=[a['finding'] for a in anchors],executed=False))
    assert len(records)==9 and '__version__ = "1.13.0"' in (RAW/'exec24_lingam_meta_2.txt').read_text()
    write(BASE/'identity-review.json',dict(status='pass_for_selected_pinned_sources',records=records,
        commit=PIN,date=cutoff['commit']['committer']['date'],version='1.13.0',
        evidence=[ref(RAW/'v12_sw2_tree_lingam.json','Complete selected source tree'),
            ref(RAW/'v12_sw2_cutoff_lingam.json','Cutoff identity metadata'),ref(BASE/'metadata-authentication.json','New metadata matched')],
        installed_release_equivalence=False))
    tree_boot=ast.parse((RAW/'v12_gap4_lingam_bootstrap.txt').read_text())
    bootstrap=next(n for n in ast.walk(tree_boot) if isinstance(n,ast.FunctionDef) and n.name=='bootstrap')
    resampling=[n for n in ast.walk(bootstrap) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='resample']
    assert len(resampling)==1 and not any(k.arg=='random_state' for k in resampling[0].keywords)
    tree_var=ast.parse((RAW/'v12_gap4_lingam_var.txt').read_text())
    var_boot=next(n for n in ast.walk(tree_var) if isinstance(n,ast.FunctionDef) and n.name=='bootstrap')
    assert not any(isinstance(n,ast.Try) and n.finalbody for n in ast.walk(var_boot))
    write(BASE/'control-flow-review.json',dict(status='pass_for_bounded_static_observation',
        generic_resample_explicit_random_state=False,var_bootstrap_finally_restoration=False,
        evidence=[ref(RAW/'v12_gap4_lingam_bootstrap.txt','Selected bootstrap'),ref(RAW/'v12_gap4_lingam_var.txt','Selected VAR'),ref(Path(__file__),'AST-only checks')],
        qualification='No native failure or global RNG behavior inferred;worker must qualify repeatability and cleanup'))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_finite_examples',
        evidence=[ref(Path(exact.__file__),'Exact Fraction reference'),ref(BASE/'exact-results.json','Reproducible results'),ref(BASE/'development.tex','Connected argument')],
        findings=['Nilpotent three-variable B gives direct-1,indirect6,total5;stipulated impulse gives1000USD gross and200net.',
            'Replicates0,.1,.9 threshold.5 give frequency1/3 and nonzero median1/2,not threshold median9/10.',
            'Independent versus shared unit-variance shocks give mean variance1/4 versus1.',
            '4200USD/210,175,140 gives20,24,30.'],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='selected_declarations_inspected_not_clearance',
        evidence=[ref(RAW/(k+'.txt'),'Original declaration') for k in ['v12_gap3_lingam_license','exec24_lingam_meta_0','exec24_lingam_meta_1','exec24_lingam_meta_2']],
        python='>=3.10',scipy='<=1.13.1',scikit_learn='>=1.6',top_level_license='MIT',
        unresolved=['Complete runtime and optional GPU dependency lock','Transitive rights and binary notices','Installed-wheel equality',
            'Initializer import coverage','Memory,solver,RNG and platform qualification'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',
        inputs=['Variables,units,clock and scientific linear/non-Gaussian/acyclic/sufficiency assumptions',
            'Node order,path priors,hard/soft mode,whitelisted measure and pruning',
            'Data/preprocessing,requested effect construction,resampling law,RNG and limits'],
        outputs=['B[target,predictor],node mapping,selected causal order and coefficient units',
            'Matrix-path effect separately from parent-adjusted regression','Threshold frequency and conditional-median denominator',
            'All original and replicate statuses,nonfinite matrices,settings before/after failure,complete costs'],
        refusals=['Unsupported model assumptions,ambiguous orientation or path prior',
            'Unqualified constants,nonfinite normalization or unknown option','Invalid dependent-data resampling',
            'Unresolved environment,termination or scale'],integration_allowed=False))
    next_action='Retain pinned LiNGAM1.13.0 source as reference. Resolve full environment/rights; preregister orientation,path-prior,pruning,constant-column,threshold/median,RNG,dependent-resampling,VAR-cleanup and full-cost native fixtures. Inspect other latent/nonlinear/temporal families separately; do not repeat selected source review.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,
        known_routes=['Typed schema and orientation round trips','Locked worker and full dependency review',
            'Public known-law scientific and adverse-state fixtures','Per-family method and original-paper review'],
        remaining=['Current DirectLiNGAM original proof review','HSIC,numerical and optional GPU dependency internals',
            'Other algorithm families and exhaustive market coverage','Native calibration,full costs and independent acceptance'],
        unknown_without_information=['True hidden banking graph','Unrestricted latent/feedback identification','Universal dependent-data calibration']))
    choice=dict(candidate='LiNGAM',canonical_candidate='cdt15/lingam',selected_revision=PIN,selected_version='1.13.0',decision='reference',
        reason='Useful selected source and matrix/summary reference;scientific and full-worker qualification remains open.',
        alternatives=[dict(route='adopt',decision='defer',reason='No general bank-service qualification'),
            dict(route='integrate',decision='conditional',reason='Isolated narrow worker after model,environment,rights and fixtures'),
            dict(route='port',decision='defer',reason='No measured benefit for graph/pruning/solver/RNG maintenance transfer'),
            dict(route='reference',decision='retain',reason='Authenticated source and independent rational conversion oracle'),
            dict(route='reject',decision='restricted',reason='Reject unsupported causal-certainty or all-family claims;retain scoped candidates')],
        owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Assumptions,graph and causal target'),
            ('Adapter','Orientation,path priors,effect methods,summary denominators and refusal'),
            ('Rights/platform','Distribution,dependencies,resources and support'),('Evaluation','Known-law tasks,all failures and full costs')]],
        costs=dict(prices='Unmeasured;4200USD authored illustration',categories=['engineering','rights/scientific review','environment',
            'all fits and bootstrap failures','validation','storage','maintenance']),
        maintenance='Named upstream contributors and pinned revision;future support and service levels unverified',
        revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    inherited=read(ROOT/'docs/program/execution/2026-10-24/ananke-reuse-reader-v1/reader/source-audit.json')
    paper=next(s for s in inherited['sources'] if s['integrated_citation_key']=='exec13_pydisc_shimizu2006');verify_bindings(paper)
    source=dict(integrated_citation_key='exec24_lingam_source',kind='software_primary_sources',
        title='LiNGAM1.13.0 pinned ordering,pruning,bootstrap and environment contracts',author='LiNGAM contributors',year=2026,
        source_identity='https://github.com/cdt15/lingam/tree/'+PIN,version_date='1.13.0;8September2026;'+PIN,
        local_copy=ref(RAW/'v12_gap3_lingam_technical.txt','Selected DirectLiNGAM source'),records=records,
        identity_evidence=[ref(BASE/'identity-review.json','Cutoff and byte authentication')],
        inspected_anchors=[r['local_copy'] for r in records],supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
    authored=dict(integrated_citation_key='exec24_lingam_choice',kind='project_evidence_not_scholarly_paper',
        title='Authored LiNGAM matrix,bootstrap-summary,dependence and reuse examples',author='Causal banking proposal project',year=2026,
        source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no package execution',
        local_copy=ref(BASE/'mathematical-review.json','Authored finite references'),
        inspected_anchors=[ref(BASE/n,'Explicit reference choice') for n in ['choice.json','conversion-contract.json','omissions-register.json','control-flow-review.json']],
        supported_claims=['Exact matrix and summary semantics','Conditional worker,owners,costs and limits','No universal causal or uncertainty guarantee'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,authored,paper],new_records=2,new_scholarly_pdfs=0,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_reference_choice',evidence=[ref(BASE/n,'Reviewed plan') for n in ['plan.md','choice.json','identity-review.json','mathematical-review.json']],
        findings=['Separate original ICA-model assumptions from current DirectLiNGAM implementation','Separate path totals,regression effects,threshold frequency and conditional median',
            'Record dependencies,per-family limits and known public qualification routes','No native or exhaustive coverage admission']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_scoped_connected_argument',evidence=[ref(BASE/'development.tex','Manuscript'),ref(BASE/'sponsor-addition.md','Sponsor argument')],
        findings=['Banking units and assumptions explained','Authored illustrations and static observations separated from native evidence',
            'Alternatives,owners,costs and unknowns explicit'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/n,'Reviewed candidate') for n in ['identity-review.json','source-audit.json','dependency-license-review.json','conversion-contract.json',
            'omissions-register.json','choice.json','control-flow-review.json','exact-results.json','mathematical-review.json',
            'plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],
        findings=['Nine selected sources authenticate to pinned cutoff tree','Finite authored references reproduce','Reference choice grants no native capability'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated=len(records),decision='reference',new_records=2,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value);evidence=[ref(BASE/n,'Reviewed decision') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Pinned identity,version,license,dependencies and maintenance limits explicit.',
        'Scientific assumptions,conversion,alternatives,owners,costs and revisit trigger reviewed.',
        'Reference only;no integration or native capability admission.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],
        limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result)
    print('LiNGAM reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
