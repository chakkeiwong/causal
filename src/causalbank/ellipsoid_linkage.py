"""Global outer projection of a joint response ellipsoid and audit intervals."""
from itertools import product
import numpy as np
from scipy.stats import chi2
from .linkage_sets import binomial_interval, encode_set


def ellipsoid_projection(mean, covariance, successes, sizes, *, alpha=.05, offset=0.):
    """Coordinates: average0, half-difference0, average1, half-difference1.

    At fixed ranks the functional is linear. In reciprocal ranks its upper
    support is convex, its lower support concave: corners give global extrema.
    Rank intervals containing zero retain the whole line conservatively.
    """
    m=np.asarray(mean,float);v=np.asarray(covariance,float)
    if m.shape!=(4,) or v.shape!=(4,4) or not np.all(np.isfinite(m)) or not np.all(np.isfinite(v)):
        raise ValueError('four finite responses and their covariance required')
    if not 0<alpha<1 or not np.isfinite(offset) or not np.allclose(v,v.T,rtol=1e-10,atol=1e-12):
        raise ValueError('invalid region or nonsymmetric covariance')
    counts=np.asarray(successes);n=np.asarray(sizes)
    if counts.shape!=(2,) or n.shape!=(2,):
        raise ValueError('two audit strata required')
    # The count routine validates integrality rather than silently truncating.
    bands=[binomial_interval(k.item(),s.item(),alpha/4) for k,s in zip(counts,n)]
    eigen=np.linalg.eigvalsh(v)
    if eigen.min() < -1e-10*max(1.,eigen.max()):
        raise ValueError('response covariance not positive semidefinite')
    reason=None
    if eigen.min()<=1e-12*max(1.,eigen.max()):
        reason='response rank not qualified for the fixed four-dimensional chi-square limit'
    elif any(lo<=.5<=hi for lo,hi in bands):
        reason='audit rank interval contains zero; conservative whole-line enclosure'
    if reason:
        return {'status':'computed_set','financial_set':[{'lower':None,'upper':None}],
                'numerical_status':'conservative_outer_fallback','reason':reason,'audit_intervals':bands}
    reciprocal=[sorted([1/(2*lo-1),1/(2*hi-1)]) for lo,hi in bands]
    critical=float(chi2.ppf(1-alpha/2,4))
    bounds=[]
    for r0,r1 in product(*reciprocal):
        c=np.array([.5,.5*r0,.5,.5*r1])
        mid=float(c@m+offset);width=float(np.sqrt(critical*(c@v@c)))
        bounds.append((mid-width,mid+width))
    # Outward rounding at representable endpoints; not an interval-arithmetic
    # certificate for chi-square or beta special functions.
    lo=np.nextafter(min(b[0] for b in bounds),-np.inf)
    hi=np.nextafter(max(b[1] for b in bounds),np.inf)
    return {'status':'computed_set','financial_set':encode_set([(lo,hi)]),
            'numerical_status':'global_analytic_corner_extrema_with_floating_point_evaluation',
            'audit_intervals':bands,'critical_chi_square':critical,'corners':bounds,
            'coverage_claim':'outer asymptotic response ellipsoid plus exact marginal audit regions; prespecified union bound'}
