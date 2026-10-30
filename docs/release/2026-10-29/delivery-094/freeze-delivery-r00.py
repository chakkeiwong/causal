"""Freeze a versioned final-integration manifest without altering packages."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import sys

R=Path(__file__).resolve().parents[1]
B=R/'docs/release/2026-10-29'
D=B/'delivery-094'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def save(p,d): p.write_text(json.dumps(d,indent=2)+'\n')

def freeze(revision):
    target=D/f'manifest-r{revision:02d}.json'
    if target.exists(): raise SystemExit('Refuse to overwrite frozen delivery manifest')
    snapshot=D/f'controls-r{revision:02d}';snapshot.mkdir(exist_ok=False)
    controls=['CURRENT.md','docs/mission-control.md','docs/mission-control.html','docs/program/master-live.md','docs/program/release-programme-2026-10-29.md','docs/release/2026-10-29/state.json','docs/release/2026-10-29/review-scope-current.json','docs/release/2026-10-29/remaining-inventory.json','docs/release/2026-10-29/remaining-inventory.md','docs/release/2026-10-29/execution-log.md']
    identities={};control_refs={}
    for path in controls:
        p=snapshot/path;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/path,p)
        rel=str(p.relative_to(R));identities[rel]=sha(p);control_refs[path]={'snapshot':rel,'sha256':sha(p)}
    relative_evidence=[
        'edits.json','full-deletion-ledger.md','deletion-audit.json','semantic-deletion-review-current.json',
        'review-currency-current.json','source-verification.json','numerical-verification.json','latest-build.json',
        'package-verification-batch-086-r01.json','portability-batch-086-r01/result.json',
        'portability-batch-086-r01/preservation-replay.json','portability-batch-086-r01/adversarial-preservation.json',
        'numerical-portability-batch-086-r01/result.json',
        'packages/batch-086-r01/manifest.json','packages/batch-086-r01/SHA256SUMS','packages/batch-086-r01/README.md',
        'numerical-packages/batch-086-r01/manifest.json','numerical-packages/batch-086-r01/README.md',
        'closing-review-092/contextual-review.json','closing-review-092/semantic-deletion-review.json',
        'standard-review-090/writing-standard-assessment.md',
        'final-readiness-093/writing-standard-current.md','final-readiness-093/contextual-review.json',
        'final-readiness-093/review.md','final-readiness-093/reviewer-handoff.md',
        'final-readiness-093/review-binding-closure.json','final-readiness-093/review-binding-closure-scan.json',
        'final-readiness-093/package-evidence-repair.json','final-readiness-093/preserved-qualification-anchors.json',
        'final-readiness-093/visual-handoff/manifest.json','final-readiness-093/pdf-navigation/navigation-verification.json',
        'final-readiness-093/pdf-navigation/navigation-initial-overstrict.json',
        'final-readiness-093/pdf-navigation/report.json',
        'delivery-094/control-reconciliation.json','delivery-094/current-review-basis-scan.json',
        'delivery-094/programme-checks.json','delivery-094/historical-check.stdout.json',
        'delivery-094/scientific-check.stdout.json','delivery-094/historical-status.stdout.json',
        'delivery-094/README.md']
    for path in relative_evidence:
        p=B/path;identities[str(p.relative_to(R))]=sha(p)
    for p in (B/'final-readiness-093/visual-handoff').glob('*.jpg'):
        identities[str(p.relative_to(R))]=sha(p)
    for path in ['tools/finalize_release_delivery_20261030.py','tools/verify_release_delivery_20261030.py','tools/freeze_release_delivery_20261030.py','tools/refresh_release_controls_20261029.py']:
        identities[path]=sha(R/path)
    a=load(B/'deletion-audit.json');state=load(B/'state.json')
    for pub in a['publication'].values(): identities[pub['path']]=sha(R/pub['path'])
    gates=[
        {'id':'scholarly_argument','status':'author_review_complete_independent_review_open','evidence':'review-currency-current.json','limit':'124 attributed records and component chains;no new whole-book reading or independent verdict.'},
        {'id':'source_traceability','status':'pass_in_declared_scope','evidence':'source-verification.json','limit':'Identity and inspected-anchor navigation;22 frontier originals and separate TCDF/Windmeijer omissions remain.'},
        {'id':'numerical_reconstruction','status':'pass_in_declared_scope','evidence':'numerical-portability-batch-086-r01/result.json','limit':'68 retained groups;five supplied external inputs;not every experiment regenerated.'},
        {'id':'post_execution_deletion_review','status':'pass_in_author_scope','evidence':'semantic-deletion-review-current.json','limit':'Cumulative292-edit semantic assessment and exact replay;not an independent semantic guarantee.'},
        {'id':'portable_manuscript','status':'pass_in_declared_environment','evidence':'package-verification-batch-086-r01.json','limit':'Same installed TeX system;both PDFs byte-identical;genuine third-party originals stay in research workspace.'},
        {'id':'publication_structure','status':'pass_mechanical','evidence':'final-readiness-093/pdf-navigation/navigation-verification.json','limit':'Warnings,bounds,fonts and navigation do not certify visual quality.'},
        {'id':'fresh_visual_review','status':'open','evidence':'final-readiness-093/visual-handoff/manifest.json','limit':'Session image allowance exhausted;previews prepared only.'},
        {'id':'independent_editorial_scientific_acceptance','status':'open','evidence':'final-readiness-093/reviewer-handoff.md','limit':'No actual independent verdict and no external contact.'}]
    manifest={'schema_version':1,'delivery_revision':revision,'batch':86,'package_revision':1,'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'disposition':'qualified_release_candidate','programme_status':state['status'],'programme_phase':state['phase'],
              'authorized_window':{'start_utc':state['started_utc'],'end_utc':state['deadline_utc'],'timezone':'Asia/Shanghai'},
              'release_accepted':False,'fresh_visual_acceptance':False,'independent_acceptance':False,
              'publications':a['publication'],'ledger_sha256':a['ledger_sha256'],'release_edits':292,'preserved_baseline_edits':505,
              'gates':gates,'identity_files':identities,'control_snapshots':control_refs,
              'scope':'Post-package delivery binds actual relocation results and exact final-review evidence. Frozen package creation-time records are preserved. Goal/timebox completion is distinct from publication acceptance.',
              'next_action':'Fresh-session visual inspection and actual independent critical reading of these exact PDFs;repair only demonstrated defects with renewed contextual/deletion/build/package evidence. Source and general-capability limits remain explicit.'}
    save(target,manifest)
    save(B/'delivery-current.json',{'batch':86,'package_revision':1,'delivery_revision':revision,'stage':state['phase'],'manifest':str(target.relative_to(R)),'manifest_sha256':sha(target),'directory':str(D.relative_to(R)),'updated_utc':manifest['recorded_utc'],'release_accepted':False})
    print(json.dumps({'manifest':str(target.relative_to(R)),'sha256':sha(target),'identity_files':len(identities),'release_accepted':False}))

if __name__=='__main__': freeze(int(sys.argv[1]))
