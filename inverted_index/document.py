"""Document class, read document, clean document, get terms."""
import uuid
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter


class Document(object):

    def __init__(self, path, r_d, r_p):
        print path
        self.path = path
        self._name = path.split('/')[-1]
        self._term = None
        # init redis instance for postings and dictionary
        self.r_d = r_d
        self.r_p = r_p

    def read(self):
        """Get terms within documents."""
        try:
            with open(self.path, 'r') as f:
                self._term = f.read()
                return self
        except EnvironmentError:
            raise IOError("File not found")

    def lower(self):
        """Terms to lower case."""
        self._term = self._term.lower()
        return self

    def del_punc(self):
        """Remove punc."""
        self._term = self._term.translate(
        	None,
        	string.punctuation
        	)
        return self

    def del_space_stop(self):
        """Remove spaces, stopwords."""
        cached = stopwords.words("english")
        self._term = [word for word in self._term.split() if word not in cached]
        return self

    @property
    def terms(self):
        """Finish process"""
        self.read().lower().del_punc().del_space_stop()
        return self._term

    @property 
    def name(self):
        """doc name"""
        return self._name

    def store(self, terms):
    	"""Store in db."""
        terms = Counter(terms).most_common()
        for t, tf in terms:
            idx = str(uuid.uuid4())
            node_dict = self.r_d.hgetall(t)
            if node_dict and node_dict['d'] != self._name:
                self.r_d.hmset(t,
                    {'id': idx, 'df': int(node_dict['df']) + 1,
                     'd': ','.join([self.r_p.hget(node_dict['id'], 'd'), self._name])})
                self.r_p.hmset(idx,
                    {
                    't': t,
                    'd':  ','.join([self.r_p.hget(node_dict['id'], 'd') , self._name]),
                    'tf': ','.join([self.r_p.hget(node_dict['id'], 'tf'), str(tf)])})
            else:
                self.r_d.hmset(t,
                    {'id': idx, 'df': 1, 'd': self._name})
                self.r_p.hmset(idx,
                    {
                    't': t,
                    'd': self._name,
                    'tf': tf
                    })
                


