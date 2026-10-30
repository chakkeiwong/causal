from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];D=R/'docs';O=D/'writing-repair/2026-10-29';P='writing-repair/2026-10-29/'
M=json.loads((O/'source-map.json').read_text());E=json.loads((O/'edits.json').read_text())
def path(suffix):
 hit=[v for k,v in M.items() if k.endswith(suffix)];assert len(hit)==1;return R/hit[0]
def edit(p,old,new,why,dest):
 s=p.read_text();assert s.count(old)==1,(p,old[:80],s.count(old));p.write_text(s.replace(old,new,1));E.append(dict(file=str(p.relative_to(R)),before=old,after=new,reason=why,substantive_destination=dest))
def append(p,text,why):
 s=p.read_text();edit(p,s,s+'\n'+text,why,'Added explanation with all existing evidence retained.')
def inp(p):return r'\input{'+str(p.relative_to(D))+'}'
j=path('/journeys.tex')
# Add explicit inference paths. These are connections to completed evidence, not new claims of experiments.
sections=[(r'\chapter{Servicing decisions change',r'''\section{From the household offer to broader funding evidence}
Two extensions show what this transparent report leaves to be learned.
Chapter~\ref{gap29:public} estimates an assignment contrast from the retained
public experiment, compares adjusted and unadjusted estimators, examines
influence, and subtracts an explicit cost. Its earnings units and population
are different from the deposit account: the exercise tests an inferential
and reporting route, not transport of an earnings effect into bank balances.
Chapter~\ref{gap29:funding} follows institutions rather than households and
asks whether fixed effects can repair a misassigned outcome. They cannot
recover the institution's identity merely by absorbing a persistent level.
The structural funding and calendar arguments explain the additional shock
and dependence assumptions needed for that journey.

For the offer study, the next source of information is assignment support and
correct household aggregation; for the institutional panel it is a coherent
exposure and outcome history. A bank cannot substitute a successful estimate
in one of these populations for the missing design evidence in the other.
The shared report can preserve both questions without pretending they have
the same estimator or sampling law.

'''),(r'\chapter{A learned graph can leave',r'''\section{Estimated policies, missing rewards and decision uncertainty}
Chapters~\ref{gap29:servicing} and \ref{gap29:policy-uncertainty} carry the
policy question into fitted data. They use a separate three-decision economy,
with continuous states and rewards already net of the stipulated action cost.
Those reward units are not the pounds in this two-contact example. Whole
customers, rather than isolated rows, supply the sampling units. A separate
training sample chooses the policy; evaluation and resampling hold that
selected policy fixed.

The fitted comparison is informative precisely because it can fail.
Under its maintained state and observation model, improvement coverage is
94\% with an average interval width of 0.711 reward units. Future-dependent
dropout reduces coverage to 6\%; omitting a state predictor reduces it to
61\%. These observed fractions have Monte Carlo uncertainty, reported in
the study. They demonstrate that resampling an estimated model does not
repair an invalid observation assumption.

The financial interpretation follows the reward definition. Where costs are
already subtracted, subtracting contact cost again would double-count it.
Where a bank's reward law and initial distribution must also be estimated,
the supplied-law components of the generated comparison cannot be treated
as known. Outcome follow-up, action support and measured decision history
therefore determine whether its narrower uncertainty can be useful.

'''),(r'\chapter{Correcting records can change',r'''\section{From a known covariance to estimated effect sets}
Chapter~\ref{exec13:temporal-region} supplies the next inferential step under
a restricted stationary Gaussian time-series model. It constructs a region
jointly over the observed covariance, a continuous unknown common lag and a
declared family of causal models, then maps that region to effects. The
coverage argument keeps the true model and observed-law uncertainty together;
it does not condition on an orientation chosen for convenience. The chapter
also shows what a direct intervention can add.

This is a developed restricted construction, not an executed general
bank-discovery pipeline. The maintained graph family, scalar lag and
innovation law must be defensible before applying it. An unrestricted latent
model may leave the whole line admissible. In the opening pricing example,
the narrower set already contains opposite net values, so a more elaborate
estimator is useful only if its information or restrictions can resolve a
consequential ambiguity. A labelled whole-line result can be the correct
answer to a well-defined question.

''')]
for marker,addition in sections:
 s=j.read_text();a=s.index(marker);edit(j,s[a:a+len(marker)],addition+marker,'Connect the opening journey to its existing fitted or restricted-inference treatment.','Named retained chapters, with units, targets and qualifications explicit.')
