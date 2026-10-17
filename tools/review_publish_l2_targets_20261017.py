#!/usr/bin/env python3
"""Review and publish six evidence-backed L1 author-field corrections."""
import argparse
import json
from pathlib import Path
import re
import build_l2_targets_v2_reader_20261017 as build
import l2_monetary_reference_20261017 as monetary
import l2_policy_reference_20261017 as policy
from collections import Counter
import build_integrated_monograph_v12 as shared
import master_control as core
import review_s3_20261017 as preservation
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write
ROOT,WORK,BASE,OUT=build.ROOT,build.WORK,build.BASE,build.OUT
REVIEWER=dict(name='Codex author/coordinator',kind='author')
CANONICAL=ROOT/'docs/program/execution/2026-10-17/l1-review-v1'
CANONICAL_DRIVER=ROOT/'docs/causal_proposal_frontier_authors_reviewed_2026-10-17.tex'
LIMITS=[
 'Author source, mathematical and extracted-page review; no independent or visual acceptance.',
 'Exact monetary, policy, credit and measurement constructions are stipulated, not observed bank or provider results.',
 'Original census remains37 inspected/76 unread of113, plus separate citation-chain leads.',
 'Chapter coverage/depth has its own actual outcome; physical pages do not establish acceptance.',
 'Q1/Q5, mandatory repairs and whole-proposal acceptance remain open.',
 'Visual acceptance remains false under the exhausted inherited image allowance.']
NEXT='Record the actual L2 review, then review I2/I4 independently and continue original census and software coverage; commit and push durable work.'


def read(path):
 return json.loads(path.read_text())


def filtered_contexts(index, excluded):
 return {r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts'] if x['path'] not in excluded) for r in index['records']}


def verify():
 for base in [WORK,BASE]:
  for name in ['prepared-inputs.json','author-review.json','mathematical-review.json','source-audit.json','exact-results.json','plan-review.json']:
   verify_bindings(read(base/name))
 for path in [OUT/'build-report.json',OUT/'source-audit.json',BASE/'traceability-review.json',BASE/'inherited-math-review.json']:
  verify_bindings(read(path))
 report=read(OUT/'build-report.json');audit=read(OUT/'source-audit.json');index=read(BASE/'traceability-review.json')
 assert report['cited_records']==747 and index['scholarly_pdfs']==196
 assert index['status']=='pass' and not index['issues']
 bounds=read(OUT/'text-layout-review.json');assert bounds['status']=='pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
 assert not [w for w in report['warnings'] if 'Underfull' not in w]
 assert build.DRIVER.read_text()==build.expected_driver()
 assert monetary.serial(monetary.calculate())==read(WORK/'exact-results.json')
 assert policy.serial(policy.calculate())==read(BASE/'exact-results.json')
 previous=read(CANONICAL/'reader/source-audit.json');old={x['integrated_citation_key']:x for x in previous['sources']};new={x['integrated_citation_key']:x for x in audit['sources']}
 assert len(old)==745 and all(new[k]==v for k,v in old.items())
 replaced={'docs/program/comprehensive-v14/work/TEXT.DRAFT.L2/chapter-layout-v4.tex',str(CANONICAL_DRIVER.relative_to(ROOT))}
 files={r['path']:r for r in audit['tex_files']};kept=[r for r in previous['tex_files'] if r['path'] not in replaced]
 assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
 current=filtered_contexts(index,set());prior=filtered_contexts(read(CANONICAL/'traceability-review.json'),replaced)
 assert all(not c-current[k] for k,c in prior.items())
 for path in [BASE/'chapter-corrected.tex',BASE/'monetary.tex',WORK/'policy.tex']:
  tex=path.read_text();expected={}
  for match in re.finditer(shared.CITE,tex):
   for k in match.group(1).split(','):
    expected.setdefault(k.strip(),[]).append(dict(path=str(path.relative_to(ROOT)),line=tex.count('\n',0,match.start())+1,context=tex[max(0,match.start()-550):match.end()+220]))
  actual={r['citation_key']:[c for c in r['citation_contexts'] if c['path']==str(path.relative_to(ROOT))] for r in index['records']}
  assert {k:v for k,v in actual.items() if v}==expected
 # No old citation disappears from the corrected L2 source.
 old_tex=(ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L2/chapter-layout-v4.tex').read_text()
 assert Counter(re.findall(shared.CITE,old_tex))==Counter(re.findall(shared.CITE,(BASE/'chapter-corrected.tex').read_text()))
 for oldpath,newname in build.BIBS.items():
  expected,_=build.corrected_bibliography(oldpath);assert (BASE/(newname+'.bib')).read_text()==expected
 bbl=(OUT/(build.NAME+'.bbl')).read_text();entries={key:' '.join(label.split()) for label,key in re.findall(r'\\bibitem\[(.*?)\]\{([^{}]+)\}',bbl,re.S)}
 for key,prefix in {'exec13_census_texts':'Egami et~al.','exec13_census_text_review_arxiv':"Keith et~al.",'exec13_census_credible':'Geraldo~Bastías','exec13_hallucination':'Sng et~al.','exec13_pulse':'Shyalika et~al.','exec13_ci_brodersen2015':'Brodersen et~al.'}.items():
  label=entries[key]
  if key=='exec13_census_credible':assert 'Geraldo' in label and 'Bast' in label,label
  else:assert label.startswith(prefix+'('),(key,label)
 aux=(OUT/(build.NAME+'.aux')).read_text();equations={}
 for suffix in ['stock','cost','value','decomposition','numeric','marginal','joint','error','selection','sequential-reward','sequential-value','credit-value','credit-switchers']:
  label='exec17:l2-'+suffix;m=re.search(re.escape('\\newlabel{'+label+'}{{')+r'([^}]+)',aux)
  assert m and re.fullmatch(r'42\.\d+',m.group(1)),label
  equations[label]=m.group(1)
 start=report['added_section_printed_pages']['la:translation'];end=report['added_section_printed_pages']['exec17:l2-policy-end']
 pages=(OUT/'reader.txt').read_text().split(chr(12));text=' '.join(' '.join(pages[start+21:end+22]).split())
 assert all('('+n+')' in text for n in equations.values())
 assert 'C(1) − C(0)' in text and 'balance-time' in text
 assert '1571/30000' in text and '−21/200' in text
 return report,dict(preserved_records=745,new_project_records=2,unchanged_compiled_inputs=len(kept),unrelated_citation_contexts_preserved=True,changed_contexts_recomputed=True,corrected_author_fields=6,exact_families=7,equations=equations,chapter_printed_pages=[start,end],chapter_physical_pages=[start+22,end+22],visual_acceptance=False)


def review():
 report,checks=verify()
 evidence=[ref(p,'Reviewed L2 source, mathematical and preservation evidence') for p in [WORK/'plan-review.json',WORK/'author-review.json',WORK/'mathematical-review.json',WORK/'depth-review-initial.json',BASE/'plan-review.json',BASE/'author-review.json',BASE/'mathematical-review.json',BASE/'inherited-math-review.json',BASE/'prepared-inputs.json',BASE/'traceability-review.json',OUT/'build-report.json',OUT/'source-audit.json',OUT/'reader.txt',OUT/'text-layout-review.json',Path(__file__)]]
 write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope='Preserving L2 monetary, measurement and policy target development',reviewer=REVIEWER,reviewed_reader=report['pdf'],checks=checks,evidence=evidence,findings=['Canonical745 sources and unrelated manuscript/citation contexts are preserved; two exact project references added.','Dimensional mismatch, comparator costs, funding sign and question-tuple inconsistency repaired.','Six scholarly author lists are verified against genuine original title pages.','Seven new exact families and inherited target/measurement calculations reproduce;13 new equations present.','Exclusive depth and coverage remain subject to chapter review; visual acceptance remains false.'],limitations=LIMITS,final_acceptance=False,visual_acceptance=False))
 write(BASE/'chapter-yield.json',dict(finding='Preserving L2 target successor passes source/math and extracted-page checks.',next_action=NEXT,yield_reason='Publish reviewed working successor and renew exact-reader Q2-Q4 before recording actual chapter review.',evidence=evidence+[ref(BASE/'release-source-review.json','Reviewed working successor')]))
 print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


