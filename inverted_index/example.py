import os
# -*- coding: utf-8 -*-
import os
import json
import uuid
import redis
from random import randint
from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

# connect strings
host = os.environ.get('HOST')
port = int(os.environ.get('PORT'))
db_postings = os.environ.get('DBP')
db_dictionary = os.environ.get('DBD')
db_documents = os.environ.get('DBO')
# connect
r_p = redis.Redis(host, port, db_postings) # db of postings
r_d = redis.Redis(host, port, db_dictionary) # db of dictionary
r_o = redis.Redis(host, port, db_documents) # db of global statistics

print r_p.hgetall('logical')
print r_d.hgetall(r_p.hgetall('logical')['id'])
print r_o.get('num_docs')
print r_o.get('d3.txt')
