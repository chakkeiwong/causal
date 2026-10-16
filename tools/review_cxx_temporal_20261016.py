#!/usr/bin/env python3
"""Bounded primary-source audit and independent authored temporal references."""
import argparse
from datetime import datetime
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

import master_control as core
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-16/cxx-temporal'
RAW = ROOT/'docs/literature/raw'
PRIOR = ROOT/'docs/program/execution/2026-10-16/longitudinal-policy/publication/reader/source-audit.json'
OP = 'SW.CELL.discovery_temporal_interventional.Cxx'
OUTPUT = ROOT/('docs/program/comprehensive-v14/work/'+OP+'/coverage-review.json')
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Bounded cutoff-compatible source comparison; no exhaustive native-software census or unsupported absence finding.',
    'Static upstream inspection and executed project-authored exact references are separate; no upstream compilation or runtime benchmark.',
    'Missing licenses, file-specific license discrepancies, uninspected dependencies and mirror provenance remain reuse prerequisites.',
    'Independent rows, known targets, stationarity, physical clocks, state identity and graph semantics require explicit validation; no general dependent effect calibration is established.',
    'Banking values are stipulated USD illustrations, not observed bank returns or vendor prices.',
    'Public/generated prototype and CLI/MCP contracts are proposed; integration remains disabled.',
    'Inherited six-preview allowance is exhausted; text and bounds review does not confer rendered visual, Q1 or Q5 acceptance.'
]
FAMILIES = {
    'pcalg': ('cran/pcalg', 'exec13_pcalg_cutoff_commits', 'exec13_pcalg_tree'),
    'agrum': ('agrumery/aGrUM', 'v12_sw_cutoff_commit_agrum', 'v12_sw2_tree_agrum'),
    'bayesnetty': ('NewcastleRSE/BayesNetty', 'exec16_ct_commit_bayesnetty', 'exec16_ct_tree_bayesnetty'),
    'mocapy': ('juliusHuelsmann/MocapyPP', 'exec16_ct_commit_mocapy', 'exec16_ct_tree_mocapy'),
    'sdbn': ('JBSants/sDBN', 'exec16_ct_commit_sdbn', 'exec16_ct_tree_sdbn')
}
# Inspected source ranges. These bind static findings, not runtime claims.
ANCHORS = {
    'pcalg_1_v2': [(180,203,'EssGraph and representative outputs'),(222,292,'GIES wrapper phases and native dispatch')],
    'pcalg_2_v2': [(40,70,'Rcpp local-score entry, target and vertex conversion')],
    'pcalg_3_v2': [(79,98,'Fixed-gap adjacency representation'),(1230,1265,'Greedy forward search entry')],
    'pcalg_4_v2': [(26,83,'One-based to zero-based targets; raw/scatter/R score dispatch'),(210,236,'Scatter score and failed Cholesky'),(304,369,'Nonintervened row conversion, intercept and raw QR score')],
    'pcalg_5_v2': [(100,114,'Preprocessed Rcpp data is part of score interface'),(278,315,'Raw score row/count representation')],
    'pcalg_6_v2': [(259,269,'Undirected fixed gaps'),(308,318,'Children-only compatibility comment is not an enforced premise'),(668,725,'Representative and greedy phase interfaces')],
    'pcalg_7_v2': [(35,62,'Manual constructor intercept FALSE and row/target meaning')],
    'pcalg_8_v2': [(18,38,'Symmetric gaps and phase options'),(101,128,'Adaptive constraints may change gaps'),(130,135,'Essential graph and random representative')],
    'pcalg_9': [(253,293,'Integer coercion and target validation'),(619,679,'Target coverage, row count, sorting and nonintervened row masks'),(724,740,'Actual constructor defaults intercept TRUE')],
    'pcalg_10': [(1,41,'Package version/date, dependencies, compiled code and GPL>=2 declaration')],
    'agrum_1': [(1,36,'LGPL-3-or-later OR MIT file header'),(158,190,'Slice suffix and domain-size checks'),(281,355,'Unrolling guard, parent ordering and numeric CPT copying')],
    'agrum_2': [(1,40,'Official dynamic-network helper documentation')],
    'bayesnetty_1': [(1,35,'Genetic-network software identity')],
    'bayesnetty_2': [(1,18,'GPL3 license text')],
    'bayesnetty_3': [(103,118,'Ordered blacklist edges'),(150,166,'Both whitelist directions require adjacency; conflict is documented error')],
    'bayesnetty_4': [(16,75,'Greedy search, random and jitter restart options')],
    'bayesnetty_5': [(1,20,'Documented executable and g++ installation route')],
    'bayesnetty_6': [(54,74,'Selected serial search returns zero for initial loop; caller not traced')],
    'bayesnetty_7': [(1,10,'Network likelihood score and distributional assumptions')],
    'mocapy_1': [(1,12,'Root license text is LGPL2.1')],
    'mocapy_2': [(1,55,'Legacy CMake and compiler-matched Boost instructions')],
    'mocapy_3': [(1,23,'C,C++,Fortran project and declared build version')],
    'mocapy_4': [(1,20,'Source header declares LGPL3-or-later'),(186,215,'Sampling a supplied DBN')],
    'mocapy_5': [(1,20,'Source header declares LGPL3-or-later'),(124,180,'Sequence/mask inference and E step'),(268,300,'Node parameter M step')],
    'mocapy_6': [(1,20,'Example header declares LGPL3-or-later'),(60,81,'Both example structures have edges supplied before fitting'),(115,137,'E/M parameter fitting loop')],
    'sdbn_1': [(1,38,'C++14, Release fast-math, dependencies and host-specific include path')],
    'sdbn_2': [(23,69,'CLI no-hill, lag, stationarity and stdout default'),(89,102,'Loader selection'),(174,180,'Output path versus directed search')],
    'sdbn_3': [(55,110,'Directed-search caller and result'),(113,125,'No-hill path passes null directed result')],
    'sdbn_4': [(17,55,'Categorical coordinate training; future/lag exclusions permit same-time candidates')],
    'sdbn_5': [(113,180,'Overlapping stationary transition windows'),(183,219,'Already-rolled input path'),(223,257,'Nonstationary input path')],
    'sdbn_6': [(12,26,'Selected local trainer creates regularization paths'),(65,104,'Adaptive path loop')],
    'sdbn_7': [(1,11,'Base trainer constructor only; no additional causal semantics')],
    'sdbn_8': [(11,46,'Native sparse-matrix binary serialization; proposed portable wrapper needs separate contract')],
    'sdbn_9': [(59,107,'Skeleton is directed allowed-pair array; directed result optional')],
    'sdbn_10': [(42,86,'Discrete count log-likelihood used by orientation search')],
    'sdbn_11': [(11,35,'Categorical node state arrays and fitting initialization')],
    'sdbn_12': [(156,177,'Restricted search assumes valid allowed edges, cycle-checks additions and writes diagnostic to stdout'),(197,246,'Reversals restricted to same time and cycle check; no explicit reversed-pair membership check in this branch; progress written to stdout')]
}


