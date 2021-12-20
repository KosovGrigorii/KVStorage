
import json

from TableElement import TableElement
from TableElementEncoder import TableElementEncoder


class HashTable:
    def __init__(self, filename):

        with open(filename, 'r') as data_file:
            data = json.load(data_file)
            self.capacity = data[2]

        self.buckets = [-1 for i in range(self.capacity)]
        self.entries = [None for i in range(self.capacity)]
        self.filename = filename
        self.element_encoder = TableElementEncoder()

    def get_hash(self, key):
        fin_hash = 0
        for char in key:
            fin_hash += ord(char)
        return fin_hash

    def find_empty_entry(self):
        with open(self.filename, 'r') as data_file:
            data = json.load(data_file)
            with open(data[1], 'r') as entries_file:
                entries = json.load(entries_file)
                for index, element in enumerate(entries):
                    if element is None:
                        return index

        return None
        # self.expand_storages()
        # return self.find_empty_entry()

    def put(self, key, value):

        index = self.find_empty_entry()
        if index is None:
            self.expand_storages()
            index = self.capacity//2

        entries_position = index

        key_hash = self.get_hash(key)
        bucket_position = key_hash % self.capacity

        with open(self.filename, 'r') as data_file:
            data = json.load(data_file)
            with open(data[0], 'r+') as bucket_file:
                buckets = json.load(bucket_file)
                if buckets[bucket_position] != -1:
                    entries_position = buckets[bucket_position]
                else:
                    buckets[bucket_position] = index

            with open(data[1], 'r+') as entries_file:

                entries = json.load(entries_file)
                if buckets[bucket_position] != index:

                    while True:
                        if entries[entries_position]['key'] == key:
                            entries[entries_position]['value'] = value
                            break

                        elif entries[entries_position]['next'] is not None:
                            entries_position = entries[entries_position]['next']
                            continue

                        else:
                            entries[entries_position]['next'] = index
                            entries[index] = self.element_encoder.default(TableElement(key_hash, key, value))
                            break

                else:
                    entries[entries_position] = self.element_encoder.default(TableElement(key_hash, key, value))

            with open(data[0], 'w') as bucket_file:
                json.dump(buckets, bucket_file)

            with open(data[1], 'w') as entries_file:
                json.dump(entries, entries_file)

    def get(self, key):
        key_hash = self.get_hash(key)
        bucket_position = key_hash % self.capacity
        entries_position = -1

        with open(self.filename, 'r') as data_file:
            data = json.load(data_file)
            with open(data[0], 'r') as bucket_file:
                buckets = json.load(bucket_file)

                if buckets[bucket_position] == -1:
                    raise Exception(f"key {key} is not found")
                else:
                    entries_position = buckets[bucket_position]

            with open(data[1], 'r') as entries_file:
                entries = json.load(entries_file)
                while True:

                    if entries[entries_position]["key"] == key:
                        with open(entries[entries_position]["value"], 'r') as value_file:
                            value = value_file.read()
                            print(value)
                        break

                    elif entries[entries_position]["next"] is not None:
                        entries_position = entries[entries_position]["next"]
                        continue

                    else:
                        raise Exception(f"key {key} is not found")

    def expand_storages(self):
        new_buckets = [-1] * (self.capacity * 2)
        new_entries = [None] * (self.capacity * 2)

        with open(self.filename, 'r+') as data_file:
            data = json.load(data_file)
            with open(data[0], 'r') as bucket_file:
                buckets = json.load(bucket_file)

            with open(data[1], 'r') as entries_file:
                entries = json.load(entries_file)

                for i in range(0, len(entries)):
                    key_hash = entries[i]["hash_code"]

                    if new_buckets[key_hash % (self.capacity * 2)] == -1:
                        new_buckets[key_hash % (self.capacity * 2)] = i
                        entries[i]['next'] = None
                        new_entries[i] = entries[i]

                    else:
                        entries_position = new_buckets[key_hash % (self.capacity * 2)]
                        while True:
                            if new_entries[entries_position]['next'] is not None:
                                entries_position = new_entries[entries_position]['next']
                                continue

                            else:
                                new_entries[entries_position]['next'] = i
                                entries[i]['next'] = None
                                new_entries[i] = entries[i]
                                break

            with open(data[0], 'w') as bucket_file:
                json.dump(new_buckets, bucket_file)

            with open(data[1], 'w') as entries_file:
                json.dump(new_entries, entries_file)

        with open(self.filename, 'w') as data_file:
            json.dump(["buckets.txt", "values.txt", self.capacity * 2], data_file)

        self.capacity = self.capacity * 2

    def check_valid_key(self, key, db):

        if not isinstance(key, str):
            raise ValueError('%r is not a valid key type' % key)
        if key not in db:
            raise ValueError('%r could not be found' % key)