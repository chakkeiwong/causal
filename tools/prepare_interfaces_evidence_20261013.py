#!/usr/bin/env python3
"""Check the exact printed I2 example and bind implementation/claim evidence."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/interfaces'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I2/chapter.tex'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'anchor': anchor}


def write(path, value):
    if path.exists():
        raise ValueError('Preserve prior evidence: ' + str(path))
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def main():
    printed = BASE / 'printed-listings'
    work = ROOT / '.runtime/interface-i2-printed-20261013'
    printed.mkdir(); work.mkdir()
    blocks = re.findall(r'\\begin\{lstlisting\}\[language=Python\]\n(.*?)\\end\{lstlisting\}',
                        CHAPTER.read_text(), re.S)
    assert len(blocks) == 2
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src'), 'OPENBLAS_NUM_THREADS': '1',
           'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'}
    python = ROOT / '.runtime/in04/bin/python'
    for block, name in zip(blocks, ['offer_request.py', 'client.py']):
        script = printed / name
        script.write_text(block)
        subprocess.run([str(python), str(script)], cwd=work, env=env, capture_output=True, check=True, timeout=18)
    request = json.loads((work / 'request.json').read_text())
    response = json.loads((work / 'response.json').read_text())
    frozen_request = json.loads((BASE / 'examples/requests/backdoor.json').read_text())
    frozen_response = json.loads((BASE / 'examples/results/backdoor.json').read_text())['library']
    env['CAUSALBANK_STATE_ROOT'] = str(work / '.runtime/offer-client')
    cli = subprocess.run([str(python), '-m', 'causalbank.cli_v12', 'operation', 'identify.effect',
                          '--input', 'request.json'], cwd=work, env=env, text=True,
                         capture_output=True, check=True, timeout=18)
    cli_response = json.loads(cli.stdout)
    checks = {'printed_request_matches_frozen_request': request == frozen_request,
              'printed_library_matches_frozen_response': response == frozen_response,
              'printed_cli_matches_library': cli_response == response}
    write(printed / 'request.json', request)
    write(printed / 'response.json', response)
    write(printed / 'review.json', {'status': 'pass' if all(checks.values()) else 'fail', 'checks': checks,
          'listing_hashes': [hashlib.sha256(b.encode()).hexdigest() for b in blocks],
          'evidence': [ref(printed / n, 'Exact printed executable example') for n in
                       ['offer_request.py', 'client.py', 'request.json', 'response.json']],
          'scope': 'One displayed identification example; no MCP execution or performance claim'})
    assert all(checks.values())

    anchors = {
        'runtime_v12.py': 'Runtime.invoke, _run_sync, _replay_or_run, _submit_report, resume, _job_query, _report_worker, execution_identity',
        'operation_service_v12.py': '_identify, _estimate, _sensitivity, _audit, validate_request; method and premise boundaries',
        'operation_contract_v12.py': 'validate_context, context_digest, validate_set, validate_response',
        'artifacts_v12.py': 'encode, digest, local_root, bounded_read, ArtifactStore.put/get, atomic',
        'cli_v12.py': 'read_request, state_root and main exception/exit branches',
        'mcp_server_v12.py': 'AVAILABLE, build_server, negotiation, structured/text results, errors and resource role/size policy',
        'worker_v12.py': 'main: address-space/wall limits, fixed process entry and canonical error mapping',
        'responses.py': 'moment_test_sets: Bonferroni normal critical values and quadratic inversion; quadratic_sublevel',
        'causal_workflow.py': 'AdjustmentQuery and adjustment_expression: supplied-DAG back-door boundary'}
    records = [ref(ROOT / 'src/causalbank' / name, anchor) for name, anchor in anchors.items()]
    records += [ref(ROOT / 'docs/program/repair-v12/work/IN02' / name, 'Canonical schema and protocol mapping')
                for name in ['request-schema.json', 'response-schema.json', 'mcp-contract.json']]
    records += [ref(p, a) for p, a in [
        (BASE / 'examples/protocol.json', 'Prospectively frozen deterministic examples and selected execution identity'),
        (BASE / 'examples/review.json', 'Thirteen complete response comparisons and ten lifecycle checks'),
        (BASE / 'printed-listings/review.json', 'Executed exact request and library code printed in I2'),
        (ROOT / 'tools/interface_examples_20261013.py', 'Example definitions, four independent algebraic references and observations'),
        (Path(__file__), 'Exact printed example validation and primary-source audit preparation')]]
    for path in sorted((BASE / 'examples/results').glob('*.json')):
        records.append(ref(path, 'Complete request binding, observed library/CLI replies and outcome checks'))
    records.append(ref(BASE / 'examples/lifecycle.json', 'Observed replay, budget conflict, report declarations, terminal state and completed-job cancellation'))
    claims = [
        'Nine implemented operations; missing discovery/formulation/design engines remain unavailable.',
        'Selected supplied-DAG expression retains risk adjustment, units and assumptions; dependent sampling unsupported and contradicted premise refused.',
        'Thirteen generated library/CLI responses agree, including four deterministic set shapes, weak moments, context failure and clock diagnostics.',
        'Printed complete request and library/CLI instructions reproduce the frozen identification example.',
        'Execution status, scientific disposition, qualification and job payload state are distinct.',
        'Error mapping depends on the layer that catches the failure; exit zero is not scientific acceptance.',
        'Artifact context/descriptor hashes, bounded nonsymlink reads and operator custody have the stated local limits.',
        'Replay binds request plus selected code/Python/numerical environment; changed budget conflicts.',
        'Reports retain declared qualification; checkpoint/retry/cancellation do not imply remote exactly-once or rollback.',
        'MCP adapter maps canonical results and restricts legacy protocol/resources; no new MCP transport run or modern/HTTP acceptance.',
        'Worker limits exclude resident coordinator/SDK; this evidence is not bank deployment or performance qualification.']
    source = {'id': 'exec13_i2_examples', 'integrated_citation_key': 'exec13_i2_examples',
              'kind': 'project_implementation_and_generated_examples',
              'title': 'Library and CLI reference examples and interface implementation inspection',
              'author': 'Causal banking research project', 'authors': ['Causal banking research project'],
              'year': 2026, 'version_date': 'Observed 13 October 2026; local-runtime/1; new project evidence, not backdated literature',
              'source_identity': 'Local inspected implementation and prospectively frozen generated examples',
              'local_records': records, 'inspected_anchors': list(anchors.values()),
              'supported_claims': claims,
              'limits': 'Author implementation review and deterministic examples. No new MCP run, live model, empirical coverage, bank validation or independent acceptance.'}
    write(BASE / 'source-audit.json', {'cutoff': '2026-10-07', 'observed_project_date': '2026-10-13', 'sources': [source]})
    write(BASE / 'claim-map.json', {
        'implementation_and_new_examples': {'citation': 'exec13_i2_examples', 'claims': claims},
        'inherited_mcp_and_fault_trials': {'citation': 'v12_in_runtime',
            'evidence': ref(ROOT / 'docs/program/repair-v12/work/IN04/review.md', 'Eleven historical MCP/library/CLI cases; nine local faults; sandbox limitation')},
        'official_protocol_sources': {'citations': ['v12_mcp_legacy_lifecycle', 'v12_mcp_legacy_stdio',
            'v12_mcp_legacy_tools', 'v12_mcp_legacy_resources', 'v12_mcp_legacy_cancellation',
            'v12_mcp_versioning', 'v12_mcp_basic'],
            'audit': ref(ROOT / 'docs/program/repair-v12/work/IN02/source-audit.json', 'Pinned primary copies, identity/version, source hashes and inspected anchors'),
            'newly_inspected_anchors': ['Lifecycle Initialization/Version Negotiation/Operation',
                'Transports stdio', 'Tools Structured Content/Output Schema/Error Handling',
                'Cancellation Behavior Requirements/Timing Considerations', 'Resources capabilities/list/read']},
        'project_derivations': ['Back-door expression specialized to generated risk/offer/net-value graph',
            'Four real quadratic solution sets by elementary inequalities',
            'Gaussian residual quadratic and explicit squared Bonferroni critical value'],
        'proposed_paths': ['Common consumer decoding/display library', 'New R/Java/C++ consumers',
                           'HTTP/multi-tenant wrapper', 'Modern protocol adapter', 'Bank-facing egress and authorization policy'],
        'no_proposal_acceptance': True})
    print(json.dumps({'printed_example_checks': checks, 'new_source_records': 1, 'source_bindings': len(records)}))


if __name__ == '__main__':
    main()
