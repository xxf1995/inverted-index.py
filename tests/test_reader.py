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
		pass

	def test_make_runs(self):
		pass
