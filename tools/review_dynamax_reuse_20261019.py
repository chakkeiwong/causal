#!/usr/bin/env python3
"""Review pinned Dynamax proposal reuse without running upstream software."""
import hashlib
import json
from pathlib import Path
import re
import dynamax_semantic_reference_20261019 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=extension.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-19/dynamax-reuse-v1';RAW=ROOT/'docs/literature/raw'
PIN='5098927f2c377c0dd548cda750e6f1436220aac6';OP='SW.DECISION.inherited_dynamax'
OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    assert read(BASE/'plan-review.json')['status']=='pass'
    c=read(RAW/'exec19_dynamax_commit_exact.json');t=read(RAW/'exec19_dynamax_tree_exact.json')
    assert c['sha']==PIN and c['commit']['committer']['date']=='2026-09-29T18:17:46Z'
    assert t['sha']==c['commit']['tree']['sha'] and not t['truncated'] and len(t['tree'])==169
    assert t['tree']==read(RAW/'exec19_dynamax_tree.json')['tree']
    blobs={r['path']:r['sha'] for r in t['tree'] if r['type']=='blob'}
    rows=read(BASE/'acquisition-manifest.json')['files']+read(BASE/'contract-acquisition-manifest.json')['files']
    ranges=[[(1,60)],[(1,21)],[(1,105)],[(263,283),(525,655)],[(15,102),(114,160),(263,327)],[(22,125)],[(177,222),(357,438)],[(1,55)],[(13,102),(131,183),(254,305)],[(1,45),(48,119)],[(106,154)],[(60,132)]]
    records=[];extracts=[]
    for row,selected in zip(rows,ranges):
        p=RAW/(row['id']+'.txt');rpath=RAW/(row['id']+'.receipt.json');receipt=read(rpath);data=p.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        url=f'https://raw.githubusercontent.com/probml/dynamax/{PIN}/{row["path"]}'
        assert receipt['status']=='saved' and receipt['url']==url and receipt['sha256']==core.sha(p)
        assert blob==blobs[row['path']],row['path']
        lines=data.decode().splitlines();anchors=[f'lines{lo}-{min(hi,len(lines))}' for lo,hi in selected]
        records.append(dict(role='inspected_primary_technical_text',source_identity=url,version_date='Historical commit29September2026; '+PIN,local_copy=ref(p,'; '.join(anchors)),git_blob_sha1=blob,receipt=ref(rpath,'Bounded public-source acquisition'),inspected_anchors=anchors,executed=False))
        extracts.append(dict(path=row['path'],ranges=[dict(start=lo,end=min(hi,len(lines)),text='\n'.join(f'{i+1}: {lines[i]}' for i in range(lo-1,min(hi,len(lines))))) for lo,hi in selected]))
    assert len(records)==12
    deps=re.findall(r'"([^"]+)"',(RAW/'exec19_dynamax_source_2.txt').read_text().split('dependencies = [')[1].split(']')[0])
    assert deps==['jax','jaxlib','tfp-nightly','fastprogress','optax','jaxtyping','typing-extensions','numpy']
    identity_evidence=[ref(RAW/n,'Exact selected identity or acquisition receipt') for n in ['exec19_dynamax_commit_exact.json','exec19_dynamax_commit_exact.receipt.json','exec19_dynamax_tree_exact.json','exec19_dynamax_tree_exact.receipt.json','r3g_commit_dynamax.json']]
    write(BASE/'identity-review.json',dict(status='pass_for_selected_revision',commit=PIN,commit_date=c['commit']['committer']['date'],tree=t['sha'],tree_entries=169,original_blobs=12,evidence=identity_evidence,repair=ref(BASE/'tree-identity-failure.json','Preserved failed equality check; exact tree object matches inherited commit and prior entry list'),version_limit='Dynamic versioneer source is not executed; inherited PyPI1.0.2 is a separate release observation, not assigned to this commit.'))
    write(BASE/'inspected-extracts.json',dict(records=extracts,upstream_execution=False))
    claims=[
        'Pinned project metadata requires Python>=3.10 and eight unversioned direct runtime dependencies, including tfp-nightly; optional groups and build requirements are separate.',
        'HMM inference arguments contain initial-state, transition and emission factors. No separate observed-action/logger factor is automatically added.',
        'The generic transition helper builds time-varying matrices from inputs[1:]; standard transition implementations accept but ignore inputs. Model and low-level API timing descriptions must be reconciled explicitly.',
        'Filtering conditions on the observation prefix; smoothing uses the whole observed sequence. A future-informed smoother cannot supply an online state without changing its information clock.',
        'Normalization preserves zeros, floors positive tiny values and replaces a zero normalizer by one; the all-zero vector stays zero. The likelihood helper subtracts ll.max without an explicit all-minus-infinity branch.',
        'The smoother uses isclose to mask near-zero predicted probabilities before a later normalization. These local stabilizers are not a typed scientific validity result.',
        'fit_em runs a specified iteration count, returns parameters and an objective trace, and returns unchanged parameters with an empty trace when num_iters<=0. No convergence or causal-identification certificate follows.',
        'Selected upstream tests compare filtering/smoothing to finite path summation and check model fitting; the inspected tests were not run here.',
        'A selected helper rejects partially frozen groups for joint EM updates; chosen model tests document support differences between EM and SGD. Parameter flags are not universal fitting promises.',
        'Root MIT notice is inspected at the same commit; complete environment/distribution notices and backend qualification remain unresolved.'
    ]
    limits=['Twelve selected historical source files are not complete algorithm, model-family or transitive dependency/rights coverage.',
        'No upstream code, tests, package, downloaded script, sibling repository or native runtime executed.',
        'Static nonfinite/normalization and indexing observations require future native conformance; no observed runtime defect rate is claimed.',
        'An observational conditional state-space model does not identify intervention effects or qualify an adaptive private logger.',
        'Current maintenance, latest release, selected wheel identity, resolved versions, device precision and cost are unverified.',
        'Exact project examples use declared laws and hypothetical monetary values; no empirical model performance or bank ROI.',
        'The bounded proposal decision grants no integration capability, distribution approval or bank acceptance.']
    source=dict(integrated_citation_key='exec19_dynamax_source',kind='software_primary_sources',title='Dynamax: selected historical HMM inference, transition, fitting, tests, parameter and dependency sources',author='Dynamax contributors',year=2026,source_identity='https://github.com/probml/dynamax',version_date='Selected commit29September2026; '+PIN,selected_commit=PIN,local_copy=ref(RAW/'exec19_dynamax_source_0.txt','Selected pinned README'),records=records,identity_evidence=identity_evidence,inspected_anchors=[dict(anchor=c,inspection='Selected primary code/metadata/test/notice text') for c in claims],supported_claims=claims,limitations=limits,software_executed=False,rights_qualified=False)
    reference=dict(integrated_citation_key='exec19_dynamax_reference',kind='project_authored_exact_reference',title='Exact private-logger and filtering-clock examples for a state-space adapter',author='Causal banking proposal project',year=2026,source_identity='tools/dynamax_semantic_reference_20261019.py',version_date='2026-10-19',local_copy=ref(ROOT/'tools/dynamax_semantic_reference_20261019.py','calculate(): exact rational enumeration'),inspected_anchors=[dict(anchor='calculate()',inspection='Executed authored exact enumeration')],supported_claims=['Private-logger contrast12/25 despite zero causal effect; posterior36/37 versus4/5 when logger omitted.','Filtered state1/5 versus smoothed1/2; assumed net values-10/20USD differ because future information was added.'],limitations=['Authored finite examples, not upstream execution, fitted uncertainty or bank economics.'])
    audit=dict(sources=[source,reference],records=records,cutoff='2026-10-07',limitations=limits)
    write(BASE/'source-audit.json',audit);write(BASE/'exact-results.json',exact.calculate())
    contract=dict(status='proposed_not_implemented',requirements=[
        'Freeze target, allowed history, action and emission clocks, latent-state interpretation, sampling law and conditioning regime.',
        'Either establish external/ignorable inputs or supply and justify a logger-aware joint law; refuse to label conditional fitting as intervention identification.',
        'Require an explicit action-to-input index map and subclass check; compare simulation, model wrapper and low-level filter on a deterministic indexed sequence.',
        'Expose predicted/filtered/smoothed values as separate types with available-through timestamps.',
        'Preserve zero support, invalid probabilities, NaN/infinity, unsupported graph/law, numerical failure and successful outputs as distinct statuses.',
        'Pin dependency graph, backend/device, precision, random seeds, batch and parameter-tree shapes, frozen groups and optimization settings.',
        'Run native finite-path comparisons, impossible-emission and zero-support cases, nonstationary transitions, empty/one-step sequences, partial-freeze rejection, iteration/convergence and device-completion checks.',
        'Retain all fitting traces, starts and failures; qualify parameter uncertainty and model selection separately from state posterior probabilities.'])
    write(BASE/'adapter-contract.json',contract)
    evidence=[ref(BASE/n,'Reviewed proposal evidence') for n in ['plan-review.json','identity-review.json','source-audit.json','inspected-extracts.json','exact-results.json','adapter-contract.json','tree-identity-failure.json','search-leads.json']]+[ref(Path(__file__),'Exact preserving review')]
    decision=dict(operation_id=OP,status='pass',decision='defer',decision_scope='Complete bounded proposal selection of original Dynamax as a conditional state-space comparator; defer executable admission.',preferred_proposal_route='Retain original pinned engine behind a narrow typed conditional-state-space adapter; do not port its numerical stack without demonstrated need.',integration_allowed=False,capabilities=[],runtime_qualification=False,deployment_allowed=False,original_gap_qualification=False,
        identity=dict(canonical_repository='probml/dynamax',entry='inherited_dynamax',selected_commit=PIN,version='Historical commit; no release equivalence established',cutoff='2026-10-07',aliases=['Dynamax','dynamax'],alias_boundary='sts-jax, BlackJAX and bayeux are separate candidates; README links grant no shared qualification.'),
        license=dict(root='MIT',notice_retention_observed=True,complete_distribution_or_transitive_rights=False,permissible_selected_embedding_verified=False),dependencies=dict(python='>=3.10',direct_runtime=deps,resolved_environment=False),maintenance=dict(commit_date=c['commit']['committer']['date'],observation_date='2026-10-19',current_support_or_latest_release_verified=False),
        target_and_uncertainty='Conditional state inference/learning under a declared model; state posterior probabilities are not automatically intervention-effect or parameter-estimation confidence.',
        reason=['Inspected inference and fitting interfaces justify retaining a conditional comparator for a public/synthetic prototype.','Original-engine integration preserves tested semantics and avoids an unsupported numerical port; source tests still require actual conformance.','Private logger, chronology, support, numerical failure and unresolved dependencies prevent executable admission now.'],
        alternatives=[dict(route='Small exact finite-state reference',disposition='retain_baseline',reason='Transparent truth for tiny laws; exponential enumeration is not a scale solution.'),dict(route='Original engine behind narrow adapter',disposition='preferred_proposal',reason='Reuse selected inference with explicit conditional-law and clock contracts.'),dict(route='Port whole inference/learning stack',disposition='defer',reason='No measured target-platform need offsets derivative/numerical and maintenance duplication.'),dict(route='Automatic causal policy optimizer',disposition='reject_initial_profile',reason='Conditional likelihood alone cannot supply logger truth, intervention identification or qualified policy uncertainty.')],
        costs_to_measure=['Dependency and license inventory','Conversion and device startup/JIT','Full computation and synchronization','Multiple fitting starts and failed requests','Native reference conformance and upgrades','Scientific model and logger review'],measured_prices_or_bank_ROI=False,
        owner_obligations=dict(scientific_owner='Own state interpretation, logger, estimand and information clocks.',adapter_maintainer='Own pinned environment, typed conversions, numerical contracts and test evidence.',product_rights_owner='Own complete distribution, notices and release policy.'),
        revisit_trigger='Bind a resolved distribution/backend with notices and run declared finite-path, clock, support, parameter and failure conformance; new versions, regimes or devices reopen review.',evidence=evidence,limitations=limits,reviewer=REVIEWER,bank_inputs_required_for_next_step=False)
    write(OUTPUT,decision);write(BASE/'review.json',dict(status='pass_for_scoped_proposal_decision',reviewer=REVIEWER,reviewed_output=ref(OUTPUT,'Bounded proposal selection with executable admission deferred'),evidence=evidence,findings=claims,limitations=limits))
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    findings=['Selected revision, alias boundaries,12source blobs, root notice, eight direct dependencies and historical maintenance observations are authenticated.','Conditional-law, logger, timing, uncertainty and numerical distinctions, alternatives, costs and owners are explicit.','Bounded proposal selection defers executable admission; exact reference and proposed conformance grant no integration capability.']
    receipt.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,capabilities=[],outputs=[ref(OUTPUT,'Contracted Dynamax proposal reuse decision')],limitations=limits,nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Author review')]) for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt);verify_bindings([audit,decision,receipt])
    print(json.dumps(dict(operation=OP,outcome='pass',source_blobs=12,dependencies=8,integration_allowed=False)))


if __name__=='__main__':main()
