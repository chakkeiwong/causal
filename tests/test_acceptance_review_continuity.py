"""A changed reader must be reviewable without rewriting accepted evidence."""
import copy

import pytest

from test_run_program import workspace, receipt, transition, run


def set_reader(root, state, name):
    (root / name).write_bytes(b'%PDF-1.4\n' + name.encode())
    state['reader'] = run.bind(root, name, 'Test reader identity')


def review_receipt(root, state, key, attempt=0):
    if attempt == 0:
        path = receipt(root, state, key)
        data = run.core.read(root, path)
    else:
        graph, _, _ = run.combined(root, state)
        node = run.ledger.operation(graph, key)
        data = run.ledger.receipt_template(node)
        target = run.review_output_paths(node, state['reader'], attempt)[0]
        run.core.write(root / target, {'reader': state['reader'], 'review_attempt': attempt})
        refs = [run.bind(root, target, 'Reviewed new reader')]
        data.update(outcome='pass', execution='performed', scope='Test review',
                    reviewer={'name': 'test author', 'kind': 'author'}, outputs=refs,
                    criteria=[{'index': 0, 'verdict': 'pass', 'finding': 'Reviewed', 'evidence': refs}])
        path = 'receipts/' + key + '-attempt-' + str(attempt) + '.json'
    data.update(acceptance_scope='proposal_only', reviewed_reader=copy.deepcopy(state['reader']),
                review_attempt=attempt)
    run.core.write(root / path, data)
    return path


def reopening_note(root, state, key):
    old = state['execution_runtime']['results'][key]
    note = {'reason': 'Review changed reader with preserved earlier evidence',
            'next_action': 'Inspect new reader claims and evidence',
            'prior_result': copy.deepcopy(old), 'reviewed_reader': copy.deepcopy(state['reader']),
            'evidence': [state['reader']]}
    run.core.write(root / 'reopen.json', note)
    return 'reopen.json'


def test_acceptance_can_follow_new_reader_without_overwriting_old(workspace):
    root, state = workspace
    transition(root, state, 'record', 'OLD', receipt(root, state, 'OLD'))
    set_reader(root, state, 'book-one.pdf')
    old_path = review_receipt(root, state, 'PROPOSAL.Q2')
    transition(root, state, 'record', 'PROPOSAL.Q2', old_path)
    old_result = copy.deepcopy(state['execution_runtime']['results']['PROPOSAL.Q2'])
    old_bytes = (root / old_path).read_bytes()
    old_output = (root / 'out/q2.json').read_bytes()
    set_reader(root, state, 'book-two.pdf')
    transition(root, state, 'reopen', 'PROPOSAL.Q2', reopening_note(root, state, 'PROPOSAL.Q2'))
    assert run.status(root, state)['active']['operation'] == 'PROPOSAL.Q2'
    assert not run.status(root, state)['proposal_accepted']
    transition(root, state, 'record', 'PROPOSAL.Q2', review_receipt(root, state, 'PROPOSAL.Q2', 1))
    assert state['execution_runtime']['review_history']['PROPOSAL.Q2'][0]['result'] == old_result
    assert (root / old_path).read_bytes() == old_bytes
    assert (root / 'out/q2.json').read_bytes() == old_output
    assert next(x for x in run.status(root, state)['proposal_gaps'] if x['id'] == 'Q2')['status'] == 'pass'
    graph, merged, _ = run.combined(root, state)
    run.validate_review_binding(root, merged, graph, 'PROPOSAL.Q2', old_result)
    run.validate_review_binding(root, merged, graph, 'PROPOSAL.Q2', state['execution_runtime']['results']['PROPOSAL.Q2'])
    (root / 'out/q2.json').write_text('changed old review')
    with pytest.raises(ValueError):
        run.validate_review_binding(root, merged, graph, 'PROPOSAL.Q2', old_result)


def test_current_passing_review_cannot_be_reopened(workspace):
    root, state = workspace
    transition(root, state, 'record', 'OLD', receipt(root, state, 'OLD'))
    set_reader(root, state, 'book.pdf')
    transition(root, state, 'record', 'PROPOSAL.Q2', review_receipt(root, state, 'PROPOSAL.Q2'))
    with pytest.raises(ValueError, match='already passes this reader'):
        transition(root, state, 'reopen', 'PROPOSAL.Q2', reopening_note(root, state, 'PROPOSAL.Q2'))


def test_reopen_never_waives_ordinary_completion_or_evidence(workspace):
    root, state = workspace
    path = receipt(root, state, 'P1.DESIGN')
    transition(root, state, 'record', 'P1.DESIGN', path)
    with pytest.raises(ValueError, match='proposal acceptance'):
        transition(root, state, 'reopen', 'P1.DESIGN', path)


