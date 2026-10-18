#!/usr/bin/env python3
"""Preserving publication of inspected graph-wrapper and panel-target findings."""
import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess

import audit_reader_traceability_v2_20261013 as trace
import build_integrated_monograph_v12 as shared
import graph_panel_reference_20261018 as exact
import review_gap_reader_v13 as layout
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-18/graph-panel-reader-v1'
OUT = BASE/'reader'
PREDECESSOR = DOCS/'program/execution/2026-10-18/census-frameworks-v1'
OLD = DOCS/'causal_proposal_framework_evaluation_reviewed_2026-10-18.tex'
PRIOR = PREDECESSOR/'reader/source-audit.json'
GRAPH = BASE/'graph-development.tex'
PANEL = BASE/'panel-development.tex'
EVIDENCE = DOCS/'program/execution/2026-10-18'
NAME = 'causal_proposal_graph_panels_reviewed_2026-10-18'
DRIVER = DOCS/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
LABELS = ['exec18:gp-graph', 'exec18:gp-graph-laws', 'exec18:gp-confounding',
          'exec18:gp-collider', 'exec18:gp-panel', 'exec18:gp-cohort-target',
          'exec18:gp-panel-example', 'exec18:gp-fwl', 'exec18:gp-negative-weight']


def read(path):
    return json.loads(path.read_text())


def expected_driver():
    text = OLD.read_text()
    for marker, addition in [
        (r'\input{program/execution/2026-10-18/r-identification/development.tex}', GRAPH),
        (r'\input{program/execution/2026-10-17/s4/depth-extension/development.tex}', PANEL)]:
        assert text.count(marker) == 1, marker
        text = text.replace(marker, marker+'\n'+r'\input{'+str(addition.relative_to(DOCS))+'}')
    assert len(re.findall(r'\\bibliography\{([^}]+)\}', text)) == 1
    return re.sub(r'\\bibliography\{([^}]+)\}', lambda m:
        r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}', text)


def source_records():
    original = EVIDENCE/'dagitty-reuse/source-audit.json'
    dag = copy.deepcopy(read(original))
    dag.update(integrated_citation_key='exec18_gp_dagitty',
        author='jtextor/dagitty contributors', year=2024,
        original_audit=ref(original, 'Unchanged original fourteen-blob inspection'),
        inspected_anchors=[r['local_copy'] for r in dag['records']],
        bibliography_note='Commit 7a657776dc8f5e5ba4e323edb028e2c2aaf29327, 6 December 2024; R0.3-4 dated 7 December 2023; static inspection, no upstream execution',
        publication_note='The original audit describes its then-unintegrated snapshot. This successor integrates its bounded claims, without runtime or rights admission.')
    assert len(dag['records']) == 14
    sources = [dag]
    keys = ['stata_did', 'stata_hdid', 'stata_xthdid', 'stata_post', 'eviews']
    manuals = read(EVIDENCE/'commercial-panels/source-audit.json')['sources']
    assert len(manuals) == len(keys)
    for key, raw in zip(keys, manuals):
        source = copy.deepcopy(raw)
        eviews = key == 'eviews'
        source.update(integrated_citation_key='exec18_gp_'+key,
            author='EViews' if eviews else 'StataCorp', year=2025 if eviews else 2026,
            original_audit=ref(EVIDENCE/'commercial-panels/source-audit.json', 'Preserved five-original inspection'),
            bibliography_note=('Displayed update 12 March 2025' if eviews else
                'Public manual snapshot with July/August 2026 creation metadata')+
                '; acquired 18 October 2026; exact cutoff bytes and edition entitlements unverified')
        sources.append(source)
    for short, title, script, saved, claims in [
        ('graph_reference', 'Exact graphical adjustment and conditioning references',
         ROOT/'tools/review_dagitty_reuse_20261018.py', EVIDENCE/'dagitty-reuse/exact-reference.json',
         ['Confounding adjustment gives 1/4 versus naive 5/16.',
          'Collider conditioning gives -7/96 despite zero effect; mediator standardization gives 1/8 versus total 1/4.']),
        ('panel_reference', 'Exact staggered branch-rollout and negative-weight reference',
         ROOT/'tools/review_commercial_panels_20261018.py', EVIDENCE/'commercial-panels/exact-reference.json',
         ['The specified fifteen rows have ATT34 and TWFE -91/8 thousand USD, with weights 5/8,-1/8,1/2.',
          'A differential postperiod shock is compatible with exact preperiod equality.',
          'Stipulated cost10000USD yields average net24000USD; -21375USD illustrates invalid projection-as-ATT accounting.'])]:
        sources.append(dict(integrated_citation_key='exec18_gp_'+short,
            title=title, author='Causal banking proposal project', year=2026,
            kind='project_derivation', source_identity='Project-authored finite structural laws and exact rational arithmetic',
            version_date='18 October 2026', local_copy=ref(script, 'Pure exact reference function; main is not rerun'),
            inspected_anchors=[ref(saved, 'Saved exact reference'),
                ref(BASE/'exact-results.json', 'Separate structural calculation and normal-equation check')],
            independent_reference=ref(ROOT/'tools/graph_panel_reference_20261018.py', 'Independent calculation'),
            supported_claims=claims,
            limitations=['Stipulated mathematical examples; no sampling coverage, vendor runtime, live upstream or bank evidence.']))
    probe = EVIDENCE/'commercial-panels/local-probe.json'
    sources.append(dict(integrated_citation_key='exec18_gp_dispatch',
        title='Bounded dependent-panel request to the local causal dispatcher',
        author='Causal banking proposal project', year=2026, kind='project_implementation_probe',
        source_identity='Local dispatcher request and saved response', version_date='18 October 2026',
        local_copy=ref(probe, 'Actual completed/unsupported response with null result'),
        inspected_anchors=['panel_DID_request and schema_source'],
        implementation=read(probe)['schema_source'],
        supported_claims=['The selected dependent-panel DID request is unsupported at this common interface.'],
        limitations=['No absence claim about other panel research code; no new adapter or vendor engine execution.']))
    assert len(sources) == 9
    return sources


