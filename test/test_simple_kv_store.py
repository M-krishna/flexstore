import unittest
from simple_kv_store import SimpleKVStore

class TestSimpleKVStore(unittest.TestCase):

    def test_get_1(self):
        kv = SimpleKVStore()
        kv.put("name", "krishna")

        self.assertEqual(kv.get("name"), "krishna")

    def test_get_2(self):
        kv = SimpleKVStore()
        kv.put("name", "krishna")

        self.assertIsNone(kv.get("age"))

    def test_delete_1(self):
        kv = SimpleKVStore()
        kv.put("name", "krishna")

        self.assertTrue(kv.delete("name"))
        self.assertFalse(kv.delete("age"))


if __name__ == "__main__":
    unittest.main()