#!/usr/bin/env python3
"""Stage a bounded, original-source-only software comparison acquisition."""
import json
from pathlib import Path
from urllib.parse import urlencode
from publish_latent_r_review_v2_20261013 import ref, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-17/other-temporal'
RAW=ROOT/'docs/literature/raw'


def main():
    old=ROOT/'docs/literature/fetch-manifest.json'
    write(BASE/'previous-fetch-manifest.json',json.loads(old.read_text()))
    pins=json.loads((ROOT/'docs/program/execution/2026-10-13/other-discovery/pins.json').read_text())
    selected={
        'associations':['src/methods/information/definitions/transferentropy/TEShannon.jl',
            'src/methods/information/definitions/transferentropy/embedding.jl',
            'src/independence_tests/surrogate/transferentropy.jl',
            'src/independence_tests/local_permutation/transferentropy.jl',
            'src/methods/crossmappings/ccm-like/ConvergentCrossMapping.jl',
            'src/methods/crossmappings/ccm-like/common.jl','Project.toml'],
        'varlingam':['src/var_lingam.rs','Cargo.toml'],
        'bnt':['BNT/general/mk_dbn.m','BNT/general/do_intervention.m',
            'BNT/general/unroll_dbn_topology.m','BNT/general/sample_dbn.m']}
    requests=[];items=[]
    for package,paths in selected.items():
        pin=pins[package];tree=json.loads((RAW/f'exec13_other_tree_{package}.json').read_text())
        assert not tree['truncated']
        by_path={r['path']:r for r in tree['tree'] if r['type']=='blob'}
        for i,path in enumerate(paths):
            row=by_path[path];key=f'exec17_other_temporal_{package}_{i}'
            request={'id':key,'url':f'https://raw.githubusercontent.com/{pin["repository"]}/{pin["sha"]}/{path}','extension':'txt'}
            requests.append(request);items.append(dict(request,package=package,source_path=path,
                blob_sha1=row['sha'],expected_bytes=row['size'],pin=pin))
    queries=['causal discovery language:Julia','causal discovery language:Rust',
        'causal discovery language:Matlab','Granger causality language:Matlab',
        'transfer entropy language:Matlab','causal discovery language:JavaScript']
    for i,q in enumerate(queries):
        requests.append({'id':f'exec17_other_temporal_search_{i}',
            'url':'https://api.github.com/search/repositories?'+urlencode({'q':q+' created:<=2026-10-07','per_page':10,'page':1}),
            'extension':'json'})
    manifest={'requests':requests,'cutoff':'2026-10-07','stopping_rule':'Six queries, one ten-result page each; selected exact pinned files; no completeness or absence inference.'}
    write(BASE/'acquisition-manifest.json',manifest);write(BASE/'selected-files.json',{'items':items})
    write(BASE/'inherited-search.json',{'query':ref(RAW/'v12_sw_cell_discovery_temporal_interventional_other.json','Original ten returned scholarly leads'),
        'result':'35 metadata matches, first10 saved; no selected package in inherited matrix. No absence finding.',
        'pins':ref(ROOT/'docs/program/execution/2026-10-13/other-discovery/pins.json','Reused original cutoff-compatible identities')})
    old.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'requests':len(requests),'pinned_files':len(items),'bounded_queries':6}))


if __name__=='__main__':main()
