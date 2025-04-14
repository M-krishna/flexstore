import unittest
import os
import json
from kv_server.persistent_kv_store import PersistentKVStore

# This test is written by AI
class TestPersistentKVStore(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_kvstore.json"
        self.store = PersistentKVStore(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_init(self):
        self.assertEqual(self.store.file_path, self.test_file)
        self.assertEqual(self.store.storage, {})

    def test_put_and_persistence(self):
        self.store.put("key1", "value1")
        
        # Check if file exists and contains correct data
        with open(self.test_file, 'r') as f:
            stored_data = json.load(f)
        self.assertEqual(stored_data["key1"], "value1")
        
        # Create new instance to verify loading
        new_store = PersistentKVStore(self.test_file)
        new_store._load()
        self.assertEqual(new_store.get("key1"), "value1")

    def test_get(self):
        self.store.put("key1", "value1")
        self.assertEqual(self.store.get("key1"), "value1")
        self.assertIsNone(self.store.get("nonexistent"))

    def test_delete(self):
        self.store.put("key1", "value1")
        
        self.assertTrue(self.store.delete("key1"))
        self.assertFalse(self.store.delete("nonexistent"))
        self.assertIsNone(self.store.get("key1"))

    def test_load_invalid_json(self):
        # Create invalid JSON file
        with open(self.test_file, 'w') as f:
            f.write("invalid json")
        
        store = PersistentKVStore(self.test_file)
        store._load()
        self.assertEqual(store.storage, {})

if __name__ == '__main__':
    unittest.main()