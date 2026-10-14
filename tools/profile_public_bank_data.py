#!/usr/bin/env python3
"""Describe the public UCI bank archive; no fitting or causal inference."""
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/public-data-v15'
ARCHIVE = ROOT / 'docs/literature/raw/pd15_uci_bank_archive.txt'
OUT = ROOT / 'docs/datasets/public-v15/bank-marketing'


def binding(path):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    allowed = {'bank.csv', 'bank-full.csv', 'bank-names.txt',
               'bank-additional.csv', 'bank-additional-full.csv', 'bank-additional-names.txt'}
    members = {}
    def inspect(blob, depth=0):
        if depth > 1:
            raise ValueError('Unexpected nesting')
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            for item in z.infolist():
                if item.file_size > 32 * 1024 * 1024:
                    raise ValueError('Member exceeds profiling budget')
                if item.filename.endswith('.zip'):
                    inspect(z.read(item), depth + 1)
                elif Path(item.filename).name in allowed:
                    name = Path(item.filename).name
                    if name in members:
                        raise ValueError('Duplicate member')
                    members[name] = z.read(item)
    inspect(ARCHIVE.read_bytes())
    if set(members) != allowed:
        raise ValueError('Unexpected archive contents')
    reports = []
    for name, data in sorted(members.items()):
        path = OUT / name
        path.write_bytes(data)
        if not name.endswith('.csv'):
            continue
        rows = list(csv.DictReader(io.StringIO(data.decode('utf-8')), delimiter=';'))
        fields = list(rows[0])
        reports.append({
            'file': binding(path), 'rows': len(rows), 'columns': fields,
            'predictor_columns': len(fields) - 1,
            'subscription_counts': dict(sorted(Counter(r['y'] for r in rows).items())),
            'empty_cells': {k: sum(r[k] == '' for r in rows) for k in fields},
            'unknown_cells': {k: sum(r[k] == 'unknown' for r in rows) for k in fields
                              if any(r[k] == 'unknown' for r in rows)},
            'duration_seconds': {'minimum': min(int(r['duration']) for r in rows),
                                 'maximum': max(int(r['duration']) for r in rows)},
            'duplicate_complete_rows': len(rows) - len({tuple(r.items()) for r in rows}),
            'duplicate_note': 'Identical rows do not identify duplicate people; no entity key is supplied.',
        })
    report = {'status': 'completed_descriptive_profile',
              'code': binding(Path(__file__)), 'archive': binding(ARCHIVE),
              'archive_receipt': binding(ARCHIVE.with_name('pd15_uci_bank_archive.receipt.json')),
              'datasets': reports, 'extracted_files': [binding(OUT / n) for n in sorted(members)],
              'causal_effect_estimated': False, 'study_registration_claim': False,
              'limits': ['Descriptive inspection only; no hypothesis test, model fit or causal effect.',
                         'No customer identity, random-assignment probabilities or uncontacted control population established.',
                         'Call duration is measured during the contact; it is unavailable for a pre-contact decision.',
                         'No blanks does not mean no missing information: categorical unknown values remain.',
                         'The full and ten-percent versions overlap; never treat them as independent replications.']}
    (BASE / 'bank-profile.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'rows': {r['file']['path'].split('/')[-1]: r['rows'] for r in reports},
                      'causal_effect_estimated': False}))


if __name__ == '__main__':
    main()
