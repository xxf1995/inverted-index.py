import os
import json
import unittest
import inverted_index.app as app
from inverted_index.utils import manipulate


class TestManipulate(unittest.TestCase):
    """Test reader module."""

    def test_remove_punc(self):
        test_str = "Hi, this is a test sentence."
        test_str = manipulate.remove_punc(test_str)
        self.assertEqual(test_str, 'Hi this is a test sentence')
