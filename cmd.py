import sys
import src.model.template as template
from prettytable import PrettyTable
from src.helpers.log import setup_logging
import src.model.history as history

setup_logging()


def truncate_string(input_string, max_length, truncation_indicator="..."):
    if len(input_string) <= max_length:
        return input_string
    else:
        return input_string[:max_length - len(truncation_indicator)] + truncation_indicator


def print_help():
    print("\nusage: [cmd] [args] \n")
    print("The following commands are available: \n")
    print("[show] [count] : show mail templates")
    print("[history] [count] : show mail history")
    print("[find] [id] : show mail history by id")
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

        result = history.get_all(cnt)

        if result is None or len(result) == 0:
            print("Not found mail history")
            return
        # run_date, service , status , template , subject, recipient ,arg, message
        table = PrettyTable(["ID", "Date", "Service", "Status", "Template", "Subject"])

        for row in result:
            table.add_row(
                [row[8], row[0], truncate_string(row[1], 8), truncate_string(row[2], 8), truncate_string(row[3], 8),
                 truncate_string(row[4], 8)])

        print(table)

    elif cmd == "find":
        if(args is None):
            print("If you want to find history, you must input id")
            print("[find] [id] : show mail history by id")
        id = args
        result = history.get_by_id(id)
        # id,run_date, service , status , template , subject, recipient ,arg, message
        print("ID: " + str(result[0]))
        print("Date: " + str(result[1]))
        print("Service: " + str(result[2]))
        print("Status: " + str(result[3]))
        print("Template: " + str(result[4]))
        print("Subject: " + str(result[5]))
        print("Recipient: " + str(result[6]))
        print("Arg: " + str(result[7]))
        print("Message: " + str(result[8]))

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
