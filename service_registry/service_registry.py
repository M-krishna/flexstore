#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
nodes = set() # A simple set to store unique URLs


@app.route("/register", methods=['POST'])
def register_nodes():
    # This function will receive the node URL in the request data
    data = request.get_json()
    if data and 'node_url' in data:
        nodes.add(data['node_url'])
        return f"success: true, node: {data['node_url']}", 200
    return f"success: false, error: 'node_url' missing", 400

@app.route("/nodes", methods=["GET"])
def get_nodes():
    return jsonify({"nodes": list(nodes)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ['PORT'])


