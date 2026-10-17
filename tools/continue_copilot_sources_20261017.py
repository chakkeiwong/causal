#!/usr/bin/env python3
"""Preserve crash recovery and stage bounded public version/identity lookups."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlencode

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-17/census-recovery'
RAW = ROOT/'docs/literature/raw'
MANIFEST = ROOT/'docs/literature/fetch-manifest.json'


def stage():
    observations = BASE/'search-v5/recovered-observations'
    observations.mkdir(exist_ok=False)
    evidence = []
    for label, source in [
        ('sandbox-dns-failure', Path('/tmp/causal-search5-fetch-20261017.log')),
        ('elevated-fetch', Path('/tmp/causal-search5-fetch-20261017-elevated.log'))]:
        destination = observations/(label+'.log')
        destination.write_bytes(source.read_bytes())
        evidence.append(ref(destination, label))
    for stem in ['exec17_census_search5_copilot_abs', 'exec17_census_search5_copilot_v1']:
        source = RAW/(stem+'.receipt.json')
        destination = observations/source.name
        destination.write_bytes(source.read_bytes())
        evidence.append(ref(destination, 'Preserved successful source receipt'))
    write(observations/'observation.json', dict(
        outcome='Original v1 acquired after sandbox DNS failure and elevated retry.',
        evidence=evidence,
        limits=['Earlier failed collector receipts were replaced by the successful attempt; the original failure log is preserved.',
                'arXiv metadata establishes v2 dated2025-04-21; v1 alone is not a latest-version review.']))
    out = BASE/'search-v6'
    out.mkdir(exist_ok=False)
    (out/'previous-fetch-manifest.json').write_bytes(MANIFEST.read_bytes())
    requests = [
        dict(id='exec17_census_search6_copilot_v2', url='https://arxiv.org/pdf/2504.13263v2', extension='pdf'),
        dict(id='exec17_census_search6_candidate27_author',
             url='https://arxiv.org/search/?'+urlencode(dict(query='Mossop', searchtype='author', abstracts='show', order='-announced_date_first', size=50)), extension='html'),
        dict(id='exec17_census_search6_copilot_repositories',
             url='https://api.github.com/search/repositories?'+urlencode(dict(q='Causal-Copilot in:name', per_page=10)), extension='json')]
    write(out/'acquisition-manifest.json', dict(requests=requests))
    write(out/'plan-review.json', dict(
        status='pass', scope='Bounded primary-source continuation, not program acceptance',
        cutoff='2026-10-07',
        actions=['Acquire and inspect exact arXiv v2 and retain v1 as a separate predecessor.',
                 'Inspect algorithm assumptions, bootstrap/post-processing claims, evaluation units, adverse results and case-study limits.',
                 'Resolve the repository identity before selecting a dated source pin; do not execute downloaded code.',
                 'Try an author-based arXiv route for candidate27; retain every failure without declaring global unavailability.',
                 'Integrate reviewed substantive findings in a preserving reader; keep original census and new citation-chain denominators separate.'],
        review=['Public GET only; no uploads, model calls, external messages or sibling edits.',
                'No metadata-derived technical claims, rights closure or independent validation.',
                'Known benchmark publication and other ready work must continue despite this branch’s local failures.'],
        evidence=[ref(out/'previous-fetch-manifest.json', 'Preserved mutable-manifest predecessor'),
                  ref(out/'acquisition-manifest.json', 'Three bounded public reads'),
                  ref(observations/'observation.json', 'Recovered failure/success history'),
                  ref(RAW/'exec17_census_search5_copilot_abs.html', 'Submission history: v1 and v2 before cutoff')]))
    MANIFEST.write_text(json.dumps(dict(requests=requests), indent=2)+'\n')
    print(json.dumps(dict(staged=str(out.relative_to(ROOT)), requests=len(requests))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['stage'])
    stage()
