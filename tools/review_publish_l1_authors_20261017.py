#!/usr/bin/env python3
"""Review and publish six evidence-backed L1 author-field corrections."""
import argparse
import json
from pathlib import Path
import re
import build_l1_authors_reader_20261017 as build
import master_control as core
import review_s3_20261017 as preservation
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write
ROOT,WORK,BASE,OUT=build.ROOT,build.WORK,build.BASE,build.OUT
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=[
 'Six inspected scholarly author fields are presentation repairs; source records and scientific claims are unchanged.',
 'Original census remains37 inspected/76 unread of113, with three separate inspected citation-chain leads.',
 'L1 exclusive depth and complete coverage remain governed by the separate chapter review, not this publication.',
 'No new source acquisition, upstream execution, independent review or bank validation is claimed.',
 'Q1/Q5, all mandatory manuscript repairs and final acceptance remain open.',
 'Rendered visual acceptance remains false under the exhausted inherited image allowance.']
NEXT='Record the actual L1 chapter-review outcome; continue L2/I2/I4 independently, then original source census and sponsor reconciliation; commit and push recovery.'


def read(path):
 return json.loads(path.read_text())


def verify():
 for path in [BASE/'prepared-inputs.json',BASE/'author-review.json',BASE/'mathematical-replay.json',
              OUT/'build-report.json',OUT/'source-audit.json',BASE/'traceability-review.json']:
  verify_bindings(read(path))
 report=read(OUT/'build-report.json');audit=read(OUT/'source-audit.json')
 index=read(BASE/'traceability-review.json');bounds=read(OUT/'text-layout-review.json')
 assert report['cited_records']==745 and index['scholarly_pdfs']==196
 assert index['status']=='pass' and not index['issues']
 assert bounds['status']=='pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
 assert not [w for w in report['warnings'] if 'Underfull' not in w]
 assert build.DRIVER.read_text()==build.expected_driver()
 kept=preservation.preserve(audit,index,build.PREDECESSOR,745,[str(build.OLD.relative_to(ROOT))])
 old={s['integrated_citation_key']:s for s in read(build.PRIOR)['sources']}
 assert old=={s['integrated_citation_key']:s for s in audit['sources']}
 for oldpath,new in build.BIBS.items():
  expected,_=build.corrected_bibliography(oldpath)
  assert (BASE/(new+'.bib')).read_text()==expected
 bbl=(OUT/(build.NAME+'.bbl')).read_text()
 entries={key:label for label,key in re.findall(r'\\bibitem\[(.*?)\]\{([^{}]+)\}',bbl,re.S)}
 expected={'exec13_census_causaleval':'Yu et~al.', 'exec13_census_graph_validation':'Susanti and Holsmoelle',
  'exec13_census_collaboration':'Zhang et~al.', 'exec17_frontier_chang':'Chang',
  'exec17_frontier_yang':'Yang et~al.', 'exec17_frontier_liu':'Liu et~al.'}
 for key,prefix in expected.items():
  label=' '.join(entries[key].split());assert label.startswith(prefix+'('),(key,label)
 aux=(OUT/(build.NAME+'.aux')).read_text();equations={}
 labels=['exec13:frontier-'+x for x in ['claim','mixture','rank','chain','frechet','oracle','regret','minimax']]+['exec17:frontier-'+x for x in ['transition','multiclass','scm','observed']]
 for label in labels:
  m=re.search(re.escape('\\newlabel{'+label+'}{{')+r'([^}]+)',aux)
  assert m and re.fullmatch(r'40\.\d+',m.group(1)),label
  equations[label]=m.group(1)
 pages=(OUT/'reader.txt').read_text().split(chr(12))
 physical_start=next(i for i,t in enumerate(pages,1) if 'What language models contribute to' in t and 'Chapter 40' in t)
 start=report['added_section_printed_pages']['la:frontier']
 end=report['added_section_printed_pages']['exec17:frontier-end']
 offset=physical_start-start
 text=' '.join(' '.join(pages[physical_start-1:end+offset]).split())
 for term in ['Yu et al. (2025','Susanti and Holsmoelle','Zhang et al. (2024','Chang, 2026','Yang et al., 2026','Liu et al., 2026']:
  assert term in text,term
 for term in ['Longxuan Yu, Delin Chen','Jinseok Yang and Jung-Hee','Haochen Liu and Ke Shi']:
  assert term not in text,term
 assert all('('+n+')' in text for n in equations.values())
 return report,dict(preserved_records=745,unchanged_compiled_tex_files=kept,
  corrected_scholarly_author_fields=6,source_records_unchanged=True,
  citation_context_multisets_preserved=True,chapter_printed_pages=[start,end],
  chapter_physical_pages=[physical_start,end+offset],equations=equations,
  visual_acceptance=False,exclusive_depth_credit=None)


