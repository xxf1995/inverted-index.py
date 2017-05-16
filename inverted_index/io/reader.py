#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import string
from os import listdir
from os.path import isfile, join


class Reader:

    def __init__(self):
        self.dir = os.environ.get('DIRECTORY')

    def _get_docs(self):
        """Get all docs under directory, as docId
            - Args:
            - Returns:
                docs: list of docs
               num_docs: number of documents
        """
        docs = [f for f in listdir(self.dir) if isfile(join(self.dir,
                f))]
        return (docs, len(docs))

    def _remove_punc(self, content):
        """Remove punctuation from given text"""

        return content.translate(None, string.punctuation)

    def _read_doc(self, doc_path):
        """Read a document, get all terms
        - Args:
            doc_path: str of document path
        - Returns:
            terms: terms within document as list
        """

        with open(doc_path, 'r') as f:
            terms = self._remove_punc(f.read())
            return terms.split()

    def _make_runs(self, docs, num_docs):
        """Make runs for memory saving
        - Args:
            docs: name of docs
            num_docs: number of documents
        - Returns:
            runs: list of list of docs
                  e.g. [[doc1, doc2], [doc3, doc4]]
        """
        num_runs = num_docs / 10 + 1
        runs = []
        for run in xrange(0, num_runs):
            # get current run of docs.
            current_run = docs[:10]
            # remove current run from docs.
            docs = docs[10:]
            # append to runs.
            runs.append(current_run)
        return runs



