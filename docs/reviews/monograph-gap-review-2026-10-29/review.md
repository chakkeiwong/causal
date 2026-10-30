# Gap assessment of the causal banking monograph

29 October 2026, Asia/Shanghai. Prepared in response to the request to review the current work against the required standard.

## Verdict and scope

The current reading edition requires a substantial developmental rewrite and a targeted scientific review before it meets the commissioned monograph standard. It contains valuable derivations, careful counterexamples, substantial source inspection and some reproducible studies. Those assets do not yet form a consistently developed argument that lets a bank choose a bounded product, understand why it should work, compare credible alternatives and decide which experiment to fund. The most consequential deficiency is the connection between the accumulated technical material and the proposal's decisions. Another introductory chapter or a further collection of package reviews will not resolve that deficiency.

The supplied [editorial review](../../reading-edition/editorial-review.md) is chiefly a release note and a statement of verification limits. Its preservation findings are useful, and it explicitly withholds visual, human and full-survey acceptance. It does not provide the adverse, chapter-specific assessment needed to establish that the repair meets the standard. This report supplies that assessment without treating the earlier review as a claim of final acceptance.

The assessed artifact is `docs/causal_banking_reading_edition_2026-10-29.pdf`, SHA-256 `3e8e7e88eea953e50da745eb3bcaa4faa1af34ed48d81d75fad8f3bb4b361ac3`. It has 1,795 physical pages, 89 numbered chapters, nine parts, 1,705 numbered main-text pages and an 83-page bibliography. The protected 1,774-page predecessor is a different artifact. Page references below are printed body pages; add seven for the physical PDF page.

This assessment combines an all-page text/structure scan, close reading of the cited passages and their source files, comparison with the archived FinMarketing exemplars, and six newly rendered page inspections. It is not a line-by-line mathematical referee report on all 1,795 pages. No new literature search or external package-performance assessment was undertaken. The literature cutoff remains 7 October 2026. The findings are about this manuscript, its evidence organization and its declared requirements. The manuscript and historical evidence were not rewritten.

## What the required standard actually demands

The [master program](../../program/master-program.md), [active repair plan](../../program/scientific-editorial-repair.md) and applicable prose/source policies require more than topic presence. A reader must be able to reconstruct the chain from a banking decision and information clock through the causal model, identification, estimation, uncertainty, numerical behavior and monetary consequence. Alternatives must be compared on their assumptions and outputs; evidence must justify an actual recommendation.

The inspected FinMarketing examples establish a useful comparison. Its heterogeneous-effect treatment introduces the target, compares learner losses, explains the remainder and rate conditions, and interprets what the resulting inference permits. Its dynamic-choice discussion matches the primitives of the customer's problem, derives the fixed-point and continuation calculations, and distinguishes the customer's objective from the bank's. The standard is this continuity of explanation, not a page count or an obligation to duplicate that book's structure. The comparison uses the preserved excerpts and hashes in [reference-standards-2026-10-08.json](../reference-standards-2026-10-08.json), not an assertion that those reference monographs have received independent correctness approval.

| Requirement | Current assessment | Consequence |
|---|---|---|
| Developed causal foundations and derivations | Substantial material exists; quality is uneven and a full correctness review is outstanding. | Preserve and improve the strong chapters; do not repeat the obsolete diagnosis that the book contains only method names. |
| One cumulative economic argument | Part headings and introductions improve orientation, but do not reconcile the underlying collection. | Developmental rewrite is required. |
| Comparative software conclusions across the required scope | Detailed individual reviews coexist with an incomplete common recommendation. | Finish the synthesis before claiming the software survey is complete. |
| Evidence-based assessment of language assistance | Strong critical examples and evaluation designs; proposed comparisons and external reports remain distinct from demonstrated local benefit. | Complete the task-level synthesis and make recommendation strength explicit. |
| Worked banking studies and practical use | Existing examples and local executions are useful, but the reader must assemble the complete route across distant chapters. | Reconstruct complete cases with consistent targets and results. |
| Conditional investment recommendation | Reproducible illustrative accounts exist; the selected scope and discriminating experiment remain insufficiently integrated. | Derive the proposed first investment from the comparative evidence. |
| Traceable sources and preserved evidence | Strong file-identity results; these do not establish claim fidelity or complete literature coverage. | Retain the audit and perform claim-level review where recommendations depend on it. |
| Reader-ready prose, references and presentation | Six sampled pages are legible; confirmed citation defects and disruptive passages remain. | Contextual editing and a broader rendered review are still required. |

