#!/usr/bin/env python3
"""Build a preserving S9 successor with an exact joint-law extension."""
import argparse
import json
import re
from pathlib import Path

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import s9_law_results_20261017 as laws
from build_integrated_monograph_v12 import ref, verify_refs
from publish_latent_r_review_v2_20261013 import verify_bindings, write

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-17/s9'
V1=BASE/'publication-v1';PUB=BASE/'publication-v2';OUT=PUB/'reader'
OLD=DOCS/'causal_proposal_language_reuse_reviewed_2026-10-17.tex'
NAME='causal_proposal_language_reuse_reviewed_v2_2026-10-17'
DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf')
CHAPTER=PUB/'chapter.tex';LAW=PUB/'law-results.json'
SOURCE_AUDIT=PUB/'source-audit.json';PRIOR=V1/'reader/source-audit.json'
INSERT=r'\input{program/execution/2026-10-17/s9/publication-v2/chapter.tex}'

EXTENSION=r'''
\section{A joint-law boundary for port decisions}
\label{exec17:s9-law-boundary}

The shared-control example gives a decision-relevant reason to retain joint
randomness. Let $Z_A$ and $Z_B$ denote the two offer scores after subtracting
the same control score, and compare a bridge that independently redraws its
control for each offer. Under the finite Rademacher construction, exhaustive
enumeration gives
\begin{equation}
 \Pr(Z_A-Z_B=d)=
 \begin{cases}1/4&d=-2,\\1/2&d=0,\\1/4&d=2,
 \end{cases}\qquad\text{(shared control)},
 \label{exec17:s9-law-shared}
\end{equation}
and
\begin{equation}
 \Pr(\widetilde Z_A-\widetilde Z_B=d)=
 \begin{cases}1/16&d\in\{-4,4\},\\1/4&d\in\{-2,2\},\\3/8&d=0,
 \end{cases}\qquad\text{(split controls)}.
 \label{exec17:s9-law-split}
\end{equation}
The total variation distance of these two laws is $1/8$, and the probabilities
of a strictly positive difference are $1/4$ and $5/16$. A bridge can therefore
change the probability of selecting A even though both individual offer
contrasts have the same marginal variance. These are exact authored laws,
not a variance estimate or an execution of CausalML~\citep{exec17_s9_law}.

The corresponding numerical rule is also local to a declared decision. If a
source score $s$ and replacement score $\widetilde s$ satisfy
$|\widetilde s-s|\leq\epsilon$, then a threshold decision agrees whenever
$|s-c|>\epsilon$. At equality the bound cannot certify the branch. For a
finite action set with source values $v_a$, replacement errors bounded by
$\epsilon_a$, the source maximizer $a^*$ remains selected when
\begin{equation}
 v_{a^*}-\max_{a\ne a^*}v_a
   >\epsilon_{a^*}+\max_{a\ne a^*}\epsilon_a.
 \label{exec17:s9-action-gap}
\end{equation}
Without that gap, the replacement may choose a different action; its regret
is nevertheless bounded by $2\epsilon_{\max}$ under a uniform error bound.
This makes a porting claim testable at the level of the bank decision rather
than at an arbitrary number of decimal places. A result close to the boundary
must carry the interval or return an indeterminate-selection status.

For a language bridge, the finite law and the deterministic gap rule form two
different admission tests. The first asks whether shared inputs, fit objects
and resampling units preserve a joint output law. The second asks whether a
known numerical discrepancy can alter a selected action. Passing one does not
repair the other. The protocol should report both, together with the source
population, output status and refusal boundary. A bridge that cannot expose
shared-fit identity can still return marginal estimates, but it cannot claim
the paired offer decision is equivalent. Likewise, a graph endpoint map that
rounds a near-threshold p-value cannot call an adaptive search path identical
without the trace and margin evidence above.

The extension narrows the proposed integration decision. Native workers remain
the default when they satisfy the declared profile. A port earns a trial only
when its operational constraint is demonstrated, its admitted domain is
bounded, its exact and joint-law fixtures pass, and its decision-boundary
errors are disclosed. Otherwise the scientifically correct output is a
refusal or a native-worker recommendation. No software count or common API
can replace this evidence~\citep{exec17_s9_admission,exec17_s9_route_decisions}.
'''


def read(p): return json.loads(Path(p).read_text())


