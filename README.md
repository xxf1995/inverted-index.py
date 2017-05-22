# inverted-index

[![CircleCI](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master.svg?style=shield&circle)](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master)
[![Requirements Status](https://requires.io/github/bwanglzu/inverted-index.py/requirements.svg?branch=master)](https://requires.io/github/bwanglzu/inverted-index.py/requirements/?branch=master)
[![codecov](https://codecov.io/gh/bwanglzu/inverted-index.py/branch/master/graph/badge.svg)](https://codecov.io/gh/bwanglzu/inverted-index.py)
[![Language](https://img.shields.io/badge/language-python-brightgreen.svg)](https://www.python.org/)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/bwanglzu/inverted-index.py/blob/master/LICENSE)

Eanble fast search for information retrieval (text retrieval/text[tag]-based multimedia retrieval).
A side small project for thesis.

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
`postings` was stored in redis as `[sorted set](http://jadianes.me/intro-redis-python)` as `('postings', score, {term, term.freq, doc.name})`, for example:

```python
('postings', 1, {'a', 1, '1.txt'})
('postings', 2, {'a', 3, '2.txt'})
('postings', 3, {'b', 1, '1.txt'})
```

They are **ordered**.

## What's next?

1. Load `dictionary` into memory for fast query and query documents from redis.
2. Get `term`, `doc.freq` and it's `position` from memory.
3. Retrieve `term.freq`, `doc.id` from redis with:

```python
r.zrange('postings', from, to)
# from is the start position, to is the end position, e.g.
r.zrange('postings', positing, positing + doc.freq) is the current term's postings
```

Then plug into ranking model.