#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import string
import mult_thread
import manipulate


class IO:

    def __init__(self):
        self.dir = os.environ.get('DIRECTORY')
        self.run_id = 0

    def _get_docs(self):
        """Get all docs under directory, as docId
        - Args:
        - Returns:
            docs: list of docs
            num_docs: number of documents
        """
        docs = [self.dir + f for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir,
                f))]
        return (docs, len(docs))

    def _remove_punc(self, content):
        """Remove punctuation from given text"""
        return content.translate(None, string.punctuation)

    def _read_doc(self, doc_name):
        """Read a document, get all terms
        - Args:
            doc_name: str of document name
        - Returns:
            terms: {term1:doc_name, term2:doc_name...}
        """
        with open(doc_name, 'r') as f:
            terms = self._remove_punc(f.read())
            terms = [term.lower() for term in terms.split()]
            return dict.fromkeys(terms, doc_name.split('/')[-1])

    def _make_runs(self, docs, num_docs):
        """Make runs for memory saving
        - Args:
            docs: name of docs
            num_docs: number of documents
        - Returns:
            runs: list of list of docs
                  e.g. [[doc1, doc2], [doc3, doc4]]
        """
        num_runs = num_docs / 5 + 1
        runs = []
        for run in xrange(0, num_runs):
            # get current run of docs.
            current_run = docs[:5]
            # remove current run from docs.
            docs = docs[5:]
            # append to runs.
            runs.append(current_run)
        return runs

    def _run_to_temp(self, run):
        """Read documents in a run
        - Args:
            run: a list of document (10 at most)
        - Returns:
            terms: all terms within the current run
        """
        terms = mult_thread.mlp(self._read_doc, run)
        temp_path = os.path.abspath(os.path.join(
            __file__,
            os.pardir)) + '/temp/'
        # merge list of dict, split and sort.
        terms = { k: v for d in terms for k, v in d.items()}
        terms = manipulate.alphabetically(terms)
        # write to temp folder.
        with open(temp_path + str(self.run_id) + '.json', 'w') as f:
            json.dump(terms, f)
        self.run_id += 1

    def _merge_run_pairwisely(self, run1_path, run2_path):
        """Merge runs pairwisely, sort alphabetically"""
        terms_run1 = []
        terms_run2 = []
        with open(run1_path) as f1:
            terms_run1 = json.load(f1)
        with open(run2_path) as f2:
            terms_run2 = json.load(f2)
        terms_merge = manipulate.alphabetically(
            dict(terms_run1.items() + terms_run2.items()))
        # delete run1 and run 2
        os.remove(run1_path)
        os.remove(run2_path)
        # store merged run
        with open(run1_path, 'w') as f:
            json.dump(terms_merge, f)

    def merge_runs(self):
        """Merge sorted runs into big text
        - Args:
            docs: temp runs (sorted)
        - Returns:
        """
        # change current dir to temp dir
        self.dir = os.path.abspath(os.path.join(
            __file__,
            os.pardir)) + '/temp/'
        docs, num_docs = self._get_docs()
        # merge sorted runs pair-wisely
        while num_docs >= 2:
            self._merge_run_pairwisely(docs[0], docs[1])
            docs, num_docs = self._get_docs()
