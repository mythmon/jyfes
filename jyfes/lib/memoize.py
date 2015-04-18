from datetime import datetime, timedelta
from functools import wraps


class Expired(Exception):
    pass


class CacheEntry(object):
    def __init__(self, value, expiration):
        self.value = value
        self.expiration = expiration

    def get(self):
        if self.expiration is not None and datetime.now() > self.expiration:
            raise Expired()
        else:
            return self.value


def memoize(timeout=None):
    cache = {}

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                try:
                    return cache[key].get()
                except Expired:
                    del cache[key]

            val = func(*args, **kwargs)
            if val is not None:
                expiration = datetime.now() + timedelta(seconds=timeout)
                cache[key] = CacheEntry(val, expiration)

            return val

        return inner

    return decorator
