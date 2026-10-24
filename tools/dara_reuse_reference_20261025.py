#!/usr/bin/env python3
"""Independent exact graph and request invariants; not execution of Dara source."""
from fractions import Fraction
import json

def acyclic(edges):
    nodes={x for edge in edges for x in edge};remaining=set(nodes);edges=set(edges)
    while remaining:
        roots={n for n in remaining if not any(b==n and a in remaining for a,b in edges)}
        if not roots:return False
        remaining-=roots
    return True

def calculate():
    original={('A','B'),('A','C'),('C','B')};reversed_graph=(original-{('A','B')})|{('B','A')}
    assert acyclic(original) and not acyclic(reversed_graph)
    # Explicit symbolic composition of the two inspected endpoint-swapping stages.
    internal=('A','B');edge_serializer=('B','A');outer_serializer=(edge_serializer[1],edge_serializer[0]);outer_keys=('B','A')
    assert outer_serializer==internal and outer_serializer!=outer_keys
    requested_version='g1';current_version='g2';assert requested_version!=current_version
    costs=dict(preparation=1000,all_attempts=1000,scientific_review=2500,maintenance=500);assert sum(costs.values())==5000
    return dict(scope='Authored graph invariants and symbolic source-path composition;no native frontend/backend execution',
        original_edges=sorted(map(list,original)),reversed_edges=sorted(map(list,reversed_graph)),original_acyclic=True,reversed_acyclic=False,
        backwards_edge=dict(internal=list(internal),first_swap=list(edge_serializer),second_swap=list(outer_serializer),outer_keys=list(outer_keys),nested_endpoints_match_outer_keys=False,reachable_native_behavior_unverified=True),
        stale_edit=dict(requested=requested_version,current=current_version,proposed_result='refuse_stale_version'),
        acceptance=dict(rendering_accepted=True,scientific_identification='not_implied'),
        costs_usd=costs,total_usd=5000,attempted=100,completed=80,admissible=50,
        per_attempt_usd=str(Fraction(5000,100)),per_completion_usd=str(Fraction(5000,80)),per_admissible_usd=str(Fraction(5000,50)))
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
