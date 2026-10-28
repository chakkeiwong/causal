"""Recover acquired originals into finite reviewed packets without native execution."""
import ast
import hashlib
import json
from pathlib import Path
import attention_boundary_reference_20261028 as exact
from prepare_followup_program_20261028 import ROOT, ref, write
from run_followup_program_20261028 import append, load
from run_followup_program_v2_20261028 import selected

RAW = ROOT/'docs/literature/raw'


def original(req):
    p = RAW/(req['id']+'.'+req['extension'])
    rp = RAW/(req['id']+'.receipt.json')
    r = json.loads(rp.read_text()); data = p.read_bytes()
    assert r['status'] == 'saved' and r['url'] == req['url']
    assert r['sha256'] == hashlib.sha256(data).hexdigest()
    result = dict(source_identity=req['url'], local_copy=ref(p,'Acquired original'),
                  acquisition_receipt=ref(rp,'Observed acquisition and SHA-256'), accessed_utc=r['accessed_utc'])
    if 'git_blob_sha1' in req:
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob == req['git_blob_sha1']
        result.update(git_blob_sha1=blob, upstream_path=req['upstream_path'],
                      version=req['url'].split('githubusercontent.com/',1)[1].split('/')[2])
    return result


def anchors(record, spans):
    p = ROOT/record['local_copy']['path']; lines = p.read_text().splitlines()
    record['inspected_anchors'] = []
    for lo, hi, claim in spans:
        assert 1 <= lo <= hi <= len(lines), (p,lo,hi,len(lines))
        record['inspected_anchors'].append(dict(lines=[lo,hi],
            excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest(), finding=claim))
    record['supported_claims'] = [c for _,_,c in spans]
    record['native_execution'] = False
    return record


def transition(base, task, name, output, findings, next_action, evidence, outcome='pass'):
    receipt = base/(name+'-receipt.json')
    write(receipt,dict(task=task,awards_acceptance=False,execution='performed',outcome=outcome,
        outputs=[ref(output,'Reviewed finite work and explicit limits')], evidence=evidence,
        criteria=[dict(index=i,verdict='pass',finding=f) for i,f in enumerate(findings)],next_action=next_action))
    append('record',task,str(receipt.relative_to(ROOT)),ROOT,base)


def start(base, task, stem, evidence):
    assert load(ROOT,base)['active'] is None
    p=base/(stem+'-start.json')
    write(p,dict(task=task,awards_acceptance=False,next_action='Verify acquired originals, record inspected anchors and finite limits.', evidence=evidence))
    append('start',task,str(p.relative_to(ROOT)),ROOT,base)


