#!/usr/bin/env python3
"""Bind the recovered exact-version papers and independent authored examples."""
import hashlib
import json
from pathlib import Path
import subprocess

import advice_validity_reference_20261017 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ROOT/'docs/program/execution/2026-10-17/census-recovery'
BASE = RECOVERY/'advice-validity-v1'
RAW = ROOT/'docs/literature/raw'
LIMITS = [
    'Author primary-source and mathematical review; no acquired upstream code, LLM or bank experiment executed.',
    'Long et al. assumes the true starting MEC and an adviser error model; posterior mass is not automatic fixed-truth coverage.',
    'Zhang et al. findings concern published v1 text, pseudocode and prompt, not uninspected implementation or linked manual-review website.',
    'The source survey counts, Barley statement and bibliometric search specificity remain unreconciled.',
    'Both papers are additional citation-chain leads; the original census remains37 inspected/76 unread of113, plus4 cross-cutting records.',
    'Independent examples are stipulated exact constructions, not observed source failures, model accuracy, bank data or ROI.',
    'Source code, complete rights and scalable runtime qualification remain open; no exclusive-depth or mandatory-repair acceptance awarded.',
    'Visual acceptance remains false under the exhausted inherited image allowance; Q1/Q5 and final acceptance remain open.']


def read(path):
    return json.loads(path.read_text())


def paper(key, raw_id, title, first, author, year, version, pages, digest, anchors, claims, issues):
    original = RAW/(raw_id+'.pdf')
    receipt_path = original.with_suffix('.receipt.json')
    receipt = read(receipt_path)
    assert receipt['status'] == 'saved' and receipt['http_status'] == 200
    assert receipt['sha256'] == hashlib.sha256(original.read_bytes()).hexdigest() == digest
    assert receipt['bytes'] == original.stat().st_size
    destination = ROOT/'docs/papers'/(title+' '+first+f'({year}).pdf')
    assert not destination.exists()
    destination.write_bytes(original.read_bytes())
    stem = 'imperfect' if first == 'Long' else 'consistency'
    full = BASE/(stem+'-full.txt')
    subprocess.run(['pdftotext', '-layout', str(destination), str(full)], check=True, timeout=20)
    extracted = full.read_text().split(chr(12))
    assert sum(bool(p.strip()) for p in extracted) == pages
    reviewed = []
    for number, finding in anchors.items():
        excerpt = BASE/(stem+f'-page-{number}.txt')
        excerpt.write_text(extracted[number-1])
        reviewed.append(dict(anchor=f'Physical PDF page{number}', finding=finding,
                             extracted_text=ref(excerpt, 'Inspected genuine primary page')))
    return dict(integrated_citation_key=key, kind='paper', title=title,
        filename_title=title, first_author=first, author=author, year=year,
        source_identity=receipt['url'], version_date=version+'; acquired2026-10-17',
        cutoff='2026-10-07', local_copy=ref(destination, 'Authentic exact-version scholarly PDF'),
        local_path=str(destination.relative_to(ROOT)), sha256=digest,
        inspected_anchors=reviewed, related_primary_bytes=[ref(original, 'Preserved retrieved original'),
            ref(receipt_path, 'Successful bounded HTTPS receipt')],
        supported_claims=claims, unresolved_source_issues=issues, limitations=LIMITS)


