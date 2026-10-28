#!/usr/bin/env python3
"""Audit two real preprints, preserving separate unavailable journal obligations."""
from collections import Counter
from copy import deepcopy
import hashlib,html,json,re
from pathlib import Path
import agent_evaluation_survey_reference_20261025 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/census-observation-workflow-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-25/census-route-followup-v1/census-register.json'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Two selected2024preprints are independent originals;exact journal equivalence not established.',
 'Reviews support their own frameworks,syntheses and limits;underlying empirical/software findings not inherited transitively.',
 'Authored finite examples are stipulated;no model,downloaded code or bank experiment executed.',
 'Candidate12and188journal obligations stay open;no coverage saturation or absence claim.',
 'Mandatory coverage/depth,visual,independent and final acceptance remain open.',
]
SPECS={
 'chemistry':dict(candidate='LA01-candidate-12',arxiv='2407.01603v3',first_author='Ramos',
   pdf='A Review of Large Language Models and Autonomous Agents in Chemistry Ramos(2024).pdf',
   extract='chemistry-original.txt',pages=79,date='14November2024archive submission;18November2024cover date',
   anchors=[(28,31,'Agent loop,taxonomy,decision modules,environment/tools,memory and proposal/evaluation/selection stages.'),(38,40,'Hypothesis versus assistance,secondary predictor-feedback accounts,benchmark relevance and evaluation criteria limits.'),(41,42,'Sanity tools not hallucination-proof;human validation;one-week workflow is an illustrative proposed scenario,not measured ROI.')]),
 'vulnerability':dict(candidate='LA01-candidate-188',arxiv='2404.02525v3',first_author='Zhou',
   pdf='Large Language Model for Vulnerability Detection and Repair Literature Review and the Road Ahead Zhou(2024).pdf',
   extract='vulnerability-original.txt',pages=30,date='7October2024version3',
   anchors=[(1,6,'Review identity,58-study stated scope and search method;not current ecosystem saturation.'),(18,20,'Dated synthesis of heuristic labels,missing repair tests,input granularity,contamination and offline deployment limits.'),(22,24,'Proposed benchmark/repository/deployment roadmap and explicit keyword/selection threats to validity.')]),
}

