"""Publication must not rewrite past evidence or misbind the current release."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import causal_program_v13_1 as control


class RefreshTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposed = json.loads((ROOT/control.BASE/'proposed-state.json').read_text())

    def setUp(self):
        self.state = copy.deepcopy(self.proposed)

    def rejected(self):
        self.assertTrue(control.validate_state(ROOT, self.state))

    def test_reviewed_candidate_passes(self):
        self.assertEqual(control.validate_state(ROOT, self.state), [])

    def test_cannot_rewrite_v13_feasibility_receipt(self):
        self.state['results']['RG1']['sha256'] = '0'*64
        self.rejected()

    def test_cannot_remove_successor_gate(self):
        final = next(t for t in self.state['work_packages'] if t['id'] == 'F01')
        final['depends'] = [d for d in final['depends'] if d['id'] != 'R03S']
        self.rejected()

    def test_cannot_drop_v13_book(self):
        self.state['deliveries'] = [d for d in self.state['deliveries'] if d['path'] != 'docs/causal_integrated_working_v13_2026-10-12.pdf']
        self.rejected()

    def test_cannot_point_reader_to_a_different_pdf(self):
        self.state['reader']['path'] = 'docs/causal_integrated_working_v13_2026-10-12.pdf'
        self.rejected()

    def test_cannot_misstate_reader_page_count(self):
        self.state['reader']['pages'] += 1
        self.rejected()

    def test_cannot_silently_replace_execution_queue(self):
        self.state['execution_refresh']['documents']['queue']['sha256'] = '0'*64
        self.rejected()


if __name__ == '__main__':
    unittest.main()
