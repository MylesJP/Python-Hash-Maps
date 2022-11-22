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


    # Quadratic probing can be done without any multiplication apparently
    # Load factor threshold in this one is 0.5 (remember to throw out tombstones on resize)

    def put(self, key: str, value: object) -> None:
        """
        Updates the key:val pair in the Hash Table, inserting a new entry if not
        present. Also resizes the Hash Table when load factor = 1.
        """
        # Resize the HashTable if load >= 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._next_prime(self._capacity*2))
        
        initialIndex = self._hash_function(key) % self._capacity
        hashIndex = initialIndex
        j = 0

        while self._buckets[(hashIndex + j**2) % self.get_capacity()] and \
            self._buckets[(hashIndex + j**2) % self.get_capacity()].key != key:
            j += 1

        # If overwriting, don't increment size
        if self._buckets[(initialIndex + j**2) % self.get_capacity()] and \
            self._buckets[(initialIndex + j**2) % self.get_capacity()].key == key:
            self._buckets[(initialIndex + j**2) % self.get_capacity()] = HashEntry(key, value)
        else:
            self._buckets[(initialIndex + j**2) % self.get_capacity()] = HashEntry(key, value)
            self._size += 1


    def table_load(self) -> float:
        """
        Returns the current Hash Table load.
        """
        return self.get_size() / self.get_capacity()


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the Hash Table.
        """           
        return self.get_capacity() - self.get_size()


    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        if new_capacity == self.get_capacity() or new_capacity < 1:
            return
        
        # If new_capacity isn't prime, adjust up to next prime
        if not self._is_prime(new_capacity):
            prime_capacity = self._next_prime(new_capacity)
        else:
            prime_capacity = new_capacity

        # Copy current entries into a temporary table
        tempArray = DynamicArray()
        for entry in range(self.get_capacity()):
            if self._buckets[entry] and self._buckets[entry].is_tombstone == False:
                tempArray.append(self._buckets[entry])

        self.clear()
        # Increase the size of the Hash Table to prime_capacity
        for _ in range(prime_capacity - self.get_capacity()):
            self._buckets.append(None)

        self._capacity = prime_capacity
        for item in range(tempArray.length()):
            self.put(tempArray[item].key, tempArray[item].value)


    def get(self, key: str) -> object:
        """
        Returns the value for the given key if it is in the Hash Table.
        """
        initialIndex = self._hash_function(key) % self.get_capacity()
        counter = 0
        j = 0
        while counter <= self.get_capacity() and self._buckets[(initialIndex + j**2) % \
            self.get_capacity()] is not None and self._buckets[(initialIndex + j**2) % \
            self.get_capacity()].is_tombstone == False:
            if self._buckets[(initialIndex + j**2) % self.get_capacity()].key == key:
                return self._buckets[(initialIndex + j**2) % self.get_capacity()].value
            j += 1
            # To prevent infinite loops during testing
            counter += 1


    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the Hash Table, else, False.
        """
        # Should only check for is_tombstone
        if self.get(key):
            return True
        return False


    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        initialIndex = self._hash_function(key) % self.get_capacity()
        counter = 0
        j = 0
        while counter <= self.get_capacity() and self._buckets[(initialIndex + j**2) \
            % self.get_capacity()] is not None:
            if self._buckets[(initialIndex + j**2) % self.get_capacity()].key == key:
                self._buckets[(initialIndex + j**2) % self.get_capacity()].is_tombstone = True
                self._size -= 1
                break
            j += 1
            # To prevent infinite loops during testing
            counter += 1


    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        for index in range(self._capacity):
            self._buckets[index] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        pass

    def __iter__(self):
        """
        TODO: Write this implementation
        """
        pass

    def __next__(self):
        """
        TODO: Write this implementation
        """
        # Remember to skip None and __TS__ values
        pass


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(14):
    #     m.put('str' + str(i), i * 100)
    # print(m)
    # m.put("str14", 1400)
    # print(m)
    # m.put("str14", 1500)
    # print(m)

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
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

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())

    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)

    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
