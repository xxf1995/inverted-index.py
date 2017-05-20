import os
import json
import unittest
import inverted_index.app as app
from inverted_index.utils.io import IO


class TestApp(unittest.TestCase):
    """Test app."""

    def test_pipeline(self):
    	r = IO()
    	r.dir = os.path.dirname(os.path.realpath(__file__)) + '/test_docs/'
        app.pipeline()
