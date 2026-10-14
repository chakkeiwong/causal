#!/usr/bin/env python3
"""Recheck the estimation/validation synthesis and prepare a reviewed receipt."""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

import run_program as control
import master_control as core

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-14/estimation-validation'
SYN = ROOT/'docs/program/comprehensive-v14/work/LL.TASK.estimation_validation/task-synthesis.md'
AUDIT = ROOT/'docs/program/repair-v12/work/LA01/source-audit.json'
CENSUS = ROOT/'docs/program/execution/2026-10-13/llm-census/source-audit.json'
OMISSIONS = ROOT/'docs/program/repair-v12/work/LA01/omissions.json'
SEARCH = ROOT/'docs/program/execution/2026-10-13/llm-census/search-ledger.json'


def ref(path, anchor):
    path=Path(path)
    return {'path':str(path.relative_to(ROOT)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'anchor':anchor}


def write(path, obj):
    assert not path.exists(), f'Preserve existing evidence: {path}'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')


def exact_oracle():
    masses=[F(1,2),F(3,10),F(1,5)]
    propensities=[F(1,20),F(1,2),F(19,20)]
    effects=[F(0),F(4),F(12)]
    full=sum((p*t for p,t in zip(masses,effects)),F(0))
    trimmed=sum((p*t for p,e,t in zip(masses,propensities,effects) if F(1,10)<=e<=F(9,10)),F(0))/sum((p for p,e in zip(masses,propensities) if F(1,10)<=e<=F(9,10)),F(0))
    weights=[p*e*(1-e) for p,e in zip(masses,propensities)]
    overlap=sum((w*t for w,t in zip(weights,effects)),F(0))/sum(weights,F(0))
    assert (full,trimmed,overlap)==(F(18,5),F(4),F(1656,433))
    uncapped=[sum(x)/2 for x in ([1,100],[9,9])]
    capped=[sum(min(x,10) for x in row)/2 for row in ([1,100],[9,9])]
    assert uncapped==[50.5,9] and capped==[5.5,9]
    return {'type':'exact_project_fixture_not_package_or_bank_execution','strata_masses':list(map(str,masses)),
            'propensities':list(map(str,propensities)),'conditional_effects':list(map(str,effects)),
            'full_ATE':str(full),'trimmed_rule':'0.1 <= e(X) <= 0.9','trimmed_ATE':str(trimmed),
            'overlap_weights':list(map(str,weights)),'overlap_ATE':str(overlap),
            'normalized_interval_score_example':{'raw_pairs':[[1,100],[9,9]],'uncapped_means':uncapped,
                'cap':10,'capped_means':capped,'ranking_reverses':True},
            'selection_example':{'all_requests':8,'accepted':6,'covered_accepted':6,
                'selected_coverage':'1','all_request_return_and_cover':'3/4'},
            'limitations':['Scores are an exact abstract comparison, not empirical confidence intervals.',
                           'Selected coverage does not establish conditional coverage.',
                           'The propensity and effect law is stipulated, not observed.']}


def main():
    assert SYN.exists() and '1656}{433}' in SYN.read_text()
    audit=json.loads(AUDIT.read_text()); census=json.loads(CENSUS.read_text())
    sources={x['id']:x for x in audit['sources']}
    papers=[]
    for key, anchors in [
      ('v12_la_2607_22443',['PDF pp. 3-5: AIPW, trimming, author-reported ACIC and LaLonde results']),
      ('v12_la_2607_08093',['PDF pp. 3, 10, 14: identification, noisy observations, exam and discussion']),
      ('v12_la_2407_19118',['PDF pp. 2, 4, 9: causal roadmap, eligibility and limitations']),
      ('v12_la_2609_30867',['PDF pp. 2, 6, 9: evidence audit, retrieval gate, human pilot'])]:
        x=sources[key]; p=ROOT/x['local_path']
        assert p.read_bytes().startswith(b'%PDF-')
        assert ref(p,'Original PDF')['sha256']==x['sha256']
        assert p.name.endswith(f" {x['first_author']}({x['year']}).pdf")
        papers.append({'id':key,'identity':x['url'],'version_date':x['arxiv_version']+'; '+x['published'],
            'original':ref(p,'; '.join(anchors)),'inspected_anchors':anchors,
            'supported_claims':x['claims'],'local_audit':ref(AUDIT,key)})
    packages=[]
    for key in ['v12_la_package_oci_agent','v12_la_package_causalds']:
        x=sources[key]; local=[]
        for row in x['local_sources']:
            p=ROOT/row['path']; assert ref(p,'Original source snapshot')['sha256']==row['sha256']
            local.append(ref(p,row.get('anchor','Pinned source bytes')))
        packages.append({'id':key,'identity':x['url'],'commit':x['commit'],'commit_date':x['commit_date'],
            'originals':local,'inspected_anchors':x['anchors'],'supported_claims':x['claims'],
            'limitations':x['adverse_findings_and_limits'],'executed':False})
    crows={x['integrated_citation_key']:x for x in census['sources']}
    resolved=[]
    for key,old in [('exec13_census_orca','LA01-candidate-241'),('exec13_census_texts','LA01-candidate-175')]:
        x=crows[key]; resolved.append({'old_candidate':old,'later_source_key':key,'source_identity':x.get('source_identity'),
            'later_audit':ref(CENSUS,key),'resolution':'Original PDF inspected in later census; older omission remains historical.'})
    omissions=json.loads(OMISSIONS.read_text())
    wanted={'LA01-candidate-31','LA01-candidate-256','LA01-candidate-266','LA01-candidate-269'}
    pending=[{'id':x['id'],'title':x['title'],'status':x['status'],'next_action':x['next_action']}
             for x in omissions['items'] if x.get('id') in wanted]
    assert {x['id'] for x in pending}==wanted
    search=json.loads(SEARCH.read_text())
    assert any('ten' in x.get('limit','').lower() for x in search['searches'])
    write(BASE/'primary-review.json',{'cutoff':'2026-10-07','acquired':'2026-10-12/13; later acquisition explicitly labeled',
        'papers':papers,'packages':packages,'source_audits':[ref(AUDIT,'Inspected four original papers and two pinned packages'),
               ref(CENSUS,'Later inspected ORCA and text original PDFs')],
        'correction':'The inspected CausalDS scorer computes BOTH uncapped and capped interval means; earlier abbreviated narrative must not say only capped.',
        'scorer_original':ref(ROOT/'docs/literature/raw/v12_la_causalds_source_2.txt','lines 152-174 missing ID defaults; 1507-1568 interval; 3529-3546 both score means'),
        'oci_notebook':ref(ROOT/'docs/literature/raw/v12_la_oci_notebook.json','Code cells 42-43: trim_by_propensity then aipw_summary(Y_DR[keep]) serialized as ATO')})
    write(BASE/'candidate-reassessment.json',{'resolved_later':resolved,'still_uninspected':pending,
        'omissions':ref(OMISSIONS,'Original inherited candidate dispositions'),
        'search':ref(SEARCH,'Bounded Crossref/OpenAlex routes, ten ranked results and coverage limits'),
        'other_limits':['No full package dependency/license/runtime closure.',
                        'No package executed, no head-to-head agent trial, no bank validation.',
                        'No exhaustive frontier saturation or absence claim.']})
    write(BASE/'exact-oracle.json',exact_oracle())
    evidence=[ref(SYN,'Reviewed target, frontier evidence, remedies, worked example and limitations'),
      ref(BASE/'primary-review.json','Original PDFs and pinned source identities, anchors, supported claims'),
      ref(BASE/'candidate-reassessment.json','Resolved versus still-uninspected candidates and bounded searches'),
      ref(BASE/'exact-oracle.json','Independent exact arithmetic and failure metrics')]
    review={'outcome':'pass','scope':'Research synthesis and exact project fixture only',
            'criteria':[{'index':0,'verdict':'pass','finding':'Four primary papers and two pinned packages compared; favorable and adverse evidence, remedies, historical omissions and open research explicit.'},
                        {'index':1,'verdict':'pass','finding':'Account-level offer target, clock, identification premises, target-change failure, three-stratum exact effects and interval-score reversal explained.'},
                        {'index':2,'verdict':'pass','finding':'Author-reported results and source inspection separated from exact project derivations; no live-model or bank causal-performance claim.'}],
            'limitations':['Not an exhaustive current-source survey or executable package validation.',
                           'Not independent scientific review or bank-data truth.'],
            'evidence':evidence,'reviewer':{'name':'Codex author/coordinator','kind':'author'}}
    write(BASE/'author-review.json',review)
    graph,_,_=control.combined(ROOT,core.read(ROOT,core.STATE)); node=control.ledger.operation(graph,'LL.TASK.estimation_validation')
    receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope=review['scope'],reviewer=review['reviewer'],
                   limitations=review['limitations'],capabilities=[],outputs=[evidence[0]])
    for i,row in enumerate(review['criteria']):
        receipt['criteria'][i].update(verdict=row['verdict'],finding=row['finding'],evidence=evidence)
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'status':'reviewed','paper_pdf_hashes':len(papers),'package_source_sets':len(packages),
                      'resolved_historical_candidates':len(resolved),'pending_candidates':len(pending),
                      'exact_full_ATE':'18/5','exact_trimmed_ATE':'4','exact_overlap_ATE':'1656/433'}))

if __name__=='__main__': main()
