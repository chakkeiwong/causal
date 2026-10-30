"""Bind an observed author reading and reconcile the candidate's residuals."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'standard-review-090'


def read(p):
    return json.loads(p.read_text())


def save(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    build, audit = read(B / 'latest-build.json'), read(B / 'deletion-audit.json')
    assert build['batch'] == 85 and audit['status'] == 'pass'
    assert len(read(B / 'edits.json')) == 290
    assert audit['ledger_sha256'] == sha(B / 'edits.json')
    for pub in audit['publication'].values():
        assert sha(R / pub['path']) == pub['sha256']
    assert not (O / 'contextual-review.json').exists()
    snapshots = {}
    for name in ['docs/reading-edition/editorial-review.md',
                 'docs/reviews/scholarship-reset-2026-10-08.md']:
        target = O / ('standard-' + Path(name).name)
        shutil.copy2(R / name, target)
        snapshots[name] = dict(original_sha256=sha(R / name), retained=bind(target))
    manifest = read(B / 'context-review-290/manifest.json')
    complete = set(range(6, 13)) | {17, 18, 20, 26, 27, 30, 42, 101}
    contexts = []
    for item in manifest['chapters']:
        if item['chapter'] not in complete:
            continue
        assert sha(R / item['extract']) == item['sha256']
        for name, digest in item['source_bindings'].items():
            assert sha(R / name) == digest
        contexts.append({k: item[k] for k in ['chapter', 'title', 'extract',
                                            'sha256', 'lines', 'source_bindings']})
    assert len(contexts) == 15
    observations = [
        'Chapters6–12 and26 were read completely in the immediately preceding continuation. Chapter17 lines1–300 were read there; lines300–1108 here complete that context. Chapters18,20,27,30,42 and101 were read in their complete expanded source contexts here, including nested inputs. This is a bounded central-argument reread, not a fresh101-chapter reading.',
        'The graph/IV/ML sequence now explains the original missing connections through recursive identification, target distinctions, pathwise derivatives and inverse problems. The signed bridge example retains its clipping failure rather than treating an inverse solution as ordinary positive weights.',
        'The longitudinal/state-space sequence distinguishes the observed logger, the intervention, policy information and the marked reward law. Its supported finite cases and exact remainders do not claim universal hidden-state identification.',
        'Chapter17 supplies an actual stationary ratio CLT and covariance construction, distinguishes the general Newey bandwidth theorem from the stronger Gaussian argument, controls a growing fitted-score lag sum, and carries calendar rather than branch counts into funding uncertainty. Weak-IV, near-unit, invalid-exclusion and misspecified-learning failures remain visible.',
        'Chapter18 separates structural invariance from fitting, derives exact irregular sampling and an alias, distinguishes pathwise equilibrium from invariant distributions, includes no-event likelihood terms, and distinguishes mark interventions from changing visit times.',
        'Chapter20 distinguishes causal and ancestral graph objects and follows graph uncertainty into effect sets. Its conservative Gaussian covariance construction, whole-line latent witness and encouragement restriction are separate from a selected temporal graph. Every finite-sample threshold cell and adverse timing-follow-up result remains in the reader.',
        'Chapters30 and42 derive representation and inference obligations rather than relying on schema names: the gradient pullback assumes a fixed transformation, kernels retain support and clocks, unsupported queries differ from nonidentification, and covariance forwarding and orientation have concrete witnesses.',
        'Chapters26/27/101 and the sponsor consistently select a matched small offer-study comparison, preserve expert and commercial alternatives, and distinguish documented capability from native qualification. The26.74-study planning threshold and1.14-million broad tranche are not the new comparison budget. Policy contribution is not incremental software decision value.',
        'The complete rendered conclusion, physical pages1840–1852, and all four sponsor pages were read as text. Printed references, conditional recommendation, source exclusions, outcome dates and useful-answer cost definitions agree with the inspected sources. Earlier selected physical pages2,4,29,52,60,76 were read in the preceding continuation; page4 is contents, not independent body review.',
        'No new mathematical defect or justified substantive deletion was established in this pass. Fifteen central source contexts and selected rendered passages do not certify the entire book. Fresh visual and independent editorial/scientific acceptance remain open.'
    ]
    record = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
        status='complete_in_author_scope', batch=85, ledger=bind(B / 'edits.json'),
        manuscript_edits=[], publication=audit['publication'],
        standard_documents=snapshots, complete_source_contexts=contexts,
        additional_complete_sources=[bind(B / 'source/docs/writing-repair/2026-10-29/src/45358a4637eac946.tex'),
            bind(B / 'source/docs/writing-repair/2026-10-29/sponsor-body.tex')],
        rendered=[dict(**bind(O / 'investment-rendered.txt'), physical_pages=[1840, 1852], complete_chapter=101),
                  dict(**bind(O / 'sponsor-rendered.txt'), physical_pages=[1, 4], complete_sponsor=True),
                  dict(**bind(O / 'selected-rendered-passages.json'), physical_pages=[2, 4, 29, 52, 60, 76], scope='Selected pages; includes contents page4')],
        assessment=bind(O / 'writing-standard-assessment.md'),
        review_currency=bind(B / 'review-currency-current.json'),
        semantic_deletion_assessment=bind(B / 'semantic-deletion-review-current.json'),
        findings=observations,
        scope='Attributed central-argument source and selected rendered-text review. No new primary-source reading, simulation, native execution, fresh visual inspection or independent acceptance.',
        acceptance=dict(author_context=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', record)

    inventory_path = B / 'remaining-inventory.json'
    inventory = read(inventory_path)
    original_path = B / 'source-flexbcf-016/protected-inventory-original.json'
    original = read(original_path)
    assert sha(original_path) == inventory['basis']['sha256']
    admitted = {
        48: 'text-signals-066/source-audit.json',
        136: 'graph-source-064/source-audit.json',
        155: 'source-closure-018/source-audit.json',
        202: 'graph-source-064/source-audit.json',
        206: 'source-closure-018/source-audit.json',
        218: 'energy-integration-071/source-audit.json',
    }
    admitted_ids = {f'LA01-candidate-{i}' for i in admitted}
    old_rows = original['frontier_unread']
    assert len(old_rows) == 28 and admitted_ids <= {r['id'] for r in old_rows}
    residual = [dict(row) for row in old_rows if row['id'] not in admitted_ids]
    assert len(residual) == 22
    inventory['basis'] = dict(**bind(original_path),
        original_live_path=inventory['basis']['path'],
        scope='Exact protected85/28 predecessor. The separately updated live scientific inventory is not the release basis and is not overwritten.')
    inventory['as_of'] = datetime.now(timezone.utc).isoformat()
    inventory['status'] = 'candidate_bound_residuals_final_evidence_revision_pending'
    inventory['candidate_binding'] = dict(batch=85, ledger=bind(B / 'edits.json'), publication=audit['publication'])
    inventory['frontier_unread'] = residual
    inventory['frontier_reconciliation'] = dict(
        starting_counts=original['current_frontier_counts'], denominator=113,
        admitted=[dict(id=f'LA01-candidate-{i}', audit=bind(B / name),
            disposition='inspected_quality_quarantine_not_positive_support' if i == 202 else 'inspected_with_claim_specific_limits')
            for i, name in admitted.items()],
        remaining_counts=dict(inspected=91, unread=22),
        priority_counts=dict(Counter(r['decision_priority'] for r in residual)),
        scope='Only six reviewed release admissions change the fixed frontier. No automatic import from another campaign; supporting originals and the separate energy exclusion do not enlarge the denominator.')
    descriptions = {
        'SW.DECISION.inherited_doubleml': ('Selected6884b5f IRM source and licence/dependency declarations are compared in chapter26; earlier installed0.11.4 matched examples remain version-specific.',
            'Freeze the selected complete distribution/dependencies and qualify the intended target, sampling, weights, folds and adverse cases before broader native admission.'),
        'SW.DECISION.inherited_did': ('Same74b88eb DESCRIPTION is recovered and byte-matched, identifying2.5.1.902 and its declared dependencies. Weight and panel-composition consequences are developed.',
            'Complete the selected R environment and dependency/rights profile; test cohort, aggregation, influence output, changing weights and adverse cases. Do not reacquire the already recovered DESCRIPTION as if absent.'),
        'SW.DECISION.seed_048': ('The1.3.17/ff6059f symbolic identification role, hidden-edge semantics and source date discrepancy are explicit.',
            'Retain the bounded historical identity or resolve the date; obtain complete distribution/rights and matched adjustment, IDC, nonidentification, permutation and failure fixtures.'),
        'SW.DECISION.seed_088': ('Official fixed/random panel capabilities are documented; current R2026b pages are a dated update, not proven pre-cutoff availability.',
            'Establish exact entitlement/version and historical scope if required; compare matched unit/time effects, missing-ID behavior and covariance on an entitled installation. No absent-capability claim follows from the old blocked receipt.'),
        'SW.DECISION.seed_089': ('The named Digital Workers/Factory/System of Work service is compared alongside Dara; advertised scope is distinguished from causal performance.',
            'Specify matched scientific requests, exact deployment/rights/price and independently reconstructed performance; qualify selected Dara conversions before native integration.'),
        'SW.DECISION.seed_092': ('GUI9.8 decision/information semantics, continuous-node restriction, separate conditional-Gaussian family and OEM distribution term are developed.',
            'Resolve dated edition scope and actual order/entitlement, then test the selected discrete decision approximation and matched continuous alternative. Do not repeat the stale assertion that no manual or terms were obtained.'),
    }
    reuse = []
    for row in original['unresolved_reuse_decisions']:
        observed, next_action = descriptions[row['id']]
        reuse.append(dict(id=row['id'], title=row['title'], historical_status=row['status'],
            historical_evidence=row['action_basis'], completed_documentary_comparison=observed,
            candidate_context=bind(B / 'context-review-290/chapter-026.tex'),
            remaining_action=next_action, status='conditional_reuse_not_general_native_admission'))
    inventory['reuse_reconciliation'] = reuse
    inventory['historical_software_inventory'] = dict(rows=len(original['software_cells']),
        status_counts=dict(Counter(row['status'] for row in original['software_cells'])),
        retained_basis=bind(original_path),
        interpretation='Mixed coverage, source, distribution and native obligations; not99 absent chapters. Original receipts remain unchanged; the release comparisons and specific followups do not close every cell.')
    inventory['writing_standard_assessment'] = bind(O / 'writing-standard-assessment.md')
    inventory['author_review'] = bind(O / 'contextual-review.json')
    inventory['release_blockers'] = ['Fresh visual inspection of the exact candidate PDFs',
        'Independent editorial/scientific findings and acceptance',
        'Final evidence revision must include the final assessment/residuals and pass actual relocation']
    inventory['completed_candidate_checks'] = dict(
        manuscript_relocation=bind(B / 'package-verification-batch-085.json'),
        numerical_relocation=bind(B / 'numerical-portability-batch-085/result.json'),
        semantic_deletions=bind(B / 'semantic-deletion-review-current.json'),
        scope='Batch085 is already portable. The remaining package task concerns the new final evidence revision, not an unresolved manuscript reproduction failure.')
    save(inventory_path, inventory)
    save(O / 'residual-reconciliation.json', dict(recorded_utc=inventory['as_of'],
        before=bind(O / 'before-remaining-inventory.json'), after=bind(inventory_path),
        original=bind(original_path), admitted_ids=sorted(admitted_ids), unread_ids=[r['id'] for r in residual],
        software_rows=99, reuse_records=6, no_shared_inventory_write=True,
        no_source_acquisition=True, no_new_native_or_bank_evidence=True))
    rows = ['# Candidate residual inventory', '',
        'Batch085; final evidence revision pending. The exact protected predecessor is preserved and the independently updated scientific inventory is unchanged.', '',
        '## Publication and review', '',
        '- Exact source, numerical and preservation checks pass; batch085 already reproduces after relocation.',
        '- Fresh visual inspection and independent editorial/scientific acceptance remain open.',
        '- Final packaging must carry the new standard assessment and this residual reconciliation.', '',
        '## Unread originals in the fixed frontier', '',
        '91 inspected and22 unread of113 entries. One inspected entry is quarantined. These originals do not support technical claims in this candidate.', '',
        '| ID | Original | Priority |', '|---|---|---|']
    rows += [f"| {r['id']} | {r['title']} | {r['decision_priority']} |" for r in residual]
    rows += ['', 'Exact prior routes, availability limits and next actions are preserved per item in remaining-inventory.json. Separate TCDF and Windmeijer original omissions are not silently added to the frontier denominator.', '',
        '## Software and future qualification', '',
        'The historical99 software rows contain98 inconclusive and1 open result. They mix coverage, source, rights and runtime obligations; they do not count missing chapters. Six reuse decisions now have explicit candidate followups in the JSON. Previously recovered did metadata, MATLAB documentation and HUGIN manual/terms must not be listed as still unacquired.', '',
        'General dependent learning, useful latent/graph effect sets and persistent-linkage precision retain their stated research limits. Native admission, live-model benefit, authentic bank validation, actual prices and institutional adoption remain separate later evidence.', '',
        '[Writing-standard assessment](standard-review-090/writing-standard-assessment.md) · [Exact reconciliation](standard-review-090/residual-reconciliation.json)', '']
    (B / 'remaining-inventory.md').write_text('\n'.join(rows))
    review = read(B / 'review-scope-current.json')
    paths = [O / 'contextual-review.json', O / 'writing-standard-assessment.md',
             O / 'residual-reconciliation.json', O / 'investment-rendered.txt',
             O / 'sponsor-rendered.txt', O / 'selected-rendered-passages.json',
             O / 'selected-rendered-passages.txt', inventory_path, B / 'remaining-inventory.md']
    paths += [R / v['retained']['path'] for v in snapshots.values()]
    paths += [R / c['extract'] for c in contexts]
    for p in paths:
        review['basis'][str(p.relative_to(R))] = sha(p)
    review['standard_assessment'] = bind(O / 'writing-standard-assessment.md')
    review['latest_contextual_review'] = str((O / 'contextual-review.json').relative_to(R))
    review['remaining'] = inventory['release_blockers'] + ['Bounded original-source omissions and explicitly scoped theoretical extensions; no exhaustive survey or universal implementation claim.']
    save(B / 'review-scope-current.json', review)
    with (B / 'execution-log.md').open('a') as stream:
        stream.write('\n## Standard review090 and residual reconciliation\n\n')
        stream.write('Reviewed the original scholarship objections against15 complete central source contexts and the exact rendered conclusion/sponsor. No manuscript edit was justified. Recorded the standard, developed bridges, continuing theory/source limits and separate visual/independent gates. Reconciled22 unread entries from the protected28-entry predecessor and six admitted dispositions; corrected stale documentary tasks without changing shared scientific controls. Batch085 portability and290-edit deletion assessment remain current. Final evidence revision is next.\n')
    print(json.dumps(dict(status='recorded', batch=85, central_contexts=15,
        frontier=dict(inspected=91, unread=22), manuscript_edits=0,
        independent_acceptance=False, fresh_visual_acceptance=False)))


if __name__ == '__main__':
    main()
