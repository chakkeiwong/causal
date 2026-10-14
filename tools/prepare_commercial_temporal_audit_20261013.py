#!/usr/bin/env python3
"""Bind inspected official passages and explicit omissions; no automatic acceptance."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re

from normalize_commercial_temporal_20261013 import BASE, RAW, ROOT, ref


def main():
    assert not (BASE / 'source-audit.json').exists()
    rows = [
        ('genie_dbn','exec13_ct_genie_dbn','GeNIe: Dynamic Bayesian networks','BayesFusion, LLC',2024,
         'GeNIe manual family 5.0.R2, built 2024-11-23; mutable technical page',
         ['A dynamic Bayesian network (DBN) is a Bayesian network extended', 'DBNs can include continuous nodes'],
         ['The overview describes a stationary discrete-time stochastic-process representation, temporal observations and continuous-node examples.'],
         'Model representation and inference, not learned temporal structure or verified intervention invariance.'),
        ('genie_dbn_learning','exec13_ct_genie_learning','GeNIe: Learning the parameters of discrete DBNs','BayesFusion, LLC',2024,
         'GeNIe manual family 5.0.R2, built 2024-11-23; mutable technical page',
         ['While GeNIe structure learning algorithms','The file used for learning the parameters','Once we press OK, the EM algorithm','A remark on the network structure'],
         ['The inspected page expressly excludes dynamic structure learning while documenting EM parameter learning in a fixed discrete DBN, time-indexed columns and ignored existing evidence.'],
         'Explicit page-specific exclusion; no market-wide absence claim or extension to arbitrary continuous DBN fitting.'),
        ('smile_tutorial6','exec13_ct_smile_tutorial','SMILE Programmer Manual: Tutorial 6, A dynamic model','BayesFusion, LLC',2024,
         'SMILE manual family 2.2.4.R1, built 2024-04-27; mutable tutorial',
         ['The model contains three discrete chance nodes','Two of the three arcs','CPTs for the nodes are initialized','Finally, we adjust','Note that DSL_nodeVal','Because the probabilities'],
         ['C++ temporal construction retains initial and transition CPTs, lag orders, slice counts, integer evidence indices and slice-major beliefs.'],
         'Source tutorial inspected; no C++ vendor engine or wrapper runtime executed.'),
        ('stata_vargranger','exec13_ct_stata_granger','Stata Time-Series Reference: vargranger','StataCorp',2026,
         'Retrieved Stata command manual; r19 data route appears in examples; exact cutoff edition not independently authenticated',
         ['vargranger performs a set of Granger', 'A variable', 'For each equation and each endogenous', 'Because it may be interesting'],
         ['Pairwise Granger tests concern predictive lag restrictions; use after svar or ivsvar still tests the underlying reduced-form VAR.'],
         'Manual inspection only; no finite selected-model or intervention coverage claim.'),
        ('stata_varsvar','exec13_ct_stata_svar','Stata Time-Series Reference: var svar','StataCorp',2026,
         'Retrieved Stata structural-VAR command manual; mutable route, exact cutoff bytes not authenticated',
         ['svar fits a vector autoregressive', 'noidencheck requests', 'careful in specifying this option. Models that are not structurally'],
         ['User-specified short-/long-run restrictions supply structural interpretation. Local identification checking can be suppressed and convergence does not establish identification.'],
         'Truth of economic restrictions and global identification are not established by local checks or convergence.'),
        ('stata_ivsvar','exec13_ct_stata_ivsvar','Stata Time-Series Reference: var ivsvar','StataCorp',2026,
         'Retrieved Stata external-instrument structural-VAR command manual; mutable route',
         ['ivsvar estimates the parameters', 'vides two estimators', 'vce(vcetype)', 'We call', 'normalization is the unit effect normalization', 'Short-run constraints are required'],
         ['GMM for a single target and minimum distance for multiple targets; instrument relevance and nontarget exclusion; normalized target-column identification; additional multi-target constraints; robust/cluster/HAC GMM options.'],
         'The text extraction reports k(k-1)/2 information counts in its introductory covariance discussion; this comparison does not rely on those counts. Symmetric covariance counts and all displayed matrix algebra are independently derived project calculations. No instrument-validity or weak-instrument coverage guarantee inferred.'),
        ('sas_causal','exec13_ct_sas_causal','SAS/ETS 14.1 User Guide: VARMAX CAUSAL statement','SAS Institute',2026,
         'Archived SAS/ETS 14.1 manual; acquisition 2026-10-13',
         ['A CAUSAL statement prints','If the P=0 option','The null hypothesis'],
         ['The CAUSAL statement fits VAR Granger tests using GROUP1/GROUP2 variables and MODEL lag order; order zero is inapplicable.'],
         'Printed word causal does not establish a surgical intervention effect; no generic SAS product absence claim.'),
        ('sas_structural','exec13_ct_sas_structural','SAS/ETS 14.1 User Guide: Dynamic simultaneous equations modeling','SAS Institute',2026,
         'Archived SAS/ETS 14.1 manual; acquisition 2026-10-13',
         ['form is referred to as a dynamic','Because is assumed to be positive-definite','The PRINT=(DYNAMIC) option','A dynamic simultaneous equations model involves'],
         ['The page documents a lower-triangular dynamic representation and PRINT=(DYNAMIC).'],
         'Equation images are absent from the extracted text. Only explicit prose/command claims are used; the monograph supplies its own exact matrices, not a transcription of missing equations.'),
        ('mplus_addendum81','exec13_ct_mplus81','Mplus Version 8.1 Language Addendum','Muthen and Muthen',2018,
         'Version 8.1 language addendum with 2018 reference dates; acquired 2026-10-13',
         ['residual dynamic structural equation modeling','Residual dynamic structural equation modeling','RDSEM is available for both N=1','When there is missing data on the covariate','LAGGED = y(1);','s | y ON time;'],
         ['DSEM/RDSEM lag outcome/residual distinctions; N=1 and two-level models; random slopes, latent centering, categorical lags, linear trends and missing-covariate/TINTERVAL limitations.'],
         'Supplied-model syntax and fitting documentation, not causal-graph discovery, policy identification or arbitrary regime handling.'),
        ('ibm_tcm','exec13_ct_ibm_tcm','IBM SPSS Statistics: Temporal Causal Models','IBM',2026,
         'SPSS Statistics 31.0.0 documentation route; retrieved 2026-10-13',
         ['In temporal causal modeling, you specify','causal refers to Granger causality.','Temporal causal modeling supports two types','Separate time series','This procedure pastes'],
         ['Automatic predictive-input selection is described in Granger terms; column and multidimensional data structures; TCM MODEL syntax.'],
         'Detailed build/time-grid routes redirected to an IBM Documentation shell. Those settings remain unverified; overview wording supplies no intervention or selected-graph coverage guarantee.'),
        ('bayesia_inference','exec13_ct_bayesia_inference','BayesiaLab: Inference, diagnosis, prediction and simulation','Bayesia',2026,
         'Mutable official feature documentation, acquisition 2026-10-13; edition unspecified',
         ['Bayesian networks represent a Joint Probability Distribution','Hard Evidence:','Beyond observation, BayesiaLab can compute intervention effects.'],
         ['Observation/evidence and intervention operations are distinguished; Graph Surgery and Likelihood Matching are named.'],
         'Feature-level workflow evidence only. Exact temporal algorithm/API, statistical uncertainty, license edition and runtime remain unverified.'),
        ('bayesia_identification','exec13_ct_bayesia_identification','BayesiaLab E-Book: Causal identification and estimation','Bayesia',2026,
         'Mutable official technical e-book section, acquisition 2026-10-13; edition unspecified',
         ['Identification analysis is about determining','Where do we get such causal assumptions?','It is important to realize that the absence','But if the causal effect is identifiable'],
         ['Identification requires causal information represented by a DAG in the chapter and is distinguished from subsequent estimation; more data do not replace missing causal assumptions.'],
         'No temporal discovery/latent-confounding algorithm or API parity established by this passage.')]
    sources = []
    for key, cite, title, author, year, version, markers, claims, limits in rows:
        receipt_path = RAW / ('exec13_temporal_' + key + '.receipt.json')
        r = json.loads(receipt_path.read_text()); assert r['status'] == 'saved'
        text_path = BASE / (key + '.txt'); lines = text_path.read_text().splitlines()
        anchors = []
        for marker in markers:
            found = [i for i,line in enumerate(lines) if marker in line]
            assert found, (key,marker)
            index = found[0]; excerpt = '\n'.join(lines[index:min(index+3,len(lines))])
            anchors.append({'anchor':f'Extracted primary text lines {index+1}-{min(index+3,len(lines))}',
                            'quote':excerpt})
        sources.append({'integrated_citation_key':cite,'kind':'official_documentation',
            'title':title,'author':author,'year':year,'source_identity':r['url'],
            'version_date':version,'cutoff':'2026-10-07','accessed_utc':r['accessed_utc'],
            'cutoff_limit':'Post-cutoff acquisition; edition identity does not independently authenticate exact cutoff bytes.',
            'local_copy':r['local_copy'],'text_copy':r['text_copy'],
            'acquisition_receipt':ref(receipt_path,'Bounded official acquisition, headers and content identity'),
            'inspected_anchors':anchors,'supported_claims':claims,'limits':limits})
    examples = BASE / 'exact-results.json'
    sources.append({'integrated_citation_key':'exec13_ct_examples','kind':'project_derivation',
        'title':'Temporal funding prediction, intervention, frequency and common-calendar exact examples',
        'author':'Causal banking proposal project','year':2026,
        'source_identity':'Project-owned exact stipulated models and assumptions',
        'version_date':'2026-10-13 exact rational/symbolic evaluation',
        'local_copy':ref(examples,'All four exact example groups'),
        'code':ref(ROOT/'tools/commercial_temporal_examples_20261013.py','Exact algebra and two calculation routes'),
        'inspected_anchors':['predictive_common_factor','equivalent_dynamic_models','sampling_frequency','common_calendar'],
        'supported_claims':['Predictive coefficient 17/42 while the surgical effect is zero in the specified law.',
            'Two equal-observational-law structures imply assumed three-month net values USD137.50 and minus300.',
            'Quarter-end cross-lag 3/20 differs from monthly1/5.',
            'Twenty branches with the declared common shock give variance ratio21/2.'],
        'limits':['No vendor execution, bank estimate, general identification theorem or empirical calibration. Zero random draws.']})
    all_commands = []
    for name in ['acquisition-commands-01.json','acquisition-commands-02.json','acquisition-commands-03-complete.json']:
        all_commands += json.loads((BASE/name).read_text())['requests']
    assert len(all_commands) == 28 and len({r['id'] for r in all_commands}) == 28
    acquisition = {'total_public_gets':28,'successful_transports':sum(x['exit_code']==0 for x in all_commands),
        'requests':[ref(RAW/('exec13_temporal_'+x['id']+'.receipt.json'),'Observed official GET result') for x in all_commands],
        'normalization_repair':'Batch03 normalization was started while one command still ran. The initial incomplete command record remains. First two records were already normalized; batch04 completed the remaining two after exit. No source was overwritten or HTTP success mistaken for technical content.',
        'content_failures':['IBM build and interval routes return a documentation shell despite HTTP200. EViews help is navigation only; technical routes remain unavailable.']}
    (BASE/'acquisition-review-complete.json').write_text(json.dumps(acquisition,indent=2)+'\n')
    source_audit={'sources':sources,'cutoff':'2026-10-07','search_scope':'Thirteen explicit candidate families; 28 bounded official public reads and preserved local records. Not exhaustive market coverage.',
        'acquisition_review':ref(BASE/'acquisition-review-complete.json','All28 completed reads and semantic-content failures'),
        'normalizer':ref(ROOT/'tools/normalize_commercial_temporal_20261013.py','Inert document normalization'),
        'audit_preparer':ref(Path(__file__),'Inspected primary passages and scoped claims'),
        'runtime_executed':False,'original_gap_qualification':False}
    (BASE/'source-audit.json').write_text(json.dumps(source_audit,indent=2)+'\n')
    print(json.dumps({'sources':len(sources),'public_gets':28,'saved':acquisition['successful_transports']}))


if __name__ == '__main__':
    main()