def exact():
    """Stipulated laws: exact moments, finite enumeration and score arithmetic."""
    a = F(1,2); noise = F(3,4)
    cov1 = [[F(1),a],[a,a*a+noise]]
    cov2 = [[a*a+noise,a],[a,F(1)]]
    assert cov1 == cov2 == [[1,a],[a,1]]
    intervention = [[[F(4),4*a],[4*a,4*a*a+noise]], [[F(4),F(0)],[F(0),F(1)]]]
    net = [20*a-4, F(-4)]
    assert net == [6,-4]
    y = [F(8),F(10),F(10),F(12)]; mean = sum(y)/len(y)
    rss = sum((v-mean)**2 for v in y); raw = sum(v*v for v in y)
    assert (rss,raw,raw/rss) == (8,408,51)
    with localcontext() as ctx:
        ctx.prec = 40
        delta = Decimal(2)*Decimal(51).ln()
        # Independently substitute each residual sum in the specified native formula.
        s1 = -Decimal(2)*(1+(Decimal(8)/4).ln())
        s0 = -Decimal(2)*(1+(Decimal(408)/4).ln())
        assert abs((s1-s0)-delta) < Decimal('1e-36')
    means = [sum(F(v) for v in shocks)/3 for shocks in itertools.product([-1,1],repeat=3)]
    repeated = [sum([F(v) for v in shocks for _ in range(3)])/9 for shocks in itertools.product([-1,1],repeat=3)]
    assert means == repeated and sum(v*v for v in means)/8 == F(1,3)
    p1 = F(1,10); from_d = F(4,5)
    p2 = (1-p1)*p1+p1*from_d
    corrupt = (1-p1)*from_d+p1*p1
    correct_value = 100-40*p2; corrupt_value = 100-40*corrupt
    assert (p2,corrupt) == (F(17,100),F(73,100))
    assert (correct_value,corrupt_value,correct_value-corrupt_value)==(F(466,5),F(354,5),F(112,5))
    # Distinct graph predicates on a two-node universe.
    universe = [frozenset(),frozenset({('A','B')}),frozenset({('B','A')})]
    gap = [g for g in universe if not g]
    ordered_ban = [g for g in universe if ('A','B') not in g]
    adjacency = [g for g in universe if g]
    assert list(map(len,[gap,ordered_ban,adjacency])) == [1,2,2]
    return {'scope':'Executed authored exact references; not upstream output or empirical performance',
        'regimes':{'coefficient':str(a),'noise_variance':str(noise),'observational_covariance':[[str(x) for x in row] for row in cov1],
            'independent_X_intervention_variance':4,'intervention_covariances':[[[str(x) for x in row] for row in mat] for mat in intervention],
            'one_unit_action_value_per_Y_USD':20,'cost_USD':4,'net_values_USD':[str(x) for x in net],
            'meaning':'The same centered Gaussian observed law admits two causal worlds; intervening on X replaces its equation.'},
        'intercept':{'values':[int(v) for v in y],'mean':str(mean),'centered_RSS':str(rss),'uncentered_RSS':str(raw),
            'same_penalty_score_difference':'2*log(51)','difference_decimal':str(delta)},
        'windows':{'subjects':3,'time_points':4,'lag':1,'transition_rows':9,'independent_units':3,
            'shared_subject_shock_variance':1,'true_mean_variance':'1/3','naive_variance':'1/9',
            'enumerated_shock_worlds':8,'calendar':[0,1,4,5],'adjacent_gaps':[1,3,1]},
        'state_order':{'initial_labels':['current','delinquent'],'repeated_labels':['delinquent','current'],
            'delinquency_from_current':'1/10','delinquency_from_delinquent':'4/5','initial_state':'current',
            'correct_two_step':str(p2),'blind_parent_index_copy_two_step':str(corrupt),
            'correct_value_USD':str(correct_value),'corrupt_value_USD':str(corrupt_value),'difference_USD':str(correct_value-corrupt_value),
            'qualification':'Authored conversion counterexample; no actual pyagrum runtime probe.'},
        'constraints':{'no_adjacency_admissible_graphs':1,'ordered_ban_admissible_graphs':2,'required_adjacency_admissible_graphs':2,
            'meaning':'Symmetric gaps, one-direction bans and required adjacency are different predicates; two whitelist entries are not a latent bidirected edge.'}}


