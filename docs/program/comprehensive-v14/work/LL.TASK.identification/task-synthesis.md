# LLM-assisted identification: preserving the question and the proof

The proposed assistant translates a banking decision into a candidate formal
question, retrieves and organizes assumptions, and requests a result from a
separate formal engine. Its own suggested adjustment variables, instruments or
mediators remain hypotheses. A proof that a particular expression identifies a
particular target is conditional on the submitted model; neither a persuasive
explanation nor repeated model agreement establishes the model's truth.

## What the primary literature supports

CLadder (Jin et al., inspected 2312.04350v3) supplies formal question generation
and verbalizations rather than commonsense answers alone. Its historical
reported CausalCoT gain is useful evidence for structured prompting, while the
paper retains language-to-formal formulation as a challenge. The inspected
repository revision and paper dataset version are distinct. A selected IV ratio
appears within an ATE template; the ratio cannot be promoted to an unrestricted
population ATE without the extra assumptions and per-item target being checked.

CounterBench (Chen et al., 2502.11008v1) supplies 1,000 balanced yes/no questions
from deterministic structural mechanisms. Its v1 title differs from the later
title in the inherited candidate register; this review uses the acquired v1
title. Table 3 reports GPT-4o accuracy of 52.5% with standard prompting, 78.8%
with CausalCoT and 92.0% with CoIn. The same table reports 51.8% versus 49.8%
for Davinci, so improvements are not universal. CoIn organizes extraction,
iterative reasoning and backtracking through instructions and examples. A
described reasoning algorithm is not automatically an executed proof checker.
The authors retain probabilistic mechanisms and hidden confounders as future
work. Nested and conditional templates need item-level semantic review before
becoming an independent answer key for our proposed product.

METER (Li et al., 2604.11502v1) aligns three linguistic question families across
4,145 contexts. It calls textual causal-relation extraction discovery; this is
different from graph identification from an observational probability law.
Intervention and counterfactual options are model-generated and then edited and
filtered by human annotators. Table 4 reports GPT-4o zero-shot accuracy of
87.92%, 77.96% and 67.42%, and lower CoT accuracy of 86.46%, 75.14% and 66.18%.
Its distractor categories and shared context design are relevant to faithful
translation. Curated semantic answer labels do not become a complete formal
identification oracle. These historical paper results are not current service
benchmarks or local replications.

Gendron et al. (2410.06392v1) separate graph extraction from counterfactual
mechanism evaluation and report that supplying the correct graph does not
eliminate reasoning failures. Their limitation that some real-world
counterfactual ground truth is proxied by model outputs prevents treating that
evaluation as independent causal truth.

CausalDS (Leban and Sun, 2607.08093v1) explicitly distinguishes population ATE
and counterfactual identification, conceptual variables and noisy observations,
public scene files and private truth. Its abstention and file-oriented design
are useful proposed components. Static inspection nevertheless shows that
false and unknown are not uniformly separated: missing target nodes return
false with input-error metadata; missing engines and exceptions can return
None; a negative DoWhy criterion result can survive an unavailable or failed y0
fallback. A consuming wrapper must preserve the reason and method scope. A
negative sufficient-criterion result is not itself a general impossibility
certificate. No upstream execution was performed here.

CausalSmith (Tan and Syrgkanis, 2607.22511v4) separates mechanical proof checks
from matching the formal statement to the intended claim. Its reported 144
runs include 14 accepted, 59 downgraded and 71 failed, with one acceptance among
94 identification/SCM runs. These are internal run outcomes, with reruns counted
separately. The paper explicitly lacks independent human validation of research
quality and an estimated statement-match error rate. A formally valid proof of
a changed statement remains the wrong answer to the original banking question.

## Package paths and reuse decisions

Seven selected PyWhyLLM blobs are verified against revision
66f2d59b0cf74dfabf0a83704bd1de708f8520ac. The public initializer imports the
suggestion classes. IdentificationSuggester delegates backdoor suggestions,
leaves its frontdoor method unimplemented, and has a commented estimand path.
SimpleIdentificationSuggester separately prompts for IV/backdoor/frontdoor names
and extracts tags. IdentifierProtocol declares methods; ValidationSuggester
adds prompted critique rather than a formal identification certificate. Selected
tests mock model responses and verify extracted lists. These are useful parser
tests, not live-model or scientific-validity tests.

