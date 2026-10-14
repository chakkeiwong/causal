#!/usr/bin/env python3
"""Integrate reviewed native, reuse and evaluation work in a preserving reader."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

import build_integrated_monograph_v12 as shared
import master_control as core
import review_gap_reader_v13 as layout
import review_causalml_reuse_20261014 as causalml
import review_cxx_latent_20261014 as native
import review_evaluation_cost_20261014 as evaluation

ROOT = core.ROOT
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-14/native-evaluation-reader/v3'
OUT = BASE/'reader'
OLD = DOCS/'causal_proposal_discovery_review_v3_2026-10-14.tex'
NAME = 'causal_proposal_native_evaluation_v3_2026-10-14'
DRIVER = DOCS/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = DOCS/'program/execution/2026-10-14/l4-completion/v3/reader/source-audit.json'
ref = shared.ref


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(data, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')


def guard():
    assert not any(d['path'] == str(PDF.relative_to(ROOT))
                   for d in core.read(ROOT, core.STATE)['deliveries']), 'Delivered reader is immutable'


def source(key, title, author, kind, identity, version, path, anchor, claims, records):
    return {'integrated_citation_key': key, 'title': title, 'author': author,
            'kind': kind, 'year': 2026, 'source_identity': identity,
            'version_date': version, 'local_copy': ref(path, anchor),
            'inspected_anchors': [anchor], 'supported_claims': claims, 'records': records,
            'limitations': ['Only the stated static-source or exact project scope; no upstream execution or bank acceptance.']}


def prepare():
    guard()
    assert not DRIVER.exists() and not (BASE/'prepared-inputs.json').exists()
    BASE.mkdir(parents=True, exist_ok=True)
    native_text = (native.BASE/'comparison.tex').read_text()
    native_text = native_text.replace(
        r'$\{\text{circle},\text{tail},\text{arrowhead}\}^2$',
        'the three endpoint marks taken in pairs')
    (BASE/'native-comparison.tex').write_text(native_text)
    assert native.exact() == json.loads((native.BASE/'exact-oracle.json').read_text())
    assert causalml.exact_examples() == json.loads((causalml.BASE/'oracle-results.json').read_text())
    assert evaluation.calculate() == json.loads((evaluation.BASE/'exact-oracle.json').read_text())
    n = json.loads((native.BASE/'primary-review.json').read_text())
    c = json.loads((causalml.BASE/'primary-review.json').read_text())
    e = json.loads((evaluation.BASE/'primary-review.json').read_text())
    for x in [n, c, e]:
        shared.verify_refs(x)
    sources = []
    for key, pkg in zip(['agrum', 'miic', 'rcmgm'], n['packages']):
        sources.append(source('exec14_native_'+key,
            pkg['repository']+' pinned latent-discovery and endpoint source review', pkg['repository'],
            'software_primary_sources', 'https://github.com/'+pkg['repository'],
            pkg['revision']+'; '+pkg['source_date']+'; inspected 2026-10-14',
            native.BASE/'primary-review.json', 'Package '+pkg['repository']+'; all recorded source anchors',
            [claim for r in pkg['records'] for claim in r['supported_claims']], pkg['records']))
    sources += [source('exec14_native_oracle', 'Exact native graph-conversion and hidden-risk references',
        'Causal banking proposal', 'project_derivation', 'Project-authored finite laws', '2026-10-14',
        native.BASE/'exact-oracle.json', 'Nine local endpoint pairs; four conversion classes; equal observed laws',
        ['Endpoint information loss', 'Effects 0/20 USD and net values -8/12 under two stipulated observationally equivalent worlds'],
        [{'local_copy': ref(ROOT/'tools/review_cxx_latent_20261014.py', 'Exact Fraction and endpoint enumeration')}]),
        source('exec14_causalml_primary', 'CausalML binary T-learner, R-learner and uncertainty source review',
        'uber/causalml', 'software_primary_sources', 'https://github.com/uber/causalml',
        c['revision']+'; 2026-10-05; declared 0.17.0; inspected 2026-10-14',
        causalml.BASE/'primary-review.json', 'Nine selected blobs, target/variance/row-bootstrap and dependencies',
        [claim for r in c['sources'] for claim in r['supported_claims']], c['sources']),
        source('exec14_causalml_oracle', 'Exact population-weight, policy and rare-arm bootstrap references',
        'Causal banking proposal', 'project_derivation', 'Project-authored stratified offer law', '2026-10-14',
        causalml.BASE/'oracle-results.json', 'ATE10 ATT13 ATC7 raw25; deterministic R-loss; empty-arm bootstrap',
        ['Target and policy arithmetic only; no learned-policy inference or bank ROI'],
        [{'local_copy': ref(ROOT/'tools/review_causalml_reuse_20261014.py', 'Exact rational calculations')}]),
        source('exec14_evaluation_code', 'CLadder and CausalDS benchmark reuse contracts',
        'causalNLP/cladder; andleb/causalds', 'software_primary_sources',
        'https://github.com/causalNLP/cladder ; https://github.com/andleb/causalds',
        'CLadder 3d2d1169 (2024-05-29); CausalDS c74671d0 (2026-07-17); inspected 2026-10-14',
        evaluation.BASE/'primary-review.json', 'Packages: label, target, identification metadata and capped/uncapped score limits',
        ['Source-inspected prospective reuse, without execution or complete dependency/rights closure'],
        [{'source_identity': p['source_identity'], 'version_date': p['commit_date']+'; '+p['commit'],
          'originals': p['originals'], 'inspected_anchors': p['inspected_anchors']} for p in e['packages']]),
        source('exec14_evaluation_oracle', 'Exact request accounting, assistance costs and prospective precision',
        'Causal banking proposal', 'project_derivation', 'Project-authored illustrative assumptions', '2026-10-14',
        evaluation.BASE/'exact-oracle.json', 'Conditional availability/coverage; error-sensitive break-even; bounded-mean planning',
        ['Illustrative variable cost31 versus18.50 USD;1000 versus5000 break-even under declared assumptions',
         'Mechanism rather than request independence;2952 sufficient bounded-mean units at stated tolerance'],
        [{'local_copy': ref(ROOT/'tools/review_evaluation_cost_20261014.py', 'Exact arithmetic and planning calculation')}])]
    synopsis = evaluation.SYN.read_text()
    # Keep the immutable task synthesis; use a copy without internal process identifiers.
    synopsis = synopsis.split('## Coverage limits and the next research decisions')[0]
    synopsis = synopsis.replace('The preserved LA06 protocol is a reviewed prospective design',
                                'The proposed evaluation protocol is a reviewed prospective design')
    synopsis = synopsis.replace('All seven genuine PDFs, inspected anchors and exact versions are bound in the accompanying primary review. Their results remain author-reported literature evidence.',
                                'The reported results remain literature evidence from distinct tasks, populations and model settings.')
    insertions = {
        'Jin et al.\'s *CLadder*': r'*CLadder* by Jin et al.\citep{v12_la_2312_04350}',
        'Yu et al.\'s *CausalEval*': r'*CausalEval* by Yu et al.\citep{exec13_census_causaleval}',
        'Leban and Sun\'s *CausalDS*': r'*CausalDS* by Leban and Sun\citep{v12_la_2607_08093}',
        'Feng et al.\'s *On the Reliability': r'The study by Feng et al.\citep{v12_la_2407_19638}, *On the Reliability',
        'Zhang et al.\'s *CausalChat*': r'*CausalChat* by Zhang et al.\citep{v12_la_2410_14146}',
        'Le et al.\'s *Multi-Agent': r'The study by Le et al.\citep{v12_la_2407_15073}, *Multi-Agent',
        'Murphy et al.\'s *Model Discovery': r'The study by Murphy et al.\citep{v12_la_2608_09696}, *Model Discovery'}
    for old, new in insertions.items():
        assert synopsis.count(old) == 1, old
        synopsis = synopsis.replace(old, new)
    synopsis = synopsis.replace('Neither upstream package has been executed for this synthesis.',
        r'Neither upstream package has been executed for this synthesis.\citep{exec14_evaluation_code}')
    synopsis = synopsis.replace('None of these stipulated counts estimates actual model performance.',
        r'None of these stipulated counts estimates actual model performance.\citep{exec14_evaluation_oracle}')
    synopsis = synopsis.replace('These sensitivities explain why an inexpensive-looking model call is not a business case.',
        r'These sensitivities explain why an inexpensive-looking model call is not a business case.\citep{exec14_evaluation_oracle}')
    synopsis = synopsis.replace('This calculation does not choose a final sample size or justify normal inference in every stratum.',
        r'This calculation does not choose a final sample size or justify normal inference in every stratum.\citep{exec14_evaluation_oracle}')
    # Partition the synthesis at a genuine change of question, within existing chapters.
    before, after = synopsis.split('## Full cost and the investment threshold', 1)
    before = before.replace('# Evaluating causal assistance and its full cost',
        '# What published evaluations establish and how to reuse them\n\n\\label{exec14:evaluation-development}')
    after = '# Full cost and the investment threshold\n\n\\label{exec14:cost-development}\n'+after
    after += '\nThe immediate investment is a narrow prototype using public data and stipulated mechanisms. Its purpose is to resolve target errors, unsupported assumptions, tool failures and review burden before an expensive bank experiment. Hidden evaluation, actual prices, bank-specific loss and institutional review remain later inputs; the proposal does not invent their outcomes.\n\n\\label{exec14:cost-development-end}\n'
    before = before.replace('`3d2d1169b4b939a09048a6a75956c8972a93cc38`', '`3d2d1169b4b9`').replace('`c74671d0a0924efc5bb021fc8966f856d5b80a4f`', '`c74671d0a092`')
    before = before.replace('=87.5\\%,\\qquad', '=87.5\\%,\\\\\n').replace('=90\\%,\\qquad', '=90\\%,\\\\\n')
    before = before.replace('A_{\\mathrm{id}}=70/80', '\\begin{gathered}\n A_{\\mathrm{id}}=70/80').replace('=78.75\\%.', '=78.75\\%.\n\\end{gathered}')
    display = '\\[\n \\begin{gathered}'
    ending = '\\end{gathered}\n\\]'
    assert before.count(display) == 1 and before.count(ending) == 1
    before = before.replace(display, '```{=latex}\n' + display).replace(ending, ending + '\n```')
    before = before.replace('\\\\\n\n C_', '\\\\\n C_')
    for name, text in [('evaluation-development', before), ('cost-development', after)]:
        (BASE/(name+'.md')).write_text(text)
        subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash',
            '--to=latex', '--wrap=auto', str(BASE/(name+'.md')), '-o', str(BASE/(name+'.tex'))],
            check=True, timeout=20)
    write(BASE/'source-audit.json', {'cutoff': '2026-10-07', 'sources': sources,
        'prior': ref(PRIOR_AUDIT, '506 preserved citation records'),
        'primary_rereads': ref(evaluation.BASE/'primary-review.json', 'Seven authentic primary PDFs and exact inspected anchors'),
        'coverage_limits': ref(native.BASE/'omissions-register.json', 'Open native coverage/method questions'),
        'evaluation_omissions': ref(evaluation.BASE/'candidate-reassessment.json', 'Resolved CausalEval identity and five remaining uninspected leads')})
    bib = []
    for s in sources:
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+
            '}},\n title={'+shared.escape(s['title'])+'},\n year={2026},\n note={'+shared.escape(s['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    book = OLD.read_text().replace('13 October 2026\\\\Proposal working edition', '14 October 2026\\\\Proposal working edition')
    paths = [('program/execution/2026-10-13/cxx-discovery/comparison.tex', BASE/'native-comparison.tex'),
             ('program/execution/2026-10-14/reader-repair/causallearn-decision.tex', causalml.BASE/'decision.tex'),
             ('program/execution/2026-10-13/live-evaluation/evaluation.tex', BASE/'evaluation-development.tex'),
             ('program/repair-v12/work/LA07/economics-chapter.tex', BASE/'cost-development.tex')]
    for previous, addition in paths:
        marker = r'\input{'+previous+'}'
        assert book.count(marker) == 1
        book = book.replace(marker, marker+'\n'+r'\input{'+str(addition.relative_to(DOCS))+'}')
    marker = r'\chapter*{Reader\'s contract}'
    marker = "\\addcontentsline{toc}{chapter}{Reader's contract}"
    introduction = ("\n\nSections~\\ref{exec14:cxx-latent} and~\\ref{exec14:causalml} extend the native discovery and heterogeneous-offer software comparison. "
        "Sections~\\ref{exec14:evaluation-development} and~\\ref{exec14:cost-development} connect primary evaluations to explicit error, availability and full-cost decisions. "
        "These additions comprise inspected software, literature and reproducible illustrative calculations; the external engines and proposed model study have not been executed.\n")
    assert book.count(marker) == 1
    book = book.replace(marker, marker+introduction)
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    book = pattern.sub(lambda m: r'\bibliography{'+m.group(1)+',program/execution/2026-10-14/native-evaluation-reader/v3/refs}', book)
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json', {'inputs': [ref(p, 'Reviewed preserving input') for p in
        [OLD, PRIOR_AUDIT, evaluation.SYN, native.BASE/'primary-review.json', causalml.BASE/'primary-review.json',
         evaluation.BASE/'primary-review.json', Path(__file__)]],
        'generated': [ref(p, 'Successor source') for p in [DRIVER, BASE/'source-audit.json', BASE/'refs.bib',
        BASE/'evaluation-development.tex', BASE/'cost-development.tex', BASE/'native-comparison.tex', causalml.BASE/'decision.tex']],
        'credit_policy': 'No automatic chapter-depth or whole-repair credit; repeated exposition requires deduction in Q1.',
        'visual_acceptance': False})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'added_citation_records': len(sources),
                      'three_exact_references': 'pass', 'previous_reader_preserved': True}))


def build():
    guard()
    shared.verify_refs(json.loads((BASE/'prepared-inputs.json').read_text()))
    shared.scan(DRIVER)
    OUT.mkdir(exist_ok=True)
    env = dict(os.environ)
    env['TEXINPUTS'] = str(DOCS)+'//:'+env.get('TEXINPUTS', '')
    env['BIBINPUTS'] = str(DOCS)+'//:'+env.get('BIBINPUTS', '')
    command = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
               '-output-directory='+str(OUT), str(DRIVER)]
    def execute(args, name):
        with (OUT/name).open('w') as stream:
            p = subprocess.run(args, cwd=DOCS, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=55)
        if p.returncode:
            raise ValueError('Build failed; inspect '+str(OUT/name))
    execute(command, 'pass-1.log')
    execute(['bibtex', str((OUT/NAME).relative_to(DOCS))], 'bibtex-pass.log')
    for i in range(2, 6):
        execute(command, f'pass-{i}.log')
        log = (OUT/(NAME+'.log')).read_text(errors='replace')
        if i >= 3 and not any(t in log for t in ['Label(s) may have changed', 'Rerun to get']):
            break
    for token in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character']:
        assert token not in log, token
    files = shared.scan(DRIVER)
    joined = '\n'.join(t for _, t in files)
    labels = re.findall(shared.LABEL, joined)
    assert len(labels) == len(set(labels)), 'Duplicate labels'
    cited = {k.strip() for group in re.findall(shared.CITE, joined) for k in group.split(',')}
    entries = {}
    for path in [PRIOR_AUDIT, BASE/'source-audit.json']:
        audit = json.loads(path.read_text())
        shared.verify_refs(audit)
        for s in audit['sources']:
            key = s['integrated_citation_key']
            assert key not in entries or entries[key] == s
            entries[key] = s
    assert cited <= entries.keys(), cited-entries.keys()
    PDF.write_bytes((OUT/(NAME+'.pdf')).read_bytes())
    audit = {'sources': [entries[k] for k in sorted(cited)],
        'tex_files': [ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
        'source_audits': [ref(p, 'Preserved audited inputs') for p in [PRIOR_AUDIT, BASE/'source-audit.json']],
        'cutoff': '2026-10-07', 'visual_acceptance': False}
    core.write(OUT/'source-audit.json', audit)
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT/'reader.txt')], check=True, timeout=30)
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    aux = (OUT/(NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    report = {'status': 'compiled_source_and_text_checked_working_draft', 'pages': pages,
        'pdf': ref(PDF, 'Native software and evaluation working successor'),
        'driver': ref(DRIVER, 'Preserving driver'), 'builder': ref(Path(__file__), 'Bounded source/audit builder'),
        'predecessor_pdf': ref(OLD.with_suffix('.pdf'), 'Frozen683-page working reader'),
        'source_audit': ref(OUT/'source-audit.json', 'Whole-reader source identities'),
        'cited_records': len(cited),
        'added_sections': {name: page('exec14:'+name) for name in ['cxx-latent', 'cxx-latent-end',
            'causalml', 'causalml-end', 'evaluation-development', 'cost-development', 'cost-development-end']},
        'warnings': [line for line in log.splitlines() if any(t in line for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])],
        'final_acceptance': False, 'mandatory_repairs_closed': [], 'visual_acceptance': False,
        'visual_review': 'Pending fresh session under exhausted inherited image allowance'}
    core.write(OUT/'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    assert json.loads((OUT/'text-layout-review.json').read_text())['status'] == 'pass'
    print(json.dumps({k: report[k] for k in ['pages', 'cited_records', 'added_sections', 'warnings']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
