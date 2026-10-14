#!/usr/bin/env python3
"""Prepare a reviewed native-route decision without authorizing an adapter."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/grf-native-decision'
OLD = ROOT / 'docs/program/execution/2026-10-13/grf-cxx'
OP = 'SW.DECISION.seed_080'
ref = shared.ref


def main():
    state = core.read(ROOT, core.STATE)
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    assert OP not in state['execution_program']['results']
    audit = json.loads((OLD / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    contract_path = ROOT / 'docs/program/comprehensive-v14/work/IN.DESIGN.Cxx/adapter-contract.json'
    contract = json.loads(contract_path.read_text())
    assert contract['engine']['commit'] == '5bee99b51471f76cb2d63acbc8a9b0ffec408ba0'
    assert contract['engine']['runtime_admitted'] is False
    evidence = [ref(OLD / name, 'Preserved reviewed source/design/reference') for name in
                ['source-audit.json', 'author-review.json', 'adapter.md', 'adapter.tex',
                 'reproduction-review.json', 'wire-examples.json']]
    evidence += [ref(contract_path, 'Exact target/conversion/failure/qualification contract'),
                 ref(ROOT / 'docs/program/repair-v12/candidate-seeds.json', 'Native seed and inherited package identities'),
                 ref(ROOT / 'docs/literature/raw/v12_sw2_cutoff_grf.json', 'Upstream commit identity/date only'),
                 ref(ROOT / 'docs/literature/raw/v12_exec13_grfcxx_5.txt', 'Package requirements, maintainer, bug tracker and license'),
                 ref(ROOT / 'docs/literature/raw/v12_exec13_grfcxx_6.txt', 'C++17 executable build with test/source collection'),
                 ref(ROOT / 'docs/literature/raw/v12_gap3_grf_license.txt', 'GPLv3 primary text, Section 2 and distribution terms')]
    reading = {
        'status': 'pass', 'issues': [], 'source_revision': contract['engine']['commit'],
        'inspections': [
            {'anchor': 'DESCRIPTION: Version, Authors@R, BugReports, Depends, LinkingTo, Imports, License, SystemRequirements',
             'finding': 'Version 2.6.1, named maintainer/issue tracker, GPL-3 and R/native requirements re-inspected.'},
            {'anchor': 'CMakeLists: CMAKE_CXX_STANDARD, GLOB_RECURSE and add_executable',
             'finding': 'C++17 executable source/test collection does not establish a stable shared-library ABI.'},
            {'anchor': 'COPYING Section 2, lines 153 onward',
             'finding': 'Permission to run unmodified program is explicit; no distribution/dependency clearance inferred.'},
            {'anchor': 'adapter.md: Deployment choices and the next informative comparison',
             'finding': 'Current monograph already recommends R/native first and rejects initial direct embedding pending parity.'}],
        'evidence': evidence, 'runtime_executed': False}
    core.write(BASE / 'source-review.json', reading)
    reader = {k: state['reader'][k] for k in ['path', 'sha256']}
    reader['anchor'] = 'Current monograph: native forest boundary and deployment choices'
    output = ROOT / node['outputs'][0]
    decision = {
        'operation_id': OP, 'outcome': 'pass', 'execution': 'performed',
        'decision': 'reject_initial_direct_native_embedding_and_algorithm_port',
        'preferred_route': 'Pinned isolated R process invoking the maintained native core, subject to separate runtime admission',
        'candidate': 'seed:080', 'canonical_family': 'grf-labs/grf',
        'alias_relation': 'Native core of inherited:grf; distinct integration route, same engine lineage',
        'engine': contract['engine'], 'integration_allowed': False, 'capabilities': [],
        'target_and_exclusions': contract['scope'], 'failure_contract': contract['responses'],
        'environment_and_rights': contract['deployment'],
        'maintenance_evidence': 'Dated pinned commit, named maintainer and tracker, source test/build machinery; no support SLA or installed test result.',
        'cost_evidence': 'No measured R/native workload comparison; direct embedding transfers statistical and lifetime ownership without established savings.',
        'owner_obligations': contract['admission_sequence'],
        'revisit_trigger': 'Concrete host constraint or measured identical-workload benefit, plus complete environment/rights and native/R statistical/lifetime/reload/failure parity evidence.',
        'evidence': evidence + [ref(BASE / 'decision.md', 'Developed reuse rationale and alternatives'),
                                 ref(BASE / 'source-review.json', 'Bounded primary re-inspection')],
        'manuscript': {'current_reader': reader,
                       'source': ref(OLD / 'adapter.tex', 'Already integrated substantive route comparison'),
                       'new_pages_needed': False, 'reason': 'The exact decision and alternatives already appear in the current reader; this closes the matching ledger decision without duplicate narrative.'},
        'independent_acceptance': False, 'runtime_qualified': False}
    core.write(output, decision)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed',
                   scope='Reviewed initial native reuse decision; no integration capability granted',
                   reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
                   capabilities=[], outputs=[ref(output, 'Pinned native route choice and rejection reasons')],
                   limitations=['No installed grf engine, runtime performance, forest coverage or distribution/dependency clearance.',
                                'R-package reuse/admission remains its own reviewed operation; this native alias does not grant it by inheritance.'],
                   nonexecution_reason='', revisit_trigger=decision['revisit_trigger'])
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'pass', 'finding': 'Resolved native/R alias at an exact commit; primary package, license and build/dependency sources plus bounded maintenance identity are bound with explicit limitations.',
         'evidence': [ref(BASE / 'source-review.json', 'Re-inspected sources and precise scope'), ref(output, 'Alias and source resolution')]},
        {'index': 1, 'verdict': 'pass', 'finding': 'The developed decision distinguishes ATE/CATE and uncertainty, compares R/native/port alternatives, specifies full-workflow costs and owner duties, and names a concrete reversal trigger.',
         'evidence': [ref(BASE / 'decision.md', 'Developed rationale'), ref(contract_path, 'Mathematical/conversion/failure obligations')]},
        {'index': 2, 'verdict': 'pass', 'finding': 'Rejects initial direct embedding/port with evidence-based reasons; integration_allowed remains false. Existing exact references are labeled project arithmetic, not qualified forest execution.',
         'evidence': [ref(output, 'No capability grant'), ref(OLD / 'reproduction-review.json', 'Scoped exact reference'), reader]}]
    core.write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'receipt': str((BASE / 'operation-receipt.json').relative_to(ROOT)),
                      'outcome': 'pass', 'integration_allowed': False, 'narrative_already_integrated': True}))


if __name__ == '__main__':
    main()
