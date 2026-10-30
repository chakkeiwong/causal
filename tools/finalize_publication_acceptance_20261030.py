from pathlib import Path
import datetime, hashlib, json, shutil
R=Path(__file__).resolve().parents[1]
D=R/'docs/release/2026-10-30/publication-acceptance-001'
B=R/'docs/release/2026-10-29'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def save(p,d): p.write_text(json.dumps(d,indent=2)+chr(10))
review=load(D/'independent-ai-review/review.json'); state=load(D/'state.json')
assert review['decision']=='accept' and review['blocking_findings']==0 and not review['required_manuscript_revisions']
assert review['reviewer']['independent_of_edits']
assert review['review_md_sha256']==sha(D/'independent-ai-review/review.md')
assert review['visual_review']['status']=='accept_sampled_visual_presentation'
assert review['visual_review']['preview_count']==6 and not review['visual_review']['every_page_inspected']
assert 'IR-01 is resolved' in (D/'independent-ai-review/errata-verification.md').read_text()
assert load(D/'preservation-check.json')['status']=='pass'
assert not (D/'manifest.json').exists(),'Refuse to overwrite final manifest'
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
publications={}
for key,name in [('reader','docs/causal_banking_publication_2026-10-30.pdf'),('sponsor','docs/causal_banking_sponsor_publication_2026-10-30.pdf')]:
    source=R/review['pdfs'][key]['path']; target=R/name
    assert sha(source)==review['pdfs'][key]['sha256']
    if target.exists(): assert sha(target)==sha(source)
    else: shutil.copy2(source,target)
    assert sha(target)==sha(source)
    publications[key]={'path':name,'sha256':sha(target),'pages':review['pdfs'][key]['pages'],'byte_identical_reviewed_candidate':review['pdfs'][key]['path']}
