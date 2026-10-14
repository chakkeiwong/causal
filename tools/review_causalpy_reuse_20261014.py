#!/usr/bin/env python3
"""Review pinned CausalPy RD semantics without importing upstream code."""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import tomllib

import run_program as control
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-14/causalpy-reuse'
OUTPUT = ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_causalpy/decision.json'
AUDIT = ROOT/'docs/program/execution/2026-10-14/commercial-identification-comparison/v2/reader/source-audit.json'
OP = 'SW.DECISION.inherited_causalpy'
PIN = 'f17b30ff1d33b065119acac83122abe79210fda3'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = ['Static upstream source inspection and exact project arithmetic only; no CausalPy installation, sampling or engine execution.',
          'Resolved dependencies, complete third-party rights and actual sampler behavior remain unqualified.',
          'Identification requires an explicit design; no general RD coverage, bank value or implemented adapter is claimed.',
          'Rendered visual acceptance awaits a fresh image allowance; Q1 and Q5 remain open.']


def exact():
    e = F(1, 1000)
    def mean(x, treated):
        return F(100) + 20*x + 5*treated + 10*x*treated
    jump = mean(0, 1)-mean(0, 0)
    contrast = mean(e, 1)-mean(-e, 0)
    assert jump == 5 and contrast == F(101, 20)
    # Keep the physical model fixed while changing score coordinates z=100*x.
    converted = mean(e/100, 1)-mean(-e/100, 0)
    preserved = mean(100*e/100, 1)-mean(-100*e/100, 0)
    assert converted == F(10001, 2000) and preserved == contrast
    # Same observed mean law, two counterfactual extensions, same sharp assignment.
    rows = [F(-1, 10), F(-1, 100), F(1, 100), F(1, 10)]
    worlds = []
    for x in rows:
        t = int(x >= 0)
        observed_a = 100+20*x+5*t
        observed_b = 100+20*x+5*int(x >= 0)
        assert observed_a == observed_b
        worlds.append({'x': str(x), 'treatment': t, 'observed_A': str(observed_a), 'observed_B': str(observed_b)})
    return {'kind': 'exact_project_reference', 'upstream_execution': False, 'random_draws': 0,
        'model': 'm(x,t)=100+20x+5t+10xt; c=0',
        'epsilon': str(e), 'threshold_jump': str(jump), 'finite_epsilon_contrast': str(contrast),
        'difference': str(contrast-jump), 'identity': 'Delta_epsilon=tau+(2*beta+gamma)*epsilon',
        'unit_change_z_100x': {'unchanged_numeric_epsilon': str(converted), 'physical_epsilon_preserved': str(preserved),
            'required_epsilon_z': str(100*e), 'required_beta_z': '1/5', 'required_gamma_z': '1/10'},
        'identification_counterexample': {'rows': worlds,
            'world_A': 'Y(t)=100+20x+5t; continuous potential means; effect5',
            'world_B': 'Y(t)=100+20x+5*1{x>=0}; no treatment effect; baseline discontinuous',
            'same_observed_law': True, 'effect_A': '5', 'effect_B': '0'},
        'illustrative_economics': {'units': 'USD per borrower near threshold', 'cost': '3',
            'net_A': '2', 'net_B': '-3', 'scope': 'Stipulated values, not population ROI or estimated bank profit'},
        'uncertainty': 'Finite contrast and identification algebra do not establish posterior or frequentist coverage.'}


