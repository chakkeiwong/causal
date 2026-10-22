#!/usr/bin/env python3
"""Source-grounded observation comparison; no market-completion or native claim."""
import argparse
import json
from pathlib import Path
import observations_reference_20261022 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-22/observations-commercial-v1'
OP='SW.CELL.observations_data.commercial';COMPARE='SW.COMM.observations_data'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Eight-family candidate frame is bounded, not an exhaustive market census; four have inspected technical text.',
 'Cutoff 7 October 2026; later mutable manuals, page update labels and document histories do not establish exact cutoff-era bytes.',
 'AWS PDF has 22 October 2026 creation metadata; latest listed change is 27 April 2026. Runtime revision and deployment region remain unverified.',
 'IBM 11.7.0 overview supports only documented high-level matching scope, not scoring or threshold mathematics.',
 'No vendor engine, downloaded code, live model, bank trial, subscription, purchase or contact was performed.',
 'Commercial rights, exact deployment editions, prices, calibration and export equivalence remain unverified.',
 'Numerical examples are authored hypothetical laws; they do not measure vendor accuracy, bank returns or empirical interval coverage.',
 'Visual review remains pending a fresh image allowance; mandatory repairs, Q1/Q5 and final acceptance remain open.']

def original(name,folder,title,author,version,ranges,claims,extension='html'):
    p=BASE/'acquisition'/folder/(name+'.'+extension);receipt=p.with_suffix('.receipt.json');r=read(receipt)
    assert r['returncode']==0 and r['format_valid'] and core.sha(p)==r['sha256']
    extracted=BASE/'extracted'/(name+'.txt');body=extracted.read_text();lines=body.split('\n')
    anchors=[]
    for lo,hi in ranges:
        assert 1<=lo<=hi<=len(lines)
        anchors.append(dict(anchor=f'extracted newline-delimited lines {lo}-{hi}',
            physical_page='\n'.join(lines[:lo-1]).count(chr(12))+1 if extension=='pdf' else None,
            inspected_text='\n'.join(lines[lo-1:hi])))
    return dict(integrated_citation_key='exec22_obs_'+name,kind='official_documentation',
        title=title,author=author,year=2026,source_identity=r['url'],version_date=version,
        accessed_utc=r['finished_at'],local_copy=ref(p,'Authentic official original'),
        text_copy=ref(extracted,'Inert extraction; original authoritative'),
        acquisition_receipt=ref(receipt,'Public acquisition, identity and hash'),
        inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS)

def receipt(operation,output,evidence,findings,scope):
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==operation
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,operation)
    value=run.ledger.receipt_template(node)
    value.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=REVIEWER,
        capabilities=[],outputs=[ref(output,'Reviewed scoped result')],limitations=LIMITS,
        nonexecution_reason='',revisit_trigger='Finish complementary discovery, exact cutoff editions, scoring/calibration originals and commercial terms; qualify generated cases before bank trials.',
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    return value

