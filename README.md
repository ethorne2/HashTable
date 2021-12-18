# HashTable

Implementation of a Hash Table data structure in Python with the following characteristics:
* A Dynamic Array to hold the hash map
* Each bucket of the Dynamic Array is an empty Linked List
* Collisions are resolved via adding a node to the Linked List within each bucket
* Initializes the Hashmap with a specific capacity and hash function
* Each key/value is help in a Node within the Linked List for each bucket

The Hash Table has the following methods available to use:
* clear()
* get()
* put()
* remove()
* contains_key()
* empty_buckets()
* table_load()
* resize_table()
* get_keys()
