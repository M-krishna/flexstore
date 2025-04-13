class SimpleKVStore:
    def __init__(self):
        self.storage = {}

    def get(self, key: str):
        return self.storage.get(key)

    def put(self, key: str, value: str):
        self.storage[key] = value
        return True

    def delete(self, key: str):
        if key in self.storage:
            del self.storage[key]
            return True
        return False