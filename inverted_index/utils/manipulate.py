"""Manipulate terms."""
import os
import json
import string
import redis_init
import pandas as pd
from itertools import chain
from operator import itemgetter


def remove_punc(content):
    """Remove punctuation from given text."""
    return content.translate(None, string.punctuation)


def lower_dict(terms, value):
    """List of terms to lower case make dictionary."""
    terms = terms.split()
    return [{'t': term.lower(), 'd': value, 'tf': terms.count(term)} for term in terms]


def flatten(terms):
    """list to np array."""
    return list(chain.from_iterable(terms))


def alphabetically(terms):
    """Sort terms alphabetically.
    - Args:
        terms: list of dict of terms
    - Returns:
        terms: list of terms (sorted)
    """
    return sorted(terms, key=itemgetter('t'))


def _dict_aggregation(data):
    """Generate dictionary, term: doc.freq.
    - Args:
    data: list(dict) of aggregated runs.
    """
    dictionary = []
    terms = [item['t'] for item in data]
    data = pd.DataFrame(data)
    processed_terms = []
    for idx, term in enumerate(terms):
        if term in processed_terms:
            continue
        sub = data[data.t == term]
        document_frequency = len(sub.d.unique())
        processed_terms.append(term)
        dictionary.append({term:document_frequency, 'id': idx})

    return dictionary


def _post_aggregation(r, data):
    """Generate postings, term: term.freq doc.name.
    - Args:
        con: redis connection instance.
        terms: list(dict) of aggregated runs
    """
    for idx, item in enumerate(data):
        r.zadd('postings',
            idx,
            item)
