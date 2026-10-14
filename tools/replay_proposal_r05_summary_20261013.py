#!/usr/bin/env python3
"""Use R05-v2's registered summary version; retain the first harness failure."""
import json
from pathlib import Path

import master_experiment_v2 as registered
from review_proposal_demonstration_boundaries_20261013 import BASE, ROOT, ref, save


def main():
    out = BASE / 'followup-r05-summary-repaired'
    out.mkdir(exist_ok=False)
    base = ROOT / 'docs/program/master/work/R05-v2'
    protocol = base / 'protocol.json'
    spec = json.loads(protocol.read_text())
    original = base / 'results.json'
    frozen = json.loads(original.read_text())
    identities = {name: ref(ROOT / name)['sha256'] for name in spec['input_sha256']}
    assert identities == spec['input_sha256']
    assert 'tools/master_experiment_v2.py' in identities
    rows, hashes = [], {}
    for cell in range(len(spec['designs'])):
        for index in range(spec['replications']):
            key = f'{cell:02d}-{index:05d}'
            path = base / 'requests' / (key + '.json')
            identity = ref(path)
            assert frozen['request_sha256'][identity['path']] == identity['sha256']
            row = json.loads(path.read_text())
            assert (row['key'], row['cell'], row['index'], row['registration_sha256']) == (
                key, cell, index, ref(protocol)['sha256'])
            rows.append(row)
            hashes[identity['path']] = identity['sha256']
    fresh = registered.summary(rows, spec)
    fresh.update(launch=json.loads((base / 'launch.json').read_text()),
                 registration_sha256=ref(protocol)['sha256'], request_sha256=hashes)
    assert fresh == frozen
    manuscript_path = ROOT / 'docs/program/repair-v12/integrated-reader/chapters/master_execution.tex'
    manuscript = manuscript_path.read_text()
    table_rows = []
    for cell in fresh['cells']:
        primary = cell['methods'][spec['methods'][0]]
        challenger = cell['methods'][spec['methods'][1]]
        median = '--' if primary['width_quantiles'] is None else f"{primary['width_quantiles'][1]:.3f}"
        row = (f"{cell['design']['name'].replace('_', ' ')} & {primary['covered']}/512 & "
               f"{primary['simultaneous_lower95']:.3f} & {primary['finite']}/512 & "
               f"{median} & {challenger['covered']}/512")
        assert row in manuscript, row
        table_rows.append(row)
    save(out / 'R05-v2-summary.json', fresh)
    receipt = {'status': 'pass', 'harness': ref(Path(__file__)),
        'original': ref(original), 'protocol': ref(protocol),
        'summary_implementation': ref(Path(registered.__file__)),
        'original_failure': ref(BASE / 'followup-summaries/receipt.json'),
        'finding': 'The first follow-up harness selected the original summary module for R05-v2. Its registered protocol binds master_experiment_v2.py, which adds topology and true-class fields. Using that exact module reconstructs every field with no change to the study.',
        'requests': len(rows), 'full_summary_exact': True,
        'table_rows_verified': table_rows, 'manuscript': ref(manuscript_path),
        'recomputed': ref(out / 'R05-v2-summary.json'), 'new_simulator_draws': 0,
        'limits': ['Saved summary reconstruction, not a full rerun of all random requests.']}
    save(out / 'receipt.json', receipt)
    print(json.dumps({'status': 'pass', 'requests': len(rows), 'table_rows': len(table_rows)}))


if __name__ == '__main__':
    main()
