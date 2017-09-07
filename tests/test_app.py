import os
import json
import unittest
from mock import patch
import inverted_index.app as app
import inverted_index.util as util


class TestApp(unittest.TestCase):
    """Test app."""
    
    @patch.object(util, 'get_docs')
    def test_pipeline(self, mock_getdocs):
    	path = os.path.dirname(os.path.realpath(__file__)) + '/test_docs/'
    	docs = [path + f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
    	mock_getdocs.return_value = docs, len(docs)
        app.pipeline()
        assert docs[0].split('/')[-1].split('.')[0] == 'd1'
        assert len(docs) == 3
