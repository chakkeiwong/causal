"""Bind energy claims to original papers and exact static software revisions."""
from pathlib import Path
import hashlib,json,shutil,re
R=Path(__file__).resolve().parents[1]
O=R/'docs/twelve-hour-closure/2026-10-29'
RAW=R/'docs/literature/raw'
def art(p):
    p=Path(p);p=p if p.is_absolute() else R/p
    return dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def save(name,data):
    p=O/name;assert not p.exists(),name;p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def copy_pdf(raw,title,surname,year):
    p=R/'docs/papers'/f'{title} {surname}({year}).pdf';src=RAW/raw
    assert src.read_bytes().startswith(b'%PDF-')
    if p.exists():assert p.read_bytes()==src.read_bytes()
    else:shutil.copyfile(src,p)
    return art(p)
def main():
    title='Measuring and Improving the Energy Efficiency of Large Language Models Inference'
    comp='Sustainable LLM Inference for Edge AI: Evaluating Quantized LLMs for Energy Efficiency, Output Accuracy, and Inference Latency'
    sources=[dict(id='argerich2024',census_id='LA01-candidate-218',title=title,
       authors=['Mauricio Fadel Argerich','Marta Patiño-Martínez'],year=2024,
       doi='10.1109/ACCESS.2024.3409745',version='IEEE Access12,80194–80207;published5June2024,current version13June2024',
       original_url='https://oa.upm.es/86674/1/10226248.pdf',
       artifact=copy_pdf('closure30_energy_original.pdf',title,'Argerich',2024),
       classification='EMPIRICAL_EXAMPLE and IMPLEMENTATION_OR_SOFTWARE',status='retained_with_limits',
       inspected=['PDF3–5,SectionsIII–IV:measurement alternatives,CPU/DRAM RAPL,GPU500ms mean-power method,disk estimation,scope limits',
       'PDF6–11,SectionsV–VI:hardware,10-repeat short-prompt comparison,batching,backend-dependent quantization andQA setup/query phases',
       'PDF12–13,SectionVII:accuracy explicitly not evaluated;batching recommendation and hardware limitations',
       'PDF13–14:references for backward comparison'],
       allowed=['The paper studies inference energy on its specified system and separates component measurements.',
         'Its2024 GPU method differs from the pinned2026 trapezoidal implementation.',
         'Reported quantization gains depend on runtime;accuracy is not jointly tested.'],
       forbidden=['Energy per token establishes energy per useful causal study.','Paper results validate our bank task quality or savings.',
         'The2026source counterexample invalidates the2024experiments.','Physical unit slips in SectionII and disk coefficient labels are correct.'],
       qualification='Wh is watt-hour,not watts per hour;1Wh=3600J. Disk coefficients multiplied by seconds require watts. Do not inherit the source unit slips or compute new hardware values from them.'),
       dict(id='husom2025',title=comp,authors=['Erik Johannes Husom','Arda Goknil','Merve Astekin','Lwin Khin Shar','Andre Kåsen','Sagar Sen','Benedikt Andreas Mithassel','Ahmet Soylu'],
       year=2025,doi='10.1145/3767742',version='Inspected arXiv2504.03360v1,4April2025,30pages. Published counterpart35pages;not asserted identical.',
       original_url='https://arxiv.org/pdf/2504.03360v1',
       artifact=copy_pdf('closure30_sustainable_energy_original.pdf',comp,'Husom',2025),
       classification='RETRACTED_OR_QUARANTINED',status='project_quarantine_for_accuracy_and_joint_rankings',
       inspected=['PDF6–11,Sections3.2–3.9:hardware,time alignment,sampled task counts,prompts,score definitions,baseline subtraction',
         'PDF12–24,Section4,Tables4–10:claimed energy,accuracy,latency andPareto comparisons',
         'PDF24–25,Section5:hardware/task limits;threats paragraph inconsistently says latency is not analyzed despite Section4.3',
         'PDF25–30,related work andreferences',
         'Pinned evaluation code,data164tests,metric implementation andpublication-era identical files'],
       allowed=['Describe the inspected source and why its joint quality-energy comparisons are excluded pending reconstruction.'],
       forbidden=['Treat its HumanEval rates as verified correctness.','Use its joint accuracy-energy rankings to choose a bank model.',
         'Conclude all its power measurements are false.','Claim misconduct or exact published execution without retained run provenance.'],
       risk_record=art(O/'energy-scoring-review.json'),
       version_limit='OpenAlex publication_date17September2025;Crossref published18November2025,ACMToIT6,1–35. Keep repository preprint date distinct;this audit uses the30-pagev1.'),
       dict(id='energymeter2026',title='EnergyMeter',classification='IMPLEMENTATION_OR_SOFTWARE',
       version='2.0.2;commit7b53911e59f1e58500ca06d3a427e291273a4bcf,5February2026',
       original_url='https://github.com/maufadel/EnergyMeter',license='MIT,inspected LICENSE andpyproject',
       artifacts=[art(RAW/n)for n in ['closure30_energy_README_md.txt','closure30_energy_LICENSE.txt','closure30_energy_pyproject_toml.txt','closure30_energy_src_energymeter_energy_meter_py.txt']],
       inspected=['get_total_joules_gpu,lines415–445:active sample filtering before timestamp trapezoid',
         'CPU/DRAM missing readings returnzero withwarning;GPUzero/single sample limits',
         'Sampling default0.1s;begin/end timing anddisk process-name aggregation'],
       status='conditional_integration_after_measurement_repairs',
       allowed=['State exact static branch behavior andthe independently authored trace consequence.'],
       forbidden=['Native measurement qualified.','Zero return proves zero consumption.','Shared device energy belongs entirely to one bank study.']),
       dict(id='edgecode2026',title='neurips-edge-llm-challenge-sampled evaluation sources',classification='IMPLEMENTATION_OR_SOFTWARE',
       version='c11fe134709bd41a6a35344a988b9edc8d03016e,25September2026;HumanEval files identical at18February2025commit a130cb8583bed65e76c8190e3b6c3435bd79b07e',
       original_url='https://github.com/ejhusom/neurips-edge-llm-challenge-sampled',license='No root LICENSE found in complete pinned tree;do not assume redistribution or port rights.',
       artifacts=[art(RAW/n)for n in ['closure30_edge_README_md.txt','closure30_edge_src_evaluate_HumanEval_py.txt','closure30_edge_humaneval_data.txt','closure30_edge_src_postprocess_joulescope_data_py.txt','closure30_edge_src_postprocess_subtract_idle_energy_consumption_py.txt','closure30_edge_humaneval_history.json']],
       inspected=['evaluate_pass_at_k,lines63–102;main selects noentry_point',
         'All164storedtestASTs:Assign andFunctionDef only,nocheck invocation',
         'Main energy postprocessor subtracts idlewatts timesduration;unusedhelper mismatch distinguished',
         'README100kHz setting conflicts withpreprint2MHz description'],
       status='do_not_adopt_scoring_unchanged',
       allowed=['The inspected data/evaluator composition does not invoke its stored assertions unless candidate code does so itself.'],
       forbidden=['Exact published outcomes reconstructed.','All paper metrics necessarily use this unmodified path.']),
       dict(id='hfeval2022',title='Hugging Face evaluate code_eval implementation',classification='IMPLEMENTATION_OR_SOFTWARE',
       version='c447fc8eda9c62af501bfdc6988919571050d950,22September2022',
       original_url='https://github.com/huggingface/evaluate/tree/c447fc8eda9c62af501bfdc6988919571050d950/metrics/code_eval',
       artifacts=[art(RAW/n)for n in ['closure30_hf_code_eval_py.txt','closure30_hf_execute_py.txt']],
       inspected=['code_eval.py155–188 concatenates candidate andreference','execute.py68–80 declares passed when execution terminates without error'],
       status='static_semantics_only',allowed=['User-supplied reference must execute its test;metric does not invent acheck invocation.'],
       forbidden=['The comparator pinned this exact dependency in its experiments.','Downloaded/generated code was run by this audit.'])]
    save('energy-source-support.json',dict(cutoff='2026-10-07',access_date='2026-10-30 Asia/Shanghai',sources=sources,
       census_change='Only candidate218 changes disposition;comparator andsoftware are separate follow-up support.'))
    metadata=[]
    for tag,n in [('argerich','energy'),('husom','sustainable_energy')]:
        op=RAW/f'closure30_{n}_openalex.json';d=json.loads(op.read_text());d=d['results'][0]if'results'in d else d
        cr=RAW/f'closure30_{n}_crossref.json';c=json.loads(cr.read_text())['message']
        metadata.append(dict(source=tag,openalex=art(op),crossref=art(cr),citations=d.get('cited_by_count'),is_retracted=d.get('is_retracted'),
          venue=c.get('container-title'),published=c.get('published'),online=c.get('published-online'),update_to=c.get('update-to'),updated_by=c.get('updated-by'),relation=c.get('relation'),
          venue_rank='not independently checked;not correctness evidence',access_date='2026-10-30 Asia/Shanghai',
          caveat='No update/retraction flag inthese records isnot exhaustive absence. Comparator independently quarantined forscoring defect regardless ofmetadata. Counts postdate literature cutoff.'))
    save('energy-citation-metadata.json',metadata)
    groups=[
      ('ArgerichIII andrefs17–28','RAPL David2010;RAPL inAction Khan2018;Schöne2021;NVML;pyNVML;Kepler;Scaphandre;CodeCarbon;memory-estimation criticism','IMPLEMENTATION_OR_SOFTWARE','Sensor attribution alternatives;exact current implementations not audited here;do not import runtime accuracy claims.'),
      ('Argerichrefs8,10,11,14,29,31–35','Patterson2021;McDonald2022;Strubell2020;Luccioni2022BLOOM;energy-aware ML andhardware efficiency studies','BACKGROUND','Training andenvironmental-accounting antecedents;not direct causal-study quality evidence.'),
      ('Argerichrefs36–58','Pythia,BLOOM,Dolly,RedPajama,Llama2;bitsandbytes,GGUF,ctransformers;hardware specifications;quantization accuracy','DIRECT_METHOD','Runtime-dependent comparisons motivate protocol;do not port algorithms or inherit unseen benchmarks.'),
      ('HusomSections2,6;refs1,15,30','Argerich2024;medical-model energy comparatorDoo;Husom2024ThePriceofPrompting','COMPETITOR','Firstinspected;others candidates requiring genuine originals before technical use.'),
      ('Husomrefs27,28,32,33,37,39,44,46,48','Huanglow-bitLlama3;JaiswalCompressingLLMs;Jinquantizationevaluation;Langquantization;Lievaluation;Liuemergentability/generalization;Maocompressibility','COMPETITOR','Task-dependentquality alternatives;no source-specific theorem or numeric claim imported.'),
      ('Husomrefs7,25,43,52,60,61,66,74,76,78,80','GPTQ/quantizationfamilies;AWQ;LUT-GEMM;Agile-Quant;EdgeQAT;MobileQuant;OutlierSuppression;SmoothQuant;ZeroQuant;Edge-LLM','DIRECT_METHOD','Algorithm alternatives beyond present measurement question;inspect before anyport decision.'),
      ('Husomrefs31,40,45,54,58,70','AIbenchmark;PalmBench;Edge-LLMscompetition;Qinedgeguidelines;MLPerfInference;MLPerfPower','COMPETITOR','Relevant hardware/taskprotocols;future comparativequalification;not claimed covered exhaustively.'),
      ('Husomrefs34,35,47,49–51,53,59','Joulemeter,Joulescope,llama.cpp,Monsoon,Ollama,pyJoules,Scaphandre','IMPLEMENTATION_OR_SOFTWARE','Potentialmeasurement/runtimealternatives;paperdescriptionisnot independentlycheckedcurrentcapability.'),
      ('Husomrefs36,41,55,62,67,72,73,77,79,81,82,84','Edgecloudinference;TPI-LLM;FlexGen;GreenLLM;T-MAC;EdgeShard;inference/compressionsurveys','BACKGROUND','Scheduling andcompression alternatives;no causal-quality claims imported.'),
      ('Husomrefs8,12,29,42,69,71','HumanEval;TruthfulQA;ROUGE;automatictextassessment','DIRECT_METHOD','Inspected testdata andscoringimplementation directly;benchmark scores not causal-study validity.'),
      ('Both bibliographies','General foundation models,application examples,webusage anecdotes andunrelatedtranslation/recommendation tasks','PERIPHERAL','Not used to establish energycost orquality;retained originals allow complete bibliography inspection.')]
    save('energy-backward-snowball.json',[dict(anchor=a,candidates=b,classification=c,disposition=d)for a,b,c,d in groups])
    fw=[]
    for seed in ['energy','sustainable_energy']:
      for sort in ['cited','recent']:
        p=RAW/f'closure30_{seed}_{sort}.json';d=json.loads(p.read_text())
        fw.append(dict(seed=seed,order=sort,query=art(p),cutoff='2026-10-07',indexed_count=d['meta']['count'],
          results=[dict(title=x['title'],date=x['publication_date'],doi=x.get('doi'),citations=x['cited_by_count'],
             disposition='Inspected butquarantined comparator' if 'Sustainable LLM Inference for Edge AI'in x['title'] else 'Candidateonly;nottechnicalsupport')for x in d['results']],
          limit='Bounded firstfive bycitations/recent;no completenessclaim;indexdateanomalies preserved,not silent evidence.'))
    save('energy-forward-snowball.json',fw)
    save('energy-claim-support.json',[
      dict(claim='Inference energy differs from cost per useful study',support='PROJECT_DERIVATION',anchor='energy-study.tex,ratios ofexpectations andqualitybreak-even'),
      dict(claim='2024paperdoesnotjointlytestaccuracy',support='PRIMARY_TECHNICAL_SUPPORT',anchor='ArgerichSectionVII,PDF12'),
      dict(claim='Activefilterbridgesidleintervals',support='IMPLEMENTATION_EVIDENCE andPROJECT_DERIVATION',anchor='PinnedEnergyMeterget_total_joules_gpu;energy-study-attempt-1/power-trace.json'),
      dict(claim='Poissonbatchwaiting',support='PROJECT_DERIVATION andGENERATED_ARRIVALS',anchor='Exactformula,900000independentbatches,ninecells;independent-check.json'),
      dict(claim='Comparatorqualityrankingexcluded',support='IMPLEMENTATION_EVIDENCE andPROJECT_COUNTEREXAMPLE',anchor='energy-scoring-review.json;onlyauthoredliterals executed'),
      dict(claim='Adoptionconditionalonmeasurement/testrepair',support='PROJECT_RECOMMENDATION',anchor='Staticreview,MITlicense,missingrootcomparatorlicense;notnativequalification')])
    save('energy-omissions-risk.json',dict(omissions=[
       dict(source='Husom published35pageversion',reason='Only30pagearXivv1 primarytext acquired;publishedversion not silently substituted',next='Obtainpublisheroriginalandcompare experiment/testcorrections.'),
       dict(source='ActualHusommodeloutputs,dependencylockandnativeexecution',reason='Notreconstructed;staticfilehistorydoesnotproveexactpublishedexecution',next='Obtainexactartifactmanifest,repairedtests,andrerunpreservedoutputsunderapprovedisolatedevaluation.'),
       dict(source='Towards sustainable and energy-efficient agentic AI via small language models,2026-10-05,10.1016/j.cosrev.2026.101076',reason='Metadata candidateonly;unreadoriginal',next='Retrieveoriginal;useasnavigation,nottheoremsupport.'),
       dict(source='MLPerfPower,CodeCarbon,Kepler,Scaphandre,pyJoulesandhardwaremetercalibration',reason='Alternativesidentified;currentprimaryimplementationsnotinspected',next='Prioritizeonlyifchoicechangesproposedmeasurementboundary.')],
       risks=['Noactualenergy,carbon,bankcostorROImeasurement.',
         'Noqualityprobabilityderivedfromgenericbenchmarks.',
         'KnownPoissonarrivalmodelisillustrative;realarrivals,backlogandcancellationunqualified.',
         'Needwholeworkflowfailureandretryaccounting;refusalandusefulanswerseparate.',
         'Noarbitraryroot/sensoraccessor downloadedcodeexecution.']))
    print(json.dumps(dict(sources=len(sources),ledgers=6,comparator_quarantined=True)))
if __name__=='__main__':main()
