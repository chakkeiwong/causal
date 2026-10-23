#!/usr/bin/env python3
"""Bind inspected original/scorer spans and preserve the census successor."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unlearning_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-24/census-agent-unlearning-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-24/census-language-collaboration-v1'
RAW = ROOT / 'docs/literature/raw'
PDF = ROOT / 'docs/papers/K-Bench A Benchmark for LLM Unlearning in Agentic Deployments Yu(2026).pdf'
COMMIT = '50c0874caf3ec2b544d70d02ccd61559efb33586'
read = lambda p: json.loads(p.read_text())
LIMITS = ['Primary text and selected immutable code spans inspected; no downloaded code, upstream tests, model or bank experiment executed.',
          'Reported empirical results and source contradictions are retained without selecting a corrected value or alleging misconduct.',
          'Current-source cutoff is 7 October 2026; selected original v2 is 14 September 2026.',
          'Source, arithmetic and extracted text review only; visual, independent and final acceptance remain open.',
          'No universal erasure, causal identification, native integration, bank economics or compliance conclusion.']

SPECS = {
 'README.md': [(1, 151, 'Declared channels, exact target, CLI record contract and cheap local fingerprint; prose does not override inspected source.')],
 'LICENSE': [(1, 21, 'Direct code MIT terms; not a blanket model or dataset license.')],
 'assets/manifest.json': [(1, 101, 'Separate baseline, model and retrieval tiers declare sizes and hashes; their bytes were not acquired or run here.')],
 'docs/METRICS.md': [(1, 127, 'Binary and graded metrics, answer fallback, seed protocol and distinct eligibility conditions.')],
 'docs/protocol_amendments.md': [(1, 168, 'Post-evidence amendments change adapter loading, FDR families, retention labels and disjoint split contracts; dated run mapping remains needed.')],
 'chcons/metrics.py': [(1, 136, 'Canonical value variants and substring CER; queried target, not corpus-wide or joint reconstruction.')],
 'scripts/09_k_verdict_v2.py': [(120, 243, 'Last-row query deduplication, conditional channel denominators, raw-answer fallback and query bootstrap.'),
   (441, 641, 'Seed-pooled paired intersections, BH by family, a below-twofold reduction branch, separate retention label, and approximate averaging of bootstrap endpoints.')],
 'scripts/kscore.py': [(1, 464, 'Graded severity, raw-answer health/evidence distinction, guarded direct-reply fallback, query signatures and baseline-relative scalar; direct script is not the full CLI gate.')],
 'main_pinned_requirements.txt': [(1, 30, 'Version list explicitly omits monorepo lock and includes a ranged release-only dependency.')],
 'reproduce/README.md': [(1, 49, 'Selected released targets, separate probe commands, unrebuildable paper-only panels and approximate study budget.')],
 'chcons/pii.py': [(1, 175, 'Faker generator and disjoint split loader; corpus declarations alone cannot settle separate LUME provenance.')],
 'scripts/01_generate_pii.py': [(1, 65, 'Seeded synthetic generator entry point; inspected only, not executed.')],
 'scripts/kbench.py': [(213, 280, 'CLI attaches binary labels through the inspected public classifier.'),
   (356, 412, 'Local fingerprint binds config bytes and weight names/sizes, not weight bytes; hosted revision and API model identities differ.'),
   (485, 647, 'Strict per-seed query identity and seed alignment, baseline gates, scalar, retention ratio and separate absolute terminal-collapse gate.')],
 'docs/COMPUTE.md': [(1, 71, 'Approximate500GPU-hour study, selected18GPU-hour target and explicit unresolved OpenUnlearning PEFT/freeze; no actual bank cost.')],
 'data/LICENSE': [(1, 18, 'Synthetic corpus CC BY4.0 declaration is separate from code and external assets.')],
 'pyproject.toml': [(1, 36, 'Python>=3.11,<3.13, declared dependency ranges and packaged CLI sources; no resolved environment claim.')],
 'scripts/02_baseline_leakage.py': [(463, 488, 'Queries sampled without replacement within a seed from entity-field records in declared eval splits; cross-seed dependence remains an evaluation question.')],
 'chcons/transcript.py': [(237, 314, 'Raw first-answer health and terminal-label checks are protocol diagnostics, not correctness proofs.')],
 'scripts/19_convert_lume_to_kbench.py': [(1, 97, 'Converter describes LUME Task2 input as synthetic and extracts fields; input dataset and outputs absent from this audit.')],
 'docs/DATASHEET.md': [(1, 65, 'Faker corpus, real retrieval background and separate nonredistributed LUME block have different provenance and rights.')],
}


def main():
    assert not (BASE/'review.json').exists()
    acq=read(BASE/'acquisition.json');data=PDF.read_bytes()
    assert hashlib.sha256(data).hexdigest()==acq['paper']['sha256']
    receipt=read(RAW/'exec24_unlearning_kbench_v2.receipt.json')
    assert receipt['status']=='saved' and receipt['sha256']==acq['paper']['sha256']
    assert (RAW/'exec24_unlearning_kbench_v2.pdf').read_bytes()==data
    pages=(BASE/'paper.txt').read_text().split(chr(12));assert len([x for x in pages if x.strip()])==52
    paper_specs=[(1,8,'Four substrate configurations and a fixed, nonadaptive observer over six emitted channels; no weight-erasure proof.'),
      (9,16,'Signed Equation3 differs from absolute-retention prose; gates, graded scalar, seed pooling and method adaptations are distinct.'),
      (17,27,'Reported topology, channel rates and model panels are observations of declared configurations; answer-channel denominators can differ from query OR.'),
      (28,40,'Method ports and matched-budget tests retain explicit objective, training and conformance departures; no reproduction of every original method.'),
      (41,42,'Ecological block uses real-name/birth-date language inconsistent with the later synthetic-only claim; exact dataset required.'),
      (43,47,'Gated rankings, injection/model sensitivity and observer limits constrain interpretation; no bank cost or acceptance.'),
      (48,49,'Joint reconstruction, other-entity disclosures and bounded replicated subset remain explicit; ethics statement claims synthetic-only PII.'),
      (50,52,'Bibliography inspected as discovery only; cited upstream works are not adopted without their own original review.')]
    paper=dict(integrated_citation_key='exec24_unlearning_original',kind='paper',title='K-Bench: A Benchmark for LLM Unlearning in Agentic Deployments',
      filename_title='K-Bench A Benchmark for LLM Unlearning in Agentic Deployments',author='Guangsheng Yu and Yanna Jiang and Qin Wang and Baihe Ma and Xu Wang',first_author='Yu',year=2026,
      source_identity='https://arxiv.org/abs/2609.12808v2',version_date='v2;14September2026;latest listed before7October2026 cutoff',
      local_path=str(PDF.relative_to(ROOT)),sha256=receipt['sha256'],local_copy=ref(PDF,'Genuine52-page original'),
      identity_evidence=[ref(RAW/n,'Archive identity and genuine acquisition') for n in ['exec24_unlearning_kbench_landing.html','exec24_unlearning_kbench_landing.receipt.json','exec24_unlearning_kbench_v2.receipt.json']],
      inspected_anchors=[dict(anchor=f'PDF pages{a}-{b}',pages=[a,b],finding=f,text_extract=ref(BASE/'paper.txt',f'Form-feed pages{a}-{b}')) for a,b,f in paper_specs],supported_claims=[f for _,_,f in paper_specs],limitations=LIMITS)
    inventories=[read(BASE/n) for n in ['authenticated-source-inventory.json','authenticated-source-inventory-2.json','authenticated-source-inventory-3.json']]
    rows={x['path']:x for inv in inventories for x in inv['sources']};assert len(rows)==25 and SPECS.keys()<=rows.keys()
    tree=read(RAW/'exec24_unlearning_repo_tree.json');assert not tree['truncated'] and len(tree['tree'])==208
    tree_by={x['path']:x for x in tree['tree']};records=[]
    for path,spans in SPECS.items():
        row=rows[path];p=ROOT/row['local'];blob=p.read_bytes();sha=hashlib.sha256(blob).hexdigest()
        assert sha==row['sha256'] and hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()==tree_by[path]['sha']
        rec=read(p.with_suffix('.receipt.json'));assert rec['sha256']==sha
        lines=blob.decode().splitlines();anchors=[]
        for a,b,claim in spans:
            b=min(b,len(lines));assert 1<=a<=b
            anchors.append(dict(anchor=f'{path} lines{a}-{b}',inspected_text='\n'.join(lines[a-1:b]),supported_claim=claim))
        records.append(dict(source_identity=rec['url'],version_date='Cutoff commit '+COMMIT,local_copy=ref(p,'Authenticated original'),acquisition_receipt=ref(p.with_suffix('.receipt.json'),'Original receipt'),git_blob_sha1=tree_by[path]['sha'],inspected_anchors=anchors,supported_claims=[x['supported_claim'] for x in anchors],technical_inspected=True,executed=False))
    software=dict(integrated_citation_key='exec24_unlearning_software',kind='software_primary_sources',title='K-Bench pinned scorer, protocol, custody and reuse contract',author='K-Bench authors',year=2026,
      source_identity='https://github.com/OniReimu/kbench/tree/'+COMMIT,version_date='Commit50c0874;14September2026;package1.0.0;before7October cutoff',
      local_copy=ref(RAW/'exec24_unlearning_source_04.txt','Metrics contract'),records=records,
      identity_evidence=[ref(RAW/n,'Cutoff commit and complete tree') for n in ['exec24_unlearning_repo_cutoff.json','exec24_unlearning_repo_tree.json']],
      inspected_anchors=[dict(anchor='Selected spans listed in records;20 of25 authenticated blobs inspected for claims',inspection='Author static source review')],
      supported_claims=[x['supported_claim'] for r in records for x in r['inspected_anchors']],limitations=LIMITS)
    project=dict(integrated_citation_key='exec24_unlearning_reference',kind='project_derivation_and_exact_reference',title='Authored observer, retention, clustering and custody witnesses',author='Causal banking proposal project',year=2026,
      source_identity='tools/unlearning_reference_20261024.py',version_date='24October2026;exact stipulated examples',local_copy=ref(ROOT/'tools/unlearning_reference_20261024.py','calculate'),
      inspected_anchors=['calculate: exhaustive fair-bit table, exact fractions and distinct payload hashes'],
      supported_claims=['Split target has zero binary per-channel detection and one-half graded maximum despite joint reconstruction.','Fair XOR shares each leave one bit; joint shares identify the bit; stipulated200USD wrong-action loss implies100USD versus0 expected loss.','Negative3/5 passes the printed signed tolerance but fails the absolute requirement.','Stipulated1.5-fold reduction conflicts with paper twofold requirement under inspected public classifier branch; no native execution.','200 independent entity outcomes repeated three times give variance1/800, not1/2400.','A collapsed method can retain scalar1/2 while failing the separate terminal gate.','Equal-sized payloads need not be byte-identical.'],limitations=LIMITS)
    assert exact.calculate()==read(BASE/'exact-results.json')
    write(BASE/'source-audit.json',dict(sources=[paper,software,project],cutoff='2026-10-07',authenticated_blobs=25,claim_inspected_blobs=len(records),native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_finite_examples',evidence=[ref(BASE/'source-audit.json','Inspected definitions'),ref(BASE/'exact-results.json','Exact authored outputs'),ref(ROOT/'tools/unlearning_reference_20261024.py','Independent project code')],findings=project['supported_claims'],limitations=LIMITS))
    omissions=[('Scorer reconciliation','Bind one endpoint revision and reconcile below-twofold labels, signed/absolute retention, answer denominators, raw fallback, terminal eligibility and old table inputs.'),
      ('Empirical identity and dependence','Acquire exact query/entity/seed/run manifests and experiment artifacts; justify paired-sign law, cluster uncertainty and topology intervals before empirical adoption.'),
      ('Data provenance','Resolve original real-data versus synthetic-only wording using exact LUME version/conversion artifacts and rights. Preserve both accounts; no real-data validation claim.'),
      ('Observer coverage','Register public synthetic corpus-wide and joint-reconstruction observers, adaptive and mixed-storage extensions, authorized retention and correct-refusal tasks.'),
      ('Environment and rights','Acquire full hashed environment, missing upstream PEFT identity, model/index rights and content identities; local weight filenames/sizes are insufficient.'),
      ('Economics and native acceptance','Meter complete training, storage, failures, review and accepted outputs in a registered public prototype; no downloaded-code execution authorized by this source audit.'),
      ('Visual and final acceptance','Fresh image allowance and independent/final review remain open; no global blocker for source work.')]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=g,next_action=a) for g,a in omissions],global_blocker=None))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected scholarly argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],findings=['Separate source reports, static findings and authored exact examples.','Avoid silently fixing contradictory source claims; denominators and independent units explicit.','Conditional original-worker recommendation grants no native capability.'],visual_acceptance=False))
    write(BASE/'plan-review-v2.json',dict(status='pass',supersedes=ref(BASE/'plan-review.json','Initial acquisition plan retained'),evidence=[ref(BASE/'source-audit.json','Inspected source'),ref(BASE/'mathematical-review.json','Exact examples')],steps=['Complete source and protocol inspection before citation.','Preserve contradictory definitions and data claims with exact follow-ups.','Integrate preserving monograph and paired sponsor; renew exact-byte review.','Reconcile census and complete queue; commit/push and continue independent obligations.'],visual_acceptance=False))
    reg=deepcopy(read(PRIOR/'census-register.json'));old=deepcopy(reg);row=next(x for x in reg['items'] if x['id']=='LA01-candidate-181');assert row['disposition']=='open_original_not_inspected'
    row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key=paper['integrated_citation_key'],primary_source_record=paper,
      publication_keys=[paper['integrated_citation_key'],software['integrated_citation_key'],project['integrated_citation_key']],task_families=['agent_architecture','evaluation_cost','data_code'],
      mapping_basis='Agent observation/custody and evaluation contracts, not causal discovery or effect qualification.',availability='Genuine52-page v2 and25 immutable source blobs acquired; only20 blobs support inspected claims; no native/visual review.',
      effect_on_claims='Retain public synthetic evaluation design; withhold native integration, universal forgetting and real-data validation claims.',next_action='Resolve scorer/provenance/dependency identities and preregister joint-observer, retention and cluster-aware public trials.')
    assert all(x==next(y for y in reg['items'] if y['id']==x['id']) for x in old['items'] if x['id']!=row['id'])
    counts=dict(Counter(x['disposition'] for x in reg['items']));assert counts['inspected_primary_retained_with_limits']==74 and counts['open_original_not_inspected']==39
    reg.update(counts=counts,supersedes=ref(PRIOR/'census-register.json','Preserved73/40census'),changes=['Only candidate181 changes;113 identities preserved.'],closure=False,interpretation='74of113 inspected;39unread;four crosscutting obligations open.');write(BASE/'census-register.json',reg)
    mapping=deepcopy(read(PRIOR/'task-map.json'))
    for fam in mapping['task_families']:
        if row['id'] in fam.get('uninspected_candidate_ids',[]):fam['uninspected_candidate_ids'].remove(row['id'])
        if fam['id'] in row['task_families']:
            for field,vals in [('inspected_candidate_ids',[row['id']]),('inspected_source_keys',row['publication_keys'])]:
                fam.setdefault(field,[]);fam[field].extend(x for x in vals if x not in fam[field])
        fam['coverage_acceptance']=False
    mapping.update(register=ref(BASE/'census-register.json','74/39successor'),supersedes=ref(PRIOR/'task-map.json','Preserved mapping'));write(BASE/'task-map.json',mapping)
    evidence=[ref(BASE/n,'Reviewed source and proposal evidence') for n in ['source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review-v2.json','development.tex','sponsor-addition.md','omissions-register.json','census-register.json','task-map.json']]+[ref(Path(__file__),'Preserving review logic')]
    review=dict(status='pass_for_scoped_adverse_source_review',reviewer=dict(name='Codex author/coordinator',kind='author'),candidate=row['id'],evidence=evidence,findings=['Three audited records bind original,20inspected source blobs and exact project examples.','Scorer, provenance, dependency and statistical limits remain explicit.','Only candidate181 advances to74/39;four crosscutting tasks remain open.'],limitations=LIMITS,coverage_acceptance=False,native_execution=False,visual_acceptance=False)
    verify_bindings(review);write(BASE/'review.json',review)
    write(BASE/'progress.json',dict(finding='Candidate181 original and selected immutable sources reviewed; exact observer/retention/dependence witnesses developed;74/39census.',next_action='Publish preserving unlearning reader/sponsor pair and renew exact-reader checks; continue39unread originals and four crosscutting tasks.',yield_reason='Release the census operation for publication, not a global stop.',evidence=[ref(BASE/'review.json','Scoped review'),ref(BASE/'census-register.json','74/39census')]))
    print(json.dumps(dict(inspected=74,unread=39,audited_records=3,authenticated_blobs=25,claim_inspected_blobs=len(records),native_execution=False)))


if __name__=='__main__':main()