def coverage():
    output=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
    assert not output.exists() and not (BASE/'source-audit.json').exists()
    sources=[
      original('aws_er_manual','network-details','AWS Entity Resolution User Guide','Amazon Web Services',
        'Latest mutable guide; PDF creation 22 October 2026; document history latest listed 27 April 2026; exact cutoff bytes unverified',
        [(2991,3043),(3706,3748),(3810,3848),(4327,4346),(4531,4554),(4562,4581),(5884,5941),(10600,10612),(11042,11064),(11493,11535)],
        ['Simple and Advanced rules have different operators and workflow support; selected table includes fuzzy Advanced matching despite exact-only generic glossary wording.',
         'Transitive matching is Advanced/API-only and configured at creation; rule order and earlier match identifiers affect output.',
         'ML uses cleartext, not hashed inputs; group confidence differs from record confidence, the latter only in incremental ML.',
         'Match ID identifies an output record group; many-to-many terminology describes field comparisons, not legal ownership.',
         'Success/error records and job identifiers must both survive; specified data errors can incur charges.',
         'Provider matching requires a public subscription or private provider offer; no entitlement verified here.'],'pdf'),
      original('ibm_matching','network-details','Matching data: IBM InfoSphere QualityStage 11.7.0','IBM',
        'Versioned 11.7.0 documentation route, acquired 22 October 2026; publication date and installed build unverified',
        [(1,27),(28,42)],
        ['QualityStage describes probabilistic record linkage, tunable matching and handling missing or inaccurate fields.',
         'Match Designer defines/tests specifications; one-source/two-source stages and per-pass statistics are documented.',
         'Overview does not establish exact weight formulas, score calibration or joint mapping uncertainty.']),
      original('databricks_pit','network','Point-in-time feature joins','Databricks',
        'Page reports 11 September 2026; mixed Unity Catalog and legacy client APIs; acquired 22 October 2026',
        [(4,16),(40,52),(76,80),(108,109),(164,167),(193,200),(222,228)],
        ['Time-series AS OF joins require designated time keys and retrieve latest prior values; ordinary primary-key timestamps do not imply that behavior.',
         'Point-in-time feature lookup is distinct from Delta Lake storage time travel.',
         'Latest null feature rows are not skipped; default lookback is unbounded.',
         'Lookback applies in training/batch, while online inference uses latest feature values; snapshot online mode lacks point-in-time lookup.',
         'Selected API semantics do not independently authenticate the availability meaning of user-supplied timestamps.']),
      original('databricks_feature','network','Work with feature tables in Workspace Feature Store (legacy)','Databricks',
        'Page reports 11 September 2026; legacy Workspace Feature Store, with Unity Catalog recommended; acquired 22 October 2026',
        [(4,10),(17,27),(115,126)],
        ['Selected feature-table manual is legacy; edition/client paths must not be silently combined.',
         'Feature computations return keyed DataFrames and populate Delta tables; feature keys are an input contract, not identity verification.',
         'Merge leaves rows whose keys are absent from the update unchanged; selected metadata cannot be updated in place.']),
      original('snowflake_time','network','Understanding and using Time Travel','Snowflake',
        'Mutable official service manual acquired 22 October 2026; Standard versus Enterprise/permanent versus transient distinctions explicit; exact cutoff revision unknown',
        [(3,19),(31,48),(58,64),(79,83),(147,165)],
        ['Time Travel queries historical storage states within retention, with current schema.',
         'Default retention is one day; permanent Enterprise-and-higher objects can retain up to 90 days, unlike temporary/transient objects.',
         'Increasing retention cannot recover history already outside Time Travel; retention incurs storage cost.']),
      original('snowflake_at','network','AT and BEFORE: Snowflake SQL reference','Snowflake',
        'Mutable official SQL reference acquired 22 October 2026; exact service build/cutoff revision unknown',
        [(6,14),(31,49),(111,114),(159,173)],
        ['AT includes boundary changes; BEFORE statement means just before statement completion, not start, and can include concurrent commits.',
         'Explicit timestamp types/time zones and 14-day statement-ID limits need preservation.',
         'Historical table data uses current columns/defaults and current access requirements; unavailable history raises an error.'])]
    sources.append(dict(integrated_citation_key='exec22_obs_reference',kind='project_authored_exact_reference',
        title='Exact linkage, availability and inclusion examples for customer observations',author='Causal banking proposal project',year=2026,
        source_identity='tools/observations_reference_20261022.py',version_date='22 October 2026; finite authored laws and rational arithmetic',
        local_copy=ref(ROOT/'tools/observations_reference_20261022.py','Exact authored calculation'),
        inspected_anchors=[dict(anchor='calculate(): clocks, two-map law, independent noise and selection reweighting',inspection='Author inspection and exact execution')],
        supported_claims=['Event-only retrieval returns9 although only2 is available at decision10.',
            'Map means+4/-4 at p=4/5 yield12/5, total variance1049/100, and stipulated margins10/-6.',
            'Population effect4 becomes26/5 in the retained sample; correct inverse inclusion weighting returns4 under stated assumptions.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07T15:59:59Z',sources=sources,visual_acceptance=False))
    write(BASE/'exact-results.json',exact.calculate())
    specs=[
      ('AWS','AWS Entity Resolution; rule-based; ML; provider matching','Complete official guide; selected technical sections inspected',
       'Workflow IDs, rule ordering, confidence level granularity, transitive links, success/error partitions and input provenance.',
       'Pin region/API workflow contract and historical edition; inspect confidence calibration and billing/license terms; preserve full group hypotheses.'),
      ('IBM','InfoSphere Information Server 11.7.0; QualityStage; Match Designer','Versioned matching overview inspected; detailed scoring remains unread',
       'Probabilistic linkage, specification design and per-pass statistics; no exact score or posterior claim.',
       'Recover weights/comparators/blocking/clerical-cutoff originals, match-spec export, release fixes and deployment entitlements.'),
      ('Databricks','Feature Engineering in Unity Catalog; Workspace Feature Store (legacy)','Two official technical pages inspected',
       'AS OF keys, explicit nulls, lookback, client/API distinctions and online snapshot versus training/batch behavior.',
       'Pin supported client/Runtime and availability-clock semantics; inspect serving/provider configuration, license and measured parity.'),
      ('Snowflake','Time Travel; AT; BEFORE; Standard; Enterprise','Two official manuals inspected',
       'Storage snapshots, retention/edition/object type, timestamp casts, statement completion, current schema and permissions.',
       'Pin service configuration/edition, preserve schema and source availability separately, price retention/export, test historical refusals.'),
      ('Informatica','MDM; Intelligent Data Management Cloud; Customer 360','Candidate lead only; no technical original inspected',
       'No capability conclusion from product family name.',
       'Acquire exact-edition matching/survivorship, temporal history, lineage/export and licensing manuals.'),
      ('Precisely','Spectrum; entity resolution; data integrity','Candidate lead only; no technical original inspected',
       'No capability conclusion from product family name.',
       'Resolve product/version aliases and acquire matching, temporal lineage, uncertainty export and deployment terms.'),
      ('SAS','Data Quality; DataFlux; data management','Candidate lead only; no technical original inspected',
       'Earlier SAS estimation reviews do not cover this matching contract.',
       'Recover selected-release match codes, clustering/quality-knowledge-base dependence, audit exports and licensed runtime terms.'),
      ('Tecton','Feature platform; historical retrieval; online serving','Candidate lead only; no technical original inspected',
       'No point-in-time/availability parity conclusion without original semantics.',
       'Acquire exact-version temporal join, late-arrival, materialization/serving and commercial deployment originals.')]
    candidates=[dict(family=f,aliases=a,source_status=s,technical_scope=t,next_public_evidence=n,
        absence_claim=False,runtime_executed=False,entitlement_verified=False) for f,a,s,t,n in specs]
    write(BASE/'search-coverage.json',dict(cutoff='2026-10-07T15:59:59Z',
        local_inventory='Existing observation catalog had no commercial candidate profile; inherited open-source neighbors do not establish vendor coverage.',
        external_discovery='No search connector available; six fixed official requests plus three official-link followups. Not a complementary index census.',
        stopping_rule='Completed six fixed requests and three followups within four-link allowance; failed URL and IBM index preserved separately from recovered technical originals.',
        complete_market_search=False,no_hit_claim=False))
    write(BASE/'candidate-register.json',dict(cutoff='2026-10-07',candidates=candidates,market_census_complete=False))
    attempts=[ref(p,'Authentic acquisition outcome, including DNS and HTTP failures') for p in sorted((BASE/'acquisition').glob('*/*.receipt.json'))]
    write(BASE/'acquisition-review.json',dict(status='pass_for_provenance',attempts=attempts,
        findings=['Nine sandbox DNS failures retained before elevated retry; initial AWS PDF404 retained.',
            'IBM initial HTML is an index, not matching technical evidence; a linked 11.7.0 overview was recovered.',
            'AWS corrected PDF link recovered from official index; complete272-page guide authenticated, only declared sections inspected.',
            'Optional bs4 import was unavailable; deterministic standard-library inert HTML parser used without installation.'],
        evidence=[ref(ROOT/'tools/extract_observations_sources_20261022.py','Deterministic text extraction')]))
    write(BASE/'omissions-register.json',dict(global_blocker=False,bank_inputs_required_for_next_public_work=False,
        acquisition=ref(BASE/'acquisition-review.json','Preserved attempts and recoveries'),
        candidates=[dict(family=c['family'],next_action=c['next_public_evidence']) for c in candidates],
        additional=['Complementary market discovery and exact cutoff-era source revisions.',
            'Independent stratified linkage truth, joint-map uncertainty, ownership semantics and inclusion positivity.',
            'Native replay, full costs and commercial terms; public generated tests precede private bank experiments.',
            'Rendered visual review remains pending the inherited session image limit.']))
    requirements=[
        'Declare observational unit and relationship: person, account, household and beneficial ownership are different objects.',
        'Retain source row keys, match groups/rules, alternative links, score scope, calibration limits and coherent joint mapping constraints.',
        'Bind decision time, event/valid time, system/availability time, mapping issue time, time zone and replay vintage.',
        'Preserve processed, unmatched, rejected and error populations plus audit sample design; no silent success-only selection.',
        'Preserve native null/stale semantics, feature transformations, schema, retention/configuration and offline/online differences.',
        'Separate conditional sampling, linkage, graph and missingness uncertainty; do not turn an uncalibrated confidence into a posterior.',
        'Produce identical typed evidence/refusals across library, CLI and MCP; an agent can draft mappings, not certify identity or event truth.',
        'Qualify matched generated cases with wrong links, late corrections, schema drift and retention expiry before costly bank studies.']
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,requirements=requirements))
    evidence=[ref(BASE/n,'Reviewed observation evidence') for n in ['plan.md','plan-review.json','source-audit.json','search-coverage.json',
        'candidate-register.json','acquisition-review.json','omissions-register.json','conversion-contract.json','exact-results.json']]+[ref(Path(__file__),'Review construction')]
    findings=[('inconclusive','Eight-family bounded frame with four supported profiles; complementary discovery, four originals and exact editions remain unresolved.'),
        ('pass','Six authentic official originals have exact bytes, source/version limits and inspected newline/page anchors; mathematical examples are separately authored.'),
        ('pass','Recovered sources, failed attempts, unknown capabilities, rights and next actions remain explicit; no absence finding or source waiver.')]
    scope='Bounded commercial observation comparison: identity, clocks, inclusion and audit'
    item=dict(operation_id=OP,status='inconclusive',scope=scope,reviewer=REVIEWER,candidates=candidates,
        criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)],evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False)
    write(output,item);write(BASE/'review.json',item)
    write(BASE/'operation-receipt.json',receipt(OP,output,evidence,findings,scope));verify_bindings(item)
    print(json.dumps(dict(operation=OP,outcome='inconclusive',originals=6,supported_families=4,candidates=8)))

