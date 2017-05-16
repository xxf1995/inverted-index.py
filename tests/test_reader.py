import unittest
from inverted_index.io.reader import Reader

class TestReader(unittest.TestCase):
	"""Test reader module."""
	def test_get_docs(self):
		r = Reader()
		# mock dirs
		with mock.patch('Reader.isdir') as mocked_isdir, \
		    mock.patch('Reader.listdir') as mocked_listdir:
		    mocked_isdir.return_value = True
		    mocked_listdir.return_value = ['filename1', 'filename2']
		docs, num_docs = r._get_docs()
		self.assertIsInstance(docs, list)
		self.assertIsInstance(num_docs, int)

	def test_remove_punc(self):
		r = Reader()
		test_str = "Hi, this is a test sentence."
		test_str = r._remove_punc(test_str)
		print test_str
		self.assertEqual(test_str, 'Hi this is a test sentence.')

	def test__read_doc(self):
		pass

	def test_make_runs(self):
		pass