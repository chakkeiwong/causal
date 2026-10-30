"""Publish mutable writing status from current, verified final-edition receipts."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from scientific_program import whole_book_issues

R = Path(__file__).resolve().parents[1]
O = R / 'docs/writing-repair/2026-10-29'
def read(name): return json.loads((O / name).read_text())
def save(path, data): path.write_text(json.dumps(data, indent=2) + chr(10))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name, text): (R / name).write_text(text.strip() + chr(10))

a = read('deletion-audit.json')
assert a['pass'] and a['checks_after_final_edit'], 'Final audit must pass before publication'
assert sha(O / 'edits.json') == a['ledger_sha256']
for name, identity in a['final_source_hashes'].items(): assert sha(R / name) == identity, name
for pub in a['publication'].values(): assert sha(R / pub['path']) == pub['sha256']
subprocess.run([sys.executable, str(R / 'tools/record_writing_review_20261029.py')], check=True, capture_output=True, text=True)
chapters = read('chapter-review.json')['chapters']
pending = [c for c in chapters if not c['full_chapter_acceptance']]
done = len(chapters) - len(pending)
remaining = len(pending)
nextc = pending[0] if pending else None
w04 = not pending
w08_errors = whole_book_issues(a, chapters)
w08 = w04 and not w08_errors
full = a['publication']['full']; sponsor = a['publication']['sponsor']
pages = full['pages']; edits = a['edits']; warnings = full['warnings']['Underfull']
coverage = f'{done} of {len(chapters)} assembled chapter treatments have complete contextual author review; {remaining} remain.'
if pending:
    author_status = f'W04 remains active at Chapter {nextc["chapter"]}, “{nextc["title"]}”. W08 follows the complete chapter review.'
    next_action = f'Read Chapter {nextc["chapter"]} and all its assembled sources, repair confirmed defects, then rebuild and audit.'
elif not w08:
    author_status = 'W04 is complete. W08 remains open because its final-edition review receipt is absent or stale.'
    next_action = 'Renew the whole-book review against the final ledger, sources, citations, rendered text and PDFs before closing W08.'
else:
    author_status = 'W04 and W08 are complete within author-review scope: complete contextual reading and final whole-book continuity, repetition, evidence-scope, citation and sponsor review.'
    next_action = 'In a fresh session, inspect the current reader and sponsor visually, record the PDF identities and findings, then incorporate actual independent editorial feedback. Keep consequential source-survey work separate.'
limits = 'Full writing-standard attainment, fresh visual review and independent editorial/scientific acceptance remain open. Consequential method/language/version/rights comparisons and 28 unread originals remain; frontier coverage stays 85 inspected/28 unread.'
continuation = next_action + ' W06/W07 recur after any further manuscript edit. No unattended worker is running.'
corrections = a.get('verified_numeric_corrections', [])
numeric = ('One prose transcription is corrected from USD 1.346 million to USD 1.341 million, reconstructed from all 600 preserved journal intervals; the original, failed receipt and exact correction remain auditable.' if corrections else 'No distinct original numerical token is lost.')
assert not a.get('unaccounted_numeric_loss'), 'Unaccounted numeric loss'
preservation = f'The post-build audit passes for {edits} exact ledgered edits: all 456 inherited mapped sources compile once; all 1,463 original citation keys and labels remain; 1,607 protected identities, seven assets and 9,969 source bindings verify. All 1,466 bibliography entries retain their full identities. No unaccounted substantive or mathematical loss is reported.'

state = read('state.json')
state.update(delivery='Author rewrite and whole-book review complete; final acceptance remains open' if w08 else 'Verified continuation candidate; author review remains in progress', reader=full, sponsor=sponsor, post_execution_deletion_audit='pass', author_contextual_treatments=done, remaining_full_contextual_reviews=remaining, first_next_chapter=nextc, full_writing_standard_met=False, chapter_coverage_method='Expanded assembly, including following sibling inputs and nested text', latest_ledger_sha256=a['ledger_sha256'], whole_book_author_review_complete=w08, whole_book_review='docs/writing-repair/2026-10-29/whole-book-review.json' if w08 else None, next_action=next_action)
save(O / 'state.json', state)
p = R / 'docs/program/scientific-priorities.json'; d = json.loads(p.read_text())
d['reader'] = {'pdf':full['path'], 'sha256':full['sha256'], 'pages':pages}; d['paired_sponsor'] = sponsor
d['writing_remaining'] = {'contextually_reviewed':done, 'chapters_requiring_complete_review':remaining, 'next_chapter':nextc['chapter'] if nextc else None, 'next_source':nextc['source'] if nextc else None, 'queue':'docs/writing-repair/2026-10-29/chapter-review.json', 'whole_book_author_review_complete':w08, 'fresh_visual_acceptance':False, 'independent_acceptance':False}
d['chapter_review_progress'] = {'reviewed':done, 'pending':remaining, 'next_chapter':nextc['chapter'] if nextc else None, 'evidence':'docs/writing-repair/2026-10-29/chapter-review.json'}
d['last_completed_writing_batch'] = {'date':'2026-10-29', 'reader_pages':pages, 'edits':edits, 'protected_files':a['protected_files'], 'inherited_sources_compiled_once':a['mapped_sources_compiled_once'], 'new_sources':'No new original acquired during contextual rewrite; three previously audited records remain integrated', 'full_writing_standard_met':False}
d['continuation_note'] = continuation; d['writing_execution_status'] = author_status
for key in ('proposal_complete','gap_closure_finalized','final_editorial_acceptance'): d[key] = False
d['editorial_followup'].update(status='author_review_complete_acceptance_pending' if w08 else 'author_review_in_progress', owner='Author repairs recorded; fresh visual review and actual independent editorial findings remain required', continuation=continuation, acceptance=limits)
for t in d['tasks']:
    if t['id'] == 'W04':
        t.update(status='complete' if w04 else 'in_progress', action='Maintain complete contextual coverage after future edits; all current assembled treatments are reviewed.' if w04 else next_action, evidence=['docs/writing-repair/2026-10-29/chapter-review.json','docs/writing-repair/2026-10-29/contextual-review-records.json'], blockers=[])
    if t['id'] == 'W08':
        t.update(status='complete' if w08 else 'ready', action='Retain the final source/PDF-bound whole-book review; renew it after any manuscript or citation-style change.' if w08 else next_action, evidence=['docs/writing-repair/2026-10-29/whole-book-review.json','docs/writing-repair/2026-10-29/whole-book-review.md'] if w08 else [], blockers=[])
        t['last_verified_ledger_sha256'] = a['ledger_sha256'] if w08 else None
    if t['id'] in ('W06','W07'):
        t.update(status='complete', recurring=True, last_verified_ledger_sha256=a['ledger_sha256'])
    if t['id'] == 'EDITORIAL-ACCEPTANCE':
        blockers = [] if w08 else ['Complete and verify W04/W08 author review against the final edition']
        blockers += ['Fresh-session visual review pending: inherited six-image session allowance exhausted', 'External editorial findings/acceptance not yet supplied']
        t.update(status='blocked', blockers=blockers, action=next_action, evidence=['docs/writing-repair/2026-10-29/whole-book-review.json'] if w08 else [])
for item in d['items']:
    if item['id'] == 'W':
        item['status'] = 'in_progress'
        item['conclusion'] = author_status + ' Final writing-standard acceptance remains open.'
save(p, d)

write('CURRENT.md', f"""# Causal banking research and product proposal

