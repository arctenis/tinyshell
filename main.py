import os
import subprocess
import sys


builtin_commands = ["exit", "echo", "type", "cd"]


def command_not_found(command):
    sys.stdout.write(f"{command}: command not found\n")


def cd_command(args):
    if not args:
        new_path = os.path.expanduser("~")
    else:
        new_path = args[0]
    new_path = os.path.expanduser(new_path)

    if not os.path.isabs(new_path):
        new_path = os.path.join(os.getcwd(), new_path)

    try:
        os.chdir(new_path)
    except FileNotFoundError:
        print(f"No such directory: {new_path}")
    except NotADirectoryError:
        print(f"Not a directory: {new_path}")
    except PermissionError:
        print(f"Permission denied: {new_path}")


def exit_command(args):
    exit_code = int(args[0]) if args else 0
    return exit_code


def echo_command(args):
    print(" ".join(args))


def get_paths():
    path = os.getenv("PATH")
    paths = path.split(":") if path else []
    return paths


def command_exists(command):
    paths = get_paths()
    for p in paths:
        if os.path.exists(f"{p}/{command}"):
            return True
    if command in builtin_commands:
        return True
    return False


def current_directory():
    return os.getcwd()


def type_command(args):
    if len(args) != 1:
        sys.stdout.write("type: too many arguments\n")
        return
    command = args[0]

    if command in builtin_commands:
        sys.stdout.write(f"{command} is a shell builtin\n")
        return

    if command_exists(command):
        paths = get_paths()
        for p in paths:
            if os.path.exists(f"{p}/{command}"):
                sys.stdout.write(f"{command} is {p}/{command}\n")
                sys.stdout.flush()
                return
    sys.stdout.write(f"{args[0]} not found\n")
    sys.stdout.flush()


def run_command(cmd_args):
    if not cmd_args:
        return
    cmd, *args = cmd_args

    if not command_exists(cmd):
        command_not_found(cmd)
        return

    if cmd in builtin_commands:
        if cmd == "exit":
            exit_code = exit_command(args)
            if exit_code == 0:
                sys.exit()
            else:
                print(f"exit: {exit_code}")
                print("exit: can only have 0 as an argument")
        if cmd == "echo":
            echo_command(args)
        if cmd == "type":
            type_command(args)
        if cmd == "cd":
            cd_command(args)
    else:
        try:
            subprocess.run(cmd_args)
        except FileNotFoundError:
            command_not_found(cmd)


def main():
    while True:
        sys.stdout.write(f"{current_directory()} $ ")
        sys.stdout.flush()
        command = input().strip().split()
        run_command(command)



main()
