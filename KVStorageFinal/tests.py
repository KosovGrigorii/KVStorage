import unittest
from storageCleaner import empty_storage
import random
from HashTable import HashTable
import hashlib
import string
import json


class MyTestCase(unittest.TestCase):
    def test_same_key(self):
        table = HashTable('output.txt')
        same_key = 'same'
        first_file = 'buckets.txt'
        second_file = 'values.txt'
        with open(first_file) as b:
            first_item = b.read()
        table.put(same_key, first_file)
        with open(second_file) as v:
            second_item = v.read()
        table.put(same_key, second_file)
        final_item = table.get(same_key)
        self.assertNotEqual(first_item, final_item)
        self.assertEqual(second_item, final_item)
        empty_storage()
        

    def test_change_capacity(self):
        table = HashTable('output.txt')
        key = 'key'
        file = 'buckets.txt'
        first_capacity = table.capacity
        for i in range(table.capacity + 1):
            table.put(key, file)
            key += '_key'
        second_capacity = table.capacity
        self.assertTrue(first_capacity < second_capacity)
        empty_storage()

    def test_work_with_collision(self):
        table = HashTable('output.txt')
        capacity = table.capacity
        first_key = 'key'
        h = hashlib.sha1(first_key.encode())
        first_hash = int(h.hexdigest(), 16)
        first_modulo = first_hash % capacity
        while True:
            second_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            h = hashlib.sha1(second_key.encode())
            second_hash = int(h.hexdigest(), 16)
            second_modulo = second_hash % capacity
            if second_modulo == first_modulo:
                break
        table.put(first_key, 'buckets.txt')
        table.put(second_key, 'values.txt')
        with open('values.txt') as entries_file:
            entries_file = json.load(entries_file)
        self.assertIsNotNone(entries_file[0]["next"])
        self.assertIsNotNone(entries_file[entries_file[0]["next"]])
        empty_storage()

    def test_not_existent_key(self):
        table = HashTable('output.txt')
        with self.assertRaises(Exception):
            table.get('not_existent_key')
        empty_storage()


if __name__ == '__main__':
    unittest.main()
