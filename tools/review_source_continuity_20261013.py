#!/usr/bin/env python3
"""Record this author-reviewed tranche; never infer semantic approval from hashes."""
import json
from pathlib import Path
import sys
import master_control as core
import build_integrated_monograph_v12 as shared
import pcalg_reuse_examples_20261013 as pcalg
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/traceability'
ref=shared.ref

def main():
    out=BASE/'semantic-review-04.json';assert not out.exists()
    index_path=ROOT/'docs/program/execution/2026-10-13/frontier-synthesis/traceability-review.json'
    index=json.loads(index_path.read_text());assert index['status']=='pass'
    current={r['citation_key']:r for r in index['records']}
    prior_records={}
    for name in ['semantic-review-01.json','semantic-review-02.json','semantic-review-03.json']:
        p=BASE/name;d=json.loads(p.read_text())
        for r in d['records']:prior_records[r['citation_key']]=(r,ref(p,'Preserved semantic review of these exact contexts'))
    added_findings={
      'exec13_java_adapter_contract':'Tetrad reuse contexts preserve the complete IID Gaussian CPDAG contract and distinguish specified failure propagation from actual implementation.',
      'exec13_java_adapter_oracles':'Added Tetrad context retains equal-law effects0,0,2/5 and explicitly identifies project reference calculations, not Java execution.',
      'exec13_java_adapter_source':'Added context retains interruption/failure handling as wrapper requirements; no granted runtime property.',
      'exec13_java_tetrad':'Added contexts distinguish source tests from independent scientific evidence; Fisher-Z caught singularity and restricted CPDAG comparator remain pinned source findings.',
      'exec13_bayesia_api':'Added latent comparison reuses hosting/edition distinctions without declaring that unavailable documentation proves absent capability.',
      'exec13_genie_readme':'Added contexts retain inspected edition dates and explicitly limit what later acquisition establishes about the cutoff.',
      'exec13_smile_intro':'Added temporal contexts preserve manual edition, wrapper scope and the need for configuration-specific conformance.',
      'exec13_smile_license':'Added contexts retain licensing as a selected-configuration prerequisite, with no blanket right to port proprietary source.',
      'v12_mcp_basic':'Changed interface context describes per-request metadata in the pinned newer revision and explicitly excludes it from the implemented older surface.',
      'v12_la04_autogen':'Added architecture context agrees with save/load model-context source and preserved maintenance/code-license review; external effects are not covered.'}
    continuity=[]
    for key,(old,binding) in sorted(prior_records.items()):
        oldset={(c['path'],c['context']) for c in old['contexts_reviewed']}
        contexts=current[key]['citation_contexts']
        added=[c for c in contexts if (c['path'],c['context']) not in oldset]
        assert not added or key in added_findings,key
        continuity.append({'citation_key':key,'verdict':'pass_in_stated_scope','prior_review':binding,
            'preserved_contexts':sum((c['path'],c['context']) in oldset for c in contexts),
            'new_contexts_reviewed':added,'finding':added_findings.get(key,'Every current citation context matches the preserved author-reviewed passage exactly.'),
            'contexts_reviewed':contexts})
    findings={
      'exec13_pcalg':'Reinspected manual: individual-test alpha, stable skeleton versus orientation, effect multisets and separate graph encodings. Correct claim has a misplaced historical page anchor; additive correction binds page12.',
      'exec13_pcalg_reuse_primary':'Reinspected R paths: transpose, NA replacement, conflict2/2, binarization before validity check, local/global multiplicities and declared dependencies. Manuscript limits source behavior to pin and invalid-input examples.',
      'exec13_pcalg_reuse_examples':'Exact reference rerun matches all preserved results: equal-law systems, distinct multiplicities, units,54 encoding cases and36 detected transposes. Base-R fallback remains a separate inherited scalar trace, not package execution.',
      'exec13_other_dagitty':'Selected GraphAnalyzer accepts supplied DAG/PDAG/MAG/PAG and handles adjustment/selection; browser and R share the JavaScript core. No dataset-derived graph truth claimed.',
      'v12_la_2305_00050':'Formulation and discovery contexts preserve knowledge-assisted roles and memorization limitations; no discovered bank fact inferred.',
      'v12_la_2312_04350':'Formal generated benchmark and language-to-tool gap are retained; no effect calibration, bank population or live prototype result inferred.',
      'v12_la_2402_15301':'Background/document/PC roles, adverse ASIA retrieval result and restricted orientation denominator remain visible across discovery/workflow contexts.',
      'v12_la_2609_30867':'Evidence auditing remains distinct from causal truth; injected flaws, retrieval abstention and five-paper in-sample calibration are scoped.',
      'v12_la_2602_11527':'Conversational architecture, four-page demonstration and future effect modules remain distinct from Han Causal Agent and from executed code.',
      'v12_la_2607_22443':'Actor/critic point-treatment scope, overlap refusals and notebook-weight interpretation remain explicit in formulation, economics and architecture.',
      'v12_la_2606_23608':'Protected core is a proposed architecture, not an impossibility theorem for all hybrid methods or scientific truth conferred by approval.',
      'v12_la_2608_09696':'Mechanism proposal, numerical evidence, open-loop studies and115/171 evaluable-cell denominator remain separate from causal identification.',
      'exec13_census_causaleval':'Task-specific gains/losses, sample restrictions and repeated questions support the comparisons; exact reweighting is illustrative, not a new performance claim.',
      'exec13_census_graph_validation':'DDI F1 values and labeled-training differences remain restricted to pairwise relation extraction, with no full graph or equal-cost superiority claim.',
      'exec13_census_collaboration':'Sequential exchangeability/positivity, text-version functional, CVAE estimation and generated outcomes remain distinct from actual delivered-message policy effects.',
      'v12_la_package_causalagent':'Selected module unresolved OLC function and parse-to-empty path support scoped repair requirement; no claim about every revision or deployed runtime.',
      'v12_la_package_oci_agent':'Notebook cells42/43 uniformly summarize a propensity-trimmed sample; target-measure and unrestricted-notebook boundaries match the code.',
      'v12_la04_langgraph':'Primary interrupt description restarts node logic; idempotent publication is the project remedy, not an automatic framework guarantee.',
      'v12_la04_pydantic_ai':'Typed tools and pre/post usage checks are conditional; absent price does not provide a hard monetary limit. Application permissions remain explicit.',
      'exec13_census_causal_agent':'Named graph memory, generated tasks, unequal one-shot baseline and cost sample scope remain paper-reported; no bank validation inferred.',
      'exec13_census_orca':'Abstract/table discrepancy, node-presence discovery metric, unclear CI metric and PAG-to-DAG choices remain adverse findings rather than silently corrected results.',
      'exec13_census_causalsmith':'Compiler checks are separated from unknown statement-match error and self-rated campaign quality; no proof environment execution claimed.',
      'exec13_architecture_exact':'All cited values follow exact stipulated examples, with distinct target measures, shared critic law, equal-information argument and authored costs.',
      'exec13_architecture_local':'Six preserved offline outcomes and recovery replay support only local conformance; no live model call or external platform acceptance.',
      'exec13_frontier_exact':'Mixture, conditional-versus-marginal composition, oracle-error and two-world regret calculations are explicit exact illustrations, not empirical model findings.'}
    records=[]
    for key,finding in findings.items():
        r=current[key]
        records.append({'citation_key':key,'verdict':'pass_with_corrected_anchor' if key=='exec13_pcalg' else 'pass_in_stated_scope',
            'finding':finding,'primary_sources':r['local_copies'],'inspected_anchors':r['anchors'],
            'contexts_reviewed':r['citation_contexts']})
    replay=json.loads(json.dumps(pcalg.run(),default=str))
    assert replay==json.loads((ROOT/'docs/program/execution/2026-10-13/pcalg-reuse/exact-results.json').read_text())
    done=set(prior_records)|set(findings)
    report={'status':'partial_semantic_review_not_Q2_acceptance','reviewer':{'name':'Codex author/coordinator','kind':'author'},
      'reader':core.read(ROOT,core.STATE)['reader'],'structural_review':ref(index_path,'458 source keys and their exact625-page reader contexts'),
      'prior_review_continuity':continuity,'records':records,
      'cumulative_reviewed_source_keys':len(done),'reviewed_source_key_list':sorted(done),
      'remaining_source_keys':sorted(set(current)-done),
      'anchor_corrections':ref(BASE/'source-anchor-corrections-01.json','Binding additive correction to pcalg page12'),
      'supporting_semantic_reviews':[ref(ROOT/'docs/program/execution/2026-10-13'/p,'Source/claim review reused after inspecting current contexts') for p in ['agent-architecture/primary-review.json','agent-architecture/release-source-review.json','frontier-synthesis/primary-review.json','frontier-synthesis/mathematical-review.json','pcalg-reuse/primary-review.json','pcalg-reuse/reproduction-review.json','commercial-latent/release-source-review.json','commercial-temporal/release-source-review.json','tetrad-reuse/release-source-review.json','interfaces/release-source-review.json']],
      'reproductions':[{'source':ref(ROOT/'docs/program/execution/2026-10-13/pcalg-reuse/exact-results.json','Exact reference rerun in memory'),'matches':True,'new_random_draws':0,'package_executed':False}],
      'findings':['21 earlier source keys initially had completely unchanged citation contexts;10 had new/changed contexts requiring substantive review.','The latter contexts were read and checked against their preserved primary and scoped release reviews.','The pcalg encoding claim is supported on page12; the older page39 pointer is corrected additively.','Unread source keys remain explicit; this tranche cannot award whole-reader Q2 acceptance.'],
      'next_action':'Continue with the remaining_source_keys list: R discovery alternatives and symbolic identification, then foundational theorem/derivation contexts. Include source-anchor-corrections-01.json in the next successor audit chain. Reuse only matching reviewed contexts; keep Q2 open until all essential current claims have semantic dispositions.',
      'proposal_q2_acceptance':False}
    core.write(out,report)
    print(json.dumps({'status':report['status'],'reviewed_keys':len(done),'remaining_keys':len(report['remaining_source_keys']),'corrected_anchors':1,'contexts_new_reviewed':sum(len(r['contexts_reviewed']) for r in records),'prior_keys_with_new_contexts':sum(bool(r['new_contexts_reviewed']) for r in continuity)}))

if __name__=='__main__':main()
