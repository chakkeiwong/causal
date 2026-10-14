"""Reject a changed reader identity/page count without mutating live state."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import master_control as core
import build_gap_successor_v13 as book


class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.report=json.loads((book.OUT/'build-report.json').read_text())
        self.binding=book.ref(book.OUT/'build-report.json','Complete build report')
        self.state=core.read(ROOT,core.STATE)
        self.state['successor_document']=self.binding
        self.state['reader']={'path':self.report['pdf']['path'],'sha256':self.report['pdf']['sha256'],
                              'pages':self.report['pages']}
        self.original_read=core.read

    def read(self,root,name):
        return copy.deepcopy(self.state) if name==core.STATE else self.original_read(root,name)

    def test_valid_book(self):
        with patch.object(core,'read',side_effect=self.read):self.assertEqual(book.check(self.binding)['status'],'pass')

    def test_wrong_current_reader(self):
        self.state['reader']['path']='docs/another.pdf'
        with patch.object(core,'read',side_effect=self.read):
            with self.assertRaisesRegex(ValueError,'Current reader'):book.check(self.binding)

    def test_wrong_current_page_count(self):
        self.state['reader']['pages']+=1
        with patch.object(core,'read',side_effect=self.read):
            with self.assertRaisesRegex(ValueError,'Current reader'):book.check(self.binding)

    def test_wrong_current_reader_hash(self):
        self.state['reader']['sha256']='0'*64
        with patch.object(core,'read',side_effect=self.read):
            with self.assertRaisesRegex(ValueError,'Current reader'):book.check(self.binding)


if __name__=='__main__':unittest.main()