def review():
 report,checks=verify()
 evidence=[ref(p,'Reviewed preserving author repair') for p in [BASE/'prepared-inputs.json',
  BASE/'plan.md',BASE/'plan-review.json',BASE/'author-review.json',BASE/'mathematical-replay.json',
  BASE/'traceability-review.json',OUT/'build-report.json',OUT/'source-audit.json',
  OUT/'reader.txt',OUT/'text-layout-review.json',Path(__file__)]]
 write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope='Six scholarly author fields and preserving exact-reader author review',
  reviewer=REVIEWER,reviewed_reader=report['pdf'],checks=checks,evidence=evidence,
  findings=['All745 records, manuscript inputs and citation-context multisets survive unchanged.',
   'Six title-page-verified author lists serialize as individual people; shortened citations replace corporate-name output.',
   'Twelve L1 equations and both exact-reference families reproduce; source traceability and all-page text bounds pass.',
   'Chapter depth and whole-corpus coverage are separate decisions; visual review remains pending.'],
  limitations=LIMITS,final_acceptance=False,visual_acceptance=False))
 write(BASE/'chapter-yield.json',dict(finding='Preserving author-field successor reviewed; L1 coverage/depth decision remains explicit.',
  next_action=NEXT,yield_reason='Publish reviewed successor and renew exact-reader Q2-Q4 before recording chapter outcome.',
  evidence=evidence+[ref(BASE/'release-source-review.json','Reviewed successor')]))
 print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


def publish():
    report, _ = verify()
    review = read(BASE/'release-source-review.json')
    verify_bindings(review)
    assert review['status'] == 'pass' and review['issues'] == []
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    audit = read(OUT/'source-audit.json')
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving L1 author repair reader'),
        source_review=ref(BASE/'release-source-review.json', 'Bounded source and mathematical review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=audit['tex_files']+review['evidence']+[
            ref(WORK/'author-review.json', 'Six inspected title-page author lists')],
        changes=['Repair six scholarly author fields in preserving bibliography copies; all scientific sources and manuscript claims remain unchanged.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed L1 author repair working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_l1_author_repair_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    run.ledger.validate_working_release(ROOT, ref(BASE/'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All745 audited records,196 scholarly PDFs and citation-context multisets survive. Six author lists verified against genuine title pages now serialize correctly. No source identity or claim is changed.',
        'Q3': 'Twelve L1 equation numbers and both exact-reference families agree; bibliography name parsing, extracted pages, source traceability and all-page text bounds pass. Exclusive chapter depth and visual acceptance remain separate.',
        'Q4': 'Scientific and economic inputs are unchanged from the prior exact-reader review. All illustrative monetary results remain stipulated project examples; no actual bank value or prices are inferred.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.'+q
        state = core.read(ROOT, core.STATE)
        assert run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][identifier]
        old = read(ROOT/previous['path'])
        if run.same_reader(old.get('reviewed_reader', {}), report['pdf']):
            assert old['outcome'] == 'pass'
            continue
        folder = BASE/q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE/'working-release.json', 'Exact current reader'),
            ref(BASE/'release-source-review.json', 'Preserving source/math delta'),
            ref(WORK/'author-review.json', 'Title-page author-list verification'),
            ref(WORK/'mathematical-replay.json', 'Preserved exact examples reproduce'), ref(Path(__file__), 'Exact-reader review findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded L1 author repair source, mathematical and economic delta.'))
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, dict(operation=identifier, status='pass', criterion=node['criteria'][0],
            reviewer=REVIEWER, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', scope=scope, findings=[finding], evidence=evidence,
            limitations=limits, visual_acceptance=False))
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Exact-reader '+q+' author review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[dict(index=0, verdict='pass', finding=finding, evidence=evidence)])
        write(folder/'operation-receipt.json', receipt)
        transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    {'review': review, 'publish': publish, 'renew': renew}[parser.parse_args().command]()
