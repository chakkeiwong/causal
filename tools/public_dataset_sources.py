#!/usr/bin/env python3
"""Fixed public-dataset documentation batch, reusing the frozen public collector.

The original collector and its approval rule remain unchanged. This successor
registers dataset custodians needed for the proposal survey. All original GET,
redirect/public-address validation, byte limits and receipt rules still apply.
No credentials, uploads, remote execution or approval-setting changes.
"""
import sys
from pathlib import Path

import public_sources as collector

BASE = Path(__file__).resolve().parents[1] / 'docs/program/public-data-v15'
DATASET_HOSTS = {
    'archive.ics.uci.edu',
    'www.fdic.gov', 'fdic.gov', 'banks.data.fdic.gov', 'api.fdic.gov',
    'ffiec.cfpb.gov', 'www.consumerfinance.gov',
    'www.freddiemac.com', 'sf.freddiemac.com',
    'capitalmarkets.fanniemae.com', 'www.fanniemae.com',
    'ailab.criteo.com',
}


def main():
    if sys.argv[1:] != ['fetch']:
        raise SystemExit('Exact command: tools/public_dataset_sources.py fetch')
    collector.HOSTS = collector.HOSTS | DATASET_HOSTS
    collector.MANIFEST = BASE / 'dataset-fetch-manifest.json'
    collector.main()


if __name__ == '__main__':
    main()
