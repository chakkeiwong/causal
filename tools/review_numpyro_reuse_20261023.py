#!/usr/bin/env python3
"""Review pinned NumPyro contracts without importing downloaded package code."""
import argparse
import hashlib
import json
import tomllib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpyro_reference_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
core = run.core
ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-23/numpyro-reuse-v1'
RAW = ROOT / 'docs/literature/raw'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Twenty authenticated selected primary files and project-owned exact arithmetic only; no NumPyro/JAX/Funsor code or upstream tests executed.',
    'Version 0.22.0 is declared by the selected revision; a distributed release and whole-project exhaustive review are not verified.',
    'Source-described contracts, authored semantic counterexamples and native/scientific qualification are separate evidence classes.',
    'Full dependency and rights custody, native conformance, costs, recovery, bank validation and visual/final acceptance remain open.',
]
SPANS = {
    'LICENSE.md': [([1, 202], 'Pinned Apache-2.0 root terms; dependency and distributed-artifact notices remain separate.')],
    'pyproject.toml': [([1, 44], 'Python at least 3.11, direct JAX/jaxlib requirements, device extras and declared license-file path.')],
    'numpyro/version.py': [([1, 4], 'Selected source explicitly declares 0.22.0; this does not authenticate a distributed release.')],
    'numpyro/primitives.py': [([37, 67], 'Handler-stack processing, stop and postprocessing determine composition.'),
        ([318, 341], 'Deterministic site records and returns the handler-processed value.')],
    'numpyro/handlers.py': [([200, 258], 'Replay matches sampled sites and roles, leaves target observations alone and forwards control-flow substitution.'),
        ([416, 478], 'Condition fixes matched sample values and marks observations.'),
        ([811, 907], 'Seed handler has mutable key state; source documents a closure pattern for JAX transformation use.'),
        ([909, 986], 'Substitution can also replace deterministic sites and does not make the same observation declaration.'),
        ([989, 1067], 'Do splits the original-name sampled trace site from the intervention value sent to descendants; repeated intervention warns.')],
    'numpyro/infer/util.py': [([546, 595], 'Discrete enumeration and continuous transforms have explicit support and configuration boundaries.'),
        ([610, 647], 'Enumeration prepares a model with plate validation and tensor-dimension allocation.'),
        ([898, 984], 'Prediction distinguishes posterior substitution, deterministic recomputation, output selection and discrete posterior inference.'),
        ([987, 1045], 'Predictive is experimental; new outcomes require clearing observations; batch axes and deterministic substitution are declared.'),
        ([1075, 1166], 'Constructor validates source choice and batch shapes and maps deprecated deterministic configuration to the new control.')],
    'numpyro/infer/mcmc.py': [([334, 360], 'Parallel, sequential and vectorized chain routes and compilation configuration are distinct.'),
        ([406, 440], 'Insufficient devices cause a warned sequential fallback.'),
        ([628, 656], 'Last state and post-warmup state support documented continuation; durable crash recovery is not observed.'),
        ([705, 768], 'Scalar versus batched random keys, extra-field collection and asynchronous timing caveat.'),
        ([837, 868], 'Summary and divergence display depend on retained states and collected fields.')],
    'numpyro/infer/hmc.py': [([35, 84], 'HMC state distinguishes samples, trajectory quantities and divergences.'),
        ([748, 756], 'Default HMC collected fields are z and diverging.'),
        ([947, 1053], 'NUTS configuration includes mass matrix, acceptance target, trajectory depth and initialization strategy.')],
    'numpyro/infer/hmc_gibbs.py': [([111, 128], 'HMCGibbs requires a model rather than a bare potential function.'),
        ([133, 208], 'DiscreteHMCGibbs distinguishes marginalization from discrete updates and binds proposal choices.')],
    'numpyro/infer/initialization.py': [([95, 129], 'Default uniform initialization is in unconstrained space and skips already supplied values; it is not a prior posterior draw.')],
    'numpyro/util.py': [([40, 110], 'Precision, platform and host-device settings are explicit configuration, with initialization/configuration caveats.')],
    'numpyro/diagnostics.py': [([62, 97], 'Classical and split R-hat use explicit chain/draw axes and minimum lengths.'),
        ([181, 226], 'Effective sample size is a numerical chain diagnostic, not causal identification.'),
        ([265, 321], 'Summary computes spread, HPDI, effective sample size and split R-hat; nonfinite values need a separate disposition.')],
    'numpyro/contrib/funsor/infer_util.py': [([46, 85], 'Enumeration configuration targets supported unobserved discrete sites; only parallel default is documented.')],
    'test/test_handlers.py': [([503, 578], 'Unexecuted tests distinguish returned intervention values, original-name trace values and composed observations.')],
    'test/infer/test_mcmc.py': [([557, 588], 'Unexecuted chain test distinguishes flattened from grouped-by-chain output.'),
        ([688, 701], 'Unexecuted tests request trajectory counts and adaptation step sizes explicitly.')],
    'test/infer/test_infer_util.py': [([129, 223], 'Unexecuted tests document changed-input deterministic recomputation and deprecated alias validation.'),
        ([613, 658], 'Unexecuted tests distinguish masking under discrete inference and ordinary prediction.')],
    'test/contrib/test_infer_discrete.py': [([86, 132], 'Scan tests include lengths one and two and mark length ten xfail for a sum-product adjoint limitation; no test was run.')],
    'numpyro/infer/gibbs.py': [([184, 219], 'Discrete selector excludes parallel-marginalized sites and obtains enumerable support sizes.'),
        ([322, 355], 'Composable Gibbs validates a partition and model/block conditions.'),
        ([545, 584], 'Gibbs rejects unsupported key, subsample-plate and cross-block support configurations.'),
        ([1023, 1038], 'Discrete proposal selection distinguishes conditional and random-walk routes with optional modification.')],
    'numpyro/contrib/funsor/discrete.py': [([43, 59], 'Temperature zero uses max/MAP approximation and one posterior sampling; other values rejected.'),
        ([120, 150], 'Documentation warns about scan support and inferred-trace log probabilities; scan tests constrain interpretation.')],
    'numpyro/contrib/funsor/__init__.py': [([1, 32], 'Funsor import is a separate experimental dependency and selects the JAX backend.')],
}
FINDINGS = [
    'Observation, intervention and replay have different site roles; the do trace can differ from the returned action by design.',
    'Single-world intervention marginals do not determine cross-world customer counterfactuals; structural coupling must be declared.',
    'Posterior substitution, deterministic recomputation, output selection and discrete inference are separate prediction controls.',
    'Posterior averaging and MAP decoding reverse the stipulated servicing decision; scan documentation/test tension remains qualified.',
    'Devices, precision, key lineage, diagnostic axes and complete continuation state require explicit native qualification and full costs.',
]


