#!/usr/bin/env python3
"""Exact hypothetical cold-recovery dependency law, not observed availability."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-17/s8/availability-extension'


def calculate():
    p,q=F(1,10),F(1,50)
    return dict(node_failure=str(p),common_validation_failure=str(q),
        success={str(m):str((1-q)*(1-p**m)) for m in (1,2,3)},
        ceiling=str(1-q),target=str(F(99,100)),target_feasible=False,
        omitted_common_dependency={str(m):str(1-p**m) for m in (1,2,3)},
        limitations=['Stipulated simultaneous cold-recovery window, shared validation gate and independent node readiness.',
                    'Not an assertion that loss of a license-server connection kills an already loaded engine.',
                    'No vendor runtime, entitlement, price or empirical availability is established.'])


def separate(value):
    totals={}
    for m in (1,2,3):
        total=F(0)
        for common,*nodes in product((0,1),repeat=m+1):
            mass=F(49,50) if common else F(1,50)
            for node in nodes:mass*=F(9,10) if node else F(1,10)
            if common and any(nodes):total+=mass
        totals[str(m)]=str(total)
    assert totals==value['success']=={'1':'441/500','2':'4851/5000','3':'48951/50000'}
    assert F(value['ceiling'])<F(value['target'])
    return dict(status='pass',scope='Same-author finite joint-event enumeration independent of complement formula',
                findings=['Readiness probabilities0.882,0.9702,0.97902 retain the common dependency.',
                          'No replica count can reach0.99 under common unavailability0.02.'])


if __name__=='__main__':
    r=calculate();print(json.dumps(dict(result=r,review=separate(r)),indent=2))
