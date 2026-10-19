#!/usr/bin/env python3
"""Prepare a bounded, source-grounded Feast proposal decision."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-19/feast-reuse-v1'


def main():
    assert not BASE.exists()
    BASE.mkdir(parents=True)
    manifest = ROOT / 'docs/literature/fetch-manifest.json'
    write(BASE / 'previous-fetch-manifest.json', json.loads(manifest.read_text()))
    (BASE / 'plan.md').write_text(
        '# Feast proposal reuse review, 19 October 2026\n\n'
        'Resolve inherited_feast as a feature-retrieval candidate for the banking proposal. '
        'First identify an immutable original revision dated no later than the client cutoff '
        'of 7 October 2026 (Asia/Shanghai), then authenticate selected technical blobs against '
        'its complete Git tree. The inherited mutable-branch artifacts and failed pin lookup '
        'remain evidence of their own observations, not evidence for the new revision.\n\n'
        'Inspect root license, dependency declarations, historical versus online retrieval, '
        'event-time windows, creation-time filtering, provider dispatch, duplicate revisions, '
        'missingness and error paths. Separate event, creation, ingestion, actual availability '
        'and decision clocks. Inspect an actual provider implementation and relevant test '
        'specifications before extending an API-level claim to that provider. Compare an '
        'explicit bitemporal file/query baseline, existing feature infrastructure and a port; '
        'do not infer competitor parity. Construct a small exact authored banking reference '
        'with late revisions and a decision whose historical value changes if future '
        'information leaks. Check selection invariance and explicit ambiguous outcomes.\n\n'
        'Review a conditional proposal choice with owners, unmeasured costs, conversion '
        'and failure contracts and precise revisit triggers. No downloaded code, native '
        'Feast runtime or sibling repository executes. Lack of a native benchmark does not '
        'block the proposal decision, but grants no integration capability. Bind all claims '
        'to originals and preserve failures. Integrate substantive conclusions into preserving '
        'reader and sponsor successors, then renew applicable source/math reviews. '
        'Rendered visual acceptance stays open because the inherited image allowance is '
        'exhausted. Continue independent eligible work across publication boundaries.\n')
    requests = [dict(id='exec19_feast_cutoff_commit', extension='json',
        url='https://api.github.com/repos/feast-dev/feast/commits?sha=master&until=2026-10-07T15%3A59%3A59Z&per_page=1')]
    write(BASE / 'identity-acquisition-manifest.json', dict(requests=requests,
        cutoff='2026-10-07 Asia/Shanghai', stopping_rule='One cutoff identity read; select technical paths after tree inspection.'))
    write(BASE / 'plan-review.json', dict(status='pass',
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        evidence=[ref(BASE / 'plan.md', 'Reviewed scientific, rights and admission scope'),
            ref(ROOT / 'docs/literature/software/feast.json', 'Inherited unpinned candidate and precise API caveat'),
            ref(ROOT / 'docs/literature/raw/head_feast.receipt.json', 'Preserved inherited403 identity failure'),
            ref(BASE / 'identity-acquisition-manifest.json', 'Bounded public acquisition plan')],
        checks=['Feature availability is a property of the declared observation law, not just timestamp syntax.',
            'API, provider behavior, test specifications and native execution are separate evidence levels.',
            'No existing citation or frozen binding will be overwritten.',
            'A completed proposal decision can defer native admission without claiming runtime qualification.'],
        integration_allowed=False))
    manifest.write_text(json.dumps(dict(requests=requests), indent=2) + '\n')
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)), requests=len(requests))))


if __name__ == '__main__':
    main()