def audit():
    assert not (BASE / 'source-audit.json').exists()
    sel = read(BASE / 'source-selection-v2.json')
    commit = read(RAW / 'exec23_numpyro_cutoff.json')[0]
    tree = read(RAW / 'exec23_numpyro_tree.json')
    assert sel['commit'] == commit['sha'] == '033f7e2e57bd0396fba8493ae246debe52f2c973'
    assert sel['tree'] == tree['sha'] == commit['commit']['tree']['sha'] and not tree['truncated']
    assert sel['date'] == commit['commit']['committer']['date'] == '2026-10-05T07:17:49Z'
    assert datetime.fromisoformat(sel['date'].replace('Z', '+00:00')).astimezone(ZoneInfo('Asia/Shanghai')).date().isoformat() <= '2026-10-07'
    entries = {x['path']: x for x in tree['tree']}
    records = []
    for e in sel['selected']:
        p = RAW / (e['id'] + '.txt')
        data = p.read_bytes()
        receipt = read(RAW / (e['id'] + '.receipt.json'))
        path = e['path']
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        url = 'https://raw.githubusercontent.com/pyro-ppl/numpyro/' + sel['commit'] + '/' + path
        assert blob == e['blob'] == entries[path]['sha'] and len(data) == e['size'] == entries[path]['size']
        assert receipt['status'] == 'saved' and receipt['sha256'] == core.sha(p) and receipt['url'] == url
        assert all(1 <= a <= b <= len(data.decode().splitlines()) for (a, b), _ in SPANS[path]), path
        records.append(dict(upstream_path=path, source_identity=url, version_date=sel['date'],
            local_copy=ref(p, 'Inspected immutable primary text'), receipt=ref(RAW / (e['id'] + '.receipt.json'), 'Acquisition custody'),
            git_blob_sha1=blob, inspected_anchors=[dict(lines=span, finding=claim) for span, claim in SPANS[path]],
            supported_claims=[claim for _, claim in SPANS[path]], executed=False))
    assert len(records) == 20 and exact.calculate() == read(BASE / 'exact-results.json')
    metadata = tomllib.loads((RAW / 'exec23_numpyro_01.txt').read_text())['project']
    assert metadata['requires-python'] == '>=3.11'
    assert {'jax>=0.7.0', 'jaxlib>=0.7.0'} <= set(metadata['dependencies'])
    assert '__version__ = "0.22.0"' in (RAW / 'exec23_numpyro_02.txt').read_text()
    assert metadata['license']['file'] == 'LICENSE' and 'LICENSE' not in entries and 'LICENSE.md' in entries
    identity = dict(repository='pyro-ppl/numpyro', package='numpyro', version='0.22.0',
        version_status='Declared by pinned source; no distributed release authenticated', commit=sel['commit'],
        tree=sel['tree'], date=sel['date'], source_blobs=20, python=metadata['requires-python'],
        direct_dependencies=metadata['dependencies'], optional_dependencies=metadata['optional-dependencies'],
        additional_route_dependency='Funsor for inspected enumeration/discrete posterior route; separately locked and cleared',
        license_file_custody='Metadata says LICENSE; selected root contains LICENSE.md. Verify actual distribution notices; no build failure asserted.',
        evidence=[ref(RAW / 'exec23_numpyro_cutoff.json', 'Cutoff identity'), ref(RAW / 'exec23_numpyro_tree.json', 'Complete tree metadata')],
        maintenance='Pinned revision and selected technical contracts inspected; no service-level or exhaustive maintenance claim.')
    write(BASE / 'identity.json', identity)
    write(BASE / 'static-contract-check.json', dict(native_execution=False, findings=FINDINGS,
        rejected_overclaims=['No claim that scalar-key MCMC duplicates chains.', 'No blanket scan support or native failure assertion.',
            'No automatic causal or cross-world identification.', 'No benchmark or full-environment rights clearance.'],
        documentation_test_tension=dict(doc=ref(RAW / 'exec23_numpyro_18.txt', 'infer_discrete scan warning'),
            tests=ref(RAW / 'exec23_numpyro_16.txt', 'scan lengths one/two and length-ten xfail'),
            next_action='Registered native length/construction-specific posterior and decoding oracle trial'),
        evidence=[ref(Path(exact.__file__), 'Independent finite and normalizing-integral calculations')]))
    source = dict(integrated_citation_key='exec23_numpyro_sources', kind='software_primary_sources',
        title='NumPyro 0.22.0 pinned handler, predictive, discrete and sampler contracts', author='NumPyro Contributors', year=2026,
        source_identity='https://github.com/pyro-ppl/numpyro/tree/' + sel['commit'],
        version_date='Source-declared 0.22.0; revision ' + sel['commit'] + '; ' + sel['date'],
        local_copy=records[4]['local_copy'], identity=identity, records=records,
        inspected_anchors=[dict(path=r['upstream_path'], anchors=r['inspected_anchors']) for r in records],
        supported_claims=[claim for spans in SPANS.values() for _, claim in spans],
        license_text=ref(RAW / 'exec23_numpyro_00.txt', 'Pinned Apache-2.0 root license'), limitations=LIMITS)
    project = dict(integrated_citation_key='exec23_numpyro_reference', kind='project_derivation_and_exact_reference',
        title='Exact NumPyro-worker semantic, latent-decision, cross-world and conjugate references',
        author='Causal banking proposal project', year=2026, source_identity='tools/numpyro_reference_20261023.py',
        version_date='23 October 2026; project-owned finite arithmetic', local_copy=ref(Path(exact.__file__), 'calculate'),
        inspected_anchors=['calculate', 'moments', 'beta_integral'], supported_claims=[
            'Specified confounded law has association four and intervention effect two.',
            'The specified alert has probability 5/12 and posterior high type 3/5; prior, mixture and MAP action values are -100, -20 and 100.',
            'Equal intervention success marginals 1/2 allow cross-world conditional probabilities one and zero.',
            'Beta(2,3) with four successes and one failure gives Beta(6,4), mean 3/5 and variance 6/275.',
            'Four independent Bernoulli draws have mean variance 1/16; four exact copies have 1/4, without a native PRNG defect claim.',
            'Stored square and recomputed cube means at parent values one/two differ as 5/2 and 9/2.'], limitations=LIMITS)
    write(BASE / 'source-audit.json', dict(sources=[source, project], cutoff='2026-10-07', native_execution=False))
    write(BASE / 'omissions-register.json', dict(items=[
        dict(gap='Distributed artifacts, full dependency/device identity and rights', next_action='Bind actual NumPyro/JAX/jaxlib/Funsor and device artifacts, inspect distribution notices and pin precision and compilation configuration.'),
        dict(gap='Native handler and prediction conformance', next_action='Register role/trace, observation/intervention, replay, changed-input deterministic, output-selection and new-outcome oracle trials.'),
        dict(gap='Discrete support and scan boundary', next_action='Compare enumeration, posterior sampling and MAP decoding with exact small references, including documented/tested scan lengths and xfail lead.'),
        dict(gap='Numerical diagnostics, actual costs and durable recovery', next_action='Measure complete synchronized workloads, effective samples and missing/adverse diagnostics; fault-test full-state restart and publication.'),
        dict(gap='Scientific and bank qualification', next_action='Justify causal graph, assignment, cross-world coupling and uncertainty law before costly bank validation.')], limitations=LIMITS))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_authored_exact_examples',
        evidence=[ref(Path(exact.__file__), 'Independent finite enumeration and beta-integral ratios'),
            ref(BASE / 'exact-results.json', 'Exact rational outputs'), ref(BASE / 'development.tex', 'Explained derivations')],
        checks=['Finite distributions normalize and conditional/interventional values are independently enumerated.',
            'Two explicit joint potential-outcome laws have the same marginals and different cross-world conditionals.',
            'Posterior mixture and MAP policies are compared against a common zero-action baseline.',
            'Conjugate mean/variance use normalizing-integral ratios; dependence witness enumerates both laws.'],
        native_execution=False))
    write(BASE / 'plan-review.json', dict(status='pass_for_reference_disposition', findings=FINDINGS,
        evidence=[ref(BASE / n, 'Reviewed argument and source limits') for n in ['plan.md', 'exact-results.json', 'static-contract-check.json', 'mathematical-review.json', 'development.tex']],
        amendments=['Inspect Gibbs/discrete delegates in addition to the initial seventeen files.',
            'Qualify scan documentation against actual test markings before making any support claim.',
            'Keep source version declaration separate from distributed-release custody.'], native_execution=False))
    evidence = [ref(BASE / n, 'Reviewed primary-source or project evidence') for n in [
        'source-audit.json', 'identity.json', 'static-contract-check.json', 'exact-results.json', 'omissions-register.json',
        'mathematical-review.json', 'plan-review.json', 'development.tex']]
    evidence += [ref(Path(__file__), 'Source/decision review logic'), ref(Path(exact.__file__), 'Authored arithmetic')]
    review = dict(status='pass_for_reference_disposition', reviewer=REVIEWER, evidence=evidence,
        findings=FINDINGS, limitations=LIMITS, native_execution=False)
    verify_bindings(review)
    write(BASE / 'review.json', review)
    print(json.dumps(dict(source_blobs=20, source_records=2, decision='reference', native_execution=False)))