def sources():
    packages = {}
    for key,(repo,c,t) in FAMILIES.items():
        cp=RAW/(c+'.json');tp=RAW/(t+'.json')
        commit=json.loads(cp.read_text());commit=commit[0] if isinstance(commit,list) else commit
        tree=json.loads(tp.read_text()); date=commit['commit']['committer']['date']
        assert tree['truncated'] is False
        assert tree['sha'] in [commit['sha'],commit['commit']['tree']['sha']]
        assert datetime.fromisoformat(date.replace('Z','+00:00')) <= datetime.fromisoformat('2026-10-07T23:59:59+08:00')
        packages[key]={'repository':repo,'revision':commit['sha'],'source_date':date,
            'commit_metadata':ref(cp,'Selected cutoff-compatible commit'), 'tree':ref(tp,'Complete returned pinned tree'),
            'blobs':{x['path']:x for x in tree['tree'] if x['type']=='blob'}}
    rows=[]; failed=[]
    for p in sorted(BASE.glob('acquisition-0*.json')):
        for row in json.loads(p.read_text())['requests']:
            if 'source_path' not in row: continue
            receipt_path=RAW/(row['id']+'.receipt.json'); receipt=json.loads(receipt_path.read_text())
            if receipt['status']!='saved':
                failed.append(ref(receipt_path,'Preserved failed tree-as-commit read; corrected successor acquired'));continue
            rows.append(row)
    assert len(rows)==38 and len(failed)==8
    records=[]
    for row in rows:
        key=next(k for k,v in packages.items() if v['repository']==row['repository'])
        package=packages[key]; blob=package['blobs'][row['source_path']]
        p=RAW/(row['id']+'.'+row['extension']);rp=RAW/(row['id']+'.receipt.json')
        receipt=json.loads(rp.read_text()); data=p.read_bytes()
        sha1=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert row['pin']==package['revision'] and sha1==row['blob_sha1']==blob['sha']
        assert len(data)==blob['size']==receipt['bytes'] and core.sha(p)==receipt['sha256']
        assert receipt['url']==row['url'] and receipt['status']=='saved'
        if row['extension']=='pdf':
            anchors=[{'physical_page':1,'claim':'Official manual version1.05, January2010'},
                     {'physical_page':18,'claim':'Section3.7 explicitly states structure learning is absent in this manual/version'},
                     {'physical_page':19,'claim':'Supplied structures, EM and hidden/observed/missing masks'}]
        else:
            lines=data.decode().splitlines(); anchors=[]
            for first,last,claim in ANCHORS[row['id'].removeprefix('exec16_ct_')]:
                assert first <= len(lines)
                anchors.append({'first_line':first,'last_line':min(last,len(lines)),'claim':claim,
                    'excerpt':'\n'.join(lines[first-1:min(last,len(lines))])})
        records.append({'family':key,'source_identity':row['url'],'version_date':package['revision']+'; '+package['source_date'],
            'source_path':row['source_path'],'git_blob_sha1':sha1,'local_copy':ref(p,'Authentic pinned original'),
            'retrieval':ref(rp,'Original identity and SHA256'),'inspected_anchors':anchors,
            'supported_claims':[x['claim'] for x in anchors]})
    licenses=[]
    for name,path in [('mit','LICENSES/MIT.txt'),('lgpl','LICENSES/LGPL-3.0-or-later.txt')]:
        p=RAW/('exec13_cxx_agrum_'+name+'.txt');rp=p.with_suffix('.receipt.json');data=p.read_bytes()
        blob=packages['agrum']['blobs'][path]
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob['sha']
        assert json.loads(rp.read_text())['sha256']==core.sha(p)
        licenses.append({'source_identity':json.loads(rp.read_text())['url'],
            'version_date':packages['agrum']['revision']+'; '+packages['agrum']['source_date'],
            'local_copy':ref(p,'Inherited same-pin license original'),'retrieval':ref(rp,'License retrieval'),
            'git_blob_sha1':blob['sha'],'inspected_anchors':['License title and grant; file header selects LGPL3-or-later OR MIT']})
    sdbn_names=packages['sdbn']['blobs']
    assert len(sdbn_names)==54 and not any(Path(p).name.lower().startswith(('readme','license','licence')) for p in sdbn_names)
    prior=json.loads(PRIOR.read_text());paper=next(s for s in prior['sources'] if s['integrated_citation_key']=='exec14_pt_paper_gies')
    paper_binding=paper.get('scholarly_pdf',paper.get('local_copy'))
    if 'local_path' in paper: paper_binding={'path':paper['local_path'],'sha256':paper['sha256']}
    pdf=ROOT/paper_binding['path'];assert core.sha(pdf)==paper_binding['sha256']
    inspected=BASE/'inspected';inspected.mkdir(exist_ok=True)
    extracts=[]
    for name,original,pages in [('hauser',pdf,[5,31,33]),('mocapy',RAW/'exec16_ct_mocapy_7.pdf',[1,18,19])]:
        for page in pages:
            out=inspected/f'{name}-physical-{page}.txt'
            subprocess.run(['pdftotext','-layout','-f',str(page),'-l',str(page),str(original),str(out)],check=True,timeout=20)
            assert out.read_text().strip(); extracts.append(ref(out,'Inspected physical page '+str(page)))
    for pkg in packages.values(): pkg['tree_blob_count']=len(pkg.pop('blobs'))
    return {'scope':'Static primary-source review; no upstream runtime', 'cutoff':'2026-10-07 Asia/Shanghai',
        'packages':packages,'records':records,'inherited_license_originals':licenses,'failed_predecessors':failed,
        'paper':{'citation_key':'exec14_pt_paper_gies','inherited_record':paper,'local_copy':ref(pdf,'Genuine Hauser and Buehlmann2012 original'),
            'inspected_anchors':['Physical5: independent rows, known targets, conservative family',
                'Physical31: this application excludes uncertain-target perturbations',
                'Physical33: this paper leaves consistency open; no claim about later literature']},
        'page_extracts':extracts,
        'recovery_corrections':['Mocapy root LGPL2.1 text differs from LGPL3-or-later headers in all three inspected implementation/example files; do not assign one unqualified license.',
            'Additional sDBN header closes caller trace and exposes stdout diagnostics in the default JSON stream; static trace, not runtime observation.'],
        'limitations':LIMITS}


