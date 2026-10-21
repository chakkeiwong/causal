#!/usr/bin/env python3
"""Resolve five explicit Julia registry leads by bounded public HTTPS reads."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import acquire_transport_details_20261021 as fetch

fetch.BASE=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-21/effects-other-v1'
NAMES=('CausalELM','CausalForest','CausalInference','TMLE','CausalTables')
REQUESTS=tuple((name,'https://raw.githubusercontent.com/JuliaRegistries/General/master/'+name[0]+'/'+name+'/Package.toml','toml') for name in NAMES)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--retry-network',action='store_true')
    args=parser.parse_args();attempt='registry-network' if args.retry_network else 'registry-sandbox'
    if args.retry_network:
        for name in NAMES:
            r=json.loads((fetch.BASE/'acquisition/registry-sandbox'/(name+'.receipt.json')).read_text())
            assert r['returncode'] in [5,6,7]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda row:fetch.acquire(row,attempt),REQUESTS):print(json.dumps(result),flush=True)


if __name__=='__main__':main()
