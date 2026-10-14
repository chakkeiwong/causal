#!/usr/bin/env python3
"""Author source/argument review and independent finite second-moment checks."""
from fractions import Fraction as F
from itertools import product
import copy
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/other-discovery'
INPUT = BASE / 'reader-input'
ref = shared.ref


def moments(case):
    length = 13 if case == 3 else 5
    totals = [F(0)]*3
    cross = [[F(0)]*3 for _ in range(3)]
    for bits in product((-1, 1), repeat=length):
        if case == 1:
            u = F(bits[0]); q = u/2+F(sum(bits[1:4]), 2); f = 2*q+bits[4]
        elif case == 2:
            q = F(bits[0]); u = q/2+F(sum(bits[1:4]), 2); f = 2*q+bits[4]
        else:
            f = F(sum(bits[:5])); q = F(2, 5)*f+F(sum(bits[5:10]), 5)
            u = q/2+F(sum(bits[10:]), 2)
        values = [u, q, f]
        for i in range(3):
            totals[i] += values[i]
            for j in range(3):
                cross[i][j] += values[i]*values[j]
    count = 2**length
    assert totals == [0, 0, 0]
    return {'states': count, 'covariance': [[str(v/count) for v in row] for row in cross]}


def main():
    source = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(source)
    register = json.loads((BASE / 'candidate-register.json').read_text())
    shared.verify_refs(register)
    assert register['candidates_count'] == 85 and register['selected_primary_candidates'] == 11
    chapter = BASE / 'comparison.tex'
    cited = {k.strip() for g in re.findall(shared.CITE, chapter.read_text()) for k in g.split(',')}
    keys = {s['integrated_citation_key'] for s in source['sources']}
    assert cited == keys
    results = json.loads((BASE / 'exact-results.json').read_text())
    expected = [['1', '1/2', '1'], ['1/2', '1', '2'], ['1', '2', '5']]
    rows = [moments(i) for i in (1, 2, 3)]
    assert all(r['covariance'] == expected for r in rows)
    for model in results['models'].values():
        observed = [[v['exact'] if isinstance(v, dict) else str(v) for v in row] for row in model['covariance']]
        assert observed == expected
    # Separate recursive intervention substitution, with fixed disturbances.
    assert F(2)*F(1, 4) == F(1, 2)
    assert results['effect_set_quote_slope'] == [0, 2]
    assert results['transpose_error_response'][2]['exact'] == '0'
    threshold = results['threshold_formula_example']
    assert 2.32634 < threshold['nominal_normal_critical'] < 2.32636
    assert not threshold['nominal_rejects'] and threshold['fallback_rejects']
    assert 0.04999 < threshold['normal_reference_size_at_fallback'] < 0.05001
    numerical = {'status': 'pass', 'issues': [], 'reviewer': 'Author/coordinator',
        'independent_auxiliary_enumerations': rows,
        'scope': 'Finite independent sign disturbances reproduce the stipulated second moments only. They are not Gaussian samples; equality of the Gaussian distributions in the chapter follows from the declared Gaussian laws and equal covariance.',
        'intervention_check': 'Direct equation replacement gives funding +1/2, +1/2 and 0; the transposed first model gives 0.',
        'threshold_check': 'For alpha .02 the normal critical value lies in (2.32634,2.32636); 2.2 lies above 1.960 and below this critical value.',
        'results': ref(BASE / 'exact-results.json', 'Preserved exact examples'),
        'replay': ref(BASE / 'exact-replay.json', 'Byte-identical pure replay'),
        'review_code': ref(Path(__file__), 'Independent finite second-moment enumeration'),
        'package_executions': 0, 'bank_data': False, 'runtime_performance': False}
    core.write(BASE / 'exact-review.json', numerical)
    INPUT.mkdir(exist_ok=True)
    final_source = copy.deepcopy(source)
    for s in final_source['sources']:
        if s['kind'] == 'software_primary_sources':
            # The preliminary audit was already checkpointed. Preserve it,
            # and expose its explicit inspected anchors in the reader schema.
            s['inspected_anchors'] = [r['local_copy'] for r in s['records']]
    final_source['preliminary_audit'] = ref(BASE / 'source-audit.json', 'Unchanged acquisition/inspection checkpoint')
    final_source['schema_note'] = 'Explicit inspected source anchors copied to the established reader field; no source bytes, identity or supported claim changed.'
    core.write(INPUT / 'source-audit.json', final_source)
    findings = [
        'The chapter develops eleven inspected families with their actual algorithm/interface roles and conditional reuse choices.',
        'Every new citation binds saved primary bytes, cutoff commit, acquisition date, inspected anchors and supported claims. No unacquired scholarly paper is cited or credited with a theorem.',
        'The finite Gaussian construction specifies independent disturbances and three structural laws; intervention ambiguity is separate from a transpose error.',
        'Significance-threshold and zero-denominator findings refer to inspected source; no empirical type-I error or package execution is claimed.',
        'Cached-ordering, dispatch/default and timeout findings are bounded to inspected paths; no blanket correctness/incorrectness or performance claim.',
        'Rights and platform conditions remain candidate-specific. Causal Explorer is not accepted as an unrestricted dependency; embedded licenses are not generalized to whole repositories.',
        'The 74 metadata-only candidates, missing scholarly originals and broader language coverage prevent full-cell acceptance. The chapter remains useful as a scoped source comparison.',
        'No predecessor manuscript or cited audit record is edited; visual and whole-program acceptance remain separate.'
    ]
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Selected substantive source comparison and exact examples only, not full coverage acceptance',
        'chapter': ref(chapter, 'Connected comparative argument, examples, conditions and alternatives'),
        'findings': findings, 'evidence': [ref(BASE / name, name) for name in
            ['plan-review.md', 'source-audit.json', 'candidate-register.json', 'omissions-register.json', 'exact-review.json']]
            +[ref(INPUT / 'source-audit.json', 'Reader-schema source audit preserving initial evidence')],
        'cell_outcome': 'inconclusive', 'full_cell_coverage_accepted': False,
        'visual_acceptance': False, 'independent_review': False, 'runtime_qualification': False}
    core.write(BASE / 'author-review.json', review)
    print(json.dumps({'author_review': 'pass_with_scope_limits', 'full_cell_outcome': 'inconclusive',
                      'independent_moment_states': [r['states'] for r in rows], 'cited_sources': len(keys)}))


if __name__ == '__main__':
    main()
