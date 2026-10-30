#!/usr/bin/python3
"""Fixed public-source collection; no local uploads or downloaded execution."""
from pathlib import Path
import sys
import public_sources as collector

if sys.argv[1:] != ['fetch']:
    raise SystemExit('Exact command: closure_frontier_sources_20261030.py fetch')
collector.MANIFEST = Path(__file__).resolve().parents[1] / 'docs/twelve-hour-closure/2026-10-29/frontier-fetch-manifest.json'
collector.HOSTS = collector.HOSTS | {
    'csbulletin.com', 'www.csbulletin.com',
    'meetingorganizer.copernicus.org', 'www.egu.eu',
    'zenodo.org', 'www.ebi.ac.uk', 'www.ebm-journal.org',
    'public-pages-files-2025.frontiersin.org', 'public-pages-files-2026.frontiersin.org',
}
collector.main()
