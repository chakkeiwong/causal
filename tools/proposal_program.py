#!/usr/bin/env python3
"""Current proposal scope over the preserved V14 evidence/operation ledger.

This view does not waive a scientific claim's evidence requirements or award
product acceptance. The original controller is deliberately left byte-identical.
"""
import argparse
from collections import Counter
import json
import subprocess
import sys

import build_integrated_monograph_v12 as sources
import causal_program_v14 as ledger
import master_control as core

VALIDATE_LEDGER = ledger.validate_state
BASE = 'docs/program/public-data-v15'


def scope_for(root, state):
    return core.read(root, state['proposal_program']['documents']['scope']['path'])


def validate_state(root, state):
    issues = VALIDATE_LEDGER(root, state)
    try:
        program = state['proposal_program']
        core.bound(root, program['predecessor'])
        for binding in program['documents'].values():
            core.bound(root, binding)
        scope = scope_for(root, state)
        graph = ledger.graph_for(root, state)
        if state['mission'] != scope['mission']:
            raise ValueError('Canonical mission differs from reviewed proposal scope')
        nodes = {n['id']: n for n in graph['nodes']}
        if set(scope['operation_stages']) != set(nodes):
            raise ValueError('Proposal scope drops or invents a preserved operation')
        stages = scope['operation_stages']
        if not set(stages.values()) <= {'proposal_now', 'prototype_optional', 'later_conditional'}:
            raise ValueError('Unknown evidence stage')
        for key, node in nodes.items():
            if stages[key] == 'proposal_now':
                if node['requires_inputs']:
                    raise ValueError('Authentic input incorrectly gates proposal: ' + key)
                if any(stages[d['id']] != 'proposal_now' for d in node['depends']):
                    raise ValueError('Later-stage dependency incorrectly gates proposal: ' + key)
        if set(scope['input_stages']) != {i['id'] for i in state['external_inputs']}:
            raise ValueError('Missing deferred input disposition')
        if scope['proposal_accepted'] is not False or scope['product_accepted'] is not False:
            raise ValueError('Scope correction does not award proposal or product acceptance')
        survey = core.read(root, program['documents']['dataset_register']['path'])
        if len(survey['families']) != 24 or len({r['id'] for r in survey['families']}) != 24:
            raise ValueError('Survey inventory count or identity mismatch')
        if survey['new_fitted_causal_studies'] != 0:
            raise ValueError('A survey/profile cannot award a fitted study')
        audit = core.read(root, program['documents']['source_audit']['path'])
        sources.verify_refs(audit)
        keys = {s['integrated_citation_key'] for s in audit['sources']}
        if any(not set(row['source_keys']) <= keys for row in survey['families']):
            raise ValueError('Dataset has an unaudited source')
    except (KeyError, ValueError, OSError) as exc:
        issues.append(str(exc))
    return issues


def overview(state, graph):
    scope = scope_for(core.ROOT, state)
    stages = scope['operation_stages']
    ready = ledger.ordered_ready(state, graph)
    current = [n for n in ready if stages[n['id']] == 'proposal_now']
    optional = [n for n in ready if stages[n['id']] == 'prototype_optional']
    return {'scope_revision': state['proposal_program']['revision'],
            'preserved_execution_revision': state['revision'],
            'mission': state['mission'], 'controller': 'python3 tools/proposal_program.py',
            'program': state['proposal_program']['documents']['plan']['path'],
            'proposal_accepted': False, 'product_acceptance_is_current_goal': False,
            'current_proposal_gaps': scope['proposal_acceptance'],
            'operation_stages': dict(Counter(stages.values())),
            'ready_proposal_operations': len(current), 'ready_optional_prototype_operations': len(optional),
            'next': current[0]['id'] if current else None,
            'public_evidence_next': scope['public_evidence_queue'],
            'deferred_inputs': scope['input_stages'],
            'public_data': {'surveyed_families': 24, 'new_descriptive_profiles': 1,
                            'inherited_public_studies': 2, 'new_fitted_causal_studies': 0},
            'reader': state['reader'], 'continue': bool(current or optional),
            'automation_scope': 'Scopes, selects and validates evidence records; does not execute scholarly work or award acceptance automatically.'}


