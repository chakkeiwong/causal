#!/usr/bin/env python3
"""Bind two independently authored references for the integrated continuation."""
import json
import honestdid_reference_20261022 as sensitivity
import python_iv_reference_20261022 as iv


def calculate():return dict(sensitivity=sensitivity.calculate(),iv=iv.calculate())


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
