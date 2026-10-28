#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/longitudinal-specificity-v1'
manifest=ROOT/'docs/literature/fetch-manifest.json'
assert not (BASE/'conference-chain-plan.json').exists()
(BASE/'followup-query-manifest.json').write_bytes(manifest.read_bytes())
requests=[dict(id='exec25_lsp_collab_conference_forward',url='https://api.openalex.org/works?'+urlencode(dict(filter='cites:W4401043557,to_publication_date:2026-10-07',per_page=20,page=1,sort='publication_date:asc')),extension='json')]
plan=dict(status='distinct_conference_identity_chain',requests=requests,max_records=20,source_cutoff='2026-10-07T15:59:59Z',stop='One page from distinct conference identity; no retry on unchanged failure; do not equate zero indexed citations with zero literature.')
(BASE/'conference-chain-plan.json').write_text(json.dumps(plan,indent=2)+chr(10));manifest.write_text(json.dumps(dict(requests=requests),indent=2)+chr(10))
print('Bounded conference-identity forward chain prepared.')
