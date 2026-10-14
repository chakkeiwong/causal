#!/usr/bin/env python3
"""Publish the reviewed I3 working successor without awarding proposal acceptance."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/workspace'
OUT = BASE / 'reader'
OP = 'TEXT.DRAFT.I3'
ref = shared.ref


def write(path, value):
    assert not path.exists(), 'Preserve evidence: ' + str(path)
    core.write(path, value)


def main():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    assert state['reader']['path'] == 'docs/causal_proposal_evaluation_design_2026-10-13.pdf'
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads((ROOT / 'docs/program/execution/2026-10-13/live-evaluation/reader/source-audit.json').read_text())
    for name in ['source-audit.json', 'prepared-inputs.json', 'reader/source-audit.json']:
        shared.verify_refs(json.loads((BASE / name).read_text()))
    old_driver = ROOT / 'docs/causal_proposal_evaluation_design_2026-10-13.tex'
    old_tail = ROOT / 'docs/program/execution/2026-10-13/interfaces/integration-tail.tex'
    expected = old_driver.read_text().replace(
        r'\input{program/execution/2026-10-13/interfaces/integration-tail.tex}',
        r'\input{program/execution/2026-10-13/workspace/integration-tail.tex}', 1).replace(
        'program/execution/2026-10-13/live-evaluation/refs}',
        'program/execution/2026-10-13/live-evaluation/refs,program/execution/2026-10-13/workspace/refs}', 1)
    assert (ROOT / report['driver']['path']).read_text() == expected
    old_files = [x for x in prior['tex_files'] if x['path'] != str(old_driver.relative_to(ROOT))]
    for item in old_files:
        core.bound(ROOT, item)
    a, b = old_tail.read_text(), (BASE / 'integration-tail.tex').read_text()
    end = r'\chapter{Operating the local causal service and qualifying its limits}'
    assert a.split(end, 1)[1] == b.split(end, 1)[1]
    assert a.split(r'\chapter{Workspace', 1)[0] == b.split(r'\input{program/comprehensive-v14/work/TEXT.DRAFT.I3/chapter.tex}', 1)[0]
    old_sources = {s['integrated_citation_key']: s for s in prior['sources']}
    new_sources = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(new_sources[k] == v for k, v in old_sources.items())
    assert set(new_sources) - set(old_sources) == {
        'exec13_i3_inspection', 'exec13_i3_examples', 'exec13_i3_approximation', 'exec13_i3_composition'}
    for first, second in [('examples', 'replay'), ('approximation', 'approximation-replay'),
                          ('composition', 'composition-replay')]:
        assert (BASE / (first + '.json')).read_bytes() == (BASE / (second + '.json')).read_bytes()
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['18,550.62', '47,825.93', '33,188.28', '30,260.75', '36,115.81',
                   '45.625', '2300', '2900', 'not bank estimates', 'no sibling consumer was executed']:
        assert phrase in text, phrase
    assert not any('Overfull' in w or 'undefined' in w.lower() for w in report['warnings'])
    chapter = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I3/chapter.tex'
    names = ['plan-review.md', 'primary-inspection.json', 'primary-accounting-inspection.json',
             'examples.json', 'replay.json', 'approximation.json', 'approximation-replay.json',
             'composition.json', 'composition-replay.json', 'independent-calculation-review.json',
             'substantive-review.md', 'source-audit.json', 'prepared-inputs.json', 'refs.bib']
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
              'scope': 'I3 developed draft, reproduced project examples and preserving reader delta',
              'old_compiled_files_unchanged': len(old_files), 'prior_citation_records_unchanged': len(old_sources),
              'new_citation_records': 4, 'i2_and_i4_retained': True,
              'findings': ['Four banking journeys have connected targets, derivations, diagnostics and substantive alternatives.',
                           'All 18 observed directories have dated dispositions; four primary interface declarations were reinspected.',
                           'Three scripts replay identically; sequential values have an additional independent marginal calculation.',
                           'Population change, overlapping actions, numerical error and accounting ownership retain their scientific conditions.',
                           'Old compiled sources and citation records are unchanged; references and physical text bounds pass.',
                           'No executed sibling adapter, statistical calibration, bank or visual qualification is claimed.'],
              'evidence': [ref(chapter, 'Developed I3 wrapper')] + [ref(BASE / n, n) for n in names] + [
                  ref(OUT / 'build-report.json', 'Exact compiled successor'),
                  ref(OUT / 'text-layout-review.json', 'Physical text bounds')], 'visual_acceptance': False}
    write(BASE / 'release-source-review.json', review)
    code = ['workspace_examples_20261013.py', 'workspace_approximation_20261013.py',
            'workspace_composition_20261013.py', 'build_workspace_reader_20261013.py',
            'publish_workspace_reader_20261013.py']
    release = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
               'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
               'build_report': ref(OUT / 'build-report.json', 'I3 integration'),
               'source_review': ref(BASE / 'release-source-review.json', 'Reviewed claims and preserving delta'),
               'text_layout': ref(OUT / 'text-layout-review.json', 'Whole-reader physical bounds'),
               'source_artifacts': audit['tex_files'] + [ref(BASE / n, 'New chapter evidence') for n in names + ['release-source-review.json']] +
                                   [ref(ROOT / 'tools' / n, 'Reference/build/publication code') for n in code],
               'visual_acceptance': False, 'mandatory_repairs_closed': [],
               'changes': ['Developed workspace/standalone case studies for all four banking journeys.',
                           'Added exact value, clock, sequential policy, graph, selection, numerical error and portfolio examples.',
                           'Retained dated source evidence and proposal-versus-implementation boundaries.'],
               'sponsor_binding': 'Prior sponsor preserved; exact reader reconciliation remains Q5 work.'}
    write(BASE / 'working-release.json', release)
    binding = ref(BASE / 'working-release.json', 'Reviewed I3 working reader')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_workspace_working_reader', 'manifest': binding,
                                  'original_gap_qualification': False, 'final_acceptance': False})
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope='Developed I3 draft integrated in the main working monograph',
                   reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
                   limitations=['Separate TEXT.REVIEW.I3 covers substantive allocation and depth.',
                                'No actual sibling adapter, consumer, statistical coverage or bank qualification.',
                                'Rendered visual acceptance remains pending under the inherited session image limit.'],
                   outputs=[ref(chapter, 'Connected workspace and standalone chapter')], nonexecution_reason='', revisit_trigger='')
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'pass', 'finding': 'Four connected banking journeys, all directory dispositions, target/clock/numerical/value derivations and complete proposed consumer trials are developed.',
         'evidence': [ref(chapter, 'Developed chapter'), ref(BASE / 'substantive-review.md', 'Detailed author review'), binding]},
        {'index': 1, 'verdict': 'pass', 'finding': 'New claims have primary/project audits; three exact example scripts replay; actual local evidence, proposed integrations and later acceptance remain distinct.',
         'evidence': [ref(BASE / 'source-audit.json', 'Audited sources and references'),
                      ref(BASE / 'independent-calculation-review.json', 'Independent calculation checks'),
                      ref(BASE / 'release-source-review.json', 'Exact release delta review')]}]
    path = BASE / (OP + '.receipt.json')
    write(path, receipt)
    print(json.dumps({'published': state['reader'], 'receipt': str(path.relative_to(ROOT))}))


if __name__ == '__main__':
    main()
