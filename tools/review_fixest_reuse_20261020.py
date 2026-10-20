#!/usr/bin/env python3
"""Authenticate selected fixest originals and complete a bounded proposal decision."""
import hashlib
import json
from pathlib import Path
import re

import fixest_panel_reference_20261020 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-20/fixest-reuse-v1'
RAW=ROOT/'docs/literature/raw'
PIN='789f888416e97673d154c840eec2d99101fc07b1'
OP='SW.DECISION.inherited_fixest'
OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Sixteen selected source blobs are not a complete distribution, dependency lock, compiler qualification or rights inventory.',
    'Version 0.14.2 is the selected DESCRIPTION declaration; no latest or released-version claim follows.',
    'No R engine, downloaded code, upstream test or sibling repository was executed.',
    'Exact authored examples establish algebraic reference values, not native conformance, identification or calibrated inference.',
    'Complete dependency/distribution rights, native behavior and measured costs remain admission work.',
    'Rendered visual review, mandatory repairs, Q1/Q5 and final proposal acceptance remain open.'
]


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    verify_bindings(read(BASE/'plan-review.json'))
    commit=read(RAW/'exec20_fixest_cutoff_commit.json')[0]
    tree=read(RAW/'exec20_fixest_tree.json')
    assert commit['sha']==PIN and commit['commit']['committer']['date']=='2026-06-26T12:14:19Z'
    assert tree['sha']==commit['commit']['tree']['sha']=='7ef46c3882a5ce9332199ddd741ac15ce4125d93'
    assert not tree['truncated'] and len(tree['tree'])==674
    blobs={r['path']:r['sha'] for r in tree['tree'] if r['type']=='blob'}
    assert not any(re.search(r'(^|/)(license|copying)(\.|$)',p,re.I) for p in blobs)
    paths={'root_0':'DESCRIPTION','root_2':'README.md','root_3':'NEWS.md',
        'tech_0':'R/estimation.R','tech_1':'R/fixest_env.R','tech_2':'R/VCOV.R',
        'tech_3':'R/did.R','tech_4':'man/feols.Rd','tech_5':'man/sunab.Rd',
        'tech_6':'man/ssc.Rd','tech_7':'vignettes/standard_errors.Rmd',
        'tech_8':'vignettes/collinearity.Rmd','tech_9':'.github/workflows/check-standard.yml',
        'test_0':'tests/fixest_tests.R','test_1':'R/methods.R','test_2':'R/onLoad.R'}
    ranges={'root_0':[(1,50)],'root_2':[(1,36)],'root_3':[(1,78)],
        'tech_0':[(1912,1945),(2000,2025),(2187,2225)],'tech_1':[(1778,1830)],
        'tech_2':[(208,215),(280,305),(752,758),(880,932),(1098,1113),(3140,3180)],
        'tech_3':[(60,84),(262,335),(590,622)],'tech_4':[(208,255),(354,366)],
        'tech_5':[(1,100)],'tech_6':[(1,115)],'tech_7':[(1,150)],'tech_8':[(1,140)],
        'tech_9':[(1,60)],'test_0':[(58,163),(208,260),(1333,1413)],
        'test_1':[(4130,4158)],'test_2':[(77,96)]}
    records=[]; extracts=[]
    for key,upstream in paths.items():
        p=RAW/('exec20_fixest_'+key+'.txt');rp=p.with_suffix('.receipt.json')
        data=p.read_bytes();receipt=read(rp)
        url=f'https://raw.githubusercontent.com/lrberge/fixest/{PIN}/{upstream}'
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert receipt['status']=='saved' and receipt['url']==url
        assert receipt['sha256']==core.sha(p) and blobs[upstream]==blob
        lines=data.decode().splitlines();spans=[(a,min(b,len(lines))) for a,b in ranges[key]]
        assert all(1<=a<=b for a,b in spans)
        anchors=[f'lines {a}-{b}' for a,b in spans]
        records.append(dict(source_identity=url,version_date='2026-06-26T12:14:19Z; commit '+PIN,
            git_blob_sha1=blob,local_copy=ref(p,'; '.join(anchors)),receipt=ref(rp,'Original acquisition'),
            accessed_utc=receipt['accessed_utc'],inspected_anchors=anchors,executed=False))
        extracts.append(dict(source=upstream,local_copy=ref(p,'Inspected original'),
            ranges=[dict(start=a,end=b,text='\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,b))) for a,b in spans]))
    assert len(records)==16
    license_path=RAW/'exec20_fixest_gpl3.txt';license_receipt=read(license_path.with_suffix('.receipt.json'))
    assert license_receipt['status']=='saved' and license_receipt['sha256']==core.sha(license_path)
    assert '29 June 2007' in license_path.read_text()
    description=(RAW/'exec20_fixest_root_0.txt').read_text()
    assert 'Version: 0.14.2' in description and 'License: GPL-3' in description
    dependencies=re.search(r'^Imports: (.+)$',description,re.M).group(1).split(', ')
    identity=dict(repository='lrberge/fixest',selected_commit=PIN,commit_date=commit['commit']['committer']['date'],
        cutoff='2026-10-07 Asia/Shanghai',tree_entries=674,authenticated_blobs=16,
        declared_version='0.14.2',release_version_verified=False,current_support_verified=False,
        evidence=[ref(RAW/n,'Commit/tree identity and original receipt') for n in
            ['exec20_fixest_cutoff_commit.json','exec20_fixest_cutoff_commit.receipt.json',
             'exec20_fixest_tree.json','exec20_fixest_tree.receipt.json']])
    write(BASE/'identity-review.json',identity)
    write(BASE/'inspected-extracts.json',dict(records=extracts,native_execution=False))
    claims=[
        'DESCRIPTION declares R>=3.5.0, Rcpp linking, listed imports and GPL-3 at the selected commit; NEWS and check workflow document maintenance intentions, not passing runs.',
        'The selected feols documentation describes recursive singleton/perfect-fit removal and observation/collinearity diagnostics; finite negative weights error, zero weights are removed and missing weights join sample selection.',
        'The selected covariance path reads session defaults; onLoad sets all covariance defaults to iid. Fixed-effect syntax therefore does not itself specify clustered errors.',
        'ssc separates K and G scaling from t degrees of freedom, with none/full/nonnested FE counting and optional exact counting. Upstream tests specify irregular-FE examples but were not run here.',
        'vcov_fix defaults TRUE. The inspected executable branch assigns a repaired covariance only inside if(vcov_fix); its adjacent always-fix comment is inconsistent. The warning threshold is 1e-8.',
        'sunab calendar cohorts absent from supplied period support are classified as never treated. Its own documentation warns about already-treated cohorts outside the observed range.',
        'aggregate.fixest forms sample-share or weighted-share coefficient averages and computes variance using the full coefficient covariance quadratic form.'
    ]
    source=dict(integrated_citation_key='exec20_fixest_source',kind='software_primary_sources',
        title='fixest: pinned estimation, sample selection, covariance and event-time source review',
        author='Laurent Berge and fixest contributors',year=2026,source_identity='https://github.com/lrberge/fixest',
        version_date='2026-06-26T12:14:19Z; commit '+PIN,selected_commit=PIN,
        local_copy=ref(RAW/'exec20_fixest_root_0.txt','DESCRIPTION: selected identity and declaration'),
        records=records,identity_evidence=identity['evidence'],
        license_text=dict(source_identity=license_receipt['url'],version_date='GPL version 3, 29 June 2007',
            local_copy=ref(license_path,'Standard license text named by DESCRIPTION; external to repository tree'),
            receipt=ref(license_path.with_suffix('.receipt.json'),'Original GPL text acquisition'),
            inspected_anchors=['Preamble; sections 0-6; no distribution-wide conclusion']),
        inspected_anchors=[dict(anchor=c,inspection='Pinned primary code, documentation or test specification') for c in claims],
        supported_claims=claims,limitations=LIMITS,software_executed=False)
    reference=dict(integrated_citation_key='exec20_fixest_reference',kind='project_authored_exact_reference',
        title='Exact bank-panel projection, covariance and aggregation references',
        author='Causal banking proposal project',year=2026,
        source_identity='tools/fixest_panel_reference_20261020.py',version_date='2026-10-20',
        local_copy=ref(ROOT/'tools/fixest_panel_reference_20261020.py','fit and calculate: exact algebra and contrasts'),
        inspected_anchors=[dict(anchor='fit(); calculate()',inspection='Exact rational calculations and invariance checks')],
        supported_claims=['Within and explicit-dummy slopes are 4; raw cluster variance is 8/9, with explicit K=1 and K=4 corrections 4/3 and 10/3. An absorbed treatment is undefined. Aggregation gives effect7/2, variance51/16, and net margin-1/2 versus1 under changed weights.'],
        limitations=LIMITS)
    audit=dict(sources=[source,reference],records=records,cutoff='2026-10-07',limitations=LIMITS,supported_claims=claims)
    write(BASE/'source-audit.json',audit);write(BASE/'exact-results.json',exact.calculate())
    omissions=dict(unread_or_unqualified=[
        'Complete C++/R distribution, compiled numerical behavior, resolved dependencies and transitive notices.',
        'Native IV, GLM, multiway covariance, nonlinear prediction and large-panel performance.',
        'Independent theory review of the linked 2026 fixed-effects paper; no citation or technical claim is made from its metadata.',
        'Actual CRAN release artifacts, latest support and observed check results.'],
        preserved_failures=[ref(RAW/'head_fixest.receipt.json','Inherited HEAD403'),
            ref(RAW/'exec20_fixest_root_1.receipt.json','LICENSE404; declaration remains in DESCRIPTION')],
        scope='Omissions limit affected claims only; they do not block other proposal work.')
    write(BASE/'omissions-register.json',omissions)
    write(BASE/'acquisition-review.json',dict(status='pass_for_selected_sources',authenticated_blobs=16,
        evidence=records,license_declaration='GPL-3 in pinned DESCRIPTION',
        separate_standard_license=ref(license_path,'External standard text; not a missing repository blob replacement'),
        omissions=ref(BASE/'omissions-register.json','Preserved failures and unavailable qualification')))
    contract=dict(status='proposed_not_implemented',preferred_profile='Pinned original fixest behind a typed R worker, initially linear fixed-effect estimation',
        requirements=[
            'Bind request and row IDs, data snapshot, units, formula design, categorical levels, panel calendar, contrasts and finite numeric values.',
            'Prevalidate weights: reject negatives/nonfinite/missing by declared policy; explicitly authorize any zero removal. Record every row mask and reason.',
            'Record recursive singleton/perfect-fit removal, collinear columns and any rank/convergence diagnostic; an absorbed treatment is unavailable, never zero.',
            'Set vcov, cluster keys, SSC and t degrees of freedom explicitly in a fresh worker; freeze session options, thread count and numeric environment.',
            'Preserve the covariance before and after any PSD/PD repair or refuse unobservable repair status. Warnings alone cannot reveal changes below the source threshold.',
            'Return coefficient names, complete covariance and sample IDs together. Distinguish estimate, missing target, numerical error, invalid input, interrupted job and unsupported model.',
            'Validate treatment timing independently of sunab inference: separate never treated from treated before observation, validate references, bins, support and weights.',
            'Freeze cohort aggregation target; use the full covariance quadratic form and retain component coefficients and shares.',
            'Expose the same typed request/result and refusals in library, CLI and MCP. Allow approved formula structures, not arbitrary agent-generated R evaluation.',
            'Bind actual distribution and dependency rights, then compare native output against exact dummy/projection, weighting, absorbed-treatment, covariance, aggregation and failure oracles before admission.'
        ],native_conformance_passed=False,rights_review_complete=False)
    write(BASE/'conversion-contract.json',contract)
    evidence=[ref(BASE/n,'Reviewed bounded fixest proposal evidence') for n in
        ['plan-review.json','identity-review.json','source-audit.json','inspected-extracts.json',
         'acquisition-review.json','omissions-register.json','exact-results.json','conversion-contract.json']]
    evidence.append(ref(Path(__file__),'Exact author review construction'))
    decision=dict(operation_id=OP,status='pass',decision='defer',
        decision_scope='Complete conditional proposal selection of original fixest for fixed-effect panels; defer executable admission.',
        preferred_proposal_route=contract['preferred_profile'],integration_allowed=False,capabilities=[],
        runtime_qualification=False,deployment_allowed=False,original_gap_qualification=False,
        identity=dict(canonical_repository='lrberge/fixest',entry='inherited_fixest',selected_commit=PIN,
            aliases=['fixest R package','feols entrypoint'],
            alias_boundary='feols, feglm and femlm are model surfaces in fixest; pyfixest is a separate implementation, not an admitted alias.'),
        license=dict(declaration='GPL-3',evidence=source['license_text'],
            complete_distribution_or_transitive_rights=False,
            boundary='A separate worker is an engineering boundary, not a finding about licensing obligations.'),
        dependencies=dict(R='>=3.5.0',LinkingTo='Rcpp',imports=dependencies,resolved_environment=False),maintenance=identity,
        target_and_uncertainty='Explicit fixed-effect projection/IV or event-time target with declared identifying assumptions; inference depends on sample, clusters, SSC and support.',
        reason=['Source-supported conditional proposal route preserves original model and uncertainty semantics.',
            'A new port has no demonstrated platform or cost justification at proposal stage.',
            'Native conformance, full packaging and rights are separate admission requirements.'],
        alternatives=[dict(route='Explicit dummy regression and rational reference',disposition='retain_reference',reason='Transparent small-case coefficient, rank and covariance checks; no large-scale claim.'),
            dict(route='pyfixest',disposition='separate_candidate',reason='Independent implementation requires its own source, license and native conformance; no equivalence inferred.'),
            dict(route='Port selected C++ routines',disposition='defer',reason='Must recreate R design, sample selection, df and failure semantics; no measured benefit supports duplication.'),
            dict(route='Uncontrolled formula execution in an agent tool',disposition='reject_for_initial_profile',reason='Cannot ensure reviewed model, reproducibility or a bounded evaluation contract.')],
        costs_to_measure=['R worker and compilation setup','Dependency/rights upkeep','Row/design serialization','Memory and thread management',
            'Covariance and exact rank calculation','Upgrade conformance and diagnostics'],measured_prices_or_bank_ROI=False,
        owner_obligations=dict(scientific_owner='Own causal target, information, assignment and dependence assumptions.',
            data_owner='Own identities, calendars, weights and missingness.',
            adapter_maintainer='Own pinned environment, conversions, diagnostics, native comparison and API parity.',
            rights_operator_owner='Review actual distributions, dependency terms and deployment obligations.'),
        revisit_trigger='Before admission obtain complete pinned distribution and environment, review rights, and qualify sample masks, rank, covariance options/repair, cohort support, aggregation and failures; reopen on version, platform or target change.',
        evidence=evidence,limitations=LIMITS,reviewer=REVIEWER,bank_inputs_required_for_next_step=False)
    write(OUTPUT,decision)
    write(BASE/'review.json',dict(status='pass_for_scoped_proposal_decision',reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT,'Conditional proposal choice, no executable admission'),evidence=evidence,findings=claims,limitations=LIMITS))
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    findings=['Sixteen authenticated blobs bind original engine identity, license declaration, dependency declarations and historical maintenance evidence.',
        'Target, covariance, alternatives, sample/timing failures, proposed costs, responsible roles and revisit trigger are explicit.',
        'Completed bounded defer decision grants no integration capability; exact authored reference and proposed conversion contract do not assert native qualification.']
    receipt.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,
        capabilities=[],outputs=[ref(OUTPUT,'Contracted fixest decision')],limitations=LIMITS,nonexecution_reason='',
        revisit_trigger=decision['revisit_trigger'],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Author review')]) for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt);verify_bindings([audit,decision,receipt])
    print(json.dumps(dict(operation=OP,outcome='pass',original_blobs=16,integration_allowed=False,native_execution=False)))


if __name__=='__main__':main()
