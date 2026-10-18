#!/usr/bin/env python3
"""Record a source-bounded causaleffect reuse decision without adapter approval."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-18/causaleffect-reuse'
OP = 'SW.DECISION.seed_048'
PIN = 'ff6059fbd4ee6729387e7a4725b560e733ecae7d'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/decision.json')
REVIEWER = dict(name='Codex author/coordinator', kind='author')


def read(path):
    return json.loads(path.read_text())


def exact_reference():
    """Independent finite probability oracle, not an R or ID implementation."""
    joint = {}
    for z in (0, 1):
        p_a = F(1 + 2 * z, 4)
        for a in (0, 1):
            p_y = F(1 + 2 * a + z, 8)
            for y in (0, 1):
                joint[z, a, y] = F(1, 2) * (p_a if a else 1-p_a) * (p_y if y else 1-p_y)
    assert sum(joint.values()) == 1 and all(p > 0 for p in joint.values())
    def conditional_y(a, z=None):
        rows = [(key, p) for key, p in joint.items() if key[1] == a and (z is None or key[0] == z)]
        return sum(p for key, p in rows if key[2] == 1) / sum(p for _, p in rows)
    interventions = [sum(F(1, 2) * conditional_y(a, z) for z in (0, 1)) for a in (0, 1)]
    observational = [conditional_y(a) for a in (0, 1)]
    assert interventions == [F(3, 16), F(7, 16)]
    assert observational == [F(5, 32), F(15, 32)]
    assert interventions[1]-interventions[0] == F(1, 4)
    assert observational[1]-observational[0] == F(5, 16)
    # Two SCMs in the declared graph A -> Y, A <-> Y; faithfulness is not imposed.
    laws = {}
    for model in ('Y_equals_A', 'Y_equals_U'):
        obs = {(0, 0): F(0), (0, 1): F(0), (1, 0): F(0), (1, 1): F(0)}
        do = []
        for u in (0, 1):
            obs[u, u] += F(1, 2)
        for a in (0, 1):
            do.append(sum(F(1, 2) * (a if model == 'Y_equals_A' else u) for u in (0, 1)))
        laws[model] = dict(observed={str(k): str(v) for k, v in obs.items()},
                           interventional_risks=list(map(str, do)), ATE=str(do[1]-do[0]))
    assert laws['Y_equals_A']['observed'] == laws['Y_equals_U']['observed']
    assert [laws[k]['ATE'] for k in laws] == ['1', '0']
    return dict(status='pass', kind='project_authored_exact_probability_reference',
        native_package_executed=False, adapter_executed=False,
        adjustment=dict(graph=['Z->A', 'Z->Y', 'A->Y'],
            joint_probability={str(k): str(v) for k, v in joint.items()},
            interventional_risks=list(map(str, interventions)), ATE='1/4',
            observational_risks=list(map(str, observational)), naive_difference='5/16'),
        nonidentification=dict(graph=['A->Y', 'A<->Y'], worlds=laws,
            conclusion='Identical observational laws permit distinct ATEs; do not emit a point effect under this unrestricted graph.'),
        limitations=['Exact population probabilities under authored SCMs; no estimated confidence intervals or observed banking data.',
                     'These are future adapter comparison oracles; no package, graph converter or expression parser was run.'])


def main():
    assert not BASE.exists() and not OUTPUT.exists()
    audit_path = ROOT/'docs/program/execution/2026-10-18/r-identification/source-audit.json'
    audit = read(audit_path)
    source = next(s for s in audit['sources'] if s['integrated_citation_key'] == 'exec18_rid_causaleffect')
    verify_bindings(source)
    assert source['commit'] == PIN and not source['software_executed'] and not source['rights_qualified']
    for item in source['records']:
        content = (ROOT/item['local_copy']['path']).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        assert blob == item['git_blob_sha1']
    desc = (ROOT/'docs/literature/raw/exec18_rid_causaleffect_0.txt').read_text()
    body = (ROOT/'docs/literature/raw/exec18_rid_causaleffect_2.txt').read_text()
    assert 'License: GPL (>= 2)' in desc and 'Imports: igraph' in desc
    assert 'Version: 1.3.17' in desc and 'Date: 2026-09-19' in desc
    assert 'if (steps) return(list(P = res.prob, steps = res$tree, id = FALSE))' in body
    BASE.mkdir(parents=True)
    plan = dict(status='pass', reviewer=REVIEWER,
        plan=['Bind the five selected original files, their receipts, commit/tree identity and Git blobs; retain the metadata date discrepancy.',
              'Inspect graph encoding, query validation, ID/IDC dispatch, structured success and negative outcomes.',
              'Construct exact adjustment and observational-equivalence references for a later adapter; do not relabel them native calls.',
              'Select a bounded reuse route and document alternatives, costs, ownership and exact remaining qualification work.'],
        review_findings=['The package supplies symbolic identification, not an effect estimator or sampling interval.',
                         'Paired U-tagged arcs must survive graph conversion; flattening them into directed cycles changes the model.',
                         'A caught runtime exception or empty expression cannot establish nonidentification.',
                         'A GPL declaration alone neither grants this integration permission nor proves it impossible.',
                         'Native execution is later adapter qualification; the present inconclusive finding concerns unresolved artifact/rights provenance.'])
    write(BASE/'plan-review.json', plan)
    write(BASE/'source-bindings.json', source)
    write(BASE/'exact-reference.json', exact_reference())
    excerpts = []
    for index, name in [(0, 'package-metadata'), (1, 'query-manual'), (2, 'public-dispatch'), (3, 'ID-recursion'), (4, 'IDC-recursion')]:
        original = ROOT/f'docs/literature/raw/exec18_rid_causaleffect_{index}.txt'
        lines = original.read_text().splitlines()
        target = BASE/(name+'.txt')
        target.write_text('\n'.join(f'{i}: {line}' for i, line in enumerate(lines, 1))+'\n')
        excerpts.append(ref(target, f'Inspected original {original.relative_to(ROOT)} lines 1-{len(lines)}'))
    conversion = [
        'Declare observed node identities and directed versus bidirected edge types separately. Encode a bidirected edge as two opposite igraph edges tagged description="U", preserving parallel edges; check acyclicity on the observed directed graph, not on this encoding.',
        'Require unique names, graph/query membership, disjoint outcome/intervention/conditioning sets and declared causal semantics. Do not silently remove latent tags or infer a DAG from an arbitrary PAG.',
        'For the initial profile use expr=FALSE, steps=TRUE, simp=FALSE, prune=FALSE and stop_on_nonid=FALSE. Empty z selects ID; nonempty z selects IDC. PID, simplification, transport and selection-recovery APIs are separate unqualified profiles.',
        'Parse the structured probability result through a versioned grammar. Preserve bound summation variables, conditioning sets, algorithm, original query and derivation tree; never evaluate a returned LaTeX string as code.',
        'Report identified_formula only after a valid id=TRUE result and validated structured expression. A formula is distinct from a fitted estimate, a confidence interval or validation of the supplied causal graph; conditional support must be checked when evaluating ratios.',
        'Report not_identified only for a completed validated id=FALSE derivation under the declared model class. Retain the tree; do not promise a separately extracted hedge object from this public return without further inspection.',
        'Distinguish invalid graph/query, malformed result, process failure, exhausted resources and cancelled execution from scientific nonidentification. Missing/NULL/empty results without a validated trace are unknown, never numeric zero or a negative certificate.',
        'Preserve exact source/options/input/output hashes, target units and information clock. Any subsequent estimation, numeric support checks and sampling uncertainty need their own qualified method and cannot inherit approval from symbolic ID.'
    ]
    failure = dict(valid_identified='id=TRUE plus validated probability object and derivation',
        valid_nonidentified='id=FALSE plus completed validated derivation under the selected profile',
        negative_default='stop("Not identifiable.", call.=FALSE) in the selected public wrapper',
        suppressed_unstructured='expr=TRUE gives empty string; expr=FALSE gives NULL when steps=FALSE',
        runtime_or_invalid='separate failure/unknown; never scientific nonidentification',
        implemented=False)
    evidence = [ref(audit_path, 'Selected authentic software source audit'),
        ref(BASE/'source-bindings.json', 'Version, license declaration, dependencies, receipts, inspected anchors and claims'),
        ref(BASE/'plan-review.json', 'Reviewed bounded reuse plan'),
        ref(BASE/'exact-reference.json', 'Independent exact probability oracles, not native package execution'),
        ref(Path(__file__), 'Exact decision and oracle construction')]+excerpts
    limits = ['Five pinned selected files and a Git tree are not a complete installed distribution or transitive dependency rights inventory.',
              'GPL(>=2) is a DESCRIPTION declaration; original complete license/distribution path and resolved igraph environment remain unqualified.',
              'DESCRIPTION Date 2026-09-19 differs from commit timestamp 2025-09-19; both are retained without assuming a release history.',
              'No upstream R package execution, expression converter, confidence qualification, port, bank validation or integration permission.',
              'Dated source/commit observations do not establish present maintenance capacity or a support agreement.']
    decision = dict(operation_id=OP, status='inconclusive', decision='reference', integration_allowed=False,
        capabilities=[], reviewer=REVIEWER,
        identity=dict(entry='seed_048:causaleffect', canonical_repository='santikka/causaleffect',
            version='1.3.17', selected_commit=PIN, cutoff='2026-10-07',
            aliases=['causaleffect R package', 'causal.effect public function'],
            distinct_from=['dosearch general do-calculus search', 'cfid counterfactual identification', 'DAGitty graphical adjustment']),
        license=dict(declared='GPL (>= 2)', declaration=source['records'][0]['local_copy'],
            complete_distribution_rights=False, complete_dependency_rights=False,
            interpretation='Do not infer prohibition or permission for a specific embedding/redistribution from this declaration alone.'),
        dependencies=dict(imports=['igraph'], suggests=['R.rsp', 'testthat (>=3.0.0)', 'XML'],
            vignette_builder='R.rsp', package_needs_compilation=False,
            resolved_environment=False, note='NeedsCompilation:no applies to this package, not to all dependencies.'),
        maintenance=dict(selected_commit_timestamp=source['commit_date'],
            description_date='2026-09-19', observed_on='2026-10-18',
            discrepancy_preserved=True, latest_release_or_support_verified=False),
        target='Symbolic P(Y | do(X), Z) for a supplied compatible acyclic latent-confounded graph and observational distribution; no automatic causal discovery or individual counterfactual target.',
        uncertainty='Identification status conditional on the graph/model premises; no fitted effect, confidence interval, posterior or guarantee that the causal graph is true.',
        proposed_route='Retain the original R engine as a symbolic reference and candidate narrow subprocess adapter. Defer direct adoption, embedding and porting until a permissible artifact/environment path and behavioral conformance are established.',
        conversion_contract=conversion, failure_contract=failure,
        alternatives=['DAGitty for graphical adjustment queries where its graph class and estimand suffice.',
            'dosearch for broader declared information sets, preserving incomplete-search status; do not import an ID completeness claim into a timed search.',
            'cfid for counterfactual queries with its own world/input-level semantics.',
            'A separately maintained transparent small-graph oracle for conformance; a complete port would also require graph, symbolic algebra, simplification and failure-case qualification.',
            'Return a nonidentified/unknown disposition when the declared information cannot justify the requested point target.'],
        costs=dict(measured_prices=False, known_requirements=['Pinned R/igraph artifacts and applicable license inventory',
            'Typed graph and probability-object conversion', 'Process startup, serialization, trace storage and resource budgets',
            'Adverse-query regression and version migration', 'Scientific maintenance of target/graph/uncertainty boundaries'],
            unknown=['Actual latency/memory distributions', 'Maintainer availability', 'Support prices and institutional license/deployment review']),
        owner_obligations=['Scientific owner approves graph premises, target, information set and interpretation of a negative result.',
            'Adapter maintainer preserves typed edges, variable identity, derivation/failure distinctions and reproducible environment.',
            'Authorized product/legal owner assesses the actual distribution/deployment path and all dependency notices before enabling integration.'],
        revisit_trigger='Acquire complete authentic selected distribution and license/dependency artifacts; resolve the date discrepancy or retain a bounded historical pin. Run adjustment and nonidentification oracles, an IDC case, name/edge permutations, invalid graph/query, structured-output parsing and resource-failure trials before enabling only that declared adapter profile.',
        evidence=evidence, limitations=limits)
    write(OUTPUT, decision)
    review = dict(status='pass_for_scoped_inconclusive_disposition', reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT, 'Bounded original-language reuse decision'),
        findings=['Identity, five source blobs, declarations, exact options and observed commit history are bound.',
            'An exact adjustment effect of 1/4 differs from the naive 5/16; identical observational worlds have ATE1 versus0.',
            'Structured nonidentification, invalid input and runtime unknown remain distinct; the converter/failure contract is proposed, not implemented.',
            'Reference use is retained; unresolved distribution/rights qualification is explicit and no integration capability is granted.'],
        evidence=evidence, limitations=limits)
    write(BASE/'review.json', review)
    state = core.read(ROOT, core.STATE)
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    receipt = run.ledger.receipt_template(node)
    criteria = [
        ('inconclusive', 'Concrete package/function aliases, pinned source, GPL declaration, direct dependencies and dated maintenance are bound; complete authentic distribution/license/dependency qualification and the metadata date discrepancy remain open.'),
        ('pass', 'Symbolic target and uncertainty semantics, original-language route, alternatives, cost categories, owner duties and concrete revisit trigger are explicit.'),
        ('pass', 'No adapter permission granted. Exact positive/negative population references and a proposed typed conversion/failure contract are retained without claiming native execution.')]
    receipt.update(outcome='inconclusive', execution='performed',
        scope='Source-bounded causaleffect original-language reuse review', reviewer=REVIEWER,
        capabilities=[], outputs=[ref(OUTPUT, 'Contracted causaleffect decision')], limitations=limits,
        nonexecution_reason='', revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i, verdict=v, finding=f, evidence=evidence+[ref(BASE/'review.json', 'Author disposition review')])
                  for i, (v, f) in enumerate(criteria)])
    write(BASE/'operation-receipt.json', receipt)
    print(json.dumps(dict(operation=OP, outcome='inconclusive', decision='reference',
        integration_allowed=False, adjustment_ATE='1/4', naive_difference='5/16',
        observationally_equivalent_ATEs=['1', '0'], native_execution=False)))


if __name__ == '__main__':
    main()
