#!/usr/bin/env python3
"""Bind the inspected CausalImpact proposal decision without enabling an adapter."""
from datetime import datetime, timezone
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import causalimpact_examples_20261013 as examples
import master_control as core
from publish_latent_r_review_v2_20261013 import verify_bindings, write

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-13/causalimpact-reuse'
ref = shared.ref
PIN = '0f5bf8d97cfb13321926c68b7eaeec74bb692b61'
TPIN = '2bd0a64f783616a44184d77c9180ed2af076ef05'


def main():
    completions = {}
    for p in BASE.glob('acquisition-completion-*.json'):
        for r in json.loads(p.read_text()):
            assert r['status']=='fulfilled'
            completions[r['value']['session']]=r['value']
    acquired={}
    for p in sorted(BASE.glob('acquisition-0[1-5].json')):
        for r in json.loads(p.read_text()):
            assert r['status']=='fulfilled'
            row=r['value'];result=completions[row['session_id']] if row.get('session_id') else row
            assert result['exit_code']==0,row['id']
            ext=row.get('extension','json' if row['id'].endswith('_cutoff') else 'txt')
            raw=BASE/(row['id']+'.'+ext)
            acquired[row['id']]={'url':row['url'],'local_copy':ref(raw,'Authentic pinned upstream bytes'),
                'headers':ref(BASE/(row['id']+'.headers'),'HTTP response headers'),
                'receipt':ref(p,'Bounded public acquisition command result'),
                'exit_code':result['exit_code'],'observed_result':result['output'],
                'local_write_utc':datetime.fromtimestamp(raw.stat().st_mtime,timezone.utc).isoformat()}
    write(BASE/'acquisition-review.json',{'requests':acquired,'cutoff':'2026-10-07','access_date':'2026-10-13',
        'selection':'Exact commits no later than cutoff; dependency/TFP API queries use UTC end of cutoff day.',
        'limits':'CRAN mirror DESCRIPTION and license inspection is not a resolved installed environment or a complete transitive source audit.'})
    aliases=[
        {'name':'Google R CausalImpact','canonical':'google/CausalImpact','revision':PIN,'version':'1.4.1','disposition':'reference; future isolated R wrapper conditional'},
        {'name':'TFP CausalImpact','canonical':'google/tfp-causalimpact','revision':TPIN,'version':'0.2.0','distribution':'tfp-causalimpact','import_namespace':'causalimpact','disposition':'separate candidate; backend behavior and dependency closure deferred'},
        {'name':'aGrUM CausalImpact symbol','canonical':'aGrUM graphical-identification API previously inspected under v12_sw_agrum','disposition':'name collision; not Google Bayesian time-series package'},
        {'name':'Dafiti Python causalimpact','canonical':'dafiti/causalimpact','disposition':'lineage lead named by TFP README; no source/runtime/license approval borrowed'}]
    omissions=[
        {'candidate':'Full native R environment and transitive dependencies','reason':'Observed R4.1.2 and none of seven queried packages; below R>=4.5.0 at pin. All transitive dependencies and native build terms have not been frozen.','revisit':'An isolated compatible pinned environment and dependency/notice inventory supporting a matched native oracle.'},
        {'candidate':'TFP backend implementation and equivalence to R','reason':'Pinned identity, exports, requirements, README and Apache license inspected, not sampler/backend behavior. No compatible backend lock or native results.','revisit':'Inspect backend source and licenses; choose matched targets/priors and run calibrated, declared comparisons.'},
        {'candidate':'Dafiti and other Python packages sharing the import name','reason':'Separate lineage lead, not a canonical alias and not surveyed as an interchangeable engine.','revisit':'Separate exact repository, distribution, revision, source, license and behavior review if selected.'},
        {'candidate':'Actual bank donor invariance and economic inputs','reason':'Proposal examples have stipulated controls, law and values; no bank assignment or prices.','revisit':'Only after a prototype makes the target-bank study decision relevant.'}]
    write(BASE/'omissions-register.json',{'items':omissions,'local_blocker_only':True,'no_family_level_approval':True})
    contract={'status':'proposed_not_implemented','integration_allowed':False,
        'request':['response and units; stock/flow/rate/index type and aggregation','calendar, time zone and unique row identity',
            'pre/post boundaries and permitted gaps','donor identities and intervention-invariance/stability restrictions',
            'provenance and explicit missingness/transformation policy','model structure, priors, full R random state and bsts seed semantics',
            'iteration/resource limits and compatible package/build identities'],
        'response':['effective periods and input transformations','source/runtime/compiled-dependency identities',
            'warnings and explicit execution status','posterior draws or hash-bound draw artifact',
            'point and cumulative summaries with predictive/posterior labels','absolute/relative units and denominator diagnostics'],
        'failure_rules':['Do not treat class CausalImpact alone as successful fit: NULL fitted model and NA inferences remain unavailable.',
            'Missing controls and inadmissible boundaries are distinguishable input failures.',
            'Do not clip periods, fill omitted calendar dates or change aggregation without an explicit recorded transformation.',
            'Do not replace an undefined ratio with zero or a bounded percentage.',
            'Unjustified causal restrictions are a scientific scope failure, not automatically a numerical error.'],
        'future_behavioral_oracle':{'kind':'same-environment matched direct R versus adapter execution',
            'fixtures':['missing calendar date','missing controls','constant response','single post-period row',
                'pre/post gap','out-of-range endpoints','supplied model retaining observed post outcomes'],
            'compare':['effective dates','warnings/errors/NA status','draw dimensions and identity','point/cumulative/relative summaries'],
            'source_tests':'Inspected upstream tests provide candidate cases, not executed evidence.',
            'independent_checks':ref(BASE/'exact-results.json','Authored law and reporting constructions, no native engine run'),
            'statistical_study':'Separate prospective protocol after profile: declared observation law, contamination/break stress cases, matched baselines, fixed seeds/budget/stopping rule; no post-hoc tuning.'}}
    write(BASE/'adapter-contract.json',contract)
    decision={'operation_id':'SW.DECISION.inherited_causalimpact','choice':'reference',
        'canonical_engine':'google/CausalImpact','selected_revision':{'revision':PIN,'declared_version':'1.4.1','committed':'2026-03-31T04:46:51Z','license':'Apache2.0','R_requirement':'>=4.5.0'},
        'aliases_and_distinct_candidates':aliases,
        'selected_scope':'CausalImpact as a proposed Bayesian branch-campaign baseline; future isolated R wrapper conditional on native oracle and environment.',
        'integration_allowed':False,'engine_executed':False,'runtime_qualified':False,
        'target':'Realized post-intervention response path versus modeled no-intervention path conditional on untreated/stable controls and pre-period history.',
        'uncertainty':'Joint posterior predictive trajectories; point/cumulative effect transformations; draw-wise relative ratios; one-sided finite-simulation tail area. No design-based or universal frequentist guarantee.',
        'alternatives':['simple seasonal predictive baseline','previously reviewed donor-weight methods','panel design when its target and assignment assumptions fit','randomized rollout for consequential attribution ambiguity','separately review TFP candidate before funding an R/C++ port'],
        'adopt_integrate_port_reasons':{'adopt':'Do not directly embed unexercised R/dependency behavior in the library.',
            'integrate':'An isolated compatible R process is a future candidate after a native oracle, dependency/notice review and conversion/failure checks.',
            'port':'Defer; reproducing priors, sampler/numerical behavior and dependency obligations is a separate cost; inspect TFP first.',
            'reference':'Selected now; primary-source comparative/proposal use is justified without enabled runtime.'},
        'costs':'Compatible isolated R and compiled stack, dependency notice inventory, data/calendar preparation, donor justification, Monte Carlo diagnostics, adapter fixtures and maintenance; runtime and USD integration costs not measured.',
        'owners':['Research owner declares target, clock, donor invariance and stability restrictions.',
            'Adapter owner supplies compatible environment, dependency notices, conversion/failure contract and resource handling.',
            'Reviewer evaluates native versus adapter behavior and prospective statistical protocol; no independent review claimed.'],
        'revisit_trigger':'Compatible pinned R environment plus complete intended-build dependency/notice inventory, matched native behavior oracle and inspected conversion/failure results; re-review on scientific scope, source revision or platform change.',
        'evidence':[ref(BASE/p,'Reviewed '+p) for p in ['acquisition-review.json','adapter-contract.json','runtime-inventory.json','exact-results.json','omissions-register.json']]}
    write(BASE/'decision-proposal.json',decision)
    groups=[
        ('r','Google CausalImpact maintainers','Pinned R CausalImpact identity, assumptions, license and maintenance',
         'CausalImpact1.4.1, commit '+PIN+', committed2026-03-31; acquired2026-10-13',
         [('description','All fields: package1.4.1, date and R/bsts/direct imports'),('readme','Assumptions and Python recommendation'),
          ('license','Sections2–4,6–8: rights, notice, modification, trademark and warranty terms'),('workflow','Three release-R OS targets and check steps'),('tree','Pinned file identity only')],
         ['Donor invariance and untreated relationship stability are identifying restrictions, not fit diagnostics.',
          'Exact commit records R4.5.0 requirement despite unchanged version1.4.1; workflow file is not a passing CI receipt.',
          'Apache2.0 package terms do not assign the same license to dependencies.']),
        ('semantics','Google CausalImpact maintainers','Pinned R CausalImpact input, model, inference and test source',
         'Same R commit '+PIN+'; static source review, not executed tests',
         [('impact_analysis','FormatInputData lines40–83; periods86–133; model/data branches369–455,460–506'),
          ('model','ObservationsAreIllConditioned31–61; checks63–157; ConstructModel165–256 and fixed prior constants26–30'),
          ('inference','GetPosteriorStateSamples19–38; trajectories40–69; point/cumulative71–171; summary184–283'),
          ('manual','Description, arguments, value and model.args note'),('tests_analysis','ShortTimeSeries497–539; MissingTimePoint574–594; NegativePrediction596–615; supplied-model617–704'),
          ('tests_inference','ComputeCumulativePredictions64–118; CompileSummaryTable120–175'),('tests_model','Ill-conditioning and ConstructModel test cases'),
          ('vignette','Assumptions, model arguments and supplied-model examples'),('misc','StandardizeAllVariables and pre-period standardization helper')],
         ['Post-preperiod response masking, row-time conversion, input restrictions and explicit warnings/NA outputs must be retained.',
          'Default priors and bsts seed setting coexist with R observation-noise generation; complete environment/random-state identity matters.',
          'State means, predictive quantiles, pathwise cumulative summaries, draw-wise relative ratios and appended-observation tail area have distinct meanings.',
          'Source tests establish intended cases only; no native behavior or frequentist coverage is asserted.']),
        ('dependencies','Steven L. Scott and package contributors','Pinned bsts, Boom and BoomSpikeSlab dependency and license declarations',
         'Cutoff CRAN mirrors: bsts0.9.11 9e0414e2031200f4fc87e3d55a298e187a0da622; Boom0.9.17 598578af3d4a2eff8a7249456d7700d231ebee6b; BoomSpikeSlab1.2.7 d1e93a1a39ebcd4318ff5183fce38ee5cc96a37f',
         [(n+'_description','Version, Depends, Imports/LinkingTo, License and compilation fields') for n in ['bsts','boom','spike']]+
         [('bsts_license','Complete copyright-holder/year companion'),('boom_license','LGPL2.1 Sections1–2,4–6 and warranty terms'),('spike_license','LGPL2.1 title and Sections4–6')]+[(n+'_cutoff','Revision/date identity only') for n in ['bsts','boom','spike']],
         ['Declared modeling stack needs compatible R and compiled dependencies; DESCRIPTION is not a solved lock.',
          'bsts declares LGPL-2.1 | MIT + file LICENSE; Boom/BoomSpikeSlab declare LGPL-2.1 | file LICENSE.',
          'Notice/source/relinking and incorporated-code obligations need an intended-build inventory; no blanket approval.']),
        ('python','TFP CausalImpact Authors','Pinned TFP CausalImpact distribution identity and requirements',
         'google/tfp-causalimpact commit '+TPIN+', committed2026-10-05; exported version0.2.0',
         [('tfp_readme','Assumptions, R/Dafiti lineage, unofficial-support statement and installation/import'),
          ('tfp_pyproject','Project distribution, Python requirement, dependencies and module name'),('tfp_init','Version and exports; TF logging environment side effect'),
          ('tfp_license','Apache2.0 text Sections2–4,6–8'),('tfp_cutoff','Revision/date identity only')],
         ['Distinct distribution tfp-causalimpact imports causalimpact; exports fit_causalimpact and option types.',
          'Python>=3.9 and unconstrained TensorFlow/TFP dependency declarations do not establish a compatible environment.',
          'Apache2.0 package identity and stated lineage do not establish numerical equivalence to R or qualify all Python names.'])]
    sources=[]
    for ident,author,title,version,anchors,claims in groups:
        copies=[]
        for name,anchor in anchors:
            a=acquired[name]
            copies.append({'source_identity':a['url'],'local_copy':dict(a['local_copy'],anchor=anchor),'inspected_anchor':anchor})
        sources.append({'integrated_citation_key':'exec13_ci_'+ident,'kind':'software_primary_sources',
            'title':title,'author':author,'year':2026,'source_identity':copies[0]['source_identity'],
            'version_date':version,'local_copy':copies[0]['local_copy'],'additional_sources':copies,
            'anchors':[a for _,a in anchors],'claims':claims,
            'limits':'Static primary-source evidence. No executed engine, complete transitive build approval, matched performance or bank qualification.'})
    paper=ROOT/'docs/papers/Inferring Causal Impact Using Bayesian Structural Time-Series Models Brodersen(2015).pdf'
    receipt=core.read(ROOT,'docs/literature/raw/paper_brodersen2015.receipt.json')
    assert core.sha(paper)==receipt['sha256'] and paper.read_bytes().startswith(b'%PDF-')
    sources.append({'integrated_citation_key':'exec13_ci_brodersen2015','kind':'paper',
        'title':'Inferring Causal Impact Using Bayesian Structural Time-Series Models',
        'filename_title':'Inferring Causal Impact Using Bayesian Structural Time-Series Models','first_author':'Brodersen',
        'author':'Kay H. Brodersen, Fabian Gallusser, Jim Koehler, Nicolas Remy and Steven L. Scott','year':2015,
        'source_identity':'https://doi.org/10.1214/14-AOAS788','version_date':'AOAS9(1),247–274; arXiv1506.00356v1 electronic reprint dated2015-06-01; original acquisition2026-10-07',
        'local_path':str(paper.relative_to(ROOT)),'sha256':core.sha(paper),
        'local_copy':ref(paper,'Electronic reprint pp2–3,6–7,14–15,25–26; equations2.1–2.2,2.14–2.17'),
        'additional_sources':[ref(ROOT/'docs/literature/text/brodersen2015.txt','Inspected extracted primary text'),ref(ROOT/'docs/literature/raw/paper_brodersen2015.receipt.json','Authentic PDF acquisition identity')],
        'anchors':['Reprint pp2–3 and6–7: unaffected controls and stable relation; equations2.1–2.2',
            'Reprint pp14–15: joint posterior predictive law, draw-wise effect/cumulative transforms and stock/flow distinction',
            'Reprint pp25–26: historical placebo uncertainty and alternatives; observational endogeneity caveat'],
        'claims':['State-space representation and joint posterior counterfactual path are inherited method material.',
            'Cumulative flows and stock averages have different interpretations; assumptions are needed for causal attribution.'],
        'limits':'Electronic reprint pagination differs from journal pages; historical paper timings are not current measured performance. No generalized identification or coverage guarantee.'})
    for ident,title,path,anchor,claims,extra in [
        ('examples','Exact control-contamination, aggregation and units constructions',BASE/'exact-results.json',
         'Twelve-row identical observations; opposite effects/net values; dependent draw sums; draw ratios; units',
         ['Identical observed histories can conceal opposite controlled effects under different invariance assumptions.',
          'Four artificial dependent draws and three relative-ratio draws demonstrate aggregation semantics; no fit/coverage claim.',
          'USD1/application, USD20 campaign cost and USD10000 balance examples are stipulated.'],
         [ref(ROOT/'tools/causalimpact_examples_20261013.py','Exact rational arithmetic and checks')]),
        ('reuse','CausalImpact reference decision and proposed adapter contract',BASE/'decision-proposal.json',
         'Scoped reference choice; aliases, targets, costs, owners, conditional native oracle and revisit trigger',
         ['No integration capability or native run is granted; R4.1.2 lacks queried packages and falls below reviewed pin.',
          'Future isolated R wrapper is conditional; TFP backend and port are deferred with concrete triggers.'],
         [ref(BASE/p,'Reviewed '+p) for p in ['adapter-contract.json','runtime-inventory.json','omissions-register.json','plan-review.json']])]:
        sources.append({'integrated_citation_key':('exec13_cimpact_examples' if ident=='examples' else 'exec13_ci_'+ident),'kind':'project_derivation_and_review',
            'title':title,'author':'Causal banking research proposal project','year':2026,
            'source_identity':str(path.relative_to(ROOT)),'version_date':'Project author review2026-10-13; literature cutoff2026-10-07 retained',
            'local_copy':ref(path,anchor),'additional_sources':extra,'anchors':[anchor],'claims':claims,
            'limits':'Authored constructions and proposal decisions; no native engine execution, independent review or bank evidence.'})
    audit={'cutoff':'2026-10-07','sources':sources}
    shared.verify_refs(audit);verify_bindings(audit)
    write(BASE/'source-audit.json',audit)
    assert examples.serial(examples.calculate())==json.loads((BASE/'exact-results.json').read_text())
    write(BASE/'manuscript-review.json',{'status':'pass','issues':[],
        'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'scope':'Source support, mathematical constructions, proposed reuse scope and negative implementation boundary',
        'findings':['Counterfactual law and invariance restrictions match inspected paper/README; no prediction-as-identification claim.',
            'Two observationally identical structural laws differ in donor intervention response; perfect pre-fit supplies no resolution.',
            'State/noise, joint paths, relative ratios, tail-area floor and flow/stock units preserve inspected semantics.',
            'Missing-calendar compression, clipping and warning/NULL/NA handling are source findings, not native test results.',
            'Commit-specific R4.5 requirement, separate compiled-dependency license declarations and actual runtime mismatch are explicit.',
            'Python distribution/import/export identity is separate from aGrUM and from an unreviewed Dafiti lineage lead.',
            'Reference choice resolves this decision without enabling integration; native-oracle and statistical-study work remains proposed.'],
        'evidence':[ref(BASE/p,'Reviewed '+p) for p in ['decision.tex','source-audit.json','decision-proposal.json','adapter-contract.json','exact-results.json','omissions-register.json']],
        'native_execution':False,'visual_acceptance':False,'independent_review':False,
        'checkpoint_repair':'Checkpoint01 omitted inspected anchors and was rejected; checkpoint02 preserves the error and repairs the schema.'})
    bib=[]
    for s in sources:
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+'}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+shared.escape(s['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    print(json.dumps({'sources':len(sources),'new_scholarly_pdf':1,'choice':'reference','integration_allowed':False,'exact_replay':'pass'}))


if __name__=='__main__':
    main()
