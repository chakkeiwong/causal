#!/usr/bin/env python3
"""E01 dense/streamed equivalence, contracts and local recovery."""
import json,sys,tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0,'src')
from causalbank.dynamic_funding import FundingTarget
from causalbank.linked_funding import simulate_linked,fit_linked_funding,LINKED_DECLARATIONS
from causalbank.engineering_v11 import fit_linked_stream,validate_result,recovery_trial
ROOT=Path(__file__).resolve().parents[1]
def main():
 base=json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text());obs=json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text());target=FundingTarget(horizon=base['horizon'],branches=base['branches']); law=base;ob=dict(obs,correct_pair_probability=[.55,.515]);pilot,pa=simulate_linked(law,ob,960,[801,1],[801,2],inclusion=.25);rows,a=simulate_linked(law,ob,240,[801,3],[801,4],inclusion=.25)
 dense=fit_linked_funding(pilot,rows,target,pa,a,base['penalties'],declarations=LINKED_DECLARATIONS);stream=fit_linked_stream(pilot,rows,target,pa,a,base['penalties'],chunk_size=37)
 assert dense['status']==stream['status']=='computed_set' and abs(dense['estimate']-stream['estimate'])<1e-6 and abs(dense['standard_error']-stream['standard_error'])<1e-6
 journeys=[]
 for name,topology,disposition in [('A','finite_interval','conditional_progress'),('B','finite_union','unresolved'),('C','whole_line','unresolved'),('D','unavailable','external_pending')]: journeys.append(dict(status='computed' if topology!='unavailable' else 'unavailable',set_topology=topology,assumptions=['declared synthetic or external information'],currency='USD',capability_disposition=disposition,estimate=None,interval=None))
 for r in journeys:validate_result(r)
 with tempfile.TemporaryDirectory(prefix='causal-e01-') as td: recovery=recovery_trial(td)
 assert recovery['complete'] and recovery['duplicates']==0 and recovery['fault_injected']
 out={'status':'pass','dense_streamed_estimate_difference':dense['estimate']-stream['estimate'],'dense_streamed_se_difference':dense['standard_error']-stream['standard_error'],'stream_peak_pseudo_rows':stream['peak_pseudo_rows'],'journey_contracts':journeys,'recovery':recovery,'scope':'Local single-process selected linked-outcome law; no multi-host, bank platform or scientific calibration qualification.'}
 (ROOT/'docs/program/master/work/E01/checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