def main():
    assert not (BASE/'review.json').exists()
    sources=[];extracts=[]
    for name,spec in SPECS.items():
        raw=RAW/f'exec25_cow_{name}_v3.pdf';pdf=ROOT/'docs/papers'/spec['pdf'];receipt=raw.with_suffix('.receipt.json')
        assert pdf.read_bytes()==raw.read_bytes();digest=hashlib.sha256(pdf.read_bytes()).hexdigest();assert read(receipt)['status']=='saved' and read(receipt)['sha256']==digest
        landing=RAW/('exec25_cow_chemistry_arxiv_landing.html' if name=='chemistry' else 'exec25_cow_vulnerability_landing.html');text=landing.read_text()
        title=html.unescape(re.search(r'name="citation_title" content="([^"]+)"',text)[1]);authors=[html.unescape(x) for x in re.findall(r'name="citation_author" content="([^"]+)"',text)]
        pages=[x for x in (BASE/spec['extract']).read_text().split(chr(12)) if x.strip()]
        assert len(pages)==spec['pages'] and spec['arxiv'] in pages[0]
        anchors=[]
        for lo,hi,finding in spec['anchors']:
            anchors.append(dict(anchor=f'PDFpages{lo}-{hi}',pages=[lo,hi],finding=finding,text_extract=ref(BASE/spec['extract'],f'Form-feed pages{lo}-{hi}')))
            extracts.append(dict(source=name,pages=[lo,hi],finding=finding,text=chr(12).join(pages[lo-1:hi])))
        sources.append(dict(integrated_citation_key='exec25_cow_'+name,kind='paper',title=title,filename_title=title.replace(':',''),author=' and '.join(authors),first_author=spec['first_author'],year=2024,source_identity='https://arxiv.org/abs/'+spec['arxiv'],version_date=spec['arxiv']+';'+spec['date']+';before7October2026cutoff',local_path=str(pdf.relative_to(ROOT)),sha256=digest,local_copy=ref(pdf,'Genuine version3 preprint'),identity_evidence=[ref(landing,'Archive identity/history'),ref(receipt,'Version-qualified retrieval'),ref(BASE/'inspection.md','Source/version boundary')],inspected_anchors=anchors,supported_claims=[x[2] for x in spec['anchors']],limitations=LIMITS))
    write(BASE/'inspected-extracts.json',dict(anchors=extracts,visual_review=False))
    result=exact.calculate();write(BASE/'exact-results.json',result)
    project=dict(integrated_citation_key='exec25_cow_reference',kind='project_derivation_and_exact_reference',title='Authored agent semantic-target,proxy,judge,label,test and cost witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/agent_evaluation_survey_reference_20261025.py',version_date='25October2026;finite stipulated laws;no native execution',local_copy=ref(Path(exact.__file__),'Authored exact examples'),inspected_anchors=[ref(BASE/'exact-results.json','All outputs'),ref(BASE/'development.tex','Explained premises and derivations')],supported_claims=['Gross70minus cost80is net-10USD.','Higher proxy score can select utility-10instead of20;regret30USD.','Independent three-judge majority error7/250versus common-mode1/10.','Reference-label agreement can be1while true-label agreement0.','Constant-zero patch passes input0but violates identity specification at1.','100requests/80completions/60accepted with200USDcost gives10/3per accepted versus5/2per completion.'],limitations=LIMITS)
    sources.append(project);write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_finite_authored_examples',evidence=[ref(Path(exact.__file__),'Exact reference'),ref(BASE/'exact-results.json','Replayed outputs'),ref(BASE/'development.tex','Assumptions and target definitions')],findings=project['supported_claims'],limitations=['Stipulated examples are not empirical error,productivity or bank performance estimates.']))
    route_rows=[]
    for n in ['12','48','282']:
        identity=RAW/f'exec25_cow_identity_{n}.json';route_rows.append(dict(candidate='LA01-candidate-'+n,identity=ref(identity,'Metadata only'),original_route_status='PMC outside fixed collector;no policy expansion',arxiv_query_status='HTTP429;no absence inference',evidence=[ref(RAW/f'exec25_cow_arxiv_{n}.receipt.json','Failed distinct title query')]))
    for identity in sorted(RAW.glob('exec25_cow_tail_identity_*.json')):
        if identity.name.endswith('.receipt.json'):continue
        d=read(identity);n=identity.stem.split('_')[-1]
        route_rows.append(dict(candidate='LA01-candidate-'+n,identity=ref(identity,'Metadata only'),title=d.get('title'),publication_date=d.get('publication_date'),locations=[dict(pdf=x.get('pdf_url'),landing=x.get('landing_page_url')) for x in d.get('locations',[])],original_route_status='Related arXiv original separately inspected; journal bytes pending' if n=='188' else 'Listed original hosts outside fixed collector or no exact PDF;not a global unavailable claim'))
    write(BASE/'route-review.json',dict(status='bounded_identity_and_route_review',items=route_rows,evidence=[ref(BASE/'local-title-search.json','Read-only filename search;no exact matches'),ref(BASE/'acquisition-limits.json','Preserved blocked routes')],claims_from_metadata=False,unchanged_routes_retried=False))
    write(BASE/'omissions-register.json',dict(items=[dict(gap='Journal originals12and188',next_action='Acquire authentic originals through a distinct permitted route or supplied retained original;compare against separately cited preprints before closure.'),dict(gap='Other inspected identity routes',next_action='Use distinct authorized original routes;do not infer technical claims from metadata or retry unchanged blocks.'),dict(gap='Underlying studies/packages',next_action='Read genuine originals and exact code/artifacts before empirical or implementation claims.'),dict(gap='Public qualification',next_action='Preregister semantic,graph,identification,refusal,numeric,execution and utility oracles with complete task/cost denominators.'),dict(gap='Unknown general guarantees',next_action='Require additional information or justified restrictions for assignment truth,latent identification,judge independence and bank transport.')],global_blocker=False,native_execution=False))
    prior=read(PRIOR);verify_bindings(prior);reg=deepcopy(prior)
    for name,spec in SPECS.items():
        row=next(x for x in reg['items'] if x['id']==spec['candidate']);assert row['disposition']=='open_original_not_inspected';source=next(x for x in sources if x['integrated_citation_key']=='exec25_cow_'+name)
        row.update(availability='Exact journal original remains unread;separate genuine arXiv version3 inspected and cited under its own identity.',related_primary_source_record=source,related_publication_keys=[source['integrated_citation_key'],'exec25_cow_reference'],effect_on_claims='Preprint supports its own framework/synthesis;no journal-equivalence or underlying-study qualification.',next_action='Acquire genuine journal original and compare to '+spec['arxiv']+';continue independent census and public evaluation obligations.')
    for row in reg['items']:
        if row['id'] in ['LA01-candidate-12','LA01-candidate-188']:continue
        if row['id'] in {x['candidate'] for x in route_rows}:
            row.update(availability='New identity/route review retained;listed originals not admitted through fixed collector;no global unavailability claim.',availability_evidence=ref(BASE/'route-review.json','Candidate-specific routes'),next_action='Inspect distinct permitted genuine original or supplied local original;preserve route limits and do not repeat unchanged requests.')
    counts=Counter(x['disposition'] for x in reg['items']);assert counts==Counter(x['disposition'] for x in prior['items']);assert counts['inspected_primary_retained_with_limits']==82 and counts['open_original_not_inspected']==31
    reg.update(counts=dict(counts),supersedes=ref(PRIOR,'Preserved82/31census'),changes=['Two related genuine preprints inspected;their separate journal-original obligations remain open.','Seventeen previously untested candidate identity/route records retained without unsupported exclusions.'],closure=False,interpretation='82of113candidate originals inspected;31unread;4crosscutting obligations;two additional related preprints separately inspected.');write(BASE/'census-register.json',reg)
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking target,graph,tool and evaluation argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Primary review synthesis,project examples and implementation remain separate.','Version dates and journal omissions retained.','Business translation,diagram ambiguity,oracles and CLI/MCP results connected.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan.md','inspection.md','source-audit.json','inspected-extracts.json','exact-results.json','mathematical-review.json','route-review.json','omissions-register.json','census-register.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_primary_review',evidence=evidence,steps=['Preserve two authentic preprints under own identities.','Retain unavailable journal obligations and route limits without scope waiver.','Integrate connected target/graph/validation/cost argument and exact examples.','Publish after consumed predecessor with exact source preservation and paired sponsor.'],native_execution=False,visual_acceptance=False))
    evidence += [ref(BASE/'plan-review-v2.json','Reviewed plan')]
    verify_bindings(dict(evidence=evidence));write(BASE/'review.json',dict(status='pass_for_scoped_primary_review',evidence=evidence,related_preprints=2,new_records=3,census_inspected=82,census_unread=31,crosscutting=4,limitations=LIMITS,coverage_acceptance=False,native_execution=False,visual_acceptance=False))
    print(json.dumps(dict(related_preprints=2,new_records=3,census_inspected=82,census_unread=31,crosscutting=4,native_execution=False)))

if __name__=='__main__':main()
