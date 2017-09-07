# -*- coding: utf-8 -*-
import os
import json
import uuid
import redis
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

temp_dir = os.path.abspath(
        os.path.join(
            __file__,
            os.pardir)) + '/temp/'

def clear_temp():
    """clear temp folder"""
    files = [f for f in os.listdir(temp_dir)]
    [os.remove(temp_dir + f) for f in files]


def get_docs():
    """Get all docs under directory, as docId
    - Args:
    - Returns:
        docs: list of docs
    """
    file_dir = os.environ.get('DIRECTORY')
    docs = [file_dir + f for f in os.listdir(file_dir) if os.path.isfile(os.path.join(file_dir,
            f))]
    return docs

def make_runs(docs):
    """Make runs for memory saving
    - Args:
        docs: name of docs
        num_docs: number of documents
    - Returns:
        runs: list of list of docs
              e.g. [[doc1, doc2], [doc3, doc4]]
    """
    threshold = 200
    num_runs = len(docs) / threshold + 1
    runs = []
    for run in xrange(0, num_runs):
        # get current run of docs.
        current_run = docs[:threshold - 1]
        # remove current run from docs.
        docs = docs[threshold:]
        # append to runs.
        runs.append(current_run)
    return runs

def json_writer(content):
    with open(''.join([temp_dir, 'dictionary.json']), 'w') as f:
        try:
            json.dump(content, f)
        except (UnicodeDecodeError,ValueError):
            pass


def redis_init():
    host = os.environ.get('HOST')
    port = int(os.environ.get('PORT'))
    db_postings = os.environ.get('DBP')
    db_dictionary = os.environ.get('DBD')
    db_documents = os.environ.get('DBO')
    r_p = redis.StrictRedis(host, port, db_postings)
    r_d = redis.StrictRedis(host, port, db_dictionary)
    r_o = redis.StrictRedis(host, port, db_documents)
    r_p.flushall()
    r_d.flushall()
    r_o.flushall()
    return r_p, r_d, r_o