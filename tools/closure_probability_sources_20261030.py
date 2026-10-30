#!/usr/bin/python3
"""One fixed public original, bounded download, no uploads or code execution."""
from pathlib import Path
import sys
import public_sources as collector
if sys.argv[1:] != ['fetch']:
    raise SystemExit('Exact command: closure_probability_sources_20261030.py fetch')
collector.HOSTS={'www.cs.rpi.edu'}
collector.MAX_BYTES=16*1024*1024
collector.OUT.mkdir(parents=True,exist_ok=True)
if collector.OUT.resolve()!=collector.OUT:raise SystemExit('Symlink output rejected')
print(collector.fetch_one(dict(id='closure30_hoeffding_original',
    url='https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf',extension='pdf')))
