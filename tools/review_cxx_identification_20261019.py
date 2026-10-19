#!/usr/bin/env python3
"""Bounded historical native identification/counterfactual source review."""
import hashlib
import json
from pathlib import Path
import run_program_reviews_v2 as extension
import cxx_identification_reference_20261019 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
run=extension.base;core=run.core;ROOT=core.ROOT;RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-19/cxx-identification-v1'
OP='SW.CELL.identification_counterfactual.Cxx'
OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    head=read(RAW/'v12_sw_cutoff_commit_agrum.json')[0]
    pin=head['sha'];date=head['commit']['committer']['date']
    assert pin=='2ec71906f4108684c5cfb96d1d44f2925e16a32e' and date=='2026-10-06T17:21:03Z'
    tree=read(RAW/'v12_sw2_tree_agrum.json');assert tree['sha']==pin and not tree['truncated']
    blobs={r['path']:r['sha'] for r in tree['tree'] if r['type']=='blob'}
    extracts=read(BASE/'inspected-extracts.json')['records'];records=[]
    for row,ex in zip(read(BASE/'acquisition-plan.json'),extracts):
        p=RAW/(row['id']+'.txt');rp=RAW/(row['id']+'.receipt.json');receipt=read(rp);data=p.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert receipt['url']==row['url'] and receipt['status']=='saved'
        assert receipt['sha256']==ex['sha256']==core.sha(p) and blob==blobs[row['upstream_path']]
        records.append(dict(source_identity=row['url'],version_date=date+'; '+pin,
            local_copy=ref(p,'; '.join(f"lines {s['first']}-{s['last']}" for s in ex['spans'])),
            receipt=ref(rp,'Original bounded HTTPS acquisition'),git_blob_sha1=blob,
            inspected_anchors=[dict(first=s['first'],last=s['last']) for s in ex['spans']],executed=False))
    claims=[
        'Native ID code includes ancestor restriction, intervention augmentation, latent co-child c-components, kernel factorization and hedge exception branches. Static inspection does not prove completeness or correctness.',
        'Conditional-query promotion constructs one graph with incoming intervention edges and outgoing edges from every conditioning variable removed, then tests candidates in that graph. This multi-conditioning path needs theorem-level and native comparison; no defect is asserted from comments alone.',
        'When an accumulated kernel exists, the first topological factor is constructed as ASTjointProba rather than the computed numerator. Reachability and semantic equivalence remain explicit conformance obligations, not an established bug.',
        'CausalFormula isIdentified tests whether an AST root exists; eval separately requires an observational BN. ASTdiv delegates directly to tensor division; support-zero behavior of the underlying tensor remains uninspected.',
        'The counterfactual builder reconstructs a model from the observational BN, selects parentless nodes excluding intervention and latent nodes, and fills each root CPT with its individual posterior given the profile.',
        'The selected counterfactual code has no joint-posterior root factor in this replacement path. Conditioning can induce root dependence; exact authored examples show why separate marginal replacement is insufficient generally.',
        'Reconstruction from the observational BN does not copy the original extra latent descriptors or spurious-arc declarations; preserve an explicit native graph-identity trial.',
        'The Python convenience wrapper retains its model on the returned tensor and returns None when the formula is not identified; these selected files do not settle all exception and lifetime conversions.',
        'Inspected native tests include backdoor/frontdoor manual parity, forced direct-do-calculus comparisons, a hedge evaluation exception, ID/IDC smoke tests and a salary counterfactual fixture. They were not executed and do not test every coupled-root scenario.'
    ]
    limits=[
        'Only selected aGrUM and inherited R-backed dosearch originals are inspected; the C++ candidate universe is not saturated.',
        'No installed native engine, Python wrapper, compiler, upstream test suite or third-party dependency is executed or qualified.',
        'Source labels ID/IDC and counterfactual are not proofs of their full mathematical or scientific scope.',
        'General hidden-confounder identification, arbitrary counterfactual coupling and partial-identification completeness remain unqualified.',
        'No independent review, bank evidence, actual prices, economic benefit or distribution-rights approval.',
        'The literature cutoff remains7October2026; current web discovery returned no usable text.'
    ]
    inherited=ROOT/'docs/program/execution/2026-10-18/r-identification/source-audit.json'
    inherited_audit=read(inherited);verify_bindings(inherited_audit)
    dosearch=next(s for s in inherited_audit['sources'] if s['integrated_citation_key']=='exec18_rid_dosearch')
    source=dict(integrated_citation_key='exec19_cxx_identification_source',kind='software_primary_sources',
        title='aGrUM3.2.0 native identification, counterfactual and Python-wrapper selected source contracts',
        author='aGrUM authors and contributors',year=2026,source_identity='https://github.com/agrumery/aGrUM',
        version_date='3.2.0; '+date+'; '+pin,local_copy=ref(RAW/'exec19_cxx_id_agrum_1.txt','Native ID and conditional-query recursion'),
        records=records,identity_evidence=[ref(RAW/'v12_sw_cutoff_commit_agrum.json','Pre-cutoff commit identity'),ref(RAW/'v12_sw2_tree_agrum.json','Complete inherited tree; selected blob authentication'),ref(RAW/'v12_sw2_metadata_agrum_1.txt','Version3.2.0'),ref(RAW/'v12_sw2_metadata_agrum_2.txt','CMake3.18 and C++20 declarations'),ref(RAW/'v12_sw2_metadata_agrum_3.txt','Root LGPL3-or-later OR MIT declaration')],
        inspected_anchors=[dict(anchor=c,inspection='Selected primary source and test contract') for c in claims],supported_claims=claims,limitations=limits)
    reference=dict(integrated_citation_key='exec19_cxx_identification_reference',kind='project_authored_exact_reference',
        title='Exact counterfactual coupling, posterior-factorization and lending nonidentification examples',
        author='Causal banking proposal project',year=2026,source_identity='tools/cxx_identification_reference_20261019.py',version_date='2026-10-19',
        local_copy=ref(ROOT/'tools/cxx_identification_reference_20261019.py','calculate(): finite rational enumeration'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Executed exact rational enumeration')],
        supported_claims=['Stable/switch worlds share observed and intervention marginals but profile-specific counterfactuals are1and0.','Posterior root equality has probability1; multiplying marginal roots produces1/2.','Assumed100USD success payoff less20USD cost produces80,-20and30USD under the three respective answers.'],limitations=limits[-3:]+['Authored finite models; no native execution.'])
    audit=dict(sources=[source,reference],records=records,cutoff='2026-10-07',
        inherited_alternative=ref(inherited,'Pinned R/C++ dosearch source, metadata and genuine paper audit'),
        inherited_alternative_citation=dosearch['integrated_citation_key'],limitations=limits)
    write(BASE/'source-audit.json',audit)
    assert read(BASE/'exact-results.json')==exact.calculate()
    contract=dict(status='proposed_not_implemented',integration_allowed=False,requirements=[
        'Separate symbolic identified, certified nonidentified, search unknown/timeout, unsupported graph/query, malformed input and unavailable/invalid numerics.',
        'Persist query, intervention/evidence clocks, graph class, latent descriptors, domain mapping, support and observational or experimental input law.',
        'Preserve structural functions and joint abduction over exogenous variables for a counterfactual; otherwise expose admissible coupling/set or refuse.',
        'Compare direct ID and shortcut formulas, multivariable conditional promotion, nested kernels, zero denominators, hedge/unsupported paths and wrapper lifetimes.',
        'Run a deterministic coupled-root fixture against exact enumeration; preserve the discrepancy rather than inserting independent roots as a silent repair.',
        'For dosearch retain Rcpp/environment, rule set, input distributions, timeout/completion status and proof trace; do not call an empty search result a theorem.',
        'Authenticate native build/wrapper artifacts and reconcile transitive rights before executable admission.'])
    write(BASE/'conversion-contract.json',contract)
    candidates=[dict(name='aGrUM/pyAgrum',aliases=['aGrUM','agrum','pyAgrum','pyagrum'],status='selected_native_and_wrapper_sources_inspected',route='Retain as conditional symbolic comparator; defer executable admission pending conformance.'),
        dict(name='dosearch',aliases=['do-search','Rcpp native search'],status='inherited_primary_reinspected',route='Compare native search through its supported R boundary first; a stand-alone C++ port is a separate engineering and rights decision.'),
        dict(name='Other native identification and partial-identification engines',aliases=['C++ identification','C++ counterfactual','native partial identification'],status='unresolved_candidates',route='Acquire matched dated primary algorithms; generic Bayesian inference or optimization is not an identification certificate.')]
    omissions=dict(status='open',candidates=candidates,absence_claim=False,
        remaining=['Original ID/IDC proof and graph restrictions matched line-by-line to this implementation','Full multi-conditioning, accumulated-kernel and zero-support qualification','Joint abduction and cross-world coupling interface','Native/Python exception and lifetime conversion','Other C++ candidates and partial-identification solver contracts','Transitive build/license inventory'],
        stopping_rule=read(BASE/'plan-review.json')['stopping_rule'],native_execution=False)
    write(BASE/'omissions-register.json',omissions)
    evidence=[ref(BASE/n,'Reviewed bounded evidence') for n in ['plan-review.json','authenticated-files.json','source-audit.json','inspected-extracts.json','exact-results.json','conversion-contract.json','omissions-register.json']]+[ref(Path(__file__),'Author source authentication and review')]
    findings=claims+['The inherited dosearch search loop can stop at its time limit while its result uses target-found as the identifiable flag; retained timeout versus complete-search distinction remains necessary.']
    out=dict(operation_id=OP,status='inconclusive',reviewer=REVIEWER,scope='Pinned C++ identification/counterfactual source and boundary review, with Rcpp search alternative',cutoff='2026-10-07',candidates=candidates,claims=findings,evidence=evidence,limitations=limits,integration_allowed=False,capabilities=[],revisit_trigger='Inspect matched original proofs and other native candidates; implement and run typed-status, kernel, joint-posterior and wrapper conformance protocols before admission.')
    write(OUTPUT,out);write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,output=ref(OUTPUT,'Contracted native review'),evidence=evidence,findings=findings,limitations=limits))
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    criteria=[('inconclusive','aGrUM and R-backed dosearch are retained; complete native candidate coverage and proof alignment remain open.'),('pass','Twelve new pinned sources authenticated, inherited alternative bound, claims anchored and rational examples reproduced.'),('pass','Unknown, source failure and nonidentification remain distinct; omitted proofs and engines remain explicit without waiver.')]
    receipt.update(outcome='inconclusive',execution='performed',scope=out['scope'],reviewer=REVIEWER,capabilities=[],outputs=[ref(OUTPUT,'Bounded native identification review')],limitations=limits,nonexecution_reason='',revisit_trigger=out['revisit_trigger'],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence+[ref(BASE/'review.json','Author review')]) for i,(v,f) in enumerate(criteria)])
    write(BASE/'operation-receipt.json',receipt);verify_bindings([audit,out,receipt])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',new_primary_files=len(records),exact_reference='pass',native_execution=False)))

if __name__=='__main__':main()
