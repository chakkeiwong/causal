#!/usr/bin/env python3
"""Declare a bounded original-reference chain; metadata admits no technical claim."""
import json
from pathlib import Path
from urllib.parse import urlencode
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/longitudinal-backward-chain-v1'
MANIFEST = ROOT / 'docs/literature/fetch-manifest.json'
CUTOFF = '2026-10-07T15:59:59Z'


def main():
    assert not BASE.exists()
    BASE.mkdir(parents=True)
    prior = MANIFEST.read_bytes()
    (BASE / 'prior-fetch-manifest.json').write_bytes(prior)
    targets = [
        ('taubman', 'Intervening on risk factors for coronary heart disease: an application of the parametric g-formula', 2009,
         'Original sequential g-computation application and intervention specification.'),
        ('petersen', 'Diagnosing and responding to violations in the positivity assumption', 2012,
         'Original support diagnostics and target/model modifications; no automatic support restoration.'),
        ('pryzant', 'Causal Effects of Linguistic Properties', 2021,
         'Original treatment-version and linguistic-property identification assumptions.'),
    ]
    requests = [
        dict(id='exec28_lbc_' + key + '_metadata', extension='json',
             url='https://api.openalex.org/works?' + urlencode({
                 'filter': 'to_publication_date:2026-10-07',
                 'search': title, 'per_page': 3, 'page': 1}))
        for key, title, _, _ in targets
    ]
    requests.append(dict(
        id='exec28_lbc_ldpe_crossref', extension='json',
        url='https://api.crossref.org/works/10.1109/tkde.2025.3606149'))
    plan = dict(
        status='reviewed_before_requests', client_date='2026-10-28', source_cutoff=CUTOFF,
        operation='LL.CENSUS', scientific_question=(
            'Which original support and treatment-definition restrictions survive when '
            'human-LLM longitudinal results are translated into a bank policy proposal?'),
        seed=ref(ROOT / 'docs/papers/Causal Inference for Human-Language Model Collaboration Zhang(2024).pdf',
                 'Genuine inspected seed; sections 3.2-3.3, theorem 1 and reference list'),
        extracted_seed=ref(ROOT / 'docs/program/execution/2026-10-13/llm-census/collaboration.txt',
                           'References identify these three original titles, authors and dates'),
        targets=[dict(key=key, title=title, year=year, reason=reason)
                 for key, title, year, reason in targets],
        distinct_identity_followup=dict(
            title='Large Language Models Meet Causal Inference: Semantic-Rich Dual Propensity Score for Sequential Recommendation',
            doi='10.1109/TKDE.2025.3606149',
            reason='Distinct DOI registry route after the preserved exact-title arXiv 429; no unchanged retry.'),
        requests=requests,
        budget=dict(metadata_requests=4, metadata_rows_maximum=10,
                    original_requests_maximum=4, unchanged_failed_route_retries=0),
        gates=[
            'Match original title, authors, date and DOI before proposing an original URL.',
            'Use only the existing fixed collector and permitted HTTPS hosts.',
            'An unavailable or disallowed original remains an omission.',
            'Inspect genuine PDF technical text before admitting claims or citations.',
            'The 2010 Hernan/Robins citation is not relabelled as the retained 2020 book.',
            'No search saturation, runtime qualification or coverage closure from this bounded chain.',
            'No changes to canonical publication state while the benchmark delivery is active.',
        ],
        limitations=['Three deliberately selected backward references do not exhaust the seed bibliography.',
                     'Three returned matches per title leave metadata search tails.',
                     'Original support premises cannot establish assignment truth in a bank.'],
        evidence=[ref(Path(__file__), 'Reviewed bounded request preparation'),
                  ref(BASE / 'prior-fetch-manifest.json', 'Previously consumed conference-chain request')],
    )
    verify_bindings(plan)
    write(BASE / 'plan-review.json', plan)
    write(MANIFEST, dict(requests=requests))
    write(BASE / 'metadata-fetch-manifest.json', dict(requests=requests))
    print(json.dumps(dict(prepared=True, metadata_requests=4, original_budget=4,
                          technical_claims_admitted=0)))


if __name__ == '__main__':
    main()
