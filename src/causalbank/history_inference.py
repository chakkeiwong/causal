"""Cross-fitted finite-horizon policy evaluation with monotone censoring.

History sufficiency, independent trajectories and coarsening at random are
scientific assumptions. Whole-trajectory folds prevent customer leakage.
"""
from dataclasses import dataclass
import numpy as np
from sklearn.base import clone
from sklearn.model_selection import KFold
from .causal_workflow import independent_score_result


@dataclass(frozen=True)
class HistoryQuery:
    horizon: int
    discount: float
    policy_training_id: str
    unit: str = 'customer trajectory'
    outcome_unit: str = 'synthetic currency units'
    sampling: str = 'independent_units'
    censoring: str = 'monotone_coarsening_at_random'


def evaluate_history(data, query, policies, regressor, classifier, seed=41,
                     folds=2, clip=.02, ignore_censoring=False):
    """Return trajectory scores for two frozen observable stochastic policies.

    H_t precedes A_t; D_t reveals R_t and H_(t+1). Every entry past dropout
    must be NaN. Regressions never receive such entries. Histories may be
    sufficient summaries, but the caller must justify that restriction.
    """
    if query.sampling != 'independent_units':
        raise ValueError('trajectory-iid backend requires independent units')
    if query.censoring != 'monotone_coarsening_at_random':
        raise ValueError('this score does not identify general MNAR outcomes')
    h, a, reward, observed = [data[k] for k in ['history', 'action', 'reward', 'observed']]
    n, horizon = a.shape
    if horizon != query.horizon or len(policies) != 2 or not query.policy_training_id:
        raise ValueError('two independently frozen policies and matching horizon required')
    if np.any(observed[:, 1:] > observed[:, :-1]):
        raise ValueError('censoring must be monotone')
    risk = np.column_stack((np.ones(n, bool), observed[:, :-1]))
    if not np.isfinite(h[:, 0]).all():
        raise ValueError('baseline must be observed')
    scores = np.empty((n, 2)); plugin = np.empty_like(scores)
    maximum_weights = []; clipping_counts = []
    split = list(KFold(folds, shuffle=True, random_state=seed).split(np.arange(n)))
    for train, test in split:
        action_prob = np.ones((len(test), horizon))
        censor_prob = np.ones_like(action_prob)
        clipped = 0
        for t in range(horizon):
            fitrows = train[risk[train, t]]; evalrows = test[risk[test, t]]
            pmodel = clone(classifier).fit(h[fitrows, t], a[fitrows, t])
            raw = pmodel.predict_proba(h[evalrows, t])[:, 1]
            clipped += int(np.sum((raw < clip) | (raw > 1-clip)))
            action_prob[risk[test, t], t] = np.clip(raw, clip, 1-clip)
            if not ignore_censoring:
                features = np.column_stack((h[fitrows, t], a[fitrows, t]))
                cmodel = clone(classifier).fit(features, observed[fitrows, t])
                raw = cmodel.predict_proba(np.column_stack((h[evalrows, t], a[evalrows, t])))[:, 1]
                clipped += int(np.sum(raw < clip))
                censor_prob[risk[test, t], t] = np.maximum(raw, clip)
        clipping_counts.append(clipped)
        for j, policy in enumerate(policies):
            # Prediction arrays are defined only at observed histories. The
            # terminal V is zero irrespective of the unobserved next state.
            v = np.zeros((n, horizon+1)); qa = np.zeros((n, horizon))
            for t in reversed(range(horizon)):
                fitrows = train[observed[train, t]]
                target = reward[fitrows, t] + query.discount*v[fitrows, t+1]
                evalrows = np.flatnonzero(risk[:, t])
                predictions = np.empty((len(evalrows), 2))
                for arm in [0, 1]:
                    take = a[fitrows, t] == arm
                    model = clone(regressor).fit(h[fitrows[take], t], target[take])
                    predictions[:, arm] = model.predict(h[evalrows, t])
                pi = policy(h[evalrows, t])
                if np.any((pi < 0) | (pi > 1)):
                    raise ValueError('policy probabilities outside [0,1]')
                v[evalrows, t] = predictions[:, 0]*(1-pi) + predictions[:, 1]*pi
                qa[evalrows, t] = predictions[np.arange(len(evalrows)), a[evalrows, t].astype(int)]
            score = v[test, 0].copy(); weight = np.ones(len(test))
            for t in range(horizon):
                alive = risk[test, t]; rows = test[alive]
                pi = policy(h[rows, t]); actions = a[rows, t]
                numerator = np.where(actions == 1, pi, 1-pi)
                denominator = np.where(actions == 1, action_prob[alive, t], 1-action_prob[alive, t])
                weight[alive] *= numerator / denominator / censor_prob[alive, t]
                weight[~observed[test, t]] = 0
                complete = observed[test, t]; rows = test[complete]
                score[complete] += query.discount**t * weight[complete] * (
                    reward[rows, t] + query.discount*v[rows, t+1] - qa[rows, t])
                maximum_weights.append(float(weight.max()))
            scores[test, j] = score; plugin[test, j] = v[test, 0]
    contrast = scores[:, 1]-scores[:, 0]
    return {'result': independent_score_result(contrast, query.outcome_unit),
            'plugin_contrast': float(np.mean(plugin[:, 1]-plugin[:, 0])),
            'scores': scores, 'folds': split,
            'diagnostics': {'max_cumulative_weight': max(maximum_weights),
                            'clipped_predictions': sum(clipping_counts),
                            'final_observed_fraction': float(observed[:, -1].mean())}}
