#!/usr/bin/env python3
"""Bind expert-evidence primary readings and exact banking/consensus references."""
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import build_native_evaluation_reader_v3_20261014 as schema
import master_control as core
import run_program as control
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-14/expert-evidence'
RAW = ROOT/'docs/literature/raw'
SYN = ROOT/'docs/program/comprehensive-v14/work/LL.TASK.expert_evidence/task-synthesis.md'
PIN = '66f2d59b0cf74dfabf0a83704bd1de708f8520ac'
REVIEWER = {'name':'Codex author/coordinator','kind':'author'}


def calculate():
    observed_a, observed_b = defaultdict(F), defaultdict(F)
    for z in (0,1):
        for error,p_error in [(0,F(3,4)),(1,F(1,4))]:
            observed_a[z,z ^ error] += F(1,2)*p_error
            observed_b[z ^ error,z] += F(1,2)*p_error
    assert observed_a == observed_b == {(0,0):F(3,8),(0,1):F(1,8),(1,0):F(1,8),(1,1):F(3,8)}
    means_a = [F(1,4),F(3,4)]
    means_b = [F(1,2),F(1,2)]
    effects = [means_a[1]-means_a[0],means_b[1]-means_b[0]]
    net = [100*x-20 for x in effects]
    assert effects == [F(1,2),F(0)] and net == [F(30),F(-20)]
    err=F(1,5)
    wrong=err**5
    agree=err**5+(1-err)**5
    assert wrong == F(1,3125) and agree == F(41,125) and wrong/agree == F(1,1025)
    duplicated = F(4**5,1+4**5)
    assert duplicated == F(1024,1025)
    return {'kind':'exact_project_derivations','package_execution':False,'model_calls':0,'random_draws':0,
        'banking':{'population':'Stipulated eligible collection accounts at decision time0',
            'clock':'Offer A at0; repayment indicator Y at30days; latent pre-offer U is unavailable',
            'world_A':'A~Bernoulli(1/2),E~Bernoulli(1/4) independent,Y=A xor E',
            'world_B':'U~Bernoulli(1/2),E~Bernoulli(1/4) independent,A=U xor E,Y=U',
            'observed_joint_both':{f'A={a},Y={y}':str(p) for (a,y),p in sorted(observed_a.items())},
            'intervention_means_A':list(map(str,means_a)), 'intervention_means_B':list(map(str,means_b)),
            'risk_difference_by_world':list(map(str,effects)), 'payment_USD':'100','contact_cost_USD':'20',
            'net_offer_value_USD':list(map(str,net)),
            'restricted_two_model_effect_set':['0','1/2'],'restricted_two_model_net_set':['-20','30'],
            'limits':'Restricted imposed two-model set, not a sharp identified set over every compatible SCM or bank data.'},
        'duplicate_sources':{'prior_probability':'1/2','stipulated_likelihood_ratio':'4',
            'one_independent_source_posterior':'4/5','five_copies_correct_posterior':'4/5',
            'five_copies_wrongly_independent_posterior':str(duplicated),
            'scope':'Illustrative known likelihood ratios; a citation count does not supply a likelihood ratio.'},
        'five_call_binary_consensus':{'marginal_error':'1/5',
            'independent_all_wrong':str(wrong),'independent_agreement_probability':str(agree),
            'independent_error_given_agreement':str(wrong/agree),
            'perfectly_shared_error_all_wrong':'1/5','perfectly_shared_agreement_probability':'1',
            'perfectly_shared_error_given_agreement':'1/5',
            'scope':'Two stipulated dependence laws with identical marginal error; no actual LLM performance estimate.'}}


