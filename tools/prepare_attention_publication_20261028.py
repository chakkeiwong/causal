"""Create exact preserving attention publication successors from reviewed mechanics."""
from prepare_openai_publication_20261028 import T,replace,save


def main():
    mapping={
      'rl_discovery_boundary_reference_20261028':'attention_boundary_reference_20261028',
      'rl_discovery_reader_20261028':'attention_discovery_reader_20261028',
      'rl_discovery_sponsor_20261028':'attention_discovery_sponsor_20261028',
      'rl-discovery-review-v1':'attention-discovery-review-v1',
      'rl-discovery-reader-v1':'attention-discovery-reader-v1',
      'sponsor-rl-discovery-v1':'sponsor-attention-discovery-v1',
      'boundary-profile-reader-v2':'rl-discovery-reader-v1',
      'sponsor-boundary-profile-v2':'sponsor-rl-discovery-v1',
      'causal_proposal_rl_discovery_reviewed_v1_2026-10-28':'causal_proposal_attention_discovery_reviewed_v1_2026-10-28',
      'causal_proposal_boundary_profile_reviewed_v2_2026-10-28':'causal_proposal_rl_discovery_reviewed_v1_2026-10-28',
      'sponsor_proposal_rl_discovery_reviewed_2026-10-28':'sponsor_proposal_attention_discovery_reviewed_2026-10-28',
      '1418':'1423','1423':'1430','1073':'1080','1080':'1089','273':'274','271':'273',
      'exec28_rl_':'exec28_at_','sec:exec28-rl':'sec:exec28-at','sp28rl_':'sp28at_','sp28bp_':'sp28rl_',
      'reinforcement-discovery and dependency-contract':'attention-discovery and evaluation-contract',
      'Reinforcement search and discovery contracts':'Attention discovery and evaluation contracts',
      'Qualify reinforcement discovery before reuse':'Separate attention discovery from intervention evidence',
      'publish_boundary_profile_reader':'publish_attention_discovery_reader',
      'publish_boundary_profile_sponsor':'publish_attention_discovery_sponsor',
    }
    for kind in ['build','publish']:
        for doc in ['reader','sponsor']:
            text=replace((T/f'{kind}_rl_discovery_{doc}_20261028.py').read_text(),mapping)
            text=text.replace("['zhu','wang','gcastle','cdt','reference']","['liu','ct','camcns','tacd','tcdf','cdt','reference']")
            text=text.replace('added==5','added==7').replace('added_citation_records=5','added_citation_records=7')
            text=text.replace('Add two primary discovery papers,selected RL/CORL source and CDT dependency profiles with exact penalty/keyword witnesses','Add the versioned Liu preprint,four selected attention discovery source profiles,CDT installer limits and exact permutation witnesses')
            text=text.replace('Reinforcement learning can search for a causal graph without establishing that the graph is identified.','Attention can rank predictive relationships without identifying the effect of a banking intervention.')
            text=text.replace('A discovery optimizer is useful only when its search result preserves the declared causal target and assumptions.','Attention discovery becomes a useful proposal component only when its predictive target, evaluation information and reuse conditions remain explicit.')
            text=text.replace("['penalty','mask','score','reminder','ordering']","['permutation','attention','score','reminder','training']")
            text=text.replace('Two original discovery papers and selected RL/CORL/CDT paths are inspected; exact project qualifications remain distinct from native behavior.','One versioned primary preprint and selected attention/CDT originals are inspected; exact project qualifications remain distinct from native behavior.')
            text=text.replace('Primary RL discovery assumptions and penalty boundary; selected mask,order,attention and dependency contracts with exact authored witnesses','Attention discovery assumptions,permutation-law qualification,oracle/split/empty-denominator contracts and conditional source reuse')
            text=text.replace('five additional primary-paper,software and independent-project records','seven additional primary-paper,software and independent-project records')
            text=text.replace('Exact four-graph witness preserves a cyclic tie at the non-strict penalty boundary; strict domination excludes it,and kwargs key/attribute lookup differs','Exact finite witness preserves a marginal while covariance changes1/4to-1/4,predictor loss0to1,and temporal agreement2/3to0; stipulated intervention effect remains0')
            save(f'{kind}_attention_discovery_{doc}_20261028.py',text)
    text=(T/'review_rl_discovery_chapters_20261028.py').read_text()
    text=replace(text,{'rl-discovery-reader-v1':'attention-discovery-reader-v1','rl-discovery-chapters-v1':'attention-discovery-chapters-v1','All1418prior':'All1423prior','rl_discovery_delta':'attention_discovery_delta','new original RL discovery papers and selected source/dependency findings':'one new primary attention discovery preprint and selected source/evaluation findings'})
    save('review_attention_discovery_chapters_20261028.py',text)
    print('Prepared preserving attention reader,sponsor and chapter successors.')


if __name__=='__main__':main()
