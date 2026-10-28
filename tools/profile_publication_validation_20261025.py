#!/usr/bin/env python3
"""Profile a captured state without changing canonical evidence or controls."""
import cProfile,json,pstats,time
from pathlib import Path
import run_program_checkpoint_v3 as controller
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/validation-profile-v1'
assert not BASE.exists();BASE.mkdir()
state=controller.base.core.read(ROOT,controller.base.core.STATE)
profile=cProfile.Profile();start=time.monotonic();profile.enable()
issues=controller.base.validate_state(ROOT,state)
profile.disable();elapsed=time.monotonic()-start
profile.dump_stats(str(BASE/'profile.pstats'))
with (BASE/'profile-top.txt').open('x') as out:
    pstats.Stats(profile,stream=out).sort_stats('cumulative').print_stats(25)
report=dict(scope='Read-only validation of captured state;canonical publication may advance independently.',elapsed_seconds=elapsed,issues=issues,reader=state['reader'],state_updated=state['updated'],mutation=False)
(BASE/'profile-review.json').write_text(json.dumps(report,indent=2)+chr(10))
print(json.dumps(dict(elapsed_seconds=elapsed,issues=issues)))
