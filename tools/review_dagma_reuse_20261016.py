#!/usr/bin/env python3
"""Bounded original-source review and behavioral oracles for DAGMA reuse."""
import argparse
import contextlib
import hashlib
import importlib.metadata
import importlib.machinery
import importlib.util
import io
import json
import math
from pathlib import Path
import platform
import signal

import numpy as np

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-16/dagma-reuse'
RAW = ROOT/'docs/literature/raw'
PIN = '088616885d71b56c0573cd4902c1fcbac02e649f'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
OP = 'SW.DECISION.inherited_dagma'
OUTPUT = ROOT/'docs/program/comprehensive-v14/work'/OP/'decision.json'
LIMITS = [
    'Only the saved original linear source module was executed; dagma, torch and igraph are not installed.',
    'Tiny deterministic source-module probes are contract evidence, not package qualification, accuracy or speed benchmarks.',
    'Nonlinear behavior was inspected statically; authored function examples are not PyTorch executions.',
    'Complete dependency/notice closure, release version, maintained build and native adapter remain unqualified.',
    'No causal identifiability, graph/effect coverage, bank data validation or bank ROI follows from acyclicity.',
    'Source search is bounded to saved originals at the declared cutoff; no exhaustive current census.',
    'Rendered visual acceptance remains open under the exhausted inherited session image allowance.']


def source_review():
    rows = []
    tree_path = RAW/'v12_exec13_pydisc_dagma_tree.json'
    tree = json.loads(tree_path.read_text()); assert not tree['truncated']
    entries = {x['path']: x for x in tree['tree']}
    specs = [
        ('README.md', 'Paper identity, features, requirements, NOTEARS acknowledgment'),
        ('LICENSE', 'Apache 2.0 sections 2–4, 7–9; attribution and modification duties'),
        ('src/dagma/linear.py', '_score lines 41–57; _h 77–80; minimize 178–228; fit 307–364'),
        ('src/dagma/nonlinear.py', 'DagmaMLP.forward, h_func and fc1_to_adj; nonnegative first-layer norm output'),
        ('pyproject.toml', 'Python >=3.7; alpha classifier; five unpinned dependencies; src/VERSION reference')]
    for i, (name, anchor) in enumerate(specs, 1):
        p = RAW/f'v12_exec13_pydisc_dagma_source_{i}.txt'
        receipt_path = p.with_name(p.stem+'.receipt.json'); receipt = json.loads(receipt_path.read_text())
        data = p.read_bytes(); blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert hashlib.sha256(data).hexdigest() == receipt['sha256']
        assert blob == entries[name]['sha'] and '/'+PIN+'/' in receipt['url']
        rows.append({'source_identity': receipt['url'], 'version_date': PIN+'; 2024-01-14',
                     'local_copy': ref(p, anchor), 'receipt': ref(receipt_path, 'Original acquisition identity'),
                     'git_blob_sha1': blob, 'inspected_anchors': [anchor]})
    cutoff = json.loads((RAW/'v12_exec13_pydisc_dagma_cutoff.json').read_text())[0]
    assert cutoff['sha'] == PIN
    prior = json.loads((ROOT/'docs/program/execution/2026-10-16/commercial-survival/publication/reader/source-audit.json').read_text())
    paper = next(s for s in prior['sources'] if s['integrated_citation_key'] == 'exec13_pydisc_dagma2022')
    verify_bindings(paper)
    assert (ROOT/paper['local_path']).read_bytes().startswith(b'%PDF')
    write(BASE/'source-review.json', {
        'status': 'pass', 'scope': 'Pinned original source and primary technical review', 'reviewer': REVIEWER,
        'sources': rows, 'tree': ref(tree_path, 'Nontruncated pinned Git tree'),
        'commit': ref(RAW/'v12_exec13_pydisc_dagma_cutoff.json', 'Saved latest-before-cutoff commit observation'),
        'paper': paper,
        'additional_paper_anchors': ['Section 2, p4: identifiable model chosen as a premise',
                                    'Definition 1 and Theorem 1, pp4–5: nonsingular M-matrix domain',
                                    'Algorithm 1, Lemma 6 and Section 4.1, p8: limiting central path versus finite optimizer'],
        'maintenance_observations': {
            'commit_date': cutoff['commit']['committer']['date'],
            'test_named_paths': [p for p in entries if 'test' in p.lower()],
            'version_file_in_pinned_tree': 'src/VERSION' in entries,
            'version_limit': 'Do not guess a release number from the missing referenced src/VERSION; identify by commit.',
            'test_limit': 'Demo/test-named paths and inline test() are evidence of examples, not a verified CI result or support commitment.',
            'cutoff_limit': 'Saved query used UTC end-of-day; returned January 2024 commit precedes the client Asia/Shanghai cutoff too.'},
        'license_obligations': ['Apache 2.0 license copy, retained notices, marked modifications and applicable NOTICE obligations.',
                                'Review the complete distribution and dependency terms before shipping; root license is not transitive clearance.'],
        'limitations': LIMITS})
    print(json.dumps({'source_review': 'pass', 'original_blobs': len(rows), 'paper_pdf': True, 'version_file_present': 'src/VERSION' in entries}))