def main():
    assert not OUTPUT.exists(), 'Use a preserving successor for completed decisions.'
    commit_path = ROOT/'docs/literature/raw/head_causalpy.json'
    commit = json.loads(commit_path.read_text()); tree = json.loads((BASE/'tree.json').read_text())
    assert commit['sha'] == tree['sha'] == PIN and tree['truncated'] is False
    date = commit['commit']['committer']['date']; assert date <= '2026-10-07T15:59:59Z'
    indexed = {r['path']: r for r in tree['tree']}
    write(BASE/'tree-recovery-receipt.json', {'status': 'recovered_observation',
        'recorded_utc': datetime.now(timezone.utc).isoformat(), 'acquired_utc': None,
        'url': 'https://api.github.com/repos/pymc-labs/CausalPy/git/trees/'+PIN+'?recursive=1',
        'http_status_observed_in_saved_session': 200,
        'observation': 'Saved session reports HTTP200 and122148 bytes. Exact acquisition timestamp was not retained separately.',
        'local_copy': ref(BASE/'tree.json', 'Complete tree; truncated false'),
        'headers': ref(BASE/'tree.headers', 'Preserved original response headers'),
        'commit': ref(commit_path, 'Saved commit identity/date; metadata does not establish behavior')})
    specs = [
        ('LICENSE', 'complete Apache2.0 license, conditions and notices', ['Root source license is Apache2.0; this does not settle all dependency rights.']),
        ('pyproject.toml', '18-74,181-211: Python, dynamic version, direct dependencies and test markers', ['Python>=3.12; Beta classifier; broad runtime ranges are declarations rather than a resolved environment.', 'Default test configuration excludes correctness and nightly markers.']),
        ('causalpy/version.py', 'version assignment', ['Pinned source declares1.0.0rc1, distinct from previously saved PyPI0.9.0 metadata.']),
        ('causalpy/experiments/regression_discontinuity.py', '164-252,275-338,528-540: masks, predictions, treatment rule, validation and posterior quantiles', ['Constructs a finite-epsilon upper-treated minus lower-control prediction contrast.', 'Above-cutoff treatment rule is explicit; input validation checks dummy coding but the selected method does not prove design validity.', 'Donut/bandwidth masks and small-sample warning are distinct from identifying assumptions.', 'Selected Bayesian plotting path uses equal-tail posterior quantiles.']),
        ('causalpy/pymc_models.py', '532-568,669-729,803-843: sampling, predictions and linear model', ['Linear model has Normal coefficient priors and Normal likelihood with HalfNormal noise prior.', 'Sampling merges explicit overrides; dependency declarations alone do not fix sampler behavior.', 'mu and y_hat have different meanings.']),
        ('causalpy/experiments/model_adapter.py', '72-80,553-591,773-849: expected means and point prediction conversion', ['PyMC adapter extracts mu; sklearn points acquire singleton chain/draw axes without inferential uncertainty.']),
        ('causalpy/experiments/base.py', 'model setter and build docstrings; design fingerprint warning', ['Fresh model resets result state; a frozen design fingerprint does not detect later data edits; changed data require a new experiment.']),
        ('causalpy/formula_utils.py', 'FormulaSpec dataclasses and build_design_matrices implementation', ['Formula design metadata are part of the experiment contract, not a causal-design certificate.']),
        ('causalpy/skl_models.py', 'ScikitLearnAdaptor.fit/predict and LinearRegression inheritance', ['Point-estimation interface differs from Bayesian sampling; no RD-specific coverage result inferred.']),
        ('causalpy/tests/test_integration_skl_examples.py', '264-313: RD smoke examples', ['Selected tests inspect RD fit/type/plot paths; not an executed target-recovery result here.']),
        ('causalpy/tests/test_input_validation.py', '677-785: treated normalization and donut selection', ['Source tests cover selected integer/bool conversion and mask behavior; not executed in this review.']),
        ('causalpy/tests/test_parameter_recovery.py', '35-110 and full-file literal RegressionDiscontinuity search', ['Selected recovery examples concern other designs; no RD recovery test found by this literal search.'])]
    records=[]
    for path, anchor, claims in specs:
        local=BASE/path.replace('/', '__'); data=local.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
        assert indexed[path]['sha']==blob, path
        records.append({'source_identity':'https://raw.githubusercontent.com/pymc-labs/CausalPy/'+PIN+'/'+path,
            'revision':PIN,'version_date':date,'local_copy':ref(local,anchor),
            'headers':ref(Path(str(local)+'.headers'),'Observed HTTP response'),
            'git_blob_sha1':blob,'tree_identity_verified':True,'inspected_anchors':[anchor],'supported_claims':claims})
    packaging=tomllib.loads((BASE/'pyproject.toml').read_text())['project']
    assert '1.0.0rc1' in (BASE/'causalpy__version.py').read_text()
    old=json.loads(AUDIT.read_text())
    alternatives=[s for s in old['sources']if s['integrated_citation_key'] in ['v12_sw_rdrobust','exec13_ivrd_rdrobust','exec13_ivrd_rddensity']]
    primary={'cutoff':'2026-10-07 Asia/Shanghai','revision':PIN,'source_date':date,'declared_version':'1.0.0rc1',
        'identity':ref(commit_path,'Pinned source identity/date'), 'tree':ref(BASE/'tree.json','Blob verification'),
        'sources':records,'python_requires':packaging['requires-python'],'direct_dependencies':packaging['dependencies'],
        'acquisition_receipts':[ref(BASE/f'acquisition-0{i}.json','Original bounded HTTP observations')for i in (1,2,3)],
        'alternatives':alternatives,'upstream_execution':False,
        'coverage_limits':['Selected sharp-RD path only; DiD, IV, synthetic-control and time-series designs need separate reviews.',
            'No installed lockfile, compiled runtime, CI result or complete rights/security review.',
            'Stata comparator commit uses UTC end-of-day cutoff and exceeds Shanghai cutoff; treat that snapshot as later context, not cutoff evidence. R comparator is before cutoff.']}
    write(BASE/'primary-review.json',primary);write(BASE/'exact-results.json',exact())
    contract={'status':'proposed_reference_contract','integration_allowed':False,
        'inputs':['Immutable observations, IDs, sampling unit, score name/units/cutoff, treatment direction, actual treatment and eligibility.',
            'Outcome units, observation clock, horizon, formula/design metadata, bandwidth, donut and positive epsilon in score units.',
            'Explicit target, continuity/design restrictions, model backend, priors, seed, sampler/chain/draw settings and resolved runtime.'],
        'outputs':['Distinguish finite-epsilon contrast, threshold estimand and policy population; preserve both prediction rows.',
            'Preserve chain/draw/unit IDs and whether point, prior, posterior mean or response predictive.',
            'Keep posterior quantiles, Monte Carlo diagnostics and design sensitivity separate; no singleton-draw confidence interval.',
            'Preserve selected rows, left/right effective support, extrapolation, warnings and fit lifecycle.'],
        'failures':{'treatment_direction_mismatch':'invalid_design; no qualified causal output',
            'insufficient_or_one_sided_support':'unqualified contrast; retain diagnostics',
            'donut_or_large_epsilon_extrapolation':'explicit target/extrapolation flag; no threshold relabeling',
            'nonfinite_or_stale_data':'invalid_request; construct new experiment',
            'sampler_nonconvergence':'unqualified posterior; no confident policy recommendation',
            'unsupported_fuzzy_RD':'route to separately reviewed design or refuse',
            'point_backend_interval_request':'uncertainty_unavailable',
            'runtime_error_or_timeout':'unavailable; never replace by zero effect'},
        'prospective_oracles':['Cutoff equality and reversed treatment coding','Positive epsilon and physical unit transformations',
            'Point versus posterior mean versus predictive draw preservation','Changed-data lifecycle and warnings',
            'Bandwidth/donut masks and left/right support','Seeded exact-law recovery and declared interval qualification'],
        'reference':ref(BASE/'exact-results.json','Independent exact algebra; not upstream behavior test')}
    write(BASE/'conversion-contract.json',contract)
    decision={'operation_id':OP,'canonical_package':'CausalPy','canonical_repository':'pymc-labs/CausalPy',
        'aliases':['causalpy distribution'],'distinct_engines':['PyMC dependency','CausalML','CausalNex','rdrobust'],
        'decision':'reference','decision_scope':'Retain a narrow Bayesian/point sharp-RD reference and defer production integration.',
        'revision':PIN,'revision_date':date,'declared_version':'1.0.0rc1','cutoff':'2026-10-07 Asia/Shanghai',
        'license':{'declared':'Apache-2.0','source':records[0]['local_copy']},
        'python_requires':packaging['requires-python'],'direct_dependencies':packaging['dependencies'],
        'integration_allowed':False,'runtime_qualification':False,'original_gap_qualification':False,
        'primary_evidence':ref(BASE/'primary-review.json','Twelve original blobs verified against pinned tree'),
        'behavioral_oracle':ref(BASE/'exact-results.json','Independent contrast/unit/identification references only'),
        'conversion_failure_contract':ref(BASE/'conversion-contract.json','Explicit prospective semantic contract'),
        'rationale':['Useful quasi-experimental model interface; local causal interpretation still requires design and target restrictions.',
            'Finite prediction separation and dimension conversion can silently alter target or uncertainty without an explicit wrapper.',
            'No executed upstream adapter oracle or resolved environment currently establishes qualified integration.'],
        'alternatives':[{'route':'direct adoption','decision':'defer','reason':'Target, failure and uncertainty boundaries need wrapper validation.'},
            {'route':'narrow integration','decision':'candidate after public prototype','reason':'Preserve upstream models and write a small explicit boundary layer.'},
            {'route':'port','decision':'not selected','reason':'Transfers sampler/model/design maintenance without demonstrated benefit.'},
            {'route':'reference','decision':'selected','reason':'Use pinned source to inform proposal and reproducible design examples now.'},
            {'route':'reject all uses','decision':'not justified','reason':'No evidence of fundamental infeasibility or uselessness; qualification remains scoped.'},
            {'route':'rdrobust','decision':'separate comparator','reason':'Documented local-polynomial and bias-corrected intervals answer a distinct uncertainty question.'}],
        'owner_obligations':{'scientific':'Own local estimand, continuity and exclusion of simultaneous policy changes.',
            'integration':'Own frozen data/design, conversion, failure semantics and separate operations by design.',
            'runtime':'Own resolved environment, complete notices, sampler diagnostics and change control.',
            'evaluation':'Own public/generated benchmark mechanisms, dependence units and predeclared evaluation.'},
        'costs_to_measure':['Environment resolution/build','Prior/likelihood review','Sampler and failed-fit CPU/memory',
            'Design diagnostics and expert review','Conversion maintenance and public prototype comparison'],
        'revisit_trigger':'A pinned reproducible environment plus implemented conversion contract and executed upstream-oracle results; assess each causal design separately.',
        'bank_data_required_for_next_step':False,'limitations':LIMITS}
    write(OUTPUT,decision)
    sources=[]
    for key,title,kind,path,anchor,claims,extra in [
        ('exec14_causalpy_primary','CausalPy pinned sharp regression-discontinuity and model semantics','software_primary_sources',BASE/'primary-review.json','Twelve pinned originals and declared boundaries',[claim for r in records for claim in r['supported_claims']],records),
        ('exec14_causalpy_exact','Exact threshold, coordinate and design-ambiguity examples','project_derivation',BASE/'exact-results.json','All exact calculations',['Finite-epsilon5.05 versus threshold5; equivalent observed laws with effects5 and0; stipulated net2 and-3 USD.'],[ref(Path(__file__),'Fraction arithmetic')]),
        ('exec14_causalpy_decision','CausalPy proposal reuse and conversion decision','project_analysis',OUTPUT,'Alternatives, scope, obligations and revisit trigger',['Reference selected; production integration deferred pending executed semantic and runtime checks.'],[ref(BASE/'conversion-contract.json','Prospective interface and failure contract')])]:
        sources.append({'integrated_citation_key':key,'title':title,'author':'pymc-labs contributors'if kind=='software_primary_sources'else'Causal banking proposal',
            'kind':kind,'year':2026,'source_identity':'https://github.com/pymc-labs/CausalPy/tree/'+PIN if kind=='software_primary_sources'else'Project-authored analysis',
            'version_date':PIN+'; '+date if kind=='software_primary_sources'else'2026-10-14','local_copy':ref(path,anchor),
            'inspected_anchors':[anchor],'supported_claims':claims,'records':extra,'limitations':LIMITS})
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources})
    evidence=[ref(p,'Reviewed decision evidence')for p in[OUTPUT,BASE/'primary-review.json',BASE/'exact-results.json',BASE/'conversion-contract.json',BASE/'plan-review.md',Path(__file__)]]
    verify_bindings(evidence)
    facts=['Pinned source, version, root license, dependencies and distinct designs are inspected and bound to original bytes.',
        'Local target and uncertainty semantics, alternatives, ownership and costs are explicit with reproducible independent algebra.',
        'Reference decision completes proposal selection; integration stays disabled until a real adapter and behavioral oracle are executed.']
    write(BASE/'author-review.json',{'outcome':'pass','reviewer':REVIEWER,'findings':facts,'evidence':evidence,'limitations':LIMITS})
    graph,_,_=control.combined(ROOT,control.core.read(ROOT,control.core.STATE));node=control.ledger.operation(graph,OP)
    receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,capabilities=[],outputs=[evidence[0]],limitations=LIMITS)
    assert len(receipt['criteria'])==len(facts)
    for criterion,fact in zip(receipt['criteria'],facts):criterion.update(verdict='pass',finding=fact,evidence=evidence)
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'decision':'reference','source_blobs':len(records),'version':'1.0.0rc1','integration_allowed':False,'exact':exact()}))


if __name__=='__main__':
    main()