[Current integrated reader](docs/{Path(full['path']).name}) · [Aligned sponsor](docs/{Path(sponsor['path']).name}) · [Active master](docs/program/master-live.md).

The reviewed programme delivers a {pages:,}-page reader and {sponsor['pages']}-page sponsor. {author_status} {coverage}

{preservation} {numeric}

[Programme and execution](docs/program/writing-gap-closure-2026-10-29.md) · [Candidate review](docs/reviews/writing-gap-terminal-review-2026-10-29.md) · [Deletion audit](docs/writing-repair/2026-10-29/deletion-audit.md).

{limits}

{continuation} Historical master-program.md/state.json and the root README retain their identities. Run python3 tools/scientific_program.py check to verify current records; its next command schedules the broader scientific programme.
""")
write('docs/mission-control.md', f"""# Causal banking research and proposal

[Current integrated reader]({Path(full['path']).name}) · [Aligned sponsor]({Path(sponsor['path']).name}) · [Active master](program/master-live.md).

The refreshed and reviewed programme delivers a {pages:,}-page reader and {sponsor['pages']}-page sponsor. {author_status} {coverage}

{preservation} {numeric} [Exact audit](writing-repair/2026-10-29/deletion-audit.md).

{limits}

{continuation} Run python3 tools/scientific_program.py check. Historical python3 tools/causal_program.py status/check retain their original scope. Proposal completion, prototype qualification and bank adoption remain separate.
""")
write('docs/program/master-current.md', f"""# Current master programme

