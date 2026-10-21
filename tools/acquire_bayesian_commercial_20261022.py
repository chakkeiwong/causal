#!/usr/bin/env python3
"""Fixed bounded official HTTPS reads; retain failures and never execute sources."""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
import acquire_transport_commercial_v2_20261021 as transport

BASE = transport.ROOT/'docs/program/execution/2026-10-22/bayesian-commercial-v1'
REQUESTS = (
    ('stata_sspace', 'https://www.stata.com/manuals/tssspace.pdf', 'pdf'),
    ('stata_sspace_post', 'https://www.stata.com/manuals/tssspacepostestimation.pdf', 'pdf'),
    ('stata_bayesmh', 'https://www.stata.com/manuals/bayesbayesmh.pdf', 'pdf'),
    ('sas_mcmc', 'https://support.sas.com/documentation/onlinedoc/stat/151/mcmc.pdf', 'pdf'),
    ('eviews_state', 'https://www.eviews.com/help/content/sspace-Estimating_a_State_Space_Model.html', 'html'),
    ('hugin_dbn', 'https://download.hugin.com/webdocs/manuals/9.4/htmlhelp/pages/Manual/NodesAndNetworks/DBN.html', 'html'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    assert (BASE/'plan.md').exists()
    transport.BASE = BASE
    attempt = 'network' if args.retry_network else 'sandbox'
    if args.retry_network:
        for name, _, _ in REQUESTS:
            old = json.loads((BASE/'acquisition/sandbox'/(name+'.receipt.json')).read_text())
            assert old['returncode'] in (5, 6, 7), 'Retry only preserved connection/DNS failures'
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda row: transport.acquire(row, attempt), REQUESTS):
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
