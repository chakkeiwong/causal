#!/usr/bin/env python3
"""Audit bounded latent-language sources and reproduce project diagnostics."""
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import build_native_evaluation_reader_v3_20261014 as schema
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-14/other-latent'
RAW = ROOT/'docs/literature/raw'
PRIOR = ROOT/'docs/program/execution/2026-10-13/other-discovery'
SYN = BASE/'comparison.md'
OUTPUT = ROOT/'docs/program/comprehensive-v14/work/SW.CELL.discovery_latent.other_relevant/coverage-review.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}


def exact():
    # Enumerate independent centered finite components; this is not an RCD
    # applicability claim, whose published errors have continuous laws.
    rows = [(F(u), F(u+ea), F(u+ea, 2)+2*u+ey)
            for u in [-1, 1] for ea in [-1, 1] for ey in [-1, 1]]
    var_a = sum(a*a for u, a, y in rows)/8
    cov_ay = sum(a*y for u, a, y in rows)/8
    slope = cov_ay/var_a
    effect = F(1, 2)
    selection = defaultdict(F)
    for a in [0, 1]:
        for y in [0, 1]:
            if a == y:
                selection[a, y] += F(1, 2)
    # A nonzero null contrast whose coefficient sum is zero.
    omega, crosscov = [F(1), F(-1)], [F(1), F(1)]
    residual = [(F(e1-e2), F(u+ez)) for u in [-1, 1]
                for e1 in [-1, 1] for e2 in [-1, 1] for ez in [-1, 1]]
    joint, margin_r, margin_z = defaultdict(F), defaultdict(F), defaultdict(F)
    for r, z in residual:
        joint[r, z] += F(1, 16)
        margin_r[r] += F(1, 16)
        margin_z[z] += F(1, 16)
    assert all(joint[r, z] == pr*pz for r, pr in margin_r.items() for z, pz in margin_z.items())
    assert slope == F(3, 2) and cov_ay == 3 and var_a == 2
    assert sum(x*y for x, y in zip(omega, crosscov)) == 0
    # Endpoint dictionaries explain conversion collisions, not the validity
    # of every possible PAG. Values are symbols, never causal weights.
    binary = {'tail-tail': [1, 1], 'circle-circle': [1, 1], 'arrow-arrow': [1, 1]}
    typed = {'tail-tail': [3, 3], 'circle-circle': [1, 1], 'arrow-arrow': [2, 2]}
    return {
        'scope': 'Exact imposed mechanisms and conversion algebra; no upstream code execution or empirical qualification.',
        'banking': {'variance_A': str(var_a), 'covariance_AY': str(cov_ay),
                    'population_slope': str(slope), 'intervention_slope': str(effect),
                    'value_per_Y_unit_USD': 100, 'cost_per_A_unit_USD': 80,
                    'associational_net_USD': str(100*slope-80),
                    'causal_net_USD': str(100*effect-80),
                    'refinement_bound': 'Only entries with both magnitudes<=1e-10 are eligible for shrinkage; every initial substantive coefficient is invariant.',
                    'zero_pair_after_any_shrinkage': '0',
                    'upstream_initial_coefficient_observed': False},
        'selection': {'retention_probability': '1/2', 'selected_joint':
                      {str(k): str(v) for k, v in sorted(selection.items())},
                      'selected_association': '1', 'population_intervention_effect': '0',
                      'faithfulness_claim': False},
        'contrast': {'omega': [str(v) for v in omega], 'omega_sum': str(sum(omega)),
                     'norm_squared': str(sum(v*v for v in omega)),
                     'crosscov_product': '0', 'contrast_variance': '2',
                     'independence_verified_by_enumeration': True,
                     'floating_point_SVD_outcome_observed': False},
        'endpoint_conversion': {'ordinary_binary': binary, 'latent_typed': typed,
                                'distinct_input_classes': 3, 'binary_output_classes': 1,
                                'typed_output_classes': 3},
    }


