"""Close only the authorized timebox; publication acceptance stays open."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import sys
from urllib.parse import unquote, urlsplit

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
D = B / 'delivery-094'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def save(p, data): p.write_text(json.dumps(data, indent=2) + '\n')
def now(): return datetime.datetime.now(datetime.timezone.utc)

def evidence_checks():
    files = ['CURRENT.md', 'docs/mission-control.md', 'docs/mission-control.html',
             'docs/program/master-live.md', 'docs/release/2026-10-29/delivery-094/README.md',
             'docs/release/2026-10-29/delivery-094/final-programme-review.md',
             'docs/release/2026-10-29/final-readiness-093/reviewer-handoff.md']
    rows = []
    for name in files:
        p = R / name; s = p.read_text()
        if '<!-- release-candidate:start -->' in s:
            s = s.split('<!-- release-candidate:start -->', 1)[1].split('<!-- release-candidate:end -->', 1)[0]
        elif name.endswith('.html'):
            start = s.index('<section><h2>'); end = s.index('</section>', start)
            s = s[start:end]
        links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', s) + re.findall(r'href="([^"]+)"', s)
        for href in links:
            parsed = urlsplit(href)
            if parsed.scheme or not parsed.path: continue
            target = (p.parent / unquote(parsed.path)).resolve()
            rows.append({'source': name, 'href': href, 'exists': target.exists()})
    issues = [x for x in rows if not x['exists']]
    save(D/'final-handoff-links.json', {'status': 'fail' if issues else 'pass', 'recorded_utc': now().isoformat(),
         'scope': 'Current release sections and final delivery/review entrypoints; local target existence only.',
         'links_checked': len(rows), 'issues': issues, 'links': rows})
    state = load(B/'state.json')
    protected = [{'path': p, 'expected_sha256': h, 'actual_sha256': sha(R/p)} for p,h in state['historical_protected'].items()]
    failures = [x for x in protected if x['expected_sha256'] != x['actual_sha256']]
    save(D/'final-historical-controls.json', {'status': 'fail' if failures else 'pass', 'recorded_utc': now().isoformat(), 'identities': protected})
    # Retain the original identity of every superseded delivery dependency.
    archive = {sha(p): str(p.relative_to(R)) for p in D.iterdir() if p.is_file()}
    lineage=[]; unresolved=[]
    for revision in [0,1]:
        mp=D/f'manifest-r{revision:02d}.json';m=load(mp);resolved=[]
        for path,h in m['identity_files'].items():
            live=R/path
            retained = path if live.is_file() and sha(live)==h else archive.get(h)
            if retained is None: unresolved.append({'manifest':str(mp.relative_to(R)),'path':path,'sha256':h})
            elif retained != path: resolved.append({'recorded_path':path,'expected_sha256':h,'retained_path':retained})
        lineage.append({'manifest':str(mp.relative_to(R)),'sha256':sha(mp),'superseded_identities':resolved})
    mp=D/'preflight-manifest.json';m=load(mp);resolved=[]
    for path,h in m['identity_files'].items():
        live=R/path;retained=path if live.is_file() and sha(live)==h else archive.get(h)
        if retained is None: unresolved.append({'manifest':str(mp.relative_to(R)),'path':path,'sha256':h})
        elif retained != path: resolved.append({'recorded_path':path,'expected_sha256':h,'retained_path':retained})
    lineage.append({'manifest':str(mp.relative_to(R)),'sha256':sha(mp),'scope':'nonfinal extended-verifier preflight','superseded_identities':resolved})
    save(D/'delivery-lineage.json', {'status':'fail' if unresolved else 'pass','recorded_utc':now().isoformat(),'revisions':lineage,'unresolved':unresolved,
         'scope':'Earlier immutable manifests retain their creation-time paths; all superseded bytes resolve to exact archived identities.'})
    assert not issues and not failures and not unresolved, 'Final delivery evidence checks failed'
    print(json.dumps({'status':'pass','local_links':len(rows),'historical_controls':len(protected),'prior_delivery_revisions':2}))

def close():
    state=load(B/'state.json');stamp=now();deadline=datetime.datetime.fromisoformat(state['deadline_utc'])
    if stamp < deadline: raise SystemExit('Timebox remains active; no early completion is written')
    if state['phase']=='REL08_delivered': raise SystemExit('Timebox already closed; do not repeat writes')
    assert state['phase']=='REL08_final_integration'
    assert not any(state[k] for k in ['release_accepted','fresh_visual_acceptance','independent_acceptance'])
    state.update(status='timebox_complete_candidate_delivered',phase='REL08_delivered',completed_utc=stamp.isoformat(),
        next_action='Inspect the exact bound PDFs visually in a fresh session and obtain actual independent critical reading. Preserve the candidate until a demonstrated defect requires a versioned repair; renew affected contextual, build, semantic deletion and package evidence. Source omissions and general scientific limits remain explicit.')
    for task in state['tasks']:
        if task['id']=='REL08': task.update(status='complete',scope='Qualified candidate and versioned delivery evidence delivered after the authorized twelve-hour window. Publication acceptance remains open under REL07.')
    state['final_integration']['completed_utc']=stamp.isoformat()
    state['final_integration']['closing_review']={'path':str((D/'final-programme-review.md').relative_to(R)),'sha256':sha(D/'final-programme-review.md')}
    save(B/'state.json',state)
    for name in ['CURRENT.md','docs/mission-control.md','docs/program/master-live.md']:
        p=R/name;s=p.read_text();start=s.index('<!-- release-candidate:start -->');end=s.index('<!-- release-candidate:end -->',start)
        block=s[start:end].replace('## Active release candidate: verified batch 086','## Delivered qualified release candidate: batch 086')
        block=block.replace('The twelve-hour programme remains active until **30 October 2026, 10:58:35 Asia/Shanghai** (02:58:35 UTC).','The authorized twelve-hour programme concluded on **30 October 2026, 10:58:35 Asia/Shanghai** (02:58:35 UTC).')
        block=block.replace('Delivery-manifest integration and control verification continue; no new source investigation is open.','The qualified candidate and final delivery evidence are complete within their declared scope. The next publication work is fresh visual inspection and independent critical reading.')
        s=s[:start]+block+s[end:]
        s=s.replace('The authorized twelve-hour release programme is active through 30 October 2026 10:58:35 Asia/Shanghai.','The authorized twelve-hour release programme concluded on 30 October 2026 10:58:35 Asia/Shanghai; its qualified candidate is linked above.')
        p.write_text(s)
    p=R/'docs/mission-control.html';s=p.read_text();start=s.index('<section><h2>Active release candidate:');end=s.index('</section>',start)
    block=s[start:end].replace('Active release candidate: verified batch 086','Delivered qualified release candidate: batch 086')
    block=block.replace('The programme remains active until 30 October 2026, 10:58:35 Asia/Shanghai.','The twelve-hour programme concluded on 30 October 2026, 10:58:35 Asia/Shanghai (02:58:35 UTC).')
    block=block.replace('Final delivery records and controls are being reconciled; new source investigations are closed.','The qualified candidate and final delivery records are complete in their stated scope. The next publication work is fresh visual inspection and independent critical reading.')
    p.write_text(s[:start]+block+s[end:])
    p=R/'docs/program/release-programme-2026-10-29.md';s=p.read_text()
    s=s.replace('The persistent goal is active.','The twelve-hour work window has concluded with a qualified candidate; final publication acceptance remains open.')
    s=s.replace('The baseline is the verified','At programme start, the baseline was the verified',1)
    s=s.replace('The separately completed discovery-search repair must be reconciled with the release: its main empirical and exact mathematical findings are absent from this reader. Do not rerun it as a new experiment.','At that baseline, the separately completed discovery-search repair was absent. REL02 subsequently integrated its main empirical and exact mathematical findings without rerunning it as a new experiment.',1)
    s=s.replace('## Current continuation — final integration of batch 086 revision 1','## Final delivery — batch 086 revision 1',1)
    s=s.replace('| REL08 | Final delivery manifest and control reconciliation in progress until 02:58:35 UTC. |','| REL08 | Qualified candidate delivered at the end of the authorized twelve-hour window; final manifest and control verification recorded. |',1)
    old='The remaining authorized work binds the exact candidate, package proofs,\nstandard assessment, residual inventory and reviewer handoff in a versioned\nmanifest; verifies current controls and final local links; and delivers the\nqualified candidate by 30 October 2026, 02:58:35 UTC (10:58:35 Asia/Shanghai).\nNo new source investigation starts after 01:58:35 UTC. Further changes require\na demonstrated defect and renewed review/build/deletion/package evidence.'
    new='The delivered record binds the exact candidate, successful package proofs,\nstandard assessment, residual inventory and reviewer handoff. The final closing\nreadings additionally cover complete rendered chapters 1–12, 17–18, 20, 26–28, 30, 42 and 97–99.\nThe [final programme review](../release/2026-10-29/delivery-094/final-programme-review.md)\nretains the scholarly standard and remaining acceptance judgments. Local links,\ncurrent source identities and protected historical controls verify. New source\ninvestigations closed for the final hour. Further manuscript changes require\na demonstrated defect and renewed review/build/deletion/package evidence.'
    assert old in s;s=s.replace(old,new,1);p.write_text(s)
    p=D/'README.md';s=p.read_text();s=s.replace('The candidate is ready for the outstanding publication reviews.','The twelve-hour window is complete. This qualified candidate and its evidence\nare delivered for the outstanding publication reviews.',1);p.write_text(s)
    p=B/'execution-log.md'
    with p.open('a') as f:
        f.write('\n## Twelve-hour delivery closure — '+stamp.isoformat()+'\n\nThe window ended at 02:58:35UTC. Delivered batch086 revision1 as a qualified candidate; REL08 is complete, REL07 remains blocked and all publication-acceptance flags remain false. The closing author readings cover complete rendered chapters1–12,17–18,20,26–28,30,42,97–99 and the sponsor, in addition to final-readiness093 chapters14,21,100,101. Exact reading records preserve boundaries and PDF/text hashes. No new manuscript defect was established and no new manuscript edit was made.\n\nRetained all18 actual relocation compiler records with observed-to-retained path/hash mapping. Checked10,037 extracted internal PDF links; all458 unique targets resolve. External URL extraction does not constitute online validation. The final verifier additionally binds478 current manuscript sources and exact current control snapshots. The r00 verifier failed on three historical package_path references; the corrected resolver passed r01. Both failures and superseded tool/README bytes remain preserved with explicit lineage. Final revision2 binds later readings, sponsor claim map, compiler evidence and timebox closure. Historical and scientific programme checks remain in their declared scope; no product, bank or independent acceptance is inferred.\n\nNext: fresh-session visual inspection and actual independent critical reading of these exact PDFs. Repair supported findings with renewed context, build, semantic deletion and package proofs. Keep22 unread frontier originals, separate original omissions and general scientific limits explicit.\n')
    evidence_checks()
    print(json.dumps({'status':state['status'],'phase':state['phase'],'completed_utc':stamp.isoformat(),'release_accepted':False}))

if __name__=='__main__':
    if sys.argv[1:]==['check']: evidence_checks()
    elif sys.argv[1:]==['close']: close()
    else: raise SystemExit('Usage: close_release_timebox_20261030.py check|close')
