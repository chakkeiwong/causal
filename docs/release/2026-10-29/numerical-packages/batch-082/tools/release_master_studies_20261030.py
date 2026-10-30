"""Independently reconstruct retained master-study evidence, without draws."""
from collections import Counter
from functools import lru_cache
import hashlib
import math
import statistics

import numpy as np
from scipy.optimize import brentq
from scipy.stats import binom, norm, t


def verify(root, read, raw):
    """Use injected hash-binding readers so relocation checks the same evidence."""
    def close(a, b):
        assert np.allclose(a, b, atol=1e-7, rtol=1e-10), (a, b)

    @lru_cache(maxsize=None)
    def lower(k, n, tail):
        return 0. if not k else brentq(lambda p: binom.sf(k - 1, n, p) - tail,
                                      0., 1., xtol=1e-14)

    @lru_cache(maxsize=None)
    def exact(k, n, error):
        return [lower(k, n, error / 2),
                1. if k == n else brentq(lambda p: binom.cdf(k, n, p) - error / 2,
                                         0., 1., xtol=1e-14)]

    def pieces(value):
        if 'effect_set' in value:
            return [(-math.inf if p['lower'] is None else p['lower'],
                     math.inf if p['upper'] is None else p['upper']) for p in value['effect_set']]
        if 'components' in value:
            return [tuple(p) for p in value['components']]
        bounds = value.get('interval')
        return [] if bounds is None else [(-math.inf if bounds[0] is None else bounds[0],
                                          math.inf if bounds[1] is None else bounds[1])]

    def union(parts):
        result = []
        for lo, hi in sorted(parts):
            assert lo <= hi
            if result and lo <= result[-1][1]:
                result[-1][1] = max(result[-1][1], hi)
            else:
                result.append([lo, hi])
        return result

    studies = []
    request_total = method_cells = derived_intervals = graph_unions = 0
    raw('tools/release_master_studies_20261030.py')
    source = raw('docs/release/2026-10-29/source/docs/writing-repair/2026-10-29/src/456bea026851b50a.tex').decode()
    for folder in ['R01', 'R02', 'R03', 'R04-v3', 'R05-v2']:
        base = 'docs/program/master/work/' + folder + '/'
        spec = read(base + 'protocol.json')
        report = read(base + 'results.json')
        registration = hashlib.sha256(raw(base + 'protocol.json')).hexdigest()
        assert registration == report['registration_sha256']
        for path, digest in spec['input_sha256'].items():
            assert hashlib.sha256(raw(path)).hexdigest() == digest, path
        rows = []
        for path, digest in sorted(report['request_sha256'].items()):
            body = raw(path)
            assert hashlib.sha256(body).hexdigest() == digest, path
            import json
            row = json.loads(body)
            assert row['registration_sha256'] == registration
            assert row['key'] == f"{row['cell']:02d}-{row['index']:05d}"
            rows.append(row)
        expected = {(c, i) for c in range(len(spec['designs'])) for i in range(spec['replications'])}
        assert {(r['cell'], r['index']) for r in rows} == expected
        assert len(rows) == len(expected) == report['requests']
        family = len(spec['designs']) * len(spec['methods'])
        assert family == spec['acceptance_rules']['family']
        close(sum(r['elapsed_seconds'] for r in rows), report['total_request_seconds'])
        assert max(r['process_rss_kib'] for r in rows) == report['max_process_rss_kib']
        cells = []
        for cell_index, design in enumerate(spec['designs']):
            rr = [r for r in rows if r['cell'] == cell_index]
            old_cell = report['cells'][cell_index]
            assert len(rr) == 512 and old_cell['design'] == design
            for key, f in [('mean_elapsed_seconds', lambda r: r['elapsed_seconds']),
                           ('mean_labels', lambda r: r['result'].get('labels', 0)),
                           ('mean_history_rows', lambda r: r['result'].get('history_rows', 0))]:
                close(statistics.mean(f(r) for r in rr), old_cell[key])
            flags, summaries = {}, {}
            for method in spec['methods']:
                old = old_cell['methods'][method]
                covers, widths, errors, ses, retention = [], [], [], [], []
                statuses = Counter()
                topology = dict(whole_line=0, unbounded=0, disconnected=0, empty=0)
                diagnostic95 = diagnostic99 = 0
                for row in rr:
                    data = row['result']
                    value = data['methods'][method]
                    ps = pieces(value)
                    assert all(lo <= hi for lo, hi in ps)
                    covers.append(int(any(lo <= data['truth'] <= hi for lo, hi in ps)))
                    statuses[value['status']] += 1
                    if ps and all(math.isfinite(x) for p in ps for x in p):
                        # The frozen summary reports the finite set's hull width.
                        widths.append(max(hi for lo, hi in ps) - min(lo for lo, hi in ps))
                    if 'effect_set' in value:
                        topology['whole_line'] += int(ps == [(-math.inf, math.inf)])
                        topology['unbounded'] += int(any(not math.isfinite(x) for p in ps for x in p))
                        topology['disconnected'] += int(len(ps) > 1)
                        topology['empty'] += int(not ps)
                    if 'true_class_retained' in value:
                        retention.append(bool(value['true_class_retained']))
                    if 'estimate' in value:
                        errors.append(value['estimate'] - data['truth'])
                    if 'standard_error' in value:
                        ses.append(value['standard_error'])
                        alpha = .05 if method in ['inherited_stacked', 'inherited_double_count', 'audited_policy95'] else spec['alpha']
                        df = (spec['calendars'] - 1 if folder == 'R01' and method == 'replicated_randomized'
                              else data['audited_trajectories'] - 1 if folder == 'R03' else None)
                        critical = norm.isf(alpha / 2) if df is None else t.isf(alpha / 2, df)
                        close(value['interval'], [value['estimate'] - critical * value['standard_error'],
                                                  value['estimate'] + critical * value['standard_error']])
                        derived_intervals += 1
                        for level in [.05, .01]:
                            z = norm.isf(level / 2) if df is None else t.isf(level / 2, df)
                            covered = abs(value['estimate'] - data['truth']) <= z * value['standard_error']
                            if level == .05:
                                diagnostic95 += int(covered)
                            else:
                                diagnostic99 += int(covered)
                    if folder == 'R01' and method == 'replicated_randomized':
                        scores = value['calendar_scores']
                        assert len(scores) == value['calendar_replicates'] == spec['calendars']
                        close(statistics.mean(scores) - 400000, value['estimate'])
                        close(statistics.variance(scores) / len(scores), value['standard_error'] ** 2)
                    if folder == 'R02' and method == 'interaction_adjusted' and 'standard_error' in value:
                        v = value['variance_components']
                        close(1e6 * (v['pair'] + v['calendar'] - v['interaction_subtracted'] + v['gold']), value['standard_error'] ** 2)
                    if folder == 'R02' and method == 'oracle_first_order' and 'standard_error' in value:
                        n, dates, m = design.get('pairs', 100), design.get('dates', 160), design.get('gold', 400)
                        q, e, rho = design.get('q', .4), design.get('error', .08), design.get('rho', .5)
                        a = 1 / (q * (1 - 2 * e) ** 2)
                        covariance = .36 * rho ** np.abs(np.arange(dates)[:, None] - np.arange(dates)[None, :])
                        variance = (.64 * (1 + a) / 2 + .7 ** 2 * (a - 1)) / n
                        variance += covariance.sum() / dates ** 2 + (1 + a) / (2 * n * dates)
                        variance += (1.4 / (1 - 2 * e)) ** 2 * e * (1 - e) / m
                        close(value['standard_error'] ** 2, 1e6 * variance)
                    if folder == 'R03':
                        other = data['methods']['audited_policy95' if method == 'audited_policy99' else 'audited_policy99']
                        assert value['status'] == other['status']
                        for key in ['estimate', 'standard_error', 'final_weight_ess', 'max_weight']:
                            if key in value:
                                close(value[key], other[key])
                        assert data['labels'] == data['history_rows'] == data['audited_trajectories'] * spec['horizon']
                    if folder == 'R04-v3' and method == 'class_union':
                        merged = []
                        true_edges = {'Z_to_A', 'A_to_Y'} | ({'Z_to_Y'} if design.get('direct', 0) else set())
                        support = [1, 2] if design.get('ua', .6) and design.get('uy', .7) else []
                        retained = False
                        for candidate in value['candidates']:
                            graph_parts = [p for graph in candidate['graphs'] for p in pieces(graph)]
                            close(union(graph_parts), pieces(candidate))
                            merged.extend(pieces(candidate))
                            retained |= candidate['rho'] == design.get('rho', .4) and any(
                                set(g['graph']['edges']) == true_edges and g['graph']['latent_support'] == support
                                for g in candidate['graphs'])
                        close(union(merged), ps)
                        assert retained == value['true_class_retained']
                        assert sum(len(c['graphs']) for c in value['candidates']) == value['retained_graphs']
                        graph_unions += 1
                    if folder == 'R05-v2':
                        assert data['actual_features'] == value['features'] == design.get('features', spec['features'])
                        assert data['actual_support'] == design.get('sparsity', spec['sparsity'])
                n, k = len(covers), sum(covers)
                limits, lower_bound = exact(k, n, .05 / family), lower(k, n, .05 / family)
                assert old['requests'] == n and old['covered'] == k and old['finite'] == len(widths)
                assert old['statuses'] == dict(statuses)
                assert old['minimum_95_screen'] == (lower_bound >= .95)
                close(old['coverage_all'], k / n)
                close(old['simultaneous_mc95'], limits)
                close(old['simultaneous_lower95'], lower_bound)
                if 'topologies' in old:
                    assert old['topologies'] == topology
                    assert old['true_class_retained'] == (sum(retention) if retention else None)
                sd = statistics.stdev(errors) if len(errors) > 1 else None
                derived = dict(width_quantiles=np.quantile(widths, [.1, .5, .9]).tolist() if widths else None,
                    conditional_bias=statistics.mean(errors) if errors else None, conditional_sd=sd,
                    mean_se_over_sd=statistics.mean(ses) / sd if ses and sd else None)
                for key, value in derived.items():
                    if value is None:
                        assert old[key] is None
                    else:
                        close(value, old[key])
                flags[method] = covers
                summaries[method] = dict(covered=k, finite=len(widths), minimum_95_screen=lower_bound >= .95,
                    simultaneous_lower95=lower_bound, topology=topology,
                    true_class_retained=sum(retention) if retention else None, **derived,
                    retrospective_level95_covered=diagnostic95 if folder != 'R04-v3' else None,
                    retrospective_level99_covered=diagnostic99 if folder != 'R04-v3' else None)
                method_cells += 1
            for method, old in old_cell['paired_primary'].items():
                delta = [a - b for a, b in zip(flags[spec['methods'][0]], flags[method])]
                assert old['gained'] == delta.count(1) and old['lost'] == delta.count(-1)
                close(old['coverage_difference'], statistics.mean(delta))
                close(old['difference_mc_se'], statistics.stdev(delta) / math.sqrt(len(delta)))
            primary, challenger = [old_cell['methods'][m] for m in spec['methods'][:2]]
            width = '--' if primary['width_quantiles'] is None else (
                f"{primary['width_quantiles'][1]:,.0f}" if folder in ['R01', 'R02', 'R03'] else f"{primary['width_quantiles'][1]:.3f}")
            printed = f"{design['name'].replace('_', ' ')} & {primary['covered']}/512 & {primary['simultaneous_lower95']:.3f} & {primary['finite']}/512 & {width} & {challenger['covered']}/512"
            assert printed in source, (folder, printed)
            cells.append(dict(design=design['name'], methods=summaries))
        studies.append(dict(study=folder, requests=len(rows), family=family, cells=cells))
        request_total += len(rows)
    assert request_total == 22528 and method_cells == 99
    by_study = {s['study']: {c['design']: c['methods'] for c in s['cells']} for s in studies}
    funding = by_study['R01']['baseline']
    assert funding['replicated_randomized']['retrospective_level95_covered'] == 488
    assert funding['inherited_stacked']['retrospective_level99_covered'] == 506
    joint = by_study['R02']
    assert joint['balanced']['inherited_double_count']['retrospective_level99_covered'] == 508
    assert joint['persistent_calendar']['inherited_double_count']['retrospective_level99_covered'] == 442
    assert joint['persistent_calendar']['interaction_adjusted']['retrospective_level95_covered'] == 377
    assert joint['persistent_calendar']['inherited_double_count']['covered'] == 379
    policy = by_study['R03']['baseline']
    assert [policy[m]['covered'] for m in ['audited_policy99', 'audited_policy95']] == [508, 483]
    assert [round(policy[m]['width_quantiles'][1]) for m in ['audited_policy99', 'audited_policy95']] == [735, 559]
    return dict(status='pass', retained_requests=request_total, method_cells=method_cells,
        independently_derived_intervals=derived_intervals, graph_union_reconstructions=graph_unions,
        studies=studies,
        scope='All saved requests, identities, reported summaries and printed table rows; direct interval algebra, funding calendar scores, joint variance decomposition and graph unions. Binomial-tail inversion independently checks exact Monte Carlo bounds. No simulation, nuisance fit, covariance-region construction or original generator rerun. Retrospective critical-level comparisons are diagnostics on these same saved estimates, not fresh qualification or an isolated information-only causal comparison.')
