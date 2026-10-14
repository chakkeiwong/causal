#!/usr/bin/env python3
"""Replay inherited exact witnesses against the current manuscript; keep old receipt."""
import json
import reconstruction_checks as r
from closure_common import ROOT,save

def main():
    functions={'static':r.static,'iv':r.instrument,'learning':r.learning,'longitudinal':r.longitudinal,
        'filtering':r.filtering,'inverse_proxies':r.inverse_proxies,'longer_horizon':r.longer_horizon,'weak_sets':r.weak_sets,
        'panels_time':r.panels_time,'discovery_observation':r.discovery_observation,'controlled_choice':r.controlled_choice,
        'policy_transport':r.policy_transport,'adaptive_randomization':r.adaptive_randomization,'sensitivity_controls':r.sensitivity_controls,
        'continuous_events':r.continuous_events,'recent_methods':r.recent_methods,'software_contracts':r.software_contracts,'product_contracts':r.product_contracts}
    old=json.loads((ROOT/'docs/reconstruction/checks.json').read_text());checks={k:fn() for k,fn in functions.items()}
    # Normalize tuples/fractions via the inherited output's ordinary JSON rules.
    checks=json.loads(json.dumps(checks));equal=checks==old['checks'];assert equal,'Inherited exact result changed'
    inputs=['tools/calibration_exact_replay.py','tools/reconstruction_checks.py','docs/reconstruction/checks.json','docs/causal_foundations.tex']+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'docs/reconstruction').glob('*.tex'))]
    save('docs/reviews/calibration-exact-replay.json',dict(status='pass',date='2026-10-10',checks=checks,identical_inherited_exact_results=equal,
         scope='Reexecuted inherited finite witnesses with current manuscript inputs; old assessed receipt retained unchanged. Does not prove new general theorems.'),inputs)
    print('Eighteen inherited exact witness families replayed unchanged; new receipt saved.')

if __name__=='__main__':main()