def compare():
    output=ROOT/f'docs/program/comprehensive-v14/work/{COMPARE}/vendor-comparison.json';assert not output.exists()
    rows=[]
    for c in read(BASE/'candidate-register.json')['candidates']:
        rows.append(dict(**c,documented_strength=c['technical_scope'],
            matched_use_case='Estimate a pre-action customer-retention intervention from linked histories with uncertain identity and late-arriving outcomes.',
            observed_current_capability='Authored exact references and proposal contracts; no qualified native observation adapter.',
            proposed_capability='Identity/relationship types, two-clock availability checks, inclusion ledger and uncertainty-preserving library/CLI/MCP artifacts.',
            remaining_gap=c['next_public_evidence'],reuse_disposition='Conditional isolated adapter where documented; defer unread families. Reject automatic promotion of match IDs or historical snapshots to causal truth.',
            deployment_rights='Not verified; public documentation is not runtime or redistribution permission.',price=dict(status='unavailable',amount=None,quote_obtained=False)))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['source-audit.json','review.json','candidate-register.json','conversion-contract.json','omissions-register.json','exact-results.json']]+[ref(Path(__file__),'Comparison construction')]
    findings=[('inconclusive','Four documented profiles support specific comparisons; exact deployed editions, terms/prices and four other families remain unresolved.'),
        ('pass','Each row distinguishes documented behavior, proposed addition, actual current implementation and unexecuted validation; no superiority or purchase claim.')]
    scope='Eight-family commercial observation comparison with generated validation route'
    item=dict(operation_id=COMPARE,status='inconclusive',scope=scope,reviewer=REVIEWER,vendors=rows,
        criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)],evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False)
    write(output,item);write(BASE/'comparison-review.json',item)
    write(BASE/'comparison-receipt.json',receipt(COMPARE,output,evidence,findings,scope));verify_bindings(item)
    print(json.dumps(dict(operation=COMPARE,outcome='inconclusive',families=8,supported_profiles=4)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['coverage','compare']);a=p.parse_args()
    {'coverage':coverage,'compare':compare}[a.command]()