def main():
    assert SYN.exists() and not (BASE/'operation-receipt.json').exists()
    inherited_path = ROOT/'docs/program/repair-v12/work/LA01/source-audit.json'
    inherited = {s['id']:s for s in json.loads(inherited_path.read_text())['sources']}
    readings = [
        ('v12_la_2402_15301','extracted text304-374,380-505; Algorithm1,Table1,Sections3.2-4.3',
         ['Unknown individual answers leave S unchanged, but S<=0 deletes the edge; all unknown therefore does not preserve uncertainty.',
          'ASIA skeleton F1 is1 for background and0.727 with documents; results vary across benchmarks.',
          'Conditional orientation accuracy among true-positive skeleton edges is not full graph accuracy.']),
        ('v12_la_2405_13551','extracted text198-235,650-695; Sections3.2 and5,Table2',
         ['Queries both variable orders, averages soft judgments and combines them with MI priors.',
          'Selected combined priors improve SHD; LLM-only priors are not consistently helpful and MI alone is strongest on Child.']),
        ('v12_la_2402_07770','extracted text325-400; Sections4.1-5',
         ['Some elicited priors conflict with data; KNN/random-forest imputation provide substantive alternatives.',
          'Ambiguous metadata/units and public-dataset recognition limit generalization.']),
        ('v12_la_2609_30867','extracted text365-475,515-544; Sections5.1-5.6',
         ['ARGUS audits reported evidence adequacy, not causal truth; retrieval gates trade omission detection for abstention.',
          'Five-paper pilot:22/55 abstentions and25/33 answered judgments more severe than reconciled gold; calibration is in-sample.']),
        ('v12_la_2410_14146','extracted text628-740; expert feedback and nonexpert study',
         ['Expert feedback raises missing citations; six students use ordered stages with self-selected edges.',
          'Reported incorrect edges5/18,7/18,1/18 do not isolate a randomized causal assistance effect.'])]
    papers=[]
    for key,anchor,claims in readings:
        row=inherited[key];path=ROOT/row['local_path']
        assert path.read_bytes().startswith(b'%PDF-') and core.sha(path)==row['sha256']
        papers.append({'citation_key':key,'title':row['title'],'source_identity':row['url'],
            'version':row['arxiv_version'],'version_date':row.get('version_date',row.get('updated',row.get('published'))),
            'local_original':ref(path,anchor),'primary_text':ref(ROOT/row['extracted_text'],anchor),
            'inspected_anchors':[anchor],'supported_claims':claims,
            'prior_audit':ref(inherited_path,key)})
    census_path=ROOT/'docs/program/execution/2026-10-13/llm-census/source-audit.json'
    census=json.loads(census_path.read_text())['sources']
    sng=next(s for s in census if s['integrated_citation_key']=='exec13_hallucination')
    papers.append({'citation_key':'exec13_hallucination','source_identity':sng['source_identity'],
        'version_date':sng['version_date'],'prior_audit':ref(census_path,'exec13_hallucination'),
        'local_original':ref(ROOT/'docs/papers/A Novel Approach to Eliminating Hallucinations in Large Language Model-Assisted Causal Discovery Sng(2024).pdf','PDF4,6,8'),
        'primary_extracts':[ref(ROOT/f'docs/program/execution/2026-10-13/llm-census/Sng-page-{p}.txt',f'PDF{p}') for p in [4,6,8]],
        'supported_claims':['Contradiction metric and mocked true-graph RAG differ from true-edge accuracy; authors explicitly retain that limitation.']})
    new_specs=[
        ('auditing','exec14_expert_auditor','An Explainable AI Approach to Large Language Model Assisted Causal Model Auditing and Development',
         'Yanming Zhang and Brette Fitzgibbon and Dino Garofolo and Akshith Kota and Eric Papenhausen and Klaus Mueller',
         'Zhang',2023,'2312.16211v1','2023-12-23',[1,3,5,6],
         ['Visual summaries organize model ratings and proposed mediators/confounders; source describes early cases.',
          'Section5.2 reports103/110 directions and109/110 numeric responses; not a new banking accuracy study.',
          'Section5.1 calls a change from-3673.4 to-6270.3 a70.69% improvement while captions say higher is better; do not adopt that as validated fit or causal evidence.']),
        ('argumentation','exec14_expert_argumentation','Leveraging Large Language Models for Causal Discovery: a Constraint-based, Argumentation-driven Approach',
         'Zihao Li and Fabrizio Russo','Li',2026,'2602.16481v1','2026-02-18',[1,2,4,5,6,7,8,9,20,21,22,23],
         ['ABAPC-LLM combines data CI constraints with an intersection of five LLM constraint sets; formal consistency is conditional on inputs.',
          'One-off skeleton reduction is irreversible; remaining required/forbidden arrows are hard constraints. Initial pruning and semantic errors are not automatically repaired.',
          '54 synthetic graphs of5/10/15 nodes and50 data repetitions support author-reported structural gains; one LLM-constraint set per dataset is reused.',
          'Descriptions are generated with access to the true graph; renamed/neutral metadata controls remain needed for a new application.',
          'Runtime excludes external model latency; consensus sacrifices recall and sometimes yields no constraints; hidden confounders are future work.',
          'Appendix reporting contains a900-observation table header and a different degrees-of-freedom description; statistical superiority is not independently reconstructed.'])]
    new_sources=[]
    for stem,key,title,authors,surname,year,version,date,pages,claims in new_specs:
        receipt_path=RAW/f'exec14_expert_{stem}.receipt.json'
        receipt=json.loads(receipt_path.read_text());pdf=ROOT/receipt['named_original']
        assert pdf.read_bytes().startswith(b'%PDF-') and core.sha(pdf)==receipt['sha256']
        text_path=RAW/f'exec14_expert_{stem}.txt'
        page_texts=text_path.read_text().split('\f')
        extracts=[]
        for page in pages:
            target=BASE/'inspected'/f'{stem}-page-{page}.txt'
            target.parent.mkdir(exist_ok=True)
            with target.open('x') as stream:stream.write(page_texts[page-1])
            extracts.append(ref(target,f'Physical PDF page{page}'))
        source={'integrated_citation_key':key,'kind':'paper','title':title,
            'filename_title':pdf.stem.rsplit(' '+surname+'(',1)[0], 'first_author':surname,'author':authors,'year':year,
            'source_identity':receipt['url'],'version_date':version+'; '+date,'cutoff':'2026-10-07',
            'local_path':str(pdf.relative_to(ROOT)),'sha256':receipt['sha256'],
            'local_copy':ref(pdf,'Genuine primary PDF; named and hash-bound'),
            'acquisition_receipt':ref(receipt_path,'Observed public retrieval; timestamp limits retained'),
            'inspected_anchors':[{'pdf_page':p,'extract':x} for p,x in zip(pages,extracts)],
            'supported_claims':claims,'extracted_text':ref(text_path,'Full primary extraction'),
            'limitations':['Author-reported literature findings; no local replication or universal causal guarantee.']}
        new_sources.append(source)
        papers.append({'citation_key':key,'source':source,'supported_claims':claims})
    # Existing stored API license is decoded to verify the actual notice, not its label alone.
    import base64
    license_path=RAW/'v12_la_pywhy_llm_license.json'
    license_record=json.loads(license_path.read_text())
    license_bytes=base64.b64decode(license_record['content'])
    assert license_bytes.startswith(b'MIT License')
    tree_path=RAW/'v12_la_pywhy_llm_tree.json'
    tree=json.loads(tree_path.read_text());assert tree['sha']==PIN and not tree['truncated']
    blobs={x['path']:x['sha'] for x in tree['tree']}
    assert hashlib.sha1(b'blob '+str(len(license_bytes)).encode()+b'\0'+license_bytes).hexdigest()==blobs[license_record['path']]
    keys={
        'model':('pywhyllm/suggesters/model_suggester.py','155-269: seeded treatment edge, role calls, confounder tags, retries and vote counts'),
        'augmented':('pywhyllm/suggesters/augmented_model_suggester.py','constructor and pairwise method: dataset acquisition, source fallback and A/B/C parser'),
        'utils':('pywhyllm/utils/augmented_model_suggester_utils.py','full file: BM25/embedding match, sentence flattening, vector store and separate model constructor'),
        'loader':('pywhyllm/utils/data_loader.py','full file: unbounded stream request, full decompression and duplicate-source accumulation'),
        'simple':('pywhyllm/suggesters/simple_model_suggester.py','pairwise and relationship methods: C means neither; pairwise aggregation drops those descriptions'),
        'protocol_init':('pywhyllm/protocols/__init__.py','three imported protocol classes'),
        'identifier':('pywhyllm/protocols/identifier.py','interface declarations are not identification implementations'),
        'modeler':('pywhyllm/protocols/modeler.py','no-evidence state is not distinct in declared pairwise tuple')}
    records=[]
    for key,(upstream,anchor) in keys.items():
        path=RAW/f'exec14_expert_pywhy_{key}.txt';data=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==blobs[upstream]
        records.append({'source_identity':f'https://raw.githubusercontent.com/py-why/pywhy-llm/{PIN}/{upstream}',
            'local_copy':ref(path,anchor),'acquisition_receipt':ref(path.with_suffix('.receipt.json'),'Public retrieval and pinned-blob verification'),
            'revision':PIN,'source_date':'2026-01-06T05:14:41Z','git_blob_sha1':blob,'inspected_anchors':[anchor]})
    for i,upstream,anchor in [(1,'pyproject.toml','license and Python/runtime requirements; placeholder version'),
                             (2,'pywhyllm/suggesters/identification_suggester.py','suggest_backdoor delegation; frontdoor TODO; commented estimand'),
                             (3,'pywhyllm/suggesters/simple_identification_suggester.py','IV/backdoor/frontdoor name suggestions use model text and tag parsing')]:
        path=RAW/f'v12_la_pywhy_llm_source_{i}.txt';data=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==blobs[upstream]
        records.append({'source_identity':f'https://raw.githubusercontent.com/py-why/pywhy-llm/{PIN}/{upstream}',
            'local_copy':ref(path,anchor),'acquisition_receipt':ref(path.with_suffix('.receipt.json'),'Preserved public receipt'),
            'revision':PIN,'source_date':'2026-01-06T05:14:41Z','git_blob_sha1':blob,'inspected_anchors':[anchor]})
    package={'repository':'py-why/pywhy-llm','revision':PIN,'source_date':'2026-01-06T05:14:41Z',
        'tree':ref(tree_path,'Complete pinned tree'),'license':ref(license_path,'Decoded MIT notice matched to pinned Git blob'),
        'declared_distribution_version':'0.0.0 is an explicit dynamic-versioning placeholder, not an asserted release',
        'records':records,'runtime_qualification':False,'integration_allowed':False,
        'findings':['Role-based confounder counts are prompt agreement, not probabilities; treatment-to-outcome edge is seeded before suggestions.',
            'Selected role loop retries KeyError without a finite bound; source inspection is not observed runtime hanging.',
            'Augmented path can fall back to model-only output, concatenates source sentences without document metadata and lacks a distinct unknown answer.',
            'Retrieval helper constructs OpenAI() independently of the wrapper model; caller configuration is not reliably propagated by this selected source path.',
            'Data loader downloads at construction and retains all decompressed records; dataset rights, dependencies, imports and model runtime remain unqualified.'],
        'reuse_route':'Adapt a small optional elicitation component only after source-ID/unknown-state/schema/budget repairs and deterministic graph validation. No default engine admission.',
        'uninspected_closure':['provider SDK behavior and resolved dependency licenses','validator import and unused package paths','CauseNet data rights and provenance beyond the loader declaration','embedding/model downloads and populated retrieval behavior']}
    write(BASE/'primary-review.json',{'cutoff':'2026-10-07','reviewed_utc':datetime.now(timezone.utc).isoformat(),
        'papers':papers,'package':package,'primary_sources_only':True,
        'acquisition':ref(BASE/'acquisition-review.json','Observed receipts and repaired404 path')})
    write(BASE/'exact-oracle.json',calculate())
    extra=[schema.source('exec14_expert_pywhy','PyWhyLLM expert suggestion and retrieval source review',
        'PyWhy Community','software_primary_sources','https://github.com/py-why/pywhy-llm',PIN+';2026-01-06;inspected2026-10-14',
        BASE/'primary-review.json','Eleven code blobs and decoded root license; scoped call paths',package['findings'],records),
        schema.source('exec14_expert_oracle','Exact evidence-dependence and observational ambiguity references',
        'Causal banking proposal','project_derivation','Project-authored finite mechanisms','2026-10-14',
        BASE/'exact-oracle.json','Identical observed law, distinct intervention values, duplicate evidence and correlated consensus',
        ['Restricted model values30/-20 USD; illustrative dependence defeats independent-evidence multiplication.'],
        [{'local_copy':ref(Path(__file__),'Fraction-based enumeration and arithmetic')}])]
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':new_sources+extra,
        'primary_rereads':ref(BASE/'primary-review.json','Eight primary papers and selected package path'),
        'coverage_limits':'Bounded task synthesis; no exhaustive census or runtime admission.'})
    omissions=ROOT/'docs/program/repair-v12/work/LA01/omissions.json'
    census_register=ROOT/'docs/program/execution/2026-10-13/llm-census/census-register.json'
    write(BASE/'candidate-reassessment.json',{'preserved_omissions':ref(omissions,'Original discovery dispositions'),
        'prior_census':ref(census_register,'Existing reconciliations'),
        'resolved':[{'id':'LA01-candidate-33','citation_key':'exec14_expert_auditor','outcome':'Inspected authenticv1; early visualization/ratings evidence only'},
                    {'id':'LA01-candidate-213','citation_key':'exec14_expert_argumentation','outcome':'Inspected authenticv1; scoped solver/consensus gains and limitations'}],
        'previously_resolved':[{'id':'LA01-candidate-10','citation_key':'exec13_hallucination','finding':'Reread supplied-graph RAG and contradiction metric; retain limitations.'}],
        'remaining':[{'item':'ARGUS code and ArgCausalDisco complete pinned implementation, environment and license review',
                      'next_action':'Verify cutoff pin, inspect actual method/configuration and rights before any code adoption; current claims come from paper text.'},
                     {'item':'CausalChat deployed system and representative randomized user evaluation',
                      'next_action':'Treat published usability observations as bounded; register separate evaluation if performance claims are proposed.'}],
        'new_global_search':False,'scope':'Targeted resolution of existing leads; other frontier-census omissions remain open.'})
    facts=['Eight primary papers compare useful retrieval/priors/visual auditing with adverse, conflicting and missing-evidence results; two inherited omissions are resolved and the pinned PyWhyLLM path is inspected.',
        'The banking target and clock, observed-law ambiguity, two-model decision set, duplicate-source and correlated-consensus mechanisms reproduce exactly; remedies and matched baselines are explicit.',
        'The synthesis distinguishes literature observations, exact project constructions and proposed implementation; no live model, bank truth or runtime adoption is claimed.']
    evidence=[ref(SYN,'Connected task synthesis'),ref(BASE/'primary-review.json','Actual primary readings and pinned source inspection'),
        ref(BASE/'exact-oracle.json','Exact imposed examples'),ref(BASE/'candidate-reassessment.json','Resolved and remaining scope'),
        ref(BASE/'source-audit.json','New primary source identities'),ref(BASE/'plan-review.md','Reviewed plan'),ref(Path(__file__),'Reproducible exact references')]
    verify_bindings(evidence)
    write(BASE/'author-review.json',{'status':'pass','reviewer':REVIEWER,'findings':facts,'evidence':evidence,
        'limits':['No independent review, model execution, package qualification or whole-census closure.']})
    graph,_,_=control.combined(ROOT,core.read(ROOT,core.STATE))
    node=control.ledger.operation(graph,'LL.TASK.expert_evidence')
    receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope='Bounded expert-evidence task synthesis with inspected frontier sources and exact references',
        reviewer=REVIEWER,outputs=[evidence[0]],limitations=['Proposal synthesis and exact constructions only; complete census and executable qualification remain open.'])
    for criterion,finding in zip(receipt['criteria'],facts):criterion.update(verdict='pass',finding=finding,evidence=evidence)
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'outcome':'pass','primary_papers':len(papers),'new_papers':2,'selected_code_blobs':len(records),'model_calls':0}))


if __name__=='__main__':
    main()
