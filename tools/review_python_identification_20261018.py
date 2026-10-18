#!/usr/bin/env python3
"""Bounded four-family review using authentic inert sources and exact references."""
import copy
import hashlib
import json
from pathlib import Path
import zipfile

import run_program_reviews_v2 as extension
import python_counterfactual_reference_20261018 as coupling
import python_identification_oracles_20261013 as inherited
from publish_latent_r_review_v2_20261013 import verify_bindings

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-18/python-identification-v1'
INERT = BASE/'ananke-inert-source'
PRIOR = ROOT/'docs/program/execution/2026-10-18/graph-panel-reader-v2/reader/source-audit.json'
OP = 'SW.CELL.identification_counterfactual.Python'
OUTPUT = ROOT/('docs/program/comprehensive-v14/work/'+OP+'/coverage-review.json')
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Four inherited families are compared from selected pinned sources; this is not a complete Python-market or arbitrary counterfactual/bounds survey.',
    'No upstream package was installed, imported or executed. Static findings and exact authored references do not qualify native behavior, sampling inference or adapters.',
    'Ananke 0.5.0 is a selected 2023 release, not a claim about the newest release or current support. The other packages retain their inspected pre-cutoff pins.',
    'GCM counterfactual paths, ID*/IDC* variants and Python partial-identification alternatives remain unreviewed in this attempt; absence is not inferred.',
    'Dependency declarations conflict across the selected Ananke/DoWhy/pgmpy revisions. Separate environments are a proposed design, not a resolved or tested deployment.',
    'Apache text is present in two archive files, but metadata has a conflicting proprietary classifier. Exact distribution and transitive rights remain a review obligation.',
    'The retrospective dollar example uses stipulated values; it is neither a prospective decision rule nor bank ROI.',
    'New findings await a preserving manuscript successor. Visual, independent and final proposal acceptance remain open.',
]


def read(path):
    return json.loads(path.read_text())


def ref(path, anchor):
    return dict(path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest(), anchor=anchor)


