from pathlib import Path
import datetime
import hashlib
import json
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
D = R / 'docs/release/2026-10-30/publication-acceptance-001'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d): p.write_text(json.dumps(d,indent=2)+chr(10))

D.mkdir(parents=True,exist_ok=False)
manifest = json.loads((B/'delivery-094/manifest-r02.json').read_text())
controls=['CURRENT.md','docs/mission-control.md','docs/mission-control.html','docs/program/master-live.md']
originals={}
for name in controls:
    p=D/'before'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/name,p)
    originals[name]={'path':str(p.relative_to(R)),'sha256':sha(p)}
plan=R/'docs/program/publication-acceptance-2026-10-30.md'
plan.write_text('''# Master continuation: final publication acceptance

30 October 2026, Asia/Shanghai. Authorized by the request to refresh the master programme and finish final publication acceptance. The completed twelve-hour delivery remains a historical record; this continuation evaluates the exact delivered candidate.

## Standard

A prepared economist must reconstruct the banking decision and information clock, model and notation, assumptions, identification or identified set, estimation, uncertainty and sensitivity, numerical error, monetary consequences, serious alternatives and justified recommendation. FinMarketing is an exposition benchmark. Scientific meaning and source fidelity outrank compression. Publication acceptance does not establish bank-product or institutional acceptance.

## Execution and acceptance

| Task | Work | Closure evidence |
|---|---|---|
| PA01 | Bind the delivered PDFs, preservation ledger, source records and historical controls; search for subsequent review findings. | Current hashes and exact evidence inventory; distinguish received findings from author-prepared handoffs. |
| PA02 | Review publication presentation and unresolved writing judgments. | Actual visual observations with pages and PDF hashes; critical reading addressing derivation, readability and proportionality. Mechanical checks are supporting evidence. |
| PA03 | Resolve actual independent editorial/scientific findings. | Attributed reviewer report naming candidate, scope, decision and unresolved findings; verified author responses when needed. |
| PA04 | Rebuild and audit every supported manuscript repair. | Exact before/after ledger, substantive destinations for deletions, affected-context reading, compiled-input and semantic deletion checks, renewed package proof. Verify unchanged identities when no repair is justified. |
| PA05 | Record the supported final decision and update the active master. | Accept only when visual and independent critical-review gates have evidence. Otherwise record the precise missing evidence and next action. |

## Programme review

Bind the candidate before assessing reviews; resolve findings before acceptance; renew preservation and reproducibility after each manuscript change. Bank data, native qualification and every unread frontier source are not automatically publication blockers when the corresponding claims are explicitly bounded. The 1,941-page length requires a readability and proportionality judgment, not an arbitrary reduction target. No author checklist, receipt count or deadline supplies independent acceptance.

The same session has exhausted its six-image allowance under /home/ubuntu/AGENTS.md. This is an execution constraint, not a visual defect or a passed review. The repository prohibits spawning agents without an explicit user request. No reviewer is contacted by this programme. Search existing evidence first; if a required verdict is absent, finish local review and validation and record the actual missing evidence.

## Preservation

Batch086 revision1 packages, delivery revision2 and its snapshots remain immutable. Archive the current master entrypoints before this refresh. Preserve the 292 release edits and 505-edit baseline, assumptions, derivations, alternatives, negative findings, equations, labels, citations and numeric facts. Acceptance records are a successor overlay, not a rewrite of earlier verdicts.

[Candidate and evidence](../release/2026-10-29/delivery-094/README.md) · [Current acceptance record](../release/2026-10-30/publication-acceptance-001/state.json)
''')
state={'schema_version':1,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timezone':'Asia/Shanghai','status':'in_progress','programme':str(plan.relative_to(R)),'candidate_manifest':str((B/'delivery-094/manifest-r02.json').relative_to(R)),'candidate_manifest_sha256':sha(B/'delivery-094/manifest-r02.json'),'publications':manifest['publications'],'before_controls':originals,'tasks':{'PA01':'in_progress','PA02':'pending','PA03':'pending_evidence_search','PA04':'conditional_on_supported_repair','PA05':'pending'},'release_accepted':False,'fresh_visual_acceptance':False,'independent_acceptance':False,'constraints':['Session six-image allowance exhausted; no new image forwarded.','No agents or external reviewer contact authorized.'],'next_action':'Verify candidate and search received reviews; assess outstanding writing judgments and record supported disposition.'}
save(D/'state.json',state)
for name in ['CURRENT.md','docs/mission-control.md','docs/program/master-live.md']:
    p=R/name;s=p.read_text();prefix={'CURRENT.md':'docs/','docs/mission-control.md':'','docs/program/master-live.md':'../'}[name]
    section=f'''<!-- publication-acceptance:start -->
## Final publication acceptance: active continuation

The delivered batch086 candidate is under final acceptance review. The twelve-hour preparation is complete. This continuation verifies candidate identity, checks received findings, resolves supported defects and records the actual decision. Fresh visual and independent editorial/scientific acceptance remain open until evidence is present.

[Refreshed acceptance programme]({prefix}program/publication-acceptance-2026-10-30.md) · [Current acceptance evidence]({prefix}release/2026-10-30/publication-acceptance-001/state.json)
<!-- publication-acceptance:end -->

'''
    head,sep,body=s.partition(chr(10));p.write_text(head+chr(10)*2+section+body.lstrip(chr(10)))
p=R/'docs/mission-control.html';s=p.read_text();anchor='<section><h2>Delivered qualified release candidate:';assert anchor in s
section='''<!-- publication-acceptance:start --><section><h2>Final publication acceptance: active continuation</h2><p>The delivered batch086 candidate is under final acceptance review. Fresh visual and independent editorial/scientific acceptance require actual findings.</p><p><a href='program/publication-acceptance-2026-10-30.md'>Refreshed acceptance programme</a> · <a href='release/2026-10-30/publication-acceptance-001/state.json'>Current acceptance evidence</a></p></section><!-- publication-acceptance:end -->
'''
p.write_text(s.replace(anchor,section+anchor,1))
print(json.dumps({'created':str(D.relative_to(R)),'programme':str(plan.relative_to(R)),'updated_controls':controls,'candidate_unchanged':True}))
