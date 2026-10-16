#!/usr/bin/env python3
"""Audit pinned DataHub originals and prepare a bounded proposal decision."""
import hashlib
import json
from pathlib import Path
import re
import tomllib
import datahub_reference_20261016 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR = ROOT / 'docs/program/execution/2026-10-16/commercial-policy/publication/reader/source-audit.json'
OP = 'SW.DECISION.inherited_datahub'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'decision.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Sixteen selected original files at a cutoff-compatible source revision; not whole-project or complete dependency review.',
    'Dynamic Python distribution version, resolved build, dependency rights and setup.py equivalence remain unverified.',
    'No DataHub SDK, service, connector, Cloud product or MCP server was executed or integrated.',
    'Static source meanings and authored contract oracles are distinct from observed upstream behavior.',
    'Generated worlds and stipulated money do not establish bank assignment, availability truth, performance or ROI.',
    'A catalog cannot resolve observational causal ambiguity without additional assumptions or information.',
    'Cloud and separately distributed MCP features and entitlements require their own review.',
    'Rendered visual acceptance remains open under the exhausted inherited six-preview allowance.']


def read(path):
    return json.loads(path.read_text())


def main():
    assert not (BASE / 'source-review.json').exists()
    prior = read(PRIOR); verify_bindings(prior)
    assert len(prior['sources']) == 666 and examples.calculate() == read(BASE / 'exact-results.json')
    commit = read(ROOT / 'docs/literature/raw/exec16_dh_commits.json')[0]
    tree = read(ROOT / 'docs/literature/raw/exec16_dh_tree.json')
    assert not tree['truncated'] and tree['sha'] == commit['commit']['tree']['sha']
    assert commit['commit']['committer']['date'] <= '2026-10-07T15:59:59Z'
    entries = {r['path']: r for r in tree['tree']}
    selection = [
        ([(86, 124)], 'Apache 2.0 redistribution conditions; license, modification, attribution and applicable NOTICE obligations.'),
        ([(1, 70)], 'Root NOTICE includes LinkedIn and third-party attributions; not a resolved Python dependency inventory.'),
        ([(42, 58), (101, 128)], 'OSS/Cloud distinction; separately named MCP server is an unreviewed distribution lead.'),
        ([(1, 88)], 'acryl-datahub; dynamic version, Python >=3.10, declared build/base dependencies and generated-file caveat.'),
        ([(17, 67), (71, 102), (109, 155)], 'Client setup, environment-based default configuration, SDK query interfaces and optional Cloud import boundaries.'),
        ([(421, 468)], 'get_aspect version zero latest, explicit historical version, HTTP404 None, timeseries rejection and malformed-response failure.'),
        ([(67, 152), (510, 580)], 'Opaque dataset identity dimensions and explicit field-lineage mapping; constructor delegates URN construction.'),
        ([(207, 270), (290, 299), (355, 384), (706, 797), (876, 956)], 'Separate mutations and queries; fuzzy column mapping, 3+ hop categories, paginated accumulation and schema-field-only path projection.'),
        ([(1, 35)], 'Upstream and optional fine-grained lineage aspect, not a causal DAG.'),
        ([(1, 90)], 'Optional transformation/query fields; lineage-confidence default1 and ingestion-time match interpretation.'),
        ([(1, 95)], 'Dataset lineage audit stamps, query and resolution status; comments limit matching to ingestion-time knowledge.'),
        ([(1, 90)], 'Schema aspect, schema hash and supplied field/key definitions.'),
        ([(1, 86)], 'Field path, nullable default, descriptive metadata, field audit stamps and type identity.'),
        ([(1, 70)], 'Ownership records and zero audit time explicitly meaning missing data.'),
        ([(1, 80)], 'Legacy removed flag and lifecycle-stage visibility need separate interpretation.'),
        ([(1, 80)], 'AuditStamp describes resource/lifecycle changes, actor and context, not customer feature availability.')]
    manifest = read(BASE / 'source-manifest.json'); records = []
    assert len(manifest['requests']) == len(selection) == 16
    for r, (ranges, claim) in zip(manifest['requests'], selection):
        p = ROOT / 'docs/literature/raw' / (r['id'] + '.txt'); data = p.read_bytes()
        receipt = read(p.with_suffix('.receipt.json')); lines = data.decode().splitlines()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert len(data) == r['expected_bytes'] and hashlib.sha256(data).hexdigest() == receipt['sha256']
        assert blob == r['blob_sha1'] == entries[r['source_path']]['sha']
        assert receipt['url'] == r['url'] and receipt['status'] == 'saved'
        anchors = [{'anchor': f"{r['source_path']} lines {a}-{min(b,len(lines))}",
                    'excerpt': '\n'.join(lines[a-1:min(b,len(lines))])} for a, b in ranges]
        records.append({'source_identity': r['url'], 'source_path': r['source_path'],
                        'version_date': commit['sha'] + '; ' + commit['commit']['committer']['date'],
                        'local_copy': ref(p, 'Original pinned upstream bytes'),
                        'retrieval_receipt': ref(p.with_suffix('.receipt.json'), 'Actual public retrieval/hash'),
                        'git_blob_sha1': blob, 'git_blob_verified': True,
                        'inspected_anchors': anchors, 'supported_claims': [claim]})
    deps = tomllib.loads((ROOT / 'docs/literature/raw/exec16_dh_src_03.txt').read_text())
    source = {'status': 'pass_for_bounded_reference', 'reviewer': REVIEWER, 'revision': commit['sha'],
              'cutoff': '2026-10-07 Asia/Shanghai inclusive; selected commit before 15:59:59Z',
              'commit_date': commit['commit']['committer']['date'], 'source_count': 16,
              'identity': [ref(ROOT / 'docs/literature/raw' / n, 'Public commit/tree identity') for n in
                           ['exec16_dh_commits.json','exec16_dh_commits.receipt.json','exec16_dh_tree.json','exec16_dh_tree.receipt.json']],
              'canonical': 'datahub-project/datahub; Python distribution acryl-datahub',
              'aliases_not_equivalent': ['DataHub Cloud and acryl-datahub-cloud', 'Separately distributed mcp-server-datahub'],
              'maintenance': {'observed_commit': commit['commit']['message'], 'promise': 'No service level or support lifetime inferred'},
              'dependencies': {'declared': deps['project']['dependencies'], 'python': deps['project']['requires-python'],
                               'build': deps['build-system'], 'version': 'dynamic; source revision only',
                               'limits': 'Generated pyproject declaration only. setup.py equivalence, resolved versions, transitive notices and server compatibility remain unverified.'},
              'records': records, 'evidence': [ref(BASE / 'plan.md', 'Reviewed bounded acquisition and decision plan'),
                                             ref(BASE / 'source-manifest.json', 'Sixteen file identities and Git blob expectations')],
              'limitations': LIMITS}
    write(BASE / 'source-review.json', source)
    omissions = {'status': 'explicit_limits', 'items': [
        {'gap': 'Complete supported build and rights closure', 'route': 'Resolve minimal SDK path, dynamic version, generated dependency equivalence, notices and server compatibility.'},
        {'gap': 'Actual SDK/server behavior', 'route': 'Use permitted isolated fixture server and pinned client; compare raw requests/responses, cursor exhaustion, 404/errors, version consistency and lifecycle state.'},
        {'gap': 'Separate Cloud/MCP distributions', 'route': 'Pin and review each package/license and consumer contract only when the prototype selects it.'},
        {'gap': 'Historical availability and assignment truth', 'route': 'Public/generated truth now; later obtain consequential owner evidence. Catalog metadata alone cannot prove these facts.'},
        {'gap': 'Resolved URN/server projection behavior', 'route': 'Inspect and execute the delegated URN/entity/config/filter paths in a successor review; preserve raw upstream evidence now.'}],
        'evidence': [ref(BASE / 'source-review.json', 'Bounded original-source review')], 'limitations': LIMITS}
    write(BASE / 'omissions-register.json', omissions)
    contract = {'status': 'proposed_not_integrated', 'scope': 'Read-only metadata export into causal context',
        'input': ['Opaque source URN, field path and source dataset version', 'Requested aspect version and extraction scope',
                  'Request/page/result/byte/time limits', 'Separate event, value-availability, metadata-observation and decision clocks'],
        'output': ['Raw responses and hashes, returned aspect versions and extraction time', 'Entity/environment/instance/field identities',
                   'Source lineage and matching evidence, confidence meaning, lifecycle and deletion context',
                   'Known/unknown/error state for each semantic claim; pagination completeness and clock evidence',
                   'Candidate variable mappings and causal hypotheses kept separately from catalog edges'],
        'failures': ['Missing aspect is not absent scientific relevance', 'HTTP/schema/permission errors remain distinct from successful empty context',
                     'Repeated cursor, inconsistent version or resource exhaustion returns partial/failed, never complete',
                     'Unknown/late availability prevents historical-policy admission', 'Identity collapse and mutation attempts rejected by the proposed consumer boundary'],
        'prototype': ['Begin with frozen authored export and the four exact reference families plus five missing-context cases.',
                      'Inspect the delegated implementation/dependency paths and run actual serialization against an isolated permissible server before adapter approval.',
                      'Compare manual mapping, scoped raw export and optional catalog SDK on matched semantic cases and full preparation/review/maintenance cost.',
                      'Keep library/CLI/MCP evidence objects semantically identical; require a separately selected read interface and no automatic metadata mutation.'],
        'roles': ['Prototype maintainer: source/environment, conversion, limits, error semantics and recovery.',
                  'Scientific reviewer: variable meaning, assignment, observation, clocks and ambiguity.',
                  'Future catalog owner: authorized scope, versions and historical evidence; later conditional bank input.'],
        'evidence': [ref(BASE / 'source-review.json', 'Pinned actual code and models'), ref(BASE / 'exact-results.json', 'Generated semantic references'),
                     ref(BASE / 'omissions-register.json', 'Remaining implementation and semantic inputs')], 'limitations': LIMITS}
    write(BASE / 'proposed-export-contract.json', contract)
    decision = {'operation': OP, 'candidate': 'datahub', 'decision': 'reference', 'integration_allowed': False,
        'source_identity': 'https://github.com/datahub-project/datahub', 'revision': commit['sha'],
        'canonical_identity': source['canonical'],
        'reason': 'Use pinned catalog models/client as a technical reference; conditional integration with an existing catalog follows a bounded export fixture, complete supported path and actual behavioral comparison.',
        'target_and_uncertainty': 'Metadata, lineage and candidate context. No assignment identification, historical value availability or calibrated causal confidence is supplied by a lineage edge.',
        'license': 'Apache 2.0 root license and NOTICE inspected; complete selected-distribution/dependency rights remain open.',
        'dependency_evidence': ref(BASE / 'source-review.json', 'Pinned build/dependency declarations and observed maintenance'),
        'runtime_status': 'not_run; no integration_allowed capability',
        'alternatives': [
            {'choice': 'Adopt entire platform', 'disposition': 'defer', 'reason': 'Narrow causal-context value should justify platform maintenance and deployment.'},
            {'choice': 'Integrate a read-only export', 'disposition': 'conditional future candidate', 'reason': 'Preserve existing catalog investment through an explicit version, identity, clock and failure boundary.'},
            {'choice': 'Port catalog/client into causal core', 'disposition': 'reject for this proposal', 'reason': 'Adds duplicate platform and compatibility work without demonstrated benefit.'},
            {'choice': 'Frozen manually prepared public metadata', 'disposition': 'initial comparator', 'reason': 'Tests semantics and cost before requesting a live catalog connection.'},
            {'choice': 'Other catalog or separately named MCP/Cloud package', 'disposition': 'separate review', 'reason': 'No transferred rights, API, truth or compatibility claim.'}],
        'costs': ['Mapping and review time, supported SDK/server infrastructure, rights/entitlement, schema/version maintenance and incident investigation.', 'No bank prices or ROI inferred.'],
        'owner_obligations': contract['roles'], 'conversion_failure_contract': ref(BASE / 'proposed-export-contract.json', 'Proposed bounded export and semantic oracles'),
        'revisit_trigger': 'A selected minimal permissible pinned path, complete dependency/notice inventory and actual source-matched SDK/server fixture justify reconsidering integration.',
        'limitations': LIMITS, 'evidence': [ref(BASE / n, n) for n in ['plan.md','source-review.json','exact-results.json','omissions-register.json']]}
    write(BASE / 'decision-proposal.json', decision)
    sources = []
    for key, title, kind, path, selected, claims in [
        ('primary', 'DataHub pinned catalog models and Python client semantics', 'software_primary_sources', BASE / 'source-review.json', records[4:],
         ['Asset/field identities, lineage and audit clocks have specific metadata meanings.', 'Aspect versions/errors, 3+ hop categories, cursor accumulation and schema-field path projection are static source findings.']),
        ('rights', 'DataHub source identity, license, notices and Python dependency declarations', 'software_primary_sources', BASE / 'source-review.json', records[:4],
         ['Apache 2.0 root license/NOTICE, generated dependency declaration and dynamic version.', 'OSS/Cloud and separate MCP lead require distinct scope and rights.']),
        ('exact', 'Exact catalog ambiguity, clock, identity and traversal references', 'project_derivation', BASE / 'exact-results.json',
         [ref(ROOT / 'tools/datahub_reference_20261016.py', 'Finite enumeration and authored contract reference')],
         ['Same positive observed table with effects1/2 and0; stipulated net20/-30USD.', 'Availability leakage1 versus1/2, identity3 versus1, 3+ hop meaning and501 paged records.']),
        ('contract', 'Proposed bounded catalog export and DataHub reference decision', 'project_design', BASE / 'proposed-export-contract.json',
         [ref(BASE / 'decision-proposal.json', 'Reference decision with no integration capability'), ref(BASE / 'omissions-register.json', 'Specific remaining routes')],
         ['Versioned read-only semantic boundary, unknown/error preservation and public/generated prototype.', 'Conditional integration, alternatives, roles and full-cost categories; no actual adapter claim.'])]:
        sources.append({'integrated_citation_key': 'exec16_dh_' + key, 'title': title,
            'author': 'datahub-project contributors' if kind == 'software_primary_sources' else 'Causal banking proposal',
            'year': 2026, 'kind': kind, 'source_identity': 'https://github.com/datahub-project/datahub' if kind == 'software_primary_sources' else str(path.relative_to(ROOT)),
            'version_date': commit['sha'] + '; ' + commit['commit']['committer']['date'] if kind == 'software_primary_sources' else '2026-10-16',
            'local_copy': ref(path, title), 'records': selected, 'inspected_anchors': claims,
            'supported_claims': claims, 'limitations': LIMITS})
    write(BASE / 'source-audit.json', {'sources': sources, 'prior': ref(PRIOR, '666 preserved records'), 'cutoff': '2026-10-07'})
    text = (BASE / 'development.template').read_text().replace('§', chr(92))
    keys = {s['integrated_citation_key'] for s in prior['sources'] + sources}
    assert all(k.strip() in keys for group in re.findall(r'\\citep\{([^}]+)\}', text) for k in group.split(','))
    with (BASE / 'development.tex').open('x') as stream: stream.write(text)
    write(BASE / 'author-review.json', {'status': 'pass_for_reference_integration', 'reviewer': REVIEWER,
        'criteria_verdicts': ['pass','pass','pass'], 'findings': [
            'Sixteen genuine originals match retrieval SHA-256 and pinned Git blob identities; source/license/dependency/maintenance scope and unresolved distribution are explicit.',
            'Metadata and causal targets, clock meanings, bounded retrieval, alternative reuse routes, costs, roles and revisit conditions are developed with exact examples.',
            'Reference decision grants no integration_allowed capability; proposed conversion/failure oracle is distinguished from upstream behavior and actual adapter qualification.'],
        'evidence': [ref(BASE / n, n) for n in ['plan.md','source-review.json','omissions-register.json','decision-proposal.json',
                  'proposed-export-contract.json','exact-results.json','source-audit.json','development.tex']],
        'limitations': LIMITS, 'visual_acceptance': False})
    print(json.dumps({'sources': 16, 'new_citations': 4, 'decision': 'reference', 'integration_allowed': False}))


if __name__ == '__main__':
    main()
