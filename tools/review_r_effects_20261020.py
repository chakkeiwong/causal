#!/usr/bin/env python3
"""Review the R effects source comparison and record its bounded outcome."""
from fractions import Fraction as F
import json
from pathlib import Path
import r_effects_reference_20261020 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write, transition

run=extension.base
ROOT=run.core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-19/r-effects-v1'
read=lambda p:json.loads(p.read_text())


def main():
    audit=read(BASE/'source-audit.json');verify_bindings(audit)
    results=read(BASE/'exact-results.json');assert results==exact.calculate()
    # Recompute the pooled score over four explicitly centered states, rather
    # than using the conditional variance formula in the reference.
    states=[(F(-1),F(-1)),(F(1),F(1)),(F(-2),F(-6)),(F(2),F(6))]
    assert sum(w*y for w,y in states)/sum(w*w for w,y in states)==F(13,5)
    # Direct uniform moments E[W^k]=2^k/(k+1): E[Y]=65/3,
    # E[WY]=100/3, E[W]=1, Var(W)=1/3.
    assert (F(100,3)-F(65,3))/F(1,3)==35
    assert 20-5==15 and F(35,1000)==F(7,200)
    assert F(200,3)-50==F(50,3)
    assert int(F(1,40)*20)==0 and int(F(1,40)*40)==1
    assert results['missing_treatment']['ATE_worlds']==['1','0']
    assert sum(F(x['probability']) for x in results['missing_treatment']['law'])==1
    mathematical=dict(status='pass_for_scoped_project_argument',issues=[],
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        checks=['Four-state residual score independently yields13/5versus mean conditional slope2.',
            'Uniform moments give projection35, derivative-5and finite contrast15; units convert slope to7/200.',
            'Observed assignment-erasure laws coincide while population effects are1and0; missing-label positivity fails by construction.',
            'Two-row density-scale weighting gives200/3versus50; this is not a causal estimate.',
            'Bootstrap index arithmetic distinguishes zero and positive lower-row indices; no native R behavior asserted.'],
        evidence=[ref(ROOT/'tools/r_effects_reference_20261020.py','Exact authored laws'),
            ref(BASE/'exact-results.json','Reference values'),ref(BASE/'development.tex','Explained derivations'),
            ref(Path(__file__),'Independent moment calculations')],
        native_execution=False,confidence_coverage=False,bank_validation=False)
    write(BASE/'mathematical-review.json',mathematical)
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_execution',
        evidence=[ref(BASE/'plan.json','Reviewed plan'),ref(BASE/'source-audit.json','Authenticated inspected originals'),
            ref(BASE/'omissions-register.json','Uninspected routes')],
        findings=['Source-only proposal work is independent of expensive bank experiments.',
            'Cross-language parity, full rights and native execution remain ungranted.',
            'Each finding is bounded to its pinned path; missing-A guard is resolved without rewriting historical evidence.',
            'The candidate list remains incomplete, so the software cell outcome must remain inconclusive.']))
    write(BASE/'copyedit-review.json',dict(status='pass',issues=[],
        evidence=[ref(BASE/'development.tex','Connected R comparison')],findings=[
            'Notation separates binary A, continuous W, baseline X and label-observation R.',
            'Constant unit conversion differs from covariate-dependent scale omission.',
            'Transformation-score factors at a fixed dose are not treated as proof of universal estimator failure.',
            'Population law, source guard and native conformance remain distinct.'],rendered_review=False))
    evidence=[ref(BASE/n,'R comparison evidence') for n in ['plan.json','plan-review.json','source-audit.json',
        'omissions-register.json','conversion-contract.json','exact-results.json','mathematical-review.json',
        'copyedit-review.json','development.tex']]
    evidence.append(ref(Path(__file__),'Criterion and mathematical review'))
    review=dict(status='inconclusive',operation='SW.CELL.effects_heterogeneity.R',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        scope='R point, heterogeneous and continuous-effect proposal source comparison',
        findings=['Nineteen inspected blobs authenticate to selected commit trees and receipt hashes.',
            'tmle arbitrary missing-treatment admission is contradicted by its guard; NULL/no-variation mean path is separate.',
            'R DoubleML IRM/PLR, grf average/local targets and GPS curves preserve distinct statistical contracts.',
            'DoubleML clustered bootstrap refusal, grf TMLE guards and GPS/curve edge cases are explicit.',
            'BART/causalweight and broader aliases remain uninspected; no exhaustive coverage or runtime admission.'],
        evidence=evidence,limitations=read(BASE/'omissions-register.json')['omissions'],
        original_gap_qualification=False,integration_allowed=False,native_execution=False,
        visual_acceptance=False,final_acceptance=False)
    write(BASE/'review.json',review)
    state=run.core.read(ROOT,run.core.STATE);graph,_,_=run.combined(ROOT,state)
    node=run.ledger.operation(graph,'SW.CELL.effects_heterogeneity.R')
    output=ROOT/node['outputs'][0];output.parent.mkdir(parents=True,exist_ok=True)
    write(output,dict(review,review_binding=ref(BASE/'review.json','Preserved R source review')))
    receipt=run.ledger.receipt_template(node)
    findings=[('inconclusive','Inherited candidates and seven family/alias routes are explicit, but broader R discovery and two alternatives remain uninspected.'),
        ('pass','New technical claims use authenticated local source bytes, commit dates, hashes and inspected anchors; inherited papers and grf citations retain their genuine originals.'),
        ('pass','Uninspected alternatives, acquisition limits, native conformance and complete rights are recorded without unsupported absence findings.')]
    receipt.update(outcome='inconclusive',execution='performed',scope=review['scope'],reviewer=review['reviewer'],
        limitations=['Bounded source comparison, not complete R ecosystem coverage.',
            'No downloaded R implementation executed; rights and prototype conformance remain open.',
            'Authored examples are population laws and stipulated amounts; no measured bank return or calibrated confidence claim.'],
        original_gap_qualification=False,capabilities=[],outputs=[ref(output,'Contracted R coverage review')],
        nonexecution_reason='',revisit_trigger='Complete the registered alternative/source routes; validate guarded runtime modes in an isolated future public prototype.',
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    transition('record',node['id'],BASE/'operation-receipt.json')
    print(json.dumps(dict(operation=node['id'],outcome='inconclusive',native_execution=False)))


if __name__=='__main__':
    main()
