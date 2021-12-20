from HashTable import HashTable
from storageCleaner import empty_storage

HELP_TEXT = {"help": "show all possible commands and what each one suppose to do",
             "h": "does the same thing as help",
             "get": "returns a value using this key\nFormat: get <key>",
             "put": "adding key value pair to a storage\nFormat: put <key>:<value>",
             "help <command>": "shows command usage",
             "exit": "exits the program",
             "clear": "irrevocably clears your storage, BE CAREFUL"}


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
        storage = HashTable("output.txt")
        storage.get(key)

    elif command.startswith("put"):
        try:
            key = command.split(' ')[1]
            value = command_components[1]
            storage = HashTable("output.txt")
            storage.put(key, value)
            parsed_value = value.split('/')
            print(f"Pair {key}: {parsed_value[len(parsed_value) - 1]} is added to the storage")

        except:
            print("Incorrect format. Check format by typing help or h")

    elif command.startswith("put"):
        print("You sure you want to clear your storage?\nPress A for yes, anything else for no")
        answer = input()
        if answer.lower()  == "a":
            empty_storage()

    elif command.startswith("help"):

        command_to_describe = None
        command_components = command_components[0].split(' ')
        if len(command_components) == 2:
            command_to_describe = command_components[1]
        print_help(command_to_describe)

    elif command == "h":
        print_help()

    else:
        print("command is written in a wrong format\nCheck all formats by typing help or h")