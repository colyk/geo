from django.test import TestCase

from .cache import Cache


class CacheCase(TestCase):
    def test_cache_prefixes(self):
        c_test = Cache(prefix="test")
        c_test1 = Cache(prefix="test1")

        c_test.add("test", {"test": "test"})
        c_test1.add("test", {"test1": "test1"})

        self.assertDictEqual(c_test.get("test"), {"test": "test"})
        self.assertDictEqual(c_test1.get("test"), {"test1": "test1"})

    def test_cache_add_should_overwrite_current_data(self):
        c = Cache(prefix="test")

        c.add("test", {"test": "test"})
        c.add("test", {"test1": "test1"})

        self.assertDictEqual(c.get("test"), {"test1": "test1"})

    def test_nonexistent_cache_get_should_not_rise_error(self):
        c = Cache(prefix="test3")
        self.assertIsNone(c.get("test"))

    def test_cache_remove(self):
        c = Cache(prefix="test4")

        c.add("test", {"test": "test"})
        self.assertDictEqual(c.get("test"), {"test": "test"})

        c.remove("test")
        self.assertIsNone(c.get("test"))
