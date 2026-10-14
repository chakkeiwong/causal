# E01 v2 engineering review

The earlier pass was premature: the pilot was materialized, workloads copied checks, computed contracts lacked bounds and recovery simulated a loop break. Those records remain historical.

Twelve equivalence checks cover small/large samples, low audit, near/exact rank, persistence and chunk sizes 1/37/257. Penalties, estimates, intervals and variance match within rtol 1e-9 and atol USD 1e-6. No-audit refusal and strict finite/disconnected/whole-line/unavailable consumer semantics pass.

Six isolated single-thread workloads include generation, tuning/refit, inference, serialization and whole-process RSS. The streaming fit is slower; whole-workload memory/time gains are not consistent because generation dominates peak memory. These no-gain findings remain evidence:

- dense T=240: total 0.0050s, fit 0.0027s, peak 104.00 MiB.
- stream T=240: total 0.0067s, fit 0.0042s, peak 104.00 MiB.
- dense T=12000: total 0.0972s, fit 0.0434s, peak 126.30 MiB.
- stream T=12000: total 0.1632s, fit 0.1065s, peak 132.75 MiB.
- dense T=120000: total 1.0809s, fit 0.4773s, peak 409.22 MiB.
- stream T=120000: total 1.7115s, fit 1.1242s, peak 408.46 MiB.

Actual abrupt exits during fit, partial checkpoint and final publication recover 12 records each, never publish a premature manifest, replay without duplicates and reject changed immutable input identities. This establishes local single-process integrity, not bank/platform acceptance or improved statistical calibration.
