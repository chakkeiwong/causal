#!/usr/bin/env python3
"""Audit pinned PyMC contracts without executing downloaded package code."""
import argparse
import hashlib
import json
import tomllib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pymc_reference_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
core = run.core
ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-23/pymc-reuse-v1'
RAW = ROOT / 'docs/literature/raw'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Twelve selected immutable source/doc/test files and authored exact calculations only; no upstream package or test executed.',
    'The selected development revision has a dynamically resolved version; no named release or whole-project exhaustive review is asserted.',
    'Model transformation and posterior computation do not establish causal identification, scientific truth or calibrated bank-policy uncertainty.',
    'Complete dependency custody/rights, native conformance, scientific qualification and visual/final acceptance remain open.',
]
SPANS = {
    'LICENSE': [([1,202], 'Pinned root Apache-2.0 terms; transitive dependency rights remain separate.')],
    'pyproject.toml': [([1,51], 'Dynamic version, Python/PyTensor ranges, direct and optional dependencies and root license metadata.'),
                       ([65,71], 'Versioneer derives the version from Git; no verified release label supplied here.')],
    'pymc/__init__.py': [([15,72], 'Root imports and version loading; importing this downloaded code is outside this review.')],
    'pymc/model/transform/conditioning.py': [
        ([46,122], 'observe converts supported variables with compatible type/shape in a distinct cloned model.'),
        ([125,230], 'do replaces named variables, shares constants by default, handles RV-dependent and self-referencing expressions, and optionally prunes.')],
    'pymc/model/transform/basic.py': [([33,66], 'Pruning retains ancestors of observed variables and refuses models containing Potentials.')],
    'pymc/model/fgraph.py': [
        ([162,176], 'Nondefault initial values and nested submodels are rejected; old GP objects receive a warning.'),
        ([218,240], 'Shared RNG/data/dimension variables are copied with model coordinate information.'),
        ([244,298], 'Model roles are encoded into a reconstructible function graph; this is a software conversion, not causal validation.')],
    'pymc/sampling/forward.py': [
        ([548,553], 'Prior predictive sampling warns about direct Potential effects.'),
        ([644,734], 'Name/shape/coordinate matching, output selection, regeneration, freezing and predictive grouping contracts.'),
        ([804,822], 'A changed deterministic expression can reuse its stored value unless explicitly regenerated.'),
        ([955,997], 'Trace RVs can stop regeneration cascades; explicit freeze suppresses the corresponding warning.'),
        ([1096,1102], 'Posterior predictive sampling warns about direct Potential effects; trace ancestors can still encode posterior consequences.'),
        ([1134,1223], 'Validate sample/freeze variables, auto-freeze trace RVs and select compiled versus copied outputs.'),
        ([1225,1252], 'Compilation and copying remain distinct paths; no native behavior was observed here.')],
    'pymc/sampling/mcmc.py': [
        ([668,748], 'Chain, RNG, backend and trace persistence documentation; stored draws alone do not prove resumable chain state.'),
        ([946,1008], 'Conditional default nutpie dispatch, external sampler restrictions and rejection of custom trace/callback paths.')],
    'pymc/stats/convergence.py': [
        ([64,132], 'Missing posterior, insufficient draws/chains, Rhat above 1.01 and ESS per chain below 100 have separate warnings.'),
        ([135,184], 'Missing divergence/treedepth statistics return no corresponding warning; no-warning is not proof of checks passed.')],
    'pymc/step_methods/hmc/nuts.py': [
        ([43,99], 'NUTS role, trajectory/energy diagnostics and CPU versus wall time documentation.'),
        ([132,196], 'Adaptation and trajectory depth settings; numerical diagnostics do not establish causal correctness.')],
    'tests/model/transform/test_conditioning.py': [
        ([139,308], 'Intended intervention, self-reference and dimensional behavior in upstream tests, not executed here.'),
        ([309,326], 'Constant-intervention posterior-predictive variant is marked xfail; this is a qualification lead, not a reproduced failure.')],
    'README.rst': [([70,113], 'Upstream supplied-model observe/do example; printed output is not a project observation.')],
}
FINDINGS = [
    'Conditioning, intervention and predictive regeneration are different experiments; graph transformation does not certify a causal graph.',
    'Trace matching, freeze/sample choices and changed deterministic expressions require explicit model and prediction identities.',
    'Potential factors are not generative rules; posterior ancestors can already encode their effects, so the forward limitation is kept narrow.',
    'Sampler dispatch, trace persistence and missing versus adverse diagnostics are preserved rather than collapsed into API success.',
    'Reference-only disposition has concrete native prerequisites, alternatives, measured-cost questions and owner obligations.',
]


