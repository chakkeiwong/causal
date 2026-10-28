"""Reconcile named source tails without changing broad acceptance outcomes."""
import hashlib
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'software-tail-java-panel-delta-v1'


def main():
    assert not BASE.exists(), 'Preserve the recorded reconciliation.'
    historical = ROOT / 'docs/program/execution/2026-10-13/java-discovery/omissions-register.json'
    old = json.loads(historical.read_text())
    assert {r['id'] for r in old['essential_gaps']} == {'JAVA01', 'JAVA02', 'JAVA03', 'JAVA04'}
    reviews = {}
    for name in ('weka', 'banjo', 'tetrad-bridge'):
        path = ROOT / f'docs/program/execution/2026-10-24/{name}-reuse-v1/operation-receipt.json'
        receipt = json.loads(path.read_text())
        verify_bindings(receipt)
        assert receipt['outcome'] == 'pass'
        reviews[name] = ref(path, 'Retained later reference-only decision; no native qualification')
    java = DAY / 'aitiotita-delegates-v1/author-review.json'
    verify_bindings(json.loads(java.read_text()))
    panels = ROOT / 'docs/program/execution/2026-10-24/panels-r-v1'
    receipt = json.loads((panels / 'operation-receipt.json').read_text())
    verify_bindings(receipt)
    assert receipt['outcome'] == 'inconclusive'
    remaining = json.loads((DAY / 'program-refresh-fixture-java-v1/remaining-operations.json').read_text())
    index = {r['id']: r for r in remaining['operations']}
    assert len(index) == 150
    assert index['SW.CELL.discovery_iid.Java']['status'] == 'inconclusive'
    assert index['SW.CELL.panels_did.R']['status'] == 'inconclusive'
    rows = [
        dict(id='JAVA01', status='partly_addressed_official_identity_open',
             completed='The 24 October review authenticates 18 selected historical mirror originals and retains a predictive/reference-only decision.',
             remaining='Authentic official cutoff release, binary/source equality, remaining delegates, complete dependencies/rights and native qualification.',
             next_action='Use a newly permitted official-source route or retained authentic official original; do not repeat the selected mirror review or unchanged denied-host request.',
             evidence=[reviews['weka']]),
        dict(id='JAVA02', status='partly_addressed_original_rights_open',
             completed='The 24 October review authenticates 21 selected derivative originals, exact authored witnesses and a reference-only decision.',
             remaining='Original official release and rights, full derivative changes/dependencies, remaining preprocessing/cache/export paths and native qualification.',
             next_action='Obtain an authentic permitted official identity/rights source and review remaining named delegates; retain the 21-file derivative findings.',
             evidence=[reviews['banjo']]),
        dict(id='JAVA03', status='named_source_access_addressed_broad_qualification_open',
             completed='All seven omitted oracle/orientation/graph/test/entrypoint originals have pinned-blob verification and inspected primary anchors; both current PDFs integrate the findings.',
             remaining='Oracle domain and shortcut validity, tie and propagation policy, enforcing presets, transitive rights, native numerical/statistical and operating qualification.',
             next_action='Do not reacquire the seven originals or rerun the 48-case fixture. Derive the intended oracle/orientation contract before a scoped port; keep local checks distinct from native qualification.',
             evidence=[ref(java, 'Seven inspected pinned originals'), ref(DAY / 'aitiotita-delegates-v1/remaining-gaps.json', 'Specific remaining semantics and qualification'), ref(DAY / 'fixture-java-reader-v1/working-release.json', 'Integrated findings')]),
        dict(id='JAVA04', status='nested_engine_and_lineage_review_still_open',
             completed='Cutoff reliableAI tree navigation and umbrella README are saved. Later Tetrad and bridge decisions remain separate evidence.',
             remaining='Nested BLIP and Spot exact license, implementation and tests; origin/derivative identity and compiled-artifact provenance; remaining Tetrad lineage resolution.',
             next_action='Use the saved 2 September 2026 reliableAI commit/tree to register selected nested license, score/search, graph-conversion and test originals. Compare lineages without double counting; do not execute setup scripts or JARs.',
             evidence=[ref(ROOT / 'docs/literature/raw/v12_exec13_java_reliableai_commit.json', 'Cutoff commit navigation'), ref(ROOT / 'docs/literature/raw/v12_exec13_java_reliableai_tree.json', 'Nested paths and blobs; not implementation evidence'), reviews['tetrad-bridge']]),
        dict(id='SW.CELL.panels_did.R', status='later_scoped_review_retained_coverage_tails_open',
             completed='The 24 October seven-family comparison and inspected did delegates remain the current action basis.',
             remaining='Nonabsorbing, multiple-event, stacked, panel-approach and trend-weighting leads; remaining slow/custom/helper delegates, installed dependencies and matched public fixture design.',
             next_action=receipt['revisit_trigger'],
             evidence=[ref(panels / 'operation-receipt.json', 'Latest scoped R panel receipt'), ref(panels / 'search-screening.json', 'Ten metadata leads are discovery only'), ref(panels / 'omissions-register.json', 'Known routes and scientific information limits')]),
    ]
    BASE.mkdir()
    write(BASE / 'plan-review.json', dict(
        status='pass_for_bounded_reconciliation', scope='Four historical Java groups and one later R-panel continuation',
        evidence=[ref(historical, 'Historical groups'), ref(DAY / 'program-refresh-fixture-java-v1/remaining-operations.json', 'All 150 unresolved IDs'), ref(DAY / 'followup-runtime-v1/software-tails.json', '104-row trace; full later-artifact reconciliation unfinished'), ref(Path(__file__), 'Exact reconciliation logic')],
        checks=['Check bound later receipts before assigning dispositions.', 'Separate source access, reference/reuse decision and broad capability qualification.', 'Retain all original nonpassing outcomes; no absent-capability claim from metadata.', 'Leave the other 102 software/reuse rows explicitly unreconciled here.'],
        awards_acceptance=False,
    ))
    write(BASE / 'source-tail-delta.json', dict(
        status='performed_bounded_delta_reconciliation', rows=rows,
        software_reuse_trace_rows=104, traced_operation_rows_reconciled_here=2, other_trace_rows=102,
        original_nonpassing=150, original_outcomes_unchanged=True,
        evidence=[ref(BASE / 'plan-review.json', 'Reviewed scope')],
        new_public_sources=0, new_native_execution=False, final_acceptance=False,
    ))
    text = '''# Source-tail reconciliation after crash recovery

The four historical Java omission groups have different dispositions. JAVA03's
seven named source-access omissions are addressed and integrated into the current
paired PDFs. Its scientific and native qualification remains open. Weka's 18-file
historical-mirror review and Banjo's 21-file derivative review already exist;
neither authenticates a missing official release or grants complete rights.
Retain those later reviews instead of restarting the old source requests.

JAVA04 remains a concrete independent source route. The saved reliableAI cutoff
tree names nested BLIP and Spot sources, licenses, conversion helpers, tests and
compiled artifacts. Navigation alone supplies no technical claim about them.
Register exact pinned text originals before inspecting implementation; do not run
the setup script, imported engines or JAR. Keep the later Tetrad bridge decision
separate from nested-engine and binary identity.

The R panel action basis is the 24 October seven-family review. Its next work is
the named nonabsorbing, multiple-event, stacked, panel-approach and trend-weighting
leads and remaining slow/custom/helper delegates. The inherited ten-result search
contains metadata leads, not inspected technical originals. Unknown untreated
trends and missing counterfactuals still need justified restrictions or new
information; a public fixture cannot certify those assumptions in a bank.

This is a bounded reconciliation of two of the 104 software/reuse operation rows,
with four Java subgroups. The other 102 rows still need their own later-evidence
comparison. All 150 original nonpassing obligations remain. There is no new
software, family-coverage, visual, bank or proposal acceptance here.
'''
    (BASE / 'reconciliation.md').write_text(text)
    report = json.loads((BASE / 'source-tail-delta.json').read_text())
    verify_bindings(report)
    write(BASE / 'author-review.json', dict(
        status='pass_for_bounded_delta_only', rows=len(rows),
        evidence=[ref(BASE / 'source-tail-delta.json', 'Verified exact later action bases'), ref(BASE / 'reconciliation.md', 'Readable findings')],
        criterion='No completed selected source review is reset; source-access completion grants no broad qualification.',
        original_outcomes_unchanged=True, final_acceptance=False,
    ))
    print(json.dumps(dict(performed='named Java and R panel source-tail delta', software_rows=2, java_groups=4, other_trace_rows=102, original_nonpassing=150, awards_acceptance=False)))


if __name__ == '__main__':
    main()
