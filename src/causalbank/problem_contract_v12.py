"""LA02 declaration review; no model calls, identification engine or estimator.

Passing permits conditional formal analysis. It establishes neither the truth
of evidence nor membership/completeness of a discovered graph class.
"""
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT/'docs/program/repair-v12/work/LA02'


def declaration_digest(problem, diagram):
    return hashlib.sha256(json.dumps({'problem':problem,'diagram':diagram}, sort_keys=True,
                                    separators=(',',':'),allow_nan=False).encode()).hexdigest()


def _finite(value):
    if isinstance(value,float) and not math.isfinite(value):
        raise ValueError('Nonfinite declaration')
    if isinstance(value,dict):
        for x in value.values():
            _finite(x)
    elif isinstance(value,list):
        for x in value:
            _finite(x)


def _reachable(start, arcs):
    # Finite closure also terminates for invalid cyclic input.
    seen = set()
    changed = True
    while changed:
        before = len(seen)
        seen |= {v for u,v in arcs if u == start or u in seen}
        changed = len(seen) != before
    return seen


def graph_roles(graph,treatment,outcome):
    """Conditional directed-path roles only; not a general adjustment criterion."""
    arcs=[]
    for e in graph['edges']:
        marks=(e['left_mark'],e['right_mark'])
        if marks==('tail','arrow'):
            arcs.append((e['left'],e['right']))
        elif marks==('arrow','tail'):
            arcs.append((e['right'],e['left']))
    descendants=_reachable(treatment,arcs)
    ancestors_y={n for n in graph['nodes'] if outcome in _reachable(n,arcs)}
    common={n for n in graph['nodes'] if n not in {treatment,outcome}
            and treatment in _reachable(n,arcs) and outcome in _reachable(n,arcs)}
    colliders=[]
    for node in graph['nodes']:
        parents=sorted({u for u,v in arcs if v==node})
        if len(parents)>1:
            colliders.append({'node':node,'parents':parents})
    return {'treatment_descendants':sorted(descendants),
            'directed_path_mediators':sorted((descendants & ancestors_y)-{treatment,outcome}),
            'common_ancestors':sorted(common),'collider_candidates':colliders,
            'scope':'Directed paths in this declared candidate only; latent/mixed paths and valid adjustment require a formal engine.'}


