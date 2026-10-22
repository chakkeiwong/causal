#!/usr/bin/env python3
"""Review pinned LMTP semantics and record a reference-only proposal choice."""
import hashlib
import json
from pathlib import Path

import lmtp_policy_reference_20261022 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-22/lmtp-reuse-v1'
RAW = ROOT / 'docs/literature/raw'
PIN = 'f04a2b47f46debc515ce4ae778e05ebfde922c44'
OP = 'SW.DECISION.inherited_lmtp'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Source-level proposal reference only. No downloaded R code, upstream tests, native adapter or dependency was executed.',
    'This selected pre-cutoff repository revision declares 1.5.4; CRAN artifact equality, latest-release coverage and installed environment are unverified.',
    'AGPL-3 package terms are authenticated; transitive rights and a proposed distribution/network arrangement remain to be reviewed.',
    'Source findings about cluster names and control defaults require native reproduction before claiming observed package failure.',
    'The ife variance/contrast implementation, SuperLearner internals, future RNG behavior and full survival delegates are not qualified here.',
    'A finite history, cross-fitting option or density-ratio truncation does not prove exchangeability, support, nuisance rates or calibrated uncertainty.',
    'The monetary example is exact authored arithmetic under a stipulated law, not package output, empirical validation or bank benefit.',
    'This decision does not close longitudinal software coverage or grant product/repository adoption.']


