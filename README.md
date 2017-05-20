# inverted-index

[![CircleCI](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master.svg?style=shield&circle)](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master)
[![Requirements Status](https://requires.io/github/bwanglzu/inverted-index.py/requirements.svg?branch=master)](https://requires.io/github/bwanglzu/inverted-index.py/requirements/?branch=master)
[![codecov](https://codecov.io/gh/bwanglzu/inverted-index.py/branch/master/graph/badge.svg)](https://codecov.io/gh/bwanglzu/inverted-index.py)

Eanble fast search for information retrieval (text retrieval/text[tag]-based multimedia retrieval).

## Config:

With `.env` under project root.

```python
DIRECTORY=/.../.../...  # Documents to index
HOST=localhost # redis host
PORT=6379 # redis port
POST_DB=1 # redis db
```

## Pipeline:

- Gather all documents under a directory, make runs.
- For each run, read document, extract terms and sort alphabetically.
- Merge runs pair-wisely.
- Aggregate terms into `dictionary` and `postings`.

## Structure

![inverted-index](img/1.png)

## Build:

```python
git clone https://github.com/bwanglzu/inverted-index.py.git
make init # install requirements
make test # run tests
```

## Index

`dictionary` was stored as a json file in `../project/utils/dictionary/`.
`postings` was stored in redis as:

```python
{id: {term, term.freq, doc.name}}
```

## What's next?

Load `dictionary` into memory for fast query and query documents from redis.