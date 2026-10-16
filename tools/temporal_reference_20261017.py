#!/usr/bin/env python3
"""Exact authored temporal laws for the proposal; no upstream code execution."""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-17/other-temporal'


def calculate():
    # Common-calendar shock: two accounts share the same daily shock, so ten
    # rows contain only two independent calendar units.
    effects=[F(10),F(-10)]
    household_weight=F(9,10)*effects[0]+F(1,10)*effects[1]
    # A nominal one-step lag is 1 day only under daily sampling. Resampling to
    # weekly makes it seven days; naming a lag does not define its clock.
    monthly_effect=F(30)
    daily_lag=F(1);weekly_lag=F(1)
    # BNT-style intervention on a supplied two-node transition matrix.
    transition=[[F(4,5),F(1,5)],[F(0),F(1)]]
    do_x1=[F(0),F(1)]
    p_y1_given_do_x1=transition[1][1]*do_x1[1]+transition[0][1]*do_x1[0]
    # A data law with a latent regime changes the observed lag coefficient.
    regime0=F(1,2)*F(1,2);regime1=F(1,2)*F(3,2)
    return {
        'scope':'Exact project-authored temporal examples; no package or bank execution',
        'calendar_dependence':{'effects_usd':[str(x) for x in effects],
            'independent_calendar_units':2,'rows':10,'account_weighted_effect_usd':str(household_weight),
            'warning':'Rows sharing a calendar shock are not ten independent units.'},
        'sampling_clock':{'daily_one_step_days':str(daily_lag),'weekly_one_step_days':str(weekly_lag*7),
            'same_lag_name_different_horizon':True,'monthly_effect_days':str(monthly_effect),
            'required_field':'sampling_frequency and time origin'},
        'dynamic_intervention':{'transition_matrix':[[str(x) for x in row] for row in transition],
            'do_x_1':list(map(str,do_x1)),'identified_y1_probability':str(p_y1_given_do_x1),
            'meaning':'Surgical intervention is defined on the supplied transition model; it does not validate the model.'},
        'regime_shift':{'regime_probabilities':['1/2','1/2'],'lag_coefficient_regime0':str(regime0),
            'lag_coefficient_regime1':str(regime1),'pooled_mean':str((regime0+regime1)/2),
            'stationarity_required':'A pooled lag is not a single structural effect when regimes differ.'},
        'temporal_method_limits':{
            'transfer_entropy':'Predictive information from source past to target future conditional on target/conditioning histories; embedding and surrogate law must be specified.',
            'cross_mapping':'Library-size prediction/correlation under an embedding; direction and common drivers need separate scrutiny.',
            'var_lingam':'VAR plus DirectLiNGAM under non-Gaussian independent disturbances and acyclic instantaneous structure; thresholds and sample warnings are not calibration.',
            'dbn_intervention':'BNT mutilates a supplied DBN by clamping nodes and removing incoming arcs; model construction and parameter validity precede intervention.'}
    }


if __name__=='__main__':
    result=calculate()
    with (BASE/'exact-results.json').open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({'families':4,'path':str((BASE/'exact-results.json').relative_to(ROOT))}))
