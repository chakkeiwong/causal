#!/usr/bin/env python3
"""Bind selected inspected originals and preserve finite-search omissions."""
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/python-discovery'
RAW = ROOT / 'docs/literature/raw'


def ref(path, anchor):
    path = Path(path)
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def write(name, value):
    p = BASE / name
    if p.exists():
        assert json.loads(p.read_text()) == value, 'Preserve existing evidence: '+name
    else:
        p.write_text(json.dumps(value, indent=2)+'\n')


def original(name, anchor):
    receipt_path = RAW / (name+'.receipt.json')
    receipt = json.loads(receipt_path.read_text())
    p = ROOT / receipt['path']
    assert receipt['status'] == 'saved' and hashlib.sha256(p.read_bytes()).hexdigest() == receipt['sha256']
    return {'local_copy': ref(p, anchor), 'source_identity': receipt['url'],
            'accessed_utc': receipt['accessed_utc'], 'receipt': ref(receipt_path, 'Original acquisition status and byte identity'),
            'role': 'inspected_primary_technical_text'}


def decoded(name, target, anchor):
    record = original(name, 'GitHub content response binding decoded original')
    payload = json.loads((ROOT / record['local_copy']['path']).read_text())
    p = ROOT / target
    assert base64.b64decode(payload['content']) == p.read_bytes()
    record['encoded_original'] = record['local_copy']
    record['local_copy'] = ref(p, anchor)
    return record


