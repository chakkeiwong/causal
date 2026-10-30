"""Outcome-based view of the active research and editorial programme."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'docs/program/scientific-priorities.json'


def view():
    state = json.loads(PLAN.read_text())
    completed = {x['id'] for x in state['items'] if x['status'] == 'complete'}
    ready = [x for x in state['items'] if x['status'] in ('ready', 'in_progress')
             and set(x['depends_on']) <= completed]
    ready.sort(key=lambda x: (x['priority'], x['status'] != 'in_progress', x['id']))
    return state, ready


def eligible_tasks(state):
    tasks = state.get('tasks', [])
    completed = {x['id'] for x in tasks if x['status'] == 'complete'}
    ready = [x for x in tasks if x['status'] in ('ready', 'in_progress')
             and set(x.get('depends_on', [])) <= completed
             and not x.get('blockers')]
    return sorted(ready, key=lambda x: (x.get('priority', 1), x['id']))


def task_issues(state):
    tasks = state.get('tasks', [])
    lookup = {x['id']: x for x in tasks}
    issues = []
    if len(lookup) != len(tasks):
        issues.append('Duplicate scientific task')
    for task in tasks:
        for key in ['stream', 'question', 'action', 'required_result', 'status']:
            if not task.get(key): issues.append(task['id'] + ': missing ' + key)
        if task.get('stream') not in {x['id'] for x in state['items']}:
            issues.append(task['id'] + ': unknown stream')
        for dep in task.get('depends_on', []):
            if dep not in lookup: issues.append(task['id'] + ': unknown dependency ' + dep)
        if task['status'] == 'complete' and not task.get('evidence'):
            issues.append(task['id'] + ': completed task lacks evidence')
        if task['status'] == 'blocked' and not task.get('blockers'):
            issues.append(task['id'] + ': blocked task lacks a concrete blocker')
        for path in task.get('evidence', []):
            if not (ROOT/path).is_file(): issues.append(task['id'] + ': missing evidence ' + path)
    visiting, visited = set(), set()
    def visit(name):
        if name in visiting:
            issues.append('Scientific task dependency cycle at ' + name)
            return
        if name in visited or name not in lookup: return
        visiting.add(name)
        for dep in lookup[name].get('depends_on', []): visit(dep)
        visiting.remove(name);visited.add(name)
    for name in lookup: visit(name)
    return issues


def whole_book_issues(audit, chapters, *, read_json=None, digest_file=None):
    """Check final author-review identities; this does not judge prose quality."""
    base = 'docs/writing-repair/2026-10-29/'
    if read_json is None:
        read_json = lambda name: json.loads((ROOT / name).read_text())
    if digest_file is None:
        digest_file = lambda name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    issues = []
    try:
        receipt = read_json(base + 'whole-book-review.json')
        if receipt.get('status') != 'complete_author_review':
            issues.append('W08 lacks a completed author-review receipt')
        if (receipt.get('chapters') != len(chapters) or not chapters or
                any(not c['full_chapter_acceptance'] for c in chapters)):
            issues.append('W08 lacks complete contextual chapter coverage')
        ledger = digest_file(base + 'edits.json')
        if receipt.get('ledger_sha256') != ledger or audit.get('ledger_sha256') != ledger:
            issues.append('W08 receipt predates the current edit ledger')
        sources = receipt.get('final_source_hashes', {})
        if not sources or sources != audit.get('final_source_hashes'):
            issues.append('W08 source identities differ from the final audit')
        style = base + 'causalplainnat-reading.bst'
        if style not in sources:
            issues.append('W08 omits the successor citation-style identity')
        if not {base + 'sponsor-body.tex',
                'docs/causal_banking_sponsor_integrated_2026-10-29.tex'} <= sources.keys():
            issues.append('W08 omits the sponsor source identities')
        if not any(name.startswith(base + 'references-') and name.endswith('.bib') for name in sources):
            issues.append('W08 omits the bibliography source identities')
        for name, identity in sources.items():
            if digest_file(name) != identity:
                issues.append('W08 reviewed source changed: ' + name)
        if receipt.get('publication') != audit.get('publication'):
            issues.append('W08 publication receipt differs from the final audit')
        for publication in receipt.get('publication', {}).values():
            if digest_file(publication['path']) != publication['sha256']:
                issues.append('W08 reviewed PDF changed: ' + publication['path'])
        required = {base + name for name in (
            'whole-book-review.md', 'whole-book-boundaries.json',
            'whole-book-repetition-scan.json', 'contextual-review-records.json',
            'chapter-review.json', 'citation-presentation-verification.json',
            'citation-style-edit.json', 'numeric-corrections.json',
            'citation-spacing-repair.json',
            f"rendered-continuation-{audit['edits']}.json")}
        files = receipt.get('review_files', {})
        if required - files.keys():
            issues.append('W08 omits required final review evidence')
        for name, identity in files.items():
            if digest_file(name) != identity:
                issues.append('W08 supporting review changed: ' + name)
        rendered = read_json(base + f"rendered-continuation-{audit['edits']}.json")
        if (rendered.get('edits') != audit.get('edits') or
                rendered.get('publication') != audit['publication']['full']):
            issues.append('W08 rendered-text inspection refers to another edition')
    except (OSError, KeyError, TypeError, ValueError) as exc:
        issues.append('W08 evidence cannot be verified: ' + str(exc))
    return issues


def writing_issues(state):
    """Verify the current editorial receipt, without certifying prose quality."""
    if not state.get('active_writing_plan'):
        return []
    issues = []
    base = ROOT / 'docs/writing-repair/2026-10-29'
    def read(name):
        return json.loads((base / name).read_text())
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        chapters = read('chapter-review.json')['chapters']
        pending = [c for c in chapters if not c['full_chapter_acceptance']]
        reviewed = len(chapters) - len(pending)
        expected = (reviewed, len(pending), pending[0]['chapter'] if pending else None)
        progress = state.get('chapter_review_progress', {})
        remaining = state.get('writing_remaining', {})
        if (progress.get('reviewed'), progress.get('pending'), progress.get('next_chapter')) != expected:
            issues.append('Writing chapter progress is stale')
        if (remaining.get('contextually_reviewed'), remaining.get('chapters_requiring_complete_review'), remaining.get('next_chapter')) != expected:
            issues.append('Writing remaining-work inventory is stale')
        delivery = read('state.json')
        next_chapter = delivery.get('first_next_chapter') or {}
        if (delivery.get('author_contextual_treatments'), delivery.get('remaining_full_contextual_reviews'), next_chapter.get('chapter')) != expected:
            issues.append('Writing delivery state is stale')
        tasks = {t['id']: t for t in state.get('tasks', [])}
        if pending and tasks.get('W04', {}).get('status') == 'complete':
            issues.append('W04 is complete despite unread chapter text')
        if pending and f"Chapter {pending[0]['chapter']}" not in tasks.get('W04', {}).get('action', ''):
            issues.append('W04 next action does not match the chapter queue')
        if any(c['full_chapter_acceptance'] and c.get('unreviewed_assembled_sources') for c in chapters):
            issues.append('Accepted chapter contains unread assembled sources')
        for review in read('contextual-review-records.json')['reviews']:
            for source in review['sources']:
                path = ROOT / source['path']
                if source.get('read_sha256') and path.is_file():
                    first, last = source['read_lines']
                    body = '\n'.join(path.read_text().splitlines()[first-1:last]) + '\n'
                    valid = hashlib.sha256(body.encode()).hexdigest() == source['read_sha256']
                else:
                    valid = path.is_file() and digest(path) == source['sha256']
                if not valid:
                    issues.append('Reviewed chapter source changed: ' + source['path'])
        audit = read('deletion-audit.json')
        if not audit.get('pass') or not audit.get('checks_after_final_edit'):
            issues.append('Current post-edit preservation audit has not passed')
        if audit.get('ledger_sha256') != digest(base / 'edits.json'):
            issues.append('Deletion audit predates the current edit ledger')
        if audit.get('edits') != state.get('last_completed_writing_batch', {}).get('edits'):
            issues.append('Writing batch edit count is stale')
        for name, sha in audit.get('final_source_hashes', {}).items():
            path = ROOT / name
            if not path.is_file() or digest(path) != sha:
                issues.append('Audited manuscript source changed: ' + name)
        for kind, state_key in [('full', 'reader'), ('sponsor', 'paired_sponsor')]:
            publication = audit['publication'][kind]
            advertised = state.get(state_key, {})
            advertised_path = advertised.get('pdf', advertised.get('path'))
            if (advertised_path != publication['path'] or
                    advertised.get('sha256') != publication['sha256'] or
                    advertised.get('pages') != publication['pages']):
                issues.append('Advertised ' + kind + ' publication is stale')
            path = ROOT / publication['path']
            if not path.is_file() or digest(path) != publication['sha256']:
                issues.append('Delivered ' + kind + ' PDF differs from its audit')
            delivered = delivery['reader' if kind == 'full' else 'sponsor']
            if delivered.get('sha256') != publication['sha256'] or delivered.get('pages') != publication['pages']:
                issues.append('Delivery ' + kind + ' publication is stale')
        for task_id in ('W06', 'W07'):
            task = tasks.get(task_id, {})
            if (task.get('status') == 'complete' and
                    task.get('last_verified_ledger_sha256') != audit.get('ledger_sha256')):
                issues.append(task_id + ': recurring receipt refers to another revision')
        whole_book_failures = []
        if tasks.get('W08', {}).get('status') == 'complete':
            whole_book_failures = whole_book_issues(audit, chapters)
            issues.extend(whole_book_failures)
        required_author_work = (not pending and not whole_book_failures and
                                tasks.get('W04', {}).get('status') == 'complete' and
                                tasks.get('W08', {}).get('status') == 'complete')
        fresh_visual = all(x.get('fresh_visual_acceptance')
                           for x in audit['publication'].values())
        if delivery.get('full_writing_standard_met') and not (required_author_work and fresh_visual):
            issues.append('Writing-standard completion lacks required author or visual work')
        if any(state.get(k) for k in ('proposal_complete', 'gap_closure_finalized', 'final_editorial_acceptance')):
            if not (required_author_work and fresh_visual):
                issues.append('Programme completion contradicts unfinished writing or visual review')
        if state.get('final_editorial_acceptance') and tasks.get('EDITORIAL-ACCEPTANCE', {}).get('status') != 'complete':
            issues.append('Editorial acceptance lacks its completed evidence task')
        review = ROOT / state.get('writing_review', '')
        if review.is_file():
            marker = f"The {audit['publication']['full']['pages']:,}-page integrated-argument reader"
            if marker not in review.read_text():
                issues.append('Candidate review advertises a stale reader page count')
    except (OSError, KeyError, TypeError, ValueError) as exc:
        issues.append('Writing evidence cannot be verified: ' + str(exc))
    return issues


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['status', 'next', 'check'])
    args = parser.parse_args()
    state, ready = view()
    tasks = eligible_tasks(state)
    if args.command == 'next':
        out = {'next': tasks[0] if tasks else (ready[0] if ready and not state.get('tasks') else None),
               'independent_ready': [x['id'] for x in (tasks[1:] if state.get('tasks') else ready[1:])],
               'blocked_tasks': [{'id': x['id'], 'blockers': x.get('blockers', [])}
                                 for x in state.get('tasks', []) if x['status'] == 'blocked'],
               'continue_across_phase_boundaries': True}
    elif args.command == 'check':
        issues = []
        ids = [x['id'] for x in state['items']]
        if len(ids) != len(set(ids)):
            issues.append('Duplicate work item')
        for x in state['items']:
            for key in ['question', 'required_result', 'status']:
                if not x.get(key):
                    issues.append(x['id'] + ': missing ' + key)
            if set(x['depends_on']) - set(ids) or x['id'] in x['depends_on']:
                issues.append(x['id'] + ': invalid dependency')
            if x['status'] == 'complete' and not x.get('evidence'):
                issues.append(x['id'] + ': completion lacks evidence')
            for path in x.get('evidence', []):
                if not (ROOT / path).is_file():
                    issues.append(x['id'] + ': missing evidence ' + path)
        for x in state['deferred']:
            if not x.get('reason') or not x.get('revisit'):
                issues.append('Deferred item lacks reason or revisit condition')
        if not (ROOT / state['plan']).is_file():
            issues.append('Missing active plan')
        issues.extend(task_issues(state))
        issues.extend(writing_issues(state))
        if state.get('active_gap_plan') and not (ROOT/state['active_gap_plan']).is_file():
            issues.append('Missing active gap plan')
        out = {'status': 'fail' if issues else 'pass', 'issues': issues,
               'scope': 'Priority, chapter-coverage and current publication/preservation consistency; not scholarly or editorial acceptance',
               'proposal_complete': state['proposal_complete']}
    else:
        out = {'objective': state['completion_measure'], 'current': tasks[0]['id'] if tasks else (ready[0]['id'] if ready and not state.get('tasks') else None),
               'items': [{k: x[k] for k in ['id','title','status']} for x in state['items']],
               'tasks': [{k: x[k] for k in ['id', 'stream', 'status']} for x in state.get('tasks', [])],
               'deferred': state['deferred'], 'proposal_complete': state['proposal_complete'],
               'final_editorial_acceptance': state['final_editorial_acceptance']}
    print(json.dumps(out, indent=2))
    if args.command == 'check' and out['issues']:
        raise SystemExit(1)


if __name__ == '__main__':
    cli()
