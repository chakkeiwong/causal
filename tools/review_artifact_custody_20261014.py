#!/usr/bin/env python3
"""Review actual custody observations and bind a proposal requirement decision."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-14/artifact-custody'
OP = 'IN.REQ.artifact_data_custody'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Proposal requirement review; no new product implementation or external qualification.',
    'Single local operator and generated fixtures; no bank data, authentication or tenant isolation claim.',
    'Coherent descriptor replacement and blocking FIFO are observed limitations; repairs are proposed.',
    'No new sibling-repository, live-model or network-service execution.',
    'Owner provenance, authorization, retention, revocation and target-platform inputs remain conditional.',
    'Rendered visual acceptance remains open under the exhausted inherited image allowance.',
]


def main():
    obs = json.loads((BASE / 'local-observations.json').read_text())
    verify_bindings(obs)
    assert obs['count'] == len(obs['cases']) == 15
    by_case = {r['case']: r for r in obs['cases']}
    assert by_case['coherent_rewrite_new_supplied_reference']['observation'] == 'accepted'
    assert by_case['coherent_rewrite_old_trusted_reference']['observation'] == 'refused'
    assert by_case['fifo_without_writer']['observation'] == 'blocked_until_terminated'
    assert by_case['fifo_without_writer']['returncode_after_termination'] == -15
    suite = ET.parse(BASE / 'local-tests.xml').getroot().find('testsuite')
    assert suite is not None and int(suite.attrib['tests']) == 16
    assert all(int(suite.attrib[k]) == 0 for k in ['failures', 'errors', 'skipped'])
    files = [
        ('src/causalbank/artifacts_v12.py',
         'encode/digest/local_root/atomic/bounded_read; ArtifactStore put/reference/get',
         ['Sorted finite JSON, local path scope, individually atomic publications, eight-MiB bound.',
          'Supplied reference/metadata/byte checks without reader-side descriptor-to-handle recomputation.',
          'O_RDONLY|O_NOFOLLOW open precedes fstat and lacks O_NONBLOCK.']),
        ('src/causalbank/operation_contract_v12.py',
         'finite_json; validate_artifact_ref; validate_context; context_digest',
         ['Opaque handle and digest shape checks do not establish authority.',
          'Declared context/graph structural semantics differ from causal premise verification.']),
        ('src/causalbank/operation_service_v12.py',
         'request_digest; OperationService._artifact/invoke; envelope; _sensitivity',
         ['Request digest omits only correlation/idempotency labels.',
          'Expected role/schema and declared scientific-context agreement; no claim to verify truth.',
          'Empty mathematical result and unavailable execution are distinct response states.']),
        ('src/causalbank/runtime_v12.py',
         'execution_identity; Runtime.invoke/_verify_refs/_replay_or_run/_run_sync/_submit_report/run_report_job',
         ['Input preflight occurs in parent before worker timeout.',
          'Replay binds selected code/schema, dependency/Python versions and request digest; rechecks refs.',
          'Reports preserve schema-only verification; no institutional review.']),
        ('src/causalbank/worker_v12.py',
         'main: resource limits, exception envelope and timer cleanup',
         ['Context error becomes failed/unavailable response with no result in inspected runtime.']),
    ]
    records = [{'role': 'inspected_primary_technical_text', 'local_copy': ref(ROOT / path, anchor),
                'supported_claims': claims} for path, anchor, claims in files]
    inherited = [ref(ROOT / f'docs/program/repair-v12/work/{key}/receipt.json',
                     'Preserved design or actual local qualification scope and limitations')
                 for key in ['IN02', 'IN04']]
    primary = {'status': 'reviewed', 'reviewer': REVIEWER, 'records': records,
               'inherited': inherited, 'observations': ref(BASE / 'local-observations.json', 'Fifteen actual local cases'),
               'test_replay': ref(BASE / 'local-tests.xml', 'Sixteen existing service/runtime tests pass'),
               'limitations': LIMITS}
    write(BASE / 'primary-review.json', primary)
    repairs = [
        {'id': 'descriptor_handle', 'status': 'proposed_not_implemented',
         'change': 'Validate complete descriptor shape and recompute handle from descriptor on metadata lookup and get.',
         'acceptance_cases': ['Original unchanged artifact roundtrip', 'Old trusted ref after content mutation',
                              'Coherent content+descriptor+supplied-ref replacement under old handle refused',
                              'Requested/stored/derived handle mismatch', 'Missing/extra/invalid descriptor fields'],
         'remaining_boundary': 'Independent trusted manifest required if a writer can replace request and handle too.'},
        {'id': 'file_type_availability', 'status': 'proposed_not_implemented',
         'change': 'Candidate nonblocking no-follow open then immediate descriptor-based regular-file/size check; review directory descriptors and deadlines.',
         'acceptance_cases': ['FIFO without writer', 'FIFO with writer', 'Directory', 'Symlink',
                              'Oversized and changing regular files', 'Rejection before worker launch',
                              'Controlled path-replacement scenarios in declared OS model'],
         'remaining_boundary': 'O_NONBLOCK candidate repairs observed FIFO; not all filesystem delays or races.'},
        {'id': 'trusted_authority_lifecycle', 'status': 'prospective_architecture',
         'change': 'Bind approved inputs/purposes/principals to independently trusted manifests; enforce policy before replay.',
         'acceptance_cases': ['Generated authorized/forbidden principal fixtures', 'Revoked and expired input',
                              'Changed horizon/population/clock', 'Cross-language schema migration',
                              'Deleted source and derived artifact disposition'],
         'remaining_boundary': 'Requires actual owner authority, operating policy, keys and custody agreements for bank qualification.'},
    ]
    design = {'kind': 'project_design', 'status': 'reviewed_proposal', 'reviewer': REVIEWER,
              'repairs': repairs,
              'owner_inputs': ['Trusted manifest publisher and location', 'Identity authority and permitted purposes',
                               'Target OS/filesystem and service limits', 'Population, assignment and timestamp provenance',
                               'Retention, revocation, deletion, backups and audit evidence policy',
                               'Named consumer, supported environment and acceptance decision'],
              'public_evidence_route': 'Generated accounts and public-source lineage cases first; authentic bank evidence conditional later.',
              'evidence': [ref(BASE / 'primary-review.json', 'Inspected implementation'),
                           ref(BASE / 'local-observations.json', 'Observed refusals and two negative boundaries'),
                           ref(BASE / 'plan-review.md', 'Reviewed scoped probe plan')],
              'limitations': LIMITS}
    write(BASE / 'design-review.json', design)
    sources = []
    for key, title, kind, path, anchor, claims, supporting in [
        ('implementation', 'Local causal artifact, context, replay and report implementation', 'project_implementation',
         BASE / 'primary-review.json', 'Five inspected local source records and preserved IN02/IN04 scope',
         [c for r in records for c in r['supported_claims']], records),
        ('observations', 'Generated local custody probes and preserved service/runtime test replay', 'project_execution',
         BASE / 'local-observations.json', 'Fifteen named actual cases; immutable generated inputs and returned responses',
         obs['claims'] + ['Sixteen existing local tests passed; no reliability-rate or bank-truth claim.'],
         [{'local_copy': ref(BASE / 'local-tests.xml', '16 passed, no errors/failures/skips')},
          {'local_copy': ref(ROOT / 'tools/probe_artifact_custody_20261014.py', 'Exact executable fixtures and bounded child termination')},
          *[{'local_copy': ref(ROOT / ('tests/' + n), 'Executed test cases and generated fixture context')}
            for n in ['test_operation_service_v12.py', 'test_runtime_v12.py']]]),
        ('design', 'Prospective artifact custody repairs and cross-repository acceptance design', 'project_design',
         BASE / 'design-review.json', 'Three repair/architecture decisions, acceptance cases and owner inputs',
         ['Handle derivation and nonblocking file-type candidates are proposed, not implemented.',
          'Trusted manifests, authorization, lifecycle and adapter semantics require separate evidence.'],
         [{'local_copy': ref(BASE / 'plan-review.md', 'Bounded proposal and review scope')}]),
    ]:
        sources.append({'integrated_citation_key': 'exec14_custody_' + key,
                        'title': title, 'author': 'Causal banking proposal', 'kind': kind, 'year': 2026,
                        'source_identity': 'Project-authored ' + kind + '; ' + str(path.relative_to(ROOT)),
                        'version_date': 'Source bytes pinned by SHA-256; inspected/executed 2026-10-14',
                        'local_copy': ref(path, anchor), 'inspected_anchors': [anchor],
                        'supported_claims': claims, 'records': supporting, 'limitations': LIMITS})
    write(BASE / 'source-audit.json', {'cutoff': '2026-10-07', 'sources': sources,
                                     'note': 'Project work dated after cutoff; no new external literature claim.'})
    evidence = [ref(BASE / name, anchor) for name, anchor in [
        ('primary-review.json', 'Exact inspected implementation and inherited scope'),
        ('local-observations.json', 'Actual local generated cases and negative boundaries'),
        ('local-tests.xml', 'Existing 16-test replay'),
        ('design-review.json', 'Known repairs and remaining owner inputs'),
        ('development.md', 'Connected manuscript with implementation/observation/proposed distinctions'),
        ('source-audit.json', 'Three project source identities, hashes, anchors and supported claims'),
    ]]
    evidence.append(ref(Path(__file__).resolve(), 'Author review assertions and receipt construction'))
    findings = [
        'Bound five inspected implementation files and preserved design/qualification receipts. Local byte/context/replay claims are narrow; descriptor-handle and FIFO negative boundaries have concrete proposed repairs and acceptance cases.',
        'Actual generated local cases and 16 existing tests are distinguished from static inspection and proposed features. Empty set is distinct from unavailable; changed request/replayed bytes refuse. Owner authority, provenance, retention/revocation and platform inputs are explicit.',
    ]
    output = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'requirement-review.json'
    write(output, {'operation': OP, 'status': 'pass', 'scope': 'Proposal requirement development, not product custody qualification',
                   'reviewer': REVIEWER, 'findings': findings, 'evidence': evidence,
                   'negative_findings_preserved': True, 'implementation_changed': False,
                   'gaps_closed': ['Scoped custody requirement review and local/public acceptance design'],
                   'capability_qualification': False, 'limitations': LIMITS})
    state = core.read(ROOT, core.STATE)
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope='Proposal requirement development with actual local counterexamples',
                   reviewer=REVIEWER, limitations=LIMITS, outputs=[ref(output, 'Reviewed custody proposal requirement')],
                   nonexecution_reason='', revisit_trigger='',
                   criteria=[{'index': i, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}
                             for i, finding in enumerate(findings)])
    write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'requirement_review': 'pass', 'local_cases': 15, 'existing_tests_passed': 16,
                      'observed_negative_boundaries': 2, 'repairs_implemented': False}))


if __name__ == '__main__':
    main()
