#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import mult_thread
import manipulate


class IO:

    def __init__(self):
        self.dir = os.environ.get('DIRECTORY')
        self.run_id = 0

    def _json_reader(self, path):
        with open(path) as f:
            return json.load(f)

    def _json_writer(self, path, content):
        with open(path, 'w') as f:
            json.dump(content, f)

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

    def _read_doc(self, doc_name):
        """Read a document, get all terms
        - Args:
            doc_name: str of document name
        - Returns:
            terms: {term1:doc_name, term2:doc_name...}
        """
        with open(doc_name, 'r') as f:
            terms = manipulate.remove_punc(f.read())
            # to lower case, add source (doc.id) as value
            terms = manipulate.lower_dict(terms, doc_name.split('/')[-1])
            return terms

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
        terms = manipulate.flatten(terms)
        temp_path = os.path.abspath(os.path.join(
            __file__,
            os.pardir)) + '/temp/'
        # merge list of dict, split and sort.
        terms = manipulate.alphabetically(terms)
        # write to temp folder.
        self._json_writer(temp_path + str(self.run_id) + '.json',
            terms)
        self.run_id += 1

    def _merge_run_pairwisely(self, run1_path, run2_path):
        """Merge runs pairwisely, sort alphabetically"""
        terms_run1 = self._json_reader(run1_path)
        terms_run2 = self._json_reader(run2_path)
        terms_merge = manipulate.alphabetically(
            terms_run1 + terms_run2)
        # delete run1 and run 2
        os.remove(run1_path)
        os.remove(run2_path)
        # store merged run
        self._json_writer(run1_path,
            terms_merge)

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
