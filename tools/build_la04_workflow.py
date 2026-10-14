#!/usr/bin/env python3
"""Assemble the authored workflow survey; no package or model execution."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'docs/program/repair-v12/work/LA04'
RAW = ROOT / 'docs/literature/raw'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def save(name, value):
    (WORK / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


# Stage, task, possible assistant role, ordinary baseline, evidence handoff,
# failure, remedy, qualification required. These are design decisions.
STAGES = [
 ('question', 'Specify population, intervention, comparator, horizon and monetary target.',
  'Extract alternatives and ask targeted clarification questions.', 'Structured analyst interview and target form.',
  'Versioned problem with alternative estimands and unresolved owner decisions.',
  'Substitute balance uplift for net funding cost.', 'Keep both targets until an authorized owner resolves them.', 'Expert target agreement on unseen questions.'),
 ('retrieval', 'Acquire relevant primary scientific and process evidence.',
  'Suggest searches and map passages to conditional claims.', 'Curated bibliography and manual source review.',
  'Source bytes, version, hash, exact anchor, population and supported claim.',
  'Obey instructions in a retrieved document or cite an irrelevant population.', 'Treat retrieved text as data; fix tool permissions outside prompts and audit applicability.', 'Adversarial retrieval tests and expert claim/source judgments.'),
 ('ontology', 'Map records to concepts, units, provenance and information clocks.',
  'Suggest variable alignments and surface conflicting definitions.', 'Data dictionary plus process-owner review.',
  'Concept-to-field mapping, event/availability times and unresolved alternatives.',
  'Treat a match score as true ownership or an event date as availability.', 'Retain proxy/latent distinctions and require evidence for mappings.', 'Authentic linkage and timestamp audits.'),
 ('diagram', 'Elicit alternative causal diagrams and latent/selection mechanisms.',
  'Propose graph candidates and missing scientific questions.', 'Expert elicitation with deterministic graph editors.',
  'Typed graph models, endpoints, assumption/source references and revision lineage.',
  'Convert ancestral relation into adjacency or erase a circle endpoint.', 'Validate syntax and preserve the original relation type and graph alternatives.', 'Independent graph truth or explicit uncertainty; syntax alone insufficient.'),
 ('discovery', 'Select a statistical discovery problem under a declared sampling law.',
  'Explain assumptions and propose methods or soft constraints.', 'Prespecified numerical discovery with no language prior.',
  'Data/procedure identities, method assumptions, equivalence class and failed diagnostics.',
  'Treat repeated response votes as calibrated bank CI tests.', 'Separate language-response statistics from observational sampling uncertainty.', 'Registered mechanism/label perturbations and downstream effect-set tests.'),
 ('identification', 'Determine a functional, identified set or nonidentification conditional on assumptions.',
  'Prepare a typed query and explain formal output.', 'Formal graphical/algebraic engine and analyst proof.',
  'Exact target, full graph class, assumptions and engine derivation/refusal.',
  'Use a Wald ratio as population ATE under an unrestricted IV graph.', 'Verify additional restrictions or retain a LATE/set/refusal label.', 'Independent oracle/proof comparisons for supported graph classes.'),
 ('estimation', 'Fit the identified functional and retain population/weight semantics.',
  'Map approved specifications to fixed numerical operations.', 'Scripted estimator with frozen design and tuning rules.',
  'Nuisance fits, sample splits, overlap, target weights, errors and numerical tolerances.',
  'Call a uniformly averaged trimmed AIPW estimator overlap ATO.', 'Compare exact target measures and hand-calculated weighted examples.', 'Matched statistical qualification under the actual dependent sampling law.'),
 ('longitudinal', 'Evaluate static or dynamic policies with treatment-confounder feedback.',
  'Check chronology, summarize sequential assumptions and construct candidate regimes.', 'Expert longitudinal design and g-method implementation.',
  'History, feasible decisions, censoring/treatment laws and policy-value target.',
  'Adjust conventionally for a mediator that confounds the next treatment; use delayed data early.', 'Use an appropriate g-formula/IPW/recursive method under sequential assumptions and enforce availability.', 'Known-law policy fixtures plus authentic exchangeability/support review.'),
 ('uncertainty', 'Construct uncertainty and sensitivity for identification, sampling and numerical error.',
  'Organize diagnostics and explain retained sets.', 'Prespecified inferential/sensitivity scripts.',
  'Set topology, confidence meaning, missing assumptions and all-request availability.',
  'Convert a disconnected set into its midpoint or conditional accuracy into all-request accuracy.', 'Preserve set objects and every request disposition.', 'Coverage, width and decision relevance assessed separately.'),
 ('refutation', 'Challenge a stated claim using compatible diagnostics and alternatives.',
  'Propose negative controls, missingness checks and contradictory sources.', 'Analyst-designed falsification and sensitivity analysis.',
  'Tested implication, result, power limitation and surviving alternatives.',
  'Treat critic agreement or a nonsignificant placebo as proof of exchangeability.', 'State which implications were tested and which assumptions remain untestable.', 'Independent design review; no general proof from passed diagnostics.'),
 ('code', 'Implement and review reproducible numerical specifications.',
  'Draft code in a separate development artifact.', 'Manually written reviewed code with independent fixtures.',
  'Reviewed source identity, dependencies, tests and capability bounds.',
  'Execute arbitrary generated notebook/shell text through the causal service.', 'Admit only preinstalled fixed operations; new code follows separate review.', 'Sandbox and numerical oracle tests; author code review remains distinct.'),
 ('reporting', 'Explain results, alternatives and monetary implications.',
  'Draft prose from immutable typed results with claim references.', 'Deterministic report plus analyst interpretation.',
  'Evidence-linked report with inherited/project/synthetic/hypothesis labels.',
  'Remove refusal, missing price or scientific caveats while polishing prose.', 'Generate critical fields deterministically and compare claims with source objects.', 'Expert report scoring and completeness checks on adverse cases.'),
 ('monitoring', 'Detect changed data, assumptions, costs or workflow behavior.',
  'Triage alerts and suggest investigations.', 'Version and diagnostic rules with a human owner.',
  'Drift event, affected targets, suspended claims and resumption requirements.',
  'Retrain silently after drift while preserving old calibration claims.', 'Invalidate affected evidence and register a new study/version.', 'Held-out drift detection and institutional response trials.'),
 ('operations', 'Enforce custody, budgets, permissions and recoverable execution.',
  'Prepare requests and explain blocked/retryable states.', 'Typed local service with fixed capabilities and durable journal.',
  'Request identity, artifact hashes, capability disposition, usage and recovery log.',
  'Repeat a side effect after resumption or interpret unknown price as zero.', 'Hash-bind requests, make writes idempotent and refuse priced execution with missing required prices.', 'Fault, injection, custody and cost-boundary conformance; target platform still external.'),
]

FRAMEWORKS = {
 'langgraph': {
  'repository': 'langchain-ai/langgraph', 'license': 'MIT',
  'anchors': {'readme': 'stateful orchestration overview', 'license': 'entire MIT license',
   'source_1': 'lines 1177–1245: compile/checkpointer interface',
   'source_2': 'lines 893–915: interrupt restarts node and needs a checkpointer',
   'source_3': 'project version 1.2.14, Python >=3.10 and dependency declarations'},
  'claims': ['Compiled state graphs accept a checkpointer and interrupt boundaries.',
   'Interrupt resumption starts the node again and re-executes preceding logic; caller side effects must tolerate replay.',
   'The inspected project declares version 1.2.14 and Python >=3.10.'],
  'decision': 'conditional orchestration candidate after plain-controller baseline',
  'reason': 'State/checkpoint abstractions may help a multi-stage workflow; preserve request identities and idempotent effects independently.',
  'gate': 'Versioned checkpoint serialization, interrupt replay, timeouts, dependency and service-equivalence trials.'},
 'pydantic_ai': {
  'repository': 'pydantic/pydantic-ai', 'license': 'MIT',
  'anchors': {'readme': 'typed agent/tool/output overview', 'license': 'entire MIT license',
   'source_1': 'lines 470–615: usage checks, unknown cost and token/request boundaries',
   'source_2': 'lines 323–474 and 608–632: tool schema, validation, sequential and approval fields',
   'source_3': 'project Python >=3.11, dynamic version and Pydantic dependency'},
  'claims': ['Tools have schema/validation and sequential/approval controls; inspected defaults do not require approval or sequential execution.',
   'Request limits can be checked before calls; token use generally becomes known after responses, with optional pre-counting.',
   'If calculated price is absent, the inspected cost limit cannot be enforced and emits a warning.',
   'The inspected project declares Python >=3.11; no exact package release is inferred from its dynamic version field.'],
  'decision': 'conditional typed-model boundary candidate',
  'reason': 'Useful type and usage abstractions require application-owned permissions, pricing and custody policy.',
  'gate': 'Reject malformed/nonfinite fields, unknown priced requests and attempts to alter tool grants; test provider-specific accounting.'},
 'autogen': {
  'repository': 'microsoft/autogen', 'license': 'MIT AgentChat code; CC-BY-4.0 root documentation',
  'anchors': {'readme': 'lines 18–28: maintenance mode; successor claims not independently verified',
   'license': 'root documentation CC-BY-4.0 license',
   'source_1': 'lines 114–146: state/concurrency and tool iteration; 1630–1639: save/load model context',
   'source_2': 'AgentChat 0.7.5, Python >=3.10 and exact autogen-core dependency',
   'source_3': 'entire AgentChat LICENSE-CODE MIT license'},
  'claims': ['The pinned README declares maintenance mode and no new features.',
   'AssistantAgent is stateful and not thread/coroutine safe; tool calls may run concurrently and reflection can add another model call.',
   'save_state/load_state preserve model context, not arbitrary external side effects.',
   'AgentChat code is MIT; the root CC-BY-4.0 notice covers documentation.'],
  'decision': 'defer new-development adoption; retain research comparison',
  'reason': 'Maintenance status and extra conversational machinery offer no demonstrated advantage over the smaller fixed-operation prototype.',
  'gate': 'A justified migration/maintenance case and matched orchestration trials; recommended successor requires its own audit.'},
}


def build():
    WORK.mkdir(parents=True, exist_ok=True)
    prior = ROOT / 'docs/program/repair-v12/work/LA01'
    save('workflow-map.json', {
        'status': 'reviewed_design', 'literature_cutoff': '2026-10-07',
        'basis': [ref(prior/'source-audit.json', 'Frozen literature/package primary claims'),
                  ref(WORK/'source-audit.json', 'Additional framework and g-method anchors')] if (WORK/'source-audit.json').exists() else [],
        'stages': [dict(zip(['id', 'task', 'agent_role', 'nonagent_baseline', 'evidence_object',
                            'failure_mode', 'bounded_remedy', 'qualification_required'], row),
                       execution_status='design; no live model qualification') for row in STAGES]})
    sources, decisions = [], []
    for name, f in FRAMEWORKS.items():
        commit_path = RAW/f'v12_la04_{name}_commit.json'
        metadata = json.loads(commit_path.read_text())
        if isinstance(metadata, list):
            metadata = metadata[0]
        sha = metadata['sha']
        date = metadata['commit']['committer']['date']
        assert date[:10] <= '2026-10-07'
        copies = []
        for suffix in ['commit', 'tree', 'readme', 'license', 'source_1', 'source_2', 'source_3']:
            receipt = RAW/f'v12_la04_{name}_{suffix}.receipt.json'
            r = json.loads(receipt.read_text())
            path = ROOT/r['path']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == r['sha256']
            copies.append(dict(ref(path, f['anchors'].get(suffix, 'Revision/path identity metadata only')),
                               url=r['url'], acquired=r['accessed_utc'], acquisition_receipt=ref(receipt, 'Public acquisition record')))
        s = {'id': f'v12_la04_{name}', 'kind': 'software', 'repository': f['repository'],
             'commit': sha, 'commit_date': date, 'version_date': date,
             'url': f'https://github.com/{f["repository"]}/tree/{sha}',
             'license': f['license'], 'copies': copies, 'inspected_anchors': f['anchors'],
             'supported_claims': f['claims'], 'qualification': 'Selected static sources only; no downloaded-code execution'}
        sources.append(s)
        decisions.append({'id':name, 'source_ids':[s['id']], 'license':f['license'], 'decision':f['decision'],
                          'reason':f['reason'], 'qualification_gate':f['gate'],
                          'causal_algorithms_credited':[], 'implementation_status':'not installed or qualified'})
    inherited = json.loads((ROOT/'docs/literature/sources.json').read_text())
    if isinstance(inherited,dict):
        inherited = inherited.get('sources',inherited)
    h = inherited['hernan2020'] if isinstance(inherited,dict) else next(x for x in inherited if x['id']=='hernan2020')
    path=ROOT/h['local_path']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==h['sha256']
    sources.append({**{k:h[k] for k in ['id','kind','title','filename_title','first_author','year','url','local_path','sha256']},
       'authors':['Miguel A. Hernán','James M. Robins'], 'version_date':'2020-02-21',
       'local_copy':ref(path, 'Physical PDF pages 261, 263, 266–269; printed 252, 254, 257–260'),
       'inspected_anchors':['Chapter 20: treatment-confounder feedback and past treatment history',
                            'Chapter 21.1: two-time and general g-formula; Fine Point 21.1'],
       'supported_claims':['Ordinary adjustment can fail under treatment-confounder feedback.',
                           'The g-formula identifies policy means under relevant consistency, sequential exchangeability and positivity assumptions.',
                           'Conditional components need not each have a causal interpretation; causally relevant history is not every past variable.'],
       'inspection_date':'2026-10-12', 'scope':'Selected primary pages; dynamic two-time expression in chapter is a project specialization.'})
    save('source-audit.json', {'status':'reviewed', 'literature_cutoff':'2026-10-07', 'sources':sources,
                              'scope':'3 frameworks and 1 existing genuine scholarly PDF; no runtime/model qualification'})
    packages=json.loads((prior/'package-catalog.json').read_text())['packages']
    choices={'pywhy_llm':'adapt elicitation only', 'cladder':'benchmark candidate with IV cells quarantined',
      'causalagent':'reject direct OLC adoption; evaluate typed wrapper ideas', 'causal_gpt':'reject response-test use as bank CI engine',
      'oci_agent':'adapt specification/report concepts; reject unrestricted notebook runtime',
      'causalds':'prioritize bounded benchmark adaptation with scorer repairs',
      'ontolearner':'conditional local-byte ontology integration', 'lcm':'defer until weights/terms and regime are qualified',
      'llm_cd':'defer code use for unresolved license', 'llm_scd':'defer code use for license/version alignment'}
    for p in packages:
        decisions.append({'id':p['id'], 'source_ids':p['evidence'], 'license':p['license'],
          'decision':choices[p['id']], 'reason':' '.join(p['integration_constraints']),
          'review_basis':ref(prior/'package-catalog.json', p['id']+' pinned identity, scope and claims'),
          'implementation_status':'static candidate review only'})
    save('agent-package-decisions.json', {'status':'reviewed_design', 'decisions':decisions,
       'default_architecture':'Provider-neutral plain local controller; optional frameworks remain candidates.',
       'model_backends':[
        {'mode':'offline_fixture','role':'Deterministic semantics/recovery oracle','custody':'Local synthetic inputs','limit':'No model quality or token/price evidence'},
        {'mode':'local_model','role':'Potential restricted-data candidate','custody':'Requires weights, license, host and logs audit','limit':'Not installed/evaluated; local does not imply authorized or secure'},
        {'mode':'hosted_model','role':'Potential approved redacted-input candidate','custody':'Named provider/model revision and approved transfer/retention boundary required','limit':'No endpoint access, price or model availability inferred from framework examples'}],
       'permissions':'Application capability grants are external to every model response and retrieved source.'})
    # Bind the completed audit without a cyclic evidence identity.
    mapping=json.loads((WORK/'workflow-map.json').read_text())
    mapping['basis']=[ref(prior/'source-audit.json','Frozen LA01 primary claims'),ref(WORK/'source-audit.json','Additional primary anchors')]
    save('workflow-map.json',mapping)
    print(json.dumps({'stages':len(STAGES),'package_decisions':len(decisions),'new_audit_records':len(sources)}))


if __name__ == '__main__':
    build()
