#!/usr/bin/env python3
"""Pinned, reference-only statsmodels reuse decision; no native admission."""
import argparse, hashlib, json, tomllib
from pathlib import Path
import run_program_checkpoint_v3 as controller
import python_effect_reference_20261020 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/statsmodels-reuse-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-20/python-effects-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.DECISION.seed_076'
read=lambda p:json.loads(p.read_text())

def prepare():
    assert not (BASE/'review.json').exists()
    verify_bindings(read(PRIOR/'review.json'))
    source=next(x for x in read(PRIOR/'source-audit.json')['sources'] if x['integrated_citation_key']=='exec20_python_effect_source')
    path=RAW/'exec24_statsmodels_pyproject.txt';data=path.read_bytes();receipt=read(path.with_suffix('.receipt.json'));meta=tomllib.loads(data.decode())
    assert receipt['status']=='saved' and hashlib.sha256(data).hexdigest()==receipt['sha256']
    tree=read(RAW/'exec20_pyfx_statsmodels_tree.json');assert not tree['truncated']
    entries={x['path']:x for x in tree['tree']}
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==entries['pyproject.toml']['sha']
    assert 'setup.py' not in entries and read(RAW/'exec24_statsmodels_setup.receipt.json')['status']=='failed'
    lines=data.decode().splitlines()
    spans=[(1,9),(51,70),(72,136),(138,145)]
    audit=dict(integrated_citation_key='exec24_statsmodels_distribution',kind='software_primary_sources',
        title='statsmodels pinned build, runtime dependency and distribution declarations',author='statsmodels contributors',year=2026,
        source_identity=receipt['url'],version_date='Commit8278e2d218cc85bac2c7af02feb9a19a0e499b04 of6October2026; acquired24October2026 Asia/Shanghai',
        local_copy=ref(path,'Build/runtime/optional dependency declarations'),git_blob_sha1=blob,
        identity_evidence=[ref(path.with_suffix('.receipt.json'),'Acquisition hash/date'),ref(RAW/'exec20_pyfx_statsmodels_tree.json','Complete selected-commit tree')],
        inspected_anchors=[dict(anchor=f'lines{a}-{b}',lines=[a,b],text='\n'.join(lines[a-1:b])) for a,b in spans],
        supported_claims=['Selected commit uses mesonpy and dynamic version metadata; source identity is the commit, not an inferred release number.',
            'Build-time constraints and runtime constraints differ; a source build needs the declared Meson/Cython/NumPy/SciPy/setuptools_scm chain.',
            'Runtime dependencies include NumPy, SciPy, pandas, patsy, packaging and formulaic; Python>=3.10. Test/doc/dev/Polars extras are separate.',
            'BSD-3-Clause is declared; actual notices are separately inspected. No complete environment or transitive distribution clearance is granted.',
            'The pinned tree has pyproject.toml and meson.build but no setup.py; its404 is not package unavailability.'],
        limitations=['Static original metadata only; no dependency resolver, package build or downloaded tests executed.','Constraint ranges are not a solved lock or a maintenance/SLA guarantee.'])
    write(BASE/'source-audit.json',dict(sources=[audit],cutoff='2026-10-07',inherited_semantics=ref(PRIOR/'source-audit.json','Existing treatment/GMM source review'),native_execution=False))
    license_path=RAW/'v12_gap3_statsmodels_license.txt';license_text=license_path.read_text()
    assert all(x in license_text for x in ['Redistribution and use','Neither the name of statsmodels','AS IS'])
    write(BASE/'dependency-license-review.json',dict(status='inspected_for_reference_decision',
        evidence=[ref(BASE/'source-audit.json','Authenticated dependency metadata'),source['license']['evidence']],
        build_system=meta['build-system'],runtime_dependencies=meta['project']['dependencies'],requires_python=meta['project']['requires-python'],
        optional_dependencies=meta['project']['optional-dependencies'],dynamic_version=meta['project']['dynamic'],
        license_declaration=meta['project']['license'],license_observations=['Source redistribution retains notices, conditions and disclaimer.','Binary distribution reproduces notices/conditions/disclaimer in accompanying material.','No endorsement through project/contributor names without permission; warranty disclaimer retained.'],
        limitations=['Not a full distribution or transitive dependency rights clearance.','No supplied SLA or support price; named commit is a maintenance observation only.']))
    assert exact.calculate()==read(PRIOR/'exact-results.json')
    write(BASE/'exact-results.json',exact.calculate())
    choice=dict(operation=OP,status='proposed_reference_decision',decision='reference',name='statsmodels',
        selected_commit=source['selected_commit'],version='Commit-bound; dynamic distribution version not resolved here',canonical_aliases=['statsmodels.treatment.treatment_effects.TreatmentEffect','statsmodels.sandbox.regression.gmm'],
        target='Selected binary point-treatment ATE/ATT/ATU parametric comparison profiles with linear OLS outcome models and joint moments; not the whole statsmodels catalogue.',
        reason='Original Python engines are interpretable references already developed in the monograph. Preserve target and final covariance semantics rather than porting an entire statistical library without a demonstrated benefit.',
        source=source,distribution=ref(BASE/'source-audit.json','Pinned dependency declaration'),license=ref(BASE/'dependency-license-review.json','Direct terms and unresolved transitive rights'),
        uncertainty_contract=['Declare sampling law and final stacked-moment covariance. Preliminary HC0/HC1 outcome fits do not qualify final clustered or HAC uncertainty.',
            'Bind final moments, Jacobian, optimizer residual and rank. Scalar versus column centering differs when moment means are nonzero; this source finding is not an observed native failure.',
            'Keep sample keys and nuisance score rows aligned after grouping; distinguish target ATE/ATT/ATU and record propensity clipping.'],
        conversion_failure_contract=read(PRIOR/'conversion-contract.json'),
        native_trial_requirements=['Freeze exact wheel/source and resolved runtime/build environment; no implicit latest upgrade.',
            'Check target-population weights, propensity boundary cases, row permutations, singular design/rank and optimizer nonconvergence against exact authored references.',
            'Match supported covariance to the declared sampling law; refuse unsupported dependence rather than reuse a preliminary robust label.',
            'Record warnings/exceptions and unavailable uncertainty separately from point availability.'],
        alternatives=[dict(route='Pinned original Python worker',decision='preferred conditional prototype',reason='Preserves audited algorithms and ecosystem; qualify a narrow typed profile.'),
            dict(route='Whole-library R/Java/C++ port',decision='reject for current proposal',reason='Duplicates model, formula, numerical and uncertainty maintenance without measured benefit.'),
            dict(route='DoubleML or explicit estimating equations',decision='retain comparator',reason='Choose by target, nuisance-fitting and dependence assumptions; do not declare blanket superiority.'),
            dict(route='Project exact reference',decision='retain oracle',reason='Independent target/clipping/covariance arithmetic verifies semantics without running upstream code.')],
        costs=dict(prices='Not supplied; no ROI claim',categories=['Source and distribution review','Dependency locking and build maintenance','Data/clock/schema conversion','Nuisance fitting and GMM optimization','Full covariance and resampling','Failures, retries, storage and support'],comparison='Measure complete matched-target workflow after conformance.'),
        owners=[dict(role='Method owner',obligation='Approve target, assumptions and uncertainty regime'),dict(role='Integration maintainer',obligation='Own pinned environment, typed conversion, failures and upgrades'),dict(role='Rights reviewer',obligation='Resolve full distribution and transitive notices'),dict(role='Evaluation owner',obligation='Preregister matched tests and costs')],
        maintenance='Pinned6October2026 commit and repository metadata only; no inferred SLA or abandonment.',
        revisit_trigger='Named profile, resolved environment/rights, registered native semantic/failure comparison and matched total cost evidence.',
        integration_allowed=False,capabilities=[],limitations=source['limitations']+audit['limitations'])
    write(BASE/'choice.json',choice)
    write(BASE/'plan-review.json',dict(status='pass',steps=['Bind existing method/GMM semantics and new immutable dependency metadata.','Compare conditional original worker, port and reference alternatives.','Record only a proposal reference choice with native integration disallowed.','Integrate source-backed dependency and adoption discussion, preserve all earlier evidence and refresh counts.'],
        risks=['A dynamic version cannot be labeled as an unverified release.','Licensing metadata and installed historical evidence do not qualify this source commit.','A valid reference decision does not close software coverage or native trials.']))
    evidence=[ref(BASE/n,'Reviewed proposal decision') for n in ['source-audit.json','dependency-license-review.json','choice.json','plan-review.json','exact-results.json','development.tex','sponsor-addition.md']]+[ref(PRIOR/n,'Preserved method evidence') for n in ['review.json','conversion-contract.json','exact-results.json']]+[ref(Path(__file__),'Decision and receipt logic')]
    review=dict(status='pass_for_reference_only_decision',evidence=evidence,findings=['Pinned source and dependency metadata authenticated; direct license terms and transitive limits explicit.','Targets, final covariance, row alignment, clipping, failures, alternatives, costs, owners and triggers are explicit.','Reference-only; no native integration, full rights clearance or broad software acceptance.'],integration_allowed=False,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review)
    write(BASE/'mathematical-review.json',dict(status='pass',evidence=[ref(BASE/'exact-results.json','Replayed project-owned target/clipping/centering examples'),ref(PRIOR/'mathematical-review.json','Preserved derivations')],limitations=['No native execution or general sampling-law qualification.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected adoption discussion'),ref(BASE/'sponsor-addition.md','Sponsor scope')],findings=['No unverified release number, native admission or full rights claim.','Metadata, source analysis and authored exact references are separated.'],visual_acceptance=False))
    print('statsmodels reference decision prepared; no native integration')

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));g,merged,_=run.combined(ROOT,state);node=run.ledger.operation(g,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed proposal reference disposition; integration disallowed',evidence=[ref(BASE/'review.json','Author review')]);out=ROOT/node['outputs'][0];write(out,value)
    evidence=[ref(BASE/n,'Reviewed pinned reference choice') for n in ['review.json','choice.json','dependency-license-review.json']]
    findings=['Pinned source/alias, license, dependency and maintenance evidence bound.','Target/uncertainty, alternatives, costs, owners and revisit trigger explained.','Reference-only proposal decision; integration_allowed=false, capabilities empty and native qualification explicit.']
    r=run.ledger.receipt_template(node);r.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Reference-only choice')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=value['limitations'],capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r);print('Reference receipt ready')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
