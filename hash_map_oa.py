# Name: Myles Penner
# OSU Email: pennermy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: December 2, 2022
# Description: Implementation of an Open Addressing HashMap.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        # Resize the HashTable if load >= 0.5
        if self.table_load() > 0.5:
            self.resize_table(self._next_prime(self._capacity*2))
        
        initialIndex = self._hash_function(key) % self._capacity
        j = 0

        while self._buckets[(initialIndex + j**2) % self.get_capacity()] and \
            self._buckets[(initialIndex + j**2) % self.get_capacity()].key != key and \
            self._buckets[(initialIndex + j**2) % self.get_capacity()].is_tombstone == False:
            j += 1
        # Loop stops with j at the correct increment

        # If overwriting, don't increment size
        if self._buckets[(initialIndex + j**2) % self.get_capacity()] and \
            self._buckets[(initialIndex + j**2) % self.get_capacity()].key == key and \
            self._buckets[(initialIndex + j**2) % self.get_capacity()].is_tombstone == False:
                self._buckets[(initialIndex + j**2) % self.get_capacity()] = HashEntry(key, value)
        else:
            self._buckets[(initialIndex + j**2) % self.get_capacity()] = HashEntry(key, value)
            self._size += 1


    def table_load(self) -> float:
        """
        Returns the current Hash Table load.
        """
        return float(self.get_size() / self.get_capacity())


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the Hash Table.
        """           
        return self.get_capacity() - self.get_size()


    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the Hash Table to the next prime number.
        """
        if new_capacity < self.get_size():
            return
        
        # If new_capacity isn't prime, adjust up to next prime
        if not self._is_prime(new_capacity):
            prime_capacity = self._next_prime(new_capacity)
        else:
            prime_capacity = new_capacity

        # Copy current entries into a temporary table
        tempArray = DynamicArray()
        for entry in range(self.get_capacity()):
            # If the entry exists and is not a tombstone, add it to the tempArray
            if self._buckets[entry] and self._buckets[entry].is_tombstone == False:
                tempArray.append(self._buckets[entry])

        self._buckets = DynamicArray()
        self._size = 0
        # Increase the size of the Hash Table to prime_capacity
        for _ in range(prime_capacity):
            self._buckets.append(None)
        
        self._capacity = prime_capacity

        # Rehash the values from tempArray to self._buckets
        for item in range(tempArray.length()):
            self.put(tempArray[item].key, tempArray[item].value)


    def get(self, key: str) -> object:
        """
        Returns the value for the given key if it is in the Hash Table.
        """
        initialIndex = self._hash_function(key) % self.get_capacity()
        j = 0
        while self._buckets[(initialIndex + j**2) % self.get_capacity()] is not None \
            and self._buckets[(initialIndex + j**2) % self.get_capacity()].is_tombstone == False:
            if self._buckets[(initialIndex + j**2) % self.get_capacity()].key == key:
                return self._buckets[(initialIndex + j**2) % self.get_capacity()].value
            j += 1


    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the Hash Table, else, False.
        """
        if self.get(key):
            return True
        return False


    def remove(self, key: str) -> None:
        """
        Removes a Hash Table entry with the given key from the Hash Table.
        """
        initialIndex = self._hash_function(key) % self.get_capacity()
        j = 0
        while self._buckets[(initialIndex + j**2) % self.get_capacity()] is not None:
            if self._buckets[(initialIndex + j**2) % self.get_capacity()].key == key and \
                self._buckets[(initialIndex + j**2) % self.get_capacity()].is_tombstone == False:
                self._buckets[(initialIndex + j**2) % self.get_capacity()].is_tombstone = True
                self._size -= 1
                break
            j += 1


    def clear(self) -> None:
        """
        Clears the contents of the Hash Table while preserving capacity.
        """
        for index in range(self._capacity):
            self._buckets[index] = None
        self._size = 0


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a Dynamic Array of (key, value) tuples of the Hash Table's
        contents.
        """
        outArray = DynamicArray()
        for element in range(self.get_capacity()):
            if self._buckets[element] and self._buckets[element].is_tombstone == False:
                outArray.append((self._buckets[element].key, self._buckets[element].value))

        return outArray


    def __iter__(self):
        """
        Initialize iterator.
        """
        self._index = 0
        return self


    def __next__(self):
        """
        Obtain next value and advance iterator.
        """
        if not self._buckets[self._index]:
            while not self._buckets[self._index] or self._buckets[self._index].is_tombstone == True:
                self._index += 1
        else:
            self._index += 1

        if self._index == self.get_capacity()-1 or not self._buckets[self._index]:
            raise StopIteration  

        return self._buckets[self._index]

