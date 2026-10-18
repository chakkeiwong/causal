#!/usr/bin/env python3
"""Prepare bounded identity acquisition for the inherited DuckDB proposal choice."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-19/duckdb-reuse-v1'


def main():
    assert not BASE.exists()
    BASE.mkdir(parents=True)
    manifest=ROOT/'docs/literature/fetch-manifest.json'
    write(BASE/'previous-fetch-manifest.json',json.loads(manifest.read_text()))
    (BASE/'plan.md').write_text(
        '# DuckDB reuse decision plan, 19 October 2026\n\n'
        'Review inherited_duckdb as a proposal choice for bounded local analytical data preparation. '
        'Do not infer causal identification or uncertainty guarantees from a database query. '
        'Verify a selected immutable pre-cutoff source revision before technical claims. Begin with '
        'historical tag v1.4.0, whose frozen PyPI metadata records a 16 September 2025 source release; '
        'this is not a newest-release or present-support claim. Resolve commit/tree identity and '
        'authenticate inspected source blobs. Inspect license scopes, build dependencies, query/null/order '
        'semantics, transaction boundaries and external-access/extension controls. Propose row/key/time/ '
        'missingness and failure contracts with an exact authored reference. Compare narrower file, '
        'SQLite and columnar alternatives without asserting uninspected parity. No downloaded code, '
        'package or sibling repository will execute. Defer executable admission until complete pinned '
        'distribution/dependencies, rights and native conformance are reviewed. Record a bounded proposal '
        'decision and integrate it in preserving reader/sponsor successors. Preserve failed original pin '
        'lookup and all new acquisition failures. One blocked source does not stop independent work.\n')
    requests=[dict(id='exec19_duckdb_commit_v140',url='https://api.github.com/repos/duckdb/duckdb/commits/v1.4.0',extension='json'),
        dict(id='exec19_duckdb_release_v140',url='https://api.github.com/repos/duckdb/duckdb/releases/tags/v1.4.0',extension='json')]
    write(BASE/'identity-acquisition-manifest.json',dict(requests=requests,cutoff='2026-10-07',
        selected_version='Historical v1.4.0; not a latest-release claim',
        stopping_rule='Two bounded identity reads; select technical paths only after verified tree inspection.'))
    write(BASE/'plan-review.json',dict(status='pass',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/'plan.md','Reviewed identity, semantics, rights and admission obligations'),
            ref(ROOT/'docs/literature/raw/head_duckdb.receipt.json','Inherited403 pin lookup failure'),
            ref(ROOT/'docs/literature/raw/pypi_duckdb.receipt.json','Frozen7October2026 metadata acquisition'),
            ref(BASE/'identity-acquisition-manifest.json','Bounded public identity reads')],
        checks=['No causal guarantee follows from database execution.',
            'Historical revision is selected explicitly and pinned; default branch is not frozen.',
            'Root MIT evidence cannot clear all bundled extensions or transitive dependencies.',
            'Query ordering, missingness, snapshots and external reads have separate obligations.',
            'Executable admission can be deferred within a completed proposal decision.'],integration_allowed=False))
    manifest.write_text(json.dumps(dict(requests=requests),indent=2)+'\n')
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)),requests=len(requests))))


if __name__=='__main__':
    main()
