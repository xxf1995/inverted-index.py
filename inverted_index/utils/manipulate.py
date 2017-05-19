"""Manipulate terms."""

def alphabetically(terms):
	"""Sort terms alphabetically
	- Args:
	    terms: list of terms
	- Returns:
	    terms: list of terms (sorted)
	"""
	return sorted(terms, key=str.lower)