def main():
    sources = []
    config = [
        ('causallearn', 'py-why/causal-learn', '0dacacf36390e3084704636bc3c36e82e35ee0cc', '2026-09-04',
         ['causal-learn', 'causallearn', 'causal_learn'],
         [('v12_sw2_source_causallearn_pc', 'pc and pc_alg, lines20-142: tests, collider rules, endpoint return encoding'),
          ('v12_exec13_pydisc_causallearn_extra_1', 'ges, lines11-60: score choices and CPDAG endpoint contract'),
          ('v12_exec13_pydisc_causallearn_extra_2', 'local_score_BIC, lines1-100: residual variance, pseudoinverse, variance clamp'),
          ('v12_exec13_pydisc_causallearn_extra_4', 'FisherZ lines193-228; KCI lines230-260: test calculation and singularity')],
         ['PC encodes endpoint types and exposes missing-value and collider choices.',
          'FisherZ inverts a correlation submatrix, raises for singularity and uses sqrt(n-|S|-3).',
          'GES exposes multiple scores; its numeric scores cannot be assumed comparable across engines.'],
         'Integrate selected PC/GES through a typed graph adapter; preserve test and endpoint semantics.'),
        ('causalnex', 'mckinsey/causalnex', 'b87ab20599876af8d15d20f317cfcd591b28b32a', '2026-08-31',
         ['CausalNex', 'causalnex', 'quantumblacklabs/causalnex', 'mckinsey/causalnex'],
         [('v12_exec13_pydisc_causalnex_source_2', 'Apache2 license and separate trademark terms'),
          ('v12_exec13_pydisc_causalnex_source_3', 'from_numpy/from_pandas lines57-344; _learn_structure lines351-439; lasso threshold line549'),
          ('v12_exec13_pydisc_causalnex_source_4', 'StructureModel edge origin lines90-145; threshold_till_dag lines286-293'),
          ('v12_exec13_pydisc_causalnex_source_5', 'setup lines65-91: Python>=3.8,<3.11 and dependencies')],
         ['Tabu direction constraints are optimization bounds; selected unpenalized path does not center input.',
          'The StructureModel supports an explicit destructive threshold_till_dag operation that warns about units.',
          'The pinned package declares Python>=3.8,<3.11.'],
         'Defer default adoption; compare an isolated older-Python path only for a concrete StructureModel consumer.'),
        ('causica', 'microsoft/causica', 'c3b7dd2b09fe0efb543adb05b89716d0dbdee780', '2026-08-24',
         ['Causica', 'causica', 'DECI'],
         [('v12_exec13_pydisc_causica_source_1', 'README Model Description, Simulation-based Causal Inference and Further extensions'),
          ('v12_exec13_pydisc_causica_source_2', 'MIT permission and notice terms'),
          ('v12_exec13_pydisc_causica_source_3', 'DECIModule setup/training_step lines165-223; test_step methods lines249-310'),
          ('v12_exec13_pydisc_causica_source_4', 'DECIEmbedFunctionalRelationships wrapper and forward method'),
          ('v12_exec13_pydisc_causica_source_5', 'ExpertGraphContainer and GibbsDAGPrior sparsity/expert terms')],
         ['The module optimizes a variational/noise/function objective with a DAG penalty and graph prior.',
          'Documented DECI intervention simulation is conditional on its learned SEM; not calibrated causal uncertainty.',
          'The inspected README states that Rhino and DDECI were removed from this refactored codebase.'],
         'Retain as a separate experimental SEM backend; defer general bank discovery/effect admission.'),
        ('gcastle', 'huawei-noah/trustworthyAI', 'fd8a04f3b57a0f00930406257d5c30dcb91da0a5', '2026-05-29',
         ['gCastle', 'gcastle', 'castle', 'trustworthyAI/gcastle'],
         [('v12_exec13_pydisc_gcastle_source_1', 'README algorithm catalog and use of castle imports'),
          ('v12_exec13_pydisc_gcastle_source_2', 'Apache2 root license'),
          ('v12_exec13_pydisc_gcastle_source_3', 'Notears learn lines94-118; polynomial _h lines154-163; loss centering lines196-199'),
          ('v12_exec13_pydisc_gcastle_source_4', 'PC constructor/learn lines26-124; orient skeleton and separation-set processing'),
          ('v12_exec13_pydisc_gcastle_source_5', 'setup distribution and package requirements')],
         ['The selected Notears uses a polynomial DAG constraint and separate weighted/binary outputs.',
          'Binary edges use abs(weight)>threshold, whereas the reference removes abs(weight)<threshold.',
          'PC has original/stable/parallel variants and multiple CI tests; these are separate mechanisms.'],
         'Keep as a matched comparison backend; preserve the chosen algorithm and do not equate class names with numerical parity.'),
        ('dagma', 'kevinsbello/dagma', '088616885d71b56c0573cd4902c1fcbac02e649f', '2024-01-14',
         ['DAGMA', 'dagma', 'DagmaLinear'],
         [('v12_exec13_pydisc_dagma_source_2', 'Apache2 license'),
          ('v12_exec13_pydisc_dagma_source_3', '_score/_h lines41-89; domain backtracking lines180-207; fit lines228-362'),
          ('v12_exec13_pydisc_dagma_source_5', 'pyproject declared Python and numpy/scipy/torch/igraph dependencies')],
         ['Linear loss uses column response XW and log-determinant acyclicity.',
          'fit documents possible cyclic output and no guarantee on requested included edges.',
          'fit centers its supplied array in place and saves h_final before thresholding; adapter must protect input and recompute diagnostics.'],
         'Integrate linear discovery as a research baseline with independent topology, domain and input-mutation checks; defer nonlinear admission.'),
        ('notears', 'xunzheng/notears', '4a9ab19fe502e392503da331773c5223d82d3666', '2026-05-26',
         ['NOTEARS', 'notears', 'notears_linear'],
         [('v12_exec13_pydisc_notears_source_2', 'Apache2 license'),
          ('v12_exec13_pydisc_notears_source_3', 'notears_linear lines7-87; _h lines40-49; loss/centering/threshold'),
          ('v12_exec13_pydisc_notears_source_5', 'setup package identity and dependency declaration')],
         ['Reference linear loss predicts XW and centers least-squares inputs.',
          'Exponential DAG constraint, augmented-Lagrangian stopping, L1 penalty and post-fit threshold are distinct choices.',
          'The demonstration main performs a separate is_dag check.'],
         'Adopt the small reference as an isolated numerical baseline; prefer wrapping to a new port until parity and usefulness are established.'),
        ('pgmpy', 'pgmpy/pgmpy', '1f6296fc2606eb479f1f1b9fbfdd9c41aa7ad312', '2026-10-05',
         ['pgmpy', 'pgmpy.causal_discovery.PC', 'pgmpy.causal_discovery.GES'],
         [('v12_exec13_pydisc_pgmpy_source_1', 'PC parameters and return types lines13-110; current causal_discovery API'),
          ('v12_exec13_pydisc_pgmpy_source_2', 'GES parameters lines14-118; phases lines280-520; final pdag/dag conversion')],
         ['Current PC and GES expose a partially directed output and optional selected DAG.',
          'PC defaults to max_cond_vars=5; GES uses forward/backward/turning steps and minimum score improvement.',
          'Causal-discovery modules inspected here differ from the separately inherited LLM pairwise path.'],
         'Integrate the pinned graph objects and selected PC/GES; explicitly request pdag and reject silent DAG completion.'),
        ('lingam', 'cdt15/lingam', '0f089670dbb2a470c3ef43bc0f34ef823ae59a0a', '2026-09-08',
         ['LiNGAM', 'lingam', 'cdt15/lingam', 'DirectLiNGAM'],
         [('v12_gap3_lingam_license', 'MIT license and retained notices'),
          ('v12_gap3_lingam_technical', 'DirectLiNGAM constructor and fit lines15-124'),
          ('v12_gap4_lingam_base', '_estimate_adjacency_matrix lines123-167, B[target,predictors]'),
          ('v12_exec13_pydisc_lingam_extra_1', 'predict_adaptive_lasso lines756-794; find_all_paths lines797-872; calculate_total_effect lines1084-1156')],
         ['The selected DirectLiNGAM chooses an order and estimates B[target,predictor].',
          'The helper standardizes for BIC pruning and refits selected predictors on original units.',
          'The total-effect helper sums products along continuous directed paths of a supplied coefficient matrix.'],
         'Integrate only under an explicit linear non-Gaussian, causally sufficient scope; transpose matrices at the typed boundary.'),
        ('cdt', 'FenTechSolutions/CausalDiscoveryToolbox', 'ff46dbca3d91f2dba30e6ae54986eea30c9b331f', '2025-10-13',
         ['CDT', 'cdt', 'CausalDiscoveryToolbox', 'FenTechSolutions/CausalDiscoveryToolbox'],
         [('v12_exec13_pydisc_cdt_source_2', 'MIT repository license'),
          ('v12_exec13_pydisc_cdt_source_3', 'PC dependency checks lines173-179, R dispatch lines284-311'),
          ('v12_exec13_pydisc_cdt_source_4', 'GES pcalg check and score map lines106-126; sorted node relabeling lines141-148'),
          ('v12_exec13_pydisc_cdt_source_5', 'setup version0.6.0 and conflicting Apache2 license metadata')],
         ['Selected PC/GES delegate to R; PC checks pcalg/kpcalg/RCIT and GES checks pcalg.',
          'Repository MIT text conflicts with Apache2 setup metadata; downstream licenses are separate.',
          'GES documentation labels int categorical, but code selects GaussL0penIntScore; do not infer a discrete likelihood from the label.'],
         'Defer porting/default adoption; compare direct R and wrapper paths after template, ordering and terms review.'),
    ]
    candidates = []
    for key, repo, pin, day, aliases, files, claims, decision in config:
        records = [original(n, a) for n, a in files]
        if key == 'causallearn':
            records.append(decoded('license_causallearn', 'docs/literature/raw/license_causallearn.txt',
                                   'MIT text; mutable-main snapshot acquired2026-10-07, not asserted at technical commit'))
        if key == 'pgmpy':
            records.append(decoded('v12_sw_pinned_license_pgmpy', 'docs/program/repair-v12/work/SW01/extracted/pinned-pgmpy-LICENSE.txt', 'Pinned MIT license'))
        source = {'integrated_citation_key': 'exec13_pydisc_'+key, 'kind': 'software_primary_sources',
                  'title': aliases[0]+': selected static discovery implementation and terms', 'author': repo,
                  'year': 2026, 'source_identity': 'https://github.com/'+repo,
                  'version_date': pin+'; commit '+day+'; accessed 12–13 October2026; cutoff7 October2026 Asia/Shanghai',
                  'local_copy': records[0]['local_copy'], 'records': records, 'claims': claims,
                  'limits': 'Selected source review only; no engine execution, performance ranking, calibration or bank qualification.'}
        sources.append(source)
        candidates.append({'id': key, 'aliases': aliases, 'repository': repo, 'commit': pin, 'commit_date': day,
                           'source_key': source['integrated_citation_key'], 'bounded_disposition': decision,
                           'search_route': 'Inherited coverage and official pinned repository; canonical namespace recovery when necessary.'})
    registry = json.loads((ROOT/'docs/literature/sources.json').read_text())
    registry = registry if isinstance(registry, list) else registry['sources']
    for key, anchor, claims in [
            ('dagma2022', 'PDF pp4–5, Definition1, domain Ws, Theorem1; p4 separate identifiability premise',
             ['Log-determinant characterization is valid on s>spectral_radius(W elementwise squared).', 'Identifiability of the model is a separate premise.']),
            ('shimizu2006', 'PDF pp1–3, Section2 assumptions; original ICA method distinct from current DirectLiNGAM implementation',
             ['Linear acyclic equations, independent non-Gaussian disturbances, repeated independent vectors and causal sufficiency define the original model.'])]:
        s = next(x for x in registry if x['id'] == key)
        p = ROOT/s['local_path']; assert p.read_bytes().startswith(b'%PDF-') and hashlib.sha256(p.read_bytes()).hexdigest() == s['sha256']
        sources.append({'integrated_citation_key': 'exec13_pydisc_'+key, 'kind': 'paper', 'title': s['title'],
                        'author': s['authors'].replace(r'\u00e4', 'ä'), 'year': s['year'], 'source_identity': s['url'],
                        'filename_title': s['filename_title'], 'first_author': s['first_author'],
                        'version_date': s['version_status'], 'local_copy': ref(p, anchor),
                        'local_path': s['local_path'], 'sha256': s['sha256'], 'accessed': s['accessed'],
                        'text': ref(ROOT/s['text_path'], anchor), 'inspected': [anchor], 'claims': claims,
                        'limits': 'Inherited premise; no theorem for the proposed full bank workflow.'})
    example = BASE/'oracle-results.json'
    sources.append({'integrated_citation_key': 'exec13_pydisc_examples', 'kind': 'project_analysis',
                    'title': 'Exact funding orientation, observational equivalence and numerical diagnostics',
                    'author': 'Causal banking proposal project', 'year': 2026, 'source_identity': str(example.relative_to(ROOT)),
                    'version_date': '13 October2026; deterministic generated examples, no package execution',
                    'local_copy': ref(example, 'Six exact/algebraic examples'),
                    'code': ref(ROOT/'tools/python_discovery_examples_20261013.py', 'Reproducible project algebra'),
                    'claims': ['Funding change is USD0.25million under the declared 0.25pp intervention.',
                               'Gaussian same-law models have effects0 and0.6.', 'A two-cycle can have all three acyclicity residuals below1e-8.'],
                    'limits': 'Hypothetical financial coefficients; no observed bank data or fitted discovery result.'})
    write('source-audit.json', {'cutoff': '2026-10-07 Asia/Shanghai', 'sources': sources})
    query = json.loads((RAW/'v12_sw_cell_discovery_iid_python.json').read_text())
    hits = [{'id': r['id'], 'title': r['display_name'], 'date': r['publication_date'],
             'status': 'discovery_metadata_only; technical claims require an independently inspected original'} for r in query['results']]
    write('candidate-register.json', {'candidate_scope': 'Seven inherited Python candidates plus LiNGAM successor and CDT neighbor',
        'cutoff': '2026-10-07 Asia/Shanghai', 'candidates': candidates, 'search': original('v12_sw_cell_discovery_iid_python', 'Discovery identity only; first10 of655 metadata hits'),
        'metadata_hits': hits, 'total_hits': query['meta']['count'], 'inspected_metadata_hits': len(hits),
        'stopping_rule': ref(BASE/'plan-review.md', 'Bounded inherited-candidate acquisition rule'),
        'recovery': ref(BASE/'recovery-audit.json', 'Saved52 acquisition receipts,51 successful; hash checked'),
        'special_dispositions': ['Old CausalNex namespace404 is resolved by canonical mckinsey source; not evidence of abandonment.',
                                'Causica UTC-end-of-day query returned a commit after the local cutoff. Only the earlier local-cutoff commit supports claims.',
                                'CDT and cdt15/lingam are distinct projects; the substring cdt is not an alias relation.'],
        'exhaustive_ecosystem_coverage': False})
    omissions = [
        {'id': 'PY-CENSUS', 'essential_for_cell_completion': True,
         'gap': 'The inherited search inspects10 of655 metadata results. ENCO, reinforcement-learning DAG search and attention-based discovery appear as unresolved neighboring method families.',
         'action': 'Run a reviewed finite complementary repository/package-index search; identify canonical implementations and original papers for those three families; disposition aliases and duplicates. Do not infer absence or current maintenance from the truncated search.',
         'blocks': 'Full static-Python candidate coverage; does not block the nine-family comparison or other cells.'},
        {'id': 'CDT-DELEGATES', 'essential_for_cell_completion': True,
         'gap': 'Selected wrappers are inspected; R templates, delegated-version combinations, node order and conflicting license metadata are not resolved.',
         'action': 'Inspect pinned pc.R/ges.R and the wrapper launcher, bind delegated R package versions and terms, then specify positive/negative round-trip fixtures. Keep the documented int-label conflict unresolved until traced.',
         'blocks': 'CDT adoption/porting and full wrapper coverage, not direct Python comparisons.'},
        {'id': 'CAUSALLEARN-LICENSE-PIN', 'essential_for_cell_completion': False,
         'gap': 'MIT text is an authentic snapshot acquired on the cutoff date; it is not asserted to match the selected technical commit.',
         'action': 'Retrieve LICENSE at0dacacf before any distribution or vendoring decision; current use is a conditional proposal.'},
        {'id': 'EXTENDED-METHODS', 'essential_for_cell_completion': False,
         'gap': 'Full nonlinear, missing-data, latent-variable, temporal and catalog implementations are outside these selected static paths.',
         'action': 'Use their dedicated coverage cells and candidate reuse decisions; do not export static findings as support for every method in a package.'},
        {'id': 'RUNTIME-AND-CALIBRATION', 'essential_for_cell_completion': False,
         'gap': 'No reviewed downloaded engine was executed or statistically qualified here.',
         'action': 'After source and adapter admission, prospectively register matched known-truth and failure cases before any accuracy or interval-coverage claim.'},
    ]
    write('omissions-register.json', {'cutoff': '2026-10-07', 'omissions': omissions,
                                     'no_unavailable_original_replaced': True, 'whole_cell_outcome': 'inconclusive'})
    print(json.dumps({'sources': len(sources), 'candidates': len(candidates), 'essential_omissions': 2}))


if __name__ == '__main__':
    main()
