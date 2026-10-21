#!/usr/bin/env python3
"""Resolve five registry-backed repository heads at the declared client cutoff."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import acquire_transport_details_20261021 as fetch

fetch.BASE=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-21/effects-other-v1'
REPOS=(('CausalELM','dscolby/CausalELM.jl'),('CausalForest','BereniceAlexiaJocteur/CausalForest.jl'),
    ('CausalInference','mschauer/CausalInference.jl'),('TMLE','TARGENE/TMLE.jl'),('CausalTables','salbalkus/CausalTables.jl'))
REQUESTS=tuple((name,'https://api.github.com/repos/'+repo+'/commits?until=2026-10-07T15%3A59%3A59Z&per_page=1','json') for name,repo in REPOS)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--retry-network',action='store_true')
    args=parser.parse_args();attempt='commits-network' if args.retry_network else 'commits-sandbox'
    records=json.loads((fetch.BASE/'registry-identities.json').read_text())['entries']
    assert {r['repo'].removesuffix('.git') for r in records}=={'https://github.com/'+repo for _,repo in REPOS}
    if args.retry_network:
        for name,_ in REPOS:
            r=json.loads((fetch.BASE/'acquisition/commits-sandbox'/(name+'.receipt.json')).read_text())
            assert r['returncode'] in [5,6,7]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda row:fetch.acquire(row,attempt),REQUESTS):print(json.dumps(result),flush=True)


if __name__=='__main__':main()
