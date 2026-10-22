#!/usr/bin/env python3
"""Bind six inspected official originals and the exact authored workflow reference."""
from copy import deepcopy
import json
from pathlib import Path

import vendor_text_20261013 as extract
import workflow_denominator_reference_20261023 as exact
from acquire_dataiku_workflow_20261023 import REQUESTS
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-23/dataiku-workflow-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-22/computation-commercial-preflight-v1'
read = lambda p: json.loads(p.read_text())

# Line ranges are checked against the independently inspected extracted originals.
SPECS = {
    'latest_flow': ('Dataiku DSS 15: Step-based execution control', [
        (165, 165, 'version 15', 'The mutable current manual identifies DSS 15.'),
        (169, 175, 'downgraded to a warning', 'Default sequential stopping, optional warning downgrade and Ignore failure are documented.'),
        (177, 194, 'ABORTED', 'Never/Always/conditional execution and four scenario outcomes are documented.')]),
    'latest_triggers': ('Dataiku DSS 15: Launching a scenario and trigger handling', [
        (176, 176, 'version 15', 'The mutable current trigger manual identifies DSS 15.'),
        (180, 209, 'changes to the data are not detected', 'Independent triggers, filesystem metadata detection, SQL-query output change and evaluation intervals are documented.'),
        (222, 227, 'doesn’t imply', 'SQL proxy examples and promotion before actual start are distinguished.'),
        (243, 268, 'Suppress triggers while running', 'Default suppression and ignored evaluations during an active run are documented.'),
        (268, 311, 'not covered by run delaying', 'Delay/squash controls, serial throughput and exemptions for time/manual/hidden child triggers are documented.')]),
    'latest_steps': ('Dataiku DSS 15: Scenario steps', [
        (176, 176, 'version 15', 'The mutable current scenario-step manual identifies DSS 15.'),
        (186, 205, 'at least one check', 'Build, deletion by Clear and failure of a selected check are documented.'),
        (234, 236, 'regardless', 'Run another scenario waits, inherits the child outcome and uses the initiating step user regardless of child Run as.'),
        (246, 252, 'Comparing', 'Pytest selection and stable-reference flow integration testing are documented.')]),
    'latest_releases': ('Dataiku DSS: Current release index', [
        (178, 215, 'Version 15.0.2 - September 24th, 2026', 'The index lists 15.2.0 on 15 October, 15.1.0 on 8 October and 15.0.2 on 24 September 2026.'),
        (253, 256, 'Version 15.0.0 - August 14th, 2026', 'DSS 15 existed before the cutoff; feature headings alone do not qualify detailed agent/MCP semantics.')]),
    'dss14_flow': ('Dataiku DSS 14: Step-based execution control', [
        (165, 165, 'version 14', 'The versioned URL identifies the DSS 14 documentation branch.'),
        (169, 194, 'downgraded to a warning', 'The inspected substantive step-control body equals the current DSS 15 body; neither URL supplies immutable patch bytes.')]),
    'dss14_releases': ('Dataiku DSS 14: Release index', [
        (181, 189, 'Version 14.7.5 - Sept 24th, 2026', 'The DSS 14 index lists 14.7.5 on 24 September and 14.7.4 on 10 September 2026; dates establish listed release identity only.')]),
}


