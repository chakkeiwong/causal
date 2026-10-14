#!/usr/bin/env python3
"""Prepare a source-bound gap audit and scoped work graph; never award outcomes."""
import copy
import json
from collections import Counter
from pathlib import Path

import master_control as core

ROOT = core.ROOT
BASE = 'docs/program/comprehensive-v14'
OUT = ROOT / BASE
REVISION = '14.0-scoped-dependency-program'
COVERAGE = 'docs/program/repair-v12/coverage-contract.json'
CHAPTERS = 'docs/program/repair-v12/chapter-plan.json'
PROGRESS = 'docs/program/gap-execution-v13_1/reader/chapter-progress.json'
CELLS = 'docs/program/gap-execution-v13_1/work/SW01/coverage-matrix.json'
CATALOG = 'docs/program/gap-repair-v13/work/SW01/catalog.json'
LITERATURE = 'docs/program/repair-v12/work/LA01/literature-map.json'
OMISSIONS = 'docs/program/repair-v12/work/LA01/omissions.json'
INPUTS = 'docs/program/gap-repair-v13/work/X00/intake-packets.json'


def ref(path, anchor):
    return {'path': path, 'sha256': core.sha(ROOT / path), 'anchor': anchor}


def read(path):
    return core.read(ROOT, path)


def slug(value):
    return value.replace('::', '.').replace(':', '_').replace('++', 'xx')


# Scope-specific review obligations, not assertions about packages.
AREA_CHECKS = {
    'discovery_iid': 'Separate constraint, score, functional and continuous methods; test CI assumptions, acyclicity, scale, orientation convention and equivalence; banking example: a funding DAG with reversed matrix orientation.',
    'discovery_latent': 'Preserve ADMG/CPDAG/PAG endpoints, selection and latent-confounding restrictions; distinguish an equivalence class from a selected DAG; banking example: hidden borrower risk.',
    'discovery_temporal_interventional': 'Specify lags, contemporaneous edges, sampling frequency, stationarity, regimes and intervention types; banking example: funding shocks under common calendars.',
    'identification_counterfactual': 'Separate adjustment from ID/IDC, counterfactual and partial identification; require identified/not-identified/unknown states and graph-class scope; banking example: a lending intervention with hidden confounding.',
    'effects_heterogeneity': 'Match ATE/ATT/CATE/dose-response targets, nuisance learning, cross-fitting, overlap, weighting and inference sampling units; banking example: servicing effects by risk group.',
    'iv_rd_design': 'Inspect exclusion, monotonicity, weak rank, bandwidth and manipulation diagnostics; retain weak-IV sets and discrete running-variable limits; banking example: a credit eligibility threshold.',
    'longitudinal_survival': 'Match treatment histories, time zero, censoring, competing events, positivity and bootstrap failures; banking example: repeated collections with default/prepayment.',
    'policies_offpolicy': 'Separate fixed-policy evaluation, policy selection and unknown optimum; require logger, support and hidden-state scope; banking example: dynamic servicing.',
    'panels_did': 'Inspect cohort/time aggregation, anticipation, treatment reversal, heterogeneous effects, clustering and trend sensitivity; banking example: staggered branch policy rollout.',
    'synthetic_controls': 'Check donor eligibility, spillovers, pre-fit, selection, placebo denominators and donor/time uncertainty; banking example: a treated regional portfolio.',
    'dynamic_panel_timeseries': 'Separate structural from predictive VAR/state-space fits, dynamic-panel instruments, common shocks, local projections and small-date uncertainty; banking example: funding transmission.',
    'networks_interference': 'Declare exposure mappings, network/cluster dependence, missing ties and target intervention; banking example: borrower or branch spillovers.',
    'mediation_sensitivity': 'Distinguish natural/interventional/path-specific targets, cross-world assumptions, negative controls and nonprobabilistic sensitivity sets; banking example: channel-mediated credit response.',
    'transport_missingness': 'Specify target population, selection/measurement models, missingness, support and transport formulas; banking example: moving a pilot across branches.',
    'bayesian_scm_state': 'Separate posterior computation from causal identification; inspect state observability, priors, approximation error and intervention semantics; banking example: hidden credit state.',
    'observations_data': 'Carry identity/ownership, linkage uncertainty, event and availability clocks, inclusion and audit truth; banking example: linked customer observations.',
    'computation_workflow': 'Bind numerical tolerance, job/artifact versions, custody, failure denominators, memory and complete workflow cost; banking example: a restarted causal batch.',
}

INTEGRATION = {
    'one_shared_operation_layer': ('Nine local operation/method scopes execute through a common dispatcher; formulation, discovery and design comparison remain unsupported.', 'Extend only declared methods with explicit capability/refusal records; verify identical core dispatch and scientific context hashes.'),
    'library_cli_mcp_semantic_parity': ('Eleven scientific parity cases and local report/status/cancel exchanges pass; representative cross-language paths remain unqualified.', 'Test every selected operation and adverse request through the library, CLI and pinned MCP client with one reference object.'),
    'artifact_data_custody': ('Local opaque artifacts, hashes, regular-file checks and bounded reads work; bank custody, authentication and multi-tenant boundaries are absent.', 'Prove local artifact/context binding and stale/tampered-input refusal; obtain owner custody requirements for external qualification.'),
    'long_jobs_resume_cancel': ('Local worker interruption, checkpoint restart, idempotency and cancellation are exercised; multi-host recovery is absent.', 'Retain terminal-state semantics; add whole-workload and target-platform failure measurements after genuine workload input.'),
    'schema_version_negotiation': ('MCP 2025-11-25 with SDK 1.27.0 is tested; 2026-07-28 and HTTP/modern metadata are deferred.', 'Review pinned modern primary specifications, produce explicit compatibility decisions, and run negotiation/refusal tests before claiming support.'),
    'graph_and_set_topology': ('Local syntax and result objects preserve selected graph marks and empty/whole-line/disconnected sets; full graph recognition and inference are absent.', 'Add cross-language topology and coordinate counterexamples; preserve unknown identification and distinguish syntax from graph-theoretic validity.'),
    'four_banking_journeys': ('Funding, servicing, discovery-to-effect and trusted observations have designs/fixtures; end-to-end authentic consumer trials are absent.', 'Give each journey its own frozen input, target, sampling law, baseline, diagnostics, loss and refusal examples; qualify each independently.'),
    'standalone_clients': ('Notebook, batch, MCP and service use cases are proposed; selected local CLI/MCP exchange is real.', 'Implement independent local notebook/batch/client fixtures in causal with reproducible setup, input schemas, expected output and failure examples.'),
    'all_workspace_repos_disposition': ('Eighteen directory entries and 53 selected source records were inspected; this was not complete call-chain verification.', 'Refresh every directory disposition and trace only relevant interfaces read-only; place adapters and test fixtures inside causal.'),
    'actual_vs_mocked_execution': ('Receipts distinguish selected local execution from proposals; no actual sibling consumer or cross-language engine qualification.', 'Require engine version/hash and execution journals for runtime labels; retain mock, static, local engine and owner-run consumer labels separately.'),
    'failure_trials': ('Nine local runtime/artifact/replay fault cases pass; bridge, whole-workflow and operator faults remain.', 'Run changed units/context/schema, unsupported methods, killed workers, partial publication and recovery trials with all requests retained.'),
    'signed_adoption_separate': ('No owner adoption is supplied; all twelve external input categories remain empty.', 'Prepare scoped evaluation packages now; accept only authentic owner receipts on an exact release for final adoption.'),
}


