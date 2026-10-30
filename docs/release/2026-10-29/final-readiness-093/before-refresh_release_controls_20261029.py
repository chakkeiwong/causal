"""Refresh mutable release entrypoints from the current passing audit."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 a=json.loads((B/'deletion-audit.json').read_text());build=json.loads((B/'latest-build.json').read_text());batch=build['batch'];n=a['edits'];assert a['status']=='pass' and a['ledger_sha256']==sha(B/'edits.json')
 for pub in a['publication'].values():assert sha(R/pub['path'])==pub['sha256']
 state=json.loads((B/'state.json').read_text());state.update(publication=a['publication'],verified_batch=batch,release_edits=n,phase='REL03/REL04/REL06')
 warnings=a['publication']['full']['warnings'];state['layout_result']=f"Current reader: {warnings['Underfull']} underfull, {warnings['Overfull']} overfull, zero unresolved references and geometry issues. No global warning suppression; exact source edits retain mathematical content. Fresh visual review remains open."
 inventory=json.loads((B/'remaining-inventory.json').read_text());counts=inventory['frontier_counts']
 state['frontier_counts']=counts
 state['observed_gaps']=[f"{counts['unread']} unread frontier originals and consequential comparisons remain",'Changed-context source/PDF-bound author reviews require final renewal','Fresh visual allowance and independent editorial findings unavailable','Final-candidate relocation/package renewal remains after final manuscript changes']
 state['next_action']='Continue consequential source and cross-chapter review from the current verified candidate. Current review scope and exact dispositions are in review-scope-current.json; package and numerical reconstruction proofs have their own versioned receipts. Renew affected reviews, source checks, portable package and deletion audit after further manuscript edits.'
 package_verified=False;packaged_batch=None
 for package_proof in sorted(B.glob('package-verification-batch-*.json'),reverse=True):
  proof=json.loads(package_proof.read_text())
  if proof.get('status')!='pass':continue
  packaged_batch=proof['batch']
  package_verified=(packaged_batch==batch and proof['reader_sha256']==a['publication']['full']['sha256'] and proof['sponsor_sha256']==a['publication']['sponsor']['sha256'])
  assert sha(R/proof['package']/'manifest.json')==proof['manifest_sha256']
  state['package_verification']={'path':str(package_proof.relative_to(R)),'sha256':sha(package_proof),'scope':proof['scope'],'current_candidate':package_verified}
  state['portable_package']={'batch':packaged_batch,'revision':proof.get('package_revision',0),'package':proof['package'],'manifest_sha256':proof['manifest_sha256'],'relocation_test':'pass','current_candidate':package_verified,'release_accepted':False,'scope':proof['scope']}
  state['reproducibility']=f"Batch{packaged_batch:03d} has a passing same-system relocation and preserved-original edit replay. Current-candidate match: {package_verified}. Renew after manuscript changes."
  break
 trace=json.loads((B/'source-verification.json').read_text());numerics=json.loads((B/'numerical-verification.json').read_text())
 assert trace['status']=='pass' and trace['build_batch']==batch and trace['ledger_sha256']==a['ledger_sha256']
 state['source_traceability']=f"All {trace['citation_keys']:,} cited keys have audit records; {trace['source_bindings_checked']:,} source bindings and {trace['scholarly_pdf_count']} distinct genuine scholarly PDFs verify. Mechanical traceability is separate from technical reading."
 state['numerical_verification']=f"Independent retained-data reconstruction passes for {len(numerics['checks'])} groups: "+', '.join(numerics['checks'])+'. No new bank or native qualification.'
 numerical_batch=None
 for receipt_path in sorted(B.glob('numerical-portability-batch-*/result.json'),reverse=True):
  nr=json.loads(receipt_path.read_text())
  if nr.get('status')!='pass':continue
  numerical_batch=nr.get('batch',int(receipt_path.parent.name.split('-')[3]));np=R/nr.get('package',f'docs/release/2026-10-29/numerical-packages/batch-{numerical_batch:03d}')
  nm=json.loads((np/'manifest.json').read_text());assert sha(np/'manifest.json')==nr['manifest_sha256']
  complete=next(t['report'] for t in nr['tests'] if t['case']=='complete');groups=len(complete['reconstructed_checks'])
  project_inputs=sum(not v['external'] for v in nm['inputs'].values())
  external_inputs=sum(v['external'] for v in nm['inputs'].values())
  state['numerical_package']={'batch':numerical_batch,'package':str(np.relative_to(R)),'receipt':str(receipt_path.relative_to(R)),'receipt_sha256':sha(receipt_path),'manifest_sha256':nr['manifest_sha256'],'groups':groups,'project_inputs':project_inputs,'external_inputs':sum(v['external'] for v in nm['inputs'].values()),'current_candidate':nm['reader_sha256']==a['publication']['full']['sha256'] and set(nm['check_groups'])==set(numerics['checks']) and nm['files'].get('tools/release_numerical_verification_20261029.py')==sha(R/'tools/release_numerical_verification_20261029.py')}
  break
 assert numerical_batch is not None
 (B/'state.json').write_text(json.dumps(state,indent=2)+'\n')
 backup=B/f'control-refresh-{batch:03d}';backup.mkdir(exist_ok=True)
 for file,prefix in [('CURRENT.md','docs/'),('docs/mission-control.md',''),('docs/program/master-live.md','../')]:
  p=R/file;s=p.read_text();q=backup/file.replace('/','__')
  if not q.exists():shutil.copy2(p,q)
  start=s.index('## Active release candidate:');end=s.index('<!-- release-candidate:end -->',start)
  package_text=(f'The current frozen batch{batch:03d} package has a byte-identical relocation proof and an exact edit replay from its packaged preserved originals. [Frozen package]({prefix}{proof["package"].removeprefix("docs/")}/README.md) · [Verification]({prefix}{str(package_proof.relative_to(R)).removeprefix("docs/")}). Renew after further edits.' if package_verified else f'The frozen batch{packaged_batch:03d} package has a successful relocation and edit-replay proof scoped to that earlier candidate. [Frozen package]({prefix}{proof["package"].removeprefix("docs/")}/README.md). Renew packaging for the current candidate.')
  block=f'''## Active release candidate: verified batch {batch:03d}

[Release reader]({prefix}causal_banking_release_candidate_2026-10-29.pdf) · [Four-page sponsor]({prefix}causal_banking_sponsor_release_candidate_2026-10-29.pdf) · [Release programme]({prefix}program/release-programme-2026-10-29.md)

The {a['publication']['full']['pages']:,}-page reader integrates the complete discovery-search repair and reconciles commercial comparisons with retained primary text. Its {n} exact edits preserve the 505-edit baseline, all 458 inherited reader input occurrences, mathematical expressions, labels, citation keys and 1,607 protected identities. One independently updated shared inventory retains its exact protected original at the explicitly recorded archived location; its newer live version remains in place. [Exact edit and deletion ledger]({prefix}release/2026-10-29/full-deletion-ledger.md).

The current build has {warnings['Underfull']} underfull and {warnings['Overfull']} overfull warnings, no unresolved references and no all-page text-bound errors. These are publication checks, not visual acceptance. {package_text}

The separate numerical package reconstructs {groups} retained arithmetic groups after relocation. It bundles {project_inputs} project inputs; {external_inputs} external data files require separate hash-checked intake. [Numerical package]({prefix}{str(np.relative_to(R)).removeprefix('docs/')}/README.md) · [Scope and test receipt]({prefix}{str(receipt_path.relative_to(R)).removeprefix('docs/')}). This does not regenerate every original study.

The twelve-hour programme remains active until **30 October 2026, 10:58:35 Asia/Shanghai** (02:58:35 UTC). Final source/PDF-bound author review, consequential source comparisons and final packaging continue. Candidate frontier coverage is {counts['inspected']} inspected/{counts['unread']} unread, with claim-specific limits recorded. Fresh visual inspection and independent acceptance remain open; this candidate is not an accepted final release. The historical author-review completion below applies to its unchanged baseline.

'''
  p.write_text(s[:start]+block+s[end:])
 p=R/'docs/mission-control.html';s=p.read_text();q=backup/'docs__mission-control.html'
 if not q.exists():shutil.copy2(p,q)
 start=s.index('<section><h2>Active release candidate:');end=s.index('</section>',start)+len('</section>')
 package_html=(f'Current batch{batch:03d} reproduces both PDFs after relocation and replays every edit against packaged originals.' if package_verified else 'Final packaging and relocation verification remain to be renewed for this candidate.')
 block=f'''<section><h2>Active release candidate: verified batch {batch:03d}</h2><p><a href="causal_banking_release_candidate_2026-10-29.pdf">{a['publication']['full']['pages']:,}-page release reader</a> · <a href="causal_banking_sponsor_release_candidate_2026-10-29.pdf">Four-page sponsor</a> · <a href="program/release-programme-2026-10-29.md">Twelve-hour programme</a></p><p>{n} exact edits preserve the baseline, 458 inherited input occurrences and 1,607 protected identities. The current build has {warnings['Underfull']} underfull and {warnings['Overfull']} overfull warnings, with no unresolved references or text-bound errors. {package_html} Separate numerical reconstruction passes for {groups} retained groups with explicit external-input intake.</p><p>The programme remains active until 30 October 2026, 10:58:35 Asia/Shanghai. Source-bound author reviews and consequential comparisons continue. Fresh visual and independent acceptance remain open. <a href="release/2026-10-29/state.json">Current state</a> · <a href="release/2026-10-29/full-deletion-ledger.md">Exact deletion ledger</a></p></section>'''
 p.write_text(s[:start]+block+s[end:])
 print(json.dumps({'batch':batch,'edits':n,'controls_updated':4,'publication':a['publication']['full']['sha256']}))
if __name__=='__main__':main()
