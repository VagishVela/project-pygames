""" Implements a basic cache for Views to avoid using too much memory """


class Cache:
    """Implements a basic cache"""

    def __init__(self):
        self._cache = {}

    def get(self, key, val=None):
        """
        Get a cached value or store it if not cached already
        :param key:
        :param val:
        :return:
        """

        item = self._cache.get(key, None)
        if not item:
            self._cache[key] = val
        return self._cache[key]

    def clear(self):
        """Clears the cache"""

        self._cache.clear()
