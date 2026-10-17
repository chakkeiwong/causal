#!/usr/bin/env python3
"""Preserved proposal controller plus immutable successors to negative chapter reviews.

The original controller and operation contracts remain unchanged. Successors
satisfy the same chapter contract using versioned outputs. No review is awarded
by installing this extension, and no manuscript failure is erased.
"""
import argparse
import copy
from pathlib import Path
import sys
import json
import run_program as base

_original_combined = base.combined
_original_validate_state = base.validate_state
_original_validate_receipt = base.validate_receipt
_original_status = base.status
_original_render = base.render
FIELD = 'chapter_review_successors'


def combined(root, state):
    graph, merged, stages = _original_combined(root, state)
    for identifier, records in state['execution_runtime'].get(FIELD, {}).items():
        if records:
            merged['execution_program']['results'][identifier] = copy.deepcopy(records[-1]['result'])
    return graph, merged, stages


def validate_receipt(root, state, node, receipt, sequence):
    if node['id'].startswith('TEXT.REVIEW.') and receipt.get('review_attempt', 0):
        base.require(receipt.get('operation_contract_sha256') == base.core.digest_object(node),
                     'Chapter successor changed the original contract')
        adapted = dict(node, outputs=base.review_output_paths(node, receipt.get('reviewed_reader', {}), receipt['review_attempt']))
        adjusted = dict(receipt, operation_contract_sha256=base.core.digest_object(adapted))
        return base.ledger.validate_operation_receipt(root, state, adapted, adjusted, sequence)
    return _original_validate_receipt(root, state, node, receipt, sequence)


def validate_successors(root, state):
    graph, merged, stages = combined(root, state)
    for identifier, records in state['execution_runtime'].get(FIELD, {}).items():
        base.require(identifier.startswith('TEXT.REVIEW.') and stages.get(identifier) == 'proposal_now',
                     'Only proposal chapter reviews admit this successor path')
        node = base.ledger.operation(graph, identifier)
        previous = state['execution_program']['results'].get(identifier)
        base.require(previous is not None and previous['outcome'] in ('negative', 'inconclusive'),
                     'Chapter successor requires an actual negative or inconclusive original')
        base.require(isinstance(records, list) and records, 'Empty chapter successor history')
        for attempt, record in enumerate(records, 1):
            base.require(previous['outcome'] in ('negative', 'inconclusive'), 'A passing chapter cannot be silently replaced')
            binding = record['result']; base.core.bound(root, binding)
            receipt = base.core.read(root, binding['path'])
            base.require(receipt.get('prior_result') == previous, 'Chapter successor lost its predecessor')
            base.core.bound(root, previous)
            base.require(receipt.get('review_attempt') == attempt, 'Chapter successor attempt mismatch')
            base.require(binding['outcome'] == receipt['outcome'] and binding.get('capabilities', []) == receipt.get('capabilities', []), 'Chapter successor state/receipt mismatch')
            base.require(receipt['outcome'] != 'pass' or receipt['execution'] == 'performed', 'Passing chapter work must be performed')
            base.core.bound(root, receipt.get('reviewed_reader', {}))
            validate_receipt(root, merged, node, receipt, binding['sequence'])
            for output in receipt.get('outputs', []): base.core.bound(root, output)
            if receipt['outcome'] == 'pass':
                review = base.core.read(root, receipt['outputs'][0]['path'])
                allocation = next(x['body_pages'] for x in base.core.read(root, 'docs/program/repair-v12/chapter-plan.json')['chapters'] if identifier == 'TEXT.REVIEW.'+x['id'])
                credit = sum(x['credit'] for x in review['per_page'])
                base.require(review.get('operation_id') == identifier and review.get('status') == 'pass', 'Chapter output identity/outcome mismatch')
                base.require(base.same_reader(review.get('reviewed_reader', {}), receipt['reviewed_reader']), 'Chapter output reader mismatch')
                base.require(review.get('allocation') == allocation and review.get('substantive_page_credit') == credit and credit >= allocation['min'], 'Chapter successor has insufficient exclusive depth')
                base.require(all(0 <= x['credit'] <= 1 and x.get('rationale') for x in review['per_page']), 'Chapter depth requires bounded per-page reasons')
                base.require(len({x['printed_page'] for x in review['per_page']}) == len(review['per_page']), 'Duplicate chapter page credit')
            previous = binding


