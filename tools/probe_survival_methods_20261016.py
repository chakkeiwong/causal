#!/usr/bin/env python3
"""Actual unsupported-method probes; no commercial engine is invoked."""
import json
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'tests')]
from causalbank.operation_service_v12 import OperationService
from test_operation_service_v12 import context,request
from publish_latent_r_review_v2_20261013 import ref,write

BASE=ROOT/'docs/program/execution/2026-10-16/commercial-survival'

def main():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='causal-survival-probe-',dir=ROOT/'.runtime') as tmp:
        service=OperationService(Path(tmp))
        for method in ['fixed-treatment-survival','competing-risk-incidence','sequential-policy-survival']:
            q=request('estimate.effect',{'engine_id':'proposal-survival-profile','estimator_id':method},ctx=context())
            response=service.invoke(q)
            assert (response['status'],response['disposition'],response['result'])==('completed','unsupported',None)
            rows.append({'profile':method,'request':q,'response':response})
    write(BASE/'survival-method-probes.json',{'mode':'actual local execution on authored method-dispatch fixtures',
      'profiles':rows,'claim':'These supplied method identifiers are unsupported;source inspection confirms only supplied-moment residual inversion is implemented by _estimate.',
      'scope':'Generic method dispatch,not a fully encoded survival design,licensed package run or product qualification.',
      'evidence':[ref(ROOT/'src/causalbank/operation_service_v12.py','SUPPORTED and _estimate method-pair guard'),
        ref(ROOT/'docs/program/repair-v12/work/IN02/request-schema.json','estimate.effect parameters accept engine_id and estimator_id strings'),
        ref(Path(__file__),'Bounded method-dispatch probe')]})
    print(json.dumps({'actual_profiles':len(rows),'all_dispositions':'unsupported','vendor_runtime':False}))

if __name__=='__main__':main()
