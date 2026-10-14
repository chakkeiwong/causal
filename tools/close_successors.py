from pathlib import Path
import master_control as mc
ROOT=mc.ROOT

def ref(path,anchor):return dict(path=str(path),sha256=mc.sha(ROOT/path),anchor=anchor)
def close(ident,version,outcome,verdicts,findings,dispositions,review):
 s=mc.read(ROOT,mc.STATE);task=mc.task_by_id(s,ident);p=Path('docs/program/master/work')/(ident+'-'+version)
 (ROOT/p/'review.md').write_text(review)
 evidence=[ref(Path(x),'Full corrected evidence') for x in task['outputs']]
 receipt=dict(task_id=ident,task_contract_sha256=mc.digest_object(task),outcome=outcome,reviewer=dict(name='Executing research agent; integration review',kind='author'),scope='Versioned corrected local execution; earlier errors retained and superseded.',limitations=['No independent scientific acceptance or authentic bank validation.','No general finite guarantee or supplied bank economic threshold.'],gap_dispositions=dispositions,criteria=[dict(id=c['id'],verdict=v,finding=f,evidence=evidence) for c,v,f in zip(task['criteria'],verdicts,findings)])
 if task['kind']=='research':
  result=mc.read(ROOT,str(p/'results.json'));launch=result['launch'];reg=s['registrations'][ident]
  journal=dict(task_id=ident,requests=result['requests'],registration_sha256=reg['sha256'],started_at=launch['started_at'],retained_failures=True,request_sha256=result['request_sha256'])
  mc.write(ROOT/p/'journal.json',journal)
  receipt['experiment']=dict(registration_sha256=reg['sha256'],started_at=launch['started_at'],journal=ref(p/'journal.json','Every immutable request hash and launch'),retained_failures=True)
 else:
  files=['src/causalbank/engineering_v2.py','tools/master_e01_v2.py','src/causalbank/linked_funding.py','src/causalbank/streaming_pilot.py','src/causalbank/funding_calibration.py','src/causalbank/linkage_sets.py','src/causalbank/dynamic_funding.py','docs/studies/dynamic-funding-spec.json','docs/studies/dynamic-observation-spec.json']
  receipt['input_sha256']={f:mc.sha(ROOT/f) for f in files}
 mc.write(ROOT/p/'receipt.json',receipt)

close('R04','v3','negative',['pass','inconclusive','fail','pass'],
 ['The true candidate lag yields iid innovations; covariance inclusion retains its finite graph and effect in a union over all lags.','Symbolic covariance/IV oracle and equal-law witnesses checked; full floating-point certification remains limited.','All valid cells cover and retain graph 512/512, but weak relevance and observational latent cells have zero finite sets and fail availability.','Equal-law witnesses require extra exclusion or intervention information; arbitrary temporal graphs remain open.'],
 dict(D03='conditional_progress',D04='unresolved',D09='conditional_progress'),'''# R04 v3 final review

Both serialization and the statistical experiment were repaired. A fresh 4,096-request study completed. The scalar-lag model uses invariant initialization and a union over supplied lag values {0,.4,.8}; it does not treat fitted selected residuals as iid. Covariance inclusion at the true lag retains its graph and effect.

All valid cells cover and retain the true graph 512/512. Strong encouragement has 512 finite sets, median width 3.9301 outcome/action units. Weak relevance and observational latent cells each give 512 whole-line sets. Persistence gives 507 finite and 5 whole-line sets. Finite availability therefore fails despite conservative coverage. The work is partial progress, not arbitrary graph or useful precision qualification.

False exclusion retains the true graph 0/512, although broad effect intervals cover all 512. Numerical coverage cannot validate false restrictions. Hidden-history and selection fields match graph labels, not membership of those invalid observation laws. Disconnected JSON sets are checked in fixtures even though the final union yields no disconnected sets in this grid. Exact symbolic formulas are checked; no global floating-point interval certificate is supplied.

Continuation requires stronger authentic relevance or additional experiments/measurements excluding equal-law alternatives. Unknown continuous lag and richer latent graph laws require a new observed-law confidence argument. Prior serializer failures are resolved and are no longer external blockers.
''')
s=mc.read(ROOT,'docs/program/master/work/R05-v2/results.json')
review='''# R05 v2 final review

The first attempt was invalid for its claimed argument: evaluation outcomes selected penalties, standardization used all data, covariance crossed the omitted gap, and scenario dimension overrides were ignored. Its requests remain exploratory and immutable. This successor repairs all four, uses a fresh seed and actual training-only nested selection. Independent convex optimization, soft-threshold and dense covariance fixtures pass.

The frozen 99% intervals are wider than the original 95% ones; comparisons across attempts do not isolate a correction effect.

'''
for c in s['cells']:
 m=c['methods']['nested_sparse'];review+=f"- {c['design']['name']}: {m['covered']}/512, lower {m['simultaneous_lower95']:.6f}, finite {m['finite']}, median width {m['width_quantiles'][1]:.6f}.\n"
