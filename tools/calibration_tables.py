#!/usr/bin/env python3
"""Generate V9 comparisons and paired differences from retained observations."""
import json
import numpy as np
from calibration_common import ROOT, save


def read(name):
    return json.loads((ROOT/name).read_text())


def main():
    inputs = ['tools/calibration_tables.py', 'docs/studies/calibration-diagnostics-results.json',
        'docs/studies/calibration-validation-results.json', 'docs/studies/calibration-followup-results.json',
        'docs/studies/calibration-followup-final.jsonl', 'docs/studies/calibration-workload-remeasurement-results.json']
    diagnostics = read(inputs[1])
    validation = read(inputs[2])
    followup = read(inputs[3])
    workloads = read(inputs[5])
    lines = []
    def begin(columns, header):
        lines.extend([r'\begin{table}[htbp]\centering\small', r'\begin{tabular}{'+columns+'}', r'\toprule', header+r'\\\midrule'])
    def end(caption, label):
        lines.extend([r'\bottomrule\end{tabular}', r'\caption{'+caption+'}', r'\label{'+label+'}', r'\end{table}', ''])
    begin('llrrrr', 'Dates & Nuisance / pilot & Shift & Bias & Coverage & SE/SD')
    for case in diagnostics['results']:
        if case['dates'] != 4800:
            continue
        entries = [('M400/estimated_both', 'fitted / 400'), ('M1600/estimated_both', 'fitted / 1600'),
            ('M19200/estimated_both', 'fitted / 19200'), ('M1600/known_action', 'known action'),
            ('M1600/known_outcome', 'known outcome'), ('M1600/known_both', 'both known')]
        for key, label in entries:
            s = case['summary'][key+'/innovation_horizon/known_audit']
            shift = case['conditional_bias'][key]['mean']
            lines.append(f"4800 & {label} & {shift/1000:.2f} & {s['bias']/1000:.2f} & {s['coverage_all']['frequency']:.3f} & {s['mean_se']/s['empirical_sd']:.3f}"+r'\\')
    end('Nuisance attribution with known audit probabilities and horizon covariance. Shift is the mean exact conditional pilot target minus truth; bias is the empirical finite-sample error, both in thousands of currency units. Each row uses 500 draws. Oracle rows are diagnostic information.', 'v9:diagnostic-table')
    begin('lrrrr', 'Design & Available & Pilot/B & Joint/B & Joint/H')
    labels = ['720', '1200', '4800', 'persistent 4800', 'weak audit', 'omitted action term', 'endogenous innovation']
    for label, case in zip(labels, validation['results']):
        summary = case['summary']
        primary = summary['joint_ols_innovation_horizon']
        cov = [summary[k]['coverage_all']['frequency'] for k in ['inherited_pilot_bartlett', 'joint_ols_bartlett', 'joint_ols_innovation_horizon']]
        lines.append(f"{label} & {primary['available']}/600 & {cov[0]:.4f} & {cov[1]:.4f} & {cov[2]:.4f}"+r'\\')
    end('Fresh fixed-dictionary comparison. B uses Bartlett covariance; H uses untapered lags through the response horizon. Coverage divides by all 600 requested draws; availability is common to the methods here. The last two laws violate the supplied assumptions.', 'v9:validation-table')
    begin('lrrrr', 'Dates & Old pilot/B & Fourfold/B & Fourfold/H & H MC95')
    for case in followup['results']:
        summary = case['summary'];primary = summary['fourfold_pilot_innovation_horizon']['coverage_all'];lo, hi = primary['mc95']
        cov = [summary[k]['coverage_all']['frequency'] for k in ['inherited_pilot_bartlett', 'fourfold_pilot_bartlett', 'fourfold_pilot_innovation_horizon']]
        lines.append(f"{case['design']['dates']} & {cov[0]:.4f} & {cov[1]:.4f} & {cov[2]:.4f} & [{lo:.4f}, {hi:.4f}]"+r'\\')
    end('Fresh growing-pilot comparison, 600 independent draws per design, all available. The pilot is four times evaluation length. The 720-date old pilot was already fourfold; 1200/4800 require three/twelve times the old pilot history. Monte Carlo uncertainty is not a uniform or bank-validity guarantee.', 'v9:followup-table')
    begin('lrrr', 'Dates / repeat & QR/dense memory & QR/dense time & Relative error')
    for case in workloads['comparisons']:
        lines.append(f"{case['dates']} / {case['repeat']+1} & {case['chunked_to_dense_peak_rss']:.3f} & {case['chunked_to_dense_complete_seconds']:.3f} & {case['maximum_relative_difference']:.1e}"+r'\\')
    end('Complete local joint-regression workloads, measured through a small independent launcher. Peak process memory includes mapped input pages. Both routes include input verification, fitting, inference and output read-back; acquisition is excluded equally. This is not the growing-pilot implementation or a bank-platform measurement.', 'v9:workload-table')
    output = 'docs/derivations/calibration_tables.tex'
    (ROOT/output).write_text('\n'.join(lines))
    journal = [json.loads(line) for line in (ROOT/inputs[4]).read_text().splitlines()[1:]]
    paired = []
    for case in followup['results']:
        rows = [r['result'] for r in journal if r['key'].startswith(case['design']['name']+'/')]
        truth = case['financial_truth']
        for method in ('fourfold_pilot_bartlett', 'fourfold_pilot_innovation_horizon'):
            def covered(row, name):
                r = row['methods'][name]
                return int(r['status'] == 'computed' and r['interval'][0] <= truth <= r['interval'][1])
            changes = np.array([covered(row, method)-covered(row, 'inherited_pilot_bartlett') for row in rows])
            error = changes.std(ddof=1)/np.sqrt(len(changes))
            paired.append(dict(design=case['design']['name'], method=method, paired_coverage_difference=float(changes.mean()),
                new_only=int(np.sum(changes == 1)), old_only=int(np.sum(changes == -1)),
                approximate_mc95=[float(changes.mean()-1.96*error), float(changes.mean()+1.96*error)]))
    save('docs/reviews/calibration-table-generation.json', dict(status='pass', tables=4, paired_followup=paired,
        scope='Exact retained-result table generation and descriptive paired Monte Carlo differences; no superiority selection or multiplicity-adjusted claim.'), inputs+[output])
    print(json.dumps(dict(status='pass', tables=4, paired_followup=paired)))


if __name__ == '__main__':
    main()
