import unittest
import os

from src.cache import Cache


class CacheTest(unittest.TestCase):
    CACHE_FILE = "cache_test.pkl"

    def setUp(self):
        self.cache = Cache(self.CACHE_FILE)
        return super().setUp()

    def test_pass(self):
        key, val = "key", "val"
        self.cache.cache[key] = val

        self.cache._save_cache()
        self.cache.cache = {}

        self.cache._load_cache()
        self.assertIn(key, self.cache.cache)
        self.assertEqual(val, self.cache.cache[key])

    def tearDown(self):
        if os.path.isfile(self.CACHE_FILE):
            os.remove(self.CACHE_FILE)
        return super().tearDown()
