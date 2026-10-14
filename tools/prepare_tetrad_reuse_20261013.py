#!/usr/bin/env python3
"""Review preserved Tetrad sources and record a scoped proposal reuse choice."""
import base64
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import build_integrated_monograph_v12 as shared
import java_adapter_oracles_20261013 as oracle
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/tetrad-reuse'
COMMIT = 'b89afaf952a4fd647df0d85b08102250106c6764'
ref = shared.ref


def save(path, value):
    if path.exists():
        raise ValueError('Preserve existing evidence: ' + str(path))
    core.write(path, value)


def main():
    primary_paths = [
        ('docs/literature/raw/v12_sw2_tetrad_pom.txt', 'pom.xml', [(7, 25), (55, 71)]),
        ('docs/literature/raw/v12_exec13_java_tetrad_libpom.txt', 'tetrad-lib/pom.xml', [(5, 26), (68, 162), (168, 176), (212, 217)]),
        ('docs/program/repair-v12/work/SW01/extracted/pinned-tetrad-README.md', 'README.md', [(14, 27), (40, 55), (79, 81)]),
        ('docs/program/repair-v12/work/SW01/extracted/pinned-tetrad-LICENSE.txt', 'LICENSE', [(1, 6), (154, 170), (195, 249)]),
        ('docs/literature/raw/v12_sw2_tetrad_pc.txt', 'tetrad-lib/src/main/java/edu/cmu/tetrad/search/Pc.java', [(1, 18)]),
        ('docs/literature/raw/v12_exec13_java_tetrad_testpc.txt', 'tetrad-lib/src/test/java/edu/cmu/tetrad/test/TestPc.java', [(145, 157), (165, 192)]),
        ('docs/literature/raw/v12_exec13_java_tetrad_fisherz.txt', 'tetrad-lib/src/main/java/edu/cmu/tetrad/search/test/IndTestFisherZ.java', [(362, 387), (404, 421)]),
        ('docs/literature/raw/v12_exec13_java_tetrad_fas.txt', 'tetrad-lib/src/main/java/edu/cmu/tetrad/search/Fas.java', [(379, 398), (471, 492)])]
    tree = core.read(ROOT, 'docs/literature/raw/v12_sw2_tetrad_tree.json')
    assert tree['sha'] == COMMIT and tree['truncated'] is False
    entries = {x['path']: x for x in tree['tree']}
    for kind, suffix in [('license', 'LICENSE.txt'), ('readme', 'README.md')]:
        raw = core.read(ROOT, f'docs/literature/raw/v12_sw_pinned_{kind}_tetrad.json')
        decoded = base64.b64decode(raw['content'])
        extracted = ROOT / ('docs/program/repair-v12/work/SW01/extracted/pinned-tetrad-' + suffix)
        assert decoded == extracted.read_bytes()
    records = []
    for local, upstream, spans in primary_paths:
        path = ROOT / local
        raw = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert blob == entries[upstream]['sha'], upstream
        lines = raw.decode().splitlines()
        anchors = [{'lines': [lo, hi], 'text': '\n'.join(lines[lo-1:hi])} for lo, hi in spans]
        records.append({'local_copy': ref(path, '; '.join(f'lines {a}-{b}' for a, b in spans)),
                        'source_identity': f'https://raw.githubusercontent.com/cmu-phil/tetrad/{COMMIT}/{upstream}',
                        'git_blob_sha1': blob, 'tree_identity_verified': True,
                        'inspected_anchors': anchors})
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
    library = ET.parse(ROOT / 'docs/literature/raw/v12_exec13_java_tetrad_libpom.txt').getroot()
    deps = [{k: item.findtext('m:' + k, namespaces=ns) for k in ['groupId', 'artifactId', 'version', 'scope', 'optional']}
            for item in library.findall('./m:dependencies/m:dependency', ns)]
    assert len(deps) == 20
    primary = {'source_revision': COMMIT, 'snapshot_version': '7.6.11-SNAPSHOT',
               'cutoff': '2026-10-07', 'review_date': '2026-10-13',
               'tree': ref(ROOT / 'docs/literature/raw/v12_sw2_tetrad_tree.json', 'Identity only; technical claims use source files'),
               'commit': ref(ROOT / 'docs/literature/raw/v12_sw_cutoff_commit_tetrad.json', 'Recorded 2026-09-22 commit before cutoff'),
               'records': records, 'library_declared_dependencies': deps,
               'dependency_count': 20, 'resolved_runtime_dependency_inventory': False,
               'compiler_release': 21, 'bridge_readme_jdk': '25+',
               'source_grant': 'GPL v3 root; inspected PC header GPL v3 or later',
               'maintenance_evidence': 'README build/test and issue routes; inspected upstream tests; no observed CI/SLA',
               'limits': ['Source inspection is not execution.', 'Module declarations are not a resolved runtime closure.']}
    save(BASE / 'primary-review.json', primary)
    calculated = {'kind': 'exact_proposal_adapter_references', 'java_executed': False, 'random_draws': 0,
                  'gaussian_equivalence_class': oracle.chain_class(), 'endpoint_codec': oracle.endpoints(),
                  'unit_transformation': oracle.unit_transformation(), 'scientific_identity': oracle.identity_mutations()}
    calculated = json.loads(json.dumps(calculated, default=str))
    assert calculated == core.read(ROOT, 'docs/program/execution/2026-10-13/java-integration/oracle-results.json')
    reproduction = {'status': 'pass', 'reproduced_groups': 4, 'new_random_draws': 0, 'java_executed': False,
                    'matches_preserved_results': True,
                    'program': ref(ROOT / 'tools/java_adapter_oracles_20261013.py', 'Exact reference program; not engine output'),
                    'results': ref(ROOT / 'docs/program/execution/2026-10-13/java-integration/oracle-results.json', 'Independent exact graph, unit and context reference')}
    save(BASE / 'reproduction-review.json', reproduction)
    decision = {
        'operation_id': 'SW.DECISION.inherited_tetrad',
        'canonical_package': 'cmu-phil/tetrad', 'source_identity': 'https://github.com/cmu-phil/tetrad',
        'aliases': ['Tetrad', 'tetrad-lib', 'Tetrad GUI'],
        'bridge_boundary': 'Python/R bridges add their own interfaces and environments; they are not independent Java engines or automatically qualified integrations.',
        'decision': 'defer', 'preferred_next_route': 'Restricted local Java PC/Fisher-Z adapter at the selected commit',
        'decision_scope': 'Defer executable adapter admission while selecting this source as the preferred Java prototype candidate.',
        'pinned_revision': COMMIT, 'version': '7.6.11-SNAPSHOT', 'revision_date': '2026-09-22', 'cutoff': '2026-10-07',
        'integration_allowed': False, 'runtime_qualification': False, 'deployment_allowed': False,
        'primary_evidence': ref(BASE / 'primary-review.json', 'Eight exact source identities, license and twenty active dependency declarations'),
        'source_audits': [ref(ROOT / 'docs/program/execution/2026-10-13/java-discovery/source-audit.json', 'Existing algorithm/source review'),
                          ref(ROOT / 'docs/program/execution/2026-10-13/java-integration/source-audit.json', 'Existing request/failure profile')],
        'selected_profile': 'Complete IID continuous linear Gaussian PC; causal sufficiency, acyclicity, faithfulness and no unmodeled selection; fixed settings in adapter contract.',
        'target_and_uncertainty': 'CPDAG discovery with preserved downstream question, units, clock, sampling and assumptions. No numeric effect, calibrated effect region or verified graph truth.',
        'conversion_failure_contract': ref(ROOT / 'docs/program/comprehensive-v14/work/IN.DESIGN.Java/adapter-contract.json', 'Bijection, endpoints, scientific context, job failure and graph recognition'),
        'behavioral_oracle': ref(BASE / 'reproduction-review.json', 'Four independently executed project reference groups, no Java run'),
        'reason': ['Method-specific source, existing exact references and the adapter contract make PC a concrete candidate.',
                   'No full pinned build/dependency closure, compiled failure wrapper or engine comparison is recorded.',
                   'Fisher-Z source maps singular-matrix exceptions to dependence on the default check path; the proposed getResult wrapper needs actual interface and failure qualification.',
                   'Parallel FAS interruption and graph-class validation need whole-job records before publication.'],
        'alternatives': [
            {'route': 'Adopt unrestricted Tetrad API', 'decision': 'reject_for_selected_route', 'reason': 'Would expose unreviewed algorithms, defaults and observation laws under one apparent guarantee.'},
            {'route': 'Port PC', 'decision': 'defer', 'reason': 'No measured integration constraint justifies new algorithm/orientation/test maintenance.'},
            {'route': 'Selected R/Python PC candidate', 'decision': 'retain_as_matched_comparator', 'reason': 'Requires its own pinned source, test configuration, rights and runtime; no parity assumed.'},
            {'route': 'Weka predictive networks or commercial latent fits', 'decision': 'separate_operation', 'reason': 'Different scientific object; useful baselines only for matched modeling operations.'},
            {'route': 'FCI/FGES/IDA and bridge surfaces', 'decision': 'separate_profiles', 'reason': 'Additional graph, score, effect or environment assumptions; no inherited admission.'}],
        'rights_and_maintenance': {'local_route': 'GPL basic permissions support consideration of local research, subject to applicable grants and third-party terms.',
                                 'distribution': 'Keep notices, license and corresponding-source obligations for the actual arrangement; process separation is not a blanket exemption.',
                                 'unresolved': ['Effective runtime/build artifact and license inventory', 'Runtime/bridge version reconciliation', 'Measured CI, upkeep and behavior across upgrades']},
        'costs_to_measure': ['Environment setup and disk', 'Full-request latency and peak memory', 'Conversion and analyst correction', 'Maintenance and upgrade regression', 'Failed/cancelled/unsupported task costs'],
        'owner_obligations': {'adapter_maintainer': 'Lock compiler/runtime/dependencies and inspect grants; implement failure wrapper.',
                              'scientific_reviewer': 'Check scoped assumptions, graph recognition and matched references.',
                              'workflow_owner': 'Measure all-request workflow and failure behavior against a usable comparator.'},
        'revisit_trigger': 'Actual pinned build and dependency/rights inventory plus wrapper/interface, CPDAG, numerical-failure, cancellation and conversion results; reopen choice on revision, license, API, dependency or scientific-target change.',
        'scientific_capability_awarded': False, 'bank_inputs_required_for_next_step': False}
    output = ROOT / 'docs/program/comprehensive-v14/work/SW.DECISION.inherited_tetrad/decision.json'
    save(output, decision)
    sources = [
        {'integrated_citation_key': 'exec13_tetrad_reuse_primary', 'kind': 'software_primary_sources',
         'title': 'Tetrad pinned build, license, maintenance and failure source review',
         'author': 'cmu-phil/tetrad', 'year': 2026, 'source_identity': 'https://github.com/cmu-phil/tetrad',
         'version_date': COMMIT + '; 2026-09-22; 7.6.11-SNAPSHOT; inspected 2026-10-13',
         'local_copy': records[0]['local_copy'], 'records': records,
         'derived_inventory': ref(BASE / 'primary-review.json', 'XML active-declaration extraction; not executed dependency resolution'),
         'inspected_anchors': [r['local_copy']['anchor'] for r in records],
         'supported_claims': ['Twenty direct library POM declarations; Java21 compiler and bridge README25+; GPL grant and conveyance terms.',
                              'Source tests and issue routes exist; no CI or runtime acceptance is inferred.'],
         'limits': ['No Java execution or resolved runtime distribution.']},
        {'integrated_citation_key': 'exec13_tetrad_reuse_decision', 'kind': 'project_design',
         'title': 'Tetrad reuse choice for a restricted causal discovery prototype',
         'author': 'Causal banking proposal project', 'year': 2026,
         'source_identity': str(output.relative_to(ROOT)), 'version_date': '2026-10-13; author proposal decision',
         'local_copy': ref(output, 'Decision, alternatives, responsibilities and revisit conditions'),
         'inspected_anchors': ['decision_scope; selected_profile; reason; alternatives; rights_and_maintenance; revisit_trigger'],
         'supported_claims': ['Preferred Java PC candidate; executable admission deferred with concrete remaining conditions.'],
         'limits': ['No scientific capability, engine execution or deployment awarded.']}]
    audit = {'sources': sources, 'cutoff': '2026-10-07',
             'reproduction': ref(BASE / 'reproduction-review.json', 'Independent exact reference replay')}
    shared.verify_refs(audit)
    save(BASE / 'source-audit.json', audit)
    print(json.dumps({'decision': decision['decision'], 'integration_allowed': False,
                      'primary_files': len(records), 'declared_dependencies': len(deps), 'exact_examples_reproduced': 4}))


if __name__ == '__main__':
    main()
