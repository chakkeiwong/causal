#!/usr/bin/env python3
"""Review exact metadata identities and retain unavailable original routes."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
import public_sources
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/longitudinal-backward-chain-v1'
RAW = ROOT / 'docs/literature/raw'
MANIFEST = ROOT / 'docs/literature/fetch-manifest.json'
read = lambda path: json.loads(path.read_text())


def main():
    plan = read(BASE / 'plan-review.json')
    verify_bindings(plan)
    records = []
    for request in plan['requests']:
        path = RAW / (request['id'] + '.json')
        receipt = RAW / (request['id'] + '.receipt.json')
        saved = read(receipt)
        assert saved['status'] == 'saved' and saved['url'] == request['url']
        assert saved['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        records.append(dict(identity=request['url'], local_copy=ref(path, 'Metadata only'),
                            retrieval=ref(receipt, 'Fixed-collector successful retrieval')))
    selected = []
    expected = {
        'taubman': ('W2166689328', '10.1093/ije/dyp192'),
        'petersen': ('W2155169076', '10.1177/0962280210386207'),
        'pryzant': ('W3094245163', '10.18653/v1/2021.naacl-main.323'),
    }
    for target in plan['targets']:
        key = target['key']
        rows = read(RAW / ('exec28_lbc_' + key + '_metadata.json'))['results']
        identity, doi = expected[key]
        matches = [r for r in rows if r['id'].endswith('/' + identity)]
        assert len(matches) == 1
        row = matches[0]
        assert row['title'].casefold() == target['title'].casefold()
        assert row['doi'].lower().endswith(doi)
        locations = [
            dict(landing=x.get('landing_page_url'), pdf=x.get('pdf_url'),
                 version=x.get('version'),
                 pdf_host_permitted=urlsplit(x.get('pdf_url') or '').hostname in public_sources.HOSTS)
            for x in row['locations']
        ]
        selected.append(dict(
            key=key, title=row['title'], doi=doi, metadata_identity=row['id'],
            metadata_date=row['publication_date'], seed_bibliography_year=target['year'],
            authors=[a['author']['display_name'] for a in row['authorships']],
            locations=locations, technical_claims_admitted=False))
    ldpe = read(RAW / 'exec28_lbc_ldpe_crossref.json')['message']
    assert ldpe['DOI'].lower() == '10.1109/tkde.2025.3606149'
    assert ldpe['title'][0] == plan['distinct_identity_followup']['title']
    requests = [
        dict(id='exec28_lbc_pryzant_identity', url='https://arxiv.org/abs/2010.12919', extension='html'),
        dict(id='exec28_lbc_pryzant_v1', url='https://arxiv.org/pdf/2010.12919v1', extension='pdf'),
    ]
    omissions = [
        dict(key='taubman', reason='No exact primary PDF URL returned; publisher/PMC landing pages do not establish inspected original text.',
             next_action='Resolve an authoritative exact PDF through the permitted collector or an existing genuine local original.'),
        dict(key='petersen', reason='No primary PDF URL returned; PMC and bepress locations lie outside the fixed collector host list.',
             next_action='Seek a distinct authoritative permitted PDF route; do not broaden the collector host list or treat metadata as text.'),
        dict(key='ldpe', reason='Crossref identifies a non-HTTPS staging link and an IEEE landing page outside the fixed collector. No permitted original route was resolved.',
             next_action='Retain the earlier arXiv 429 and seek a distinct author/archive original; no unchanged retry.'),
        dict(key='hernan2010', reason='The seed cites 2010; the retained 2020 book is a distinct edition.',
             next_action='Use the 2020 book under its own existing identity, and leave the seed edition unverified.'),
        dict(key='pryzant_conference', reason='Conference PDF is on an unlisted host; the planned arXiv v1 is a distinct preprint.',
             next_action='Inspect preprint identity and technical text separately; do not assert equivalence to the conference version.'),
    ]
    review = dict(
        status='pass_for_identity_and_bounded_original_attempt', evidence=records + [
            ref(BASE / 'plan-review.json', 'Four metadata requests and four-original maximum'),
            ref(Path(__file__), 'Identity, route and version review')],
        selected=selected,
        ldpe=dict(doi=ldpe['DOI'], title=ldpe['title'][0],
                  issue_date=ldpe.get('published'), links=ldpe.get('link'),
                  date_limit='Issue November 2025 differs from earlier metadata September 2025; both precede cutoff, original history remains unverified.'),
        omissions=omissions, original_requests=requests,
        request_budget_used=dict(metadata=4, originals_planned=2, original_maximum=4),
        technical_claims_admitted=0, search_saturation=False, source_cutoff=plan['source_cutoff'])
    verify_bindings(review)
    write(BASE / 'metadata-review.json', review)
    write(BASE / 'original-fetch-manifest.json', dict(requests=requests))
    assert read(MANIFEST) == read(BASE / 'metadata-fetch-manifest.json')
    MANIFEST.write_text(json.dumps(dict(requests=requests), indent=2) + chr(10))
    print(json.dumps(dict(metadata_identities=4, planned_original_requests=2,
                          technical_claims_admitted=0, omissions=len(omissions))))


if __name__ == '__main__':
    main()
