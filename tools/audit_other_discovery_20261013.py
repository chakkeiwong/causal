#!/usr/bin/env python3
"""Bind inspected other-language primary sources and explicit survey omissions."""
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import master_control as core
import other_discovery_examples_20261013 as exact

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/other-discovery'
RAW = ROOT / 'docs/literature/raw'
ref = shared.ref

# Only the following selected anchors have been inspected for technical claims.
# Acquired files outside these anchors remain available without capability credit.
INSPECTION = {
 'causalinference': {
  'title': 'CausalInference.jl 0.19.4: PC, Gaussian GES and graph contracts',
  'anchors': {0: 'README: declared algorithm inventory only', 1: 'MIT Expat permission, notice and warranty clauses',
   2: 'Project.toml: version 0.19.4, dependencies and Julia compatibility declaration',
   3: 'pcalg and orient_unshielded: CPDAG as DiGraph, stable dispatch, reciprocal arcs for unresolved edges',
   4: 'ges lines 22-59, forward/backward loops and local_score_ lines 350-365: defaults, return tuple, relative score and zero residual variance',
   5: 'PC example: declared Gaussian test and unresolved directions',
   6: 'GES example: Gaussian BIC, graph display and uninspected additional methods'},
  'claims': ['Selected PC returns a CPDAG encoded as a directed container with reciprocal arcs for unresolved edges.',
   'Selected Gaussian GES defaults to penalty 0.5 and returns graph, score improvement and time tuple.',
   'The covariance score uses log(max(0,Cp)); zero residual variance can yield a nonfinite score.'],
  'choice': 'Integrate selected Julia PC/GES as a candidate numerical backend after graph, degeneracy and matched-output tests; no immediate port.',
  'limits': ['No Julia execution, performance or bank qualification.', 'FCI, exact search and Zig-Zag are README/documentation leads, not technically qualified here.']},
 'associations': {
  'title': 'Associations.jl: PC and conditional-independence interfaces',
  'anchors': {0: 'README: prior CausalityTools.jl name and association/independence/graph API',
   1: 'MIT Expat permission and notice clauses', 3: 'causal_graphs documentation: infer_graph API and listed graph methods',
   4: 'PC docstring and constructor/check_input: nondirectional requirement, maxdepth spelling and commented direction check',
   5: 'skeleton_unconditional! and conditionaltest_and_remove_edge!: pvalue > alpha deletion; conditioning depth',
   6: 'cpdag lines 32-66 and edge predicates: reciprocal arcs, orientation sweep limit',
   7: 'LocalPermutationTest declaration/constructor lines 30-124: documented kperm=5 versus constructor 10, 100 shuffles, RNG and window'},
  'claims': ['CausalityTools.jl is the former package name, not an independent implementation in this count.',
   'PC requires nondirectional association tests; its selected check_input does not enforce the documented direction check.',
   'The inspected constructor uses maxdepth, and the local-permutation constructor defaults to kperm=10 despite documentation listing 5.'],
  'choice': 'Integrate selected test interfaces conditionally, validating measure direction, actual defaults and resampling assumptions.',
  'limits': ['No general validity claim for an arbitrary measure/resampler or dependent bank panels.', 'No runtime confirmation of API discrepancies.']},
 'recursive': {
  'title': 'RecursiveCausalDiscovery.jl 0.2.0: RSL-D implementation scope',
  'anchors': {0: 'README: only RSL-D implemented; MARVEL, L-MARVEL and ROL unchecked; Julia 1.10 statement',
   1: 'MIT license', 2: 'Project.toml version 0.2.0 and julia=1 declaration',
   3: 'find_markov_boundary_matrix!, rsld overloads and removable fallback, lines 1-160',
   4: 'pdag.jl edge predicates: reciprocal undirected representation and CausalInference attribution'},
  'claims': ['The README implements RSL-D rather than all four named recursive families.',
   'The matrix overload forwards mkbd_ci_test=ci_test, losing a distinct supplied mkbd_ci_test.',
   'Boundary initialization tests pairs conditional on every other variable; failure to find a removable variable selects smallest boundary.'],
  'choice': 'Retain an experimental comparison candidate; verify overload forwarding and fallback semantics before integration.',
  'limits': ['The cited RCD scholarly original was not acquired in this tranche; no theorem or speed claim is credited.', 'README/manifest Julia requirement discrepancy remains unresolved.']},
 'flopsearch': {
  'title': 'FLOP/flopsearch 0.3.0: Rust search and R/Python boundary',
  'anchors': {0: 'README: linear score search, R/Python entrypoints and CPDAG encoding',
   1: 'Mozilla Public License 2.0 identity and redistribution sections',
   2: 'flop Cargo.toml: 0.3.0, Rust edition 2021, numerical and RNG dependencies',
   3: 'algo.rs run lines 42-129: exclusive stopping choices, thread_rng, initial local search, abort check and outer restart loop',
   6: 'flopsearch.pyi: data orientation, required termination choice, first-local-optimum and 1/2 adjacency encoding'},
  'claims': ['The selected Python stub specifies 1 for directed and symmetric 2 for unresolved edges.',
   'The run path requires exactly one of restarts, timeout or manual termination; uses thread_rng and no supplied seed in that configuration.',
   'The first local search is allowed to reach an optimum before the shown abort check. A strict request deadline is not established.'],
  'choice': 'Prefer existing R/Python boundary to a new port; qualify reproducibility, outer deadline and graph decoding first.',
  'limits': ['Uninspected ICLR original and delegated parent-fitting routines limit scientific/performance claims.', 'MPL-2.0 source obligations and dependency notices need a distribution-specific review.']},
 'varlingam': {
  'title': 'varlingam-rs 0.1.0: selected static DirectLiNGAM path',
  'anchors': {0: 'README: algorithm and performance statements are author claims only',
   1: 'Apache-2.0 license heading and grant terms', 2: 'MIT license permission and notice',
   3: 'Cargo.toml: 0.1.0, dual licensing, PyO3 and nalgebra dependencies',
   4: 'direct_lingam lines 150-270 and find_root_optimized lines 300-340: cache, residual updates, target-row coefficients and unused data argument'},
  'claims': ['The coefficient matrix writes B[target,predictor].',
   'Entropy cache is constructed once; residuals change but root scoring uses cached values and ignores its data argument.',
   'Advertised same accuracy and speedups are not independently established by inspected source.'],
  'choice': 'Defer default adoption and porting pending proof or matched evidence for cached ordering and complete numerical helpers.',
  'limits': ['No claim that the optimization is necessarily wrong; its equivalence argument is unreviewed.',
   'Time-series, latent, bootstrap and validation implementations are not qualified by this static-path review.']},
 'why': {
  'title': 'why-rs 0.2.1: selected PC implementation and limitations',
  'anchors': {0: 'README: DAG/FCM modeling and PC claims', 1: 'MIT or Apache-2.0 choice and MIT terms',
   2: 'Cargo.toml: 0.2.1, Rust edition 2024 and dependencies',
   3: 'pc.rs lines 19-245: reciprocal edge container, single orientation rule, fixed alpha thresholds and zero-denominator correlation'},
  'claims': ['Only orientation propagation Rule 1 is implemented in the inspected method; Rules 2 and 3 are explicitly left for addition.',
   'Thresholds are hardcoded for 0.01, 0.05 and 0.10; every other supplied alpha uses 1.960.',
   'A zero denominator in recursive partial correlation returns zero, which can turn degeneracy into an independence decision.'],
  'choice': 'Reject this pinned PC path as the proposal reference engine; retain modeling interfaces as separately unqualified candidates.',
  'limits': ['Source-level finding; no Rust build or empirical graph-accuracy result.', 'No extrapolation to later revisions or all repository functions.']},
 'explorer': {
  'title': 'Causal Explorer 1.5: MATLAB manual and restrictive license',
  'anchors': {0: 'README: November 2019 1.5 and MATLAB R2017b P-code compatibility statement',
   1: 'License.md: academic noncommercial single-user restriction; no redistribution/modification grant',
   2: 'Manual printed page 7: PC data, domain counts, mi/g2/z test and threshold contract',
   3: 'License PDF pages 1-2: same restrictive grant and registration conditions'},
  'claims': ['The manual describes columns as variables and PC with discrete/continuous test choices.',
   'The saved license restricts use to noncommercial academic single-user purposes and does not grant modification or redistribution.',
   'The P-code compatibility claim is for MATLAB R2017b, not an executed modern MATLAB/Octave test.'],
  'choice': 'Reject direct adoption or porting under the saved terms for the proposed commercial library; retain as a documented comparator.',
  'limits': ['No license accepted, no software installed or executed.', 'Manual wording public domain does not resolve the accompanying restrictive grant.']},
 'generalized': {
  'title': 'Generalized-score GES MATLAB reference: scores and edge conventions',
  'anchors': {0: 'README: score_type, multi_sign, maxP, parameters and 1/-1 edge contract',
   1: 'readme.txt: documented input/return convention',
   2: 'GES.m lines 1-145: negative-score selection, empty initialization, validity checks and decreasing score',
   4: 'local_score_CV_general.m lines 1-105: dense Gram matrices, bandwidth, contiguous fold slicing and regularization',
   5: 'KCI-test/COPYING: embedded component redistribution clauses only'},
  'claims': ['The selected implementation minimizes negative cross-validated or marginal likelihood, unlike a maximized BIC convention.',
   'Directed entries are 1; unresolved directions are -1; these are graph marks, not slopes.',
   'The inspected score builds dense T by T kernel arrays and slices contiguous folds.',
   'The component COPYING file cannot establish a grant for the top-level GES code.'],
  'choice': 'Retain a methodological comparator; defer redistribution/porting until top-level rights and algorithmic originals are inspected.',
  'limits': ['No complete mixed-data/nonlinear consistency or performance result established.', 'No root license discovered in the saved complete tree; this is a snapshot finding, not a claim that no rights can be obtained.']},
 'bnt': {
  'title': 'Bayes Net Toolbox MATLAB reference: ordered K2 and PC',
  'anchors': {0: 'BNT README: Murphy authorship and 2007 document date',
   1: 'BNT/license.gpl.txt: GNU Library General Public License version 2 grant',
   2: 'learn_struct_K2.m: variables by rows, fixed order, local Bayesian/BIC scores and dag[parent,child]',
   3: 'learn_struct_pdag_pc.m: directed -1 and symmetric undirected 1 contract; CI callback and orientation rules',
   4: 'bnt.html lines 1-40: historical documentation identity and Library GPL link'},
  'claims': ['K2 takes variables in rows and observations in columns, unlike the selected Julia/FLOP interfaces.',
   'K2 only admits predecessors in a supplied order; the order is an input restriction, not inferred causal truth.',
   'The selected PC output uses -1 for a directed edge and symmetric 1 for unresolved edges.',
   'The selected BNT license grants Library GPL v2; the whole bundle and dependencies require separate review.'],
  'choice': 'Retain selected legacy functions as reference comparisons; defer production adoption and whole-bundle porting.',
  'limits': ['No modern MATLAB/Octave compatibility or all-component license qualification.', 'Historical documentation prices are not current quotations and are not used.']},
 'webapp': {
  'title': 'Expert-in-loop JavaScript discovery demo: residual association calculation',
  'anchors': {0: 'README: build instruction only', 1: 'package.json: 1.0.0, ISC metadata and failing placeholder test command',
   3: 'ci_test.js pillai_test and compute_effects: same-row RF training/prediction, squared canonical correlations, F approximation and arrow display'},
  'claims': ['The inspected calculation fits and predicts residual models on the same rows, then computes a Pillai-style statistic and F reference.',
   'Its effectSize field is a sum of squared canonical correlations, not a currency-valued intervention effect.',
   'ISC appears in package metadata; no complete project permission grant is established from that field alone.'],
  'choice': 'Retain interaction ideas; reject direct interpretation of effectSize as the proposed causal effect and defer estimator adoption.',
  'limits': ['No theorem for validity after adaptive same-row fitting or empirical calibration is established.', 'Browser/server behavior and delegated helpers remain uninspected.']},
 'dagitty': {
  'title': 'DAGitty JavaScript core: graph-based adjustment interface',
  'anchors': {0: 'README: shared JavaScript core, browser GUI and R/V8 boundary',
   1: 'GNU GPL version 2 license heading and distribution provisions',
   3: 'GraphAnalyzer.js isAdjustmentSet lines 385-415: graph types, source/target and adjustment/selection handling'},
  'claims': ['The JavaScript core underlies both browser and R interfaces, so these are not independent discovery engines.',
   'The selected adjustment check accepts DAG/PDAG/MAG/PAG graph types and reasons about supplied graph/query objects.',
   'This operation does not establish the graph from a banking dataset.'],
  'choice': 'Integrate graph authoring/analysis as a separate candidate layer; preserve graph type and review GPL distribution obligations.',
  'limits': ['No new browser/R execution or unrestricted graph-identification theorem.', 'A process boundary is not itself a license exemption.']},
}


