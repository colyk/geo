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

    def test_cache_adding_should_overwrite_current_data(self):
        c = Cache(prefix="test")

        c.add("test", {"test": "test"})
        c.add("test", {"test1": "test1"})

        self.assertDictEqual(c.get("test"), {"test1": "test1"})

    def test_nonexistent_cache_get_should_not_rise_error(self):
        c = Cache(prefix="test3")
        self.assertIsNone(c.get("test"))

    def test_list_of_caches(self):
        c = Cache(prefix="test")
        c.invalidate_all()
        self.assertEqual(len(c.caches), 0)
        c.add("test", {"test": "test"})
        self.assertEqual(len(c.caches), 1)

    def test_objects_cache(self):
        c = Cache(prefix="test")
        c.invalidate_all()
        obj = {"test": "test"}
        c.add("test", obj, format_="object")
        self.assertDictEqual(c.get("test"), obj)

    def test_cache_invalidation(self):
        c = Cache(prefix="test")
        c.invalidate_all()

        c.add("test", {"test": "test"})
        c.add("test1", {"test": "test"})
        c.add("test2", {"test": "test"})
        self.assertDictEqual(c.get("test"), {"test": "test"})
        self.assertDictEqual(c.get("test1"), {"test": "test"})
        self.assertDictEqual(c.get("test2"), {"test": "test"})

        c.invalidate("test")
        self.assertIsNone(c.get("test"))
        self.assertDictEqual(c.get("test1"), {"test": "test"})
        self.assertDictEqual(c.get("test2"), {"test": "test"})

        c.invalidate_all()
        self.assertIsNone(c.get("test"))
        self.assertIsNone(c.get("test1"))
        self.assertIsNone(c.get("test2"))
