#!/usr/bin/env python3
"""Install the reviewed execution supplement once; retain all existing contracts."""
import argparse
import copy
import json
from pathlib import Path

import run_program as runtime
from run_program import core, ledger, proposal


def prepare(root, state):
    scope = proposal.scope_for(root, state)
    graph = ledger.graph_for(root, state)
    nodes = []
    details = {
        'P1.DESIGN': ['Freeze distinct eligibility ATE, participation IV/LATE and UCI prediction/effect briefs, information clocks and admissible alternatives.',
                      'Bind local data/docs; freeze a deterministic schema baseline and ambiguity/refusal rubric; disclose development exposure and no live-model claim.'],
        'P2.DESIGN': ['Inspect FDIC dictionary and release-vintage evidence, define extract fields and institution/branch continuity, and retain unresolved vintage claims.',
                      'Provide an executable local/generated fallback design independent of FDIC availability; separate description from identification.'],
        'P3.DESIGN': ['Specify a fully generated known-truth assignment/outcome law, estimands, matched baselines, uncertainty and failure metrics.',
                      'Freeze independent evaluation, resource limits and prospective registration requirements; optional ACIC rights/NSW provenance cannot block generated work.'],
        'P4.DESIGN': ['Specify sequential history, action, censoring and outcome laws with known support and independent policy training/evaluation.',
                      'Define fixed and learned policy comparisons, positivity stress, censoring handling and final-study registration requirements.'],
        'P5.DESIGN': ['Specify observationally equivalent graph cases and generated identity corruptions; separate hidden truth from analysis inputs.',
                      'Freeze graph/effect-set/linkage metrics, harmful false certainty checks, development/final splits and registration requirements.'],
        'P6.DESIGN': ['Freeze public/generated agent tasks, provenance, task-family splits, ambiguity rubric and deterministic/template baselines.',
                      'Separate offline checks from live-model evaluation; record optional custody, budget, contamination and adjudication requirements.']}

    def node(key, lane, title, action, outputs, criteria, depends=()):
        return {'id': key, 'lane': lane, 'parents': ['I02'], 'title': title,
                'action': action, 'outputs': outputs, 'criteria': criteria,
                'depends': [{'id': d, 'outcomes': ['pass']} for d in depends],
                'requires_inputs': [], 'capabilities': [], 'study': False, 'priority': 10,
                'owner_role': 'Author; no independent or institutional acceptance implied',
                'evidence_start': [], 'failure_action': 'Record observed limits and exact continuation; continue independent work.'}

    for task in scope['public_evidence_queue']:
        nodes.append(node(task['id'], 'public_evidence', task['next_action'], task['next_action'],
                          [task['output']], details[task['id']]))
    deps = {
        'Q1': [n['id'] for n in graph['nodes'] if n['id'].startswith('TEXT.REVIEW.')],
        'Q2': [],
        'Q3': [f'P{i}.DESIGN' for i in range(1, 7)],
        'Q4': ['ECON.DESIGN'],
        'Q5': ['PROPOSAL.Q' + str(i) for i in range(1, 5)] + ['RELEASE.RECONCILE', 'RELEASE.VISUAL']}
    criteria = {
        'Q1': ['Review MR01/MR02/MR03 against all 102 software cells, 14 LLM tasks, 12 integration requirements and 22 chapter allocations, including substantive depth and no duplicated page credit.'],
        'Q2': ['Review every cited source and capability on the exact current reader; primary technical anchors, real paper PDFs, supported claims, alternatives and omissions are traceable with no essential unreviewed claim.'],
        'Q3': ['Review the bounded portfolio against actual manuscript claims: every claimed executed demonstration has reproduced evidence and retained failures; plans and public/synthetic truth are labeled; design approval alone is insufficient.'],
        'Q4': ['Review developed baseline/cost/risk/value-of-information scenarios and a decision-relevant conditional next experiment; author assumptions are labeled and no bank ROI is asserted.'],
        'Q5': ['Reconcile sponsor, all proposal gates, exact compiled monograph and actual rendered inspection; no unresolved essential claim/source/coverage/layout finding remains.']}
    for q in scope['proposal_acceptance']:
        key = 'PROPOSAL.' + q['id']
        nodes.append(node(key, 'proposal_acceptance', q['requirement'], q['requirement'],
                          [runtime.BASE + '/acceptance/' + q['id'] + '.json'], criteria[q['id']], deps[q['id']]))
    contracts = {'schema_version': 1, 'scope': 'Proposal execution supplement, not a replacement research program',
                 'evidence': [runtime.bind(root, state['proposal_program']['documents']['scope']['path'], 'Preserved proposal scope and P1–P6 queue')],
                 'nodes': nodes}
    path = root / runtime.CONTRACTS
    if path.exists():
        ledger.require(core.read(root, runtime.CONTRACTS) == contracts, 'Do not overwrite a changed contract')
    else:
        core.write(path, contracts)
    return contracts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'install'])
    args = parser.parse_args()
    root = core.ROOT
    state = core.read(root, core.STATE)
    before = core.sha(root / core.STATE)
    ledger.require('execution_runtime' not in state, 'Runtime is already installed')
    ledger.require(not proposal.validate_state(root, state), 'Predecessor validation failed')
    contracts = prepare(root, state)
    if args.command == 'prepare':
        print(json.dumps({'contracts': runtime.CONTRACTS, 'new_tasks': len(contracts['nodes'])})); return
    verification = core.read(root, runtime.BASE + '/verification.json')
    ledger.require(verification['status'] == 'pass', 'Repair tests must pass before install')
    for evidence in verification['artifacts']:
        core.bound(root, evidence)
    snapshot = runtime.BASE + '/pre-install-state.json'
    if (root / snapshot).exists():
        ledger.require(core.read(root, snapshot) == state, 'Preinstall state changed')
    else:
        core.write(root / snapshot, state)
    installation = {'date': core.now(), 'predecessor': runtime.bind(root, snapshot, 'Full pre-repair canonical state'),
                    'verification': runtime.bind(root, runtime.BASE + '/verification.json', 'Regression checks and exact tested code'),
                    'controller': runtime.bind(root, 'tools/run_program.py', 'Installed runtime code; preserved release copy below'),
                    'claim': 'Execution control repaired; no scholarly operation or proposal acceptance awarded by installation'}
    # A future control update preserves this release copy; the entrypoint stays stable.
    release = runtime.BASE + '/releases/runtime-' + installation['controller']['sha256'] + '.py'
    core.safe(root, release).parent.mkdir(parents=True, exist_ok=True)
    core.safe(root, release).write_bytes((root / 'tools/run_program.py').read_bytes())
    installation['controller'] = runtime.bind(root, release, 'Exact tested runtime at installation')
    core.write(root / runtime.BASE / 'installation.json', installation)
    state['execution_runtime'] = {'schema_version': 1,
        'contracts': runtime.bind(root, runtime.CONTRACTS, 'P1–P6 and Q1–Q5 operation contracts'),
        'installation': runtime.bind(root, runtime.BASE + '/installation.json', 'Reviewed repair installation'),
        'results': {}, 'registrations': {}, 'blocks': {}, 'progress': {}, 'turns': [], 'active': None}
    runtime.commit(root, before, state, {'action': 'install_unified_proposal_execution', 'new_tasks': len(contracts['nodes']),
                                       'preserved_operations': 416, 'automatic_acceptance': False})
    print(json.dumps(runtime.status(root, state), indent=2))


if __name__ == '__main__':
    main()
