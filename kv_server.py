#!/usr/bin/env python3
import sys
import requests
import argparse
from flask import Flask, request
from persistent_kv_store import PersistentKVStore

app = Flask(__name__)
store = PersistentKVStore("server_store.json") # default store


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


def register_with_service_register(node_url: str, registry_url: str):
    try:
        response = requests.post(
            registry_url,
            json={"node_url": node_url},
            timeout=3
        )
        if response.status_code == 200:
            print(f"Successfully registered node {node_url}")
        else:
            print(f"Failed to register node {node_url}: {response.text}")
    except Exception as e:
        print(f"Exception during registration: {e}")
        sys.exit(1)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a key value server node.")
    parser.add_argument("--port", type=int, default=5000, help="port to run the server on")
    parser.add_argument("--store", type=str, help="JSON file to use for persistence. Example, 'server_store.json'", required=True)
    parser.add_argument("--registry_url", type=str, default="http://localhost:8000/register", help="Registry server URL")
    args = parser.parse_args()

    # Initialize the store with the provided file path
    store = PersistentKVStore(args.store)

    # Determine the node's URL
    node_url = f"http://localhost:{args.port}"
    register_with_service_register(node_url, args.registry_url)
    app.run(host='0.0.0.0', port=args.port, debug=True)