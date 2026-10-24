#!/usr/bin/env python3
"""Prepare the all-obligation successor reconciliation before publication."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
b=ROOT/'docs/program/execution/2026-10-24/augsynth-reuse-v1'
(b/'publication-order-review.json').write_text(json.dumps(dict(status='reviewed_before_receipt',prior_plan_preserved=True,reason='Sponsor requires actual canonical counts and exact published reader; recording the reference decision first grants no proposal acceptance.',sequence=['Source and witness review','Build and review reader','Record reference decision','Publish reader and renew Q2-Q4','Pair sponsor','Refresh and check all obligations'],final_acceptance=False),indent=2)+chr(10))
s=(ROOT/'tools/refresh_synth_reuse_program_20261024.py').read_text()
s=s.replace('program-refresh-synth-reuse-v1','program-refresh-augsynth-reuse-v1').replace("PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-panels-r-v1'","PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-synth-reuse-v1'")
s=s.replace("/synth-reuse-reader-v1'","/augsynth-reuse-reader-v1'").replace("/sponsor-synth-reuse-v1'","/sponsor-augsynth-reuse-v1'").replace("/synth-reuse-v1'","/augsynth-reuse-v1'")
s=s.replace('1127','1129').replace('1125','1127').replace('631','635').replace('263','264').replace('191','190')
s=s.replace("groups['reuse']['pass']==68","groups['reuse']['pass']==69").replace("groups['reuse']['open']==44","groups['reuse']['open']==43")
s=s.replace('reuse68pass/3inconclusive/44open','reuse69pass/3inconclusive/43open').replace('44 open and three inconclusive','43 open and three inconclusive')
s=s.replace('Python-panel coverage has a bounded inconclusive outcome; no exhaustive or adapter capability admission.','augsynth reference decision recorded; no exhaustive or adapter capability admission.')
s=s.replace('Python adds three records;Synth adds two;all earlier records remain preserved. Synth reference decision grants no native admission.','augsynth adds two records preserving all earlier records; reference decision grants no native admission.')
a=s.index('## Newly reconciled work');z=s.index('## Remaining gaps and routes',a)
s=s[:a]+'''## Newly reconciled work

The successor integrates the augsynth 0.2.0 reference decision. Thirteen
original files authenticate to the 4 September 2026 repository pin. The
chapter distinguishes single-date, multiple-outcome and staggered dispatch,
negative donor weights, donor eligibility, tuning calendars, solver status
and conditional confidence-grid states. Exact authored financial examples
reproduce; downloaded package code was not executed.

A draft misinterpreted R sequence semantics. An authored base-R check
established that the lambda grid includes its nominal endpoints. The rejected
witness and correction are preserved. Remaining holdout and interval findings
are conditional static observations, not observed native failures.

All 1,127 predecessor records, citation contexts and compiled inputs survive;
two new audited records bring the total to 1,129. The paired sponsor preserves
all 631 prior citation records and adds four. The source/arithmetic/text review
is not fresh visual, independent or final acceptance.

'''+s[z:]
p=ROOT/'tools/refresh_augsynth_reuse_program_20261024.py';assert not p.exists();p.write_text(s)
print('Publication order and full successor refresh prepared.')