disposition={'recorded_utc':stamp,'review':{'path':str((D/'independent-ai-review/review.json').relative_to(R)),'sha256':sha(D/'independent-ai-review/review.json')},'findings':[{'id':'IR-01','severity':'minor_nonblocking','status':'resolved_by_publication_errata','evidence':str((D/'errata.md').relative_to(R)),'reviewer_confirmation':str((D/'independent-ai-review/errata-verification.md').relative_to(R)),'manuscript_change':False},{'id':'IR-02','severity':'optional','status':'future_edition_optional','action':'Consider larger Figure101.2 labels or individual panels; retain both demonstrations and caption.','acceptance_condition':False},{'id':'IR-03','severity':'optional','status':'future_edition_optional','action':'Consider cross-references for repeated synthesis; preserve derivations, alternatives, adverse findings and reversal conditions. No arbitrary shortening.','acceptance_condition':False}],'unresolved_blocking_findings':0,'required_manuscript_revisions':0,'manuscript_deletions':0}
save(D/'findings-disposition.json',disposition)
state.update(status='publication_accepted_in_independent_ai_review_scope',completed_utc=stamp,release_accepted=True,independent_acceptance=True,fresh_visual_acceptance=True,independent_acceptance_scope='Independent of authorship, user-authorized fresh Codex Astra AI review; not human peer review or external signed X01.',visual_acceptance_scope='Six inspected pages plus inherited all-page mechanical checks; not every-page visual certification.',publication_acceptance_scope=review['accepted_scope'],human_peer_review=False,external_X01_acceptance=False,bank_acceptance=False,all_pages_visually_reviewed=False,publication_copies=publications,reviewer_report=disposition['review'],next_action='Read the accepted publication with its bound errata. No mandatory revision remains in the AI publication-review scope. Optional improvements belong to a future version with renewed context/build/deletion/package evidence. External human and bank qualification remain separate.')
state['tasks']={'PA01':'complete_candidate_and_evidence_verified','PA02':'complete_bounded_critical_and_sampled_visual_review','PA03':'complete_independent_ai_review_and_findings_disposition','PA04':'complete_no_manuscript_edit_preservation_verified','PA05':'complete_publication_accepted_in_declared_scope'}
save(D/'state.json',state)
contract=load(D/'acceptance-contract.json');contract['decision']='accept_in_independent_ai_publication_scope';contract['decision_evidence']=state['reviewer_report'];save(D/'acceptance-contract.json',contract)
(D/'decision.md').write_text('''# Final publication acceptance

30 October 2026, Asia/Shanghai. **Accepted for scholarly publication** as a research monograph/reference and bounded product proposal. The decision follows the user-authorized fresh Codex Astra review, independent of this revision's authorship. Same-provider AI limitations are explicit. This is not human peer review, external signed X01, institutional approval or bank-product acceptance.

## Published documents

- [Monograph: 1,941 pages](../../../causal_banking_publication_2026-10-30.pdf)
- [Sponsor proposal: four pages](../../../causal_banking_sponsor_publication_2026-10-30.pdf)
- [Companion errata](errata.md)
- [Independent AI review](independent-ai-review/review.md)
- [Structured review and exact coverage](independent-ai-review/review.json)

The publication copies are byte-identical to the reviewed candidate. Existing build, source, numerical and preservation evidence continues to apply; no unreviewed manuscript change or fresh build is implied. The title-page date remains 29 October 2026, the candidate date; publication acceptance is dated 30 October 2026.

## Actual review and disposition

The fresh reviewer read 91 pages of complete chapter contexts, complete section14.5, the entire sponsor and specified additional contexts. Four selective primary-source checks and independent arithmetic supplement its reasoned assessment of correctness, explanatory sufficiency and proportionality. Zero blocking findings and no mandatory manuscript revisions remain.

All six prepared visual samples were actually inspected by the fresh reviewer. No blocking clipping, overlap or typography defect was observed. This establishes sampled visual acceptance for the editorial decision, not every-page inspection or a new whole-book proof. Existing all-page bounds, references, fonts and navigation checks provide supporting evidence.

IR-01 is resolved by the bound errata: on physical52/printed46, the Ghassami locator should read Sections3.2–3.3. The theorem and scientific claim are correct. The reviewer confirmed the notice resolves this navigation defect without a rebuild. IR-02 (small plot labels) and IR-03 (repeated synthesis) remain optional future refinements, with preservation requirements recorded. The original reviewer report and its finding remain unchanged.

## Preservation and scope

No manuscript text was edited or deleted during this continuation. All478 current sources, the292-edit release ledger,505-edit baseline and semantic deletion evidence retain their identities. Both packages, source bindings and actual relocation receipts remain verified. The four refreshed master entrypoints preserve original content and exact before-copies. Earlier manifests and verdicts are historical records; this decision supersedes their open acceptance status without rewriting history.

The22 unread frontier sources, original omissions and general hidden-state/dependence/linkage/graph-confidence limits remain explicit. The review accepts a developed scholarly argument with those limitations, not an exhaustive survey or a generally qualified deployed product.

[Programme](../../../program/publication-acceptance-2026-10-30.md) · [Finding dispositions](findings-disposition.json) · [Preservation check](preservation-check.json) · [Final verification](verification.json)
''')
p=R/state['programme'];t=p.read_text();t=t.replace('## Execution and acceptance','''## Completed decision

PA01–PA05 are complete in the declared publication-review scope. The user-authorized fresh Codex Astra reviewer accepts with zero blocking findings after critical reading, four selective primary-source checks, independent arithmetic and six actual visual samples. A minor source locator is resolved by the attached errata. No manuscript deletion or rebuild is required. Human peer review, every-page inspection, external X01 and bank acceptance are not asserted.

[Final publication decision](../release/2026-10-30/publication-acceptance-001/decision.md) · [Original reviewer report](../release/2026-10-30/publication-acceptance-001/independent-ai-review/review.md)

## Execution and acceptance''',1)
t+=chr(10)+'''## Final programme review

The author did not certify its own independent gate: a fresh reviewer supplied a separately attributed verdict and actual visual observations. Its minor finding was preserved and resolved by a bound errata notice. Optional improvements remain visible without removing important scientific material. The published PDFs are the exact bytes reviewed and reproduced. Historical programmes remain preserved records. Future edits require exact before/after and retained destinations, affected-context review, compilation, semantic deletion assessment and renewed package proof.
''';p.write_text(t)
start='<!-- publication-acceptance:start -->';end='<!-- publication-acceptance:end -->'
for name in ['CURRENT.md','docs/mission-control.md','docs/program/master-live.md']:
    p=R/name;t=p.read_text();a=t.index(start);z=t.index(end,a)+len(end);prefix={'CURRENT.md':'docs/','docs/mission-control.md':'','docs/program/master-live.md':'../'}[name]
    section=f'''{start}
## Publication accepted: independent AI review

30 October 2026, Asia/Shanghai. The user-authorized fresh Codex Astra reviewer accepts the exact monograph and sponsor for scholarly publication in their research/proposal scope. Zero blocking findings; one minor source locator is resolved by the accompanying errata.

[Published monograph]({prefix}causal_banking_publication_2026-10-30.pdf) · [Sponsor proposal]({prefix}causal_banking_sponsor_publication_2026-10-30.pdf) · [Errata]({prefix}release/2026-10-30/publication-acceptance-001/errata.md)

Fresh review includes91 complete chapter pages, section14.5, the full sponsor, four selective primary-source checks and six actual visual samples. This is a bounded same-provider AI publication judgment, not human peer review, every-page inspection, external X01 or bank acceptance. No manuscript text was removed. Published PDFs are byte-identical to the verified candidate.

[Final acceptance decision]({prefix}release/2026-10-30/publication-acceptance-001/decision.md) · [Independent report]({prefix}release/2026-10-30/publication-acceptance-001/independent-ai-review/review.md) · [Refreshed master programme]({prefix}program/publication-acceptance-2026-10-30.md)

Earlier candidate and scientific-continuation sections below retain historical statuses; this is the current publication disposition.
{end}'''
    p.write_text(t[:a]+section+t[z:])
