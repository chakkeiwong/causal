# Identification must preserve the query and the reason for refusal

A lending query can ask for an average intervention effect, a conditional
intervention distribution, a retrospective counterfactual for one profile,
or the values compatible with incomplete information. These are different
objects. For an observed law P and admitted causal models M(P), the effect
set contains every target value produced by a compatible model. Point
identification means that all these values agree. An estimator's return
code, a chosen DAG or a narrow posterior cannot establish that agreement.
The product contract needs identified, nonidentified-with-witness,
unsupported, undefined and incomplete-search states.
\citep{exec18_pyid_contract,exec18_rid_causaleffect,exec18_rid_dosearch}

## Adjustment is one route within a larger problem

DAGitty and Julia CausalInference.jl supply useful graph and adjustment
operations. Allowed controls must exclude unobserved variables and preserve
baseline versus mediator timing. One valid empty adjustment set is different
from no returned sets. Julia's inspected do! graph mutation deletes incoming
edges; it does not evaluate an intervention probability. The reviewed pgmpy
candidate-set route needs independent total-effect validation, and its
advertised minimum-variance branch is unimplemented. An adjustment-search
failure cannot by itself certify that no other functional identifies the
query. \citep{exec19_otherid_dagitty,exec19_otherid_julia,exec13_pgmpy_reuse_primary}

Consider the positive binary structural law U~Bernoulli(1/2),
P(A=1|U)=1/4+U/2, P(M=1|A)=1/4+A/2 and
P(Y=1|M,U)=1/8+M/2+U/4, using independent structural randomizations.
Its graph is U->A, U->Y, A->M->Y. Direct intervention enumeration gives
risks 3/8 and 5/8, with effect 1/4. The observed contrast is 3/8.
The front-door expression sum_m P(m|a) sum_b P(Y=1|b,m)P(b) reproduces
the interventional risks. Ordinary standardization on M instead gives
contrast 1/8. At USD 100 per success and cost USD 20, the three proposed
values are 5,17.50,-7.50. The exact law checks the identifying expression
and shows why a missing observed back-door set is not global failure.
It is not a proof of every front-door implementation.
\citep{exec19_otherid_reference}

Python DoWhy separates specification, identification and estimation; its
reviewed method choices and returned assumptions need preservation. y0
offers symbolic ADMG identification, but its inspected conditional rule-2
separation path retains a known collider counterexample. The conditional
native route remains disabled. Identifying a joint law and normalizing
where its denominator is positive is a useful restricted route, but failure
of that joint problem does not prove failure of the conditional query.
Ananke's OneLineID offers district/fixing expressions, while its string
functional and Boolean result require a typed expression and status boundary.
Precondition errors in experimental variants must not be relabeled as
graphical nonidentification witnesses. \citep{exec13_dowhy,exec13_y0_id,exec13_y0_idc,exec13_y0_rule2,exec13_y0_separation,exec13_y0_oracles,exec18_pyid_one_line}

## Sound failures require the procedure's domain and completion status

R causaleffect supplies ID/IDC and selected extensions with output-dependent
error, false, empty-string and NULL nonidentification paths. dosearch searches
across supplied observational and experimental laws, with completeness
limited to its stated classes. Its pinned positive-time-limit path can
return without a separate timeout flag, so not-found after truncation must
remain unknown. Its missing-data extension is explicitly incomplete.
cfid supplies ID*/IDC* counterfactual conjunctions and defaults to an
interventional information level. Its undefined field, impossible conjunctions
and zero-probability conditioning events have meanings distinct from an
unidentified query. \citep{exec18_rid_causaleffect,exec18_rid_dosearch,exec18_rid_dosearch_paper,exec18_rid_cfid,exec18_rid_cfid_paper}