review+='''
High dimension and larger support fail the simultaneous .95 minimum screen. This means the frozen rule did not qualify these cells; it does not establish a universal defect. Nonlinear misspecification gives 0/512 coverage. Weak-IV intervals are wide, and a tiny-denominator guard is not a strong-IV test.

Next research: independent-pilot separation, restricted-eigenvalue/growing-dimension rates, weak-IV test inversion and richer prespecified nonlinear nuisance bases. New arguments need new protocols; no saved seeds or critical values are changed. Arbitrary learners and bank precision remain unqualified.
'''
close('R05','v2','negative',['pass','pass','fail','pass'],
 ['Actual nested training, gap and within-fold Bartlett procedure now matches the fixed-dimensional rate argument; growing dimension remains conditional.','Independent convex solver, exact soft-threshold boundary and separate dense covariance calculation agree.','High-dimensional and larger-support valid cells fail the frozen .95 lower-bound rule; nonlinear/weak-IV failures remain visible.','Fixed correct linear nuisance/mixing conditions attach to outputs; no arbitrary-learner guarantee.'],dict(D06='conditional_progress',D09='unresolved'),review)
p=ROOT/'docs/program/master/work/E01-v2'
(p/'contract.md').write_text('''# Shared results, full linked streaming and recovery

A-D outputs bind actual set pieces or an unavailable reason, scientific assumptions, units and capability disposition. Computed sets without bounds and malformed/overlapping pieces are rejected. Null endpoints denote extended-real bounds.

Both chronological pilot halves are reduced into augmented QR factors with online target moments; validation losses and full refit preserve the existing objective. All linked pseudo-outcomes are constructed in bounded chunks, including pilot and evaluation. Source histories can be memory-mapped; whole-process memory in the measured workloads includes full in-memory data generation and is not O(chunk).

Recovery locks one request directory, binds dependency hashes/seed/count, fsyncs pending data, atomically renames complete records, fsyncs the directory and publishes a hash manifest after all records exist. Real subprocess exits cover fit, partial checkpoint and publication boundaries. Replay validates identities and rejects altered inputs. No multi-host or bank SLA claim.
''')
review='''# E01 v2 engineering review

The earlier pass was premature: the pilot was materialized, workloads copied checks, computed contracts lacked bounds and recovery simulated a loop break. Those records remain historical.

Twelve equivalence checks cover small/large samples, low audit, near/exact rank, persistence and chunk sizes 1/37/257. Penalties, estimates, intervals and variance match within rtol 1e-9 and atol USD 1e-6. No-audit refusal and strict finite/disconnected/whole-line/unavailable consumer semantics pass.

Six isolated single-thread workloads include generation, tuning/refit, inference, serialization and whole-process RSS. The streaming fit is slower; whole-workload memory/time gains are not consistent because generation dominates peak memory. These no-gain findings remain evidence:

'''
for r in mc.read(ROOT,'docs/program/master/work/E01-v2/workloads.json')['rows']:
 review+=f"- {r['mode']} T={r['origins']}: total {r['total_seconds']:.4f}s, fit {r['fit_seconds']:.4f}s, peak {r['peak_rss_kib']/1024:.2f} MiB.\n"
review+='\nActual abrupt exits during fit, partial checkpoint and final publication recover 12 records each, never publish a premature manifest, replay without duplicates and reject changed immutable input identities. This establishes local single-process integrity, not bank/platform acceptance or improved statistical calibration.\n'
close('E01','v2','pass',['pass']*4,
 ['Actual A-D sets, refusals, qualifiers and units survive roundtrip; malformed computed sets reject.','Pilot/evaluation chunking matches dense computation; six complete workload measurements retain losses.','Three actual process-death trials recover immutable identities atomically and idempotently.','Scientific and platform limits remain attached; only authorized repository work.'],dict(D01='conditional_progress',D06='conditional_progress',D07='conditional_progress',D08='unresolved'),review)
print('Corrected reviews and receipts prepared.')
