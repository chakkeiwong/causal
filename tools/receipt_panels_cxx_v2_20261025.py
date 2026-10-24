#!/usr/bin/env python3
"""Record the preserving short-panel-corrected review, not its predecessor."""
import review_panels_cxx_20261025 as prior
prior.BASE=prior.BASE.parent/'panels-cxx-v2'
if __name__=='__main__':prior.receipt()
