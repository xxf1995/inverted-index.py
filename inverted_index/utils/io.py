#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import mult_thread
import manipulate


class IO:

    def __init__(self):
        self.dir = os.environ.get('DIRECTORY')
        self.temp = os.path.abspath(
            os.path.join(__file__, os.pardir)
            ) + '/temp/'
        self.run_id = 0

    def json_reader(self, path):
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except (UnicodeDecodeError,ValueError):
                return []

    def json_writer(self, path, content):
        with open(path, 'w') as f:
            try:
                json.dump(content, f)
            except (UnicodeDecodeError,ValueError):
                pass

    def clear_temp(self):
        """clear temp folder"""
        files = [f for f in os.listdir(self.temp)]
        [os.remove(self.temp + f) for f in files]

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

    def _get_docs_with_path(self, path):
        """Get all docs under directory, as docId
        - Args:
            path: document path.
        - Returns:
            docs: list of docs
            num_docs: number of documents
        """
        docs = [path + f for f in os.listdir(path) if os.path.isfile(os.path.join(path,
                f))]
        return (docs, len(docs))

    def _read_manipulate(self, doc_name):
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

    def run_to_temp(self, run):
        """Read documents in a run
        - Args:
            run: a list of document (10 at most)
        - Returns:
            terms: all terms within the current run
        """
        terms = mult_thread.mlp(self._read_manipulate, run)
        terms = manipulate.flatten(terms)
        # merge list of dict, split and sort.
        terms = manipulate.alphabetically(terms)
        # write to temp folder.
        self.json_writer(self.temp + str(self.run_id) + '.json',
            terms)
        self.run_id += 1

    def _merge_run_pairwisely(self, run1_path, run2_path):
        """Merge runs pairwisely, sort alphabetically"""
        terms_run1 = self.json_reader(run1_path)
        terms_run2 = self.json_reader(run2_path)
        terms_merge = manipulate.alphabetically(
            terms_run1 + terms_run2)
        # delete run1 and run 2
        os.remove(run1_path)
        os.remove(run2_path)
        # store merged run
        self.json_writer(self.temp + 'merged.json',
            terms_merge)

    def merge_runs(self):
        """Merge sorted runs into big text
        - Args:
            docs: temp runs (sorted)
        - Returns:
        """
        # change current dir to temp dir
        docs, num_docs = self._get_docs_with_path(self.temp)
        # merge sorted runs pair-wisely
        while num_docs >= 2:
            self._merge_run_pairwisely(docs[0], docs[1])
            docs, num_docs = self._get_docs_with_path(self.temp)
