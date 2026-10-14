"""Adverse scientific declarations for LA02; no downloaded implementation runs."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from causalbank.problem_contract_v12 import declaration_digest, graph_roles, review_problem

WORK=Path(__file__).resolve().parents[1]/'docs/program/repair-v12/work/LA02'


def case(name):
    return deepcopy(next(c for c in json.loads((WORK/'casebook.json').read_text())['cases'] if c['id']==name))


def check(c):
    return review_problem(c['problem'],c['diagram'])


@pytest.mark.parametrize('name',['funding','servicing','discovery','observation'])
def test_case_disposition(name):
    c=case(name)
    out=check(c)
    assert out['gate']==c['expected_gate'],out
    assert out['scientific_qualification']=='none'


def test_unresolved_question_cannot_carry_silent_choice():
    c=case('funding'); c['problem']['resolution']['selected_id']='balance_response'
    assert check(c)['gate']=='invalid'


def test_model_rating_cannot_be_called_causal_probability():
    c=case('discovery')
    c['diagram']['models'][0]['edges'][0]['model_score']={'value':0.99,'meaning':'causal_probability',
        'model_id':'model-fixture','prompt_sha256':'a'*64}
    assert check(c)['gate']=='invalid'


def test_every_edge_needs_evidence_anchor():
    c=case('discovery'); c['diagram']['models'][0]['edges'][0]['evidence_refs']=[]
    assert check(c)['gate']=='invalid'


def test_declared_evidence_reference_must_exist():
    c=case('discovery'); c['diagram']['models'][0]['edges'][0]['evidence_refs']=['invented-paper']
    assert check(c)['gate']=='invalid'


def test_reported_counterevidence_needs_a_source():
    c=case('discovery'); c['diagram']['models'][0]['edges'][0]['counterevidence']['status']='reported'
    assert check(c)['gate']=='invalid'


def test_future_information_rejected_at_decision():
    c=case('servicing'); c['problem']['decision_points'][1]['time']=10
    out=check(c)
    assert out['gate']=='invalid'
    assert any('unavailable information L1' in e for e in out['errors'])


def test_simultaneous_action_cannot_be_a_policy_input():
    c=case('servicing'); c['problem']['decision_points'][1]['information_set'].append('A1')
    assert any('simultaneous/future decision' in e for e in check(c)['errors'])


def test_derived_value_cannot_precede_its_input():
    c=case('servicing'); v=c['problem']['variables'][0]
    v['measurement']='derived'; v['derived_from']=['L1']
    assert any('unavailable input' in e for e in check(c)['errors'])


def test_latent_variable_is_not_observed_history():
    c=case('observation'); c['problem']['decision_points'][0]['information_set'].append('ownership')
    assert check(c)['gate']=='invalid'


def test_dynamic_rule_needs_declared_history():
    c=case('servicing')
    c['problem']['estimand_alternatives'][0]['intervention']['actions'][1]['rule']['variable']='Y'
    assert check(c)['gate']=='invalid'


def test_infeasible_action_retains_review_obligation():
    c=case('servicing')
    c['problem']['estimand_alternatives'][0]['intervention']['actions'][0]['feasibility']='infeasible'
    assert check(c)['gate']=='needs_review'


def test_total_effect_does_not_silently_adjust_for_mediator():
    c=case('servicing'); c['problem']['resolution']['selected_id']='static_total'
    c['problem']['estimand_alternatives'][1]['adjustment']['variables'].append('L1')
    out=check(c)
    assert out['gate']=='needs_review'
    assert any('post-treatment adjustment' in x for x in out['blockers'])


def test_intermediate_confounder_and_mediator_roles_coexist():
    c=case('servicing'); g=c['diagram']['models'][0]
    assert 'L1' in graph_roles(g,'A0','Y')['directed_path_mediators']
    assert 'L1' in graph_roles(g,'A1','Y')['common_ancestors']


def test_selected_population_is_not_silently_original_population():
    c=case('observation'); c['problem']['resolution'].update(status='selected',selected_id='linked_accounts')
    out=check(c)
    assert out['gate']=='needs_review'
    assert any('post-treatment variables' in x for x in out['blockers'])
    assert any('collider candidate' in x for x in out['obligations'])


def test_cpdag_cannot_be_retyped_as_dag_without_changing_marks():
    c=case('discovery'); c['diagram']['models'][0]['kind']='DAG'
    assert check(c)['gate']=='invalid'


def test_pag_marks_survive_round_trip():
    c=case('discovery'); g=c['diagram']['models'][0]
    g['kind']='PAG'; g['edges'][0]['left_mark']='circle'; g['edges'][0]['right_mark']='arrow'
    c=json.loads(json.dumps(c)); before=deepcopy(c)
    out=check(c)
    assert out['gate']=='ready_for_formal_analysis'
    assert c==before
    assert any('endpoint ambiguity' in x for x in out['obligations'])


def test_cycle_is_invalid_even_with_positive_reviews():
    c=case('discovery'); g=c['diagram']['models'][1]
    g['edges'].append(deepcopy(c['diagram']['models'][2]['edges'][0]))
    assert any('directed cycle' in e for e in check(c)['errors'])


def test_explicit_forbidden_direction_is_enforced():
    c=case('discovery'); g=c['diagram']['models'][1]
    g['forbidden_directions']=[{'source':'A','target':'Y','evidence_refs':['case_definition']}]
    assert any('forbidden direction' in e for e in check(c)['errors'])


def test_model_proposal_is_not_accepted_scientific_evidence():
    c=case('discovery'); c['problem']['evidence'][0]['kind']='model_proposal'
    c['diagram']['models'][0]['edges'][0]['review']={'status':'accepted_assumption','reviewer':'Declared person'}
    assert check(c)['gate']=='needs_review'


def test_synthetic_review_cannot_be_promoted_to_bank_analysis():
    c=case('servicing'); c['problem']['provenance_mode']='proposed_bank_analysis'
    assert check(c)['gate']=='invalid'


def test_revision_requires_exact_predecessor():
    c=case('discovery'); old=deepcopy(c['diagram'])
    c['diagram'].update(revision_id='discovery-v2',prior_revision_sha256='0'*64)
    assert review_problem(c['problem'],c['diagram'],previous_diagram=old)['gate']=='invalid'
    c['diagram']['prior_revision_sha256']=hashlib.sha256(json.dumps(old,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert review_problem(c['problem'],c['diagram'],previous_diagram=old)['gate']=='ready_for_formal_analysis'


def test_estimand_change_changes_bound_declaration():
    c=case('discovery'); old=declaration_digest(c['problem'],c['diagram'])
    c['problem']['estimand_alternatives'][0]['population']='A different population'
    assert declaration_digest(c['problem'],c['diagram'])!=old


def test_overlap_name_cannot_hide_uniform_population_measure():
    c=case('discovery'); c['problem']['estimand_alternatives'][0]['family']='overlap_ATE'
    assert any('population measure' in e for e in check(c)['errors'])


def test_contradicted_bound_assumption_blocks_selected_analysis():
    c=case('servicing'); c['problem']['assumptions'][0]['status']='contradicted'
    assert check(c)['gate']=='needs_review'


def test_derived_lineage_cannot_be_circular_at_equal_timestamps():
    c=case('discovery')
    for v in c['problem']['variables']:
        v['measurement']='derived'; v['derived_from']=['Y' if v['id']=='A' else 'A']
    assert any('lineage contains a cycle' in e for e in check(c)['errors'])


@pytest.mark.parametrize('value',[float('nan'),float('inf')])
def test_nonfinite_time_rejected(value):
    c=case('servicing'); c['problem']['decision_points'][0]['time']=value
    assert check(c)['gate']=='invalid'
