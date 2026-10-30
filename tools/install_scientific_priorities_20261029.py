"""Install the requested priority change without rewriting historical evidence."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
items = [
 ('E01',0,'Restructure and edit the integrated banking monograph',
  'Can an economist follow the argument from a banking choice to an investment decision?',
  'A parts-based edition, banking-language openings and transitions, contextual prose repairs, explanatory figures and preserved science.', 'in_progress'),
 ('S01',1,'Complete comparative software recommendations',
  'Which capabilities should we adopt, integrate, port or reject?',
  'Developed conclusions across 17 areas and all required language/commercial dimensions, with evidence and consequential unknowns.', 'ready'),
 ('S02',1,'Synthesize language models and causal reasoning',
  'Where does assistance improve formulation, diagrams, discovery, identification and interpretation?',
  'Primary-source synthesis, meaningful baselines, failures and remedies, and discriminating experiments.', 'ready'),
 ('S03',1,'Synthesize and extend public-data evidence',
  'Which available demonstrations justify spending on a prototype?',
  'Comparable estimands and practitioner baselines, uncertainty and negative results, implications for the design.', 'ready'),
 ('S04',1,'Explain practical library, CLI and MCP use',
  'How would a bank economist conduct a defensible study using these tools?',
  'Worked studies from data and assumptions to interpretation; reuse decisions; proposed and executed behavior distinguished.', 'ready'),
 ('S05',2,'Form the conditional investment recommendation',
  'What should be built or reused, and what evidence would reverse the choice?',
  'Alternatives, conditional costs and benefits, information value and a justified next experiment.', 'ready')]
state = dict(updated='2026-10-29', authority='User scientific and editorial repair',
 plan='docs/program/scientific-editorial-repair.md',
 completion_measure='Answered scientific questions and justified proposal decisions, not administrative activity',
 legacy_state='docs/program/state.json',
 items=[dict(id=i,priority=p,title=t,question=q,required_result=r,status=s,depends_on=[],evidence=[]) for i,p,t,q,r,s in items],
 deferred=[dict(topic='Packed-bit RNG and complete header chain',reason='Material effect on the recommendation is not established',revisit='Evidence of changed inferential validity or adoption choice'),
 dict(topic='Default LINPACK pivot reachability and transitive runtime qualification',reason='The conditional example supports alignment; full product qualification is later',revisit='A claim about a default-package defect or a specific native deployment')],
 proposal_complete=False, final_editorial_acceptance=False)
(ROOT/'docs/program/scientific-priorities.json').write_text(json.dumps(state,indent=2)+'\n')
(ROOT/'docs/program/master-live.md').write_text('''# Current master: scientific progress and a readable banking proposal

Updated 29 October 2026. [Active repair plan](scientific-editorial-repair.md) · [Scientific priorities](scientific-priorities.json).

## Objective

Explain which banking decisions causal analysis can improve, under which assumptions, using which tools, and at what expected cost. Progress means an answered scientific question, a completed comparative argument, a justified choice, or a useful negative conclusion. Pages, receipts and publication checks do not establish progress.

## Active priorities

1. Reorganize and edit the integrated monograph into a linear economics and finance narrative, arranged in parts. Explain the mathematics, preserve evidence and qualifications, and add diagrams. Remove internal administration and authoring history from reader prose.
2. Complete software recommendations across all required causal areas, languages and commercial alternatives.
3. Complete the language-model synthesis, especially formulation, diagrams and discovery, with credible baselines, failures and remedies.
4. Synthesize and extend public/generated evidence when it can change a proposal decision.
5. Develop worked library, CLI and MCP banking examples and a conditional investment recommendation.

These streams are independently eligible. An unavailable source blocks its claim, not another ready stream. Phase boundaries do not stop execution. Report changed conclusions, evidence, decision consequences and remaining uncertainty.

## Required standard

Follow all three policies in ~/workspace/claudecodex/policies: scientific validity and proportionality, scholarly source audit, and natural prose. Write in economics, finance and statistics language. The Economist is a reference for clarity; FinMarketing remains the standard for developed argument and derivation.

Explain interventions, populations, information dates, identification, estimation, uncertainty and monetary consequences. Engineering terms belong in actual implementation discussions. Retain assumptions and negative findings. AI remains a research subject; chatbot phrasing and internal authoring machinery stay outside reader prose.

## Deferred and later work

Full RNG/header qualification and default-LINPACK reachability are deferred unless they change a specific scientific claim or adoption recommendation. Existing conditional examples and limitations remain. Bank validation, independent acceptance and production qualification are later decisions, not prerequisites for proposal scholarship.

## Baseline and continuation

The protected predecessor is [the integrated monograph](../causal_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf), with its [sponsor version](../sponsor_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf). Historical evidence and nonpassing outcomes remain in [state.json](state.json). This reprioritization awards no scientific or final acceptance.

Use python3 tools/scientific_program.py status, next and check. Historical controls remain available through python3 tools/causal_program.py status and check. The old followup packet no longer selects priorities. Batch publication checks after meaningful content changes; do not regenerate the archive for a prose change.
''')
(ROOT/'docs/program/execution/current-program.md').write_text('''# Current executable proposal programme

Updated 29 October 2026. [Active master](../master-live.md) · [Reviewed plan](../scientific-editorial-repair.md) · [Priorities](../scientific-priorities.json).

Run python3 tools/scientific_program.py next. Complete a scientific or editorial deliverable, record the conclusion and evidence, and continue another ready item. Streams do not depend on blanket completion of another survey or later bank acceptance.

Immediate work: the integrated reading edition, with logical parts, thematic placement of accumulated additions, economics and finance language, preserved mathematics, explanatory graphics and an honest editorial review. Continue the software, language-model, public-evidence and integration syntheses independently. Builds and record counts do not close those obligations.

Old dependency queues remain historical evidence and no longer determine priority. Native qualification proceeds when material to a specific proposal claim. Preserve previous failures and results without recursive review packets.
''')
(ROOT/'docs/mission-control.md').write_text('''# Causal banking research and proposal

[Active master](program/master-live.md) · [Scientific and editorial repair](program/scientific-editorial-repair.md).

Current priority: turn the accumulated research into a readable economic argument and complete scientific comparisons that change the proposal. Run python3 tools/scientific_program.py next.

Independent streams: software synthesis, language models and causal reasoning, public-data evidence, practical integration and the investment recommendation. Administrative counts are not scientific completion measures.

[Protected monograph](causal_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf) · [Protected sponsor version](sponsor_proposal_panel_runtime_reviewed_v2_2026-10-29.pdf). A new reading edition is in preparation; final editorial and scientific acceptance remain open.

Continue ready work across phase boundaries. Keep calls short and output bounded. Preserve evidence without regenerating superseded governance. No unattended worker is running.
''')
print('Installed active priorities and master, execution and mission-control instructions.')
