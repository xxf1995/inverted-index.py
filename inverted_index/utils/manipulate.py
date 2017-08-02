"""Manipulate terms."""
import os
import json
import string
import redis_init
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


def _dict_aggregation(terms):
    """Generate dictionary, term: doc.freq.
    - Args:
    data: list(dict) of aggregated runs.
    """
    dictionary = []
    for idx, term in enumerate(terms):
        count = terms.count(term)
        if count > 0:
            dictionary.append({term: count, 'id': idx})
            terms = filter(lambda a: a != term, terms)

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
