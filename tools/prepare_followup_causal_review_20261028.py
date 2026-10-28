"""Prepare source-specific causal-survey and representation argument for review."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'followup-causal-review-v1';INPUT=DAY/'followup-identity-reconciliation-v1'
def main():
 assert not BASE.exists();BASE.mkdir()
 text=r'''§section[Causal tasks and representation interventions]{Causal tasks and representation interventions: what the evidence actually supports}
§label{sec:exec28-fr}
A causal assistant must preserve the distinction between answering a causal question and changing a language model.
The distinction is practical for a bank. An assistant might extract covariates from a scanned credit file,
propose a graph for a servicing decision, identify an admissible adjustment set, or estimate the effect of a payment reminder.
Better image descriptions can improve the first step without establishing the assumptions needed by the last three.
Conversely, a correct identification formula cannot repair an incorrectly extracted treatment date. Each part needs its own
target, observation contract, evidence and failure state.

§subsection{A task taxonomy that retains the information supplied}
Ma's selected September 2024 survey separates pairwise and full-graph discovery, effect estimation,
attribution, counterfactual reasoning and explanation. It discusses prompting, fine-tuning, combinations with conventional
causal algorithms, and knowledge or tool augmentation. This is useful as a taxonomy, rather than a new common benchmark.
The survey explicitly notes that the evaluations collected in its comparison tables can use different prompts and settings;
its dataset table also distinguishes pairs, relations, samples and questions as units. A percentage attached to one of these
units must not silently become a percentage of successfully completed banking analyses.§citep{exec28_fr_ma}

Consider a hypothetical collections analyst asking whether a reminder reduces thirty-day arrears. A pairwise query about
reminders and arrears may recover familiar domain associations. A graph task also needs eligibility, prior delinquency,
contactability, exposure opportunities and the decision clock. An effect task needs an intervention policy and a population;
a counterfactual question about one borrower requires more than the marginal average effect. These are different scientific
requests even if the interface presents each as a sentence. The proposed compiler should retain the supplied graph,
assumptions, empirical information and requested quantity as separate fields. A model that receives the correct graph and
potential-outcome table has solved a different problem from one asked to infer both from administrative records.

The survey's discussion identifies prompt sensitivity, memorized knowledge, inconsistent answers and scenario-dependent
rankings; it does not establish a universally best model. Its discussion of high-dimensional text also flags support problems.
For a longitudinal bank example, encoding all earlier messages does not by itself create treatment overlap at each history,
nor establish that every common cause was recorded before the action. Such omissions should produce a restricted answer,
an identified set or a refusal under the library's existing contracts. Additional prose from an agent does not supply the
missing observation law.§citep{exec28_fr_ma}

For public prototype evaluation, separate three modes: supplied-structure symbolic queries with known answers;
discovery under a declared generative model; and interpretation of genuinely observed documents with independently checked
labels. Keep the data-generating mechanism and test answers outside the evaluated agent's context. Record rejected,
unidentified, timed-out and malformed requests in the denominator. A public corpus can test extraction and workflow usability,
while generated outcomes test a stipulated causal target. Neither alone validates a bank's assignment mechanism.
This is a proposed evaluation design, not a claim that all these tests have been executed.

§subsection{Causality used inside a multimodal model}
Hu and colleagues' Causal-LLaVA preprint addresses object hallucination. It adds a projector module and a module in the
language model's final transformer block, using visual and textual dictionaries formed from category-averaged representations
of 5,000 instruction samples. Their proposed graph and approximate adjustment motivate the architecture; the reported
experiments evaluate image-language behavior. They do not evaluate identification of a servicing or lending effect.
The inspected version reports training on eight H20 GPUs and an additional dictionary-estimation cost of approximately
one hour. These are the authors' experimental conditions, not a measured cost for this proposal.§citep{exec28_fr_hu}

The source's tables support a qualified empirical comparison. Its LLaMA-2-7B comparison reports CHAIR sentence hallucination
33.0 versus 30.9 and recall 65.6 versus 65.9; these are distinct metrics. It also reports small regressions in particular
general-comprehension entries: the 13B ScienceQA entry changes from 65.1 to 65.0, and the Vicuna-v1.5-7B VizWiz entry
from 50.1 to 49.5. The blanket reading that every score improves is therefore unwarranted. The table does not by itself
establish significance, cross-bank transfer or an end-to-end error rate. The source's limitations mention computing demands
and confounder sensitivity across environments and datasets.§citep{exec28_fr_hu}

§subsection{Three mathematical distinctions behind the architecture}
Under an appropriate adjustment set and the usual identification conditions, the target is an arithmetic mixture
§[
 p(y§mid§operatorname{do}(x))=§sum_z p(y§mid x,z)p(z).
§]
Its weighting distribution is the target marginal, not automatically uniform. A uniform weighting is an additional target
choice. Nor does the formula license replacing the marginal with input-dependent attention weights without proving that the
result retains the same intervention meaning. The Causal-LLaVA appendix explicitly conditions dictionary weights on hidden
states to preserve representational capacity. That may be a useful predictive architecture, but predictive usefulness and
identification of the displayed intervention target require separate arguments.§citep{exec28_fr_hu,pearl2009}

The normalized weighted geometric mean is likewise distinct from the arithmetic mixture. Let the two conditional event
probabilities be §(1/10§) and §(9/10§), with target weights §(3/4,1/4§). The arithmetic probability is §(3/10§).
For a binary softmax representation, the corresponding logits are §(-§log9,§log9§); their weighted mean is
§(-§tfrac12§log9=-§log3§), whose logistic probability is §(1/4§). Thus even a linear logit map does not make the arithmetic
mixture equal to the normalized geometric approximation. The difference is §(1/20§), or five percentage points.
This finite construction tests a mathematical equality, not the authors' observed benchmark performance.§citep{exec28_fr_reference}

The same stipulated event law illustrates the importance of weights. Uniform weights give §(1/2§); input-conditioned
weight §(4/5§) on the high-risk category gives §(37/50§). If the event incurs a stipulated USD 1,000 loss, the four
calculations produce expected losses of USD 300, 250, 500 and 740, respectively. These amounts are exact consequences of
the example's assumptions. They are not bank forecasts, a superiority result, or evidence that a particular implementation
actually uses these example weights.§citep{exec28_fr_reference}

A second distinction concerns joint confounders. In general, marginalizing visual and textual confounders requires their
joint law, conditional or interventional as appropriate. Replacing that law by a product of marginals requires an independence
condition. If two Bernoulli variables are identical and each is one with probability §(1/2§), their joint-one probability is
§(1/2§), whereas multiplying the marginals gives §(1/4§). Equation (4) in the inspected source uses a product of conditional
marginals. The proposed product should require the corresponding independence premise or preserve the joint distribution;
the example establishes the consequence of omitting that premise, not a measured failure of the trained network.
Freezing an encoder also does not by itself prove that contextual common causes disappear from its representations.
That causal claim needs a model of the data and the frozen transformation.§citep{exec28_fr_hu,exec28_fr_reference}

§subsection{A bounded adoption decision and interface consequence}
The appropriate proposal disposition is to retain the architecture as a candidate measurement component and defer direct
adoption pending exact artifact, weight, data and dependency rights and a reproducible matched evaluation. The source provides
a repository lead; this review has not pinned or executed that repository. A low-cost first prototype should compare against
the existing extractor on a public or generated document set with separately adjudicated object labels, then assess how
extraction errors propagate into a fixed causal query. A successful vision score is neither an effect-identification certificate
nor a substitute for an uncertainty calculation.

CLI and MCP requests should therefore distinguish measurement improvement, model-mechanism intervention and a real-world
policy intervention. Return the target population, dictionary construction, weighting rule, approximation status, graph
assumptions and unavailable artifacts explicitly. Report a source-derived method as source-derived, a proposed adapter as
proposed, and an executed test with its exact code and data identities. For the banking analyst, the useful output is an
auditable answer whose scientific target survives every translation and approximation.
'''
 (BASE/'development.tex').write_text(text.replace('§',chr(92)))
 sponsor='''## Separate causal reasoning from model repair

The selected Ma survey organizes discovery, effects, counterfactuals and explanations while warning that collected evaluations use different prompts and task units. It supports a task-specific evaluation contract, not a universal model ranking. The selected Causal-LLaVA preprint improves several image-language scores, with some small regressions, and reports substantial training resources. These are source-reported findings about perception, not evidence of bank-effect identification. [@exec28_fr_ma; @exec28_fr_hu]

An exact authored example separates arithmetic adjustment from normalized geometric approximation and from changes in target weights. With a stipulated USD1,000 event loss, the resulting expected losses are USD300,250,500 and740. These are mathematical examples,not observed bank losses. The proposal retains Causal-LLaVA as a candidate measurement component,with native artifact,rights,matched evaluation and bank transfer still open. CLI/MCP must keep the measurement task,model intervention and business intervention distinct. [@exec28_fr_reference]
'''
 (BASE/'sponsor-addition.md').write_text(sponsor)
 refs=[ROOT/'tools/followup_causal_reference_20261028.py',Path(__file__),INPUT/'review.json',INPUT/'acquisition-plan-review.json',INPUT/'survey-followup-plan.json']
 evidence=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),anchor='Reviewed source/argument preparation') for p in refs]
 plan=dict(status='pass',scope='Two selected genuine originals,exact arithmetic examples and connected banking argument; preserve inherited1397records.',evidence=evidence,checks=['Ma survey used for its taxonomy and stated limits,not as primary support for every paper it cites.','Hu selectedv1methods,evaluation tables,limitations and appendix inspected; causal premises and approximate implementation distinguished.','Financial examples are explicitly stipulated and exactly reproducible.','Integrate two scholarly originals and one project reference; preserve269prior originals and1397records.','Journal/conference editions remain distinct; no visual,independent,native or final acceptance.'])
 (BASE/'plan-review.json').write_text(json.dumps(plan,indent=2)+chr(10));print('Prepared connected argument and exact review plan.')
if __name__=='__main__':main()
