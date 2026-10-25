#!/usr/bin/env python3
"""Authenticate pinned Remaining-language originals and review authored laws, without native execution."""
import argparse,hashlib,json
from pathlib import Path
import other_transport_missingness_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as fresh_write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/other-transport-missingness-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.transport_missingness.other_relevant'
read=lambda p:json.loads(p.read_text())
def write(p,value):
    if p.exists():assert read(p)==value,'Existing evidence differs: '+str(p)
    else:fresh_write(p,value)
LIMITS=['Four bounded queries and three selected ecosystems do not establish saturation; returned candidates and other languages remain open.', '35 authentic originals support Julia, Scala and Rust component contracts, not population-transport identification.', 'No downloaded code executed; exact authored witnesses do not establish native failure rates.', 'Julia default initialization, neighbor ties, missingness threshold, fit/transform masks, integer casts and temporal ordering require explicit adapter semantics.', 'Complete native runtimes, numerical delegates, distribution rights and total public-prototype costs remain unqualified.', 'Package-mentioned scholarly references are discovery leads without newly admitted genuine PDFs.', 'No visual, independent, bank or final acceptance; mandatory coverage/depth and Q1/Q5 remain open.']
NEXT='Inspect remaining-language candidates and qualify mask/default semantics, neighbor ties, within-entity temporal order, leakage, integer casts, exact quantile configuration and complete runtime rights using public fixtures before native admission.'
DECISIONS=['Impute.jl: conditionally reuse explicit summary, donor and temporal routines after typed initialization, tie and ordering qualification; no universal missingness correction.', 'Spark: conditionally adopt fitted numeric surrogates with training-only fit, typed casts, quantile/error semantics and explicit null/NaN policy.', 'Polars: conditionally adopt null/NaN and ordered-data operations as data infrastructure; reject treating fill/interpolation as causal imputation or transport identification.']
ANCHORS={'imputejl': [('src01', 1, 15, 'MIT', 'Selected MIT declaration; dependency rights separate.'),
              ('src04',
               21,
               58,
               'KNN(k + 1',
               'Requested k increments to include presumed self; initializes via Substitute and queries a KD tree over completed data.'),
              ('src04',
               57,
               91,
               'isfinite',
               'First zero-distance index assumed self; missing-neighbor threshold and finite-weight guard can leave initialized values.'),
              ('src06', 36, 50, 'defaultstats', 'Substitution uses selected statistic and warns/returns unchanged when every value is missing.'),
              ('src06',
               93,
               146,
               'median',
               'Weighted mask alignment and default real median/integer rounding semantics; KNN comment saying mean is not authoritative.'),
              ('src05', 40, 52, 'rand(imp.rng', 'Random donor imputation samples marginal observed values; all-missing input remains unfilled.'),
              ('src07', 44, 63, 'start_idx', 'LOCF uses sequence order and limit; no entity boundary supplied in selected vector kernel.'),
              ('src08', 43, 62, 'end_idx', 'Backward fill uses subsequent observations and retains tail without donor.'),
              ('src09', 44, 65, '_interpolate!', 'Interpolation uses future endpoint and optional gap-length limit.'),
              ('src09', 70, 94, 'length(indices) + 1', 'Interpolation is based on position spacing with optional integer rounding.'),
              ('src11',
               33,
               88,
               'isfinite(C)',
               'SVD has rank and stopping branches, retained mask and mutable missing entries; maxiter return is not a convergence receipt.'),
              ('src12', 38, 41, 'mratio', 'Unweighted threshold reports missing fraction rather than inferential adequacy.'),
              ('src12',
               63,
               74,
               'sum(wt.weights)',
               'Weighted threshold checks shape then divides weighted missing sum by total weights; denominator policy requires '
               'qualification.')],
 'polars': [('src01', 1, 15, 'Permission is hereby granted', 'Selected MIT-style rights declaration; component/dependency scope separate.'),
            ('src02', 58, 73, 'null_count', 'No-null and all-null statistic/propagation paths can return an unchanged clone.'),
            ('src02', 78, 94, 'Some(limit)', 'Forward/backward fill limit is implemented in series context.'),
            ('src02', 218, 239, 'NumCast', 'Mean fill casts to the physical numeric type; original dtype matters.'),
            ('src08', 906, 922, 'is_not_nan', 'Null fill and NaN fill are distinct expressions; fill_nan preserves existing nulls.'),
            ('src03', 40, 104, 'first_non_null', 'Positional interpolation preserves boundary nulls and returns all-null input unchanged.'),
            ('src04',
             15,
             39,
             'range_y / range_x',
             'Coordinate interpolation uses supplied coordinate differences; duplicate coordinates need explicit policy.'),
            ('src04', 93, 104, 'null values in', 'Substantive coordinate-interpolation branch refuses null coordinates after unchanged-input early return.'),
            ('src04',
             181,
             199,
             'arg_sort',
             'Unsorted coordinate path sorts by the by column; entity partition and decision-time rules remain caller obligations.')],
 'spark': [('src01', 1, 8, 'Apache License', 'Selected Apache2 declaration; binary dependencies separately listed.'),
           ('src03', 103, 115, 'truncated', 'Numeric-only surrogate imputation and integer truncation are explicitly documented.'),
           ('src03',
            154,
            183,
            'isNaN',
            'Fit excludes null, selected sentinel and NaN; mean and approximate median have separate aggregation routes.'),
           ('src03', 185, 207, 'negative_count', 'Mode ties choose smallest value; empty surrogate columns refuse.'),
           ('src03',
            280,
            294,
            'cast(inputType)',
            'Transform replaces null and selected sentinel then casts to original type; explicit non-NaN sentinel does not make every NaN a '
            'replacement.'),
           ('src04',
            80,
            105,
            'Double.NaN',
            'Upstream tests retain NaN in transform when configured sentinel is -1, while excluding it during fit.'),
           ('src05', 35, 61, 'rank(x)', 'Documented quantile error concerns rank, not arbitrary value-distance error.'),
           ('src05',
            80,
            99,
            'Int.MaxValue',
            'Selected implementation maps zero relative error to max integer accuracy for approximate percentile; exactness cannot be inferred '
            'solely from the comment.')]}
