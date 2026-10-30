#!/usr/bin/python3
"""Bounded public HTTPS collection for the twelve-hour proposal campaign."""
from pathlib import Path
import sys
import public_sources as collector

if sys.argv[1:] != ['fetch']:
    raise SystemExit('Exact command: closure_sources_20261029.py fetch')
collector.MANIFEST = Path(__file__).resolve().parents[1] / 'docs/twelve-hour-closure/2026-10-29/fetch-manifest.json'
collector.HOSTS = collector.HOSTS | {
    'pmc.ncbi.nlm.nih.gov', 'www.ncbi.nlm.nih.gov', 'cdn.ncbi.nlm.nih.gov',
    'europepmc.org', 'www.europepmc.org', 'engrxiv.org', 'www.mdpi.com',
    'mdpi-res.com', 'mdpi-res.com', 'pdfs.semanticscholar.org',
    'www.frontiersin.org', 'public-pages-files-2025.frontiersin.org',
}
collector.main()
