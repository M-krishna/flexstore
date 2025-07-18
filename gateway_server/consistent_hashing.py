import hashlib


class ConsistentHashing:
    def __init__(self, nodes):
        self.nodes = nodes
        self.hash_ring = {}
        self.sorted_array = []

        self._add_nodes(nodes)
    
    def _hash_key(self, key: str):
        key_str = str(key) # incase if its not a string
        return int(hashlib.md5(key_str.encode()).hexdigest(), 16)