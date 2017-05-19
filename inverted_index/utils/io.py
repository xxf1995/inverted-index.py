#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
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
            terms: terms within document as list
        """
        with open(doc_name, 'r') as f:
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
        # sort.
        terms = manipulate.alphabetically(terms)
        # write to temp folder.
        with open(temp_path + str(self.run_id) + '.txt',
            'w') as f:
            f.write("\n".join(terms))
        self.run_id += 1

    def _merge_run_pairwisely(self, run1_path, run2_path):
        """Merge runs pairwisely, sort alphabetically"""
        terms_run1, terms_run2 = []
        with open(run1_path, 'r') as f:
            terms_run1 = f.readlines()
        with open(run2_path, 'r') as f:
            terms_run2 = f.readlins()
        terms_merge = manipulate.alphabetically(
            terms_run1 + terms_run2)
        # delete run1 and run 2
        os.remove(run1_path)
        os.remove(run2_path)
        # store merged run
        with open(run1_path, 'w') as f:
            f.write("\n".join(terms))

    def merge_runs(self, docs):
        """Merge sorted runs into big text
        - Args:
            docs: temp runs (sorted)
        - Returns:
        """
        # change current dir to temp dir
        self.dir = os.path.abspath(os.path.join(
            __file__,
            os.pardir)) + '/temp/'
        # merge sorted runs pair-wisely
        while len(self._get_docs()) > 2:
            runs = self._get_docs()
            self._merge_run_pairwisely(runs[0], runs[1])
