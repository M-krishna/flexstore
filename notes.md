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



## What is Consistent hashing?
