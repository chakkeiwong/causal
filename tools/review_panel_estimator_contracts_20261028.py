"""Authenticate inspected primary implementation and exact project witnesses."""
import hashlib,json
from pathlib import Path
import panel_estimator_reference_20261028 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28';BASE=DAY/'panel-estimator-contracts-v1';RAW=ROOT/'docs/literature/raw'

def main():
 assert not (BASE/'review.json').exists()
 anchors={
 'fastdid_0':[(1,28,'Balanced/unbalanced dispatch and covariate activation'),(32,67,'Balanced propensity cap and covariance replacement'),(85,111,'Weighted outcome-change regression and normalized contrast'),(115,180,'Nuisance influence, effective support and residual inflation'),(183,246,'Unbalanced support and presence-weighted propensity'),(258,407,'Period-specific regression, means, influence and effective-size checks')],
 'fastdid_1':[(18,85,'Calendar normalization and irregular-spacing refusal'),(89,208,'Unit indexing, first-observation inputs and weight normalization'),(212,275,'Output clock recovery and zero reference row')],
 'fastdid_2':[(19,62,'Weight, expression, bootstrap and provenance options'),(77,151,'Validation, estimation, aggregation and full result dispatch')],
 'nonabsdid_0':[(35,114,'Alias conflicts, range checks, integer coercion and horizon map')],
 'nonabsdid_1':[(83,162,'Labelled-to-factor and tagged-missing defaults'),(211,246,'Name sanitation, truncation then uniqueness'),(249,260,'Implicit DTA reader defaults')],
 'nonabsdid_2':[(3,36,'Plot-data extraction, shifted clock and native bounds')],
 'nonabsdid_3':[(24,58,'Fect estimates, bounds and matching-length SE extraction'),(60,72,'Unknown method label falls back to IFE')],
 'nonabsdid_4':[(30,100,'PanelMatch post/placebo fields and artificial reference'),(103,119,'Named relative-time parsing')],
 'nonabsdid_5':[(3,35,'Stored tidy results delegated to constructor')]}
 identities={r['candidate']:r for r in json.loads((DAY/'panel-originals-v1/identity-review.json').read_text())['repositories']};rows=[]
 for planned in json.loads((BASE/'source-plan.json').read_text())['sources']:
  stem=planned['id'];candidate=stem.split('_')[2];idx=stem.rsplit('_',1)[1];p=RAW/(stem+'.txt');rp=RAW/(stem+'.receipt.json');receipt=json.loads(rp.read_text());data=p.read_bytes()
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==planned['git_blob_sha1'];assert hashlib.sha256(data).hexdigest()==receipt['sha256'] and receipt['url']==planned['url'];lines=data.decode().splitlines();inspected=[]
  for a,b,finding in anchors[candidate+'_'+idx]:
   assert 1<=a<=b<=len(lines);inspected.append(dict(lines=[a,b],finding=finding,excerpt_sha256=hashlib.sha256(chr(10).join(lines[a-1:b]).encode()).hexdigest()))
  rows.append(dict(candidate=candidate,source_identity=receipt['url'],version_date=identities[candidate]['date']+'; '+planned['commit'],local_copy=ref(p,'Exact implementation'),acquisition_receipt=ref(rp,'Observed public response'),git_blob_sha1=blob,inspected_anchors=inspected,supported_claims=[x['finding'] for x in inspected],native_execution=False))
 assert len(rows)==9;write(BASE/'exact-results.json',exact.calculate())
 sources=[dict(integrated_citation_key='exec28_panel_estimator_sources',kind='software_primary_sources',title='Pinned fastdid estimator and nonabsdid conversion internals',author='Selected panel package contributors',year=2026,source_identity='Nine pinned files from TsaiLintung/fastdid and cran/nonabsdid',version_date='Pre-cutoff commits; reviewed 28 October 2026',local_copy=rows[0]['local_copy'],records=rows,inspected_anchors=[dict(anchor='Per-record line ranges and excerpt digests',inspection='Primary implementation review')],supported_claims=['Selected support, nuisance, clock, interval, naming and delegation contracts.'],limits=['No native package, writer or bootstrap execution.']),dict(integrated_citation_key='exec28_panel_estimator_reference',kind='project_reference_not_external_paper',title='Exact effective-support and adapter-boundary witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/panel_estimator_reference_20261028.py',version_date='28 October 2026; exact project arithmetic',local_copy=ref(Path(exact.__file__),'Independent witnesses'),results=ref(BASE/'exact-results.json','Performed outputs'),inspected_anchors=[dict(anchor='calculate: support, odds, aliases, time and names',inspection='Authored exact derivation')],supported_claims=['Effective support 9/5; capped odds9999999999; alias truncation; clock shift; name collision length34.'],limits=['Source-contract witnesses, not native or statistical qualification.'])]
 audit=dict(sources=sources,cutoff='2026-10-07',native_execution=False);verify_bindings(audit);write(BASE/'source-audit.json',audit)
 evidence=[ref(BASE/p,'Reviewed source or authored argument') for p in ['source-audit.json','exact-results.json','development.tex','sponsor-addition.md','plan-review.json','fetch-exit.json']]+[ref(Path(__file__),'Source reviewer'),ref(Path(exact.__file__),'Exact witness')]
 write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_project_derivations',evidence=evidence,issues=[],findings=['Effective support and odds derived exactly.','Alias/time/name transformations are independent transcriptions.','Influence correctness and finite calibration are not inferred.'],native_execution=False,empirical_coverage=False))
 write(BASE/'copyedit-review.json',dict(status='pass_for_source_text',evidence=evidence,findings=['Banking consequences and adapter requirements are connected.','Native bounds, inferred labels and plotting anchors remain distinct.','No original paper substituted.'],rendered_review=False))
 remaining=['Inspect BMisc bootstrap, parglm and remaining pinned dependency/test versions.','Inspect nonabsdid common constructor/list coercion and exact upstream DCDH,fect,PanelMatch objects.','Resolve later fastdid paper and M>=3/anticipation proof.','Retain pampe,Synth,trend-weighting originals and exact leaps omissions.','Qualify declared public profiles, rights, all failures and costs before stronger claims.','Visual, broad coverage, independent and final acceptance remain open.']
 write(BASE/'remaining-obligations.json',dict(status='open_local_continuations',actions=remaining,canonical_gaps_closed=[],evidence=evidence))
 write(BASE/'review.json',dict(status='pass_for_bounded_source_addition',pinned_files=9,evidence=evidence+[ref(BASE/'mathematical-review.json','Exact review'),ref(BASE/'remaining-obligations.json','Remaining work')],native_execution=False,visual_acceptance=False,final_acceptance=False))
 print(json.dumps(dict(pinned_files=9,source_records=2,exact_witnesses='pass',canonical_acceptance=False)))

if __name__=='__main__':main()
