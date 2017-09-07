"""Query all document w.r.t current term."""
import os
import pymongo

class Collection(object):
	def __init__(self, conn, terms):
		self.conn = conn
		self.terms = terms
    
	def create_index(self):
		"""Create index for term field."""
		self.conn.create_index([('t', pymongo.TEXT)], name='term_index', default_language='english')

	def aggregate(self, terms):
		"""Map term to term:[doc1, doc2, doc....], count df."""
		df = self.conn.find({'t': term}, {'_id': 0, 'tf': 0, 't': 0}).distinct("d")
		return term, len(df)

	@property
	def terms(self):
		"""get unique terms"""
		return list(set(self.terms))
		

