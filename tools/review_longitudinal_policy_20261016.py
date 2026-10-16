#!/usr/bin/env python3
"""Audited primary-source synthesis and exact authored policy references."""
import argparse
import ast
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess

import master_control as core
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-16/longitudinal-policy'
RAW = ROOT/'docs/literature/raw'
PRIOR = ROOT/'docs/program/execution/2026-10-16/dagma-reuse/publication-v2/reader/source-audit.json'
OP = 'LL.TASK.longitudinal_policy'
OUTPUT = ROOT/('docs/program/comprehensive-v14/work/'+OP+'/task-synthesis.md')
PIN = '3b88317fc074eeeff3a25825ef7fe3db3dce9309'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Bounded primary-literature synthesis, static code inspection and exact authored arithmetic; no upstream imports, live LLM evaluation or fitted bank policy.',
    'Cutoff 2026-10-07 Asia/Shanghai; broad and off-policy searches are noisy and not exhaustive. Candidate122 original remains unavailable to this review.',
    'No root reuse license or dependency lock was found in the complete pinned tree; paper states rebuilt datasets cannot be redistributed.',
    'Model revisions, dependencies, full data rights and native execution remain prerequisites to any reuse; no integration capability is enabled.',
    'General longitudinal identification, representation sufficiency, learned-policy uncertainty, missing-not-at-random recovery and bank truth remain conditional or research questions.',
    'Banking amounts and support probabilities are stipulated examples, not measured performance, actual prices or bank ROI.',
    'Six-preview session allowance is exhausted; extracted text and bounds do not confer rendered visual acceptance, Q1 or Q5.'
]


def exact():
    """Finite laws, enumeration and a separate backward calculation."""
    p = F(2, 5)
    def y(l, a): return F(102-40*l+(30*l-8)*a)
    adaptive = sum(w*y(l, l) for l, w in [(0, 1-p), (1, p)])
    fixed_marginal = sum(w*v*y(l, a) for l, w in [(0, 1-p), (1, p)]
                         for a, v in [(0, 1-p), (1, p)])
    no_second = sum(w*y(l, 0) for l, w in [(0, 1-p), (1, p)])
    assert adaptive == F(474, 5) and fixed_marginal == F(438, 5)
    assert adaptive-fixed_marginal == F(36, 5) and no_second == 86
    backward = F(102)-40*p+p*22
    factorized = F(102)-40*p+p*(30*p-8)
    assert backward == adaptive and factorized == fixed_marginal
    historical = F(3, 4)*120+F(1, 4)*60-8
    generator = F(1, 4)*120+F(3, 4)*60-8
    assert (historical, generator) == (97, 67)
    # At s=0, the derivative is20 but the s=1 finite contrast is-20.
    def value(s): return F(100)+20*s-40*s*s
    h = F(1, 1000)
    derivative = (value(h)-value(-h))/(2*h)
    assert derivative == 20 and value(1)-value(0)-8 == -28
    with localcontext() as ctx:
        ctx.prec = 40
        q = Decimal('0.1')**4
        retained_q = q*Decimal('0.8')**4
        zero = (1-q)**10000
        retained_zero = (1-retained_q)**10000
    return {
        'scope': 'Independent exact authored constructions, not upstream runtime or empirical performance.',
        'text_versions': {'gross_USD': [120, 60], 'cost_USD': 8,
            'historical_first_version_probability': '3/4', 'generator_first_version_probability': '1/4',
            'historical_net_USD': str(historical), 'generator_net_USD': str(generator),
            'difference_USD': str(historical-generator)},
        'adaptive_rollout': {'law': 'P(L1=1|do(A0=1))=2/5;Y=102-40L1+(30L1-8)A1',
            'adaptive_rule': 'A1=L1', 'broken_rule': 'A1~Bernoulli(2/5) independent of regenerated L1',
            'adaptive_USD': str(adaptive), 'fixed_marginal_USD': str(fixed_marginal),
            'no_second_contact_USD': str(no_second), 'difference_USD': str(adaptive-fixed_marginal),
            'adaptive_gain_over_no_second_USD': str(adaptive-no_second),
            'fixed_marginal_gain_over_no_second_USD': str(fixed_marginal-no_second),
            'backward_reference_USD': str(backward), 'independent_factorization_USD': str(factorized)},
        'local_vs_finite': {'gross_value': '100+20s-40s^2', 'origin_derivative_USD_per_style_unit': str(derivative),
            'finite_style_change': 1, 'gross_change_USD': str(value(1)-value(0)),
            'deployment_cost_USD': 8, 'finite_net_change_USD': str(value(1)-value(0)-8)},
        'support': {'steps': 4, 'each_required_action_probability': '1/10',
            'independent_trajectories': 10000, 'path_probability': str(q),
            'expected_matches': str(q*10000), 'zero_matches_probability': str(zero),
            'each_step_independent_retention': '4/5', 'complete_path_probability': str(retained_q),
            'expected_complete_matches': str(retained_q*10000),
            'zero_complete_matches_probability': str(retained_zero),
            'scope': 'Planning arithmetic under independent action/retention stipulations; no estimator variance or accuracy claim.'},
        'clock': {'event_day': 7, 'available_day': 9, 'decision_day': 8,
            'available_for_decision': 9 <= 8},
        'monte_carlo_work': {'outer_draws': 50, 'inner_draws': 50,
            'outcome_rows_per_case': 50*50, 'scope': 'Source loop count, not effective independent sample size or measured runtime.'}
    }


