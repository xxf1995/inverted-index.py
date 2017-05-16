import os
import unittest
from inverted_index.io.reader import Reader


class TestReader(unittest.TestCase):
    """Test reader module."""

    def test_get_docs(self):
        r = Reader()
        r.dir = os.path.dirname(os.path.realpath(__file__)) + '/test_docs/'
        docs, num_docs = r._get_docs()
        self.assertIsInstance(docs, list)
        self.assertIsInstance(num_docs, int)

    def test_remove_punc(self):
        r = Reader()
        test_str = "Hi, this is a test sentence."
        test_str = r._remove_punc(test_str)
        self.assertEqual(test_str, 'Hi this is a test sentence')

    def test_read_doc(self):
        r = Reader()
        r.dir = os.path.dirname(os.path.realpath(__file__)) + '/test_docs/'
        file_path = r.dir + '1.txt'
        self.assertIsInstance(r._read_doc(file_path), list)

    def test_make_runs(self):
        r = Reader()
        r.dir = os.path.dirname(os.path.realpath(__file__)) + '/test_docs/'
        docs, num_docs = r._get_docs()
        runs = r._make_runs(docs, num_docs)
        self.assertIsInstance(runs, list)
