#!/usr/bin/env python3
"""Compare commercial-host synthetic-control evidence without inventing vendor capabilities."""
import json
from pathlib import Path
import sys
import tempfile

import run_program_reviews_v2 as extension
import synthetic_control_contract_reference_20261019 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-19/commercial-synthetic-comparison-v1'
PREVIOUS = ROOT/'docs/program/execution/2026-10-19/commercial-synthetic-controls-v1'
OP = 'SW.COMM.synthetic_controls'
OUTPUT = ROOT/f'docs/program/comprehensive-v14/work/{OP}/vendor-comparison.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())


def local_probe():
    sys.path[:0] = [str(ROOT/'src'), str(ROOT/'tests')]
    from causalbank.operation_service_v12 import OperationService, REQUEST_SCHEMA, SUPPORTED
    from test_operation_service_v12 import context, request
    with tempfile.TemporaryDirectory(prefix='causal-synth-comparison-', dir=ROOT/'.runtime') as tmp:
        service = OperationService(Path(tmp))
        ctx = context()
        ctx['sampling'] = dict(law='dependent_panel', unit='region', fold_unit='region')
        query = request('identify.effect', {'method_id': 'synthetic_control'}, ctx=ctx)
        response = service.invoke(query)
        assert response['disposition'] == 'unsupported'
        return dict(mode='Actual bounded local dispatcher invocation; no commercial runtime',
            request=query, response=response, declared_operations=REQUEST_SCHEMA['properties']['operation']['enum'],
            implemented_profiles=SUPPORTED,
            source=ref(ROOT/'src/causalbank/operation_service_v12.py', 'Declared dispatcher and scientific admission'),
            fixture_source=ref(ROOT/'tests/test_operation_service_v12.py', 'Declared synthetic request context'),
            limit='The dependent-panel synthetic-control request was refused; this is not a repository-wide claim that every relevant research module is absent.')