def main():
    assert not (BASE / 'source-audit.json').exists(), 'Preserve bound review; use a successor.'
    verify_bindings(read(BASE / 'plan-review.json'))
    sources, reproduced = [], []
    for name, url, _ in REQUESTS:
        receipt_path = BASE / 'acquisition/network' / (name + '.receipt.json')
        receipt = read(receipt_path)
        original = ROOT / receipt['local_copy']
        assert receipt['url'] == url and receipt['returncode'] == 0 and receipt['format_valid']
        assert ref(original, '')['sha256'] == receipt['sha256'] and original.stat().st_size == receipt['bytes']
        document = extract.read(original)
        extracted = BASE / 'extracted' / (name + '.txt')
        links = BASE / 'extracted' / (name + '.links.json')
        assert extracted.read_text() == document.text + '\n'
        assert read(links) == [list(x) for x in document.links]
        lines, anchors = document.text.splitlines(), []
        title, specs = SPECS[name]
        for first, last, token, claim in specs:
            text = '\n'.join(lines[first-1:last])
            assert token in text, (name, first, last, token)
            anchors.append(dict(anchor=f'{name}.txt lines {first}-{last}',
                inspected_text=text, supported_claim=claim))
        sources.append(dict(integrated_citation_key='exec23_dss_' + name,
            kind='official_documentation', title=title, author='Dataiku', year=2026,
            source_identity=url,
            version_date=('DSS 14 branch' if name.startswith('dss14') else 'Mutable DSS 15/latest branch') +
                '; acquired ' + receipt['finished_at'] + '; exact cutoff patch revision unauthenticated',
            local_copy=ref(original, 'Authentic official HTML original'),
            acquisition_receipt=ref(receipt_path, 'Bounded acquisition identity and hash'),
            headers=ref(ROOT / receipt['headers'], 'Observed public response headers'),
            extracted_text=ref(extracted, 'Reproduced inert text'),
            extracted_links=ref(links, 'Reproduced inert links'),
            inspected_anchors=anchors, supported_claims=[a['supported_claim'] for a in anchors],
            limitations=['Current technical observation acquired after the 7 October 2026 cutoff.',
                'Major-version label, release date and equality of two current bodies do not authenticate exact cutoff bytes.',
                'No native vendor test, complete product coverage, licensed entitlement or current price is established.']))
        reproduced.append(dict(id=name, original=ref(original, 'Inspected primary original'),
            extracted=ref(extracted, 'Exact extraction reproduced'), links=ref(links, 'Exact links reproduced')))
    latest = (BASE / 'extracted/latest_flow.txt').read_text().splitlines()[168:194]
    older = (BASE / 'extracted/dss14_flow.txt').read_text().splitlines()[168:194]
    assert latest == older and len(latest) == 26
    write(BASE / 'extraction-review.json', dict(status='pass', evidence=reproduced +
        [ref(Path(extract.__file__), 'Inert HTML text/link extraction')],
        checks=['All six original hashes and response receipts match.',
            'All six saved text and link extractions reproduce exactly.',
            'DSS 14 and DSS 15 substantive step-control bodies match for inspected lines 169-194.'],
        immutable_cutoff_byte_identity=False))
    code = Path(exact.__file__)
    sources.append(dict(integrated_citation_key='exec23_dss_denominator_reference',
        kind='project_evidence_not_scholarly_paper', title='Exact authored workflow denominator and query-proxy counterexamples',
        author='Causal banking proposal project', year=2026, source_identity=str(code.relative_to(ROOT)),
        version_date='23 October 2026; exact authored construction', local_copy=ref(code, 'Finite arithmetic and assumptions'),
        inspected_anchors=[dict(anchor='calculate(): stipulated two-cohort law, cents cross-check and table versions',
            inspected_text=code.read_text())],
        supported_claims=['Fixed-population net -11 USD and available-cohort net +9 USD differ by 20 USD.',
            'Failed, skipped and tolerated-without-effect illustrations retain two requested cases and one returned case.',
            'Assumed missing-cohort effect bounds [-50,50] imply target-net bounds [-21,29].',
            'A row-count/max-date proxy can remain unchanged while the target net changes to +19 USD.'],
        limitations=['Exact stipulated mathematics; not estimated effects, statistical intervals, native vendor runs or bank returns.']))
    write(BASE / 'source-audit.json', dict(cutoff='2026-10-07', sources=sources,
        extraction_review=ref(BASE / 'extraction-review.json', 'Reproduced originals and source anchors')))
    write(BASE / 'exact-results.json', exact.calculate())
    prior = deepcopy(read(PRIOR / 'omissions-register.json'))
    for candidate in prior['candidates']:
        if candidate['family'] == 'Dataiku: Automation scenarios':
            candidate['status'] = 'detailed_current_primary_text_inspected_exact_cutoff_patch_open'
            candidate['evidence'] = ref(BASE / 'source-audit.json', 'Detailed controls, triggers, steps and release indices')
            candidate['next_action'] = ('Authenticate DSS 15.0.2 or another relevant cutoff patch technical revision; '
                'inspect variables, trigger edge cases and relevant API originals as needed. Preserve separate rights, price and native qualification.')
    prior['crosscutting'] = [x for x in prior['crosscutting'] if not x.startswith('Main-reader integration')]
    prior['crosscutting'].append('Integrate this new detailed comparison into the existing workflow chapter and pair the sponsor; earlier six-manual integration is preserved.')
    prior['predecessor_register'] = ref(PRIOR / 'omissions-register.json', 'Unchanged previous candidate and temporal omissions')
    prior['new_temporal_findings'] = dict(dss15_pre_cutoff_release='15.0.2, 24 September 2026',
        later_dss15_releases=['15.1.0, 8 October 2026', '15.2.0, 15 October 2026'],
        dss14_pre_cutoff_release='14.7.5, 24 September 2026',
        exact_cutoff_technical_bytes_authenticated=False)
    write(BASE / 'omissions-register.json', prior)
    findings = [
        'The earlier index-only Dataiku omission is narrowed by inspected detailed controls, triggers and steps.',
        'Default sequential stopping and configurable warning/conditional controls do not themselves determine scientific request completeness.',
        'Suppression, ignored evaluations, squashing and non-delayed trigger types require explicit request/event contracts.',
        'DSS 15 is pre-cutoff; current major-version manuals still do not authenticate exact 15.0.2 bytes.',
        'Exact authored arithmetic exposes a sign reversal when a missing cohort is silently removed.',
        'Query-change detection observes the chosen query; unchanged count/max does not prove unchanged scientific data.',
        'No capability absence, native behavior, bank price or whole-commercial-cell completion is inferred.']
    paths = ['plan.md', 'plan-review.json', 'source-audit.json', 'extraction-review.json',
        'exact-results.json', 'omissions-register.json', 'development.tex', 'sponsor-addition.md']
    evidence = [ref(BASE / n, 'Reviewed bounded source, argument and limits') for n in paths]
    evidence += [ref(Path(__file__), 'Exact author review'), ref(code, 'Independent cents and fraction checks')]
    review = dict(status='pass_with_temporal_and_native_limits', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'), evidence=evidence,
        findings=findings, inspected_official_originals=6, authored_exact_reference=True,
        proposal_acceptance=False, whole_cell_complete=False, integration_allowed=False,
        capabilities=[], native_execution=False, visual_acceptance=False)
    verify_bindings(review)
    write(BASE / 'review.json', review)
    note = dict(finding='Six Dataiku detailed/release originals inspected; exact failed/skipped/tolerated request example shows target net -11 versus available-only +9 USD. Current manuals do not authenticate cutoff patch bytes.',
        next_action='Authenticate the cutoff technical revision (DSS 15.0.2 is listed before cutoff; 15.1/15.2 are later); retain historical omissions for all earlier six manuals. Inspect SAS Viya, Domino and Posit primary originals and complementary market discovery. License, price, native qualification and further trigger/API details remain separate. Integrate only the new detailed Dataiku argument into the next paired release; earlier six-manual and semantic integrations are delivered.',
        evidence=[ref(BASE / n, 'Completed bounded Dataiku inspection') for n in
            ['review.json', 'source-audit.json', 'exact-results.json', 'omissions-register.json']],
        yield_reason='Detailed Dataiku source unit complete; wider commercial-cell obligations remain open and independent work can continue.',
        coverage_acceptance=False, native_execution=False, global_blocker=None)
    verify_bindings(note)
    write(BASE / 'inspection-progress.json', note)
    print(json.dumps(dict(review='pass_with_limits', official_originals=6,
        target_net_usd=-11, available_net_usd=9, native_execution=False, whole_cell_complete=False)))


if __name__ == '__main__':
    main()