def review_problem(problem,diagram,*,previous_diagram=None):
    """Return errors and unresolved declarations without inventing causal facts."""
    from jsonschema import Draft202012Validator

    errors, blockers, obligations, roles = [], [], [], []
    try:
        _finite(problem)
        _finite(diagram)
    except ValueError as exc:
        errors.append(str(exc))
    for name,value in [('problem',problem),('diagram',diagram)]:
        schema=json.loads((SCHEMAS/(name+'-schema.json')).read_text())
        for error in Draft202012Validator(schema).iter_errors(value):
            errors.append(name+':'+'.'.join(map(str,error.path))+': '+error.message)
    if errors:
        return {'gate':'invalid','errors':errors,'blockers':[],'obligations':[], 'graph_roles':[],
                'declaration_sha256':None,'scientific_qualification':'none'}
    if problem['problem_id']!=diagram['problem_id']:
        errors.append('Problem and diagram identities differ')

    def unique(rows,label):
        if len({x['id'] for x in rows}) != len(rows):
            errors.append('Duplicate '+label+' identity')

    for field in ['variables','decision_points','estimand_alternatives','assumptions','evidence']:
        unique(problem[field],field)
    unique(diagram['models'],'model')
    variables={v['id']:v for v in problem['variables']}
    decisions={d['id']:d for d in problem['decision_points']}
    targets={t['id']:t for t in problem['estimand_alternatives']}
    evidence={e['id']:e for e in problem['evidence']}
    assumptions={a['id']:a for a in problem['assumptions']}

    def references(values,allowed,label):
        unknown=set(values)-set(allowed)
        if unknown:
            errors.append(label+' has undeclared references: '+','.join(sorted(unknown)))
        return not unknown

    def review_declaration(review,refs,label):
        if review['status'] in {'accepted_assumption','synthetic_fixture'} and not review['reviewer']:
            errors.append(label+' has no declared reviewer')
        if review['status']=='synthetic_fixture' and problem['provenance_mode']!='synthetic_fixture':
            errors.append(label+' tries to promote a synthetic fixture to bank evidence')
        if review['status']=='accepted_assumption' and refs and all(evidence.get(i,{}).get('kind')=='model_proposal' for i in refs):
            blockers.append(label+' has only model proposals; independent scientific review evidence is missing')

    for v in variables.values():
        if (v['measurement']=='derived') != bool(v['derived_from']):
            errors.append(v['id']+' derived measurement and lineage disagree')
        if v['measurement']=='latent' and v['available_time'] is not None:
            errors.append(v['id']+' latent variable has an observed availability time')
        if v['available_time'] is not None and v['event_time']>v['available_time']:
            errors.append(v['id']+' is available before its event')
        if references(v['derived_from'],variables,v['id']+' derivation'):
            for parent in v['derived_from']:
                a,b=variables[parent]['available_time'],v['available_time']
                if a is None or b is None or a>b:
                    errors.append(v['id']+' derivation uses an unavailable input')
    lineage=[(p,v['id']) for v in variables.values() for p in v['derived_from']]
    if any(n in _reachable(n,lineage) for n in variables):
        errors.append('Derived-variable lineage contains a cycle')
    for decision in decisions.values():
        if references(decision['information_set'],variables,decision['id']+' history'):
            for n in decision['information_set']:
                v=variables[n]
                if v['available_time'] is None or v['available_time']>decision['time']:
                    errors.append(decision['id']+' uses unavailable information '+n)
    for a in assumptions.values():
        references(a['evidence_refs'],evidence,a['id']+' evidence')
        review_declaration(a['review'],a['evidence_refs'],a['id'])
        if a['status']=='contradicted':
            obligations.append('Contradicted assumption '+a['id']+' cannot support an analysis without a replacement model')
    selected=problem['resolution']['selected_id']
    if problem['resolution']['status']=='selected':
        if selected not in targets:
            errors.append('Selected estimand is undeclared')
        if problem['resolution']['review']['status'] not in {'accepted_assumption','synthetic_fixture'}:
            blockers.append('Selected estimand lacks an explicit reviewed choice')
    else:
        if selected is not None:
            errors.append('Unresolved/refused question contains a selected estimand')
        blockers.append('Business question is '+problem['resolution']['status']+'; preserve the alternatives')
    review_declaration(problem['resolution']['review'],[], 'Estimand resolution')
    expected_measure={'ATE':'population_uniform','ATT':'treated_population','overlap_ATE':'overlap_propensity',
                      'trimmed_ATE':'propensity_trimmed','policy_value':'population_uniform',
                      'policy_contrast':'population_uniform','population_mean':'population_uniform'}
    action_times={}
    for t in targets.values():
        references([t['treatment'],t['outcome']],variables,t['id']+' target')
        references(t['adjustment']['variables'],variables,t['id']+' adjustment')
        references([x['variable'] for x in t['population_condition']],variables,t['id']+' population')
        if t['target_measure']['kind']!=expected_measure[t['family']]:
            errors.append(t['id']+' target family disagrees with its population measure')
        bounds=t['target_measure']['trimming_bounds']
        if t['family']=='trimmed_ATE':
            if bounds is None or not 0<=bounds[0]<bounds[1]<=1:
                errors.append(t['id']+' needs ordered trimming bounds in [0,1]')
        elif bounds is not None:
            errors.append(t['id']+' carries trimming bounds for a different target')
        if t['horizon']['end']<t['horizon']['start']:
            errors.append(t['id']+' horizon is reversed')
        y=variables.get(t['outcome'])
        if y and not t['horizon']['start']<=y['event_time']<=t['horizon']['end']:
            errors.append(t['id']+' outcome event is outside the target horizon')
        for regime in ['intervention','comparator']:
            interventions=t[regime]['actions']
            pairs=[(a['decision_id'],a['variable']) for a in interventions]
            if len(set(pairs))!=len(pairs):
                errors.append(t['id']+' repeats an action in one regime')
            if (t[regime]['kind']=='dynamic') != any(a['rule'] is not None for a in interventions):
                errors.append(t['id']+' regime kind disagrees with its rule')
            for action in interventions:
                references(action['evidence_refs'],evidence,t['id']+' feasibility')
                ok=references([action['variable']],variables,t['id']+' action')
                ok=references([action['decision_id']],decisions,t['id']+' decision') and ok
                if not ok:
                    continue
                d=decisions[action['decision_id']]
                action_times[action['variable']]=d['time']
                if variables[action['variable']]['event_time']!=d['time']:
                    errors.append(t['id']+' action time disagrees with its variable event')
                references(action['depends_on'],d['information_set'],t['id']+' policy history')
                rule=action['rule']
                if rule is not None and (rule['variable'] not in action['depends_on'] or action['value'] is not None):
                    errors.append(t['id']+' dynamic rule has an undeclared input or fixed competing value')
                if rule is None and action['value'] is None:
                    blockers.append(t['id']+' action value is unresolved')
                if action['feasibility'] in {'infeasible','unknown'}:
                    (blockers if selected==t['id'] else obligations).append(t['id']+' action feasibility is '+action['feasibility'])
                if action['feasibility']=='hypothetical' and problem['provenance_mode']!='synthetic_fixture':
                    blockers.append(t['id']+' hypothetical action lacks bank feasibility evidence')
    for d in decisions.values():
        for n in d['information_set']:
            if n in action_times and action_times[n]>=d['time']:
                errors.append(d['id']+' history includes a simultaneous/future decision action '+n)

    if previous_diagram is not None:
        expected=hashlib.sha256(json.dumps(previous_diagram,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
        if diagram['prior_revision_sha256']!=expected or previous_diagram['problem_id']!=diagram['problem_id']:
            errors.append('Graph revision does not link to the supplied predecessor')
        if diagram['revision_id']==previous_diagram['revision_id']:
            errors.append('Graph revision reuses its predecessor identity')
    elif diagram['prior_revision_sha256'] is not None:
        blockers.append('Graph predecessor must be supplied to verify the revision chain')
    for g in diagram['models']:
        references(g['nodes'],variables,g['id']+' nodes')
        references(g['estimand_ids'],targets,g['id']+' estimands')
        references(g['assumption_ids'],assumptions,g['id']+' assumptions')
        if any(assumptions.get(a,{}).get('status')=='contradicted' for a in g['assumption_ids']):
            (blockers if selected in g['estimand_ids'] else obligations).append(g['id']+' depends on a contradicted assumption')
        unique(g['edges'],g['id']+' edge')
        arcs=[]
        seen=set()
        for e in g['edges']:
            references([e['left'],e['right']],g['nodes'],e['id']+' endpoints')
            references(e['evidence_refs'],evidence,e['id']+' evidence')
            references(e['counterevidence']['evidence_refs'],evidence,e['id']+' counterevidence')
            if e['counterevidence']['status']=='reported' and not e['counterevidence']['evidence_refs']:
                errors.append(e['id']+' reported counterevidence lacks an anchor')
            review_declaration(e['review'],e['evidence_refs'],e['id'])
            if e['review']['status']=='rejected':
                blockers.append(e['id']+' rejected edge remains in a candidate graph')
            if e['left']==e['right']:
                errors.append(e['id']+' self edge')
            marks=(e['left_mark'],e['right_mark'])
            allowed={'DAG':{('tail','arrow'),('arrow','tail')},
                     'ADMG':{('tail','arrow'),('arrow','tail'),('arrow','arrow')},
                     'CPDAG':{('tail','arrow'),('arrow','tail'),('tail','tail')}}
            if g['kind'] in allowed and marks not in allowed[g['kind']]:
                errors.append(e['id']+' marks cannot represent '+g['kind'])
            forward=(e['left'],e['right'],*marks)
            reverse=(e['right'],e['left'],marks[1],marks[0])
            if forward in seen or reverse in seen:
                errors.append(e['id']+' duplicate endpoint relation')
            seen.add(forward)
            if marks==('tail','arrow'):
                arcs.append((e['left'],e['right']))
            elif marks==('arrow','tail'):
                arcs.append((e['right'],e['left']))
        for n in g['nodes']:
            if n in _reachable(n,arcs):
                errors.append(g['id']+' directed cycle')
                break
        for u,v in arcs:
            if u in variables and v in variables and variables[u]['event_time']>variables[v]['event_time']:
                errors.append(g['id']+' directed edge reverses the declared event order')
        for restriction in g['forbidden_directions']:
            references([restriction['source'],restriction['target']],g['nodes'],g['id']+' forbidden edge')
            references(restriction['evidence_refs'],evidence,g['id']+' restriction evidence')
            if (restriction['source'],restriction['target']) in arcs:
                errors.append(g['id']+' violates a forbidden direction')
        for tid in g['estimand_ids']:
            if tid not in targets:
                continue
            t=targets[tid]
            references([t['treatment'],t['outcome']],g['nodes'],g['id']+' bound target')
            r=graph_roles(g,t['treatment'],t['outcome'])
            roles.append({'graph_id':g['id'],'estimand_id':tid,**r})
            if t['adjustment']['purpose']=='total_effect':
                bad=set(t['adjustment']['variables']) & set(r['treatment_descendants'])
                if bad:
                    (blockers if selected==tid else obligations).append(tid+' proposes post-treatment adjustment: '+','.join(sorted(bad)))
            population={x['variable'] for x in t['population_condition']}
            if population & set(r['treatment_descendants']):
                (blockers if selected==tid else obligations).append(tid+' conditions population membership on post-treatment variables; specify the selection/principal-stratum target')
            collider_nodes={x['node'] for x in r['collider_candidates']}
            if (population|set(t['adjustment']['variables'])) & collider_nodes:
                obligations.append(tid+' conditions on a collider candidate in '+g['id']+'; formal path analysis required')
        if g['kind'] in {'CPDAG','PAG'}:
            obligations.append(g['id']+' retains endpoint ambiguity; full graph-class recognition and identification are delegated to a formal engine')
    if selected is not None and not any(selected in g['estimand_ids'] for g in diagram['models']):
        errors.append('Selected estimand has no candidate graph binding')
    obligations.append('All conclusions remain conditional on declarations; validation does not establish causal or audit truth')
    return {'gate':'invalid' if errors else 'needs_review' if blockers else 'ready_for_formal_analysis',
            'errors':list(dict.fromkeys(errors)),'blockers':list(dict.fromkeys(blockers)),
            'obligations':list(dict.fromkeys(obligations)),'graph_roles':roles,
            'declaration_sha256':declaration_digest(problem,diagram),'scientific_qualification':'none'}
