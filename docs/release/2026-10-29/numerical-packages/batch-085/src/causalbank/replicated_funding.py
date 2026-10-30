"""Known randomized action law and genuinely independent funding calendars.

This is a changed information/sampling experiment, not a correction that can
be applied to adjacent blocks of a single bank calendar.
"""
import numpy as np
from scipy.stats import t
from .funding_calibration import pilot_data
from .linked_funding import pseudo_rows
from .streaming_pilot import train_streaming_pilot


def control_score(rows, audit, horizon, weights, coefficient, control):
    data = pilot_data(pseudo_rows(rows, *audit, horizon))
    # The conditional action mean and variance are supplied by randomization.
    v = data['action'] - .5*rows[:, 3] - .2*rows[:, 4]
    outcome = data['outcomes']@weights - (data['x']@coefficient[:, 1:])@weights
    return v*outcome - control*(v*v-1.)


def fit_replicates(pilot, pilot_audit, calendars, audits, target, penalties, alpha=.01):
    if len(calendars) < 3 or len(calendars) != len(audits):
        raise ValueError('Independent aligned calendar replicates required')
    transformed = pseudo_rows(pilot, *pilot_audit, target.horizon)
    coefficient = train_streaming_pilot(transformed, penalties)['coefficient']
    data = pilot_data(transformed)
    v = data['action']-.5*pilot[:, 3]-.2*pilot[:, 4]
    control = float(np.mean(v*(data['outcomes']@target.weights())))
    values = np.array([control_score(r, a, target.horizon, target.weights(), coefficient, control).mean()
                       for r, a in zip(calendars, audits)])
    estimate = float(values.mean()-target.direct_cost())
    se = float(values.std(ddof=1)/np.sqrt(len(values)))
    if not np.isfinite(se) or se <= 0:
        return dict(status='unavailable_calendar_variance')
    critical = float(t.ppf(1-alpha/2, len(values)-1))
    return dict(status='computed_conditional', estimate=estimate, standard_error=se,
                interval=[estimate-critical*se, estimate+critical*se],
                calendar_replicates=len(values), calendar_scores=values.tolist(),
                alpha=alpha, pilot_control=control,
                scope='Asymptotic across independent calendars conditional on independent pilot; known randomized action mean/variance. Student critical is not an exact t pivot.')
