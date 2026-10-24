#!/usr/bin/env python3
"""Bounded GCM source decision; downloaded code remains inert."""
import argparse,ast,hashlib,json
from pathlib import Path
import gcm_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/gcm-reuse-v1';RAW=ROOT/'docs/literature/raw'
PIN='b06369ed4a01a54c9d6422a24f103626fbcaec19';OP='SW.DECISION.seed_075'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected pinned GCM source;dynamic version placeholder is not a release version;installed equality unverified.',
 'Model,noise and sampling assumptions remain scientific inputs;prediction and non-rejection do not prove causal truth.',
 'Full dependency rights,native behavior,public calibration and deployment remain open.',
 'No downloaded code executed;all finite and population witnesses are authored.',
 'Reference only;no integration capability,visual,independent,bank or final acceptance.']
SPECS={
 'exec24_gcm_source_0':('dowhy/gcm/causal_models.py',[(29,93,'Model storage and untrained clone lifecycle'),(95,179,'Structural classes,assignment and fitted-parent validation')]),
 'exec24_gcm_source_1':('dowhy/gcm/whatif.py',[(27,103,'Intervention inputs,affected descendants and fresh conditional draws'),(105,190,'Noise provenance,abduction and scalar action shape checks'),(192,240,'ACE event and baseline contract'),(242,303,'Ancestor restriction,alternative/reference draws and class mapping')]),
 'exec24_gcm_source_2':('dowhy/gcm/fitting_sampling.py',[(20,75,'Per-node fitting and restricted optional evaluation'),(78,108,'Target missingness filtering and fitted-parent persistence'),(110,137,'Topological sampling and ordered columns')]),
 'exec24_gcm_source_3':('dowhy/gcm/causal_mechanisms.py',[(14,73,'Stochastic,functional and invertible interfaces'),(75,218,'Post-nonlinear and additive-noise fit/evaluation'),(267,352,'Categorical uniform-noise mechanism and class mapping')]),
 'exec24_gcm_source_5':('dowhy/gcm/confidence_intervals.py',[(14,46,'Geometric median and percentile-summary contract'),(75,127,'Seeded repetitions,per-key accumulation and coordinatewise quantiles')]),
 'exec24_gcm_source_6':('dowhy/gcm/falsify.py',[(105,181,'Local-Markov tests and effective tested denominators'),(428,516,'Evaluable,falsifiable and rejection states'),(518,681,'Node-permutation test,subset option and summary logic')]),
 'exec24_gcm_source_7':('dowhy/gcm/auto.py',[(184,232,'Supplied-graph mechanism classes and predictive criteria'),(280,388,'Missingness,override and per-node assignments'),(390,437,'Model classes and five-fold selection'),(489,570,'Shuffled folds,warning suppression,skipped folds and nonfinite scores')]),
 'exec24_gcm_source_8':('dowhy/gcm/_noise.py',[(19,65,'Noise/data propagation and explicit noninvertible abduction refusal')]),
 'exec24_gcm_source_9':('dowhy/gcm/confidence_intervals_cms.py',[(13,39,'Query partial application does not refit'),(42,99,'Clone,75percent without-replacement sampling,optional reassignment and refit')]),
 'exec24_gcm_source_10':('dowhy/graph.py',[(62,85,'Sorted parents,ancestor subgraph and graph validators')]),
 'exec13_dowhy_project':('pyproject.toml',[(1,62,'Dynamic version placeholder,MIT and build system'),(69,105,'Interpreter and numerical/dependency requirements')]),
 'exec13_dowhy_license':('LICENSE',[(1,21,'MIT grant,notice and disclaimer')])}

