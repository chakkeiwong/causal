"""Prepare immutable protocol publication successors from the verified attention builders."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'


def read(name):return (TOOLS/name).read_text()
def put(name,text):
    path=TOOLS/name
    assert not path.exists(),path
    ast.parse(text);path.write_text(text)


def main():
    b=read('build_attention_protocol_reader_v2_20261028.py')
    b=b.replace("PREDECESSOR=DOCS/'program/execution/2026-10-28/rl-discovery-reader-v1'",
                "PREDECESSOR=DOCS/'program/execution/2026-10-28/attention-discovery-reader-v1'")
    b=b.replace("LABELS=['sec:exec28-ap']","LABELS=['sec:exec28-at2']")
    b=b.replace("assert original.startswith(BS+'section[Attention protocols and source contracts]{')",
                "assert original.startswith(BS+'section[Delegate-level temporal and evaluation protocol]{')")
    b=b.replace("Preserve all1430 prior source records,citation contexts and content inputs. Add the versioned Liu preprint,four selected attention discovery source profiles,CDT installer limits and exact permutation witnesses; preserve all inherited comparisons. Keep coverage, native, visual and final acceptance open. Pair sponsor and reconcile all obligations.",
                "Preserve all1430 prior source records,citation contexts and content inputs. Add exact TCDF/TACD delegates and source-free temporal/evaluation fixtures; retain original-paper and native limits.")
    put('build_attention_protocol_reader_v4_20261028.py',b)

    p=read('publish_attention_discovery_reader_v2_20261028.py')
    p=p.replace('import build_attention_discovery_reader_20261028 as build','import build_attention_protocol_reader_v4_20261028 as build')
    p=p.replace('import build_attention_protocol_reader_20261028 as build','import build_attention_protocol_reader_v4_20261028 as build')
    p=p.replace('import build_attention_protocol_reader_20261028 as build','import build_attention_protocol_reader_v3_20261028 as build')
    p=p.replace("attention-discovery-reader-v1","attention-protocol-reader-v1").replace("attention-discovery","attention-protocol")
    p=p.replace("causal_proposal_attention_discovery_reviewed_v1_2026-10-28","causal_proposal_attention_protocol_reviewed_v1_2026-10-28")
    p=p.replace("1430 and index['scholarly_pdfs']","1433 and index['scholarly_pdfs']")
    p=p.replace("len(old)==1423","len(old)==1430")
    p=p.replace("new.keys()-old.keys()=={'exec28_at_'+k for k in ['liu','ct','camcns','tacd','tcdf','cdt','reference']}",
                "new.keys()-old.keys()=={'exec28_ap_'+k for k in ['tcdf_temporal','tacd_protocol','protocol_reference']}")
    p=p.replace("preserved_citation_records=1423,added_citation_records=7","preserved_citation_records=1430,added_citation_records=3")
    p=p.replace("opening='Attention can rank predictive relationships without identifying the effect of a banking intervention.';closing='Attention discovery becomes a useful proposal component only when its predictive target, evaluation information and reuse conditions remain explicit.'",
                "opening='A precise temporal/evaluation contract keeps a predictive graph separate from banking intervention evidence.';closing='A temporal discovery result is admissible only when its observation window, graph truth access and failure denominator are explicit.'")
    p=p.replace("['permutation','attention','score','reminder','training']","['split_ratio','cuda:4','lag zero','threshold','unavailable']")
    p=p.replace("claims remain distinct from native behavior.","claims remain distinct from native behavior.")
    p=p.replace("One versioned primary preprint and selected attention/CDT originals are inspected; exact project qualifications remain distinct from native behavior.",
                "Six exact TCDF/TACD delegate files and source-free fixtures are inspected; native behavior and full scholarly coverage remain unclaimed.")
    p=p.replace("All1423","All1430").replace("seven additional","three additional")
    p=p.replace("1423 prior records","1430 prior records").replace("1430 records and274","1433 records and274")
    p=p.replace("publish_attention_discovery_reader","publish_attention_protocol_reader")
    put('publish_attention_protocol_reader_v3_20261028.py',p)

    b=read('build_attention_discovery_sponsor_20261028.py')
    b=b.replace('import build_attention_discovery_reader_20261028 as reader','import build_attention_protocol_reader_v4_20261028 as reader')
    b=b.replace('import build_attention_protocol_reader_20261028 as reader','import build_attention_protocol_reader_v4_20261028 as reader')
    b=b.replace('sponsor-attention-discovery-v1','sponsor-attention-protocol-v1')
    b=b.replace("PRIOR=DOCS/'program/execution/2026-10-28/sponsor-rl-discovery-v1'","PRIOR=DOCS/'program/execution/2026-10-28/sponsor-attention-discovery-v1'")
    b=b.replace('sponsor_proposal_attention_discovery_reviewed_2026-10-28.pdf','sponsor_proposal_attention_protocol_reviewed_2026-10-28.pdf')
    b=b.replace("rl-discovery-reader-v1/reader/build-report.json","attention-discovery-reader-v1/reader/build-report.json")
    b=b.replace("'1423 audited citation records'","'1430 audited citation records'")
    b=b.replace("'1430 audited citation records')","'1433 audited citation records')")
    b=b.replace("assert text.count('273 genuine scholarly PDFs')==1","assert text.count('274 genuine scholarly PDFs')==1")
    b=b.replace("text=text.replace('273 genuine scholarly PDFs','274 genuine scholarly PDFs')","")
    b=b.replace("marker='sp28rl_reader,sp28rl_progress';assert text.count(marker)==1","marker='sp28at_reader,sp28at_progress';assert text.count(marker)==1")
    b=b.replace("('sp28at_reader'","('sp28ap_reader'").replace("('sp28at_progress'","('sp28ap_progress'")
    b=b.replace("sponsor-addition.md","sponsor-addition.md")
    b=b.replace('assert len(sources)==1089','assert len(sources)==1094')
    b=b.replace("1430 audited citations; no final acceptance","1433 audited citations; no final acceptance")
    b=b.replace("1430 audited citation records","1433 audited citation records")
    b=b.replace("1080 prior citations","1089 prior citations")
    b=b.replace("attention-discovery and evaluation-contract","attention-protocol and source-contract")
    put('build_attention_protocol_sponsor_v3_20261028.py',b)

    p=read('publish_attention_discovery_sponsor_20261028.py')
    p=p.replace('import build_attention_discovery_sponsor_20261028 as build','import build_attention_protocol_sponsor_v3_20261028 as build')
    p=p.replace('import build_attention_protocol_sponsor_20261028 as build','import build_attention_protocol_sponsor_v3_20261028 as build')
    p=p.replace('sponsor-attention-discovery-v1','sponsor-attention-protocol-v1')
    p=p.replace('attention-discovery-reader-v1','attention-protocol-reader-v1')
    p=p.replace('attention-discovery','attention-protocol')
    p=p.replace("report['cited_records']==len(audit['sources'])==1089","report['cited_records']==len(audit['sources'])==1094")
    p=p.replace('len(old)==1080','len(old)==1089')
    p=p.replace("{'exec28_at_'+k for k in ['liu','ct','camcns','tacd','tcdf','cdt','reference']}|{'sp28at_reader','sp28at_progress'}",
                "{'exec28_at_'+k for k in ['liu','ct','camcns','tacd','tcdf','cdt','reference']}|{'exec28_ap_'+k for k in ['tcdf_temporal','tacd_protocol','protocol_reference']}|{'sp28ap_reader','sp28ap_progress'}")
    p=p.replace("'1430 audited'","'1433 audited'")
    p=p.replace("'Separate attention discovery from intervention evidence'","'Keep graph truth outside TACD evaluation'")
    p=p.replace("records=1089","records=1094").replace("All1080","All1089").replace("1089 records audited","1094 records audited")
    p=p.replace("publish_attention_discovery_sponsor","publish_attention_protocol_sponsor")
    put('publish_attention_protocol_sponsor_v3_20261028.py',p)

    c=read('review_attention_discovery_chapters_20261028.py')
    c=c.replace('attention-discovery-reader-v1','attention-protocol-reader-v1').replace('attention-discovery-chapters-v1','attention-protocol-chapters-v1')
    c=c.replace('All1423prior','All1430prior').replace('rl_discovery_delta','attention_protocol_delta')
    put('review_attention_protocol_chapters_v3_20261028.py',c)
    print('Prepared five preserving protocol publication successors.')


if __name__=='__main__':main()
