"""Prepare a preserving exact-reader protocol supplement and paired sponsor."""
from prepare_openai_publication_20261028 import T,replace,save


def main():
    mapping={
      'build_attention_discovery_reader_20261028':'build_attention_protocol_reader_20261028',
      'publish_attention_discovery_reader_v2_20261028':'publish_attention_protocol_reader_20261028',
      'build_attention_discovery_sponsor_20261028':'build_attention_protocol_sponsor_20261028',
      'publish_attention_discovery_sponsor_20261028':'publish_attention_protocol_sponsor_20261028',
      'review_attention_discovery_chapters_20261028':'review_attention_protocol_chapters_20261028',
      'attention-discovery-review-v1':'attention-protocol-review-v1',
      'attention-discovery-reader-v1':'attention-protocol-reader-v1',
      'sponsor-attention-discovery-v1':'sponsor-attention-protocol-v1',
      'attention_discovery_reader':'attention_protocol_reader',
      'attention_discovery_sponsor':'attention_protocol_sponsor',
      'causal_proposal_attention_discovery_reviewed_v1_2026-10-28':'causal_proposal_attention_protocol_reviewed_v1_2026-10-28',
      'causal_proposal_rl_discovery_reviewed_v1_2026-10-28':'causal_proposal_attention_discovery_reviewed_v1_2026-10-28',
      'sponsor_proposal_attention_discovery_reviewed_2026-10-28':'sponsor_proposal_attention_protocol_reviewed_2026-10-28',
      'attention-discovery and evaluation-contract':'attention-protocol and source-contract',
      'Attention discovery and evaluation contracts':'Attention protocols and source contracts',
      '1423':'1430','1080':'1089','273':'274',
      'exec28_at_':'exec28_ap_','sec:exec28-at':'sec:exec28-ap','sp28at_':'sp28ap_','sp28rl_':'sp28at_',
      'Attention can rank predictive relationships without identifying the effect of a banking intervention.':'A precise temporal/evaluation contract keeps a predictive graph separate from banking intervention evidence.',
      'Attention discovery becomes a useful proposal component only when its predictive target, evaluation information and reuse conditions remain explicit.':'A temporal discovery result is admissible only when its observation window, graph truth access and failure denominator are explicit.',
      'Separate attention discovery from intervention evidence':'Keep graph truth outside TACD evaluation',
    }
    for kind in ['build','publish']:
        for doc in ['reader','sponsor']:
            source=T/f'{kind}_attention_discovery_{doc}_20261028.py'
            text=replace(source.read_text(),mapping)
            if kind=='build' and doc=='reader':
                text=text.replace('import attention_discovery_boundary_reference_20261028 as exact',
                                  'import attention_delegate_reference_20261028 as exact')
                text=text.replace("assert prior_count==1423 and added==7", "assert prior_count==1430 and added==3")
                text=text.replace("Preserve all1423 prior source records,citation contexts and content inputs. Add the versioned Liu preprint,four selected attention discovery source profiles,CDT installer limits and exact permutation witnesses; preserve all inherited comparisons.",
                    "Preserve all1430 prior source records,citation contexts and content inputs. Add exact TCDF/TACD delegates and source-free temporal/evaluation fixtures; retain original-paper and native limits.")
            elif kind=='publish' and doc=='reader':
                text=text.replace("['liu','ct','camcns','tacd','tcdf','cdt','reference']",
                    "['tcdf_temporal','tacd_protocol','protocol_reference']")
                text=text.replace('added==7','added==3').replace('added_citation_records=7','added_citation_records=3')
                text=text.replace("assert report['cited_records']==1430","assert report['cited_records']==1433")
                text=text.replace("index['scholarly_pdfs']==274","index['scholarly_pdfs']==274")
                text=text.replace("{'exec28_at_'+k for k in ['liu','ct','camcns','tacd','tcdf','cdt','reference']}",
                    "{'exec28_at_'+k for k in ['liu','ct','camcns','tacd','tcdf','cdt','reference']}|{'exec28_ap_'+k for k in ['tcdf_temporal','tacd_protocol','protocol_reference']")
                text=text.replace('len(old)==1423','len(old)==1430').replace('preserved_citation_records=1423,added_citation_records=7','preserved_citation_records=1430,added_citation_records=3')
                text=text.replace('All1423','All1430').replace('seven additional','three additional')
                text=text.replace('Attention can rank predictive relationships without identifying the effect of a banking intervention.','A precise temporal/evaluation contract keeps a predictive graph separate from banking intervention evidence.')
                text=text.replace('Attention discovery becomes a useful proposal component only when its predictive target, evaluation information and reuse conditions remain explicit.','A temporal discovery result is admissible only when its observation window, graph truth access and failure denominator are explicit.')
                text=text.replace("['permutation','attention','score','reminder','training']","['split_ratio','cuda:4','lag zero','threshold','unavailable']")
                text=text.replace('One versioned primary preprint and selected attention/CDT originals are inspected; exact project qualifications remain distinct from native behavior.',
                    'Six additional exact TCDF/TACD delegate files and source-free fixtures are reviewed; native behavior and full scholar coverage remain unclaimed.')
            elif kind=='build' and doc=='sponsor':
                text=text.replace('1430 audited citation records','1433 audited citation records').replace('274 genuine scholarly PDFs','274 genuine scholarly PDFs')
                text=text.replace('1423 prior citations','1430 prior citations')
                text=text.replace('assert len(sources)==1089','assert len(sources)==1092')
            elif kind=='publish' and doc=='sponsor':
                text=text.replace("['liu','ct','camcns','tacd','tcdf','cdt','reference']","['liu','ct','camcns','tacd','tcdf','cdt','reference','tcdf_temporal','tacd_protocol','protocol_reference']")
                text=text.replace('assert len(old)==1080','assert len(old)==1089').replace('sources]==1096','sources]==1092')
                text=text.replace('1430 audited','1433 audited').replace('274 genuine scholarly PDFs','274 genuine scholarly PDFs')
            save(f'{kind}_attention_protocol_{doc}_20261028.py',text)
    print('Prepared preserving protocol reader and sponsor builders/reviewers.')


if __name__=='__main__':main()
