#!/usr/bin/env python3
"""Combined exact panel references; no third-party runtime execution."""
import pyfixest_contract_reference_20261023 as pyfixest
import synthdid_contract_reference_20261023 as sdid
def calculate(): return dict(pyfixest=pyfixest.calculate(),synthdid=sdid.calculate())
