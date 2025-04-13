from flask import Flask, request
from persistent_kv_store import PersistentKVStore

app = Flask(__name__)
store = PersistentKVStore("server_store.json")


@app.route("/kv/<key>", methods=['GET'])
def get_value(key: str):
    value = store.get(key)
    if not value:
        return "key not found", 404
    return f"key: {key}, value: {value}"

@app.route("/kv/<key>", methods=['PUT'])
def put_value(key: str):
    value = request.get_data(as_text=True)
    if not value:
        return "value should be None", 400
    store.put(key, value)
    return f"status: success, key: {key}"

@app.route("/kv/<key>", methods=['DELETE'])
def delete_key(key: str):
    success = store.delete(key)
    if not success:
        return f"key: {key} not found"
    return f"success: true, key: {key}"

@app.route("/kv/list", methods=['GET'])
def list_keys():
    keys = store.list_keys()
    return f"success: true, keys: {keys}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)