p=R/'docs/mission-control.html';t=p.read_text();a=t.index(start);z=t.index(end,a)+len(end)
section='''<!-- publication-acceptance:start --><section><h2>Publication accepted: independent AI review</h2><p>30 October 2026, Asia/Shanghai. A user-authorized fresh Codex Astra reviewer accepts the exact research monograph and sponsor with zero blocking findings. A minor source locator is resolved by the accompanying errata. Sampled visual review covers six actual pages; human peer review, every-page inspection, external X01 and bank acceptance are not asserted. Earlier sections retain historical statuses.</p><p><a href='causal_banking_publication_2026-10-30.pdf'>Published monograph</a> · <a href='causal_banking_sponsor_publication_2026-10-30.pdf'>Sponsor</a> · <a href='release/2026-10-30/publication-acceptance-001/errata.md'>Errata</a> · <a href='release/2026-10-30/publication-acceptance-001/decision.md'>Acceptance and evidence</a> · <a href='program/publication-acceptance-2026-10-30.md'>Refreshed master programme</a></p></section><!-- publication-acceptance:end -->'''
p.write_text(t[:a]+section+t[z:])
for filename,key in [('entrypoint-preservation.json','controls'),('control-successor-verification.json','resolved_controls')]:
    p=D/filename;data=load(p)
    for row in data[key]:row['current_sha256']=sha(R/row.get('live_path',row.get('path')))
    save(p,data)
log=load(D/'execution-log.json');log['events'].append({'action':'Complete independent AI review','outcome':'Actual bounded critical and six-page visual review accepts. IR01 resolved by bound errata and reviewer confirmation. IR02/03 optional. Manuscript unchanged; publication copies byte-identical.'});save(D/'execution-log.json',log)
print(json.dumps({'status':state['status'],'publications':publications,'blocking_findings':0,'manuscript_changes':0}))