PAPERS = {
    'exec13_census_collaboration': {
        1: 'Exact identity and arXiv version',
        4: 'Sequential edits and responses; original treatment-history g-formula',
        5: 'ISE derivative, conditional text-version mixture, Theorem1 with exchangeability and positivity',
        6: 'CVAE, outcome model and Monte Carlo Algorithm1; semi-synthetic evaluation rationale',
        7: 'Generated counterfactual data, label and constructed confounding design',
        8: 'Table2; CoAuthor .188/.353 unadjusted versus .216/.219 G-E+CVAE; three seeds',
        9: 'Discussion and public code identity',
        10: 'Optimal strategies future work; rebuilt datasets research-only and cannot be redistributed'
    },
    'v12_la_2407_19118': {4: 'Target population, eligibility, time-varying exposure and causal roadmap',
                         9: 'Co-pilot responsibilities and limitations'},
    'v12_la_2305_16183': {5: 'Task experiments and need for intervention at evaluation',
                         19: 'AppendixB.2 active test-time exploration critical'},
    'v12_la_2608_09696': {3: 'Open-loop versus closed-loop prediction definitions',
                         4: 'Experiments use open-loop policies'},
    'v12_la_2607_22443': {1: 'Human-augmenting workflow and supplied causal assumptions',
                         7: 'Multiple simultaneous treatments via partially linear models'},
    'exec15_latent_shi': {6: 'Two-wave linear non-Gaussian assumptions and scalar confounder',
                         9: 'Nonzero higher-cumulant detection premises',
                         29: 'Path detection does not consistently estimate effect magnitude'}
}


