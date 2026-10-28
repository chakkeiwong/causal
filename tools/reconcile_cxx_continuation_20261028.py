"""Preserve scoped C++ findings and exact unresolved source/rights routes."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'cxx-tail-reconciliation-v1'


def main():
    assert not BASE.exists()
    omission_path = ROOT / 'docs/program/execution/2026-10-13/cxx-discovery/omissions-register.json'
    audit_path = DAY / 'nested-reader-v2/reader/source-audit.json'
    omissions = json.loads(omission_path.read_text())
    audit = json.loads(audit_path.read_text())
    sources = {s.get('integrated_citation_key', s.get('id')): s for s in audit['sources']}
    selected = ['exec13_cxx_xges', 'exec13_cxx_lges', 'exec13_cxx_other_leads', 'exec13_cxx_ccdr', 'exec13_cxx_agrum', 'exec13_cxx_openbnsl']
    retained = []
    for key in selected:
        record = sources[key]
        verify_bindings(record)
        retained.append(dict(citation_key=key, record=record))
    # Exact current-source selection is a bounded corpus comparison. It makes no
    # assertion about unindexed local files or new upstream releases.
    bindings = {
        'CXX01': dict(keys=['exec13_cxx_xges', 'exec13_cxx_lges'],
            disposition='Current audited records retain root/derivative terms gaps; no superseding exact grant is established by this bounded comparison.',
            action='For ANazaret/XGES at 3c60d7a2cc3b69cbbdb28ff30be681ecd265101c and CausalAILab/lges at 0fd41f7f2b31fde0607f17c27fe19389457436ad, inspect a permitted exact release/package source grant or an authenticated author grant. Preserve nested GES terms separately. Do not repeat the unchanged license-API 404 route or infer no license exists.',
            alternative='Retain aGrUM/OpenBNSL source comparisons as independently eligible references; their native and dependency qualifications also remain open.'),
        'CXX02': dict(keys=['exec13_cxx_other_leads'],
            disposition='Conditional-entropy and incremental-BN candidate sources remain retained with unresolved grants and full update/score semantics.',
            action='Use retained trees at sama1habibi/Conditional-Entropy-Based-Causal-Discovery 8b28decb7730adf55e18f556b25565ca9aa9e6b6 and tiancity-NJU/Incremental-bayesian-network-structure-learning 412fc6681cebc37fd50dac431c8470317dd5001e to enumerate exact score/update delegates. Obtain documented redistribution terms separately; keep no-adoption until scope is resolved.',
            alternative='Source-only comparison and an independently authored update oracle remain possible without adopting unlicensed source.'),
        'CXX03': dict(keys=['exec13_cxx_other_leads', 'exec13_cxx_ccdr'],
            disposition='Selected experiment, native-kernel and ccdr records survive; complete build/alias/delegate provenance is not established.',
            action='Reconcile Sanaxen/Causal_discovery-Experiment f412f648f2cb5fef434e3a4024184bfa37ace1fe distributed artifacts, godai0519/BayesianNetwork ab72b5fe96f1b648a98b8b659c4cafcfe96d8204 delegated learners, kaixiany/BN_SMC acb13a312c3e8dd0233cb28bd753cc4d08ef0c15 kernels and bryonaragam/ccdrAlgorithm 717d51c3fde3188c0cdbcf0569e2e9a4a8537b97 upstream aliases. Inspect exact unreviewed paths; do not infer current maintenance or algorithmic coverage from names.',
            alternative='Keep inspected Gaussian/categorical comparator boundaries distinct from post-nonlinear and sequential claims.'),
    }
    rows = []
    for row in omissions['essential_gaps']:
        fix = bindings[row['id']]
        rows.append(dict(historical=row, **fix, source_access_closed=False, rights_closed=False, native_execution=False))
    BASE.mkdir()
    evidence = [ref(omission_path, 'Preserved three omission groups'), ref(audit_path, 'Current integrated exact source records'), ref(Path(__file__), 'Bounded current-corpus reconciliation')]
    write(BASE / 'plan-review.json', dict(status='pass_for_bounded_three_group_reconciliation', evidence=evidence,
        checks=['Verify exact current records and keep their version/rights limitations.',
                'Use source-specific next steps rather than blanket acquisition or no-license claims.',
                'Do not treat absence of a later match in this finite audit as proof no local or upstream evidence exists.',
                'Keep independently eligible comparisons separate from rights/native acceptance.'], awards_acceptance=False))
    write(BASE / 'reconciliation.json', dict(status='performed_bounded_reconciliation', operation_id='SW.CELL.discovery_iid.Cxx',
        rows=rows, retained_verified_sources=retained, evidence=evidence + [ref(BASE / 'plan-review.json', 'Reviewed bounds')],
        current_corpus='1438-record integrated source audit; selected candidate families and exact records',
        original_outcome='inconclusive', acquisition_omissions_closed=0, new_originals=0, global_blocker=False,
        limitations=['Full filesystem/upstream search not performed; no universal missing-source or rights conclusion.',
                     'Selected candidate routes remain open and require genuine original terms and technical source inspection.',
                     'No native engine, statistical calibration or causal qualification.'], awards_acceptance=False))
    write(BASE / 'author-review.json', dict(status='pass_for_three_group_disposition',
        evidence=[ref(BASE / 'reconciliation.json', 'Exact preserved identities and bounded actions')],
        original_outcome_unchanged=True, awards_acceptance=False))
    lines = ['# C++ discovery continuation', '',
        'The three historical omission groups remain unresolved after comparison with their current integrated source records.',
        'Their selected originals are retained, and exact candidate revisions now govern the next actions.',
        'A license API failure does not establish absence of a grant. A source review does not establish native capability.', '']
    for row in rows:
        lines += ['## ' + row['historical']['id'], '', row['disposition'], '', row['action'], '', row['alternative'], '']
    lines += ['This is a bounded current-audit reconciliation, not a full repository or upstream absence search. Original coverage remains inconclusive.', '']
    (BASE / 'reconciliation.md').write_text(chr(10).join(lines))
    print(json.dumps(dict(groups=3, retained_records=6, source_gaps_closed=0, original_outcome='inconclusive')))


if __name__ == '__main__':
    main()