def audit():
    assert not (BASE / 'source-audit.json').exists()
    sel = read(BASE / 'source-selection.json')
    commit = read(RAW / 'exec23_pymc_cutoff.json')[0]
    tree = read(RAW / 'exec23_pymc_tree.json')
    assert sel['commit'] == commit['sha'] == '2394fd441ae5f79597dc6012bd771e2ea28b01a6'
    assert tree['sha'] == sel['tree'] == commit['commit']['tree']['sha'] and not tree['truncated']
    assert sel['date'] == commit['commit']['committer']['date'] == '2026-10-07T15:02:58Z'
    assert datetime.fromisoformat(sel['date'].replace('Z', '+00:00')).astimezone(ZoneInfo('Asia/Shanghai')).date().isoformat() <= '2026-10-07'
    entries = {e['path']: e for e in tree['tree']}
    records = []
    for e in sel['selected']:
        p = RAW / (e['id'] + '.txt')
        data = p.read_bytes()
        receipt = read(RAW / (e['id'] + '.receipt.json'))
        path = e['path']
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        url = 'https://raw.githubusercontent.com/pymc-devs/pymc/' + sel['commit'] + '/' + path
        assert blob == e['blob'] == entries[path]['sha']
        assert len(data) == e['size'] == entries[path]['size']
        assert receipt['sha256'] == core.sha(p) and receipt['url'] == url
        assert all(1 <= a <= b <= len(data.decode().splitlines()) for (a,b),_ in SPANS[path]), path
        records.append(dict(upstream_path=path, source_identity=url, version_date=sel['date'],
            local_copy=ref(p, 'Inspected pinned primary text'), receipt=ref(RAW / (e['id'] + '.receipt.json'), 'Acquisition custody'),
            git_blob_sha1=blob, inspected_anchors=[dict(lines=span, finding=c) for span,c in SPANS[path]],
            supported_claims=[c for _,c in SPANS[path]], executed=False))
    assert len(records) == 12 and exact.calculate() == read(BASE / 'exact-results.json')
    metadata = tomllib.loads((RAW / 'exec23_pymc_01.txt').read_text())['project']
    assert metadata['dynamic'] == ['version'] and metadata['requires-python'] == '>=3.12,<3.15'
    assert metadata['license'] == 'Apache-2.0' and 'pytensor>=3.2.2,<3.4' in metadata['dependencies']
    identity = dict(repository='pymc-devs/pymc', package='pymc', version=None,
        version_status='Dynamically derived version; no release label verified', commit=sel['commit'], tree=sel['tree'],
        date=sel['date'], source_blobs=12, python=metadata['requires-python'],
        direct_dependencies=metadata['dependencies'], optional_dependencies=metadata['optional-dependencies'],
        evidence=[ref(RAW / 'exec23_pymc_cutoff.json', 'Cutoff revision'), ref(RAW / 'exec23_pymc_tree.json', 'Canonical tree')],
        maintenance='Inspected repository revision and metadata only; no support, service-level or complete release-history assertion.')
    write(BASE / 'identity.json', identity)
    write(BASE / 'static-contract-check.json', dict(native_execution=False, findings=FINDINGS,
        evidence=[ref(Path(exact.__file__), 'Independent calculations and text assertions')],
        limits=['Upstream tests are inspected intentions, including xfail; no package behavior or performance was observed.']))
    source = dict(integrated_citation_key='exec23_pymc_sources', kind='software_primary_sources',
        title='PyMC pinned model-transformation, forward-sampling and diagnostic contracts',
        author='PyMC Developers', year=2026,
        source_identity='https://github.com/pymc-devs/pymc/tree/' + sel['commit'],
        version_date='Development revision ' + sel['commit'] + '; ' + sel['date'],
        local_copy=records[3]['local_copy'], identity=identity, records=records,
        inspected_anchors=[dict(path=r['upstream_path'], anchors=r['inspected_anchors']) for r in records],
        supported_claims=[c for spans in SPANS.values() for _,c in spans],
        license_text=ref(RAW / 'exec23_pymc_00.txt', 'Pinned root Apache-2.0 license'), limitations=LIMITS)
    project = dict(integrated_citation_key='exec23_pymc_reference', kind='project_derivation_and_exact_reference',
        title='Exact conditioning, intervention, conjugate-posterior and predictive witnesses',
        author='Causal banking proposal project', year=2026,
        source_identity='tools/pymc_reference_20261023.py', version_date='23 October 2026; independently authored finite arithmetic',
        local_copy=ref(Path(exact.__file__), 'calculate'), inspected_anchors=['calculate'],
        supported_claims=[
            'Specified confounded law has conditional means 1 and 5, association 4 and intervention effect 2; stipulated nets are 150 and -50.',
            'Two observationally equivalent structural models have effects 1 and 0; equal likelihoods leave prior model odds unchanged.',
            'Uniform beta prior and six successes/four failures give beta(7,5), mean 7/12 and variance 35/1872.',
            'Trace freezing and regeneration target different experiments; replacing square by cube changes illustrative means 5/2 to 9/2.',
            'A hard-positive density factor yields weighted probability 1 versus unconstrained generator probability 1/2; posterior ancestors can still reflect the factor.',
            'Conditional posterior computation, causal identification and sampling-law calibration are separate proposal arguments, not package qualification.'], limitations=LIMITS)
    write(BASE / 'source-audit.json', dict(sources=[source, project], cutoff='2026-10-07', native_execution=False))
    write(BASE / 'omissions-register.json', dict(items=[
        dict(gap='Verified release and complete dependency/rights custody', next_action='Choose a release or commit, bind Python/PyTensor/compiler/sampler and all dependency artifacts and notices.'),
        dict(gap='Native transformations and predictions', next_action='Register exact-oracle tests for do/observe, self-reference, cloning, initial values, shared/constant interventions, dimensions, changed expressions, freeze/sample and Potentials; inspect actual warnings and xfail behavior.'),
        dict(gap='Numerical diagnostics, cost and recovery', next_action='Measure effective samples, compilation, CPU/wall time, memory and prediction cost; distinguish missing from adverse diagnostics; test persistence/restart per selected backend.'),
        dict(gap='Causal and policy qualification', next_action='Justify assignment/latent model and interventions, sensitivity/model comparison and the evaluation law for model/policy selection uncertainty.')], limitations=LIMITS))
    write(BASE / 'plan-review.json', dict(status='pass_for_reference_disposition',
        evidence=[ref(BASE / n, 'Reviewed argument') for n in ['plan.md', 'exact-results.json', 'static-contract-check.json', 'development.tex']],
        findings=FINDINGS, native_execution=False))
    evidence = [ref(BASE / n, 'Reviewed primary-source or authored evidence') for n in [
        'source-audit.json', 'identity.json', 'static-contract-check.json', 'exact-results.json', 'omissions-register.json', 'plan-review.json', 'development.tex']]
    evidence += [ref(Path(__file__), 'Source-audit logic'), ref(Path(exact.__file__), 'Authored examples')]
    review = dict(status='pass_for_reference_disposition', reviewer=REVIEWER, evidence=evidence,
        findings=FINDINGS, limitations=LIMITS, native_execution=False)
    verify_bindings(review)
    write(BASE / 'review.json', review)
    print(json.dumps(dict(source_blobs=12, source_records=2, decision='reference', native_execution=False)))


