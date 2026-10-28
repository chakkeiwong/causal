#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/longitudinal-specificity-v1'
manifest=ROOT/'docs/literature/fetch-manifest.json'
assert not (BASE/'followup-plan.json').exists()
(BASE/'first-query-manifest.json').write_bytes(manifest.read_bytes())
query='ti:'+chr(34)+'Semantic-Rich Dual Propensity'+chr(34)
requests=[dict(id='exec25_lsp_ldpe_title',url='https://export.arxiv.org/api/query?'+urlencode(dict(search_query=query,start=0,max_results=5)),extension='xml'),dict(id='exec25_lsp_collab_forward',url='https://api.openalex.org/works?'+urlencode(dict(filter='cites:W4393758865,to_publication_date:2026-10-07',per_page=20,page=1,sort='publication_date:asc')),extension='json')]
plan=dict(status='declared_distinct_followup_budget',max_responses=2,max_records=25,source_cutoff='2026-10-07T15:59:59Z',requests=requests,stop='One exact-title and one forward-chain page; do not repeat errors. Metadata is discovery only; verify originals and versions before claims.')
(BASE/'followup-plan.json').write_text(json.dumps(plan,indent=2)+chr(10))
manifest.write_text(json.dumps(dict(requests=requests),indent=2)+chr(10))
print('Two bounded distinct follow-up queries prepared.')
