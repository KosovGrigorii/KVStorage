from ConsoleComandsHandler import execute_command


def main():
    while True:
        command = input()
        if command is None or command == "exit":
            break
        execute_command(command.split(':'))


if __name__ == '__main__':
    main()
