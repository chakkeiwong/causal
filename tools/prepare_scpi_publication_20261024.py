#!/usr/bin/env python3
"""Prepare scoped preserving publication tools; does not mutate canonical state."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
T=ROOT/'tools'
def save(name,text):
 p=T/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text)

s=(T/'build_augsynth_reuse_reader_20261024.py').read_text().replace('augsynth','scpi')
s=s.replace("PREDECESSOR=DOCS/'program/execution/2026-10-24/synth-reuse-reader-v1'","PREDECESSOR=DOCS/'program/execution/2026-10-24/augsynth-reuse-reader-v1'")
s=s.replace("OLD=DOCS/'causal_proposal_synth_reuse_reviewed_2026-10-24.tex'","OLD=DOCS/'causal_proposal_augsynth_reuse_reviewed_2026-10-24.tex'")
s=s.replace('2026-10-24/synth-reuse-reader-v1/development.tex','2026-10-24/augsynth-reuse-reader-v1/development.tex').replace('1127','1129')
s=s.replace('preparation, normalization and solver contracts','prediction, failure and bound contracts')
save('build_scpi_reuse_reader_20261024.py',s)

s=(T/'publish_augsynth_reuse_reader_20261024.py').read_text().replace('augsynth','scpi')
s=s.replace('1129','1131').replace('1127','1129')
s=s.replace('A banking intervention may affect a regional portfolio outside the convex','A synthetic banking portfolio needs more than a fitted counterfactual curve.')
s=s.replace("['3,600 USD','1/4','130','20, 24 and 30 USD']","['4,200 USD','77.5','85','20, 24 and 30 USD']")
s=s.replace('Thirteen authenticated scpi files','Eight authenticated scpi mirror files')
s=s.replace('scpi dispatch,negative weights,tuning,inference and reference choice','scpi target,constraint,uncertainty,failed-tail and bound reference choice')
s=s.replace('Augmented-control dispatch,negative weights,tuning,inference and reference choice','scpi prediction,solver,failure and bound contracts')
s=s.replace('Extrapolation,tuning,inference,numerical status','Prediction uncertainty,failed solves,asymmetric bounds,numerical status')
a=s.index('    findings=dict(Q2=');z=s.index(chr(10),a)
s=s[:a]+"    findings=dict(Q2='Preserves1129 predecessor source records and citation contexts;adds2 scpi records;1131total and253scholarly PDFs.',Q3='Eight mirror originals bound with release limits;exact interval,failed-tail,flag,matrix and cost witnesses reproduce;no package execution.',Q4='Proposed interface preserves targets,requested/resolved inputs,numerical statuses,full failure denominators,uncertainty scopes,refusals,rights and costs;no native capability.')"+s[z:]
save('publish_scpi_reuse_reader_20261024.py',s)

s=(T/'build_augsynth_reuse_sponsor_20261024.py').read_text().replace('augsynth','scpi')
s=s.replace("PRIOR=DOCS/'program/execution/2026-10-24/sponsor-synth-reuse-v1'","PRIOR=DOCS/'program/execution/2026-10-24/sponsor-augsynth-reuse-v1'")
a=s.index('def manuscript(pages):');z=s.index('def prepare():',a)
body=s[z:].replace('635','639').replace('631','635').replace('1129','1131').replace('reuse69/3/43','reuse70/3/42')
manuscript='''def manuscript(pages):
    text=(PRIOR/'proposal.md').read_text()
    text=text.replace('1,466 pages',f'{pages:,} pages').replace('1129 audited citation records','1131 audited citation records')
    text=text.replace('sp24augsynth_reader,sp24augsynth_progress','sp24augsynth_reader,sp24augsynth_progress,sp24scpi_reader,sp24scpi_progress')
    old='Current software coverage is three passing, 53 inconclusive and 46 open cells; reuse is 69 passing, three inconclusive and 43 open. Census has 80 inspected and 33 unread originals, plus four crosscutting obligations. The program has 264 recorded outcomes of 376, including inconclusive results.'
    assert text.count(old)==1
    text=text.replace(old,old.replace('69 passing','70 passing').replace('43 open','42 open').replace('264 recorded','265 recorded'))
    marker='# Public evidence before expensive bank experiments';assert text.count(marker)==1
    return text.replace(marker,(READER_BASE/'sponsor-addition.md').read_text()+chr(10)*2+marker)

'''
s=s[:a]+manuscript+body
s=s.replace('augmented-control','scpi prediction-inference')
save('build_scpi_reuse_sponsor_20261024.py',s)

s=(T/'publish_augsynth_reuse_sponsor_20261024.py').read_text().replace('augsynth','scpi')
s=s.replace('635','639').replace('631','635').replace('1129','1131').replace('69 passing','70 passing').replace('43 open','42 open').replace('264 recorded','265 recorded')
s=s.replace("['pass']==69","['pass']==70").replace("['open']==43","['open']==42")
s=s.replace('Augmentation needs an extrapolation contract','Prediction intervals need complete failure accounting').replace('3,600 USD','4,200 USD').replace('Augmented-control','scpi prediction-inference')
save('publish_scpi_reuse_sponsor_20261024.py',s)

s=(T/'refresh_augsynth_reuse_program_20261024.py').read_text().replace('augsynth','scpi')
s=s.replace("PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-synth-reuse-v1'","PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-augsynth-reuse-v1'")
s=s.replace('1129','1131').replace('1127','1129').replace('635','639').replace('264','265').replace('190','189')
s=s.replace("groups['reuse']['pass']==69","groups['reuse']['pass']==70").replace("groups['reuse']['open']==43","groups['reuse']['open']==42")
s=s.replace('reuse69pass/3inconclusive/43open','reuse70pass/3inconclusive/42open').replace('43 open and three inconclusive','42 open and three inconclusive')
a=s.index('## Newly reconciled work');z=s.index('## Remaining gaps and routes',a)
s=s[:a]+'''## Newly reconciled work

The successor integrates the scpi 4.0.1 R reference decision. Eight originals
authenticate to the 10 June 2026 CRAN-mirror pin. The observed packager field
and future-dated bibliography remain explicit provenance limits; no author
release equality, paper theorem or native qualification is inferred.

The chapter distinguishes targets,weight constraints,coefficient/future-error
components,joint-coverage scopes,failed simulated solves,asymmetric supplied
bounds and degenerate matrices. Exact interval,tail,Boolean,matrix and financial
examples reproduce. Downloaded package code was not executed.

All 1,129 predecessor source records,contexts and compiled inputs survive;
two new records bring the total to 1,131. The paired sponsor preserves all635
previous citation records and adds four. Source/arithmetic/text checks do not
establish fresh visual,independent or final acceptance.

'''+s[z:]
save('refresh_scpi_reuse_program_20261024.py',s)
print('Five publication tools and one complete reconciliation tool prepared.')
