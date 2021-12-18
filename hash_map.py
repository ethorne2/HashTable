# Name: Elizabeth Thorne
# OSU Email: thorneel@oregonstate.edu
# Course: CS261 - Data Structures Section 401
# Assignment: Assignment 7, HashMap
# Due Date: 12/03/2021
# Description: Implementation of a HashMap with the following methods: empty_buckets, table_load, clear, put,
# contains_key, get, remove, resize_table, and get_keys


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Parameters: None
        Returns: None
        Clears the contents of the hash map. Does not change the underlying hash table capacity.
        """
        # go through the buckets, if the bucket is not empty, set's them to an empty LinkedList
        for index in range(self.capacity):
            self.buckets[index] = LinkedList()
        self.size = 0

    def get(self, key: str) -> object:
        """
        Parameters: a key (string)
        Returns: If the key is found, returns the value associated with the given key.
        Else, returns None.
        """
        hash = self.hash_function(key) # compute element's bucket using hash function
        bucket_index = hash % self.capacity
        bucket = self.buckets[bucket_index]  # a LinkedList
        if bucket.contains(key) is not None:
            node = bucket.contains(key)
            return node.value

        return None

    def put(self, key: str, value: object) -> None:
        """
        Parameters: a key (string) and value (object)
        Returns: None
        Updates the key/value pair in the hashmap.
        If given key already exists in the hashmap, associated value must be replaced with new value
        If given key is not in hash map, key/value pair is added
        """
        hash_val = self.hash_function(key)  # compute element's bucket using hash function
        bucket_index = hash_val % self.capacity
        bucket = self.buckets[bucket_index]  # a LinkedList
        node = bucket.head  # assign node variable as the bucket's head
        key_exists = False

        while node is not None:
            if node.key == key:  # if the key already exists, value must be replaced with new value
                node.value = value
                key_exists = True
            node = node.next

        if key_exists is False:
            bucket.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Parameters: a key (string)
        Returns: None
        Removes the given key and its associated value from the hash map.
        If given key is not in the hash map, method does nothing (no exception raised).
        """
        hash_val = self.hash_function(key)  # compute element's bucket using hash function
        bucket_index = hash_val % self.capacity
        bucket = self.buckets[bucket_index]  # a LinkedList

        node_removed = bucket.remove(key)
        if node_removed is True:
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Parameters: a key (string)
        Returns: a boolean expression, True if given key is in the hash map, otherwise False.
        An empty hash map does not contain any keys
        """
        hash_val = self.hash_function(key)  # compute element's bucket using hash function
        bucket_index = hash_val % self.capacity
        if bucket_index < self.capacity:  # if the index is within the Dynamic array
            bucket = self.buckets[bucket_index]
            if bucket.contains(key) is not None:
                return True
        return False

    def empty_buckets(self) -> int:
        """
        Parameters: None
        Returns: the number (integer) of empty buckets in the hash table.
        """
        empty_buckets = 0  # initialize empty buckets to 0

        for index in range(self.capacity):
            bucket = self.buckets[index]
            if bucket.length() == 0:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """
        Parameters: None
        Returns: the current hash table load factor (float)
        """
        load_factor = 0.0  # initialize load factor as 0.0
        number_buckets = self.capacity  # initialize number of buckets as self.capacity
        number_elements = 0  # initialize number of elements stored in table as zero

        for index in range(self.capacity):  # for each bucket, add up the length to number_elements
            bucket = self.buckets[index]
            number_elements += bucket.length()

        load_factor += (number_elements / number_buckets)  # use += so result of 0.0 + value is a float

        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        Parameters: new_capacity (integer)
        Returns: None
        Changes the capacity of the internal hash table
        All existing key/value pairs must remain in the new hash map and all hash table links rehashed
        If new_capacity less than 1, method does nothing.
        """
        if new_capacity < 1:
            return

        new_hashmap = HashMap(new_capacity, self.hash_function)  # create a new Hashmap
        for index in range(self.capacity):  # iterate through each bucket in original hash table
            bucket = self.buckets[index]  # a LinkedList
            for node in bucket:
                new_hashmap.put(node.key, node.value)  # use put method to insert into new_hashmap

        # assign the buckets and capacity to the new_hashmap's buckets and capacity
        self.buckets = new_hashmap.buckets
        self.size = new_hashmap.size
        self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        Parameters: None
        Returns: a Dynamic Array
        Returns a Dynamic Array that contains all keys stored in the hash map.
        Order of keys in the Dynamic Array does not matter
        """
        keys_da = DynamicArray()
        for index in range(self.capacity):  # iterate through each bucket in original hash table
            bucket = self.buckets[index]  # a LinkedList
            for node in bucket:
                keys_da.append(node.key)  # use append method to add the node's key to the keys da

        return keys_da


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
