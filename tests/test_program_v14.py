"""Behavioral tests for independent execution, safe rollups and preserved evidence."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import causal_program_v14 as control
import master_control as core


class SchedulingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = core.read(ROOT, control.BASE + '/work-graph.json')
        cls.candidate = core.read(ROOT, control.BASE + '/candidate-state.json')

    def setUp(self):
        self.state = copy.deepcopy(self.candidate)

    def done(self, identifier, outcome='pass', capabilities=None):
        self.state['execution_program']['results'][identifier] = {'outcome': outcome, 'capabilities': capabilities or []}

    def ready(self, identifier):
        return not control.blockers(self.state, control.operation(self.graph, identifier))

    def test_all_nine_lanes_receive_work_before_any_lane_repeats(self):
        lanes = []
        for unused in self.graph['lanes']:
            item = control.ordered_ready(self.state, self.graph)[0]
            lanes.append(item['lane'])
            self.done(item['id'])
            self.state['execution_program']['turns'].append({'operation': item['id'], 'lane': item['lane'], 'action': 'record'})
        self.assertEqual(set(lanes), set(self.graph['lanes']))
        self.assertEqual(len(set(lanes)), len(lanes))

    def test_blocked_head_does_not_stop_other_work(self):
        first = control.ordered_ready(self.state, self.graph)[0]
        self.state['execution_program']['blocks'][first['id']] = {'reason': 'Original unavailable'}
        following = control.ordered_ready(self.state, self.graph)
        self.assertTrue(following)
        self.assertNotIn(first['id'], [x['id'] for x in following])

    def test_partial_progress_rotates_lanes_without_awarding_completion(self):
        first = control.ordered_ready(self.state, self.graph)[0]
        self.state['execution_program']['turns'].append({'operation': first['id'], 'lane': first['lane'], 'action': 'progress'})
        following = control.ordered_ready(self.state, self.graph)[0]
        self.assertNotEqual(first['lane'], following['lane'])
        self.assertNotIn(first['id'], self.state['execution_program']['results'])

    def test_python_adapter_does_not_wait_for_other_languages_or_whole_survey(self):
        self.done('IN.DESIGN.Python')
        self.done('SW.DECISION.seed_071', capabilities=['integration_allowed'])
        self.assertNotIn('SW01', self.state['results'])
        self.assertNotIn('SW07', self.state['results'])
        self.assertTrue(self.ready('IN.ADAPTER.Python'))
        self.assertFalse(self.ready('IN.ADAPTER.Java'))

    def test_completed_rejection_does_not_enable_adapter(self):
        self.done('IN.DESIGN.Python')
        self.done('SW.DECISION.seed_071')  # Completed decision, but no permitted reuse.
        self.assertFalse(self.ready('IN.ADAPTER.Python'))

    def test_negative_license_review_cannot_enable_adapter(self):
        self.done('IN.DESIGN.Python')
        self.done('SW.DECISION.seed_071', outcome='negative')
        self.assertFalse(self.ready('IN.ADAPTER.Python'))

    def test_commercial_cell_failure_does_not_block_noncommercial_area_review(self):
        node = control.operation(self.graph, 'SW.REVIEW.identification_counterfactual')
        for dep in node['depends']:
            self.done(dep['id'])
        self.done('SW.CELL.identification_counterfactual.commercial', outcome='inconclusive')
        self.assertTrue(self.ready(node['id']))

    def test_chapters_are_ready_without_software_or_adapter_rollups(self):
        self.assertTrue(self.ready('TEXT.DRAFT.S2'))
        self.assertTrue(self.ready('TEXT.DRAFT.L4'))
        self.assertTrue(self.ready('TEXT.DRAFT.I3'))

    def test_local_workflow_can_be_prepared_before_every_adapter(self):
        self.assertTrue(self.ready('IN.JOURNEY.DESIGN.funding'))
        self.done('IN.JOURNEY.DESIGN.funding')
        node = control.operation(self.graph, 'IN.JOURNEY.LOCAL.funding')
        self.assertEqual(control.blockers(self.state, node), ['requires prospective operation registration'])

    def test_live_inputs_block_live_execution_only(self):
        self.assertTrue(self.ready('LL.LIVE.DESIGN'))
        self.assertTrue(self.ready('LL.TASK.longitudinal_policy'))
        self.done('LL.LIVE.DESIGN')
        blockers = control.blockers(self.state, control.operation(self.graph, 'LL.LIVE.RUN'))
        self.assertEqual(sum('missing authentic input' in x for x in blockers), 5)

    def test_scoped_external_review_does_not_wait_for_i02(self):
        self.assertNotIn('I02', self.state['results'])
        self.state['input_receipts']['independent_review'] = {'test_only': True}
        self.assertTrue(self.ready('EXT.SCOPED.REVIEW'))
        self.assertTrue(core.unmet(self.state, core.task_by_id(self.state, 'X01')))

    def test_research_argument_ready_while_successor_study_is_blocked(self):
        self.assertTrue(self.ready('SCI.ARGUMENT.R02S'))
        self.assertFalse(self.ready('SCI.STUDY.R02S'))

    def test_ready_operations_do_not_award_parent_or_gap(self):
        before = copy.deepcopy(self.state['results'])
        self.done('IN.DESIGN.Python')
        overview = control.overview(self.state, self.graph)
        self.assertEqual(before, self.state['results'])
        self.assertEqual(overview['qualified_original_gaps'], [])
        self.assertTrue(overview['continue'])

    def test_package_source_gates_remain_stricter_than_a_draft(self):
        self.done('SW.COMP.discovery_iid')
        unmet = control.dependency_blockers(self.state['execution_program'], self.graph['package_gates']['SW02'])
        self.assertTrue(unmet)

    def test_all_contractual_scopes_are_present(self):
        control.validate_graph(self.state, self.graph)

    def test_dependency_cycle_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph['nodes'][0]['depends'].append({'id': graph['nodes'][0]['id'], 'outcomes': ['pass']})
        with self.assertRaisesRegex(ValueError, 'cycle'):
            control.validate_graph(self.state, graph)

    def test_phase_gate_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph['nodes'][0]['requires_phase'] = 3
        with self.assertRaisesRegex(ValueError, 'Phases'):
            control.validate_graph(self.state, graph)

    def test_missing_cell_cannot_be_hidden_by_an_equal_count_replacement(self):
        graph = copy.deepcopy(self.graph)
        graph['nodes'][0]['id'] = 'SW.CELL.imagined.Python'
        with self.assertRaises(ValueError):
            control.validate_graph(self.state, graph)


class PreservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate = core.read(ROOT, control.BASE + '/candidate-state.json')

    def test_complete_candidate_passes_preservation_and_current_validation(self):
        self.assertEqual(control.validate_state(ROOT, copy.deepcopy(self.candidate)), [])

    def test_original_negative_research_cannot_be_relabeled_pass(self):
        state = copy.deepcopy(self.candidate)
        state['results']['R02']['outcome'] = 'pass'
        self.assertTrue(control.validate_state(ROOT, state))

    def test_final_investment_dependency_cannot_be_removed(self):
        state = copy.deepcopy(self.candidate)
        core.task_by_id(state, 'F01')['depends'] = []
        self.assertTrue(control.validate_state(ROOT, state))

    def test_page_or_source_criteria_cannot_be_dropped(self):
        state = copy.deepcopy(self.candidate)
        core.task_by_id(state, 'LA07')['criteria'] = []
        self.assertTrue(control.validate_state(ROOT, state))

    def test_old_book_identity_cannot_be_replaced(self):
        state = copy.deepcopy(self.candidate)
        state['reader']['sha256'] = '0' * 64
        self.assertTrue(control.validate_state(ROOT, state))

    def test_changed_graph_bytes_are_rejected(self):
        state = copy.deepcopy(self.candidate)
        state['execution_program']['documents']['graph']['sha256'] = '0' * 64
        self.assertTrue(control.validate_state(ROOT, state))


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='causal-v14-test-')
        self.root = Path(self.temp.name)
        (self.root / 'finding.txt').write_text('Observed evidence for a bounded test only.\n')
        self.evidence = {'path': 'finding.txt', 'sha256': core.sha(self.root / 'finding.txt'), 'anchor': 'Complete test evidence'}
        self.node = {'id': 'TEST.OP', 'depends': [], 'requires_inputs': [], 'study': False,
                     'criteria': ['Require actual evidence.'], 'outputs': ['finding.txt'], 'capabilities': ['integration_allowed']}
        self.state = {'execution_program': {'results': {}, 'registrations': {}, 'blocks': {}, 'turns': []}, 'input_receipts': {}}
        self.receipt = control.receipt_template(self.node)
        self.receipt.update(outcome='pass', execution='performed', scope='Test scope', reviewer={'name': 'Test author', 'kind': 'author'},
                            outputs=[self.evidence], criteria=[{'index': 0, 'verdict': 'pass', 'finding': 'Observed', 'evidence': [self.evidence]}])

    def tearDown(self):
        self.temp.cleanup()

    def validate(self):
        control.validate_operation_receipt(self.root, self.state, self.node, self.receipt, 2)

    def test_scoped_evidence_can_be_recorded_without_parent_outcome(self):
        self.validate()

    def test_evidence_tampering_is_rejected(self):
        (self.root / 'finding.txt').write_text('Changed after review')
        with self.assertRaisesRegex(ValueError, 'changed evidence'):
            self.validate()

    def test_operation_cannot_qualify_original_gap(self):
        self.receipt['original_gap_qualification'] = True
        with self.assertRaisesRegex(ValueError, 'cannot award'):
            self.validate()

    def test_rejected_or_unavailable_path_can_be_dispositioned_without_execution(self):
        self.node['depends'] = [{'id': 'ABSENT.LICENSE', 'outcomes': ['pass']}]
        self.receipt.update(operation_contract_sha256=core.digest_object(self.node), outcome='inconclusive', execution='not_performed',
                            nonexecution_reason='Required original license not available', revisit_trigger='Original license received and reviewed')
        self.receipt['criteria'][0]['verdict'] = 'inconclusive'
        self.validate()

    def test_unavailable_disposition_cannot_grant_reuse_capability(self):
        self.receipt.update(outcome='inconclusive', execution='not_performed', capabilities=['integration_allowed'])
        with self.assertRaisesRegex(ValueError, 'Only an executed'):
            self.validate()

    def test_study_cannot_be_run_without_prospective_registration(self):
        self.node['study'] = True
        self.receipt['operation_contract_sha256'] = core.digest_object(self.node)
        with self.assertRaisesRegex(ValueError, 'prospective'):
            self.validate()

    def test_passing_receipt_cannot_hide_an_unmet_criterion(self):
        self.receipt['criteria'][0]['verdict'] = 'inconclusive'
        with self.assertRaisesRegex(ValueError, 'unresolved criterion'):
            self.validate()


class WorkingDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='causal-v14-book-test-')
        self.root = Path(self.temp.name)
        source = ROOT / 'docs/program/master-program-v14.pdf'
        (self.root / 'book.pdf').write_bytes(source.read_bytes())
        self.pages = core.read(ROOT, control.BASE + '/program-pdf/build-report.json')['pages']
        (self.root / 'source.tex').write_text('Test artifact for manifest validation, not a scientific source.\n')
        self.manifest = {'kind': 'working_monograph', 'final_acceptance': False,
                         'pdf': self.binding('book.pdf'), 'pages': self.pages,
                         'source_artifacts': [self.binding('source.tex')]}
        for name, data in [('build_report', {'pdf': self.manifest['pdf'], 'pages': self.pages}),
                           ('text_layout', {'status': 'pass', 'pages': self.pages}),
                           ('source_review', {'status': 'pass', 'issues': [], 'evidence': [self.binding('source.tex')]})]:
            core.write(self.root / (name + '.json'), data)
            self.manifest[name] = self.binding(name + '.json')

    def binding(self, path):
        return {'path': path, 'sha256': core.sha(self.root / path), 'anchor': 'Bound test artifact'}

    def tearDown(self):
        self.temp.cleanup()

    def validate(self):
        core.write(self.root / 'manifest.json', self.manifest)
        return control.validate_working_release(self.root, self.binding('manifest.json'))

    def test_actual_working_pdf_can_be_admitted_without_final_acceptance(self):
        self.assertFalse(self.validate()['final_acceptance'])

    def test_working_delivery_cannot_award_i02(self):
        self.manifest['final_acceptance'] = True
        with self.assertRaisesRegex(ValueError, 'cannot award'):
            self.validate()

    def test_changed_source_artifact_invalidates_working_delivery(self):
        (self.root / 'source.tex').write_text('Changed source')
        with self.assertRaisesRegex(ValueError, 'changed evidence'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