def sources():
    tree = json.loads((RAW/'exec16_longpolicy_collab_tree.json').read_text())
    assert tree['sha'] == PIN and tree['truncated'] is False
    blobs = {r['path']: r for r in tree['tree'] if r['type'] == 'blob'}
    commit = json.loads((RAW/'exec16_longpolicy_collab_cutoff.json').read_text())[0]
    assert commit['sha'] == PIN and commit['commit']['committer']['date'][:10] == '2024-06-24'
    records = []
    for n in range(1, 6):
        plan = json.loads((BASE/f'acquisition-{n:02}.json').read_text())
        for row in plan['requests']:
            if 'source_path' not in row and row['id'] != 'exec16_longpolicy_collab_readme':
                continue
            path = RAW/(row['id']+'.txt')
            receipt_path = RAW/(row['id']+'.receipt.json')
            receipt = json.loads(receipt_path.read_text())
            data = path.read_bytes()
            assert receipt['status'] == 'saved' and receipt['sha256'] == core.sha(path)
            source_path = row.get('source_path', 'README.md')
            actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert actual == blobs[source_path]['sha'] and len(data) == blobs[source_path]['size']
            anchors = []
            if source_path.endswith('.py'):
                for item in ast.walk(ast.parse(data.decode())):
                    if isinstance(item, (ast.FunctionDef, ast.ClassDef)):
                        anchors.append({'symbol': item.name, 'first_line': item.lineno,
                                        'last_line': item.end_lineno})
            records.append({'source_identity': row['url'], 'version_date': PIN+';2024-06-24',
                'source_path': source_path, 'git_blob_sha1': actual,
                'local_copy': ref(path, 'Original pinned bytes; inspected source control flow'),
                'retrieval': ref(receipt_path, 'Public acquisition identity and SHA256'),
                'inspected_anchors': anchors or ['README run example, code/paper identity and dataset links']})
    assert len(records) == 22
    prior = json.loads(PRIOR.read_text())
    index = {s['integrated_citation_key']: s for s in prior['sources']}
    paper_reviews = []
    (BASE/'inspected').mkdir(exist_ok=True)
    for key, anchors in PAPERS.items():
        record = index[key]
        if 'local_path' in record:
            pdf = ROOT/record['local_path']; expected = record['sha256']
        else:
            named = record.get('scholarly_pdf', record['local_copy'])
            pdf = ROOT/named['path']; expected = named['sha256']
        assert core.sha(pdf) == expected
        text = BASE/(key+'-review.txt')
        assert not text.exists()
        subprocess.run(['pdftotext', '-layout', str(pdf), str(text)], check=True, timeout=30)
        pages = text.read_text().split('\f')
        extracts = []
        for page, finding in anchors.items():
            assert pages[page-1].strip()
            target = BASE/'inspected'/(key+f'-page-{page}.txt')
            with target.open('x') as stream: stream.write(pages[page-1])
            extracts.append({'pdf_page': page, 'finding': finding,
                             'extract': ref(target, 'Inspected primary technical page')})
        paper_reviews.append({'citation_key': key, 'title': record['title'],
            'source_identity': record.get('source_identity', record.get('url')),
            'version_date': record.get('version_date', record.get('published')),
            'original': ref(pdf, 'Genuine inherited scholarly PDF; exact version retained'),
            'inspected_anchors': extracts})
    findings = [
        'main -> loading -> frame/model factories -> g_adjust_model: caller, fit, last-state sampling and output paths inspected.',
        'README CVAE differs in case from cVAE dispatch key; default action_num=2, decompose_a=0 and cuda=7.',
        'utils imports unrevisioned bert-base-uncased weights and unconditionally calls feature_model.cuda after a CPU branch.',
        'Shuffled row KFold is not grouped by participant/topic; those IDs are retained by the CoAuthor loader. Leakage magnitude was not measured.',
        'cal_g_estimate fixes supplied action/style vectors, resamples baseline embeddings and last state; no history-dependent action recomputation occurs in this path.',
        'sk_gMLP uses a learned conditional mean and Normal noise with default sigma=1 for the last state; arbitrary-horizon adaptive recursion is not supplied by that path.',
        'sk_cVAE sets kld_weight=0; inherited vae_loss backpropagates MSE plus zero times KL. Both encoders and decoder are linear; encoded representation sampling is stochastic.',
        'Reported outputs are observed/counterfactual class probabilities, gE0/gE1 and MSE; this inspected caller/output path has no explicit ISE limit/derivative or confidence interval.',
        'Optional decompose_cond reuses a PCA object across different history widths; not executed or qualified here.',
        'Complete pinned tree has no LICENSE, requirements lock, package setup or tests. Public source visibility is not reuse permission.',
        'Twenty-two original blobs verified; no upstream source was imported or executed. Other dataset loaders and installed dependency behavior remain uninspected.'
    ]
    write(BASE/'source-review.json', {'repository': 'XMUBQ/dtr-text', 'pin': PIN,
        'commit_date': commit['commit']['committer']['date'], 'complete_tree': ref(RAW/'exec16_longpolicy_collab_tree.json', 'All28 blobs;not truncated'),
        'cutoff_commit': ref(RAW/'exec16_longpolicy_collab_cutoff.json', 'Latest returned commit under client cutoff'),
        'records': records, 'papers': paper_reviews, 'findings': findings,
        'root_license_found': False, 'upstream_execution': False, 'limitations': LIMITS})
    leads = []
    searches = []
    for name in ['exec16_longpolicy_search', 'exec16_longpolicy_search_specific']:
        saved = json.loads((RAW/(name+'.json')).read_text())
        receipt = json.loads((RAW/(name+'.receipt.json')).read_text())
        assert receipt['sha256'] == core.sha(RAW/(name+'.json'))
        searches.append({'source': ref(RAW/(name+'.json'), 'Discovery metadata only'),
            'query_url': receipt['url'], 'reported_hits': saved['meta']['count'],
            'returned': len(saved['results']), 'technical_evidence': False})
        leads += [{'title': r['display_name'], 'date': r['publication_date'], 'doi': r.get('doi'),
                   'disposition': 'Metadata-only search lead; no added technical citation or claim'} for r in saved['results']]
    identity = json.loads((RAW/'exec16_longpolicy_candidate122_identity.json').read_text())['message']
    write(BASE/'omissions-register.json', {
        'cutoff': '2026-10-07 Asia/Shanghai', 'searches': searches, 'metadata_leads': leads,
        'candidate122': {'title': identity['title'][0], 'doi': identity['DOI'],
            'identity': ref(RAW/'exec16_longpolicy_candidate122_identity.json', 'Crossref identity only'),
            'disposition': 'Original not inspected; no technical inference from metadata. MDPI outside current fixed collector host list.',
            'revisit': 'Acquire permitted authentic original, inspect method/targets/data rights and then compare.'},
        'candidate148': {'disposition': 'Recovered genuine Shi original in earlier task; now compared with correct two-wave discovery scope.',
            'evidence': ref(ROOT/'docs/program/execution/2026-10-15/latent-temporal/candidate-reassessment.json', 'Preserved candidate recovery')},
        'inherited_failures': [
            ref(BASE/'sandbox-dns-failure.json', 'Saved initial source-read failure; later successful retries do not erase it'),
            ref(ROOT/'docs/program/repair-v12/work/LA01/source-audit.json', 'Original literature coverage and failed provider requests')
        ],
        'remaining': [
            {'gap': 'Relevant-source census saturation', 'route': 'Task-specific searches, citation chaining and genuine originals; neither noisy ten-hit response exhausts literature.'},
            {'gap': 'Code and data reuse rights', 'route': 'Clarify upstream license, transitive model/data terms and redistribution; use independently generated examples meanwhile.'},
            {'gap': 'Adaptive policy implementation', 'route': 'Implement/verify bounded history-conditioned recursion and matched deterministic baselines before exposing an adapter.'},
            {'gap': 'Scientific extensions', 'route': 'Representation sufficiency, hidden time-varying confounding, learned-policy inference and support violations need assumptions, designs or research, not generic prompt repair.'}
        ], 'limitations': LIMITS})
    print(json.dumps({'verified_source_blobs': len(records), 'primary_papers': len(paper_reviews),
                      'search_hits_returned': len(leads), 'upstream_execution': False}))


def numbers():
    result = exact()
    write(BASE/'exact-results.json', result)
    write(BASE/'independent-arithmetic-review.json', {
        'status': 'pass', 'method': 'Exact Fraction enumeration versus backward/factorized formulas;40-digit Decimal binomial calculation',
        'evidence': [ref(BASE/'exact-results.json', 'Six authored reference families'),
                     ref(Path(__file__), 'Reproducible exact function')],
        'findings': ['Adaptive94.8 versus independent-action87.6;difference7.2USD.',
                     'Text-version mixture97 versus67USD despite same style scalar.',
                     'Positive origin derivative20 does not prevent finite net loss28USD.',
                     'Four0.1 support factors give expected matching count1 in10000 trajectories.',
                     'Event day7 available day9 is excluded from day8 decision.'],
        'not_claimed': ['Upstream runtime', 'Estimated model accuracy', 'Statistical coverage', 'Bank ROI']})
    print(json.dumps({'exact_references': 'pass', 'adaptive_gap_USD': 7.2,
                      'zero_matches_probability': result['support']['zero_matches_probability']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['sources', 'numbers'])
    args = parser.parse_args()
    {'sources': sources, 'numbers': numbers}[args.command]()