def main():
    base=selected(); assert base.name=='followup-runtime-v4'
    names=['acquisition-plan.json','attention-followup-plan.json','attention-tree-plan.json',
           'attention-readme-plan.json','tcdf-source-plan.json','attention-primary-plan.json']
    plans={n:json.loads((base/n).read_text()) for n in names}
    requests={r['id']:r for d in plans.values() for r in d['requests']}
    custody={key:original(req) for key,req in requests.items()}
    evidence=[ref(base/n,'Preserved finite acquisition plan') for n in names]
    start(base,'ATTENTION.SEARCH','attention-search',evidence)
    queries=[]; repos={}; works={}
    for key,req in requests.items():
        if 'query' not in req: continue
        d=json.loads((ROOT/custody[key]['local_copy']['path']).read_text())
        github='items' in d; rows=d['items'] if github else d['results']
        total=d['total_count'] if github else d['meta']['count']
        ids=[]
        for row in rows:
            identity=row['full_name'].lower() if github else row['id']
            ids.append(identity)
            target=repos if github else works
            target.setdefault(identity,dict(identity=identity,title=row.get('title',row.get('full_name')),queries=[],disposition='Metadata lead; primary source not reviewed by this packet.'))['queries'].append(key)
        queries.append(dict(query=req['query'],total_reported=total,returned=len(rows),identities=ids,
            incomplete_results=d.get('incomplete_results'),evidence=custody[key],technical_claims=False))
    spans={
      'exec28_attention_readme_0':[(1,23,'Journal target and figure reproduction from recorded results; package says no LaTeX sources'),(37,48,'Training benchmarks are not rerun'),(123,126,'Academic-review statement; no general license grant established')],
      'exec28_attention_readme_1':[(1,28,'Attention/multilag scope and TCFMODEL architecture description'),(105,109,'Project states GPL-3 license')],
      'exec28_attention_readme_2':[(1,37,'Telecommunication topology/event scope and declared dependency lower bounds')],
      'exec28_attention_code_0_0':[(43,65,'Subprocess figure and PDF helpers'),(76,110,'Conditional LaTeX path requests manuscript.tex and ESM_1.tex')],
      'exec28_attention_code_1_0':[(143,175,'Softmax feature gate followed by depthwise/pointwise convolution; train is a TCFMODEL method'),(230,265,'VAL is a TCFMODEL method')],
      'exec28_attention_code_1_1':[(1,19,'Imports train and VAL directly from model_code'),(476,505,'Autocorrelation/Spearman-based lag selection'),(581,617,'Permutation loss and directional validation path')],
      'exec28_attention_code_1_2':[(1,16,'GNU GPL version 3 notice; not full transitive license clearance')],
      'exec28_attention_code_2_0':[(296,382,'Learned ordering mask,positive excitation and regularized loss'),(424,435,'NaN losses omitted; no valid batch yields zero'),(447,568,'When supplied, dag_matrix enters threshold and F1 checkpoint selection'),(590,621,'Shuffled event-pair split; absent split_ratio defaults to same train/validation pairs')],
      'exec28_attention_code_2_1':[(1,10,'Wrapper forwards optional true graph to TACD')],
      'exec28_tcdf_source_0':[(1,25,'TCDF project and primary-paper identity')],
      'exec28_tcdf_source_1':[(1,16,'GNU GPL version 3 notice; not full dependency clearance')],
      'exec28_tcdf_source_2':[(14,28,'Target shifted one period with zero initial value'),(31,79,'MSE training'),(84,132,'Attention candidate selection and one seeded permutation per candidate on training data'),(137,164,'Kernel-weight delay extraction')],
      'exec28_tcdf_source_3':[(9,33,'Softmax variable gate and imported depthwise delegate')],
    }
    sources=[anchors(custody[k],ss) for k,ss in spans.items()]
    pins=[]
    for key in ['exec28_attention_pin_0','exec28_attention_pin_1','exec28_attention_pin_2','exec28_attention_tcdf_pin']:
        d=json.loads((ROOT/custody[key]['local_copy']['path']).read_text())[0]
        date=d['commit']['committer']['date']; assert date<='2026-10-07T15:59:59Z'
        pins.append(dict(commit=d['sha'],committer_date=date,evidence=custody[key]))
    tree=json.loads((RAW/'exec28_attention_tree_0.json').read_text()); assert not tree['truncated']
    missing_tex=[n for n in ['manuscript.tex','ESM_1.tex'] if n not in {r['path'] for r in tree['tree']}]
    assert len(missing_tex)==2
    model=ast.parse((RAW/'exec28_attention_code_1_0.txt').read_text())
    definitions={n.name for n in model.body if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef))}
    imports=ast.parse((RAW/'exec28_attention_code_1_1.txt').read_text())
    requested=[a.name for n in imports.body if isinstance(n,ast.ImportFrom) and n.module=='model_code' for a in n.names]
    missing_imports=sorted(set(requested)-definitions); assert missing_imports==['VAL','train']
    static=base/'attention-static-inspection.json'
    write(static,dict(status='pass',inspection='AST and repository-tree text only; no imported original code',
        camcns_top_level_definitions=sorted(definitions),camcns_requested_imports=requested,missing_top_level_definitions=missing_imports,
        causal_transformer_missing_tex=missing_tex,evidence=[custody[k] for k in ['exec28_attention_tree_0','exec28_attention_code_1_0','exec28_attention_code_1_1']]))
    paperreq=requests['exec28_inverted_paper_v1']; paper=ROOT/'docs/papers'/(paperreq['title']+' Liu(2026).pdf')
    assert paper.read_bytes()==(RAW/'exec28_inverted_paper_v1.pdf').read_bytes()
    pages=(base/'inverted-primary.txt').read_text().split('\f')
    paperrecord=dict(title=paperreq['title'],edition='arXiv2607.28212v1;2026-07-30',local_copy=ref(paper,'Genuine versioned primary PDF'),
        acquisition=custody['exec28_inverted_paper_v1'],identity=custody['exec28_attention_inverted_identity'],
        extracted_text=ref(base/'inverted-primary.txt','Inspected primary text'),
        inspected_anchors=[dict(physical_page=p,excerpt_sha256=hashlib.sha256(pages[p-1].encode()).hexdigest(),finding=f) for p,f in [
            (1,'Title,authors and versioned primary identity'),(4,'Granger DAG,Markov,faithfulness,strict i<j ordering and bounded signal assumptions'),
            (7,'Aggregated attention and top-k potential graph; permutation with other variables held fixed'),(8,'Fixed-network loss comparison and declared experimental environment')]],
        edition_limit='2025 proceedings metadata is a separate edition; identity/content equivalence not established.',native_execution=False)
    witness=base/'attention-exact-results.json';write(witness,exact.calculate())
    omissions=base/'attention-omissions.json'
    write(omissions,dict(status='local_source_limits',cutoff='2026-10-07T15:59:59Z',candidates=[
        dict(title='Causal Discovery with Attention-Based Convolutional Neural Networks',first_author='Nauta',year=2019,doi='10.3390/make1010019',
             inspected='Selected pinned TCDF source only; scholarly primary PDF not acquired.',reason='Current fixed collector excludes discovered MDPI/University of Twente hosts; prior local filename search found no matching original.',
             next_action='Locate a lawful matching original on an already permitted repository or obtain a separately approved bounded source route; inspect before scholarly citation.'),
        dict(title='Causal Discovery by Graph Attention Reinforcement Learning',first_author='Yang',year=2023,doi='10.1137/1.9781611977653.ch4',
             inspected='Metadata identity lead only.',reason='No genuine primary PDF acquired in this finite search.',next_action='Resolve author repository/preprint identity and acquire original through permitted collector route.')],
        limitations='Local acquisition limits do not imply universal unavailability; no agent summary substituted.'))
    for identity,decision in {
        'sgao-academics/causaltransformer':'Selected source supports figure reproduction scope; training implementation/publication status and rights unresolved; defer adapter.',
        'nicoirribarra/camcns-causal-discovery':'Selected static namespace mismatch and feature-gate architecture; conditional research comparison after source repair/fixtures and license intake.',
        'aquariuaa/tacd':'Event/topology specialist; separate oracle-guided model selection,missingness and temporal split contracts; defer native adapter.',
        'm-nauta/tcdf':'Selected code supports candidate gating/permutation/delay mechanics; paper/depthwise delegate and calibration unresolved; conditional comparison only.'}.items():
        assert identity in repos;repos[identity]['disposition']=decision
    out=base/'attention-search.json'
    write(out,dict(status='performed_bounded_primary_review',cutoff='2026-10-07T15:59:59Z',queries=queries,
        unique_repository_metadata_candidates=len(repos),unique_scholarly_metadata_candidates=len(works),
        deduplication='Repository owner/name casefold and OpenAlex work id separately; do not add provider totals.',
        repository_candidates=list(repos.values()),scholarly_candidates=list(works.values()),
        search_limits=['Finite top20 pages; metadata can postdate cutoff; not saturation.','Only selected pinned originals support technical findings.','Earlier gCastle attention is preserved,not treated as all attention discovery families.'],
        selected_sources=sources,cutoff_pins=pins,additional_identity_custody=[v for k,v in custody.items() if 'tree' in k],
        primary_papers=[paperrecord],static_inspection=ref(static,'Namespace/tree inspection'),
        authored_witness=ref(witness,'Exact marginal,joint,temporal and intervention distinctions'),reference=ref(Path(exact.__file__),'Independent arithmetic'),
        omissions=ref(omissions,'Two unavailable original-source candidates'),full_family_coverage='inconclusive',
        next_actions=['Inspect TCDF depthwise delegate and exact temporal padding boundaries.','Inspect TACD configuration/scorer delegates before asserting selected defaults.','Integrate reviewed evidence and exact permutation witness into preserving reader/sponsor successor.','Resolve remaining metadata candidates and omitted primary papers without treating finite work as coverage completion.'],
        evidence=evidence+[ref(Path(__file__),'Finite review implementation')],native_execution=False))
    transition(base,'ATTENTION.SEARCH','attention-search',out,[
        'Six bounded queries retain provider/returned/unique denominators,duplicate keys and metadata/cutoff limits.',
        'Four selected repositories and one genuine preprint have pinned originals,inspected anchors and precise adoption/access limits; full coverage stays inconclusive.'
    ],'Complete independent CDT installer packet,deliver pending RL publication,then execute source delegates and attention integration.',evidence)
    start(base,'CDT.INSTALLER','cdt-installer',[ref(base/'acquisition-plan.json','Pinned source request')])
    installer=anchors(custody['exec28_cdt_installer'],[(3,11,'Unversioned OS package install; several allow-unauthenticated options'),
        (12,15,'Unversioned HTTP CRAN installs,HTTP biocLite source and unpinned GitHub package installation')])
    out=base/'cdt-installer.json'
    write(out,dict(status='performed_bounded_primary_review',source_records=[installer],native_execution=False,
        immediate_remote_delegates=[dict(identity='http://bioconductor.org/biocLite.R',status='Not fetched or executed; mutable unpinned script'),
            dict(identity='CRAN and GitHub package installation hooks',status='Unresolved versioned/transitive source and rights closure')],
        findings=['A pinned installer does not pin its package resolution or remote scripts.','The inspected source cannot reconstruct a historical resolved environment.','No inference that current package versions/licenses equal historical ones.'],
        proposed_replacement=['Declare OS/R/compiler and package versions plus immutable archive/content digests.','Acquire lawful original sources over verified HTTPS using reviewed bounded routes; inspect selected delegates and component terms.','Prepare an isolated public-fixture execution protocol with resolved dependencies,logs and complete failed-request denominator before native enablement.'],
        outcome_scope='Installer source review complete; reproducible dependency closure and native adoption inconclusive.',
        evidence=[ref(base/'acquisition-plan.json','Original acquisition contract'),ref(Path(__file__),'Exact source-only review')]))
    transition(base,'CDT.INSTALLER','cdt-installer',out,[
        'All15lines of pinned original verified against collector SHA-256 and Git blob; package sources and absent pins recorded.',
        'Immediate mutable remote script/package delegates and component/runtime limits explicit; none fetched or executed.'
    ],'Prepare immutable resolved-environment intake and continue independent source integration; do not run historical installer.',evidence[:1])
    print(json.dumps(dict(status='pass',source_records=len(sources),papers=1,repository_candidates=len(repos),scholarly_candidates=len(works),states=load(ROOT,base)['states'])))


if __name__=='__main__':main()
