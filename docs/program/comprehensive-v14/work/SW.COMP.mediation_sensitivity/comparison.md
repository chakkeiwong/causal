# Compare mediation and sensitivity on the intervention they describe

A servicing offer may affect repayment through understanding, liquidity and
staff behavior. A decomposition of its total effect does not automatically
give the effect of an operational intervention on a dashboard score. The
request must name the treatment A, mediator M, outcome Y, baseline population,
measurement clock and intervention. Write mu_ab=E[Y(a,M(b))]. Natural means
with a!=b involve nested counterfactuals. A controlled mean holds a specified
mediator value fixed; a distributional intervention draws a specified mediator
law; a path-specific target requires an explicit graph and path set. Software
must not relabel one as another. \citep{exec20_med_stata_intro,exec20_med_reference}

## Native workflows have different targets and defaults

Stata's inspected one-mediator manual supplies natural and controlled effects,
potential-outcome means and model-specific combinations. It includes
treatment-mediator interaction by default. The additive total effect has
compatible decompositions (mu_10-mu_00)+(mu_11-mu_10) and
(mu_11-mu_01)+(mu_01-mu_00); mixing components across them need not add to
the total. Identification by the mediation integral needs the stated treatment
and mediator ignorability, support and absence of a treatment-induced
mediator-outcome confounder for that formulation. Convergence cannot supply
these premises. Supported outcome/mediator model combinations also constrain
what an adapter can accept. \citep{exec20_med_stata_one}

The distinct StataNow two-mediator profile covers parallel and ordered
mediators with specified continuous-variable models and interaction switches.
It does not discover the ordering or authenticate independent errors from a
business description. Stata's controlled-effect postestimation averages over
the covariate population by default; atmeans changes that target. Its proportion-
mediated command normally refuses conflicting effect signs, with a force
override that permits calculation without making the result a share of benefit.
\citep{exec20_med_stata_multiple,exec20_med_stata_post}

Mplus's selected chapter separates conventional coefficient products from
counterfactual effects. Categorical-variable paths can involve a latent-response
scale, which is not a repayment-risk difference. The counterfactual branch
describes pure direct, total indirect and total effects for a single mediator,
alongside controlled mediator values. MODEL INDIRECT defaults to delta-method
standard errors with documented alternatives and command-specific restrictions
including TYPE=RANDOM. Those restrictions do not establish absence in every
other Mplus route or later edition. The historical chapter's 2017 metadata
does not authenticate today's entitlement or cutoff bytes.
\citep{exec20_med_mplus_ch17}

For open-source sensitivity, the inspected sensemakr 0.1.6 documentation uses
partial R-squared quantities and observed-covariate benchmarks, with kd and ky
encoding user-supplied relative strengths. This is a regression sensitivity
contract; it does not identify natural effects or establish a mechanism merely
because the chosen benchmark looks plausible. HonestDiD's selected 0.2.8 source
addresses a different restriction: deviations from untreated parallel trends.
Its relative-magnitude and smoothness parameters have different units and
different zero cases. Such tools can coexist in a proposal, but their tuning
values, targets and covariance cannot be converted by name alone.
\citep{v12_sw_sensemakr,exec22_honestdid_engine,exec22_honestdid_reference}

## Exact banking examples separate attribution from feasible action

Let M(a)=2+3a+U and Y(a,m)=5+4a+2m+am+V, with independent mean-zero errors
in the stipulated causal model. The four mu values are 9,15,15,24 for
00,10,01,11. Total effect 15 decomposes as 6+9 or 9+6. Multiplying the
mediator slope 3 by the untreated outcome slope 2 yields the pure indirect
component 6, not the total indirect component 9. Controlled direct effects
are 4+m: 4,6,9 at m=0,2,5. A USD 10 cost for the complete offer gives total
margin 5; applying that cost to one channel needs a separately justified
component intervention. \citep{exec20_med_reference}

Now let A and U be independent fair bits and M(a)=a XOR U. In a direct world,
Y(a,m)=a; in a mediated world, Y(a,m)=m XOR U. Both observed laws have Y=A
and the same mediator overlap. The pure direct and total indirect components
are nevertheless (1,0) and (0,1). Randomizing the offer cannot remove hidden
mediator-outcome confounding. In the mediated world, setting M=1 versus M=0
has mean effect zero although the natural indirect component is one. With
USD 100 per outcome and USD 20 intervention cost, the complete offer margin
is 80 while that mediator-only contrast gives -20. Enumeration verifies the
observational equivalence and nested means; no vendor failure is asserted.
\citep{exec20_med_reference}

Population averaging also matters. For X equally likely -1 and 1 and a
controlled action effect 1/10+X^2/10, averaging gives 1/5 while evaluating at
E(X)=0 gives 1/10. USD 100 per response and USD 15 cost give margins 5 and
-5. In the separate inconsistent-mediation law M(a)=a and Y(a,m)=3a-2m,
total effect is 1 but the indirect component is -2 and its ratio to total
is -2. An interval or forced display cannot turn that ratio into a percentage
of positive benefit. \citep{exec20_med_reference}

## Sensitivity scenarios and statistical uncertainty are separate

For M=aA+u and Y=cA+bM+e, with A independent of errors, projection gives
b_OLS=b+rho sigma_e/sigma_u. At a=2, b_OLS=3, assumed structural scale ratio
2 and rho in [-1/2,1/2], the indirect effect ab ranges from 4 to 8. Under a
separately justified intervention valued at USD 100 per unit and costing
USD 500, arithmetic net ranges from -100 to 300. This is an assumed scenario
set, not a 95% interval, posterior or proven sharp identified set. The
structural error scale is not automatically the fitted regression-residual
scale. \citep{exec20_med_reference}

HonestDiD illustrates why even a sensitivity implementation needs covariance
and numerical contracts. With precontrast x=-2, postcontrast y=4 and reference
delta_0=0, relative magnitude |delta_1|<=m|x| gives [y-m|x|,y+m|x|], while
smoothness |delta_1+x|<=M gives [y+x-M,y+x+M]. Zero relative magnitude yields
4; zero smoothness yields 2. Estimated precontrasts must retain joint sampling
uncertainty. The exact Gaussian projection example with covariance
[[1,1.5],[1.5,4]], estimated x=0,y=4 and m=1 yields approximately
[-2.9233,10.9233], not the positive-only ordinary postcontrast interval.
This conservative reference is not the package's optimized estimator.
\citep{exec22_honestdid_reference}

The inspected engine's selected grid, hull and solver-status branches motivate
explicit checks for missed narrow sets, filled rejected gaps, boundary
acceptance and failed optima. A point interval returned after failed solves
must not be certified as identification. These are source and mathematical
findings needing native reproduction, not measured runtime failures.
\citep{exec22_honestdid_engine,exec22_honestdid_bridges}

The proposed public comparison should retain the four nested means, exact
decomposition, effect scale, interactions, target weights, resampling unit,
covariance, sensitivity parameter and unsupported states. Test the finite
worlds, nonlinear averaging, opposing signs and numerical failure cases before
any licensed trial. Negative controls need their own exclusion and confounding
structure; an assistant's label supplies neither. SAS CAUSALMED, IBM/AMOS,
PROCESS and wider open implementations remain source-specific obligations.
PROCESS's author page identifies an independent extension for multiple hosts,
not a native feature of each vendor or an inspected substitute for its book.
No port, live adapter, complete market survey, calibrated bank inference or
commercial superiority is established by this scoped comparison.
\citep{exec20_med_process_lead}
