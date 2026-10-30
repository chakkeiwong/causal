"""Record actual scoped author readings after the verified graph-source batch."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
OUT = BASE / 'graph-source-064'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def bind(p):
    return dict(path=str(p.relative_to(ROOT)),sha256=sha(p))

def read(p):
    return json.loads(p.read_text())

def save(p,value):
    p.write_text(json.dumps(value,indent=2)+chr(10))

def main():
    audit=read(BASE/'deletion-audit.json');build=read(BASE/'latest-build.json')
    assert build['batch']==54 and audit['status']=='pass'
    assert audit['ledger_sha256']==build['ledger_sha256']==sha(BASE/'edits.json')
    assert not (OUT/'contextual-review.json').exists()
    for name in ['deletion-audit.json','source-verification.json','numerical-verification.json']:
        shutil.copy2(BASE/name,OUT/('verified-'+name))
    manifest=read(BASE/'context-review-168/manifest.json')
    contexts={r['chapter']:r for r in manifest['chapters'] if r['chapter']}
    previous=read(BASE/'context-review-162/manifest.json')
    old=next(r for r in previous['chapters'] if r['chapter']==69)
    edits=read(BASE/'edits.json');expected=(ROOT/old['extract']).read_text()
    for i in [163,168]:
        e=edits[i-1];assert expected.count(e['before'])==1
        expected=expected.replace(e['before'],e['after'],1)
    assert expected==(ROOT/contexts[69]['extract']).read_text()
    component=ROOT/edits[162]['file']
    record=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=54,chapter=69,
        complete_predecessor=dict(extract=old['extract'],sha256=old['sha256']),
        source_context=dict(extract=contexts[69]['extract'],sha256=contexts[69]['sha256']),
        edit_numbers=[163,168],reviewed_source_bindings={str(component.relative_to(ROOT)):sha(component)},
        rendered_text=bind(OUT/'rendered-selections-final.txt'),
        numerics=bind(OUT/'verified-numerical-verification.json'),
        publication=audit['publication']['full'],
        findings=['Complete415-line changed graph component reread; new197-line comparison, preceding expert-ensemble argument and following domain-knowledge bridge reviewed. Exact replay proves all other chapter69 text remains identical to its complete reviewed predecessor.',
            'Error-floor direction, full-distribution versus selected-answer KL, mixture equality, binary branch ambiguity, joint DAG marginals and interval-overlap versus coverage independently checked.',
            'The existing two-world100USD/unit,40USD-cost example supplies the economic consequence. No duplicate simulation, native run, live model call or bank effect is claimed.',
            'Four citation-spacing defects found in rendered review and repaired in edit168; edit167 separately repairs escaped reference/citation commands in chapter27.',
            'Source-reported comparisons retain their reference, unequal information and hidden-confounder/calibration limitations. Version1 and version3 are distinct inspected originals.'],
        scope='Complete predecessor plus exact-replayed, fully read changed component and selected final rendered text. This is not a fresh full4,592-line chapter69 reread.',
        acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
    save(OUT/'component-renewal-069.json',record)
    review=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=54,edits=list(range(163,169)),
        contexts=[contexts[27]],graph_component=bind(OUT/'component-renewal-069.json'),
        rendered_text=bind(OUT/'rendered-selections-final.txt'),
        numerics=bind(OUT/'verified-numerical-verification.json'),
        final_context_snapshot=bind(BASE/'context-review-168/manifest.json'),
        publication=audit['publication'],source_audit=bind(OUT/'source-audit.json'),
        sponsor_rendered=bind(OUT/'sponsor-rendered-final.txt'),
        findings=['Complete477-line chapter27 source and all eight rendered pages read; corrected citation/reference commands verified. Questionnaire, measurement uncertainty, negative results and alternatives preserved.',
            'Sponsor complete source and all four rendered pages reread.89 inspected includes one explicit source-quality quarantine;24 remain unread. No positive scientific admission inferred from quarantine.',
            'Four bibliography entries checked against exact author/version originals and final bibliography text.',
            'Post-build deletion audit retains all505 baseline edits,458 inherited occurrences and1,607 protected identities, with no mathematical, label, citation or distinct numeric loss.'],
        scope='Complete chapter27 and sponsor author reading; chapter69 complete predecessor plus scoped component renewal. Text and geometry review do not substitute for fresh visual or independent acceptance.',
        acceptance=dict(author_context=True,fresh_visual=False,independent=False,release_accepted=False))
    save(OUT/'contextual-review.json',review)
    current=read(BASE/'changed-context-review.json')
    c=contexts[27]
    current['reviews'].append(dict(chapter=27,title=c['title'],status='complete_in_author_scope',
        source_bindings=c['source_bindings'],extract=c['extract'],extract_sha256=c['sha256'],
        review_scope='Complete chapter27 source and all eight rendered pages read against batch054; final rendered pages unchanged from read batch053.',
        findings=review['findings'],publication_batch=54,publication=audit['publication']['full'],fresh_visual_acceptance=False,independent_acceptance=False))
    current.setdefault('exact_component_renewals',[]).append(bind(OUT/'component-renewal-069.json'))
    current['component_review_renewals'].append(bind(OUT/'contextual-review.json'))
    current['current_snapshot']='docs/release/2026-10-29/context-review-168/manifest.json'
    sponsor=current['sponsor_review']
    sponsor.update(scope='Complete current sponsor source and all four rendered pages read; exact final text matches read batch053.',
        publication=audit['publication']['sponsor'],rendered_text=bind(OUT/'sponsor-rendered-final.txt'),review_record=bind(OUT/'contextual-review.json'),
        renewal='Renewed for89 inspected including one quarantine and24 unread; graph-confidence limits align with chapter69. No fresh visual or independent acceptance.')
    sponsor['source_bindings']={n:sha(ROOT/n) for n in sponsor['source_bindings']}
    sponsor['findings'].append('The new source comparison limits graph/effect calibration, and the inspected quarantine is explicitly excluded from positive evidence.')
    save(BASE/'changed-context-review.json',current)
    inventory=read(BASE/'remaining-inventory.json')
    assert inventory['frontier_counts']==dict(inspected=87,unread=26)
    inventory['frontier_counts']=dict(inspected=89,unread=24)
    inventory['inspected_quarantines']=[dict(id='LA01-candidate-202',scope='Quantitative/survey support excluded; source-specific identity and denominator disposition only.',audit=bind(OUT/'source-audit.json'))]
    inventory['scope']='Candidate overlay with four newly read frontier entries since the85/28 baseline, including one explicit quarantine; selected source closures do not establish broad native qualification.'
    row=next(x for x in inventory['reconciliations'] if x['id']=='LA01-candidate-136')
    oldrow=dict(row);row.clear();row.update(id='LA01-candidate-136',prior_disposition=oldrow,source_audit=bind(OUT/'source-audit.json'),
        disposition='Authentic complete thesis now read in claim-bearing sections; graph-confidence and interval-reference comparison integrated. No source experiment independently reproduced.',manuscript_edits=[163,164,165,166,167,168],
        still_required=['Joint graph/effect uncertainty and matched-information comparison before adoption; no native or bank acceptance.'])
    inventory['reconciliations'].append(dict(id='LA01-candidate-202',source_audit=bind(OUT/'source-audit.json'),
        disposition='Inspected source-quality quarantine.10/80 study counts conflict; selected reference identifiers mismatch. No accuracy, time-saving, survey completeness or reproducibility claim admitted.',
        manuscript_edits=[164,165,166,167]))
    inventory['shared_inventory_notice']['scope']='Exact shared original remains preserved. Candidate89/24 admits only independently reviewed and integrated dispositions; one is explicitly quarantined. Later campaign counts are not imported wholesale.'
    inventory['graph_source_integration']=dict(candidate_ids=['LA01-candidate-136','LA01-candidate-202'],supporting_versioned_originals=['rel64chlonone','rel64chlonthree'],batch=54,audit=bind(OUT/'source-audit.json'),review=bind(OUT/'contextual-review.json'))
    save(BASE/'remaining-inventory.json',inventory)
    scope=read(BASE/'review-scope-current.json')
    scope.update(batch=54,ledger_sha256=audit['ledger_sha256'],publication=audit['publication'],
        full_context_records=len(current['reviews']),release_edits=168,
        scope='101 numbered chapters:99 exact complete-context matches and two complete-predecessor/component-renewal chains. Two introductory contexts and preamble separately current.104 author records are not104 unique chapters. No fresh whole-book reread or external acceptance.')
    for name in list(scope['basis']):
        scope['basis'][name]=sha(ROOT/name)
    for p in [OUT/'contextual-review.json',OUT/'component-renewal-069.json',OUT/'source-audit.json',OUT/'exact-witnesses.json']:
        scope['basis'][str(p.relative_to(ROOT))]=sha(p)
    save(BASE/'review-scope-current.json',scope)
    (BASE/'review-scope-current.md').write_text('# Current author-review scope'+chr(10)*2+scope['scope']+chr(10)*2+'Batch054:168 exact edits,56 numerical groups and post-build preservation pass. Graph-source evidence is in graph-source-064. Fresh visual and independent acceptance remain open.'+chr(10))
    summary=read(OUT/'integration.json');summary.update(status='verified_in_author_scope',batch=54,edits=list(range(163,169)),review=bind(OUT/'contextual-review.json'));save(OUT/'integration.json',summary)
    print(json.dumps(dict(batch=54,edits=168,full_context_records=len(current['reviews']),counts=inventory['frontier_counts'])))

if __name__=='__main__':
    main()