def receipt():
    op = 'SW.DECISION.inherited_pymc'
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == op
    verify_bindings(read(BASE / 'review.json'))
    evidence = [ref(BASE / n, 'Reviewed PyMC reference disposition') for n in [
        'source-audit.json', 'identity.json', 'review.json', 'plan-review.json', 'exact-results.json',
        'static-contract-check.json', 'omissions-register.json', 'development.tex']]
    evidence += [ref(Path(__file__), 'Receipt construction')]
    output = ROOT / f'docs/program/comprehensive-v14/work/{op}/decision.json'
    identity = read(BASE / 'identity.json')
    decision = dict(operation_id=op, status='pass', decision='reference',
        decision_scope='Source-qualified PyMC model and predictive-contract reference; no native integration approval',
        identity=identity,
        reason='Retain concrete Bayesian graph transformation and sampling contracts as a conditional native-worker route; causal meaning and prediction identity require separate review.',
        target_and_uncertainty='Posterior and predictive quantities under a supplied prior/likelihood/intervention model; numerical diagnostics do not identify observationally equivalent causal effects or establish bank-policy confidence.',
        license=dict(declaration='Apache-2.0 root package', text=ref(RAW / 'exec23_pymc_00.txt', 'Pinned license'), transitive_clearance=False),
        dependencies=dict(python=identity['python'], direct=identity['direct_dependencies'], optional=identity['optional_dependencies'], environment_locked=False),
        conversion_contract=[
            'Bind original/transformed graph, prior, likelihood, intervention, model/data/coordinate digest, horizon and units.',
            'Distinguish observe from do, fixed assignment from self-reference, and rejected/pruned conversions from accepted ones.',
            'Bind trace/parameter identity, output selection, regenerated and frozen variables and deterministic expressions; name/shape matching alone is insufficient.',
            'State Potential role and requested generative law, retaining effects already encoded in posterior ancestors.',
            'Pin sampler/backend; preserve absent, unavailable, adverse and satisfactory diagnostics and backend-specific persistence restrictions.',
            'Library/CLI/MCP share targets, warnings, uncertainty/refusal and budget semantics; an LLM model proposal does not certify scientific truth.'],
        alternatives=[
            dict(route='Native Python worker', decision='conditional future prototype', reason='Keeps upstream graph and sampling semantics after locked-artifact review and exact-oracle conformance.'),
            dict(route='Blanket R/Java/C++ port', decision='reject for current scope', reason='Duplicating transformations, predictive volatility and numerical kernels has no demonstrated benefit.'),
            dict(route='Independent finite and conjugate oracle', decision='retain', reason='Separates model meaning and arithmetic from selected numerical engine.'),
            dict(route='Universal causal discovery/identification engine', decision='reject', reason='Supplying a graph and obtaining posterior draws does not establish causal truth or distinguish equal observed laws.'),
            dict(route='Automatic policy-confidence engine', decision='reject', reason='Model selection, hidden mechanisms and sampling-law calibration need separate arguments.')],
        costs_to_measure=['Artifact and rights custody', 'Compilation and warmup', 'Effective samples and diagnostics',
            'Prediction regeneration and memory', 'Serialization and model conversion', 'Backend-specific persistence/recovery', 'Version maintenance'],
        owner_obligations=dict(scientific='Causal model, intervention/prediction meaning and uncertainty law',
            maintainer='Pinned environment, model/trace conversion and native conformance', operator='Rights, budgets, diagnostic visibility and recovery'),
        revisit_trigger='Locked release/commit environment, full rights/dependency custody and registered native conjugate/finite-oracle transformation and prediction results; model/clock changes require renewed review.',
        evidence=evidence, reviewer=REVIEWER, limitations=LIMITS, integration_allowed=False, runtime_qualification=False, capabilities=[])
    write(output, decision)
    graph, merged, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, op)
    receipt = run.ledger.receipt_template(node)
    findings = ['Pinned development revision, dynamic version and selected source/license/dependencies inspected.',
        'Targets, prediction/uncertainty semantics, alternatives, costs, owners and revisit trigger explicit.',
        'Reference disposition separates source intentions, authored calculations and native/scientific qualification.']
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'], reviewer=REVIEWER,
        outputs=[ref(output, 'Contracted PyMC reference decision')],
        criteria=[dict(index=i, verdict='pass', finding=f, evidence=evidence) for i,f in enumerate(findings)],
        limitations=LIMITS, capabilities=[], nonexecution_reason='', revisit_trigger=decision['revisit_trigger'])
    run.validate_receipt(ROOT, merged, node, receipt, len(state['execution_program']['turns']))
    verify_bindings(receipt)
    write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps(dict(operation=op, decision='reference', integration_allowed=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['audit', 'receipt'])
    globals()[parser.parse_args().command]()
