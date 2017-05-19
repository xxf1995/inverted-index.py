"""Manipulate terms."""
import collections

def alphabetically(terms):
	"""Sort terms alphabetically
	- Args:
	    terms: list of terms
	- Returns:
	    terms: list of terms (sorted)
	"""
	return collections.OrderedDict(sorted(terms.items()))