def prepare():
    assert not PUB.exists() and not DRIVER.exists() and not PDF.exists()
    PUB.mkdir(parents=True)
    val=laws.calculate(); assert laws.check(val)['status']=='pass'; write(LAW,val)
    CHAPTER.write_text((BASE/'development.tex').read_text()+EXTENSION)
    previous=read(V1/'reader/source-audit.json')
    prior_sources={s['integrated_citation_key'] for s in previous['sources']}
    source=dict(integrated_citation_key='exec17_s9_law',title='Exact joint-law and decision-boundary references for software ports',
        author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Authored finite shared/split-control laws and deterministic action-stability inequalities',
        version_date='2026-10-17',local_copy=ref(LAW,'Exact eight- and sixteen-path enumeration plus decision bounds'),
        inspected_anchors=['shared_difference_law','split_difference_law','total_variation','decision_stability'],
        supported_claims=['Shared and split finite laws differ in total variation by1/8 and positive-choice probability by1/16.',
                          'A scalar threshold is stable away from its boundary by more than the error bound.',
                          'An action gap larger than the two relevant score-error bounds preserves the source maximizer; uniform regret is at most2 epsilon.'],
        records=[ref(ROOT/'tools/s9_law_results_20261017.py','Exact Fraction law and inequality checks'),ref(BASE/'admission-protocol.json','Prospective admission levels')],
        limitations=['Authored finite laws, not upstream execution, calibration or bank measurement.',
                     'Decision bounds are deterministic sufficient conditions, not necessary conditions for every algorithm.'])
    write(SOURCE_AUDIT,dict(sources=[source],cutoff='2026-10-07',prior=ref(PRIOR,'729-record S9 v1 audit')))
    (PUB/'refs.bib').write_text('@misc{exec17_s9_law,\n author={{Causal banking proposal}},\n title={Exact joint-law and decision-boundary references for software ports},\n year={2026},\n note={Authored finite references; no upstream execution}\n}\n')
    old=OLD.read_text();marker=r'\input{program/execution/2026-10-17/s9/development.tex}'
    assert old.count(marker)==1
    driver=old.replace(marker,INSERT)
    driver=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s9/publication-v2/refs}',driver)
    DRIVER.write_text(driver)
    write(PUB/'prepared-inputs.json',dict(inputs=[ref(OLD,'S9 v1 driver'),ref(PRIOR,'729-record S9 v1 reader audit'),
        ref(BASE/'development.tex','S9 v1 chapter'),ref(CHAPTER,'S9 v2 chapter with joint-law extension'),ref(LAW,'Exact law'),
        ref(SOURCE_AUDIT,'One new source record'),ref(BASE/'admission-protocol.json','Admission protocol'),ref(Path(__file__),'Successor builder')],
        generated=[ref(DRIVER,'S9 v2 driver'),ref(PUB/'refs.bib','S9 v2 bibliography')],
        transform='Replace the S9 v1 chapter input with a preserving v2 chapter and append one project bibliography record.',
        prior_records=729,added_records=1,visual_acceptance=False))
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'prior_records':729,'added_records':1}))


def build():
    assert PUB.exists() and not OUT.exists() and not PDF.exists()
    verify_bindings(read(PUB/'prepared-inputs.json'))
    engine.BASE=PUB;engine.OUT=OUT;engine.OLD=OLD;engine.NAME=NAME;engine.DRIVER=DRIVER;engine.PDF=PDF;engine.PRIOR_AUDIT=PRIOR
    engine.build()
    report=read(OUT/'build-report.json'); assert report['cited_records']==730 and report['pages']>1007
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    idx=trace.audit(DRIVER,OUT/'source-audit.json');write(PUB/'traceability-review.json',idx)
    assert idx['status']=='pass' and not idx['issues'] and idx['scholarly_pdfs']==188
    text=(OUT/'reader.txt').read_text();
    for phrase in ['A joint-law boundary for port decisions','total variation distance','decision-boundary errors']:
        assert phrase in text,phrase
    write(PUB/'build-review.json',dict(status='pass',reviewer={'name':'Codex author/coordinator','kind':'author'},
        reader=report['pdf'],pages=report['pages'],cited_records=730,prior_records_preserved=729,new_records=1,
        scholarly_pdfs=188,material_warnings=[],visual_acceptance=False,
        limitations=read(SOURCE_AUDIT)['sources'][0]['limitations']))
    print(json.dumps({'pages':report['pages'],'cited_records':730,'traceability':'pass','scholarly_pdfs':188}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args();{'prepare':prepare,'build':build}[a.command]()
