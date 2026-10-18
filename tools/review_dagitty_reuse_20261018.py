#!/usr/bin/env python3
"""Review a pinned DAGitty proposal route; grant no executable capability."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-18/dagitty-reuse'
OP = 'SW.DECISION.seed_045'
PIN = '7a657776dc8f5e5ba4e323edb028e2c2aaf29327'
OUTPUT = ROOT / f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')


def read(path):
    return json.loads(path.read_text())


def reference():
    """Enumerate authored SCMs with exact fractions, without an upstream call."""
    confounding = {}
    for z in (0, 1):
        pa = F(1 + 2*z, 4)
        for a in (0, 1):
            py = F(1 + 2*a + z, 8)
            for y in (0, 1):
                confounding[z, a, y] = F(1, 2)*(pa if a else 1-pa)*(py if y else 1-py)
    assert sum(confounding.values()) == 1
    def conf_y(a, z=None):
        rows = [(k, p) for k, p in confounding.items() if k[1] == a and (z is None or k[0] == z)]
        return sum(p for k, p in rows if k[2]) / sum(p for _, p in rows)
    adjusted = [sum(F(1, 2)*conf_y(a, z) for z in (0, 1)) for a in (0, 1)]
    naive = [conf_y(a) for a in (0, 1)]
    assert adjusted == [F(3, 16), F(7, 16)]
    assert naive == [F(5, 32), F(15, 32)]

    # A and U independent; A -> C <- U -> Y, Y=U, no A -> Y path.
    collider = {}
    for a in (0, 1):
        for u in (0, 1):
            pc = F(1+2*a+2*u, 8)
            for c in (0, 1):
                collider[a, u, c] = F(1, 4)*(pc if c else 1-pc)
    assert sum(collider.values()) == 1 and min(collider.values()) > 0
    def collider_y(a, c):
        rows = [(k, p) for k, p in collider.items() if k[0] == a and k[2] == c]
        return sum(p for k, p in rows if k[1]) / sum(p for _, p in rows)
    stratum = [collider_y(1, c)-collider_y(0, c) for c in (0, 1)]
    collider_adjusted = sum(sum(p for k, p in collider.items() if k[2] == c)*stratum[c] for c in (0, 1))
    assert stratum == [F(-1, 24), F(-1, 8)] and collider_adjusted == F(-7, 96)

    # A randomized, A -> M -> Y and A -> Y; mediator adjustment changes target.
    mediation = {}
    for a in (0, 1):
        pm = F(1+2*a, 4)
        for m in (0, 1):
            py = F(1+a+2*m, 8)
            for y in (0, 1):
                mediation[a, m, y] = F(1, 2)*(pm if m else 1-pm)*(py if y else 1-py)
    assert sum(mediation.values()) == 1 and min(mediation.values()) > 0
    def mediation_y(a, m=None):
        rows = [(k, p) for k, p in mediation.items() if k[0] == a and (m is None or k[1] == m)]
        return sum(p for k, p in rows if k[2]) / sum(p for _, p in rows)
    total = mediation_y(1)-mediation_y(0)
    mediator_adjusted = sum(sum(p for k, p in mediation.items() if k[1] == m)*(mediation_y(1, m)-mediation_y(0, m)) for m in (0, 1))
    assert total == F(1, 4) and mediator_adjusted == F(1, 8)
    serialize = lambda law: {str(k): str(v) for k, v in law.items()}
    return dict(status='pass', kind='project_authored_exact_probability_reference',
        native_DAGitty_executed=False, browser_Node_R_executed=False,
        confounding=dict(graph=['Z->A', 'Z->Y', 'A->Y'],
            law=serialize(confounding), equations=['P(Z=1)=1/2', 'P(A=1|Z=z)=(1+2z)/4', 'P(Y=1|A=a,Z=z)=(1+2a+z)/8'],
            risks_adjusting_Z=list(map(str, adjusted)), risks_unadjusted=list(map(str, naive)),
            ATE='1/4', naive_difference='5/16'),
        collider=dict(graph=['A->C', 'U->C', 'U->Y'],
            law=serialize(collider), equations=['A,U independent Bernoulli(1/2)', 'P(C=1|A=a,U=u)=(1+2a+2u)/8', 'Y=U'],
            ATE='0', differences_conditioning_C=list(map(str, stratum)), standardized_difference=str(collider_adjusted),
            conclusion='The empty adjustment set is valid; conditioning on the collider creates association despite positive stratum support.'),
        mediator=dict(graph=['A->M', 'M->Y', 'A->Y'], law=serialize(mediation),
            equations=['P(A=1)=1/2', 'P(M=1|A=a)=(1+2a)/4', 'P(Y=1|A=a,M=m)=(1+a+2m)/8'],
            total_effect=str(total), difference_standardized_over_marginal_M=str(mediator_adjusted),
            conclusion='An observed descendant on the causal path must not be included as a total-effect adjustment covariate.'),
        limits=['Finite population references under declared authored SCMs; no data estimation, confidence calibration or observed bank/model performance.',
                'No graph parser, adjustment enumeration or native wrapper has been executed. These are future conformance oracles, not evidence of upstream behavior.'])


def main():
    assert not OUTPUT.exists()
    assert read(BASE/'plan-review.json')['plan_review']['status'] == 'pass_to_execute'
    current_audit = ROOT/'docs/program/execution/2026-10-18/census-frameworks-v1/reader/source-audit.json'
    inherited = [s for s in read(current_audit)['sources'] if s['integrated_citation_key'] in ('exec13_other_dagitty', 'exec14_olatent_dagitty')]
    assert len(inherited) == 2
    verify_bindings(inherited)
    commit_file = ROOT/'docs/literature/raw/exec13_other_commit_dagitty.json'
    tree_file = ROOT/'docs/literature/raw/exec13_other_tree_dagitty.json'
    commit = read(commit_file)[0]
    tree = read(tree_file)
    assert commit['sha'] == PIN and commit['commit']['committer']['date'] == '2024-12-06T12:57:41Z'
    assert not tree['truncated'] and len(tree['tree']) == 261
    blobs = {r['path']: r['sha'] for r in tree['tree'] if r['type'] == 'blob'}
    selected = [
        ('README.md', 'exec13_other_file_dagitty_0', '1-46: shared core, local GUI and remote save/load, R/V8 boundary'),
        ('LICENSE.txt', 'exec13_other_file_dagitty_1', 'GPLv2 full text, distribution/source/modification conditions and warranty disclaimer'),
        ('jslib/graph/Graph.js', 'exec13_other_file_dagitty_2', '1-139: typed graph and source/target/adjustment/latent/selection properties'),
        ('jslib/graph/GraphAnalyzer.js', 'exec13_other_file_dagitty_3', '385-443: adjustment/query/selection behavior;1594-1640: graph validation and MAG/PAG TODOs'),
        ('jslib/graph/GraphTransformer.js', 'exec14_other_latent_dagitty_0', '1418-1445: clone, endpoint conversion and graph-type change'),
        ('test/test/pags.js', 'exec14_other_latent_dagitty_1', '1-62: collider/conditioning assertions and capped enumeration; inspected only'),
        ('r/DESCRIPTION', 'exec18_reuse_dagitty_0', '1-44: version0.3-4, Date2023-12-07, GPL-2, R/import/suggest declarations'),
        ('r/R/dagitty.R', 'exec18_reuse_dagitty_1', '1-8 imports;1025-1209 adjustment API, query checks, total/direct and enumeration cap'),
        ('jslib/Makefile', 'exec18_reuse_dagitty_2', '1-41: core/parser/build order, browser/Node/R output routes'),
        ('jslib/graph/Class.js', 'exec18_reuse_dagitty_3', '1-67: inheritance helper, MIT declaration and Node export'),
        ('jslib/graph/Hash.js', 'exec18_reuse_dagitty_4', '1-54: GPL2-or-later header and Underscore usage'),
        ('jslib/graph/underscore-min.js', 'exec18_reuse_dagitty_5', '1-4: Underscore1.8.3 MIT declaration; no execution or full minified-code review'),
        ('jslib/underscore-min.js', 'exec18_reuse_dagitty_6', '2-5: Underscore1.13.1 MIT declaration; no execution or full minified-code review'),
        ('test/package.json', 'exec18_reuse_dagitty_7', '1-9: test-only qunit^2.18.0 and underscore^1.13.2 declarations'),
    ]
    records = []
    for remote, local, anchor in selected:
        path = ROOT/f'docs/literature/raw/{local}.txt'
        receipt_path = ROOT/f'docs/literature/raw/{local}.receipt.json'
        data = path.read_bytes()
        receipt = read(receipt_path)
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        url = f'https://raw.githubusercontent.com/jtextor/dagitty/{PIN}/{remote}'
        assert receipt['status'] == 'saved' and receipt['url'] == url
        assert receipt['sha256'] == core.sha(path) and blob == blobs[remote], remote
        records.append(dict(source_identity=url, version_date=commit['commit']['committer']['date']+'; '+PIN,
            accessed_utc=receipt['accessed_utc'], git_blob_sha1=blob,
            local_copy=ref(path, anchor), receipt=ref(receipt_path, 'Authentic bounded public acquisition'),
            inspected_anchors=[anchor], executed=False))
    desc = (ROOT/'docs/literature/raw/exec18_reuse_dagitty_0.txt').read_text()
    wrapper = (ROOT/'docs/literature/raw/exec18_reuse_dagitty_1.txt').read_text()
    analyzer = (ROOT/'docs/literature/raw/exec13_other_file_dagitty_3.txt').read_text()
    assert all(t in desc for t in ['Version: 0.3-4', 'Date: 2023-12-07', 'License: GPL-2', 'V8,', 'jsonlite,'])
    assert 'Both exposure(s) and outcome(s) need to be set!' in wrapper
    assert 'TODO implement proper MAG validation' in analyzer and 'TODO implement proper PAG validation' in analyzer
    imports = ['V8', 'jsonlite', 'boot', 'MASS', 'methods', 'grDevices', 'stats', 'utils', 'graphics']
    suggests = ['igraph', 'knitr', 'base64enc (>= 0.1-3)', 'testthat', 'markdown', 'rmarkdown', 'lavaan', 'CCP', 'fastDummies']
    limits = [
        'Fourteen authentic selected files and a complete tree support a bounded proposal selection, not a complete distribution, resolved executable environment or transitive-rights inventory.',
        'Root GPLv2 text, R GPL-2 declaration, a GPL2-or-later file header and MIT helper declarations retain their own scopes; blanket rights for a specific product arrangement are not inferred.',
        'Two vendored Underscore versions and a third test dependency range are distinct observations. Their presence alone proves no version vulnerability, runtime loading path or interchangeability.',
        'No browser, Node, R or upstream test execution; no adapter permission, effect estimate, confidence guarantee, graph discovery or verified bank causal premises.',
        'The selected commit is dated2024 and R DESCRIPTION dated2023. These establish historical identity, not present maintenance capacity or a support contract.',
        'This new reuse record is program evidence; its additional source findings are not yet merged into a successor of the current1068-page monograph.'
    ]
    audit = dict(kind='software_primary_sources', title='DAGitty pinned reuse-route and wrapper review',
        source_identity='https://github.com/jtextor/dagitty', selected_commit=PIN,
        commit_tree_sha=commit['commit']['tree']['sha'], recursive_tree_response_sha=tree['sha'],
        cutoff='2026-10-07', version_date='R0.3-4 /2023-12-07; selected repository commit2024-12-06',
        local_copy=ref(ROOT/'docs/literature/raw/exec18_reuse_dagitty_0.txt', 'Original package identity and declarations'),
        records=records, identity_evidence=[ref(commit_file, 'Commit/date/root tree identity'), ref(tree_file, 'Complete261-entry selected tree')],
        inherited_records=inherited,
        supported_claims=[
            'Browser and R surfaces use the shared JavaScript core; wrapper preconditions differ and must be reviewed separately.',
            'The selected R package declares GPL-2, R>=3.0.0, nine imports and nine suggests; these declarations are not an installed lockfile.',
            'The R adjustment entry points reject missing exposure/outcome, while the JavaScript boolean check returns false in that case.',
            'Minimal enumeration accepts max.results; a cap must not be reported as exhaustive enumeration or global absence of an adjustment set.',
            'Graph validation leaves proper MAG/PAG validation TODO; internal PAG conversion changes endpoints and graph type.',
            'The tree/build/helper sources expose multiple Underscore versions and third-party notice boundaries; no runtime or complete license closure is claimed.'
        ], software_executed=False, rights_qualified=False, limitations=limits)
    write(BASE/'source-audit.json', audit)
    write(BASE/'exact-reference.json', reference())
    conversion = dict(status='proposed_not_implemented', preferred_profile='Pinned R original-language wrapper, supplied fully observed directed acyclic graph, single exposure/outcome, total-effect adjustment',
        requirements=[
            'Bind a bijection between application and graph variable names, graph revision, information clock, measured units and analyst-owned causal assumptions.',
            'Validate graph syntax, directed acyclicity, unique existing distinct exposure/outcome, candidate covariate membership and disjointness before the wrapper call. Restrict this initial profile to observed nodes and directed edges, without latent/selection flags.',
            'Specify effect=total and the exact enumeration type/max.results. Treat query-set validation and set enumeration as different outputs. Finite capped enumeration must carry truncated_or_exhaustiveness_unknown unless a separate complete stopping certificate exists.',
            'Preserve source, target, adjusted, latent and selected annotations on stored input even when unsupported annotations cause this profile to refuse. No silent deletion of flags, edge types or unresolved endpoints.',
            'Do not use pagToPdag to manufacture a fully oriented scientific graph. MAG/PAG/PDAG, direct effects, odds-ratio queries, instruments and simulation require separate profiles and references.',
            'Keep returned set members and the original graph/query; a valid adjustment set gives a conditional identification route, not an estimated effect, uncertainty interval or verification that the graph is true.',
            'For later numerical evaluation require consistency, valid intervention interpretation, positivity and an estimator/uncertainty argument under its sampling law. Do not attribute those guarantees to the graph tool.'
        ], failures=dict(
            valid_set='validated completed call confirms this covariate set under the supplied compatible graph; no causal-graph truth guarantee',
            invalid_set='this candidate set fails the adjustment check; not general nonidentification of the causal query',
            no_sets='claim no adjustment route only after validated complete enumeration under the declared profile; general ID may still succeed',
            invalid_query='missing exposure/outcome, absent names, cycle, unsupported graph/flags or malformed set: reject before inference',
            runtime='exceptions, timeout, cancellation, bridge parse failures and missing output remain execution unknown',
            representation='a list with one empty set is a valid unadjusted solution; an empty result list is different; verify exact wrapper conversion in native conformance',
            unresolved_core_false='raw JavaScript false without validated query completion is insufficient to infer a scientific negative'))
    write(BASE/'conversion-contract.json', conversion)
    evidence = [ref(BASE/'plan-review.json', 'Reviewed proposal plan'), ref(BASE/'source-audit.json', 'Fourteen authenticated blobs and bounded primary-source claims'),
        ref(BASE/'exact-reference.json', 'Three independent exact SCM oracles; no native execution'),
        ref(BASE/'conversion-contract.json', 'Proposed selected conversion and failure contract'),
        ref(BASE/'failed-acquisition-sandbox.json', 'Preserved DNS failure before successful authorized fixed-collector retry'),
        ref(Path(__file__), 'Exact source checks and authored reference computation')]
    decision = dict(operation_id=OP, status='pass', decision='defer',
        decision_scope='Complete a source-bounded proposal selection; defer executable adapter admission and retain the pinned engine as a reference.',
        preferred_proposal_route=conversion['preferred_profile'], integration_allowed=False, capabilities=[],
        runtime_qualification=False, deployment_allowed=False, original_gap_qualification=False,
        identity=dict(canonical_repository='jtextor/dagitty', entry='seed_045:DAGitty', selected_commit=PIN,
            package_version='0.3-4', package_date='2023-12-07', cutoff='2026-10-07',
            aliases=['DAGitty JavaScript core', 'DAGitty browser GUI', 'dagitty R package'],
            alias_boundary='Interfaces share a core but have distinct wrappers, build inputs and precondition behavior; they are not independent discovery engines.'),
        license=dict(root='GNU GPL version2 full text', package_declaration='GPL-2',
            hash_helper='GPL version2 or later header', class_helper='MIT Licensed declaration',
            underscore_helpers='MIT declarations at selected1.8.3 and1.13.1 files',
            permissible_selected_embedding_verified=False, complete_distribution_or_transitive_rights=False,
            interpretation='Preserve applicable notices and actual corresponding-source/distribution duties; a subprocess or browser boundary alone is not a license exemption.'),
        dependencies=dict(R='>=3.0.0', imports=imports, suggests=suggests, vignette_builder='knitr',
            JS_observed=['graph/underscore-min.js1.8.3', 'jslib/underscore-min.js1.13.1', 'Class.js', 'Hash.js', 'generated parser/core concatenation'],
            test_only=dict(qunit='^2.18.0', underscore='^1.13.2'), resolved_environment=False,
            boundary='Do not mix browser/Node/R generated artifacts or borrow the test dependency range as a production lock.'),
        maintenance=dict(commit_date='2024-12-06T12:57:41Z', package_date='2023-12-07', observation_date='2026-10-18',
            current_support_or_latest_release_verified=False, comment='README reports infrequent CRAN updates; this is an historical author statement, not a verified current maintenance conclusion.'),
        target_and_uncertainty='Graphical adjustment for a supplied causal graph and declared total-effect query. No automatic discovery, fitted effect, calibrated graph/effect uncertainty or verified causal premises.',
        reason=[
            'The pinned shared core, original license and direct dependency/build/wrapper declarations support a concrete proposal route without prior bank or prototype evidence.',
            'A narrow original-language wrapper avoids assuming that an implementation port preserves adjustment semantics; no measured embedding need justifies a port now.',
            'R query checks are stronger than the selected raw JavaScript boolean boundary for missing endpoints. The chosen wrapper and future native comparisons must be explicit.',
            'General graph-class and ambiguity-removing transformations exceed the preferred initial profile. Keep graph authoring and analyst approval separate from identification and estimation.',
            'Deferring executable admission is a prototype obligation, not a reason to block other proposal research or declare this proposal choice unresolved.'
        ],
        alternatives=[
            dict(route='Unrestricted adoption of GUI, R and all graph classes', disposition='reject_for_initial_profile', reason='Distinct wrappers, graph validation limits and unsupported estimands would share an unjustified blanket guarantee.'),
            dict(route='Port adjustment algorithms to Python/C++', disposition='defer', reason='Would duplicate parser, graph, algorithm and regression obligations without a demonstrated deployment constraint.'),
            dict(route='Pinned direct Node or local browser use', disposition='retain_separate_candidate', reason='Requires its own artifact loading, dependency, error and data-flow review. Default remote graph save/load must not be assumed local.'),
            dict(route='causaleffect or dosearch', disposition='separate_symbolic_ID_reference', reason='Some identifiable effects lack an adjustment formula. Each engine has its own graph/input completeness and failure contract.'),
            dict(route='Human-reviewed explicit DAG and transparent small oracle', disposition='retain_baseline', reason='Makes premises and invalid conditioning visible while claiming no automatic graph truth.')
        ],
        costs_to_measure=['Pinned R/V8 and generated JS build retention', 'Conversion and analyst graph review',
            'Enumeration growth, startup, latency and memory including failed requests', 'Complete notices and transitive dependency inventory',
            'Version migration and adverse-query regression', 'Separate estimation, support and uncertainty qualification'],
        measured_prices_or_bank_ROI=False,
        owner_obligations=dict(scientific_owner='Own the graph assumptions, total-effect estimand, time ordering, selected covariates, positivity and interpretation of refusal.',
            adapter_maintainer='Own the exact wrapper/generated artifacts, lockfile, typed query checks, truncation and failure distinctions, and native conformance.',
            product_rights_owner='Review the actual dependency/distribution path and third-party notices before admitting executable reuse.'),
        revisit_trigger='Acquire and bind the complete selected R/V8/generated-core distribution and dependency/notice inventory; compare native valid-empty-set, confounding, collider, mediator, invalid names/query, cycles, capped enumeration, parse errors and resource failures against the declared contract. A new revision, graph class, wrapper or deployment arrangement reopens review.',
        evidence=evidence, limitations=limits, reviewer=REVIEWER, bank_inputs_required_for_next_step=False)
    write(OUTPUT, decision)
    review = dict(status='pass_for_scoped_proposal_decision', reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT, 'Completed proposal choice, no executable capability'),
        findings=['Fourteen selected original blobs match one pre-cutoff revision and every acquisition receipt.',
            'R0.3-4, the GPL/MIT notice boundaries, nine imports/nine suggests and distinct JS/test versions are recorded.',
            'The selected wrapper/query, total/direct, cap, graph validity and scientific-negative distinctions have a concrete proposed contract.',
            'Exact authored references reproduce1/4 versus5/16; collider adjustment gives-7/96 despite true0; mediator adjustment gives1/8 versus total1/4.',
            'A narrow proposal route is selected without requiring bank data or prior prototype merit; executable admission is explicitly deferred.'],
        evidence=evidence, limitations=limits)
    write(BASE/'review.json', review)
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    findings = [
        'Source/aliases, pre-cutoff commit, original root and file-specific licenses, direct R/JS/test dependencies and bounded historical maintenance observations are bound; unresolved transitive/runtime qualification is not represented as complete.',
        'The supplied-graph total-effect target, uncertainty limits, original-language route, alternatives, costs, owners and exact prototype revisit triggers are explicit.',
        'No integration_allowed capability is granted. Deferred executable admission is supported by authored exact oracles and a proposed typed conversion/failure contract; no native execution or rights closure is claimed.'
    ]
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'], reviewer=REVIEWER,
        capabilities=[], outputs=[ref(OUTPUT, 'Contracted DAGitty proposal reuse decision')], limitations=limits,
        nonexecution_reason='', revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i, verdict='pass', finding=f, evidence=evidence+[ref(BASE/'review.json', 'Author decision review')]) for i, f in enumerate(findings)])
    write(BASE/'operation-receipt.json', receipt)
    verify_bindings([audit, decision, receipt])
    print(json.dumps(dict(operation=OP, outcome='pass', scope='proposal_selection_only',
        original_blobs=len(records), decision='defer_executable_admission', integration_allowed=False,
        exact_reference_groups=3, upstream_execution=False)))


if __name__ == '__main__':
    main()
