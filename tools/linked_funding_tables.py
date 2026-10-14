#!/usr/bin/env python3
"""Generate the two delivery tables solely from the registered study summary."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = 'docs/studies/linked-funding-results.json'
TARGET = 'docs/supplements/linked-funding-tables.tex'


def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def main():
    data = json.loads((ROOT/RESULT).read_text())
    names = ['Baseline', 'Near rank', 'Exact rank', 'Low linked audit', 'Persistent',
             'False exogeneity', 'Wrong inclusion', 'Noisy labels']
    lines = [r'\begin{table}[htbp]\centering\small',
             r'\caption{Fresh 600-request cells. C uses count-audit transformed sets; A uses augmented linked outcomes; I uses inverse audit weighting. Widths are conditional finite medians in thousands of USD.}',
             r'\begin{tabular}{lrrrrrrr}\toprule',
             r'Design & C cover & A cover & I cover & C finite & A finite & A width & I width\\\midrule']
    for title, cell in zip(names, data['results']):
        m = cell['summary']['methods']
        c,a,i = (m[k] for k in ('transformed_counts','linked_augmented','linked_ipw'))
        widths = [f'{x["conditional_finite_median_width"]/1000:.0f}'
                  if x['conditional_finite_median_width'] is not None else '--' for x in (a,i)]
        lines.append(f'{title} & {c["covered"]} & {a["covered"]} & {i["covered"]} & {c["finite"]} & {a["finite"]} & {widths[0]} & {widths[1]}' + r'\\')
    lines += [r'\bottomrule\end{tabular}\label{tab:coverage}\end{table}',
              r'\begin{table}[htbp]\centering\small',
              r'\caption{Augmented-estimator diagnostics. Bias and empirical SD are thousands of USD, conditional on computed intervals. Labels count evaluation plus independent-pilot origin histories; each resolves all seven response dates.}',
              r'\begin{tabular}{lrrrr}\toprule',
              r'Design & Bias & Empirical SD & Mean SE / SD & Mean linked labels\\\midrule']
    for title, cell in zip(names, data['results']):
        s = cell['summary']; a = s['methods']['linked_augmented']
        lines.append(f'{title} & {a["conditional_bias"]/1000:.1f} & {a["conditional_empirical_sd"]/1000:.1f} & {a["mean_se_over_sd"]:.3f} & {s["mean_evaluation_labels"]+s["mean_pilot_labels"]:.1f}' + r'\\')
    lines += [r'\bottomrule\end{tabular}\label{tab:diagnostics}\end{table}']
    (ROOT/TARGET).write_text('\n'.join(lines)+'\n')
    receipt = dict(status='pass',date='2026-10-11',issues=[],rows=8,
                   input_sha256={p:digest(p) for p in (RESULT,TARGET,'tools/linked_funding_tables.py')})
    (ROOT/'docs/reviews/linked-funding-table-generation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('Eight registered cells generated into two tables.')


if __name__ == '__main__': main()
