#!/usr/bin/env python3
"""Reexecute inherited finite witnesses against the current V10 manuscript."""
import json
import reconstruction_checks as reconstruction
from precision_common import ROOT, save


FUNCTIONS = {
    'static': reconstruction.static,
    'iv': reconstruction.instrument,
    'learning': reconstruction.learning,
    'longitudinal': reconstruction.longitudinal,
    'filtering': reconstruction.filtering,
    'inverse_proxies': reconstruction.inverse_proxies,
    'longer_horizon': reconstruction.longer_horizon,
    'weak_sets': reconstruction.weak_sets,
    'panels_time': reconstruction.panels_time,
    'discovery_observation': reconstruction.discovery_observation,
    'controlled_choice': reconstruction.controlled_choice,
    'policy_transport': reconstruction.policy_transport,
    'adaptive_randomization': reconstruction.adaptive_randomization,
    'sensitivity_controls': reconstruction.sensitivity_controls,
    'continuous_events': reconstruction.continuous_events,
    'recent_methods': reconstruction.recent_methods,
    'software_contracts': reconstruction.software_contracts,
    'product_contracts': reconstruction.product_contracts,
}


def main():
    inherited = json.loads((ROOT/'docs/reconstruction/checks.json').read_text())
    checks = json.loads(json.dumps({key: function() for key, function in FUNCTIONS.items()}))
    if checks != inherited['checks']:
        raise ValueError('Inherited exact witness changed')
    inputs = ['tools/precision_exact_replay.py', 'tools/reconstruction_checks.py',
              'docs/reconstruction/checks.json', 'docs/causal_foundations.tex']
    inputs += [str(path.relative_to(ROOT)) for path in sorted((ROOT/'docs/reconstruction').glob('*.tex'))]
    save('docs/reviews/precision-exact-replay.json', dict(
        status='pass', checks=checks, identical_inherited_exact_results=True,
        scope='Eighteen inherited finite witness families rerun against the V10 manuscript. Historical V9 receipt remains in its archive; finite witnesses do not prove general results.'), inputs)
    print('Eighteen inherited exact witness families replayed unchanged for V10.')


if __name__ == '__main__':
    main()
