#!/usr/bin/env python3
"""Resolve the inherited did identity and retain unqualified integration limits."""
from fractions import Fraction as F
import json
from pathlib import Path
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=core.ROOT;BASE=ROOT/'docs/program/execution/2026-10-17/did-reuse'
OUTPUT=ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_did/decision.json'


def main():
    assert not BASE.exists() and not OUTPUT.exists();BASE.mkdir(parents=True)
    snapshot=ROOT/'docs/literature/software/did.json';package=json.loads(snapshot.read_text());verify_bindings(package)
    source=ROOT/'docs/literature/raw/r3g_api_did.txt';lines=source.read_text().splitlines()
    pin=package['scientific_qualification']['pinned_api_revision']['sha']
    assert pin=='74b88eb07f1faa644df1271055a0f77848f6550c'
    excerpts=[]
    for name,lo,hi in [('weights',18,65),('inference-options',66,110),('identity',240,251),
                       ('validation',334,383),('cluster-fallback',552,650),('points-only',761,773)]:
        p=BASE/(name+'.txt');p.write_text('\n'.join(f'{i+1}: {lines[i]}' for i in range(lo-1,min(hi,len(lines))))+'\n')
        excerpts.append(ref(p,f'Exact original att_gt.R lines{lo}–{hi}'))
    # Independent conversion reference; no upstream R execution.
    influences={'b':F(-2),'a':F(1),'c':F(1)}
    clusters={'a':'X','b':'X','c':'Y'}
    sums={k:sum(v for u,v in influences.items() if clusters[u]==k) for k in ['X','Y']}
    correct=sum(v*v for v in sums.values())/9
    source_order=['a','c','b'];cluster_order=['a','b','c']
    bad_sums={k:sum(influences[u] for u,label in zip(source_order,cluster_order) if clusters[label]==k) for k in ['X','Y']}
    bad=sum(v*v for v in bad_sums.values())/9
    assert correct==F(2,9) and bad==F(8,9)
    oracle=dict(status='pass',evidential_status='authored conversion reference; upstream_execution=false',
        influence_by_id={k:str(v) for k,v in influences.items()},cluster_by_id=clusters,
        source_row_order=source_order,incoming_cluster_order=cluster_order,
        keyed_variance=str(correct),positional_misalignment_variance=str(bad),
        interpretation='Cluster-sum variance divided by n squared; a source row reorder must retain unit identity.',
        points_only_contract='NA standard errors and null covariance/pretest stay unavailable; numeric critical value alone is not an interval.')
    write(BASE/'conversion-oracle.json',oracle)
    desc=ROOT/'docs/literature/raw/description_did.txt'
    deps=['BMisc>=1.4.4','Matrix','pbapply','ggplot2','DRDID>=1.3.0','generics','methods','tidyr','fastglm','data.table>=1.15.4','dreamerr>=1.4.0']
    evidence=[ref(snapshot,'Inherited identity and scope-qualified source pin'),ref(source,'Commit-pinned att_gt.R original'),
        ref(ROOT/'docs/literature/raw/r3g_api_did.receipt.json','Pinned retrieval URL and acquisition date'),
        ref(ROOT/'docs/literature/raw/r3g_commit_did.json','Commit metadata; not current maintenance proof'),
        ref(desc,'Mutable DESCRIPTION: version, GPL-3 declaration and direct dependencies'),
        ref(ROOT/'docs/literature/raw/repo_did.json','Preserved repository maintenance observation'),
        ref(BASE/'conversion-oracle.json','Independent unit-identity variance reference'),ref(Path(__file__),'Reviewed decision builder')]+excerpts
    limits=['Selected API file is commit-pinned; mutable DESCRIPTION/README are not proven to belong to that commit.',
        'GPL-3 is an observed declaration, not complete same-commit license/dependency or deployment-rights closure.',
        'No package installation, R worker, upstream benchmark, coverage study or bank acceptance is claimed.',
        'Observed August2026 repository metadata is not a current maintenance guarantee.',
        'Exact conversion example tests identity semantics only, not did estimator correctness or uncertainty calibration.']
    findings=['did resolves to bcallaway11/did; did2s is a distinct two-stage package and cannot inherit this approval.',
        'att_gt.R is pinned to74b88eb07f1faa644df1271055a0f77848f6550c; source snapshot remains separate from published release identity.',
        'Group-time ATT target requires first-adoption cohorts, comparison support, no anticipation and conditional parallel-trends premises.',
        'Inference functions are keyed by unit identity. Analytic extra-cluster failure can return unclustered errors with a warning; an adapter must not label those cluster-robust.',
        'Point-only mode returns NA errors and null covariance/pretests. A numeric normal critical value does not restore missing uncertainty.',
        'Weight anchor settings can change retained units or estimator family; preserve warnings and population changes.']
    payload=dict(operation_id='SW.DECISION.inherited_did',status='inconclusive',decision='reference',
        integration_allowed=False,capabilities=[],identity=dict(entry='inherited:did',canonical_repository=package['repository'],
            distinct_from='did2s',pinned_api_revision=pin,observed_package_version=package['package_version']),
        license=dict(observed='GPL-3 in mutable DESCRIPTION',same_commit_original_complete=False),
        dependencies=dict(runtime='R>=4.1.0',direct_imports=deps,resolved_transitive_environment=False),
        maintenance=dict(observed_at=package['observed_at'],last_push_observation=package['last_push'],current_support_contract=False),
        proposed_route='Retain as the R group-time ATT reference; defer integration permission until whole-package pin, rights, environment and behavioral qualification are complete.',
        target='ATT(g,t) and explicitly weighted aggregations; panel and repeated-cross-section paths remain distinct.',
        uncertainty='Preserve influence identities, cluster design, bootstrap/band scope, unavailable pretests, zero-SE NA and large-critical-value warnings.',
        conversion_contract=['First treatment0 means never treated; do not encode arbitrary switching treatment as absorbing adoption.',
            'Align influence rows by rowname/unit ID, never physical position.',
            'Preserve dropped-unit/weight-anchor diagnostics and chosen comparison group.',
            'Requested clustering with fallback warning returns unqualified uncertainty, not a successful cluster-robust result.',
            'Point-only output cannot be promoted to a confidence interval or aggregation requiring influence functions.'],
        alternatives=['A separately qualified did2s or other modern DiD estimator for its own target and assumptions.',
            'A licensed Stata comparator only under its own edition and matched target.',
            'Authored finite reference for conversion diagnostics; not a replacement estimator.'],
        costs=dict(prices='not measured',required=['R/dependency packaging','Rights review','Panel/weight conversion','Bootstrap compute and memory','Maintenance and validation']),
        owner_obligations=['Prototype maintainer pins package/environment and tests warning preservation.','Scientific reviewer approves cohort, comparison, sampling and uncertainty profile.',
                           'Authorized owner resolves applicable deployment/redistribution terms before implementation commitment.'],
        revisit_trigger='Acquire same-commit DESCRIPTION/license/dependency sources and a reproducible complete R environment; execute exact and adverse public/generated profile tests before granting integration_allowed.',
        findings=findings,evidence=evidence,limitations=limits,reviewer=dict(name='Codex author/coordinator',kind='author'))
    write(OUTPUT,payload)
    criteria=[('inconclusive','Identity, selected API pin, observed GPL declaration, dependencies and maintenance metadata are bound; whole-package same-commit rights/environment closure is absent.'),
              ('pass','Target, uncertainty, alternatives, costs, owner obligations and exact revisit trigger are explicit.'),
              ('pass','No integration capability is granted; reference-only decision retains conversion/failure contract and exact authored oracle.')]
    write(BASE/'review.json',dict(status='pass_for_scoped_inconclusive_disposition',findings=findings,evidence=evidence,
        reviewed_output=ref(OUTPUT,'Reference-only decision; no integration permission'),limitations=limits))
    g,_,_=run.combined(ROOT,core.read(ROOT,core.STATE));node=run.ledger.operation(g,'SW.DECISION.inherited_did')
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',scope='Source-bounded reuse decision; no adapter qualification',reviewer=payload['reviewer'],
        capabilities=[],outputs=[ref(OUTPUT,'Contracted reuse decision')],limitations=limits,nonexecution_reason='',revisit_trigger=payload['revisit_trigger'],
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence+[ref(BASE/'review.json','Author decision review')]) for i,(v,f) in enumerate(criteria)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps(dict(outcome='inconclusive',decision='reference',integration_allowed=False,source_pin=pin,identity_oracle='pass')))


if __name__=='__main__':main()
