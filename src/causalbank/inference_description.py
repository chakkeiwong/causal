"""Public scientific meaning carried unchanged through monetary consumers."""
from copy import deepcopy


def funding_inference(method, alpha=.05, scope=None):
    if method not in ('regular_delta', 'weak_linkage_projection'):
        raise ValueError('unknown funding inference method')
    regular = method == 'regular_delta'
    return {
        'schema_version': 1,
        'method': method,
        'confidence_level': 1 - alpha,
        'coverage_claim': 'asymptotic conditional on the declared response and audit law',
        'audit_coverage': 'delta approximation' if regular else 'exact binomial marginal regions with prespecified error allocation',
        'sampling_unit': 'common calendar origin; separate independent representative map audits',
        'identification_conditions': [
            'conditional structural price innovation', 'noninformative within-stratum pair swaps',
            'independent invariant training pilot', 'stable calendar and consistent response covariance',
            'truthful representative independent audits',
        ] + (['mapping ranks bounded away from zero in the limiting experiment'] if regular else []),
        'numerical_status': 'computed; uncertainty qualification is separate',
        'empirical_qualification': (
            'research_only_adverse_calibration' if regular else 'conservative_in_tested_designs_precision_limited'),
        'evidence': {
            'path': 'docs/studies/linkage-projection-results.json',
            'regular_strong_coverage': .925,
            'regular_strong_mc95': [.8947, .9488],
            'nominal': .95,
            'projection_coverage': '2000/2000 retained draws; all weak/singular sets were whole line',
            'interpretation': 'synthetic evidence, not a finite-sample coverage guarantee or bank validation',
        },
        'scope': scope,
    }


def public_inference(result):
    """Upgrade a legacy result transparently; never infer a favorable method."""
    if 'inference' in result:
        return deepcopy(result['inference'])
    method = 'weak_linkage_projection' if result['status'] == 'computed_set' else 'regular_delta'
    description = funding_inference(method, 1 - result.get('confidence_level', .95), result.get('scope'))
    description['legacy_result_upgrade'] = True
    if result.get('status') not in ('computed', 'computed_set'):
        description['numerical_status'] = 'unavailable'
    return description