def main():
    assert BASE.exists() and (BASE/'plan.md').exists() and not (BASE/'source-audit.json').exists()
    write(BASE/'plan-review.json', dict(status='pass', issues=[],
        scope='Author review of concrete source, mathematical and preserving-publication plan',
        evidence=[ref(BASE/'plan.md', 'Reviewed continuation'),
            ref(RECOVERY/'search-v11/plan-review.json', 'Bounded acquisition review'),
            ref(ROOT/'tools/advice_validity_reference_20261017.py', 'Independent exact reference inspected')],
        findings=[
            'Exact PDFs precede technical claims; known-class and adviser-model assumptions stay explicit.',
            'Coefficient covariance, all-simple-path d-separation and full finite enumeration are independent reference routes.',
            'Pseudocode defects do not establish behavior of uninspected code; linked website and code/rights remain scoped omissions.',
            'L3/L7 integration preserves existing source identities and citation contexts without automatic depth credit.',
            'Publication, checks and Git are bounded recovery work, followed by eligible source/chapter work.'],
        visual_acceptance=False, global_blocker=False))
    long = paper('exec17_imperfect_experts', 'exec17_census_search11_imperfect_v1',
        'Causal Discovery with Language Models as Imperfect Experts', 'Long',
        'Stephanie Long and Alexandre Piché and Valentina Zantedeschi and Tibor Schuster and Alexandre Drouin',
        2023, 'arXiv2307.02390v1,2023-07-05', 10,
        'b227fd07b54e279d5b117a07319c054831e5b1da2f2b29a3d684e86f9efe2460', {
            1:'Title, five authors and exact arXiv v1 date.',
            2:'Known true MEC, metadata-only pair adviser and true-graph retention target.',
            3:'Uniform prior on legal DAGs; conditionally factorized constant-error expert; joint posterior and greedy size/risk strategies.',
            4:'Ground-truth-derived starting MEC,5/8 repetitions, GPT3.5 historical models, ALARM ambiguity and003 overconfidence.',
            5:'Conclusion retains dependence on a suitable error model and discusses future uncertainty in the starting MEC.',
            8:'Code/codebook links are leads; scored A/B log probabilities, softmax and randomized causal verbs; deterministic fixed prompt.'}, [
            'The method refines a known true MEC using metadata-based imperfect pair orientations under an explicit adviser-error model.',
            'The prior is uniform over legal DAGs and posterior orientations are dependent even when adviser errors factorize.',
            'Greedy graph-size/risk choices use posterior retention; no automatic frequentist guarantee for a learned starting class follows.',
            'The experiment starts from benchmark true-graph MECs and reports ALARM metadata problems and text-davinci003 overconfidence.',
            'Historical text-davinci002/003 scoring, randomized causal verbs and small repetition counts do not qualify a current banking model.'], [
            'Causal-disco code, codebooks, license and runtime not inspected here.',
            'No general adviser calibration, bank ontology or learned-starting-class guarantee established.'])
    zhang = paper('exec17_benchmark_consistency', 'exec17_census_search11_consistency_v1',
        'Consistency evaluation of benchmarks used for causal discovery', 'Zhang',
        'Yuzhe Zhang and Chihui Chen and Lina Yao and Chen Wang', 2026,
        'arXiv2606.01789v1,2026-06-01', 32,
        '360dd9e8f67432cab42e5491f39386a044351175a08fcc6b5089e9990c9543f4', {
            1:'Title, four authors, exact date and reported11 benchmark/38081 full-text scope.',
            2:'Conference selection process and Barley misalignment assertion.',
            3:'96 selected papers and69 unique benchmarks; distinction from the arXiv bibliometric search.',
            4:'Claim11633 LLM discovery papers in2025; correct definition includes collider-activation condition omitted from Algorithm1.',
            5:'Association/d-separation converse and adjacent-always-correlated claim require more than Markov.',
            6:'Retrieval rank cap500, pair cap200, PubMed/PMC/OpenAlex routes, synonym expansion, Qwen model/H100, unknown denominator and Barley exclusion.',
            22:'Appendix benchmark list reaches72; main text69 retained unreconciled.',
            23:'MATH/ImageNet/COCO bibliometric labels; reported manual90/100 check and uninspected linked details.',
            24:'Algorithm1 minimal hitting sets of collider-free paths; adjacency branch; Table2 answer categories.',
            25:'Prompt rule3 converts nonsignificant tests to independence; conditioning and covariate language.'}, [
            'The proposed pipeline retrieves literature, forms graph-derived association queries and uses an LLM verifier with an unknown category.',
            'Reported scope is96 papers/69 benchmarks surveyed and11 benchmarks/38081 full texts evaluated; limits and conflicting appendix count remain.',
            'Unknown answers are excluded from the reported inconsistency-rate denominator.',
            'Published adjacency claims need faithfulness beyond Markov, and Algorithm1 does not check conditioning-activated collider paths.',
            'The published prompt treats nonsignificant association tests as independence; this is not statistically justified.',
            'Manual90/100 correctness is author-reported; its linked artifacts are not inspected here.'], [
            'Main69 benchmarks versus appendix72 remain unreconciled.',
            'Introduction lists Barley as misaligned, but evaluation excludes it.',
            'Bibliometric search specificity is unresolved: large headline count and unrelated benchmark labels cannot establish field size.',
            'Linked manual-review website and upstream implementation not inspected.',
            'Apparent literature inconsistency can reflect population, measurement, conditioning, intervention or selection differences.'])
    write(BASE/'exact-results.json', exact.serial(exact.calculate()))
    derivation = dict(integrated_citation_key='exec17_advice_validity_exact', kind='project_derivation',
        title='Joint adviser evidence, active-path and nonsignificance exact references',
        author='Causal banking proposal', year=2026, version_date='2026-10-17',
        source_identity='Project-authored exact graph, Gaussian and binary examples',
        local_copy=ref(BASE/'exact-results.json', 'Exact rational results and complete finite references'),
        inspected_anchors=['Three legal DAGs and factorized adviser likelihood; dependent repeated-answer joint law',
            'Positive-density Gaussian cancellation covariance and determinant',
            'All-simple-path active-path oracle versus published collider-free hitting-set specification',
            'Gaussian conditional covariance -2/7 from independent disturbance coefficients',
            'All256 binary sample sequences and exact Fisher hypergeometric distribution',
            'Stipulated missing-answer bounds and randomized incremental USD20'],
        supported_claims=[
            'Agreeing advice produces posterior81/91,9/91,1/91; conflicting advice produces9/19,1/19,9/19.',
            'Five copies of one noisy answer retain posterior.9; falsely independent copies yield59049/59050.',
            'A positive-density Markov Gaussian SCM can have adjacent independent X,Y by cancellation.',
            'The stipulated Algorithm1 output{Z} leaves two active paths and conditional covariance-2/7;{B,Z} separates.',
            'A randomized binary effect.5 admits balanced four-row data with probability27/512 and Fisher p1; hypothetical valueUSD20.',
            'Twenty contradictions among30 answered of100 stipulated queries yield answered rate2/3 and full-query range[.2,.9].'],
        records=[ref(ROOT/'tools/advice_validity_reference_20261017.py', 'Independent authored reference')],
        limitations=LIMITS)
    sources = [long, zhang, derivation]
    write(BASE/'source-audit.json', dict(cutoff='2026-10-07', sources=sources,
        prior=ref(RECOVERY/'copilot-v1/publication-v2/reader/source-audit.json', '742 predecessor records')))
    verify_bindings(read(BASE/'source-audit.json'))
    write(BASE/'primary-review.json', dict(status='pass', issues=[], reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Bounded exact-version primary text and independently verified mathematical review',
        sources=sources, source_limits=long['unresolved_source_issues']+zhang['unresolved_source_issues'],
        evidence=[ref(BASE/'plan-review.json', 'Reviewed plan'), ref(BASE/'exact-results.json', 'Exact reference results'),
            ref(Path(__file__), 'Audits and primary-page selections')], limitations=LIMITS,
        upstream_executed=False, final_acceptance=False, visual_acceptance=False))
    prior = RECOVERY/'copilot-v1/citation-chain-register.json'
    write(BASE/'citation-chain-register.json', dict(
        original_census=ref(RECOVERY/'benchmark-v1/census-register.json', 'Unchanged original census'),
        predecessor_additional_leads=ref(prior, 'Separately inspected Copilot lead retained'),
        original_inspected=37, original_unread=76, original_candidates=113, cross_cutting_records=4,
        new_additional_leads=[dict(id=key, title=source['title'], disposition='inspected_primary_retained_with_limits',
            source_key=source['integrated_citation_key'], primary_review=ref(BASE/'primary-review.json', 'Inspected original'))
            for key, source in [('citation-chain-imperfect-2307.02390', long), ('citation-chain-consistency-2606.01789', zhang)]],
        total_additional_inspected_leads=3, original_census_closed=False, saturation_claim=False))
    write(BASE/'omissions.json', dict(cutoff='2026-10-07', global_blocker=False,
        entries=[dict(candidate='Causal-disco source, codebooks and license',
                      identity='https://github.com/StephLong614/Causal-disco',
                      disposition='Paper link inspected; upstream bytes, rights and runtime not inspected',
                      next_action='Acquire cutoff-pinned source and rights before making code-adoption claims.'),
                 dict(candidate='Benchmark-consistency linked manual-review artifacts and implementation',
                      disposition='Paper-reported check only; original linked artifacts not inspected',
                      next_action='Resolve exact links and acquisition; compare code to pseudocode without assuming identity.'),
                 dict(candidate='Systematic longitudinal/off-policy LLM coverage',
                      disposition='Title-restricted20-of259 metadata query is noisy and not primary evidence or saturation',
                      next_action='Continue independent focused citation-chain and task-specific searches.')],
        evidence=[ref(BASE/'primary-review.json', 'Retained primary limitations')]))
    print(json.dumps(dict(primary_review='pass', added_records=3, genuine_pdfs=2,
        original_census='37 inspected/76 unread of113', additional_inspected_leads=3)))


if __name__ == '__main__':
    main()
