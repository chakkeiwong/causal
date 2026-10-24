#!/usr/bin/env python3
"""Independent finite panel algebra; no downloaded package execution."""
from fractions import Fraction as F
import json

def calculate():
    d=[[F(0),F(1),F(1)],[F(0),F(0),F(1)]]
    y=[[F(0),F(1),F(4)],[F(0),F(0),F(1)]]
    mean=lambda x:sum(x)/len(x)
    row=[mean(x) for x in d];col=[mean([d[i][j] for i in range(2)]) for j in range(3)];grand=mean(sum(d,[]))
    residual=[[d[i][j]-row[i]-col[j]+grand for j in range(3)] for i in range(2)]
    beta=sum(residual[i][j]*y[i][j] for i in range(2) for j in range(3))/sum(v*v for v in sum(residual,[]))
    assert beta==F(-1,2) and mean([y[0][1],y[0][2],y[1][2]])==2
    panel=[('A',1,F(1)),('A',2,F(2)),('B',1,F(3))]
    onepass=[v-mean([x for ii,_,x in panel if ii==i])-mean([x for _,tt,x in panel if tt==t])+mean([x for _,_,x in panel]) for i,t,v in panel]
    time_sums={str(t):sum(v for (_,tt,_),v in zip(panel,onepass) if tt==t) for t in [1,2]}
    assert onepass==[F(-1,2),F(1,2),F(0)] and any(v!=0 for v in time_sums.values())
    actual=['Z','GZ','X1Z','X2Z','GX1Z','GX2Z'];labels=['Z','GZ','X1Z','GX1Z','X2Z','GX2Z']
    mismatches=[dict(position=i+1,actual=a,label=b) for i,(a,b) in enumerate(zip(actual,labels)) if a!=b]
    assert [x['position'] for x in mismatches]==[4,5]
    return dict(kind='exact_authored_witnesses',twfe=dict(treatment=[[int(v) for v in x] for x in d],outcome=[[int(v) for v in x] for x in y],coefficient=str(beta),treated_cell_average='2',all_treated_effects_positive=True,late_cohort_clean_control_at_last_period=False),unbalanced_demeaning=dict(onepass=[str(x) for x in onepass],time_sums={k:str(v) for k,v in time_sums.items()},orthogonal_to_time_effects=False),factorial_label_order=dict(actual=actual,labels=labels,mismatches=mismatches),aggregation=dict(effects=['1','4'],cohort_weights=['1/2','1/2'],cohort_mean=str(F(5,2)),observation_weights=['3/4','1/4'],observation_mean=str(F(7,4))),anticipation=dict(cohort=3,delta=1,baseline=1,control_cohort=4,target_time=3,eligible=False),reversal=dict(observed=[0,1,0],first_on=2,absorbing_reconstruction=[0,1,1],information_preserved=False),cost=dict(currency='USD',measured=False,total=9600,attempts=240,completions=160,admissible=80,per_attempt='40',per_completion='60',per_admissible='120'),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
