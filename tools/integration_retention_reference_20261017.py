#!/usr/bin/env python3
"""Finite proposal model of publication pins and collection; never deletes files."""
from itertools import permutations
import json

DEPS={'report':{'data'},'data':set()}

def closure(roots):
    seen=set();todo=list(roots)
    while todo:
        x=todo.pop()
        if x not in seen:seen.add(x);todo.extend(DEPS[x])
    return seen

def simulate(order,recheck):
    present=set(DEPS);roots=set();pins=set();mark=set();admitted=False
    trace=[]
    for event in order:
        if event=='pin':
            admitted=closure({'report'})<=present
            if admitted:pins.add('report')
        elif event=='publish':
            if admitted:roots.add('report')
        elif event=='unpin':pins.clear()
        elif event=='snapshot':mark=closure(roots|pins)
        elif event=='sweep':
            keep=mark|(closure(roots|pins) if recheck else set())
            present &= keep
        else:raise AssertionError(event)
        dangling=not closure(roots|pins)<=present
        trace.append(dict(event=event,present=sorted(present),roots=sorted(roots),pins=sorted(pins),dangling=dangling))
    return dict(order=list(order),admitted=admitted,published=bool(roots),unsafe=any(x['dangling'] for x in trace),trace=trace)

def calculate():
    names=['pin','publish','unpin','snapshot','sweep']
    orders=[x for x in permutations(names) if x.index('pin')<x.index('publish')<x.index('unpin') and x.index('snapshot')<x.index('sweep')]
    unsafe=[simulate(x,False) for x in orders];safe=[simulate(x,True) for x in orders]
    assert len(orders)==10
    assert not any(x['unsafe'] for x in safe)
    assert any(x['unsafe'] for x in unsafe)
    witness=simulate(('snapshot','pin','publish','sweep','unpin'),False)
    assert witness['unsafe'] and witness['published']
    # Monotone roots and atomic present-check/pin acquisition allow only an
    # admission rejection when collection wins; no invalid published reference.
    rejected=[x for x in safe if not x['admitted']]
    assert len(rejected)==1
    # A stale pin preserves both objects. Expiring a live pin without fencing
    # the resumed publisher produces the same dangling-reference hazard.
    stale=closure({'report'});assert stale==set(DEPS)
    # A prior mark protects this particular schedule, so use a fresh empty
    # snapshot after expiry to exhibit the unsafe lease shortcut directly.
    expired_present=set(DEPS)-closure({'report'})
    resumed_roots={'report'}
    assert not closure(resumed_roots)<=expired_present
    return dict(kind='finite_project_design_reference',orders=len(orders),snapshot_only_unsafe=sum(x['unsafe'] for x in unsafe),rechecked_unsafe=0,admission_rejections=len(rejected),protected_successes=sum(x['published'] for x in safe),snapshot_witness=witness,protected=safe,stale_pin_retained=sorted(stale),expired_live_pin_counterexample=dict(present=sorted(expired_present),resumed_roots=sorted(resumed_roots),dangling=True),limitations=['Atomic metadata transitions, immutable complete dependency graph, cooperating actors and one logical store.','Not a running collector, filesystem durability proof, distributed protocol or bank retention policy.'])

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
