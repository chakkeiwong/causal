#!/usr/bin/env python3
"""Create scoped fect publication successors; do not mutate canonical state."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
T=ROOT/'tools'


def save(name,text):
    p=T/name
    assert not p.exists(),p
    compile(text,str(p),'exec')
    p.write_text(text)


s=(T/'build_scpi_reuse_reader_20261024.py').read_text().replace('scpi','fect')
s=s.replace('augsynth-reuse','scpi-reuse').replace('augsynth_reuse','scpi_reuse')
s=s.replace('1129','1131').replace('prediction, failure and bound contracts','panel targets, clocks and inference contracts')
s=s.replace('authenticated fect implementation','authenticated fect source')
save('build_fect_reuse_reader_20261024.py',s)

s=(T/'publish_scpi_reuse_reader_20261024.py').read_text().replace('scpi','fect')
s=s.replace('1131','1133').replace('1129','1131')
s=s.replace('A synthetic banking portfolio needs more than a fitted counterfactual curve.',
            'A banking servicing policy may start, stop and restart across regional')
s=s.replace("['4,200 USD','77.5','85','20, 24 and 30 USD']", "['4,800 USD','109/101','501','20, 24 and 30 USD']")
s=s.replace('fect target,constraint,uncertainty,failed-tail and bound reference choice',
            'fect targets,clocks,validation,numerical,inference and reference choice')
s=s.replace('Eight authenticated fect mirror files and exact preparation/solver witnesses',
            'Twelve authenticated fect archive originals and exact authored witnesses')
s=s.replace('Prediction uncertainty,failed solves,asymmetric bounds,numerical status',
            'Targets,validation clocks,numerical exits,bootstrap failures and sensitivity')
s=s.replace('fect prediction,solver,failure and bound contracts',
            'fect panel targets,clocks,validation and inference contracts')
a=s.index('    findings=dict(Q2=');z=s.index(chr(10),a)
s=s[:a]+"    findings=dict(Q2='Preserves1131 predecessor source records and contexts;adds2 fect records;1133total and253scholarly PDFs.',Q3='Twelve archive originals and exact target,clock,selection,shrinkage,interval,iteration and cost witnesses;no native run.',Q4='Proposed worker preserves requested/resolved options,targets,clocks,masks,denominators,numerical exits,all failures,rights and costs;no capability admission.')"+s[z:]
save('publish_fect_reuse_reader_20261024.py',s)

s=(T/'build_scpi_reuse_sponsor_20261024.py').read_text().replace('scpi','fect')
s=s.replace('sponsor-augsynth-reuse','sponsor-scpi-reuse')
a=s.index('def manuscript(pages):');z=s.index('def prepare():',a)
body=s[z:].replace('639','643').replace('635','639').replace('1131','1133').replace('reuse70/3/42','reuse71/3/41')
manuscript='''def manuscript(pages):
    text=(PRIOR/'proposal.md').read_text()
    text=text.replace('1,469 pages',f'{pages:,} pages').replace('1131 audited citation records','1133 audited citation records')
    text=text.replace('sp24scpi_reader,sp24scpi_progress','sp24scpi_reader,sp24scpi_progress,sp24fect_reader,sp24fect_progress')
    old='Current software coverage is three passing, 53 inconclusive and 46 open cells; reuse is 70 passing, three inconclusive and 42 open. Census has 80 inspected and 33 unread originals, plus four crosscutting obligations. The program has 265 recorded outcomes of 376, including inconclusive results.'
    assert text.count(old)==1
    text=text.replace(old,old.replace('70 passing','71 passing').replace('42 open','41 open').replace('265 recorded','266 recorded'))
    marker='# Public evidence before expensive bank experiments';assert text.count(marker)==1
    return text.replace(marker,(READER_BASE/'sponsor-addition.md').read_text()+chr(10)*2+marker)

'''
s=s[:a]+manuscript+body
s=s.replace('fect prediction-inference','fect panel-inference')
save('build_fect_reuse_sponsor_20261024.py',s)

s=(T/'publish_scpi_reuse_sponsor_20261024.py').read_text().replace('scpi','fect')
s=s.replace('639','643').replace('635','639').replace('1131','1133')
s=s.replace('70 passing','71 passing').replace('42 open','41 open').replace('265 recorded','266 recorded')
s=s.replace("['pass']==70","['pass']==71").replace("['open']==42","['open']==41")
s=s.replace('Prediction intervals need complete failure accounting','Switching policies require a qualified panel contract')
s=s.replace('4,200 USD','4,800 USD').replace('fect prediction-inference','fect panel-inference')
save('publish_fect_reuse_sponsor_20261024.py',s)

s=(T/'refresh_scpi_reuse_program_20261024.py').read_text().replace('scpi','fect')
s=s.replace('program-refresh-augsynth-reuse','program-refresh-scpi-reuse')
s=s.replace('1131','1133').replace('1129','1131').replace('639','643').replace('265','266').replace('189','188')
s=s.replace("groups['reuse']['pass']==70","groups['reuse']['pass']==71").replace("groups['reuse']['open']==42","groups['reuse']['open']==41")
s=s.replace('reuse70pass/3inconclusive/42open','reuse71pass/3inconclusive/41open')
s=s.replace('42 open and three inconclusive','41 open and three inconclusive')
a=s.index('## Newly reconciled work');z=s.index('## Remaining gaps and routes',a)
s=s[:a]+'''## Newly reconciled work

The successor integrates the separate fect 2.4.5 reference decision.
Twelve selected originals authenticate byte-for-byte to the preserved
30 May 2026 CRAN-mirror archive. Identity is not complete distribution
rights, an installed environment or scientific/native qualification.

The chapter develops panel targets, treatment switches and carryover,
validation clocks and denominators, normalized matrix shrinkage, iteration
termination, bootstrap failures and optional sensitivity delegation.
Exact authored examples and base-R language checks reproduce. Downloaded
package code was not executed. Conditional static findings remain bounded.

All 1,131 predecessor records, citation contexts and content inputs survive;
two new records bring the total to 1,133. The paired sponsor preserves all
639 prior citations and adds four. Source, arithmetic and text/bounds
checks do not establish visual, independent or final acceptance.

'''+s[z:]
save('refresh_fect_reuse_program_20261024.py',s)
print('Prepared fect reader, sponsor and whole-program reconciliation tools.')