def prepare():
    assert not (BASE/'review.json').exists()
    tree=read(RAW/'exec24_gcm_tree.json');assert tree['sha']==PIN and not tree['truncated']
    lookup={x['path']:x for x in tree['tree']};cutoff=read(RAW/'exec13_dowhy_commit.json')[0]
    assert cutoff['sha']==PIN and cutoff['commit']['committer']['date']=='2026-10-04T00:05:51Z'
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
            version_date='Pinned4October2026;dynamic release version unresolved;'+PIN,
            local_copy=ref(p,'Authenticated original'),acquisition=ref(RAW/(key+'.receipt.json'),'Acquisition receipt'),
            inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
    assert len(records)==12 and 'dowhy/gcm/fcms.py' not in lookup
    write(BASE/'identity-review.json',dict(status='pass_for_selected_pinned_sources',records=records,
        commit=PIN,date=cutoff['commit']['committer']['date'],version='Pinned revision;release unresolved',
        evidence=[ref(RAW/'exec24_gcm_tree.json','Complete pinned tree'),ref(RAW/'exec13_dowhy_commit.json','Cutoff metadata'),
            ref(BASE/'acquisition-repair.json','Preserved nonexistent-path404 and tree correction'),ref(RAW/'exec24_gcm_source_4.receipt.json','Failed acquisition preserved')],
        installed_release_equivalence=False))
    helper=ast.parse((RAW/'exec24_gcm_source_9.txt').read_text())
    alias=next(n for n in helper.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='bootstrap_sampling' for t in n.targets))
    assert ast.unparse(alias.value)=='partial'
    choices=[n for n in ast.walk(helper) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='choice']
    assert len(choices)==1 and any(k.arg=='replace' and isinstance(k.value,ast.Constant) and k.value.value is False for k in choices[0].keywords)
    summaries=ast.parse((RAW/'exec24_gcm_source_5.txt').read_text())
    ci=next(n for n in summaries.body if isinstance(n,ast.FunctionDef) and n.name=='confidence_intervals')
    assert any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='setdefault' for n in ast.walk(ci))
    write(BASE/'control-flow-review.json',dict(status='pass_for_bounded_static_deductions',
        bootstrap_sampling='partial_only',refit_replace=False,dict_summary='Per-key append then column stacking;replicate identity not locally validated',
        evidence=[ref(RAW/'exec24_gcm_source_9.txt','Query/refit helper'),ref(RAW/'exec24_gcm_source_5.txt','Summary helper'),ref(Path(__file__),'AST-only checks')],native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_structural_and_finite_witnesses',
        evidence=[ref(Path(exact.__file__),'Independent rational oracle'),ref(BASE/'exact-results.json','Exact results'),ref(BASE/'development.tex','Connected derivation')],
        findings=['Supplied Y=2A+N gives individual untreated3 versus stipulated population mean0.',
            'Two cross-world couplings have identical intervention marginals and effects but conditional answers0versus1.',
            'Size3without-replacement empirical mean variance1/9 versus size4ordinary bootstrap1/4.',
            'Equal per-key counts can contain disjoint replicate IDs.',
            'Event complement reverses1/5 sign;stipulated extra loss20000USD;cost denominators20,24,30.'],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='selected_declarations_not_clearance',
        evidence=[ref(RAW/'exec13_dowhy_project.txt','Pinned project declarations'),ref(RAW/'exec13_dowhy_license.txt','MIT original')],
        version='Dynamic;0.0.0 is placeholder',python='>=3.9,<3.14',numpy='>2.0',scipy='>=1.10or>=1.15byPython',
        networkx='>=3.3or>=2.8.5byPython',top_level_license='MIT',
        unresolved=['Installed distribution equality','Full numerical and optional dependency lock','Transitive rights and notices','Predictor and independence-test internals','Resource/RNG/platform qualification'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',
        inputs=['Reviewed DAG,node units,clock,mechanisms,invariance and noise law','Fitted parent order and node-specific missingness masks',
            'Typed action grammar and population-versus-individual target','Positive event,noise provenance,seeds,split and resampling law'],
        outputs=['Named target and action semantics','Fitted-versus-untrained model state and parent checks','All raw repetitions with fixed keys and IDs',
            'MonteCarlo,sampling,selection,graph and model-uncertainty scope','Evaluable,falsifiable,rejected and refused states separately','All-request costs'],
        refusals=['Unsupported causal/noise assumptions','Noninvertible abduction without justified noise','Unqualified dependence or shuffled split',
            'Ambiguous positive class or intervention scope','Changing output schemas or nonfinite selection','Unresolved worker rights/environment'],integration_allowed=False))
    next_action='Retain pinned GCM sources as reference distinct from DoWhy identification. Inspect authentic GCM/falsification original papers and predictor/test dependencies; preregister parent,missingness,event,action,abduction,cross-world,subsampling,schema/RNG and all-cost native public fixtures. No general causal or interval capability admission;do not repeat this selected source review.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,
        known_routes=['Authentic original-paper and delegate review','Locked worker and complete rights assessment','Independent known-law structural/refusal fixtures',
            'Separate simulation,sampling,selection,graph and misspecification uncertainty designs'],
        remaining=['Original GCM and graph-falsification scholarly justifications not newly inspected','Other anomaly,attribution and distribution-change paths',
            'Full native calibration,dependencies and service costs','Mandatory survey completeness and final acceptance'],
        unknown_without_information=['True bank graph and hidden assignment','Individual cross-world coupling from marginal intervention laws alone','Universal arbitrary-dependence uncertainty']))
    choice=dict(candidate='DoWhy GCM',canonical_candidate='py-why/dowhy:gcm',alias_boundary='Submodule of DoWhy;separate from inherited identification approval and PyWhy umbrella',
        selected_revision=PIN,selected_version='Pinned4October2026;dynamic release unresolved',decision='reference',
        reason='Useful explicit mechanism and query reference;scientific,uncertainty and full-worker qualification remains open.',
        alternatives=[dict(route='adopt',decision='defer',reason='All GCM paths and bank assumptions unqualified'),
            dict(route='integrate',decision='conditional',reason='Narrow isolated worker after science,rights,environment and native fixtures'),
            dict(route='port',decision='defer',reason='No measured advantage for assuming mechanism,abduction and uncertainty maintenance'),
            dict(route='reference',decision='retain',reason='Pinned originals and independent structural/uncertainty witnesses'),
            dict(route='reject',decision='restricted',reason='Reject invented individual noise and automatic graph truth;retain bounded candidates')],
        owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Graph,target,invariance,noise and sampling law'),
            ('Adapter','Parent identity,actions,event coding,noise provenance,replicate schemas and refusal'),
            ('Rights/platform','Pinned distributions,notices,resources and support'),('Evaluation','Known-law tasks,all failures and full costs')]],
        costs=dict(prices='Unmeasured;5400USD authored illustration',categories=['scientific review','adapter','rights','environment','all fits and queries','validation','maintenance']),
        maintenance='Pinned community source;future response and supported-service levels unverified',revisit_trigger=next_action,
        integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    source=dict(integrated_citation_key='exec24_gcm_source',kind='software_primary_sources',
        title='DoWhy GCM pinned mechanism,intervention,counterfactual and uncertainty contracts',author='PyWhy contributors',year=2026,
        source_identity='https://github.com/py-why/dowhy/tree/'+PIN+'/dowhy/gcm',version_date='4October2026;'+PIN,
        local_copy=ref(RAW/'exec24_gcm_source_1.txt','Selected query original'),records=records,
        identity_evidence=[ref(BASE/'identity-review.json','Cutoff and byte authentication')],inspected_anchors=[r['local_copy'] for r in records],
        supported_claims=[a for r in records for a in r['supported_claims']],limitations=LIMITS)
    authored=dict(integrated_citation_key='exec24_gcm_choice',kind='project_evidence_not_scholarly_paper',
        title='Authored GCM structural,cross-world,subsampling,schema and reuse witnesses',author='Causal banking proposal project',year=2026,
        source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no native execution',
        local_copy=ref(BASE/'mathematical-review.json','Authored exact witnesses'),
        inspected_anchors=[ref(BASE/n,'Bounded choice') for n in ['choice.json','conversion-contract.json','control-flow-review.json','omissions-register.json']],
        supported_claims=['Independent structural and cross-world examples','Different finite resampling laws and output alignment','Bounded worker,owners,costs and unresolved routes'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,authored],new_records=2,new_scholarly_pdfs=0,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_reference_choice',
        evidence=[ref(BASE/n,'Reviewed plan') for n in ['plan.md','identity-review.json','choice.json','mathematical-review.json']],
        findings=['Separate GCM from inherited DoWhy identification.','Separate population interventions,abduction and cross-world information.',
            'Separate simulation,subsampling,graph and model uncertainty.','No uninspected paper cited as technical proof;original-paper followup explicit.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',
        evidence=[ref(BASE/'development.tex','Technical manuscript'),ref(BASE/'sponsor-addition.md','Sponsor summary')],
        findings=['Notation,banking signs and model assumptions explained.','Conditional static observations distinguished from native measurements.',
            'Alternatives,owner roles,all-cost denominators and unknowns explicit.'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/n,'Reviewed decision') for n in ['identity-review.json','source-audit.json','dependency-license-review.json','conversion-contract.json',
            'omissions-register.json','choice.json','control-flow-review.json','exact-results.json','mathematical-review.json','plan-review-v2.json',
            'copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],
        findings=['Twelve selected originals authenticate to pinned cutoff tree.','Finite authored witnesses reproduce.','Reference choice grants no native or causal capability.'],
        limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated=len(records),decision='reference',new_records=2,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed GCM proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed decision') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Source identity,alias boundary,version,license,dependencies and maintenance limits explicit.',
        'Mechanisms,query and uncertainty semantics,alternatives,owners,costs and revisit conditions reviewed.',
        'Reference only;integration false and no native or scientific capability admission.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],
        limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result)
    print('GCM reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
