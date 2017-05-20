import redis


def con(host, port, db):
    """Redis connection."""
    return redis.StrictRedis(
        host=host,
        port=port,
        db=db)
