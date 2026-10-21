"""Exact evaluation-accounting witnesses, not model or benchmark replication."""
from fractions import Fraction as F
import json

def calculate():
    counts=[[88,536,532,1072],[123,430,548,1008],[152,524,534,1032],[119,562,576,1084]]
    assert sum(map(sum,counts))==8920
    totals=[sum(row[j] for row in counts) for j in range(4)]
    assert totals==[482,2052,2190,4196]
    a,b=F(8227,10000),F(5946,10000)
    lo=max(F(0),a-b);hi=min(a,1-b)
    tables=[]
    for p10 in [lo,hi]:
        p11=a-p10;p01=b-p11;p00=1-p11-p10-p01
        assert min(p11,p10,p01,p00)>=0
        tables.append(dict(both=str(p11),a_only=str(p10),b_only=str(p01),neither=str(p00)))
    ga,gb=F(7168,10000),F(7680,10000)
    assert ga-gb==F(-512,10000) and min(ga,1-gb)==F(232,1000)
    margin=lambda p:10*p-30*(1-p)-1
    assert margin(F(9,10))==5 and margin(F(45,100))==-13 and margin(F(95,100))==7
    return dict(paper_counts=dict(generated=43200,selected=10800,retained=8920,removed=1880,
            retained_fraction=str(F(8920,10800)),by_task=totals,by_cell=counts),
        matched_illustration=dict(a=str(a),b=str(b),accuracy_difference=str(a-b),
            a_correct_b_wrong_bounds=[str(lo),str(hi)],joint_tables=tables,
            negative_difference=str(ga-gb),negative_difference_error_bounds=['0',str(min(ga,1-gb))]),
        selection=dict(all_requests=100,retained=50,retained_correct=45,retained_accuracy='9/10',
            full_accuracy_bounds=['9/20','19/20'],benefit=10,error_loss=30,fee=1,
            selected_margin='5',full_margin_bounds=['-13','7']),
        limits=['Marginal error bounds require a shared paired evaluation population; paper task totals differ, so these are authored matched-design illustrations, not empirical bounds on its models.',
            'Paper count arithmetic checks printed entries only, not raw data, annotation or model execution.',
            'Selection law and monetary values are hypothetical; no measured bank return.',
            'Neither benchmark accuracy nor annotation agreement establishes causal identification.'])

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
