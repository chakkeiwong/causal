#!/usr/bin/env python3
"""Fixed bounded public manuals; preserve failures and never execute downloads."""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
import acquire_transport_commercial_v2_20261021 as transport

BASE = transport.ROOT/'docs/program/execution/2026-10-22/observations-commercial-v1'
REQUESTS = (
    ('aws_er_guide', 'https://docs.aws.amazon.com/pdfs/entityresolution/latest/userguide/entityresolution-ug.pdf', 'pdf'),
    ('databricks_pit', 'https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series', 'html'),
    ('databricks_feature', 'https://docs.databricks.com/aws/en/machine-learning/feature-store/feature-tables', 'html'),
    ('snowflake_time', 'https://docs.snowflake.com/en/user-guide/data-time-travel', 'html'),
    ('snowflake_at', 'https://docs.snowflake.com/en/sql-reference/constructs/at-before', 'html'),
    ('ibm_qualitystage', 'https://www.ibm.com/docs/en/iis/11.7.0?topic=qualitystage-investigating-matching-data', 'html'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    assert (BASE/'plan-review.json').exists()
    transport.BASE = BASE
    attempt = 'network' if args.retry_network else 'sandbox'
    if args.retry_network:
        for name, _, _ in REQUESTS:
            old = json.loads((BASE/'acquisition/sandbox'/(name+'.receipt.json')).read_text())
            assert old['returncode'] in (5, 6, 7), 'Retry only preserved connection failures'
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda row: transport.acquire(row, attempt), REQUESTS):
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
