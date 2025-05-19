#!/usr/bin/env python3
import os
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
CORS(app)
nodes = set() # A simple set to store unique URLs

HEALTH_CHECK_TIME_INTERVAL = 5.0 # seconds

# Health check polling service
def health_check_poll():
    while True:
        unhealthy_nodes = set()
        for node in nodes:
            try:
                response = requests.get(f"{node}/health-check", timeout=3)
                if response.status_code != 200:
                    print(f"Node {node} unhealthy: bad status code: {response.status_code}", flush=True)
                    unhealthy_nodes.add(node)
            except Exception as e:
                print(f"Node {node} unhealthy: {str(e)}", flush=True)
                unhealthy_nodes.add(node)
        
        for node in unhealthy_nodes:
            nodes.remove(node)
            print(f"Deregistered unhealthy node: {node}")
        
        time.sleep(HEALTH_CHECK_TIME_INTERVAL)

health_check_thread = Thread(target=health_check_poll, daemon=True)
health_check_thread.start()

@app.route("/register", methods=['POST'])
def register_nodes():
    # This function will receive the node URL in the request data
    data = request.get_json()
    if data and 'node_url' in data:
        nodes.add(data['node_url'])
        return f"success: true, node: {data['node_url']}", 200
    return f"success: false, error: 'node_url' missing", 400

@app.route("/deregister", methods=['DELETE'])
def deregister_nodes():
    # This function will receive the node URL in the request data
    # This endpoint must not be exposed to the gateway server
    data = request.get_json()
    if data and 'node_url' in data:
        nodes.remove(data['node_url'])
        return jsonify({"success": True, "message": f"Deregistered {data['node_url']} successfully"}), 200
    return jsonify({"success": False, "error": f"{data['node_url']} not found in service registry"}), 404

@app.route("/nodes", methods=["GET"])
def get_nodes():
    return jsonify({"nodes": list(nodes)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ['PORT'])