## Findings, ordered by consequence

### 1. The new architecture rearranges a collection more than it reconstructs an argument

Parts IV and V occupy printed pages 164-1008, and the language-assistance part occupies pages 1009-1391. The final investment part occupies pages 1684-1705. These lengths are not quality scores. They show where the reader's attention goes: hundreds of pages of technical and package-specific qualifications precede a comparatively compact decision synthesis. The new software conclusion, Chapter 49, occupies only pages 1006-1008.

The contents also reveal unresolved overlap: Chapters 28, 33 and 44 return to heterogeneous effects; Chapters 36-40 revisit panels, rollout comparisons and synthetic controls; Chapters 48-49 both address acquisition choices; Chapters 61-63 separately cover evaluation, comparisons and the value of assistance. Recurrence can be productive, but the book needs to explain what each return adds and retire earlier provisional conclusions where later evidence supersedes them. The simple text scan did not find exact duplicate paragraph blocks; the finding is conceptual fragmentation, not a claim of verbatim copying.

The assembly preserves 328 top-level inputs and maps 425 source files. The recorded 136 editorial operations touch 83 source files. This is a credible preservation-and-reorganization exercise, but it is not evidence of contextual revision across the full manuscript. The repair should assign each central question one authoritative treatment, integrate its later findings there, and make detailed implementation evidence separately accessible. Scholarly depth must remain available rather than being replaced by an executive summary.

Acceptance requires each chapter to advance an identifiable conclusion and each part to change or substantiate a banking recommendation. A reader should not need to reconcile several generations of discussion independently.

### 2. The central banking example does not yet preserve its own target

Chapter 1 provides a useful economic opening, but its transitions expose exactly the semantic risks the book warns about. On page 3, `Y_i(a)` is quarterly household contribution under an offer. The next calculation concerns an annual balance response to a rate increase. On page 4, `Y` denotes deposit balances, while the prose moves between accepting an offer and receiving it. The annual accounting example is explicitly introduced as an illustration, so its arithmetic is not wrong. The issue is the unexplained relationship among different interventions, outcomes and horizons.

The break-even calculation reproduces: an additional balance of GBP 1,090.91, with values of GBP -2.50 and GBP 25 at additional balances of GBP 1,000 and GBP 2,000. Correct arithmetic does not make an invitation effect, an acceptance effect and a rate-change effect interchangeable. The closing reference on page 4 sends the reader to Chapters 2 and 88 for identifying alternatives; Chapter 88 is the investment account. That reference resolves mechanically but does not direct the reader to the relevant instrumental-variable and discontinuity developments.

Repair the opening around explicit notation for invitation, receipt and price, separate balance from contribution, and fix the horizon. When a new illustration changes these quantities, explain the change. Carry the same defined case through identification, a chosen estimator, uncertainty, a financial calculation and the final recommendation. Other banking journeys should retain their own targets rather than being forced into the deposit model.

### 3. Software detail has not been converted into the required comparative decision

Chapter 19 defines a broad method-by-language/commercial scope and candidly explains the limits of its initial searches (pages 174-183). Chapter 48 develops meaningful comparison principles and a stipulated paired-workload calculation (pages 997-1005). These are useful foundations for a recommendation.

Chapter 49's recommendation table nevertheless says, for example, to reuse an estimator suited to the population, compare panel estimands and use a method that represents the policy's information. These are selection principles. They do not identify the preferred candidate, serious alternative, required restriction, integration route or evidence that decides between them. Specific findings exist elsewhere, but the concluding table does not reconcile them into the required 17-area comparison. Its final statement that several editions and implementation paths remain unresolved does not name which unresolved comparisons could change the proposed product.

For each required area, produce a common comparison with the banking task, estimand, maintained assumptions, sampling restrictions, candidate versions, competing method, inspected versus executed evidence, reuse choice and consequential unknown. A defensible outcome can be a restricted recommendation or an explicit unresolved choice. A source review can justify a prototype candidate without establishing runtime superiority. Separate those strengths of recommendation.

