#!/usr/bin/env python3
"""Audit selected Java effect interfaces without executing downloaded software."""
import hashlib
import json
from pathlib import Path

import java_effect_reference_20261020 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
core=run.core
ROOT=core.ROOT
RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-20/java-effects-v1'
OP='SW.CELL.effects_heterogeneity.Java'
OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Two selected Java profiles do not close Java effect-software coverage; complementary search leads and pagination remain unread.',
 'GitHub searches were acquired after the cutoff and are discovery only; each technical profile uses an authenticated pre-cutoff commit.',
 'The inherited IDA source is unchanged and explicitly reused; new coverage comes from uplift and stability-ranking paths, not double-counting identification work.',
 'No downloaded engine, upstream test, Java compilation, live model or sibling repository was executed.',
 'Static source/document discrepancies identify native reconciliation obligations, not measured runtime failures or established upstream defects.',
 'Source license declarations do not resolve every dependency, distribution, patent, trademark or deployment question.',
 'No causal calibration, dependence correction, native admission, bank return, rendered acceptance or final proposal acceptance is established.'
]
HCLAIMS=[
 'The selected H2O-3 core is Java; gradle.properties declares3.47.0/bleeding_edge. Algorithm and genmodel modules have different dependency sets; a source pin is not a qualified binary.',
 'Selected training validates categorical two-level nonmissing treatment and binomial response; weights, offsets and built-in cross-validation are explicitly rejected. Category domains and positive-event meaning must be bound.',
 'Uplift uses a common split tree with separate treatment/control leaf probabilities, including displayed add-one/add-two smoothing; forest and MOJO scoring return their difference and both probabilities.',
 'Ordinary split candidates use smoothed arm rates; missing-feature branches and the nonsplitting-root fallback have distinct code paths requiring separate qualification.',
 'AUTO resolves to KL; DHistogram dispatches to KLDivergence. Its selected metric expression is p*log2(p/q==0 ? epsilon : q), unlike the documented p*log(p/q). At p=q=1/2 the summed literal expression is-1 versus documented KL0; no native run occurred.',
 'MetricBuilder aggregates predicted uplift into all/treated/control averages labelled ATE/ATT/ATC. It skips missing outcomes, so the averaging population must be specified; these labels alone do not establish causal identification or calibrated uncertainty.',
 'AUUC uses cumulative treated/control counts, qini/lift/gain definitions, quantile thresholds and a frequency-weighted rectangle sum divided by n+1. One-bin NaN is set to zero; other NaN curve entries call interpolation. No overlap is thereby created.',
 'The selected MOJO has three prediction entries; writer and reader both declare1.40. The selected subclasses use different threshold key strings, so superclass/default behavior and full archive roundtrip remain native inspection obligations.',
 'Selected upstream tests assert output names and Java/MOJO prediction comparisons. The inspected depth-zero test only checks that a model exists. None of those tests were run here.'
]
TCLAIMS=[
 'The unchanged IDA source admits continuous data and legal PDAGs, enumerates local parent choices, and computes covariance-based regression slopes. Name-based covariance indexing is explicit.',
 'A selected singular inverse catch returns0; other candidate exceptions are logged and skipped. Typed numerical failure must remain distinct from an actual graph-implied zero effect.',
 'CStaR computes minimum absolute candidate effects for each subsample; {-2,-1/2} gives1/2, not the absolute signed minimum2. This magnitude omits direction and is not a beneficial-treatment estimate.',
 'The selected CStaR defaults to30 half-samples without replacement; a bootstrap option samples half the rows with replacement. These row schemes do not by themselves implement calendar/cluster resampling.',
 'Ranking uses an inclusive threshold at topBracket times number of effects; ties may include more candidates. Selection frequency is computed across subsamples and is not a posterior edge probability or CATE interval.',
 'CStaR writes versioned minimum-absolute-effect caches. Its displayed PCER formula uses the displayed rank as q; neither that formula nor a frequency proves its theoretical assumptions for a bank dataset.',
 'The selected class documentation states that required/forbidden edge knowledge is not respected. The proposed wrapper must preserve or refuse incompatible business constraints.',
 'Selected Tetrad headers declare GPLv3-or-later; distribution-specific dependency and notice review remains open.'
]


