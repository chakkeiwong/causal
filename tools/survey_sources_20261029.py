#!/usr/bin/python3
"""Bounded official-source reads for the consequential survey continuation."""
import sys
from pathlib import Path
import public_sources as collector

if sys.argv[1:] != ['fetch']:
    raise SystemExit('Exact command: survey_sources_20261029.py fetch')
collector.MANIFEST = Path(__file__).resolve().parents[1] / 'docs/scientific-gap-closure/2026-10-29/survey-fetch-manifest.json'
collector.HOSTS = collector.HOSTS | {
    'escholarship.org', 'assets.escholarship.org', 'ebuah.uah.es',
    'intellectum.unisabana.edu.co', 'www.causalens.com', 'causalens.com',
    'docs.causalens.com', 'decisionos.com', 'www.decisionos.com'
}
collector.main()
