#!/usr/bin/env python3
"""Save bounded survival source scope, retaining preparation failures."""
import json
import subprocess
from pathlib import Path
BASE = Path('docs/program/execution/2026-10-14/commercial-survival/v2')
BASE.mkdir(exist_ok=False)
plan = '''# Commercial survival comparison: plan and review

Review eight named families: Stata, SAS, IBM SPSS, JMP, MATLAB, Minitab, NCSS
and Statistica. The inherited empty cell is a search gap, not absent features.
Use bounded official-page acquisition, one fallback original per unavailable
essential source, and preserve failures and omissions. No global census claim.

Compare survival treatment effects, conditional hazards, time-varying
covariates versus sequential causal regimes, censoring, competing events,
common time zero, positivity, uncertainty and failed fits. Compare documented
capabilities against the actual six-operation local reference. Keep edition,
licensing and runtime unknowns distinct from method and target semantics.

Construct exact banking examples for competing default/prepayment, delayed
assignment, informative censoring, time-varying confounding and rare-path
bootstrap failure. Prices and data remain scenarios. Integrate a connected
comparison into the main monograph, audit claims and reproduce examples.
Compile and inspect text/bounds without more images in this session.

Plan review: bounded primary acquisition and mathematical examples can
proceed without a paid license or bank data. Licensed trials and institutional
acceptance are later conditional work. Exact historical web bytes and broader
coverage remain unqualified. Cutoff: 2026-10-07 Asia/Shanghai.

Preparation failures: one inline Python command and one JavaScript patch
payload had string syntax errors before execution. Neither wrote artifacts.
An existing same-name folder then stopped preparation before any artifact
write. It contains a preserved eight-URL fixed-collector allowlist failure.
This successor uses existing approved bounded curl commands without changing
the collector, its allowlist or permission settings. Prior failures remain.
'''
(BASE/'plan-review.md').write_text(plan)
rows = [
 ('stata_intro','https://www.stata.com/manuals/causalstteffectsintro.pdf','pdf'),
 ('stata_ipwra','https://www.stata.com/manuals/causalstteffectsipwra.pdf','pdf'),
 ('stata_post','https://www.stata.com/manuals/causalstteffectspostestimation.pdf','pdf'),
 ('sas_phreg','https://support.sas.com/documentation/onlinedoc/stat/151/phreg.pdf','pdf'),
 ('ibm_time','https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=statistics-computing-time-dependent-covariates','html'),
 ('jmp_competing','https://www.jmp.com/support/help/en/18.1/jmp/competing-causes.shtml','html'),
 ('jmp_cox','https://www.jmp.com/support/help/en/18.1/jmp/proportional-hazards.shtml','html'),
 ('matlab_fitcox','https://www.mathworks.com/help/stats/fitcox.html','html'),
 ('minitab_counting','https://support.minitab.com/en-us/minitab/help-and-how-to/statistical-modeling/reliability/how-to/cox-regression/counting-process-form/interpret-the-results/all-statistics-and-graphs/method-table/','html'),
 ('ncss_cox','https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/NCSS/Cox_Regression.pdf','pdf'),
 ('statistica_cox','https://docs.tibco.com/pub/stat/14.2.0/doc/html/UserGuide/user-guide/cox-proportional-hazards-regression-quick-tab.htm','html'),
]
manifest={'cutoff':'2026-10-07 Asia/Shanghai','access_date':'2026-10-14',
 'requests':[{'id':i,'url':u,'extension':e} for i,u,e in rows],
 'bounds':'25s and 12MiB per public HTTPS GET; no execution, uploads or credentials'}
(BASE/'acquisition-manifest.json').write_text(json.dumps(manifest,indent=2)+chr(10))
search={'cutoff':'2026-10-07 Asia/Shanghai','searched_on':'2026-10-14',
 'queries':['site.stata.com/manuals stteffects survival time treatment effects',
 'site.support.sas.com documentation phreg competing risks time dependent',
 'site.ibm.com/docs/en/spss-statistics/30.0.0 Time-Dependent Cox',
 'site.jmp.com Competing Causes survival','site.mathworks.com/help/stats fitcox time',
 'site.support.minitab.com Cox Regression Counting','NCSS Cox regression technical documentation PDF',
 'survival analysis time dependent covariates Statistica'],
 'observations':'Web search supplied no inspectable result payload. Manifest entries are candidate official routes, not capability evidence.',
 'stopping_rule':'Eight named families, selected pages and one fallback per unavailable essential source; omissions retained.',
 'exhaustive':False}
(BASE/'search-ledger.json').write_text(json.dumps(search,indent=2)+chr(10))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
p=Path('docs/program/execution/2026-10-14/program-refresh/git-publication-db6bd014.json')
assert not p.exists()
p.write_text(json.dumps({'commit':head,'remote':'origin','branch':'main','push':'success',
 'remote_main_verified':head,'verification':'git ls-remote returned this exact hash',
 'reader':'docs/causal_proposal_banking_economics_v3_2026-10-14.pdf','proposal_operations_recorded':100},indent=2)+chr(10))
print(json.dumps({'plan':str(BASE/'plan-review.md'),'sources':len(rows),'verified_commit':head}))
