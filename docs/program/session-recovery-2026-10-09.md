# V6.1 saved-session recovery

9 October 2026 (Asia/Shanghai). The recovered thread is
`01a114c3-5d0d-7070-a23b-e18b962539bc`. Its saved rollout and workspace
history show three turns that ended with HTTP 502 from the configured Responses
gateway and two later interrupted turns. The upstream cause was not diagnosed.
The last saved source-audit and PDF-render commands both exited successfully.
The [machine recovery record](session-recovery-2026-10-09.json) preserves the
turn statuses, command exits, document hashes and checked receipt identities.

At recovery W00-W03 were complete, W04 was in progress, Mission Control still
reported final verification in progress, and the current delivery manifest and
visual narrative identified V6. The master program had already been edited to
say W04 was complete. Thus the interruption left inconsistent closeout records,
not an unfinished local simulation or a failed document build. The old V6
manifest correctly rejected the revised V6.1 files. Eleven pre-recovery
closeout records were preserved in the verified
`history/v6.1-interrupted-closeout.zip` before replacement.

Recovery checked every bound input of 13 scientific/build receipts and found
no stale identity. Retained-set reconstruction and the source/build audit were
run again and passed. The identical-seed 2,000-draw replay and separate final
workload run had already finished, so unchanged studies were not repeated.
No scientific code, registered draw, manuscript body or PDF was revised by
this recovery.

The final monograph and sponsor PDFs have 214 and 15 pages, respectively.
All 229 page images were compared with the preceding render: only monograph
contents pages 4-8 changed after the section-number spacing repair. Recovery
viewed those pages, the changed contact sheet, and the relevant mathematics,
result, product, workload and sponsor pages. The final visual receipt covers
20 contact sheets and 22 enlarged pages, with 15 fresh views and 27 prior
views reused only after byte-identical image comparison. It records no
blocking layout finding. The [inspection narrative](../reviews/reconstruction-visual-inspection.md)
and [image comparison](../reviews/linkage-render-equivalence.json) retain the
exact basis for that judgment.

The closeout actions are to bind W1-W4 dispositions and current input/PDF
hashes in the author-review receipt; replace the V6 delivery narrative;
reconcile W04 and Mission Control with the master program; run the program
consistency check; and freeze and verify the V6.1 manifest. The
[delivery record](delivery.md) and [manifest](reconstruction-delivery-manifest.json)
carry the resulting identity. A passing identity check is evidence of the
delivered files, not independent scientific review, bank data validation,
accepted sibling integration or deployment.
