#!/usr/bin/env python3
"""Authored panel covariance counterexamples, not downloaded package runs."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/panel-followups-v1'
def calculate():
    # Scalar score contributions in a two-by-two entity/time panel.
    scores=[F(1),F(-1),F(-1),F(1)]
    entity=[0,0,1,1];time=[0,1,0,1];intersection=list(zip(entity,time))
    def meat(groups):
        return sum(sum(s for s,g in zip(scores,groups) if g==key)**2 for key in set(groups))/len(scores)
    e,t,i=map(meat,[entity,time,intersection]);assert(e,t,i)==(0,0,1)
    assert e+t-i==-1
    # Calendar times are deliberately irregular; this is a contrast of laws.
    cal=[1,2,10];z=[F(1),F(1),F(-2)];w1=F(1,2)
    diagonal=sum(x*x for x in z)
    ordinal=(diagonal+2*w1*sum(a*b for a,b in zip(z[1:],z[:-1])))/len(z)
    calendar=(diagonal+2*w1*sum(z[a]*z[b] for a in range(len(z)) for b in range(a) if cal[a]-cal[b]==1))/len(z)
    assert ordinal==F(5,3) and calendar==F(7,3)
    return dict(provenance='Independent exact algebra; not package execution or a sampling guarantee',two_way=dict(scores=list(map(str,scores)),entity_groups=entity,time_groups=time,component_meats=list(map(str,[e,t,i])),combined_meat=str(e+t-i),interpretation='Finite inclusion-exclusion covariance may be indefinite; symmetrization alone does not make it positive semidefinite. This score pattern is not claimed as a fitted PanelOLS dataset.'),calendar=dict(times=cal,scores=list(map(str,z)),lag_one_weight=str(w1),ordinal_kernel_meat=str(ordinal),calendar_distance_meat=str(calendar),interpretation='Equal observed-period lags and elapsed-calendar lags define different estimands for covariance; no claim that either is universally correct.'),native_execution=False)

if __name__=='__main__':
    out=BASE/'exact-panel-witnesses.json'
    if out.exists():
        assert json.loads(out.read_text())==calculate()
    else:
        out.write_text(json.dumps(calculate(),indent=2)+chr(10))
    specs={
      'exec24_lmpanel_src_00.txt':[(1791,1819,'One-effect nested-cluster adjustment differs from multiple effects'),(1909,2022,'Weighted/unweighted and sparse/dummy routes; absorbed regressors and covariance inputs')],
      'exec24_lmpanel_src_01.txt':[(307,339,'Two-way inclusion-exclusion and separate group corrections; return symmetrized without local PSD projection'),(430,453,'Scores grouped by time code and sorted before ordinal kernel lags')],
      'exec24_lmpanel_src_03.txt':[(364,397,'Entity/time index codes, missing index refusal'),(437,536,'Iterated weighted demeaning; local while loop has tolerance but no explicit iteration cap')],
      'exec24_lmpanel_src_04.txt':[(16,42,'Group debiasing g/(g-1)*(n-1)/n; singleton group needs qualification'),(45,105,'Intersection labels and cluster score sums'),(108,139,'Kernel covariance pairs rows by ordinal lag')],
    }
    records=[]
    for name,anchors in specs.items():
        p=ROOT/'docs/literature/raw'/name;data=p.read_bytes();lines=data.decode().splitlines();inspected=[]
        for lo,hi,f in anchors:
            assert 1<=lo<=hi<=len(lines),(name,hi,len(lines))
            inspected.append(dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest()))
        records.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest(),anchors=inspected))
    checkpoint=dict(status='primary_inspection_and_authored_witnesses_not_native_qualification',records=records,exact_witnesses=dict(path=str(out.relative_to(ROOT)),sha256=hashlib.sha256(out.read_bytes()).hexdigest()),preserved_predecessor='linearmodels-inspection-checkpoint.json',findings=['Fixed effects do not select robust/clustered inference by default.','Current PanelData time IDs and kernel scores use sorted observed-category positions, not elapsed calendar distances.','Covariance inclusion-exclusion can be indefinite in finite exact score examples.','Weighted/general demeaning and absorbed-regressor state changes need explicit adapter contracts.'],next_action='Complete version/license/solver/result-distribution review; inspect missing lower-level covariance and finite-sample output delegates; construct fitted public FE,cluster and irregular-calendar fixtures before any successor coverage claim.',native_execution=False,source_cutoff='2026-10-07')
    (BASE/'linearmodels-inspection-checkpoint-v2.json').write_text(json.dumps(checkpoint,indent=2)+chr(10))
    print(json.dumps(calculate()))
