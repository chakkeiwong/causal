#!/usr/bin/env python3
"""Prepare a finite vendor/source search, without downloading or running vendors."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-identification'
PRIOR = ROOT / 'docs/program/execution/2026-10-13'


def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    BASE.mkdir(exist_ok=True)
    assert not (BASE / 'search-protocol.json').exists(), 'Preserve the prepared search'
    candidates = json.loads((PRIOR / 'commercial-temporal/search-protocol.json').read_text())['candidate_universe']
    extra = {
        'StataCorp': ['teffects', 'eteffects', 'mediate', 'ivregress'],
        'SAS': ['CAUSALTRT', 'CAUSALMED', 'PSMATCH'],
        'IBM': ['SPSS Causal Inference', 'Amos'],
        'MathWorks': ['fitrauto', 'treatment effect'],
        'Bayesia': ['causal counterfactuals'],
        'BayesFusion': ['intervention', 'causal network'],
    }
    for row in candidates:
        row['aliases'] += extra.get(row['vendor'], [])
    candidates += [
        {'vendor': 'Bayes Server', 'aliases': ['Bayes Server', 'BayesServer', 'causal inference', 'counterfactual']},
        {'vendor': 'JMP', 'aliases': ['JMP', 'JMP Pro', 'causal treatment']},
        {'vendor': 'Lumina', 'aliases': ['Analytica', 'Analytica Decision Engine', 'influence diagram']},
    ]
    requests = [
        ('bayesia_criteria', 'Bayesia', 'https://www.bayesia.com/bayesialab/e-book/chapter-10-causal-effect-identification-and-estimation/causal-identification-and-estimation/graphical-identification-criteria', 'html'),
        ('bayesia_effect', 'Bayesia', 'https://www.bayesia.com/bayesialab/e-book/chapter-10-causal-effect-identification-and-estimation/causal-identification-and-estimation/effect-estimation', 'html'),
        ('bayesia_counterfactual', 'Bayesia', 'https://www.bayesia.com/bayesialab/tutorials/webinar-calculating-contributions-using-causal-counterfactuals', 'html'),
        ('genie_causal', 'BayesFusion', 'https://support.bayesfusion.com/docs/GeNIe/causal.html', 'html'),
        ('stata_teffects', 'StataCorp', 'https://www.stata.com/manuals/teteffectsintro.pdf', 'pdf'),
        ('stata_mediate', 'StataCorp', 'https://www.stata.com/manuals/causalmediate.pdf', 'pdf'),
        ('sas_causaltrt', 'SAS', 'https://support.sas.com/documentation/onlinedoc/stat/151/causaltrt.pdf', 'pdf'),
        ('sas_causalmed', 'SAS', 'https://support.sas.com/documentation/onlinedoc/stat/151/causalmed.pdf', 'pdf'),
        ('bayesserver_causal', 'Bayes Server', 'https://www.bayesserver.com/docs/techniques/causal-inference/', 'html'),
        ('bayesserver_counterfactual', 'Bayes Server', 'https://www.bayesserver.com/docs/techniques/counterfactual/', 'html'),
        ('jmp_causal', 'JMP', 'https://www.jmp.com/en/statistics-knowledge-portal/what-is-causal-inference', 'html'),
        ('analytica_causal', 'Lumina', 'https://docs.analytica.com/index.php/Causal_Models', 'html'),
        ('causalens_docs', 'causaLens', 'https://docs.causalens.com/', 'html'),
        ('mplus_causal', 'Mplus', 'https://www.statmodel.com/causal.shtml', 'html'),
    ]
    protocol = {
        'operation_id': 'SW.CELL.identification_counterfactual.commercial',
        'cutoff': '2026-10-07', 'access_date': '2026-10-13',
        'scope': 'Declared sixteen-family commercial identification/counterfactual landscape; no exhaustive world-market claim',
        'candidate_universe': candidates,
        'search_terms': ['adjustment', 'back-door', 'front-door', 'ID', 'IDC', 'counterfactual',
                         'abduction', 'intervention', 'partial identification', 'bounds', 'latent',
                         'positivity', 'licence', 'license', 'API'],
        'stopping_rule': {'max_new_gets': 28, 'max_seconds_per_get': 25,
                          'max_bytes_per_get': 8388608, 'max_concurrent_gets': 4,
                          'followups': 'At most two technical followups per family within the total cap. Historical unavailable sources remain omissions; no repeated retries of known access blocks.',
                          'local_search': 'Every declared name/alias searched literally in the three preserved commercial text corpora and all newly acquired text. Generic aliases are navigation hints, not vendor identification.'},
        'initial_requests': [{'id': key, 'vendor': vendor, 'url': url, 'extension': ext} for key, vendor, url, ext in requests],
        'acquisition_method': 'Existing allowed curl -fL public HTTPS command form with explicit size/time limits and saved headers; the frozen public_sources.py vendor allowlist is unchanged.',
        'review': [
            'Check documented targets and assumptions separately from fitted runtime and edition entitlement.',
            'Separate supplied-DAG adjustment, complete ID/IDC, cross-world counterfactuals, and identified bounds.',
            'Build exact independent lending examples showing observational and counterfactual ambiguity; no vendor performance claim.',
            'Keep mutable post-cutoff bytes, missing licenses, unavailable originals and unknown features explicit.',
            'Integrate developed findings into the current reader and record an inconclusive full-cell result if essential comparisons remain unavailable.',
            'No bank-data prerequisite, paid license, external message or downloaded-code execution is authorized by this search.'
        ]}
    write('search-protocol.json', protocol)
    corpus = sorted(p for name in ['commercial', 'commercial-latent', 'commercial-temporal']
                    for p in (PRIOR / name).glob('*.txt'))
    contents = {p: p.read_text(errors='replace') for p in corpus}
    results = []
    for row in candidates:
        aliases = []
        for alias in dict.fromkeys([row['vendor']] + row['aliases']):
            matches = []
            for p, text in contents.items():
                line_numbers = [i for i, line in enumerate(text.splitlines(), 1) if re.search(re.escape(alias), line, re.I)]
                if line_numbers:
                    matches.append({'path': str(p.relative_to(ROOT)), 'line_count': len(line_numbers), 'first_lines': line_numbers[:5]})
            aliases.append({'alias': alias, 'matches': matches})
        results.append({'vendor': row['vendor'], 'alias_searches': aliases})
    write('local-search.json', {'corpus': [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in corpus],
                                'results': results, 'claim': 'Local literal search only, not a global capability/absence conclusion'})
    print(json.dumps({'families': len(candidates), 'initial_gets': len(requests), 'local_texts': len(corpus)}))


if __name__ == '__main__':
    main()
