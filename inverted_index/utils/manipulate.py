"""Manipulate terms."""
import string
import redis_init
from itertools import chain
from operator import itemgetter

def remove_punc(content):
    """Remove punctuation from given text."""
    return content.translate(None, string.punctuation)

def lower_dict(terms, value):
	"""List of terms to lower case make dictionary."""
	return [{'t': term.lower(), 'd': value} for term in terms.split()]

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
        data: dict of aggregated runs.
	- Returns:
	"""
	r = redis_init.con(
		os.environ.get('HOST'),
		os.environ.get('PORT'),
		os.environ.get('DICT_DB'))
	terms = [item['t'] for item in data]
	for term in terms:
		r.set(term, terms.count(term))
		terms.remove(term)

