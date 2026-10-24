#!/usr/bin/env python3
"""Independent finite framework-contract witnesses; no external code executes."""
from fractions import Fraction as F
import json

def calculate():
    # Scientific qualification is a separate status from a returned message.
    submitted,returned,qualified=1000,800,600
    conditional=F(qualified,returned);all_request=F(qualified,submitted)
    assert conditional==F(3,4) and all_request==F(3,5)
    # A hypothetical accepted side effect is repeated after a lost acknowledgement.
    intent_value=500;unkeyed=sum([intent_value]*3);keyed=intent_value
    assert unkeyed-keyed==1000
    # Check-then-act is not atomic reservation.
    budget=100;reservations=[70,70];assert all(x<=budget for x in reservations)
    overspend=sum(reservations)-budget;assert overspend==40
    # Recorded active time can exclude offline time.
    active=[20,20];downtime=3600;active_elapsed=sum(active);wall_elapsed=active_elapsed+downtime
    assert active_elapsed==40 and wall_elapsed==3640
    # A projection to a midpoint cannot recover an uncertainty set.
    sets=[[-1,1],[-2,2]];midpoints=[F(sum(x),len(x)) for x in sets]
    assert midpoints==[F(0),F(0)] and sets[0]!=sets[1]
    # Same request index, separate future identities: a per-future retry set
    # does not by itself implement a per-request count. This is an abstract
    # bookkeeping witness, not a native scheduler trace or liveness claim.
    submitted_futures=[('f0',0),('f1',0),('f2',0)]
    retried_future_ids={'f0','f1'}
    assert len({i for _,i in submitted_futures})==1 and len(retried_future_ids)==2
    costs=[F(24000,n) for n in [submitted,returned,qualified]]
    assert costs==[F(24),F(30),F(40)]
    return json.loads(json.dumps(dict(kind='authored_exact_contract_witnesses',submitted=submitted,returned=returned,qualified=qualified,conditional_rate=conditional,all_request_rate=all_request,unkeyed_total=unkeyed,keyed_total=keyed,overspend=overspend,active_seconds=active_elapsed,wall_seconds=wall_elapsed,uncertainty_sets=sets,midpoints=midpoints,future_identity_example=submitted_futures,costs_usd=costs,native_execution=False),default=lambda x:str(x) if isinstance(x,F) else x))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
