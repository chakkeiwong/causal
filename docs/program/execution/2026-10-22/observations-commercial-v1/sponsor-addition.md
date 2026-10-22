# What commercial observation infrastructure can support

Customer matching, feature retrieval and storage history solve different parts of
the evidence problem. AWS Entity Resolution distinguishes matching rules, group
confidence and, for incremental ML, record confidence. IBM QualityStage documents
tunable linkage and specification review. Databricks provides historical feature
joins, but documents different lookback behavior for training/batch and online
inference. Snowflake provides retained storage states with edition, schema and
transaction-boundary limits. These are conditional integration candidates; the
proposal does not yet have qualified native adapters. Exact cutoff-era versions,
commercial terms and four other candidate families remain unresolved.
\cite{exec22_obs_aws_er_manual,exec22_obs_ibm_matching,exec22_obs_databricks_pit,exec22_obs_databricks_feature,exec22_obs_snowflake_time,exec22_obs_snowflake_at}

The commercial opportunity is to preserve the meaning needed for a causal
decision across these systems. A historical event timestamp does not establish
when information became usable. A match identifier does not independently verify
customer ownership. In an exact hypothetical example, two possible complete
linkage maps give contrasts +4 and -4. Giving the first map probability 0.8 yields
an averaged contrast 2.4. With USD 10 per outcome unit and USD 30 offer cost,
accepting the first map gives USD 10 margin, while the mixture gives USD -6.
The mixture probability and costs are stipulated, not vendor calibration or
measured banking returns. Another example changes the population effect from 4
to 5.2 merely by selecting which records remain linked.
\cite{exec22_obs_reference}

The next justified test uses generated customer histories with hidden identity
truth, late arrivals, false merges, excluded records and known treatment effects.
It should compare matched baselines and report linkage errors, future-information
violations, effect distortion and decision loss. Library, CLI and MCP must expose
the same provenance and refusals. This public route can establish prototype merit
before paying for commercial qualification or an experiment with private bank data.