Acceptance requires the reader to be able to choose a candidate and explain why the strongest alternative was not selected, without searching hundreds of pages for qualifications.

### 4. The language-model discussion needs an integrated answer, not further accumulation alone

There is substantive analysis here. Section 62.1 examines whether benchmark scores measure the claimed task, distinguishes refusal from justified nonidentification, and scrutinizes aggregation (pages 1351-1354). Chapter 61 distinguishes held-out evaluation, contamination, failed-request denominators and complete cost. This review does not independently revalidate those external-paper conclusions; it recognizes the depth of the manuscript's argument.

Chapter 63 then offers plausible tasks and proposes comparisons with questionnaires, search and unaided analysts (pages 1390-1391). It does not consolidate the preceding studies into a clear assessment of which tasks have convincing published support, which remain conflicting, and which are only hypotheses for this product. Section 61.6 explicitly says that no final live experiment has been registered or run (page 1306). Offline examples and literature reports cannot establish the proposed assistant's incremental quality or savings.

The rewrite should compare formulation, variable construction, diagrams, discovery, identification, execution and reporting separately. For each, state the best positive evidence, strongest adverse evidence, baseline, transfer limitation, failure remedy and current recommendation. Distinguish performance on a supplied mechanism from eliciting a defensible mechanism for a new banking problem. Do not average scores across incompatible tasks.

A complete proposal can conclude that an assistant should be evaluated on a narrow task. It does not require a fabricated live evaluation. It does require a reason why that task and baseline are the most informative next comparison.

### 5. The public evidence is useful, but the proposal does not yet bring its consequences together

Section 72.3 identifies existing public 401(k) and monetary analyses and a completed UCI Bank Marketing data profile (page 1587). Chapter 75 contains fitted results, synthetic studies and limitations. For example, the public 401(k) discussion reports estimator comparisons and explicitly identifies its working iid covariance and missing survey-design information (pages 1606-1607). These are real evidentiary assets. It would be inaccurate to say the manuscript has no empirical work.

Chapter 74 proposes six further studies, while Section 89.4 explicitly says that these are not six executed new studies (pages 1594-1597 and 1704-1705). The reader needs one consolidated account linking existing findings to the proposed experiments: what failed, what changed the method choice, what remains unresolved and why resolving it merits the cost. A data profile, score-equivalence check, synthetic calibration study and observed causal estimate have different evidentiary roles.

Construct a study-level synthesis with target, data role, identifying assumptions, comparator, uncertainty, observed result, monetary implication and design consequence. Then select the smallest additional public or generated study that could change a recommendation. Do not run every proposed study merely to close a list. Missing bank data does not prevent this synthesis.

### 6. Practical use is interrupted by implementation and program-status material

The practical part spans pages 1392-1582. A chapter entitled “Conducting a study with the proposed service” begins with execution identities, hashes and idempotency (Chapter 68, page 1481). These are legitimate engineering subjects, but they do not show an economist how to conduct the study. Section 68.16 later discusses unassigned owners, the intake ledger, receipts and release-equality checks (pages 1494-1495). That is current program machinery inside the product narrative.

Section 68.17 supplies a useful bounded example: 24 authored cases, 98 invocation slots and explicit response categories, with `graph.discover` unsupported (pages 1495-1497). The text correctly distinguishes computed responses from estimated causal effects. This should become a clear explanation of what the present reference service does, followed by a separate proposed extension. The user should not have to infer functionality from conformance counts.

Begin each practical case with a bank question, permitted inputs and assumptions. Show a concrete library/CLI/MCP request, the actual returned result or explicit unsupported response, its interpretation, uncertainty and next decision. Move detailed recovery, storage and current intake administration into the technical/operating material. Retain any implementation detail that changes the scientific answer at the point where it matters.

### 7. The investment account is numerically developed but not yet tied tightly enough to the selected product

Chapter 88 contains a genuine cost comparison, avoids double-counting labor savings as business value, and distinguishes a capable expert workflow from the proposed common product. Its illustrative break-even of 26.74 annual studies and its scenario table reproduce (pages 1698-1701). These are strengths. This is not a missing-spreadsheet problem.

