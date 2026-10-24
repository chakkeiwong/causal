#!/usr/bin/env python3
"""Resolve one named agent lineage as reference use, without native admission."""
import argparse
import hashlib
import json
from pathlib import Path
import copilot_reuse_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

run = controller.base
core = run.core
ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-25/copilot-reuse-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-17/census-recovery/copilot-v1'
AUDIT = ROOT / 'docs/program/execution/2026-10-25/panels-cxx-reader-v1/reader/source-audit.json'
OP = 'SW.DECISION.seed_103'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Historical paper and source snapshot are not bound as one experiment release.',
    'No downloaded code, provider, installed agent, native CLI or MCP service executed.',
    'Selected original paths and two MIT notices do not establish complete dependency, asset, data or provider rights.',
    'Current maintenance, native scientific and runtime behavior, full costs and deployment qualification remain open.',
    'No generic agent-family approval, bank validation, visual or final acceptance.',
]


def prepare():
    assert not (BASE / 'review.json').exists()
    keys = {'exec17_copilot_paper', 'exec17_copilot_code', 'exec17_copilot_rights', 'exec17_copilot_exact'}
    sources = [s for s in read(AUDIT)['sources'] if s['integrated_citation_key'] in keys]
    assert len(sources) == 4
    for s in sources:
        verify_bindings(s)
    validation = read(PRIOR / 'git-byte-validation.json')
    assert validation['status'] == 'pass' and not validation['tree_truncated']
    assert validation['commit'] == 'a31aa7cab277d7e19478bc326dbec154525969cc'
    files = validation['validated_files']
    assert len(files) == 15
    for item in files:
        p = ROOT / item['local_copy']['path']
        data = p.read_bytes()
        assert hashlib.sha256(data).hexdigest() == item['local_copy']['sha256']
        blob = b'blob ' + str(len(data)).encode() + bytes([0]) + data
        assert hashlib.sha1(blob).hexdigest() == item['git_blob_sha1']
    anchors = {
        'readme-lines-1-25.txt': ['Causal-Copilot-V1', 'Causal-Copilot-V2', 'Lancelot39/Causal-Copilot', '2504.13263'],
        'filter-lines-15-40.txt': ['selected_algorithm is not None', 'skip the filtering process'],
        'judge-lines-58-128.txt': ['ts=False', 'fixed_pairs = []', 'revised_graph[i, j] = revised_graph[j, i] = 0'],
        'evaluator-lines-154-215.txt': ['true_graph[i, j]', 'true_graph[j, i]'],
        'requirements-lines-1-38.txt': ['huggingface-hub'],
        'pyproject-lines-1-24.txt': ['not integration and not llm and not latex'],
        'license-lines-1-21.txt': ['MIT License', 'Copyright (c) 2026'],
        'causallearn_license-lines-1-21.txt': ['MIT License', '2022'],
    }
    for name, tokens in anchors.items():
        text = (PRIOR / name).read_text()
        assert all(t in text for t in tokens), name
    write(BASE / 'inherited-review-bindings.json', dict(
        sources=sources, original_validation=ref(PRIOR / 'git-byte-validation.json', 'Fifteen original Git blobs revalidated'),
        source_review=ref(PRIOR / 'primary-review.json', 'Earlier selected primary review, preserved with historical counts'),
        inspected_again=[ref(PRIOR / n, 'Inert original source excerpt re-inspected') for n in anchors],
        cutoff='2026-10-07', native_execution=False))
    write(BASE / 'identity-review.json', dict(status='pass_for_named_lineage', repository=validation['repository'],
        commit=validation['commit'], commit_date=validation['commit_date'],
        aliases=['Causal-Copilot', 'README Causal-Copilot-V1', 'README Causal-Copilot-V2'],
        demo='Linked demonstration identity only; deployed version not authenticated',
        paper_version='arXiv:2504.13263v2; 21 April 2025', paper_experiment_binding=False,
        other_same_named_projects='Not included without independent identity and revision proof',
        evidence=[ref(BASE / 'inherited-review-bindings.json', 'Authentic identity and selected source bytes')]))
    rows = [
        ('business_translation', 'Input/diagnostics/selection/report workflow', 'Versioned population, assignment/outcome clocks, treatment and estimand; assumption provenance'),
        ('algorithm_selection', 'User selection bypasses the inspected filter', 'Preference does not waive scientific assumptions; retain rejected alternatives'),
        ('graph_conversion', 'Receiver/source convention and truth-assisted orientation in selected evaluator', 'Preserve graph class, unresolved marks, identifiers and independently defined scoring'),
        ('temporal_uncertainty', 'Inspected judge passes ts=False', 'Qualify actual resampling route and lag meanings; refuse unsupported temporal confidence'),
        ('refinement', 'Selected conditional path has an empty fixed-pair list', 'Versioned edit proposals, symmetric protection, unknown/no-edge distinction and explicit pruning precedence'),
        ('identification', 'Workflow and numerical outputs do not themselves identify the target', 'Conditional effect, identified set or refusal with assumptions and source provenance'),
        ('cli_mcp', 'No native service qualified by this static assessment', 'Stable requests, schema/data digests, typed failures, deadlines, cancellation and replay accounting'),
        ('costs', 'Selected benchmark timer is narrower than the full journey', 'All requests, provider and review expense, maintenance, failures and scientific admissibility'),
    ]
    write(BASE / 'capability-comparison.json', dict(rows=[dict(area=a,inspected=b,proposal_contract=c) for a,b,c in rows],
        evidence=[ref(BASE / 'inherited-review-bindings.json', 'Primary source limits')], native_execution=False))
    fixtures = [
        ('variable_permutation', 'Exact names, marks and receiver/source mapping survive round trip'),
        ('ambiguous_direction', 'Compatible directions remain unresolved unless new evidence excludes one'),
        ('observational_equivalence', 'No unconditional effect when admitted worlds imply different effects'),
        ('lag_pair', 'Lag-one and lag-five requests retain distinct information clocks'),
        ('protected_edit', 'Both identifier orderings obey protection and later pruning has explicit precedence'),
        ('stale_graph', 'An edit for an earlier graph digest fails without silently applying to a successor'),
        ('unknown_answer', 'Unknown is distinct from no edge and invalid response'),
        ('provider_failure', 'Malformed response, refusal, timeout and cancellation retain typed terminal/uncertain status'),
        ('duplicate_delivery', 'Replay retains logical request identity and cannot double-count one accepted result'),
        ('scientific_comparison', 'Matched information; truth-assisted compatibility separately named; target-specific predeclared errors/coverage'),
    ]
    write(BASE / 'qualification-plan.json', dict(status='proposed_not_executed',
        arms=['Fixed method/configuration','Frozen permitted upstream workflow','Proposed contract-wrapped workflow','Human-assisted comparator with recorded effort'],
        freezes=['Task/version and train/test split','Structural law and graph convention','Model/provider/prompts/settings','Environment and dependencies','Seeds and scoring rules','Target-specific error tolerance, precision and sample size'],
        fixtures=[dict(name=n,oracle=o,status='not_run') for n,o in fixtures],
        data_scope='Generated SCMs for causal truth; permitted public observational data for workflow stress, without invented truth',
        denominator='All logical requests and all attempts, completions, refusals, failures, uncertainty and costs',
        evidence=[ref(BASE / 'inherited-review-bindings.json','Source and inherited exact examples')], native_execution=False))
    contract = dict(status='proposed_reference_only',
        inputs=['request_id','schema_digest','data_digest','versioned_estimand','population','assignment_outcome_clocks','treatment_versions','assumption_provenance','graph_class','graph_digest','provider_environment','budget_deadline'],
        outputs=['scientific_status','graph_marks_and_lags','variable_matrix_convention','raw_revised_graphs','identification_assumptions','effect_or_set_or_refusal','edit_evidence_and_authority','typed_execution_status','all_attempt_costs'],
        refusal_conditions=['Lost ambiguity or lag meaning','Unavailable identifying information','Unsupported temporal uncertainty','Stale or unauthorized edit','Unknown request completion after timeout','Unestablished deployment rights'],
        native_protocol_verified=False, integration_allowed=False)
    write(BASE / 'conversion-contract.json', contract)
    write(BASE / 'dependency-license-review.json', dict(status='bounded_not_complete',
        inspected=['Root MIT 2026 notice','Vendored causal-learn MIT 2022 notice','Selected requirements and pytest configuration'],
        unresolved=['All transitive dependencies/assets/data/provider terms','Exact environment including unpinned huggingface-hub','Present upstream maintenance and support','Deployment and redistribution rights'],
        agreement_accepted=False, integration_allowed=False,
        evidence=[ref(BASE / 'inherited-review-bindings.json','Authentic declarations and limits')]))
    revisit='Select a supported immutable artifact and complete environment/rights inventory; bind experiment outputs for reproduction claims; implement and preregister graph, temporal, edit, failure and all-request cost contracts; qualify a public/generated prototype before native admission or expensive bank work.'
    choice = dict(operation=OP,candidate='Causal-Copilot name variants',canonical_candidate='Lancelot39/Causal-Copilot documented lineage',
        selected_revision=validation['commit'], selected_version='Historical 15 May 2026 source and separate April 2025 paper',
        decision='reference',reason='Useful workflow decomposition and concrete selected-source findings support architectural comparison; full implementation and qualification are absent.',
        alternatives=[dict(route=r,disposition=d,reason=f) for r,d,f in [
            ('adopt','defer','Complete environment, rights and native scientific/runtime acceptance missing'),
            ('integrate','conditional','Isolated contract boundary after permitted public qualification'),
            ('adapt','conditional','Selected parser/report components need evidence preservation and component rights'),
            ('port','defer','Requires numerical/graph/failure parity and a named maintainer; does not cure authority'),
            ('reference','retain','Use architecture and inspected limits with authentic evidence'),
            ('reject','component_specific','Reject unsupported directional authority and truth-assisted score as sole operational oracle')]],
        owners=[dict(role=r,responsibility=s) for r,s in [('Scientific','Target, assumptions, graph class, uncertainty and score'),('Adapter','Conversion, edit authority, failures and replay'),('Platform/procurement','Environment, rights, provider terms and retention'),('Evaluation','Independent oracles and complete denominators'),('Maintenance','Version drift and semantic parity')]],
        owner_status='Proposed roles, not institutional commitments',
        costs=dict(measured=False,categories=['preparation','all attempts/provider calls','review','maintenance'],illustration=ref(BASE / 'exact-results.json','Authored cost example')),
        maintenance='Current support and exact reproducible environment unresolved',
        alias_boundary='README V1/V2 labels and demo do not constitute distinct qualified engines; unrelated names excluded',
        integration_allowed=False, capabilities=[], revisit_trigger=revisit, limitations=LIMITS)
    write(BASE / 'exact-results.json', exact.calculate())
    write(BASE / 'choice.json', choice)
    write(BASE / 'omissions-register.json', dict(global_blocker=False,next_action=revisit,
        known_routes=['Complete artifact/rights inventory','Finite public graph and failure fixtures','Matched scientific comparison and full-cost study'],
        unknown_without_information=['Assignment truth and omitted causes','Direction in observationally equivalent models','Universal uncertainty over arbitrary dependent observations'],
        independent_remaining=['Generic discovery-agent and diagram-assistant candidates','Remaining census originals and crosscutting coverage'],native_execution=False))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_authored_examples',
        evidence=[ref(Path(exact.__file__),'Independent exact Python'),ref(BASE / 'exact-results.json','Exact set and Fraction results'),ref(BASE / 'development.tex','Explained derivations')],
        findings=['Unresolved, oriented and absent graph sets differ','Both identifier orders are protected','6000/120=50;6000/100=60;6000/80=75;completion5/6 versus admissibility2/3'],native_execution=False))
    authored=dict(integrated_citation_key='exec25_copilot_choice',kind='project_evidence_not_scholarly_paper',
        title='Causal-Copilot reference choice, semantic contract and public qualification design',author='Causal banking proposal project',year=2026,
        source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; cutoff 7 October 2026; retained historical originals',
        local_copy=ref(BASE / 'choice.json','Scoped reuse decision'),
        inspected_anchors=[ref(BASE/n,'Authored bounded analysis') for n in ['identity-review.json','capability-comparison.json','conversion-contract.json','qualification-plan.json','dependency-license-review.json','mathematical-review.json','omissions-register.json']],
        supported_claims=['One documented lineage, one reference decision','Component alternatives and proposed semantic/failure contracts','Public/generated comparison design with unexecuted fixtures','Exact denominator illustration, not a quote or observed performance'],limitations=LIMITS)
    write(BASE / 'source-audit.json',dict(sources=[authored],new_records=1,new_scholarly_pdfs=0,preserved_original_records=4,native_execution=False))
    write(BASE / 'plan-review.json',dict(status='pass_for_scoped_reference_decision',
        evidence=[ref(BASE/n,'Reviewed plan and evidence') for n in ['plan.md','identity-review.json','choice.json','qualification-plan.json','conversion-contract.json','mathematical-review.json']],
        findings=['All three operation criteria covered without enabling integration','Aliases resolved only within documented lineage','Independent scientific, runtime, rights and cost obligations specified','Earlier findings preserved; no paper/source experiment equivalence or native claim','Serialize after previous delivery; preserve all manuscript/source inputs']))
    write(BASE / 'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',
        evidence=[ref(BASE/'development.tex','Connected bank decision and alternatives'),ref(BASE/'sponsor-addition.md','Sponsor implications')],
        findings=['No repeated claim of new original acquisition','Proposed tests distinguished from passing tests','Reference decision distinguished from native qualification'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/n,'Reviewed evidence') for n in ['inherited-review-bindings.json','identity-review.json','capability-comparison.json','qualification-plan.json','conversion-contract.json','dependency-license-review.json','choice.json','omissions-register.json','exact-results.json','mathematical-review.json','source-audit.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review and receipt logic')],
        findings=['Fifteen retained authentic Git blobs revalidated; four inherited citation records retained','One named reference choice; no generic-family or native approval','Exact examples and public qualification route documented'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(review='pass',decision='reference',original_blobs=15,new_records=1,native_execution=False)))


def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed named-lineage proposal reference choice; no native admission',evidence=[ref(BASE/'review.json','Bounded author review')])
    output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed reference decision') for n in ['review.json','choice.json','conversion-contract.json','dependency-license-review.json','qualification-plan.json']]
    findings=['Source, revision, aliases, rights/dependencies and maintenance limits explicit','Target, uncertainty, conversion, alternatives, costs, proposed owners and revisit conditions reviewed','Reference only with public behavioral oracles; integration_allowed false and no capabilities granted']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Named reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result)
    print('Copilot reference receipt prepared.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