def publish():
    report, _ = verify()
    review = read(BASE/'release-source-review.json')
    verify_bindings(review)
    assert review['status'] == 'pass' and review['issues'] == []
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(CANONICAL_DRIVER.with_suffix('.pdf').relative_to(ROOT))
    audit = read(OUT/'source-audit.json')
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving L2 target repair reader'),
        source_review=ref(BASE/'release-source-review.json', 'Bounded source and mathematical review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=audit['tex_files']+review['evidence']+[
            ref(WORK/'author-review.json', 'Five inspected title-page author lists'),ref(BASE/'author-review.json','Brodersen title-page author list')],
        changes=['Repair L2 dimensions, comparator costs, funding sign, declaration consistency and six scholarly author fields; develop exact funding, measurement, servicing and threshold examples.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed L2 target repair working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_l2_target_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    run.ledger.validate_working_release(ROOT, ref(BASE/'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All745 canonical records and196 scholarly PDFs survive; two auditable exact project records added. Six scholarly author fields match original title pages; unchanged citation contexts preserved and changed contexts recomputed.',
        'Q3': 'Thirteen new L2 equations and seven exact families reproduce; inherited target and measurement outputs agree. Dimension, comparator and sign repairs verified; all-page text bounds pass. Visual acceptance is separate.',
        'Q4': 'Monetary outcomes explicitly value balance-time, price existing-balance repricing, compare incremental costs and minimize funding cost. Exact examples and conditional break-even rates reproduce; no actual bank rates, ROI or acceptance inferred.'}
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
            ref(WORK/'mathematical-review.json', 'Exact monetary and measurement constructions'),ref(BASE/'mathematical-review.json','Exact policy and threshold constructions'),ref(BASE/'inherited-math-review.json','Inherited examples reproduce'), ref(Path(__file__), 'Exact-reader review findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded L2 target repair source, mathematical and economic delta.'))
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