def make_audit(state):
    coverage, cells, catalog, progress = read(COVERAGE), read(CELLS), read(CATALOG), read(PROGRESS)
    literature, omissions, inputs = read(LITERATURE), read(OMISSIONS), read(INPUTS)
    receipts = []
    for task in state['work_packages']:
        if task['id'] not in state['results']:
            continue
        binding = state['results'][task['id']]
        receipt = read(binding['path'])
        receipts.append({'id': task['id'], 'outcome': receipt['outcome'], 'scope': receipt['scope'],
                         'limitations': receipt.get('limitations', []), 'evidence': binding})
    audit_cells = []
    for cell in cells['cells']:
        review = cell.get('individual_review', {})
        audit_cells.append({
            **cell, 'audit_evidence_level': 'partially_inspected' if cell['status'] == 'partial_primary_inspection' else 'search_or_candidate_only',
            'qualified': False,
            'remaining_work': review.get('remaining', cell.get('review_finding', 'Individual primary-source and coverage review still required.')),
            'review_obligations': AREA_CHECKS[cell['area']],
            'closure': 'Two complementary search routes, bounded cutoff/omissions, authentic primary source/version/license anchors, alternatives and a reviewed cell disposition. Essential missing sources prevent closure.',
            'source': ref(CELLS, 'cells[id=' + cell['id'] + ']'),
        })
    integration = []
    for key in coverage['integration_requirements']:
        current, action = INTEGRATION[key]
        integration.append({'id': key, 'current': current, 'remaining_work': action,
                            'qualified': False, 'evidence': [ref('docs/program/repair-v12/work/' + x + '/receipt.json', 'scope, limitations and criteria') for x in ('IN01', 'IN02', 'IN04')]})
    scientific = []
    for task in ('R02S', 'R03S', 'R04S', 'R05S'):
        path = f'docs/program/gap-repair-v13/work/{task}/successor-review.json'
        scientific.append({**read(path), 'evidence': ref(path, 'unresolved_design_blockers and next_action')})
    journeys = [
        {'id': 'funding', 'current': 'R01 selected independent-calendar randomized funding law passes; R02 persistent-map/calendar/audit regimes fail.', 'remaining': 'Joint estimated-nuisance uncertainty, verified identity/inclusion, useful precision, real funding workflows and economics.', 'gaps': ['D01', 'D04', 'D05', 'D09', 'D10'], 'research': ['R02S']},
        {'id': 'servicing', 'current': 'R03 selected nonlinear fixed observable policy with truthful full-state audits and supplied logger passes.', 'remaining': 'Hidden-state identification, estimated logger, policy selection, unknown optimum, censoring/support, actual workflow/value.', 'gaps': ['D02', 'D04', 'D06', 'D09', 'D10'], 'research': ['R03S', 'R05S']},
        {'id': 'discovery', 'current': 'R04 selected finite graph class retains truth but useful effect output fails; LA03 is a source/analytical synthesis.', 'remaining': 'Separating information, temporal graph/parameter uncertainty, numerical outer bounds, live LLM effect-level evaluation.', 'gaps': ['D03', 'D04', 'D09', 'D10'], 'research': ['R04S']},
        {'id': 'observations', 'current': 'Linkage/audit constructions and local clock/artifact checks exist; authentic bank labels and assignment truth are absent.', 'remaining': 'Owned measurement/linkage/inclusion law, noisy/selected audits, downstream uncertainty, custody and authentic validation.', 'gaps': ['D01', 'D04', 'D05', 'D08', 'D10'], 'research': ['R02S']},
    ]
    return {
        'revision': REVISION, 'date': '2026-10-12', 'literature_cutoff': '2026-10-07',
        'method': 'Read current contracts, bound receipts, coverage/task/chapter registers, implementation and successor reviews; verify identities. This is an author evidence/coverage audit, not a new technical reinspection of every original or an independent scientific review.',
        'summary': {'recorded_package_outcomes': len(state['results']), 'package_count': len(state['work_packages']),
                    'fully_qualified_original_gaps': 0, 'software_cells': len(audit_cells),
                    'partially_inspected_software_cells': cells['individually_partially_reviewed_cells'],
                    'remaining_individual_software_reviews': cells['remaining_individual_review_cells'],
                    'closed_software_cells': 0, 'catalog_rows_including_aliases': len(catalog['candidates']),
                    'llm_tasks': len(literature['task_families']), 'omissions_by_status': dict(Counter(x['status'] for x in omissions['items'])),
                    'integration_requirements': len(integration), 'partial_chapter_allocations': len(progress['chapters']),
                    'accepted_substantive_pages': None, 'physical_repair_spans': progress['physical_body_pages'],
                    'external_input_categories_missing': len(state['external_inputs']) - len(state['input_receipts'])},
        'software_cells': audit_cells, 'software_candidates': catalog['candidates'],
        'software_alias_relations': catalog.get('family_relations', []),
        'llm_tasks': literature['task_families'], 'llm_omissions': omissions['items'],
        'integration_requirements': integration, 'chapters': progress['chapters'],
        'journeys': journeys, 'streams': state['streams'], 'original_gaps': state['gaps'],
        'scientific_arguments': scientific, 'external_inputs': inputs['inputs'],
        'recorded_outcomes_with_scope': receipts,
        'operational_findings': [
            'Whole-family dependency barriers held up unrelated software comparisons, decisions and adapters.',
            'The old next command repeatedly selected SW01; it had no fair cross-lane operation selection.',
            'Partial source reviews and local prototypes cannot be interpreted as full literature, scientific or product completion.',
            'Physical spans 42/42/12 are below nominal repair minima 100/96/40 even before excluding nonsubstantive content; accepted substantive counts are unmeasured, not zero measured pages.',
            'All 17 commercial cells retain official_primary_unavailable; selected Stata technical material elsewhere does not establish edition-specific comparisons.',
            'Historical controller and README bytes are receipt-bound. Current navigation must name a successor entrypoint without rewriting those bytes.',
            'Rendered visual acceptance is pending under the exhausted inherited image allowance; it affects visual acceptance only.',
        ],
        'audit_inputs': [ref(p, 'Complete register in its stated scope') for p in
                         (COVERAGE, CHAPTERS, PROGRESS, CELLS, CATALOG, LITERATURE, OMISSIONS, INPUTS,
                          'docs/program/repair-v12/work/IN04/review.md', 'docs/program/repair-v12/work/IN01/workspace-inventory.json')],
    }


