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

## What is Consistent hashing?
