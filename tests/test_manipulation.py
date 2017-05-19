import os
import json
import unittest
from inverted_index.utils import manipulate


class TestManipulate(unittest.TestCase):
    """Test reader module."""

    def test_remove_punc(self):
        test_str = "Hi, this is a test sentence."
        test_str = manipulate.remove_punc(test_str)
        self.assertEqual(test_str, 'Hi this is a test sentence')

    def test_dict_aggregation(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/test_json/test.json' 
        with open(path) as f:
            data = json.load(f)
            manipulate._dict_aggregation(data)
            haha



