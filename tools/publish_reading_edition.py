"""Update mutable reading pointers after the focused editorial checks pass."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
review=json.loads((ROOT/'docs/reading-edition/review.json').read_text())
assert review['status']=='pass'
p=ROOT/'docs/program/scientific-priorities.json'
state=json.loads(p.read_text())
item=state['items'][0]
item.update(title='Deliver the structural and contextual editorial repair',status='complete',
            conclusion='Nine-part integrated reading edition delivered; banking narrative, contextual prose repairs, six figures and comparative conclusions; preservation and layout checks pass.',
            evidence=['docs/reading-edition/review.json','docs/reading-edition/content-comparison.json',
                      'docs/reading-edition/editorial-review.md','docs/causal_banking_reading_edition_2026-10-29.pdf'])
state['reader']={k:review[k] for k in ['pdf','sha256','pages']}
state['editorial_followup']=dict(status='pending_visual_and_human_review',
    reason='The inherited session image allowance is exhausted; human reading is required to judge naturalness across the manuscript.',
    does_not_block_scientific_streams=True,
    continuation='Inspect prepared previews in a fresh session; continue contextual editing against concrete reading difficulties.')
state['items'][1].update(evidence=['docs/reading-edition/software-conclusions.tex'],
    progress='Comparative conclusion added; full domain synthesis remains open.')
state['items'][2].update(evidence=['docs/reading-edition/assistance-conclusions.tex'],
    progress='Task-based economic synthesis added; frontier coverage remains open.')
p.write_text(json.dumps(state,indent=2)+'\n')
p=ROOT/'docs/program/master-live.md';s=p.read_text()
s=s.replace('## Active priorities','''## Current reading edition

[Read the integrated banking edition](../causal_banking_reading_edition_2026-10-29.pdf). Nine thematic parts connect banking decisions, methods, evidence and investment. The edition adds six explanatory figures and comparative conclusions. [Editorial review](../reading-edition/editorial-review.md) records preservation checks and pending visual/human review. Historical evidence and outcomes are unchanged. The prior sponsor is not represented as a newly paired edition.

## Active priorities''')
s=s.replace('1. Reorganize and edit the integrated monograph into a linear economics and finance narrative, arranged in parts. Explain the mathematics, preserve evidence and qualifications, and add diagrams. Remove internal administration and authoring history from reader prose.',
            '1. The structural and contextual reading-edition repair is delivered. Continue contextual editing where reading identifies a specific difficulty. Visual and human review remain pending and do not block scientific work.')
p.write_text(s)
p=ROOT/'docs/program/execution/current-program.md';s=p.read_text()
s=s.replace('Immediate work: the integrated reading edition, with logical parts, thematic placement of accumulated additions, economics and finance language, preserved mathematics, explanatory graphics and an honest editorial review.',
            'The [integrated reading edition](../../causal_banking_reading_edition_2026-10-29.pdf) is delivered with thematic parts, contextual economics-language repairs, preserved mathematics and six figures. Visual and human review remain pending.')
p.write_text(s)
(ROOT/'docs/mission-control.md').write_text('''# Causal banking research and proposal

[Current integrated reading edition](causal_banking_reading_edition_2026-10-29.pdf) · [Editorial review](reading-edition/editorial-review.md).

[Active master](program/master-live.md) · [Scientific repair plan](program/scientific-editorial-repair.md) · [Priority state](program/scientific-priorities.json).

The edition has nine parts, an economic narrative, six new explanatory figures and comparative conclusions. Source, reference and page-bound checks pass. Visual and human editorial review remain pending; this is not whole-proposal acceptance.

Continue with python3 tools/scientific_program.py next. Software synthesis, language models and causal reasoning, public-data evidence, practical integration and the investment case remain independently eligible.

The [protected monograph](causal_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf), [prior sponsor](sponsor_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf) and [historical state](program/state.json) retain their identities. The prior sponsor has not been rewritten or paired with this edition.

Continue across phase boundaries. Keep commands and output bounded. No unattended worker is running.
''')
(ROOT/'docs/mission-control.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><title>Causal banking research</title><body>
<h1>Causal banking research and proposal</h1>
<p><a href="causal_banking_reading_edition_2026-10-29.pdf">Current integrated reading edition</a> · <a href="reading-edition/editorial-review.md">Editorial review</a></p>
<p><a href="program/master-live.md">Active master</a> · <a href="program/scientific-editorial-repair.md">Scientific repair plan</a> · <a href="program/scientific-priorities.json">Priority state</a></p>
<p>The nine-part edition has an economic narrative, six explanatory figures and comparative conclusions. Source, reference and page-bound checks pass. Visual and human review remain pending.</p>
<p>Continue independent scientific streams with <code>python3 tools/scientific_program.py next</code>. Administrative activity does not establish scientific completion.</p>
<p><a href="causal_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf">Protected predecessor</a> · <a href="sponsor_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf">Prior sponsor, not newly paired</a> · <a href="program/state.json">Historical state</a></p>
</body></html>
''')
(ROOT/'docs/README.md').write_text('''# Causal inference for banking

[Read the current integrated edition](causal_banking_reading_edition_2026-10-29.pdf).

The book follows banking decisions through identification, estimation, repeated decisions, software comparisons, language assistance, practical use, public evidence and investment. It retains the existing mathematics and citations and adds six explanatory figures.

[Active master](program/master-live.md) · [Scientific priorities](program/scientific-priorities.json) · [Editorial review and limits](reading-edition/editorial-review.md).

Run python3 tools/scientific_program.py status, next or check. Historical control and source evidence remain preserved; they do not select the new priorities.

Visual and human editorial review and full scientific survey completion remain open. The [prior sponsor](sponsor_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf) has not been paired with the new reading edition.
''')
(ROOT/'docs/reading-edition/current-document.json').write_text(json.dumps(dict(reader=state['reader'],
    source='docs/causal_banking_reading_edition_2026-10-29.tex',active_program='docs/program/scientific-priorities.json',
    review='docs/reading-edition/editorial-review.md',prior_sponsor_unmodified='docs/sponsor_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf',
    final_acceptance=False),indent=2)+'\n')
print('Published current reading pointers and scientific continuation; final acceptance remains open.')
