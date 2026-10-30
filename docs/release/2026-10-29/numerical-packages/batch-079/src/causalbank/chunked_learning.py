"""Fixed nonlinear dictionary, separated blocks and chunked multi-target QR."""
import hashlib
import json
from dataclasses import asdict
import numpy as np
from .blocked_learning import blocked_covariance


def dictionary(c):
    return np.column_stack([np.ones(len(c)),c,c[:,0]*c[:,1]])


def fit_chunked(request,controls,targets,*,chunk_rows=128,algorithm='chunked_qr'):
    c=np.asanyarray(controls);y=np.asanyarray(targets);n=len(c);request.validate(n)
    if request.learner!='fixed_basis' or algorithm not in ('chunked_qr','dense_svd'):
        raise ValueError('only the prespecified fixed nonlinear dictionary is supported')
    if c.ndim!=2 or c.shape[1]<2 or y.shape!=(n,3) or n<100 or not isinstance(chunk_rows,int) or chunk_rows<4:
        raise ValueError('aligned controls and three nuisance targets, at least two controls, valid chunks required')
    identity=hashlib.sha256(json.dumps(asdict(request),sort_keys=True).encode())
    for arr in (c,y):
        for start in range(0,n,chunk_rows):
            part=np.asarray(arr[start:start+chunk_rows],float)
            if not np.all(np.isfinite(part)) or np.max(abs(part))>request.outcome_envelope:
                raise ValueError('finite bounded-law inputs required')
            identity.update(part.tobytes())
    middle=n//2;left=middle-request.gap//2;right=left+request.gap
    spans=[(0,left),(right,n)];residuals=[];folds=[];tuning=[]
    for fold,(ev0,ev1) in enumerate(spans):
        tr0,tr1=spans[1-fold];p=c.shape[1]+2
        if algorithm=='dense_svd':
            # Independent SVD algebra; intentionally materializes its design.
            coef,res,rank,singular=np.linalg.lstsq(dictionary(c[tr0:tr1]),y[tr0:tr1],rcond=None)
            if rank<p:raise ValueError('dictionary fitting design lacks numerical rank')
        else:
            reduced=None
            for start in range(tr0,tr1,chunk_rows):
                end=min(start+chunk_rows,tr1);aug=np.column_stack([dictionary(c[start:end]),y[start:end]])
                stack=aug if reduced is None else np.vstack([reduced,aug])
                reduced=np.linalg.qr(stack,mode='r')
            coef,res,rank,singular=np.linalg.lstsq(reduced[:p,:p],reduced[:p,p:],rcond=None)
            if rank<p:raise ValueError('dictionary fitting design lacks numerical rank')
        held=np.empty((ev1-ev0,3))
        for start in range(ev0,ev1,chunk_rows):
            end=min(start+chunk_rows,ev1);pred=dictionary(c[start:end])@coef
            held[start-ev0:end-ev0]=y[start:end]-np.clip(pred,-request.outcome_envelope,request.outcome_envelope)
        residuals.append(held);folds.extend([fold]*len(held))
        tuning.append(dict(training_origins=[tr0,tr1-1],evaluation_origins=[ev0,ev1-1],coefficients=coef))
    residuals=np.vstack(residuals);folds=np.asarray(folds);nret=len(residuals)
    denominator=float(np.mean(residuals[:,2]*residuals[:,1]))
    if abs(denominator)<1e-8:raise ValueError('weak numeric IV slope; no weak-IV guarantee')
    estimate=float(np.mean(residuals[:,2]*residuals[:,0])/denominator)
    scores=residuals[:,2]*(residuals[:,0]-estimate*residuals[:,1]);bandwidth=int(nret**.2)
    variance=blocked_covariance(scores,folds,bandwidth)/(nret*denominator**2)
    if not np.isfinite(variance) or variance<=0:raise ValueError('nonpositive fitted-score variance')
    se=float(np.sqrt(variance))
    return dict(status='computed',estimate=estimate,standard_error=se,interval=[estimate-1.96*se,estimate+1.96*se],
                identity=identity.hexdigest(),denominator=denominator,bandwidth=bandwidth,scores=scores,folds=folds,tuning=tuning,
                inference=dict(method='separated_block_fixed_nonlinear_dictionary_IV',confidence_level=.95,
                               sampling_unit='whole declared calendar origin; separated evaluation blocks',
                               coverage_claim='conditional asymptotic: bounded geometric mixing; fixed correctly specified dictionary; positive Gram and IV slope; growing gap and covariance-rate conditions',
                               dictionary='1,X,X0*X1',numerical_status='QR reduction or independent dense SVD; O(n) retained scores; no expanded full design in chunked route',
                               empirical_qualification='selected nonlinear dictionary; no arbitrary learner or arbitrary out-of-core fitting claim'))
