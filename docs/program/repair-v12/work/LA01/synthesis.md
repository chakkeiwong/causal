# What language assistance contributes to a causal banking workflow

The inspected literature supports a division of work in which a language model
helps express a question, locate evidence and propose mechanisms, while an
explicit causal procedure determines what follows from the declared information
and assumptions. This is a design conclusion of this review, not a theorem that
all hybrid systems must fail. The sources include hybrids with favorable results
as well as systems that deliberately protect the inferential core from model
suggestions. Their differences should be exposed to the reader before choosing
an implementation.

All source identifiers below resolve to exact local copies, version dates,
physical PDF-page anchors and scoped claims in `source-audit.json`. The map uses
the 7 October 2026 cutoff. Twenty-six original PDFs are available, but only the
recorded method, evaluation and limitation passages have been inspected. No
collected code or model endpoint was executed for this review.

## From a request to a target

“Improve retention” leaves unresolved whether the bank wants the effect of an
offer, the effect of accepting it, the value of a sequence of offers, or a change
in profit after acquisition and servicing costs. The population may be all
eligible customers or current recipients. A horizon measured from eligibility
differs from one measured from acceptance. An assistant can expose these choices;
it cannot infer the institution's intended intervention or loss function from
fluent wording alone.

Kıcıman et al. (`v12_la_2305_00050`) offer a broad proof of concept for language
support in causal reasoning. CLadder (`v12_la_2312_04350`) supplies formal query
tasks, whereas CausalDS (`v12_la_2607_08093`) separates symbolic and numerical
tasks and the observation model. These are useful sources for a typed target
contract. They do not establish that the bank's natural-language request has a
uniquely correct causal interpretation. Alaa et al. (`v12_la_2407_19118`) discuss
medical causal copilots as a roadmap with illustrations. Its relevance is the
workflow argument, not evidence of a deployed longitudinal estimator.

The distinction has an immediate implementation consequence. Chou et al.'s OCI
workflow (`v12_la_2607_22443`) and its pinned notebook compute a uniform mean of
AIPW pseudo-outcomes after propensity trimming, calling it ATO. In conventional
overlap weighting the target population instead has density proportional to
e(x)(1-e(x)) times the original covariate density, where e(x) is the treatment
propensity. Trimming retains a subset; overlap weighting continuously changes
relative weights. Under heterogeneous effects these targets differ even with
perfectly known propensities. Our interface must carry the target rule and any
change to it, rather than let an agent silently relabel an estimate. Estimated
trimming also requires a separate treatment of selection and target uncertainty.

## Evidence, variables and diagrams

OntoLearner (`v12_la_2607_01977`) is relevant to terminology and semantic
relationships. Selby et al. (`v12_la_2402_07770`) examine quantitative knowledge
retrieval. Neither licenses a conversion of semantic similarity into a causal
arrow. A bank variable needs an operational definition, units, event time,
availability time and an observation mechanism. A customer income proxy and
latent repayment capacity must remain different nodes even if an assistant uses
the same colloquial label for both. The pinned ontology loader additionally
shows why a source-code revision alone does not pin downloaded data.

CausalChat (`v12_la_2410_14146`) demonstrates graph editing, confounder and
mediator suggestions, and visual comparison of model responses. Its six-person
nonexpert study reports fewer edge errors and shorter editing times in the final
visual stage. The stages are ordered, however, and participants choose different
remaining edges at each stage. Those results motivate an interface hypothesis;
they do not isolate a causal effect of that interface under matched randomized
conditions. The paper's own expert feedback raises absent citations. A score of
four on a prompted significance scale must therefore remain a model response,
not a probability that a proposed edge is scientifically correct.

Zhang et al.'s retrieval-assisted discovery (`v12_la_2402_15301`) provides both
positive and adverse evidence: documents improve selected settings but reduce
ASIA skeleton F1 from 1 to 0.73. Its orientation metric is conditional on recovered
true-positive edges, so it cannot be read as full-graph accuracy. ARGUS
(`v12_la_2609_30867`) audits reported identification evidence. That is useful
for distinguishing supported, contradicted and missing statements, provided
failed retrieval remains separate from missing scientific evidence. An auditor
cannot establish an assumption merely by finding a paper that states it.

## Competing discovery mechanisms

Breadth-first language discovery (`v12_la_2402_01207`) reduces the number of
model calls relative to pairwise querying. The size of prompts and responses
still affects cost, and rejecting a cycle proves only that the representation is
acyclic. Cohrs et al. (`v12_la_2406_07378`) use language answers in
constraint-based discovery. Their response-proportion calculations concern the
model's YES/NO distribution. They are not automatically conditional-independence
tests under the bank's sampling law. The pinned `causal_GPT` interface turns
those decisions into binary pseudo-p-values; it must not inherit a statistical
error-control claim from the surrounding PC procedure.

