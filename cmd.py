import sys


def print_help():
    print("usage: [cmd] [args]")
    print("The following commands are available:")
    print("[show] : show all mail template")
    print("[history] [count] : show mail history")
    print("[refresh] : refresh mail template")
    print("[help] or [?] : show this help message")


def run_cmd(cmd, args):
    if cmd == "help" or cmd == "?":
        print_help()
        sys.exit(0)

    elif cmd == "show":
        # TODO: show all mail template
        sys.exit(0)

    elif cmd == "history":
        # TODO: show mail history
        sys.exit(0)

    elif cmd == "refresh":
        # TODO: refresh mail template
        sys.exit(0)


def main():
    print("Welcome to mailstorm control system! Type 'help' or '?' to list commands.")
    while True:
        user_input = input("mailstorm> ")


if __name__ == "__main__":
    main()