def build_graph(state, audit):
    nodes, gates = [], {}
    all_outcomes = ['pass', 'negative', 'inconclusive']

    def dep(identifier, outcomes=None, capability=None):
        value = {'id': identifier, 'outcomes': outcomes or ['pass']}
        if capability:
            value['capability'] = capability
        return value

    def node(identifier, lane, parent, title, action, deliverable, criteria, depends=None,
             inputs=None, capabilities=None, study=False, priority=50, evidence=None):
        row = {'id': identifier, 'lane': lane, 'parents': parent if isinstance(parent, list) else [parent],
               'title': title, 'action': action, 'outputs': [f'{BASE}/work/{identifier}/{deliverable}'],
               'criteria': criteria, 'depends': depends or [], 'requires_inputs': inputs or [],
               'capabilities': capabilities or [], 'study': study, 'priority': priority,
               'owner_role': 'Current author/coordinator; external evidence retains its authentic named owner',
               'evidence_start': evidence or [],
               'failure_action': 'Preserve findings and exact evidence. Record a scoped negative/inconclusive outcome or a blocker with acquisition/research trigger. Continue the next ready lane; no automatic phase stop.'}
        nodes.append(row)
        return identifier

    cells_by_area, comparisons, commercial = {}, {}, []
    for c in audit['software_cells']:
        identifier = 'SW.CELL.' + slug(c['id'])
        node(identifier, 'commercial' if c['dimension'] == 'commercial' else 'software', 'SW01',
             c['area'] + ' / ' + c['dimension'] + ' coverage',
             c['remaining_work'] + ' ' + c['review_obligations'], 'coverage-review.json',
             ['Every candidate and alias is identified, searched with a recorded cutoff and bounded stopping rule.',
              'Technical claims have authentic local bytes, hash, version/date, inspected anchors and supported claims; scholarly originals are real correctly named PDFs.',
              'Alternatives and omissions are explicit; no unsupported absence claim or essential unavailable-source waiver.'],
             priority=10 + list(AREA_CHECKS).index(c['area']) * 6 + ['R', 'Python', 'Java', 'C++', 'other_relevant', 'commercial'].index(c['dimension']), evidence=[c['source']])
        cells_by_area.setdefault(c['area'], []).append(identifier)
    gates['SW01'] = [dep(n['id']) for n in nodes if n['id'].startswith('SW.CELL.')]
    families = {'SW02': list(AREA_CHECKS)[:4], 'SW03': list(AREA_CHECKS)[4:6],
                'SW04': list(AREA_CHECKS)[6:8], 'SW05': list(AREA_CHECKS)[8:]}
    for parent, areas in families.items():
        gates[parent] = []
        for area in areas:
            draft = node('SW.COMP.' + area, 'software', parent, 'Develop ' + area + ' comparison',
                         AREA_CHECKS[area] + ' Use inspected evidence now, preserve unknowns, and update as each scoped source is reviewed.',
                         'comparison.md', ['Explain targets, assumptions, diagnostics, defaults, failure paths and substantive alternatives with a reproducible banking example.',
                         'Each claimed behavior has primary evidence; uninspected candidate roles remain explicitly provisional.'])
            deps = [dep(draft)] + [dep(x) for x in cells_by_area[area] if not x.endswith('.commercial')]
            accepted = node('SW.REVIEW.' + area, 'software', parent, 'Review complete ' + area + ' comparison',
                            'Reconcile the completed noncommercial language cells against the developed comparison; resolve contradictions and essential omissions.',
                            'review.json', ['All scoped language cells and comparable alternatives are accounted for with no unresolved essential-source or target mismatch.'], depends=deps)
            comparisons[area] = accepted
            gates[parent].append(dep(accepted))
        # Commercial comparisons have their own readiness and acceptance.
    for area in AREA_CHECKS:
        identifier = node('SW.COMM.' + area, 'commercial', 'SW06', 'Edition-specific commercial comparison: ' + area,
                          'Compare shortlisted vendor editions with our observed current capability, proposed capability and remaining gap. Document vendor strengths, deployment and licensing, quoted/public/unavailable prices and unknown runtime behavior.',
                          'vendor-comparison.json', ['Every shortlisted vendor has original edition/version-specific evidence and a use-case comparison.',
                          'Not evaluated is distinct from absent; no purchase, vendor contact or trial is fabricated; costs are labeled by evidence.'],
                          depends=[dep('SW.CELL.' + area + '.commercial', all_outcomes)])
        commercial.append(identifier)
    gates['SW06'] = [dep(x) for x in commercial]

    candidate_ops = {}
    for c in audit['software_candidates']:
        identifier = 'SW.DECISION.' + slug(c['id'])
        candidate_ops[c['id']] = identifier
        node(identifier, 'reuse', 'SW07', 'Resolve reuse decision: ' + c['name'],
             'Inspect this entry and any canonical alias at a pinned revision. Choose adopt, integrate, port, reference, defer or reject with reasons. An umbrella lead must be resolved into concrete candidates; cite its source and license rather than borrowing family-level approval.',
             'decision.json', ['Bind source/version/license/dependency and maintenance evidence; distinguish alias/lead from a distinct engine.',
             'Explain target/uncertainty semantics, alternatives, costs, owner obligations and revisit trigger.',
             'Grant integration_allowed only for a selected permissible pinned path with a behavioral oracle and documented conversion/failure contract; rejection may finish the decision without enabling an adapter.'],
             capabilities=['integration_allowed'], priority=10 if c['id'] in ('seed:046', 'seed:071', 'inherited:tetrad', 'seed:080') else 50)
    gates['SW07'] = [dep(x) for x in candidate_ops.values()]

    paths = [('R', 'seed:046', 'pcalg R engine'), ('Python', 'seed:071', 'y0 Python identification engine'),
             ('Java', 'inherited:tetrad', 'Tetrad Java engine'), ('Cxx', 'seed:080', 'grf C++ native core with explicit R/native boundary')]
    adapters, trials = [], []
    for language, candidate, name in paths:
        design = node('IN.DESIGN.' + language, 'integration', 'IN03', name + ' adapter contract',
                      'Specify request/result conversion, engine scope, deployment dependencies and numerical oracle inside causal; design is independent of other language paths.',
                      'adapter-contract.json', ['Preserve estimand, graph/set topology, coordinates, units and sampling law; define actionable unsupported responses.'])
        adapter = node('IN.ADAPTER.' + language, 'integration', 'IN03', 'Implement ' + name,
                       'Build the reviewed scoped adapter inside causal, bind actual engine/build identity, and execute deterministic reference and refusal cases.',
                       'adapter-manifest.json', ['Run the actual named engine rather than a fixture stand-in; keep setup and execution logs.',
                       'All conversion and refusal examples pass against independent reference objects.'],
                       depends=[dep(design), dep(candidate_ops[candidate], capability='integration_allowed')], capabilities=['engine_executed'])
        protocol = node('SW.DESIGN.' + language, 'software', 'SW08', 'Matched qualification design: ' + language,
                        'Develop matched target/design comparisons, scientific validity, useful-width/availability, all-failure denominators and whole workflow cost. Exact engine identities must be pinned before registration.',
                        'trial-design.json', ['Reference/oracle is independent of the engine; adverse regimes, threshold rationale, sample size/screen power and stopping rules are specified.',
                        'A reviewed design is not a qualification result.'])
        trial = node('SW.TRIAL.' + language, 'software', 'SW08', 'Execute registered ' + language + ' engine study',
                     'Register the exact prospective path protocol, run all planned requests, retain negative/unavailable cells and compare scientific validity before speed.',
                     'trial-results.json', ['Actual engine identity and fresh-data provenance match the registration; no results-driven threshold changes.',
                     'Report coverage, finite availability, useful width, refusal, numerical loss, complete cost and every failed request.'],
                     depends=[dep(adapter, capability='engine_executed'), dep(protocol)], study=True)
        adapters.append(adapter); trials.append(trial)
    gates['IN03'] = [dep(x, all_outcomes) for x in adapters]
    gates['SW08'] = [dep(x, all_outcomes) for x in trials]

    llm_nodes = []
    for row in audit['llm_tasks']:
        identifier = node('LL.TASK.' + row['id'], 'llm', 'LA07', 'Develop LLM evidence and remedies: ' + row['id'],
                          row['next_action'] + ' Reassess the relevant unresolved candidates, conflicting results and full package paths; keep documented search failures.',
                          'task-synthesis.md', ['Primary frontier evidence, favorable and adverse findings, applicable packages, remedies and remaining research are compared.',
                          'A worked banking question, target/clock, assumptions, failure example and numerical/formal baseline are explained.',
                          'No literature review or offline prototype is labeled live causal performance or bank truth.'],
                          evidence=[ref(LITERATURE, 'task_families[id=' + row['id'] + ']')])
        llm_nodes.append(identifier)
    census = node('LL.CENSUS', 'llm', 'LA07', 'Close bounded frontier search and omission review',
                  'Resolve the 82 relevant and 31 adjacent deferred candidates individually: inspect authentic originals, justify exclusion, or record unavailability/impact. Map all candidates to the 14 tasks; repeat failed longitudinal/off-policy and negative-result searches and record saturation limits.',
                  'search-closure.json', ['Every saved omission has an explicit evidence-backed disposition and task mapping; essential unavailable originals block affected claims.',
                  'Two complementary search routes and citation chaining cover the declared cutoff; never describe bounded search as exhaustive proof.'], evidence=[ref(OMISSIONS, 'items')])
    live_design = node('LL.LIVE.DESIGN', 'llm', 'LA06S', 'Prepare live evaluation and ablations',
                       'Specify task/graph/effect metrics, independent held-out mechanisms, language/label perturbations, prompt/retrieval/data-only/hybrid baselines, abstention, sample-size/screen-power calculations and total cost. Fill exact models and thresholds only from real inputs.',
                       'prospective-design.json', ['Expose unset model revisions, final sample sizes and thresholds; no fake registration or trial.'])
    live = node('LL.LIVE.RUN', 'llm', 'LA06S', 'Run held-out live LLM/agent study',
                'After approved successor argument and prospective registration, execute actual model calls under authentic custody/budget and independent scoring.',
                'results.json', ['All five authentic inputs are bound; exact revisions/prices, independent mechanisms/adjudication and baseline qualification are verified.',
                'Report every request, effect-level error, useful output, contamination checks, uncertainty, time and monetary cost.'],
                depends=[dep(live_design)], inputs=[x['id'] for x in state['external_inputs'] if x['id'].startswith('live_')], study=True)
    gates['LA06S'] = [dep(live)]

    req_nodes = []
    for row in audit['integration_requirements']:
        identifier = node('IN.REQ.' + row['id'], 'integration', 'IN06', 'Develop integration requirement: ' + row['id'],
                          row['remaining_work'], 'requirement-review.json', ['Bind current implementation/design evidence and specify the remaining local and external acceptance cases.',
                          'Supply reproducible local examples where available, with actual/static/mock labels, semantic refusals and remaining owner inputs.'],
                          evidence=row['evidence'])
        req_nodes.append(identifier)
    journey_runs = []
    for journey in audit['journeys']:
        design = node('IN.JOURNEY.DESIGN.' + journey['id'], 'integration', 'IN05', 'Freeze ' + journey['id'] + ' workflow cases',
                      journey['remaining'] + ' Specify local fixed-operation cases, independent references, contract doubles and authentic owner-run cases separately.',
                      'workflow-protocol.json', ['Declare full clock/target/information/sampling/uncertainty/decision chain, all failures and full workflow cost.',
                      'Existing local runtime can be tested without every cross-language adapter; no sibling repository is executed.'])
        run = node('IN.JOURNEY.LOCAL.' + journey['id'], 'integration', 'IN05', 'Run local ' + journey['id'] + ' workflow',
                   'Execute the fixed local operations and explicit unsupported cases after prospective registration, preserving qualifiers and actual failure denominators.',
                   'local-results.json', ['Use available local methods and exact immutable fixtures; do not claim unavailable discovery, policy, adapter or consumer capabilities.',
                   'Retain topology, unknown/refused results, clocks, context hashes and restart behavior.'], depends=[dep(design)], study=True)
        journey_runs.append(run)
    gates['IN05'] = [dep(x, all_outcomes) for x in journey_runs + trials]

    science_nodes = []
    for row in audit['scientific_arguments']:
        task = row['task_id']
        argument = node('SCI.ARGUMENT.' + task, 'research', task, 'Resolve successor argument: ' + task,
                        row['next_action'] + ' Explicit open conditions: ' + ' '.join(row['unresolved_design_blockers']),
                        'argument-and-counterexamples.md', ['Give the exact observation law, target, identifying/uncertainty argument and scope comparison with predecessor failures.',
                        'Prove the feasible component region/rate, or record a counterexample/information requirement with no capability closure.'],
                        evidence=[row['evidence']])
        design = node('SCI.DESIGN.' + task, 'research', task, 'Review ' + task + ' argument and study design',
                      'Evaluate the derivation, independent small reference, failed predecessor regimes, useful-width/availability and certification-screen power before approving a fresh protocol.',
                      'successor-review.json', ['Approve only a supported argument with scope matching the original obligation; preserve negative regimes and all added-information requirements.',
                      'A restricted/oracle success cannot silently replace the broader claim.'], depends=[dep(argument)])
        study = node('SCI.STUDY.' + task, 'research', task, 'Execute registered successor study: ' + task,
                     'Register and run the freshly reviewed protocol, keeping all requests and adverse regimes; stop only this study on an invalid argument or invalidating runtime finding.',
                     'study-results.json', ['Fresh protocol/data and approved successor scope are bound.',
                     'Every planned criterion including validity, availability and usefulness is adjudicated; no uniform guarantee from finite grids.'],
                     depends=[dep(design)], study=True)
        gates[task] = [dep(study, all_outcomes)]
        science_nodes.append(argument)

    for packet in audit['external_inputs']:
        key = packet['input_id']
        node('EXT.PREP.' + key, 'external', packet['affected_tasks'], 'Prepare scoped evidence exchange: ' + key,
             'Adapt the existing intake packet to exact scoped artifacts and acceptance criteria; prepare local validation and handoff files. Owner role: ' + packet['owner_role'] + '. Do not contact anyone or transfer data.',
             'scoped-packet.json', ['Concrete artifact versions, custody, owner role, authentic evidence fields and acceptance criteria are ready for review.',
             'Missing owner/input remains explicit; preparing a packet is not receiving it.'], priority=40)
        node('EXT.VALIDATE.' + key, 'external', packet['affected_tasks'], 'Validate authentic intake: ' + key,
             'Verify received authentic owner evidence, custody, hashes and intended scope before attaching it to an operation; final acceptance still needs the exact released manifest.',
             'input-validation.json', packet['authenticity_and_acceptance_checks'], inputs=[key])
    # External preparation and scoped work never wait for the whole author release.
    for key, inputs, title in [
        ('REVIEW', ['independent_review'], 'Independent review of a scoped candidate artifact'),
        ('BANK', ['bank_truth', 'pilot_and_prices'], 'Authentic bank feasibility and measurement study'),
        ('PLATFORM', ['platform'], 'Target workload and recovery experiment design'),
        ('CONSUMER', ['consumers'], 'Owner-run consumer conformance design'),
        ('ECONOMICS', ['workflow', 'pilot_and_prices'], 'Matched workflow cost and decision-value study design'),
    ]:
        parents = {'REVIEW': ['X01'], 'BANK': ['X02'], 'PLATFORM': ['E01S', 'X03'], 'CONSUMER': ['X03'], 'ECONOMICS': ['X04']}[key]
        node('EXT.SCOPED.' + key, 'external', parents, title,
             'Work against an exact hashed candidate and genuine scoped input now; record findings and reconcile changed claims with I02 at final acceptance. Scope does not authorize external messages or sibling execution.',
             'scoped-review.json', ['Authentic input and exact assessed artifact are bound; scope, findings, unresolved issues and release-reconciliation conditions are explicit.'], inputs=inputs)

    cost_design = node('ECON.DESIGN', 'external', 'X04', 'Freeze matched decision and full cost accounting',
                       'Prepare action/quality/precision criteria, task matching, held-out value estimation and separate acquisition, audit, model, analyst, compute, storage and operating prices. Keep every unfilled price explicit.',
                       'cost-design.json', ['Define economic estimands, counterfactual comparators, uncertainty, losing tasks and actual price provenance; runtime is not treated as labor saving or ROI.'])
    prices = node('ECON.PRICES', 'external', 'X04', 'Validate actual acquisition, audit and workflow prices',
                  'Bind authentic quoted/paid prices and unit definitions to the matched task; retain unknown prices and sensitivity ranges.',
                  'prices.json', ['Owner-supplied prices, units, date and applicability are authenticated; missing costs prevent a measured-TCO claim.'],
                  depends=[dep(cost_design)], inputs=['pilot_and_prices'])
    bank_trial = node('EXT.TRIAL.BANK', 'external', 'X02', 'Run scoped authentic bank validation',
                      'Register the accepted question, observation/assignment/audit law and held-out validation study, then retain precision and eligibility failures for the exact candidate.',
                      'bank-results.json', ['Authentic owners, custody and records are bound; synthetic truth cannot substitute.',
                      'Validate inclusion, clocks, labels and assumptions before causal claims; record ineligible questions.'],
                      depends=[dep('EXT.SCOPED.BANK')], inputs=['bank_truth', 'pilot_and_prices'], study=True)
    platform_trial = node('EXT.TRIAL.PLATFORM', 'external', ['E01S', 'X03'], 'Run target workload and recovery study',
                          'Use an operator-agreed complete workload and exact candidate build for scale, memory, I/O, concurrency, faults and recovery; no unrelated manuscript or language barrier.',
                          'platform-results.json', ['Bind operator input and preregistered complete-workload service criteria.',
                          'Retain multi-host/fault/data-integrity and no-gain results with actual costs.'],
                          depends=[dep('EXT.SCOPED.PLATFORM')], inputs=['platform', 'workflow'], study=True)
    consumer_trial = node('EXT.TRIAL.CONSUMER', 'external', ['IN05', 'X03'], 'Receive and verify owner-run consumer trials',
                          'Register the scoped accepted interface and receive the actual maintainer-run conformance evidence; do not execute or edit sibling repositories.',
                          'consumer-results.json', ['Bind actual consumer/build/adapter identities and genuine owner execution journals.',
                          'Preserve unsupported, whole-line, changed-input, unit/context and partial-publication failures.'],
                          depends=[dep('EXT.SCOPED.CONSUMER')], inputs=['consumers'], study=True)
    economics_trial = node('EXT.TRIAL.ECONOMICS', 'external', 'X04', 'Measure held-out decision value and full economics',
                           'Run matched feasible tasks under the accepted quality/precision and actual cost design, retaining uncertainty and losing tasks.',
                           'economic-results.json', ['Actual prices and held-out decision-value evidence match the declared action and task.',
                           'Show full workflow cost, uncertainty and no-benefit cases; no synthetic ROI claims.'],
                           depends=[dep('EXT.SCOPED.ECONOMICS'), dep(prices), dep(bank_trial), dep(consumer_trial)],
                           inputs=['workflow', 'pilot_and_prices'], study=True)
    gates['E01S'] = [dep(platform_trial)]
    gates['X01'] = [dep('EXT.SCOPED.REVIEW')]
    gates['X02'] = [dep(bank_trial)]
    gates['X03'] = [dep(platform_trial), dep(consumer_trial)]
    gates['X04'] = [dep(economics_trial)]

    chapter_reviews = {'MR01': [], 'MR02': [], 'MR03': []}
    for chapter in audit['chapters']:
        key, repair = chapter['id'], chapter['repair_id']
        parent = {'MR01': 'SW09', 'MR02': 'LA07', 'MR03': 'IN06'}[repair]
        draft = node('TEXT.DRAFT.' + key, 'manuscript', parent, 'Develop chapter ' + key + ': ' + chapter['required_title'],
                     chapter['remaining'] + ' Use the currently inspected corpus and reusable examples; incorporate later findings without blocking current scholarly development.',
                     'chapter.tex', ['A connected scholarly argument explains notation, assumptions, derivations, diagnostics, substantive alternatives and banking consequences.',
                     'All claims are source-audited and reproducible examples identify their evidential status; process logs stay outside the product narrative.'], priority=20)
        reviewed = node('TEXT.REVIEW.' + key, 'manuscript', parent, 'Review chapter ' + key + ' coverage and substantive pages',
                        'Compare the developed chapter with its full allocation, primary-source audit and adjacent chapters; measure substantive pages without duplicate credit.',
                        'chapter-review.json', ['All allocated subject matter is developed; resolve substantive/citation/derivation/notation and contradiction findings.',
                        'Measure standard-typography substantive pages, exclude logs/catalogs/repetition and record any allocation exception for substantive review; physical spans alone do not pass.'], depends=[dep(draft)])
        chapter_reviews[repair].append(reviewed)
    gates['SW09'] = [dep(x) for x in chapter_reviews['MR01']]
    gates['LA07'] = [dep(x) for x in chapter_reviews['MR02'] + llm_nodes + [census]]
    gates['IN06'] = [dep(x) for x in chapter_reviews['MR03'] + req_nodes]
    book = node('RELEASE.ASSEMBLE', 'release', 'I02', 'Continuously assemble the main monograph',
                'As accepted chapter increments arrive, integrate them into one versioned main book with coherent notation and all four journeys. Keep previous PDFs and source identities.',
                'working-book-manifest.json', ['Compile the continuous main document with primary-source, reference, arithmetic and identity checks.',
                'A working build does not supply I02 or scientific acceptance.'])
    sponsor = node('RELEASE.SPONSOR', 'release', 'I02', 'Revise the product and investment proposal',
                   'Update claims, product scope, build/buy/reuse choices, evidence-based uncertainties and economics using the current scoped findings; retain provisional fields.',
                   'sponsor-proposal.pdf', ['Every capability, decision and monetary claim matches the current evidence; distinguish proposal, implemented product and bank adoption.'])
    review = node('RELEASE.RECONCILE', 'release', 'I02', 'Review the complete release against every obligation',
                  'Reconcile all three accepted repairs, chapter allocations, source/claim ledger, sponsor proposal, negative research and all four journeys on the exact release.',
                  'release-review.json', ['No unresolved blocking coverage, citation, arithmetic, contradiction or integration finding remains; all sources and deliveries are hash-bound.'],
                  depends=[dep(book), dep(sponsor)] + [dep(x) for xs in chapter_reviews.values() for x in xs])
    visual = node('RELEASE.VISUAL', 'release', 'I02', 'Inspect the exact rendered release',
                  'Use a fresh image allowance under /home/ubuntu/AGENTS.md; inspect representative and risk-selected rendered pages plus all reported layout findings, repair and rebind exact bytes.',
                  'visual-review.json', ['Record actual rendered inspection of exact release bytes; text extraction and bounds checks are insufficient.'], depends=[dep(review)])
    gates['I02'] = [dep(review), dep(visual)]
    return {'revision': REVISION, 'lanes': ['software', 'reuse', 'commercial', 'llm', 'integration', 'research', 'manuscript', 'external', 'release'],
            'scheduling': 'Least recently served ready lane, then fewest attempts, priority and stable id. One coordinator. A failed/blocked operation does not block unrelated lanes.',
            'phase_policy': 'No phase gates. After every reviewed result or blocker, recompute readiness and continue. Only true operation prerequisites and final acceptance gates can block.',
            'nodes': nodes, 'package_gates': gates, 'qualifies_original_gaps_automatically': False}


