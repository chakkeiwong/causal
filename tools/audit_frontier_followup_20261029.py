"""Primary-text follow-up, kept separate from the preserved historical census."""
from pathlib import Path
from hashlib import sha256
import json
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/scientific-gap-closure/2026-10-29';RAW=ROOT/'docs/literature/raw'
def ref(path,anchors):
    p=ROOT/path
    return dict(path=path,sha256=sha256(p.read_bytes()).hexdigest(),inspected_anchors=anchors)
def main():
    specs=[dict(id='LA01-candidate-157',key='gap29wangshen',raw='gap29_mdpi_causal_original',year=2024,
        title='Evaluating Causal Reasoning Capabilities of Large Language Models A Systematic Analysis Across Three Scenarios',
        authors='Lei Wang and Yiqing Shen',surname='Wang',doi='10.3390/electronics13234584',
        publication='Electronics 13(23), 4584; 21 November 2024',
        anchors=['PDF pp.2-6 sections 2.1-2.2: four reasoning variants, explicit scenarios and numerical assumptions',
                 'PDF pp.7-10 sections 3.2-3.3, Tables 1-3: eight models, three prompt regimes, correct/flawed/incorrect scoring',
                 'PDF pp.10-12 section 3.4 and discussion: interpretation and limitations',
                 'PDF pp.12-14: supplementary material pointer and references'],
        claims=['Three cases, four variants and three prompting schemes give 36 prompt conditions.',
                'The scoring separates correct explanations from correct answers with flawed explanations.',
                'Prompt effects vary by case and configuration.'],
        critique=['Effect-to-cause task terminology is not a formal actual-causation identification theorem.',
                  'The hypothetical smallpox example gives population counts 99 and 40; per-person risks differ. This project arithmetic is not medical evidence.',
                  'No local reproduction, current model ranking or supplementary-response completeness claim.']),
      dict(id='LA01-candidate-217',key='gap29mdc',raw='gap29_mdc_original',year=2026,
        title='MDC-Bench A Multidisciplinary Causal Benchmark Based on Causal Structures for Evaluating Large Language Models',
        authors='Peng Wang, Yuxiong Yan, Xiao Ding, Kai Xiong, Bibo Cai, Chao Peng, Yutai Hou, Dandan Tu, Bing Qin and Ting Liu',surname='Wang',
        doi='10.18653/v1/2026.findings-acl.1409',publication='Findings of ACL 2026, 28254-28297; July 2-7, 2026',
        anchors=['PDF pp.3-5 / printed 28256-28258 sections 2.1-3.3: preprint narratives, tasks, construction, model versions, scoring and 8422 questions',
                 'PDF p.6 Table 2: basic/hard accuracies, including 84.56/59.25 for Claude thinking configuration',
                 'PDF pp.7-9: structure comparisons, related work and stated limitations',
                 'PDF p.12 Appendix A: model-built questions and manual sampling check; preprints.org sources',
                 'PDF pp.32-33 Tables 28-29: reverse-reasoning and intervention generation prompts',
                 'PDF pp.43-44 Tables 39-40: plausibility-order check and response requirements'],
        claims=['8422 questions across seven disciplines, four tasks and two answer modes.',
                'Answer construction uses model judgments of causal narratives with manual sampling review.',
                'Hard mode requires two ordered answers; benchmark accuracy does not directly estimate a bank treatment effect.'],
        critique=['A narrative intervention and plausibility ranking do not constitute a known structural equation model or identified causal effect.',
                  'No independent review of all answer keys, dataset execution or live model calls.',
                  'Published source date is now verified before the cutoff; access date remains later.'])]
    specs.append(dict(id='LA01-candidate-122',key='gap29chen',raw='gap29_dualcarbon_original',year=2025,
        title='Collaborative Causal Inference and Multi-Agent Dynamic Intervention for Dual Carbon Public Opinion Driven by Reinforced Large Language Models and Diffusion Models',
        authors='Xin Chen',surname='Chen',doi='10.3390/systems13080689',publication='Systems 13(8), 689; 12 August 2025',
        anchors=['PDF pp.17-18 section5.6 equations16-19: factorisation, CATE definition, intervention expression, chain and counterfactual metrics',
                 'PDF pp.22-26 section6.1-6.2.4 and Tables1-4: 43943 tweets, LDA/BERT/SIR baselines, reported results and ablations',
                 'PDF pp.29-31 discussion, limitations and data-availability statement'],
        claims=['The paper reports a combined language/diffusion/agent architecture and comparisons on a climate sentiment dataset.',
                'Its counterfactual metric permits annotation or simulated reference outcomes; reported predictive and simulated metrics are not bank treatment effects.'],
        critique=['Inspected sections do not provide enough information to reconstruct independently identified unit-level counterfactuals from the described tweets.',
                  'A graph factorisation and a CATE definition alone do not identify the effect from observations.',
                  'No local reproduction, general causal superiority, current model ranking or measured banking benefit.']))
    sources=[]
    for s in specs:
        raw=RAW/(s['raw']+'.pdf');dest=ROOT/'docs/papers'/(s['title']+' '+s['surname']+'('+str(s['year'])+').pdf')
        subprocess.run(['pdfinfo',str(raw)],check=True,stdout=subprocess.DEVNULL)
        if not dest.exists():shutil.copyfile(raw,dest)
        assert dest.read_bytes()==raw.read_bytes()
        receipt=json.loads((RAW/(s['raw']+'.receipt.json')).read_text())
        sources.append(dict(candidate_id=s['id'],integrated_citation_key=s['key'],title=s['title'],authors=s['authors'],year=s['year'],
          source_identity=receipt['url'],doi=s['doi'],version_date=s['publication'],accessed_utc=receipt['accessed_utc'],
          local_copy=ref(str(dest.relative_to(ROOT)),s['anchors']),supported_claims=s['claims'],project_inferences=s['critique'],
          correction_check='Publisher identity page inspected: no retraction/withdrawal/erratum notice found; bounded check only',
          citation_metadata=dict(count=24 if s['key']=='gap29wangshen' else 'not available',source='Crossref retrieved 2026-10-29' if s['key']=='gap29wangshen' else 'not available',counts_not_validity=True),
          venue_metric='not available; not a correctness proxy',status='primary_sections_inspected_not_full_reproduction'))
    docs=[dict(key='gap29matlab',title='MATLAB Econometrics Toolbox panel estimation documentation',version='R2026b retrieved 29 October 2026',
        paths=['gap29_matlab_panel.html','gap29_matlab_fixed.html','gap29_matlab_random.html'],
        anchors=['PanelModel/fitrepanel since R2026a; fitfepanel since R2026b',
                 'Algorithms: within/first-difference estimation, subject-cluster covariance',
                 'Missing Data: complete-row removal; missing subject identifier assigned an additional group',
                 'Version History'],
        claims=['Official current documented capability; one-way panel alternatives with specified transformations and covariance',
                'No exact pre-cutoff availability, native run, full toolbox coverage, price or entitlement claim']),
      dict(key='gap29hugin',title='HUGIN GUI manual',version='GUI 9.8, exact release date unresolved; accessed 29 October 2026',
        paths=['gap29_hugin_manual98.html','gap29_hugin_technology.html','gap29_hugin_limid.html'],
        anchors=['Technology: Bayesian networks, Java API and limited-memory influence diagrams',
                 'About Limited Memory Influence Diagrams: information at each decision, relaxed non-forgetting and ordering assumptions'],
        claims=['Vendor-documented information/decision representation, not empirical identification or executed native integration']),
      dict(key='gap29huginlicense',title='HUGIN published software license agreement',version='Undated public document and GUI 9.8 manual terms, accessed 29 October 2026',
        paths=['gap29_hugin_license.pdf','gap29_hugin_terms98.html'],
        anchors=['Clauses 1,4,5: use, restricted redistribution, API/OEM condition'],
        claims=['Published clause5 states API distribution needs OEM licence; actual contract, current rights and prices unresolved'])]
    for s in docs:
        sources.append(dict(integrated_citation_key=s['key'],title=s['title'],version_date=s['version'],kind='official_documentation',
           local_copies=[ref('docs/literature/raw/'+p,s['anchors']) for p in s['paths']],
           source_identities=[json.loads((RAW/(Path(p).stem+'.receipt.json')).read_text())['url'] for p in s['paths']],
           supported_claims=s['claims'],cutoff='Current retrieval is not a pre-cutoff snapshot; exact version-date qualification retained'))
    backward=[dict(seed='Chen2025',candidates=['Twitter Climate Change Sentiment Dataset','Causal multimodal fusion and intervention references43-46'],classification='Data/method leads',action='Inspect before reproducing the reported architecture; no result imported as validated causal evidence'),dict(seed='MDC-Bench',candidates=['CaLM','CausalBench','ExpliCa','ACCESS','Com2','SURD','Unveiling causal reasoning in large language models: Reality or mirage?'],
      classification='Comparators and method context',action='Reconcile with inherited inspected census; no new claim imported from a reference list'),
      dict(seed='Wang and Shen 2024',candidates=['Causal prompting','Chain-of-thought prompting','Type and actual causality references','Simpson paradox reference'],
      classification='Method context and terminology',action='No theorem claim borrowed; direct scenario arithmetic checked independently')]
    audit=dict(date='2026-10-29',cutoff='2026-10-07',sources=sources,backward_snowball=backward,
      forward_snowball=dict(status='Incomplete',attempt='Built-in search produced no visible results; Crossref identity/update metadata checked',
           consequence='No exhaustive survey or forward-citation clearance claimed'),
      inspection_delta=dict(historical=dict(inspected=82,unread=31),newly_inspected=[s['id'] for s in specs],current=dict(inspected=85,unread=28),historical_files_unchanged=True),
      quarantined=[dict(candidate='LA01-candidate-136',title='Development and implementation of an end-to-end causal inference workflow integrating large language and causal generative models',
         reason='Two downloads begin with PDF signature but are truncated without trailer/EOF; pdfinfo/pdftotext fail. Not admitted as a scholarly PDF or technical support.',
         files=[ref('docs/literature/raw/'+p,'Truncated original, no technical claim') for p in ['gap29_upm_original.pdf','gap29_upm_download_retry.pdf']],
         next_action='Obtain a complete institutional or author copy; preserve failed bytes and stop unchanged retries')],
      software_limits=['MATLAB version date at cutoff and entitlement unresolved','HUGIN version date, order-specific rights and native behavior unresolved',
        'DoubleML/did/causaleffect complete native comparisons remain later prototype work; no census pass inferred','Commercial causaLens named-profile primary comparison remains open'],
      scientific_decision='Use benchmark taxonomies as diagnostics; evaluate target validity, correct ambiguity, decisions and analyst time separately. Compare existing vendor tools before new development.')
    (OUT/'frontier-source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    bib=r'''@article{gap29wangshen,author={Wang, Lei and Shen, Yiqing},title={Evaluating Causal Reasoning Capabilities of Large Language Models: A Systematic Analysis Across Three Scenarios},journal={Electronics},year={2024},volume={13},number={23},pages={4584},doi={10.3390/electronics13234584}}
@article{gap29chen,author={Chen, Xin},title={Collaborative Causal Inference and Multi-Agent Dynamic Intervention for {Dual Carbon} Public Opinion Driven by Reinforced Large Language Models and Diffusion Models},journal={Systems},year={2025},volume={13},number={8},pages={689},doi={10.3390/systems13080689}}
@inproceedings{gap29mdc,author={Wang, Peng and Yan, Yuxiong and Ding, Xiao and Xiong, Kai and Cai, Bibo and Peng, Chao and Hou, Yutai and Tu, Dandan and Qin, Bing and Liu, Ting},title={{MDC-Bench}: A Multidisciplinary Causal Benchmark Based on Causal Structures for Evaluating Large Language Models},booktitle={Findings of the Association for Computational Linguistics: ACL 2026},year={2026},pages={28254--28297},doi={10.18653/v1/2026.findings-acl.1409}}
@manual{gap29matlab,author={{The MathWorks}},title={Econometrics Toolbox: Panel Data Regression, fitfepanel and fitrepanel},year={2026},note={R2026b documentation, accessed 29 October 2026; pre-cutoff page identity not established.}}
@manual{gap29hugin,author={{HUGIN Expert}},title={HUGIN GUI 9.8: Technology and Limited Memory Influence Diagrams},year={2026},note={Retrieved 29 October 2026; precise release date unresolved.}}
@manual{gap29huginlicense,author={{HUGIN Expert}},title={HUGIN Software License Agreement},year={2026},note={Undated public terms and GUI 9.8 manual, clauses 1, 4 and 5; accessed 29 October 2026.}}
'''
    (OUT/'frontier-refs.bib').write_text(bib)
    print(json.dumps(dict(sources=len(sources),new_originals=3,current_frontier=dict(inspected=85,unread=28),quarantined_truncated_originals=1)))
if __name__=='__main__':main()
