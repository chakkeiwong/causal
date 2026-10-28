"""Regression checks for false completion and accidental dependency bypass."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from run_followup_program_v3_20261028 import route


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.batch = dict(next=None, next_action=None, continue_work=False, ready=[], active=None)
        self.rows = [dict(id='SOURCE.A', status='inconclusive', lane='software', action='Inspect original A', prerequisites=[]),
                     dict(id='SOURCE.B', status='open', lane='llm', action='Inspect original B', prerequisites=[]),
                     dict(id='RELEASE', status='open', lane='release', action='Accept release', prerequisites=['SOURCE.A pass'])]

    def test_exhausted_packet_retains_work(self):
        r = route(self.batch, self.rows, {})
        self.assertTrue(r['continue_work'])
        self.assertEqual(r['next'], 'SOURCE.A')
        self.assertFalse(r['proposal_complete'])
        self.assertEqual(r['unresolved_obligations'], 3)

    def test_active_packet_wins(self):
        r = route(self.batch | dict(next='ACTIVE', active='ACTIVE', continue_work=True), self.rows, {})
        self.assertEqual(r['next'], 'ACTIVE')
        self.assertEqual(r['next_kind'], 'registered_packet')

    def test_latest_corrected_action_wins(self):
        self.rows[0]['corrected_continuation'] = 'Retain acquired A; inspect remaining delegate'
        self.assertEqual(route(self.batch, self.rows, {})['next_action'], self.rows[0]['corrected_continuation'])

    def test_local_hold_does_not_block_other_work(self):
        holds = {'SOURCE.A': dict(reason='Unavailable original', revisit_trigger='Permitted original', next_action='Obtain original')}
        self.assertEqual(route(self.batch, self.rows, holds)['next'], 'SOURCE.B')

    def test_dependencies_remain_acceptance_conditions(self):
        self.rows[0]['prerequisites'] = ['OTHER pass']
        r = route(self.batch, self.rows, {})
        self.assertEqual(r['acceptance_prerequisites'], ['OTHER pass'])
        self.assertEqual(r['next_kind'], 'successor_preparation')
        self.assertEqual(r['ready'], [])

    def test_only_gates_is_not_completion(self):
        r = route(self.batch, self.rows[2:], {})
        self.assertIsNone(r['next'])
        self.assertTrue(r['unresolved_requires_action'])
        self.assertFalse(r['proposal_complete'])

    def test_passed_work_is_not_reopened(self):
        self.rows[0]['status'] = 'pass'
        self.assertEqual(route(self.batch, self.rows, {})['next'], 'SOURCE.B')

    def test_incomplete_hold_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Incomplete local hold'):
            route(self.batch, self.rows, {'SOURCE.A': {'reason': 'Missing'}})

    def test_declared_preference_is_honoured(self):
        self.assertEqual(route(self.batch, self.rows, {}, 'SOURCE.B')['next'], 'SOURCE.B')


if __name__ == '__main__':
    unittest.main()
