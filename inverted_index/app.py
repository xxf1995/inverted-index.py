import os
import util
from document import Document
from tqdm import tqdm


def pipeline():
    """Build inverted index pipeline."""
    # clear temp folder.
    util.clear_temp()
    # read docs.
    docs = util.get_docs()
    # init connector
    r_p, r_d, r_o = util.redis_init()
    # build
    for f in tqdm(docs):
        doc = Document(f, r_p, r_d)
        doc_terms = doc.terms
        doc.store(doc_terms)
        # store global statis, num of documents
        # and each document length
        r_o.set('num_docs', len(docs))
        r_o.set(doc.name, len(doc_terms))

if __name__ == '__main__':
    pipeline()