def dependency_review(state, graph):
    revised = copy.deepcopy(state['work_packages'])
    drop = {'SW02': {'SW01'}, 'SW03': {'SW01'}, 'SW04': {'SW01'}, 'SW05': {'SW01'},
            'SW06': {'SW02', 'SW03', 'SW04', 'SW05'}, 'SW07': {'SW02', 'SW03', 'SW04', 'SW05'},
            'IN03': {'SW07'}, 'SW08': {'SW07', 'IN03'}, 'IN05': {'IN03'}}
    edges = []
    for task in revised:
        for d in task['depends']:
            removed = d['id'] in drop.get(task['id'], set())
            edges.append({'from': d['id'], 'to': task['id'], 'old_outcomes': d['outcomes'],
                          'disposition': 'replace_with_scoped_operation_evidence' if removed else 'retain_package_acceptance_gate',
                          'rationale': ('Only the matching area, package decision, adapter or registered path is required; unrelated family completion is not causal evidence.' if removed else
                                        'Retained for the package acceptance/rollup; preparation and independently scoped work use the operation graph without waiting for this rollup.'),
                          'replacement': graph['package_gates'].get(task['id'], []) if removed else []})
        task['depends'] = [d for d in task['depends'] if d['id'] not in drop.get(task['id'], set())]
    return {'revision': REVISION, 'scope': 'Every existing package edge reviewed. Only dependencies of unresolved, unregistered packages change; all scientific/coverage/receipt/input/final acceptance criteria remain.',
            'edges': edges, 'removed_broad_edges': sum(x['disposition'].startswith('replace') for x in edges),
            'changed_tasks': list(drop), 'work_packages': revised,
            'retained_final_gates': ['I02', 'X01', 'X02', 'X03', 'X04', 'E01S', 'F01'],
            'operation_edges': [{'from': d['id'], 'to': n['id'], 'outcomes': d['outcomes'],
                                 'capability': d.get('capability'), 'reason': 'Supplies the specific artifact/design/engine required by this operation.'}
                                for n in graph['nodes'] for d in n['depends']]}


