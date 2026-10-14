#!/usr/bin/env python3
"""Materialize reviewed proposal designs. This does not register or run final studies."""
import json
from pathlib import Path

import run_program as control

ROOT = control.core.ROOT
BASE = 'docs/program/public-data-v15/studies'


def ref(path, anchor):
    return control.bind(ROOT, path, anchor)


def save(path, value):
    full = ROOT / path
    if full.exists() and json.loads(full.read_text()) != value:
        raise ValueError('Preserve frozen design; use an explicit successor: ' + path)
    control.core.write(full, value)


def main():
    audit = control.core.read(ROOT, 'docs/program/public-data-v15/source-audit.json')
    selected = [r for r in audit['sources'] if r.get('id') in
                {'pd15_uci_bank', 'public401k', 'pd15_fdic_sod', 'pd15_fdic_api_spec', 'public_macrodata_dynamic',
                 'pd15_acic_pinned', 'pd15_nsw_docs', 'pd15_lalonde_pinned', 'pd15_febrl_source',
                 'pd15_cladder_pinned', 'pd15_corr2cause_pinned'}]
    selected.append({'id': 'p1_uci_names', 'kind': 'documentation',
        'source_identity': 'Unmodified bank-additional-names.txt member of the custodian UCI Bank Marketing archive',
        'version_date': 'Dataset 2014; archive retrieved 2026-10-12; historical cutoff bytes not established',
        'local_copy': ref('docs/datasets/public-v15/bank-marketing/bank-additional-names.txt', 'Sections 4 and 7'),
        'archive': ref('docs/literature/raw/pd15_uci_bank_archive.txt', 'Unmodified custodian ZIP'),
        'receipt': ref('docs/literature/raw/pd15_uci_bank_archive.receipt.json', 'Public acquisition receipt'),
        'inspected_anchors': ['Section 4: full file ordered May 2008–November 2010; smaller file is a 10% subsample',
                              'Section 7: duration unavailable before call; campaign includes last contact; pdays=999 means no prior contact',
                              'Section 7: macro indicators have different aggregation frequencies'],
        'supported_claims': ['Pre-call leakage rule, overlap exclusion and schema-specific sentinel handling'],
        'limits': 'No customer identifier, assignment law or release-time vintage is supplied by these passages.'})
    save(BASE + '/source-audit.json', {'date': '2026-10-12', 'cutoff': '2026-10-07', 'sources': selected,
        'project_designs': 'P3–P6 laws, metrics and acceptance choices are project proposals, not inherited empirical results.'})
    common = {'schema_version': 1, 'design_date': '2026-10-12',
        'status': 'frozen_author_design_not_final_study_registration',
        'scope': 'Proposal merit and bounded prototype design; no bank qualification',
        'source_audit': ref(BASE + '/source-audit.json', 'Primary source identities, limitations and inspected anchors'),
        'review_kind': 'author_review_not_independent',
        'final_study_gate': 'Implement and review exact code; bind data/code and protocol prospectively before final evaluation draws/calls. Preserve pilot exposure and failures.',
        'requires_bank_inputs': False, 'new_fitted_study': False, 'live_model_run': False}

    briefs = [
        {'id': 'P1.01', 'brief': 'What would 401(k) eligibility change in household net financial assets?',
         'request': {'dataset': '401k', 'target': 'eligibility_ate'}, 'expected_status': 'conditional_estimand',
         'graph_alternatives': ['X→eligibility→assets, X→assets; eligibility→participation→assets',
                                'Unmeasured preference U→eligibility and U→assets invalidates the sufficient-X adjustment claim'],
         'estimand': 'E[Y(Z=1)-Y(Z=0)] in the archived household population; Z=e401, Y=net_tfa',
         'identification': 'E_X{E[Y|Z=1,X]-E[Y|Z=0,X]} only under exchangeability, consistency and overlap; none proved by fit'},
        {'id': 'P1.02', 'brief': 'How much does participation change assets for households induced to participate by eligibility?',
         'request': {'dataset': '401k', 'target': 'participation_late'}, 'expected_status': 'conditional_iv_estimand',
         'graph_alternatives': ['X→Z,D,Y; Z→D→Y; U→D,Y is allowed by the conditional IV model',
                                'Direct Z→Y violates exclusion; common unmeasured causes of Z and Y violate instrument exogeneity'],
         'estimand': 'E[Y(1)-Y(0)|D(1)>D(0)] for eligibility compliers; D=p401, Z=e401',
         'identification': 'E_X[mu_Y(1,X)-mu_Y(0,X)] / E_X[mu_D(1,X)-mu_D(0,X)] under conditional IV assumptions and monotonicity; denominator must be nonzero',
         'alternatives': ['Participation ATE is a different target requiring backdoor assumptions', 'Report weak-first-stage and exclusion sensitivity or refuse numerical effect']},
        {'id': 'P1.03', 'brief': 'Should the bank contact customers rather than leave them uncontacted, using UCI subscriptions?',
         'request': {'dataset': 'uci_bank', 'target': 'contact_ate'}, 'expected_status': 'refuse_causal_identification',
         'graph_alternatives': ['Customer propensity→contact and subscription; contact→subscription is a hypothesis',
                                'Selection into the released archive and no documented untreated design leave the proposed contrast unidentified'],
         'estimand': 'E[Y(contact)-Y(no contact)] is a business target, not an identified archive estimand'},
        {'id': 'P1.04', 'brief': 'Score subscription before the call using age and completed call duration.',
         'request': {'dataset': 'uci_bank', 'target': 'pre_contact_prediction', 'features': ['age', 'duration']},
         'expected_status': 'refuse_features', 'reason': 'The source explicitly places duration after call initiation; remove it before considering a realistic predictive scope'},
        {'id': 'P1.05', 'brief': 'Describe a pre-contact predictive baseline using age, job and previous-campaign history.',
         'request': {'dataset': 'uci_bank', 'target': 'pre_contact_prediction', 'features': ['age', 'job', 'previous', 'poutcome']},
         'expected_status': 'conditional_prediction',
         'reason': 'Candidate clocks still need verification at deployment; current target is archive prediction, with no causal treatment or bank transport assertion'},
        {'id': 'P1.06', 'brief': 'How much will retirement saving help the bank?',
         'request': {'dataset': '401k', 'target': 'business_value'}, 'expected_status': 'clarify',
         'reason': 'Population, action, counterfactual, time horizon, outcome and bank value mapping are unspecified'},
        {'id': 'P1.07', 'brief': 'Would forcing longer calls increase subscription?',
         'request': {'dataset': 'uci_bank', 'target': 'duration_effect'}, 'expected_status': 'refuse_causal_identification',
         'reason': 'Duration is jointly determined during contact; an intervention and confounding/selection argument are missing'},
        {'id': 'P1.08', 'brief': 'Summarize duration and subscriptions after archived calls.',
         'request': {'dataset': 'uci_bank', 'target': 'post_call_description', 'features': ['duration', 'y']},
         'expected_status': 'descriptive_only', 'reason': 'A post-call description is meaningful; it does not justify pre-call decisions or interventions'}]
    save(BASE + '/P1/briefs.json', {'development_only': True, 'briefs': briefs})
    p1 = dict(common, operation_id='P1.DESIGN', title='Business formulation and information clocks',
        data=[ref('docs/literature/raw/t01_401k_data.txt', '9915-household Stata application extract'),
              ref('docs/datasets/public-v15/bank-marketing/bank-additional-full.csv', '41188 archived contact records'),
              ref('docs/studies/scope-public-spec.json', 'Inherited controls and estimand separation'),
              ref('docs/program/public-data-v15/bank-profile.json', 'Descriptive counts, missing categories and archive limitations')],
        task_briefs=ref(BASE + '/P1/briefs.json', 'Eight exposed development briefs and admissible alternative causal interpretations'),
        baseline=ref('tools/public_formulation_baseline.py', 'Normalized schema router; no free-text comprehension or effect fitting'),
        controls_401k=['age', 'inc', 'educ', 'fsize', 'marr', 'twoearn', 'db', 'pira', 'hown'],
        clock_policy={'401k': 'Cross-sectional controls are candidate adjustments; time ordering relative to eligibility must be assumed or externally established, not inferred from column names.',
                      'uci': 'duration and y unavailable before contact; campaign includes the last contact; contact/month/day and macro aggregates require an explicit decision/release clock; exclude by default.',
                      'sentinels': 'bank-additional pdays=999 differs from bank-full pdays=-1; never pool without schema-specific transformation.',
                      'sampling': 'Exclude smaller overlapping files from test data. Identical rows do not establish identical customers. Ordered rows are not exact calendar timestamps or independent customers.'},
        rubric={'critical_errors': ['Invented randomization or untreated support', 'Postdecision leakage', 'Participation ATE conflated with eligibility ATE or complier LATE',
                                    'One graph declared uniquely true without restrictions', 'Numerical bank value or causal certainty invented'],
                'dimensions': {'target_population_and_units': 2, 'decision_clock': 2, 'assumptions_and_graph_alternatives': 2,
                               'identification_or_explained_refusal': 2, 'sources_and_limits': 2},
                'scoring': '0 absent/wrong, 1 incomplete but correct, 2 complete for each dimension. Any critical error forces unsafe regardless of total. Useful clarification/refusal receives appropriate credit.',
                'denominator': 'All assigned tasks, including parse failure/refusal/API failure; route-specific scores and harmful false certainty reported separately.'},
        split_policy='These eight briefs and the inherited 401k data/results are exposed development material. No held-out score or prospective evaluation is claimed. Future variants require a frozen family split and independent review before execution.',
        remaining=['No live LLM has been tested', 'No new causal estimate is fitted', 'General natural-language parsing and bank semantic truth are unverified'])
    save(BASE + '/P1/design.json', p1)

    dictionary_rows = []
    for key, fields in [('px_fdic_sod_fields', ['CERT', 'YEAR', 'BRNUM', 'UNINUMBR', 'DEPSUMBR', 'STALPBR']),
                        ('px_fdic_financial_fields', ['CERT', 'REPDTE', 'ASSET', 'DEP'])]:
        acquisition = control.core.read(ROOT, 'docs/literature/raw/' + key + '.receipt.json')
        dictionary_rows.append({'id': key, 'kind': 'official_documentation', 'source_identity': acquisition['url'],
            'version_date': 'Current dictionary snapshot acquired ' + acquisition['accessed_utc'] + '; pre-cutoff bytes not established',
            'local_copy': ref(acquisition['path'], 'properties for ' + ', '.join(fields)),
            'receipt': ref('docs/literature/raw/' + key + '.receipt.json', 'HTTPS acquisition and exact hash'),
            'inspected_anchors': ['properties.' + f for f in fields],
            'supported_claims': ['Selected field identity, type and source mapping; CERT institution identity, REPDTE period end, branch-key candidates and deposits/assets labels'],
            'limits': 'SOD terse labels do not establish scaling, economic-perimeter continuity or historical-vintage immutability.'})
    save(BASE + '/P2/dictionary-audit.json', {'sources': dictionary_rows, 'cutoff': '2026-10-07',
        'observed_vintage_gap': 'Documentation describes historical periods but current exact bytes were acquired after the client cutoff; no pre-cutoff archive hash is established.'})
    p2 = dict(common, operation_id='P2.DESIGN', title='Funding, panel units and release vintages',
        inspected={'api': ref('docs/literature/raw/pd15_fdic_api_spec.txt', '/financials, /sod, response schema refs and fields/filter/paging definitions'),
                   'sod': ref('docs/program/public-data-v15/pd15_fdic_sod.txt', 'June 30 annual branch survey and May 29 2026 page update'),
                   'field_dictionaries': ref(BASE + '/P2/dictionary-audit.json', 'Inspected properties, units limits and unresolved historical vintage')},
        public_target='Descriptive deposit/asset trajectories of selected institutions and branch composition; no policy effect from observational covariance alone.',
        bounded_extract={'candidate_years': [2022, 2023, 2024, 2025], 'candidate_institution': 'CERT=14 as a documented API example, not a representative bank',
                         'financial_fields': ['CERT', 'REPDTE', 'ASSET', 'DEP'], 'sod_fields': ['CERT', 'YEAR', 'BRNUM', 'UNINUMBR', 'DEPSUMBR', 'STALPBR'],
                         'request_bounds': 'At most 10000 rows per request, 32 MiB total, no credentials; stop and report pagination/truncation rather than silently sample.',
                         'units': 'Do not assign dollars/thousands or sum SOD records until the selected dictionary confirms units and row granularity.',
                         'unit_continuity': 'CERT identifies a reported institution, not a guaranteed constant economic perimeter. Inspect mergers/conversions/branch transfers; retain entry/exit; do not interpolate across breaks or assume branch identifiers persist.',
                         'vintage': 'Observation years before cutoff do not prove a pre-cutoff release. The local API spec was acquired 2026-10-12. Freeze custodial archive/version and selected dictionary before any historical-vintage claim.'},
        unresolved_source_requirements=['Field names/types are now inspected; verify monetary scaling against selected reporting instructions before monetary use', 'Establish one archived release identity at/before 2026-10-07, or label a later snapshot as such',
                                        'Acquire institution history and selected branch key semantics before a constant-unit panel claim'],
        independent_local_route={'existing_macro': ref('docs/studies/dynamic-public-results.json', 'Preserved public macro local-projection study; not rerun here'),
            'generated_law': 'N=60 institutions, T=20 quarters; alpha_i~N(0,1), x_it=0.5*x_i,t-1+u_it, y_it=alpha_i+lambda_t+0.4*x_i,t-1+eps_it, iid u/eps with unit variance; lambda_t=0.2*sin(t/3). Set x_i0=0.',
            'clock': 'x at t-1 precedes y at t; common calendar retained. Baseline slope is known only in the declared generated law.',
            'stress': 'Corrupt five institution histories at a known midpoint; compare correct continuity map, naive merge and break-aware refusal. Add common shocks to test false iid covariance.',
            'comparators': 'Within-institution/time regression with institution-cluster covariance versus pooled OLS and naive iid covariance; no claim that cluster asymptotics are exact with 60 units.',
            'evaluation': '300 independent generated panels, development seed 15201 and reserved final seed 15291; report bias, availability, coverage MC interval, width and break-detection errors; register exact code first.'},
        review_disposition='Proposal design complete with generated primary route and a conditional FDIC extract contract. Field dictionaries inspected; historical bytes, scaling and unit histories remain explicit prerequisites of the optional FDIC empirical claim. No public extract or panel result is claimed.')
    save(BASE + '/P2/design.json', p2)

    p3 = dict(common, operation_id='P3.DESIGN', title='Known-truth effect estimation with matched information',
        observation_law={'unit': 'Independent generated person; no bank data', 'covariates': 'X1~N(0,1), X2~Bernoulli(0.5), independent',
            'assignment': 'A~Bernoulli(0.5), independent of X and potential outcomes',
            'potential_outcomes': 'Y(0)=200+40*X1+20*X2+50*epsilon; Y(1)=Y(0)+50+10*X1; epsilon~N(0,1)',
            'observed': 'Only X,A,Y(A) to estimators. Both potential outcomes belong to evaluator truth only.',
            'estimand': 'Superpopulation ATE=50 generated currency units; finite-sample mean treatment effect is separate.'},
        methods=['Difference in randomized arm means with unequal-variance standard error',
                 'Centered linear regression with treatment interactions and heteroskedastic covariance',
                 'Cross-fitted augmented IPW using known e=0.5 and fixed ridge nuisance fit; same folds and observed inputs for every implementation'],
        uncertainty='Asymptotic Wald intervals under iid requests; no exact finite-sample or arbitrary-learner calibration is asserted.',
        adverse_cases=['Observational e(X)=expit(0.6*X1+0.3*X2), compare correct propensity with false e=0.5',
                       'Weak support e(X)=clip(expit(3*X1),0.02,0.98); report instability and abstention',
                       'Outcome nuisance misspecification via an added 20*(X1^2-1); update evaluator truth explicitly'],
        budget={'n_per_replication': 1000, 'replications': 500, 'development_seed': 15301, 'reserved_final_seed': 15391,
                'stopping_rule': 'fixed_design_no_outcome_stopping', 'limits': 'One process, 4 GiB maximum, 30-minute cap per scenario; any cap event remains an unavailable request, never omitted.'},
        acceptance={'technical': 'All methods receive identical rows/splits; compare estimates and influence scores where mathematically identical; tolerances determined from numerical analysis before final registration.',
                    'scientific': 'Report bias/RMSE, unconditional all-request coverage, interval width, runtime and failures by scenario. Nominal coverage is not established merely because a binomial interval contains 0.95.',
                    'coverage_screen': 'For the declared randomized scenario, the 95% Wilson coverage interval must lie within [0.925,0.975] to support this bounded coverage screen; otherwise negative/inconclusive. This is a proposal choice, not a theorem.',
                    'availability': 'Unavailable/invalid intervals count as noncoverage; report availability separately. Stress failures do not silently narrow the denominator.'},
        optional_public_routes={'ACIC': 'Requires selected simulation grid, generated-truth metadata and reuse-rights inspection; no dependency on it for project-generated study.',
                                'NSW': 'Keep original randomized 445-row extract distinct from 614-row MatchIt treated/PSID comparison; inspect exact assignment and sample provenance before adoption.'},
        final_execution='Implement simulator and estimators, review algebra and pilot costs, freeze exact code and register a final-study successor before drawing reserved data.')
    save(BASE + '/P3/design.json', p3)

    p4 = dict(common, operation_id='P4.DESIGN', title='Controlled sequential servicing and censoring',
        history='Three decision times t=0,1,2. H_t=(X,L_0,A_0,...,L_t); X~N(0,1), L_0=0.4*X+epsilon_0. Previous action before t=0 is zero.',
        law={'action': 'A_t~Bernoulli(clip(expit(0.3*X-0.5*L_t+0.2*A_(t-1)),0.2,0.8))',
             'state': 'L_(t+1)=0.6*L_t+0.25*X-0.5*A_t+epsilon_(t+1), independent standard-normal innovations',
             'reward': 'R_t=10-2*L_(t+1)^2-A_t+0.5*A_t*X; total reward is sum over t=0..2',
             'observation': 'After action but before next state/reward, C_t~Bernoulli(0.65+0.30*expit(0.3*L_t-0.2*A_t)); dropout is absorbing in observed data. Latent full histories are evaluator-only.',
             'censoring_assumption': 'C independent of next innovation conditional on observed H_t,A_t by construction; stress depends on unobserved next innovation and deliberately violates this.'},
        estimand='V(pi)=E_pi[sum R_t] under interventions on actions, without conditioning on surviving observation; dropout is an observation process, not a treatment outcome.',
        comparators={'fixed_policies': ['Always zero', 'Treat when current L_t>0.5'],
                     'learned_policy': 'Select among thresholds {-0.5,0,0.5,1} by known-law IPW value on an independent training set; freeze selected threshold before evaluation.',
                     'estimators': ['Prefix importance weighting with exact behavior and censoring probabilities', 'Sequential regression/g-computation with fixed fitted model',
                                    'Complete-case unweighted comparison as an explicitly biased baseline'],
                     'weights': 'For R_t use product over s<=t of I(A_s=pi(H_s))/p(A_s|H_s) times I(C_s=1)/g(H_s,A_s). Prefixes differ by reward time.'},
        reference='Simulate 100000 independent complete trajectories per fixed candidate policy, with a separate reference seed; report reference Monte Carlo SE. This is a numerical reference with known law, not exact population truth.',
        budget={'training_n': 2000, 'evaluation_n': 1000, 'replications': 200, 'horizon': 3,
                'development_seed': 15401, 'reserved_final_seed': 15491, 'reference_seed': 15492,
                'stopping_rule': 'fixed_design_no_outcome_stopping', 'resource_limit': '4 GiB and 30 minutes per scenario; every timeout remains in denominator'},
        metrics=['Bias/RMSE and intervals for each frozen policy and paired value difference', 'Effective sample size and maximum prefix weight by t',
                 'All-request coverage and availability, with reference-MC uncertainty near interval boundaries labeled ambiguous', 'Regret relative to the finite candidate set, not the universal optimal policy'],
        adverse_cases=['Action propensities narrowed to [0.02,0.98]', 'Unobserved-future-dependent censoring', 'Misspecified state/reward regression'],
        decision_rule='Approve only the scoped method/regime that passes predeclared availability, useful-width and calibration criteria after code/pilot review; never generalize to hidden bank actions or arbitrary adaptive policies.',
        remaining='No final simulation or learned-policy result has been run. Optional mortgage records are not a prerequisite for this generated study.')
    save(BASE + '/P4/design.json', p4)

    p5 = dict(common, operation_id='P5.DESIGN', title='Graph ambiguity and observation linkage',
        graphs={'observational_law': 'Centered Gaussian (X,M,Y) with covariance [[1,.8,.48],[.8,1,.6],[.48,.6,1]]. Generate X=N1, M=.8X+.6N2, Y=.6M+.8N3 with independent standard normals.',
                'equivalence_class': ['X→M→Y', 'X←M→Y', 'X←M←Y'],
                'truth_boundary': 'Each DAG admits the same Gaussian distribution with appropriate equations; skeleton is X—M—Y without a collider. The data cannot uniquely orient it under these assumptions.',
                'effect_set': 'Total effect of do(X) on Y is {0,0.48} under these three sufficient linear DAGs; associational slope 0.48 is not a uniquely identified causal effect.',
                'intervention_case': 'Randomized external do(X=+1) versus do(X=-1) gives a 0.96 mean-Y contrast only under the first generating DAG. Keep intervention labels and observational samples distinct.',
                'metrics': ['Skeleton/adjacency accuracy', 'Coverage of admissible orientations/effect set', 'False singleton certainty', 'Effect-set width and availability'],
                'n': 2000, 'intervention_n_per_arm': 200},
        identity={'population': '1000 independent generated entities, X~Uniform[-1,1], A~Bernoulli(.5), epsilon~Uniform[-1,1]; Y=100+30*A+10*X+20*epsilon, ATE=30, outcome support [70,160].',
                  'tables': 'One table has generated names, dates and A,X; the second has corrupted identifiers and Y. Random IDs and order must not encode true cross-table identity.',
                  'corruptions': 'Rates 0,.1,.3 for missing/edited fields, collisions and duplicate candidates. Include independent errors, X-dependent missingness and outcome-dependent errors.',
                  'comparators': ['Truth join as evaluator-only upper-information benchmark', 'Exact join with explicit attrition', 'Fixed fuzzy match with abstention', 'Candidate-set sensitivity without forced singleton links'],
                  'metrics': ['True-link candidate inclusion', 'Wrong forced match and abstention rates', 'Effect bias, all-request interval/set coverage and width', 'Outcome-dependent selection failures'],
                  'partial_identification': 'Missing/ambiguous outcomes may use declared [70,160] support for worst-case sensitivity. Do not impute a unique match or infer missing-at-random from predictive fit.'},
        information_separation='Analysis exports exclude potential outcomes, true link keys and generating DAG orientation. Evaluator truth is stored separately; both exports have explicit column allowlists and disjoint paths. Future code review must test this separation.',
        budget={'replications': 200, 'development_seed': 15501, 'reserved_final_seed': 15591, 'stopping_rule': 'fixed_design_no_outcome_stopping',
                'limits': '4 GiB and 30 minutes per scenario with all failures retained'},
        decision_rule='Reward correct ambiguity and informed abstention. A forced singleton or leaked truth cannot pass through high average graph or matching accuracy. Final thresholds are fixed with the implementation protocol, not after final outcomes.',
        optional_public_inputs='FEBRL/CausalBench may add scoped evidence after rights/schema inspection; neither is bank identity truth or a dependency of generated work.')
    save(BASE + '/P5/design.json', p5)

    p6 = dict(common, operation_id='P6.DESIGN', title='Agent workflow tasks, baselines and ambiguity scoring',
        frozen_fixtures={'development': ref(BASE + '/P6/development-tasks.json', '24 project-authored hypothetical task variants'),
                         'reserved': ref(BASE + '/P6/reserved-tasks.json', '48 unevaluated variants; semantic template groups disjoint from development'),
                         'evaluator_only': ref(BASE + '/P6/author-reference.json', 'Author reference interpretations kept out of task export; not independently adjudicated'),
                         'builder': ref('tools/build_agent_tasks.py', 'Executed deterministic fixture construction; no live model calls')},
        task_families=['Business action→estimand and population', 'Clock/selection and feature availability', 'Alternative DAGs and effect-set queries',
                       'Estimator eligibility and diagnostic interpretation', 'Source/claim and negative-evidence tracing', 'CLI/MCP contract use with typed failure and resource limits'],
        provenance='Eight public-data P1 briefs are exposed development tasks. Project-generated graph/clock/schema cases are labeled synthetic. CLadder/Corr2Cause are source-audited leads, not verified uncontaminated held-out bank tasks.',
        split={'development': 'Four generated cases per family (24) plus eight exposed P1 briefs',
               'reserved_evaluation': 'Eight generated cases per family (48), disjoint semantic templates and graph topologies before surface paraphrases; freeze task manifests and rubric before any live call.',
               'seeds': {'development': 15601, 'reserved': 15691},
               'leakage': 'Split by template/topology and source family, never rows of paraphrases; forbid hidden truth in retrieval/context. Public benchmark training exposure remains unknown.',
               'languages': 'English first; other languages require explicit held-out strata rather than an unstated multilingual performance claim.'},
        baselines={'deterministic_schema': ref('tools/public_formulation_baseline.py', 'P1 subset only; unsupported tasks clarify/refuse'),
                   'static_template': 'Fixed question/assumption/source checklist, no model',
                   'retrieval_only': 'Return primary-source passages and their identities without generated causal claims',
                   'optional_live_arms': ['Model with frozen task only', 'Model with audited retrieval', 'Agent with typed tools and critique'],
                   'fairness': 'Identical assigned cases, sources allowed by arm, declared tools, total token/call budget and retry limits. Deterministic baseline is not advertised as understanding natural language.'},
        rubric={'critical_failures': ['Invented source or result', 'Unidentified causal effect reported as certain', 'Wrong population/clock/estimand', 'Hidden truth leakage', 'Unsafe or unbounded tool action'],
                'positive_dimensions': ['Correct target and assumptions', 'Admissible alternative graphs and uncertainty', 'Useful refusal/clarification', 'Traceable source/tool result', 'Reproducible next action'],
                'adjudication': 'Two human/independent reviewers are a future live-quality design option; current author rubric is not independent gold. Retain disagreements and acceptable alternative answers; assess inter-rater agreement on adjudicated cases.',
                'denominator': 'All 48 assigned cases per arm, including unavailable API calls, parse errors, abstentions and timeouts. Retries at most two; count attempts/cost separately and score case outcome once.',
                'analysis': 'Report per-family useful resolution, critical error, unjustified certainty, source validity, latency and cost; uncertainty clustered by case family/template. Do not count paraphrases as independent semantic tasks.'},
        offline_scope='Validate task/schema/router contracts and reference examples now. Offline checks make no claim about live-model accuracy, discovery performance or bank expertise.',
        live_prerequisites=['Named versioned backend with authorized credentials', 'Explicit money/token budget and current pricing identities',
                            'Frozen held-out manifest and retrieval corpus', 'Reviewed adjudication and agreed comparator budgets'],
        cost_design='At most 48 cases × 3 live arms × 3 attempts. Price token input/output, tool calls and reviewer time separately; no calls are made or costs asserted by this design.',
        fixture_limits='The current 72 fixtures are deterministic authored cases; the planned seeds apply to future random perturbations. Two context variants share each semantic template and are not independent tasks for uncertainty. References are exposed to the author and not independently adjudicated.',
        next_action='Review frozen reference interpretations and generated export separation; select and prospectively register a bounded optional live comparison only if its expected information justifies cost.')
    save(BASE + '/P6/design.json', p6)
    print(json.dumps({'designs_written': 6, 'development_briefs': len(briefs), 'new_final_studies': 0, 'live_calls': 0}))


if __name__ == '__main__':
    main()
