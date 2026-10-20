#!/usr/bin/env python3
"""One fixed primary specification linked by the acquired Statsig original."""
import acquire_network_commercial_20261020 as collect

collect.BASE = collect.BASE/'switchback'
collect.REQUESTS = (('statsig_switchback', 'https://docs-legacy.statsig.com/experiments-plus/switchback-tests', 'html'),)

if __name__ == '__main__':
    collect.BASE.mkdir(exist_ok=True)
    plan=collect.BASE/'plan.md'
    if not plan.exists():
        plan.write_bytes((collect.BASE.parent/'plan.md').read_bytes())
    collect.main()
