#!/usr/bin/env python3
"""Resolve explicit aliases from reviewed component evidence, without redoing research."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import dose_response_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=controller.base;core=run.core;ROOT=core.ROOT
DAY=ROOT/'docs/program/execution/2026-10-24'
BASE=DAY/'dose-alias-reconciliation-v1'
SOURCE=DAY/'dose-response-reuse-v1'
READ=DAY/'judge-bias-reader-v1'
read=lambda p:json.loads(p.read_text())
SPECS={
 'causaldrf':dict(operation='SW.DECISION.v13_causaldrf',candidate='causaldrf',
    commit='cb67aca60bc4dbd6792edd062cb7682c656d5908',version='0.4.2',
    source_key='exec24_dose_causaldrf',prior_key='v13_sw_causaldrf',
    scientific_scope='GPS outcome standardization over a declared population and grid; transformations, density units and pointwise interval semantics retained.',
    specific_limits=['Selected transformed normal density lacks the original-scale Jacobian; fixed-dose score information and finite outcome surfaces are distinct.',
                     'Sorted bootstrap endpoint expression has a zero lower index at B=20; native behavior and a justified sampling law remain unqualified.']),
 'causalgps':dict(operation='SW.DECISION.v13_causalgps',candidate='CausalGPS',
    commit='3a837d66e5cb791a310a18b63919abe04b4b290f',version='0.5.1',
    source_key='exec24_dose_causalgps',prior_key='v13_sw_causalgps',
    scientific_scope='Continuous-exposure design, matching/weighting and balance diagnostics; target population, support, density measure and uncertainty retained.',
    specific_limits=['Selected0.5.1body is not the historical tuning loop; preserve IDs,join cardinality and actual orchestration.',
                     'Residual density scale,allzero fallback and differing trim object fields require exact worker conformance; no native failure is claimed.'])}


def prepare():
    assert not BASE.exists();BASE.mkdir()
    choice=read(SOURCE/'choice.json');audit=read(SOURCE/'source-audit.json')
    for name in ['review.json','choice.json','source-audit.json','identity-review.json',
                 'dependency-license-review.json','conversion-contract.json','mathematical-review.json']:
        verify_bindings(read(SOURCE/name))
    verify_bindings(read(READ/'release-source-review.json'))
    assert exact.calculate()==read(SOURCE/'exact-results.json')
    integrated={s['integrated_citation_key']:s for s in read(READ/'reader/source-audit.json')['sources']}
    source_by_key={s['integrated_citation_key']:s for s in audit['sources']}
    old_choices={s['candidate']:s for s in choice['candidates']}
    rights=read(SOURCE/'dependency-license-review.json')['candidates']
    rows=[]
    for role,spec in SPECS.items():
        prior=integrated[spec['prior_key']];source=source_by_key[spec['source_key']]
        selected=old_choices[spec['candidate']]
        assert selected['revision']['commit']==spec['commit']
        assert spec['commit'] in prior['source_identity'] and spec['commit'] in source['source_identity']
        assert integrated[spec['source_key']]==source
        assert spec['version'] in selected['revision']['message']
        assert selected['decision']=='reference' and not selected['integration_allowed']
        evidence=[ref(SOURCE/n,'Existing candidate-specific reviewed evidence') for n in
                  ['review.json','source-audit.json','identity-review.json','choice.json',
                   'dependency-license-review.json','conversion-contract.json','mathematical-review.json',
                   'exact-results.json','development.tex','omissions-register.json']]
        evidence += [ref(READ/'release-source-review.json','Preserves the existing discussion and citations'),
                     ref(READ/'reader/source-audit.json','Exact integrated source identities'),
                     ref(Path(__file__),'Alias identity and contract review')]
        decision=dict(operation=spec['operation'],candidate=spec['candidate'],decision='reference',
            canonical_operation='SW.DECISION.seed_049',canonical_component=deepcopy(selected),
            alias_basis='Same named package and exact pinned distribution already individually reviewed inside the five-component decision; no family-level inference.',
            source=source,license_dependencies=rights[role],scientific_scope=spec['scientific_scope'],
            specific_limits=spec['specific_limits'],conversion_contract=ref(SOURCE/'conversion-contract.json','Existing proposed input/output/refusal contract'),
            alternatives=deepcopy(choice['alternatives']),costs=deepcopy(choice['costs']),
            owners=deepcopy(choice['owners']),maintenance=choice['maintenance'],
            revisit_trigger=choice['revisit_trigger'],limitations=deepcopy(choice['limitations'])+spec['specific_limits'],
            evidence=evidence,integration_allowed=False,capabilities=[],native_execution=False,
            incremental_research_claim=False,manuscript_already_integrated=True)
        verify_bindings(decision);write(BASE/(role+'-decision.json'),decision)
        rows.append(dict(role=role,operation=spec['operation'],decision='reference',
                         evidence=ref(BASE/(role+'-decision.json'),'Explicit candidate contract')))
    write(BASE/'plan-review.json',dict(status='pass_for_alias_reconciliation',
        findings=['Both aliases match exact prior package names and commits.','Every contract criterion is met by explicit component evidence,not umbrella approval.',
                  'Existing main-reader discussion is preserved; no duplicate manuscript chapter or new capability.','Record each alias separately only after predecessor publication completes; update counts in an exact paired sponsor and program.'],
        decisions=rows,evidence=[ref(Path(__file__),'Reconciliation procedure')],
        proposal_accepted=False,native_execution=False))
    print(json.dumps(dict(prepared=rows,incremental_native_capabilities=0)))


def receipt(role):
    state=core.read(ROOT,core.STATE);spec=SPECS[role];op=spec['operation']
    assert state['execution_runtime']['active']['operation']==op
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op)
    assert op not in merged['execution_program']['results']
    value=read(BASE/(role+'-decision.json'));verify_bindings(value)
    verify_bindings(read(BASE/'plan-review.json'))
    value.update(status='pass',scope='Completed exact-alias proposal reference choice;no native admission')
    out=ROOT/node['outputs'][0];write(out,value)
    evidence=[ref(BASE/(role+'-decision.json'),'Exact candidate decision'),ref(BASE/'plan-review.json','Reviewed reconciliation')]
    findings=['Name and exact pinned component match earlier individual source/version/rights/dependency/maintenance inspection.',
              'Scientific target,uncertainty,alternatives,unmeasured cost categories,owners and revisit conditions retained explicitly.',
              'Reference only: no adapter,integration or capability granted;public conformance and rights remain future gates.']
    result=run.ledger.receipt_template(node)
    result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        outputs=[ref(out,'Explicit alias reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],
        limitations=value['limitations'],capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result)
    write(BASE/(role+'-operation-receipt.json'),result)
    print(json.dumps(dict(role=role,operation=op,decision='reference',native_execution=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare',*SPECS])
    command=parser.parse_args().command
    prepare() if command=='prepare' else receipt(command)
