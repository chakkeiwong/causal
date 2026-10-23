#!/usr/bin/env python3
"""Authenticate selected Tigramite sources and record a bounded reuse choice."""
from pathlib import Path
import hashlib,json
import run_program_checkpoint_v3 as controller
import tigramite_contract_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=controller.base;ROOT=run.core.ROOT;RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-23/tigramite-reuse-v1'
OP='SW.DECISION.inherited_tigramite';PIN='ff3ff13e1481073b8c5833a6fde1c304627a208e'
OUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
PRIOR=ROOT/'docs/program/execution/2026-10-23/structured-causal-reader-v3/reader/source-audit.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=['This review statically inspects pinned source; downloaded code is not executed.',
'Prior installed Tigramite 5.2.10.1 trials remain separate evidence; identical version strings do not prove byte-identical builds.',
'Only selected methods/delegates are inspected; other CI tests, mediation, regime/context learners and all dependency artifacts are not newly qualified.',
'Exact authored examples are not measured package outputs, runtime failures, coverage or bank economics.',
'GPL declaration and source bytes are recorded; distribution and transitive rights require a specific reviewed delivery path.',
'No integration capability, arbitrary graph-to-effect confidence, bank validity or final proposal acceptance is granted.',
'Q1/Q5, mandatory coverage/depth rollups and fresh visual acceptance remain open.']

