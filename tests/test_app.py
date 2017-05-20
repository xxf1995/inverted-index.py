import os
import json
import unittest
import inverted_index.app as app


class TestApp(unittest.TestCase):
    """Test app."""

    def test_pipeline(self):
        app.pipeline()
