#!/usr/bin/env python3
"""Exact project-owned longitudinal fixtures; upstream programs never execute."""
from fractions import Fraction as F
import json

def calculate():
 p=F(1,10);q=F(1,5);step=(1-q)*p;survive=(1-q)*(1-p);cif=step+survive*step;elim=p+(1-p)*p
 assert (cif,elim)==(F(86,625),F(19,100))
 risk_a=1-(1-F(1,10))**2;risk_b=1-(1-F(2,5))**2;full=(risk_a+risk_b)/2
 assert full==F(83,200) and risk_a==F(19,100)
 # A mathematical fixture for the inspected two-dimensional shape predicate, not an upstream invocation.
 rows,histories=3,2;documented_shape=(rows,histories);source_predicate=(documented_shape[1]==rows)
 assert source_predicate is False
 values=[F(1),F(-1)];surviving=[values[0]];assert sum(values)/2==0 and sum(surviving)==1
 return dict(kind='exact_authored_reference_not_native_results',
  competing=dict(periods=2,default_hazard_conditional_no_prepayment=str(p),prepayment_probability=str(q),within_period_order='prepayment then default',observed_event_risk=str(cif),eliminate_prepayment_risk=str(elim),loss_USD=10000,premium_USD=1600,observed_margin_USD=str(10000*cif-1600),elimination_margin_USD=str(10000*elim-1600)),
  composition=dict(baseline_strata_equal=True,horizon=2,A_risk=str(risk_a),B_risk=str(risk_b),baseline_standardized=str(full),only_A_retained_at_horizon=str(risk_a),difference=str(full-risk_a),meaning='Fixed supplied hazards; changed averaging population alone changes risk. No native output or correction for informative censoring.'),
  treatment_shape=dict(subjects=rows,periods=histories,valid_per_subject_shape=list(documented_shape),inspected_second_dimension_equals_subjects=source_predicate,native_execution=False),
  failed_replicates=dict(requested=2,accepted=1,full_fixture_mean='0',accepted_only_fixture_mean='1',meaning='Illustrates possible selection from failures, not estimated coverage or a real bootstrap distribution.'),
  monte_carlo=dict(independent_Bernoulli_draws=10000,variance=str(cif*(1-cif)/10000),meaning='Elementary conditional simulation variance, not fitted-model uncertainty or this package variance.'),
  native_execution=False,measured_bank_benefit=False)
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
