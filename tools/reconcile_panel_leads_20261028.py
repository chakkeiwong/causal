"""Disposition ten inherited leads without admitting metadata as technical text."""
import hashlib
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'panel-lead-reconciliation-v1'


def main():
    assert not BASE.exists()
    screening = ROOT / 'docs/program/execution/2026-10-24/panels-r-v1/search-screening.json'
    metadata = ROOT / 'docs/literature/raw/v12_sw_cell_panels_did_r.json'
    audit_path = DAY / 'nested-reader-v2/reader/source-audit.json'
    leads = json.loads(screening.read_text())['candidates']
    originals = {r['id']: r for r in json.loads(metadata.read_text())['results']}
    audit = json.loads(audit_path.read_text())
    sources = {s.get('integrated_citation_key', s.get('id')): s for s in audit['sources']}
    assert len(leads) == 10 and len(originals) == 10
    selected = ['synthdid2021', 'dechaisemartin2024', 'exec24_synth_source', 'exec23_synthdid_reuse_source']
    verified = []
    for key in selected:
        s = sources[key]
        verify_bindings(s)
        if s.get('local_path'):
            p = ROOT / s['local_path']
            assert p.read_bytes().startswith(b'%PDF-')
            assert hashlib.sha256(p.read_bytes()).hexdigest() == s['sha256']
        verified.append(dict(citation_key=key, source_record=s))
    routes = {
        'W4391211929': ('uninspected_original', 'Roth event-study interpretation', 'Resolve the cutoff arXiv edition for 2401.12309, acquire genuine PDF and inspect normalization/plot estimands before borrowing conclusions.'),
        'W2952814763': ('related_work_inspected_exact_edition_distinct', 'Arkhangelsky synthetic DiD', 'Retain inspected arXiv v4 July 2021 and pinned R source. Published AER bytes and specific package behavior remain separate; do not equate records by title alone.'),
        'W3041109582': ('related_work_inspected_metadata_date_conflict', 'de Chaisemartin intertemporal effects', 'Retain inspected arXiv v14 dated 12 May 2026. Metadata says 2021 while the retained citation describes 2024 publication; resolve published edition identity without overwriting the inspected version.'),
        'W1912246770': ('software_inspected_paper_original_missing_from_current_audit', 'Synth JSS original', 'Keep Synth 1.1-10 source review. Acquire genuine JSS v42 i13 original separately; package source and its bibliography do not substitute for that paper.'),
        'W4403617820': ('uninspected_original', 'Multiple treatment events', 'Resolve the cutoff arXiv edition for 2409.05184 and canonical implementation identity, then inspect event timing, overlapping exposure and comparison weights.'),
        'W7165199999': ('uninspected_package_identity', 'Nonabsorbing treatments', 'Resolve nonabsdid CRAN archive/description dated no later than 7 October 2026, source and manual identities; metadata is not evidence that the package or claimed methods are qualified.'),
        'W2740387371': ('uninspected_original_and_package', 'Panel approach pampe', 'Acquire the authentic R Journal 2015-024 original and cutoff pampe source/manual; inspect donor selection, time-series assumptions and inference before comparison.'),
        'W2905789386': ('related_work_family_not_duplicate_edition', 'Synthetic DiD NBER working paper', 'Treat w25532 as a related working-paper edition of the Arkhangelsky family, not additional independent method coverage; match original revision before content equivalence.'),
        'W4391116639': ('uninspected_original', 'Stacked DiD', 'Acquire the genuine cutoff revision of NBER w32054 and canonical code; inspect stack composition, weights, target and cluster inference.'),
        'W2799293184': ('uninspected_original', 'Trend-weighted panel DiD', 'Acquire the authentic CESifo ify013 original using a permitted route; inspect weighting assumptions and support, and identify any canonical software separately.'),
    }
    linked = {'W2952814763': ['synthdid2021', 'exec23_synthdid_reuse_source'],
              'W3041109582': ['dechaisemartin2024'], 'W1912246770': ['exec24_synth_source'],
              'W2905789386': ['synthdid2021', 'exec23_synthdid_reuse_source']}
    rows = []
    for lead in leads:
        identity = lead['identity']
        meta = originals[identity]
        key = identity.rsplit('/', 1)[-1]
        status, family, action = routes[key]
        rows.append(dict(identity=identity, title=lead['title'], metadata_date=lead['date'],
            doi=meta.get('doi'), metadata_authors=[a['author']['display_name'] for a in meta.get('authorships', [])],
            family=family, disposition=status, retained_citation_keys=linked.get(key, []),
            next_action=action, technical_claims_from_metadata=[],
            exact_edition_equivalence_asserted=False, native_execution=False))
    BASE.mkdir()
    evidence = [ref(screening, 'Ten retained metadata leads'), ref(metadata, 'Exact discovery identities; not technical evidence'),
                ref(audit_path, 'Current integrated primary-source records'), ref(Path(__file__), 'Exact bounded reconciliation')]
    write(BASE / 'plan-review.json', dict(status='pass_for_finite_identity_disposition', evidence=evidence,
        checks=['Every retained lead has its own edition and action.', 'Title/DOI similarity creates a family link, not exact-byte equivalence.',
                'Retain acquired original texts and inspected software; never reacquire solely from stale metadata.',
                'New technical original review and broad R-panel coverage remain open.'], awards_acceptance=False))
    write(BASE / 'lead-register.json', dict(status='performed_finite_lead_reconciliation', rows=rows,
        retained_verified_sources=verified, evidence=evidence + [ref(BASE / 'plan-review.json', 'Reviewed scope')],
        newly_acquired_originals=0, related_leads_with_existing_evidence=4, wholly_uninspected_leads=6,
        original_cell_outcome='inconclusive', global_blocker=False, awards_acceptance=False,
        next_action='Run candidate-specific, cutoff-edition acquisition for the six wholly uninspected leads and separately resolve the Synth paper and related-edition identities.'))
    write(BASE / 'author-review.json', dict(status='pass_for_all_ten_lead_dispositions',
        evidence=[ref(BASE / 'lead-register.json', 'All identities, retained sources and exact actions')],
        findings=['Four metadata leads link to existing inspected work with explicit edition or source-type limits.',
                  'Six leads still require genuine technical originals or package identities.',
                  'No new method claim, coverage acceptance or native behavior inferred.'],
        original_outcome_unchanged=True, awards_acceptance=False))
    lines = ['# R-panel lead reconciliation', '',
        'All ten inherited metadata leads have explicit dispositions. Four link to retained primary work; six remain wholly uninspected.',
        'Related editions are not merged by title, and inspected package code does not replace a scholarly paper.', '',
        '| Lead | Disposition | Next action |', '|---|---|---|']
    lines += ['| ' + r['title'] + ' | ' + r['disposition'].replace('_', ' ') + ' | ' + r['next_action'] + ' |' for r in rows]
    lines += ['', 'The original R-panel coverage cell remains inconclusive. These independent source routes do not require bank data or product deployment.', '']
    (BASE / 'reconciliation.md').write_text(chr(10).join(lines))
    print(json.dumps(dict(leads=10, related_to_existing_evidence=4, wholly_uninspected=6, original_cell='inconclusive')))


if __name__ == '__main__':
    main()