Darvariu et al. (`v12_la_2405_13551`) provide a different mechanism: a soft
language-derived graph prior combined with numerical evidence. Soft priors can
retain support for graphs that a mistaken hard constraint would delete. Selected
combined results improve, while standalone priors can harm performance. Ban et
al. (`v12_la_2306_16902`) and Takayama et al. (`v12_la_2402_01454`) offer further
hybrid constructions. Their mathematical and experimental roles must be compared
individually. A probability-shaped language score is not a calibrated graph
posterior simply because it enters a Bayesian-looking formula.

MAC (`v12_la_2407_15073`) distributes discovery roles among debating agents. Its
small canonical graphs and restrictions excluding hidden confounding and cycles
limit the conclusion. Agreement among agents is not independent corroboration
when models, training corpora or retrieved documents overlap. Feng et al.
(`v12_la_2407_19638`) inspect accessible pretraining corpora and report an
association between relation frequency and prediction success. This supports
testing contamination and unfamiliar labels. Their contextual examples also
remind us that context can change the valid causal claim: not every change in a
model answer is an error. A perturbation benchmark must fix or explicitly alter
the target world rather than assume all paraphrases are scientifically equivalent.

## Time, hidden states and experiments

Three different meanings of sequential analysis occur in these sources. Verma
et al. (`v12_la_2506_16234`) process successive observation batches and noisy
expert queries while retaining PAG information. This does not itself identify a
dynamic treatment regime. RealTCD (`v12_la_2404_14786`) initializes an unrolled
temporal graph from language and then optimizes a numerical score over graphs
and intervention targets. It assumes causal sufficiency and a known
observational regime. Its industrial evaluation uses expert location rules
because the full true graph is unavailable. A detected anomaly is not, without
additional evidence, an exogenous intervention on a bank process.

The Large Causal Model of Kougioulis et al. (`v12_la_2602_18662`) is an adjacent
numerical transformer, not an LLM wrapper. Its additive-noise, stationary,
lagged-only and causal-sufficiency assumptions are material. External weights
are not acquired here. It cannot be described as a solution to the project's
unresolved arbitrary latent temporal graph problem.

Lampinen et al. (`v12_la_2305_16183`) show how passive training on expert
demonstrations can support active causal strategies. New interventions occur at
evaluation time. The distinction matters: the learner receives information that
a bank analyst with only an observational log may not possess. These results
motivate experiment planning, not an assertion that passive text overcomes all
confounding.

Murphy's MDA (`v12_la_2608_09696`) proposes executable mechanisms with an LLM
and uses numerical fitting, approximate evidence and experimental design to
compare them. Its latent ODE/SDE studies are relevant to servicing-state models.
The paper explicitly limits its claim to finite held-out interventional
prediction, uses open-loop experiments, and does not claim causal identification
from those tests. Model-pool expansion and pruning leave uncertainty about
omitted mechanisms. The model-disagreement design surrogate approximates
information gain; it is not expected bank profit. Sample efficiency also differs
from total computational efficiency. These distinctions preserve the original
R03/R04 limitations instead of obscuring them with an agent interface.

## From an architecture to a qualified implementation

CausalAgent (`v12_la_2602_11527`), OCI and causal-learn+
(`v12_la_2606_23608`) instantiate different divisions between dialogue and
numerical tools. Zheng et al. argue for agent assistance around a protected
discovery core. This is a useful default architecture. Their preference does
not prove that a separately specified, validated hybrid is impossible. In every
case the bank needs to see which part is a model suggestion, which part is a
scientific assumption, and which part is an algorithm's conditional output.

Pinned source inspection changes the adoption decision. PyWhy-LLM's inspected
front-door routine is unimplemented. The CausalAgent OLC tool calls an unbound
function in its server module and catches failure as a JSON string. OCI's
general notebook runner has an unlimited notebook timeout. These findings
favor scoped adaptation behind the completed local operation contract rather
than direct runtime adoption. No downloaded implementation has been executed
or declared compatible in this review.

Benchmark code also needs review. CLadder includes an IV ratio in an ATE
template while marking a confounder unobserved. The inspected files do not by
themselves establish the extra assumptions needed to read that ratio as a
population ATE; those cells remain quarantined. CausalDS makes useful distinctions
between intentional abstention and malformed output, but selected grader
helpers default missing identification metadata toward identification. Its
interval summaries cap a normalized score. A local benchmark must retain
unknown identification, validate numerical endpoints, and report uncapped tail
losses in addition to any capped summary. None of these static findings is a
claim that an uninspected full application necessarily reaches the suspect
branch.

The map therefore permits the next design packages to proceed. It does not
complete the approximately one-hundred-page LLM repair, qualify a package, or
provide bank acceptance. Relevant uninspected candidates remain named in the
omissions register with acquisition routes. The targeted longitudinal and
off-policy searches that failed are recorded as failures, not evidence that no
relevant work exists. The next empirical task must measure scientific fidelity,
valid refusal, complete-request availability, effect loss and total cost with
independent oracles and registered failure denominators.

