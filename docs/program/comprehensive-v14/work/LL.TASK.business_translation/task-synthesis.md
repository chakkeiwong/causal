# A formulation workflow that preserves unresolved alternatives
\label{exec13:formulation}

A language model can make a business question more precise by exposing the decisions that its wording leaves open. Its useful output is a set of explicit candidate questions, with evidence for their variables and clocks, followed by a reasoned choice of a supported analysis. Fluency alone does not determine which candidate the bank intended. A formal causal engine also cannot repair a mistake that was made before the graph, intervention and target reached the engine.

Consider a manager who asks, “Which customers should receive a retention invitation next month, and how much value will it create?” One interpretation is the effect of offering the invitation to every currently eligible customer. Another is the effect among customers who historically received it. A third is the value of a targeting rule under a fixed contact budget. The first two are averages over different populations. The third also requires a feasible policy class, the information available when the rule acts, a comparator policy and a cost definition. A model that estimates historical recipients' average effect and calls it the expected value of the new targeting rule has changed the question.

The formulation record should therefore contain the eligible population and exclusions, the sampling unit, invitation and comparator, actual receipt if distinct, the decision time, permissible information, outcome horizon, monetary units and accounting treatment of contact cost. It should distinguish invitation from successful contact and from subsequent product use. Those variables may be causally related, but they are different interventions. It should also retain alternatives that remain unresolved: all eligible customers versus historical recipients, a single action versus a sequence, and gross revenue versus net value.

For a binary invitation \(A\), a baseline record \(W\) available at time zero, and a fixed-horizon outcome \(Y\), an initial target may be

\[
 \psi=\mathbb E_{\nu}\{Y(1)-Y(0)\},
\]

where \(\nu\) names the eligible population. The adjustment expression

\[
 \psi=\int\{m_1(w)-m_0(w)\}\,d\nu(w),
 \qquad m_a(w)=\mathbb E[Y\mid A=a,W=w],
\]

requires consistency, conditional exchangeability, positivity, suitable sampling and the declared interference restriction. The model may help elicit and document those assumptions. It cannot infer their truth from a plausible explanation or from a successful estimator call. In a generated development example, the project can stipulate and inspect the complete assignment law. In a later bank application, the assignment mechanism and measurement meanings need accountable scientific ownership.

## What the frontier evidence supports

The knowledge-assisted perspective of Kıcıman and colleagues motivates graph drafts, critique and connections to formal tools. Its own memorization probes and discussion of novel scenarios limit what benchmark success establishes. The inspected original distinguishes knowledge-based graph generation from conventional discovery from observations. For this proposal, a directional suggestion is a hypothesis with source provenance, not a discovered bank fact. A model can suggest that financial distress confounds retention contact and subsequent deposits; the analysis still needs to determine what was measured, when staff observed it and how it affected assignment. \citep{v12_la_2305_00050}

The medical co-pilot proposal develops a causal roadmap from a scientific question through study design and interpretation. Its examples of prevalent versus incident users are directly relevant to the distinction between existing account holders and newly eligible customers. That transfer is a project design proposal, not evidence that a medical demonstration validates banking workflows. The paper's evaluation discussion also makes clear that medical question-answering ability and causal study-design quality are different evaluation targets. Carefully cued illustrative responses do not establish reliable autonomous formulation. \citep{v12_la_2407_19118}

CLadder provides formally generated causal questions and explicitly separates levels of causal reasoning. Its results and limitations support using a formal reference to evaluate whether verbalized information was translated into the right query. Binary answer accuracy on its selected query families does not measure effect calibration, correct bank populations or decision loss. The paper also identifies the language-to-formal-tool interface as a remaining problem. The proposed baseline therefore checks the structured query before it scores a numerical answer. \citep{v12_la_2312_04350}

The 2026 CausalDS paper adds narrated synthetic structural models, data files, an observation layer and separate private scoring information. It distinguishes the conceptual variables used for identification from their noisy observed proxies. Its reported results separate symbolic reasoning, estimation, interval quality, abstention and tool cost. This is useful evidence for a multidimensional evaluation: correctly extracting a story's graph does not guarantee that the observed data identify or precisely estimate the stated effect. The paper's historical model results are author-reported; they have not been reproduced in this project. \citep{v12_la_2607_08093}

The 2026 observational causal-inference agent paper provides a concrete principal, actor and critic workflow built around deterministic analysis tools and reproducible notebooks. It reports favorable comparisons under its evaluated settings, while its disguised observational-study examples retain important overlap-related refusals. This supports investigating constrained analytical workflows with explicit diagnostics. It does not establish unmeasured-confounding control, longitudinal-policy identification or valid conditional coverage after the critic selects which estimates to report. Its point-in-time scope must survive transfer to the banking proposal. \citep{v12_la_2607_22443}

