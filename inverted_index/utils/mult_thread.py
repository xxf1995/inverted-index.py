from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool

def mlp(func, run):
    """multithead_processing
    - Args:
        func: function for multithead_processing
        run: list of documents
    - Returns:
        terms: list of terms in all runs
    """
    pool = ThreadPool(cpu_count())
    terms = pool.map(func, run)
    pool.close()
    pool.join()
    return terms