#!/usr/bin/env python3
"""Exact authored graph/transport laws; no upstream package or bank experiment."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-17/s7'


def graph(theta):
    return {(0, 0): theta, (1, 1): theta,
            (1, 0): F(1, 2)-theta, (0, 1): F(1, 2)-theta}


def actions(p, both):
    return {(0, 0): 1-2*p+both, (1, 1): both,
            (1, 0): p-both, (0, 1): p-both}


def exposure(theta, p, both):
    return p-both*theta


def enumeration(theta, p, both):
    return sum(pg*pa*int(bool(u*a or v*b))
               for (u, v), pg in graph(theta).items()
               for (a, b), pa in actions(p, both).items())


def text(value):
    return str(value)


def calculate():
    p0, p1 = F(1, 5), F(3, 5)
    endpoint_rows = []
    for theta in [F(0), F(1, 4), F(1, 2)]:
        q0, q1 = [exposure(theta, p, p*p) for p in [p0, p1]]
        endpoint_rows.append(dict(theta=text(theta),
            graph={f'{u}{v}':text(m) for (u,v),m in graph(theta).items()},
            q0=text(q0), q1=text(q1), delta=text(q1-q0),
            action_cost='16', before_investment=text(100*(q1-q0)-16),
            after_investment=text(100*(q1-q0)-16-16)))
    policy_rows=[]
    for name, r1 in [('independent',p1*p1),('shared',p1),('dispersed',F(1,5))]:
        delta_r=r1-p0
        vals=[8-100*delta_r*t for t in [F(0),F(1,2)]]
        policy_rows.append(dict(policy=name,old_both='1/5',new_both=text(r1),
            new_assignment={f'{a}{b}':text(m) for (a,b),m in actions(p1,r1).items()},
            value_intercept='8',value_theta_coefficient=text(-100*delta_r),
            value_set=[text(min(vals)),text(max(vals))]))
    topology=[]
    for name,degrees in [('source',[1]*8),('target',[0]*4+[2]*4)]:
        q=[sum((1-(1-p)**d for d in degrees),F(0))/8 for p in [p0,p1]]
        v=100*(q[1]-q[0])-20*(p1-p0)
        topology.append(dict(population=name,degrees=degrees,mean_degree='1',
            q0=text(q[0]),q1=text(q[1]),before_investment=text(v),
            after_investment=text(v-24)))
    pooled=[]
    for t0,t1 in [(F(1,6),F(1,2)),(F(1,3),F(0)),(F(1,4),F(1,4))]:
        v0,v1=-8-32*t0,32-64*t1
        pooled.append(dict(theta0=text(t0),theta1=text(t1),
            pooled_overlap=text(F(3,4)*t0+F(1,4)*t1),
            stratum_values=[text(v0),text(v1)],
            target_value=text(F(1,4)*v0+F(3,4)*v1)))
    audit=[]
    for name,n0,n1,c1 in [('equal_cost_target',100,600,1),
                          ('equal_cost_source',525,175,1),
                          ('priced_target',140,420,4),
                          ('priced_source',780,260,4)]:
        audit.append(dict(design=name,n0=n0,n1=n1,cost=n0+c1*n1,
            worst_variance_bound=text(F(16,n0)+F(576,n1))))
    with localcontext() as ctx:
        ctx.prec=45
        threshold=Decimal(128)*Decimal(40).ln()
        radius=(Decimal(40).ln()/Decimal(2*473)).sqrt()
        concentration=dict(alpha='0.05',log_argument=40,
            strict_n_threshold=str(threshold),first_sufficient_integer=473,
            radius_at_473=str(radius),twice_radius=str(2*radius),
            theta_assumed_upper='1/8',sign_boundary='1/4',
            sufficient_condition='2*r_n < 1/8')
    return dict(status='exact_authored_references',units='illustrative USD per focal beneficiary; topology example per population member',
        independent_edge_completion=endpoint_rows,coordinated_policy=policy_rows,
        topology_shift=topology,pooled_audit_transport=pooled,
        conditional_mixture=dict(values=['-8','8'],weights=['1/2','1/2'],
            conditional_variance='1',between_variance='64',total_variance='65'),
        neighborhood_design=concentration,target_weighted_audit=audit,
        evidential_status='Stipulated finite laws and prospective analytic design; no sampled study, upstream execution, authentic bank observation or ROI.')


def separate(result):
    checked=0
    for theta in [F(0),F(1,8),F(1,4),F(3,8),F(1,2)]:
        g=graph(theta)
        assert min(g.values())>=0 and sum(g.values())==1
        assert sum(m*u for (u,v),m in g.items())==F(1,2)
        assert sum(m*v for (u,v),m in g.items())==F(1,2)
        for p in [F(1,5),F(3,5)]:
            for r in [max(F(0),2*p-1),p*p,p]:
                a=actions(p,r)
                assert min(a.values())>=0 and sum(a.values())==1
                assert enumeration(theta,p,r)==exposure(theta,p,r)
                checked+=1
    # Distinct topology check: enumerate all 256 global assignments on actual graphs.
    edges=[[(0,1),(2,3),(4,5),(6,7)],[(4,5),(5,6),(6,7),(7,4)]]
    global_means=[]
    for es in edges:
        neighbors={i:set() for i in range(8)}
        for u,v in es:
            neighbors[u].add(v);neighbors[v].add(u)
        vals=[]
        for p in [F(1,5),F(3,5)]:
            mean=F(0)
            for av in product([0,1],repeat=8):
                na=sum(av);mass=p**na*(1-p)**(8-na)
                affected=sum(any(av[j] for j in neighbors[i]) for i in range(8))
                mean+=mass*F(affected,8)
            vals.append(mean)
        global_means.append(vals)
    for row,vals in zip(result['topology_shift'],global_means):
        assert [row['q0'],row['q1']]==[str(x) for x in vals]
    # Box/affine intersections, independent of the reduced one-dimensional formula.
    vertices=set()
    for which in [0,1]:
        for boundary in [F(0),F(1,2)]:
            if which==0:
                t0=boundary;t1=1-3*t0
            else:
                t1=boundary;t0=(1-t1)/3
            if 0<=t0<=F(1,2) and 0<=t1<=F(1,2):
                vertices.add((t0,t1))
    assert vertices=={(F(1,6),F(1,2)),(F(1,3),F(0))}
    target=[]
    for t0,t1 in vertices:
        stratum=[]
        for t,b in [(t0,100),(t1,200)]:
            dq=enumeration(t,F(3,5),F(9,25))-enumeration(t,F(1,5),F(1,25))
            stratum.append(b*dq-16-32)
        target.append(F(1,4)*stratum[0]+F(3,4)*stratum[1])
    assert sorted(target)==[F(-10,3),F(58,3)]
    # Explicit four-point mixture with conditional noise +/-1.
    values=[m+e for m in [-8,8] for e in [-1,1]]
    mean=F(sum(values),4)
    assert sum((v-mean)**2 for v in values)/4==65
    assert result['neighborhood_design']['first_sufficient_integer']==473
    with localcontext() as ctx:
        ctx.prec=45
        for n,expected in [(472,False),(473,True)]:
            r=(Decimal(40).ln()/Decimal(2*n)).sqrt()
            assert (2*r<Decimal(1)/8)==expected
    designs={r['design']:r for r in result['target_weighted_audit']}
    assert designs['equal_cost_target']['cost']==designs['equal_cost_source']['cost']==700
    assert F(designs['equal_cost_target']['worst_variance_bound'])==F(784,700)
    assert designs['priced_target']['cost']==designs['priced_source']['cost']==1820
    assert F(designs['priced_target']['worst_variance_bound'])==F(2704,1820)
    for theta0,theta1 in product([F(0),F(1,4),F(1,2)],repeat=2):
        for row in result['target_weighted_audit']:
            v=64*theta0*(1-theta0)/row['n0']+2304*theta1*(1-theta1)/row['n1']
            assert v<=F(row['worst_variance_bound'])
    return dict(status='pass',reviewer_kind='distinct author calculations, not independent reviewer',
        graph_action_enumerations=checked,global_assignments_per_topology_and_policy=256,
        affine_box_vertices=[[str(x) for x in t] for t in sorted(vertices)],
        checks=['Coherent joint probabilities and exact exposure enumeration',
                'Realizable matching/cycle graph global allocation enumeration',
                'Affine-box sharp transport vertices and stratum value enumeration',
                'Four-point completion/noise variance decomposition',
                'Concentration threshold on both adjacent integers',
                'Budget identities, variance inequalities and continuous optimum certificates'],
        limits=['All structural and monetary values are supplied hypothetical inputs.',
                'Analytic audits require independent truthful neighborhood units and declared inclusion.',
                'No sampled coverage, fitted software, network-port qualification or bank benefit is inferred.'])


def main():
    exact=calculate();checked=separate(exact)
    write(BASE/'exact-results.json',exact)
    write(BASE/'mathematics-review.json',dict(checked,evidence=[
        ref(BASE/'exact-results.json','Exact rational and high-precision references'),
        ref(Path(__file__),'Finite enumeration and distinct author calculations'),
        ref(BASE/'plan.md','Reviewed scope and assumptions')]))
    print(json.dumps(dict(status='pass',exact_laws=7,checks=checked['checks'])))


if __name__=='__main__': main()