SPECS = {
    'causalinference': {
        'title': 'CausalInference.jl FCI endpoint, callback and path-search review',
        'anchors': {
            0: 'src/fci.jl:1-60 endpoint convention;149-239 FCI stages and keyword forwarding;187-442 bounded paths;460-500 plotting styles',
            1: 'test/fci.jl:1-160 oracle, hidden-node, selection and plotting assertions; inspected but not run',
            3: 'src/skeleton.jl:43-154 stable callback construction and selection-aware dseporacle'},
        'claims': ['FCI returns paired endpoint marks; mark on arc i,j is at j.',
                   'Initial skeleton call drops kwargs while later CI calls use them; selection tests bind selection in a closure.',
                   'Selected possible-separation and orientation paths cap shortest paths at100 and materialize separating power sets.',
                   'Plot preparation lacks an explicit bidirected style although raw graph and tests support bidirected marks.'],
        'decision': 'Conditional raw-endpoint integration; no immediate port or enabled backend.',
        'limits': ['Dependency/runtime closure, path-cap completeness, callback coherence and rendered plotting are unqualified.'],
        'inherited': [(1, 'Root MIT Expat notice'), (2, 'Project manifest version0.19.4 and dependency declarations')]},
    'varlingam': {
        'title': 'varlingam-rs RCD control flow and confidence semantics',
        'anchors': {0: 'src/rcd.rs:189-213 settings;249-333 heuristic scores and adjacency exclusion;337-432 latent scores and shrinkage;435-549 convergence and outputs;584-639 tests',
                    1: 'src/lib.rs:74-86 public module;146-150 Python entrypoint registration'},
        'claims': ['Starts with DirectLiNGAM and tests pairs only when both direct coefficients are<=1e-10.',
                   'Threshold is labeled p-value but uses heuristic correlation/entropy score; score becomes confidence and latent-effect averages.',
                   'Refinement only shrinks coefficients already below the edge threshold; substantive initial coefficients are invariant.',
                   'Convergence compares pair counts; declared convergence_threshold is unused in the inspected path.',
                   'Basic recovery test prints output without asserting recovery of the specified confounded pair.'],
        'decision': 'Reject default qualified RCD backend; defer port until algorithmic and empirical correspondence is established.',
        'limits': ['No upstream execution or measured failure rate; full DirectLiNGAM/numerical helper and dependency closure remains open.'],
        'inherited': [(1, 'Apache2 notice'), (2, 'MIT notice'), (3, 'Cargo dependencies and version declaration')]},
    'dagitty': {
        'title': 'DAGitty PAG transformation, validation and adjustment boundaries',
        'anchors': {0: 'GraphTransformer.js:1418-1445 PAG-to-PDAG endpoint conversion',
                    1: 'test/test/pags.js:1-62 PAG and conditioning examples; not executed'},
        'claims': ['Graph/query analysis is distinct from discovery from banking observations.',
                   'Selected adjustment routine accepts DAG/PDAG/MAG/PAG; full MAG/PAG validation is explicitly TODO.',
                   'Internal conversion maps unresolved endpoint classes to ordinary classes and changes graph type; do not export as newly learned truth.'],
        'decision': 'Conditional graph-analysis component with separate input validation and preserved raw graph.',
        'limits': ['No browser/Node execution; complete graph-validity guarantees and distribution rights are not closed.'],
        'inherited': [(1, 'GPLv2 root text'), (3, 'GraphAnalyzer.js:386-443 adjustment types;1594-1640 validation TODO and partial checks')]},
    'lmarvel': {
        'title': 'L-MARVEL MATLAB skeleton, removability and CI source review',
        'anchors': {0: 'README implementation and Gaussian CI inventory', 1: 'Root MIT notice',
                    2: 'LMARVEL.m:1-63 outputs, initialization, early break;165-188 fixed0.8 call;246-355 embedded helper attributions',
                    3: 'Mb_TC.m:1-26 total-conditioning initializer',
                    4: 'CI_Test.m:1-30 correlation inverse, degrees of freedom, transformed statistic and tcdf',
                    5: 'main.m:1-35 sample input and skeleton precision/recall'},
        'claims': ['Entry returns skeleton/separators/counts, not oriented PAG or intervention effect.',
                   'Unresolved entries start at-1 and can remain on no-removable-variable exit.',
                   'One removability subtest uses fixed alpha0.8; helper inverts correlation and uses tcdf without explicit degeneracy guards.',
                   'Root MIT notice coexists with embedded helper attributions requiring scope review.'],
        'decision': 'Conditional optional skeleton component after test-law, unresolved-state, rights and numerical review.',
        'limits': ['Original scholarly paper, full correctness inheritance, runtime and helper-rights closure remain open.']},
    'gin': {
        'title': 'GIN MATLAB latent clusters, null contrast and dependency boundaries',
        'anchors': {0: 'README inputs/outputs and test sensitivity statement', 1: 'Readme.txt version0.0 dated2020-10-21 and bundled KCI/KMI dependencies',
                    2: 'GIN_Main.m:1-62 centered row-variable data, clusters and latent order',
                    3: 'GIN_Condition_Test.m:19-62 SVD, sum(omega)==0 branch, KCI and Fisher aggregation',
                    4: 'Find_Causal_Clusters.m:18-55 subset search and first-empty-level stopping',
                    5: 'Find_Causal_Order.m:21-30 default MI helper versus alternate independence-test path',
                    6: 'KCI/COPYING component notice; not a grant over all repository files',
                    7: 'Example_GIN_Main.m: declared latent measurement structure and toolbox calls'},
        'claims': ['Produces clusters and latent order, with variables in rows; not arbitrary PAG or identified monetary effect.',
                   'SVD contrast uses a zero coefficient-sum check, which is not a zero-vector check.',
                   'Ordering delegates to MI by default; KCI/MI dependencies require further source and numerical review.',
                   'Selected component notice does not establish repository-wide rights; complete tree and inspected readmes have no such grant.'],
        'decision': 'Reference candidate; defer direct adoption/port pending original, helper and applicable-rights review.',
        'limits': ['No theorem inheritance or package execution; floating-point SVD behavior not observed; remaining implementation may contain component-specific notices.']},
    'oct': {
        'title': 'OCT MATLAB tuning, Tetrad delegation and latent endpoint conversion',
        'anchors': {0: 'README algorithms, required Tetrad6.8.1 jar and graph encodings', 1: 'Root GPLv3 text',
                    2: 'causalDiscovery.m: output ordering and delegation', 3: 'tetradAlgs.m: backend construction and runSearch',
                    4: 'tetradToMatrix.m: binary collisions between circle, tail and arrow pairs',
                    5: 'tetradToMatrixL.m: endpoint codes0/1/2/3',
                    6: 'OutofsampleCausalTuning.m:1-166 ten row folds, TreeBagger, selected MAG boundaries and permutation comparison',
                    7: 'runSearch.m: selected DAG and PAG-to-MAG branches'},
        'claims': ['Tetrad-delegated FCI is a wrapper pathway, not an independent engine.',
                   'Maintains PAG and selected MAG separately; typed converter preserves endpoint codes, ordinary binary converter collapses distinct marks.',
                   'Tuning uses ten row folds and predictive Markov-boundary models; MAG branch uses a selected member.',
                   'Root GPLv3, historical Java jar, MATLAB/toolboxes and remaining helpers need deployment-specific review.'],
        'decision': 'Adapt the comparison design prospectively; keep selected graph and class distinct and do not infer identification from prediction.',
        'limits': ['No workflow run, dependency/license closure or source-paper theorem/performance claim.']},
}


