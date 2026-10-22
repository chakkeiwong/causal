#!/usr/bin/env python3
"""Six fixed public documentation GETs, immutable attempts and bounded transport."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json

import acquire_transport_commercial_v2_20261021 as transport

BASE = transport.ROOT / 'docs/program/execution/2026-10-23/dataiku-workflow-v1'
REQUESTS = (
    ('latest_flow', 'https://doc.dataiku.com/dss/latest/scenarios/step_flow_control.html', 'html'),
    ('latest_triggers', 'https://doc.dataiku.com/dss/latest/scenarios/triggers.html', 'html'),
    ('latest_steps', 'https://doc.dataiku.com/dss/latest/scenarios/steps.html', 'html'),
    ('latest_releases', 'https://doc.dataiku.com/dss/latest/release_notes/index.html', 'html'),
    ('dss14_flow', 'https://doc.dataiku.com/dss/14/scenarios/step_flow_control.html', 'html'),
    ('dss14_releases', 'https://doc.dataiku.com/dss/14/release_notes/index.html', 'html'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    assert (BASE / 'plan-review.json').is_file()
    attempt = 'network' if args.retry_network else 'sandbox'
    if args.retry_network:
        for name, _, _ in REQUESTS:
            prior = json.loads((BASE / 'acquisition/sandbox' / (name + '.receipt.json')).read_text())
            assert prior['returncode'] in (5, 6, 7), 'Retry only preserved connection failures.'
    transport.BASE = BASE
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda item: transport.acquire(item, attempt), REQUESTS):
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
