#!/usr/bin/env python3
"""Render selected saved results, without outcome-selected method choice."""
import json
from reliability_common import ROOT
from closure_common import save

def read(name):return json.loads((ROOT/('docs/studies/reliability-'+name+'-results.json')).read_text())
def table(rows,caption,label):
    lines=['\\begin{table}[htbp]','\\centering\\small','\\begin{tabular}{lrrr}','\\toprule','Design / method & Available & Coverage & MC95 \\\\','\\midrule']
    for name,r in rows:
        c=r['coverage_all'];lo,hi=c['mc95'];lines.append(f'{name} & {r["available"]}/{r["requested"]} & {c["frequency"]:.4f} & [{lo:.4f}, {hi:.4f}] \\\\')
    lines+=['\\bottomrule','\\end{tabular}',f'\\caption{{{caption}}}',f'\\label{{{label}}}','\\end{table}'];return '\n'.join(lines)

def main():
    names=['calibration','joint','graphs','nonlinear','learning','followup','workloads'];r={n:read(n) for n in names};cal=[]
    for d in r['calibration']['results']:
        name=d['design']['name'].replace('_',' ')
        for method,label in [('bandwidth_2','window 2'),('bandwidth_10','window 10'),('independent_reference_covariance','reference')]:cal.append((name+' / '+label,d['summary'][method]))
    sections=[table(cal,'Fresh funding calibration. Each method has 500 final draws per design. Reference covariance uses separate synthetic training; it is diagnostic information, not a bank-ready repair.','r8:calibration-table')]
    mainrows=[]
    for d in r['joint']['results']:mainrows.append((d['case'].replace('_',' '),d['summary']['joint']))
    follow=r['followup']['results'];mainrows.append(('larger joint / longer window',follow[0]['summary']['window_5']))
    sections.append(table(mainrows,'Persistent identities and a shared calendar. Adverse inclusion and selected-label declarations violate the supplied model. The larger design is a fresh registered follow-up.','r8:joint-table'))
    rows=[]
    for d in r['graphs']['results']:
        if d['case'] in ('strong_valid','weak_valid','zero_stage','false_exclusion'):rows.append((d['case'].replace('_',' '),d['summary']['pivot_randomized_encouragement']))
        if d['case']=='sufficient':rows.append(('observed sufficiency',d['summary']['pivot_observed_sufficiency']))
    for d in r['nonlinear']['results']:rows.append(('nonlinear / '+d['case'].replace('_',' '),d['summary']['heterogeneous_variance']))
    for d in r['learning']['results']:rows.append(('learner / '+d['case'].replace('_',' '),d['summary']['chunked']))
    rows.append(('larger learner / longer window',follow[1]['summary']['window_5']))
    sections.append(table(rows,'Selected graph, nonlinear and learner procedures. Coverage is over every requested draw; unqualified fits count as unavailable. Monte Carlo intervals describe simulation uncertainty, not bank validity.','r8:extension-table'))
    path='docs/derivations/reliability_tables.tex';(ROOT/path).write_text('\n\n'.join(sections)+'\n')
    save('docs/reviews/reliability-table-generation.json',dict(status='pass',output=path,scope='Deterministic display of prespecified saved arms, not scientific approval.'),['tools/reliability_tables.py',path]+['docs/studies/reliability-'+n+'-results.json' for n in names])
    print('Saved three selected comparison tables.')

if __name__=='__main__':main()
