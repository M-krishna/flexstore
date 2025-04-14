![FlexStore](./assets/flexstore.png)
# FlexStore: Distributed Key-Value Store

A distributed key-value store implementation with service discovery and load balancing.

## Architecture
```
               ┌─────────────┐
               │   Service   │
               │  Registry   │
               └─────────────┘
                      ▲
                      │
               ┌─────────────┐
       ┌─────▶│   Gateway    │◀─────┐
       │      └─────────────┘       │
       ▼                            ▼
┌─────────────┐            ┌─────────────┐
│  KV Server  │            │  KV Server  │
│      1      │            │      2      │
└─────────────┘            └─────────────┘
```
There could be n number of KV Servers

## Components

- **Service Registry**: Manages available KV server nodes
- **Gateway Server**: Routes client requests to appropriate KV servers
- **KV Servers**: Store and manage key-value pairs persistently

## Setup

### Prerequisites
- Python 3.9+
- Docker
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flexstore.git
cd flexstore
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running with Docker
Start all services:
```bash
docker-compose up --build
```

## API Endpoints

**Gateway Server (Default port: 8002)**

* `GET /kv/<key>` - Retrieve value for key
* `PUT /kv/<key>` - Store value for key
* `DELETE /kv/<key>` - Delete key-value pair

**Service Registry (Default port: 8000)**

* `GET /nodes` - List all registered nodes
* `POST /register` - Register a new KV server node

### Example usage
1. Store a value:
```bash
curl -X PUT -d "value123" http://localhost:5000/kv/mykey
```

2. Retrieve a value:
```bash
curl http://localhost:5000/kv/mykey
```

3. Delete a value:
```bash
curl -X DELETE http://localhost:5000/kv/mykey
```

## Development
Run individual components:
```bash
# Start Service Registry
python service_registry/service_registry.py

# Start Gateway Server
python gateway_server/gateway_server.py

# Start KV Servers
PORT=8001 python kv_server/kv_server.py
PORT=8002 python kv_server/kv_server.py
```