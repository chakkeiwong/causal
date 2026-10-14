#!/usr/bin/env python3
"""Prepare bounded cutoff acquisition without changing the collector or rules."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/python-discovery'
RAW = ROOT / 'docs/literature/raw'
MANIFEST = ROOT / 'docs/literature/fetch-manifest.json'
PREFIX = 'v12_exec13_pydisc_'
REPOS = {'causalnex': 'quantumblacklabs/causalnex', 'causica': 'microsoft/causica',
         'gcastle': 'huawei-noah/trustworthyAI', 'dagma': 'kevinsbello/dagma',
         'notears': 'xunzheng/notears', 'cdt': 'FenTechSolutions/CausalDiscoveryToolbox'}


def save(phase, requests, purpose):
    p = BASE / ('fetch-' + phase + '.json')
    assert not p.exists()
    value = {'purpose': purpose, 'cutoff': '2026-10-07', 'requests': requests}
    p.write_text(json.dumps(value, indent=2) + '\n')
    MANIFEST.write_bytes(p.read_bytes())
    print(json.dumps({'manifest': str(p.relative_to(ROOT)), 'requests': len(requests)}))


def pins():
    previous = BASE / 'previous-fetch-manifest.json'
    assert not previous.exists()
    previous.write_bytes(MANIFEST.read_bytes())
    rows = []
    for name, repo in REPOS.items():
        query = {'until': '2026-10-07T23:59:59Z', 'per_page': 1}
        if name == 'gcastle':
            query['path'] = 'gcastle'
        rows.append({'id': PREFIX + name + '_cutoff',
                     'url': 'https://api.github.com/repos/' + repo + '/commits?' + urlencode(query),
                     'extension': 'json'})
    save('01', rows, 'Unresolved declared Python discovery candidates and CDT neighbor: cutoff-bounded source identity')


def trees():
    rows = []
    for name, repo in REPOS.items():
        path = RAW / (PREFIX + name + '_cutoff.json')
        if not path.exists():
            continue
        commits = json.loads(path.read_text())
        if not isinstance(commits, list) or not commits:
            continue
        sha = commits[0]['sha']
        rows.append({'id': PREFIX + name + '_tree',
                     'url': 'https://api.github.com/repos/' + repo + '/git/trees/' + sha + '?recursive=1',
                     'extension': 'json'})
    save('02', rows, 'Pinned primary repository tree for bounded implementation/license selection')


def restore():
    MANIFEST.write_bytes((BASE / 'previous-fetch-manifest.json').read_bytes())
    print(json.dumps({'restored_manifest': True}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['pins', 'trees', 'restore'])
    args = p.parse_args(); {'pins': pins, 'trees': trees, 'restore': restore}[args.command]()
