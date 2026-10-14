#!/usr/bin/env python3
"""Bind manuscript demonstration locations to replay evidence; not acceptance."""
import hashlib
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as manuscript
from replay_proposal_demonstrations_20261013 import ref

ROOT = manuscript.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/prototype-review'
READER = ROOT / 'docs/causal_proposal_temporal_information_2026-10-13.pdf'

PROJECT = {
    'exec13_diagram_examples': 'exact-replay/diagrams.json',
    'exec13_diagram_restrictions': 'exact-replay/restrictions.json',
    'exec13_examples': 'exact-replay/software-contract.json',
    'exec13_formulation_targets': 'exact-replay/formulation-targets.json',
    'exec13_grf_design': None,
    'exec13_grf_oracle': 'native-temporal-replay/native/reproduction-review.json',
    'exec13_i2_examples': 'runtime-replay/examples/review.json',
    'exec13_interchange_composition': 'exact-replay/composition.json',
    'exec13_interchange_examples': 'exact-replay/interchange.json',
    'exec13_interchange_runtime': 'runtime-replay/examples/review.json',
    'exec13_java_adapter_contract': None,
    'exec13_java_adapter_oracles': 'exact-replay/java-adapter.json',
    'exec13_java_examples': 'exact-replay/java-discovery.json',
    'exec13_latent_examples': 'exact-replay/commercial-latent.json',
    'exec13_ontology_examples': 'exact-replay/ontology.json',
    'exec13_persistent_derivation': 'exact-replay/persistent-region.json',
    'exec13_persistent_examples': 'exact-replay/persistent-region.json',
    'exec13_persistent_predecessor': 'master-request-replay/receipt.json',
    'exec13_pydisc_examples': 'python-discovery-wrapper-replay.json',
    'exec13_servicing_argument': 'exact-replay/servicing.json',
    'exec13_servicing_exact': 'exact-replay/servicing.json',
    'exec13_servicing_predecessor': 'master-request-replay/receipt.json',
    'exec13_survey_comparison': 'exact-replay/survey-comparison.json',
    'exec13_temporal_argument': 'native-temporal-replay/temporal/reproduction-review.json',
    'exec13_temporal_exact': 'native-temporal-replay/temporal/reproduction-review.json',
    'exec13_temporal_predecessor': 'master-request-replay/receipt.json',
    'exec13_tetrad_reuse_decision': None,
    'exec13_y0_contract': None,
    'exec13_y0_oracles': 'exact-replay/python-identification.json',
    'pd15_profile': 'public-profile-replay/receipt.json',
    'v12_in_contract': 'runtime-replay/examples/review.json',
    'v12_in_inventory': None,
    'v12_in_runtime': 'runtime-replay/faults.json',
    'v131_project_semantics': 'exact-replay/semantic-v131.json',
    'v13_project_exact': 'exact-replay/design-v13.json',
}
HISTORY = {
    'R3-': ['inherited-witness-replay/receipt.json', 'foundation-replay/receipt.json', 'verifiers/revision/replay.json'],
    'S-C': ['verifiers/completion/replay.json'],
    'T-C': ['verifiers/scope/replay.json'],
    'U-C': ['archived/dynamic/replay.json'],
    'W-C': ['archived/linkage/replay.json'],
    'C-G': ['archived/closure/replay.json'],
    'E-R': ['archived/reliability/replay.json'],
    'F-R': ['archived/calibration/replay.json'],
    'J-R': ['verifiers/precision/replay.json'],
}