Retain a small suggestion component only behind explicit candidate status,
variable allowlists, finite retry budgets, source provenance and graph/query
validation. Do not adopt a package-level scientific capability based on a class
name. Its decoded MIT root notice is already pinned; complete runtime and
dependency rights remain separate work. Reuse of CLadder and CausalDS should
retain their separate code/data notices and audit actual item/generator/scorer
semantics before an evaluation. Porting is not justified by this inspection.
CounterBench and METER are literature evidence now; dataset/code rights and
released-item audits are still open. Integration remains disabled.

## Exact banking target example

At time zero, an eligible servicing population is randomly encouraged with Z.
Actual servicing A is received by day seven and repayment Y is measured at
day thirty. Let one quarter always receive servicing, one quarter never
receive it and one half be compliers. Thus A(0),A(1) are (1,1), (0,0), and
(0,1). Assume independent encouragement, consistency, no interference,
exclusion, monotone take-up and binary repayment.

In world A, all strata have potential outcomes Y(0),Y(1)=(0,1). In world B,
always-takers have (1,1), never-takers (0,0), and compliers (0,1). Both worlds
have E[A|Z=0]=E[Y|Z=0]=1/4 and E[A|Z=1]=E[Y|Z=1]=3/4 and the same complete
joint law of (Z,A,Y). The encouragement ratio is 1 in both. The population
ATE is 1 in world A and 1/2 in world B.

Under the stated restrictions, only compliers change treatment with Z. The
first stage is their probability; the reduced form is that probability times
their effect, so the ratio identifies their effect, not the unobserved
potential outcomes of always-takers and never-takers. In this exact law,
their missing binary potential outcomes give a compatible population ATE
range [1/2,1]. Mixtures attain interior values. This is a constructed reference
with a fully specified model class, not a claim that every IV application has
this interval. The executable Fraction calculation enumerates both worlds.

With a stipulated USD 100 repayment benefit and USD 75 servicing cost per
borrower, treating the whole population rather than nobody has net value
between minus USD 25 and plus USD 25 per borrower. The complier calculation
alone gives plus USD 25. The latter cannot decide the population policy.
These are hypothetical treatment-policy payoffs, not the encouragement-policy
value, observed bank returns or a recommendation to force treatment.

## Proposed three-state contract

- Identified: a checked expression or result for the exact target, assumptions
  and supported model/query class, with a retained certificate.
- Not identified: a verified witness or an applicable complete-method
  certificate for that same class and target.
- Unknown: invalid inputs, missing assumptions, unsupported methods, absent
  engines, timeout, failed execution or an unverified negative criterion.

Execution status, scientific status and failure reason are separate fields.
Graph/query hashes, variable domains, observation law, target population,
assumption identities, engine version and certificate must travel with the
result. LLM prose cannot silently turn unknown into not identified, local into
population, or a proposed assumption into a fact. A formal result can remain
conditional while the banking owner considers whether its assumptions apply.

## Known route and remaining work

Build the smallest public/generated prototype that preserves these states.
Use independently enumerated finite mechanisms and checked expressions as
references; vary prose, names, latent structure, observation masks and targets
while holding the appropriate mathematical object fixed. Include malformed
queries and deliberate engine failures. Quarantine unsupported IV-as-ATE
labels rather than score them as truth. Keep private answer artifacts outside
the assistant's input. Report false identification, target substitutions,
invalid certificates, unknown reasons, availability and full computation and
review cost separately.

The engineering route is known. Representative business-to-formal error rates,
reliable detection of missing assumptions, robust general-purpose proof
translation and calibration on unrestricted causal models remain research
questions. Source audits cannot resolve those empirically. Dataset/generator
rights, complete engines and independent statement matching need further
inspection and a prototype. Bank truth and expensive institution-specific
experiments are later conditional work, justified by public/generated results.
The original omissions register and prior search failures remain intact; this
task resolves two candidates without claiming exhaustive frontier coverage.
