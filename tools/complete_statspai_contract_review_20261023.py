#!/usr/bin/env python3
"""Preserve cutoff source review; execute only project-authored data inspections."""
import json
from pathlib import Path
import statspai_contract_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
DAY=ROOT/'docs/program/execution/2026-10-23'
BASE=DAY/'statspai-contract-v1'
ACQ=DAY/'statspai-acquisition-v1'
read=lambda p:json.loads(p.read_text())
ANCHORS={
0:('1-21','MIT notice, attribution condition and warranty disclaimer inspected; transitive and dataset rights remain separate.'),
1:('1-101;165-173','Cutoff source declares version1.39.0, Python>=3.10, lower-bounded dependencies and optional stacks, and CLI/MCP entrypoints. The JOSS archive1.23.0 is a different version.'),
2:('complete file','Only method is required. CI length/order, nonnegative SE, probability range and observation-count integrality are not enforced.'),
3:('1-168','Import-free schema bundle description; exported result schema matches the inspected permissive contract. Generator functions are inspected, not executed.'),
4:('1-100;240-307;370-418;514-567','Evidence taxonomy separates aliases, helpers, cross-package references and internal fixtures. Eight Python-reference entries contradict the stale comment saying two. Aggregation differences refute an alias.'),
5:('complete file','Typed JSON-RPC exception codes; these do not by themselves establish causal identification or successful tool execution.'),
6:('1-100;780-940;1450-1670;1800-2090','Compact tool output schema admits any object. Structured error, nonfinite and truncation metadata are separate. Thread fallback may remain running after timeout; process route depends on helper eligibility and transfer. Budget applies to structuredContent, repeated text and images add wire bytes. Underlying helpers uninspected.'),
7:('140-153;270-307','Guide distinguishes committed comparisons from separately configured live R/Stata runtimes. Local and remote provenance differ; save external datasets and metadata before handing to estimator.'),
8:('251-281','Working-paper and distribution claims do not establish independent adoption. Open-source package and commercial downstream product are separate; wider dossier numerical claims not reproduced.'),
9:('1-160','Tests specify underidentified-IV typed errors and retention of diagnostics/alternatives. Test source inspected, no native test run or failure claimed.'),
10:('250-390','Saved-fixture tests specify estimator/statistic-specific tolerances, shared DML folds and nonunique SCM limits. RD standard-error tolerance can be7% although point tolerances are much tighter. No external results reproduced.')}
LIMITS=['Static primary-source review and project-authored schema/arithmetic witnesses only; no downloaded package code executed.',
'No native integration, full dependency rights clearance, scientific calibration, visual acceptance or bank adoption.',
'Cutoff revision is distinct from the published paper archive; eleven files are not a whole-repository audit.']

