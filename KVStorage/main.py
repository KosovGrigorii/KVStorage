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


def _check_valid_key(key, db):

    if not isinstance(key, str):
        raise ValueError('%r is not a valid key type' % key)
    if key not in db:
        raise ValueError('%r could not be found' % key)


def get_db_filename(key):
    return f'./my_db{hash(key) % 33}.sqlite'