def validate_state(root, state):
    issues = _original_validate_state(root, state)
    try: validate_successors(root, state)
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as exc: issues.append(str(exc))
    return issues


def record_chapter(root, state, identifier, path):
    base.require(state['execution_runtime']['active'] is None, 'Finish or yield the active task before recording a chapter successor')
    graph, merged, stages = combined(root, state)
    base.require(identifier.startswith('TEXT.REVIEW.') and stages.get(identifier) == 'proposal_now', 'Only proposal chapter reviews admit this successor path')
    node = base.ledger.operation(graph, identifier)
    base.require(not base.ledger.blockers(merged, node, include_protocol=False), 'Chapter prerequisites remain unmet')
    previous = merged['execution_program']['results'].get(identifier)
    base.require(previous is not None and previous['outcome'] in ('negative', 'inconclusive'), 'Only a negative or inconclusive chapter can be repaired')
    receipt = base.core.read(root, path)
    base.require(receipt.get('prior_result') == previous, 'Chapter successor lost its predecessor')
    base.require(base.same_reader(receipt.get('reviewed_reader', {}), state['reader']), 'Chapter successor is for a stale reader')
    attempt = len(state['execution_runtime'].get(FIELD, {}).get(identifier, []))+1
    base.require(receipt.get('review_attempt') == attempt, 'Chapter successor attempt mismatch')
    candidate = copy.deepcopy(state)
    binding = base.bind(root, path, 'Preserving chapter review successor')
    binding.update(sequence=len(state['execution_program']['turns']),outcome=receipt['outcome'],capabilities=receipt.get('capabilities', []))
    candidate['execution_runtime'].setdefault(FIELD, {}).setdefault(identifier, []).append({'result':binding})
    validate_successors(root, candidate)
    state['execution_runtime'][FIELD] = candidate['execution_runtime'][FIELD]
    return dict(action='chapter_review_successor',operation=identifier,receipt=binding,prior_result=previous)


def status(root, state):
    result = _original_status(root, state)
    result['controller'] = 'python3 tools/run_program_reviews_v2.py'
    result['chapter_successors'] = {k:len(v) for k,v in state['execution_runtime'].get(FIELD, {}).items()}
    return result


def render(root, state):
    _original_render(root, state)
    for name in ['docs/mission-control.md','docs/mission-control.html']:
        path=root/name
        path.write_text(path.read_text().replace('tools/run_program.py','tools/run_program_reviews_v2.py'))


# In-memory extension only; frozen predecessor source is never rewritten.
base.combined=combined
base.validate_receipt=validate_receipt
base.validate_state=validate_state
base.status=status
base.render=render


def main():
    if len(sys.argv)>1 and sys.argv[1]=='chapter-record':
        parser=argparse.ArgumentParser(description=__doc__)
        parser.add_argument('command');parser.add_argument('operation');parser.add_argument('--receipt',required=True)
        args=parser.parse_args()
        state=base.core.read(base.core.ROOT,base.core.STATE)
        base.require(not (issues:=validate_state(base.core.ROOT,state)), '; '.join(issues))
        before=base.core.sha(base.core.ROOT/base.core.STATE)
        event=record_chapter(base.core.ROOT,state,args.operation,args.receipt)
        base.commit(base.core.ROOT,before,state,event)
        print(json.dumps(dict(action='chapter-record',operation=args.operation,reader=state['reader'],proposal_accepted=status(base.core.ROOT,state)['proposal_accepted'])))
    else:base.main()


if __name__=='__main__':main()
