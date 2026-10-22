#!/usr/bin/env python3
"""Record a bounded IV reference decision from already inspected pinned bytes."""
import hashlib
import json
from pathlib import Path
import tomllib

import python_iv_reference_20261022 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-22/linearmodels-reuse-v1'
PREFLIGHT = ROOT / 'docs/program/execution/2026-10-22/python-iv-rd-preflight-v2'
KERNELS = ROOT / 'docs/program/execution/2026-10-22/python-iv-kernels-v1'
OP = 'SW.DECISION.inherited_linearmodels'
PIN = '13390eee49ea06fc42f831255ff2163f2ad13e8b'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Source-level proposal reference only; no downloaded code, native adapter or upstream tests executed.',
    'Repository version is dynamic; equality to the inherited PyPI 7.0 release, wheel or installed environment is unverified.',
    'Top-level NCSA terms are inspected; transitive dependency rights, binary notices and environment compatibility remain open.',
    'The bounded IV inspection does not qualify panel, system, GMM, dynamic-panel or heterogeneous-treatment effects.',
    'No causal assignment, exclusion, instrument strength, weak-IV coverage or empirical calibration follows from rank checks or diagnostic labels.',
    'Exact references are authored arithmetic, not package output, vendor measurements or bank returns.']


def main():
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    for p in [PREFLIGHT / 'source-audit.json', KERNELS / 'source-audit.json', KERNELS / 'review.json']:
        verify_bindings(read(p))
    selected = [x for x in read(PREFLIGHT / 'selected-paths.json') if x['family'] == 'linearmodels']
    assert len(selected) == 5 and all(x['commit'] == PIN for x in selected)
    originals = []
    for item in selected:
        path = ROOT / item['artifact']
        body = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        assert blob == item['git_blob_sha']
        originals.append(dict(repository_path=item['path'], git_blob=blob,
            source_identity=f'https://raw.githubusercontent.com/bashtage/linearmodels/{PIN}/{item["path"]}',
            local_copy=ref(path, 'Unchanged pinned primary source')))
    metadata_path = ROOT / 'docs/literature/raw/exec22_pyiv_linearmodels_cutoff.json'
    metadata = read(metadata_path)[0]
    assert metadata['sha'] == PIN
    date = metadata['commit']['committer']['date']
    assert date <= '2026-10-07T15:59:59Z'
    paths = {x['path']: ROOT / x['artifact'] for x in selected}
    config = tomllib.loads(paths['pyproject.toml'].read_text())
    assert config['project']['license'] == 'NCSA'
    assert config['project']['dynamic'] == ['version']

    anchors = []
    for name, lo, hi, finding in [
        ('LICENSE.md', 1, 32, 'NCSA grant; source and binary notice retention; no endorsement without permission; no warranty.'),
        ('pyproject.toml', 1, 21, 'Meson/Cython/NumPy/setuptools-scm build requirements differ from the runtime dependency floors.'),
        ('pyproject.toml', 37, 67, 'Panel/IV/system description is scope metadata; version is dynamic, NCSA is declared, Python >=3.10 is required.'),
        ('linearmodels/iv/model.py', 174, 211, 'Positive mean-normalized weights and missing-row removal change the effective analysis inputs.'),
        ('linearmodels/iv/model.py', 342, 358, 'Separate regressor and instrument rank checks do not establish projected rank or exclusion.'),
        ('linearmodels/iv/model.py', 580, 609, 'Low-level k-class static estimate uses a projected inverse and explicitly performs no error checking.'),
        ('linearmodels/iv/model.py', 631, 716, 'Robust covariance and debiased=false are defaults; fixed-kappa estimation can preserve unavailable LIML diagnostics.'),
        ('linearmodels/iv/covariance.py', 625, 687, 'Actual one/two-cluster inclusion-exclusion branch must govern conversion rather than the One-Way label.'),
        ('linearmodels/iv/results.py', 679, 705, 'First-stage statistic and distribution are separate output fields.'),
        ('linearmodels/iv/results.py', 720, 746, 'Unadjusted covariance scales by restriction count and uses F; other covariance uses chi-square Wald.'),
        ('linearmodels/iv/results.py', 1320, 1353, 'anderson_rubin uses LIML kappa for overidentification; it accepts no coefficient-null argument.')]:
        lines = paths[name].read_bytes().decode().split('\n')
        assert hi <= len(lines)
        excerpt = '\n'.join(lines[lo - 1:hi])
        anchors.append(dict(source=ref(paths[name], 'Inspected original'), lines=[lo, hi],
            finding=finding, excerpt=excerpt, excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest()))
    write(BASE / 'inspected-extracts.json', dict(anchors=anchors, native_execution=False))
    write(BASE / 'plan-review.json', dict(status='pass',
        evidence=[ref(BASE / 'plan.md', 'Reviewed scope and failure checks')],
        checks=['Use existing originals and reverify immutable identities.',
            'Decide a reference role without granting native integration.',
            'Do not confuse numerical diagnostics with causal identification or calibrated inference.']))
    write(BASE / 'identity-review.json', dict(repository='bashtage/linearmodels', commit=PIN,
        commit_date=date, version='Dynamic repository version; release equivalence unverified',
        license='NCSA with notice and endorsement conditions',
        build_dependencies=config['build-system'], runtime_dependencies=config['project']['dependencies'],
        python=config['project']['requires-python'],
        maintenance=dict(evidence=ref(metadata_path, 'Commit identity and maintenance event'),
            observed=metadata['commit']['message'], limitation='Commit metadata shows an update; this review has not validated its panel implementation or a support commitment.'),
        alias_boundary='One bashtage/linearmodels lineage. statsmodels is a dependency and pyfixest a separate alternative; neither grants this engine equivalence.',
        primary_sources=originals,
        inherited_catalog=ref(ROOT / 'docs/literature/software/linearmodels.json', 'Preserved earlier package lead, not runtime admission')))
    results = exact.calculate()
    assert results == read(KERNELS / 'exact-results.json')
    write(BASE / 'exact-results.json', results)
    write(BASE / 'source-audit.json', dict(cutoff='2026-10-07', sources=[dict(
        integrated_citation_key='exec22_linearmodels_reuse', kind='software_primary_source',
        title='Pinned linearmodels IV reference choice and conversion boundary',
        author='Kevin Sheppard and contributors', year=2026,
        source_identity=f'https://github.com/bashtage/linearmodels/tree/{PIN}',
        version_date=f'Repository revision {PIN}; {date}; dynamic package version',
        local_copy=ref(BASE / 'identity-review.json', 'Identity, dependencies and five authentic originals'),
        primary_sources=originals,
        inspected_anchors=[dict(anchor=x['source']['path'] + ' lines ' + str(x['lines']),
            finding=x['finding'], evidence=ref(BASE / 'inspected-extracts.json', 'Verbatim inspected anchor')) for x in anchors],
        supported_claims=[x['finding'] for x in anchors], limitations=LIMITS)]))
    contract = dict(status='proposed_not_implemented', integration_allowed=False,
        inputs=['Pin repository, build and runtime environment separately; preserve user and executed estimator/covariance settings.',
            'Bind unit identities, full retained-row/column map, weight roles, target, instrument/exogenous definitions and information clock.',
            'Require an explicit moment/exclusion argument and sampling/dependence law; passing rank is insufficient.'],
        outputs=['Coefficient target, standard errors, full covariance and covariance settings, group IDs, bandwidth and reference distribution.',
            'Each diagnostic retains null, statistic, degrees of freedom, distribution, p-value, unavailable status and warnings.',
            'Numerical conditioning and residual diagnostics accompany a result; unsupported causal targets return a refusal.'],
        failures=['Refuse singular/ill-conditioned projected designs under the initial prototype profile rather than silently substituting a pseudoinverse.',
            'Do not substitute a robust variance for dependence-specific inference or one cluster label for actual grouping columns.',
            'Do not convert the overidentification property into a coefficient-null confidence-set inversion.',
            'Preserve a failed LIML diagnostic even if fixed-kappa coefficients return; do not publish unavailable diagnostics as evidence of validity.',
            'Refuse undeclared missing-row/weight changes and unsupported targets; retain all attempts.'],
        qualification=['Inspect remaining numerical delegates and test cases; freeze dependency versions and rights before native admission.',
            'Compare a direct pinned Python call and typed wrapper on prospectively fixed public/generated targets and exact projections.',
            'Add weak/projected-rank, invalid exclusion, missingness, calendar, cluster and covariance-failure cases; retain failure denominators.',
            'Register sampling-law-specific coverage and resource budgets before claiming calibration or economic benefit.'],
        behavioral_reference=ref(BASE / 'exact-results.json', 'Authored rank/exclusion and distribution witnesses; no package parity'))
    write(BASE / 'conversion-contract.json', contract)
    omissions = [
        dict(item='Native implementation', owner='Prototype author', next_action='Qualify a pinned direct Python call and typed contract; no adapter is currently admitted.'),
        dict(item='Release and dependencies', owner='Build/distribution owner', next_action='Bind release/wheel equality, lock runtime/build dependencies and audit transitive notices and compatibility.'),
        dict(item='Broader methods', owner='Research author', next_action='Inspect panel, system, GMM and alternative engines separately; preserve their distinct targets and assumptions.'),
        dict(item='Sampling guarantees', owner='Method reviewer', next_action='Register known-law weak-IV and dependence studies; mathematical source review alone grants no empirical coverage.'),
        dict(item='Editorial reconciliation', owner='Monograph author', next_action='Include the reference-only choice in the next source-backed integrated edition; the present reader already develops the IV source semantics.')]
    write(BASE / 'omissions-register.json', dict(items=omissions, global_blocker=None))
    evidence = [ref(BASE / name, 'Bounded reference decision evidence') for name in
        ['plan-review.json', 'identity-review.json', 'source-audit.json', 'inspected-extracts.json',
         'exact-results.json', 'conversion-contract.json', 'omissions-register.json']]
    evidence += [ref(KERNELS / 'review.json', 'Preserved earlier numerical-source review'),
        ref(ROOT / 'tools/python_iv_reference_20261022.py', 'Replayed authored reference')]
    decision = dict(operation=OP, status='pass', decision='reference', capabilities=[], integration_allowed=False,
        scope='Retain the pinned linearmodels linear-IV engine as a proposal reference; native adoption, broader engine coverage and calibration remain unqualified.',
        source=dict(repository='bashtage/linearmodels', commit=PIN, distinct_engine_lineages=1),
        alternatives=[
            dict(choice='pinned_Python_worker', disposition='preferred_future_candidate', reason='Preserve upstream estimator and covariance semantics, with explicit row/target/diagnostic conversion and an isolated pinned environment.'),
            dict(choice='unrestricted_direct_adoption', disposition='not_selected', reason='No native behavioral, dependency or law-specific calibration qualification supports an unrestricted interface.'),
            dict(choice='port_to_R_Java_Cxx', disposition='not_selected_initially', reason='No measured requirement offsets the numerical and distributional parity burden.'),
            dict(choice='pyfixest_or_R_IV_engines', disposition='separate_comparators', reason='Match population, instrument law, weighting, covariance and diagnostic meaning; a shared 2SLS label does not imply equivalent behavior.'),
            dict(choice='authored_exact_projection', disposition='qualification_reference', reason='Useful for finite deterministic cases but not a replacement for maintained estimation or justified sampling inference.'),
            dict(choice='reject_entire_engine', disposition='not_selected', reason='Inspected IV paths offer a substantive candidate; remaining obligations justify a limited reference role rather than a blanket absence claim.')],
        costs='No measured native runtime or license cost. Include dependency setup, data/formula conversion, diagnostics, covariance, failure review, maintenance and repeated inference in matched workflow costs.',
        owner_obligations=omissions, evidence=evidence, limitations=LIMITS,
        revisit_trigger='A selected prototype build, release/dependency change, new target or sampling law, or a need for weak-IV/panel/system inference.')
    output = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'decision.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    write(output, decision)
    write(BASE / 'review.json', dict(status='pass_for_bounded_reference_decision',
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        evidence=evidence + [ref(output, 'Canonical reference-only decision')],
        findings=['Five authentic pinned originals reverified; full NCSA conditions and distinct build/runtime dependencies inspected.',
            'The inherited broad adapter lead is restricted to a reference-only IV choice, without erasing that historical record.',
            'Target, uncertainty, warnings and diagnostic distributions retain separate contracts; authored examples reproduce.',
            'The decision does not close a software coverage cell or grant integration_allowed.'],
        limitations=LIMITS, native_execution=False, visual_acceptance=False))
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    receipt = run.ledger.receipt_template(node)
    findings = ['Pinned source identity, NCSA terms, dependency declarations and maintenance limits bound; distinct engine lineage preserved.',
        'Target/uncertainty and failure semantics, reuse alternatives, costs, owners and revisit trigger are explicit.',
        'Reference-only proposal choice passes with no integration capability; qualification and omissions remain recorded.']
    receipt.update(outcome='pass', execution='performed', scope=decision['scope'],
        reviewer=dict(name='Codex author/coordinator', kind='author'), limitations=LIMITS,
        capabilities=[], original_gap_qualification=False, nonexecution_reason='',
        revisit_trigger=decision['revisit_trigger'], outputs=[ref(output, 'Required reuse decision')],
        criteria=[dict(index=i, verdict='pass', finding=finding,
            evidence=evidence + [ref(BASE / 'review.json', 'Author review'),
                ref(Path(__file__), 'Reproducible review')]) for i, finding in enumerate(findings)])
    write(BASE / 'operation-receipt.json', receipt)
    verify_bindings(read(BASE / 'review.json'))
    print(json.dumps(dict(decision='reference', integration_allowed=False, originals=5,
        inspected_anchors=len(anchors), outcome='pass', native_execution=False)))


if __name__ == '__main__':
    main()
