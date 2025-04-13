# Store the data in a JSON file and update the JSON file
import os
import json

class PersistentKVStore:
    def __init__(self, file_path: str = "kvstore.json"):
        self.file_path = file_path
        self.storage = {}

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.storage = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: could not load data from {self.file_path}")
                self.storage = {}
        

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.storage, f)

    def get(self, key: str):
        return self.storage.get(key)

    def put(self, key: str, value: str):
        self.storage[key] = value
        self._save()
        return True

    def delete(self, key: str):
        if key in self.storage:
            del self.storage[key]
            self._save()
            return True
        return False