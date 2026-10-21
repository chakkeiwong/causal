#!/usr/bin/env python3
"""Four linked SAS official HTML sections; preserve bounded public-read attempts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json

from acquire_transport_details_20261021 import BASE, acquire

REQUESTS = (
    ('sas_assumptions', 'https://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/statug_mi_details03.htm', 'html'),
    ('sas_combining', 'https://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/statug_mi_details53.htm', 'html'),
    ('sas_sensitivity', 'https://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/statug_mi_details58.htm', 'html'),
    ('sas_mnar', 'https://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/statug_mi_syntax08.htm', 'html'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    attempt = 'assumptions-network' if args.retry_network else 'assumptions-sandbox'
    if args.retry_network:
        for name, _, _ in REQUESTS:
            record = json.loads((BASE/'acquisition/assumptions-sandbox'/(name+'.receipt.json')).read_text())
            assert record['returncode'] in [5, 6, 7]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda row: acquire(row, attempt), REQUESTS):
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
