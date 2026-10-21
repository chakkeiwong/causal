#!/usr/bin/env python3
"""Four pinned public source archives, bounded reads; never execute their code."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import acquire_transport_details_20261021 as fetch

fetch.BASE=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-21/effects-other-v1'
REVISIONS=(
    ('CausalELM','dscolby/CausalELM.jl','328138c545d57f1f3542fdf7c68f96731e2fa4cd'),
    ('CausalForest','BereniceAlexiaJocteur/CausalForest.jl','36f05cb5250ed69d45f62ddd04819e9ea706a216'),
    ('CausalTables','salbalkus/CausalTables.jl','f0ec5ad689ef521db2a975ab779428f44f3d64fe'),
    ('TMLE','TARGENE/TMLE.jl','016bdd3a973c3368f2bc3d22637ea90c119ed0e4'),
)
REQUESTS=tuple((name,'https://codeload.github.com/'+repo+'/tar.gz/'+commit,'tgz') for name,repo,commit in REVISIONS)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--retry-network',action='store_true')
    args=parser.parse_args();attempt='sources-network' if args.retry_network else 'sources-sandbox'
    records=json.loads((fetch.BASE/'version-selection.json').read_text())['entries']
    selected={r['name']:r['commit'] for r in records}
    assert all(selected[name]==commit for name,repo,commit in REVISIONS)
    if args.retry_network:
        for name,repo,commit in REVISIONS:
            r=json.loads((fetch.BASE/'acquisition/sources-sandbox'/(name+'.receipt.json')).read_text())
            assert r['returncode'] in [5,6,7]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda row:fetch.acquire(row,attempt),REQUESTS):print(json.dumps(result),flush=True)


if __name__=='__main__':main()
