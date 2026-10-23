#!/usr/bin/env python3
"""Authenticate OBP's selected bandit profile and close its proposal disposition."""
import argparse,hashlib,json
from pathlib import Path
import obp_reference_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-23/obp-reuse-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text());REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Selected immutable software sources and exact authored examples only; no downloaded code or dataset executed.',
 'No full artifact, transitive dependency/data rights, environment lock, native conformance, empirical coverage or bank benefit established.',
 'Continuous/slate/multiple-logger/action-embedding and full learning families require separate review.']
SPANS={
 'LICENSE':[([1,201],'Apache2.0 source text and named copyright holders; no transitive rights clearance.')],
 'setup.py':[([1,60],'Author, package metadata, dependency minima, classifiers and packaging declarations.')],
 'pyproject.toml':[([1,44],'Version0.5.5, Python below3.10, selected exact library pins and Poetry build metadata.')],
 'obp/version.py':[([1,1],'Runtime version declaration0.5.5 matches Poetry metadata.')],
 'obp/ope/estimators.py':[([73,114],'Replay exact-one match and zero vector when no matches occur.'),([276,290],'IPW threshold and estimated-propensity flag defaults.'),([330,338],'Observed-action importance ratio and clipping.'),([384,407],'Selected propensity array and core validator.'),([465,494],'Fixed round-score bootstrap delegation.'),([575,658],'Self-normalized IPW inheritance and mean-weight normalization.'),([977,996],'DR regression expectation and clipped residual correction.')],
 'obp/ope/helper.py':[([14,60],'Direct clipping-bias calculation; theorem citation is not independently reviewed here.'),([63,114],'Bias-upper-bound helper expression and selected delta.'),([117,158],'One-sided Hoeffding helper accepts provided bound or observed maximum.'),([161,234],'Bernstein lower bound and one-sided Student quantile; distinct from symmetric-interval contract.')],
 'obp/ope/meta.py':[([102,140],'Model prediction dimensions and estimator-specific input validation.'),([192,241],'Per-estimator selected propensity and fitted-input forwarding.'),([398,421],'Common alpha and bootstrap settings passed to each estimator.')],
 'obp/ope/regression_model.py':[([67,89],'Model clones per position and default action identity features.'),([157,180],'Per-position normal, importance-weighted and MRDR fitting paths.'),([280,331],'Uniform propensity fallback, one-fold in-sample fit and shuffled row cross-fitting.')],
 'obp/ope/estimators_tuning.py':[([116,189],'MSE and score-stability threshold selection.'),([235,273],'Selected propensity alias, cached hyperparameter and point-estimator constructor.'),([332,371],'Cached threshold interval delegate forwards selected pscore alias despite omitted constructor flag.'),([549,577],'Outer tuning interval validates and forwards the selected array.')],
 'obp/utils.py':[([16,86],'Bootstrap settings, fixed-round resampling, percentile endpoints and bootstrap-mean output.'),([150,177],'Array helper checks type and dimension, not general finiteness.'),([347,412],'Action sum, index, prediction shape and positive-propensity checks; no separate nonnegative target entry check.')],
 'obp/dataset/real.py':[([67,101],'Campaign/behavior identity and default data path.'),([124,208],'On-policy empirical mean, timestamp sorting, logged propensity extraction and feature construction.'),([240,285],'Optional chronological split after feature preparation.'),([329,355],'Row bootstrap of selected feedback arrays.')]
}
FINDINGS=['Bandit IPW/DR, replay and clipping preserve different contracts; one-step evaluation is not longitudinal identification.',
 'Selected input checks need independent probability/finiteness/identity validation; regression fallback and row-fold clocks are explicit.',
 'Bootstrap fixes scores and tuned thresholds; object cache and selected-policy uncertainty remain qualification obligations.',
 'Apparent interval estimated-propensity flag omission is resolved by selected-array forwarding; one-sided Student helper is not a symmetric interval.',
 'Public on-policy comparison is an empirical campaign mean, not exact counterfactual truth; preprocessing precedes optional chronological split.']
