# inverted-index

[![CircleCI](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master.svg?style=shield&circle)](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master)
[![Requirements Status](https://requires.io/github/bwanglzu/inverted-index.py/requirements.svg?branch=master)](https://requires.io/github/bwanglzu/inverted-index.py/requirements/?branch=master)
[![codecov](https://codecov.io/gh/bwanglzu/inverted-index.py/branch/master/graph/badge.svg)](https://codecov.io/gh/bwanglzu/inverted-index.py)
[![Language](https://img.shields.io/badge/language-python-brightgreen.svg)](https://www.python.org/)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/bwanglzu/inverted-index.py/blob/master/LICENSE)

Eanble fast search for information retrieval (text retrieval/text[tag]-based multimedia retrieval).

A side project for my master thesis.

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

![inverted-index](img/inverted_index.png)

## Build:

```python
git clone https://github.com/bwanglzu/inverted-index.py.git
make init # install requirements
make test # run tests
```

## Run

```python
python app.py
```

## Index

`dictionary` was stored as a json file in `../project/utils/dictionary/` as: `[{"term": {"document frequency": number, "term id": number}}]`, e.g.:

```python
[
    {"a": {"df": 1, "id": 0}},
    ....
]
```

`postings` was stored in redis with [SortedSet](http://jadianes.me/intro-redis-python) as `('postings', term id, {term, term.freq, doc.name})`, for example:

```python
[
    (postings, 1, "{'tf': 1, 't': 'a', 'd': '1.txt'}"),
    ...
]
```

`postings` and `dictionary` is connected by term_id, i.e. `id` in `postings`.

## What's next?

1. Load `dictionary` into memory for fast query and query documents from redis.
2. Get term to be queried from memory.
3. Retrieve `term.freq`, `doc.id` from `postings` in redis with:

```python
import redis
# init redis instance
# configuration same as .env
r = redis.StrictRedis(
        host=localhost,
        port=6379,
        db=1)
# query the first term, (suppose first term is a and id is 0, df is 1)
# with z.zrangebyscore('postings', id, id + df - 1)
r.zrangebyscore('postings', 0, 0)
# another example, term `b`, id is 1, df is 3
r.zrangebyscore('postings', 1, 1 + 3 - 1)
```

Then plug into ranking model.

A Python implemented ranking function [ranking.py](https://github.com/bwanglzu/ranking.py)