def write(path, value):
    assert not path.exists(), str(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def source(member, ranges, claims, title):
    path = INERT/member
    lines = path.read_text().splitlines()
    anchors = []
    for start, end, finding in ranges:
        assert 1 <= start <= end <= len(lines), (member, start, end)
        anchors.append(dict(lines=[start,end], text_sha256=hashlib.sha256('\n'.join(lines[start-1:end]).encode()).hexdigest(), finding=finding))
    acq = read(BASE/'acquisition.json')
    return dict(title=title, kind='software_primary_source', author='Ananke community', year=2023,
        source_identity=acq['source_identity']+'#'+member, version_date='ananke-causal 0.5.0; uploaded '+acq['declared_upload'],
        accessed_utc=acq['accessed_utc'], cutoff='2026-10-07',
        local_copy=ref(path, 'Verbatim authenticated archive member, never imported'),
        archive=ref(BASE/'ananke_causal-0.5.0-py3-none-any.whl', 'PyPI SHA-256 matches saved release identity'),
        acquisition=ref(BASE/'acquisition.json', 'Bounded acquisition and identity'),
        inspected_anchors=anchors, supported_claims=claims, limitations=LIMITS[1:3])


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    verify_bindings(read(BASE/'plan-review.json'))
    extraction = read(BASE/'extraction.json')
    verify_bindings(extraction)
    with zipfile.ZipFile(ROOT/extraction['archive']['path']) as z:
        for item in extraction['records']:
            assert z.read(item['member']) == (ROOT/item['local_copy']['path']).read_bytes()
    prior = read(PRIOR)
    keys = ['exec13_dowhy','exec13_dowhy_license','exec13_dowhy_project',
            'exec13_pgmpy_reuse_primary','exec13_y0_api','exec13_y0_id','exec13_y0_idc',
            'exec13_y0_graph','exec13_y0_dsl','exec13_y0_metadata','exec13_y0_license',
            'exec13_y0_rule2','exec13_y0_separation','exec13_y0_oracles']
    mapping = {s['integrated_citation_key']: s for s in prior['sources']}
    selected = [copy.deepcopy(mapping[k]) for k in keys]
    for record in selected:
        verify_bindings(record)
    sources = [
        source('ananke/identification/one_line.py',[(37,59,'Intervention fixation and outcome ancestors'),
            (90,140,'District fixability; Boolean result; functional string and stdout'),
            (250,262,'Ancestral experiment precondition raises NotIdentifiedError'),
            (343,367,'GID experiment conformance uses the same exception'),
            (378,427,'Checks supplied pair of models; not automatic counterfactual witness construction')],
            ['OneLineID performs district-fixability identification on the supplied graph and query.',
             'functional() is a string plus fixing-order diagnostics, not a portable typed numerical estimator.',
             'The same exception can indicate invalid experimental preconditions; adapters require explicit preflight and method-specific error interpretation.',
             'Supplied-model witness comparison is distinct from constructing witnesses or arbitrary cross-world identification.'],
            'Ananke one-line identification and supplied-model witnesses'),
        source('ananke/identification/oracle.py',[(18,49,'Supplied true-model intervention and conditional normalization')],
            ['The oracle explicitly bypasses identification; conditional normalization in a supplied model is not IDC from observed data.'],
            'Ananke supplied-model intervention oracle'),
        source('ananke/identification/missing_id.py',[(6,47,'Missing full-law query using R_/X_ convention and colluding paths')],
            ['This selected routine checks missing-data full-law identification under its graph naming convention; it is not a general counterfactual service.'],
            'Ananke missing-data identification scope'),
        source('ananke/estimation/counterfactual_mean.py',[(1,46,'ACE target and estimator dispatch'),(54,123,'a-/p-/nested-fixability selection')],
            ['CausalEffect targets an average E[Y(1)-Y(0)] for one named treatment/outcome and distinguishes fixability strategies.',
             'An estimator name or counterfactual filename does not establish an arbitrary cross-world joint or conditional query.'],
            'Ananke average-effect estimation interface'),
        source('ananke/graphs/sg.py',[(13,41,'Constructor graph preconditions'),(55,99,'Cycle check and correctness TODO')],
            ['Graph preconditions raise TypeError. Independent input validation remains proposed; a source TODO is not an observed runtime failure.'],
            'Ananke segregated-graph validation'),
        source('ananke_causal-0.5.0.dist-info/METADATA',[(1,33,'Identity, date-independent dependency declarations and conflicting license classifiers')],
            ['Python>=3.9,<4; numpy>=1.23,<2; pandas>=1.4.3,<2; pgmpy>=0.1.21,<0.2; statsmodels>=0.13.2,<0.14.',
             'Apache2.0 and Other/Proprietary classifiers coexist. Sympy is imported by one_line.py but is not explicitly declared here; transitive provision is unverified.'],
            'Ananke 0.5.0 distribution identity and dependencies'),
        source('LICENSE',[(1,5,'Apache2.0 text'),(66,121,'Grant and notice/change/attribution conditions'),(178,201,'Unfilled example appendix notice')],
            ['Two byte-identical Apache2.0 license files are present; retain the metadata conflict and dependency rights as unresolved distribution questions.'],
            'Ananke archive license text'),
    ]
    assert (INERT/'LICENSE').read_bytes() == (INERT/'ananke_causal-0.5.0.dist-info/LICENSE').read_bytes()
    exact = dict(frontdoor=inherited.frontdoor(), bow=inherited.bow(),
                 collider=inherited.collider(), coupling=coupling.calculate())
    old = read(ROOT/'docs/program/execution/2026-10-13/python-integration/oracle-results.json')
    assert exact['frontdoor']==old['frontdoor'] and exact['bow']==old['bow']
    assert exact['collider']==old['bidirected_collider']
    candidates = [
        dict(family='DoWhy',aliases=['dowhy','PyWhy/DoWhy','py-why/dowhy'],
             pin='b06369ed4a01a54c9d6422a24f103626fbcaec19',scope='Explicit-graph model/identify/estimate boundary; selected ID versus AutoIdentifier dispatch.',
             route='Preferred optional prototype identification route; executable admission deferred.',
             gaps='GCM individual/counterfactual paths not reviewed here; flag propagation and returned estimand must be checked; lock, runtime and transitive rights open.'),
        dict(family='pgmpy',aliases=['pgmpy','pgmpy.identification','Adjustment'],
             pin='1f6296fc2606eb479f1f1b9fbfdd9c41aa7ad312',scope='Selected single exposure/outcome graphical adjustment and independently validated candidate sets.',
             route='Restricted candidate generation; independent descendant/backdoor checks before use; no arbitrary ID claim.',
             gaps='minimal_variance branch raises NotImplementedError; permissive adjustment validation is source-traced; dependency/runtime review pending.'),
        dict(family='y0',aliases=['y0','y0-causal-inference','identify_outcomes'],
             pin='cc6644d3b470a1ab2a1eb9da4f0fdb0c843f5d3a',scope='Symbolic ADMG ID; native IDC depends on inspected separation path.',
             route='Candidate unconditional ID and restricted typed expression conversion. Native conditional path remains disabled pending repair; joint ID plus normalization is proposed where identifiable and denominator positive.',
             gaps='Counterfactual DSL representation does not prove general ID*/IDC*. Joint-ID fallback is sufficient only in its declared regime and is not a completeness claim.'),
        dict(family='Ananke',aliases=['ananke-causal','ananke','causal/ananke','OneLineID','OneLineAID','OneLineGID'],
             pin='0.5.0 uploaded 2023-12-05',scope='ADMG intervention identification, experimental extensions, missing-full-law test, true-model oracle and ACE interfaces are distinct.',
             route='Source reference and candidate isolated optional comparator; defer executable adoption and source port.',
             gaps='String expression conversion; method-specific failures; independent graph preflight; older incompatible dependencies; classifier conflict; no arbitrary counterfactual/bounds evidence.')
    ]
    omissions = [
        dict(id='PY-CF-GCM',target='DoWhy GCM counterfactual APIs',action='Inspect pinned structural-model assumptions, factual-noise abduction, discrete/invertible mechanism restrictions, and same-unit cross-world semantics.',status='unreviewed_scope_not_absence'),
        dict(id='PY-CF-ALGORITHMS',target='Python ID*/IDC* and counterfactual transport implementations',action='Record registry/repository search with cutoff, acquire exact technical originals and query/graph classes; no inference from DSL support.',status='search_and_primary_review_open'),
        dict(id='PY-BOUNDS',target='Python response-function/optimization bounds, including autobounds as an unverified search lead',action='Authenticate identity, selected cutoff source, solver obligations, sharpness and primal/dual certificates; no current capability claim.',status='candidate_identity_and_technical_review_open'),
        dict(id='PY-ANANKE-RIGHTS',target='Ananke selected distribution and dependency rights',action='Resolve conflicting metadata, authentic notices and component scope before distribution; retain existing Apache text.',status='open'),
        dict(id='PY-NATIVE',target='Four native package boundaries',action='After source/design selection, isolate and resolve environments, then execute declared structural reference and error cases; not needed to invent proposal trial results.',status='prototype_stage_deferred'),
    ]
    contract = dict(status='proposed_not_implemented',
        request=['explicit graph class with named nodes, latent status and edge endpoints',
                 'query kind: adjustment, intervention, conditional intervention, cross-world, or bounds',
                 'intervention values, conditioning events, target population, observation clock and assumptions',
                 'available observational/experimental laws and support; exact engine revision'],
        result_variants=['identified_expression','identified_set','nonidentified_under_declared_model',
                         'unknown_or_unsupported','invalid_request','engine_failure'],
        conversion=['Retain empty valid adjustment sets separately from failed searches.',
                    'Never use eval on Ananke functional strings; design a named-variable AST with sum/product/fixing structure and preserve original diagnostics.',
                    'Reject cycles, dangling nodes, duplicate IDs, unresolved PAG/CPDAG or experimental preconditions outside the chosen algorithm.',
                    'Do not map every NotIdentifiedError, None, timeout or missing result to proved nonidentification.',
                    'Separate means, same-world conditional distributions and individual cross-world queries; a supplied true model answers a different information problem.',
                    'Conditional joint-normalization fallback requires an identified joint and positive denominator; it can leave identifiable conditional queries unresolved.',
                    'For bounds carry feasible-set assumptions, attained endpoints or solver certificates; no uncertainty interval is manufactured from an identification interval.'],
        environment=dict(ananke_numpy='>=1.23,<2',dowhy_numpy='>2',pgmpy_numpy='>=2',
                         ananke_statsmodels='>=0.13.2,<0.14',dowhy_statsmodels='>=0.14',pgmpy_statsmodels='>=0.14.5',
                         conclusion='Declared intervals have empty intersections; selected distributions cannot share one satisfying environment unchanged.',
                         proposed_route='Separate pinned processes with a versioned JSON semantic contract; no claim that this resolves scientific or rights issues.'),
        port_decision='Do not port initially: symbolic semantics, graph rules and maintenance costs transfer to this project without a measured deployment need.',
        banking='A lending/servicing intervention can have identified average recovery while the same customer counterfactual remains ambiguous.')
    write(BASE/'exact-reference.json', exact)
    write(BASE/'source-audit.json',dict(status='pass_for_scoped_primary_claims',reviewer=REVIEWER,
         cutoff='2026-10-07', sources=sources, inherited_sources=selected,
         archive_verification=dict(files=len(extraction['records']),all_bytes_match=True), limitations=LIMITS))
    write(BASE/'candidate-register.json',dict(candidates=candidates,cutoff='2026-10-07',market_saturation=False,
         inherited=ref(ROOT/'docs/program/gap-execution-v13_1/work/SW01/coverage-matrix.json','identification_counterfactual::Python'),
         stopping_rule='Four inherited families, all40 extracted inert members authenticated, seven technical/identity/rights files inspected in this continuation, and previously pinned source reviews retained. No exhaustive market claim.',
         search_limits='An additional server search for selected Ananke and autobounds identity returned no source text in this continuation; it supplies no technical evidence or absence conclusion.'))
    write(BASE/'conversion-contract.json',contract)
    write(BASE/'omissions-register.json',dict(items=omissions,independent_work_may_continue=True))
    names=['plan.md','plan-review.json','acquisition.json','acquisition-failure-1.json',
           'extraction.json','source-audit.json','candidate-register.json','conversion-contract.json',
           'omissions-register.json','exact-reference.json']
    evidence=[ref(BASE/n,'Preserved inspection, exact reference or proposed boundary') for n in names]
    evidence += [ref(Path(__file__),'Bounded review implementation'),
                 ref(ROOT/'tools/python_counterfactual_reference_20261018.py','Exact coupling proof and rational enumeration')]
    findings=['Equal randomized observed laws and both interventional means leave conditional recovery0 versus1; sharp benefit share [0,1/2] and retrospective conditional net[-50,350]USD.',
              'Intervention ID, invalid experimental preconditions, true-model oracles, missing-full-law tests and average-effect estimation require distinct service contracts.',
              'Selected dependency intervals conflict; separate environments are proposed, not tested.',
              'Four inherited families have bounded evidence, but unreviewed GCM/cross-world/bounds alternatives prevent full cell acceptance.']
    write(BASE/'author-review.json',dict(status='pass_for_scoped_inconclusive_disposition',reviewer=REVIEWER,
         findings=findings,evidence=evidence,issues=[],limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
    write(OUTPUT,dict(operation_id=OP,status='inconclusive',scope='Four-family Python identification and counterfactual source comparison',
         reviewer=REVIEWER,candidates=candidates,evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False))
    run=extension.base
    state=run.core.read(ROOT,run.core.STATE)
    graph,merged,stages=extension.combined(ROOT,state)
    node=run.ledger.operation(graph,OP)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',scope='Bounded source review, exact mathematics and proposed semantic boundary; wider coverage remains open.',
        reviewer=REVIEWER,limitations=LIMITS,outputs=[ref(OUTPUT,'Contracted coverage output')],capabilities=[],original_gap_qualification=False,
        revisit_trigger='Complete the specific GCM, cross-world and bounds source searches/reviews; retain native qualification as later prototype work; integrate the reviewed mathematical and source delta.')
    verdicts=[('inconclusive','Four inherited families and aliases are retained with cutoff and bounded search; wider counterfactual/bounds coverage remains open.'),
              ('pass','Positive technical claims bind to authentic pinned primary bytes and inspected anchors; all40 extracted files match the authenticated archive.'),
              ('inconclusive','Omissions and concrete follow-ups are recorded without an absence claim or a waiver of essential missing sources.')]
    receipt['criteria']=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(verdicts)]
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps(dict(status='inconclusive',candidates=4,new_primary_records=7,
        authenticated_members=40,coupling_bounds=['0','1'],native_execution=False)))


if __name__=='__main__':
    main()