Native aGrUM separates symbolic expressions from numerical evaluation using
a supplied observational network. Its reviewed conditional graph surgery
and accumulated-kernel branches require proof-aligned native fixtures; those
source questions alone do not establish defects. Java Tetrad's selected
Identifiability object has its own observed-table subtype and evidence
semantics, maps one failure branch to probability -1 and uses distinct
exceptions elsewhere. Clamping that sentinel to zero invents a probability.
Its PDAG/IDA candidate failures can also become zeros or omitted entries,
so a list is not automatically exhaustive or a confidence set.
\citep{exec19_cxx_identification_source,exec19_javaid_source}

Commercial Bayes Server documents back-door/front-door criteria and separate
identification exports, supporting a concrete licensed comparator. Its
version-family history and later-acquired pages do not authenticate all
cutoff bytes or establish general ID/IDC completeness. Its abduction API
documents a step of the workflow but leaves multivariate posterior propagation
to be resolved for the selected route. Failure of one criterion is not
failure of every identification method, commercially or in open source.
\citep{exec14_ci_causal_query,exec14_ci_api_frontdoor,exec14_ci_release_history,exec14_ci_abduction,exec14_ci_api_abduction}

## Randomization does not reveal every individual counterfactual

Let randomized A and U be independent fair bits. Stable potential responses
(Y(0),Y(1))=(U,U) and switching responses (U,1-U) both yield uniform
observed (A,Y), marginal intervention risks 1/2 and ATE zero. Among factual
untreated failures, P(Y(1)=1|A=0,Y=0) is nevertheless zero in the stable
world and one in the switching world. The conditioning event has positive
probability. Exact enumeration verifies the distinction; additional
independent randomized observations of the same marginal experiment do not
reveal the within-person coupling. \citep{exec19_javaid_reference}

A second construction quantifies a sharp bound. Suppose randomized-arm
population risks are P(Y(0)=1)=1/4 and P(Y(1)=1)=3/4. For
t=P(Y(0)=1,Y(1)=1), response-type probabilities in order 00,01,10,11 are
(t,3/4-t,1/4-t,t), with 0<=t<=1/4. Every such distribution is attainable
under independent randomization. ATE is 1/2 throughout, but the necessity
fraction P(Y(0)=0|Y(1)=1)=1-4t/3 ranges sharply over [2/3,1]. Monotonicity
forces t=1/4 and the endpoint 2/3 as an added restriction.
\citep{exec18_rid_exact}

For retrospective accounting 1000*necessity-800 USD per treated responder,
the range is [-400/3,200]. This is not a prospective policy selected on an
unobserved future response. Two stipulated priors over t=0,1/8,1/4 retain
their weights under the equal arm-count likelihood and give posterior mean
necessity 5/6 versus 7/9. More concentrated posterior reporting can therefore
reflect supplied prior information along an unidentified direction. It is
neither a sharp identified set nor automatically repeated-sampling coverage.
\citep{exec18_rid_exact,exec18_rid_causalqueries}

Joint abduction is another separate requirement. With independent fair roots
U,V, observing their equality leaves each marginal fair but makes the roots
perfectly dependent. Replacing their posterior joint by the product of
posterior marginals changes the probability of equality from one to one-half.
The native aGrUM source's separate root-update construction motivates this
fixture; it does not prove a reproduced installed-runtime defect. Retain the
joint posterior or a justified factorization, return a set, or refuse.
\citep{exec19_cxx_identification_source,exec19_cxx_identification_reference}

causaloptim and bpbounds supply restricted response-function and binary-IV
bounding alternatives; their model classes and extra constraints must remain
explicit. A plug-in bound is not a confidence region. The proposed trials
should combine independent positive-law structural oracles, front-door and
conditional cancellation cases, impossible/undefined events, counterfactual
couplings, graph-class conversion and forced search interruption. Preserve
the formula, support conditions, information level, witness and failure
reason across library/CLI/MCP. Whole-census coverage, native qualification,
general counterfactual identification and bank acceptance remain open.
\citep{exec18_rid_causaloptim,exec18_rid_bpbounds}
