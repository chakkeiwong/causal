# Compare discovery by its assumptions and returned object

A funding team wants the response of retained balances and net margin to an
offered rate. A directed picture learned from customer records is an
intermediate object. A discovery request must declare the observation unit,
clock, variables and scales, missingness and selection, admissible causal
models and whether the answer is a DAG, equivalence class or weighted
structural system. Repeated customer months do not become IID customers
because a matrix has one row per month. The comparison therefore separates
constraint, score, functional and continuous methods before comparing their
interfaces. \citep{exec13_pcalg,exec14_causallearn_reuse,exec13_java_tetrad}

Constraint methods use conditional-independence information under assumptions
that give it a graphical meaning. The selected Gaussian PC profiles in
causal-learn, pcalg and Tetrad require suitable CI tests, acyclicity, causal
sufficiency, faithfulness and no unmodeled selection. Their partially directed
graphs retain unresolved orientations. Alpha is the threshold of a named
test, not whole-graph confidence or effect coverage. Stable skeleton search
delays deletions within a conditioning level; conservative orientation is a
different rule. Neither justifies completing an ambiguous graph without
recording the additional assumption. \citep{exec13_pcalg,exec13_pydisc_causallearn,exec13_java_tetrad}

Score searches instead require a declared likelihood or score, search space,
penalty and optimization convention. Causal-learn GES exposes several scores;
Tetrad FGES uses the supplied score; native XGES uses its inspected Gaussian
residual-variance score. Their reported numbers cannot be ranked as one
universal fit statistic. XGES alpha weights a BIC penalty and defaults to two,
whereas ccdrAlgorithm alpha bounds edges relative to variables. The latter
returns a regularization path with MCP or L1 choices. A common argument called
alpha cannot preserve all these meanings. \citep{exec13_pydisc_causallearn,exec13_java_tetrad,exec13_cxx_xges,exec13_cxx_ccdr}

Functional identification adds restrictions on structural functions and
disturbances. The reviewed LiNGAM path depends on linearity, independent
non-Gaussian disturbances and its causal model; it cannot orient every
Gaussian observational equivalence class. NOTEARS and DAGMA expose continuous
optimization routes, but numerical acyclicity does not establish statistical
identification. In DAGMA, h_s(W)=-log det(sI-W elementwise-squared)+d log s
has its nonnegative DAG characterization inside the specified M-matrix
domain. A small helper residual outside that domain is insufficient. A
nonlinear first-layer norm is an unsigned adjacency measure, not an
intervention derivative. \citep{exec13_pydisc_lingam,exec13_pydisc_notears,exec16_dagma_primary,exec16_dagma_exact}

The implementation boundary adds failures that the mathematical target alone
does not describe. The selected DAGMA linear-module execution found in-place
centering, integer-input casting failure and a constraint branch that accepts
tuples but constructs rather than raises an error for lists. Short-budget
raw and thresholded outputs had different graphs, scores and acyclicity
residuals. These are bounded source/module findings, not a graph-recovery
study. A proposed wrapper needs copies and transformations recorded, hard
constraints verified, raw and returned objects distinguished, and retry
budgets enforced. Porting the algorithm would inherit these scientific
obligations while adding maintenance. \citep{exec16_dagma_primary,exec16_dagma_runtime}

## Matrix direction is part of a financial contract

For a stipulated funding system F=epsilon_F, R=4F+epsilon_R and
C=-F+R/2+epsilon_C, use row observations X=XW+E with W[source,target]. Then
W=[[0,4,-1],[0,0,1/2],[0,0,0]], and (I-W)^(-1) has first row [1,4,1].
Measuring F in percentage points and R,C in USD millions, a 0.25-point
intervention increases retention by USD 1 million and margin by USD 0.25
million. Transposing W while retaining the decoder gives zero forward
effect and invents reverse paths. Both matrices are acyclic, so a DAG test
alone misses the error. The exact rational replay checks structural paths
and the matrix convention against the integrated example.
\citep{exec13_pydisc_examples}

