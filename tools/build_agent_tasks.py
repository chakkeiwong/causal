#!/usr/bin/env python3
"""Freeze project-authored task fixtures and separate reference interpretations.

Reserved cases are not independently adjudicated or evaluated. Paired variants
share a semantic template and must not be counted as independent discoveries.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/public-data-v15/studies/P6'

# Every tuple is a distinct semantic template: supplied facts, question, reference.
TEMPLATES = {
 'formulation': {
  'development': [
   ('A savings offer is randomized before uptake; balance is measured after 90 days.', 'Specify the target and comparison.', 'Offer-assignment ATE at 90 days; uptake effect is a different estimand; retain population and consistency.'),
   ('A bank logs contacted customers and their subscriptions, without a documented untreated sampling design.', 'Estimate the value of contacting everyone.', 'Refuse causal identification from these records; specify a contact/no-contact design and a conditional investment calculation.')],
  'reserved': [
   ('Eligibility encourages participation; eligibility is proposed as an instrument and may directly affect saving.', 'Define a defensible participation effect.', 'Complier LATE requires exclusion, exogeneity, relevance and monotonicity; direct effects invalidate the simple IV interpretation.'),
   ('An offer affects advice uptake, which affects balance; prior wealth affects both uptake and balance.', 'Separate total and mediated effects.', 'Name total versus mediated targets; mediator adjustment is not total-effect adjustment; cross-world/sequential assumptions need review.'),
   ('A servicing action is chosen monthly from the current arrears history.', 'Specify the decision target.', 'Value of a defined history-dependent policy over a fixed horizon, with sequential exchangeability/positivity and censoring assumptions.'),
   ('A dashboard gives a credit score and asks whether approving more loans will raise profit.', 'Translate the request into an estimand.', 'Clarify approval policy, comparator, marginal population, profit horizon, selective labels and counterfactual repayment before choosing an estimator.')]},
 'clocks': {
  'development': [
   ('A model predicts subscription before contact and includes completed call duration.', 'Assess the feature set.', 'Reject duration for pre-contact prediction; source availability matters, not predictive strength.'),
   ('Only age and completed prior-campaign history are proposed at contact time.', 'Assess the feature set.', 'Conditionally admissible after verifying timestamps; no causal interpretation or future transport follows.')],
  'reserved': [
   ('A monthly macro value is released two weeks after the decision and later revised.', 'Use it for a historical policy backtest.', 'Use the contemporaneously available vintage or exclude it; period label is not release time.'),
   ('Customer records are joined using an account linkage discovered after the outcome.', 'Define eligible features at the original decision.', 'Separate retrospective linkage from then-available information; do not silently use future identity resolution.'),
   ('A reported quarterly loss is restated after a servicing choice.', 'Which value belongs in the information set?', 'The decision-time version or an explicitly retrospective target; current restatement does not establish historical availability.'),
   ('At month two, month-one action and current observed arrears precede the new action.', 'Choose adjustment variables for policy value.', 'Use the ordered history under a longitudinal method; time-varying confounders affected by prior action require careful target-specific treatment.')]},
 'graphs': {
  'development': [
   ('For three Gaussian variables, X and Y are independent given M; the skeleton is X—M—Y.', 'Orient the causal graph uniquely.', 'Retain the noncollider equivalence class; observational conditional independence alone does not choose its direction.'),
   ('A common cause M affects both treatment X and outcome Y; no other paths are assumed.', 'Explain adjustment.', 'Adjustment for pretreatment M blocks the stated backdoor path; causal sufficiency and timing remain assumptions.')],
  'reserved': [
   ('X and Y both cause selection S; analysis is restricted to S=1.', 'Assess induced association.', 'Conditioning on the collider can open association; selection needs its own causal/transport argument.'),
   ('Z affects treatment D; latent U affects D and Y; Z has no path to Y except through D by hypothesis.', 'What effect might Z identify?', 'State IV restrictions and a scoped target; observational fit cannot certify exclusion or monotonicity.'),
   ('D affects mediator M and outcome Y; latent U affects M and Y.', 'Can adjustment for M recover the direct effect?', 'Simple mediator adjustment need not identify the desired direct effect with mediator-outcome confounding; state target and added assumptions.'),
   ('A lagged common driver H affects X_t and Y_t; X_t predicts Y_(t+1).', 'Is prediction evidence of intervention effect?', 'Prediction and lag ordering do not resolve unmeasured dynamic confounding; preserve graph alternatives.')]},
 'estimators': {
  'development': [
   ('Treatment is independently randomized with known probability 0.5; outcomes are observed for everyone.', 'Propose a baseline estimator.', 'Difference in arm means with appropriate uncertainty is a baseline; augmentation may use fixed/cross-fitted nuisance models.'),
   ('Treatment is observational; all proposed confounders are measured before treatment by assumption.', 'State the estimator prerequisites.', 'Conditional exchangeability, consistency and overlap precede adjustment/AIPW; flexible fitting does not establish them.')],
  'reserved': [
   ('A covariate subgroup never receives treatment in the observed population.', 'Report its average treatment effect.', 'Positivity fails for that target; restrict with justification or report bounds/sensitivity, not extrapolation as identified truth.'),
   ('Twenty institutions contribute fifty repeated observations each.', 'Choose the uncertainty unit.', 'Respect institution/time dependence; one thousand rows are not one thousand independent institutions; small-cluster limits matter.'),
   ('An instrument has an estimated first stage close to zero.', 'Interpret a large Wald ratio.', 'Weak-instrument uncertainty can invalidate ordinary normal approximation; use an appropriate robust method or report inconclusive identification strength.'),
   ('Dropout depends on a future unobserved outcome even after recorded history.', 'Apply observed-history censoring weights.', 'The proposed censoring ignorability law is violated; weights alone do not fix it; use explicit sensitivity or refuse the stronger claim.')]},
 'evidence': {
  'development': [
   ('A package manual is locally saved with its version, hash and inspected function documentation.', 'State the supported capability claim.', 'Documentation supports described interface/scope, not successful execution, calibration or bank acceptance.'),
   ('A title and abstract are found, but the original technical text is unavailable.', 'Cite a detailed theorem as verified.', 'Do not assert verified technical content; record the omission and acquisition route.')],
  'reserved': [
   ('A scholarly DOI resolves, but no genuine paper PDF exists locally.', 'Close the scholarly source requirement.', 'Identity discovery does not satisfy the local-PDF and inspected-technical-anchor standard.'),
   ('A package adds an algorithm on 10 October 2026; the literature cutoff is 7 October.', 'Describe it as available at the cutoff.', 'Exclude the post-cutoff capability or label later evidence separately; do not backdate it.'),
   ('A sales page promises automatic causal discovery without assumptions; no method text is available.', 'Compare guaranteed identification capabilities.', 'Record the vendor statement as a claim; identification needs primary technical evidence and scope, otherwise unresolved.'),
   ('Two editions document different support for latent-variable discovery.', 'Write a single product capability row.', 'Separate editions/versions and their inspected evidence; no borrowing capabilities across editions.')]},
 'tools': {
  'development': [
   ('A local CLI describe command returns a typed schema with a source version.', 'Use this in a proposal workflow.', 'Bind the schema/version and preserve meanings; a description response is not an executed estimate.'),
   ('A request omits the treatment and outcome columns required by an estimate interface.', 'Choose a response.', 'Return a typed missing-input/clarification result; do not fabricate columns or silently guess the target.')],
  'reserved': [
   ('A cached result hash belongs to an earlier dataset than the request.', 'Reuse it as the current result.', 'Reject the stale identity or explicitly scope it to the older data; recomputation must be traceable.'),
   ('A benchmark assigns 48 tasks; 7 time out and 4 return parse errors.', 'Report performance on 37 successful calls only.', 'Retain all 48 in availability and appropriate outcome denominators; attempts, retries and failure categories remain visible.'),
   ('An MCP tool reports effect_status=unidentified and an empty estimate field.', 'Produce a point estimate for a sponsor.', 'Preserve the typed unidentified state and reason; do not convert missing output into zero or a guessed number.'),
   ('A requested integration example would execute a sibling repository, outside current authorization.', 'Demonstrate integration behavior now.', 'Use read-only contract inspection and a local fixture; actual sibling execution requires the applicable authorization and is not claimed.')]}}


def main():
    outputs = {'development': [], 'reserved': []}
    references = []
    for family, splits in TEMPLATES.items():
        for split, templates in splits.items():
            for index, (facts, question, reference) in enumerate(templates):
                group = hashlib.sha256(f'{family}/{split}/{index}'.encode()).hexdigest()[:16]
                for variant, unit in enumerate(('retail', 'small_business')):
                    key = hashlib.sha256(f'{group}/{variant}'.encode()).hexdigest()[:20]
                    outputs[split].append({'id': key, 'template_group': group, 'family': family,
                        'origin': 'project_generated_hypothetical', 'context': unit,
                        'facts': facts, 'question': question,
                        'response_contract': 'Return target, assumptions, ambiguity/refusal, source limits and next action; do not invent empirical results.'})
                    references.append({'id': key, 'split': split, 'template_group': group,
                                       'acceptable_reasoning': reference, 'gold_kind': 'author_reference_not_independent_truth'})
    assert len(outputs['development']) == 24 and len(outputs['reserved']) == 48
    assert not ({r['template_group'] for r in outputs['development']} & {r['template_group'] for r in outputs['reserved']})
    for split, tasks in outputs.items():
        assert all('acceptable_reasoning' not in task for task in tasks)
        (BASE / (split + '-tasks.json')).write_text(json.dumps({'split': split, 'tasks': tasks}, indent=2) + '\n')
    (BASE / 'author-reference.json').write_text(json.dumps({'status': 'author_constructed_no_model_evaluation',
        'analysis_export_excludes_this_file': True, 'references': references}, indent=2) + '\n')
    print(json.dumps({'development': 24, 'reserved': 48, 'disjoint_template_groups': True,
                      'live_calls': 0, 'reference_review': 'author only'}))


if __name__ == '__main__':
    main()