def main():
 state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active']['operation']==OP
 assert not OUT.exists()
 commit=read(RAW/'exec14_pt_commit_tigramite.json')[0];tree=read(RAW/'exec23_tigramite_canonical_tree.json')
 assert commit['sha']==PIN and tree['sha']==commit['commit']['tree']['sha'] and not tree['truncated']
 assert commit['commit']['committer']['date']<'2026-10-07T15:59:59Z'
 entries={r['path']:r for r in tree['tree']}
 maps=[dict(id=f'exec14_pt_file_tigramite_{i}',source_path=p) for i,p in enumerate(['README.md','license.txt','tigramite/jpcmciplus.py','tigramite/rpcmci.py','tigramite/data_processing.py'],1)]
 for name in ['pinned-source-manifest.json','delegate-manifest.json']:
  maps += [r for r in read(BASE/name)['requests'] if r.get('source_path')]
 findings={
 'README.md':('18-39; 65-120','Method/test assumption table; graphs differ by method, effect class assumes graph, GPLv3-or-later declaration and broad dependency guidance.'),
 'license.txt':('1-674','Preserved upstream GPLv3 license text; this review records identity and does not clear a proposed distribution.'),
 'tigramite/jpcmciplus.py':('previous exec14_pt_tigramite inspected context-exogeneity anchors','Prior reviewed joint-context assumptions remain separate; no new execution or blanket transfer.'),
 'tigramite/rpcmci.py':('20-88','Finite persistent stationary regimes; scalar single-series restriction; supplied mask ignored and replaced; missing flag distinct.'),
 'tigramite/data_processing.py':('439-491; 711-733; 748-903','Integer offsets/reference positions, cutoff and mask selection; bootstrap start excludes last possible full block; missing expansion lacks bound clipping; used-index attribute written after dataset loop.'),
 'setup.py':('30-90','Declares 5.2.10.1; minimal numpy/scipy/six, optional algorithm dependencies, beta classifier; unpinned environment and test-extra pytorch name.'),
 'tigramite/pcmci.py':('1746-1760; 1854-1947; 3373-3431','Method signature defaults fdr_method to none despite docstring default fdr_bh; selected links omitted from assumptions are absent; statistics and CI matrices are not effect estimates; endpoint conflicts retained.'),
 'tigramite/lpcmci.py':('18-61; 155-166; 328-338','Temporal PAG/DPAG and adjacency p/statistic outputs; endpoint information must survive conversion.'),
 'tigramite/causal_effects.py':('15-110; 705-880; 1148-1290','DAG/ADMG variants supported; PAG graph types excluded. Adjustment validity, hard/additive-soft predictions and percentile effect fits use a supplied graph, not discovery uncertainty.'),
 'tigramite/independence_tests/independence_tests_base.py':('360-465; 870-951; 974-1066','Constant X/Y shortcut, threshold rules, optional None confidence return, dependence-statistic CI and block sampling; no independent causal-effect meaning.'),
 'tigramite/independence_tests/parcorr.py':('15-38; 62-147; 149-235','OLS residual correlation; analytic t uses T-dim, returns NaN for nonpositive degrees of freedom; shuffled residual p value uses plus-one correction.'),
 'tigramite/models.py':('229-370','Hard values versus additive shifts of observed X; adjustment distribution and optional conditional nested regression; aggregation returns predictions before any caller contrast.'),
 'tigramite/graphs.py':('37-172; 282-317','Supported graph-type and edge-string validation; ambiguous discovery output cannot be relabeled as a unique supported causal graph.'),
 'tigramite/pcmci_base.py':('262-365; 928-1045','BH correction test family explicit; graph summary chooses modal mark and sums tied modal counts, so link_frequency is not necessarily chosen-mark occurrence or confidence.')}
 records=[]
 for row in maps:
  p=RAW/(row['id']+'.txt');data=p.read_bytes();rp=p.with_suffix('.receipt.json');receipt=read(rp);up=row['source_path']
  expected=f'https://raw.githubusercontent.com/jakobrunge/tigramite/{PIN}/{up}'
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert blob==entries[up]['sha'] and len(data)==entries[up]['size']
  assert receipt['status']=='saved' and receipt['url']==expected and receipt['sha256']==run.core.sha(p)
  span,claim=findings[up];anchor=span+'; '+claim
  records.append(dict(source_identity=expected,upstream_path=up,version_date=commit['commit']['committer']['date']+'; '+PIN,
   local_copy=ref(p,anchor),receipt=ref(rp,'Acquisition receipt'),git_blob_sha1=blob,inspected_anchors=[anchor],supported_claims=[claim],executed=False))
 assert len(records)==14
 old_sources={s['integrated_citation_key']:s for s in read(PRIOR)['sources']}
 prior_keys=['exec14_pt_tigramite','runtime_tigramite_scope','runtime_networkx_dynamic']
 write(BASE/'prior-evidence.json',dict(sources=[old_sources[k] for k in prior_keys],boundary='Preserved prior source and installed-operation evidence; not a new execution.'))
 write(BASE/'exact-results.json',exact.calculate())
 identity=dict(repository='jakobrunge/tigramite',selected_commit=PIN,commit_date=commit['commit']['committer']['date'],tree_sha=tree['sha'],declared_version='5.2.10.1',
  source_blobs=14,cutoff='2026-10-07',maintenance='Cutoff-selected merge commit and beta setup declaration; support duration, all branches and complete release history not assessed.',
  alias_resolution='Tigramite is the package; PCMCI, PCMCI+, LPCMCI, RPCMCI and J-PCMCI+ are distinct method profiles, not interchangeable engines.',
  canonical_tree_note='New acquisition verifies actual tree SHA against commit; earlier tree endpoint used the commit identifier.',
  evidence=[ref(RAW/'exec14_pt_commit_tigramite.json','Cutoff commit'),ref(RAW/'exec23_tigramite_canonical_tree.json','Canonical tree')])
 write(BASE/'identity-review.json',identity)
 source=dict(integrated_citation_key='exec23_tigramite_reuse_source',kind='software_primary_sources',title='Tigramite pinned temporal discovery, graph, effect and resampling contracts',author='Jakob Runge and Tigramite contributors',year=2026,
  source_identity='https://github.com/jakobrunge/tigramite/tree/'+PIN,version_date=identity['commit_date']+'; '+PIN,
  local_copy=records[0]['local_copy'],records=records,inspected_anchors=[v[0] for v in findings.values()],supported_claims=[v[1] for v in findings.values()],limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_tigramite_reference',kind='project_derivation_and_exact_reference',title='Temporal package conversion, intervention and resampling reference examples',author='Causal banking proposal project',year=2026,
  source_identity='tools/tigramite_contract_reference_20261023.py',version_date='2026-10-23',local_copy=ref(ROOT/'tools/tigramite_contract_reference_20261023.py','calculate() rational and enumeration witnesses'),
  inspected_anchors=['calculate()'],supported_claims=['Partial correlation 4/5 differs from a stipulated 20 USD effect; net 8 USD versus erroneous -56/5 USD.',
  'Hard zero-to-one and additive plus-one interventions on square response give 1 and 3 under the declared population.',
  'Tied modes can have mass one while the emitted conflict mark occurs zero times; last-block exclusion and missing-boundary witnesses are finite enumerations.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 contract=dict(status='proposed_not_implemented',selected_path='Method-specific isolated Python reference worker, conditional on environment, rights and conformance; no immediate native integration.',
  scientific_requirements=['Specify ordered variables, time grid, unit/panel IDs, availability clock, missingness, stationarity, latent status and test regime.',
   'Separate statistic, edge hypothesis, endpoint class, graph assumptions, identification and intervention target.'],
  conversion=['Preserve source/target/lag axes and raw endpoint strings, conflicts, absent and prohibited edges; never silently orient a PAG.',
   'Keep alpha, search constraints, explicit fdr_method/test family, confidence target and resampling design.',
   'Record row-level effective sample provenance for every dataset, mask role, cutoff and missing expansion.',
   'Export intervention predictions with baseline, hard/additive policy, units and transforms; form contrasts explicitly.',
   'Distinguish bootstrap conditional on a supplied graph from discovery resampling; no graph confidence claim from frequency.'],
  failure=['Reject nonfinite p/statistic values, insufficient degrees of freedom and inadmissible arrays with typed diagnostics.',
   'Treat constant-variable shortcut as degeneracy, not empirical proof of independence.',
   'Block ambiguous graph-to-effect conversion and ignore_identifiability bypass in an accepted profile.',
   'Require oracle cases for tied modal marks, end block support, missing tail expansion, masks and all-panel index custody.',
   'Preserve source behavior or propose a separately named reviewed patch; never silently repair and claim upstream equivalence.',
   'Record every failure, warning, budget, seed, mutable dataframe/model ownership and dependency identity.'],
  oracle=ref(BASE/'exact-results.json','Independent exact cases; native replay remains outstanding'),integration_allowed=False)
 write(BASE/'conversion-contract.json',contract)
 omissions=[dict(gap='Native replay of selected source hazards',next_action='Resolve pinned environment and reproduce tie summary, block-end support, tail missingness and per-panel provenance against independent references before adoption.'),
  dict(gap='Other algorithm and estimator delegates',next_action='Inspect exact CI tests/regime/context profiles and selected sklearn estimator; qualify each target separately.'),
  dict(gap='Graph-to-effect identification and uncertainty',next_action='Retain compatible graph family and explicit added assumptions; justify effect set and uncertainty law instead of arbitrary orientation.'),
  dict(gap='Artifact rights and maintenance',next_action='Review actual GPL distribution path, dependency artifacts and upgrade ownership; do not infer exemption from process isolation.'),
  dict(gap='Scientific and monetary value',next_action='Use registered public/synthetic prospective trials with a matched failure denominator and full workflow costs before later bank experiments.')]
 write(BASE/'omissions-register.json',dict(items=omissions,limits=LIMITS))
 write(BASE/'plan-review.json',dict(status='pass_for_scoped_reference_decision',reviewer=REVIEWER,evidence=[ref(BASE/'plan.md','Plan reviewed before acquisition')],
  findings=['Acquire graph/models/PCMCI base delegates before conversion conclusions.','Preserve older installed evidence and exact tree identity.','Static hazards need native confirmation; do not grant adapter approval from authored witnesses.','Continue other eligible work despite graph/rights/native gaps.']))
 evidence=[ref(BASE/n,'Reviewed Tigramite reuse evidence') for n in ['plan.md','plan-review.json','identity-review.json','prior-evidence.json','source-audit.json','exact-results.json','conversion-contract.json','omissions-register.json']]
 evidence += [ref(Path(__file__),'Audit and receipt implementation'),ref(ROOT/'tools/tigramite_contract_reference_20261023.py','Exact independent reference')]
 decision=dict(operation_id=OP,decision='reference',status='pass',decision_scope='Method-specific proposal reference disposition with conditional future isolated-worker route.',identity=identity,
 license=dict(declaration='GNU GPL version 3 or later in README; GPLv3 text preserved',evidence=records[1]['local_copy'],transitive_clearance=False),
 dependencies=dict(setup_minimum=['numpy>=1.18','scipy>=1.10.0','six'],method_specific=['numba','scikit-learn','dcor','torch','gpytorch','joblib','ortools'],versions_locked=False),
 target_and_uncertainty='Method-specific lagged graph/CPDAG/PAG and CI statistics; separately, graph-conditioned intervention predictions and fit bootstrap; no general effect confidence region from discovery.',
 reason='Explicit method assumptions and source transparency make a useful temporal comparator; unresolved conversion and resampling edge cases prevent immediate adoption without replay.',
 alternatives=[dict(route='Direct whole-package adoption',disposition='defer',reason='Distinct graph/effect targets, source hazards and unlocked environment require selected profiles and behavioral oracles.'),
 dict(route='Selected Python worker',disposition='conditional future prototype',reason='Retains upstream scientific methods while adding provenance, refusal and failure contracts; does not settle distribution rights.'),
 dict(route='Port to R/Java/C++',disposition='reject for current proposal',reason='No measured platform advantage justifies reimplementing orientation, tests and resampling; compare complete workflow cost first.'),
 dict(route='LPCMCI for latent temporal discovery',disposition='separate profile',reason='Retains PAG uncertainty but cannot directly enter the selected DAG/ADMG effect class.'),
 dict(route='Known-graph adjustment or other reviewed engine',disposition='question-dependent alternative',reason='Use a scientifically justified graph and separate identification/estimator contract; cross-package approval never transfers.'),
 dict(route='Treat graph frequency or ParCorr as monetary effect confidence',disposition='reject',reason='Different mathematical targets; explicit counterexamples show incorrect conversion.')],
 costs_to_measure=['Installation and dependency custody','CI search/graph ambiguity and failed queries','Resampling and seed ownership','Serialization and calendar validation','Upgrade regression, rights review and scientific labor'],
 owner_obligations=dict(scientific='Model/test/target, additional assumptions, uncertainty and calibration',maintainer='Pinned artifacts, oracle replay, all failures and conversions',operator='Rights, custody, platform budgets and recovery'),
 revisit_trigger='Reopen after permissible artifact/environment pinning and passing native oracle/public trial results for a declared method; source, sampling law or platform changes trigger re-review.',
 contract=ref(BASE/'conversion-contract.json','Proposed conversion/failure contract'),integration_allowed=False,capabilities=[],runtime_qualification=False,original_gap_qualification=False,reviewer=REVIEWER,evidence=evidence,limitations=LIMITS)
 write(OUT,decision)
 findings_review=['Fourteen authenticated source blobs bind exact commit, canonical tree, version, license, dependencies, prior evidence and maintenance limits.',
 'Method-specific target, uncertainty, alternatives, explicit cost/owner responsibilities and reopening conditions are stated with independent exact examples.',
 'Reference-only disposition and prospective conversion/failure contract grant no integration or runtime capability.']
 write(BASE/'review.json',dict(status='pass_for_scoped_proposal_reference',reviewer=REVIEWER,findings=findings_review,evidence=evidence,reviewed_output=ref(OUT,'Tigramite reuse decision'),limitations=LIMITS))
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);receipt=run.ledger.receipt_template(node)
 receipt.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,limitations=LIMITS,original_gap_qualification=False,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],outputs=[ref(OUT,'Contracted decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Author review')]) for i,f in enumerate(findings_review)])
 verify_bindings(receipt);run.validate_receipt(ROOT,merged,node,receipt,len(state['execution_program']['turns']));write(BASE/'operation-receipt.json',receipt)
 print(json.dumps(dict(operation=OP,source_blobs=len(records),decision='reference',integration_allowed=False)))
if __name__=='__main__':main()