Two additional primary studies sharpen the boundary between an effective workflow and causal truth. Sng and colleagues study inconsistencies in causal-edge ratings and compare retrieval augmentation with a debate-and-arbiter design. Their retrieval experiment supplies a mocked true causal graph. The authors explicitly state that reduced inconsistency does not imply accurate causal prediction and call for true-graph validation. The title's language about eliminating hallucinations should therefore not become a guarantee in this product proposal. Consistent agents can agree on an incorrect edge, and a retrieval corpus can encode the same incorrect premise. \citep{exec13_hallucination}

CausalPulse describes query planning, semantic descriptions, process constraints, agent cards and MCP/A2A coordination for manufacturing diagnostics. Its reported operational success is a useful architecture comparison. The paper separately reports root-cause attribution, with a PSE Hits@1 of 0.44 and F1 of 0.39, using annotations of variables that changed at the anomaly time. Such annotations and tool-invocation success are different from interventional causal truth. The paper's local timing setup and manufacturing deployment discussion likewise do not establish banking runtime or treatment-effect performance. We can adapt its separation of semantic services, deterministic tools and workflow state as a design pattern while retaining those scientific limits. \citep{exec13_pulse}

These studies suggest complementary roles: retrieve definitions, draft alternatives, check logical consistency, construct typed calls, retain execution artifacts and explain formal results. The adverse findings point to the same missing link: a linguistic interpretation must be checked against the intended population, intervention, measurement model and information clock. An additional critic can help find mistakes, but agreement between related models is not independent validation of an assumption.

## A worked failure: an overlap remedy changes the population

Suppose the bank initially asks for the average invitation effect among all eligible customers. A diagnostic finds weak overlap for one customer stratum. An agent proposes trimming that stratum and continues to report the result as if it answered the original question. Even with perfect estimation, that continuation can be wrong.

To isolate the target issue, stipulate a three-stratum population with known masses, propensities and conditional effects. These are generated numerical assumptions; the units of the conditional effect are thousands of currency units per customer.

| Stratum \(w\) | Population mass \(p(w)\), invitation propensity \(e(w)\) | Conditional effect \(\tau(w)\) |
|---|---|---|
| 0 | \(0.5,\ 0.05\) | \(0\) |
| 1 | \(0.3,\ 0.50\) | \(2\) |
| 2 | \(0.2,\ 0.80\) | \(8\) |

The full-population ATE is \(0.5(0)+0.3(2)+0.2(8)=2.2\). Trimming to true propensities in \([0.1,0.9]\) retains half the population and gives \(2.2/0.5=4.4\). The conventional overlap-weighted target instead uses the measure proportional to \(p(w)e(w)\{1-e(w)\}\):

\[
 \psi_{\rm OW}
 =\frac{\sum_w p(w)e(w)\{1-e(w)\}\tau(w)}
        {\sum_w p(w)e(w)\{1-e(w)\}}
 =\frac{0.406}{0.13075}
 =\frac{1624}{523}\simeq 3.1052.
\]

The effect among treated customers is different again: \(\psi_{\rm ATT}=316/67\simeq4.7164\). Exact rational calculations reproduce all four values. None is an empirical estimate from a package or a live language model. Their disagreement arises entirely from the population measure. \citep{exec13_formulation_targets}

This distinction is visible in a real proposed reuse path. The inspected oci-agent notebook applies a propensity-based keep mask and averages AIPW pseudo-outcomes over that subset while labeling the output “ATO.” The accompanying paper describes the trimming remedy in the same terminology. A hard-trimmed average and an \(e(W)\{1-e(W)\}\)-weighted overlap effect are not generally equal. The integration must either label the result as a trimmed-population ATE, with its actual eligibility rule, or implement and validate the intended weighting operation. It must also retain the original all-eligible request and the excluded population. Estimated propensities add randomness to selection; the simple known-law calculation above does not validate that further inference step. \citep{v12_la_package_oci_agent,v12_la_2607_22443}

The correct translation response is therefore a revised analysis proposal: the original target is unresolved under the current information or diagnostics; a specified restricted-population target may be feasible; and the bank must assess whether that restricted target still informs its decision. In a public or generated prototype, this branch can be evaluated without bank data by stipulating both populations and checking that the system preserves their difference. It is not necessary to obtain expensive authentic evidence merely to detect a target substitution.

## Concrete package choices and the formal baseline

The inspected pywhy-llm path is a candidate for eliciting hypotheses and candidate variables. Its \texttt{IdentificationSuggester.suggest\_backdoor} delegates to a language-model confounder suggester. That class's front-door method is a stub, whereas \texttt{SimpleIdentificationSuggester} has a front-door method that generates text suggestions. Neither fact establishes a formal identification algorithm. The proposal should reuse the suggestion pattern selectively and send the resulting explicit graph and query to a separately admitted causal engine. It should preserve cited source passages and unresolved alternatives instead of interpreting a generated factor list as an approved adjustment set. \citep{v12_la_package_pywhy_llm}