def render(root, state):
    view = overview(state, ledger.graph_for(root, state))
    md = f"""# Mission control: causal banking product proposal

The current goal is a scholarly product proposal supported by bounded public/synthetic prototype evidence. Authentic bank validation, production adoption and measured bank ROI are conditional later work, **not proposal blockers**.

[Current master program](program/master-program-proposal.md) · [Public-data survey PDF](program/public-data-v15/public-data-survey.pdf) · [Survey source](program/public-data-v15/survey.md) · [Dataset register](program/public-data-v15/dataset-register.json) · [Scope and plan review](program/public-data-v15/review.md)

[Current integrated working monograph]({state['reader']['path'].removeprefix('docs/')}) — {state['reader']['pages']} pages. All three mandatory software, LLM/agent and integration repairs remain open. The public-data section does not receive duplicate page credit.

The survey covers 24 dataset families. One new public Bank Marketing archive was acquired and descriptively profiled; two earlier public studies are preserved. Six study families are proposed. No new fitted causal study, live LLM score or bank qualification is claimed.

Current commands: `python3 tools/proposal_program.py status`, `next`, `check`. Use `work` to forward a scoped operation to the preserved receipt controller. `tools/program.py` and earlier entrypoints are historical qualification views; their product-gap counts do not measure proposal completion.

{view['ready_proposal_operations']} preserved proposal operations are ready. Next existing lane: **{view['next']}**. Immediate public-evidence continuation: freeze P1's 401(k)/UCI task briefs, admissible alternatives and baseline rubric. P2–P6 design work has independent local/generated routes and does not wait for private bank inputs.

The scope record assigns all 416 operations and all twelve authentic input categories to their proper claim stage. It retains original evidence and product qualification requirements. There are no later-stage dependency edges into the proposal operation graph, no phase stopping points and no checkpoint permission stops.

Proposal acceptance still needs the full manuscript repairs, claim/source review, the scoped prototype evidence portfolio, a developed conditional investment case, sponsor consistency and rendered PDF review. A completed proposal is different from an implemented or accepted product.

The [V14 program](program/master-program-v14.md), [full gap audit](program/comprehensive-v14/gap-audit.md), original receipts and all earlier PDFs remain preserved. Four open mathematical successor arguments remain research obligations; public observations do not prove them.

PDF compilation, citation/source identities and extracted text/page bounds are checked. Rendered visual acceptance is pending a fresh session under the exhausted inherited image allowance in `/home/ubuntu/AGENTS.md`; it affects visual acceptance only.
"""
    (root / 'docs/mission-control.md').write_text(md)
    body = subprocess.run(['pandoc', '--from=gfm', '--to=html'], input=md, capture_output=True, text=True, check=True, timeout=20).stdout
    (root / 'docs/mission-control.html').write_text("<!doctype html><meta charset='utf-8'><title>Causal banking proposal</title>" + body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for cmd in ['status', 'check', 'render']:
        sub.add_parser(cmd)
    p = sub.add_parser('next'); p.add_argument('operation', nargs='?')
    p = sub.add_parser('work'); p.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    state = core.read(core.ROOT, core.STATE)
    issues = validate_state(core.ROOT, state)
    if issues:
        raise SystemExit('; '.join(issues))
    graph = ledger.graph_for(core.ROOT, state)
    if args.command == 'check':
        result = {'status': 'pass', 'issues': [], 'preserved_ledger': 'pass',
                  'proposal_has_no_authentic_input_or_later_stage_dependencies': True,
                  'audited_dataset_families': 24, 'proposal_acceptance': False, 'product_acceptance': False}
    elif args.command == 'status':
        result = overview(state, graph)
    elif args.command == 'render':
        render(core.ROOT, state); result = {'rendered': True}
    elif args.command == 'next':
        view = overview(state, graph)
        key = args.operation or view['next']
        node = ledger.operation(graph, key) if key else None
        result = {'public_evidence_continuation': view['public_evidence_next'],
                  'existing_operation': node,
                  'stage': scope_for(core.ROOT, state)['operation_stages'].get(key),
                  'blockers': ledger.blockers(state, node) if node else [],
                  'rule': 'Execute true prerequisites; a local branch failure or phase boundary does not stop independent work.'}
    else:
        if not args.arguments or args.arguments[0] not in ['next', 'template', 'progress', 'register', 'record', 'block', 'resume', 'package', 'deliver', 'intake']:
            raise SystemExit('Use work with a preserved evidence-controller command')
        ledger.validate_state = validate_state
        ledger.render = render
        ledger.overview = overview
        sys.argv = [sys.argv[0]] + args.arguments
        ledger.main()
        return
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
