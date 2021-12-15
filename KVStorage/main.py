
#import shelve
from contextlib import closing
from sqlitedict import SqliteDict

HELP_TEXT = {"help": "show all possible commands and what each one suppose to do",
             "h": "does the same thing as help",
             "get": "returns a value using this key\nFormat: get <key>",
             "put": "adding key value pair to a storage\nFormat: put <key>:<value>",
             "help <command>": "shows command usage",
             "exit": "exits the program"}


# try:
#     key = command.split(' ')[1]
#     value = command_components[1]
#     put(key, value)
#     print(f"Pair {key}: {value} is added to the storage")
# except Exception:
#
#     print("Incorrect format. Check format by typing help or h")


# def put(key, file_name):
#     with shelve.open('storage') as storage:
#         storage[key] = []
#         with open(file_name) as f:
#             storage[key] = f.readlines()
#
#
# def get(key, file_name):
#     with shelve.open('storage') as storage:
#         with open(file_name, 'w') as f:
#             f.write(*storage[key])


def put(key, file_name):

    with closing(SqliteDict('./my_db1.sqlite', tablename='filenames', autocommit=True)) as db:
        db[key] = file_name

    with closing(SqliteDict('./my_db1.sqlite', tablename='values', autocommit=True)) as db:
        db[key] = []
        with open(file_name) as f:
            db[key] = f.readlines()


def get(key):

    file_name = ""
    with closing(SqliteDict('./my_db1.sqlite', tablename='filenames', autocommit=True)) as db:
        if check_valid_key(key, db):
            file_name = db[key]
        else:
            return

    with closing(SqliteDict('./my_db1.sqlite', tablename='values', autocommit=True)) as db:
        if check_valid_key(key, db):
            with open(file_name, 'w') as f:
                f.writelines(db[key])
                print(f)


def check_valid_key(key, db):

    if not isinstance(key, str):
        print('key %r is not a valid key type' % key)
        return False

    if key not in db:
        print('key %r could not be found' % key)
        return False

    return True


# def get_db_filename(key):
#     return f'./my_db{hash(key) % 33}.sqlite'


def print_help(command=None):
    if command is not None:
        print(HELP_TEXT[command])
    else:
        print("DOCUMENTATION\n--------------------------")
        for key, value in HELP_TEXT.items():
            print(f"{key}: {value}")
            print()


def execute_command(command_components):
    command = command_components[0]
    if command.startswith("get"):
        key = command.split(' ')[1]
        get(key)

    elif command.startswith("put"):
        try:
            key = command.split(' ')[1]
            value = command_components[1]
            put(key, value)
            parsed_value = value.split('/')
            print(f"Pair {key}: {parsed_value[len(parsed_value) - 1]} is added to the storage")

        except Exception as exep:
            print(exep)
            print("Incorrect format. Check format by typing help or h")

    elif command == "help":

        command_to_describe = None
        if len(command_components[0].split(' ')) == 2:
            command_to_describe = command_components[1]
        print_help(command_to_describe)

    elif command == "h":
        print_help()


def main():
    while True:
        command = input()
        if command is None or command == "exit":
            break
        execute_command(command.split(':'))


if __name__ == '__main__':
    main()
