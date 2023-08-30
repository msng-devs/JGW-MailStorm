import sys
import src.model.template as template
from prettytable import PrettyTable
from src.helpers.log import setup_logging
import src.model.history as history
setup_logging()


def print_help():
    print("\nusage: [cmd] [args] \n")
    print("The following commands are available: \n")
    print("[show] [count] : show mail templates")
    print("[history] [count] : show mail history")
    print("[refresh] : refresh mail template")
    print("[help] or [?] : show this help message")
    print("[exit] : exit program")
    print("\n")


def run_cmd(cmd, args):
    if cmd == "help" or cmd == "?":
        print_help()


    elif cmd == "show":
        cnt = args

        if cnt is None:
            cnt = 10

        result = template.getAll(cnt)

        if result is None or len(result) == 0:
            print("Not found mail template")
            return

        table = PrettyTable(["ID", "Name", "Args"])
        for row in result:
            table.add_row([row[0], row[1], row[2]])
        print(table)

    elif cmd == "history":
        cnt = args

        if cnt is None:
            cnt = 10

        result = history.getAll(cnt)

        if result is None or len(result) == 0:
            print("Not found mail history")
            return
        #run_date, service , status , template , subject, recipient ,arg, message
        table = PrettyTable(["Date", "Service", "Status", "Template", "Subject", "Recipient", "Arg", "Message"])

        for row in result:
            table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

        print(table)


    elif cmd == "refresh":
        result = template.refresh_template_list()
        if result:
            print("Success refresh template list")
        else:
            print("Failed refresh template list")

    elif cmd == "exit":
        print("Goodbye!")
        sys.exit(0)

    else:
        print("\nUnknown command: " + cmd)
        print_help()


def main():
    print("Welcome to mailstorm control system! Type 'help' or '?' to list commands. \n")
    while True:
        user_input = input("mailstorm> ")

        if user_input == "":
            continue

        split_input = user_input.split(" ")

        if len(split_input) == 1:
            run_cmd(split_input[0], None)
        else:
            run_cmd(split_input[0], split_input[1])


if __name__ == "__main__":
    main()
