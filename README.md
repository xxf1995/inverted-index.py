# inverted-index

[![CircleCI](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master.svg?style=shield&circle)](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master)
[![Requirements Status](https://requires.io/github/bwanglzu/inverted-index.py/requirements.svg?branch=master)](https://requires.io/github/bwanglzu/inverted-index.py/requirements/?branch=master)
[![codecov](https://codecov.io/gh/bwanglzu/inverted-index.py/branch/master/graph/badge.svg)](https://codecov.io/gh/bwanglzu/inverted-index.py)

Eanble fast search for information retrieval (text retrieval/text[tag]-based multimedia retrieval).

## WORKING

## Pipeline:

- Gather all documents under a directory, make runs.
- For each run, read document, extract terms and sort alphabetically.
- Merge runs pair-wisely.
- Aggregate terms into `dictionary` and `postings`.

## Structure

![inverted-index](img/1.png)