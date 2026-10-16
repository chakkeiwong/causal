#!/usr/bin/env python3
"""Exact authored measurement laws; never imports or runs upstream code."""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-17/variable-ontology'


def calculate():
    prevalence = F(1, 5)
    sensitivities = [F(4, 5), F(9, 10)]
    false_positives = [F(1, 20), F(3, 20)]
    cells, observed, accuracy, corrected = [], [], [], []
    for s, f in zip(sensitivities, false_positives):
        table = {'true1_label1': prevalence*s, 'true1_label0': prevalence*(1-s),
                 'true0_label1': (1-prevalence)*f, 'true0_label0': (1-prevalence)*(1-f)}
        assert sum(table.values()) == 1
        q = table['true1_label1'] + table['true0_label1']
        cells.append({k: str(v) for k, v in table.items()})
        observed.append(q); accuracy.append(table['true1_label1'] + table['true0_label0'])
        corrected.append((q-f)/(s-f))
    effects, multiplicities = [F(10), F(-10)], [9, 1]
    observed_mass = prevalence + (1-prevalence)*F(1, 4)
    selected_risk = prevalence/observed_mass
    # Population-weighted selected contributions using the known stipulated
    # observation law, not an estimated weighting method or imputation model.
    corrected_selected = (prevalence/1)/(prevalence/1 + (1-prevalence)*F(1,4)/F(1,4))
    common = 'monthly household income before tax during the reporting period'.split()
    gold, predicted = set(['document_a']+common), set(['document_b']+common)
    jaccard = F(len(gold & predicted), len(gold | predicted))
    return {
        'scope': 'Exact project-authored examples; no package, LLM or bank execution',
        'differential_measurement': {
            'true_risks': [str(prevalence)]*2, 'sensitivities': list(map(str,sensitivities)),
            'false_positive_rates': list(map(str,false_positives)), 'joint_cells_given_arm': cells,
            'measured_risks': list(map(str,observed)), 'accuracies': list(map(str,accuracy)),
            'pooled_balanced_accuracy': str(sum(accuracy)/2),
            'true_effect': '0', 'measured_effect': str(observed[1]-observed[0]),
            'known_law_corrected_risks': list(map(str,corrected)),
            'stipulated_usd_per_event': 1000, 'spurious_usd_per_account': int(1000*(observed[1]-observed[0])),
            'alternative_perfect_measurement_true_effect': str(observed[1]-observed[0]),
            'same_observed_arm_label_law': True,
            'identification_limit': 'Unknown sensitivity and false-positive rates do not identify latent risks.'},
        'aggregation': {'household_effects_usd': list(map(str,effects)), 'accounts_per_household': multiplicities,
            'household_uniform_usd': str(sum(effects)/len(effects)),
            'account_weighted_household_usd': str(sum(e*n for e,n in zip(effects,multiplicities))/sum(multiplicities)),
            'independent_households': 2, 'replicated_rows': 10},
        'units': {'debt_usd_per_month': 1500, 'income_usd_per_month': 3000,
            'income_usd_per_year': 36000, 'matched_period_ratio': str(F(1500,3000)),
            'unconverted_period_ratio': str(F(1500,36000)),
            'converted_period_ratio': str(F(1500,1)/(F(36000,12)))},
        'availability': {'event':1,'available':5,'decision':3,
            'event_precedes_decision':1<=3,'available_by_decision':5<=3,
            'parent_availability':[2,5],'declared_derived_availability':4,
            'earliest_derived_availability':max([2,5]),'derived_declaration_valid':4>=max([2,5])},
        'selective_notes': {'true_risks':['1/5','1/5'],
            'observation_given_treated_event':'1','observation_given_treated_nonevent':'1/4',
            'treated_observation_probability':str(observed_mass),
            'observed_control_risk':'1/5','observed_treated_risk':str(selected_risk),
            'selected_contrast':str(selected_risk-prevalence),
            'known_selection_corrected_risk':str(corrected_selected)},
        'metric_identity': {'gold_document':'document_a','predicted_document':'document_b',
            'common_tokens':common,'jaccard':str(jaccard),'threshold':'4/5',
            'lexical_threshold_match':jaccard>=F(4,5),'exact_document_match':False,
            'directed_cause_reversal_matches':False,'declared_sameas_reversal_matches':True,
            'scope':'Authored mathematical counterexample to inspected scoring definition; upstream function not executed.'}
    }


if __name__ == '__main__':
    result = calculate()
    with (BASE/'exact-results.json').open('x') as stream:
        json.dump(result, stream, indent=2); stream.write('\n')
    print(json.dumps({'families':6,'path':str((BASE/'exact-results.json').relative_to(ROOT))}))
