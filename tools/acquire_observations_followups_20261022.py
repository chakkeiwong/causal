#!/usr/bin/env python3
"""Bounded public official index recovery; no credential use or code execution."""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
import acquire_transport_commercial_v2_20261021 as transport

BASE = transport.ROOT/'docs/program/execution/2026-10-22/observations-commercial-v1'
REQUESTS = (
    ('aws_er_index', 'https://docs.aws.amazon.com/entityresolution/latest/userguide/what-is-service.html', 'html'),
)

def main():
    p=argparse.ArgumentParser();p.add_argument('--retry-network',action='store_true');a=p.parse_args()
    transport.BASE=BASE
    attempt='network-followup' if a.retry_network else 'sandbox-followup'
    for row in REQUESTS:
        if a.retry_network:
            old=json.loads((BASE/'acquisition/sandbox-followup'/(row[0]+'.receipt.json')).read_text())
            assert old['returncode'] in (5,6,7)
        print(json.dumps(transport.acquire(row,attempt)),flush=True)

if __name__=='__main__':main()
