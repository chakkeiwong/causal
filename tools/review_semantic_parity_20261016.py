#!/usr/bin/env python3
"""Review frozen observations without rerunning or altering the observed runtime."""
from datetime import datetime
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
from statistics import NormalDist

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-16/semantic-parity'
PRIOR = ROOT / 'docs/program/execution/2026-10-16/cxx-temporal/publication-v2/reader/source-audit.json'
OP = 'IN.REQ.library_cli_mcp_semantic_parity'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/requirement-review.json')
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Bounded generated local stdio observations; no universal parity, HTTP, multi-tenant or newer-protocol qualification.',
    'Stored-replay error attribution remains a known implementation defect; the repair is proposed, not implemented.',
    'Source inspection is static evidence; shared response equality does not establish causal truth, calibration or useful bank precision.',
    'No live model, sibling integration, bank acceptance, independent institutional review or measured ROI is claimed.',
    'Rendered visual acceptance remains open under the inherited exhausted six-image allowance.',
]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def observations():
    protocol = read(BASE / 'protocol.json')
    verify_bindings(protocol)
    batches = [read(BASE / (n + '-observations.json')) for n in ['a', 'b', 'adverse', 'lifecycle']]
    for batch in batches:
        verify_bindings(batch)
        assert batch['execution_identity'] == protocol['execution_identity']
        assert batch['protocol'] == '2025-11-25'
        assert batch['advertised_tools'] == batches[0]['advertised_tools']
    rows, operations = [], set()
    for case in protocol['cases']:
        request = read(ROOT / case['request']['path'])
        observed = read(BASE / 'observed' / (case['name'] + '.json'))
        verify_bindings(observed)
        a, b, m = observed['library'], observed['cli'], observed['mcp']
        assert a == b['response'] == m['structuredContent'] == json.loads(m['content'][0]['text'])
        assert all(v is True for v in observed['checks'].values())
        expected = case['expected']
        assert (a['status'], a['disposition']) == (expected['status'], expected['disposition'])
        assert a['request_id'] == request['request_id'] and a['operation'] == request['operation']
        context = request['scientific_context']
        context_hash = None if context is None else hashlib.sha256(
            json.dumps(context, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
        assert a['context_sha256'] == context_hash
        operations.add(request['operation'])
        rows.append({'case': case['name'], 'operation': request['operation'], 'status': a['status'],
                     'disposition': a['disposition'], 'cli_exit': b['exit_code'], 'mcp_is_error': m['isError'],
                     'canonical_and_text_equal': True, 'observation': ref(BASE / 'observed' / (case['name'] + '.json'), 'Complete saved observations')})
    lifecycle = read(BASE / 'observed/lifecycle.json')
    assert all(v is True for v in lifecycle['checks'].values())
    for a, b, m in [(lifecycle['submitted'], lifecycle['cli_submission'], lifecycle['mcp_submission']),
                    (lifecycle['polls'][-1], lifecycle['terminal_cli'], lifecycle['terminal_mcp']),
                    (lifecycle['cancel_library'], lifecycle['cancel_cli'], lifecycle['cancel_mcp'])]:
        assert a == b['response'] == m['structuredContent'] == json.loads(m['content'][0]['text'])
        assert b['exit_code'] == 0 and m['isError'] is False
        operations.add(a['operation'])
    assert lifecycle['submitted']['status'] == 'queued'
    assert lifecycle['cancel_library']['result']['payload']['state'] == 'completed'
    assert [x['declared_disposition'] for x in lifecycle['report']['summaries']] == ['computed', 'unsupported', 'refused']
    assert all(x['verification'] == 'schema_only_not_causal_or_external_review' for x in lifecycle['report']['summaries'])
    advertised = read(BASE / 'observed/capabilities.json')['library']['result']['payload']['implemented']
    assert operations == set(advertised) and len(operations) == 9
    adverse = {}
    for name in ['unadvertised', 'invalid', 'corrupt-replay']:
        obj = read(BASE / 'observed' / (name + '.json')); verify_bindings(obj)
        assert all(v is True for v in obj['checks'].values())
        adverse[name] = {'finding': obj['finding'], 'observation': ref(BASE / 'observed' / (name + '.json'), 'Actual adverse observations')}
    corrupt = read(BASE / 'observed/corrupt-replay.json')
    assert corrupt['library']['exception']['type'] == 'JSONDecodeError'
    assert corrupt['cli']['exit_code'] == 2 and corrupt['cli']['response']['error']['code'] == 'invalid_request'
    assert 'Invalid local causal request' in corrupt['mcp']['tool_result']['content'][0]['text']
    request = read(BASE / 'requests/corrupt-replay.json')
    slot = ROOT / '.runtime/semantic-parity-20261016/replay' / (hashlib.sha256(request['idempotency_key'].encode()).hexdigest() + '.json')
    assert slot.read_bytes() == (BASE / 'replay-before.json').read_bytes()
    return {'status': 'pass_for_saved_observation_review', 'reviewer': REVIEWER, 'scientific_cases': rows,
            'scientific_comparisons': 13, 'lifecycle_comparisons': 3, 'adverse_cases': adverse,
            'operations_exercised': sorted(operations), 'all_advertised_operations_exercised': True,
            'lifecycle_text_and_structured_equal': True, 'replay_restoration_verified': True,
            'runtime_identity': protocol['execution_identity'], 'sdk_versions': protocol['sdk_versions'],
            'trial_execution': 'Actual local library, CLI and MCP stdio in approved outside-sandbox environment; generated inputs; no network',
            'recovery_action': 'Read and independently compare saved observations; no frozen trials rerun',
            'evidence': [ref(BASE / (n + '-observations.json'), 'Saved batch') for n in ['a', 'b', 'adverse', 'lifecycle']]
                        + [ref(BASE / n, n) for n in ['protocol.json', 'replay-before.json', 'sandbox-thread-probe.json', 'outside-thread-probe.json']]}


def independent_meanings():
    shapes = {'finite': ('finite_interval', [[-2, 2]]), 'empty': ('empty', []),
              'whole': ('whole_line', [[None, None]]), 'disconnected': ('unbounded_union', [[None, -2], [2, None]])}
    algebra = []
    for name, (topology, intervals) in shapes.items():
        coeff = read(BASE / 'inputs' / (name + '.json'))['quadratics'][0]
        result = read(BASE / 'observed' / (name + '.json'))['library']['result']
        assert result['coordinate_sets'] == [{'topology': topology, 'intervals': intervals}]
        assert result['uncertainty']['coverage'] == 'none' and result['uncertainty']['level'] is None
        # A rational sign check supplements the elementary analytic inequality, without using the product solver.
        for x in map(Fraction, [-100, -3, -2, -1, 0, 1, 2, 3, 100]):
            inside = any((lo is None or lo <= x) and (hi is None or x <= hi) for lo, hi in intervals)
            assert inside == (coeff[0] * x*x + coeff[1]*x + coeff[2] <= 0)
        algebra.append({'case': name, 'coefficients': coeff, 'topology': topology, 'intervals': intervals,
                        'meaning': 'Deterministic sublevel set; no probability statement'})
    z = NormalDist().inv_cdf(.975)
    bound = math.sqrt(100 / (z*z) - .01)
    weak = read(BASE / 'observed/weak-moments.json')['library']['result']
    actual = weak['coordinate_sets'][0]['intervals']
    assert actual[0][0] is None and actual[1][1] is None
    assert abs(actual[0][1] + bound) < 1e-12 and abs(actual[1][0] - bound) < 1e-12
    clocks = read(BASE / 'inputs/clocks.json')['rows']; failed = []
    for i, row in enumerate(clocks):
        if 'available_at' not in row or not datetime.fromisoformat(row['event_at']) <= datetime.fromisoformat(row['available_at']) < datetime.fromisoformat(row['decision_at']):
            failed.append(i)
    assert failed == [1, 2] == read(BASE / 'observed/clock.json')['library']['result']['payload']['clock_failures']
    identification = read(BASE / 'observed/backdoor.json')['library']['result']['payload']['expression']
    assert identification['query']['controls'] == ['risk']
    assert identification['expression']['difference_of_actions'] == [1, 0]
    return {'status': 'pass', 'scope': 'Separate author algebra and stored-object review, not external review or a new empirical trial',
            'algebra': algebra, 'weak_moment_boundary': bound,
            'weak_moment_derivation': '100 <= z(.975)^2 * (0.01 + b^2); invert directly using standard-library NormalDist, without the implementation solver',
            'weak_moment_limit': 'Conditional Gaussian-moment approximation, no finite-sample or uniform guarantee',
            'clock_failures': failed,
            'backdoor': 'Risk blocks the sole offer <- risk -> net_value backdoor path in the stipulated DAG; integrate risk under common target population; assumptions remain conditional',
            'evidence': [ref(Path(__file__), 'independent_meanings, separate arithmetic'), ref(BASE / 'protocol.json', 'Frozen inputs and meanings')]}


def sources():
    folder = BASE / 'runtime-source'; folder.mkdir(exist_ok=False)
    names = ['artifacts_v12.py', 'operation_contract_v12.py', 'operation_service_v12.py', 'runtime_v12.py',
             'worker_v12.py', 'cli_v12.py', 'mcp_server_v12.py', 'responses.py', 'causal_workflow.py']
    anchors = {
        'runtime_v12.py': ['execution_identity lines 28-36: selected local hashes and dependencies', '_validate/invoke lines 73-101: schema, semantic checks and request dispatch', '_replay_or_run lines 103-118: stored JSON parsing and idempotency identity', '_submit_report/resume: queued handle, durable state and completion'],
        'cli_v12.py': ['read_request and main: explicit local launch root and bounded input', 'main lines 68-83: exit mapping and broad ValueError/JSONDecodeError caller-input attribution'],
        'mcp_server_v12.py': ['mapping/AVAILABLE and negotiation lines 22-38: nine advertised operations, pinned protocol', 'call_tool lines 49-72: adapter validation and broad ValueError handler', 'guarded_call lines 80-87: unknown tool JSON-RPC invalid-params'],
        'operation_contract_v12.py': ['context_digest/finite_json: scientific identity and finite values', 'validate_response lines 127-180: context, disposition, units, topology and uncertainty meaning'],
        'operation_service_v12.py': ['invoke lines 96-125: contradicted premises, unsupported operation and semantic validation', '_artifact: context-bound generated artifacts', '_estimate/_sensitivity/_audit lines 180-264: conditional moment sets, nonprobabilistic inequalities and strict clocks'],
        'worker_v12.py': ['main: resource-bound subprocess, structured execution error and response output'],
        'artifacts_v12.py': ['encode/bounded_read/atomic: canonical JSON and local storage'],
        'responses.py': ['moment_test_sets lines 148-163: Gaussian residual-test quadratic coefficients'],
        'causal_workflow.py': ['Supplied graph/query semantics used by the bounded operation service'],
    }
    records, identity = [], {}
    for name in names:
        original = ROOT / 'src/causalbank' / name; copy = folder / name
        copy.write_bytes(original.read_bytes()); identity[name] = sha(copy)
        records.append({'kind': 'project_implementation_source', 'source_identity': str(original.relative_to(ROOT)),
                        'version_date': 'Observed runtime source on 2026-10-16; exact SHA-256', 'local_copy': ref(copy, '; '.join(anchors[name])),
                        'inspected_anchors': anchors[name], 'supported_claims': anchors[name], 'original_sha256': sha(original)})
    for name in ['request-schema.json', 'response-schema.json', 'mcp-contract.json']:
        original = ROOT / 'docs/program/repair-v12/work/IN02' / name; copy = folder / name
        copy.write_bytes(original.read_bytes())
        if name != 'mcp-contract.json': identity[name] = sha(copy)
        records.append({'kind': 'project_interface_contract', 'source_identity': str(original.relative_to(ROOT)),
                        'version_date': 'Canonical schema 1.0.0 / pinned MCP 2025-11-25; observed 2026-10-16',
                        'local_copy': ref(copy, 'Operation, context, response and tool mapping fields'),
                        'inspected_anchors': ['Properties/required fields and tool mapping'],
                        'supported_claims': ['Schema and tool-map identities for the observed local interfaces']})
    digest = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    assert digest == read(BASE / 'protocol.json')['execution_identity']['source_sha256']
    audit = read(ROOT / 'docs/program/repair-v12/work/IN04/runtime-source-audit.json'); verify_bindings(audit)
    installed = ROOT / '.runtime/in04/lib/python3.13/site-packages/mcp'
    pairs = ['server/lowlevel/server.py', 'server/session.py', 'server/stdio.py', 'client/stdio/__init__.py', 'shared/version.py', 'types.py']
    sdk = []
    for item, rel in zip(audit['entries'], pairs):
        assert sha(installed / rel) == item['local_copy']['sha256']
        sdk.append({'identity': item['identity'], 'version_date': item['version_date'], 'local_copy': item['local_copy'],
                    'installed_path': str((installed / rel).relative_to(ROOT)), 'installed_bytes_match_saved_original': True,
                    'inspected_anchors': item['inspected_anchors']})
    sdk[0]['inspected_anchors'] = ['call_tool lines 525-588: explicit CallToolResult returns before later output-schema branch; local adapter must validate its response']
    spec = ROOT / 'docs/literature/raw/v12_mcp_legacy_tools.md'
    return {'status': 'pass', 'reviewer': REVIEWER, 'records': records, 'sdk_originals': sdk,
            'runtime_source_identity_reproduced': digest, 'identity_omissions': ['mcp version', 'anyio version', 'mcp-contract.json', 'negotiated protocol and launch/normalizer profile'],
            'static_findings': ['Replay JSONDecodeError is caught as broad ValueError by both adapters.',
                'Explicit CallToolResult bypasses the SDK later schema-validation branch; current local adapter validates schema, runtime validates semantics.',
                'Runtime scientific/source identity omits the complete transport identity; current trials separately record SDK versions.'],
            'historical_protocol': ref(spec, 'Structured content lines 324-344; protocol versus tool errors lines 459-478'),
            'sdk_original_audit': ref(ROOT / 'docs/program/repair-v12/work/IN04/runtime-source-audit.json', 'Six installed original files'),
            'cutoff_policy': 'No new literature search. Preserve inherited protocol source/cutoff record; current installed software and project trials are dated observations, not newly claimed frontier literature.'}


def main():
    assert not (BASE / 'observation-review.json').exists() and not OUTPUT.exists()
    observed = observations(); exact = independent_meanings()
    write(BASE / 'observation-review.json', observed)
    write(BASE / 'independent-meanings.json', exact)
    primary = sources(); write(BASE / 'source-review.json', primary)
    contract = {
        'status': 'proposed_not_implemented', 'implementation_qualification': False,
        'equality': 'Runtime.invoke response equals decoded CLI response and both MCP representations only for a request in the negotiated common domain; retain every scientific field and error',
        'error_layers': [
            {'layer': 'input', 'trigger': 'Unparseable incoming JSON or schema-invalid caller fields', 'response': 'Surface input/protocol error; never fabricate a scientific context'},
            {'layer': 'capability', 'trigger': 'Unknown MCP tool or unsupported canonical method', 'response': 'Negotiate shared domain first; retain unknown-tool protocol error separately from completed scientific unsupported'},
            {'layer': 'scientific', 'trigger': 'Contradicted premise, unavailable identification or unsupported law', 'response': 'Canonical refusal/unsupported/unavailable as justified; successful transport does not imply a causal answer'},
            {'layer': 'artifact', 'trigger': 'Missing, invalid, wrong-role or wrong-context referenced artifact', 'response': 'Canonical failed/unavailable after request validation, preserving target and artifact reason'},
            {'layer': 'stored_state', 'trigger': 'Malformed replay, missing required replay keys or incompatible saved state', 'response': 'Specific stored-state failure, canonical failed/unavailable for validated request; preserve corrupt bytes; do not automatically repeat consequential work'},
            {'layer': 'worker', 'trigger': 'Timeout, resource exhaustion or malformed worker response', 'response': 'Canonical unavailable with worker/resource/protocol code; retain failure and no scientific output'},
            {'layer': 'transport', 'trigger': 'Framing, connection, SDK or output serialization failure', 'response': 'Transport evidence; do not manufacture causal nonidentification or success'},
        ],
        'repair_sequence': ['Separate input parsing/validation from runtime handling; define typed failure origins.',
            'Validate saved replay shape, identity and references at storage boundary; convert corruption into a context-bound stored-state failure.',
            'Retain explicit response-schema and semantic validation before every adapter return path; serialize one validated object into both MCP outputs.',
            'Bind scientific identity plus transport protocol, schemas, tool map, SDK, AnyIO, launch profile and normalizer.',
            'Freeze fresh successor cases with expected failure layer before executing; preserve all old negative evidence.'],
        'local_acceptance_cases': [
            'Malformed incoming JSON versus extra fields versus wrong operation/tool mapping',
            'Valid request plus truncated replay, missing replay key, incompatible identity, missing referenced artifact and symlink/storage access errors',
            'Unsupported canonical method versus unadvertised tool and contradicted assumptions',
            'Changed target, sign, coordinate order, units, clocks and sampling law with old context-bound evidence',
            'Finite, empty, whole and disconnected sets; nonprobabilistic versus conditional sampling interpretation',
            'Nonfinite/mistyped output, wrong context, wrong units and output-budget envelope on each adapter return path',
            'MCP text/structured divergence and SDK/tool-map/profile change in replay identity',
            'Queued/running/terminal report states; in-flight cancellation; completed cancellation; crash/restart without duplicated external effects',
            'Each proposed language decoder preserves whole canonical response, large integers, null endpoints and error identity',
        ],
        'known_route': 'Generated fixtures and saved public evidence can exercise deterministic semantics before an expensive bank pilot; match complete objects and expected layer, keep failures in denominator.',
        'external_inputs': [
            {'owner': 'Consumer repository maintainer', 'input': 'Actual caller version, decoder, display behavior and permission to modify that repository', 'acceptance': 'Consumer preserves units, sets, dispositions, evidence and retry behavior'},
            {'owner': 'Platform/security operator', 'input': 'Target launch, authentication, tenant, transport and service limits', 'acceptance': 'Frozen platform/HTTP/recovery protocol and observed results'},
            {'owner': 'Bank scientific/data owner', 'input': 'Causal assumptions, assignment truth, information clocks and decision precision/loss', 'acceptance': 'Separate later scientific and bank-use review'},
        ],
        'unknowns': ['General identification or calibration outside declared models cannot be repaired by a transport adapter.',
                     'Actual bank usefulness, operating cost and owner acceptance require later evidence; no promised outcome.'],
        'comparative_costs': ['Request/semantic preparation', 'Adapter implementation and dependency maintenance', 'Execution/replay and storage', 'Error investigation and scientific review', 'Consumer/platform qualification'],
        'later_experiment_trigger': 'A public/generated prototype shows that preserved scientific meaning and explicit failure handling merit a limited consumer/platform pilot.',
        'observations': ref(BASE / 'observation-review.json', 'Actual bounded demonstrations and known failure'),
    }
    write(BASE / 'proposed-contract.json', contract)
    text = (BASE / 'development.template').read_text().replace('§', chr(92))
    text, spacing = re.subn(r'(?<=\S)(\\citep\{)', r' \1', text)
    assert not re.search(r'\S\\citep\{', text)
    with (BASE / 'development.tex').open('x') as f: f.write(text)
    write(BASE / 'plan-review.json', {'status': 'pass_for_bounded_proposal_review', 'reviewer': REVIEWER,
        'plan': ref(BASE / 'plan.md', 'Reviewed original plan'),
        'findings': ['Completed batches survive crash with all request, response, harness and source bindings intact; no reruns.',
            'Independent review additionally compares lifecycle MCP text, verifies replay restoration and recomputes weak-moment boundary.',
            'All nine advertised operations have selected cases; this does not cover all inputs, branches or environments.',
            'The existing implementation defect is carried into an executable repair/acceptance design, not silently labeled fixed.',
            'Installed SDK originals match all six saved copies; response validation ownership and transport-identity omissions are explicit.',
            'Citation spacing corrected before first compilation; no change to frozen experimental harness.'],
        'citation_spaces_added': spacing, 'known_limits': LIMITS,
        'evidence': [ref(BASE / n, n) for n in ['observation-review.json', 'independent-meanings.json', 'source-review.json', 'proposed-contract.json']]})
    entries = []
    for suffix, title, kind, path, claims, records in [
        ('observed', 'Actual local library, CLI and MCP parity and adverse observations', 'project_implementation_evidence', BASE / 'observation-review.json',
         ['Thirteen generated scientific requests and three lifecycle calls match across canonical and MCP text/structured responses.',
          'All nine advertised operations exercised; three adverse cases preserve capability asymmetry, schema rejection and replay corruption misclassification.',
          'Static current-source findings: adapter validation ownership and incomplete transport identity; six installed SDK originals match saved copies.'],
         [ref(BASE / n, n) for n in ['protocol.json', 'source-review.json', 'independent-meanings.json']] + primary['records'] + primary['sdk_originals']),
        ('design', 'Proposed semantic parity, error attribution and transport identity acceptance contract', 'project_design', BASE / 'proposed-contract.json',
         ['Common-domain response equality, typed failure layers and concrete successor cases.', 'Public/generated prototype first; consumer, platform and bank evidence remain later conditional inputs.'],
         [ref(BASE / 'plan-review.json', 'Reviewed scope and limitations')]),
    ]:
        entries.append({'integrated_citation_key': 'exec16_parity_' + suffix, 'title': title, 'author': 'Causal banking proposal',
            'kind': kind, 'year': 2026, 'source_identity': 'Project-authored local evidence and explicitly proposed design',
            'version_date': '2026-10-16; local runtime/1; MCP 2025-11-25; SDK 1.27.0 where applicable',
            'local_copy': ref(path, title), 'inspected_anchors': claims, 'supported_claims': claims, 'records': records, 'limitations': LIMITS})
    write(BASE / 'source-audit.json', {'sources': entries, 'prior': ref(PRIOR, '656 preserved source records'), 'cutoff': '2026-10-07'})
    findings = ['Current source, schemas, tool map and six SDK originals are hash-bound; explicit error, identity and local/external acceptance cases are proposed with known defects retained.',
                'Thirteen actual generated scientific requests and three lifecycle comparisons exercise all nine advertised operations; three adverse cases, independent algebra, scientific refusals and owner inputs retain their precise meanings.']
    evidence = [ref(BASE / n, n) for n in ['observation-review.json', 'source-review.json', 'independent-meanings.json', 'proposed-contract.json', 'plan-review.json', 'source-audit.json', 'development.tex']]
    write(BASE / 'author-review.json', {'status': 'pass_for_bounded_proposal_review', 'reviewer': REVIEWER, 'criteria_verdicts': ['pass', 'pass'],
        'findings': findings, 'evidence': evidence, 'limitations': LIMITS, 'universal_parity': False, 'implementation_repair_completed': False,
        'original_gap_qualification': False, 'visual_acceptance': False})
    write(OUTPUT, {'requirement': 'library_cli_mcp_semantic_parity', 'status': 'pass_for_bounded_proposal_review', 'reviewer': REVIEWER,
        'criteria_verdicts': ['pass', 'pass'], 'findings': findings, 'evidence': evidence + [ref(BASE / 'author-review.json', 'Criterion-specific author review')],
        'limitations': LIMITS, 'capabilities': [], 'original_gap_qualification': False, 'implementation_repair_completed': False})
    print(json.dumps({'review': 'pass_for_bounded_proposal_review', 'scientific': 13, 'lifecycle': 3, 'adverse': 3, 'advertised_operations': 9, 'new_citations': 2, 'repaired_implementation': False}))


if __name__ == '__main__':
    main()
