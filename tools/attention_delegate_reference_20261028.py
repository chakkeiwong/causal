"""Independent temporal support and threshold fixtures; no package imports."""
from fractions import Fraction


def supports(kernel, dilation, levels):
    offsets={0}
    for layer in range(levels):
        offsets={old+q*dilation**layer for old in offsets for q in range(kernel)}
    return sorted(offsets)


def f1(truth, predicted):
    tp=sum(a==b==1 for a,b in zip(truth,predicted))
    fp=sum(a==0 and b==1 for a,b in zip(truth,predicted))
    fn=sum(a==1 and b==0 for a,b in zip(truth,predicted))
    return Fraction(2*tp,2*tp+fp+fn) if 2*tp+fp+fn else None


def calculate():
    offsets=supports(2,2,3);assert offsets==list(range(8))
    target_offsets=[i+1 for i in offsets];assert target_offsets==list(range(1,9))
    seq=[10,20,30];assert seq[:-0]==[]
    scores=[Fraction(4,5),Fraction(1,5)];truth=[1,0];threshold=Fraction(4,5)
    inclusive=[int(s>=threshold) for s in scores]
    strict=[int(s>threshold) for s in scores]
    assert f1(truth,inclusive)==1 and f1(truth,strict)==0
    return dict(status='pass',kind='authored finite fixture expectations',
        temporal=dict(kernel=2,dilation_base=2,levels=3,non_target_lags=offsets,
                      shifted_target_lags=target_offsets,receptive_field_upper_bound=1+(2-1)*sum(2**i for i in range(3)),
                      zero_chomp_python_slice=seq[:-0],scope='Index support of the displayed stride1,pad-and-chop construction; no learned attribution or native torch result.'),
        threshold=dict(scores=[str(x) for x in scores],truth=truth,threshold=str(threshold),
                       inclusive_matrix=inclusive,strict_matrix=strict,inclusive_f1=str(f1(truth,inclusive)),strict_f1=str(f1(truth,strict)),
                       scope='Comparator consistency witness; installed precision-recall implementation/version must be bound before native mismatch is asserted.'),
        empty_score=dict(requested=3,valid=0,required_result='unavailable',numeric_loss=None),native_execution=False)


if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
