"""Refresh mutable writing dashboards only from the actual post-build audit."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1];O=R/'docs/writing-repair/2026-10-29'
def read(n):return json.loads((O/n).read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=read('deletion-audit.json');assert a['pass'] and a['checks_after_final_edit']
assert sha(O/'edits.json')==a['ledger_sha256']
for name,h in a['final_source_hashes'].items():assert sha(R/name)==h,name
for pub in a['publication'].values():assert sha(R/pub['path'])==pub['sha256']
# Regenerate assembly coverage from final contextual records before publishing counts.
import subprocess,sys
subprocess.run([sys.executable,str(R/'tools/record_writing_review_20261029.py')],check=True,capture_output=True,text=True)
cs=read('chapter-review.json')['chapters'];pending=[c for c in cs if not c['full_chapter_acceptance']];done=len(cs)-len(pending);nextc=pending[0] if pending else None
full=a['publication']['full'];sponsor=a['publication']['sponsor'];pages=full['pages'];edits=a['edits'];remaining=len(pending)
next_text=f"Chapter {nextc['chapter']}, “{nextc['title']}”" if nextc else 'the whole-book W08 review'
coverage=f'{done} of {len(cs)} chapters/treatments have complete contextual author review; {remaining} remain.'
state=read('state.json');state.update(delivery='Verified continuation candidate; full writing programme remains in progress',reader=full,sponsor=sponsor,post_execution_deletion_audit='pass',author_contextual_treatments=done,remaining_full_contextual_reviews=remaining,first_next_chapter=nextc,full_writing_standard_met=False,chapter_coverage_method='Expanded assembly, including following sibling inputs and nested text',latest_ledger_sha256=a['ledger_sha256'])
save(O/'state.json',state)
p=R/'docs/program/scientific-priorities.json';d=json.loads(p.read_text());d['reader']={'pdf':full['path'],'sha256':full['sha256'],'pages':pages};d['paired_sponsor']=sponsor
d['writing_remaining']={'contextually_reviewed':done,'chapters_requiring_complete_review':remaining,'next_chapter':nextc['chapter'] if nextc else None,'next_source':nextc['source'] if nextc else None,'queue':'docs/writing-repair/2026-10-29/chapter-review.json','fresh_visual_acceptance':False}
d['chapter_review_progress']={'reviewed':done,'pending':remaining,'next_chapter':nextc['chapter'] if nextc else None,'evidence':'docs/writing-repair/2026-10-29/chapter-review.json'}
d['last_completed_writing_batch']={'date':'2026-10-29','reader_pages':pages,'edits':edits,'protected_files':a['protected_files'],'inherited_sources_compiled_once':a['mapped_sources_compiled_once'],'new_sources':'No new original acquired during contextual rewrite; three previously audited records remain integrated','full_writing_standard_met':False}
d['continuation_note']=f'Continue W04 at {next_text}; {remaining} complete contextual reviews remain. W08 owns final whole-book continuity and citations. No unattended worker. Completed experiments are not rerun.'
d['writing_execution_status']='Current continuation built and preservation-audited; W04 and W08 remain open.'
d['editorial_followup']['continuation']=d['continuation_note']
for t in d['tasks']:
 if t['id']=='W04':t['action']=f'Read {next_text}, including all assembled segments and inputs; {remaining} complete contextual reviews remain. Refresh from chapter-review.json before continuing.'
 if t['id'] in ['W06','W07']:t['status']='complete';t['recurring']=True;t['last_verified_ledger_sha256']=a['ledger_sha256']
save(p,d)
(R/'CURRENT.md').write_text(f'''# Causal banking research and product proposal

[Current integrated reader](docs/{Path(full['path']).name}) · [Aligned sponsor](docs/{Path(sponsor['path']).name}).

The {pages:,}-page continuation preserves the detailed scholarly corpus while consolidating the main recommendations and repairing exposition. The sponsor has {sponsor['pages']} pages. The programme has been refreshed, reviewed and executed through this verified continuation, not through completion of the whole rewrite.

- [Active master](docs/program/master-live.md) and [reviewed programme](docs/program/writing-gap-closure-2026-10-29.md).
- [Current candidate review](docs/reviews/writing-gap-terminal-review-2026-10-29.md).
- [Post-execution deletion audit](docs/writing-repair/2026-10-29/deletion-audit.md): {edits} exact edits, with substantive destinations.
- [Chapter queue](docs/writing-repair/2026-10-29/chapter-review.md): {coverage} Next: {next_text}.

Full writing-standard attainment, source-comparison completion, fresh visual review and independent acceptance remain open. W08 explicitly requires a final whole-book/citation pass. No unattended worker is running. Run python3 tools/scientific_program.py next. Historical controls and the hash-bound root README retain their identities.
''')
(R/'docs/mission-control.md').write_text(f'''# Causal banking research and proposal

[Current integrated reader]({Path(full['path']).name}) · [Aligned sponsor]({Path(sponsor['path']).name}) · [Active master](program/master-live.md).

The reviewed programme has produced a {pages:,}-page continuation and {sponsor['pages']}-page sponsor. Main recommendations and four journeys are integrated; the contextual continuation repairs notation, argument transitions, chapter roles and confirmed stale prose. [Execution record](writing-repair/2026-10-29/README.md).

The final-edit deletion audit passes: {edits} exact changes, 456 inherited mapped sources compiled once, all original citation keys and labels retained, and 1,607 protected identities verified. [Audit](writing-repair/2026-10-29/deletion-audit.md).

W04 remains active. {coverage} Next: {next_text}. The expanded input assembly determines chapter scope; primary-source reading alone cannot certify following sections. W08 owns the final whole-book continuity and citation review. Fresh visual and independent acceptance remain open. Frontier source coverage remains 85 inspected/28 unread.

Run python3 tools/scientific_program.py next and check. Historical python3 tools/causal_program.py status/check retain their original scope. No unattended worker is running. Proposal completion, prototype qualification and bank adoption remain separate.
''')
(R/'docs/program/master-current.md').write_text(f'''# Current master programme

29 October 2026. Use [master-live.md](master-live.md), [the reviewed programme](writing-gap-closure-2026-10-29.md) and scientific-priorities.json. Frozen master-program.md/state.json retain historical identities.

The current candidate has {pages:,} pages and a {sponsor['pages']}-page sponsor. Preservation and publication checks pass for {edits} ledgered edits. {coverage} Continue W04 at {next_text}, then W08 for whole-book continuity and citation presentation. Full writing-standard, fresh visual and independent acceptance remain open.

Run python3 tools/scientific_program.py next and check. No unattended worker is running; bank qualification and adoption are later gates.
''')
(R/'docs/program/master-live.md').write_text(f'''# Active master: scholarly integration and remaining writing work

29 October 2026. [Reader](../{Path(full['path']).name}) · [Sponsor](../{Path(sponsor['path']).name}) · [Programme](writing-gap-closure-2026-10-29.md) · [Programme review](../reviews/writing-gap-program-review-2026-10-29.md) · [Candidate review](../reviews/writing-gap-terminal-review-2026-10-29.md).

## Delivered continuation

The {pages:,}-page candidate consolidates software, assistance and investment conclusions, connects the four journeys to appropriate evidence and inference, and preserves the mathematical and comparative corpus. The continuation explains notation and clocks, develops transitions between nested treatments, removes confirmed stale instructions and clarifies the supporting role of detailed software comparisons. The aligned sponsor has {sponsor['pages']} pages.

The post-build audit passes for {edits} exact edits: all 456 inherited mapped sources compile once, all 1,463 original citation keys and labels survive, 1,607 protected identities and 9,969 source bindings verify. Three already-audited source keys remain integrated. The original 1,851-page integration delivery and its receipts are preserved separately. No distinct derivation or numerical finding was discarded. [Deletion audit](../writing-repair/2026-10-29/deletion-audit.md).

## Standard and work remaining

The standard is a connected scholarly argument from decision and information clock through model, assumptions, identification, estimation, uncertainty, monetary consequence and serious comparison. FinMarketing supplies the developed-exposition benchmark; clear economic prose is the language benchmark. Page count and checks cannot certify it.

W01/W02/W03/W05 have delivered their scoped outputs. W06/W07 verify the current revision and recur after further edits. **W04 remains active: {coverage}** Continue at {next_text}, using [the actual assembled chapter queue](../writing-repair/2026-10-29/chapter-review.md). W08 then requires a complete-book review of continuity, purposeful repetition and citation usability. Neither work package is complete.

Coverage follows the expanded TeX input order, including sibling sources after a chapter's primary file. A reading record binds inspected text to hashes and cannot cover unmentioned additions. The programme checker now rejects mismatched counts, stale publication identities and audits predating the current edit ledger.

Fresh visual review is pending under the inherited session image limit. The reader has {full['warnings']['Underfull']} underfull warnings, no overfull boxes or unresolved references, and no empty pages or out-of-page text. Human editorial and independent scientific acceptance remain separate. Consequential method/language/version/rights comparisons and 28 unread originals remain source-survey work; the current frontier count is 85/28.

Completed public/generated experiments are evidence to integrate, not new runs to claim. Native package trials, matched live-model evaluation, real bank truth and prices, operating acceptance and adoption retain their own obligations. They do not excuse unfinished writing.

## Execute

Run python3 tools/scientific_program.py next and check. After each substantive manuscript batch, rebuild, audit exact deletions and refresh current status with python3 tools/refresh_writing_status_20261029.py. Historical python3 tools/causal_program.py status/check remain available. Preserve master-program.md/state.json and original source evidence. Literature cutoff: 7 October 2026. No sibling edits, agents or unattended worker.
''')
p=R/'docs/program/writing-gap-closure-2026-10-29.md';s=p.read_text();start=s.index('## Executed outcome');end=s.index('## Continuation review',start)
s=s[:start]+f'''## Executed outcome

The first integration delivery (1,851 pages, 75 edits) remains preserved in deliveries/first-integration. The current continuation has {pages:,} pages, a {sponsor['pages']}-page sponsor and {edits} ledgered edits, with a passing final-edit deletion audit. W06/W07 are recurring checks of the actual revision. {coverage} W04 continues at {next_text}; W08 remains pending. This is not completion of the whole writing programme.

'''+s[end:];p.write_text(s)
p=O/'README.md';s=p.read_text();s=re.sub(r'The reader has [\d,]+ pages and the sponsor four\.',f'The reader has {pages:,} pages and the sponsor four.',s);start=s.index('## Continue');s=s[:start]+f'''## Continue

W04 remains active. {coverage} Next: {next_text}, including every source assigned by the expanded TeX assembly. W08 then reviews whole-book continuity and citation presentation. The {edits}-edit preservation audit certifies the changed material, not untouched prose. Fresh visual, independent editorial/scientific and source-survey acceptance remain open.

The original 1,851-page integration and its receipts are preserved in deliveries/first-integration. Intermediate audit receipts are preserved under deliveries/continuation-96, continuation-104, continuation-106, continuation-113 and continuation-121. Refresh active dashboards after a final build/audit with python3 tools/refresh_writing_status_20261029.py. No agents or unattended worker are running.
''';p.write_text(s)
(O/'deletion-audit.md').write_text(f'''# Post-execution deletion audit

Result: **pass for the current {edits}-edit continuation**, after its last manuscript edit and build. This is preservation and author semantic review, not whole-book editorial acceptance.

- {edits} exact replacements/additions/relocations replay to the delivered sources. Full before/after text is in full-deletion-ledger.md and all-inherited-content.diff.
- All 456 inherited mapped sources compile once; all 1,463 original citation keys and labels survive. Three previously audited source keys remain integrated.
- All 1,607 protected identities and seven referenced assets verify. The six during-run changes remain reconciled with both observed versions preserved.
- No distinct derivation, numerical result or adverse finding is removed. The continuation adds definitions for expectation and empirical operators; continuation-math-dispositions.json binds those exact additions to edit 76. No mathematical display changed in this continuation.
- Chapter 34 source-handling administration moved to chapter34-source-provenance.md; its evidential limits and all scientific comparisons remain in the reader. semantic-preservation-review.md records other substantive destinations.
- All 9,969 source bindings verify. The {pages:,}-page reader and {sponsor['pages']}-page sponsor pass reference and all-page text/geometry checks. Fresh visual acceptance remains pending.

The first continuation audit rejected the new inline notation until an exact edit/hash/occurrence disposition was supplied. Its failure remains in continuation-first-audit-failure.json. The 131-edit numeric-token failure and lexical repair remain in continuation-131-numeric-token-failure.json and numeric-token-check-repair.json: full version literals survive whitespace-only repairs, with no number-specific exemption. No generic permission to change mathematics was introduced. Exact replay, occurrence checks and author semantic review complement one another; numeric-token retention alone cannot establish scientific meaning.
''')
p=R/'docs/reviews/writing-gap-terminal-review-2026-10-29.md';s=p.read_text();s=re.sub(r'The [\d,]+-page integrated-argument reader',f'The {pages:,}-page integrated-argument reader',s);s=re.sub(r'\| 4\. Chapter exposition \|.*',f'| 4. Chapter exposition | {coverage} Complete assembly, including sibling inputs, defines the review scope. | Read the remaining {remaining} chapters in final position, then complete W08. |',s);s=re.sub(r'The exact ledger has \d+ edits\.',f'The exact ledger has {edits} edits.',s);s=re.sub(r'Continue W04 at Chapter \d+, .*?then the remaining chapters in chapter-review.json\.',f'Continue W04 at {next_text}, then the remaining chapters in chapter-review.json.',s);s=s.replace('Fresh-session visual inspection, human voice review','W08 whole-book/citation review, fresh-session visual inspection, human voice review');s+='\n## Continuation outcome\n\nThe continuation adds contextual reading and repairs across learning, longitudinal, panel, observation and detailed software chapters. It clarifies expectation/empirical notation, fold versus full-sample exposition, clocks, nested-study roles and stale chapter transitions. The heading about an absence of observations now states its intended evidential meaning. Additional discovery comparisons preserve the distinctions between graph ambiguity, fitted coefficients, numerical diagnostics and intervention results. The temporal and identification continuation reconciles superseded CD-NOD, TACD, BLIP, GCM and LiNGAM access claims and carries the specific y0 conditional-path restriction into later summaries. The attention explanation now precedes its evaluation protocol; new chapter transitions connect the existing derivations. All distinct equations, numerical findings, counterexamples and alternatives remain.\n\nReview-control defects were also repaired: expanded input traversal prevents primary-file reading from certifying unread sibling sections, and programme checks now bind active counts and publication claims to the actual source/audit identities. The first notation audit failure and a deliberately observed stale-state failure remain recorded. None of these checks certifies natural prose or independent scientific validity.\n';# Replace this repeated continuation section on later refreshes.
marker='\n## Continuation outcome\n';parts=s.split(marker);s=parts[0]+marker+parts[-1] if len(parts)>2 else s;p.write_text(s)
print(json.dumps({'reader_pages':pages,'edits':edits,'reviewed':done,'remaining':remaining,'next_chapter':nextc['chapter'] if nextc else None}))
from link_scientific_delivery_20261029 import refresh as refresh_scientific_delivery_links
refresh_scientific_delivery_links()
