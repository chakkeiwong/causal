#!/usr/bin/env python3
"""Review and integrate the scoped mathematical argument as project evidence."""
import json
from pathlib import Path
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/temporal-graphs'
ARG=ROOT/'docs/program/comprehensive-v14/work/SCI.ARGUMENT.R04S/argument-and-counterexamples.md'
ref=shared.ref


def main():
    reproduction=json.loads((BASE/'reproduction-review.json').read_text())
    shared.verify_refs(reproduction);assert reproduction['status']=='pass'
    findings=[
        ('law_target','Continuous unknown scalar lag, invariant initialization, independent Gaussian innovations and contemporaneous effect are explicit; rho(I-B) structural lag retained. General VAR/latent-history/selection laws excluded.'),
        ('finite_region','Orthogonal normal projection proves sample-variance moments; Chebyshev/union bound covers nine directions at true rho. Union over all lags/graphs contains the true tuple without selection or a continuum multiplicity penalty.'),
        ('nuisance_and_cost','All unknown covariance and structural nuisance parameters remain in the region. Rational relative tolerance requires explicit sample-size/error condition; n=240 cannot use t=1/4,alpha=.02, and receives a whole-line fallback.'),
        ('numerical_enclosure','Exact convex quadratics bound complete lag cells; polarization and dropping PSD/consistency constraints enlarge sets. Input rounding receives a proven Cauchy-Schwarz inflation conditional on a supplied enclosure; no optimizer is used to exclude a graph.'),
        ('set_topology','Moment inversion retains disconnected rays, whole line, singleton and empty cases. Zero-zero feasibility implies all effects. 1324 direct rectangle-intersection comparisons independently confirm the exact reference.'),
        ('information_limit','Symbolic structural inversion gives the same positive-definite observed covariance and temporal law for every real effect; surgical derivative is tau. Strong relevance does not justify exclusion; zero relevance can remain uninformative even with exclusion.'),
        ('separating_experiment','Directly assigned actions in independent common-history Gaussian episodes identify the invariant effect. Independent means/residual sums yield a Student pivot and finite conservative second-moment bound; encouragement-only, dependent episodes and nonnormal cases are distinct.'),
        ('composition','Intersection covers the common transported effect on both component events with error alphaO+alphaI; dependence between sources is permitted. Empty intersections are retained. Actual graph topology can remain unidentified.'),
        ('planning','m=200 per binary arm, effect20, pooled variance100 and alphaI=.03 imply squared half-width9950/297. Planning net lower bound is about -2364.19 dollars for3000 customers at15 dollars cost; no bank result or ROI claimed.'),
        ('scope','Argument and deterministic reference outcome only. No final data generated, approved final-study design, empirical qualification, full R04S/D03/D09 closure or independent scientific acceptance.')]
    review={'status':'pass','issues':[],'reviewer':{'name':'Current author/coordinator','kind':'author'},
            'scope':'SCI.ARGUMENT.R04S restricted argument and counterexample criteria',
            'findings':[{'criterion':a,'finding':b} for a,b in findings],
            'evidence':[ref(ARG,'Full proof and counterexamples'),ref(BASE/'plan-review.md','Reviewed plan and pitfalls'),
                        ref(BASE/'reproduction-review.json','Independent exact verification'),
                        ref(ROOT/'docs/program/master/work/R04-v3/derivation.md','Predecessor finite-lag law'),
                        ref(ROOT/'docs/program/master/work/R04-v3/review.md','Preserved failures'),
                        ref(ROOT/'docs/program/master/work/R04-v3/results.json','Exact original study counts')],
            'original_gap_qualification':False,'final_study_registered':False}
    core.write(BASE/'argument-author-review.json',review)
    specs=[('argument','Continuous-lag confidence region and separating intervention',ARG,
            'law; Gaussian projection proof; continuous covariance region; rounding inflation; equal-law family; direct intervention; conservative precision',
            'Restricted finite-confidence and numerical outer-bound argument with explicit sample cost; not unrestricted temporal inference.'),
           ('exact','Exact temporal moment inversion and information-design references',BASE/'reproduction-review.json',
            '1324 ratio checks;648 variance identities;1944 perturbation checks;symbolic equal-law and surgical derivative;rational planning interval',
            'Deterministic references reproduce covariance, topology, continuum enclosure and intervention planning; no random evaluation.'),
           ('predecessor','Preserved temporal graph-retention study and limitations',ROOT/'docs/program/master/work/R04-v3/review.md',
            '4096 requests;weak/latent512 whole-line;persistent507 finite;false-exclusion0 true-class retained',
            'The prior valid-grid coverage did not establish finite availability or correctness of a false exclusion.')]
    sources=[]
    for key,title,path,anchor,claim in specs:
        sources.append({'integrated_citation_key':'exec13_temporal_'+key,'kind':'project_study' if key=='predecessor' else 'project_derivation',
            'title':title,'author':'Causal banking research project','year':2026,
            'source_identity':str(path.relative_to(ROOT)),
            'version_date':'2026-10-13 author argument/review; preserved predecessor2026-10-11',
            'local_copy':ref(path,anchor),'inspected_anchors':[anchor],'supported_claims':[claim],
            'limits':['Project evidence, not an external scholarly paper, bank validation or independent review.']})
    audit={'cutoff':'2026-10-07','sources':sources,'new_scholarly_citations':[],
           'evidence':[ref(BASE/'argument-author-review.json','Author proof and scope review'),
                       ref(BASE/'oracle-results.json','Exact illustrative results'),
                       ref(ROOT/'tools/temporal_graph_oracles_20261013.py','Candidate exact calculations'),
                       ref(ROOT/'tools/review_temporal_graph_oracles_20261013.py','Independent symbolic/arithmetic checks')]}
    shared.verify_refs(audit);core.write(BASE/'source-audit.json',audit)
    # Reuse the developed argument, removing process/gap identifiers from the product narrative.
    body=ARG.read_text()
    body=body.replace('# Continuous temporal uncertainty and the information that changes an effect decision',
                      r'\chapter{Continuous temporal uncertainty and an informative intervention}'+'\n'+r'\label{exec13:temporal-region}')
    body=body.replace('## Observation law and the preserved failure', '## The banking question and the observation law')
    opening=('A bank can observe a stable association between an offer and a subsequent outcome yet remain unable to price the effect of changing the offer. '
             'The missing information can persist even with an exactly known observational distribution. '
             'This chapter develops a restricted temporal confidence construction and shows what an additional direct intervention would contribute. '
             'The mathematical construction and exact calculations are project derivations, not a fitted bank result. '+r'\cite{exec13_temporal_argument,exec13_temporal_exact}'+'\n\n')
    body=body.replace('This is a project derivation and deterministic reference calculation. It\nextends one component of the predecessor; it does not qualify arbitrary\ntemporal graphs. In R04-v3,',opening+'In the preserved temporal graph study,')
    body=body.replace('The original\nstudy, failures and scope remain unchanged.',
                      'These findings distinguish numerical coverage from informative effects and from a valid causal restriction. '+r'\cite{exec13_temporal_predecessor}')
    body=body.replace('No full R04S, original D03/D09 gap, bank capability or independent acceptance\nis awarded by this argument.',
                      'This argument establishes no general temporal-graph capability, bank validation or independent acceptance.')
    body+='\n'+r'\label{exec13:temporal-region-end}'+'\n'
    (BASE/'chapter.md').write_text(body)
    note={'finding':'Completed author-reviewed continuous-lag region, certified rational enclosure strategy, equal-law counterexample and direct-action finite inference route. Exact checks pass; no random final study or original-gap closure.',
          'next_action':'Compile and text-review a preserving monograph successor with this argument, bind the delivery, record SCI.ARGUMENT.R04S, then continue the next eligible operation.',
          'evidence':[ref(ARG,'Full argument'),ref(BASE/'argument-author-review.json','Reviewed proof and scope'),
                      ref(BASE/'reproduction-review.json','Exact verification'),ref(BASE/'chapter.md','Product narrative prepared')]}
    core.write(BASE/'checkpoint-01.json',note)
    print(json.dumps({'review':'pass','source_records':len(sources),'chapter_words':len(body.split()),'random_draws':0}))


if __name__=='__main__':main()