The gap is the link to the selected scope: which repeated studies generate the assumed savings, which components provide those savings, how much of the work is still bespoke, and which alternative could supply equivalent quality more cheaply. Chapter 87 gives four possible next routes; Chapter 89 gives a value-of-information framework and further hypothetical arithmetic. The ending should make one conditional, evidence-based recommendation about the first experiment or bounded prototype, with explicit reasons for its priority.

Separate measured quantities, stipulated planning inputs and unknowns. Compare expert composition, minimal integration, the proposed shared service and relevant commercial alternatives at equivalent scope. Identify the parameter or observation that reverses the choice. Actual institutional prices are necessary for an adopted business case, but are not a reason to postpone a coherent conditional proposal. The sponsor predecessor also needs eventual alignment with the revised recommendation; it is currently disclosed as unpaired.

### 8. Source preservation is strong; citation presentation and survey closure remain separate gaps

The inherited audit contains 1,453 citation records, including 277 paper records and 388 records explicitly categorized as project material. A recursive check of 9,487 distinct local path/hash bindings found no missing files or hash mismatches. All paper records resolve to PDF-header files beneath `docs/papers`, including one intentionally versioned subdirectory. This is file-identity evidence, not an exhaustive authenticity, filename, claim-support or corrections audit.

The initial review probe recognized only the principal-binding schema and falsely flagged 39 differently structured records. Inspection of `local_records`, `local_sources` and nested `records` resolved them. A direct-parent-only paper check also incorrectly flagged the legitimate version subdirectory. These diagnostic failures and corrections are retained in [source-binding-check.json](source-binding-check.json). No missing-paper finding is asserted.

The count of 1,453 must not be described as 1,453 independent scholarly studies. The many project and software entries have useful evidentiary roles, but the bibliography should make those roles intelligible. There is also a confirmed rendering defect: the CELLO authors appear as the literal string “Meiqi Chen and Bo Peng and Yan Zhang and Chaochao Lu” throughout page 1352. The generated bibliography treats the entire list as one braced author. Missing spaces before several parenthetical citations are visible on page 693, and some bibliography titles/date strings are compressed. Reference resolution did not detect these problems.

Normalize author and title metadata in the successor's bibliography-generation path, keep stable audit keys, and reconcile repeated records for the same work where their identities and claim scopes permit it. Do not erase version distinctions. State which conclusions use inspected primary technical support, which use project derivations and which remain provisional. Finish the material omission/competing-source decisions as of the fixed cutoff; more citation keys alone do not close the survey.

### 9. Mathematical preservation is necessary but the current comparison is too narrow for a rewrite

The foundations contain real constructions: Chapter 3 derives the linear IV moment and the different complier interpretation; Chapter 4 derives an influence function, an exact nuisance remainder and distinctions among learner losses; Chapter 6 derives mechanism replacement and a treatment-confounder feedback example. These are evidence of substantive progress relative to the early October assessment. They should be treated as the starting assets for reconstruction.

The builder's preservation check, however, compares citation-key counts, equation-environment counts, labels and displayed-math strings (`tools/build_reading_edition.py`, lines 447-465). It does not prove that explanatory prose, inline mathematics, quantifiers, assumptions or the attachment of a citation to a claim retain their meaning. Literal equality of all displayed mathematics also makes it difficult to consolidate repeated derivations in a genuine rewrite.

Preserve the predecessor and introduce a reviewed map from substantive claims and derivations to their new locations. Each removal, merger or changed assumption needs a reason; a mathematical correction must be allowed and recorded. Then conduct targeted scientific review of the product's load-bearing arguments: the chosen funding inference under dependence, sequential policy identification and uncertainty, graph uncertainty carried to effects, and measurement/linkage uncertainty carried to financial value. This assessment has not proved those arguments wrong. Their full correctness remains a separate review obligation.

### 10. The editorial completion label is stronger than the evidence for its stated question

The active priority file marks E01 complete and asks whether an economist can follow the argument from a banking choice to an investment decision. Its evidence establishes delivery of a reorganized artifact and mechanical checks; the same file leaves final editorial acceptance false and a separate review pending. The active master describes structural and contextual repair as delivered. These distinctions should be made sharper in light of the present findings.

