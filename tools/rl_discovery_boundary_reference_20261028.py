"""Independent finite witnesses; imports no reviewed discovery implementation."""
from fractions import Fraction
from itertools import product,permutations

def calculate():
    graphs=[]
    for ab,ba in product([0,1],repeat=2):
        cyclic=bool(ab and ba);score=0 if cyclic else 1
        graphs.append(dict(edges=[ab,ba],cyclic=cyclic,score=score,penalty_equal=score+int(cyclic),penalty_strict=str(Fraction(score)+Fraction(3,2)*int(cyclic))))
    assert {g['penalty_equal'] for g in graphs}=={1}
    assert min(Fraction(g['penalty_strict']) for g in graphs if g['cyclic'])>min(Fraction(g['penalty_strict']) for g in graphs if not g['cyclic'])
    kwargs={'dag_mask':[[0,0],[0,0]]}
    assert getattr(kwargs,'dag_mask',None) is None and kwargs.get('dag_mask')==[[0,0],[0,0]]
    orders=list(permutations(range(3)))
    return dict(scope='Authored exact witnesses,not native package execution',graphs=graphs,score_lower_bound=0,dag_optimum_upper_bound=1,lambda1_equal=1,lambda2=0,equality_condition_satisfied=True,cyclic_minimizer_at_equality=True,strict_lambda1='3/2',strict_condition_excludes_cyclic_minimizer=True,kwargs_attribute_lookup=None,kwargs_key_lookup=kwargs['dag_mask'],three_node_orderings=len(orders),order_graph_edge_counts=[sum(i<j for i in range(3) for j in range(3)) for order in orders],native_execution=False)

if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