def prepare():
    assert not (BASE/'review.json').exists()
    pins=read(BASE/'pins.json');selected=sum((read(BASE/n) for n in ['selected-paths.json','delegate-paths.json','defaults-paths.json','default-delegates-paths.json']),[])
    assert len(selected)==35;rows=[];identities=[];originals=[]
    for group,pin in pins.items():
        cp=RAW/f'exec25_otm_{group}_commit.json';tp=RAW/f'exec25_otm_{group}_tree.json'
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        commit=read(cp);commit=commit[0] if isinstance(commit,list) else commit;assert commit['sha']==pin['sha'] and commit['commit']['committer']['date']==pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha'] in {pin['sha'],pin['tree_sha']} and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned identity'),ref(tp,'Complete selected tree')])
        for item in [x for x in selected if x['group']==group]:
            p=RAW/(item['id']+'.txt');rp=p.with_suffix('.receipt.json');r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p)
            expected='https://raw.githubusercontent.com/'+pin['repository']+'/'+pin['sha']+'/'+item['upstream_path']
            assert r['url']==expected
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==blobs[item['upstream_path']]
            rows.append(dict(group=group,upstream_path=item['upstream_path'],local_path=str(p.relative_to(ROOT)),receipt=str(rp.relative_to(ROOT)),sha256=core.sha(p),git_blob=blob,url=expected))
            originals.append(dict(group=group,upstream_path=item['upstream_path'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'Public receipt'),git_blob=blob))
    write(BASE/'selected-originals.json',rows);write(BASE/'authenticated-originals.json',dict(count=35,groups=3,originals=originals,identities=identities,native_execution=False))
    sources=[];fragments=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[ref(RAW/f'exec25_otm_{group}_commit.json','Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_otm_{group}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,lo,token)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=group,source=binding,first_line=lo,last_line=hi,text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_otm_'+group,kind='software',title=group+' pinned Remaining-language missingness and numerical-completion contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['sha'],version_date=pin['date']+';'+pin['sha'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_otm_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only; creation-date filter is not historical search reconstruction'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results'],lexical_mismatch=False))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==4
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals.json','Selected original declarations')],findings=['Impute.jl and Polars selected MIT-style declarations; Spark Apache2 plus separate binary dependency ledger.','No exact installed/runtime dependency rights or distribution clearance.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Exact authored laws'),ref(BASE/'exact-results.json','Arithmetic replay'),ref(BASE/'inspected-extracts.json','Implementation contracts')],findings=['Marginal donor mean1/2 and variance1/4 do not preserve conditional dependence.','KNN requested1uses2including assumed self; duplicate zero distance triggers finite-weight guard.','Integer mean7/3can be cast to2; mode tie policy selects1.','Positional interpolation5differs from coordinate interpolation1.','Null and NaN fills affect different masks; global forward fill can cross entity boundaries.','Rank tolerance does not bound monetary value error; hypothetical population difference yieldsUSD80000.'],native_execution=False))
    tests=['Freeze population, estimand, observation mask, decision time and entity identity.','Qualify each language null/NaN/sentinel and dtype conversion separately.','Test requested versus internal KNN counts, self identity, zero-distance ties, threshold skip and initialization trace.','Test donor draws against joint/conditional laws and retain RNG scope.','Separate training-only fitted surrogates from transform; preserve weighted and approximate-quantile assumptions.','Test temporal ordering, within-entity groups, boundary nulls, gap limits, irregular spacing and duplicate coordinates.','Retain native convergence/empty-output/refusal diagnoses rather than inferring success from return.','Resolve exact artifacts/dependencies and replay typed CLI/MCP fixtures with complete costs.']
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Julia Scala Rust missingness, temporal ordering and population contracts',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Prototype implementation owner to be appointed',tests=tests,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded candidates'),ref(BASE/'dependency-license-review.json','Rights scope')],known_routes=tests,uninspected=['Returned Julia imputation candidates and wider Scala/Rust catalogs.','Other relevant languages and complete current frontier literature.','Complete nearest-neighbor, quantile, numerical and runtime qualification.','Package-mentioned scholarly originals not admitted here.'],unknown_universal_repairs=['Unrestricted MNAR is not solved by mask conversion or interpolation.','Unsupported populations and unobserved assignment require information or defended assumptions.','Arbitrary dependence and model uncertainty have no universal software correction.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','mathematical-review.json','comparison-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_otm_choice',kind='project_evidence_not_scholarly_paper',title='Authored Julia Scala Rust missingness and transport qualification decisions',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; cutoff7 October2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence+[ref(Path(exact.__file__),'Authored reference')],inspected_anchors=[dict(anchor='Finite laws, source contracts and comparison decisions',inspection='Author inspection')],supported_claims=['35 authentic originals ground three bounded component comparisons.','Exact laws distinguish masks, neighbors, temporal ordering, type conversions and target population.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=4,new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Imputation is distinct from population transport and causal identification.','Authored witnesses do not imply measured native failures.','Independent public qualification can proceed before bank trials; bounded source limits do not block independent work.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Population target through masks, donors, fitted transforms, temporal ordering and alternatives.','Three source collections and authored witnesses cited with limits.','No scholarly citation admitted without original; no native or visual acceptance.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    verify_bindings(dict(evidence=evidence));write(BASE/'review.json',dict(status='pass_for_bounded_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=35,scholarly_originals=0,limitations=LIMITS,native_execution=False));print(json.dumps(dict(review='pass',outcome='inconclusive',originals=35,anchors=len(fragments))))

def receipt():
    review=read(BASE/'review.json');verify_bindings(review);assert exact.calculate()==read(BASE/'exact-results.json')
    state=core.read(ROOT,core.STATE);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);output=ROOT/node['outputs'][0]
    write(output,read(BASE/'comparison-review.json'))
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Three source collections inspected; ecosystem, current-edition and native coverage remain incomplete.','Pinned originals and exact authored laws support claims; scholarly metadata is discovery only.','Conditional adoption, port, defer and reject routes retain scientific and rights conditions.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Remaining-language transport and missingness primary-source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Remaining-language transport/missingness coverage receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
