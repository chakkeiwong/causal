#!/usr/bin/env python3
"""Generate the bounded supplement table from the verified request summary."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'docs/studies/weak-audit-projection-results.json'
TARGET = 'docs/supplements/weak-audit-table.tex'


def digest(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def main():
    result = json.loads((ROOT / SOURCE).read_text())
    if result['status'] != 'pass' or result['requests'] != 3000:
        raise ValueError('Incomplete registered final study')
    labels = dict(baseline_1200='Baseline', small_audit_1200='Small audit',
                  near_rank_1200='Near rank', persistent_1200='Persistent',
                  false_exogeneity_1200='False exogeneity')
    lines = [r'\begin{table}[htbp]', r'\centering\small',
             r'\caption{Fresh paired funding inference: all-request coverage and useful precision. Each row has 600 independent synthetic requests. A whole-line set counts as coverage if it contains the fixed truth, but has no finite decision width. Finite median widths are in thousands of USD, conditional on a finite set.}',
             r'\label{tab:weak-audit-results}',
             r'\begin{tabular}{lrrrrrr}', r'\toprule',
             r'Design & Regular cover & Set cover & Finite set & Whole line & Regular width & Set width \\',
             r'\midrule']
    for row in result['results']:
        name = row['design']['name']
        a = row['summary']['methods']['pilot4_horizon']
        b = row['summary']['methods']['weak_audit_projection']
        if not b['finite_width_quantiles'] or not a['finite_width_quantiles']:
            raise ValueError('Missing finite width quantile')
        lines.append(f"{labels[name]} & {a['covered']}/600 & {b['covered']}/600 & "
                     f"{b['finite']}/600 & {b['whole_line']}/600 & "
                     f"{a['finite_width_quantiles'][1]/1000:.0f} & "
                     f"{b['finite_width_quantiles'][1]/1000:.0f} " + r'\\')
    lines += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
    path = ROOT / TARGET
    path.parent.mkdir(exist_ok=True)
    path.write_text('\n'.join(lines) + '\n')
    receipt = dict(status='pass', date='2026-10-11', rows=len(result['results']),
                   scope='Direct table from saved summaries; scientific interpretation requires the author review.',
                   input_sha256={name: digest(name) for name in (SOURCE, 'tools/weak_audit_tables.py', TARGET)})
    (ROOT / 'docs/reviews/weak-audit-table-generation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('Weak-audit table generated from five fixed summary rows.')


if __name__ == '__main__':
    main()