def main():
    assert not BASE.exists() and not OUTPUT.exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    coverage_path = ROOT/'docs/program/comprehensive-v14/work/SW.CELL.synthetic_controls.commercial/coverage-review.json'
    coverage, audit, omissions = [read(p) for p in [coverage_path, PREVIOUS/'source-audit.json', PREVIOUS/'omissions-register.json']]
    verify_bindings([coverage, audit, omissions])
    assert len(coverage['candidates']) == 6 and len(audit['records']) == 12
    BASE.mkdir()
    write(BASE/'plan-review.json', dict(status='pass_to_execute', reviewer=REVIEWER,
        scope='Documentary six-family comparison with one actual local dispatcher probe',
        plan=['Preserve all six shortlisted families and their actual technical-evidence classes.',
            'Compare documented community-estimator outputs, current common-service behavior and proposed semantic contract.',
            'Keep host, community code, compiled plugin, entitlement, pricing and support distinct.',
            'Record every unmet edition-evidence criterion with a specific independent acquisition route; continue eligible work.'],
        review=['Five families lack matched originals; criterion one cannot pass.',
            'The fixed collector rejected four prior routes. Preserve those failures and do not relax its policy or call failure an absence finding.',
            'A bounded local request can establish its own refusal, not a universal capability inventory.',
            'Native commercial trials and bank data are later prototype/qualification work, not requirements to record a documentary proposal assessment.'],
        evidence=[ref(coverage_path, 'Existing scoped coverage outcome'), ref(PREVIOUS/'source-audit.json', 'Twelve authenticated originals')]))
    probe = local_probe()
    write(BASE/'local-probe.json', probe)
    replay = exact.calculate()
    assert replay == read(PREVIOUS/'exact-results.json')
    write(BASE/'exact-replay.json', replay)
    next_sources = {
        'Stata': 'Obtain dated host-edition and automation/support terms and authoritative clarification of the selected community distribution and optimizer notices; inspect compiled Mata and plugin/source correspondence for a later prototype.',
        'EViews': 'Locate a dated synthetic-control-specific official manual or identified add-in with its author/version/license. The rejected add-in index route establishes no estimator or absence conclusion.',
        'SAS': 'Identify the exact licensed procedure or supported extension and inspect its donor-weighted estimator and uncertainty specification; a real-world-evidence or synthetic-control-arm marketing description does not establish this panel target.',
        'IBM': 'Identify an exact SPSS/other product module or supported extension with primary donor, clock and inference documentation; do not infer this capability from generic regression.',
        'MathWorks': 'Separate official toolbox functionality from File Exchange or separately licensed user code; bind the exact implementation, release compatibility and donor/uncertainty method.',
        'Commercial hosted open-source frontends': 'Name a concrete vendor, service edition and numerical backend; inspect backend pin, source rights, service terms and target-preserving export before making a capability or cost comparison.'}
    vendors = []
    source = next(s for s in audit['sources'] if s['integrated_citation_key'] == 'exec19_synth_stata_source')
    for candidate in coverage['candidates']:
        family = candidate['family']
        selected = family == 'Stata'
        vendors.append(dict(family=family, aliases=candidate['aliases'], evidence_class=candidate['status'],
            implementation_identity=source['version_date'] if selected else 'not established by inspected primary evidence',
            documented_strengths=candidate['documented_scope'], source_records=[source] if selected else [],
            scientific_target='Untreated postintervention trajectory under declared donor, timing and no-interference assumptions; validity is method/design specific.',
            current_service='The actual declared dependent-panel synthetic-control request returns unsupported; see local-probe.json.',
            proposed_service='Typed donor weights, untreated trajectory and gap, effective observation windows, balance, optimizer status and separately justified uncertainty.',
            difference_to_proposal=(
                'Selected community source exposes concrete weight/trajectory/RMSPE computations inside Stata; our inspected common interface refuses the selected panel request. Proposed strict clocks, typed numerical failures and explicit inference remain design obligations.'
                if selected else 'Comparison unknown until a concrete edition-specific estimator and primary contract are identified; no superiority or absence claim.'),
            deployment_and_support=(
                'Commercial Stata host plus community ado/help, compiled plugin and Mata library; a Stata13 command declaration is not verified entitlement, installed-version compatibility or vendor support.'
                if selected else 'Unknown: exact installation, hosting, embedding, automation and support unit not established.'),
            rights=(
                'README GPL>=2 and bundled optimizer proprietary/commercial-use notices remain unresolved; no reuse or redistribution permission granted.'
                if selected else 'Unresolved for the exact product/module/extension and proposed use.'),
            price=dict(status='unavailable', amount=None, currency=None, quotation=None,
                limitation='No authenticated matched price for the relevant edition, options, seats, hosting or support; no zero-cost inference.'),
            runtime=dict(status='not_evaluated', installation=False, purchase=False, contact=False, licensed_trial=False),
            prototype_comparison=['Same treated/donor universe and history', 'Same pre-action predictor/tuning windows and missingness',
                'Explicit optimizer settings and feasible-status check', 'Matched placebo selection and uncertainty target',
                'All-attempt runtime, acquisition and maintenance cost'],
            next_public_evidence=next_sources[family], absence_claim=False))
    write(BASE/'vendor-evidence-matrix.json', dict(vendors=vendors, complete=False))
    evidence = [ref(PREVIOUS/n, 'Preserved authentic source and semantic evidence') for n in
        ['source-audit.json', 'inspected-extracts.json', 'conversion-contract.json', 'omissions-register.json', 'development.tex']]
    evidence += [ref(BASE/n, 'New reviewed comparison evidence') for n in
        ['plan-review.json', 'local-probe.json', 'exact-replay.json', 'vendor-evidence-matrix.json']]
    evidence += [ref(Path(__file__), 'Exact comparison construction and local probe')]
    limits = ['Only one community implementation in a commercial host has selected technical originals; five vendor families remain unresolved.',
        'No exact commercial edition entitlement, authenticated price, qualified rights, vendor runtime or support guarantee.',
        'Original collector rejections remain acquisition failures; no source absence or policy relaxation is inferred.',
        'The local probe establishes one scoped unsupported request only; exact synthetic arithmetic is not bank evidence or inference qualification.',
        'Existing integrated synthetic-control narrative contains the source conclusions; this comparison adds no manuscript-depth credit or final acceptance.']
    trigger = 'Continue the six independent public-evidence actions in vendor-evidence-matrix.json; obtain permitted or user-supplied authentic originals for blocked routes. Licensed execution is a later prototype choice, not a global proposal blocker.'
    comparison = dict(operation_id=OP, status='inconclusive', reviewer=REVIEWER,
        scope='Six-family commercial-host synthetic-control proposal comparison', cutoff='2026-10-07',
        vendors=vendors, current_capability=ref(BASE/'local-probe.json', 'One actual unsupported dependent-panel request'),
        proposed_contract=ref(PREVIOUS/'conversion-contract.json', 'Typed donor, clock, numerical and inference contract'),
        exact_reference=ref(BASE/'exact-replay.json', 'Stipulated gap 20, contaminated 10 and postoutcome-selected 0 thousand USD'),
        narrative=ref(PREVIOUS/'development.tex', 'Already integrated commercial synthetic-control argument'),
        evidence=evidence, limitations=limits, revisit_trigger=trigger, capabilities=[], integration_allowed=False,
        bank_truth_required_for_next_public_research=False)
    write(OUTPUT, comparison)
    criteria = [dict(index=0, verdict='inconclusive', finding='All six families are retained, but matched edition-specific originals exist only for selected community code inside one host; complete vendor comparison remains open.'),
        dict(index=1, verdict='pass', finding='Unknown capabilities, unavailable prices, unresolved rights and unevaluated runtimes stay distinct; no purchase, contact or vendor trial is fabricated.')]
    write(BASE/'review.json', dict(status='inconclusive', reviewer=REVIEWER, criteria=criteria,
        output=ref(OUTPUT, 'Bounded vendor comparison'), evidence=evidence, limitations=limits, revisit_trigger=trigger))
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    receipt.update(outcome='inconclusive', execution='performed', scope=comparison['scope'], reviewer=REVIEWER,
        capabilities=[], outputs=[ref(OUTPUT, 'Contracted commercial comparison')], limitations=limits,
        nonexecution_reason='', revisit_trigger=trigger,
        criteria=[dict(c, evidence=evidence+[ref(BASE/'review.json', 'Author criterion findings')]) for c in criteria])
    write(BASE/'operation-receipt.json', receipt)
    verify_bindings([comparison, receipt])
    print(json.dumps(dict(operation=OP, outcome='inconclusive', vendors=6, technical_originals=12,
        local_panel_request=probe['response']['disposition'], vendor_trials=0, global_blocker=None)))


if __name__ == '__main__':
    main()
