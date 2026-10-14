#!/usr/bin/env python3
"""Apply the preserved archival replay runner to the V7 closure evidence."""
import replay_archived_verifier_20261013 as replay

replay.CASES['closure'] = ('v7', 'closure_verify', 'closure-verification')

if __name__ == '__main__':
    raise SystemExit(replay.main())
