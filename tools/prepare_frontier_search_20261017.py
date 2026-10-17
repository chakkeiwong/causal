#!/usr/bin/env python3
"""Stage bounded complementary searches and versioned original acquisitions."""
import json
from pathlib import Path
from urllib.parse import urlencode

from publish_latent_r_review_v2_20261013 import ref, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-17/census-recovery/search-v2'


def main():
    assert not BASE.exists()
    BASE.mkdir()
    manifest=ROOT/'docs/literature/fetch-manifest.json'
    write(BASE/'previous-fetch-manifest.json',json.loads(manifest.read_text()))
    requests=[]
    def add(key,url,extension='json'):
        identifier='exec17_census_search2_'+key
        assert not (ROOT/'docs/literature/raw'/f'{identifier}.receipt.json').exists()
        requests.append(dict(id=identifier,url=url,extension=extension))
    add('candidate27_openalex','https://api.openalex.org/works/W7130543099')
    add('candidate27_crossref','https://api.crossref.org/works/10.1109%2FFLLM67465.2025.11391103')
    queries=[('candidate27','ti:"Agent-guided Causal Discovery with a Small Language Model"'),
             ('longitudinal','(all:"causal" AND (all:"longitudinal" OR all:"off-policy")) AND (all:"language model" OR all:"LLM")'),
             ('negative','all:"causal discovery" AND all:"language model" AND (all:"failure" OR all:"benchmark")')]
    for key,query in queries:
        add('arxiv_'+key,'https://export.arxiv.org/api/query?'+urlencode(dict(
            search_query=query+' AND submittedDate:[202001010000 TO 202610072359]',
            start=0,max_results=20,sortBy='submittedDate',sortOrder='descending')),'xml')
    for key,query in [('longitudinal','causal language model longitudinal off-policy'),
                      ('negative','causal discovery language model benchmark failure')]:
        add('openalex_'+key,'https://api.openalex.org/works?'+urlencode({
            'search':query,'filter':'to_publication_date:2026-10-07','per-page':20,'page':1}))
    papers=[('medical_policy','2604.21493'),('causalreasonbench','2604.12737'),
            ('re_causal','2603.04157'),('cello','2406.19131'),('dynamic_graph','2602.14854')]
    for key,identifier in papers:
        add('paper_'+key,'https://arxiv.org/pdf/'+identifier+'v1','pdf')
    planned=dict(requests=requests,cutoff='2026-10-07',
        stopping_rule='One twenty-result page for each of two search themes and an exact-title query; five specifically reported v1 PDF leads. No exhaustiveness or unavailability inference.',
        provenance='The continuation summary supplied titles/identifiers as discovery leads only. New saved API responses establish observed search outcomes; each genuine original requires separate inspection.',
        prior_search=ref(BASE.parent/'tranche-v1/search-observations.json','Preserved earlier unsuccessful visible search'),
        source_use='Metadata establishes discovery and identity only. No uninspected original supports a technical manuscript claim.',
        live_models_called=False,uploaded_local_data=False)
    write(BASE/'acquisition-manifest.json',planned)
    manifest.write_text(json.dumps({'requests':requests},indent=2)+'\n')
    print(json.dumps(dict(requests=len(requests),bounded_query_routes=['arXiv','OpenAlex'],original_pdf_leads=5)))


if __name__=='__main__':main()
