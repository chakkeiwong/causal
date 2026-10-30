"""Clarify expected volume and conditional investment without changing inputs."""
from pathlib import Path
import json
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'investment-review-083'


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 230
    patches = [
        ('src/830f6276ba2598e7.tex',
         'where each probability conditions on reaching the preceding stage.\nThis is the chain rule, not an independence assumption.',
         'where each probability conditions on reaching the preceding stage.\n'
         'The left side denotes expected usable studies for a fixed number of\n'
         'starts, not the realized integer count. Each stage probability refers\n'
         'to that same starting cohort and must be updated when its composition\n'
         'changes. Dependence between studies affects the dispersion of completed\n'
         'volume even when its expectation is correctly specified.\n'
         'This is the chain rule, not an independence assumption.',
         'Distinguish the expected planning volume from realized completed studies.'),
        ('src/830f6276ba2598e7.tex',
         'The first tranche should compare matched tasks in the intervention,\nsequential-decision and dynamic-systems workspaces.',
         'If the initial offer-study comparison supports broader investment,\n'
         'a subsequent construction tranche should compare matched tasks in the\n'
         'intervention, sequential-decision and dynamic-systems workspaces.',
         'Align the broader construction comparison with the selected narrow first investment.'),
        ('investment.tex',
         'waiting separately. This makes the eventual prototype experiment worth\n'
         'funding: it can test whether a saving survives the costs of producing an\n'
         'answer that a decision-maker can actually use.',
         'waiting separately. This defines what the eventual prototype experiment\n'
         'would test: whether a saving survives the costs of producing an answer\n'
         'that a decision-maker can actually use. Funding is warranted only when\n'
         'its expected improvement in the investment decision justifies its full\n'
         'cost.',
         'Distinguish a useful measurement question from a justified funding decision.')
    ]
    for name in sorted({x[0] for x in patches}):
        p = B / 'source/docs/writing-repair/2026-10-29' / name
        shutil.copy2(p, O / ('before-' + p.name))
    for name, before, after, reason in patches:
        p = B / 'source/docs/writing-repair/2026-10-29' / name
        text = p.read_text()
        assert text.count(before) == 1
        p.write_text(text.replace(before, after, 1))
        ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
            reason=reason, substantive_destination='All equations, stipulated inputs, alternatives, cost accounts, failed-study costs, measurement requirements and adverse findings remain in their original context. Added or replaced prose clarifies expected volume and conditional funding; no substantive scientific material is deleted.'))
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    record = dict(status='written_pending_build_review', edits=[231, 232, 233],
        new_citations=False, new_financial_inputs=False, new_draws=False,
        mathematical_change=False, new_qualification=False,
        deletion_review_required='Edit231 retains both original sentences. Edit232 replaces first-tranche timing while retaining all workspaces. Edit233 removes an unsupported automatic funding inference while retaining the proposed empirical question and full-cost account.')
    (O / 'integration.json').write_text(json.dumps(record, indent=2) + '\n')
    print('Added edits231–233: expected usable volume and conditional investment.')


if __name__ == '__main__':
    main()
