#!/usr/bin/env python3
import sys
import os
import socket
import requests
from threading import Timer
from flask import Flask, request, jsonify
from persistent_kv_store import PersistentKVStore

app = Flask(__name__)
store = PersistentKVStore("server_store.json") # default store


@app.route("/kv/<key>", methods=['GET'])
def get_value(key: str):
    value = store.get(key)
    if not value:
        return jsonify({"success": False, "error": "key not found"}), 404
    return jsonify({"key": key, "value": value}), 200

@app.route("/kv/<key>", methods=['PUT'])
def put_value(key: str):
    value = request.get_data(as_text=True)
    if not value:
        return jsonify({"success": False, "error": "Value should not be None"}), 400
    store.put(key, value)
    return jsonify({"success": True, "key": key}), 201

@app.route("/kv/<key>", methods=['DELETE'])
def delete_key(key: str):
    success = store.delete(key)
    if not success:
        return jsonify({"success": False, "error": f"{key} not found"}), 404
    return jsonify({"success": True, "key": key}), 200

@app.route("/kv/list", methods=['GET'])
def list_keys():
    keys = store.list_keys()
    return jsonify({"success": True, "keys": keys}), 200

@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"success": True}), 200

@app.route("/destroy", methods=['GET'])
def destroy():
    host = socket.gethostname()
    # TODO: fix duplicate
    port = int(os.getenv('PORT', 5000))
    registry_url = os.getenv('REGISTRY_URL', 'http://localhost:8000')
    server_url = f"http://{host}:{port}"

    try:
        # Deregistry from the registry
        requests.delete(f"{registry_url}/deregister", json={"node_url": server_url})

        # Save store state
        store._save()

        # Schedule shutdown
        def shutdown():
            os._exit(0)

        Timer(1.0, shutdown).start()
        return jsonify({"success": True, "message": "Server shut down"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

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

    # Get the configuration from environment variable
    port = int(os.getenv('PORT', 5000))
    store_file = os.getenv('STORE_FILE', 'server_store.json')
    registry_url = os.getenv('REGISTRY_URL', 'http://localhost:8000/register')
    host = socket.gethostname()

    # Initialize the store with the provided file path
    store = PersistentKVStore(store_file)

    # Determine the node's URL
    node_url = f"http://{host}:{port}"
    register_with_service_register(node_url, f"{registry_url}/register")
    app.run(host='0.0.0.0', port=port, debug=True)