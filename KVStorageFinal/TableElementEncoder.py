
from json import JSONEncoder


class TableElementEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
