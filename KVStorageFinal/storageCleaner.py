import json


def empty_storage():
    with open('buckets.txt', 'w') as file_handle:
        json.dump([-1, -1, -1, -1], file_handle)

    with open('values.txt', 'w') as file_entries:
        json.dump([None, None, None, None], file_entries)

    with open('output.txt', 'w') as file_buckets:
        json.dump(["buckets.txt", "values.txt", 4], file_buckets)
