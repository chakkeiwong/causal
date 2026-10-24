#!/usr/bin/env python3
"""Replay only project-authored exact references, never upstream software."""
import review_d3rlpy_reuse_20261015 as d3
import scope_rl_reference_20261023 as scope
import obp_reference_20261023 as obp
import pomdp_py_reference_20261023 as pomdp

def calculate():
    return {'d3rlpy':d3.exact(),'scope_rl':scope.calculate(),
            'obp':obp.calculate(),'pomdp_py':pomdp.calculate()}

if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