def main():
    pins = json.loads((BASE / 'pins.json').read_text())
    selection = json.loads((BASE / 'file-selection.json').read_text())
    sources = []
    for name, spec in INSPECTION.items():
        pin = pins[name]
        assert pin['date'] <= '2026-10-07T15:59:59Z'
        records = []
        for i, anchor in spec['anchors'].items():
            key = f'exec13_other_file_{name}_{i}'
            chosen = next(x for x in selection if x['id'] == key)
            receipt_path = RAW / (key+'.receipt.json')
            receipt = json.loads(receipt_path.read_text())
            path = RAW / (key+'.'+chosen['extension'])
            assert receipt['status'] == 'saved' and core.sha(path) == receipt['sha256']
            if chosen['extension'] == 'pdf':
                assert path.read_bytes().startswith(b'%PDF-')
            records.append({'local_copy': ref(path, anchor), 'source_identity': receipt['url'],
                'accessed_utc': receipt['accessed_utc'], 'role': 'inspected_primary_source',
                'receipt': ref(receipt_path, 'Original bounded acquisition and byte identity')})
        source = {'integrated_citation_key': 'exec13_other_'+name,
            'kind': 'software_primary_sources', 'title': spec['title'],
            'author': pin['repository']+' contributors', 'year': int(pin['date'][:4]),
            'source_identity': 'https://github.com/'+pin['repository'],
            'version_date': 'Commit '+pin['sha']+' ('+pin['date'][:10]+'); accessed 13 October 2026; cutoff 7 October 2026 Asia/Shanghai',
            'local_copy': records[0]['local_copy'], 'records': records,
            'identity_evidence': [ref(RAW / f'exec13_other_commit_{name}.json', 'Pre-cutoff commit metadata'),
                                  ref(RAW / f'exec13_other_tree_{name}.json', 'Complete pinned repository tree')],
            'supported_claims': spec['claims'], 'proposed_disposition': spec['choice'],
            'limits': spec['limits'], 'software_executed': False}
        sources.append(source)

    search_paths = [RAW / ('exec13_other_search_'+tag+'.json') for tag in
                    ['julia', 'rust', 'matlab', 'javascript', 'matlab_bn', 'rust_graph']]
    search_paths.append(RAW / 'v12_sw_language_julia.json')
    candidates, searches = {}, []
    for path in search_paths:
        result = json.loads(path.read_text())
        searches.append({'source': ref(path, 'Repository discovery metadata, not capability evidence'),
            'reported_total': result['total_count'], 'returned': len(result['items']),
            'incomplete_results': result['incomplete_results'],
            'complete_for_returned_query': len(result['items']) == result['total_count'] and not result['incomplete_results']})
        for row in result['items']:
            repo = row['full_name']
            candidates.setdefault(repo, {'repository': repo, 'description_at_retrieval': row.get('description'),
                'created_at': row['created_at'], 'metadata_sources': [], 'aliases': [],
                'status': 'uninspected_discovery_lead',
                'finding': 'Metadata records this lead only. No technical capability, absence or licensing conclusion.',
                'next_action': 'Inspect a cutoff-pinned original before inclusion, exclusion or reuse.'})
            candidates[repo]['metadata_sources'].append(ref(path, 'items[full_name='+repo+']'))
    for name, pin in pins.items():
        repo = pin['repository']
        item = candidates.setdefault(repo, {'repository': repo, 'metadata_sources': [], 'aliases': [],
            'origin': 'Named technical/reference lead included in reviewed plan'})
        item.update(status='selected_primary_inspected_no_runtime', pin=pin,
            claims=INSPECTION[name]['claims'], proposed_disposition=INSPECTION[name]['choice'],
            limits=INSPECTION[name]['limits'],
            next_action='Complete the specific qualification or rights checks before any stronger adoption claim.')
        item.pop('finding', None)
    aliases = {'JuliaDynamics/Associations.jl': ['CausalityTools.jl'],
               'CausalDisco/flopsearch': ['FLOP', 'flop crate', 'flopsearch R and Python wrappers'],
               'edy-os/varlingam-rs': ['varlingam crate'], 'jwhogg/why-rs': ['why_rs'],
               'bayesnet/bnt': ['Bayes Net Toolbox', 'BNT'],
               'jtextor/dagitty': ['DAGitty', 'dagitty R frontend and JavaScript core']}
    for repo, names in aliases.items():
        candidates[repo]['aliases'] = names
    register = {'operation': 'SW.CELL.discovery_iid.other_relevant', 'cutoff': '2026-10-07',
        'retrieved_after_cutoff': True, 'plan': ref(BASE / 'plan-review.md', 'Frozen finite query and source selection rules'),
        'searches': searches, 'candidates': list(candidates.values()),
        'candidates_count': len(candidates), 'selected_primary_candidates': len(pins),
        'uninspected_candidates': len(candidates)-len(pins),
        'scope_limits': ['Six query result sets fully returned as reported; inherited Julia broad query is 30 of 275.',
            'Star ordering, language labels and wording are retrieval/index dependent, not a census of all relevant packages.',
            'Rust/Julia registries, Octave, Scala, Go, Clojure and every continuous-optimization implementation are not systematically covered.',
            'Independent similarly named CausalDiscovery.jl repositories are not collapsed into aliases.',
            'RCD in RecursiveCausalDiscovery.jl and varlingam-rs refers to distinct algorithm families.',
            'No software executed or benchmark speedup independently established.']}
    core.write(BASE / 'candidate-register.json', register)
    omissions = {'status': 'open', 'essential_sources_waived': False,
        'candidate_register': ref(BASE / 'candidate-register.json', 'All discovered and named candidates, aliases and follow-up actions'),
        'items': [
            {'gap': 'Remaining '+str(len(candidates)-len(pins))+' metadata-only candidates and additional language/registry searches',
             'remedy': 'Continue dated primary inspection and declare a separately bounded search tranche.', 'blocks': 'Full cell census/coverage acceptance'},
            {'gap': 'Recursive Causal Discovery, FLOP and generalized-score original scholarly texts were not acquired in this source tranche',
             'remedy': 'Acquire and inspect authentic convention-named PDFs before theorem, applicability or speed claims.', 'blocks': 'Scholarly equivalence/consistency and empirical superiority claims'},
            {'gap': 'Selected source limitations and delegated algorithms/CI helpers remain unqualified',
             'remedy': 'Use the per-candidate adverse fixtures and matched implementations in a registered future evaluation.', 'blocks': 'Runtime and statistical qualification'},
            {'gap': 'Generalized-score top-level rights, webapp grant and whole-bundle/dependency notices incomplete',
             'remedy': 'Inspect explicit applicable grants and component notices; request permission only if needed for a later distribution.', 'blocks': 'Redistribution, adoption or code porting of affected candidates'},
            {'gap': 'Causal Explorer restrictive academic license',
             'remedy': 'Keep the comparator; prefer eligible alternatives or obtain separately scoped rights before later use.', 'blocks': 'Direct commercial adoption/porting under the saved terms'},
        ], 'no_ecosystem_absence_claim': True}
    core.write(BASE / 'omissions-register.json', omissions)
    results = exact.serialize(exact.calculate())
    core.write(BASE / 'exact-results.json', results)
    core.write(BASE / 'exact-replay.json', exact.serialize(exact.calculate()))
    assert (BASE / 'exact-results.json').read_bytes() == (BASE / 'exact-replay.json').read_bytes()
    sources.append({'integrated_citation_key': 'exec13_other_exact', 'kind': 'project_exact_construction',
        'title': 'Exact funding equivalence, graph encoding and significance-threshold examples',
        'author': 'Causal banking proposal project', 'year': 2026,
        'source_identity': 'Project construction on 13 October 2026, after the literature cutoff',
        'version_date': 'Project calculation 13 October 2026; no package or bank experiment',
        'local_copy': ref(BASE / 'exact-results.json', 'Three Gaussian constructions, intervention effects and scalar threshold example'),
        'records': [ref(ROOT / 'tools/other_discovery_examples_20261013.py', 'Exact rational structural covariance and intervention algebra')],
        'supported_claims': ['Same covariance in three stipulated Gaussian worlds but quote effects 0 or 2.',
            'A transpose changes the stipulated quote effect from 2 to 0.',
            'For alpha 0.02 a 1.960 fallback differs from the normal reference critical value.'],
        'limits': ['No package execution, sampled study, fitted bank response or empirical calibration.']})
    audit = {'cutoff': '2026-10-07', 'acquisition_date': '2026-10-13', 'sources': sources}
    shared.verify_refs(audit)
    core.write(BASE / 'source-audit.json', audit)
    note = {'finding': 'Acquired 90 bounded primary/metadata responses; restored original collector manifest. Inspected selected technical/license paths for 11 of '+str(len(candidates))+' candidates. Specific representation, alpha, overload and rights findings are recorded; full coverage and runtime qualification remain open.',
        'evidence': [ref(BASE / p, p) for p in ['acquisition-results.json', 'candidate-register.json', 'source-audit.json', 'omissions-register.json', 'exact-results.json']],
        'next_action': 'Independently verify the finite covariance/intervention and threshold calculations; write and review the comparative chapter, compile a preserving reader, record actual coverage outcome and continue the next eligible operation.'}
    core.write(BASE / 'source-progress.json', note)
    print(json.dumps({'sources': len(sources), 'candidates': len(candidates), 'inspected_candidates': len(pins),
                      'remaining_candidates': len(candidates)-len(pins), 'exact_replay': 'pass'}))


if __name__ == '__main__':
    main()
