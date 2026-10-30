"""Bind completed text-method contextual reading to the corrected candidate."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
OUT = BASE / 'text-signals-066'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text())

def save(p, value):
    p.write_text(json.dumps(value, indent=2) + chr(10))

def bind(p):
    return dict(path=str(p.relative_to(ROOT)), sha256=sha(p))

def main():
    audit = read(BASE / 'deletion-audit.json')
    build = read(BASE / 'latest-build.json')
    assert build['batch'] == 56 and audit['status'] == 'pass'
    assert audit['ledger_sha256'] == build['ledger_sha256'] == sha(BASE / 'edits.json')
    assert not (OUT / 'contextual-review.json').exists()
    for pub in audit['publication'].values():
        assert sha(ROOT / pub['path']) == pub['sha256']
    for name in ['deletion-audit.json', 'source-verification.json', 'numerical-verification.json']:
        shutil.copy2(BASE / name, OUT / ('verified-' + name))
    manifest = read(BASE / 'context-review-176/manifest.json')
    contexts = {r['chapter']: r for r in manifest['chapters'] if r['chapter']}
    current = read(BASE / 'changed-context-review.json')
    old = next(r for r in current['reviews'] if r['chapter'] == 66)
    edits = read(BASE / 'edits.json')
    indices = [169, 173, 174, 175, 176]
    expected = (ROOT / old['extract']).read_text()
    for i in indices:
        edit = edits[i - 1]
        assert expected.count(edit['before']) == 1
        expected = expected.replace(edit['before'], edit['after'], 1)
    assert expected == (ROOT / contexts[66]['extract']).read_text()
    component = ROOT / edits[168]['file']
    stamp = datetime.now(timezone.utc).isoformat()
    record = dict(
        recorded_utc=stamp, batch=56, chapter=66,
        complete_predecessor=dict(extract=old['extract'], sha256=old['extract_sha256']),
        source_context=dict(extract=contexts[66]['extract'], sha256=contexts[66]['sha256']),
        edit_numbers=indices, reviewed_source_bindings={str(component.relative_to(ROOT)): sha(component)},
        rendered_text=bind(OUT / 'rendered-selections-final.txt'),
        numerics=bind(OUT / 'verified-numerical-verification.json'),
        publication=audit['publication']['full'],
        findings=[
            'Complete current linguistic-measurement component read as source and on physical PDF pages1181–1187, with adjacent transitions. All other chapter66 text reconstructs exactly from its complete reviewed predecessor.',
            'Score-group comparison is distinguished from an intervention; code-specific support, square-root standard error and significance handling retain their inspected scope.',
            'Source-reported term relevance, sentence-level split and test-based checkpoint selection are separated from drug-level evaluation, causal accuracy and bank usefulness.',
            'Authored finite law gives score gap0.36 but causal effect0 and net26 versus minus10USD; treated-population weighting gives ATT0.24 versus ATE0.15 and net4 versus minus5USD.',
            'The sufficient-text alternative, overlap and estimation conditions remain explicit. The published ATT notation mismatch is distinguished from the project derivation; no unseen appendix proof is claimed.',
            'The four demonstrated prose repairs are present in the final rendered text. Prior perception/proxy counterexample, longitudinal g-formula, public-data study and component alternatives remain.'],
        scope='Complete predecessor plus exact-replayed, fully read changed component and final rendered component text. No fresh complete chapter66 reread or repeat of every primary-source reading.',
        acceptance=dict(author_component=True, fresh_visual=False, independent=False, release_accepted=False))
    save(OUT / 'component-renewal-066.json', record)
    review = dict(
        recorded_utc=stamp, batch=56, edits=list(range(169, 177)), contexts=[contexts[27]],
        text_component=bind(OUT / 'component-renewal-066.json'),
        rendered_text=bind(OUT / 'rendered-selections-final.txt'),
        rendered_selection=bind(OUT / 'rendered-selection-map-final.json'),
        numerics=bind(OUT / 'verified-numerical-verification.json'),
        final_context_snapshot=bind(BASE / 'context-review-176/manifest.json'),
        publication=audit['publication'], source_audit=bind(OUT / 'source-audit.json'),
        sponsor_rendered=bind(OUT / 'sponsor-rendered-final.txt'),
        findings=[
            'Complete chapter27 source and physical pages218–226 read. Questionnaire, independent measurement, adverse retrieval and benchmark findings, ORCA limits and formal-procedure alternatives remain.',
            'Complete sponsor source and all four rendered pages read. The fixed frontier is90 inspected including one explicit quarantine, with23 unread; supporting primary-method papers do not enlarge that denominator.',
            'The final comparison is consistent with the earlier measurement-error argument and separates observational prediction, sufficient adjustment and the population receiving the action.',
            'All six added bibliography identities remain in the compiled source audit. This renewal reviews contextual use; the separately bound primary-reading audit owns source-specific claims.',
            'Final build has no unresolved citations, overfull/underfull warnings or detected out-of-page text. Post-build audit reports no mathematical, citation-key, label or distinct numeric loss; all458 inherited occurrences and1607 protected identities survive.'],
        execution_observations=[
            'The default and base Miniforge Python interpreters lack PyMuPDF. Rendered-text extraction used installed pdftotext instead; no dependency installation or visual acceptance was inferred.',
            'Compared selected rendered text against batch055: only physical pages1183 and1185 change. Final text on both was reread.'],
        scope='Complete chapter27 and sponsor author reading; chapter66 complete predecessor plus full changed-component renewal. No fresh whole-book, visual or independent acceptance.',
        acceptance=dict(author_context=True, fresh_visual=False, independent=False, release_accepted=False))
    save(OUT / 'contextual-review.json', review)
    c = contexts[27]
    current['reviews'].append(dict(
        chapter=27, title=c['title'], status='complete_in_author_scope',
        source_bindings=c['source_bindings'], extract=c['extract'], extract_sha256=c['sha256'],
        review_scope='Complete source and nine rendered chapter27 pages read against batch056.',
        findings=review['findings'], publication_batch=56, publication=audit['publication']['full'],
        fresh_visual_acceptance=False, independent_acceptance=False))
    current.setdefault('exact_component_renewals', []).append(bind(OUT / 'component-renewal-066.json'))
    current['component_review_renewals'].append(bind(OUT / 'contextual-review.json'))
    current['current_snapshot'] = 'docs/release/2026-10-29/context-review-176/manifest.json'
    sponsor = current['sponsor_review']
    sponsor.update(scope='Complete current sponsor source and all four final rendered pages read.',
                   publication=audit['publication']['sponsor'],
                   rendered_text=bind(OUT / 'sponsor-rendered-final.txt'),
                   review_record=bind(OUT / 'contextual-review.json'),
                   renewal='Renewed for90 inspected including one quarantine and23 unread; text-method limits align with chapter66. No fresh visual or independent acceptance.')
    sponsor['source_bindings'] = {n: sha(ROOT / n) for n in sponsor['source_bindings']}
    sponsor['findings'].append('Text relevance does not identify an intervention; sufficient adjustment information and target-population weights remain necessary.')
    save(BASE / 'changed-context-review.json', current)
    inventory = read(BASE / 'remaining-inventory.json')
    assert inventory['frontier_counts'] == dict(inspected=89, unread=24)
    inventory['frontier_counts'] = dict(inspected=90, unread=23)
    inventory['scope'] = 'Candidate overlay with five newly inspected fixed-frontier entries since85/28, including one explicit quarantine. Supporting method originals are separate from the fixed frontier; native and bank qualification remain open.'
    inventory['reconciliations'].append(dict(
        id='LA01-candidate-48', source_audit=bind(OUT / 'source-audit.json'),
        disposition='Authentic pharmacovigilance original read with its two primary methods and a sufficient-text alternative. Term relevance and score contrasts do not identify a banking intervention; source formula/reference discrepancies are explicit.',
        manuscript_edits=list(range(169, 177)),
        still_required=['Independent source-experiment reproduction, matched-information evaluation and causal identification before any bank-effect or native-qualification claim.']))
    inventory['shared_inventory_notice']['scope'] = 'Exact shared original remains preserved. Candidate90/23 admits only reviewed and integrated dispositions; one is explicitly quarantined. Other campaign counts are not imported wholesale.'
    inventory['text_source_integration'] = dict(
        candidate_ids=['LA01-candidate-48'], supporting_originals=['rel66inferbert', 'rel66deepcausality', 'rel66veitch'],
        batch=56, audit=bind(OUT / 'source-audit.json'), review=bind(OUT / 'contextual-review.json'))
    save(BASE / 'remaining-inventory.json', inventory)
    scope = read(BASE / 'review-scope-current.json')
    scope.update(batch=56, ledger_sha256=audit['ledger_sha256'], publication=audit['publication'],
                 full_context_records=len(current['reviews']), release_edits=176, edits=176,
                 numerical_groups=57, latest_contextual_review=str((OUT / 'contextual-review.json').relative_to(ROOT)),
                 latest_rendered_review=str((OUT / 'contextual-review.json').relative_to(ROOT)),
                 scope='101 numbered chapters:98 exact complete-context matches and three complete-predecessor/component-renewal chains. Two introductory contexts and preamble separately current.105 author records are not105 unique chapters. No fresh whole-book reread or external acceptance.')
    for name in list(scope['basis']):
        scope['basis'][name] = sha(ROOT / name)
    for p in [OUT / 'contextual-review.json', OUT / 'component-renewal-066.json', OUT / 'source-audit.json', OUT / 'exact-witnesses.json']:
        scope['basis'][str(p.relative_to(ROOT))] = sha(p)
    scope['portable_package_current'] = False
    scope['numerical_package_current'] = False
    save(BASE / 'review-scope-current.json', scope)
    (BASE / 'review-scope-current.md').write_text('# Current author-review scope' + chr(10)*2 + scope['scope'] + chr(10)*2 + 'Batch056:176 exact edits,57 numerical groups and post-build preservation pass. Text-method evidence is in text-signals-066. Packages require renewal; fresh visual and independent acceptance remain open.' + chr(10))
    summary = read(OUT / 'integration.json')
    summary.update(status='verified_in_author_scope', batch=56, edits=list(range(169,177)), review=bind(OUT / 'contextual-review.json'))
    save(OUT / 'integration.json', summary)
    print(json.dumps(dict(batch=56, edits=176, full_context_records=len(current['reviews']), counts=inventory['frontier_counts'])))

if __name__ == '__main__':
    main()