def main():
    prior_register = json.loads((PRIOR/'candidate-register.json').read_text())
    inherited_pins = json.loads((PRIOR/'pins.json').read_text())
    matlab_pins = json.loads((BASE/'matlab-pins.json').read_text())
    pins = inherited_pins | matlab_pins
    selections = json.loads((BASE/'initial-selection.json').read_text()) + json.loads((BASE/'matlab-selection.json').read_text())
    inherited_files = json.loads((PRIOR/'file-selection.json').read_text())
    sources, packages = [], []
    for key, spec in SPECS.items():
        pin = pins[key]
        tree_path = RAW/(('exec14_other_latent_tree_' if key in matlab_pins else 'exec13_other_tree_')+key+'.json')
        tree = json.loads(tree_path.read_text())
        assert tree['sha'] == pin['sha'] and not tree['truncated']
        assert pin['date'] < '2026-10-08'
        blobs = {r['path']: r['sha'] for r in tree['tree'] if r['type'] == 'blob'}
        selected = []
        for i, anchor in spec['anchors'].items():
            row = next(r for r in selections if r['id'] == f'exec14_other_latent_{key}_{i}')
            selected.append((row['id'], row['path'], anchor))
        for i, anchor in spec.get('inherited', []):
            row = next(r for r in inherited_files if r['id'] == f'exec13_other_file_{key}_{i}')
            selected.append((row['id'], row['source_path'], anchor))
        records = []
        for identity, source_path, anchor in selected:
            path = RAW/(identity+'.txt')
            data = path.read_bytes()
            digest = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert digest == blobs[source_path], (identity, digest, blobs[source_path])
            receipt_path = RAW/(identity+'.receipt.json')
            receipt = json.loads(receipt_path.read_text())
            assert receipt['sha256'] == core.sha(path) and pin['sha'] in receipt['url']
            records.append({'source_identity': receipt['url'], 'local_copy': ref(path, anchor),
                            'version_date': pin['date']+'; '+pin['sha'],
                            'receipt': ref(receipt_path, 'Observed public acquisition'),
                            'inspected_anchors': [anchor], 'git_blob_sha1': digest})
        package = {'candidate': key, 'repository': pin['repository'], 'revision': pin['sha'],
                   'source_date': pin['date'], 'tree': ref(tree_path, 'Complete pinned tree'),
                   'records': records, 'supported_claims': spec['claims'],
                   'proposed_disposition': spec['decision'], 'limitations': spec['limits'],
                   'software_executed': False, 'integration_allowed': False}
        packages.append(package)
    write(BASE/'primary-review.json', {'cutoff': '2026-10-07', 'packages': packages,
                                      'inspection_kind': 'Static primary source; no upstream code execution'})
    for key, spec in SPECS.items():
        package = next(p for p in packages if p['candidate'] == key)
        entry = schema.source('exec14_olatent_'+key, spec['title'], package['repository'],
            'software_primary_sources', 'https://github.com/'+package['repository'],
            package['revision']+'; '+package['source_date']+'; inspected2026-10-14',
            BASE/'primary-review.json', key+'; recorded paths and anchors', spec['claims'], package['records'])
        entry['limitations'] += spec['limits']
        entry['identity_evidence'] = [package['tree']]
        sources.append(entry)

    # The entire returned discovery set and inherited aliases remain available,
    # including unrelated and uninspected hits; no silent negative filtering.
    candidates = {c['repository']: {'repository': c['repository'], 'aliases': c.get('aliases', []),
                  'status': 'inherited_lead_not_latent_qualified',
                  'metadata_sources': c.get('metadata_sources', []),
                  'previous_disposition': c['status']} for c in prior_register['candidates']}
    searches = []
    mirror_aliases = []
    for name in ['julia', 'rust', 'matlab_fci', 'matlab_latent', 'javascript']:
        path = RAW/f'exec14_other_latent_search_{name}.json'
        receipt_path = path.with_name(path.stem+'.receipt.json')
        data, receipt = json.loads(path.read_text()), json.loads(receipt_path.read_text())
        assert core.sha(path) == receipt['sha256']
        searches.append({'query_url': receipt['url'], 'source': ref(path, 'Every returned repository identity'),
                         'receipt': ref(receipt_path, 'Post-cutoff retrieval date retained'),
                         'reported_total': data['total_count'], 'returned': len(data['items']),
                         'incomplete_results': data['incomplete_results'],
                         'stopping_rule': 'First20 results, star order; no later pages in this tranche.'})
        for row in data['items']:
            identity = row['full_name']
            if identity.startswith(('UnofficialJuliaMirror/', 'UnofficialJuliaMirrorSnapshots/')):
                mirror_aliases.append(identity)
                record = candidates['mschauer/CausalInference.jl']
                record['aliases'].append(identity)
            else:
                record = candidates.setdefault(identity, {'repository': identity, 'aliases': [],
                    'status': 'uninspected_search_lead', 'metadata_sources': []})
            record['metadata_sources'].append(ref(path, 'items[full_name='+identity+']'))
    for p in packages:
        row = candidates.setdefault(p['repository'], {'repository': p['repository'], 'aliases': [], 'metadata_sources': []})
        row.update(status='scoped_primary_inspection_no_runtime', proposed_disposition=p['proposed_disposition'],
                   primary=ref(BASE/'primary-review.json', p['candidate']))
    write(BASE/'candidate-register.json', {
        'operation': 'SW.CELL.discovery_latent.other_relevant', 'cutoff': '2026-10-07',
        'retrieved_after_cutoff': True, 'prior_register': ref(PRIOR/'candidate-register.json', '85 inherited identities and aliases'),
        'searches': searches, 'candidates': list(candidates.values()), 'candidate_count': len(candidates),
        'deduplicated_mirror_aliases': mirror_aliases, 'selected_primary_families': 6,
        'scope_limits': ['Post-cutoff index contents are not historical census evidence.',
                         'Rust640 and MATLAB74 totals exceed20 inspected search results; other registries/languages remain open.',
                         'Metadata-only hits are retained without capability, absence or rights claims.'],
    })
    write(BASE/'omissions-register.json', {
        'status': 'open', 'essential_sources_waived': False, 'no_ecosystem_absence_claim': True,
        'preserved_register': ref(PRIOR/'omissions-register.json', 'Earlier omissions not rewritten'),
        'items': [
            {'gap': 'Search pages beyond declared limit and all uninspected candidates',
             'next_action': 'Run a separately declared search tranche and inspect cutoff-pinned originals; prioritize ETIO, triad constraints, SEM-ME-UR, other Julia and JavaScript leads.'},
            {'gap': 'L-MARVEL and GIN authentic scholarly originals; OCT theory',
             'next_action': 'Acquire convention-named originals and inspect precise assumptions before inheriting correctness/performance results; present discussion remains selected code analysis.'},
            {'gap': 'GIN full-method rights and numerical/order helpers; remaining component notices elsewhere',
             'next_action': 'Inspect applicable grants and immediate call-path closure before adoption or porting.'},
            {'gap': 'Runtime and statistical qualification of all selected packages',
             'next_action': 'Freeze adversarial graph/oracle fixtures, resolve environments and compare exact outputs before fresh simulated or public-data studies.'},
        ],
    })
    write(BASE/'exact-oracle.json', exact())
    paper = ROOT/'docs/papers/RCD Repetitive causal discovery of linear non-Gaussian acyclic models with latent confounders Maeda(2020).pdf'
    receipt = json.loads((RAW/'exec14_other_latent_rcd_paper.receipt.json').read_text())
    assert paper.read_bytes().startswith(b'%PDF-') and core.sha(paper) == receipt['sha256']
    extracted = RAW/'exec14_other_latent_rcd_paper.txt'
    pages = extracted.read_text().split('\f')
    inspected = []
    for page in [1, 2, 3]:
        path = BASE/'inspected'/f'rcd-page-{page}.txt'
        path.parent.mkdir(exist_ok=True)
        with path.open('x') as stream:
            stream.write(pages[page-1])
        inspected.append(ref(path, 'Physical primary PDF page'+str(page)))
    sources.append({
        'integrated_citation_key': 'exec14_olatent_rcd_paper', 'kind': 'paper',
        'title': 'RCD: Repetitive causal discovery of linear non-Gaussian acyclic models with latent confounders',
        'filename_title': paper.stem.rsplit(' Maeda(', 1)[0],
        'first_author': 'Maeda', 'author': 'Takashi Nicholas Maeda and Shohei Shimizu', 'year': 2020,
        'source_identity': receipt['url'], 'version_date': 'PMLR108:735-745;2020-06-03', 'cutoff': '2026-10-07',
        'local_path': str(paper.relative_to(ROOT)), 'sha256': core.sha(paper),
        'local_copy': ref(paper, 'Authentic conference primary PDF'),
        'acquisition_receipt': ref(RAW/'exec14_other_latent_rcd_paper.receipt.json', 'Public PDF acquisition'),
        'identity_evidence': ref(RAW/'exec14_other_latent_rcd_page.html', 'Publisher author/title/date fields'),
        'inspected_anchors': inspected, 'extracted_text': ref(extracted, 'Full primary text'),
        'supported_claims': ['Sections2-3:linear acyclic model, independent non-Gaussian influences, ancestor/parent/confounded-pair stages, restricted direct-edge target.'],
        'limitations': ['No proof reconstruction, empirical replication or arbitrary latent-graph guarantee.'],
    })
    sources += [schema.source('exec14_olatent_search', 'Bounded other-language latent discovery search and omissions',
        'Causal banking proposal', 'search_audit', 'Public GitHub queries and preserved candidate identities',
        'cutoff2026-10-07;retrieved2026-10-14', BASE/'candidate-register.json', 'All five queries, counts, candidates and aliases',
        ['Selected six families; historical and ecosystem coverage remain incomplete.'],
        [{'local_copy': ref(BASE/'omissions-register.json', 'Unwaived remaining sources and remedies')}]),
        schema.source('exec14_olatent_oracle', 'Exact hidden-risk, selection, null-contrast and endpoint diagnostics',
        'Causal banking proposal', 'project_derivation', 'Authored finite mechanisms and algebra', '2026-10-14',
        BASE/'exact-oracle.json', 'Exact rational diagnostics; no upstream execution',
        ['Slope3/2 versus intervention1/2; net70 versus-30 USD; selection contrast1 versus effect0; nonzero null contrast with sum0; endpoint collisions.'],
        [{'local_copy': ref(Path(__file__), 'Independent rational enumeration and algebra')}])]
    write(BASE/'source-audit.json', {'cutoff': '2026-10-07', 'sources': sources,
                                    'primary_review': ref(BASE/'primary-review.json', 'Six selected families')})
    evidence = [ref(p, anchor) for p, anchor in [
        (SYN, 'Connected comparative manuscript'), (BASE/'plan-review.md', 'Reviewed bounded plan'),
        (BASE/'primary-review.json', 'Authenticated pinned code and claim-specific inspection'),
        (BASE/'source-audit.json', 'Nine new citation records'),
        (BASE/'candidate-register.json', 'All searches and retained aliases'),
        (BASE/'omissions-register.json', 'Known remaining work; no absence or waiver'),
        (BASE/'exact-oracle.json', 'Reproducible diagnostic mechanisms'),
        (Path(__file__), 'Review and exact arithmetic procedure'),
    ]]
    verify_bindings(evidence)
    findings = [
        'Five bounded searches and85 inherited identities are retained, with explicit deduplication and cutoff pins for six selected families. Full cell coverage remains inconclusive because pagination, relevant leads and other registries remain open.',
        'All scoped technical claims bind inspected pinned source bytes and licenses; the RCD comparison binds an authentic named original. Exact diagnostics reproduce independently; no execution, confidence calibration or theorem inheritance beyond inspected evidence is claimed.',
        'Alternatives and adoption/port decisions are explicit for six families. Missing scholarly originals, helpers, rights, runtimes and broader coverage have concrete next actions; none is waived or converted into a false absence claim.',
    ]
    write(OUTPUT, {'operation': 'SW.CELL.discovery_latent.other_relevant', 'status': 'inconclusive',
                   'reviewer': REVIEWER, 'scope': 'Bounded source-grounded comparison; full census remains open',
                   'findings': findings, 'evidence': evidence, 'selected_families': 6,
                   'runtime_qualified': False, 'full_cell_coverage': False, 'integration_allowed': False})
    write(BASE/'author-review.json', {'status': 'pass_for_scoped_content', 'reviewer': REVIEWER,
                                    'findings': findings, 'evidence': evidence,
                                    'coverage_outcome': 'inconclusive', 'visual_acceptance': False})
    state = core.read(ROOT, core.STATE)
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, 'SW.CELL.discovery_latent.other_relevant')
    receipt_out = run.ledger.receipt_template(node)
    receipt_out.update(outcome='inconclusive', execution='performed', reviewer=REVIEWER,
        scope='Six selected latent-language families and exact diagnostics; incomplete broader census',
        outputs=[ref(OUTPUT, 'Reviewed coverage disposition')],
        limitations=['Full census, missing method originals and executable qualification remain open.'],
        revisit_trigger='Next declared coverage tranche or acquisition of the listed missing primary sources.')
    for i, finding in enumerate(findings):
        receipt_out['criteria'][i].update(verdict='inconclusive' if i == 0 else 'pass', finding=finding, evidence=evidence)
    write(BASE/'operation-receipt.json', receipt_out)
    print(json.dumps({'selected_families': 6, 'inspected_blobs': sum(len(p['records']) for p in packages),
                      'candidate_identities': len(candidates), 'sources': len(sources), 'outcome': 'inconclusive'}))


if __name__ == '__main__':
    main()
