#!/usr/bin/env python3
# This server acts as the gateway layer and client

import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
REGISTRY_URL = os.getenv('REGISTRY_URL', 'http://localhost:8000')

def fetch_nodes():
    try:
        response = requests.get(f"{REGISTRY_URL}/nodes", timeout=3)
        data = response.json()
        return data.get('nodes', [])
    except Exception as e:
        print(f"Error while fetching nodes: {e}")
        return []


def get_node_for_key(key: str, nodes: list):
    node_index = hash(key) % len(nodes)
    return nodes[node_index]

@app.route("/kv/<key>", methods=['GET'])
def gateway_get(key: str):
    nodes = fetch_nodes()
    if not nodes:
        return jsonify({"success": False, "error": "No available nodes"}), 503
    selected_node = get_node_for_key(key, nodes)
    try:
        response = requests.get(f"{selected_node}/kv/{key}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": f"Error contacting the node: {e}"}), 500

@app.route("/kv/<key>", methods=['PUT'])
def gateway_put(key: str):
    nodes = fetch_nodes()
    if not nodes:
        return jsonify({"success": False, "error": "No available nodes"}), 503
    selected_node = get_node_for_key(key, nodes)
    value = request.get_data(as_text=True)
    try:
        response = requests.put(f"{selected_node}/kv/{key}", data=value)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": f"Error contacting the node: {e}"}), 500

@app.route("/kv/<key>", methods=['DELETE'])
def gateway_delete(key: str):
    nodes = fetch_nodes()
    if not nodes:
        return jsonify({"success": False, "error": "No available nodes"}), 503
    selected_node = get_node_for_key(key, nodes)
    try:
        response = requests.delete(f"{selected_node}/kv/{key}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": f"Error contacting the node: {e}"}), 500


if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    app.run(host=host, port=os.environ['PORT'], debug=True)