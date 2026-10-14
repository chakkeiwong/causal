#!/usr/bin/env python3
"""Bounded observations of the preserved local custody implementation.

Generated fixtures only. This script does not patch the implementation or
establish authentication, bank provenance, or remote attack reachability.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-14/artifact-custody'
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'tests'))


def observe():
    from causalbank.artifacts_v12 import ArtifactStore, atomic, bounded_read, digest, encode
    from causalbank.operation_contract_v12 import context_digest
    from causalbank.operation_service_v12 import OperationService
    from causalbank.runtime_v12 import Runtime, execution_identity
    from test_operation_service_v12 import context, request

    rows = []

    def refused(name, action, fragment):
        try:
            value = action()
        except (ValueError, OSError) as exc:
            assert fragment in str(exc), (name, str(exc))
            rows.append({'case': name, 'observation': 'refused',
                         'exception': type(exc).__name__, 'message': str(exc)})
        else:
            raise AssertionError((name, 'unexpected acceptance', value))

    (ROOT / '.runtime').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='custody-review-', dir=ROOT / '.runtime') as tmp:
        root = Path(tmp)
        service = OperationService(root)
        store = service.store
        value = {'balance': 100, 'unit': 'USD'}
        first = store.put(value, 'generated-account/1', 'generated_account')
        assert store.get(first) == value
        assert store.put(value, 'generated-account/1', 'generated_account') == first
        other_role = store.put(value, 'generated-account/1', 'illustration')
        assert other_role['sha256'] == first['sha256']
        assert other_role['artifact_id'] != first['artifact_id']
        rows.append({'case': 'roundtrip_and_role_binding', 'observation': 'pass',
                     'value': value, 'first_reference': first, 'other_role_reference': other_role})

        changed = store.put({'x': 1}, 'probe/1', 'changed_bytes')
        atomic(store.folder / (changed['artifact_id'] + '.json'), {'x': 2})
        refused('changed_bytes', lambda: store.get(changed), 'changed from declared identity')

        meta = store.put({'x': 1}, 'probe/1', 'changed_metadata')
        atomic(store.folder / (meta['artifact_id'] + '.meta'), {**meta, 'custody': 'another_operator'})
        refused('changed_metadata', lambda: store.get(meta), 'metadata or custody mismatch')

        scientific = context()
        payload = {'context_sha256': context_digest(scientific), 'quadratics': [[1, 0, 1]]}
        qref = store.put(payload, 'quadratic-bounds/1', 'quadratic_bounds')
        q = request('sensitivity.evaluate', {'family_id': 'quadratic-sublevel'}, ctx=scientific, refs=[qref])
        q['budget'] = {'wall_seconds': 8, 'memory_bytes': 1024**3,
                       'max_output_bytes': 100000, 'model_calls': 0}
        response = service.invoke(q)
        assert response['result']['coordinate_sets'][0]['topology'] == 'empty'
        wrong = copy.deepcopy(q)
        wrong['scientific_context']['horizon']['value'] = 24
        refused('changed_horizon_context', lambda: service.invoke(wrong), 'another scientific context')
        runtime = Runtime(root)
        unavailable = runtime.invoke(wrong)
        assert unavailable['status'] == 'failed' and unavailable['disposition'] == 'unavailable'
        assert unavailable['result'] is None and unavailable['error']['code'] == 'invalid_or_unavailable_input'
        rows.append({'case': 'runtime_context_failure_is_not_empty_set', 'observation': 'pass',
                     'original_request': q, 'original_response': response,
                     'changed_request': wrong, 'changed_response': unavailable})

        for case, schema, role, message in [
            ('wrong_role', 'quadratic-bounds/1', 'observation_rows', 'Exactly one authorized'),
            ('wrong_schema', 'quadratic-bounds/99', 'quadratic_bounds', 'Unsupported input artifact schema'),
        ]:
            altered = store.put(payload, schema, role)
            altered_request = copy.deepcopy(q)
            altered_request['artifact_inputs'] = [altered]
            refused(case, lambda: service.invoke(altered_request), message)

        refused('read_size_limit', lambda: store.get(first, limit=1), 'bounded regular file')
        refused('nonfinite_json', lambda: store.put({'x': float('nan')}, 'probe/1', 'probe'), 'finite')
        link = root / 'root-link'
        link.symlink_to(store.root, target_is_directory=True)
        refused('symlink_root', lambda: ArtifactStore(link), 'nonsymlink')
        safe = store.put({'x': 'safe'}, 'probe/1', 'symlink_content')
        content = store.folder / (safe['artifact_id'] + '.json')
        content.unlink()
        content.symlink_to(store.folder / (first['artifact_id'] + '.json'))
        refused('symlink_content', lambda: store.get(safe), 'Too many levels of symbolic links')

        q['idempotency_key'] = 'generated-custody-replay'
        initial = runtime.invoke(q)
        assert initial['status'] == 'completed'
        replay_request = copy.deepcopy(q)
        replay_request['request_id'] = 'fresh-correlation'
        replay = runtime.invoke(replay_request)
        assert replay == {**initial, 'request_id': 'fresh-correlation'}
        conflict_request = copy.deepcopy(replay_request)
        conflict_request['scientific_context']['horizon']['value'] = 24
        conflict = runtime.invoke(conflict_request)
        assert conflict['error']['code'] == 'idempotency_conflict'
        atomic(store.folder / (qref['artifact_id'] + '.json'), {**payload, 'quadratics': [[-1, 0, -1]]})
        stale = runtime.invoke(replay_request)
        assert stale['error']['code'] == 'artifact_access' and stale['result'] is None
        rows.append({'case': 'replay_and_pre_replay_recheck', 'observation': 'pass',
                     'initial': initial, 'replay': replay,
                     'context_conflict': conflict, 'changed_input_refusal': stale})

        trusted = store.put({'balance': 100}, 'probe/1', 'coherent_rewrite')
        replacement = {'balance': 900}
        data = encode(replacement)
        supplied = {**trusted, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        atomic(store.folder / (trusted['artifact_id'] + '.json'), replacement)
        atomic(store.folder / (trusted['artifact_id'] + '.meta'), supplied)
        refused('coherent_rewrite_old_trusted_reference', lambda: store.get(trusted), 'metadata or custody mismatch')
        accepted = store.get(supplied)
        assert accepted == replacement
        derived = 'a' + digest({k: v for k, v in supplied.items() if k != 'artifact_id'})
        assert derived != supplied['artifact_id']
        rows.append({'case': 'coherent_rewrite_new_supplied_reference', 'observation': 'accepted',
                     'original_reference': trusted, 'replacement_reference': supplied,
                     'returned_value': accepted, 'recomputed_artifact_id': derived,
                     'limitation': 'Local writer replaced content, metadata and supplied reference; outside single-operator trust scope.'})

        fifo = root / 'untrusted-type.fifo'
        os.mkfifo(fifo, 0o600)
        process = subprocess.Popen([sys.executable, '-u', str(Path(__file__).resolve()),
                                    'fifo-child', str(fifo)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, cwd=ROOT)
        try:
            ready, _, _ = select.select([process.stdout], [], [], 10)
            assert ready and process.stdout.readline().strip() == 'before_bounded_read'
            started = time.monotonic()
            try:
                out, err = process.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                process.terminate()
                out, err = process.communicate(timeout=2)
                rows.append({'case': 'fifo_without_writer', 'observation': 'blocked_until_terminated',
                             'deadline_seconds': 1, 'elapsed_seconds': round(time.monotonic() - started, 4),
                             'returncode_after_termination': process.returncode,
                             'stdout_after_ready': out, 'stderr': err,
                             'limitation': 'Actual local file-type boundary, not remote exposure or platform-wide timing evidence.'})
            else:
                raise AssertionError(('FIFO unexpectedly returned', process.returncode, out, err))
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate(timeout=2)

    return {'kind': 'actual_local_generated_fixture_observations', 'implementation_changed': False,
            'execution_identity': execution_identity(), 'cases': rows,
            'count': len(rows), 'public_or_bank_data_used': False,
            'claims': ['Selected byte/reference/context mutations and replay refusals observed.',
                       'Coherently replaced local reference is accepted under an inconsistent derived handle.',
                       'FIFO open can block before the regular-file check; subprocess was terminated.'],
            'limitations': ['No authentication, tenant isolation, bank provenance, rights, retention or deletion qualification.',
                           'Scientific premises are supplied declarations; hashes do not verify them.',
                           'Single local environment and deterministic cases, not empirical reliability rates.']}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'fifo-child':
        from causalbank.artifacts_v12 import bounded_read
        print('before_bounded_read', flush=True)
        bounded_read(Path(sys.argv[2]))
        return
    from publish_latent_r_review_v2_20261013 import ref, write
    observations = observe()
    observations['procedure'] = ref(Path(__file__).resolve(), 'Bounded cases and deterministic generated inputs')
    write(BASE / 'local-observations.json', observations)
    print(json.dumps({'cases': observations['count'], 'negative_boundaries': 2,
                      'receipt': str((BASE / 'local-observations.json').relative_to(ROOT))}))


if __name__ == '__main__':
    main()
