#!/usr/bin/env python3
"""Audit pinned discovery paths and reproduce exact proposal examples."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import run_program as control
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = control.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-14/iid-discovery'
OP = 'LL.TASK.iid_discovery'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'task-synthesis.md'
AUDIT = ROOT / 'docs/program/execution/2026-10-14/causica-reuse/publication/reader/source-audit.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Primary literature outcomes are author-reported; selected static paths and independent calculations are not upstream execution or live LLM performance.',
    'The two Gaussian worlds are a stipulated comparison, not an exhaustive identified set or a confidence set.',
    'A title search recovered candidate58 after metadata exposed no open PDF; candidate27 original, wider search coverage and whole-dependency rights remain open.',
    'Notebook dependencies are not locked; the later inspected LiNGAM source is a proposed integration target, not the historical notebook environment.',
    'No adapter, graph/effect calibration, bank qualification or ROI is awarded; rendered visual acceptance remains open.']


def exact():
    def covariance(loadings, variances):
        return [[sum((a*b*v for a,b,v in zip(x,y,variances)), F(0))
                 for y in loadings] for x in loadings]
    direct = covariance([[F(1), F(0)], [F(1,2), F(1)]], [F(2), F(3,2)])
    hidden = covariance([[F(1),F(1),F(0)], [F(1),F(0),F(1)]], [F(1)]*3)
    assert direct == hidden == [[2,1],[1,2]]
    assert direct[0][0]*direct[1][1]-direct[0][1]**2 == 3
    effects = [F(1,2), F(0)]
    net = [200*t-60 for t in effects]
    assert net == [40,-60]
    decisions=[]
    for p in [F(9,10),F(1,2),F(2,5)]:
        mixture=p*net[0]+(1-p)*net[1]
        current=max(F(0),mixture)
        perfect=p*max(F(0),net[0])+(1-p)*max(F(0),net[1])
        decisions.append({'assumed_direct_world_probability':str(p),
            'net_action':str(mixture),'best_current':str(current),
            'perfect_information_value':str(perfect-current)})
    assert [d['net_action'] for d in decisions]==['30','-10','-20']
    assert [d['perfect_information_value'] for d in decisions]==['6','20','16']
    boundary=[]
    for p in [F(49,1000),F(1,20),F(19,20),F(951,1000)]:
        code=0 if p<F(1,20) else 1 if p>F(19,20) else -1
        paper=0 if p<F(1,20) else 1 if p>=F(19,20) else -1
        exact_search=0 if p<F(1,20) else 1
        boundary.append({'score':str(p),'notebook_pk':code,'paper_pk':paper,
                         'notebook_exact_search_allowed':exact_search})
    assert [b['notebook_pk'] for b in boundary]==[0,-1,-1,1]
    token_cases=[]
    for token in ['Yes',' Yes']:
        atoms=[(token,F(24,25)),('No',F(1,50)),('\n',F(1,100)),('I',F(1,200)),('It',F(1,200))]
        assert sum(p for _,p in atoms)==1
        extracted=sum((p for t,p in atoms if t in ['Yes','yes']),F(0))
        normalized=sum((p for t,p in atoms if t.strip().lower()=='yes'),F(0))
        token_cases.append({'token':token,'authored_first_token_distribution':[(t,str(p)) for t,p in atoms],
            'literal_yes_score':str(extracted),'normalized_yes_score':str(normalized),
            'pk':0 if extracted<F(1,20) else 1 if extracted>F(19,20) else -1})
    assert [c['pk'] for c in token_cases]==[1,0]
    # Independent tiny graph calculation; no copied library code is executed.
    edges={(0,1),(1,2)}
    reachable=set(edges)
    for _ in range(3):reachable|={(a,d)for a,b in reachable for c,d in reachable if b==c}
    assert (0,2) in reachable and (0,2) not in edges
    return {'kind':'independent_exact_project_references','random_draws':0,'upstream_execution':False,'model_calls':0,
        'gaussian':{'direct_loadings':[['1','0'],['1/2','1']],'direct_innovation_variances':['2','3/2'],
            'hidden_loadings':[['1','1','0'],['1','0','1']],'hidden_innovation_variances':['1','1','1'],
            'common_covariance':[[str(v)for v in row]for row in direct],
            'common_covariance_determinant':'3','common_regression_slope':'1/2',
            'effects':[str(t)for t in effects],'unit_action_net_USD':[str(n)for n in net],
            'decision_scenarios':decisions,'forced_selection_bound':'For common data law and direct-selection probability q, success probabilities are q and1-q; minimum at most1/2.',
            'scope':'Independent units, centered Gaussian variables, faithful stipulated worlds, no interference; latent sufficiency differs; known order A before Y holds in both.'},
        'threshold_comparison':boundary,'lexical_score_cases':token_cases,
        'ancestry_case':{'direct_edges':[[a,b]for a,b in sorted(edges)],'reachable_pairs':[[a,b]for a,b in sorted(reachable)],
            'absent_direct_0_to_2':True,'absent_path_0_to_2':False},
        'source_trace_cases':[
            {'case':'GPTIndependenceTest missing stored row','literal_return':0,'meaning':'Numeric value does not distinguish unavailable evidence from a dependence decision.'},
            {'case':'GPTIndependenceTest wvot with a stored row','literal_return':0,'meaning':'Selected branch is an unimplemented TODO; no weighted vote is calculated.'},
            {'case':'Hybrid driver configured illustrative-model-B at temperature0.2','stored_model':'gpt-3.5-turbo','stored_temperature':'0.6','meaning':'Static assignment differs from runtime argument fields; no call executed.'}],
        'qualification':'No statistical or integration capability; examples define proposed acceptance cases.'}


def main():
    assert OUTPUT.exists() and not (BASE/'operation-receipt.json').exists()
    mapping={s['integrated_citation_key']:s for s in json.loads(AUDIT.read_text())['sources']}
    plan=json.loads((BASE/'acquisition-plan.json').read_text())
    package_records=[]
    descriptions={
        'gpt':('causal_gpt', '2024', 'IPL-UV causal GPT contributors',
            ['gpt_ci.py:565-654: response-proportion formula, cached-row aggregation, wvot TODO and missing return.',
             'PC_GPT.py:main: metadata and saved answers passed to PC; endpoints serialized separately.',
             'HybridPC_GPT.py:126-229: numerical fallback, pending query collection, one-pass driver and hardcoded result metadata.',
             'evaluate_cis.py: comparison uses graph-implied d-separation and answer records; not independent target-bank truth.']),
        'cd':('llm_cd','2025','LLM-CD contributors',
            ['prior_evaluation.py:check_GPT_prior and Path_graph_metric: parsed relations assessed as directed paths against supplied truth.',
             'CaMML_perform.py:67-100: ancestral => versus edge -> serialization; unchecked shell call and shared output paths.',
             'MINOBSx_perform.py:45-75: distinct absent-edge/order/ancestral blocks; unchecked return then parse/remove.',
             'utils.py and prior_accept_evaluation.py: saved result parsing and constraint-acceptance evaluation.']),
        'scd':('llm_scd','2024','Masataka Takayama and contributors',
            ['Five original notebooks; code-only derivatives retain original cell numbers and omit all saved output payloads.'])}
    for stem,repo,pin,paths in plan['packages']:
        oldstem,year,author,anchors=descriptions[stem]
        treepath=ROOT/f'docs/literature/raw/v12_la_{oldstem}_tree.json'
        tree=json.loads(treepath.read_text());assert tree['sha']==pin and not tree['truncated']
        blobs={x['path']:x['sha']for x in tree['tree']if x['type']=='blob'}
        records=[]
        for i,path in enumerate(paths,1):
            ext='json'if path.endswith('.ipynb')else'txt'
            local=ROOT/f'docs/literature/raw/exec14_iid_{stem}_{i}.{ext}'
            data=local.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert blob==blobs[path]
            record={'source_identity':f'https://raw.githubusercontent.com/{repo}/{pin}/{path}',
                'local_copy':ref(local,'Pinned original source; no execution'),'git_blob_sha1':blob,
                'receipt':ref(local.with_suffix('.receipt.json'),'Observed successful public acquisition')}
            if ext=='json':
                notebook=json.loads(data)
                expected='\n\n'.join('# Notebook cell '+str(j)+'\n'+''.join(c['source'])for j,c in enumerate(notebook['cells'])if c['cell_type']=='code')
                derivative=BASE/f'scd-{i}-code.txt';assert derivative.read_text()==expected
                record['code_only_derivative']=ref(derivative,'Original code cells; never executed')
            records.append(record)
        if stem=='gpt':
            p=ROOT/'docs/literature/raw/v12_la_causal_gpt_source_1.txt';data=p.read_bytes()
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==blobs['gptci/gpt_ci.py']
            records.append({'source_identity':f'https://raw.githubusercontent.com/{repo}/{pin}/gptci/gpt_ci.py',
                'local_copy':ref(p,'565-748: complete selected PC interfaces'),'git_blob_sha1':blob})
        inherited=mapping['v12_la_package_'+oldstem]
        package_records.append({'id':stem,'repository':repo,'revision':pin,'source_date':inherited['commit_date'],
            'tree':ref(treepath,'Complete pinned tree'),'records':records,'inspected_anchors':anchors,
            'inherited_identity_and_rights':inherited,'rights':inherited['license_scope'],'author':author,'year':int(year)})
    paper_specs=[
        ('v12_la_2402_15301','2402.15301',[4,5,8],['Retrieval helps some benchmarks and harms others; orientation on true-positive edges is a restricted denominator.']),
        ('v12_la_2406_07378','2406.07378',[3,5,8],['Response tests concern prompted answers; permutation agreement and data-only superiority on SACHS delimit reported findings.']),
        ('v12_la_2405_13551','2405.13551',[3,4,8,9],['Soft search priors retain possibilities but are not effect confidence; MI alone wins Child in the reported comparison.']),
        ('v12_la_2402_01454','2402.01454',[9,13,58,62,63],['Paper transformation uses >=alpha2 unlike strict notebook threshold; statistical prompting has both gains and losses; cyclic conversion and model selection require validation.']),
        ('v12_la_2407_15073','2407.15073',[5,7],['Algorithm choice/coding and debate consume different evidence; more rounds can degrade results, reported token consumption16-25 times baselines.']),
        ('v12_la_2407_19638','2407.19638',[3,8,9],['Accessible-corpus study and context experiments support novelty/metadata controls with closed-model and semantic limitations.']),
        ('v12_la_2306_16902','2306.16902',[4,5],['Ancestral priors and approximate path factorization differ from edge restrictions; prior strength is problem dependent.'])]
    rereads=[];(BASE/'inspected').mkdir(exist_ok=True)
    for key,stem,pages,claims in paper_specs:
        p=ROOT/f'docs/program/repair-v12/work/LA01/extracted/{stem}.txt'
        texts=p.read_text().split(chr(12));anchors=[]
        for page in pages:
            out=BASE/'inspected'/f'{stem}-page-{page}.txt'
            with out.open('x')as f:f.write(texts[page-1])
            anchors.append(ref(out,f'Physical PDF page{page}'))
        source=mapping[key];assert hashlib.sha256((ROOT/source['local_path']).read_bytes()).hexdigest()==source['sha256']
        rereads.append({'citation_key':key,'preserved_source':source,'primary_text':ref(p,'Genuine PDF extraction'),
                       'inspected_anchors':anchors,'supported_claims':claims})
    inherited_reviews=[ref(ROOT/'docs/program/execution/2026-10-14/expert-evidence/primary-review.json','Sng and2026 ABAPC-LLM original claims and adverse results'),
        ref(ROOT/'docs/program/execution/2026-10-14/l7-benchmarking/frontier/primary-review.json','Benchmark original identities and denominators'),
        ref(ROOT/'docs/program/repair-v12/work/LA03/response-count-derivation.json','Previously verified response-count example; no new discovery credit')]
    baseline=mapping['v13_sw_lingam'];verify_bindings(baseline)
    metadata=ROOT/'docs/literature/raw/exec14_iid_materials_metadata.xml'
    ns={'a':'http://www.w3.org/2005/Atom'}
    entry=ET.fromstring(metadata.read_text()).find('a:entry',ns)
    assert entry.findtext('a:id',namespaces=ns).endswith('2503.13833v1')
    date=entry.findtext('a:updated',namespaces=ns);assert date<'2026-10-07T16:00:00Z'
    title='Causal Discovery from Data Assisted by Large Language Models'
    assert entry.findtext('a:title',namespaces=ns)==title
    raw=ROOT/'docs/literature/raw/exec14_iid_materials_original.pdf'
    pdf=ROOT/'docs/papers'/f'{title} Barakati(2025).pdf'
    data=raw.read_bytes();assert data.startswith(b'%PDF-')
    if pdf.exists():assert pdf.read_bytes()==data
    else:pdf.write_bytes(data)
    texts=(BASE/'materials.txt').read_text().split(chr(12));assert 'Kamyar Barakati' in texts[0]
    anchors=[]
    for page in [1,3,4,5,6,7,8,9,10,11,12]:
        out=BASE/'inspected'/f'materials-page-{page}.txt'
        with out.open('x')as f:f.write(texts[page-1])
        anchors.append(ref(out,f'Physical PDF page{page}'))
    materials={'integrated_citation_key':'exec14_iid_materials','kind':'paper','title':title,'filename_title':title,
        'authors':[a.findtext('a:name',namespaces=ns)for a in entry.findall('a:author',ns)],
        'first_author':'Barakati','year':2025,'source_identity':'https://arxiv.org/pdf/2503.13833v1',
        'version_date':'arXiv2503.13833v1; '+date,'local_path':str(pdf.relative_to(ROOT)),
        'sha256':hashlib.sha256(data).hexdigest(),'pages':15,'local_copy':ref(pdf,'Genuine author original'),
        'metadata':ref(metadata,'Identity/version only; original title and authors checked'),
        'acquisition':ref(raw.with_suffix('.receipt.json'),'Successful version-specific public PDF request'),
        'inspected_anchors':anchors,'extracted_text':ref(BASE/'materials.txt','Primary original extraction'),
        'supported_claims':['Materials application uses STEM-derived unit-cell descriptors and prior published observations.',
            'Detailed method describes gCastle PC, LangChain ChatOpenAI GPT4-turbo, literature terminology and pairwise graph restrictions with an insufficient-information state.',
            'Abstract says fine-tuning but inspected method gives querying; no checkpoint/training recipe established by these anchors.',
            'The comparison is principally qualitative graph/pathway agreement; inspected results do not establish calibrated intervention-effect uncertainty.',
            'PDF page12 links to Kamyar-V2/Causal_LLM; link exists although plain extraction displays only GitHub. Repository is a reuse lead, not reviewed execution.'],
        'limits':['Author original is distinct from the later publisher version; no equivalence inferred.',
            'Spatial unit-cell observations are not established iid replications by the inspected text; bank transfer is a proposal interpretation.']}
    primary={'cutoff':'2026-10-07 Asia/Shanghai','packages':package_records,'reread_papers':rereads,'new_papers':[materials],
        'inherited_reviews':inherited_reviews,'lingam_target':baseline,
        'lingam_source':ref(ROOT/'docs/literature/raw/v12_gap3_lingam_technical.txt','26-49: constructor and path restriction semantics at later pinned target'),
        'scd_inspected_code':[
            ref(BASE/'scd-2-code.txt','Initial discovery and bootstrap paths'),
            ref(BASE/'scd-3-code.txt','254-325: data prompting;565-618:model calls;868-950:first-token score collection'),
            ref(BASE/'scd-4-code.txt','88-115: thresholds;216-253:endpoints and background knowledge;255-393:PC, exact search, LiNGAM calls'),
            ref(BASE/'scd-5-code.txt','42-71:cycle removal;151-172:fit and BIC selection; positional X is passed as random_state in later target signature'),
            ref(BASE/'scd-1-code.txt','Graph metric definitions; saved outputs are not local results')],
        'scope':'Static original inspection and exact references; no downstream package execution.'}
    write(BASE/'primary-review.json',primary)
    write(BASE/'exact-results.json',exact())
    candidates=[]
    census=json.loads((ROOT/'docs/program/execution/2026-10-13/llm-census/census-register.json').read_text())
    for r in census['items']:
        if 'iid_discovery'not in r.get('task_families',[]):continue
        row={'id':r['id'],'title':r.get('title',r['id']),'inherited_disposition':r.get('disposition'),'technical_source_review_open':r.get('technical_source_review_open',True)}
        if r['id']=='LA01-candidate-58':
            row.update(disposition='author_original_acquired_and_inspected',technical_source_review_open=False,
                source=materials['local_copy'],source_key=materials['integrated_citation_key'],
                metadata_no_copy_observation=ref(ROOT/'docs/literature/raw/exec14_iid_candidate_58.json','Preserved metadata miss'),
                search=ref(BASE/'acquisition-02-plan.json','Targeted title search recovered arXiv lead'),
                next_action='Inspect linked repository at a cutoff-compatible pin before runtime/rights claims; publisher-version differences remain unreviewed.')
        elif r['id']=='LA01-candidate-27':
            n=r['id'].rsplit('-',1)[1];p=ROOT/f'docs/literature/raw/exec14_iid_candidate_{n}.json';m=json.loads(p.read_text())
            row.update(disposition='open_original_not_acquired',metadata=ref(p,'Discovery/identity only; no original claim'),
                observation={'title':m['title'],'publication_date':m['publication_date'],'open_access':m['open_access'],
                             'pdf_locations':[l.get('pdf_url')for l in m['locations']if l.get('pdf_url')]},
                limitation='This lookup reports no open copy; it does not prove the original unavailable. Publisher text was not acquired.',
                next_action='Find a lawful author/repository original or obtain an authorized original; inspect version/method/results before citation.')
        elif r['id']in ['LA01-candidate-10','LA01-candidate-213']:
            row.update(disposition='subsequent_primary_review_retained',technical_source_review_open=False,evidence=inherited_reviews[0])
        elif r['id']in ['LA01-candidate-104','LA01-candidate-108']:
            row.update(disposition='subsequent_primary_review_retained',technical_source_review_open=False,evidence=inherited_reviews[1])
        else:
            row.update(disposition=r.get('disposition','open'),next_action=r.get('next_action','Retain inherited review limits.'))
        candidates.append(row)
    write(BASE/'candidate-reassessment.json',{'scope':'Every iid-tagged inherited census item reassessed against selected later reviews; not a new exhaustive search.',
        'prior':ref(ROOT/'docs/program/execution/2026-10-13/llm-census/census-register.json','Frozen census'),
        'items':candidates,'closure':'No search saturation or whole-task frontier completeness claimed.'})
    write(BASE/'prototype-contract.json',{
        'status':'proposed_design_not_registered_or_executed','scope':'Public/generated mechanism and semantic-adapter qualification before bank spending',
        'truth':'Keep mechanism/latent/graph/effect oracles outside model prompts; independent reference calculations.',
        'split_unit':'Mechanism family, with repeated samples, descriptions and prompts nested; no graph-family reuse across development/final evaluation.',
        'arms':['Data-only PC under sufficiency','Data-only FCI under allowed latent confounding','Score search and non-Gaussian methods only within matched assumptions',
                'No-language dictionary/clock baseline','Language only','Soft guidance with predeclared weight','Hard guidance with refusal and inconsistency traces'],
        'crossed_controls':['Natural, neutral renamed and deliberately misleading labels with declared fixed-world semantics',
            'No retrieval, applicable originals, wrong-domain and contradictory retrieval',
            'Variable/order paraphrases and bounded repeats; identical numerical data and sample-budget comparison'],
        'metrics':['All-request class/endpoint retention and validity','Conditional identified effect-set retention/width and loss under known truth',
            'Action regret and availability including refusal/error denominators','Tokens, retries, latency, numerical resources and human review'],
        'mandatory_adapter_cases':['Missing stored answer remains unknown','Weighted-vote TODO refuses unsupported method','Runtime model/revision/settings match result record',
            'Token variants and missing mass remain explicit; token score not scientific confidence','Boundary0.05/0.95 version-specific tests',
            'Absent edge versus absent path in a three-node chain','Cyclic/conflicting constraints and conversion refusal',
            'Preserve CPDAG/PAG endpoint distinctions and return all failed requests'],
        'registration_before_final_runs':['Pin implementations, environment, rights and backend revision','Freeze all targets, splits, sample sizes, repeats and numerical tolerances',
            'Use development profiling only to set resource caps; declare fixed stopping and budget','Freeze primary paired mechanism-level comparisons and multiplicity treatment'],
        'success':'Scoped information/decision benefit versus matched baseline under predeclared risk/cost limits; no generic LLM superiority claim.',
        'economic_limit':'USD6 per decision is an illustrative perfect-information upper bound at assumed world probability0.9, not an experiment value or bank budget.'})
    sources=[materials]
    claims={
        'gpt':['Saved-row pooling returns numeric0/1; missing answers and wvot TODO return0.','Hybrid driver has numerical fallback and pending queries, but stores fixed model/temperature metadata.'],
        'cd':['Selected parsers evaluate ancestral reachability; backend wrappers serialize ancestral, order and absent-edge inputs separately.','Unchecked shell status, shared paths and incomplete root rights require a new bounded adapter before adoption.'],
        'scd':['Selected notebook converts first-token top-five Yes/yes mass through strict0.05/0.95 thresholds.','PC/exact-search/LiNGAM impose different constraints; paper and notebook differ at0.95.','Unpinned notebook dependency and later LiNGAM path semantics/constructor require versioned compatibility checks.']}
    for p in package_records:
        sources.append({'integrated_citation_key':'exec14_iid_'+p['id'],'kind':'software_primary_sources',
            'title':p['repository']+' pinned discovery workflow sources','author':p['author'],'year':p['year'],
            'version_date':p['revision']+'; '+p['source_date'],'source_identity':'https://github.com/'+p['repository']+'/tree/'+p['revision'],
            'local_copy':ref(BASE/'primary-review.json','Hash-verified originals, anchors and bounded findings'),
            'local_sources':[x['local_copy']for x in p['records']],
            'inspected_anchors':p['inspected_anchors'],'supported_claims':claims[p['id']],
            'limits':LIMITS,'license_scope':p['rights']})
    sources.append({'integrated_citation_key':'exec14_iid_oracle','kind':'project_derivation',
        'title':'Exact Gaussian ambiguity, decision value and language-constraint conversion references',
        'author':'Causal banking proposal','year':2026,'version_date':'2026-10-14',
        'source_identity':'Project-authored exact rational constructions',
        'local_copy':ref(BASE/'exact-results.json','Exact covariance, effects, costs, tokens and boundary cases'),
        'inspected_anchors':['gaussian','threshold_comparison','lexical_score_cases','ancestry_case','source_trace_cases'],
        'supported_claims':['Identical nonsingular Gaussian laws can yield effects0 and0.5 under different allowed latent assumptions.',
            'Stipulated action values40/-60USD and perfect-information values6/20/16USD at specified world weights.',
            'Literal token variants and threshold boundaries give different constraint outcomes; absent direct edge differs from absent path.'],
        'records':[ref(Path(__file__).resolve(),'Independent exact arithmetic; no upstream execution')],'limits':LIMITS})
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources,'inherited_record_policy':'Preserve577 prior records byte-for-byte.'})
    evidence=[ref(p,a)for p,a in [(OUTPUT,'Connected iid-discovery synthesis'),(BASE/'plan-review.md','Reviewed task plan'),
        (BASE/'primary-review.json','Primary methods, reported gains/adverse findings and complete selected code paths'),
        (BASE/'exact-results.json','Independent exact examples'),(BASE/'candidate-reassessment.json','Current dispositions and omissions'),
        (BASE/'prototype-contract.json','Proposed public/generated qualification'),(BASE/'source-audit.json','Five additional source records'),
        (Path(__file__).resolve(),'Exact verification and review procedure')]]
    findings=['Primary alternatives and adverse findings compared, with three traced package families and retained omissions.',
        'Clock-compatible Gaussian worlds have identical observed laws and effects0/0.5; costs and perfect-information limits are conditional scenarios.',
        'Missing-answer, token/threshold, constraint-type and metadata examples define concrete prototype remedies without live-performance claims.']
    write(BASE/'author-review.json',{'status':'pass','scope':'Scoped proposal synthesis; no exhaustive frontier or runtime acceptance',
        'reviewer':REVIEWER,'findings':findings,'evidence':evidence,'limitations':LIMITS,'visual_acceptance':False})
    state=control.core.read(ROOT,control.core.STATE);graph,_,_=control.combined(ROOT,state)
    node=control.ledger.operation(graph,OP);receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope='Primary-source iid-discovery proposal and explicit adapter/prototype remedies',
        reviewer=REVIEWER,limitations=LIMITS,outputs=[ref(OUTPUT,'Reviewed task synthesis')],
        nonexecution_reason='',revisit_trigger='New accessible originals or a registered matched implementation study.',
        criteria=[{'index':i,'verdict':'pass','finding':finding,'evidence':evidence}for i,finding in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'status':'pass','source_blobs':sum(len(p['records'])for p in package_records),
        'reread_papers':len(rereads),'additional_records':len(sources),'candidate_items':len(candidates),'upstream_execution':False}))


if __name__=='__main__':main()