Retain the mechanical delivery as completed history. Record developmental rewriting and substantive editorial review as open work, with the present report as evidence. Do not convert the historical program's pass or the priority-consistency check into approval of prose, scholarship or proposal completeness. Both checks passed in this review and explicitly disclaim that interpretation. No protected historical completion receipt needs to be erased.

## What to retain and what to change

Retain the source archive, exact negative examples, target distinctions, meaningful uncertainty qualifications, selected derivations, reproducible study results and financial accounts. The six sampled pages show that the typesetting can support clear mathematics and useful figures. No clipping was visible in those samples.

Consolidate repeated method descriptions and source-specific caveats around the question they resolve. A scientific conclusion should normally lead; version-specific evidence should support it. For example, the packed-bit discussion on page 693 carefully limits its result and says material coverage consequences are not established. Its full implementation detail should not command the same narrative prominence as the adjoining sensitivity argument that changes the offer's financial interpretation. Preserve the result and evidence in an appropriate technical location.

Replace generic advice such as choosing a suitable estimator with a justified choice under stated conditions. Remove current program status from the reader's economic argument. Correct misleading transitions and notation changes. Add diagrams or worked tables where they explain the chosen model or decision; a quota of new figures is not an acceptance criterion. The six previews do not establish whole-document visual or human editorial acceptance.

## A concrete rewrite and review sequence

1. **Fix the decision structure.** Write the conditional product recommendation and the four banking questions it must answer. Map existing chapters to those questions and identify what is retained, merged, moved to detailed technical material, or still unsupported. Preserve the protected edition and source identities.
2. **Reconstruct one complete anchor case.** Start with the deposit-offer example, resolve its intervention/outcome/horizon changes, and connect it to the relevant identification argument, estimator, uncertainty, numerical evidence and monetary conclusion. Use this case to test the exposition standard before repeating the approach for servicing, discovery-to-effect and observation construction.
3. **Complete the two comparative syntheses.** Reconcile the 17-area software comparison and the task-level language-assistance evidence into explicit choices, alternatives, consequential unknowns and bounded recommendations. Finish missing scholarship before initiating broad implementation campaigns.
4. **Integrate evidence and economics.** Consolidate the executed studies, distinguish the six proposed studies, choose the next discriminating experiment, and derive the first investment recommendation from the selected scope. Reconcile the sponsor argument afterward.
5. **Review scientific meaning and presentation.** Review the central derivations against primary anchors and declared sampling laws; use a substantive preservation map; normalize citations and navigation; compile the successor and inspect its actual rendered argument, tables, figures and references. Keep human editorial acceptance separate.

The first concrete continuation should be an annotated decision outline and a rewritten anchor-case chapter with its claim-preservation map. Beginning another low-level runtime investigation would not address the leading findings in this review unless it changes that case's conclusion. No new agents, external contacts or bank inputs are needed to begin the rewrite.

The rewrite is ready for proposal acceptance when a qualified reader can reconstruct each central argument, identify the evidence behind each recommendation, compare the serious alternative, and understand what observation would change the decision. Negative scientific results and unresolved bank-specific inputs can remain. Unfinished synthesis, unexplained target changes and provisional comparative choices cannot be hidden behind those later institutional requirements.

## Evidence and limits of this assessment

The accompanying [evidence record](evidence.json) identifies inspected local sources and hashes, structure counts, sampled pages, command outcomes and diagnostic limits. [Selected page windows](inspected-page-excerpts.txt) preserve context; their inclusion is not a claim that every archived page received close reading. The [arithmetic check](arithmetic-check.json) reproduces the inspected stipulated financial examples. Six compressed page previews are saved in `previews/`; their combined forwarded image URLs were 1,275,222 characters, within the inherited session limit.

`python3 tools/causal_program.py status`, `python3 tools/causal_program.py check` and `python3 tools/scientific_program.py check` completed successfully. They establish their declared state/link/identity results. They do not establish independent scientific review, final editorial acceptance, authentic bank validation or adoption. The existing successful build receipt was inspected; the unchanged monograph was rendered for this review rather than republished.