def prepare():
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    originals = [EVIDENCE/'dagitty-reuse/source-audit.json',
        EVIDENCE/'dagitty-reuse/review.json', EVIDENCE/'dagitty-reuse/operation-receipt.json',
        EVIDENCE/'commercial-panels/source-audit.json', EVIDENCE/'commercial-panels/author-review.json',
        EVIDENCE/'commercial-panels/operation-receipt.json']
    for path in [PRIOR]+originals:
        verify_bindings(read(path))
    write(BASE/'manuscript-plan-review.json', dict(status='pass', reviewer='Author/coordinator',
        evidence=[ref(BASE/'plan.md', 'Reviewed six-step preserving plan'),
                  ref(GRAPH, 'Connected wrapper/causal-law development'),
                  ref(PANEL, 'Connected panel-target development')]+[ref(p, 'Inspected original evidence') for p in originals],
        findings=['Publication has no dependence on unresolved commercial families or a qualified native runtime.',
            'Primary byte identities, versions, anchors and supported claims are retained; cutoff-era bytes and editions remain unverified.',
            'All763 predecessor records,201 scholarly PDFs, unchanged compiled inputs and citation context multisets must survive.',
            'Capped search, invalid requests, no adjustment and general nonidentification remain distinct.',
            'Panel ATT, scalar projection, aggregate weights, cost units and uncertainty are checked separately.',
            'Source/math/text author review can finish now; visual and final acceptance remain open.',
            'Sponsor pairing and whole-register refresh follow publication without a permission checkpoint.'],
        repairs=['Clarified that positive cells refer to (A,U,C), because Y=U is deterministic.',
            'Added direct collider and mediation calculations and inverse-Gram weights, separate from saved enumerations.'],
        visual_acceptance=False, final_acceptance=False))
    results = exact.calculate()
    write(BASE/'exact-results.json', results)
    audit = dict(sources=source_records(), cutoff='2026-10-07',
                 scope='Nine bounded graph, commercial-panel and project-reference records')
    verify_bindings(audit)
    write(BASE/'source-audit.json', audit)
    write(BASE/'mathematical-review.json', dict(status='pass',
        evidence=[ref(ROOT/'tools/graph_panel_reference_20261018.py', 'Exact independent calculation'),
                  ref(BASE/'exact-results.json', 'Reproduced saved results and independent checks'),
                  ref(GRAPH, 'Graphical structural laws'), ref(PANEL, 'Cohort target and finite projection')],
        findings=['Rational normal equations and inverse-Gram weights reproduce the saved FWL coefficient and effect weights.',
            'Direct structural calculations reproduce confounding, collider and mediation contrasts.',
            'Thirty-four thousand USD minus ten thousand equals24000USD; invalid projection accounting equals-21375USD.',
            'Equal preperiod paths cannot prove postperiod counterfactual trends.',
            'No empirical confidence coverage, prospective policy value or bank ROI follows.']))
    write(BASE/'copyedit-review.json', dict(status='pass', rendered_review=False,
        evidence=[ref(GRAPH, 'Reviewed argument and notation'), ref(PANEL, 'Reviewed argument and units')],
        findings=['Graph and panel examples are explicitly hypothetical and distinct.',
            'The selected wrapper route is proposed; actual local interface refusal is identified.',
            'Vendor option restrictions, incomplete sources and rights/runtime limits are stated.',
            'Process records remain outside the product narrative.']))
    bib = []
    for s in audit['sources']:
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+
            '}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])+
            '},\n note={'+shared.escape(s.get('bibliography_note', s['source_identity']+'; '+s['version_date']))+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    paths = [OLD, PRIOR, GRAPH, PANEL, BASE/'plan.md', BASE/'source-audit.json',
        BASE/'manuscript-plan-review.json', BASE/'mathematical-review.json',
        BASE/'copyedit-review.json', BASE/'exact-results.json',
        ROOT/'tools/graph_panel_reference_20261018.py', Path(__file__)]
    write(BASE/'prepared-inputs.json', dict(inputs=[ref(p, 'Preserving reviewed input') for p in paths],
        generated=[ref(DRIVER, 'Preserving graph-panel driver'), ref(BASE/'refs.bib', 'Nine-record bibliography')],
        expected_cited_records=772, expected_scholarly_pdfs=201, visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), records=772, exact_reference=results['status'])))