def acyclic(w):
    edges = np.asarray(w) != 0
    indegree = edges.sum(axis=0).astype(int); todo = list(np.flatnonzero(indegree == 0)); count = 0
    while todo:
        node = todo.pop(); count += 1
        for target in np.flatnonzero(edges[node]):
            indegree[target] -= 1
            if indegree[target] == 0: todo.append(int(target))
    return count == len(w)


def probe():
    verify_bindings(json.loads((BASE/'source-review.json').read_text()))
    p = RAW/'v12_exec13_pydisc_dagma_source_3.txt'
    loader = importlib.machinery.SourceFileLoader('reviewed_original_dagma_linear', str(p))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    versions = {'python': platform.python_version()}
    for name in ['numpy', 'scipy', 'tqdm', 'dagma', 'torch', 'igraph']:
        try: versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: versions[name] = None
    results = []
    def deadline(*_): raise TimeoutError('20-second per-case source-module bound exceeded')
    old_handler = signal.signal(signal.SIGALRM, deadline)
    data = np.array([[1., 2.], [2., 4.], [3., 6.], [4., 8.]])
    config = dict(T=1, warm_iter=4, max_iter=4, checkpoint=1, lr=0.01, lambda1=0.03, s=1.0)
    cases = [
        ('tiny_unthresholded', data.copy(), {'w_threshold': 0}),
        ('thresholded_diagnostics', data.copy(), {'w_threshold': 0.3}),
        ('tuple_exclusion', data.copy(), {'w_threshold': 0, 'exclude_edges': ((0, 1),)}),
        ('list_exclusion', data.copy(), {'w_threshold': 0, 'exclude_edges': [(0, 1)]}),
        ('included_edge_zero_signal', np.zeros((4, 2)), {'w_threshold': 0.3, 'include_edges': ((0, 1),)}),
        ('integer_input', data.astype(int), {'w_threshold': 0.3}),
        ('empty_exclusion_tuple', data.copy(), {'w_threshold': 0.3, 'exclude_edges': ()})]
    try:
        for name, x, extra in cases:
            model = module.DagmaLinear('l2'); initial = x.copy(); log = io.StringIO()
            row = {'case': name, 'input': initial.tolist(), 'dtype': str(x.dtype), 'configuration': dict(config, **extra)}
            try:
                signal.setitimer(signal.ITIMER_REAL, 20)
                with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                    w = model.fit(x, **config, **extra)
                row.update(status='returned', output=w.tolist(), acyclic=acyclic(w),
                           h_saved=float(model.h_final), h_returned_s1=float(model._h(w, 1.0)[0]),
                           score_saved=float(model.score_final), score_returned=float(model._score(w)[0]),
                           input_after=x.tolist(), input_changed=not np.array_equal(x, initial))
            except Exception as exc:
                row.update(status='exception', exception_type=type(exc).__name__, message=str(exc), input_after=x.tolist())
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
            results.append(row)
    finally:
        signal.signal(signal.SIGALRM, old_handler)
    indexed = {r['case']: r for r in results}
    assert indexed['tiny_unthresholded']['input_changed'] and not indexed['tiny_unthresholded']['acyclic']
    assert indexed['tuple_exclusion']['output'][0][1] == 0
    assert indexed['list_exclusion']['output'][0][1] != 0
    assert indexed['included_edge_zero_signal']['output'][0][1] == 0
    assert indexed['integer_input']['status'] == 'exception' and indexed['empty_exclusion_tuple']['status'] == 'exception'
    assert indexed['thresholded_diagnostics']['h_returned_s1'] == 0 and indexed['thresholded_diagnostics']['h_saved'] > 0
    m = module.DagmaLinear('l2'); m.d = 2; m.Id = np.eye(2)
    w = np.array([[0., 0.2], [0.3, 0.]])
    s = 1.3; h, grad = m._h(w, s); delta = 1e-6; finite = np.zeros_like(w)
    for i in range(2):
        for j in range(2):
            e = np.zeros_like(w); e[i, j] = delta
            finite[i, j] = (m._h(w+e, s)[0] - m._h(w-e, s)[0])/(2*delta)
    expected = -math.log1p(-(0.2*0.3/s)**2)
    assert abs(h-expected) < 1e-12 and np.max(np.abs(grad-finite)) < 1e-8
    invalid = np.diag([math.sqrt(2), math.sqrt(2)])
    bad_h, _ = m._h(invalid, 1.0)
    assert abs(bad_h) < 1e-12 and not acyclic(invalid)
    outside = np.array([[0., 2.], [1., 0.]])
    outside_h, _ = m._h(outside, 1.0)
    assert abs(outside_h+math.log(3)) < 1e-12
    w3 = np.array([[0., 2., 1.], [0., 0., 3.], [0., 0., 0.]])
    scales = np.array([10., 1., 100.]); wz = scales[:, None]*w3/scales[None, :]
    total = np.linalg.inv(np.eye(3)-w3)-np.eye(3)
    total_z = np.linalg.inv(np.eye(3)-wz)-np.eye(3)
    assert total[0, 2] == 7 and abs(total_z[0, 2]-0.7) < 1e-14
    exact = {
        'valid_domain_gradient': {'W': w.tolist(), 's': s, 'h_native': float(h), 'h_closed_form': expected,
                                  'gradient': grad.tolist(), 'central_difference': finite.tolist(),
                                  'max_error': float(np.max(np.abs(grad-finite)))},
        'outside_domain': {'self_loop_example': invalid.tolist(), 'native_logabs_value': float(bad_h),
                           'spectral_radius': 2, 'acyclic': False,
                           'two_cycle_example': outside.tolist(), 'native_two_cycle_value': float(outside_h),
                           'explanation': 'The helper can return zero or negative outside the theorem domain; this is not a claim that fit accepted these states.'},
        'units_and_paths': {'W': w3.tolist(), 'scales': scales.tolist(), 'transformed_W': wz.tolist(),
                            'total_original_0_to_2': float(total[0, 2]), 'total_transformed_0_to_2': float(total_z[0, 2]),
                            'identity': 'Z=X D^-1 and W_Z=D W_X D^-1; total path coefficients transform alike.',
                            'fixed_raw_threshold': 0.5, 'remaining_original_edges': int(np.sum(np.abs(w3) >= 0.5)),
                            'remaining_scaled_edges': int(np.sum(np.abs(wz) >= 0.5))},
        'nonlinear_norm_counterexample': {
            'functions': ['4*sigmoid(2*x)-2', '-4*sigmoid(2*x)+2'], 'first_layer_norm_both': 2,
            'baseline_both': 0, 'derivative_at_zero': [2, -2],
            'stipulated_USD_per_outcome_unit': 100, 'stipulated_USD_cost_per_intensity_unit': 20,
            'local_net_derivative_USD': [180, -220],
            'scope': 'Authored one-parent sigmoid SEMs; exact local derivatives, not finite-change claims or PyTorch execution.'}}
    write(BASE/'runtime-probes.json', {'status': 'pass_bounded_oracles', 'runtime': versions,
          'mode': 'Actual execution of unchanged saved linear.py; no package install or service adapter',
          'cases': results, 'source': ref(p, 'Exact executed original module'),
          'harness': ref(Path(__file__), 'Bounded execution and independent references'), 'limitations': LIMITS})
    write(BASE/'exact-results.json', exact)
    print(json.dumps({'native_cases': len(results), 'statuses': {r['case']: r['status'] for r in results},
                      'gradient_max_error': exact['valid_domain_gradient']['max_error'], 'adapter_enabled': False}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['source', 'probe'])
    args = p.parse_args(); {'source': source_review, 'probe': probe}[args.command]()
