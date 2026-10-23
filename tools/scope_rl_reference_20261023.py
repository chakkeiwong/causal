#!/usr/bin/env python3
"""Independent rational witnesses; never imports or executes acquired software."""
from fractions import Fraction as F
from itertools import product
import ast, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def derive():
    gamma=F(1,2); rows=[]
    for a0,a1 in product([0,1],repeat=2):
        ratios=[F(3,2) if a else F(1,2) for a in [a0,a1]]
        rewards=[F(2*a0),F(4+4*a1)]; w0=ratios[0];w1=w0*ratios[1]
        rows.append(dict(actions=[a0,a1],rewards=rewards,tis=w1*(rewards[0]+gamma*rewards[1]),pdis=w0*rewards[0]+gamma*w1*rewards[1],target_probability=(F(3,4) if a0 else F(1,4))*(F(3,4) if a1 else F(1,4))))
    target=sum(x['target_probability']*(x['rewards'][0]+gamma*x['rewards'][1]) for x in rows)
    assert target==sum(x['tis'] for x in rows)/4==sum(x['pdis'] for x in rows)/4==5
    selected=[x for x in rows if x['actions'] in [[1,0],[0,1]]]
    assert sum(x['tis'] for x in selected)/2==3 and sum(x['pdis'] for x in selected)/2==F(15,4)
    weights=[F(1),F(3)];returns=[F(0),F(4)];scores=[w*r/(sum(weights)/2) for w,r in zip(weights,returns)]
    fixed=[];refitted=[]
    for pair in product(range(2),repeat=2):
        fixed.append(sum(scores[i] for i in pair)/2)
        refitted.append(sum(weights[i]*returns[i] for i in pair)/sum(weights[i] for i in pair))
    variance=lambda xs:sum((x-sum(xs)/len(xs))**2 for x in xs)/len(xs)
    assert fixed==[0,3,3,6] and refitted==[0,3,3,4]
    assert variance(fixed)==F(9,2) and variance(refitted)==F(9,4)
    alpha=F(1,20);family_error=1-(1-alpha)**20
    miss=(F(99,100))**20
    assert miss>F(4,5)
    src=(ROOT/'docs/literature/raw/exec23_scope_06.txt').read_text();tree=ast.parse(src)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='estimate_confidence_interval_by_hoeffding')
    ci=next(n.value for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ci' for t in n.targets))
    radicand=ci.right.args[0]
    assert isinstance(radicand,ast.BinOp) and isinstance(radicand.op,ast.Mult)
    assert isinstance(radicand.left,ast.BinOp) and isinstance(radicand.left.op,ast.Div)
    return dict(native_execution=False,target=target,enumerated_rows=rows,selected_sample=dict(tis=F(3),pdis=F(15,4)),
        terminal_reward=dict(rewards=[2,8],done=[0,1],same_row_mask_return=2,retain_terminal_return=10,stipulated_cost=6,masked_net=-4,retained_net=4),
        self_normalized_bootstrap=dict(frozen_scores=fixed,recomputed_ratio=refitted,frozen_variance=variance(fixed),recomputed_variance=variance(refitted)),
        interval_contract=dict(hoeffding_source_ast=ast.unparse(ci),source_to_denominator_n_radius_ratio=20,negative_constant_reverses_bounds=True,
            all_zero_sample_probability=miss,positive_true_mean=F(1,100),student_quantile=F(19,20),symmetric_normal_t_coverage=F(9,10),
            independent_twenty_comparison_error=family_error),
        lower_tail_pairing=dict(input_order=['A','B'],sample_returns={'A':[-10,-10,40,40],'B':[4,4,4,4]},means=[15,4],lower_quartiles=[-10,4],source_name_order=['A','B'],sorted_values=[4,-10],correct_name_order=['B','A']))
def serial(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,list):return [serial(v) for v in value]
    return value
def calculate():return serial(derive())
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
