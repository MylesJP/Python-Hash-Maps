# Name: Myles Penner
# OSU Email: pennermy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: December 2, 2022
# Description: Implementation of an Separate Chaining HashMap.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key:val pair in the Hash Table, inserting a new entry if not
        present. Also resizes the Hash Table when load factor = 1.
        """
        # Resize the HashTable if load >= 1
        if self.table_load() >= 1:
            self.resize_table(self._next_prime(self._capacity*2))
        # Insert into the front of the LL returned at the hashIndex bucket
        hashIndex = self._hash_function(key) % self._capacity
        if self._buckets[hashIndex].contains(key):
            # Overwrite old value
            self._buckets[hashIndex].contains(key).value = value
        else:
            # Create new value
            self._buckets[hashIndex].insert(key, value)
            self._size += 1


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the Hash Table.
        """
        count = 0
        # Count of empty buckets
        for index in range(self.get_capacity()):
            if self._buckets[index].length() == 0:
                count += 1
        return count


    def table_load(self) -> float:
        """
        Returns the table load of the Hash Table.
        """
        return self.get_size() / self.get_capacity()


    def clear(self) -> None:
        """
        Clears the contents of the current Hash Table without affecting the 
        capacity.
        """
        for index in range(self._capacity):
            self._buckets[index] = LinkedList()
        self._size = 0


    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the Hash Table to the next prime number.
        """
        # If resize is 0 or the same as current capacity, do nothing
        if new_capacity < 1:
            return

        # If new_capacity isn't prime, adjust up to next prime
        if not self._is_prime(new_capacity):
            prime_capacity = self._next_prime(new_capacity)
        else:
            prime_capacity = new_capacity

        # Store current Hash Table contents in a temporary dynamic array
        tempArray = DynamicArray()
        for element in range(self._buckets.length()):
            if self._buckets[element].length() != 0:
                # If there is something at index, go through the LL
                for node in self._buckets[element]:
                    tempArray.append(node)

        # Clear the existing contents from the Hash Table
        self.clear()

        # Add the appropriate number of buckets to the Hash Table
        self._capacity = prime_capacity
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Rehash the values from tempDynamicArray to self._buckets
        for index in range(tempArray.length()):
            self.put(tempArray[index].key, tempArray[index].value)


    def get(self, key: str):
        """
        Returns the value associated with the parameter key.
        """
        # Returns the value with the given key
        if self._buckets[self._hash_function(key) % self._capacity].contains(key):
            return self._buckets[self._hash_function(key) % self._capacity].contains(key).value


    def contains_key(self, key: str) -> bool:
        """
        Returns True if the HashTable contains key, else, False.
        """
        if self.get(key) is not None:
            return True
        return False


    def remove(self, key: str) -> None:
        """
        Removes an entry with a given key from the Hash Table.
        """
        if self._buckets[self._hash_function(key) % self._capacity].contains(key):
            self._buckets[self._hash_function(key) % self._capacity].remove(key)
            self._size -= 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a Dynamic Array of (key, value) tuples of the Hash Table's
        contents.
        """
        # Return a DA of tuples of key:value pairs
        outArray = DynamicArray()
        
        for element in range(self.get_capacity()):
            if self._buckets[element].length != 0:
                for node in self._buckets[element]:
                    outArray.append((node.key, node.value))

        return outArray


def find_mode(da: DynamicArray):
    """
    Returns a tuple of a Dynamic array with the modal values and their occurance.
    """
    map = HashMap(da.length(), hash_function_1)
    modeArray = DynamicArray()
    maxCount = 1
    for element in range(da.length()):
        count = 1   
        if map.contains_key(da[element]):
            count = map.get(da[element]) + 1
            map.put(da[element], count)
            # Update maxCount if new highest mode
            if map.get(da[element]) >= maxCount:
                maxCount = map.get(da[element])
        else:
            count = 1
            map.put(da[element], count)

    tupleArray = map.get_keys_and_values()
    for item in range(tupleArray.length()):
        if tupleArray[item][1] == maxCount:
            modeArray.append(tupleArray[item][0])

    return (modeArray, maxCount)

