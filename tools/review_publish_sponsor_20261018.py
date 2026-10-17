#!/usr/bin/env python3
"""Preserve the sponsor predecessor and register a scoped working successor."""
import json
from pathlib import Path
import build_sponsor_20261018 as build
import sponsor_economics_20261013 as economics
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=extension.base;core=run.core;ROOT=core.ROOT;BASE=build.BASE

def main():
 read=lambda p:json.loads(p.read_text())
 report=read(BASE/'build-report.json');audit=read(BASE/'source-audit.json')
 for obj in [report,audit,read(BASE/'plan-review.json'),read(BASE/'progress-evidence.json')]:verify_bindings(obj)
 assert report['pages']==10 and report['cited_records']==26 and not report['text_bounds_issues'] and not report['empty_pages']
 assert all('Underfull' in x for x in report['warnings'])
 assert read(BASE/'economics-results.json')==economics.calculate()
 old=ROOT/'docs/program/execution/2026-10-13/sponsor';s=(BASE/'proposal.md').read_text();o=(old/'proposal.md').read_text()
 for a,b in [('# Economics and the next experiment','# What remains before a complete proposal'),('## Funding and observations','## Discovery and agent support')]:assert s[s.index(a):s.index(b)]==o[o.index(a):o.index(b)]
 prior=read(old/'source-audit.json');new={x['integrated_citation_key']:x for x in audit['sources']};kept=[x for x in prior['sources'] if x['integrated_citation_key'] in new]
 assert len(kept)==18 and all(new[x['integrated_citation_key']]==x for x in kept)
 text=' '.join((BASE/'reader.txt').read_text().split())
 for token in ['1,060 pages','751 audited','197 genuine','40 inspected','73 unread','six actual','four fresh','five malformed','USD 5,200','USD 36,000','100–150','L1 and L6']:
  assert token.lower() in text.lower(),token
 state=core.read(ROOT,core.STATE);assert run.same_reader(state['reader'],report['paired_monograph'])
 evidence=[ref(BASE/n,'Inspected sponsor evidence') for n in ['plan-review.json','source-audit.json','build-report.json','economics-results.json','proposal.md','reader.txt','progress-evidence.json']]+[ref(Path(__file__),'Exact coherence checks')]
 findings=[
  'Recommendation retains the four journeys and a public/generated prototype before costly bank experiments.',
  'The exact1060-page monograph has751 audited citation records and197 genuine scholarly PDFs; sponsor is bound to those bytes.',
  'All18 retained predecessor source records are identical; funding/servicing discussion and complete economic section are unchanged.',
  'Thesis results are mixed and source-reported; response consistency does not verify a truth likelihood. No upstream runtime claimed.',
  'Six library/CLI calls, four response replays and five rejected replies remain separate; finite retention orders are not observed failure probabilities.',
  'Current source,software,reuse and L1/L6 gaps remain explicit; no independent,bank,product or final proposal acceptance.']
 limitations=['Author content,source,exact arithmetic and extracted-page review only.','Rendered visual acceptance remains false under inherited image allowance.','Full RELEASE.RECONCILE and Q1/Q5 remain open; this is a working sponsor update.']
 write(BASE/'author-review.json',dict(status='pass',issues=[],reviewer=dict(name='Codex author/coordinator',kind='author'),scope='Exact-reader sponsor consistency and evidence review',paired_monograph=report['paired_monograph'],sponsor=report['reader_copy'],findings=findings,evidence=evidence,limitations=limitations,visual_acceptance=False,final_acceptance=False))
 manifest=dict(kind='working_sponsor',pdf=report['reader_copy'],pages=report['pages'],paired_monograph=report['paired_monograph'],predecessor=ref(ROOT/'docs/sponsor_proposal_2026-10-13.pdf','Preserved October13 sponsor'),predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],build=ref(BASE/'build-report.json','Compiled10-page successor'),review=ref(BASE/'author-review.json','Scoped author review'),evidence=evidence,final_acceptance=False,visual_acceptance=False)
 write(BASE/'working-release.json',manifest);verify_bindings(manifest)
 before=core.sha(ROOT/core.STATE);delivery={k:report['reader_copy'][k] for k in ['path','sha256']};delivery.update(pages=10,status='Working sponsor; exact-reader content review, visual/final acceptance open',kind='working_sponsor',paired_monograph=report['paired_monograph'],release=ref(BASE/'working-release.json','Versioned sponsor evidence'))
 assert not any(x['path']==delivery['path'] for x in state['deliveries'])
 state['deliveries'].append(delivery)
 run.commit(ROOT,before,state,dict(action='publish_working_sponsor',release=delivery['release'],prior_operation_preserved=True,final_acceptance=False))
 print(json.dumps(dict(published=delivery['path'],pages=10,cited_records=26,paired_monograph=state['reader']['path'],review='pass',visual_acceptance=False,final_acceptance=False)))

if __name__=='__main__':main()
