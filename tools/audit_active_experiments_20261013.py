#!/usr/bin/env python3
"""Bind primary active-design literature, inert package sources and omissions."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/active-experiments'
RAW = ROOT / 'docs/literature/raw'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def anchors(path, needles, pdf=False):
    text = path.read_text()
    result = []
    for needle in needles:
        at = text.find(needle)
        assert at >= 0, (path, needle)
        a = {'phrase': needle, 'line': text[:at].count('\n')+1}
        if pdf:
            a['physical_pdf_page'] = text[:at].count('\f')+1
        result.append(a)
    return result


def main():
    assert not (BASE / 'source-audit.json').exists(), 'Preserve completed source audit'
    assert (ROOT / 'docs/literature/fetch-manifest.json').read_bytes() == (BASE / 'previous-fetch-manifest.json').read_bytes()
    acquired = []
    for batch in range(1, 5):
        for request in json.loads((BASE / f'fetch-{batch:02}.json').read_text())['requests']:
            p = RAW / (request['id']+'.receipt.json')
            receipt = json.loads(p.read_text())
            item = {'request': request, 'receipt': ref(p, 'Actual bounded HTTPS outcome'),
                    'status': receipt['status'], 'error': receipt.get('error')}
            if receipt['status'] == 'saved':
                q = ROOT / receipt['path']
                assert hashlib.sha256(q.read_bytes()).hexdigest() == receipt['sha256']
                item['bytes'] = ref(q, 'Acquired primary bytes; inspection scope recorded separately')
            acquired.append(item)
    assert len(acquired) == 28
    write('acquisition-review.json', {'cutoff': '2026-10-07', 'accessed': '2026-10-13',
          'requests': acquired, 'request_count': 28,
          'saved': sum(x['status'] == 'saved' for x in acquired),
          'failed': sum(x['status'] != 'saved' for x in acquired),
          'collector_manifest_restored': True, 'downloaded_code_executed': False,
          'limit': 'Finite follow-up of the saved census and paper-linked packages, not a new exhaustive frontier search.'})
    sources = []
    paper_specs = [
        ('2609_33357', 'DISCERN: Can AI Agents Work Like Scientists and Guide Discovery?', 'Huang',
         'Nan Huang and coauthors', '2026-09-27',
         ['79 Level 1', 'Hypothesis scoring and adversarial review.',
          'across models, while perfect-score', 'Limitations. Real public data',
          'median of three independent draws'],
         ['The paper evaluates 203 canonical life-science tasks: 79 L1, 102 L2 and 22 L3, across eight models and eight tracks.',
          'The levels are independently instantiated, not an executed end-to-end research pipeline; L3 counterfactual eligibility is model-prior dependent.',
          'Reported perfect-score percentages 60.8, 34.2 and 0.6 use distinct level-specific rubrics, not scientific discovery success probabilities.',
          'Human-designed grading includes deterministic L1/L2 scoring with LLM verification/adjudication and rubric-based L3 grading.',
          'Limits include task dependence, prior familiarity, residual grading uncertainty, and no established useful experimental follow-up.'],
         'Preprint; no independent reproduction, bank transfer or measured experiment benefit inferred.'),
        ('2609_15973', 'Discovery Foundation Models: Toward Open-Ended Discovery Intelligence', 'Yang',
         'Ling Yang, Zhenfei Yin and Yingcheng Wu', 'arXiv v1 stamp 2026-09-14; document front page 2026-09-15',
         ['Zetema specifies functional interfaces', 'Attribution precedes promotion.',
          'What this case establishes', 'broader cross-domain discovery transfer',
          'The budget includes more than tokens'],
         ['The report proposes explicit revisable research states, experimental gating and validation of transferred discovery skills.',
          'Its GALILEO discussion attributes specialized assays in the described coupled system to human execution as appropriate.',
          'The reported therapeutic case does not establish general-purpose discovery or broad cross-domain transfer.',
          'Matched evaluation should account for compute, expert time, tool/simulator calls and physical costs.'],
         'Framework and author-reported case account; original biomedical study and linked project implementations not independently inspected. No causal performance claim.')]
    for ident, title, surname, author, date, needles, claims, limits in paper_specs:
        raw = RAW / f'exec13_active_{ident}_v1.pdf'
        assert raw.read_bytes().startswith(b'%PDF')
        path = ROOT / 'docs/papers' / f'{title} {surname}(2026).pdf'
        if path.exists():
            assert path.read_bytes() == raw.read_bytes()
        else:
            path.write_bytes(raw.read_bytes())
        text = BASE / f'{ident}.txt'
        info = subprocess.check_output(['pdfinfo', str(path)], text=True, timeout=15)
        sources.append({'integrated_citation_key': 'exec13_active_'+ident, 'kind': 'paper',
            'title': title, 'filename_title': title, 'first_author': surname, 'author': author, 'year': 2026,
            'version_date': date, 'arxiv_version': ident.replace('_', '.')+'v1',
            'url': 'https://arxiv.org/pdf/'+ident.replace('_', '.')+'v1',
            'local_path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'pages': int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1)),
            'extracted_text': ref(text, 'Selected methods, findings and limitations inspected'),
            'retrieval_receipt': ref(RAW / f'exec13_active_{ident}_v1.receipt.json', 'Genuine original acquisition'),
            'source_identity': 'PDF title, first author and exact version/date stamp inspected',
            'accessed': '2026-10-13', 'cutoff_status': 'Stamped version no later than 2026-10-07; acquired later',
            'inspected_anchors': anchors(text, needles, pdf=True), 'supported_claims': claims,
            'inspection_scope': 'Selected primary passages; not every page or cited original.', 'limits': limits})
    package_specs = [
        ('glucosebench', 'murphyk/glucosebench', '6bb0ff6f44513e1e816ac3f0827531a366e8d7a0',
         '2026-09-27T18:16:38Z', 'MIT',
         {'readme.md': ['same patient', 'Minimal learner API', 'Scores and baseline'],
          'benchmark.txt': ['class Benchmark:', 'def observe(', 'def freeze(', 'def summarize('],
          'notice.txt': ['simglucose by Jinyu Xie', 'root license covers those additions'],
          'license.txt': ['MIT License', 'copyright notice'], 'vendor_license.txt': ['Copyright (c) 2017 Jinyu Xie', 'Permission is hereby granted'],
          'pyproject.txt': ['version = "0.1.0"', 'requires-python'], 'provenance.txt': ['upstream_sha256']},
         ['The documented benchmark forecasts interventions within the same simulated patient, not transfer to new patients or clinical use.',
          'The API returns public training/actions, limits acquisitions to six total episodes and freezes before evaluator access.',
          'summarize reports attempted/failed counts and null means if any query failed.',
          'Root and vendored MIT notices are present; the authors attribute physiological code/data to a pinned simglucose revision.',
          'Reuse the acquisition/evaluation contract as a proposal pattern; biological simulator behavior is not a bank structural model.'],
         'Source review only; no install/run, independent upstream hash validation or complete dependency/data redistribution clearance.'),
        ('neuronbench', 'murphyk/neuronbench', 'c354622458c460b419cab821d482c879f0578377',
         '2026-08-12T13:23:32Z', 'MIT',
         {'readme.md': ['The observation model', 'Budget rule', 'Evaluation criteria'],
          'agent.txt': ['def choose_experiment(', 'except Exception:', 'def forecast_counts(', 'def run_baseline('],
          'evaluator.txt': ['def held_out_targets(', 'def forecast_mse('],
          'license.txt': ['MIT License', 'copyright notice'],
          'pyproject.txt': ['version = "0.1.0"', 'requires-python']},
         ['The project exposes deterministic/stochastic electrophysiology experiments and held-out forecasts.',
          'Its reference agent accepts an injected language-model client; it is explicitly a baseline without Bayesian design inference.',
          'Experiment parse errors fall back to the first remaining protocol; forecast parse errors fall back to the observed mean or zero.',
          'A bank adapter must expose these fallbacks and separate evaluator truth from the learner rather than attributing all choices to an LLM.'],
         'No source executed, live backend or statistical reproduction; MIT file is not a dependency-wide legal audit.'),
        ('dfmplans', 'Gen-Verse/DFM-Plans', '14d47045d2fd30feca06d2cb30c70c510fad7614',
         '2026-09-19T23:27:32Z', 'Apache-2.0',
         {'readme.md': ['Individual research projects', 'It is a research design', 'Each is developed'],
          'license.txt': ['Apache License', 'Redistribution.']},
         ['The pinned README describes an overview/research map and says implementations are released in separate projects.',
          'The nontruncated pinned tree contains documentation/assets; it does not supply a complete executable Zetema implementation.',
          'The root Apache-2.0 license does not establish licenses, readiness or capabilities of separately linked projects.'],
         'Reject this overview repository as a directly executable causal agent; retain it as an architectural lead. Linked ScienceBuddy/ScienceIDE/JEPA-Anything code not inspected.')]
    for name, repo, pin, date, license_name, inspected, claims, limits in package_specs:
        paths = {suffix: RAW / f'exec13_active_{name}_{suffix}' for suffix in inspected}
        sources.append({'integrated_citation_key': 'exec13_active_'+name, 'kind': 'software_source',
            'title': repo+' pinned source and documentation', 'author': repo.split('/')[0], 'year': 2026,
            'version_date': f'{pin}, commit timestamp {date}; acquired 2026-10-13',
            'source_identity': repo, 'url': 'https://github.com/'+repo+'/tree/'+pin, 'commit': pin,
            'cutoff_status': 'Commit selected through cutoff query; current GitHub response does not independently prove historical public availability.',
            'local_copy': ref(paths['readme.md'], 'Pinned README'),
            'primary_files': [ref(p, 'Pinned inert text') for p in paths.values()],
            'tree': ref(RAW / f'exec13_active_{name}_tree.json', 'Nontruncated pinned tree'),
            'identity_metadata': [ref(RAW / f'exec13_active_{name}_{s}.json', 'Identity only') for s in ['meta', 'cutoff']],
            'inspected_anchors': {suffix: anchors(paths[suffix], needles) for suffix, needles in inspected.items()},
            'license_observed': license_name, 'supported_claims': claims, 'limits': limits,
            'runtime_executed': False, 'integration_allowed': False})
    census = ROOT / 'docs/program/execution/2026-10-13/llm-census/census-register.json'
    candidates = []
    for x in json.loads(census.read_text())['items']:
        if 'active_experiments' not in x.get('task_families', []):
            continue
        ident = x['id']; short = ident.rsplit('-', 1)[-1]
        if short in ['139', '141']:
            status = 'original_acquired_selected_methods_results_limits_inspected'
            next_action = 'Keep benchmark/framework scope restrictions; independently reproduce only under a separately registered protocol.'
        elif short in ['42', '165']:
            status = 'official_pdf_route_failed_non_pdf_response'
            next_action = 'Find an authentic author/repository original; do not cite a discovery abstract as technical evidence.'
        elif ident == 'LA01-bank-evidence':
            status = 'conditional_later_not_proposal_blocker'
            next_action = 'Require a relevant prototype and positive experiment value before a bank study.'
        else:
            status = 'original_uninspected_in_this_bounded_followup'
            next_action = 'Resolve identity/date/rights and acquire the original before making any technical claim.'
        candidates.append({'id': ident, 'title': x.get('title'), 'status': status, 'next_action': next_action,
                           'inherited_record': x})
    write('candidate-register.json', {'cutoff': '2026-10-07', 'source': ref(census, 'Saved task-specific candidate map'),
          'candidates': candidates, 'frontier_census_closed': False, 'market_absence_claim': False})
    omissions = [{'id': c['id'], 'gap': c['status'], 'next_action': c['next_action']}
                 for c in candidates if c['status'] != 'original_acquired_selected_methods_results_limits_inspected']
    omissions += [
        {'id': 'full-MDA-NLPSCM-implementation', 'gap': 'Benchmark repositories and paper dataset links do not establish the complete model-discovery or noisy-prior agent implementation.',
         'next_action': 'Acquire cutoff-pinned full agent source, tests and rights; compare numerical/random baselines before runtime admission.'},
        {'id': 'DISCERN-package', 'gap': 'No standalone implementation repository was verified from the inspected paper passages.',
         'next_action': 'Resolve an author-linked task/harness repository and inspect data rights and grading implementation.'},
        {'id': 'DFM-linked-projects', 'gap': 'Overview repository is not an implementation; separate project code and original biomedical report uninspected.',
         'next_action': 'Review the particular linked implementation/original needed for a scoped claim; do not inherit overview licenses or performance.'},
        {'id': 'bank-observation-law', 'gap': 'Costs, signal calibration, feasible bank interventions and model support are not empirically established.',
         'next_action': 'Use exact/generated planning now; obtain bank inputs only for a justified later experiment.'}]
    write('omissions-register.json', {'entries': omissions, 'frontier_census_closed': False,
          'proposal_blocked': False, 'unavailable_originals_are_not_cited_as_inspected': True})
    sources += [
        {'integrated_citation_key': 'exec13_active_exact', 'kind': 'project_derivation',
         'title': 'Exact acquisition value, availability, correlated evidence and stopping constructions',
         'author': 'Causal banking proposal project', 'year': 2026, 'version_date': '2026-10-13',
         'source_identity': 'Stipulated four-world planning model; exact rational enumeration',
         'local_copy': ref(BASE / 'exact-results.json', 'Exact planning values'),
         'code': ref(ROOT / 'tools/active_experiments_examples_20261013.py', 'World/signal enumeration'),
         'review': ref(BASE / 'exact-review.json', 'Replay and independent posterior/stop calculations'),
         'inspected_anchors': ['one_acquisition_budget', 'unavailability', 'two_independent_useful_queries', 'correlated_expert_copies', 'misspecified_support'],
         'supported_claims': ['Net values are -5, 23 and 9 for full-world-information, decision-value and uniform-random acquisition.',
                              'One-quarter unavailable attempts lower useful-query net value to 16.',
                              'For the declared horizon at most two, stopping after one useful query has optimal net value 23.',
                              'Five perfectly correlated positive expert answers retain posterior 4/5; false independence gives 1024/1025.'],
         'limits': 'No sampled study, calibrated expert/LLM accuracy, bank interventions or measured dollars.'},
        {'integrated_citation_key': 'exec13_active_scope', 'kind': 'project_evidence',
         'title': 'Bounded active-experiment literature and package follow-up',
         'author': 'Causal banking proposal project', 'year': 2026, 'version_date': '2026-10-13 with 2026-10-07 cutoff',
         'source_identity': 'Saved census follow-up, acquisition outcomes and explicit unresolved claims',
         'local_copy': ref(BASE / 'candidate-register.json', 'Eight mapped candidate dispositions'),
         'acquisition': ref(BASE / 'acquisition-review.json', '28 requests with actual failure records'),
         'omissions': ref(BASE / 'omissions-register.json', 'Remaining sources/implementation/calibration questions'),
         'inspected_anchors': ['candidates', 'frontier_census_closed', 'entries'],
         'supported_claims': ['Uninspected originals and unavailable full implementations are explicit; no comprehensive frontier or runtime claim.'],
         'limits': 'Finite corpus and acquisition routes; metadata cannot support technical capability claims.'}]
    write('source-audit.json', {'sources': sources, 'cutoff': '2026-10-07', 'runtime_executed': False,
          'acquisition': ref(BASE / 'acquisition-review.json', 'Successful/failed requests'),
          'preparer': ref(Path(__file__), 'Audited source identities, inspected passages and scope')})
    print(json.dumps({'sources': len(sources), 'papers': 2, 'packages': 3, 'requests': 28,
                      'frontier_census_closed': False}))


if __name__ == '__main__':
    main()