For oci-agent, the useful candidate is the separation of a specification, a deterministic analysis notebook and a critic report. The selected source has a general notebook runner and a target-label issue requiring correction. A bounded banking interface should expose fixed reviewed operations with resource limits and typed outputs. The proposal does not adopt a general notebook executor as the causal MCP surface. Dependency resolution, failure handling and executable parity remain separate implementation tasks; the source's research status is not a reason to infer a deployed bank service. \citep{v12_la_package_oci_agent}

CausalDS is a candidate for generated scene and task design, but its grader needs a semantic review before direct adoption. The inspected identification/scoring helpers distinguish several genuine states, yet some missing metadata defaults and finite-interval checks require attention. Unknown identification due to a missing backend is not scientific nonidentification. A malformed answer is not a justified abstention. A capped score can conceal severe tail losses unless the uncapped losses and coverage are also reported. The proposal therefore takes the task separation and private-reference design while requiring explicit metadata and failure validation. \citep{v12_la_package_causalds}

The deterministic formulation baseline has three layers. A schema check verifies that population, unit, intervention, comparator, horizon, clock and scale are present. A semantic check compares these fields with the supplied brief and dictionary: a post-contact duration cannot become a pre-contact covariate, an invitation cannot silently become actual uptake, and a requested all-eligible effect cannot become a recipients-only effect. A formal check evaluates identification under the explicitly supplied candidate graph and returns an expression, model-relative nonidentification, unsupported scope or an unresolved input. These checks validate different things. A well-formed schema does not prove the story is true, and a correctly evaluated graph does not prove its edges.

For a generated benchmark, the reference can enumerate a finite set of admissible formulations \(\mathcal Q(b)\) for brief \(b\). An explicitly resolved brief may have one acceptable target. An ambiguous brief may have several and require the system to request or retain the missing distinction. A baseline can return those alternatives directly from the supplied reference fields and use exact calculations such as the example above. This establishes a transparent lower-cost comparator and exposes what a language model is expected to add: interpretation of unstructured language, evidence retrieval and useful clarification, rather than numerical work already handled by a deterministic engine.

## Evaluation before a costly bank study

The initial evaluation can use public data dictionaries and openly documented financial examples alongside generated causal mechanisms. Public data support questions about available variables and clocks; they usually do not supply intervention truth. Generated mechanisms can supply that truth for the declared model. A reference author should create matched examples that vary one decisive feature: invitation versus uptake, all eligible versus treated population, pre-decision versus post-decision measurement, complete variables versus noisy proxies, or a single action versus repeated treatment. The target-change example supplies one exact reference family. This is a proposed evaluation design; it is not a reported live-agent comparison.

Train/development and final evaluation should be split by the underlying scenario or structural model, not merely by paraphrases of the same question. Otherwise a system can learn the reference target from exposed near-duplicates. All requests should remain in the evaluation denominator, including ambiguous requests, timeouts, unsupported estimands, malformed answers and justified nonidentification. Report target and clock fidelity, unjustified resolution of ambiguity, false causal answers, valid abstention, numerical error where a target is actually identified, interval availability and coverage where ground truth permits them, and total resource use. A high completion rate alone rewards an agent for confidently answering questions that should remain unresolved.

Retrieval, structured prompting and an actor/critic loop should be compared against the same deterministic baseline and fixed task families. A retrieval ablation tests whether source passages improve interpretation. A critic ablation tests whether additional review catches errors, while reporting the added calls, time and newly introduced mistakes. A graph-perturbation comparison tests whether a system notices that an assumption changed. Repeated runs reveal stability. These studies need their actual model, tool, prompt, data and stopping-rule identities frozen before final evaluation. Agreement across repeated runs is useful evidence about stability; it is not evidence that the agreed answer is causally correct.

Several gaps remain scientific. A general method for recovering stakeholder intent from incomplete language is not established. The immediate remedy is to preserve admissible alternatives and make the missing decision explicit. A general guarantee that retrieval or debate validates causal edges is also absent; the current studies justify investigating those tools with factual and graph-specific references, not treating consensus as truth. Identification from noisy proxies, dependent observations or repeated interventions requires the corresponding statistical model and method. Finally, whether an assisted workflow saves bank analyst time or changes an investment decision requires a later workflow study after a bounded prototype shows merit. Those gaps narrow the claims and motivate specific experiments; they do not prevent writing or testing the proposal's public/generated formulation contract.
\label{exec13:formulation-end}
