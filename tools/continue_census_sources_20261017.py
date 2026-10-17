#!/usr/bin/env python3
"""Preserve observed search results and prepare bounded identity follow-ups."""
import json
from pathlib import Path
from urllib.parse import urlencode

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-17/census-recovery'
RAW = ROOT / 'docs/literature/raw'


def main():
    out = BASE / 'search-v4'
    out.mkdir(exist_ok=False)
    searches = []
    for path in sorted(RAW.glob('exec17_census_search3_*.json')):
        if path.name.endswith('.receipt.json'):
            continue
        data = json.loads(path.read_text())
        rows = data.get('results', [data])
        records = []
        for row in rows:
            loc = row.get('best_oa_location') or row.get('primary_location') or {}
            records.append(dict(id=row['id'], title=row.get('title'), doi=row.get('doi'),
                publication_date=row.get('publication_date'), pdf_url=loc.get('pdf_url'),
                landing_page=loc.get('landing_page_url'), technical_support=False))
        searches.append(dict(response=ref(path, 'Saved metadata discovery and identity only'),
            reported_total=data.get('meta', {}).get('count'), retrieved=len(rows), records=records))
    html = RAW / 'exec17_census_search3_candidate27_arxiv_web.html'
    assert 'Sorry, your query' in html.read_text()
    write(BASE / 'search-v3/search-observations.json', dict(cutoff='2026-10-07',
        searches=searches, candidate27=dict(evidence=ref(html, 'Saved exact-title arXiv query'),
            observation='No results returned by this exact-title query.',
            effect='Original still unread; this single route does not establish unavailability.'),
        identity_repair='CausalReasonBench resolves to Research Square DOI10.21203/rs.3.rs-9181514/v1, not the unrelated inherited arXiv identifier.',
        limitations=['Metadata establishes identity/discovery only.',
            'At most20 relevance-ranked results per query; no saturation or exhaustive census.',
            'Zero-result medical/dynamic-graph queries do not establish that intended works exist or do not exist.',
            'RE-Causal and off-policy queries are noisy; screen exact original identity and method scope.'],
        census_closed=False))
    requests = [dict(id='exec17_census_search4_copilot_arxiv',
        url='https://arxiv.org/search/?' + urlencode(dict(query='Causal-Copilot',
            searchtype='title', abstracts='show', order='-announced_date_first', size=50)), extension='html'),
        dict(id='exec17_census_search4_copilot_openalex',
        url='https://api.openalex.org/works?' + urlencode(dict(filter='title.search:Causal-Copilot,to_publication_date:2026-10-07',
            per_page=20, page=1)), extension='json')]
    manifest = ROOT / 'docs/literature/fetch-manifest.json'
    write(out / 'previous-fetch-manifest.json', json.loads(manifest.read_text()))
    write(out / 'acquisition-manifest.json', dict(requests=requests, cutoff='2026-10-07',
        stopping_rule='Two bounded metadata/title queries,20 OpenAlex results maximum and50 arXiv results maximum; manually screen original dates.',
        motivation='Resolve the genuine Causal-Copilot citation chain without guessing a paper identifier.',
        evidence=[ref(BASE / 'search-v3/search-observations.json', 'Observed noisy/zero-result searches'),
                  ref(BASE / 'tranche-v1/candidate242-page-3.txt', 'Inspected original reference-list lead')],
        technical_claim_support=False))
    manifest.write_text(json.dumps(dict(requests=requests), indent=2) + '\n')
    print(json.dumps(dict(observed_searches=len(searches), new_requests=len(requests), census_closed=False)))


if __name__ == '__main__':
    main()