def audit_markdown(audit, dependencies):
    summary = audit['summary']
    lines = ['# Comprehensive evidence and gap audit', '', '12 October 2026. Client literature cutoff: 7 October 2026.', '', audit['method'], '',
             '## What completion currently means', '',
             'The program is unfinished: 23 of 48 packages have recorded outcomes, including negative and inconclusive outcomes; zero of ten original gaps is fully qualified. All three mandatory repairs and all 22 chapter allocations remain open. A recorded pass must be read with its actual scope.', '',
             'The current 375-page working monograph has physical repair spans of 42 software, 42 LLM and 12 integration pages. Nominal minimums are 100, 96 and 40, so even the physical shortfalls are at least 58, 54 and 28 pages. These are lower bounds, not an instruction to pad pages. Substantive page counts have not been accepted.', '',
             'Required: every banking use connects decision/clock, model/assumptions, identification/set, estimation, uncertainty/diagnostics, alternatives and money. Author scholarship, runtime/scientific qualification, authentic external acceptance and investment/adoption are separate decisions.', '',
             '## Planning and control defects', '']
    lines += ['- ' + x for x in audit['operational_findings']]
    lines += ['', f'The dependency review replaces {dependencies["removed_broad_edges"]} broad edges across {len(dependencies["changed_tasks"])} unresolved packages with matching operation evidence. It preserves all final release, external-input and investment gates.', '',
              '## All original gaps', '', '| Gap | Observed state | Remaining route and limit |', '|---|---|---|']
    lines += [f"| {x['id']} {x['name']} | {x['current']} | {x['route']} {x['remaining_generalization']} |" for x in audit['original_gaps']]
    lines += ['', '## Four journeys and six streams', '', '| Journey | Evidence now | Missing work |', '|---|---|---|']
    lines += [f"| {x['id']} | {x['current']} | {x['remaining']} |" for x in audit['journeys']]
    lines += ['', 'The six preserved streams are: ' + '; '.join(x['id'] + ' ' + x['name'] for x in audit['streams']) + '.', '',
              '## Software coverage: all 102 cells', '',
              'Thirty cells have partial primary inspection; 72 still need individual review. None is closed. The 115 catalog rows include aliases, umbrella leads, commercial products and generic infrastructure; they are not 115 qualified causal engines. Each row below has a separately addressable work operation. The machine audit preserves its exact candidate IDs, source binding and area-specific checks.', '',
              '| Area / dimension | Evidence level | Specific remaining work |', '|---|---|---|']
    lines += [f"| {x['area'].replace('_', ' ')} / {x['dimension'].replace('_', ' ')} | {x['status'].replace('_',' ')} | {x['remaining_work']} |" for x in audit['software_cells']]
    lines += ['', 'Commercial review covers the recorded Stata, SAS/STAT and Viya, JMP, MATLAB, causaLens/Dara, BayesiaLab, Bayes Server, HUGIN, AgenaRisk, GeNIe/SMILE, Dataiku and DataRobot leads where eligible. Scope is determined by original edition-specific evidence. Public descriptions, advertised features, licensed runtime and measured cost are different evidence levels.', '',
              '## All fourteen LLM and agent tasks', '',
              'All tasks have a bounded primary evidence map; it is not saturation or capability qualification. LA01 inspected selected passages of 26 papers; 82 relevant and 31 adjacent candidates remain deferred. Failed longitudinal/off-policy retrieval and negative-result searches must be retried or dispositioned. LA02 validates declarations; LA03 is source/analytical; LA04 is design; LA05 is a narrow offline static-ATE handoff. LA06 is inconclusive and no final live experiment is registered/executed.', '',
              '| Task | Remaining scientific or implementation gap | Next work |', '|---|---|---|']
    lines += [f"| {x['id'].replace('_', ' ')} | {x['adverse_findings_and_knowledge_gap']} | {x['next_action']} |" for x in audit['llm_tasks']]
    lines += ['', '## All twelve integration requirements', '', '| Requirement | Observed scope | Remaining work |', '|---|---|---|']
    lines += [f"| {x['id'].replace('_', ' ')} | {x['current']} | {x['remaining_work']} |" for x in audit['integration_requirements']]
    lines += ['', '## All twenty-two chapter allocations', '', '| Chapter | Required body pages | Remaining development |', '|---|---|---|']
    lines += [f"| {x['id']}: {x['required_title']} | {x['required_body_pages']['min']}-{x['required_body_pages']['max']} (target {x['required_body_pages']['target']}) | {x['remaining']} |" for x in audit['chapters']]
    lines += ['', 'No shared source chapter or development label earns duplicate page credit. All accepted_substantive_pages fields are currently null. MR01 requires 100-150 pages, MR02 96-112, MR03 an indicative 40-60 plus complete runnable explanations. Exceptions need substantive coverage review, never a silent target reduction.', '',
              '## Four unresolved arguments', '']
    for x in audit['scientific_arguments']:
        lines += ['### ' + x['task_id'], '', ' '.join(x['unresolved_design_blockers']), '', x['next_action'], '']
    lines += ['A composition formula or a research protocol is not a feasible solution. Arguments, independent small references and explicit added-information designs can proceed now; qualification studies require a justified argument, approved scope, screen-power/usefulness rules and fresh registration. Negative or impossible regimes remain visible.', '',
              '## Twelve missing authentic input categories', '', '| Input and owner role | Required evidence | Affected acceptance |', '|---|---|---|']
    lines += [f"| {x['input_id'].replace('_', ' ')}: {x['owner_role']} | {'; '.join(x['needed_artifacts'])} | {', '.join(x['affected_tasks'])} |" for x in audit['external_inputs']]
    lines += ['', 'Each input has an independent preparation and validation operation. None has arrived. Scoped reviews and input validation may precede I02; signed final acceptance must assess the exact I02 release and reconcile any changes. No external contact or sibling execution is authorized by this plan.', '',
              '## Scope of every recorded outcome', '', '| Package and outcome | What the receipt actually covers | Limits retained |', '|---|---|---|']
    lines += [f"| {x['id']} / {x['outcome']} | {x['scope']} | {'; '.join(x['limitations'])} |" for x in audit['recorded_outcomes_with_scope']]
    lines += ['', '## Evidence and limitations of this audit', '',
              'The JSON audit binds the contracts, source registers, receipts, implementation reviews, chapter mapping and intake packets used here. It preserves all 113 deferred-source entries and all 115 software catalog rows. This checks what the evidence warrants and what remains; it does not reread every cited PDF or newly execute all engines. Future operations must inspect their own required primary anchors.', '',
              'Rendered acceptance remains pending. The inherited image budget is exhausted; /home/ubuntu/AGENTS.md says to use a fresh session for further images. This leaves the visual-review operation open while all other eligible work continues.', '']
    return '\n'.join(lines)


def prepare():
    if read(core.STATE).get('revision') == REVISION:
        raise ValueError('Published audit/graph are immutable; use a reviewed successor for changed scope')
    OUT.mkdir(parents=True, exist_ok=True)
    predecessor = OUT / 'predecessor-state.json'
    if not predecessor.exists():
        predecessor.write_bytes((ROOT / core.STATE).read_bytes())
    state = read(str(predecessor.relative_to(ROOT)))
    if 'execution_program' in state:
        raise ValueError('V14 predecessor must be the preserved V13.1 state')
    audit = make_audit(state)
    graph = build_graph(state, audit)
    dependencies = dependency_review(state, graph)
    for name, value in [('gap-audit.json', audit), ('work-graph.json', graph), ('dependency-review.json', dependencies)]:
        core.write(OUT / name, value)
    (OUT / 'gap-audit.md').write_text(audit_markdown(audit, dependencies))
    print(json.dumps({'audit': audit['summary'], 'operations': len(graph['nodes']),
                      'removed_broad_edges': dependencies['removed_broad_edges'], 'changed_packages': dependencies['changed_tasks']}))


if __name__ == '__main__':
    prepare()
