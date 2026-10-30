#!/usr/bin/python3
"""Fixed public HTTPS reads of registered institutional/publisher originals.

No uploads, credentials, downloaded execution, or general shell access.
The shared collector caps each response at64MiB and writes source receipts.
"""
from pathlib import Path
import sys
import public_sources as collector

if sys.argv[1:] != ['fetch']:
    raise SystemExit('Exact command: closure_institutional_sources_20261030.py fetch')
collector.MANIFEST=Path(__file__).resolve().parents[1]/'docs/twelve-hour-closure/2026-10-29/institutional-fetch-manifest.json'
collector.HOSTS=collector.HOSTS|{
    'oa.upm.es','ebuah.uah.es','escholarship.org','intellectum.unisabana.edu.co',
    'pubs.rsc.org','link.springer.com','link.springer.com','www.ebm-journal.org',
}
collector.main()
