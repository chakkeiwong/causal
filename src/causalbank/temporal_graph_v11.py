"""Finite stationary temporal Gaussian graph class with honest outer sets."""
import itertools
import numpy as np
from .latent_temporal_sets import effect_set
from .linkage_sets import decode_set, encode_set


def simulate(graph, episodes, horizon, seed, *, selection=False, weak=False):
    rng = np.random.default_rng(seed); z = np.zeros((episodes, horizon)); a = np.zeros_like(z); y = np.zeros_like(z); u = np.zeros_like(z)
    phi = graph.get('phi', .55); rho_u = graph.get('rho_u', .45)
    for t in range(horizon):
        u[:, t] = (rho_u*u[:, t-1] if t else 0.) + rng.normal(size=episodes)
        z[:, t] = rng.normal(size=episodes)
        z_effect = graph.get('z_to_a', .7)
        a[:, t] = z_effect*z[:, t] + graph.get('a_lag', .2)*(a[:, t-1] if t else 0.) + graph.get('u_to_a', .55)*u[:, t] + rng.normal(size=episodes)
        if selection:
            a[:, t] += .5*(u[:, t] > 0)
        y[:, t] = graph.get('tau', .8)*a[:, t] + graph.get('z_to_y', .0)*z[:, t] + graph.get('y_lag', phi)*(y[:, t-1] if t else 0.) + graph.get('u_to_y', .5)*u[:, t] + rng.normal(size=episodes)
        if weak:
            z[:, t] *= .08
    return np.stack((z, a, y), axis=-1)


def residual_window(data):
    data = np.asarray(data, float)
    n, h, _ = data.shape
    if n < 8 or h < 2 or not np.isfinite(data).all(): raise ValueError('finite temporal episodes required')
    current, lagged = data[:, 1:], data[:, :-1]
    design = np.column_stack((np.ones(len(lagged.reshape(-1, 3))), lagged.reshape(-1, 3)))
    out = []
    for j in range(3):
        coef = np.linalg.lstsq(design, current[:, :, j].reshape(-1), rcond=None)[0]
        out.append(current[:, :, j].reshape(-1)-design@coef)
    return np.column_stack(out)


def exact_class(graph):
    """Exact contemporaneous intervention effect for this structural member."""
    return float(graph.get('tau', .8))


def class_rows():
    rows=[]
    for latent, direct_z, lag in itertools.product((0,1), repeat=3):
        rows.append(dict(latent=latent, direct_z=direct_z, lag=lag,
                         description='latent confounder' if latent else 'observed disturbance'))
    return rows


def infer(data, information='observational_latent', alpha=.05):
    residual = residual_window(data)
    out = effect_set(residual, information=information, alpha=alpha)
    pieces = decode_set(out['effect_set'])
    retained = class_rows() if information == 'observational_latent' else [r for r in class_rows() if not r['latent']]
    return dict(status='computed_set', effect_set=out['effect_set'], components=pieces,
                retained_graphs=len(retained), graph_class=retained,
                temporal_residual_rows=len(residual), inference=out['inference'],
                exact_oracle_scope='The finite structural member used by the fixture; arbitrary latent temporal graphs are excluded.')