def main():
 assert not (BASE/'source-audit.json').exists()
 BASE.mkdir(exist_ok=True)
 auth=read(ACQ/'authentication-review.json');assert auth['status']=='pass' and len(auth['files'])==11
 records=[]
 for f in auth['files']:
  index=int(f['id'].rsplit('_',1)[-1]);span,claim=ANCHORS[index]
  p=ROOT/f['local_copy'];receipt=p.with_suffix('.receipt.json');r=read(receipt)
  assert r['sha256']==f['sha256']
  records.append(dict(role='inspected_primary_technical_text',source_identity=r['url'],upstream_path=f['path'],
    version_date='2026-10-07T15:30:14Z; commit '+auth['commit'],local_copy=ref(p,span+'; '+claim),
    receipt=ref(receipt,'Acquisition receipt'),git_blob_sha1=f['blob'],inspected_anchors=[span],supported_claims=[claim],executed=False))
 code=ROOT/'tools/statspai_contract_reference_20261023.py';result=exact.calculate();write(BASE/'exact-results.json',result)
 software=dict(integrated_citation_key='exec23_statspai_contract',kind='software_primary_sources',
  title='StatsPAI cutoff source, schema, MCP failure and parity contracts',author='Biaoyue Wang and StatsPAI contributors',year=2026,
  source_identity='https://github.com/brycewang-stanford/StatsPAI/tree/'+auth['commit'],version_date='2026-10-07T15:30:14Z; source1.39.0; '+auth['commit'],
  local_copy=records[0]['local_copy'],records=records,inspected_anchors=[r['local_copy'] for r in records],
  supported_claims=[r['supported_claims'][0] for r in records],limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_statspai_contract_reference',kind='project_reference_not_scholarly_paper',
  title='Independent static StatsPAI schema and weighting witnesses',author='Causal banking proposal project',year=2026,
  source_identity=str(code.relative_to(ROOT)),version_date='23 October2026; exact source and data bytes',
  local_copy=ref(code,'Project code uses JSON Schema validation and AST literal inspection; no upstream import'),
  inspected_anchors=[ref(BASE/'exact-results.json','Four schema cases, compact object, eight reference keys, two weighting targets and wire-copy lower bound')],
  supported_claims=['Method-only, semantically invalid and empty-interval payloads pass the inspected JSON schema; wrong method type fails.',
    'Two equal-sized customer cohorts with effects4/-4 and post-period counts3/1 give customer effect0 and treated-observation effect2; stipulated per-customer cost1 gives net-1 for the customer decision.',
    'Two copies of a262144-byte structured JSON payload contribute at least524288 payload bytes before the enclosing envelope, escaping and any image.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[software,project],cutoff='2026-10-07',authentication=ref(ACQ/'authentication-review.json','Eleven Git blobs and cutoff publisher-PDF equality'),native_execution=False))
 write(BASE/'plan-review.json',dict(status='pass',scope='Complete bounded cutoff contract review and integrate into the product proposal',
  steps=['Authenticate the11 selected source blobs and distinguish paper archive from cutoff version.',
    'Inspect schema, failures, process fallback, output budget and parity target boundaries.',
    'Run project-owned schema/arithmetic witnesses without importing upstream code.',
    'Compare direct adoption, adapter, port, reference and reject routes; define bounded qualification prerequisites.',
    'Preserve all prior citations/content, compile reader, pair sponsor and renew exact-reader reviews.',
    'Refresh durable continuation and commit/push, preserving unresolved work.'],
  findings=['One missing helper or external runtime does not block unrelated source work.',
    'Static counterexamples prove schema permissiveness, not that any estimator emitted invalid values.',
    'Success criteria concern proposal reasoning; scientific/runtime qualification remains separate.'],
  evidence=[ref(ACQ/'authentication-review.json','Authenticated input'),ref(code,'Independent reference')]))
 write(BASE/'decision.json',dict(candidate='StatsPAI',version='1.39.0 cutoff commit '+auth['commit'],
  route='conditional isolated adapter; reference-only until qualification',
  rationale='Existing registry, results, errors and replay metadata are valuable. Preserve scientific semantics in a stricter consumer contract and supervise actual runtime mode.',
  alternatives=[dict(route='direct adoption',decision='defer',reason='Uniform transport schema and metadata do not establish estimator-specific target, covariance, diagnostics or rights.'),
    dict(route='integrate',decision='conditional preferred',reason='Pinned worker with typed consumer contract avoids replacing mature estimators; retain errors, provenance, actual execution mode and complete risk details.'),
    dict(route='port',decision='selective only',reason='A scientifically necessary kernel or deployment constraint may justify a bounded port; broad copying adds solver, dependency and maintenance burden.'),
    dict(route='reference',decision='use now',reason='Source-grounded design comparison and independent witnesses are available without claiming execution.'),
    dict(route='reject',decision='reject blanket certification and unsafe result promotion',reason='Schema acceptance or upstream certified labels cannot justify truth, all-method parity or automatically retrying a still-running call.')],
  scope_limits=LIMITS,source_audit=ref(BASE/'source-audit.json','Pinned primary contracts')))
 write(BASE/'qualification-plan.json',dict(status='ready_design_not_executed',gates=[
  dict(id='SP1',work='Inspect THIRD_PARTY_NOTICES, selected dependency/data rights and environment lock; pin one estimator family.',accept='Complete source and rights inventory; separate paper, code and executable environment versions.'),
  dict(id='SP2',work='Read process worker, runner, cache, data loader, output budget and replay helpers at the same commit.',accept='Explicit fallback, cancellation, resource admission and provenance contracts with no claims inferred solely from caller comments.'),
  dict(id='SP3',work='After a separately permitted prototype environment exists, replay exact inputs/folds against a qualified reference.',accept='Compare target, coefficient and full covariance, diagnostics and refusals with predeclared per-statistic tolerances; preserve all failures.'),
  dict(id='SP4',work='Exercise stale handles, missing files, nonfinite values, risk truncation, timeout, cancellation and replay after restart.',accept='No scientific success on incomplete output; no retry before active-worker state is reconciled; full wire size measured.'),
  dict(id='SP5',work='Compare bounded integration cost against a direct mature-package wrapper on public/generated tasks.',accept='Matched target and scientific quality; measured environment/runtime costs separated from stipulated banking economics.')],
  unavailable_now=['Native upstream execution is not authorized in this review; no runtime is installed or invoked.','Bank and independent institutional acceptance occur later.'],
  reference=ref(BASE/'exact-results.json','Executed project-owned data checks'),native_execution=False))
 write(BASE/'omissions-register.json',dict(items=['THIRD_PARTY_NOTICES, transitive licenses, datasets and selected environment lock remain uninspected.',
  'Underlying process worker, runner, data/cache/output-budget/replay helpers and actual fallback behavior remain uninspected/unexecuted.',
  'Parity builders, CSV/JSON artifacts, R/Stata installations and alias-equivalence tests need exact replay; no numerical result from upstream tests is locally verified.',
  'The separate CLI entrypoint is located but its implementation is uninspected.',
  '45 census originals and four crosscutting searches remain open; no denominator or accepted capability changes.'],
  supersedes_for_statspai=ref(DAY/'proof-statspai-v1/omissions-register.json','Earlier uninspected-source wording remains historical'),native_execution=False))
 write(BASE/'review.json',dict(status='pass_for_bounded_source_contract_review',issues=[],reviewer=dict(name='Codex author/coordinator',kind='author'),
  evidence=[ref(BASE/n,'Reviewed bounded contract') for n in ['source-audit.json','plan-review.json','decision.json','qualification-plan.json','omissions-register.json','exact-results.json','development.tex']]+[ref(Path(__file__),'Review generator')],
  findings=['All11 source blobs authenticated; paper PDF equals its cutoff publisher bytes.',
   'Separate cutoff1.39.0 from paper archive1.23.0.',
   'Four JSON-schema cases and static compact-schema acceptance reproduced without upstream execution.',
   'MCP caller explicitly distinguishes thread and process failure semantics; helper qualification remains open.',
   'Parity grades and scientific targets differ; eight Python-reference entries despite stale two-entry comment.',
   'Conditional adapter is a proposal disposition, not native certification.'],limitations=LIMITS,native_execution=False,visual_acceptance=False,coverage_acceptance=False))
 verify_bindings(read(BASE/'review.json'))
 print(json.dumps(dict(review='pass',source_files=11,additional_citations=2,native_execution=False)))
if __name__=='__main__':main()
