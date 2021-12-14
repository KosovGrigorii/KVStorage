import pickle

from contextlib import closing

from sqlitedict import SqliteDict


def put(key, value):

    filename = get_db_filename(key)
    with closing(SqliteDict(filename, autocommit=True)) as db:
        if type(value) is not list:
            db[key] = [value]
        else:
            db[key] = value


def get(table, key):

    filename = get_db_filename(key)
    with closing(SqliteDict(filename, autocommit=True)) as db:
        _check_valid_key(key, db)
        print(db[key])


def _check_valid_key(key, db):

    if not isinstance(key, str):
        raise ValueError('%r is not a valid key type' % key)
    if key not in db:
        raise ValueError('%r could not be found' % key)


def get_db_filename(key):
    return f'./my_db{hash(key) % 33}.sqlite'


# put('try13', 'omg let it be')
# put('try14', 'omg let it be')
# put('try17', ['omg let it be', 'omg let it be one more time'])
# filename = get_db_filename('try17')
# print(filename)
keys = []
# for i in range(100000):
#     if hash(f'try{i}') % 33 == 8:
#         #print(f'try{i}')
#         keys.append(f'try{i}')
#         put(f'try{i}', 'one more cell')
#
#
# with closing(SqliteDict('./my_db8.sqlite', autocommit=True)) as db:
#     for key in keys:
#         get(db, key)