def omissions(primary):
    leads=[]; searches=[]
    source=RAW/'v12_sw_cell_discovery_temporal_interventional_cpp.json'
    originals=json.loads(source.read_text())['results']
    alias={};canonical={}
    for r in originals:
        title=r['title'];doi=r.get('doi');identity=doi or title.lower()
        if 'Approximate Causal Ordering' in title: identity='approximate-causal-ordering-family'
        disposition='Uninspected primary original/implementation in this cell; metadata establishes a lead only.'
        if identity in canonical:disposition='Duplicate or journal/arXiv alias of '+canonical[identity]+'; correspondence needs original review.'
        else:canonical[identity]=r['id']
        if 'causal impact' in title.lower():disposition='Adjacent intervention-effect package family already treated in CausalImpact reuse; this metadata supplies no native discovery capability.'
        leads.append({'identity':r['id'],'title':title,'doi':doi,'year':r.get('publication_year'),
            'alias_family':identity,'disposition':disposition,'evidence':ref(source,'Saved original cell query metadata')})
    inspected={p['repository'] for p in primary['packages'].values()}
    noise={'jgagneastro/mocapy','wia048/mocapy','justinjohn0306/Mocapy','mocayo/mocapy','Idelity/Mocapy','Mocapy/B-n-hack-a9','WDBO-ALGORITHM/wdbo_criterion'}
    for n in range(1,5):
        p=RAW/f'exec16_ct_search_{n}.json';rp=p.with_suffix('.receipt.json');d=json.loads(p.read_text());receipt=json.loads(rp.read_text())
        assert receipt['sha256']==core.sha(p) and receipt['status']=='saved'
        searches.append({'query':receipt['url'],'reported':d['total_count'],'returned':len(d['items']),
            'incomplete_results':d['incomplete_results'],'local_copy':ref(p,'Bounded discovery metadata'),'retrieval':ref(rp,'Search identity/date')})
        for row in d['items']:
            name=row['full_name']
            disposition=('Selected for pinned technical inspection' if name in inspected else
                'Name/topic mismatch on returned metadata; excluded from selected technical sample, not a capability finding' if name in noise else
                'Uninspected relevant or ambiguous lead; acquire pinned original, rights and method text before capability classification')
            leads.append({'identity':name,'description':row.get('description'),'reported_language':row.get('language'),
                'created_at':row['created_at'],'disposition':disposition,'evidence':ref(p,'Returned repository lead only')})
    assert len(leads)==30
    return {'status':'bounded_inconclusive','cutoff':'2026-10-07 Asia/Shanghai','leads':leads,'searches':searches,
        'inherited_query':ref(source,'Ten results, including duplicate and publication aliases'),
        'selection':'Known pcalg and aGrUM seeds plus BayesNetty, Mocapy mirror and sDBN; four bounded queries with up to10 hits each.',
        'stopping':'Stopped after five selected families and one additional sDBN caller header. First repository query reports13 but returns10; no saturation claim.',
        'limitations':['Search executed after cutoff; created-date filter limits repository age, not current indexing. Technical claims instead use inspected cutoff-compatible commits.',
            'Metadata aliases are candidate groupings, not assertions of identical technical content or native code.',
            'dbn-pp, EISALab/DBN, pdbntk and other returned leads remain uninspected. Search is not an absence certificate.',
            'Mocapy mirror and license discrepancy require provenance and per-file terms; sDBN complete tree has54 blobs with no README/LICENSE.',
            'Later GIES consistency literature has not been systematically reviewed in this cell.',
            'Full dependency/runtime closure, causal assumptions, dependent uncertainty and matched bank usefulness remain outside this source comparison.'],
        'revisit_trigger':'Acquire pinned primary methods/rights for omitted leads or broaden a documented query; resolve source-specific terms and frozen environments before prototype reuse.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','check']);args=parser.parse_args()
    if args.command=='check':
        assert exact()==json.loads((BASE/'exact-results.json').read_text())
        for name in ['source-review.json','omissions-register.json','independent-arithmetic-review.json']:
            verify_bindings(json.loads((BASE/name).read_text()))
        print('Source bindings and five exact reference families pass.');return
    primary=sources();omitted=omissions(primary);results=exact()
    write(BASE/'source-review.json',primary);write(BASE/'omissions-register.json',omitted)
    write(BASE/'exact-results.json',results)
    write(BASE/'independent-arithmetic-review.json',{'status':'pass','reviewer':REVIEWER,
        'scope':'Independent formulations within author review; not an independent institutional reviewer',
        'checks':['Gaussian covariance by both structural factorizations; intervention moments by replacing X equation',
            'Direct residual sums versus analytic Gaussian score difference',
            'Eight shock worlds versus independent-subject variance; repeated rows leave the mean unchanged',
            'Two-state path enumeration versus transition recursion and stipulated monetary value',
            'Enumeration distinguishes three graph-constraint predicates'],
        'evidence':[ref(Path(__file__),'Executed exact function'),ref(BASE/'exact-results.json','Reproducible outputs')]})
    print(json.dumps({'new_originals':len(primary['records']),'inherited_licenses':2,'leads':len(omitted['leads']),
        'failed_reads_preserved':8,'exact_families':len(results)-1,'coverage':'inconclusive'}))


if __name__=='__main__': main()
