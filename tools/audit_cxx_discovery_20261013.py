#!/usr/bin/env python3
"""Preserve inspected C++ survey evidence without crediting downloaded-only text."""
import base64
import hashlib
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/cxx-discovery'
RAW = ROOT / 'docs/literature/raw'


def ref(path, anchor):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return {'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
            'anchor': anchor}


def write(name, data):
    (BASE / name).write_text(json.dumps(data, indent=2) + '\n')


def source(stem, anchor):
    receipt = RAW / (stem + '.receipt.json')
    r = json.loads(receipt.read_text())
    assert r['status'] == 'saved', stem
    p = ROOT / r['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == r['sha256']
    record = {'source_identity': r['url'], 'accessed_utc': r['accessed_utc'],
              'retrieval_receipt': ref(receipt, 'Original public acquisition receipt'),
              'original_response': ref(p, 'Unmodified fetched bytes')}
    if p.suffix == '.json':
        value = json.loads(p.read_text())
        if isinstance(value, dict) and value.get('encoding') == 'base64':
            body = base64.b64decode(value['content'])
            decoded = BASE / 'primary' / (stem + '.txt')
            if decoded.exists():
                assert decoded.read_bytes() == body
            else:
                decoded.write_bytes(body)
            blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            assert blob == value['sha'], stem
            record.update(git_blob_sha1=blob, decoded_response_identity_verified=True)
            p = decoded
    record['local_copy'] = ref(p, anchor)
    record['inspected_anchors'] = [anchor]
    return record


def main():
    pins = {p['index']: p for p in json.loads((BASE / 'cutoff-pins.json').read_text())}
    groups = []

    def group(key, title, owner, version, records, claims, limitations):
        inspected = [source(stem, anchor) for stem, anchor in records]
        groups.append({'integrated_citation_key': 'exec13_cxx_' + key,
                       'kind': 'software_primary_sources', 'title': title, 'author': owner,
                       'year': 2026, 'version_date': version + '; inspected 2026-10-13; cutoff 2026-10-07',
                       'source_identity': inspected[0]['source_identity'], 'local_copy': inspected[0]['local_copy'],
                       'records': inspected, 'inspected_anchors': [r['local_copy'] for r in inspected],
                       'supported_claims': claims, 'limitations': limitations})

    def version(i, extra=''):
        p = pins[str(i)]
        return p['repo'] + '; ' + p['sha'] + '; ' + p['committed_at'] + ('; ' + extra if extra else '')

    group('agrum', 'aGrUM native discovery interfaces, tests, score and license', 'aGrUM contributors',
          '3.2.0; 2ec71906f4108684c5cfb96d1d44f2925e16a32e; commit 2026-10-06T17:21:03Z', [
              ('exec13_cxx_agrum_ibase', 'usePC/useFCI and useChi2Test/useG2Test declarations, lines 818-938'),
              ('exec13_cxx_agrum_ibase_cpp', 'preparePC_ lines 716-801; learnPDAG/learnPAG lines 893-954; missing structure data check'),
              ('exec13_cxx_agrum_ci', 'learnSkeleton lines 126-235; stable delayed deletion and p-value comparison'),
              ('exec13_cxx_agrum_pc', 'learnMixedStructure lines 65-70; skeleton, constraints and unshielded colliders'),
              ('exec13_cxx_agrum_constraint', 'learnPDAG/learnDAG lines 137-143; distinct Meek completion calls'),
              ('exec13_cxx_agrum_bic', 'ScoreBIC::score_ lines 131-202; discrete count likelihood and penalty'),
              ('exec13_cxx_agrum_learner_tpl', 'useGreedyHillClimbing/useK2/useMIIC/usePC lines 963-1019'),
              ('exec13_cxx_agrum_mit', 'Full permissive license with notice-retention conditions'),
              ('exec13_cxx_agrum_lgpl', 'LGPL-3.0 alternative license; selected headers use LGPL-3.0-or-later OR MIT')],
          ['Native BNLearner exposes distinct score and CI paths; the inspected PC setup uses Chi-square or G-square tests.',
           'learnPDAG and learnDAG call different completion routines; selecting a DAG does not certify its orientation.',
           'Structure learning rejects missing database values in the inspected branches; EM is not evidence of arbitrary missing-structure support.',
           'Selected headers have LGPL-3.0-or-later OR MIT identifiers, with both saved terms.'],
          ['No native build, speed, CI calibration or causal identification trial.',
           'Dependency terms and binary distribution remain a prototype packaging decision; FCI is separately scoped.'])
    group('openbnsl', 'OpenBNSL categorical PC, CI, graph encoding and build sources',
          'OpenBNSL contributors', version(7), [
              ('exec13_cxx_lead_7_readme', 'Categorical-only scope; Features distinguish CPU PC from unchecked GPU-PC entry'),
              ('exec13_cxx_lead_7_source_1', 'CMake lines 1-57; C++20, Python, OpenMP, Boost, pybind11 and optional CUDA'),
              ('exec13_cxx_lead_7_source_20', 'PC skeleton lines 29-114; delayed updates; completion lines 125-146'),
              ('exec13_cxx_lead_7_source_22', 'pybind API arguments including max_cond_vars and timeout_sec'),
              ('exec13_cxx_lead_7_source_23', 'CI dispatch lines 21-38; observed strata, correction and return lines 75-141'),
              ('exec13_cxx_lead_7_source_24', 'Directed versus undirected edges lines 33-51; child-indexed parent bits lines 70-80'),
              ('exec13_cxx_lead_7_license', 'Full MIT license')],
          ['C++ core plus Python binding; categorical data and explicit conditioning limits.',
           'The inspected CI routine dispatches Chi-square, G-square or oracle d-separation.',
           'The selected path applies a Yates adjustment when a stratum has one degree of freedom, including the G-square branch.',
           'Parent bit storage is indexed by child; public ordered edge arguments are source then target.',
           'CUDA build support alone does not establish implemented GPU-PC.'],
          ['Saved benchmark timings are authors\' reports and are not reproduced here.',
           'Timeout/failure semantics, degenerate strata and CI distribution require prospective runtime checks.'])
    group('rcausalmgm', 'rCausalMGM mixed-data native backend and R contract',
          'Tyler C Lovelace, Max Dudek, Jack Fiore and Panayiotis V Benos', version(4, '1.0.1'), [
              ('exec13_cxx_lead_4_source_0', 'DESCRIPTION: release, GPL-3, Rcpp/Armadillo/Thread/BH linkage'),
              ('exec13_cxx_lead_4_source_1', 'pcStable arguments and CPDAG return; missing rows dropped; initial skeleton'),
              ('exec13_cxx_lead_4_source_2', 'adjMat2Graph directed defaults to FALSE; documentation does not specify endpoint convention'),
              ('exec13_cxx_lead_4_source_3', 'PcStable::search, FasStableProducerConsumer and collider/Meek routing, lines 41-144'),
              ('exec13_cxx_lead_4_source_4', 'IndTestMulti constructors and regression dispatch, lines 4-95 and 221-279'),
              ('exec13_cxx_lead_4_source_5', 'Makevars OpenMP and BLAS/LAPACK linkage')],
          ['The selected native backend is R-hosted; PC-Stable returns a CPDAG under causal sufficiency.',
           'The documented initial skeleton and dropped missing rows are scientifically material choices.',
           'Keep distinct regression CI, graph conventions and declared data types when integrating.'],
          ['No mixed/censored calibration or FCI assessment; a package name is not a standalone C++ contract.',
           'Exact converter orientation needs its delegated implementation and a runtime fixture before adoption.'])
    group('ccdr', 'ccdrAlgorithm regularized Gaussian discovery and Rcpp boundary',
          'Bryon Aragam and Dacheng Zhang', version(6, '0.0.5'), [
              ('exec13_cxx_lead_6_source_0', 'DESCRIPTION: Gaussian scope, dependencies, GPL >= 2 and upstream alias'),
              ('exec13_cxx_lead_6_source_1', 'ccdr.run data, lambdas, gamma, alpha, sigmas and path semantics'),
              ('exec13_cxx_lead_6_source_2', 'CCDrAlgorithm state and stopping flags'),
              ('exec13_cxx_lead_6_source_3', 'gridCCDr Rcpp conversion and path return, lines 54-96')],
          ['The selected release returns a regularization path and uses Rcpp with sparsebnUtils.',
           'gamma chooses MCP or L1; alpha is an edge-count stopping threshold, not a CI significance level.',
           'The documented data must be numeric without missing values.'],
          ['Old pinned release; upstream alias consistency and full build remain open.',
           'The software record supports implementation scope, not a fresh review of its cited scholarly theorem.'])
    group('bnsl', 'BNSL source and score-selection interface', 'Joe Suzuki and Jun Kawahara',
          version(10, '0.1.4'), [
              ('exec13_cxx_lead_10_source_0', 'DESCRIPTION: Rcpp, bnlearn, igraph, GPL >= 2'),
              ('exec13_cxx_lead_10_source_1', 'bnsl proc/tw/ss arguments and bn-class return'),
              ('exec13_cxx_lead_10_source_2', 'aster.cpp Rcpp export and queue/heuristic score search, lines 1-112')],
          ['R-hosted structure search with declared score and parent-set limits; native exported search exists.'],
          ['No standalone ABI, optimality, runtime or calibrated intervention claim.'])
    group('breaking', 'Breaking Bad distributed search, graph representation and missing scorer',
          'LG AI Research', version(0), [
              ('exec13_cxx_lead_0_readme', 'Public Release Notice and BIC scorer reconstruction instructions'),
              ('exec13_cxx_lead_0_source_20', 'Search::run_research and incoming-parent deletion operators'),
              ('exec13_cxx_lead_0_source_21', 'Separate directed edges, undirected neighbors and parent/child accessors, lines 35-85'),
              ('exec13_cxx_lead_0_source_22', 'BICScoreloader lines 1-49; explicit unimplemented throwing function'),
              ('exec13_cxx_lead_0_source_23', 'CMake C++23 declaration'),
              ('exec13_cxx_lead_0_license', 'BSD-3-Clause-LG AI Research License: custom text and notice conditions')],
          ['The inspected distributed scorer is a throwing placeholder with instructions to obtain XGES code.',
           'Native search and PDAG code are present; the release is not a complete executable benchmark as distributed.',
           'The custom top-level license is not a blanket license for every referenced dependency.'],
          ['No runtime trial; no confirmation of published speed or accuracy.',
           'Original paper is not cited as technical support here; paper acquisition remains a literature task.'])
    group('svidag', 'SVI-DAG selected implementation language and dependency contract',
          'SVI-DAG contributors', version(1), [
              ('exec13_cxx_lead_1_readme', 'Environment and src/svidag model path; stated GPU/CPU routes'),
              ('exec13_cxx_lead_1_source_0', 'JAX/Flax imports and SVIDAGModel lines 8-39; hard/relaxed adjacency lines 94-149'),
              ('exec13_cxx_lead_1_license', 'Apache License version 2.0')],
          ['The inspected model is Python/JAX/Flax, despite the repository-level C++ search classification.'],
          ['No claim that the whole repository lacks native code; bundled baselines are not independently audited.',
           'No Bayesian calibration or theorem claim; named paper remains an unacquired literature lead.'])
    group('other_leads', 'Additional finite-query candidates and selected native routines',
          'Named repository contributors', '; '.join(version(i) for i in [2, 3, 5, 8, 9]), [
              ('exec13_cxx_lead_2_readme', 'Post-nonlinear experiment description and author-stated impractical computation'),
              ('exec13_cxx_lead_2_license', 'MIT terms for this release'),
              ('exec13_cxx_lead_3_readme', 'Documented conditional-entropy rule and threshold 0.08'),
              ('exec13_cxx2_3_source_0', 'COJEC.cpp lines 266-269: PXY*(log(PXY)/log(PX)) and count > 9; not the standard full conditional entropy'),
              ('exec13_cxx_lead_5_readme', 'Header-only probabilistic library and compiler description'),
              ('exec13_cxx2_5_source_0', 'stepwise_structure lines 23-37 and 76-110; cluster learning and merging'),
              ('exec13_cxx2_5_source_1', 'stepwise_structure_hc search object and score-based cluster learning'),
              ('exec13_cxx_lead_5_license', 'MIT terms'),
              ('exec13_cxx_lead_8_readme', 'Incremental/offline user directions'),
              ('exec13_cxx2_8_source_0', 'run.cpp calls Train, emits DAG/matrix and waits for input, lines 60-130'),
              ('exec13_cxx_lead_9_readme', 'BN_SMC Boost and compiler requirements'),
              ('exec13_cxx2_9_source_0', 'SMC::Update lines 49-99; OpenMP loop and best-score tracking'),
              ('exec13_cxx_lead_9_license', 'GNU GPL version 3 license text')],
          ['godai0519/BayesianNetwork includes native structure-learning templates; README inference emphasis is not evidence of absence.',
           'COJEC documented rule cannot establish a causal effect from conditional entropy alone; the inspected formula also differs from full conditional entropy.',
           'Incremental and SMC candidates have source paths but no adopted statistical/operating contract in this proposal.'],
          ['COJEC and incremental rights remain unresolved after API failures and tree inspection.',
           'Post-nonlinear experiment source/build provenance and delegated routines are incomplete.',
           'No candidate was executed; a rejection for present adoption does not establish algorithmic incapability.'])
    xges = json.loads((RAW / 'exec13_cxx2_xges_commit.json').read_text())[0]
    group('xges', 'XGES native score, search and command-line contract', 'Achille Nazaret and XGES contributors',
          xges['sha'] + '; ' + xges['commit']['committer']['date'], [
              ('exec13_cxx2_xges_readme', 'Separate Python and C++ implementations; arbitrary DAG extension description'),
              ('exec13_cxx2_xges_source_0', 'fit_xges lines 35-55; optional extended edge deletion search'),
              ('exec13_cxx2_xges_source_1', 'Gaussian covariance and BIC computation lines 6-85; unused intervention-index overload'),
              ('exec13_cxx2_xges_source_2', 'PDAG directed and undirected getters, parent and child accessors'),
              ('exec13_cxx2_xges_source_3', 'Command-line npy input, BIC alpha default 2 and output file')],
          ['A separate C++ implementation exists with Gaussian residual-variance BIC scoring and a command-line entrypoint.',
           'Its alpha multiplies the BIC complexity penalty, so cannot be mapped to a PC significance threshold.',
           'The inspected covariance overload ignores its intervention-index parameter; it does not establish support for interventional scoring.',
           'An arbitrary DAG extension is not a uniquely discovered causal direction.'],
          ['No full license file identified in the inspected cutoff tree; no redistribution or source-port permission inferred.',
           'No runtime claim or reproduction of advertised speed advantage; positive residual/LLT failure behavior needs evaluation.'])
    lges = json.loads((RAW / 'exec13_cxx2_lges_commit.json').read_text())[0]
    group('lges', 'LGES upstream identity and nested implementation terms', 'LGES and nested GES contributors',
          lges['sha'] + '; ' + lges['commit']['committer']['date'], [
              ('exec13_cxx2_lges_readme', 'Python quick start and top-level MIT assertion'),
              ('exec13_cxx2_lges_source_0', 'Nested Python GES source BSD notice and fit entrypoints, lines 1-113'),
              ('exec13_cxx2_lges_source_1', 'Nested GES BSD license text')],
          ['The inspected upstream path is Python; an algorithm name in a C++ derivative does not establish a separate upstream native implementation.',
           'Top-level README MIT assertion and nested BSD terms must remain distinct.'],
          ['Root license API returned 404; nested GES license is not proof of root grant.',
           'No evaluation of LGES theoretical guarantees or experimental superiority.'])
    group('inference', 'libDAI and OpenGM discrete inference documentation and terms',
          'libDAI and OpenGM contributors',
          'libDAI mirror 6df66a8ce7eb6f669bae933ab6ec35bbba56182f (2012-05-16), README 0.3.0 (2011); OpenGM decdacf4caad223b0ab5478d38a855f8767a394f (2019-07-26)', [
              ('v12_sw_pinned_readme_libdai', 'About libDAI discrete factor-graph inference; 0.3.0 and old GPL/license transition'),
              ('exec13_cxx_libdai_license', 'BSD-2-Clause notice and distribution conditions'),
              ('exec13_cxx_opengm_readme', 'Unmaintained title; discrete factor-graph representation, optimization and inference'),
              ('exec13_cxx_opengm_license', 'MIT terms')],
          ['These inspected releases provide discrete graphical-model inference/optimization roles, not evidence of a causal-discovery/effect-identification workflow.'],
          ['Old mirror snapshots are not claims about all current upstream versions.',
           'No ecosystem-wide absence claim; inference may be useful behind an independently justified causal model.'])

    groups.append({'integrated_citation_key': 'exec13_cxx_examples', 'kind': 'project_derivation',
                   'title': 'Exact orientation, equivalence, entropy and coarsening examples',
                   'author': 'Causal banking proposal project', 'year': 2026,
                   'version_date': '2026-10-13; exact rational constructions; no vendor execution',
                   'source_identity': 'Project code and reproducible exact outputs',
                   'local_copy': ref(BASE / 'exact-results.json', 'Four exact project constructions'),
                   'inspected_anchors': ['funding, equivalence, entropy and coarsening outputs; exact code assertions'],
                   'code': ref(ROOT / 'tools/cxx_discovery_examples_20261013.py', 'Gauss-Jordan, topological and law-enumeration references'),
                   'supported_claims': ['A matrix transpose loses a synthetic USD100000 effect; six permutations and independent substitution agree.',
                                        'Identical Gaussian covariance permits effects USD0 or USD200000.',
                                        'Zero conditional entropy permits causal effects zero or one.',
                                        'Coarsening a sufficient risk variable produces association 9/25 despite a zero effect.'],
                   'limitations': ['No fitted discovery algorithm, bank data, empirical coverage or operational qualification.']})
    audit = {'cutoff': '2026-10-07', 'sources': groups, 'runtime_claims': False,
             'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'}}
    shared.verify_refs(audit)
    write('source-audit.json', audit)

    decisions = {
        '0': ('defer_incomplete_release', 'Native search is present but the scorer throws; assemble lawful upstream sources and test before use.'),
        '1': ('route_to_python_survey', 'Inspected principal model is Python/JAX; review bundled baselines separately.'),
        '2': ('unresolved_research_demonstrator', 'Post-nonlinear claim is a documented experiment; complete technical source/build identity is not established.'),
        '3': ('reject_causal_rule_contract', 'Conditional entropy does not identify intervention effects; selected formula also differs from full conditional entropy; rights unresolved.'),
        '4': ('evaluate_R_integration', 'Use an explicit R-hosted mixed-data CPDAG path; do not strip the R semantic and license boundary.'),
        '5': ('secondary_native_candidate', 'Structure-learning templates exist; require delegated score/search/acyclicity and tests before selection.'),
        '6': ('evaluate_R_regularization_path', 'Keep lambdas, MCP/L1 and edge-count stopping distinct from CI thresholds; upstream alias review remains.'),
        '7': ('evaluate_categorical_benchmark_boundary', 'Explicit categorical scope, graph tags and CI implementation must survive the native/Python boundary.'),
        '8': ('defer_unresolved_rights_and_contract', 'No license identified in bounded source tree; native batch entrypoint alone does not validate online causal discovery.'),
        '9': ('secondary_score_search_candidate', 'Native OpenMP score search and GPL terms found; posterior/SMC and graph-effect semantics remain unqualified.'),
        '10': ('retain_R_score_baseline', 'Inspect through documented R interface; C++ internals do not supply a standalone causal-effect API.')}
    queries = []
    for key in ['causal', 'bayes']:
        p = RAW / ('exec13_cxx_search_' + key + '.json')
        d = json.loads(p.read_text())
        queries.append({'query': key, 'total_count': d['total_count'], 'returned': len(d['items']),
                        'incomplete_results': d['incomplete_results'],
                        'response': ref(p, 'Current index filtered by creation cutoff; discovery only'),
                        'receipt': ref(p.with_name(p.stem + '.receipt.json'), 'Exact search URL and access date')})
    candidates = []
    for i, p in pins.items():
        status, decision = decisions[i]
        candidates.append({**p, 'route': 'bounded_query', 'status': status, 'decision': decision,
                           'commit_response': ref(RAW / ('exec13_cxx_lead_' + i + '_commit.json'), 'Cutoff identity')})
    for name, decision in [
        ('aGrUM/pyAgrum', 'Prioritize a restricted native discrete discovery adapter; retain CPDAG and documented missing-data refusal.'),
        ('pcalg', 'Retain the existing R integration selection; native components are not counted as a second independent engine.'),
        ('libDAI', 'Candidate for inference after model identification; reject as evidence of a discovery/effect workflow.'),
        ('OpenGM', 'Discrete factor-graph inference alternative; old unmaintained snapshot, no discovery absence claim.'),
        ('ANazaret/XGES', 'Direct native alternative; technical source inspected, redistribution rights unresolved.'),
        ('CausalAILab/lges', 'Upstream Python route with nested GES terms; root/license and derivative equivalence unresolved.')]:
        candidates.append({'name': name, 'route': 'known_or_direct_upstream_lead', 'decision': decision})
    registry = {'cutoff': '2026-10-07', 'queries': queries, 'candidates': candidates,
                'candidate_count': len(candidates),
                'aliases': {'aGrUM/pyAgrum': 'One native core with bindings; not two independent engines',
                            'ccdrAlgorithm/itsrainingdata/ccdrAlgorithm/sparsebn': 'Package references these ecosystem aliases; no complete revision-equivalence proof',
                            'PC/PC-Stable/FCI/MIIC': 'Distinct algorithms/configurations inside named packages; not extra packages',
                            'Breaking Bad/XGES/LGES': 'Algorithm reuse/reference is not identity or license inheritance'},
                'source_review': ref(BASE / 'source-audit.json', 'Inspected technical passages and limited claims'),
                'followup_acquisition': ref(BASE / 'continuation-acquisition.json', '26 additional reads, 24 saved and two 404s'),
                'coverage_limit': 'Two finite current-index query routes, all 11 returned candidates, four known leads and two direct upstream leads. No claim of exhaustive C++ ecosystem coverage or pre-cutoff index completeness.'}
    write('candidate-register.json', registry)
    omissions = {'essential_gaps': [
        {'id': 'CXX01', 'candidate': 'XGES and LGES root terms',
         'gap': 'Complete rights and derivative/dependency provenance are unresolved; API 404 is not proof that no license exists.',
         'next_action': 'Inspect official release archives/package metadata and lawful grant at the pinned revisions, preserving nested license distinctions; select an already licensed alternative while unresolved.'},
        {'id': 'CXX02', 'candidate': 'COJEC and incremental BN',
         'gap': 'No release license identified in the inspected tree; incremental score/dependence and update semantics are incomplete.',
         'next_action': 'Locate a documented grant and trace the complete score/update path; retain no-adoption disposition without asserting technical absence.'},
        {'id': 'CXX03', 'candidate': 'Post-nonlinear experiment and secondary native engines',
         'gap': 'Complete build/source provenance, delegated score/cycle rules, and current aliases remain unreviewed.',
         'next_action': 'Bound a new source review for the exact distributed artifact, godai delegated learners, BN_SMC kernels and ccdr upstream alias; do not claim comprehensive coverage meanwhile.'}],
        'later_prototype_work': ['Compile selected aGrUM/OpenBNSL native boundaries in a pinned isolated build.',
                                'Test input coercion, missing/degenerate strata, graph endpoints, sign, scale and permutation fixtures.',
                                'Register matched graph/effect, failure, runtime and memory studies before final draws.'],
        'literature_leads_not_cited_as_papers': ['Breaking Bad original paper', 'SVI-DAG original paper',
                                               'XGES original paper', 'LGES original paper', 'CCDr original paper'],
        'global_blocker': False, 'cell_disposition': 'inconclusive',
        'reason': 'Selected technical comparisons and finite search census are complete, but essential rights/alias/secondary-source questions prevent full cell coverage acceptance.'}
    write('omissions-register.json', omissions)
    identity = []
    tree_by_repo = {'agrumery/aGrUM': RAW / 'v12_sw2_tree_agrum.json'}
    for i, p in pins.items():
        files = [RAW / f'exec13_cxx_lead_{i}_tree.json', RAW / f'exec13_cxx2_lead_{i}_tree.json']
        tree_by_repo[p['repo']] = next(f for f in files if f.exists())
    tree_by_repo.update({'ANazaret/XGES': RAW / 'exec13_cxx2_xges_tree.json',
                         'CausalAILab/lges': RAW / 'exec13_cxx2_lges_tree.json'})
    for s in groups:
        for r in s.get('records', []):
            u = r['source_identity']
            if not u.startswith('https://raw.githubusercontent.com/'):
                continue
            parts = u.split('/')
            repo, path = '/'.join(parts[3:5]), '/'.join(parts[6:])
            if repo not in tree_by_repo:
                continue
            tree = json.loads(tree_by_repo[repo].read_text())
            expected = {x['path']: x['sha'] for x in tree['tree']}.get(path)
            body = (ROOT / r['local_copy']['path']).read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            assert expected == actual, (repo, path)
            identity.append({'file': r['local_copy'], 'git_blob_sha1': actual,
                             'tree': ref(tree_by_repo[repo], 'Cutoff tree entry matching raw source bytes')})
    write('identity-review.json', {'status': 'pass', 'issues': [], 'verified_raw_blobs': len(identity), 'evidence': identity})
    print(json.dumps({'sources': len(groups), 'candidates': len(candidates), 'verified_raw_blobs': len(identity),
                      'cell_coverage': 'inconclusive', 'vendor_runtime_executed': False}))


if __name__ == '__main__':
    main()
