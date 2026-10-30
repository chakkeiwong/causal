"""Single-use, preservation-ledgered fitting-contract integration."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
from release_candidate_20261029 import MATH

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/release/2026-10-29'
OUT = BASE/'source-pygformula-025'
SOURCE = BASE/'source/docs/writing-repair/2026-10-29'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def binding(p):
    return dict(path=str(p.relative_to(ROOT)), sha256=sha(p))


def main():
    ledger = json.loads((BASE/'edits.json').read_text())
    assert len(ledger) == 103, 'Single-use integration; do not rerun.'
    assert not (OUT/'source-audit.json').exists()
    changes = {}
    def edit(p, before, after, reason, destination):
        old, current = changes.get(p, (p.read_text(), p.read_text()))
        assert current.count(before) == 1, (str(p), before[:90])
        changes[p] = (old, current.replace(before, after, 1))
        ledger.append(dict(file=str(p.relative_to(ROOT)), before=before, after=after,
                           reason=reason, substantive_destination=destination))
    p = SOURCE/'src/0cdefa558bd74864.tex'
    anchor = '\\subsection{Integration choices and the remaining survey boundary}'
    addition = (OUT/'addition.tex').read_text().replace('USD100 receipt', 'USD 100 receipt')
    edit(p, anchor, addition+'\n'+anchor,
         'Develop selected fitting-population and observation-clock contracts with exact banking consequences.',
         'Two additive subsections inside the Python comparison; all inherited zEpid/pygformula derivations, uncertainty caveats and alternatives remain.')
    edit(p, 'causal assumptions, numerical diagnostics and operating acceptance remain\nseparate responsibilities.',
         'causal assumptions, numerical diagnostics and operating acceptance remain\nseparate responsibilities. The selected fitting-helper inspection resolves\nthe named population and event-conditioning questions; it also supplies a\nspecific reason to withhold the documented covariate-restriction profile\nuntil native correction and verification. This does not close the other\nhelper, dependency or statistical-qualification requirements.',
         'Reconcile conditional reuse with the developed restriction and risk-set findings.',
         'The original open-survey and native-qualification boundaries remain; selected completed inspection is distinguished from unresolved work.')
    p = SOURCE/'src/9ac4870b17074c5a.tex'
    edit(p, 'The model-fitting risk sets were not newly inspected for this comparison,\nso the simulation order alone cannot establish how every fitted probability\nis conditioned.~\\citep{v13_sw_pygformula,exec17_s5_paths}',
         'Simulation order alone cannot establish how every fitted probability\nis conditioned. The later Python comparison inspects the selected fitting\nhelpers and develops the distinction between missing outcomes, current\ncompeting-event exclusions and deterministic covariate histories. Its\nconclusions remain specific to that revision and declared input clock.\n\\citep{v13_sw_pygformula,exec17_s5_paths,rel25pygfit}',
         'Replace the now-stale uninspected-risk-set statement with the exact scope of the later comparison.',
         'The original ordered-event derivation and its warning against inferring fitting semantics from simulation survive; the completed primary inspection is linked.')
    bib = SOURCE/'references-0.bib'
    tail = bib.read_text()[-180:]
    extra = r'''
@misc{rel25pygfit,
 author={{pygformula contributors}},
 title={{pygformula}: fitting populations, deterministic histories and event clocks},
 year={2026},
 note={Version 1.2.1; commit e66f787fcef2d6a9092b88135147c6b13785795c, 22 May. Selected primary-source and input-documentation inspection; no native execution},
 url={https://github.com/CausalInference/pygformula}
}
@misc{rel25pygwitness,
 author={{Causal Banking Research Project}},
 title={Exact fitting-population and event-denominator constructions},
 year={2026},
 note={Authored likelihood, finite-population and payoff calculations, 29 October. No package execution, bank observations or causal service-effect estimate}
}
'''
    edit(bib, tail, tail+extra, 'Add primary-source and exact-project identities for the fitting comparison.',
         'All previous bibliography entries remain; two new records support the additive treatment.')
    specs = {
        'docs/source/Specifications/Input data.rst': [(37,66,'Interval k covariates, interval k+1 outcome; survival censor-row encoding has a fine-interval qualification.'),(77,83,'Explicit competing event stops the observed history and requires missing target outcome.')],
        'docs/source/Specifications/Deterministic knowledge.rst': [(14,40,'Fit the stochastic histories only, then deterministically assign known values; documented list-of-lists schema.')],
        'docs/source/Specifications/Censoring event.rst': [(6,26,'Censoring model supports observed natural-course IPW comparison.')],
        'pygformula/parametric_gformula/fit.py': [(106,139,'Post-baseline covariate fitting; whole-first-list membership mismatch and complete predictor rows.'),(315,339,'Outcome nonmissing selection; current competing-event-zero conditioning.'),(404,413,'Competing model uses nonmissing competing outcomes.'),(423,435,'Censoring fitting role.'),(474,477,'Censoring model selects its own nonmissing indicator.')],
        'pygformula/parametric_gformula/parametric_gformula.py': [(300,319,'Restriction and censoring arguments are retained directly.'),(346,354,'Censor and explicit competing-event branch selection.'),(381,393,'Input checker receives no restriction-transformation argument.'),(498,540,'Caller forwards restrictions and invokes separate outcome, competing and censoring models.')],
        'pygformula/parametric_gformula/simulate.py': [(371,386,'Simulation correctly extracts covariate names and applies deterministic restrictions.'),(405,449,'Competing draw precedes target outcome; target outcome missing on competing occurrence.'),(455,469,'Current competing-event survival multiplies the conditional default increment.')],
        'pygformula/utils/util.py': [(150,260,'Selected executable input checks; no change of restriction schema or outcome censor-row selection.')]
    }
    rows = json.loads((OUT/'authenticated-files.json').read_text())+json.loads((OUT/'authenticated-retained-files.json').read_text())
    bindings = []; anchors = []
    for row in rows:
        p = ROOT/row['local_path']; assert sha(p) == row['sha256']
        bindings.append(binding(p)); bindings.append(binding(ROOT/row['receipt']))
        lines = p.read_text().splitlines()
        for first,last,finding in specs.get(row['path'], []):
            anchors.append(dict(path=row['local_path'],sha256=sha(p),lines=[first,last],
                                text='\n'.join(lines[first-1:last]),finding=finding))
    for name in ['exec24_longpy_pygformula_tree.json','exec24_longpy_pygformula_source_0.txt']:
        bindings.append(binding(ROOT/'docs/literature/raw'/name))
    source = dict(citation_key='rel25pygfit',kind='software_primary_sources',
                  source_identity='https://github.com/CausalInference/pygformula/tree/e66f787fcef2d6a9092b88135147c6b13785795c',
                  version_date='1.2.1; e66f787fcef2d6a9092b88135147c6b13785795c; 2026-05-22T19:45:58Z; client cutoff2026-10-07; selected additional originals retrieved2026-10-29',
                  local_bindings=bindings,inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],
                  limitations=['Static source inspection, no downloaded implementation or upstream test execution.',
                               'Findings apply to the selected documented schema and paths; no all-version or all-model claim.',
                               'Additional parser/category/baseline checks are not generalized into qualified failures.',
                               'Papers named by documentation are discovery leads unless independently admitted; no new scholarly original is claimed.',
                               'Native environment, dependencies, coverage, causal identification and bank qualification remain separate.'])
    witness = OUT/'exact-witnesses.json'; generator = ROOT/'tools/release_pygformula_witnesses_20261029.py'
    derivation = dict(citation_key='rel25pygwitness',kind='project_derivation',source_identity=str(generator.relative_to(ROOT)),
                      version_date='2026-10-29 exact authored constructions',local_bindings=[binding(witness),binding(generator)],
                      inspected_anchors=['main(): full-rank binomial scores and positive information determinant; finite missing-outcome bounds; ordered-event factorization and contingent payoffs.'],
                      supported_claims=['Restricted fitted probability4/5 versus pooled2/5; half-eligible means2/5 versus1/5 and margins10 versus-10.',
                                        'Observed8/80 versus zero-encoded8/100; finite population bounds2/25 to7/25 and stipulated margins100 versus-100.',
                                        'Conditional competing-first factorization gives2/25; double multiplication gives8/125, retaining two-period86/625 versus19/100.'],
                      limitations=['Exact invented laws and analytical fitting traces, not upstream runtime or bank observations.',
                                   'No empirical coverage, causal service benefit or automatic censoring identification.'])
    ap = OUT/'source-audit.json'
    audit_text = json.dumps(dict(cutoff='2026-10-07',sources=[source,derivation],scope='Selected fitting populations and observation law; no exhaustive software census.'),indent=2)+'\n'
    rp = BASE/'mathematical-addition-reviews.json'; reviews=json.loads(rp.read_text())
    e = ledger[103]
    occurrences = lambda text: Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(text))
    assert not occurrences(e['before'])-occurrences(e['after'])
    reviews['reviews'].append(dict(scope='Additive fitting-population, missing-outcome and competing-event derivations.',
        edits=[dict(edit=104,file=e['file'],before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),after_sha256=hashlib.sha256(e['after'].encode()).hexdigest())],
        allowed_added=dict(occurrences(e['after'])-occurrences(e['before'])),allowed_removed={},status='reviewed_additions_only',
        derivation='Solve binomial scores separately in two full-rank predictor cells, standardize over eligibility and evaluate contingent receipts. Bound unknown binary outcomes by completion0/1. Factor competing-first probability into current survival and conditional default.',
        reviewed_assumptions=['Known deterministic ineligible zeros; predictor-cell overlap and a specified logistic submodel.',
                              'Half-eligible target population and fixed stipulated receipt/cost; no causal effect interpretation.',
                              'Censored outcomes unknown; observed-risk identification additionally needs censoring assumptions and support.',
                              'Within-period prepayment priority; conditional default given no current prepayment.'],
        witness=binding(witness),source_audit=dict(path=str(ap.relative_to(ROOT)),sha256=hashlib.sha256(audit_text.encode()).hexdigest()),
        fresh_visual_acceptance=False,independent_acceptance=False))
    before = OUT/'before'; before.mkdir(exist_ok=False)
    for p,(old,new) in changes.items():
        assert p.read_text() == old
        (before/p.name).write_text(old)
    for name in ['edits.json','mathematical-addition-reviews.json']:
        (before/name).write_bytes((BASE/name).read_bytes())
    ap.write_text(audit_text)
    for p,(_,new) in changes.items():p.write_text(new)
    (BASE/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    rp.write_text(json.dumps(reviews,indent=2)+'\n')
    print(json.dumps(dict(edits=len(ledger),source_audit_sha256=sha(ap),witness_sha256=sha(witness))))


if __name__ == '__main__':
    main()