append(j,r'''\section{A fitted linkage analysis needs an external information budget}
Chapter~\ref{gap29:observation} studies a different observation problem:
matching randomized participants to outcomes when identifiers are corrupted.
It compares exact and fuzzy rules, keeps unmatched customers in the target,
and derives a contribution bound when at most a supplied number of candidate
lists omit the true match. Sampling uncertainty is then added under explicit
support and assignment assumptions. This is not an estimate of the receipt
matrix used above; the two studies concern different measurement mechanisms.

At 30\% outcome-dependent corruption, the robust population interval averages
119.1 outcome units in width, compared with about 4.1 for the fuzzy analysis.
The extra width prices justified ignorance. The corruption budget and outcome
support are external premises, not quantities learned from matching confidence.
A monetary decision first maps those outcome units and bounds into its own
expense equation. When the admissible set straddles that decision threshold,
an independently resolved audit sample can be more valuable than a forced
match. The detailed history and audit studies retain the further complications
of dependent records and uncertain audit truth.
''','Complete the observation path without conflating linkage with receipt misclassification.')
# Correct stale interface account with the newer fitted-summary path.
old='The existing MCP walkthrough separately establishes graph syntax, conditional\nadjustment, information-date checks and refusal of a dependent sampling law\nthrough that route. It does not expose this new estimator as an MCP operation.'
new='The earlier MCP walkthrough establishes graph syntax, conditional\nadjustment, information-date checks and refusal of a dependent sampling law.\nThe public study in Chapter~\\ref{gap29:public} additionally sends actual\nfitted estimates and covariance summaries through library, CLI and MCP.\nIt preserves the resulting interval and conditional or contradicted\nassignment status. Neither path exposes the deposit raw-data estimator\nas an MCP operation.'
edit(j,old,new,'Align the implementation boundary with already executed newer evidence.','gap29:public preserves fitted-summary transformation and raw-data/report limitations; original walkthrough remains.')
p=path('/decision-synthesis.tex');old='Neither is a matched analyst trial, a full general\nestimation service, or evidence of improved bank outcomes.'
new='The later public experiment also carries fitted effect and covariance\nsummaries through all three interfaces (Chapter~\\ref{gap29:public}).\nRaw-data fitting and final reporting remain local scripts. These executions\nare not a matched analyst trial, a general estimation service or evidence\nof improved bank outcomes.'
edit(p,old,new,'Include the latest interface evidence without overstating it.','Public study and all former cases retained.')
append(p,r'''\section{What the newer studies add to that choice}
The public earnings contrast tests the complete chain from observed rows to
uncertainty and an explicit spending hurdle. A positive contrast alone does
not establish that a cost is covered. The servicing comparisons show why a
fitted policy can offer narrow but misleading uncertainty when dropout or
state assumptions fail. The institutional panel separates persistent level
adjustment from a coherent economic unit; the linkage study makes the cost
of a justified error budget visible. These results explain which information
the proposed study description must carry, rather than establish the benefit
of buying the service.

Together they favour a comparison on completed scientific work: whether an
analyst identifies the right target, preserves uncertainty, recognizes an
unsupported premise and reaches the correct conditional decision. The
software choices in Chapter~\ref{scisyn:software} and the investment account
in Chapter~\ref{rewrite:investment-decision} follow from that evidence.
''','Integrate already completed studies into the recommendation rationale.')
# Rewrite the reading guide, preserving the substantive opening.
p=path('/opening.tex');s=p.read_text();a=s.index('The main argument starts');z=s.index('Throughout the opening case',a)
new=r'''The opening develops an annual deposit decision and four worked journeys.
Their cross-references distinguish exact supplied-law calculations, fitted
public and generated evidence, and unresolved identification. The longitudinal
and panel foundations are followed by the servicing and funding studies;
the observation foundations lead directly into the linkage bounds. The graph
journey points to the restricted temporal confidence construction and its
additional-information argument.

The evidence and method-choice part compares statistical targets before
selecting software. Chapter~\ref{scisyn:software} is the authoritative
software treatment: developed comparisons, the seventeen-area selection,
commercial alternatives and a target-weight illustration sit together.
Chapter~\ref{rewrite:assistance-tasks} brings formulation, measurement,
benchmark evidence and task selection into one assistance treatment.
The subsequent detailed parts supply source-specific derivations and
comparisons for readers examining a particular method or operating route.

The final investment part distinguishes the value of information from the
value of a common analytical product. Chapter~\ref{rewrite:investment-decision}
brings the annual benefit account, multi-year cost examples, institutional
variation and value-of-information calculation into one conditional decision.
Its recommendation is tested against expert composition and existing
commercial capability. PDF bookmarks expose the detailed sections; chapter
and section references carry the reader between the opening question and
the supporting result.

'''
edit(p,s[a:z],new,'Make navigation reflect authoritative treatments and actual scientific sequence.','All original reading-guide distinctions retained in clearer locations.')
# Root assembly: import unified sections once and place applied studies beside foundations.
root=D/'causal_banking_integrated_argument_2026-10-29.tex';s=root.read_text();before=s
for parent,children in [(path('/software-decisions.tex'),[path('/software-followup.tex'),path('/software-selection.tex'),path('/software-conclusions.tex')]),(O/'assistance.tex',[path('/assistance-decisions.tex'),path('/assistance-conclusions.tex'),path('/measurement.tex'),path('/frontier.tex')])]:
 append(parent,'\n'.join(inp(x) for x in children)+'\n','Assemble one authoritative treatment with all distinct supporting sections.')
 for child in children:
  token=inp(child)+'\n';assert s.count(token)==1,(token,s.count(token));s=s.replace(token,'',1)
