#!/usr/bin/python3
"""Fetch this research batch's public sources with the retained bounded collector."""
import sys
from pathlib import Path
import public_sources as collector

if sys.argv[1:] != ['fetch']:
    raise SystemExit('Exact command: scientific_sources_20261029.py fetch')
collector.MANIFEST = Path(__file__).resolve().parents[1] / 'docs/scientific-gap-closure/2026-10-29/fetch-manifest.json'
# The author's NBER archive supplies the experiment design and original data.
collector.HOSTS = collector.HOSTS | {'users.nber.org'}
collector.main()
