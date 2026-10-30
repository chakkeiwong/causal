#!/usr/bin/python3
"""Bounded public original/documentation acquisition for the named residual gaps."""
import sys
from pathlib import Path
import public_sources as collector

if sys.argv[1:] != ['fetch']:
    raise SystemExit('Exact command: gap_sources_frontier_20261029.py fetch')
collector.MANIFEST=Path(__file__).resolve().parents[1]/'docs/scientific-gap-closure/2026-10-29/frontier-fetch-manifest.json'
collector.HOSTS=collector.HOSTS|{'oa.upm.es','aclanthology.org','www.mdpi.com','download.hugin.com','www.hugin.com','www.mathworks.com'}
collector.main()
