# inverted-index

[![CircleCI](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master.svg?style=shield&circle)](https://circleci.com/gh/bwanglzu/inverted-index.py/tree/master)
[![Requirements Status](https://requires.io/github/bwanglzu/inverted-index.py/requirements.svg?branch=master)](https://requires.io/github/bwanglzu/inverted-index.py/requirements/?branch=master)
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
DBP=1 # redis db to store postings
DBD=2 # redis db to store dictionary
DBO=3 # redis db to store global statistics
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

`dictionary` was stored in redis `DBP` as `{'df': document frequency, 'id': id, 'd': document name}`:

```python
...
{'df': '2', 'id': '85dd927c-844f-40b8-af26-040d16d0fe9b', 'd': 'd2.txt,d3.txt'}
...
```

`postings` was stored in redis with as `{'tf': term frequency, 't': term, 'd': document}`:

```python
# appear in single document
{'tf': '1', 't': 'logical', 'd': 'd2.txt'}
# appear in multiple documents
{'tf': '1,1', 't': 'logical', 'd': 'd2.txt,d3.txt'}
```

`postings` and `dictionary` is connected by `id`, i.e. `id` in `dictionary`. First use term query `dictionary` with term name, use retrieved `id` field get id from `postings`.

Global statistics was also stored, such as `number of documents in collection` and `document length`:

```python
# number of documents in collection
{'num_docs': 100}
# document length
{'d1.txt': 12}
```

## What's next?

1. Connect redis.
2. query by `dictionary` by term.
3. query `postings` by `id`.

```python
import redis
# init redis instance
r_p = redis.Redis(host, port, db_name) # db of postings
r_d = redis.Redis(host, port, db_name) # db of dictionary
r_o = redis.Redis(host, port, db_name) # db of global statistics
# query df -> tf -> number docs and document length
print r_p.hgetall('logical')
>> {'df': '2', 'id': '85dd927c-844f-40b8-af26-040d16d0fe9b', 'd': 'd2.txt,d3.txt'}
print r_d.hgetall(r_p.hgetall('logical')['id'])
>> {'tf': '1,1', 't': 'logical', 'd': 'd2.txt,d3.txt'}
print r_o.get('num_docs')
>> 5
print r_o.get('d3.txt')
>> 9
```

Then plug into ranking model.

A Python implemented ranking function [ranking.py](https://github.com/bwanglzu/ranking.py)