def main():
    output = BASE / 'demonstration-inventory.json'
    if output.exists():
        raise ValueError('Preserve earlier review index')
    files = manuscript.scan(READER.with_suffix('.tex'))
    labels = {}
    for path, text in files:
        for m in re.finditer(r'\\label\{([^}]+)\}', text):
            labels.setdefault(m[1], []).append({'path': str(path.relative_to(ROOT)),
                'line': text.count('\n', 0, m.start()) + 1})
    claims_path = ROOT / 'docs/literature/reconstruction-claims.json'
    claims = json.loads(claims_path.read_text())
    rows, issues = [], []
    for claim in claims:
        artifacts = claim.get('artifacts', [])
        if not artifacts:
            continue
        locations = labels.get(claim['manuscript_anchor'], [])
        replays = next((paths for prefix, paths in HISTORY.items() if claim['id'].startswith(prefix)), None)
        if replays is None:
            issues.append('Unmapped inherited claim: ' + claim['id'])
        rows.append({'claim_id': claim['id'], 'claim': claim['claim'], 'evidence_class': claim['evidence_class'],
                     'manuscript_anchor': claim['manuscript_anchor'], 'compiled_locations': locations,
                     'current_reader_contains_anchor': bool(locations),
                     'artifact_locations': artifacts,
                     'replay_evidence': [ref(BASE / p) for p in replays or []],
                     'version_rule': 'Runtime/scientific identities come from the bound study receipts, including preserved archival views. A current path alone is not a historical version.',
                     'fresh_simulator_reexecution_of_all_requests': False})
    context = json.loads((BASE / 'source-contexts.json').read_text())
    project = []
    for record in context['records']:
        if not record['kind'].startswith('project'):
            continue
        key = record['citation_key']
        if key not in PROJECT:
            issues.append('Unmapped project citation: ' + key)
            continue
        target = PROJECT[key]
        project.append({'citation_key': key, 'kind': record['kind'],
                        'supported_claims': record['supported_claims'], 'limits': record['limits'],
                        'compiled_locations': [{k: c[k] for k in ('path', 'line')} for c in record['citation_contexts']],
                        'source_evidence': record['local_copies'],
                        'replay_evidence': ref(BASE / target) if target else None,
                        'disposition': 'bounded_executed_evidence_or_argument_examples' if target else 'design_or_read_only_inspection_no_executed_integration_claim'})
    additional = [
        ('earlier-finite-witnesses', ['r3:nonidentification'], ['inherited-witness-replay/receipt.json'], 'Eighteen exact witness families; not general theorem validation'),
        ('foundational-examples', [], ['foundation-replay/receipt.json'], 'Six seeded or finite families; old environment metadata is retained, not regenerated'),
        ('weak-audit', ['v11:weak-audit'], ['verifiers/weak-audit/replay.json'], 'Saved sets and 3000 requests reconstructed'),
        ('weak-audit-sharpening', [], ['verifiers/weak-sharpening/replay.json'], 'Saved sharpened sets reconstructed with prior adverse work preserved'),
        ('linked-funding', [], ['verifiers/linked-funding/replay.json'], 'All saved intervals/counts reconstructed; eight fixed requests regenerated; 600-request failure retained'),
        ('master-studies', ['integrated:master_execution'], ['master-request-replay/receipt.json'], 'Fifteen representative requests across five frozen studies; their full study claims remain historical'),
        ('offline-agent', [], ['agent-replay/receipt.json', 'agent-tests.xml'], 'Six real local workflow paths and 29 tests; zero live-model calls'),
        ('llm-illustrations', [], ['exact-replay/llm-census.json'], 'Exact hypothetical measurement and policy arithmetic; no model benchmark'),
        ('current-interfaces', [], ['runtime-replay/examples/review.json', 'runtime-replay/faults.json'], 'Thirteen CLI/library cases, report lifecycle and nine faults; MCP evidence is the preserved installed-SDK run'),
        ('public-bank-profile', [], ['public-profile-replay/receipt.json'], 'Four descriptive tables regenerated from the same public archive; no causal-effect experiment'),
    ]
    extra = [{'id': name, 'labels': anchors, 'replay_evidence': [ref(BASE / p) for p in paths], 'scope': scope}
             for name, anchors, paths, scope in additional]
    # This index preserves design-only status for all six new public study families.
    public_designs = []
    state = json.loads((ROOT / 'docs/program/state.json').read_text())
    for i in range(1, 7):
        key = f'P{i}.DESIGN'
        result = state['execution_runtime']['results'][key]
        public_designs.append({'id': key, 'design_receipt': result,
                              'credited_as_final_public_study_execution': False})
    value = {'status': 'pass' if not issues else 'fail', 'issues': issues,
             'reviewed_reader': ref(READER), 'driver': ref(READER.with_suffix('.tex')),
             'index_code': ref(Path(__file__)), 'historical_claim_register': ref(claims_path),
             'compiled_sources': [ref(p) for p, _ in files], 'inherited_claims': rows,
             'project_citations': project, 'additional_families': extra, 'public_designs': public_designs,
             'review_boundary': 'This index binds locations and evidence. The author review decides adequacy and limitations; no automated acceptance.',
             'source_audit_followup': context['issues']}
    output.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'status': value['status'], 'issues': issues, 'inherited_claims': len(rows),
                      'compiled_inherited_claims': sum(r['current_reader_contains_anchor'] for r in rows),
                      'project_records': len(project), 'compiled_sources': len(files)}))


if __name__ == '__main__':
    main()
