#!/usr/bin/env python3
"""Prepare bounded authentic-original follow-ups for two unread census entries."""
import json
from pathlib import Path
from urllib.parse import urlencode

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-18/census-biomedical-reasoning-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-18/census-frameworks-v1'


def main():
    assert not BASE.exists()
    register = json.loads((PRIOR / 'census-register.json').read_text())
    selected = ['LA01-candidate-46', 'LA01-candidate-115']
    items = {item['id']: item for item in register['items']}
    assert all(items[key]['disposition'] == 'open_original_not_inspected' for key in selected)
    requests = [dict(id='exec18_biomedical_reasoning_identity',
        url='https://export.arxiv.org/api/query?' + urlencode(dict(id_list='2505.16982,2506.14239')),
        extension='xml')]
    for name, identifier in [('biomedical', '2505.16982'), ('neuron', '2506.14239')]:
        requests += [dict(id='exec18_census_' + name + '_v1',
            url='https://arxiv.org/pdf/' + identifier + 'v1', extension='pdf'),
            dict(id='exec18_census_' + name + '_history',
            url='https://arxiv.org/abs/' + identifier, extension='html')]
    BASE.mkdir()
    (BASE / 'plan.md').write_text(
        'Inspect two authentic originals before changing the preserved census: '
        'Beyond Correlation (candidate46) and Causes in neuron diagrams (candidate115). '
        'Check actual titles, authors, selected revision dates and the7October2026 cutoff. '
        'The v1 acquisition is a deliberately historical selection, not a latest-version claim. '
        'Read methods, causal targets, benchmark construction, experimental units, adverse findings '
        'and limitations. Distinguish the authors\' conceptual proposals and reported observations '
        'from proved identification and local execution. Retain genuinely separate definitions '
        'of causation; do not translate philosophical actual causation into bank intervention '
        'identification without an argument. Record route failures, version limits and claim effects. '
        'Only actually inspected originals may reduce the113-entry census denominator. '
        'Preserve all other records and the fourteen-task mapping. Produce a source review and '
        'connected manuscript development before claiming reader integration. '
        'No downloaded code, model, package or sibling repository will be executed.\n')
    manifest = ROOT / 'docs/literature/fetch-manifest.json'
    write(BASE / 'previous-fetch-manifest.json', json.loads(manifest.read_text()))
    write(BASE / 'acquisition-manifest.json', dict(requests=requests, cutoff='2026-10-07',
        candidates=selected, predecessor=ref(PRIOR / 'census-register.json', '42inspected/71unread original census'),
        stopping_rule='Five registered public reads; no unbounded search, retries, or performance experiment.',
        selected_version='Initial archived revisions; verify actual dates and history before citation.',
        metadata_supports_technical_claims=False))
    write(BASE / 'plan-review.json', dict(status='pass', reviewer=dict(name='Codex author/coordinator', kind='author'),
        evidence=[ref(BASE / 'plan.md', 'Reviewed bounded source inspection and reconciliation plan'),
            ref(BASE / 'acquisition-manifest.json', 'Fixed public acquisition scope')],
        checks=['Two independent original inspections may proceed after reader/sponsor publication.',
            'Authentic bytes and technical anchors precede scholarly claims and census updates.',
            'Philosophical actual causation, learned graphs and statistical effect identification retain distinct semantics.',
            'Historical version coverage and all acquisition failures remain explicit; no frontier completeness or bank validation is implied.',
            'Compilation and extracted text cannot award rendered visual acceptance under the inherited image limit.'],
        global_blocker=None, coverage_acceptance=False))
    write(manifest, dict(requests=requests))
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)), requests=len(requests), selected=selected)))


if __name__ == '__main__':
    main()
