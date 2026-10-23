# Require a policy evaluator to preserve the business decision

SCOPE-RL 0.2.1 is a useful reference for offline servicing-policy evaluation,
but its inspected source cannot yet be admitted as a banking safety evaluator.
Eleven authenticated files at the selected December 2023 revision expose the
episode layout, logging and target probabilities, fitted-value preparation,
interval helpers and policy-ranking contracts. The proposal retains this
profile as a reference. Full adoption and runtime integration remain deferred;
porting to another language has no demonstrated advantage sufficient to justify
replicating these contracts and their maintenance.
\citep{exec23_scope_rl_sources}

Even a small conversion error can change the investment decision. The default
high-level evaluator masks the reward on the done row itself. If the flag means
that the current transition just delivered a terminal receipt, rewards USD 2
and USD 8 become USD 2 instead of USD 10. At stipulated service cost USD 6, net
value becomes USD -4 instead of USD 4. A different flag convention may justify
the mask; the proposed adapter must define and test the actual clock. These
are exact authored examples, not measured package or banking results.
\citep{exec23_scope_rl_sources,exec23_scope_rl_reference}

The interval names also require source review. The Hoeffding-named expression
multiplies by sample size where its adjacent display divides by it, uses an
observed maximum rather than a declared population range, and can reverse its
bounds for negative constant scores. The Bernstein-named expression has a
different variance scaling from its display. The Student helper returns
symmetric endpoints using a one-sided quantile: under the exact normal-sample
pivot model, a 95-percent label corresponds to 90-percent central coverage.
The fixed-score bootstrap does not refit learned quantities or recompute a
self-normalized denominator. In an exact two-episode example, fixed-score and
recomputed-ratio bootstrap variances are 9/2 and 9/4. None of these witnesses
is an empirical coverage trial of the package.
\citep{exec23_scope_rl_sources,exec23_scope_rl_reference}

The selected lower-bound ranking path requires on-policy return arrays even
when metrics are omitted, which makes it a benchmark interface rather than a
ready logged-only banking service. Its selected calls do not adjust alpha
across candidate policies, and a lower-quartile helper needs an explicit
policy-name/value pairing repair. A public prototype should use finite known
trajectory laws, adverse terminal/reward conventions, support failures, signed
and degenerate returns, shared calendar shocks, and held-out policy selection.
It must preserve policy identity and refuse unsupported requests consistently
through the library, CLI and MCP interfaces.
\citep{exec23_scope_rl_sources,exec23_scope_rl_reference}

The required route is concrete: bind the complete release and actual dependency
versions and rights; review the time, interval and selection repairs; then run
registered native fixtures in that environment. The source license declaration
does not establish transitive clearance. Scientific logging truth, selected-policy
uncertainty, measured workflow cost and institutional adoption remain separate
obligations. The current paired reader has 994 audited citations and 232 genuine
scholarly PDFs. The reuse register has 43 passing proposal dispositions, three
inconclusive and 69 open entries; these counts do not grant native capabilities.
\citep{exec23_scope_rl_sources,sp23scope_reader,sp23scope_progress}
