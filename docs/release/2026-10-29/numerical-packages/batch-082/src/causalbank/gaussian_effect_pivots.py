"""Prespecified exact Gaussian pivots for finite ordered information classes."""
import numpy as np
from scipy.stats import t
from .linkage_sets import encode_set
from .latent_temporal_sets import graph_class


def quadratic_sublevel(a,b,c):
    a,b,c=map(np.longdouble,(a,b,c))
    if not np.all(np.isfinite([a,b,c])):
        raise ValueError('finite quadratic coefficients required')
    if a==0:
        if b==0:return [(-np.inf,np.inf)] if c<=0 else []
        root=float(-c/b)
        return [(-np.inf,np.nextafter(root,np.inf))] if b>0 else [(np.nextafter(root,-np.inf),np.inf)]
    disc=b*b-4*a*c
    if disc<0:return [] if a>0 else [(-np.inf,np.inf)]
    if disc==0:
        if a<0:return [(-np.inf,np.inf)]
        root=float(-b/(2*a));return [(np.nextafter(root,-np.inf),np.nextafter(root,np.inf))]
    q=-.5*(b+np.copysign(np.sqrt(disc),b))
    low,high=sorted([float(q/a),float(c/q)])
    if a>0:return [(np.nextafter(low,-np.inf),np.nextafter(high,np.inf))]
    return [(-np.inf,np.nextafter(low,np.inf)),(np.nextafter(high,-np.inf),np.inf)]


def effect_confidence(data,*,information,alpha=.05,sampling='independent_gaussian_episodes'):
    x=np.asarray(data,float)
    if x.ndim!=2 or x.shape[1]!=3 or len(x)<8 or not np.all(np.isfinite(x)) or not 0<alpha<1:
        raise ValueError('finite Gaussian Z,A,Y episodes and confidence level required')
    if sampling!='independent_gaussian_episodes':
        raise ValueError('dependent histories need a different pivot')
    graphs=graph_class(information);n=len(x);details={}
    if information=='observational_latent':
        pieces=[(-np.inf,np.inf)];method='unrestricted_latent_equivalence_witness'
    elif information=='observed_sufficiency':
        design=np.column_stack([np.ones(n),x[:,:2]])
        if np.linalg.matrix_rank(design)<3:
            return dict(status='unqualified_design',reason='regression design lacks numeric rank')
        coef=np.linalg.lstsq(design,x[:,2],rcond=None)[0];res=x[:,2]-design@coef
        q,r=np.linalg.qr(design,mode='reduced');inverse=np.linalg.solve(r,np.eye(3))
        se=float(np.sqrt((res@res)/(n-3)*(inverse@inverse.T)[2,2]))
        half=float(t.ppf(1-alpha/2,n-3)*se);point=float(coef[2])
        pieces=[(point-half,point+half)];method='conditional_gaussian_partial_regression_t'
        details=dict(estimate=point,standard_error=se,degrees_of_freedom=n-3)
    else:
        z,a,y=(x-x.mean(axis=0)).T;k=float(z@z)
        if k<=1e-12:
            return dict(status='unqualified_design',reason='encouragement has no numeric variation')
        sa=float(z@a/k);sy=float(z@y/k);ea=a-sa*z;ey=y-sy*z
        critical=float(t.ppf(1-alpha/2,n-2)**2/((n-2)*k))
        coefficients=[sa*sa-critical*float(ea@ea),
                      -2*sa*sy+2*critical*float(ea@ey),
                      sy*sy-critical*float(ey@ey)]
        pieces=quadratic_sublevel(*coefficients);method='gaussian_reduced_form_test_inversion'
        details=dict(quadratic_coefficients=coefficients,first_stage_slope=sa,degrees_of_freedom=n-2)
    return dict(status='computed_set',effect_set=encode_set(pieces),enumerated_graphs=len(graphs),
                information=information,details=details,
                inference=dict(method=method,confidence_level=1-alpha,
                    coverage_claim='finite-sample Gaussian true-null pivot under supplied class; no selected-graph inference',
                    sampling_unit='independent ordered Z,A,Y episode',
                    information='observed sufficiency or valid encouragement/exclusion is supplied scientific information',
                    numerical_status='analytic regression/quadratic inversion with outward endpoint rounding; no full floating-point certificate',
                    empirical_qualification='finite model-class operation; general PAG confidence and dependent histories excluded'))