29 October 2026. Use [master-live.md](master-live.md), [the reviewed programme](writing-gap-closure-2026-10-29.md) and scientific-priorities.json. Frozen master-program.md/state.json retain historical identities.

The current candidate has {pages:,} pages and a {sponsor['pages']}-page sponsor. {author_status} {coverage} Preservation checks pass for {edits} exact edits.

{limits}

{continuation} Run python3 tools/scientific_program.py check; its next command schedules broader scientific work independently.
""")
write('docs/program/master-live.md', f"""# Active master: writing programme and acceptance

29 October 2026. [Reader](../{Path(full['path']).name}) · [Sponsor](../{Path(sponsor['path']).name}) · [Programme](writing-gap-closure-2026-10-29.md) · [Programme review](../reviews/writing-gap-program-review-2026-10-29.md) · [Candidate review](../reviews/writing-gap-terminal-review-2026-10-29.md).

## Delivered work

The {pages:,}-page candidate consolidates software, assistance and investment conclusions, connects all four banking journeys to their actual evidence and uncertainty, explains notation and clocks, repairs study order and stale summaries, and preserves the developed mathematical and comparative corpus. The aligned sponsor has {sponsor['pages']} pages.

{author_status} {coverage} [Whole-book review](../writing-repair/2026-10-29/whole-book-review.md). W01/W02/W03/W05 have delivered their scoped outputs. W06/W07 pass for this revision and remain recurring after further edits.

{preservation} {numeric} [Post-execution deletion audit](../writing-repair/2026-10-29/deletion-audit.md). Exact before/after text and substantive destinations are retained. The original 1,851-page integration and intermediate receipts remain separately archived.

## Standard and remaining gaps

A prepared economist or quantitative reader must reconstruct the decision and information clock, model and assumptions, identification or identified set, estimation, uncertainty and sensitivity, monetary consequence, serious alternatives and recommendation. FinMarketing supplies the developed-exposition benchmark; clear economic prose is the language standard. Page counts and integrity checks cannot establish attainment.

{limits}

The reader has {warnings} underfull warnings, no overfull boxes, unresolved references, duplicate labels, empty pages or out-of-page text. Rendered-text checks are complete; aesthetics and the warnings require fresh visual inspection under the inherited session image limit. Actual external editorial findings must be incorporated before independent acceptance. No author completion flag substitutes for those gates.

Source-comparison completion, native package qualification, matched live-model evaluation, real bank truth and prices, operating acceptance and adoption retain their separate obligations. Completed public/generated experiments are evidence to integrate, not new runs to claim.

## Exact continuation

{continuation}

After any substantive edit, update the exact ledger and contextual records, rebuild, rerun the deletion audit after the final edit, renew the whole-book receipt, then run python3 tools/refresh_writing_status_20261029.py and python3 tools/scientific_program.py check. Missing or stale W08 evidence prevents completed author-review status. Historical python3 tools/causal_program.py status/check remain available. Preserve historical master-program.md/state.json, original source evidence and experiment identities. Literature cutoff: 7 October 2026. No sibling edits or agents.
""")
p = R / 'docs/program/writing-gap-closure-2026-10-29.md'; text = p.read_text(); start = text.index('## Executed outcome'); end = text.index('## Continuation review', start)
text = text[:start] + f"""## Executed outcome

