"""Reconcile all obligations while preserving hash-bound historical dashboards."""
import copy
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import load, view
from run_followup_program_v2_20261028 import selected

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'program-refresh-fixture-java-v1'
PRIOR = DAY / 'program-refresh-attention-protocol-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    run = controller.base
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    results = merged['execution_program']['results']
    rb, sb = DAY / 'fixture-java-reader-v1', DAY / 'sponsor-fixture-java-v1'
    reader, sponsor = read(rb / 'working-release.json'), read(sb / 'working-release.json')
    for release in (reader, sponsor):
        verify_bindings(release)
    assert run.same_reader(state['reader'], reader['pdf'])
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    nodes = [n for n in graph['nodes'] if stages[n['id']] == 'proposal_now']
    remaining = copy.deepcopy(read(PRIOR / 'remaining-operations.json'))
    ids = {n['id'] for n in nodes if results.get(n['id'], {}).get('outcome') != 'pass'}
    assert len(nodes) == 376 and len(ids) == 150
    assert ids == {r['id'] for r in remaining['operations']}
    for row in remaining['operations']:
        if row['id'] in ('TEXT.REVIEW.L1', 'TEXT.REVIEW.L6'):
            binding = results[row['id']]
            row.update(action=read(ROOT / binding['path'])['revisit_trigger'], evidence=binding, action_basis=binding)
    counts = Counter(results.get(n['id'], {}).get('outcome', 'open') for n in nodes)
    recorded = sum(n['id'] in results for n in nodes)
    assert recorded == 351
    assert Counter(results.get(k, {}).get('outcome', 'open') for k in ids) == dict(inconclusive=121, open=25, negative=4)
    protected = [ROOT / 'docs/program/master-program.md', ROOT / 'docs/program/master-current.md']
    protected_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    BASE.mkdir()
    remaining.update(reader=state['reader'], ready=len(ready), predecessor=ref(PRIOR / 'remaining-operations.json', 'All unresolved IDs retained'))
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'remaining-operations.json', remaining)
    queue = view(load(ROOT, selected()))
    write(BASE / 'followup-snapshot.json', queue)
    evidence = [ref(BASE / 'remaining-operations.json', 'Complete nonpassing register'),
                ref(selected() / 'contracts.json', 'Independent packet contracts'),
                ref(rb / 'working-release.json', 'Exact integrated reader'),
                ref(sb / 'working-release.json', 'Exact paired sponsor'),
                ref(DAY / 'followup-runtime-v6/publication-receipt.json', 'Recovered prior publication'),
                ref(DAY / 'public-attention-contract-v2/author-review.json', '48 actual passed cases'),
                ref(DAY / 'aitiotita-delegates-v1/author-review.json', 'Seven pinned Java originals'),
                ref(Path(__file__), 'Reconciliation implementation')]
    write(BASE / 'program-review.json', dict(status='pass_for_consistency_not_completion',
          recorded=recorded, proposal_operations=376, nonpassing=150, ready=len(ready), outcome_counts=dict(counts),
          evidence=evidence, followup=queue, protected_historical_hashes=protected_hashes,
          mutable_dashboard_policy='Bind preserved snapshots; live dashboards are not acceptance evidence.',
          visual_acceptance=False, final_acceptance=False))
    current = ROOT / 'docs/program/execution/current-program.md'
    old = current.read_text()
    (BASE / 'prior-current-program.md').write_bytes(current.read_bytes())
    gaps = old[old.index('## Remaining gaps and routes'):old.index('## Execution repair')]
    continuation = '''Continue scoped commit/push with transitive evidence custody, then independent
software/source successors against the complete 150-item register. Do not repeat
the completed 48-case test run, seven Java acquisitions, prior TCDF/TACD acquisition
or unchanged blocked identity requests. Original-access limits remain local to
their candidates. A fresh visual session is needed for rendered acceptance;
source and proposal work remain eligible. No background research worker is running.'''
    header = f'''# Current executable proposal program

Updated 28 October 2026. The [program review](2026-10-28/{BASE.name}/program-review.json)
and [complete remaining register](2026-10-28/{BASE.name}/remaining-operations.json)
reconcile all 376 original obligations. The [live master](../master-live.md) governs
continuation; historical masters and dated snapshots retain their exact bytes.

The program develops a research and product proposal for four banking journeys,
including software/reuse, LLM and agents, CLI/MCP integration, public-data
prototype design, scholarly exposition and the investment case. Public and
synthetic evidence justify later expensive bank experiments. Proposal acceptance,
native implementation, independent review, bank validation and adoption are distinct.

Use `python3 tools/run_followup_program_v2_20261028.py status`, `next`, `check` for
active work. Original controllers retain integrity and acceptance. Independent
eligible work continues across phases; checkpoints are recovery records.

## Current integrated documents

The [monograph](../../{Path(reader['pdf']['path']).name}) has {reader['pages']:,} pages,
1,436 audited citation records and 274 genuine scholarly PDFs. Its exact paired
[sponsor](../../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and
1,099 records. All 1,433 reader and 1,094 sponsor predecessor records survive.
Reader contexts and compiled content inputs are preserved. Q2-Q4 exact-byte
author reviews pass; Q1/Q5, required coverage/depth, fresh visual review and final
acceptance remain open.

**351 of 376 original operations recorded; {len(ready)} original operations ready;
150 nonpassing: 121 inconclusive, 25 open and four negative.** Software remains
three passing, 98 inconclusive and one open cell. Reuse remains 109 passing,
four inconclusive and two open decisions. The frontier census remains 82 inspected
and 31 unread inherited originals. Later metadata/acquisition denominators remain
separate. Zero original ready operations is not completion; reviewed successors
are needed to advance unresolved evidence.

## Recovered and integrated work

Both saved unchanged-controller checks passed after frozen-master restoration.
The prior protocol publication is durably recorded. The stronger local contract
and seven Java delegates were recovered without repeating tests or acquisition,
and integrated into both documents. All 48 performed adversarial cases passed.
The exact example retains one unavailable graph among two requests: conditional
F1 is one, availability one half, and the full-request mean has accounting bound
[1/2,1]. This is not confidence coverage, process isolation or authentic-label proof.

The Java review distinguishes the generic Gaussian shortcut counterexample from
the bundled linguistic oracle. It gives half-vote, contradictory rule-3 endpoint,
optional literal-p-value and preset-mutation findings with conditional port routes.
No Java or external discovery code was run; broad software and bank qualification
remain open. A source-access omission is narrower than these larger obligations.

'''
    current.write_text(header + gaps + '''## Execution and recovery

Prior failures and repairs are preserved. Both historical masters retain exact
bytes. The new live master and this execution page are mutable dashboards;
future evidence binds their saved snapshots. Local blockers affect their own
tasks; checkpoints and phase boundaries do not stop independent eligible work.

## Exact continuation

''' + continuation + '\n')
    live = ROOT / 'docs/program/master-live.md'
    assert not live.exists()
    live.write_text(f'''# Current master program: causal banking proposal

Updated 28 October 2026. [Current executable program](execution/current-program.md)
and [all 150 unresolved obligations](execution/2026-10-28/{BASE.name}/remaining-operations.json)
govern continuation. The [V11 master](master-program.md) and
[earlier recovery pointer](master-current.md) are hash-bound historical records.
This live dashboard is updated without changing those sources.

The standard is a connected scholarly proposal linking each banking question
through causal assumptions, identification, estimation, uncertainty, diagnostics,
alternatives and monetary consequences. Genuine local scholarly PDFs, exact
official software identities, reproducible examples and inspected rendered
documents are required. FinMarketing is an exposition standard, not a page target.
Software coverage, the LLM/agent frontier and CLI/MCP integration remain mandatory.

The current [monograph](../{Path(reader['pdf']['path']).name}) has {reader['pages']:,} pages,
1,436 records and 274 scholarly PDFs; the paired
[sponsor](../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and 1,099 records.
There are 351 recorded original operations of 376, with 150 nonpassing.
The 48-case local fixture and seven Java delegates are integrated. Q2-Q4 author
checks pass; Q1/Q5 and visual/final acceptance remain open. This working proposal
does not establish a bank-qualified product.

Known routes are bounded primary-source review, explicit vendor/reuse comparisons,
public fixtures and manuscript development. Unrestricted latent-state identification,
arbitrary persistence, authentic truth and universal uncertainty have no promised
general repair. External acceptance, bank validation and real costs belong to
later conditional gates and do not globally block this proposal.

{continuation}
''')
    controller.render(ROOT, state)
    mission = ROOT / 'docs/mission-control.md'
    text = mission.read_text().replace('# Mission control: causal banking proposal\n',
        '# Mission control: causal banking proposal\n\n[Current master program](program/master-live.md).\n', 1)
    start, end = text.index('Current entrypoint:'), text.index('Public design outcomes:')
    text = text[:start] + '''Current work entrypoint: `python3 tools/run_followup_program_v2_20261028.py status`, `next`, `check`.
Original controllers retain proposal integrity and acceptance.

**351 / 376 original operations recorded; 150 nonpassing.** The original zero-ready
scheduler is not completion. Independent successor work continues across phases.

''' + text[end:]
    text += f'\n[Current paired sponsor]({Path(sponsor["pdf"]["path"]).name}) — {sponsor["pages"]} pages.\n'
    mission.write_text(text)
    html = subprocess.run(['pandoc', '--from=gfm', '--to=html'], input=text, text=True,
                          capture_output=True, check=True, timeout=20).stdout
    (ROOT / 'docs/mission-control.html').write_text("<!doctype html><meta charset='utf-8'><title>Causal proposal execution</title>" + html)
    assert protected_hashes == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    write(BASE / 'continuation-checkpoint.json', dict(reader=state['reader'], sponsor=sponsor['pdf'], evidence=evidence,
          next_action='Consume full-check exits, record publication, scoped commit/push, continue independent unresolved work.',
          live_entrypoint='docs/program/master-live.md', visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(recorded=351, nonpassing=150, reader_pages=reader['pages'],
                          sponsor_pages=sponsor['pages'], protected_master_bytes_unchanged=True)))


if __name__ == '__main__':
    main()
