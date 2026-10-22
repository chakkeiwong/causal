#!/usr/bin/env python3
"""Six fixed public manual reads; bounded transport, immutable attempts, no execution."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json

import acquire_transport_commercial_v2_20261021 as transport

BASE = transport.ROOT / 'docs/program/execution/2026-10-22/computation-commercial-preflight-v1'
REQUESTS = (
    ('databricks_repair', 'https://docs.databricks.com/aws/en/jobs/repair-job-failures', 'html'),
    ('databricks_monitor', 'https://docs.databricks.com/aws/en/jobs/monitor', 'html'),
    ('snowflake_graphs', 'https://docs.snowflake.com/en/user-guide/tasks-graphs', 'html'),
    ('azure_reuse', 'https://learn.microsoft.com/en-us/azure/machine-learning/how-to-debug-pipeline-reuse-issues?view=azureml-api-2', 'html'),
    ('dataiku_scenarios', 'https://doc.dataiku.com/dss/latest/scenarios/index.html', 'html'),
    ('aws_errors', 'https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html', 'html'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    assert (BASE / 'plan-review.json').exists()
    transport.BASE = BASE
    attempt = 'network' if args.retry_network else 'sandbox'
    if args.retry_network:
        for name, _, _ in REQUESTS:
            old = json.loads((BASE / 'acquisition/sandbox' / (name + '.receipt.json')).read_text())
            assert old['returncode'] in (5, 6, 7), 'Retry only preserved connection failures.'
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda row: transport.acquire(row, attempt), REQUESTS):
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
