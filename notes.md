# Implementing features one at a time

* Write a simple key value store (store data in-memory)
* Make the data persistent

## Scratching
Lets take a step back and think in terms of first principles.

**What is our current system doing?**

This of our current system as a single node, where the **json files** are created, updated and deleted for the key-value operations GET, PUT AND DELETE.

What if we make our system distributed? Basically, instead of having only one node, we now have multiple nodes. This is mainly done for fault tolerance.

### How to make our key-value store distributed?
With the current setup we have, we will run multiple instances of the server each representing a node. Each node will have its own file store (JSON file for data persistance). This way we can run multiple node instances.

Okay, now we have the ability to run multiple instances of our server (meaning node). But if we wanna put data to the node, we have to specify which node we want to put the data to.

For example, if we have two nodes (two instances) running on port 5000 and 5001, while putting the data, we have to mention which node the data has to be stored.
> `curl -X PUT -d myvalue1 http://localhost:5000/kv/mykey1`
> `curl -X PUT -d myvalue2 http://localhost:5001/kv/mykey2`
> `curl http://localhost:5000/kv/mykey1` => `{success: true, key: mykey1, value: myvalue1}`
> `curl http://localhost:5001/kv/mykey2` => `{success: true, key: mykey2, value: myvalue2}`

Instead of explicitly mentioning the nodes, the client shouldn't worry about the nodes. All it cares about is storing the data, updating the data, deleting the data.

### How can we solve this?
One thing we can do is maintain the list of all available nodes somewhere. It could be static for now (for every node, we'll hardcode the URL of the node)

When the client tries to put a key value, we will first hash the key and modulo it with the number of nodes and the result we get can be used as a node index.

For example, imagine we have two active nodes.
```
nodes = [
    "http://localhost:5000",
    "http://localhost:50001"
]
```

The client is doing something like: `curl -X PUT -d myvalue1 http://localhost:8001/kv/mykey1`

To acheive something like this, we need to implement the following:
* **Service registry:** Whenever the node starts up it needs to register in the service registry
* **Gateway server:** The client interacts with this server. The gateway server holds the logic for hashing the key and decide which node to forward the request to.

By implementing this, we should be able to acheive the above

**Currently implemented**

1. Gateway server, which is present in `gateway_server.py`
2. Service registry, which is present in `service_registry.py`
3. In `kv_server.py`, the logic was implemented as whenever the node/instance is started, it'll will get registered in the service registry

## What is Consistent hashing?
Consistent hashing is a technique used in distributed systems to distribute data across a dynamic set of nodes (like servers or caches) such that minimal reshuffling of data is required when nodes are added or removed. It's particularly useful in systems like distributed systems like distributed caches, databases, and load balancers.

### Traditional hashing Vs Consistent hashing
In traditional hashing, a key is assigned to a server using a simple modulo operation:
```
server = hash(key) % N, where N = number of servers
```

However when a server is added or removed, `N` changes, causing almost all keys to be remapped, leading to massive cache misses or data movement.

Consistent hashing addresses this issue by mapping both servers and keys onto a circle (or ring) using a hash function. Each key is assigned to the next server in the clockwise direction. When a server is added or removed, only the keys between the server and its predecessor need to move, minimizing the amount of data that needs to be reassigned.

## Currently Implemented
As of now, I have implemented the following:
* Persistent Key Value server, which persists data in a json file and saves in the same server.
* Service registry and discovery.
    * Whenever a new Key Value server is added or removed. It should be updated in the service registry.
* Gateway server. This is the server which the client interacts with. This server talks to the service registry server to get the available nodes and transfers the client request.

## Update Key Value server and Service Registry server with the following
* Key Value Server
    * Expose a `/health-check` endpoint that returns a 200 OK as response. This indicates that the server is up and running properly
    * For debugging, expose a `/destroy` endpoint which kills the server.
* Service Registry
    * Poll the `/health-check` endpoint of the Key Value servers at some interval to check if the nodes are healthy or not.
    * If the nodes are healthy, then fine.
    * If the nodes are unhealthy, then we need to stop forwarding request to the unhealthy server