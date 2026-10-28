"""Create explicit preserving successors without mutating bound predecessors."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];T=ROOT/'tools'

def replace(text,mapping):
    return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)

def save(name,text):
    p=T/name
    assert not p.exists(),p
    compile(text,str(p),'exec');p.write_text(text)

def main():
    reader=replace((T/'build_benchmark_oracles_reader_20261025.py').read_text(),{
      'benchmark_oracle_reference_20261025':'linguistic_measurement_reference_20261028',
      '2026-10-25/benchmark-oracles-reader-v1':'2026-10-28/linguistic-measurement-reader-v1',
      '2026-10-25/benchmark-oracles-v1':'2026-10-28/linguistic-measurement-v1',
      '2026-10-25/agent-evaluation-surveys-reader-v2':'2026-10-25/benchmark-oracles-reader-v1',
      'causal_proposal_agent_evaluation_surveys_reviewed_v2_2026-10-25':'causal_proposal_benchmark_oracles_reviewed_v1_2026-10-25',
      'causal_proposal_benchmark_oracles_reviewed_v1_2026-10-25':'causal_proposal_linguistic_measurement_reviewed_v1_2026-10-28',
      'sec:exec25-bor':'sec:exec28-lm','1390':'1392','added==2':'added==3','expected_scholarly_pdfs=267':'expected_scholarly_pdfs=268',
      'Independent causal and scoring oracles':'Linguistic measurement and executable interventions',
      'independent causal and scoring oracle argument':'linguistic measurement and component adoption argument'})
    reader=reader.replace('Add pinned benchmark branch inspection and independent IV,identification-state,interval and capped-loss witnesses;','Add the inspected Pryzant preprint, exact heterogeneous measurement witness and component-specific runtime findings;')
    save('build_linguistic_measurement_reader_20261028.py',reader)
    pub=replace((T/'publish_benchmark_oracles_reader_20261025.py').read_text(),{
      'build_benchmark_oracles_reader_20261025':'build_linguistic_measurement_reader_20261028',
      '1392':'1395','1390':'1392','267':'268','added_citation_records=2':'added_citation_records=3',
      'benchmark_oracles':'linguistic_measurement','independent benchmark-oracle':'linguistic measurement and adoption'})
    pub=pub.replace("{'exec25_bor_'+k for k in ['sources','reference']}","{'exec28_lm_'+k for k in ['pryzant','artifacts','reference']}")
    pub=pub.replace('A public benchmark can justify a prototype only if its reference answer represents the scientific decision we intend to test.','A language-assisted banking decision begins with an intervention that a bank can actually implement.')
    pub=pub.replace('the proposed product must obtain information, narrow assumptions or return the unresolved set.','The proposed product must preserve the distinction between a meaningful scientific question, a justified answer and an executable method.')
    pub=pub.replace("['CLadder','CausalDS','250,000','quarantine','overflow']","['CFPB','TextCause','77.5','50,000','LCM']")
    pub=pub.replace('two additional pinned-source and independent-project records','three additional primary-paper, component-source and independent-project records')
    pub=pub.replace('Exact IV-compatible-world,three-state-identification,finite-interval and capped-loss witnesses reproduce;','Exact conditional-mean enumeration and separate algebra reproduce heterogeneous effects,proxy sign reversal and stipulated USD consequences;')
    pub=pub.replace('Pinned source branches are inspected; independent finite witnesses remain distinct from native benchmark results.','Preprint conditions and component inventories are inspected; the stochastic-proxy witness remains distinct from source theorem assumptions and native results.')
    save('publish_linguistic_measurement_reader_20261028.py',pub)
    sponsor=replace((T/'build_benchmark_oracles_sponsor_v2_20261028.py').read_text(),{
      'build_benchmark_oracles_reader_20261025':'build_linguistic_measurement_reader_20261028',
      '2026-10-25/sponsor-benchmark-oracles-v1':'2026-10-28/sponsor-linguistic-measurement-v1',
      '2026-10-25/sponsor-agent-evaluation-surveys-v2':'2026-10-25/sponsor-benchmark-oracles-v1',
      '2026-10-25/agent-evaluation-surveys-reader-v2':'2026-10-25/benchmark-oracles-reader-v1',
      '2026-10-25/benchmark-oracles-v1':'2026-10-28/linguistic-measurement-v1',
      'sponsor_proposal_benchmark_oracles_reviewed_2026-10-25':'sponsor_proposal_linguistic_measurement_reviewed_2026-10-28',
      '1390':'1392','1392':'1395','1031':'1035','1035':'1040',
      'sp25aes_reader,sp25aes_progress':'sp25bor_reader,sp25bor_progress',
      'sp25bor_reader':'sp28lm_reader','sp25bor_progress':'sp28lm_progress',
      'independent benchmark-oracle':'linguistic measurement and component adoption',
      '25 October 2026':'28 October 2026'})
    old="assert text.count('267 genuine scholarly PDFs')==1\n    text=text.replace('267 genuine scholarly PDFs','267 genuine scholarly PDFs')"
    assert old in sponsor
    sponsor=sponsor.replace(old,"assert text.count('267 genuine scholarly PDFs')==1\n    text=text.replace('267 genuine scholarly PDFs','268 genuine scholarly PDFs')")
    save('build_linguistic_measurement_sponsor_20261028.py',sponsor)
    sp=replace((T/'publish_benchmark_oracles_sponsor_v2_20261028.py').read_text(),{
      'build_benchmark_oracles_sponsor_v2_20261028':'build_linguistic_measurement_sponsor_20261028',
      '1035':'1040','1031':'1035','1392':'1395','267':'268',
      'sp25bor_reader':'sp28lm_reader','sp25bor_progress':'sp28lm_progress',
      'Qualify the scientific oracle before funding the agent trial':'Measure the intervention before funding the language workflow',
      'independent benchmark-oracle':'linguistic measurement and component adoption',
      'publish_benchmark_oracles_sponsor':'publish_linguistic_measurement_sponsor'})
    sp=sp.replace("{'exec25_bor_'+k for k in ['sources','reference']}","{'exec28_lm_'+k for k in ['pryzant','artifacts','reference']}")
    save('publish_linguistic_measurement_sponsor_20261028.py',sp)
    print('Created four preserving publication successors.')

if __name__=='__main__':main()
