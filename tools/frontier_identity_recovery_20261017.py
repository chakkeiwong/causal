#!/usr/bin/env python3
"""Record identity mismatches and stage complementary, bounded public searches."""
import json
from pathlib import Path
from urllib.parse import urlencode

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'docs/literature/raw'
BASE = ROOT / 'docs/program/execution/2026-10-17/census-recovery'
OLD = BASE / 'search-v2'
OUT = BASE / 'search-v3'
IDENTITIES = {
    'medical_policy': ('When and Why LLMs Causally Reason in Medical Decision Making',
        'Signatures of Very Massive Stars in the Epoch of Reionization', False),
    'causalreasonbench': ('CausalReasonBench',
        'Evaluating Differential Privacy Against Membership Inference in Federated Learning: Insights from the NIST Genomics Red Team Challenge', False),
    're_causal': ('RE-Causal: Reasoning-Based Causal Discovery with Reinforcement Learning',
        'Structure-resolved free energy estimation of the 38-atom Lennard–Jones cluster via population annealing', False),
    'dynamic_graph': ('LLM-Powered Multi-Agent Dynamic Graph Optimization for Causal Discovery',
        'Domain decomposition dynamical low-rank for multi-dimensional radiative transfer equations', False),
    'cello': ('CELLO: Causal Evaluation of Large Vision-Language Models',
        'CELLO: Causal Evaluation of Large Vision-Language Models', True),
}


def main():
    assert not OUT.exists()
    rows = []
    for suffix, (expected, observed, matches) in IDENTITIES.items():
        key = 'exec17_census_search2_paper_' + suffix
        text = OLD / (key + '.txt')
        pages = text.read_text().split(chr(12))
        anchor = OLD / (key + '-identity-page.txt')
        anchor.write_text(pages[0])
        receipt = RAW / (key + '.receipt.json')
        assert json.loads(receipt.read_text())['status'] == 'saved'
        rows.append(dict(id=key, expected_title=expected, observed_title=observed,
            identity_matches=matches, original_bytes=ref(RAW / (key + '.pdf'), 'Saved genuine PDF response'),
            retrieval=ref(receipt, 'Bounded public acquisition receipt'),
            inspected_identity=ref(anchor, 'Original physical page1'),
            disposition='eligible_for_primary_review' if matches else 'rejected_identity_mismatch',
            technical_claim_support=False,
            effect='No unrelated PDF is copied into docs/papers or cited as the intended work.'))
    receipts = [json.loads(p.read_text()) for p in sorted(RAW.glob('exec17_census_search2_*.receipt.json'))]
    assert len(receipts) == 12
    searches = []
    for suffix in ['openalex_longitudinal', 'openalex_negative']:
        path = RAW / ('exec17_census_search2_' + suffix + '.json')
        data = json.loads(path.read_text())
        searches.append(dict(id=suffix, response=ref(path, 'Saved metadata response; not technical evidence'),
            retrieved=len(data['results']), reported_total=data['meta']['count'],
            candidates=[dict(id=r['id'], title=r.get('title'), doi=r.get('doi'),
                             publication_date=r.get('publication_date')) for r in data['results']],
            limitation='Only the first20 relevance-ranked results. Broad full-text matching returns substantial unrelated material; no saturation or absence inference.'))
    cross = json.loads((RAW / 'exec17_census_search2_candidate27_crossref.json').read_text())['message']
    assert cross['title'][0] == 'Agent-guided Causal Discovery with a Small Language Model'
    authors = [a['given'] + ' ' + a['family'] for a in cross['author']]
    assert authors == ['Brandon Mossop', 'Salimur Choudhury']
    write(OLD / 'acquisition-observations.json', dict(
        cutoff='2026-10-07', rows=rows, saved_requests=9, failed_requests=3,
        failures=[r for r in receipts if r['status'] == 'failed'],
        searches=searches, candidate27=dict(
            title=cross['title'][0], authors=authors,
            identity_correction='The inherited continuation-summary author lead was wrong. Crossref identifies Mossop and Choudhury; do not attribute this work to Cheong/Ranasinghe/Bandara.',
            evidence=[ref(RAW / 'exec17_census_search2_candidate27_crossref.json', 'DOI identity and author metadata'),
                      ref(RAW / 'exec17_census_search2_candidate27_openalex.json', 'No OA URL in this lookup')],
            original_inspected=False,
            limitation='Metadata identities do not prove technical claims or worldwide unavailability.'),
        evidence=[ref(OLD / 'acquisition-manifest.json', 'Preserved unverified discovery leads'),
                  ref(Path(__file__), 'Identity-screening and search preparation procedure')],
        census_closed=False, visual_acceptance=False))
    OUT.mkdir()
    requests = [dict(id='exec17_census_search3_candidate113',
        url='https://api.openalex.org/works/W7154072656', extension='json')]
    for suffix, query in [
        ('copilot', '"Causal-Copilot: An Autonomous Causal Analysis Agent"'),
        ('medical', '"When and Why LLMs Causally Reason in Medical Decision Making"'),
        ('re_causal', '"RE-Causal"'),
        ('dynamic_graph', '"LLM-Powered Multi-Agent Dynamic Graph Optimization for Causal Discovery"'),
        ('off_policy', '"large language model" AND "off-policy"')]:
        requests.append(dict(id='exec17_census_search3_' + suffix,
            url='https://api.openalex.org/works?' + urlencode(dict(search=query,
                filter='to_publication_date:2026-10-07', per_page=20, page=1)), extension='json'))
    requests.append(dict(id='exec17_census_search3_candidate27_arxiv_web',
        url='https://arxiv.org/search/?' + urlencode(dict(query='Agent-guided Causal Discovery with a Small Language Model',
            searchtype='title', abstracts='show', order='-announced_date_first', size=50)), extension='html'))
    manifest = ROOT / 'docs/literature/fetch-manifest.json'
    write(OUT / 'previous-fetch-manifest.json', json.loads(manifest.read_text()))
    write(OUT / 'acquisition-manifest.json', dict(requests=requests, cutoff='2026-10-07',
        stopping_rule='Six metadata requests, at most20 results per search, plus one exact-title arXiv web query. Inspect saved original titles and dates before acquisition/use.',
        motivation='Repair four unverified identifier mismatches using actual metadata responses and an original reference-list citation chain.',
        provenance=[ref(OLD / 'acquisition-observations.json', 'Observed identity and search failures'),
                    ref(BASE / 'tranche-v1/candidate242-page-3.txt', 'Original Causal-Copilot reference')],
        limitations=['Uninspected metadata and abstracts cannot establish technical capability.',
                    'The arXiv web query has no backend cutoff; screen every result against2026-10-07.',
                    'Bounded result pages cannot establish complete coverage.']))
    manifest.write_text(json.dumps(dict(requests=requests), indent=2) + '\n')
    print(json.dumps(dict(matching_pdf_leads=1, rejected_identity_mismatches=4,
                          new_requests=len(requests), original_census_closed=False)))


if __name__ == '__main__':
    main()
