"""Inspected primary spans for the bounded Bayesian/state comparison."""
ANCHORS = {
    'stan': [
        ('src01',1,14,'BSD 3-Clause','Selected BSD3 declaration; complete dependency rights separate.'),
        ('src02',14,27,'STAN_MINOR 40','Pinned source declares Stan2.40.0; not proof of a distributed stable artifact.'),
        ('src03',69,111,'error_codes::OK','Selected adaptive diagonal NUTS service separates configuration and propagated software exceptions, then returns OK.'),
        ('src08',57,90,'Exception initializing step size.','Helper catches step-size initialization exception, logs and returns void before draws; outer service return alone is insufficient.'),
        ('src08',87,102,'disengage_adaptation','Warmup and sampling phases separate; adapted state and timing have writer channels.'),
        ('src04',150,157,'Posterior is improper','Step-size search contains explicit improper-posterior and zero-step-size exception branches.'),
        ('src11',114,170,'num_path_successes','Non-PSIS path returns OK with some successful paths and warning; all failures return software error.'),
        ('src12',17,58,'test_gradients','Diagnose compares local automatic gradients with finite differences; it is not a global posterior or causal audit.'),
    ],
    'rstan': [
        ('src01',1,12,'GNU','Original RStan license text; component-specific rights.'),
        ('src02',1,53,'GPL (>=3)','Pinned RStan development version2.39.0.9000 and GPL>=3; runtime and linking dependencies separate.'),
        ('src09',37,46,'BSD_3_clause','StanHeaders metadata has distinct BSD3 declaration and build dependencies.'),
        ('src03',18,56,'else return(0)','Automatic warnings skip Fixed_param; unavailable divergence/depth columns contribute zero to warning counts.'),
        ('src03',57,94,'get_num_upars','Automatic energy warning uses parameter-count/sample-energy-variance; Rhat and ESS thresholds are selected implementation conventions.'),
        ('src03',227,246,'sum(diff(x) ^ 2)','Explicit BFMI helper uses successive squared increments divided by sample variance; differs from automatic-warning formula.'),
    ],
    'nimble': [
        ('src01',1,27,'Redistribution','Selected BSD-style root declaration; package holder notice and dependencies separately retained.'),
        ('src02',1,20,'Version: 1.4.4','Pinned package identity; description is not evidence that every advertised algorithm was inspected.'),
        ('src05',160,187,'non-data stochastic','Configuration distinguishes sampled nodes, monitors, conjugacy and scalar/block choices.'),
        ('src05',314,355,'downstreamNoSelfIDs','Posterior-predictive grouping depends on all downstream nodes being eligible for sampling.'),
        ('src05',434,450,'partially observed','Selected default multivariate assignment handles mixed data via partial_mvn for dmnorm and refuses other cases in this branch.'),
        ('src07',79,97,'model$simulate','Posterior-predictive sampler simulates downstream nodes, updates log probabilities and saved state.'),
        ('src06',47,59,'previous chain ended','Without inits subsequent chains start from previous chain endpoint; runMCMC does not expose reset=FALSE continuation.'),
        ('src06',132,155,'set.seed','Per-chain RNG and optional initialization are explicit; WAIC accumulation has separate reset policy.'),
        ('src08',138,167,'Halting','Posterior-predictive reordering can refuse custom order; mixed predictive/nonpredictive blocks have option-dependent restriction.'),
        ('src08',270,325,'resetMV','Low-level continuation retains adaptation and optional draws; first-run reset, burn-in refusal and partial-thinning warnings are explicit.'),
    ],
    'keanu': [
        ('src01',1,19,'MIT License','Selected historical MIT declaration; installed JVM and numerical dependencies unqualified.'),
        ('src04',127,165,'calculateLogProbFor','Latent excludes observed; joint probability includes latent and observed vertices.'),
        ('src10',108,116,'!state.isObserved','setValue does not replace an already observed value.'),
        ('src10',188,223,'new VertexState','observe changes value/observation status; selected method does not cut incoming factors; numeric deterministic observation is restricted.'),
        ('src12',9,37,'logProbAtValue','Probability aggregation retains probabilistic vertex contributions; impossible helper treats negative infinity and NaN explicitly.'),
        ('src05',78,85,'PriorProposalDistribution','Default MH proposal is prior-based with single-variable selection; adapter must retain kernel identity.'),
        ('src06',98,145,'getContinuousLatentVariables','Selected NUTS setup takes continuous latent variables and requires a supported gradient model and viable starting probability.'),
        ('src06',153,165,'saveStatistics = false','NUTS defaults include1000adaptation steps and optional general statistics disabled.'),
        ('src08',23,24,'dropCount = 0','Generator defaults to zero initial dropping and thinning interval one.'),
        ('src08',81,112,'i % downSampleInterval','Generator counts total transitions before dropping and retains positions0,k,2k; nondivisible remainder gives ceiling retained count.'),
        ('src13',151,171,'stepCount > adaptCount','General statistics optional; divergence after adaptation has separate logging/storage branch, not controlled solely by saveStatistics.'),
    ],
    'turing': [
        ('src02',1,8,'MIT License','Selected MIT declaration; full numerical dependency custody remains open.'),
        ('src01',1,83,'0.49.0','Pinned source version0.49.0,Julia1.10.8compatibility and separate DynamicPPL/AdvancedHMC/AbstractMCMC dependencies.'),
        ('src04',1,21,'InitFromPrior','Default initialization draws from prior; discrete-support check is sampler-specific.'),
        ('src05',88,160,'nadapts=0','Fresh adaptive chains resolve warmup/drop defaults; supplied initial state uses zero additional adaptation and zero initial dropping.'),
        ('src06',659,683,'irreducibility','Selected documentation warns that changing disjoint supports between Gibbs blocks can prevent movement despite conditional invariance.'),
        ('src06',1039,1078,'did not report a value','Variable-set checks track appearance/disappearance and omitted reported values; support changes are a distinct issue.'),
        ('src07',211,245,'rand(rng','Analytical conditional sampler draws from supplied distributions and refuses use outside Gibbs.'),
        ('src07',256,278,'get_cond_dists','Conditional distributions are supplied by user callback; schema compatibility alone cannot prove conditional-law correctness.'),
        ('src08',5,47,'threadsafe','Particle execution advances at likelihood statements; selected path refuses models needing threadsafe evaluation.'),
        ('src08',439,479,'≤','ESS resampling threshold uses less-than-or-equal predicate; normalized weight ESS differs from MCMC ESS and genealogy.'),
        ('src08',574,610,'isfinite(total)','Particle sweep refuses nonfinite total weight, accumulates log-normalizer ratios and retains per-step ESS on selected path.'),
    ],
}

REUSE = {
    'R': ['exec24_bnlearn_sources','exec24_bnlearn_contract','exec25_cdyn_bssm','exec25_cdyn_choice'],
    'Python': ['exec23_pymc_sources','exec23_pymc_reference','exec23_numpyro_sources','exec23_numpyro_reference','exec19_dynamax_source','exec19_dynamax_reference','exec25_pydyn_pydlm','exec25_pydyn_choice'],
    'Java': ['exec25_jdyn_tetrad','exec25_jdyn_jdplus','exec25_jdyn_choice','exec24_smile_choice'],
    'Cxx': ['exec24_libdai_source','exec24_libdai_choice','exec24_opengm_source','exec24_opengm_choice','exec25_cdyn_bssm','exec25_cdyn_bsvars','exec25_cdyn_choice'],
    'other_relevant': ['exec25_odyn_ssm','exec25_odyn_gretl','exec25_odyn_choice'],
}

NEW_GROUPS = {'R':['rstan','nimble','stan'],'Python':[], 'Java':['keanu'], 'Cxx':['stan'], 'other_relevant':['turing']}