def receipt():
    op = 'SW.DECISION.inherited_numpyro'
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == op
    verify_bindings(read(BASE / 'review.json'))
    evidence = [ref(BASE / n, 'Reviewed NumPyro reference disposition') for n in [
        'source-audit.json', 'identity.json', 'review.json', 'plan-review.json', 'mathematical-review.json',
        'exact-results.json', 'static-contract-check.json', 'omissions-register.json', 'development.tex']]
    evidence += [ref(Path(__file__), 'Receipt construction')]
    output = ROOT / f'docs/program/comprehensive-v14/work/{op}/decision.json'
    identity = read(BASE / 'identity.json')
    decision = dict(operation_id=op, status='pass', decision='reference',
        decision_scope='Source-qualified NumPyro probabilistic-worker reference; no native integration approval', identity=identity,
        reason='Retain handler, enumeration and compiled inference as a conditional Python-worker route, preserving experiment and prediction identities.',
        target_and_uncertainty='Model-specific posterior/predictive quantities; MAP state decoding, causal identification, cross-world coupling and policy calibration require separate declarations.',
        license=dict(declaration='Apache-2.0 root package', text=ref(RAW / 'exec23_numpyro_00.txt', 'Pinned terms'), transitive_clearance=False,
            distribution_notice_custody=False),
        dependencies=dict(python=identity['python'], direct=identity['direct_dependencies'], optional=identity['optional_dependencies'],
            additional_route=identity['additional_route_dependency'], environment_locked=False),
        conversion_contract=[
            'Bind model/data/clock/units, sample versus observed roles, handler order and returned versus original-trace treatment values.',
            'Declare causal graph, intervention and factual/cross-world target, including structural-noise coupling.',
            'Bind posterior sample identity, fixed/regenerated sites, deterministic substitution, output selection and batch axes.',
            'Distinguish marginalization, posterior draws and MAP decoding; retain support, block, plate and scan limits.',
            'Bind actual devices, precision, chain method, key lineage and collected diagnostic definitions/availability.',
            'Bind complete sampler/adaptation state and immutable model/environment for tested durable restart.',
            'Library/CLI/MCP share uncertainty, refusal, diagnostic and budget semantics; an LLM proposal is not scientific acceptance.'],
        alternatives=[
            dict(route='Native Python process worker', decision='conditional future prototype', reason='Preserves upstream execution/compiler semantics after locked custody and oracle conformance.'),
            dict(route='General R/Java/C++ port', decision='reject for current scope', reason='Duplicating handlers, enumeration and compiler behavior has no measured benefit.'),
            dict(route='PyMC worker', decision='retain substantive alternative', reason='Different graph-transformation and predictive defaults require matched semantic/cost evaluation.'),
            dict(route='Finite and conjugate exact reference', decision='retain', reason='Independent targets and arithmetic separate semantic meaning from numerical engine.'),
            dict(route='Universal discovery or individual-counterfactual engine', decision='reject', reason='Supplied execution and posterior inference cannot identify missing causal or cross-world information.')],
        costs_to_measure=['Complete artifact/rights custody', 'Compilation and synchronized warmup', 'Effective posterior samples',
            'Enumeration dimension and memory', 'Prediction regeneration', 'Conversion/serialization', 'Durable recovery', 'Version/device maintenance'],
        owner_obligations=dict(scientific='Assignment/latent/cross-world assumptions, intervention and policy uncertainty law',
            maintainer='Pinned artifacts and experiment-preserving conversion with native oracles',
            operator='Actual devices, precision, key/diagnostic custody, budgets and recovery'),
        revisit_trigger='Locked complete artifacts/rights, registered native finite/conjugate and scan-specific results, full costs and restart evidence; model or experiment changes require renewed review.',
        evidence=evidence, reviewer=REVIEWER, limitations=LIMITS, integration_allowed=False, runtime_qualification=False, capabilities=[])
    write(output, decision)
    graph, merged, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, op)
    receipt = run.ledger.receipt_template(node)
    findings = ['Pinned version/revision, primary contracts, root license and explicit dependency/device custody inspected.',
        'Targets, uncertainty, conversion, alternatives, costs, owners and revisit trigger are concrete.',
        'Reference-only decision preserves authored/source/native distinctions and named scientific limits.']
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'], reviewer=REVIEWER,
        outputs=[ref(output, 'Contracted NumPyro reference decision')],
        criteria=[dict(index=i, verdict='pass', finding=f, evidence=evidence) for i, f in enumerate(findings)],
        limitations=LIMITS, capabilities=[], nonexecution_reason='', revisit_trigger=decision['revisit_trigger'])
    run.validate_receipt(ROOT, merged, node, receipt, len(state['execution_program']['turns']))
    verify_bindings(receipt)
    write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps(dict(operation=op, decision='reference', integration_allowed=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['audit', 'receipt'])
    globals()[parser.parse_args().command]()
