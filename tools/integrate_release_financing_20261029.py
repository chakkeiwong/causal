"""Integrate the already delivered financing study, preserving its complete text."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import shutil

from release_candidate_20261029 import MATH

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
OUT = BASE / 'source-closure-018'
PRIOR = ROOT / 'docs/twelve-hour-closure/2026-10-29'
SOURCE = BASE / 'source/docs/writing-repair/2026-10-29'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def binding(path):
    return dict(path=str(path.relative_to(ROOT)), sha256=sha(path))


def main():
    ledger = json.loads((BASE / 'edits.json').read_text())
    assert len(ledger) == 83, 'Single-use integration; do not replay.'
    assert not (OUT / 'source-audit.json').exists()
    original = PRIOR / 'formulation.tex'
    original_text = original.read_text()
    expected = json.loads((PRIOR / 'formulation-attempt-1/results.json').read_text())
    assert sha(PRIOR / 'formulation-attempt-1/results.json') == 'db789a1cafc586af9c1c64ac9497381510bdb80776f2bae3dabd7be39599aa29'

    # Independent closed-form mixture calculation, not a second execution of
    # the original state-enumeration program.
    p = F(1, 5)
    discordance = 2 * p * (1 - p)
    risks = {0: 1 - discordance, 1: discordance}
    joint = {(f, y): F(1, 2) * (risks[f] if y else 1 - risks[f])
             for f in [0, 1] for y in [0, 1]}
    assert joint == {(r['F'], r['Y']): F(r['probability']) for r in expected['observed_joint']}
    assert sum(joint.values()) == 1
    effects = {'confounded': F(0), 'causal': risks[0] - risks[1]}
    for name, effect in effects.items():
        assert effect == F(expected['interventions'][name]['relief_effect'])
    assert risks[0] == F(17, 25) and risks[1] == F(8, 25)
    witness = dict(status='pass', kind='independent_retained_law_reconstruction',
                   observed_joint=[dict(F=f, Y=y, probability=str(v)) for (f, y), v in sorted(joint.items())],
                   observational_risks={str(k): str(v) for k, v in risks.items()},
                   relief_effects={k: str(v) for k, v in effects.items()},
                   original_result=binding(PRIOR / 'formulation-attempt-1/results.json'),
                   method='Closed-form disagreement probability of two independent Bernoulli errors, symmetry and mixture factorization; no source empirical experiment or original script rerun.',
                   text_channel_argument='Any common deterministic t(F,Y) pushes equal joint measures to equal transcript laws; independent prompt randomization is a common Markov kernel and preserves equality.',
                   scope='Two compatible models establish nonidentification; neither a sharp bound nor an effect of an actual bank credit offer.')
    dump(OUT / 'exact-witnesses.json', witness)

    transformed = original_text.replace(r'\section{', r'\subsubsection{').replace(r'\chapter{', r'\subsection{')
    transformed = transformed.replace('closure30li', 'rel18li').replace('closure30mugleston', 'rel18mugleston')
    # Keep all equation, figure and label bytes. Add explicit provenance for the
    # project derivation without presenting it as a third-party result.
    anchor = 'estimate for Chinese firms or a bank portfolio.'
    assert transformed.count(anchor) == 1
    transformed = transformed.replace(anchor, anchor + r' \citep{rel18witness}', 1)
    target = SOURCE / 'src/62cabebeedc23664.tex'
    before = r'\hypertarget{evaluation-before-a-costly-bank-study}{%'
    after = transformed + '\n' + before
    assert target.read_text().count(before) == 1
    edits = [dict(file=str(target.relative_to(ROOT)), before=before, after=after,
                  reason='Integrate the completed financing-source comparison and full observational-equivalence proof before the formulation evaluation discussion.',
                  substantive_destination='Every original formulation paragraph remains. The complete delivered financing text, mathematics, figure, reported results and limits survive; only section depth and citation namespace change, with an added project-evidence citation.')]
    bib = SOURCE / 'references-0.bib'
    bib_before = bib.read_text()[-500:]
    bib_extra = r'''

@misc{rel18li,
 author={Li, Rongxue},
 title={Large Language Models for Unraveling the Causal Impact of Financing Constraints on Corporate Exports},
 year={2025},
 doi={10.31224/5380},
 note={EngrXiv preprint version 1, 15 September 2025; genuine 16-page original inspected; reported scores are not independently reproduced}
}

@article{rel18mugleston,
 author={Mugleston, Jennifer and Truong, Vuong Hung and Kuang, Cindy and Sibiya, Lungile and Myung, Jihwan},
 title={Epistemology in the Age of Large Language Models},
 journal={Knowledge},
 volume={5}, number={1}, pages={3}, year={2025},
 doi={10.3390/knowledge5010003},
 note={Published 1 February 2025; genuine 19-page publisher PDF; philosophical argument, not a banking identification result}
}

@misc{rel18witness,
 author={{Causal banking proposal project}},
 title={Exact financing-constraint observational equivalence and transcript witness},
 year={2026},
 note={29 October 2026; retained two-model construction with independent closed-form reconstruction; effects zero and 9/25 are examples, not sharp bounds or bank estimates}
}
'''
    edits.append(dict(file=str(bib.relative_to(ROOT)), before=bib_before, after=bib_before + bib_extra,
                      reason='Add the two genuine source identities and project-derivation provenance.',
                      substantive_destination='All previous bibliography entries remain; source empirical reports and project mathematical construction are distinct.'))
    support = json.loads((PRIOR / 'source-support.json').read_text())
    sources = []
    for key, newkey in [('closure30li', 'rel18li'), ('closure30mugleston', 'rel18mugleston')]:
        row = next(x for x in support['sources'] if x['citation_key'] == key)
        pdf = ROOT / row['local_copy']
        assert sha(pdf) == row['sha256'] and pdf.read_bytes().startswith(b'%PDF-')
        local = [binding(pdf)] + row['identity_evidence']
        for x in local:
            assert sha(ROOT / x['path']) == x['sha256']
        local.append(binding(OUT / (key + '.txt')))
        sources.append(dict(citation_key=newkey, kind='paper', source_identity=row['source_identity'],
                            version_date=row['version_date'], local_bindings=local,
                            inspected_anchors=row['inspected_anchors'], supported_claims=row['supported_claims'],
                            limitations=row['forbidden_claims'] + [
                                'Li: all16 pages read as extracted text. Mugleston: title page and claim-bearing sections3.1-9 on pp6-17 read; no complete foundational-history or reference-list reading claimed.',
                                'No secondary empirical scores or current product/policy assertions imported. No visual acceptance transferred from the other publication.']))
    sources.append(dict(citation_key='rel18witness', kind='project_derivation',
                        source_identity='Project-authored financing construction, retained from the separate closure campaign and reconstructed algebraically for this candidate.',
                        version_date='2026-10-29 UTC; separate study labeled2026-10-30 Asia/Shanghai',
                        local_bindings=[binding(PRIOR / 'formulation-attempt-1/results.json'), binding(ROOT / 'tools/run_formulation_study_20261030.py'), binding(OUT / 'exact-witnesses.json'), binding(Path(__file__))],
                        inspected_anchors=['Complete formulation.tex and original enumerator read; retained joint table and both intervention distributions checked by independent closed-form mixture algebra.'],
                        supported_claims=['Observed joint cells4/25,17/50,17/50,4/25 match in two models; intervention relief effects0 and9/25 differ.', 'A common deterministic transcript or independent randomized text channel preserves observational equivalence.', 'Abstract constraint relief differs from a specified offer or facility draw; the two models are not sharp bounds.'],
                        limitations=['No rerun of the source empirical study, live model, vendor code or bank trial.']))
    audit = dict(cutoff='2026-10-07', sources=sources,
                 scope='Primary text read and exact authored law checked; narrative integration retains the complete existing study with separate scientific roles.')
    audit_path = OUT / 'source-audit.json'
    dump(audit_path, audit)
    math_path = BASE / 'mathematical-addition-reviews.json'
    math = json.loads(math_path.read_text())
    count = lambda s: Counter(re.sub(r'\s+', ' ', m[0]) for m in MATH.finditer(s))
    assert not count(before) - count(after)
    math['reviews'].append(dict(scope='Complete additive financing proof; no inherited mathematical removal.',
        edits=[dict(edit=84, file=edits[0]['file'], before_sha256=hashlib.sha256(before.encode()).hexdigest(), after_sha256=hashlib.sha256(after.encode()).hexdigest())],
        allowed_added=dict(count(after) - count(before)), allowed_removed={}, status='reviewed_additions_only',
        derivation='Independent binary-error mixture yields conditional risks17/25 and8/25. Intervention on F leaves Y unchanged in the common-cause model but changes its Bernoulli probability in the direct model. Equal joint measures remain equal after a common transcript map or independent stochastic kernel.',
        reviewed_assumptions=['Mutually independent stipulated exogenous variables and exact binary equations.', 'The transcript supplies no additional information beyond the declared F,Y; no claim about all real reports.', 'Two models demonstrate nonidentification, not sharp bounds or an identified actual facility effect.'],
        witness=binding(OUT / 'exact-witnesses.json'), source_audit=binding(audit_path), fresh_visual_acceptance=False, independent_acceptance=False))
    backup = OUT / 'before'
    backup.mkdir(exist_ok=False)
    for p in [target, bib, BASE / 'edits.json', math_path]:
        shutil.copy2(p, backup / p.name)
    shutil.copy2(original, OUT / 'formulation-original.tex')
    shutil.copy2(PRIOR / 'source-support.json', OUT / 'inherited-source-support.json')
    shutil.copy2(PRIOR / 'formulation-author-review.json', OUT / 'inherited-author-review.json')
    dump(OUT / 'integration-map.json', dict(original=binding(original), preserved_original=binding(OUT / 'formulation-original.tex'),
        target=str(target.relative_to(ROOT)), transformation=['chapter to subsection; section to subsubsection', 'closure30 citation keys to rel18 keys', 'one explicit project witness citation'],
        complete_text_retained=True, independent_visual_acceptance=False, attribution='Prior campaign author/visual receipts are retained as attribution only, not acceptance of this successor.'))
    for edit in edits:
        p = ROOT / edit['file']
        assert p.read_text().count(edit['before']) == 1
        p.write_text(p.read_text().replace(edit['before'], edit['after'], 1))
    dump(BASE / 'edits.json', ledger + edits)
    dump(math_path, math)
    print(json.dumps(dict(edits=len(ledger + edits), source_audit_sha256=sha(audit_path), witness_sha256=sha(OUT / 'exact-witnesses.json'))))


if __name__ == '__main__':
    main()