def main():
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    meta_path = RAW / 'r3g_commit_lmtp.json'
    meta = read(meta_path)[0]
    tree_path = RAW / 'r3g_tree_lmtp.json'
    tree = read(tree_path)
    assert meta['sha'] == PIN and meta['commit']['committer']['date'] < '2026-10-07T15:59:59Z'
    assert tree['truncated'] is False
    entries = {x['path']: x for x in tree['tree']}
    # The saved API header repeats the requested commit. Authenticate the
    # actual Git tree objects rather than treating that header as a tree OID.
    tree_proof = []
    for directory in ['', 'R']:
        children = [x for x in tree['tree'] if str(Path(x['path']).parent).replace('.', '', 1) == directory]
        children.sort(key=lambda x: (Path(x['path']).name + ('/' if x['type'] == 'tree' else '')).encode())
        body = b''.join(x['mode'].lstrip('0').encode() + b' ' + Path(x['path']).name.encode()
            + b'\0' + bytes.fromhex(x['sha']) for x in children)
        oid = hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        expected = entries[directory]['sha'] if directory else meta['commit']['tree']['sha']
        assert oid == expected, (directory, oid, expected)
        tree_proof.append(dict(directory=directory or '/', reconstructed_git_tree=oid,
            expected=expected, immediate_children=len(children)))
    selected = read(BASE / 'source-selection.json')
    paths, originals = {}, []
    for x in selected:
        p = ROOT / x['artifact']
        body = p.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        assert blob == x['git_blob'] == entries[x['path']]['sha']
        assert len(body) == x['bytes'] == entries[x['path']]['size']
        paths[x['path']] = p
        receipt = p.with_suffix('.receipt.json')
        if p.name == 'pinned-LICENSE.md':
            receipt = RAW / 'license_detail_lmtp.receipt.json'
        assert receipt.exists()
        r = read(receipt)
        if p.name != 'pinned-LICENSE.md':
            assert r['status'] == 'saved' and r['sha256'] == run.core.sha(p)
        originals.append(dict(repository_path=x['path'], git_blob=blob,
            source_identity=f'https://raw.githubusercontent.com/nt-williams/lmtp/{PIN}/{x["path"]}',
            local_copy=ref(p, 'Authentic bytes matching the pinned Git tree'),
            retrieval=ref(receipt, 'Original acquisition record; HEAD bytes independently matched to pinned tree where applicable')))
    assert len(originals) == 17
    write(BASE / 'tree-identity-review.json', dict(status='pass',
        api_header=tree['sha'], commit_tree=meta['commit']['tree']['sha'], reconstructed=tree_proof,
        evidence=[ref(meta_path, 'Authenticated commit/tree link'), ref(tree_path, 'Original complete tree listing'),
            ref(BASE / 'review-attempt-1.log', 'Preserved failed assumption that API header was tree OID'),
            ref(BASE / 'review-generator-attempt-1.py', 'Preserved failed verifier')]))
    specs = [
        ('DESCRIPTION', 1, 52, 'Version 1.5.4, AGPL-3, R floor and imported dependencies; declaration does not establish a resolved runtime.'),
        ('LICENSE.md', 1, 14, 'Authentic license is GNU Affero GPL version 3.'),
        ('LICENSE.md', 534, 554, 'Section 13 addresses source offers for modified versions used over a network, and combination with GPLv3 work.'),
        ('README.md', 6, 19, 'README GPLv3 badge differs from the authenticated AGPL-3 declaration and license text.'),
        ('R/estimators.R', 7, 88, 'Ordered histories, policy/shifted precedence, finite-history k, cluster ID, sampling weights, cross-fitting and documented result semantics.'),
        ('R/estimators.R', 93, 144, 'TMLE builds a task and passes density ratios and sequential fits to theta_dr; it does not itself return a treatment contrast.'),
        ('R/shift.R', 1, 55, 'Supplied shifted data overrides shift; censoring becomes one and each shift function reads the original data argument.'),
        ('R/shift.R', 108, 148, 'ipsi applies a randomized binary risk-ratio-style modification, with separate up/down branches; it is not the odds-tilt map.'),
        ('R/Task.R', 24, 60, 'Task checks finite weights, constructs/rescales outcome bounds, makes folds and normalizes weights; constant-range behavior needs qualification.'),
        ('R/Task.R', 63, 120, 'Observed uses censoring=1, risk-free uses competing event=0, and at-risk combines previous-time outcome/competing-event states.'),
        ('R/Task.R', 132, 190, 'Outer folds read ._lmtp_id while as_lmtp_data writes ..i..lmtp_id; supplied weights are mean-normalized unless already normalized.'),
        ('R/Vars.R', 12, 50, 'History construction depends on k and declared ordering; this is a computational restriction requiring a scientific sufficiency argument.'),
        ('R/checks.R', 1, 19, 'Missing treatment/covariates among relevant uncensored at-risk observations are rejected.'),
        ('R/checks.R', 59, 77, 'Shifted data may differ only in declared treatment/censoring columns and shifted censoring must be one.'),
        ('R/make_folds.R', 1, 59, 'Without cluster IDs the helper splits rows; with IDs it groups rows, may lower V, and V=1 uses the same training and validation set.'),
        ('R/sl.R', 2, 22, 'Nuisance learner CV checks the number of supplied unique IDs and forwards IDs to SuperLearner; this is distinct from outer cross-fitting.'),
        ('R/sl.R', 25, 33, 'Prediction bound is controlled by the actual tol call; NULL returns unbounded predictions.'),
        ('R/lmtp_control.R', 3, 48, 'Documented .bound=1e-5 differs from the function default 1e5; the control field is returned without a range bound.'),
        ('R/tmle.R', 66, 84, 'Inspected TMLE predictions pass hard-coded 1e-05; no control$.bound read occurs in this source.'),
        ('R/tmle.R', 104, 110, 'Fluctuation wraps glm in sw and update calls bound with its own default.'),
        ('R/sdr.R', 69, 91, 'SDR prediction calls pass NULL and feed the sequential influence expression into the earlier-time pseudo-outcome.'),
        ('R/density_ratios.R', 9, 22, 'Per-fold futures request seeded evaluation; recombined ratios are then trimmed.'),
        ('R/density_ratios.R', 51, 62, 'Density-ratio denominator uses a 0.999 cap; followed-rule and censoring/risk states multiply the returned ratios.'),
        ('R/utils.R', 20, 50, 'bound clips to [p,1-p], trim uses one quantile over the supplied object, and sw suppresses warnings.'),
        ('R/utils.R', 64, 74, 'Survival conversion reverses binary coding; weight normalization checks a mean of one.'),
        ('R/eif.R', 1, 12, 'Sequential expression sums cumulative ratio-weighted residuals with na.rm=TRUE; distinguish structural missingness from unexpected failures.'),
        ('R/theta.R', 1, 25, 'TMLE and SDR use distinct weighted means, rescale, and call ife::ife with weights and task$id; returned key is estimate, singular.')]
    anchors = []
    for name, lo, hi, finding in specs:
        lines = paths[name].read_text().splitlines()
        assert hi <= len(lines), (name, hi, len(lines))
        excerpt = '\n'.join(lines[lo-1:hi])
        anchors.append(dict(source=ref(paths[name], 'Inspected original'), lines=[lo, hi],
            finding=finding, excerpt=excerpt, excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest()))
    write(BASE / 'inspected-extracts.json', dict(anchors=anchors))
    description = paths['DESCRIPTION'].read_text()
    assert 'License: AGPL-3' in description and 'Version: 1.5.4' in description
    write(BASE / 'identity-review.json', dict(repository='nt-williams/lmtp', commit=PIN,
        commit_date=meta['commit']['committer']['date'], declared_version='1.5.4',
        license='AGPL-3; LICENSE.md is AGPLv3, despite the README GPLv3 badge',
        imports=description.split('Imports:')[1].split('URL:')[0].strip(),
        R_floor='R >= 2.10 as declared; actual dependency compatibility not resolved',
        maintenance=dict(event=meta['commit']['message'], evidence=ref(meta_path, 'Selected maintenance event'),
            limit='This event and the inherited July push metadata do not establish future support or latest published release identity.'),
        alias_boundary='One nt-williams/lmtp lineage. ltmle and gfoRmula are separate estimators, not aliases or inherited approvals.',
        originals=originals, tree=ref(tree_path, 'Complete tree bound to the authenticated commit'),
        license_extraction=ref(RAW / 'license_detail_lmtp.json', 'Original API response containing base64 license bytes')))
    write(BASE / 'plan-review.json', dict(status='pass_for_reference_decision',
        evidence=[ref(BASE / 'plan.md', 'Reviewed scope')],
        checks=['Bound every technical file to the same pre-cutoff revision.',
            'Trace the surprising control default into actual prediction calls before describing consequences.',
            'Distinguish outer folds, nuisance CV and variance IDs; do not infer calibration from a cluster option.',
            'Keep exact policy arithmetic separate from package execution and empirical benefit.']))
    write(BASE / 'source-audit.json', dict(cutoff='2026-10-07', sources=[dict(
        integrated_citation_key='exec22_lmtp_reuse', kind='software_primary_source',
        title='Pinned lmtp policy, cross-fitting, nuisance and uncertainty interface inspection',
        author='Nicholas Williams, Ivan Diaz and contributors', year=2026,
        source_identity=f'https://github.com/nt-williams/lmtp/tree/{PIN}',
        version_date=f'1.5.4 declared; {PIN}; {meta["commit"]["committer"]["date"]}',
        local_copy=ref(BASE / 'identity-review.json', 'Authentic originals and identity'),
        primary_sources=originals,
        inspected_anchors=[dict(anchor=x['source']['path']+' lines '+str(x['lines']), finding=x['finding'],
            evidence=ref(BASE / 'inspected-extracts.json', 'Verbatim anchors')) for x in anchors],
        supported_claims=[x['finding'] for x in anchors], limitations=LIMITS)]))
    result = exact.calculate()
    assert [x['expected_net_dollars'] for x in result['results']] == ['184/25', '456/25', '107/9']
    write(BASE / 'exact-policy-results.json', result)
    contract = dict(status='proposed_not_implemented', integration_allowed=False,
        inputs=['Explicit time-zero, ordered histories, units, outcome/event/censoring meanings and target population.',
            'Distinguish a policy mean from a contrast; preserve reference policy, natural versus assigned histories and mtp/k.',
            'Freeze stochastic shift RNG or explicit shifted data, row mapping, cluster IDs, weights, bounds and all learner settings.',
            'Record actual outer-fold memberships, inner learner folds, trimming thresholds and denominator caps.'],
        outputs=['Policy mean and reference/contrast objects with full covariance and influence contributions once the ife delegate is qualified.',
            'Executed row/cluster map and weights, outcome scale, density-ratio distribution and trimmed counts by time/fold.',
            'Explicit failure/unavailable states for missingness, unsupported histories, empty folds, no support, degenerate outcomes or nonfinite computations.'],
        refusal_and_repairs=['Do not admit clustered outer cross-fitting until the inconsistent ID-column names are resolved and group-disjointness is observed.',
            'Do not claim the .bound control governs these fits: inspected TMLE passes 1e-5, SDR passes NULL; resolve documentation and effective options.',
            'Require valid nonnegative weights and a positive normalization total under the initial profile; finite-only source validation is insufficient.',
            'Separate intended post-event missingness from unexpected numerical NA values before allowing na.rm=TRUE reductions.',
            'Capture warnings and estimator failure, including warnings suppressed in the inspected fluctuation helper.',
            'Do not treat a one-fold fit as held-out cross-fitting, or a requested fold count as the realized one.'],
        qualification=['Pin and inspect ife covariance/contrast, remaining survival, fold recombination and SuperLearner/future dependencies.',
            'Resolve source findings through a reviewed upstream version or separately declared patch; retain both original and patched identities.',
            'Compare direct pinned R execution and the proposed worker against exact finite policy laws, with clustered IDs and altered target weights.',
            'Register support, near-support, censoring, competing-event, constant-outcome, weak-nuisance and failure cases before a calibration claim.',
            'Review AGPL obligations and transitive licenses for the actual distribution and network use; a process boundary is not automatic clearance.'],
        reference=ref(BASE / 'exact-policy-results.json', 'Authored finite-law policy oracle; not upstream parity'))
    write(BASE / 'conversion-contract.json', contract)
    omissions = [
        dict(item='Pinned source discrepancies', owner='Prototype author', next_action='Resolve outer-fold ID and documented/effective control semantics with native public/generated fixtures before enabling the engine.'),
        dict(item='Delegates and dependency rights', owner='Build and method reviewers', next_action='Inspect ife uncertainty/contrasts, full survival and recombination; lock and audit dependencies and the chosen distribution terms.'),
        dict(item='Scientific qualification', owner='Method reviewer', next_action='Specify sequential assumptions, policy support, target weights and sampling law; register fresh coverage, width and failure-denominator evaluation.'),
        dict(item='Editorial reconciliation', owner='Monograph author', next_action='Integrate the bounded decision, source findings and worked policy example in the next substantive software release; current reader does not yet contain this review.')]
    write(BASE / 'omissions-register.json', dict(items=omissions, global_blocker=None))
    evidence = [ref(BASE / name, 'Bounded reuse evidence') for name in [
        'plan-review.json', 'identity-review.json', 'tree-identity-review.json', 'source-audit.json', 'inspected-extracts.json',
        'exact-policy-results.json', 'conversion-contract.json', 'omissions-register.json']]
    evidence += [ref(ROOT / 'tools/lmtp_policy_reference_20261022.py', 'Exact arithmetic and separate moment cross-check')]
    decision = dict(operation=OP, status='pass', decision='reference', capabilities=[], integration_allowed=False,
        scope='Retain pinned lmtp as a longitudinal policy-semantics reference and future R comparator; no native integration or calibrated clustered inference is admitted.',
        source=dict(repository='nt-williams/lmtp', commit=PIN, distinct_engine_lineages=1),
        alternatives=[
            dict(choice='pinned_R_worker', disposition='future_candidate', reason='Preserve original estimator and policy semantics after source discrepancies, dependencies and uncertainty are qualified.'),
            dict(choice='immediate_direct_adoption', disposition='not_selected', reason='Unresolved source conversion, outer-fold, control and delegate issues preclude native admission.'),
            dict(choice='port_to_Python_Java_Cxx', disposition='not_selected_initially', reason='No measured requirement offsets policy, learner, RNG, event and uncertainty parity costs.'),
            dict(choice='ltmle_or_gfoRmula', disposition='separate_comparators', reason='Match intervention and event/target law; neither family name grants equivalence or inherited approval.'),
            dict(choice='blanket_rejection', disposition='not_selected', reason='The pinned implementation provides useful technical reference; bounded issues do not establish that every release or method is unusable.')],
        costs='No runtime, ROI or commercial price measured. Include R/dependency setup, rights review, row/history conversion, RNG/fold control, learner fitting, support diagnostics, uncertainty, failed runs and maintenance.',
        owner_obligations=omissions, evidence=evidence, limitations=LIMITS,
        revisit_trigger='A prototype selects this family, source findings are resolved, a release/dependency changes, or a new event/target/sampling law is requested.')
    output = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'decision.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    write(output, decision)
    write(BASE / 'review.json', dict(status='pass_for_bounded_reference_decision',
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        evidence=evidence+[ref(output, 'Canonical reference-only decision')],
        findings=['Seventeen authentic originals bind source identity, AGPL terms and technical behavior.',
            'The control default mismatch was traced to hard-coded TMLE and unbounded SDR calls; no fictitious 100000-valued estimator failure is asserted.',
            'Outer-fold ID naming, inner learner IDs and ife IDs are distinct observations with unresolved native consequences.',
            'Exact two-period net values are 184/25, 456/25 and 107/9 USD under three stipulated policies.',
            'A reference decision passes the proposal contract while native admission and longitudinal coverage remain open.'],
        limitations=LIMITS, native_execution=False, visual_acceptance=False))
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    receipt = run.ledger.receipt_template(node)
    findings = ['Pinned identity, license, declared dependencies and maintenance limits bound; one distinct engine lineage.',
        'Target/uncertainty semantics, source findings, alternative choices, full-workflow costs, owners and revisit trigger are explicit.',
        'Reference-only proposal choice; no integration capability granted. Exact policy oracle and proposed conversion/refusal contract retained.']
    receipt.update(outcome='pass', execution='performed', scope=decision['scope'],
        reviewer=dict(name='Codex author/coordinator', kind='author'), limitations=LIMITS,
        capabilities=[], original_gap_qualification=False, nonexecution_reason='',
        revisit_trigger=decision['revisit_trigger'], outputs=[ref(output, 'Required reuse decision')],
        criteria=[dict(index=i, verdict='pass', finding=finding,
            evidence=evidence+[ref(BASE / 'review.json', 'Author review'), ref(Path(__file__), 'Review generator')])
            for i, finding in enumerate(findings)])
    write(BASE / 'operation-receipt.json', receipt)
    verify_bindings(read(BASE / 'review.json'))
    print(json.dumps(dict(operation=OP, originals=len(originals), anchors=len(anchors), decision='reference', integration_allowed=False)))


if __name__ == '__main__':
    main()