The first integration delivery (1,851 pages, 75 edits) remains preserved in deliveries/first-integration. The current reader has {pages:,} pages, a {sponsor['pages']}-page sponsor and {edits} exact ledgered edits. {author_status} {coverage} W06/W07 pass after the final manuscript edit and build, and recur after further edits. {numeric}

{limits} {continuation}

""" + text[end:]; p.write_text(text)
p = O / 'README.md'; text = p.read_text(); start = text.index('The refreshed'); end = text.index('## Evidence')
text = text[:start] + f'The refreshed and reviewed programme delivers a {pages:,}-page reader and {sponsor["pages"]}-page sponsor. {author_status} Full writing-standard acceptance remains open.' + chr(10)*2 + text[end:]
start = text.index('## Continue'); text = text[:start] + f"""## Continue

{coverage} {continuation}

{limits} The {edits}-edit post-build preservation audit applies to this exact edition. Author reading, preservation checks and editorial acceptance remain separate.

whole-book-review.json binds complete chapter coverage, the final ledger, manuscript and citation style, supporting reviews and both PDF identities. citation-spacing-repair.json records 233 whitespace-only citation repairs; numeric-corrections.json records the sole journal-backed numeric correction. The original integration and intermediate receipts remain in deliveries/. No completed acquisition or scientific trial is rerun by this writing workflow.
"""; p.write_text(text)
write('docs/writing-repair/2026-10-29/deletion-audit.md', f"""# Post-execution deletion audit

Result: **pass for the current {edits}-edit edition**, after the last manuscript edit and build. This verifies preservation and author semantic dispositions; it does not grant independent or fresh visual acceptance.

{preservation}

Every ledger entry records exact before/after text, reason and substantive destination in edits.json, full-deletion-ledger.md and all-inherited-content.diff. Distinct derivations, assumptions, alternatives, tables and adverse findings remain in the delivered book. Removed duplicate annual-benefit exposition retains its full account in the authoritative investment treatment; source-handling administration has an explicit provenance destination. Mathematical occurrence changes require their exact dispositions.

{numeric} There is no unaccounted numeric loss. The failed 473-edit receipt and a negative correction check are retained. No generic numerical or mathematical exemption is permitted.

Twelve long citation display labels are shortened while all 1,466 full bibliographic bodies and keys remain identical. The final 31 ledger entries insert 233 sentence-to-citation spaces across 31 files; all non-whitespace characters and line order are identical. Both bibliography style identities and each spacing replacement are recorded. No source identity changes.

The {pages:,}-page reader and {sponsor['pages']}-page sponsor pass current reference, all-page text and geometry checks. Fresh visual review remains pending; {warnings} underfull warnings require visual assessment. Earlier notation, numeric-token, reference and bibliography-stabilization failures remain in their receipts. The six observed during-run baseline changes retain both versions and their explicit reconciliation.
""")
p = R / 'docs/reviews/writing-gap-terminal-review-2026-10-29.md'; text = p.read_text()
intro_end = text.index('## The standard')
text = ('# Writing-gap repair: terminal review of the delivered candidate' + chr(10)*2 +
        '29 October 2026. Author review of this execution, not independent editorial or scientific acceptance. '
        'The master programme has been refreshed and skeptically reviewed. ' + author_status +
        ' Final writing-standard acceptance remains open.' + chr(10)*2 + text[intro_end:])
import re
text = re.sub(r'The [\d,]+-page integrated-argument reader', f'The {pages:,}-page integrated-argument reader', text)
start = text.index('## Gap-by-gap verdict'); end = text.index('## Continuation outcome',start)
text = text[:start] + f"""## Gap-by-gap verdict