def test_reopen_requires_actual_current_reader_and_prior_receipt(workspace):
    root, state = workspace
    transition(root, state, 'record', 'OLD', receipt(root, state, 'OLD'))
    set_reader(root, state, 'book.pdf')
    transition(root, state, 'record', 'PROPOSAL.Q2', review_receipt(root, state, 'PROPOSAL.Q2'))
    set_reader(root, state, 'new-book.pdf')
    note_path = reopening_note(root, state, 'PROPOSAL.Q2')
    note = run.core.read(root, note_path)
    note['prior_result']['sha256'] = '0' * 64
    run.core.write(root / note_path, note)
    before = copy.deepcopy(state)
    with pytest.raises(ValueError):
        transition(root, state, 'reopen', 'PROPOSAL.Q2', note_path)
    assert state == before


def test_previous_final_review_replays_when_its_prerequisite_is_reopened(workspace):
    root, state = workspace
    contract = run.core.read(root, 'contracts.json')
    next(n for n in contract['nodes'] if n['id'] == 'PROPOSAL.Q5')['depends'] = [
        {'id': 'PROPOSAL.Q2', 'outcomes': ['pass']}]
    run.core.write(root / 'contracts.json', contract)
    transition(root, state, 'record', 'OLD', receipt(root, state, 'OLD'))
    set_reader(root, state, 'first.pdf')
    for number in range(1, 6):
        key = 'PROPOSAL.Q' + str(number)
        transition(root, state, 'record', key, review_receipt(root, state, key))
    assert run.status(root, state)['proposal_accepted']
    old_final = copy.deepcopy(state['execution_runtime']['results']['PROPOSAL.Q5'])
    set_reader(root, state, 'second.pdf')
    assert not run.status(root, state)['proposal_accepted']
    assert 'PROPOSAL.Q2' in run.status(root, state)['review_reopen_candidates']
    transition(root, state, 'reopen', 'PROPOSAL.Q2', reopening_note(root, state, 'PROPOSAL.Q2'))
    graph, merged, _ = run.combined(root, state)
    run.validate_review_binding(root, merged, graph, 'PROPOSAL.Q5', old_final)
    assert not run.status(root, state)['proposal_accepted']


def test_repeated_review_cannot_reuse_previous_output_path(workspace):
    root, state = workspace
    transition(root, state, 'record', 'OLD', receipt(root, state, 'OLD'))
    set_reader(root, state, 'old.pdf')
    old_path = review_receipt(root, state, 'PROPOSAL.Q2')
    old_data = run.core.read(root, old_path)
    transition(root, state, 'record', 'PROPOSAL.Q2', old_path)
    set_reader(root, state, 'new.pdf')
    transition(root, state, 'reopen', 'PROPOSAL.Q2', reopening_note(root, state, 'PROPOSAL.Q2'))
    new_path = review_receipt(root, state, 'PROPOSAL.Q2', 1)
    new_data = run.core.read(root, new_path)
    new_data['outputs'] = old_data['outputs']
    run.core.write(root / new_path, new_data)
    with pytest.raises(ValueError, match='declared deliverable'):
        transition(root, state, 'record', 'PROPOSAL.Q2', new_path)
    assert 'PROPOSAL.Q2' not in state['execution_runtime']['results']


def test_nonexecuted_negative_review_preserves_missing_prerequisites(workspace):
    root, state = workspace
    set_reader(root, state, 'book.pdf')
    path = review_receipt(root, state, 'PROPOSAL.Q1')
    data = run.core.read(root, path)
    data.update(outcome='inconclusive', execution='not_performed',
                nonexecution_reason='Chapter evidence absent', revisit_trigger='Reviewed chapters supplied')
    data['criteria'][0]['verdict'] = 'inconclusive'
    run.core.write(root / path, data)
    transition(root, state, 'record', 'PROPOSAL.Q1', path)
    graph, merged, _ = run.combined(root, state)
    binding = state['execution_runtime']['results']['PROPOSAL.Q1']
    run.validate_review_binding(root, merged, graph, 'PROPOSAL.Q1', binding)
    assert binding['prerequisites'] == {}
    assert not run.status(root, state)['proposal_accepted']


def test_same_reader_negative_review_can_follow_repair(workspace):
    root, state = workspace
    transition(root, state, 'record', 'OLD', receipt(root, state, 'OLD'))
    set_reader(root, state, 'book.pdf')
    path = review_receipt(root, state, 'PROPOSAL.Q2')
    data = run.core.read(root, path)
    data['outcome'] = data['criteria'][0]['verdict'] = 'negative'
    run.core.write(root / path, data)
    transition(root, state, 'record', 'PROPOSAL.Q2', path)
    transition(root, state, 'reopen', 'PROPOSAL.Q2', reopening_note(root, state, 'PROPOSAL.Q2'))
    transition(root, state, 'record', 'PROPOSAL.Q2', review_receipt(root, state, 'PROPOSAL.Q2', 1))
    assert state['execution_runtime']['review_history']['PROPOSAL.Q2'][0]['result']['outcome'] == 'negative'
