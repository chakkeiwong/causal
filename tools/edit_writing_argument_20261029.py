"""Explicit, ledgered edits to the protected scientific-progress successor."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];D=R/'docs';O=D/'writing-repair/2026-10-29';P='writing-repair/2026-10-29/'
M=json.loads((O/'source-map.json').read_text());E=json.loads((O/'edits.json').read_text())
def path(suffix):
 hits=[v for k,v in M.items() if k.endswith(suffix)]
 assert len(hits)==1,(suffix,hits)
 return R/hits[0]
def edit(p,old,new,why,destination):
 s=p.read_text();assert s.count(old)==1,(str(p),old[:120],s.count(old));p.write_text(s.replace(old,new,1))
 E.append(dict(file=str(p.relative_to(R)),before=old,after=new,reason=why,substantive_destination=destination))
def between(p,start,end,new,why,dest):
 s=p.read_text();a=s.index(start);z=s.index(end,a);edit(p,s[a:z],new,why,dest)
def demote(p,newtitle):
 s=p.read_text();m=re.search(r'\\chapter\{([^}]+)\}',s);assert m
 replacement=r'\section{'+newtitle+'}'
 # Demote existing subdivisions as a group, preserving labels and content.
 s2=re.sub(r'\\(chapter|section|subsection)\{',lambda m:'\\'+{'chapter':'section','section':'subsection','subsection':'subsubsection'}[m[1]]+'{',s)
 s2=s2.replace(r'\section{'+m[1]+'}',replacement,1)
 edit(p,s,s2,'Unify the treatment under one question; retain every distinct argument and label.','Same file, subordinate treatment in unified chapter')
def inp(p):return r'\input{'+str(p.relative_to(D))+'}'
def write_new(name,text):
 p=O/name;p.write_text(text);return p
# Split the three distinct syntheses so their authoritative treatments can be assembled once.
p=path('/decision-synthesis.tex');s=p.read_text();parts=re.split(r'(?=\\chapter\{)',s);parts=[x for x in parts if x.strip()];assert len(parts)==3
ass=write_new('assistance.tex',parts[1]);inv=write_new('investment.tex',parts[2])
edit(p,s,parts[0],'Separate evidence, assistance and investment for subject-based assembly.','Evidence remains here; assistance.tex and investment.tex contain the other two chapters verbatim before further ledgered edits.')
# Software: keep developed comparisons, a single selection, distinct panel illustration.
sw=path('/software-decisions.tex')
edit(sw,'The numerical study later in this supplement examines\nthe decision consequence of an omitted effect modifier.','The generated study in Chapter~\\ref{scisyn:evidence} examines\nthe decision consequence of an omitted effect modifier.','Replace obsolete edition-relative navigation.','Same supported claim; current cross-reference.')
replacements=[
('Retain the partially directed or ancestral graph, its assumptions and the\nresulting range of intervention conclusions. Integrate a latent-variable route\nonly with a separately specified interpretation of its endpoints. Reject the\nproposed practice of selecting one convenient orientation and reporting its\neffect as identified.','The partially directed or ancestral graph determines a range of intervention\nconclusions under its stated assumptions. A latent-variable route also needs\nan explicit interpretation of its endpoints. Selecting one convenient\norientation would instead report an unidentified effect as identified.'),
('Integrate symbolic identification as an explicit stage before estimation, with\nan intelligible statement of what cannot be identified. Retain model-based\ncounterfactual simulation as a separate, conditional analysis. Reject the use\nof a supplied-model answer as evidence that observational records identify it.','Symbolic identification determines what can be learned before an estimator\nis selected. Model-based counterfactual simulation answers a separate question\nconditional on the supplied structure. A simulation from that structure\ntherefore cannot establish identification from observational records.'),
('Integrate established effect-estimation machinery through a narrow specification;\nretain separate adjustment variables, effect modifiers and population weights.','An explicit specification separates adjustment variables, effect modifiers\nand population weights before an existing estimator is used.')]
for old,new in replacements:edit(sw,old,new,'Replace repeated commands with the scientific reason for the choice.','Same local assumptions, comparison and limits.')
p=path('/software-conclusions.tex')
between(p,r'\section{Buy a method for a question}', 'Panel comparisons require the same care.',r'\section{Why equal data do not imply equal targets}'+'\n\n'+'The projection comparison in Section~\\ref{scisyn:software} and the offer\nexample in Chapter~\\ref{rewrite:deposit} show why target weights matter.\nThe inspected EconML implementation and its independent calculation support\nthat restricted comparison. \\citep{exec19_econml_source,exec19_econml_reference}\n\n','Remove repeated selective-reuse and projection exposition.','scisyn:software subsection 5 retains the equation, restrictions and source; rewrite:deposit retains its monetary consequence.')
a=p.read_text();a0=a.index(r'\section{A selective recommendation}');a1=a.index('These are proposal recommendations',a0)
edit(p,a[a0:a1],r'''\section{When an implementation detail is consequential}
The selected routes in Section~\ref{rewrite:software-selection} use existing
procedures under declared targets and observation laws. A native port incurs
another implementation and validation burden; its benefit must cover that
burden. The inspected integration design develops that cost comparison.
\citep{exec16_s10_design}

''','Remove the second recommendation table and duplicated porting conclusion.','rewrite:software-selection retains all five table needs, alternatives and reversal conditions across its seventeen areas; uncertainty and rollout examples remain here.')
s=p.read_text();a=s.index(r'\section{The unresolved comparisons}')
edit(p,s[a:],r'''The remaining uncertainty is specific to a candidate: its supported target,
version, reuse terms or performance on the proposed study. The commercial
comparison in Section~\ref{gap29:software-followup} distinguishes those
questions from missing bank entitlements and actual prices. An unobserved
capability remains unknown. The investment decision in
Chapter~\ref{rewrite:investment-decision} compares the resulting routes.
''','Remove a third generic selective-investment conclusion.','software-followup retains omissions and version/rights limits; investment-decision retains the alternatives and decision rule.')
# Unify software parts by using one top-level chapter.
for suffix,title in [('/software-followup.tex','Existing commercial capabilities and their terms'),('/software-selection.tex','The selected routes and the comparisons that could change them'),('/software-conclusions.tex','An implementation comparison must preserve the target')]:demote(path(suffix),title)
# Assistance: preserve distinct worked measurement example, consolidate repeated advice.
p=path('/assistance-decisions.tex');s=p.read_text()
new=r'''\section{Mechanisms, timing and the interpretation of a diagram}
\label{scisyn:assistance}
A retention request can mean an invitation, acceptance, a price change or a
repeated contact rule. The distinction determines the population and
intervention before any graph is evaluated. Question clarification and graph
critique are plausible assisted tasks in the inspected literature.
\citep{v12_la_2305_00050,v12_la_2606_23608}

Each proposed edge needs an economic interpretation, an information date and
supporting evidence. A graph with unresolved directions can already guide a
decision when every credible member implies the same action. Conversely, one
wrong orientation can reverse a financial sign even when most edges are
correct. The mixed LACR retrieval results support testing the retrieval choice
itself. \citep{v12_la_2402_15301}

Formal reasoning under a supplied mechanism and eliciting the mechanism of a
new bank are different tasks. CLadder and causal-learn+ motivate different
comparisons on that distinction. In a repeated policy, later observations
cannot silently become pretreatment adjustment variables. An unsupported
calculation calls for an explanation of the missing information or a revised
question. \citep{v12_la_2312_04350,v12_la_2606_23608}
'''
edit(p,s,new,'Consolidate duplicated formulation, questionnaire, graph and evaluation recommendations.','rewrite:assistance-tasks contains detailed task comparators, refusals, held-out evaluation requirements, costs and ORCA evidence; this section preserves the distinct same-action-across-models observation and policy clock.')
p=path('/assistance-conclusions.tex')
between(p,r'\section{Improve the question before automating the answer}',r'\section{Better measurement can still leave confounding}', '', 'Remove repeated formulation and LACR recommendations.','rewrite:assistance-tasks and scisyn:assistance preserve all tasks, evidence roles, retrieval limits and citations.')
s=p.read_text();a=s.index(r'\section{Keep the economist');edit(p,s[a:],r'''This example concerns the validity of the measurement used for adjustment.
The task comparisons in Chapter~\ref{rewrite:assistance-tasks} separately
address formulation, discovery, formal reasoning, execution and reporting.
They distinguish supplied-structure benchmarks from elicitation of a new
bank mechanism. \citep{v12_la_2312_04350,v12_la_2606_23608}
''','Remove a third task-level conclusion and duplicated evaluation rules.','rewrite:assistance-tasks retains the questionnaire, search, formal, scripted and template comparators, full correction cost, refusals and conditional expansion rule.')
demote(p,'Measurement accuracy and causal validity')
edit(ass,'The evidence\nsynthesis in Chapter~\\ref{scisyn:assistance} and the detailed studies','The evidence\nsynthesis in Section~\\ref{scisyn:assistance} and the detailed studies','Repair chapter reference after consolidation.','Same evidence.')
edit(ass,'The\nfrontier census remains 82 inspected and 31 unread; this synthesis does\nnot claim those omissions have been resolved.','The\nfrontier evidence includes the three additional inspected originals discussed\nin Section~\\ref{gap29:frontier}. The current census is 85 inspected and\n28 unread; these omissions still limit broad claims.','Update a stale census using the existing inspected-source delta.','gap29:frontier and preserved frontier-source-audit.json; historical 82/31 remains in baseline records.')
for suffix,title in [('/measurement.tex','What repeated readings add to measurement'),('/frontier.tex','What causal reasoning benchmarks establish')]:demote(path(suffix),title)
# Investment: one authoritative recommendation with its detailed accounts retained.
p=path('/practical-investment.tex');s=p.read_text();a=s.index(r'\section{A conditional recommendation to the sponsor}')
edit(p,s[a:],r'''The economic comparison of these workflows is developed in
Chapter~\ref{rewrite:investment-decision}. Its account includes unsuccessful
studies, correction, interpretation and maintenance, and distinguishes a
prototype comparison from a later bank-data pilot.
''','Remove duplicate investment recommendation and annual benefit formula.','investment.tex retains B=N(wh+D)-C-K, all variables, double-counting caution, no observed ROI, matched study and stop/narrow/continue decisions.')
edit(p,r'\chapter{A worked local study and the next investment}',r'\chapter{What the local study interfaces preserve}','Give the operational chapter a distinct purpose.','Same walkthrough, initial timeout, versions, commands and public-data roles retained.')
p=path('/s_617eeb5ab919f5.tex');demote(p,'The multi-year investment account and institutional variation')
s=p.read_text();a=s.index('For a banking group, the defensible first investment is therefore');edit(p,s[a:],r'''The multi-year account prices the reuse hypothesis rather than a causal
method in isolation. Its cost and volume assumptions are sensitivity inputs
to the decision in this chapter, not observed bank demand.
''','Remove repeated final recommendation.','investment.tex supplies the current conditional recommendation; all cost formulas, examples, budget assumptions and institutional variations remain here.')
# Preserve EVSI and source/rights limits but eliminate a superseded status claim.
p=path('/split_327_3.tex');demote(p,'The value of obtaining additional evidence')
edit(p,'The survey has established a usable portfolio and a concrete public-data\nacquisition/profile, not six executed new studies. Current-source web\nsnapshots still need exact data-file vintages for future analyses.','The public-data portfolio supports specific analyses, including the\nearnings experiment and the UCI timing comparison in this volume. These\nexecutions do not qualify every candidate dataset. Current-source web\nsnapshots still need exact data-file vintages for future analyses.','Replace stale survey status after the new executed studies.','gap29:public and scisyn:evidence supply actual studies; individual rights and access omissions remain in this section.')
# Insert the two distinct detailed treatments before the final spending sequence.
mark=r'\section{A spending sequence with real alternatives}'
edit(inv,mark,inp(path('/s_617eeb5ab919f5.tex'))+'\n'+inp(path('/split_327_3.tex'))+'\n\n'+mark,'Bring detailed accounts and value of information under the authoritative investment decision.','All imported material remains compiled once at its existing labels.')
edit(inv,'The detailed comparisons\nand operating evidence that follow allow a reader to inspect those','The detailed comparisons\nand operating evidence developed in the book allow a reader to inspect those','Remove obsolete forward direction after relocation.','Same rationale.')
edit(inv,'The earlier illustrative investment account in Chapter~\\ref{r3:investment}','The illustrative investment account in Section~\\ref{r3:investment}','Repair intra-chapter navigation.','Same account and 26.74 threshold.')
# Dated administrative state belongs in the audit; preserve substantive conditions.
p=path('/s_7d439ea161defb.tex')
old='The current external-input\nregister has seven missing groups, including scientific review, bank truth,\nplatform, consumers, workflow economics, and sponsor decision; the named\nowners remain unassigned and the intake ledger contains no external\nreceipt.'
new='Institutional acceptance additionally requires identifiable responsible\nowners and authentic evidence for scientific review, bank truth, platform,\nconsumers, workflow economics and the sponsor decision.'
edit(p,old,new,'Move dated owner/intake status out of the scholarly narrative.','The exact former status is preserved in edits.json; all six substantive adoption conditions remain in this section.')
start='The integrated next step is a preserving, generated/public prototype that'
s=p.read_text();a=s.index(start);z=s.index(r'\label{exec17:integration-continuity-end}',a)
new=r'''A prototype comparison can test whether the same scientific context survives
library calls, command-line decoding, protocol transport and declared job or
storage failures. Its record needs full request, response, cost and refusal
denominators. Success under constructed failures supports a scoped consumer
and platform trial; it supplies no authentic bank truth or institutional
approval. The economic decision to fund that trial depends on its information
value and a meaningful precision requirement, as developed in
Chapter~\ref{rewrite:investment-decision}.
'''
edit(p,s[a:z],new,'Replace obsolete next-step administration with its substantive evaluation argument.','All test dimensions, complete denominators, scoped trials and adoption boundaries retained; current execution status is in the programme.')
(O/'edits.json').write_text(json.dumps(E,indent=2)+'\n');print(json.dumps({'explicit_edits':len(E)}))