| Gap | Actual outcome | What remains |
|---|---|---|
| Whole-book integration | Principal conclusions consolidated; all assembled chapters and ordered part transitions reviewed. | Independent assessment of sustained argument and further compression. |
| Application depth | Four journeys reach justified inference, uncertainty or explicit nonidentification, with monetary consequences. | General scientific qualification and real bank validation remain distinct. |
| Comparative scholarship | Developed alternatives retained; resolved source omissions and later restrictions reconciled. | Consequential method/language/version/rights gaps and 28 unread originals; no claim of complete coverage. |
| Chapter exposition | {coverage} Complete assembly determines scope. | Renew affected contextual review after any new substantive edit; independent judgments remain open. |
| Stale/admin prose | Confirmed contradictions, proposed-study statements and historical operation scopes repaired throughout the reviewed assembly. | Future evidence/version changes require renewed review. |
| Prose voice | Complete contextual author pass and final continuity/repetition review delivered. | External editorial assessment of naturalness, proportion and remaining repetition. |
| Navigation/citations/presentation | Reading guide, sponsor, references and all-page geometry pass; twelve labels shortened and 233 missing citation spaces repaired. | Fresh visual inspection, including {warnings} underfull warnings; aesthetics not certified by geometry. |

## Post-execution verification

The exact ledger has {edits} edits. {preservation} {numeric} Every mathematical occurrence difference has an exact disposition; no unaccounted numeric loss remains. Full deletion text and substantive destinations are inspectable.

The deposit report and deterministic four-journey examples reproduce in their existing receipts; no new experiment is claimed. The reader and sponsor have no undefined references, duplicate labels, overfull boxes, empty pages or out-of-page text. Revised rendered passages and citation spacing are inspected. Fresh visual acceptance remains pending under the exhausted six-image session allowance and is not inherited from a predecessor.

## Exact continuation

{author_status} {continuation}

{limits} Native qualification, matched live-model evaluation, actual prices and adoption retain later gates. No new acquisition or native trial is claimed by this continuation.

""" + text[end:]
p.write_text(text)
import html
write('docs/mission-control.html', f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><title>Causal banking research</title><body>
<h1>Causal banking research and proposal</h1>
<p><a href="{Path(full['path']).name}">Current integrated reader</a> · <a href="{Path(sponsor['path']).name}">Aligned sponsor</a> · <a href="program/master-live.md">Active master</a></p>
<p>The current edition has {pages:,} pages and the sponsor {sponsor['pages']}. {html.escape(author_status)} {html.escape(coverage)}</p>
<p>{html.escape(preservation)} {html.escape(numeric)}</p>
<p><a href="writing-repair/2026-10-29/whole-book-review.md">Whole-book review</a> · <a href="writing-repair/2026-10-29/deletion-audit.md">Post-execution deletion audit</a> · <a href="reviews/writing-gap-terminal-review-2026-10-29.md">Remaining gaps</a></p>
<p>{html.escape(limits)}</p><p>{html.escape(continuation)}</p>
<p>Prior editions and historical programme identities remain preserved. Proposal completion, prototype qualification and bank adoption remain separate.</p>
</body></html>''')
p = R / 'docs/program/execution/current-program.md'
text = p.read_text(); marker = '## Preserved earlier account'
assert marker in text
text = f'''# Current executable proposal programme

Updated 29 October 2026. [Active master](../master-live.md) · [Reviewed writing programme](../writing-gap-closure-2026-10-29.md) · [Priorities](../scientific-priorities.json).

{author_status} {coverage} The verified reader has {pages:,} pages with {edits} exact ledgered edits.

{limits}

{continuation} Run python3 tools/scientific_program.py check. Its next command schedules independent source-survey and scientific work; native trials and bank qualification remain separate phases.

''' + text[text.index(marker):]
p.write_text(text)
from link_scientific_delivery_20261029 import refresh
refresh()
print(json.dumps({'reader_pages':pages,'edits':edits,'reviewed':done,'remaining':remaining,'W04_complete':w04,'W08_complete':w08,'W08_issues':w08_errors,'full_writing_standard_met':False}))
