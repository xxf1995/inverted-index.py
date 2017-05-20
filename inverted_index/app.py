import os
from utils.io import IO
import utils.redis_init as redis_init
import utils.manipulate as manipulate

def pipeline():
	"""Build inverted index pipeline."""
	# read docs.
	io = IO()
	docs, num_docs = io._get_docs()
	# make runs.
	runs = io._make_runs(docs, num_docs)
	[io.run_to_temp(run) for run in runs]
	io.merge_runs()
	# merged runs will be the only doc in temp.
	path = os.path.dirname(
		os.path.realpath(__file__)
		) + '/utils/temp/merged.json'
	# load run
	data = io._read_doc(path)
	# build inverted index
	_build_inverted_index(data)


def _build_inverted_index(data):
	"""Build inverted index.
	"""
	r_p = redis_init.con(
		os.environ.get('HOST'),
		os.environ.get('PORT'),
		os.environ.get('POST_DB'))
	# flush db before create new index.
	# remove dictionary.json
	dict_path =  os.path.abspath(
		os.path.join(__file__,os.pardir)
		) + '/dictionary/'
	if os.path.isfile(dict_path):
	    os.remove(dict_path)
	r_p.flushdb()
	# get all terms.
	terms = [item['t'] for item in data]
	manipulate._dict_aggregation(terms)
	manipulate._post_aggregation(r_p, data)

if __name__ == '__main__':
	pipeline()