def authenticate():
    trees={
        'h2o':read(RAW/'exec20_javaeffects_h2o_tree.json'),
        'tetrad':read(RAW/'exec20_javaeffects_tetrad_root.json')}
    roots={'h2o':'13cf48316c1dc92aa49bcf26389e7687c02af6f9',
           'tetrad':'c6490309e24d368629aa15e98d8bc2e3f7263d47'}
    pins={'h2o':'bcd39665671494f1032824acee0c2a3bdad84104',
          'tetrad':'b89afaf952a4fd647df0d85b08102250106c6764'}
    for k,t in trees.items(): assert t['sha']==roots[k] and not t['truncated']
    # Exact ranges inspected by the author; other acquired bytes are identity/dependency evidence only.
    spans={
     'h2o_source_00':[(1,202)],'h2o_source_01':[(1,30)],
     'h2o_source_03':[(1,98)],'h2o_source_04':[(1,42)],
     'h2o_source_05':[(1,115)],'h2o_source_06':[(27,113),(200,242)],
     'h2o_source_07':[(1,98)],'h2o_source_08':[(1,103)],
     'h2o_source_09':[(1,26)],'h2o_source_10':[(1,23)],'h2o_source_11':[(1,13)],
     'h2o_source_12':[(31,85),(87,228),(355,429),(433,473)],
     'h2o_source_13':[(85,127),(174,210),(250,284)],
     'h2o_source_14':[(80,188),(228,303),(349,400),(425,487)],
     'h2o_source_15':[(1,52)],'h2o_source_16':[(1,43)],
     'h2o_source_17':[(1,68)],'h2o_source_18':[(1,28)],
     'h2o_extra_0':[(1690,1838),(1859,1900)],
     'h2o_extra_1':[(245,263),(648,664)],
     'h2o_extra_2':[(1201,1223),(1245,1258)],
     'h2o_extra_3':[(295,304)],'h2o_extra_4':[(69,79)],
     'tetrad_source_0':[(1,21),(97,126),(166,247),(279,321),(332,391),(404,456)],
     'tetrad_source_1':[(1,118)],'tetrad_source_2':[(1,56),(87,117),(189,199),(330,429),(430,518),(657,723)],
     'tetrad_source_3':[(20,93)]}
    records={'h2o':[],'tetrad':[]};extracts=[]
    for name in ['source-acquisition-manifest.json','dependency-acquisition-manifest.json']:
        for row in read(BASE/name)['requests']:
            if 'upstream_path' not in row:continue
            key='h2o' if '_h2o_' in row['id'] else 'tetrad'
            p=RAW/(row['id']+'.txt');rp=RAW/(row['id']+'.receipt.json')
            receipt=read(rp);data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            entry=next(x for x in trees[key]['tree'] if x['path']==row['upstream_path'])
            assert receipt['status']=='saved' and receipt['sha256']==core.sha(p)
            assert receipt['url']==row['url'] and blob==entry['sha'] and pins[key] in row['url']
            short=row['id'].replace('exec20_javaeffects_','');lines=data.decode().splitlines()
            ranges=[(a,min(b,len(lines))) for a,b in spans.get(short,[])]
            records[key].append(dict(source_identity=row['url'],version_date=pins[key],
                local_copy=ref(p,'Selected primary original'),receipt=ref(rp,'Bounded public acquisition'),
                git_blob_sha1=blob,upstream_path=row['upstream_path'],
                inspected_anchors=[f'lines {a}-{b}' for a,b in ranges],
                inspection_scope='Selected anchors only' if ranges else 'Identity only; no semantic claim',executed=False))
            if ranges:extracts.append(dict(source=row['upstream_path'],local_copy=ref(p,'Inspected original'),
                ranges=[dict(start=a,end=b,text='\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,b))) for a,b in ranges]))
    assert len(records['h2o'])==24 and len(records['tetrad'])==4
    assert (RAW/'exec20_javaeffects_tetrad_source_0.txt').read_bytes()==(RAW/'exec19_java_id_4.txt').read_bytes()
    write(BASE/'inspected-extracts.json',dict(records=extracts,software_executed=False))
    write(BASE/'authenticated-sources.json',dict(status='pass',root_trees=roots,pins=pins,records=records,
        inherited_ida_unchanged=True,native_execution=False))
    return records


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    records=authenticate()
    searches=[];leads={}
    for name in ['exec20_javaeffects_search_uplift','exec20_javaeffects_search_causal',
                 'exec20_javaeffects_search_treatment','exec20_javaeffects_search_uplift_readme',
                 'v12_sw_cell_effects_heterogeneity_java']:
        p=RAW/(name+'.json');rp=RAW/(name+'.receipt.json');j=read(p);rc=read(rp)
        assert rc['sha256']==core.sha(p)
        rows=j.get('items',j.get('results',[]))
        searches.append(dict(source=ref(p,'Discovery metadata only'),receipt=ref(rp,'Query and acquisition date'),
            total=j.get('total_count',j.get('meta',{}).get('count')),returned=len(rows),
            query=rc['url'],cutoff_filtered=False if 'items' in j else True))
        for r in j.get('items',[]):leads[r['full_name']]=dict(name=r['full_name'],url=r['html_url'],
            status='unread_metadata_lead',technical_relevance='not_adjudicated',pre_cutoff_identity='unverified')
    write(BASE/'search-review.json',dict(cutoff='2026-10-07',searches=searches,unread_leads=list(leads.values()),
        search_complete=False,absence_claim=False,browser_open='Pinned primary URL returned no usable browser audit content; original collector bytes provide evidence.',
        stopping_rule='Bounded two-profile primary review, preserving remaining candidates and first-page search remainder.'))
    write(BASE/'plan-review.json',dict(status='pass_to_execute',reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md','Reviewed plan'),ref(BASE/'search-review.json','Unclosed coverage'),
            ref(BASE/'authenticated-sources.json','28 authenticated blobs')],
        checks=['Separate uplift contrasts, target averages, ranking and signed graph effects.',
            'Review documentation against actual selected defaults, helpers and failure branches.',
            'Keep source findings, authored references and native validation separate.',
            'Reuse unchanged IDA without duplicate coverage credit and retain all uninspected candidates.']))
    sources=[]
    for key,title,claims,repo,date in [
       ('h2o','H2O-3 Java uplift forest, scoring, metrics and numerical source contracts',HCLAIMS,'h2oai/h2o-3','20 September2026; selected3.47.0 bleeding_edge source'),
       ('tetrad','Tetrad Java IDA and CStaR magnitude, subsampling and ranking contracts',TCLAIMS,'cmu-phil/tetrad','22 September2026; pinned source, not released-binary qualification')]:
        sources.append(dict(integrated_citation_key='exec20_javaeffects_'+key,kind='software_primary_sources',
            title=title,author=('H2O.ai contributors' if key=='h2o' else 'Tetrad contributors'),year=2026,
            source_identity='https://github.com/'+repo,version_date=date,
            local_copy=records[key][0]['local_copy'],records=records[key],
            identity_evidence=[ref(BASE/'authenticated-sources.json','Immutable root and blob identities')],
            inspected_anchors=[dict(anchor=c,inspection='Selected primary source and documentation anchors') for c in claims],
            supported_claims=claims,limitations=LIMITS,native_execution=False))
    sources.append(dict(integrated_citation_key='exec20_javaeffects_reference',kind='project_authored_exact_reference',
        title='Exact uplift, confounding, ranking, direction and numerical-reference examples',
        author='Causal banking proposal project',year=2026,version_date='20 October2026',
        source_identity='tools/java_effect_reference_20261020.py',
        local_copy=ref(ROOT/'tools/java_effect_reference_20261020.py','calculate: rational arithmetic and finite enumeration'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Exact assertions and independent displayed derivations')],
        supported_claims=['Confounding9/25 despite causal0; assumed net16 versus-20. Smoothed1/2 versus raw3/5. Means1/4,3/20,7/20 depend on retained rows. Same rank with doubled scores retains curve but doubles mean. Literal KL witness-1 versus0; signed candidates-2,-1/2 give magnitude1/2; ties can select3 at nominal bracket1.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',limitations=LIMITS,
        inherited_ida_review=ref(ROOT/'docs/program/execution/2026-10-19/java-identification-v1/source-audit.json','Preserved identification scope, not new duplicate coverage')))
    write(BASE/'exact-results.json',exact.calculate())
    candidates=[dict(name='H2O-3 UpliftDRF',language='Java fitting/scoring core; R/Python clients separate',
        target='Binary-treatment binary-outcome conditional response difference and retained-row mean predictions',
        assignment='Requires a separate causal identification and support argument; assignment column alone supplies neither',
        weights='Rejected in selected training path',cross_fitting='Built-in cross-validation rejected; externally held-out evaluation proposed',
        uncertainty='Inspected outputs do not establish a calibrated CATE interval; AUUC and OOB scores are different objects',
        route='Propose original Java worker and independently tested MOJO scorer; defer admission and literal port pending split and fallback reconciliation',
        rights='Inspected root Apache2.0 declaration; full distribution/dependencies unqualified'),
      dict(name='Tetrad IDA/CStaR',language='Java source',
        target='Linear graph-compatible slope candidates and minimum-absolute-effect stability rankings, not nonlinear CATE',
        assignment='Graph, linear-model and sampling assumptions explicit; signed effects and class uncertainty retained',
        weights='No weight-aware effect argument established by selected source',
        cross_fitting='Half-row subsampling/bootstrapping is a ranking construction, not cross-fitting or dependent-sample inference',
        uncertainty='Frequency, magnitude and displayed PCER formula do not establish calibrated effect intervals',
        route='Retain graph-effect reference; a JVM worker must report sign, candidate failures, tie policy and original-scale effects',
        rights='Selected GPLv3-or-later headers; actual dependency/distribution obligations remain unresolved')]
    write(BASE/'candidate-register.json',dict(candidates=candidates,complete_census=False,native_admission=False))
    gaps=[
      ('Complementary Java coverage','Inspect saved metadata leads, aliases, search remainder and cross-language implementations before excluding any candidate.'),
      ('H2O split discrepancy','Build a pinned, rights-reviewed minimal Java reference; evaluate metric methods and splits at equal probabilities and boundary support. Resolve source/document mismatch before KL-path admission.'),
      ('H2O root, missingness and export','Trace priorClassDist, missing-feature branches, superclass serialization and threshold keys; qualify full engine/MOJO equivalence, treatment/category maps and unsupported groups.'),
      ('Tetrad numerical and ranking contract','Inspect matrix exception types, legal-graph helpers and cache identity; test signed/absolute minima, ties, singular covariances and category/column permutations.'),
      ('Foundational algorithm proofs','Acquire and inspect genuine PDFs named in upstream headers before attributing theorem or formal error-control claims; this review relies on source behavior only.'),
      ('Causal uncertainty and public experiments','Register independent unit/cluster/time sampling laws and held-out mechanisms; establish coverage and policy value before any deployment decision.'),
      ('Runtime and rights','Freeze source revision, JVM, build, complete artifacts, dependencies and notices; process boundaries do not themselves resolve licensing.') ]
    write(BASE/'omissions-register.json',dict(items=[dict(item=k,status='open',route=v) for k,v in gaps],
        unread_candidates=ref(BASE/'search-review.json','All saved unread discovery leads'),essential_sources_waived=False,global_blocker=None))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,requirements=[
        'Bind question, treatment and positive outcome level, horizon, units, target population and sampling law.',
        'Preserve row/category identifiers, assignment probabilities, eligibility and missing-outcome exclusions.',
        'Expose uplift contrast, target-row mean, AUUC curve, signed graph candidates and stability rank as distinct typed results.',
        'Keep unsupported exposure, numerical failure, graph-implied zero and unqualified uncertainty distinct.',
        'Record split criterion expression, smoothing, missingness, root fallback, forest normalization and artifact format version.',
        'Retain signed effects and variable scales beside absolute graph rankings; freeze ties and dependence-aware resampling.',
        'Use a keyed CLI/MCP request with source/artifact hashes and explicit refusal status; do not claim the proposed Java worker exists.',
        'Run public synthetic adversarial references only after pinned executable/rights admission; separate bank validation.']))
    names=['plan-review.json','search-review.json','authenticated-sources.json','inspected-extracts.json',
        'source-audit.json','exact-results.json','candidate-register.json','omissions-register.json','conversion-contract.json']
    evidence=[ref(BASE/n,'Java effects evidence') for n in names]+[ref(Path(__file__),'Exact author review')]
    trigger='Complete complementary sources; reconcile uplift splitting/fallback/export and graph ranking/numerical semantics; qualify pinned public prototypes with target and uncertainty contracts.'
    criteria=[dict(index=0,verdict='inconclusive',finding='H2O and Tetrad selected paths are reviewed; complementary Java sources and search remainder remain open.'),
        dict(index=1,verdict='pass',finding='28 blobs match immutable trees and acquisition hashes; claims bind inspected anchors; native and theoretical proof claims are withheld.'),
        dict(index=2,verdict='pass',finding='Concrete original-engine routes, unresolved alternatives and exact public references are supplied without waiving essential evidence.')]
    coverage=dict(operation_id=OP,status='inconclusive',scope='Two-profile Java effects and stability-ranking source review',
        reviewer=REVIEWER,candidates=candidates,evidence=evidence,criteria=criteria,limitations=LIMITS,
        revisit_trigger=trigger,capabilities=[],integration_allowed=False,original_gap_qualification=False)
    write(OUTPUT,coverage)
    write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,reviewed_output=ref(OUTPUT,'Contracted coverage'),
        findings=HCLAIMS+TCLAIMS,criteria=criteria,evidence=evidence,limitations=LIMITS))
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope=coverage['scope'],reviewer=REVIEWER,
        outputs=[ref(OUTPUT,'Java effects coverage review')],limitations=LIMITS,nonexecution_reason='',
        revisit_trigger=trigger,capabilities=[],criteria=[dict(c,evidence=evidence+[ref(BASE/'review.json','Author criterion review')]) for c in criteria])
    write(BASE/'operation-receipt.json',receipt);verify_bindings([coverage,receipt])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',authenticated_blobs=28,native_runs=0)))


if __name__=='__main__':main()
