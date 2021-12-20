
class TableElement:

    def __init__(self, hash_code, key, value, next=None):

        self.hash_code = hash_code
        self.key = key
        self.value = value
        self.next = next