NOTEARS and DAGMA use the XW convention; the reviewed LiNGAM coefficient
matrix uses target rows. Causal-learn's endpoint pair (-1,1) denotes a
directed edge and (-1,-1) an undirected edge, not signed coefficients.
pcalg's selected CPDAG coercion and underlying graph accessor have different
orientation conventions, and its PAG uses a distinct endpoint scheme.
Node identity, edge marks, accessor and units must therefore travel with the
matrix. \citep{exec13_pydisc_notears,exec13_pydisc_dagma,exec13_pydisc_lingam,exec13_pydisc_causallearn,exec13_pcalg_reuse_primary}

## Ambiguity, selection and numerical failure change the decision

Three stipulated causally sufficient Gaussian models, a forward chain,
reverse chain and fork over (X,M,Y), have the identical covariance
[[1,1,1],[1,2,2],[1,2,3]]. Their X-to-Y total effects are 1,0,0. At USD 30
per outcome unit and USD 8 per action, the margins are 22,-8,-8. Equal
weights produce expected action value 2 only because those weights were
supplied; neither graph multiplicity nor an LLM vote estimates them. The
compatible effect values {0,1} describe this declared finite class, not a
sampling confidence interval. Maximin prefers declining, while other loss
criteria can choose differently. More observations of the same Gaussian law
cannot resolve the direction. \citep{exec16_s2_exact,exec13_pcalg_reuse_primary}

Faithfulness and selection have visible consequences. In X=U, M=X+V and
Y=(-1+epsilon)X+M+W with independent centered errors, the total effect and
Cov(X,Y) both equal epsilon. At zero they cancel despite two directed
paths; near zero statistical detection becomes difficult. Separately, let
X and U be independent fair bits, Y=U, and retain records only when X=U.
The retained observational contrast is one and the population intervention
contrast zero. A missing-row or selection policy belongs to the scientific
model, not just preprocessing. \citep{exec16_s2_exact}

The inspected Fisher-Z implementation uses sqrt(n-|S|-3) times the Fisher
transform of the partial correlation and can fail on singular correlation
submatrices. At correlation 0.1, treating 100 independent observations as
1,000 duplicated rows changes the unconditioned statistic from about 0.988
to 3.168 without new information. Replacing n alone is not a justified
dependence correction. \citep{exec13_pydisc_examples} Tetrad's selected wrapper catches singularity in
one path and returns dependence with p=0, whereas its result method propagates
the exception. A common interface should preserve unavailable numerical
tests separately from genuine rejection. \citep{exec13_pydisc_causallearn,exec13_java_tetrad}

## A defensible proposal selection

The current scoped routes favor causal-learn PC for Python and pcalg PC/IDA
for R, with locked environments and method-specific conversions still needed.
Java Tetrad supplies a substantive comparator; native aGrUM separates DAG,
PDAG and PAG entrypoints and its reviewed PC setup uses discrete tests and
rejects missing structure-learning data. OpenBNSL supplies a categorical
C++ route with its own CI conventions. These are different admissible
profiles, not interchangeable engines. Inference libraries such as libDAI
operate on supplied models and should not be counted as extra discovery
methods. \citep{exec14_causallearn_reuse,exec13_pcalg_reuse_primary,exec13_java_tetrad,exec13_cxx_agrum,exec13_cxx_openbnsl,exec13_cxx_inference}

The next matched trials should test exact graphs and endpoint conversions,
the funding reversal, ambiguous chains, dependent duplicates, selection,
singular inputs and constraint failures. Score, model and CI settings must
match before runtime comparisons; all failures stay in the denominator.
Selected-source coverage, distribution/dependency rights and native trial
qualification remain separate obligations. The exact financial constructions
use stipulated laws and costs. They establish neither bank benefit nor
commercial superiority, and the full software census remains open.
