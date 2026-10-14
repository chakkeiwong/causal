#!/usr/bin/env python3
"""Generate follow-up table directly from the repaired 3,600-request summary."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE='docs/studies/weak-audit-sharpening-results.json'
TARGET='docs/supplements/weak-audit-sharpening-table.tex'


def digest(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()


def main():
    data=json.loads((ROOT/SOURCE).read_text())
    if data['status']!='pass' or data['requests']!=3600:raise ValueError('Incomplete follow-up')
    names={'baseline_1200':'Baseline','small_audit_1200':'Small audit',
           'near_rank_1200':'Near rank','persistent_1200':'Persistent',
           'false_exogeneity_1200':'False exog.','near_rank_more_audit_1200':'Near rank, 8x audit'}
    rows=[r'\begin{table}[htbp]',r'\centering\small',
          r'\caption{Fresh 600-request matched designs. C is the candidate rectangle and A/D the transformed average/difference rectangle. Finite median widths are thousands of USD and are descriptive only on the paired finite subset. Whole-line outputs have no finite decision width.}',
          r'\label{tab:sharpening}',r'\begin{tabular}{lrrrrrr}',r'\toprule',
          r'Design & C cover & A/D cover & Both finite & Whole A/D & C width & A/D width \\',r'\midrule']
    for item in data['results']:
        name=item['design']['name']; a=item['summary']['methods']['candidate_rectangle'];
        b=item['summary']['methods']['average_difference_rectangle'];p=item['summary']['paired']
        rows.append(f"{names[name]} & {a['covered']}/600 & {b['covered']}/600 & {p['both_finite']}/600 & "
                    f"{b['whole_line']}/600 & {a['conditional_finite_median_width']/1000:.0f} & "
                    f"{b['conditional_finite_median_width']/1000:.0f} " + r'\\')
    rows += [r'\bottomrule',r'\end{tabular}',r'\end{table}']
    (ROOT/TARGET).write_text('\n'.join(rows)+'\n')
    receipt=dict(status='pass',date='2026-10-11',issues=[],rows=6,
        scope='Direct generated table from the fresh registered summary; not bank validation.',
        input_sha256={name:digest(name) for name in [SOURCE,TARGET,'tools/weak_audit_sharpening_tables.py']})
    (ROOT/'docs/reviews/weak-audit-sharpening-table-generation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('Six-design repaired follow-up table generated.')


if __name__=='__main__':main()