def audit():
 assert not (BASE/'source-audit.json').exists()
 sel=read(BASE/'source-selection.json');commit=read(RAW/'exec23_obp_cutoff.json')[0];tree=read(RAW/'exec23_obp_tree.json')
 assert sel['commit']==commit['sha']=='8cbd5fa4558b7ad2ba4781546d6604e4cc3e07c4'
 assert tree['sha']==commit['commit']['tree']['sha']==sel['tree'] and not tree['truncated']
 assert sel['date']==commit['commit']['committer']['date']=='2022-11-05T01:31:18Z'
 entries={e['path']:e for e in tree['tree']};records=[]
 for e in sel['selected']:
  p=RAW/(e['id']+'.txt');data=p.read_bytes();receipt=read(RAW/(e['id']+'.receipt.json'));path=e['path'];blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  url='https://raw.githubusercontent.com/st-tech/zr-obp/'+commit['sha']+'/'+path
  assert blob==entries[path]['sha'] and len(data)==entries[path]['size'] and receipt['sha256']==core.sha(p) and receipt['url']==url
  assert all(1<=a<=b<=len(data.decode().splitlines()) for (a,b),_ in SPANS[path]),path
  records.append(dict(upstream_path=path,source_identity=url,version_date=sel['date'],local_copy=ref(p,'Inspected technical spans'),receipt=ref(RAW/(e['id']+'.receipt.json'),'Acquisition custody'),git_blob_sha1=blob,inspected_anchors=[dict(lines=span,finding=c) for span,c in SPANS[path]],supported_claims=[c for _,c in SPANS[path]],executed=False))
 assert len(records)==11
 assert (RAW/'exec23_obp_10.txt').read_text().strip()=='__version__ = "0.5.5"'
 result=exact.calculate();assert result==read(BASE/'exact-results.json')
 write(BASE/'static-contract-check.json',dict(native_execution=False,inert_ast_only=True,findings=FINDINGS,rejected_concern='The selected estimated propensity is passed as pscore_ to the default base interval; omission of the flag does not establish a wrong-array defect.',evidence=[ref(Path(exact.__file__),'Inert AST and exact examples')]))
 identity=dict(repository='st-tech/zr-obp',version='0.5.5',commit=commit['sha'],tree=tree['sha'],date=sel['date'],source_blobs=11,evidence=[ref(RAW/'exec23_obp_cutoff.json','Cutoff identity'),ref(RAW/'exec23_obp_tree.json','Canonical tree')],maintenance='Named author and selected revision only; current support and complete release history unqualified.')
 write(BASE/'identity.json',identity)
 source=dict(integrated_citation_key='exec23_obp_sources',kind='software_primary_sources',title='Open Bandit Pipeline0.5.5 selected logging, clipping, fitting and interval contracts',author='Yuta Saito and Open Bandit Pipeline contributors',year=2022,source_identity='https://github.com/st-tech/zr-obp/tree/'+commit['sha'],version_date='0.5.5; '+sel['date'],local_copy=records[3]['local_copy'],identity=identity,records=records,
  inspected_anchors=[dict(path=r['upstream_path'],anchors=r['inspected_anchors']) for r in records],supported_claims=[c for spans in SPANS.values() for _,c in spans],license_text=ref(RAW/'exec23_obp_00.txt','Authenticated license'),limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_obp_reference',kind='project_derivation_and_exact_reference',title='Independent contextual-bandit weighting, clipping and caller-contract witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/obp_reference_20261023.py',version_date='23 October2026; independently authored exact examples',local_copy=ref(Path(exact.__file__),'calculate'),inspected_anchors=['calculate'],supported_claims=['Two equal context types give target/IPW7/2, clipped3 and uniform-logger/replay17/4.',
  'Stipulated ten-dollar reward conversion and cost32 give margins3,-2 and10.50.', 'Correct response regression gives DR population7/2 in the stated law despite clipping.',
  'An invalid probability row sums to one; stochastic target has no exact-one replay matches.', 'Inert AST confirms selected-array forwarding resolves the apparent tuning flag omission.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 omissions=dict(items=[dict(gap='Complete artifact, dependency/data rights and runtime',next_action='Resolve the selected Python/Poetry/setup requirements against authentic full release and dependency/data notices.'),
  dict(gap='Native validation, replay, state and interval contracts',next_action='Register exact-law adverse fixtures for invalid/nonfinite probabilities, action/position identity, no matches, clipping, fitted nuisances, tuned-object reuse and complete resampling.'),
  dict(gap='Scientific and temporal generalization',next_action='Justify logging truth, common context law, clustering, chronology and policy selection separately; do not infer a sequential target from flattened rows.'),
  dict(gap='Broader software families and public dataset',next_action='Inspect each additional family, full delegates and actual data/license artifacts before native or rights claims.')],limitations=LIMITS)
 write(BASE/'omissions-register.json',omissions)
 write(BASE/'plan-review.json',dict(status='pass_for_reference_disposition',evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan.md','exact-results.json','static-contract-check.json','development.tex']],findings=FINDINGS,native_execution=False))
 evidence=[ref(BASE/n,'Reviewed technical argument') for n in ['source-audit.json','identity.json','static-contract-check.json','exact-results.json','omissions-register.json','plan-review.json','development.tex']]+[ref(Path(__file__),'Audit logic'),ref(Path(exact.__file__),'Independent examples')]
 review=dict(status='pass_for_reference_disposition',reviewer=REVIEWER,evidence=evidence,findings=FINDINGS,limitations=LIMITS,native_execution=False);verify_bindings(review);write(BASE/'review.json',review)
 print(json.dumps(dict(source_blobs=11,source_records=2,decision='reference',native_execution=False)))
def receipt():
 op='SW.DECISION.inherited_obp';state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op;verify_bindings(read(BASE/'review.json'))
 evidence=[ref(BASE/n,'Reviewed bandit reference decision') for n in ['source-audit.json','identity.json','review.json','plan-review.json','exact-results.json','static-contract-check.json','omissions-register.json','development.tex']]+[ref(Path(__file__),'Receipt logic')]
 output=ROOT/f'docs/program/comprehensive-v14/work/{op}/decision.json'
 decision=dict(operation_id=op,status='pass',decision='reference',decision_scope='Source-qualified contextual-bandit proposal reference; no native adapter approval',identity=read(BASE/'identity.json'),reason='Retain explicit one-decision estimators, preprocessing and comparison contracts; qualify logging, validation, tuning and uncertainty before native use.',target_and_uncertainty='Common context distribution and one-decision policy value with action/position-specific logging; clipped scores, fitted nuisances, row bootstrap and adaptive threshold selection remain distinct.',
  license=dict(declaration='Apache2.0',evidence=ref(RAW/'exec23_obp_01.txt','Packaging declaration'),text=ref(RAW/'exec23_obp_00.txt','Pinned text'),transitive_clearance=False),
  dependencies=dict(evidence=[ref(RAW/'exec23_obp_01.txt','Setup minima'),ref(RAW/'exec23_obp_02.txt','Poetry versions/Python restriction')],environment_locked=False),
  conversion_contract=['Preserve row/customer IDs, context/action/outcome clocks, position vocabulary, target, logging/estimated propensity provenance and monetary units.',
   'Validate finite nonnegative target probabilities and positive observed propensities; preserve no-match replay as unavailable evidence.',
   'Bind response fits, customer/calendar folds, clipping and tuning state; define whether bootstrap refits or conditions on selected quantities.',
   'Keep library/CLI/MCP target, identity, uncertainty and refusal semantics identical; never infer truth from an agent-filled schema.'],
  alternatives=[dict(route='Full adoption',decision='defer',reason='Uninspected families, full rights and native qualification exceed this profile.'),dict(route='Isolated Python worker',decision='conditional future prototype',reason='Original estimator semantics may be preserved after explicit environment and adverse qualification.'),dict(route='R/Java/C++ port',decision='reject for current scope',reason='No demonstrated benefit warrants reproducing preparation, tuning and uncertainty maintenance.'),dict(route='Independent exact oracle',decision='retain',reason='Known finite laws test contracts without claiming full software parity.'),dict(route='Longitudinal or generic safe policy replacement',decision='reject',reason='Single-decision logged-bandit structure does not establish sequential causal identification or selected-policy safety.')],
  costs_to_measure=['Environment/data rights','Clock/position/identity conversion','Nuisance and threshold qualification','Native adverse fixtures','Complete fitting/resampling compute','Upgrade maintenance'],owner_obligations=dict(scientific='Logging truth, target, sampling and selected-policy uncertainty',maintainer='Frozen source/environment, adapter validation and native conformance',operator='Dataset custody, actual rights, costs and recovery'),revisit_trigger='Complete source/data/dependency custody and registered native qualification; changed target, environment, clocks or selection rule requires review.',evidence=evidence,reviewer=REVIEWER,limitations=LIMITS,integration_allowed=False,runtime_qualification=False,capabilities=[])
 write(output,decision);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);r=run.ledger.receipt_template(node)
 findings=['Concrete cutoff version, source license, dependency and maintenance limits inspected.','Target, conversion, uncertainty, alternatives, costs and owner/revisit obligations explicit.','Reference-only scope preserves native/scientific limitations and rejects an unsupported defect claim.']
 r.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,outputs=[ref(output,'Contracted reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r)
 print(json.dumps(dict(operation=op,decision='reference',integration_allowed=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
