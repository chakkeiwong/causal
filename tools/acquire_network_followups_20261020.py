#!/usr/bin/env python3
"""Fixed official follow-ups using the bounded network acquisition helper."""
import acquire_network_commercial_20261020 as collect

collect.BASE = collect.BASE/'followups'
collect.REQUESTS = (
    ('sas151_spatial', 'https://support.sas.com/documentation/onlinedoc/ets/151/spatialreg.pdf', 'pdf'),
    ('sas_latest_spatial', 'https://documentation.sas.com/api/collections/pgmsascdc/v_050/docsets/etsug/content/spatialreg.pdf?locale=en', 'pdf'),
    ('statsig_types', 'https://docs-legacy.statsig.com/statsig-warehouse-native/features/types-of-experiments/', 'html'),
    ('statsig_units', 'https://docs-legacy.statsig.com/metrics/different-id/', 'html'),
    ('optimizely_exclusion', 'https://docs.developers.optimizely.com/full-stack-experimentation/docs/mutually-exclusive-experiments', 'html'),
)

if __name__ == '__main__':
    collect.BASE.mkdir(exist_ok=True)
    plan = collect.BASE/'plan.md'
    if not plan.exists():
        plan.write_bytes((collect.BASE.parent/'plan.md').read_bytes())
    collect.main()
