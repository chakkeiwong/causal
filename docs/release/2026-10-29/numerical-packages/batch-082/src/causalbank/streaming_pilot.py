"""Blockwise equivalent of the selected independent-pilot funding procedure.

Statistical premises and refusal semantics are inherited from V9. QR factors
compress the original chronological tuning/refit objective, not a new learner.
"""
import numpy as np
from .funding_calibration import DECLARATIONS, LagAccumulator, _prepare, _finish, pilot_data


def _blocks(rows, size):
    for start in range(0, len(rows), size):
        block = np.asarray(rows[start:start+size])
        if (not np.isfinite(block).all() or
                not np.isin(block[:, 0], [0, 1]).all() or
                not np.all(block[:, 2] == 1)):
            raise ValueError('Nonfinite history, invalid stratum or missing intercept')
        yield block


def _factor(rows, size):
    factor = None
    count, mean, centered = 0, None, None
    for block in _blocks(rows, size):
        data = pilot_data(block)
        y = np.column_stack((data['action'], data['outcomes']))
        augmented = np.column_stack((data['x'], y))
        factor = np.linalg.qr(augmented if factor is None else
                              np.vstack((factor, augmented)), mode='r')
        block_mean = y.mean(axis=0)
        block_centered = np.sum((y-block_mean)**2, axis=0)
        if not count:
            mean, centered = block_mean, block_centered
        else:
            difference = block_mean-mean
            centered += block_centered+difference**2*count*len(block)/(count+len(block))
            mean += difference*len(block)/(count+len(block))
        count += len(block)
    if factor is None or count < 7 or np.linalg.matrix_rank(factor[:, :6]) != 6:
        raise ValueError('Pilot half requires full dictionary rank and enough dates')
    return factor, centered/count


def _ridge(factor, penalty):
    regularizer = np.diag([0.]+[np.sqrt(penalty)]*5)
    x = np.vstack((factor[:, :6], regularizer))
    y = np.vstack((factor[:, 6:], np.zeros((6, factor.shape[1]-6))))
    return np.linalg.lstsq(x, y, rcond=None)[0]


def train_streaming_pilot(rows, penalties, chunk_size=4096):
    """Preserve first-half validation tuning and full-pilot refit via QR."""
    if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size < 1:
        raise ValueError('Positive integer chunk size required')
    if np.ndim(rows) != 2 or rows.shape[1] < 7:
        raise ValueError('Pilot history dimensions are invalid')
    if not penalties or any(not np.isfinite(p) or p < 0 for p in penalties):
        raise ValueError('Nonnegative fixed pilot penalties required')
    split = len(rows)//2
    training, scale = _factor(rows[:split], chunk_size)
    validation, _ = _factor(rows[split:], chunk_size)
    if np.any(scale <= 0) or not np.isfinite(scale).all():
        raise ValueError('Pilot training targets require positive finite variances')
    losses = []
    for penalty in penalties:
        coefficient = _ridge(training, penalty)
        residual = validation[:, 6:]-validation[:, :6]@coefficient
        losses.append(float(np.sum(residual**2/scale)/((len(rows)-split)*len(scale))))
    selected = int(np.argmin(losses))
    full = np.linalg.qr(np.vstack((training, validation)), mode='r')
    unique_losses = sorted(set(losses))
    return dict(coefficient=_ridge(full, penalties[selected]), penalty=penalties[selected],
                validation_losses=losses, training_origins=len(rows),
                validation_loss_gap=unique_losses[1]-unique_losses[0] if len(unique_losses)>1 else 0.)


def fit_streaming_pilot(pilot_rows, rows, target, successes, sizes, penalties,
                        *, chunk_size=4096, covariance='innovation_horizon', declarations=None):
    if len(pilot_rows) < 4*len(rows):
        raise ValueError('Selected growing-pilot route requires at least four pilot dates per evaluation date')
    if np.ndim(pilot_rows) != 2 or pilot_rows.shape[1] != 5+2*(target.horizon+1):
        raise ValueError('Pilot dimensions do not match the target')
    if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size < 1:
        raise ValueError('Positive integer chunk size required')
    result, audit = _prepare(rows, target, successes, sizes, (0, 1, 2), covariance, declarations)
    if audit is None:
        return result
    fit = train_streaming_pilot(pilot_rows, penalties, chunk_size)
    n = len(rows)
    qsum = np.zeros(2)
    products = np.zeros((2, rows.shape[1]-5))
    for block in _blocks(rows, chunk_size):
        data = pilot_data(block)
        prediction = data['x']@fit['coefficient']
        action = data['action']-prediction[:, 0]
        outcome = data['outcomes']-prediction[:, 1:]
        for group in (0, 1):
            keep = data['stratum'] == group
            qsum[group] += action[keep]@action[keep]
            products[group] += action[keep]@outcome[keep]
    if np.any(qsum <= 0):
        raise ValueError('Missing stratum/action variation')
    slopes = products/qsum[:, None]
    lag = target.horizon if covariance == 'innovation_horizon' else int(2*n**.2)
    accumulator = LagAccumulator(lag)
    for block in _blocks(rows, chunk_size):
        data = pilot_data(block)
        prediction = data['x']@fit['coefficient']
        action = data['action']-prediction[:, 0]
        outcome = data['outcomes']-prediction[:, 1:]
        score = np.empty(len(block))
        for group in (0, 1):
            keep = data['stratum'] == group
            residual = (outcome[keep]-action[keep, None]*slopes[group])@audit[2][group]
            score[keep] = n*action[keep]*residual/qsum[group]
        accumulator.add(score)
    result = _finish(result, slopes, accumulator.variance_of_mean(covariance == 'bartlett'),
                     target, audit, n, 'streaming_independent_pilot')
    result.update(pilot_dates=len(pilot_rows), pilot_penalty=fit['penalty'],
                  pilot_rate='M >= 4 T; fixed dictionary and stable-law coefficient rates required',
                  coefficient=fit['coefficient'].tolist(),
                  pilot_validation_losses=fit['validation_losses'],
                  pilot_validation_loss_gap=fit['validation_loss_gap'])
    result['qualifications'].append('Requires an independent invariant pilot with the stated growing information; its acquisition and fitting are additional costs.')
    return result