# Place unified assistance after software; the evidence chapter stays separate.
s=s.replace(inp(path('/software-decisions.tex')),inp(path('/software-decisions.tex'))+'\n'+inp(O/'assistance.tex'),1)
# Remove investment supports from their old positions; they are now in investment.tex.
for child in [path('/s_617eeb5ab919f5.tex'),path('/split_327_3.tex')]:
 token=inp(child)+'\n';assert s.count(token)==1;s=s.replace(token,'',1)
s=s.replace(inp(path('/s_8fab961defb5b0.tex')),inp(path('/s_8fab961defb5b0.tex'))+'\n'+inp(O/'investment.tex'),1)
for child,anchor in [(path('/servicing.tex'),path('/s_5bed5c573f1359.tex')),(path('/policy-uncertainty.tex'),path('/servicing.tex')),(path('/funding.tex'),path('/s_dfc3f7ec33f467.tex')),(path('/observation.tex'),path('/s_866a36af07dddf.tex'))]:
 token=inp(child)+'\n';assert s.count(token)==1;s=s.replace(token,'',1);s=s.replace(inp(anchor),inp(anchor)+'\n'+inp(child),1)
s=s.replace(r'\part{From evidence to a bounded investment}',r'\part{Evidence and the choice of analytical methods}')
old='The banking journeys and their foundations determine what a useful service\nmust preserve. The next chapters connect software choices, assistance,\nobserved studies, practical capabilities and the full cost account. Their\nconclusion selects the first experiment. Detailed comparative and operating\ntreatments remain in the following parts.'
new='The journeys and their foundations determine what a useful service must\npreserve. These chapters bring software selection, assistance, public\nevidence and implemented interfaces into that argument. Detailed comparisons\nthen develop the individual methods. The final investment part uses their\nresults and limitations to price the next experiment.'
assert old in s;s=s.replace(old,new)
edit(root,before,s,'Reassemble the book by question; remove duplicate chapter-level conclusions, not scientific treatments.','All inherited source files remain reachable exactly once; software and assistance subsections unify their evidence; final investment chapter incorporates all cost and information accounts.')
# Sponsor successor: integrate completed evidence and update status, retain all earlier substantive material.
sponsor=(D/'causal_banking_sponsor_rewrite_2026-10-29.tex').read_text()
sp=O/'sponsor-body.tex';sp.write_text((D/'developmental-rewrite/2026-10-29/sponsor-body.tex').read_text())
old='The\nnew estimator is not implemented as an MCP financial-analysis operation.'
new='The\ndeposit raw-data estimator is not an MCP financial-analysis operation. The\npublic experiment additionally sends actual fitted estimates and covariance\nsummaries through library, CLI and MCP with matching intervals; fitting and\nreport generation remain local scripts.'
edit(sp,old,new,'Update sponsor interface evidence.','Same limited route as the public-study chapter.')
edit(sp,'82 inspected and 31 unread entries.','85 inspected and 28 unread entries.','Reconcile sponsor with inspected frontier delta.','Three newly inspected originals retained in main assistance treatment; prior census archived.')
marker=r'\section*{What to reuse and what to compare}'
extra=r'''The public experimental subset contains 445 participants. Its estimated
earnings contrast is about 1,794, with approximate interval [479, 3,109] in
the archive's units. Subtracting an illustrative cost of 1,000 leaves an
interval crossing zero. The study compares native R and Python fits, which
agree within the declared numerical tolerance; it supplies no bank treatment
effect or general package ranking.

The newer generated comparisons sharpen the adverse cases. Servicing policy
improvement coverage falls from 94\% under the maintained model to 6\% with
future-dependent dropout and 61\% with an omitted state predictor. Fixed
effects leave bias when institutional outcomes are reassigned. Linkage bounds
can preserve a stated error budget while becoming too wide to support action.
These are conditional studies, with Monte Carlo uncertainty reported in the
monograph. They explain why observation assumptions and information costs
must remain visible in a completed report.

'''
edit(sp,marker,extra+marker,'Align sponsor with already delivered scientific evidence.','Current monograph chapters retain designs, denominators, uncertainty and limitations.')
edit(sp,'This sponsor text is aligned to the developmental rewrite dated\n29 October 2026, including its declared constructed examples and retained\nscientific continuation.','This sponsor text is aligned to the integrated argument dated\n29 October 2026, including its public experimental study, generated\ncomparisons and retained scientific derivations.','Pair sponsor with the actual successor.','No new empirical or deployment claim.')
header=(root.read_text().split(r'\begin{document}')[0]).replace('Integrated argument and comparative evidence','Sponsor proposal')
(D/'causal_banking_sponsor_integrated_2026-10-29.tex').write_text(header+'\\begin{document}\n\\maketitle\n'+inp(sp)+'\n\\end{document}\n')
(O/'edits.json').write_text(json.dumps(E,indent=2)+'\n')
print(json.dumps({'ledger_entries':len(E),'root':str(root.relative_to(R))}))