def build():
    verify_bindings(read(BASE/'prepared-inputs.json'))
    assert DRIVER.read_text() == expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    assert not OUT.exists() and not PDF.exists()
    OUT.mkdir()
    env = dict(os.environ)
    env['TEXINPUTS'] = str(DOCS)+'//:'+env.get('TEXINPUTS', '')
    env['BIBINPUTS'] = str(DOCS)+'//:'+env.get('BIBINPUTS', '')
    command = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
               '-output-directory='+str(OUT), str(DRIVER)]
    def execute(args, name):
        with (OUT/name).open('x') as stream:
            result = subprocess.run(args, cwd=DOCS, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=120)
        assert result.returncode == 0, 'Failure preserved in '+str(OUT/name)
    execute(command, 'pass-1.log')
    execute(['bibtex', str((OUT/NAME).relative_to(DOCS))], 'bibtex-pass.log')
    for turn in range(2, 6):
        execute(command, f'pass-{turn}.log')
        log = (OUT/(NAME+'.log')).read_text(errors='replace')
        if turn >= 3 and not any(t in log for t in ['Label(s) may have changed', 'Rerun to get']):
            break
    for token in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character', 'Overfull']:
        assert token not in log, token
    files = shared.scan(DRIVER)
    joined = '\n'.join(t for _, t in files)
    labels = re.findall(shared.LABEL, joined)
    assert len(labels) == len(set(labels))
    cited = {k.strip() for g in re.findall(shared.CITE, joined) for k in g.split(',')}
    entries = {}
    for path in [PRIOR, BASE/'source-audit.json']:
        audit = read(path)
        verify_bindings(audit)
        for s in audit['sources']:
            k = s['integrated_citation_key']
            assert k not in entries or entries[k] == s
            entries[k] = s
    assert cited <= entries.keys(), cited-entries.keys()
    assert len(cited) == 772
    PDF.write_bytes((OUT/(NAME+'.pdf')).read_bytes())
    write(OUT/'source-audit.json', dict(sources=[entries[k] for k in sorted(cited)],
        tex_files=[ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
        source_audits=[ref(p, 'Preserved audited input') for p in [PRIOR, BASE/'source-audit.json']],
        cutoff='2026-10-07', visual_acceptance=False))
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT/'reader.txt')], check=True, timeout=30)
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    aux = (OUT/(NAME+'.aux')).read_text()
    anchors = {}
    for label in LABELS:
        m = re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^}]+)\}\{(\d+)\}', aux)
        assert m, label
        anchors[label] = dict(number=m.group(1), printed_page=int(m.group(2)))
    report = dict(status='compiled_source_and_text_checked_working_draft', pages=pages,
        pdf=ref(PDF, 'Preserving graph and commercial-panel successor'),
        driver=ref(DRIVER, 'Preserving driver'), builder=ref(Path(__file__), 'Exact preserving builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Immutable1068-page framework reader'),
        source_audit=ref(OUT/'source-audit.json', '772 audited citation records'),
        cited_records=len(cited), added_anchors=anchors,
        warnings=[line for line in log.splitlines() if any(t in line for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])],
        final_acceptance=False, mandatory_repairs_closed=[], visual_acceptance=False,
        visual_review='Pending fresh session; inherited image allowance exhausted')
    write(OUT/'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    assert read(OUT/'text-layout-review.json')['status'] == 'pass'
    index = trace.audit(DRIVER, OUT/'source-audit.json')
    write(BASE/'traceability-review.json', index)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 201
    print(json.dumps(dict(pages=pages, records=772, scholarly_pdfs=201,
        anchors=anchors, warnings=report['warnings'], visual_acceptance=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
