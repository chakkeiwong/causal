#!/usr/bin/env python3
"""Record a reviewed, preserving working reader and honest bounded coverage."""
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-13/python-discovery'
OUT = BASE/'reader'
OP = 'SW.CELL.discovery_iid.Python'
ref = shared.ref


def write(path, value):
    if path.exists():
        raise ValueError('Preserve existing evidence: '+str(path))
    core.write(path, value)


def main():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    assert state['reader']['path'] == 'docs/causal_proposal_interfaces_2026-10-13.pdf'
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    shared.verify_refs(audit)
    shared.verify_refs(json.loads((BASE/'prepared-inputs.json').read_text()))
    bounds = json.loads((OUT/'text-layout-review.json').read_text())
    assert bounds['status'] == 'pass' and bounds['pages'] == report['pages']
    assert not any('Overfull' in w or 'undefined' in w for w in report['warnings'])
    assert json.loads((BASE/'reproduction-review.json').read_text())['status'] == 'pass'
    pages = (OUT/'reader.txt').read_text().split('\f')
    first = next(i for i,p in enumerate(pages) if 'A funding analyst can obtain' in p)
    last = next(i for i in range(first,len(pages)) if 'Adding another optimizer does not answer that question.' in pages[i])
    body = '\n'.join(pages[first:last+1])
    assert last-first+1 == report['python_discovery']['physical_span'] == 9
    for term in ['0.25 million', '50.32', '0.467', '3.168', 'GaussL0penIntScore', '10−8', 'CDT']:
        assert term in body, 'Missing extracted anchor: '+term
    write(BASE/'chapter-text-review.json', {
        'status': 'pass', 'scope': 'Extracted text and source inspection, not rendered visual acceptance',
        'pdf': report['pdf'], 'section': ref(BASE/'comparison.tex', 'Ten connected subsections, source comparison and derived examples'),
        'physical_pages': list(range(first+1,last+2)), 'printed_span': report['python_discovery'],
        'page_word_counts': [len(p.split()) for p in pages[first:last+1]],
        'page_credit': 'Nine-page physical span shares its boundary pages with neighboring sections; no independent MR01 depth acceptance.',
        'findings': ['Comparison table, named assumptions and financial quantities survive extraction.',
                     'Citations resolve; no overfull text or physical-boundary failure.',
                     'Mathematical glyphs require the still-pending visual review; extraction is not visual acceptance.'],
        'visual_acceptance': False})
    inputs = [BASE/p for p in ['author-review.md','source-audit.json','candidate-register.json',
                              'omissions-register.json','reproduction-review.json','chapter-text-review.json',
                              'build-repair.json','recovery-audit.json']]
    write(BASE/'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': {'name': 'Current author/coordinator', 'kind': 'author'},
        'scope': 'Incremental source/claim correctness and preserving integration; the full software cell remains inconclusive',
        'evidence': [ref(p, 'Reviewed evidence for this bounded delivery') for p in inputs],
        'limits': ['No engine execution or calibrated effects', 'Not independent review or bank evidence',
                   'No full Python census, MR01 or Q1–Q5 acceptance', 'Visual acceptance remains pending']})
    release = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'],
        'pages': report['pages'], 'supersedes': {k: state['reader'][k] for k in ['path','sha256']},
        'build_report': ref(OUT/'build-report.json', 'Compiled preserving Python discovery successor'),
        'source_review': ref(BASE/'release-source-review.json', 'Author source and claim review'),
        'text_layout': ref(OUT/'text-layout-review.json', 'Whole-reader text and physical bounds'),
        'source_artifacts': audit['tex_files']+[ref(p, 'Working successor source/evidence') for p in
            inputs+[BASE/'refs.bib',BASE/'prepared-inputs.json',
                    ROOT/'tools/build_python_discovery_reader_20261013.py',
                    ROOT/'tools/audit_python_discovery_20261013.py',
                    ROOT/'tools/python_discovery_examples_20261013.py',
                    ROOT/'tools/review_python_discovery_examples_20261013.py', Path(__file__)]],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Nine-family Python discovery comparison integrated into the existing software chapter.',
                    'Six deterministic examples independently checked; USD0.25million funding-margin calculation reproduced.',
                    'Source, version, license, selection and numerical limitations developed; two essential coverage omissions retained.'],
        'sponsor_binding': 'Prior sponsor snapshot is not silently rebound; exact-reader coherence remains Q5 work.'}
    release_path = BASE/'working-release.json'
    write(release_path,release)
    binding = ref(release_path,'Reviewed505-page working monograph')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_python_discovery_working_reader','manifest':binding,
                                 'original_gap_qualification':False,'final_acceptance':False})
    graph,_,_ = run.combined(ROOT,state)
    node = run.ledger.operation(graph,OP)
    output = ROOT/node['outputs'][0]
    write(output,{'operation':OP,'outcome':'inconclusive','candidate_families':9,
        'scope':'Bounded inherited candidates and two named additions, selected static mechanisms',
        'candidate_register':ref(BASE/'candidate-register.json','Identities, aliases, cutoff and stopping rule'),
        'source_audit':ref(BASE/'source-audit.json','Twelve incremental source records'),
        'omissions':ref(BASE/'omissions-register.json','Two essential unresolved coverage groups'),
        'examples':ref(BASE/'reproduction-review.json','Independent deterministic checks'),
        'manuscript':ref(BASE/'comparison.tex','Developed argument'),
        'working_release':binding,'full_cell_closed':False})
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',
        scope='Nine-family source comparison, six exact examples and preserving505-page reader; full Python coverage remains incomplete',
        reviewer={'name':'Current author/coordinator','kind':'author'},
        limitations=['Only10 of655 inherited metadata hits inspected; complementary method-family search remains.',
                     'CDT delegated templates, versions, ordering and metadata conflicts remain unresolved.',
                     'No downloaded engine execution, empirical qualification, visual acceptance or MR01 closure.'],
        outputs=[ref(output,'Reviewed bounded Python discovery coverage')],
        nonexecution_reason='Not applicable: source review, manuscript development and exact calculations performed.',
        revisit_trigger='Acquire and disposition the two essential groups in omissions-register.json under a reviewed successor coverage contract; preserve this receipt.')
    receipt['criteria']=[
        {'index':0,'verdict':'inconclusive','finding':'All nine declared families and aliases have cutoff source identities; full candidate coverage is limited by the truncated inherited search and unresolved neighboring methods.',
         'evidence':[ref(BASE/'candidate-register.json','Finite search and candidate dispositions'),ref(BASE/'omissions-register.json','Essential search continuation')]},
        {'index':1,'verdict':'pass','finding':'New technical claims bind authentic originals, versions, dates, hashes and inspected anchors; scholarly PDFs are genuine and correctly named; project examples independently reproduce.',
         'evidence':[ref(BASE/'source-audit.json','Primary sources and correctly named papers'),ref(BASE/'reproduction-review.json','Reproduced algebra'),ref(BASE/'release-source-review.json','Author claim review')]},
        {'index':2,'verdict':'inconclusive','finding':'Alternatives and adoption/integration/porting deferrals are explicit. Essential source gaps are retained without an absence claim or completion waiver.',
         'evidence':[ref(BASE/'omissions-register.json','Exact gaps and actions'),ref(BASE/'author-review.md','Full criterion review'),binding]}]
    write(BASE/(OP+'.receipt.json'),receipt)
    print(json.dumps({'published':state['reader'],'receipt':str((BASE/(OP+'.receipt.json')).relative_to(ROOT))}))


if __name__ == '__main__':
    main()
